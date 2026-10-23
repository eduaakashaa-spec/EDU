"""FutureReady routes. Every student-scoped route starts with `profile_or_403`; templates only decide what to *show*, never what is *allowed*."""
import csv
import io
import json
from datetime import date, datetime, timedelta

from flask import Blueprint, Response, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from app.decorators import admin_required, staff_required
from app.extensions import db
from app.futureready import access, engine, reco, reports
from app.futureready.access import STAFF, audit, login_needed, my_profiles, notify, profile_or_403
from app.futureready.models import (FrAction, FrAdmission, FrAssessment, FrAttempt, FrAudit, FrBadge, FrBranch, FrGoal, FrNote, FrNotice, FrParentLink,
                                    FrProfile, FrProject, FrQuestion, FrRecommendation, FrReport, FrResource, FrSession, FrShortlist, FrSkillScore, FrWindow,
                                    _now, jl)

fr_bp = Blueprint('futureready', __name__, url_prefix='/futureready')

STEPS = [(1, 'Welcome'), (2, 'About the student'), (3, 'Parent consent'), (4, 'Interests'), (5, 'How I learn'), (6, 'My goals'),
         (7, 'Parent goals'), (8, 'Programme'), (9, 'Baseline plan'), (10, 'Review')]
LEARNING_PREFS = ['Reading and writing', 'Watching videos', 'Hands-on projects', 'Discussing with others', 'Practice questions', 'Drawing and diagrams']
CURRICULA = ['CBSE', 'ICSE / ISC', 'State board', 'IB', 'Cambridge (IGCSE)', 'Other']
TIERS = {'Essential': 1, 'Standard': 2, 'Intensive': 4}   # label -> live meetings per month; configurable per student by staff
BADGES = {'first_assessment': 'First assessment completed', 'five_assessments': 'Five assessments completed', 'all_core': 'All core assessments completed',
          'first_action': 'First action completed', 'five_actions': 'Five actions completed', 'project_done': 'Project completed', 'sampler_5': 'Five sampler sets practised'}


def _d(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date() if s else None
    except ValueError:
        return None


def _page(tpl, p=None, role=None, **ctx):
    notices = []
    if current_user.is_authenticated:
        notices = FrNotice.query.filter_by(user_id=current_user.id, read=False).order_by(FrNotice.id.desc()).limit(5).all()
    return render_template(tpl, p=p, role=role, is_staff=role in STAFF, notices=notices, STEPS=STEPS, **ctx)


def _award(p):
    have = {b.key for b in FrBadge.query.filter_by(profile_id=p.id).all()}
    n_att = FrAttempt.query.filter_by(profile_id=p.id, status='submitted', audience='student').join(FrAssessment).filter(FrAssessment.group != 'sampler').count()
    core = FrAssessment.query.filter(FrAssessment.group.in_(['core', 'engineering', 'entrance']), FrAssessment.active == True, FrAssessment.number != None).count()  # noqa
    done_keys = {a.assessment.key for a in FrAttempt.query.filter_by(profile_id=p.id, status='submitted', audience='student').all()}
    keys = {a.key for a in FrAssessment.query.filter(FrAssessment.group.in_(['core', 'engineering', 'entrance']), FrAssessment.number != None).all()}  # noqa
    acts = FrAction.query.filter_by(profile_id=p.id, status='Done').count()
    s = FrAttempt.query.filter_by(profile_id=p.id, status='submitted').join(FrAssessment).filter(FrAssessment.group == 'sampler').count()
    want = []
    if n_att >= 1: want.append('first_assessment')
    if n_att >= 5: want.append('five_assessments')
    if keys and keys <= done_keys: want.append('all_core')
    if acts >= 1: want.append('first_action')
    if acts >= 5: want.append('five_actions')
    if FrProject.query.filter_by(profile_id=p.id, status='Completed').count(): want.append('project_done')
    if s >= 5: want.append('sampler_5')
    for k in want:
        if k not in have:
            db.session.add(FrBadge(profile_id=p.id, key=k))
    db.session.commit()


# ---- entry ----------------------------------------------------------------------------------------------------------------
@fr_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('futureready/public.html', STEPS=STEPS, p=None, role=None, is_staff=False, notices=[])
    rows = my_profiles()
    if len(rows) == 1 and not current_user.is_admin and not current_user.is_ea_mentor:
        return redirect(url_for('futureready.dashboard', pid=rows[0][0].id))
    return _page('futureready/index.html', rows=rows, can_admin=current_user.is_admin)


@fr_bp.route('/privacy')
def privacy():
    return _page('futureready/privacy.html')


@fr_bp.route('/s/<int:pid>')
@login_needed
def dashboard(pid):
    p, role = profile_or_403(pid)
    if not p.onboarding_done_at and role in ('student', 'parent'):
        return redirect(url_for('futureready.onboarding', pid=pid, step=p.onboarding_step or 1))
    rows = reports._assessment_status(p)
    done = sum(1 for r in rows if r['done'])
    acts = FrAction.query.filter_by(profile_id=p.id).all()
    open_acts = [a for a in acts if a.status in ('Not started', 'In progress')]
    sess = FrSession.query.filter_by(profile_id=p.id).filter(FrSession.status == 'Planned').order_by(FrSession.planned_at).first()
    flags = []
    if role in STAFF:
        needs_rubric = [a for a in FrAttempt.query.filter_by(profile_id=p.id, status='submitted').join(FrAssessment).filter(FrAssessment.kind == 'rubric').all() if not a.rubric]
        if needs_rubric:
            flags.append(('Practical task awaiting your rubric rating', url_for('futureready.result', pid=pid, aid=needs_rubric[0].id)))
        pending = FrRecommendation.query.filter_by(profile_id=p.id, approved=False).filter(FrRecommendation.status != 'Dismissed').count()
        if pending:
            flags.append((f'{pending} recommendation(s) awaiting your review', url_for('futureready.recs', pid=pid)))
        late = [a for a in open_acts if a.due_date and a.due_date < date.today()]
        if late:
            flags.append((f'{len(late)} overdue action(s)', url_for('futureready.plan', pid=pid)))
        if not p.consent_at:
            flags.append(('Parent consent not recorded: assessments are locked', url_for('futureready.onboarding', pid=pid, step=3)))
    badges = [(b.key, BADGES.get(b.key, b.key)) for b in FrBadge.query.filter_by(profile_id=p.id).all()]
    return _page('futureready/dashboard.html', p, role, rows=rows, done=done, total=len(rows), acts=acts, open_acts=open_acts[:5], sess=sess, flags=flags, badges=badges,
                 branches=engine.branch_matches(p.id, 3), goals=FrGoal.query.filter_by(profile_id=p.id, status='Active').all(),
                 recs_n=len(reco.visible_to_family(p.id)), today=date.today())


@fr_bp.route('/notices/read', methods=['POST'])
@login_needed
def notices_read():
    FrNotice.query.filter_by(user_id=current_user.id, read=False).update({'read': True})
    db.session.commit()
    return redirect(request.referrer or url_for('futureready.index'))


# ---- onboarding -----------------------------------------------------------------------------------------------------------
@fr_bp.route('/s/<int:pid>/onboarding/<int:step>', methods=['GET', 'POST'])
@login_needed
def onboarding(pid, step):
    p, role = profile_or_403(pid)
    step = max(1, min(10, step))
    if request.method == 'POST':
        f = request.form
        err = None
        if step == 2:
            p.grade = 9 if f.get('grade') == '9' else 8
            p.curriculum = f.get('curriculum', '')[:40]
            p.school = f.get('school', '')[:160]
        elif step == 3:
            if role not in ('parent', 'admin', 'mentor'):
                err = 'A parent or guardian must record consent. Ask them to sign in, or ask your mentor to record it after speaking with them.'
            elif not f.get('agree') or not f.get('by', '').strip():
                err = 'Please tick the box and type the parent or guardian’s full name.'
            else:
                p.consent_at = _now()
                p.consent_by = f['by'].strip()[:160] + (' (recorded by ' + role + ')' if role != 'parent' else '')
                audit('consent_recorded', p, p.consent_by, role)
        elif step == 4:
            p.interests_text = f.get('interests', '')[:2000]
        elif step == 5:
            p.learning_prefs = ', '.join(x for x in f.getlist('prefs') if x in LEARNING_PREFS)
        elif step == 6:
            p.student_goals = f.get('goals', '')[:2000]
        elif step == 7:
            if role in ('parent', 'admin', 'mentor'):
                p.parent_goals = f.get('goals', '')[:2000]
        elif step == 8:
            if role in STAFF:
                p.tier = f.get('tier') if f.get('tier') in TIERS else 'Standard'
                try:
                    p.meetings_per_month = max(1, min(8, int(f.get('meetings') or TIERS[p.tier])))
                except ValueError:
                    p.meetings_per_month = TIERS[p.tier]
        if err:
            flash(err, 'error')
            return redirect(url_for('futureready.onboarding', pid=pid, step=step))
        if step == 10:
            if not p.consent_at:
                flash('Parent consent is still needed before finishing.', 'error')
                return redirect(url_for('futureready.onboarding', pid=pid, step=3))
            p.onboarding_done_at = _now()
            notify(p.mentor_id, f'{p.student.name} finished onboarding', url_for('futureready.dashboard', pid=p.id), p.id)
            db.session.commit()
            return redirect(url_for('futureready.dashboard', pid=pid))
        p.onboarding_step = max(p.onboarding_step or 1, min(10, step + 1))
        db.session.commit()
        return redirect(url_for('futureready.onboarding', pid=pid, step=step + 1))
    return _page('futureready/onboarding.html', p, role, step=step, LEARNING_PREFS=LEARNING_PREFS, CURRICULA=CURRICULA, TIERS=TIERS,
                 prefs=[x.strip() for x in (p.learning_prefs or '').split(',') if x.strip()], plan=FrAssessment.query.filter(FrAssessment.group.in_(['core', 'engineering', 'entrance']), FrAssessment.number != None).order_by(FrAssessment.number).all())  # noqa


# ---- assessments ----------------------------------------------------------------------------------------------------------
def _can_take(p, role, a):
    if role == 'student' or (role == 'admin' and p.demo):
        return True
    if role == 'parent':
        return a.key == 'alignment'
    return False


@fr_bp.route('/s/<int:pid>/assessments')
@login_needed
def assessments(pid):
    p, role = profile_or_403(pid)
    items = []
    for a in FrAssessment.query.filter(FrAssessment.group.in_(['core', 'engineering', 'entrance']), FrAssessment.active == True).order_by(FrAssessment.position).all():  # noqa
        aud = 'parent' if role == 'parent' else 'student'
        at = engine.latest_attempt(p.id, a.key, aud, submitted=False)
        items.append(dict(a=a, at=at, last=engine.latest_attempt(p.id, a.key, aud), count=FrQuestion.query.filter_by(assessment_id=a.id, active=True).count(), can=_can_take(p, role, a)))
    return _page('futureready/assessments.html', p, role, items=items, locked=not access.consent_ok(p))


@fr_bp.route('/s/<int:pid>/a/<key>', methods=['GET', 'POST'])
@login_needed
def take(pid, key):
    p, role = profile_or_403(pid)
    a = FrAssessment.query.filter_by(key=key, active=True).first_or_404()
    if not _can_take(p, role, a):
        abort(403)
    if not access.consent_ok(p):
        flash('Parent or guardian consent is needed before assessments open.', 'error')
        return redirect(url_for('futureready.onboarding', pid=pid, step=3))
    aud = 'parent' if role == 'parent' else 'student'
    set_key = request.values.get('set') or None
    at = FrAttempt.query.filter_by(profile_id=p.id, assessment_id=a.id, audience=aud, status='in_progress', set_key=set_key).order_by(FrAttempt.id.desc()).first()
    if not at:
        n = FrAttempt.query.filter_by(profile_id=p.id, assessment_id=a.id, audience=aud, set_key=set_key).count()
        at = FrAttempt(profile_id=p.id, assessment_id=a.id, audience=aud, set_key=set_key, attempt_no=n + 1, version=a.version, responses_json='{}')
        db.session.add(at)
        db.session.commit()
    qs = engine.questions_for(at)
    if request.method == 'POST':
        resp = at.responses
        for q in qs:
            if q.qtype == 'multi':
                vals = request.form.getlist(q.code)
                resp[q.code] = [int(v) for v in vals if v.isdigit()]
            else:
                v = request.form.get(q.code, '').strip()
                if v != '':
                    resp[q.code] = int(v) if q.qtype in ('mcq', 'likert', 'choice') and v.isdigit() else v
                else:
                    resp.pop(q.code, None)
        at.responses_json = json.dumps(resp)
        if request.form.get('action') == 'submit':
            if not resp:
                flash('Please answer at least one question.', 'error')
                return redirect(request.url)
            at.status = 'submitted'
            at.submitted_at = _now()
            engine.score_attempt(at)
            db.session.commit()
            _award(p)
            notify(p.mentor_id, f'{p.student.name} submitted “{a.title}”', url_for('futureready.result', pid=p.id, aid=at.id), p.id)
            db.session.commit()
            audit('attempt_submitted', p, a.key, role)
            return redirect(url_for('futureready.result', pid=pid, aid=at.id))
        db.session.commit()
        flash('Progress saved. You can continue later.', 'ok')
        return redirect(request.url)
    return _page('futureready/take.html', p, role, a=a, at=at, qs=qs, resp=at.responses, set_key=set_key)


@fr_bp.route('/s/<int:pid>/a/<key>/save', methods=['POST'])
@login_needed
def autosave(pid, key):
    """Background save while answering (so a lost connection does not lose work)."""
    p, role = profile_or_403(pid)
    a = FrAssessment.query.filter_by(key=key).first_or_404()
    if not _can_take(p, role, a):
        abort(403)
    aud = 'parent' if role == 'parent' else 'student'
    at = FrAttempt.query.filter_by(profile_id=p.id, assessment_id=a.id, audience=aud, status='in_progress', set_key=request.args.get('set') or None).order_by(FrAttempt.id.desc()).first()
    if not at:
        return jsonify(ok=False), 404
    data = request.get_json(silent=True) or {}
    resp = at.responses
    valid = {q.code: q for q in engine.questions_for(at)}
    for code, v in data.items():
        if code in valid:
            if v in (None, '', []):
                resp.pop(code, None)
            else:
                resp[code] = v
    at.responses_json = json.dumps(resp)
    db.session.commit()
    return jsonify(ok=True, n=len(resp))


@fr_bp.route('/s/<int:pid>/attempt/<int:aid>')
@login_needed
def result(pid, aid):
    p, role = profile_or_403(pid)
    at = db.session.get(FrAttempt, aid)
    if not at or at.profile_id != p.id:
        abort(404)
    if role == 'parent' and at.audience == 'student' and at.assessment.key == 'alignment':
        abort(403)   # the parent sees their own alignment answers, and the shared comparison once both are done
    r = at.result
    if role == 'parent':
        r = dict(r)
        r['text'] = {}
    meta = engine.rubric_meta(at.assessment.key) if at.assessment.kind == 'rubric' else {}
    return _page('futureready/result.html', p, role, at=at, r=r, meta=meta, label=engine.label, align=reports.alignment(p) if at.assessment.key == 'alignment' else None)


@fr_bp.route('/s/<int:pid>/attempt/<int:aid>/rubric', methods=['POST'])
@login_needed
def rubric(pid, aid):
    p, role = profile_or_403(pid, STAFF)
    at = db.session.get(FrAttempt, aid)
    if not at or at.profile_id != p.id or at.assessment.kind != 'rubric':
        abort(404)
    data = dict(request.form)
    ratings = {k: data.get(k) for k in [c for c, _ in engine.rubric_meta(at.assessment.key).get('criteria', [])]}
    ratings['feedback'] = request.form.get('feedback', '')[:1500]
    engine.rate_rubric(at, ratings)
    db.session.commit()
    notify(p.user_id, 'Your mentor reviewed your practical task', url_for('futureready.result', pid=p.id, aid=at.id), p.id)
    db.session.commit()
    audit('rubric_rated', p, at.assessment.key, role)
    flash('Rubric saved.', 'ok')
    return redirect(url_for('futureready.result', pid=pid, aid=aid))


@fr_bp.route('/s/<int:pid>/sampler')
@login_needed
def sampler(pid):
    p, role = profile_or_403(pid)
    from app.futureready.content.extra import SAMPLER_SKILLS
    s = FrAssessment.query.filter_by(key='sampler').first_or_404()
    done = {}
    for at in FrAttempt.query.filter_by(profile_id=p.id, assessment_id=s.id, status='submitted').order_by(FrAttempt.id).all():
        done[at.set_key] = at.result.get('overall_pct')
    return _page('futureready/sampler.html', p, role, skills=SAMPLER_SKILLS, done=done, can=_can_take(p, role, s), locked=not access.consent_ok(p))


# ---- engineering exploration ---------------------------------------------------------------------------------------------------
@fr_bp.route('/branches')
@login_needed
def branches():
    fam = {}
    for b in FrBranch.query.filter_by(active=True).order_by(FrBranch.position).all():
        fam.setdefault(b.family, []).append(b)
    pid = request.args.get('pid', type=int)
    p, role, sl = None, None, set()
    if pid:
        p, role = profile_or_403(pid)
        sl = {s.branch_id for s in FrShortlist.query.filter_by(profile_id=p.id).all()}
    return _page('futureready/branches.html', p, role, fam=fam, shortlist=sl)


@fr_bp.route('/branches/<key>')
@login_needed
def branch(key):
    b = FrBranch.query.filter_by(key=key, active=True).first_or_404()
    pid = request.args.get('pid', type=int)
    p, role, on = None, None, False
    if pid:
        p, role = profile_or_403(pid)
        on = bool(FrShortlist.query.filter_by(profile_id=p.id, branch_id=b.id).first())
    rel = FrBranch.query.filter(FrBranch.key.in_((b.related or '').split(','))).all()
    return _page('futureready/branch.html', p, role, b=b, rel=rel, on=on, tags=jl(b.tags_json, {}), label=engine.label)


@fr_bp.route('/branches/compare')
@login_needed
def compare():
    keys = [k for k in request.args.getlist('k') if k][:3]
    items = FrBranch.query.filter(FrBranch.key.in_(keys)).all() if keys else []
    allb = FrBranch.query.filter_by(active=True).order_by(FrBranch.position).all()
    pid = request.args.get('pid', type=int)
    p, role = (profile_or_403(pid) if pid else (None, None))
    return _page('futureready/compare.html', p, role, items=items, allb=allb, keys=keys)


@fr_bp.route('/s/<int:pid>/shortlist/<key>', methods=['POST'])
@login_needed
def shortlist(pid, key):
    p, role = profile_or_403(pid)
    if role not in ('student', 'admin'):
        abort(403)
    b = FrBranch.query.filter_by(key=key).first_or_404()
    row = FrShortlist.query.filter_by(profile_id=p.id, branch_id=b.id).first()
    if row:
        db.session.delete(row)
    else:
        db.session.add(FrShortlist(profile_id=p.id, branch_id=b.id, note=request.form.get('note', '')[:400]))
    db.session.commit()
    return redirect(request.referrer or url_for('futureready.branches', pid=pid))


@fr_bp.route('/s/<int:pid>/interest-map')
@login_needed
def interest_map(pid):
    p, role = profile_or_403(pid)
    prof = engine.interest_profile(p.id)
    return _page('futureready/interest_map.html', p, role, prof=[(k, engine.label(k), v) for k, v in prof.items()], matches=engine.branch_matches(p.id, 6),
                 shortlist=FrShortlist.query.filter_by(profile_id=p.id).all())


@fr_bp.route('/admissions')
def admissions():
    rows = FrAdmission.query.filter_by(active=True).order_by(FrAdmission.position).all()
    return render_template('futureready/admissions.html', rows=rows, p=None, role=None, is_staff=False, notices=[], STEPS=STEPS, today=date.today())


@fr_bp.route('/foundations')
@login_needed
def foundations():
    res = {r.key: r for r in FrResource.query.all()}
    return _page('futureready/foundations.html', items=engine.foundations(), res=res)


# ---- recommendations / plan -----------------------------------------------------------------------------------------------------
@fr_bp.route('/s/<int:pid>/recommendations', methods=['GET', 'POST'])
@login_needed
def recs(pid):
    p, role = profile_or_403(pid)
    if request.method == 'POST':
        act = request.form.get('do')
        if act == 'generate' and role in STAFF:
            made = reco.generate(p)
            flash(f'{len(made)} new suggestion(s) created. Review them before the family sees them.', 'ok')
        elif act in ('approve', 'dismiss', 'edit') and role in STAFF:
            r = db.session.get(FrRecommendation, request.form.get('rid', type=int))
            if r and r.profile_id == p.id:
                if act == 'approve':
                    r.approved = True
                    notify(p.user_id, 'New suggestions from your mentor', url_for('futureready.recs', pid=p.id), p.id)
                elif act == 'dismiss':
                    r.status = 'Dismissed'
                else:
                    r.why = request.form.get('why', r.why)[:1000]
        elif act == 'accept' and role in ('student', 'admin'):
            r = db.session.get(FrRecommendation, request.form.get('rid', type=int))
            if r and r.profile_id == p.id and r.approved and r.status == 'Suggested':
                reco.accept_as_action(r, p)
                flash('Added to your action plan.', 'ok')
        db.session.commit()
        return redirect(url_for('futureready.recs', pid=pid))
    items = FrRecommendation.query.filter_by(profile_id=p.id).order_by(FrRecommendation.id.desc()).all() if role in STAFF else reco.visible_to_family(p.id)
    for r in items:
        r.ev = jl(r.evidence_json, {})
    return _page('futureready/recs.html', p, role, items=items)


@fr_bp.route('/s/<int:pid>/plan', methods=['GET', 'POST'])
@login_needed
def plan(pid):
    p, role = profile_or_403(pid)
    if request.method == 'POST':
        f = request.form
        do = f.get('do')
        if do == 'goal' and role in STAFF + ('student', 'parent'):
            db.session.add(FrGoal(profile_id=p.id, title=f.get('title', '')[:200], metric=f.get('metric', '')[:120], due_date=_d(f.get('due')),
                                  baseline=f.get('baseline', type=float), target=f.get('target', type=float), current=f.get('baseline', type=float), unit=f.get('unit', '')[:30],
                                  set_by='mentor' if role in STAFF else role))
        elif do == 'goal_update':
            g = db.session.get(FrGoal, f.get('gid', type=int))
            if g and g.profile_id == p.id and role in STAFF:
                g.current = f.get('current', type=float)
                g.status = f.get('status') if f.get('status') in ('Active', 'Achieved', 'Revised', 'Dropped') else g.status
        elif do == 'action' and f.get('title', '').strip():
            owner = f.get('owner') if f.get('owner') in ('student', 'parent', 'mentor') else 'student'
            if role == 'student':
                owner = 'student'
            if role == 'parent':
                owner = 'parent'
            db.session.add(FrAction(profile_id=p.id, title=f['title'][:240], detail=f.get('detail', '')[:1000], owner=owner, due_date=_d(f.get('due')), why=f.get('why', '')[:300],
                                    source='mentor' if role in STAFF else 'student', goal_id=f.get('goal_id', type=int) or None))
            if role in STAFF and owner != 'mentor':
                notify(p.user_id, 'New action from your mentor: ' + f['title'][:80], url_for('futureready.plan', pid=p.id), p.id)
        elif do == 'action_update':
            a = db.session.get(FrAction, f.get('aid', type=int))
            if a and a.profile_id == p.id:
                mine = (a.owner == role) or (role == 'student' and a.owner == 'student') or role in STAFF
                if mine:
                    st = f.get('status')
                    if st in ('Not started', 'In progress', 'Done', 'Skipped'):
                        a.status = st
                        a.completed_at = _now() if st == 'Done' else None
                    a.evidence = f.get('evidence', a.evidence or '')[:2000]
                    a.reflection = f.get('reflection', a.reflection or '')[:2000]
                if role in STAFF and f.get('feedback'):
                    a.mentor_feedback = f['feedback'][:1500]
                    notify(p.user_id, 'Mentor feedback on: ' + a.title[:80], url_for('futureready.plan', pid=p.id), p.id)
        elif do == 'project' and f.get('title', '').strip() and role in ('student', 'admin') + ('mentor',):
            db.session.add(FrProject(profile_id=p.id, title=f['title'][:200], description=f.get('description', '')[:2000]))
        elif do == 'project_update':
            pr = db.session.get(FrProject, f.get('prid', type=int))
            if pr and pr.profile_id == p.id:
                if role in ('student', 'admin'):
                    pr.status = f.get('status') if f.get('status') in ('Planned', 'In progress', 'Completed') else pr.status
                    pr.evidence_url = f.get('url', pr.evidence_url or '')[:400]
                    pr.reflection = f.get('reflection', pr.reflection or '')[:2000]
                if role in STAFF and f.get('feedback'):
                    pr.mentor_feedback = f['feedback'][:1500]
        db.session.commit()
        _award(p)
        return redirect(url_for('futureready.plan', pid=pid))
    acts = FrAction.query.filter_by(profile_id=p.id).order_by(FrAction.status.in_(['Done', 'Skipped']), FrAction.due_date).all()
    return _page('futureready/plan.html', p, role, acts=acts, goals=FrGoal.query.filter_by(profile_id=p.id).all(), projects=FrProject.query.filter_by(profile_id=p.id).all(),
                 today=date.today(), res={r.key: r for r in FrResource.query.all()})


# ---- mentor workspace: notes + sessions -------------------------------------------------------------------------------------------
@fr_bp.route('/s/<int:pid>/mentor', methods=['GET', 'POST'])
@login_needed
def mentor_space(pid):
    p, role = profile_or_403(pid)
    if request.method == 'POST':
        f = request.form
        do = f.get('do')
        if do == 'note':
            body = f.get('body', '').strip()
            if role in STAFF and body:
                vis = 'shared' if f.get('visibility') == 'shared' else 'mentor'
                db.session.add(FrNote(profile_id=p.id, author_id=current_user.id, kind=f.get('kind', 'observation')[:14], basis=f.get('basis', 'mentor')[:16] if f.get('basis') in ('self_report', 'parent', 'assessment', 'mentor') else 'mentor', visibility=vis, body=body[:4000]))
                if vis == 'shared':
                    notify(p.user_id, 'Your mentor shared a note', url_for('futureready.mentor_space', pid=p.id), p.id)
            elif role == 'parent' and body:
                db.session.add(FrNote(profile_id=p.id, author_id=current_user.id, kind='parent', basis='parent', visibility='mentor', body=body[:4000]))
                notify(p.mentor_id, 'Parent sent a note about ' + (p.student.name or ''), url_for('futureready.mentor_space', pid=p.id), p.id)
        elif do == 'session' and role in STAFF:
            when = f.get('when')
            try:
                dt = datetime.strptime(when, '%Y-%m-%dT%H:%M') if when else None
            except ValueError:
                dt = None
            db.session.add(FrSession(profile_id=p.id, kind=f.get('kind', 'monthly')[:14], title=f.get('title', '')[:200], planned_at=dt, agenda=f.get('agenda', '')[:2000]))
            notify(p.user_id, 'A mentoring session was scheduled', url_for('futureready.mentor_space', pid=p.id), p.id)
        elif do == 'session_update' and role in STAFF:
            s = db.session.get(FrSession, f.get('sid', type=int))
            if s and s.profile_id == p.id:
                s.status = f.get('status') if f.get('status') in ('Planned', 'Held', 'Missed', 'Cancelled') else s.status
                s.summary = f.get('summary', s.summary or '')[:3000]
                if s.status == 'Held' and not s.held_at:
                    s.held_at = _now()
        elif do == 'assign' and role == 'admin':
            from app.models import User
            u = User.query.filter_by(email=f.get('email', '').strip().lower()).first()
            if u and u.is_ea_mentor:
                p.mentor_id = u.id
            else:
                flash('No staff mentor account with that email.', 'error')
        db.session.commit()
        return redirect(url_for('futureready.mentor_space', pid=pid))
    q = FrNote.query.filter_by(profile_id=p.id)
    if role not in STAFF:
        q = q.filter_by(visibility='shared')
    return _page('futureready/mentor_space.html', p, role, notes=q.order_by(FrNote.id.desc()).all(), sessions=FrSession.query.filter_by(profile_id=p.id).order_by(FrSession.id.desc()).all(),
                 parent_notes=[n for n in FrNote.query.filter_by(profile_id=p.id, basis='parent').all()] if role == 'parent' else [])


# ---- reports --------------------------------------------------------------------------------------------------------------------
@fr_bp.route('/s/<int:pid>/reports', methods=['GET', 'POST'])
@login_needed
def report_list(pid):
    p, role = profile_or_403(pid)
    if request.method == 'POST':
        if role not in STAFF:
            abort(403)
        kind = request.form.get('kind')
        if kind in reports.KINDS:
            r = reports.save(p, kind, current_user)
            audit('report_created', p, kind, role)
            return redirect(url_for('futureready.report_view', pid=pid, rid=r.id))
    q = FrReport.query.filter_by(profile_id=p.id)
    if role not in STAFF:
        q = q.filter_by(status='Shared')
    return _page('futureready/reports.html', p, role, items=q.order_by(FrReport.id.desc()).all(), KINDS=reports.KINDS)


@fr_bp.route('/s/<int:pid>/reports/<int:rid>', methods=['GET', 'POST'])
@login_needed
def report_view(pid, rid):
    p, role = profile_or_403(pid)
    r = db.session.get(FrReport, rid)
    if not r or r.profile_id != p.id or (role not in STAFF and r.status != 'Shared'):
        abort(404)
    if request.method == 'POST' and role in STAFF:
        if request.form.get('do') == 'share':
            r.status = 'Shared'
            r.shared_at = _now()
            notify(p.user_id, 'A new report is ready: ' + r.title, url_for('futureready.report_view', pid=p.id, rid=r.id), p.id)
            for l in FrParentLink.query.filter_by(profile_id=p.id).all():
                notify(l.parent_id, 'A new report is ready: ' + r.title, url_for('futureready.report_view', pid=p.id, rid=r.id), p.id)
            audit('report_shared', p, r.kind, role)
        elif request.form.get('do') == 'unshare':
            r.status = 'Draft'
        db.session.commit()
        return redirect(request.url)
    return _page('futureready/report_view.html', p, role, r=r, d=r.data)


@fr_bp.route('/s/<int:pid>/reports/<int:rid>.pdf')
@login_needed
def report_pdf(pid, rid):
    p, role = profile_or_403(pid)
    r = db.session.get(FrReport, rid)
    if not r or r.profile_id != p.id or (role not in STAFF and r.status != 'Shared'):
        abort(404)
    audit('report_pdf', p, r.kind, role)
    return Response(reports.pdf(r), mimetype='application/pdf', headers={'Content-Disposition': f'inline; filename=futureready-{r.kind}-{p.id}.pdf'})


# ---- administration ---------------------------------------------------------------------------------------------------------------
@fr_bp.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_home():
    from app.models import User
    if request.method == 'POST':
        f = request.form
        do = f.get('do')
        if do == 'enrol':
            u = User.query.filter_by(email=f.get('student_email', '').strip().lower()).first()
            if not u:
                flash('That student must first register on the site with this email.', 'error')
            elif FrProfile.query.filter_by(user_id=u.id).first():
                flash('That student already has a FutureReady profile.', 'error')
            else:
                m = User.query.filter_by(email=f.get('mentor_email', '').strip().lower()).first()
                pr = FrProfile(user_id=u.id, mentor_id=m.id if m and m.is_ea_mentor else None, grade=9 if f.get('grade') == '9' else 8)
                db.session.add(pr)
                db.session.flush()
                pe = User.query.filter_by(email=f.get('parent_email', '').strip().lower()).first()
                if pe:
                    db.session.add(FrParentLink(profile_id=pr.id, parent_id=pe.id))
                db.session.commit()
                audit('profile_created', pr, u.email, 'admin')
                flash('Student enrolled.' + ('' if pe or not f.get('parent_email') else ' The parent email has no account yet: link them after they register.'), 'ok')
        elif do == 'link_parent':
            pr = db.session.get(FrProfile, f.get('pid', type=int))
            pe = User.query.filter_by(email=f.get('parent_email', '').strip().lower()).first()
            if pr and pe and not FrParentLink.query.filter_by(profile_id=pr.id, parent_id=pe.id).first():
                db.session.add(FrParentLink(profile_id=pr.id, parent_id=pe.id, relation=f.get('relation', 'Parent')[:40]))
                db.session.commit()
                audit('parent_linked', pr, pe.email, 'admin')
            else:
                flash('Could not link: check the parent email is registered.', 'error')
        elif do == 'seed':
            n = engine.seed_content()
            flash(f'Content loaded ({n} new assessment(s)). Existing edits were kept.', 'ok')
        elif do == 'demo':
            from app.futureready import demo
            info = demo.create_demo(current_user)
            flash(info, 'ok')
        elif do == 'delete_profile':
            pr = db.session.get(FrProfile, f.get('pid', type=int))
            if pr and f.get('confirm') == 'DELETE':
                audit('profile_deleted', pr, f'user_id={pr.user_id}', 'admin')
                db.session.delete(pr)
                db.session.commit()
                flash('Profile and all linked FutureReady records deleted.', 'ok')
            else:
                flash('Type DELETE to confirm.', 'error')
        return redirect(url_for('futureready.admin_home'))
    return render_template('futureready/admin.html', p=None, role='admin', is_staff=True, notices=[], STEPS=STEPS, profiles=FrProfile.query.order_by(FrProfile.id.desc()).all(),
                           assessments=FrAssessment.query.order_by(FrAssessment.position).all(), windows=FrWindow.query.order_by(FrWindow.id.desc()).limit(20).all(),
                           qcount={a.id: FrQuestion.query.filter_by(assessment_id=a.id, active=True).count() for a in FrAssessment.query.all()},
                           admissions=FrAdmission.query.order_by(FrAdmission.position).all(), branches=FrBranch.query.order_by(FrBranch.position).all(),
                           resources=FrResource.query.all(), audit=FrAudit.query.order_by(FrAudit.id.desc()).limit(40).all())


@fr_bp.route('/admin/question/<int:qid>', methods=['GET', 'POST'])
@admin_required
def admin_question(qid):
    q = db.session.get(FrQuestion, qid) or abort(404)
    if request.method == 'POST':
        f = request.form
        new = FrQuestion(assessment_id=q.assessment_id, code=q.code, version=(q.version or 1) + 1, position=q.position, qtype=q.qtype, prompt=f.get('prompt', q.prompt).strip(),
                         options_json=json.dumps([l.strip() for l in f.get('options', '').splitlines() if l.strip()]) if q.qtype in ('mcq', 'multi') else q.options_json,
                         answer_json=q.answer_json, explanation=f.get('explanation', ''), distractor_json=q.distractor_json, skill=q.skill, reverse=q.reverse, level=q.level,
                         grade_min=q.grade_min, grade_max=q.grade_max, meta_json=q.meta_json)
        if q.qtype == 'mcq' and f.get('answer', '').isdigit():
            new.answer_json = json.dumps(int(f['answer']))
        q.active = False   # old row stays so earlier attempts keep their wording
        db.session.add(new)
        a = q.assessment
        a.version = (a.version or 1) + 1
        a.review_date = date.today()
        db.session.commit()
        audit('question_versioned', None, f'{q.code} v{new.version}', 'admin')
        flash(f'Saved as version {new.version}. Earlier attempts keep the earlier wording.', 'ok')
        return redirect(url_for('futureready.admin_home') + '#content')
    return render_template('futureready/admin_question.html', q=q, p=None, role='admin', is_staff=True, notices=[], STEPS=STEPS)


@fr_bp.route('/admin/admission/<key>', methods=['POST'])
@admin_required
def admin_admission(key):
    a = FrAdmission.query.filter_by(key=key).first_or_404()
    f = request.form
    for fld in ('summary', 'how_it_works', 'eligibility', 'admission_year', 'official_url', 'reviewer'):
        setattr(a, fld, f.get(fld, '').strip() or None)
    a.last_verified = _d(f.get('last_verified'))
    complete = a.last_verified and a.official_url and a.admission_year and a.reviewer
    a.status = 'verified' if complete else 'needs_verification'
    db.session.commit()
    audit('admission_edited', None, f'{a.key} -> {a.status}', 'admin')
    flash('Saved. ' + ('Marked verified.' if complete else 'Still “requires verification”: it needs the year, official link, reviewer and date.'), 'ok')
    return redirect(url_for('futureready.admin_home') + '#admissions')


@fr_bp.route('/admin/branch/<key>', methods=['POST'])
@admin_required
def admin_branch(key):
    b = FrBranch.query.filter_by(key=key).first_or_404()
    for fld in ('studies', 'problems', 'projects', 'foundations', 'skills', 'activities', 'environment'):
        if fld in request.form:
            setattr(b, fld, request.form[fld].strip())
    b.active = bool(request.form.get('active'))
    b.last_reviewed = date.today()
    db.session.commit()
    audit('branch_edited', None, b.key, 'admin')
    return redirect(url_for('futureready.admin_home') + '#branches')


@fr_bp.route('/admin/window', methods=['POST'])
@admin_required
def admin_window():
    f = request.form
    db.session.add(FrWindow(assessment_key=f.get('assessment_key') or None, label=f.get('label', '')[:120], opens_on=_d(f.get('opens')), closes_on=_d(f.get('closes')), grade=f.get('grade', type=int)))
    db.session.commit()
    return redirect(url_for('futureready.admin_home') + '#windows')


@fr_bp.route('/admin/export.csv')
@admin_required
def admin_export():
    """Aggregate skill scores for real (non-demo) students only. Open-text answers and private notes are never exported."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(['profile_id', 'grade', 'assessment', 'skill', 'kind', 'value', 'n', 'recorded'])
    for s in (FrSkillScore.query.join(FrProfile, FrProfile.id == FrSkillScore.profile_id).filter(FrProfile.demo == False).order_by(FrSkillScore.id)):  # noqa
        pr = db.session.get(FrProfile, s.profile_id)
        w.writerow([s.profile_id, pr.grade, s.assessment_key, s.skill, s.kind, s.value, s.n, s.created_at.isoformat()])
    audit('export_csv', None, 'skill scores (non-demo)', 'admin')
    return Response(out.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=futureready-scores.csv'})
