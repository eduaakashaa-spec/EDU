"""EduPulse - Reinforcement routes. Authorization is decided here, on the server:

student  /edupulse-reinforce/            own assignments, progress, released explanations
mentor   /edupulse-reinforce/mentor...   own roster only (admin: everyone): assign, review answers, analytics, question bank
parent   /edupulse-reinforce/parent/<id> read-only weekly report, only for linked parents and only when the student's profile allows it
admin    /edupulse-reinforce/admin       thresholds, taxonomy, review queue, audit, demo workspace
Answer keys, explanations and misconceptions never leave the server for a student until `services.reinforce.released()` says so.
"""
import json
import os
from datetime import datetime, timedelta

from flask import Blueprint, Response, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import admin_required, premium_required, staff_required
from app.extensions import db
from app.models import User
from app.models_reinforce import (RfAssignment, RfAssignmentStudent, RfAttempt, RfAudit, RfDraft, RfItem, RfNotice, RfObservation, RfQuestion, RfRecommendation, RfSetting, RfStudent, RfTaxonomy, jl)
from app.services import reinforce as rf

reinforce_bp = Blueprint('reinforce', __name__, url_prefix='/edupulse-reinforce')
IST = timedelta(hours=5, minutes=30)


def ist_dt(s):
    """datetime-local string typed in IST -> naive UTC."""
    try:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M') - IST if s else None
    except ValueError:
        return None


@reinforce_bp.app_template_filter('ist')
def _ist(d, fmt='%d %b, %I:%M %p'):
    return (d + IST).strftime(fmt) if d else ''


@reinforce_bp.app_template_filter('istinput')
def _istinput(d):
    return (d + IST).strftime('%Y-%m-%dT%H:%M') if d else ''


@reinforce_bp.app_context_processor
def _inject():
    return {'rf_popup': _popup, 'rf_label': rf.STATUS_LABEL, 'rf_mlabel': rf.MENTOR_STATUS_LABEL}


def _my_student():
    if not current_user.is_authenticated:
        return None
    return RfStudent.query.filter_by(user_id=current_user.id, active=True).first()


def _popup():
    """The daily reinforcement popup for the member home page: pending, un-snoozed assignments only; nothing for completed work."""
    rs = _my_student()
    if not rs:
        return None
    cands = rf.popup_candidates(rs)
    if not cands:
        return None
    total = sum(len(x.items.all()) for x in cands)
    first = cands[0]
    a = first.assignment
    qs = [it.question for it in first.items.all()]
    return {'count': len(cands), 'asg': first, 'a': a, 'questions': total, 'minutes': max(1, round(sum((q.est_sec or 90) for q in qs) / 60)), 'focus': ', '.join(dict.fromkeys(filter(None, [a.subject, a.chapter]))) or a.exam,
            'mentor': rs.mentor.name if rs.mentor else 'Your EduAakashaa mentor', 'dismissible': a.popup != 'mandatory' and a.allow_remind, 'status': first.status}


def _staff_students():
    q = RfStudent.query.filter_by(active=True)
    if not current_user.is_admin:
        q = q.filter_by(mentor_id=current_user.id)
    return q


def _student_or_404(rsid):
    rs = db.session.get(RfStudent, rsid) or abort(404)
    if not current_user.is_admin and rs.mentor_id != current_user.id:
        abort(404)
    return rs


def _asg_or_404(aid):
    a = db.session.get(RfAssignment, aid) or abort(404)
    if not current_user.is_admin and a.created_by != current_user.id and not any(s.student.mentor_id == current_user.id for s in a.students.all()):
        abort(404)
    return a


def _int(name, default=None, lo=None, hi=None):
    try:
        v = int(request.form.get(name))
    except (TypeError, ValueError):
        return default
    if lo is not None:
        v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v


# =================================================================================================================================
# student
# =================================================================================================================================
@reinforce_bp.route('/')
@premium_required
def home():
    rs = _my_student()
    if not rs:
        if current_user.is_staff:
            return redirect(url_for('reinforce.mentor_home'))
        return render_template('reinforce/not_enrolled.html')
    rf.process_events()
    sm = rf.student_summary(rs)
    t = rf.now()
    pend = rf.pending_for(rs)
    done = (RfAssignmentStudent.query.filter_by(student_id=rs.id, status='completed').order_by(RfAssignmentStudent.completed_at.desc()).limit(8).all())
    recs = RfRecommendation.query.filter_by(student_id=rs.id, status='approved').order_by(RfRecommendation.id.desc()).limit(3).all()
    notices = RfNotice.query.filter_by(user_id=current_user.id, read=False).order_by(RfNotice.id.desc()).limit(6).all()
    return render_template('reinforce/home.html', rs=rs, sm=sm, pend=pend, done=done, recs=recs, notices=notices, PATTERNS=rf.PATTERNS, CONF=rf.CONF, rf=rf, now=t)


@reinforce_bp.route('/notices/read', methods=['POST'])
@login_required
def notices_read():
    RfNotice.query.filter_by(user_id=current_user.id, read=False).update({'read': True})
    db.session.commit()
    return redirect(request.referrer or url_for('reinforce.home'))


def _mine(asid):
    rs = _my_student() or abort(403)
    x = db.session.get(RfAssignmentStudent, asid) or abort(404)
    if x.student_id != rs.id or x.assignment.status != 'active' and x.status != 'completed':
        abort(404)
    if x.assignment.start_at > rf.now():
        abort(404)
    return rs, x


@reinforce_bp.route('/do/<int:asid>')
@premium_required
def do(asid):
    rs, x = _mine(asid)
    return render_template('reinforce/do.html', x=x, a=x.assignment, rs=rs, CONF=rf.CONF)


def _item_payload(it):
    q = it.question
    return {'id': it.id, 'pos': it.position, 'qtype': q.qtype, 'stem': q.stem, 'options': q.options if q.qtype != 'nat' else [], 'chapter': q.chapter, 'topic': q.topic, 'subject': q.subject,
            'exam': q.exam, 'difficulty': rf.DIFF_LABEL.get(q.difficulty, ''), 'est_sec': q.est_sec}


@reinforce_bp.route('/api/asg/<int:asid>')
@premium_required
def api_asg(asid):
    rs, x = _mine(asid)
    a = x.assignment
    items = x.items.all()
    drafts = {d.item_id: d for d in RfDraft.query.filter(RfDraft.item_id.in_([i.id for i in items])).all()} if items else {}
    out = []
    first_open = None
    for n, it in enumerate(items):
        p = _item_payload(it)
        d = drafts.get(it.id)
        p['answer'] = jl(d.answer_json, None) if d and d.answer_json else None
        p['confidence'] = d.confidence if d else None
        p['seconds'] = d.seconds if d else 0
        out.append(p)
        if x.status != 'completed' and first_open is None and not (p['answer'] not in (None, '', []) and p['confidence']):
            first_open = n
    if x.status == 'not_started':
        x.status, x.started_at = 'in_progress', rf.now()
        db.session.commit()
    return jsonify(ok=True, status=x.status, title=a.title, instructions=a.instructions or '', exam=a.exam, allow_back=a.allow_back, timed=a.timed, due=a.due_at.isoformat() if a.due_at else None, items=out,
                   resume=first_open or 0, completed=x.status == 'completed', released=rf.released(x))


@reinforce_bp.route('/api/asg/<int:asid>/save', methods=['POST'])
@premium_required
def api_save(asid):
    rs, x = _mine(asid)
    if x.status == 'completed':
        return jsonify(ok=False, error='already submitted'), 409
    d = request.get_json(silent=True) or {}
    it = db.session.get(RfItem, d.get('item_id') or 0)
    if not it or it.asg_student_id != x.id:
        return jsonify(ok=False, error='unknown item'), 404
    conf = d.get('confidence') if d.get('confidence') in ('G', 'L', 'M', 'H') else None
    raw = d.get('answer')
    value, err = rf.parse_answer(it.question, raw) if raw not in (None, '', []) else (None, None)
    row = RfDraft.query.filter_by(item_id=it.id).first() or RfDraft(item_id=it.id)
    row.answer_json = json.dumps(raw) if value is not None else None
    row.confidence = conf if value is not None else None                          # a rating without an answer is meaningless
    try:
        row.seconds = max(0, min(int(d.get('seconds') or 0), 3600))
    except (TypeError, ValueError):
        row.seconds = 0
    db.session.add(row)
    x.last_pos = it.position
    db.session.commit()
    return jsonify(ok=True)


@reinforce_bp.route('/api/asg/<int:asid>/submit', methods=['POST'])
@premium_required
def api_submit(asid):
    rs, x = _mine(asid)
    items = x.items.all()
    drafts = {d.item_id: d for d in RfDraft.query.filter(RfDraft.item_id.in_([i.id for i in items])).all()} if items else {}
    missing = [i.position for i in items if not (drafts.get(i.id) and drafts[i.id].answer_json and drafts[i.id].confidence)]
    if x.status != 'completed' and missing:
        return jsonify(ok=False, error='Answer every question and choose a confidence level for each.', missing=missing), 400
    first = rf.submit(x)
    rows = RfAttempt.query.filter_by(student_id=rs.id, assignment_id=x.assignment_id).filter(RfAttempt.answered_at >= (x.completed_at - timedelta(minutes=1))).all() if x.completed_at else []
    right = sum(1 for r in rows if r.correct)
    revisit = len({r.chapter + '|' + (r.topic or '') for r in rows if not r.correct})
    return jsonify(ok=True, first_time=first, answered=len(items), correct=right, revisit=revisit, released=rf.released(x), streak=rf.streak(rs.id),
                   release_note={'immediate': 'Explanations are available now.', 'after_submit': 'Explanations are available now.', 'scheduled': 'Explanations are released at the time your mentor set.',
                                 'manual': 'Your mentor will release the explanations.'}[x.assignment.release])


@reinforce_bp.route('/api/asg/<int:asid>/review')
@premium_required
def api_review(asid):
    """Answer keys and explanations: only after the release rule allows it."""
    rs, x = _mine(asid)
    if not rf.released(x):
        return jsonify(ok=False, error='Explanations are not released yet.'), 403
    out = []
    for it in x.items.all():
        q = it.question
        att = RfAttempt.query.filter_by(student_id=rs.id, assignment_id=x.assignment_id, question_id=q.id).order_by(RfAttempt.id.desc()).first()
        d = RfDraft.query.filter_by(item_id=it.id).first()
        out.append({'pos': it.position, 'stem': q.stem, 'options': q.options, 'qtype': q.qtype, 'answer': q.answer, 'explanation': q.explanation, 'misconception': q.misconception if att and att.confidence == 'H' and not att.correct else '',
                    'yours': jl(att.answer_json, None) if att else (jl(d.answer_json, None) if d and d.answer_json else None), 'correct': att.correct if att else None, 'confidence': att.confidence if att else None})
    return jsonify(ok=True, items=out)


@reinforce_bp.route('/remind/<int:asid>', methods=['POST'])
@premium_required
def remind(asid):
    rs, x = _mine(asid)
    if x.assignment.popup == 'mandatory' or not x.assignment.allow_remind:
        abort(403)
    x.dismissed_until = rf.now() + timedelta(hours=4)
    db.session.commit()
    return redirect(request.form.get('next') or url_for('memberhub.home'))


# =================================================================================================================================
# parent (read-only)
# =================================================================================================================================
def _parent_allowed(rs):
    if current_user.is_admin or (current_user.is_staff and rs.mentor_id == current_user.id):
        return True
    if not rs.parent_report:
        return False
    try:
        from app.models_mentorship import MsEnrolment, MsParentLink
        ids = [e.id for e in MsEnrolment.query.filter_by(student_id=rs.user_id).all()]
        if ids and MsParentLink.query.filter(MsParentLink.enrolment_id.in_(ids), MsParentLink.parent_id == current_user.id).first():
            return True
    except Exception:
        pass
    try:
        from app.futureready.models import FrParentLink, FrProfile
        p = FrProfile.query.filter_by(user_id=rs.user_id).first()
        if p and FrParentLink.query.filter_by(profile_id=p.id, parent_id=current_user.id).first():
            return True
    except Exception:
        pass
    return False


@reinforce_bp.route('/parent/<int:rsid>')
@login_required
def parent(rsid):
    rs = db.session.get(RfStudent, rsid) or abort(404)
    if not _parent_allowed(rs):
        abort(404)
    days = 30 if request.args.get('period') == 'month' else 7
    return render_template('reinforce/parent.html', r=rf.parent_report(rs, days), rs=rs, rf=rf, PATTERNS=rf.PATTERNS)


@reinforce_bp.route('/parent')
@login_required
def parent_list():
    """Children whose reinforcement report this account may read."""
    out = [rs for rs in RfStudent.query.filter_by(active=True, parent_report=True).all() if _parent_allowed(rs) and rs.user_id != current_user.id]
    if len(out) == 1:
        return redirect(url_for('reinforce.parent', rsid=out[0].id))
    return render_template('reinforce/parent_list.html', rows=out)


# =================================================================================================================================
# mentor
# =================================================================================================================================
@reinforce_bp.route('/mentor')
@staff_required
def mentor_home():
    rf.process_events()
    q = _staff_students()
    exam, grp, status, term = request.args.get('exam', ''), request.args.get('group', ''), request.args.get('status', ''), request.args.get('q', '').strip().lower()
    mentor_f = request.args.get('mentor', type=int)
    if exam:
        q = q.filter_by(exam=exam)
    if grp:
        q = q.filter_by(group_name=grp)
    if mentor_f and current_user.is_admin:
        q = q.filter_by(mentor_id=mentor_f)
    rows = []
    for rs in q.all():
        if term and term not in (rs.user.name + ' ' + rs.user.email + ' EA%d' % rs.user_id).lower():
            continue
        sm = rf.student_summary(rs)
        pend = rf.pending_for(rs)
        st = 'overdue' if any(rf.is_overdue(x.assignment) for x in pend) else 'pending' if pend else 'clear'
        if status and status != st:
            continue
        rows.append({'rs': rs, 'sm': sm, 'status': st, 'pend': pend})
    rows.sort(key=lambda r: ({'overdue': 0, 'pending': 1, 'clear': 2}[r['status']], r['rs'].user.name))
    notices = RfNotice.query.filter_by(user_id=current_user.id, read=False).order_by(RfNotice.id.desc()).limit(8).all()
    groups = sorted({s.group_name for s in _staff_students().all() if s.group_name})
    mentors = User.query.filter(User.tier.in_(['ea_mentor', 'admin'])).order_by(User.name).all() if current_user.is_admin else []
    return render_template('reinforce/mentor_home.html', rows=rows, notices=notices, groups=groups, mentors=mentors, f={'exam': exam, 'group': grp, 'status': status, 'q': request.args.get('q', ''), 'mentor': mentor_f}, rf=rf)


@reinforce_bp.route('/mentor/students', methods=['GET', 'POST'])
@staff_required
def mentor_students():
    if request.method == 'POST':
        do = request.form.get('do')
        if do == 'add':
            u = User.query.filter(db.func.lower(User.email) == request.form.get('email', '').strip().lower()).first()
            if not u:
                flash('That student must first register on the site with this email.', 'danger')
            elif RfStudent.query.filter_by(user_id=u.id).first():
                flash('That student is already on a roster.', 'info')
            else:
                mid = _int('mentor_id') if current_user.is_admin else current_user.id
                db.session.add(RfStudent(user_id=u.id, mentor_id=mid or current_user.id, exam='UCEED' if request.form.get('exam') == 'UCEED' else 'JEE', grade=request.form.get('grade', '')[:20], group_name=request.form.get('group', '')[:60] or None))
                db.session.commit()
                rf.audit(current_user.id, 'student_added', u.email)
                flash('Student added.', 'success')
        elif do == 'import':
            n = 0
            try:
                from app.models_mentorship import MsEnrolment
                for e in MsEnrolment.query.filter(MsEnrolment.status == 'Active', (MsEnrolment.mentor_id == current_user.id) if not current_user.is_admin else True).all():
                    if not RfStudent.query.filter_by(user_id=e.student_id).first():
                        db.session.add(RfStudent(user_id=e.student_id, mentor_id=e.mentor_id or current_user.id, exam='UCEED' if 'UCEED' in (e.programme.name or '').upper() else 'JEE', grade=e.grade))
                        n += 1
            except Exception:
                pass
            try:
                from app.models_pulse import PulseProfile
                for p in PulseProfile.query.filter(PulseProfile.mentor_id == current_user.id if not current_user.is_admin else True).all():
                    if not RfStudent.query.filter_by(user_id=p.user_id).first():
                        db.session.add(RfStudent(user_id=p.user_id, mentor_id=p.mentor_id or current_user.id, exam='UCEED', grade=p.student_class))
                        n += 1
            except Exception:
                pass
            db.session.commit()
            flash('%d student(s) imported from Mentorship and EduPulse.' % n, 'success')
        elif do == 'update':
            rs = _student_or_404(_int('id', 0))
            rs.exam = 'UCEED' if request.form.get('exam') == 'UCEED' else 'JEE'
            rs.grade = request.form.get('grade', '')[:20]
            rs.group_name = request.form.get('group', '')[:60] or None
            rs.parent_report = bool(request.form.get('parent_report'))
            if current_user.is_admin and _int('mentor_id'):
                rs.mentor_id = _int('mentor_id')
            if request.form.get('remove'):
                rs.active = False
            db.session.commit()
            flash('Saved.', 'success')
        return redirect(url_for('reinforce.mentor_students'))
    mentors = User.query.filter(User.tier.in_(['ea_mentor', 'admin'])).order_by(User.name).all() if current_user.is_admin else []
    return render_template('reinforce/mentor_students.html', students=_staff_students().all(), mentors=mentors)


@reinforce_bp.route('/mentor/student/<int:rsid>')
@staff_required
def mentor_student(rsid):
    rs = _student_or_404(rsid)
    sm = rf.student_summary(rs)
    subject, chapter, topic = request.args.get('subject', ''), request.args.get('chapter', ''), request.args.get('topic', '')
    rows = rf.attempts_of(rs.id)
    drill = [a for a in rows if (not subject or a.subject == subject) and (not chapter or a.chapter == chapter) and (not topic or a.topic == topic)]
    topics = {}
    if chapter:
        for a in rows:
            if a.chapter == chapter:
                t = topics.setdefault(a.topic or '-', [0, 0])
                t[0] += 1
                t[1] += 1 if a.correct else 0
    recs = RfRecommendation.query.filter_by(student_id=rs.id).filter(RfRecommendation.status == 'suggested').order_by(RfRecommendation.id.desc()).all()
    obs = RfObservation.query.filter_by(student_id=rs.id).order_by(RfObservation.id.desc()).limit(10).all()
    asgs = RfAssignmentStudent.query.filter_by(student_id=rs.id).order_by(RfAssignmentStudent.id.desc()).limit(10).all()
    mocks = {}
    try:
        from app.services import pulse_jee as pj
        from app.services import pulse_mock as pm
        mocks = {'jee': pj.summary(rs.user_id), 'uceed': pm.summary(rs.user_id)}
    except Exception:
        pass
    for r in recs:
        r.qs = [db.session.get(RfQuestion, i) for i in jl(r.question_ids, [])]
    return render_template('reinforce/mentor_student.html', rs=rs, sm=sm, drill=list(reversed(drill))[:60], subject=subject, chapter=chapter, topic=topic, topics=topics, recs=recs, obs=obs, asgs=asgs, mocks=mocks,
                           PATTERNS=rf.PATTERNS, CONF=rf.CONF, rf=rf, settings=rf.settings(), pattern_of=rf.pattern_of)


@reinforce_bp.route('/mentor/student/<int:rsid>/obs', methods=['POST'])
@staff_required
def mentor_obs(rsid):
    rs = _student_or_404(rsid)
    body = request.form.get('body', '').strip()
    if body:
        fu = None
        try:
            fu = datetime.strptime(request.form.get('follow_up', ''), '%Y-%m-%d').date() if request.form.get('follow_up') else None
        except ValueError:
            pass
        db.session.add(RfObservation(student_id=rs.id, author_id=current_user.id, chapter=request.form.get('chapter', '')[:80] or None, body=body[:3000], follow_up_on=fu, for_parent=bool(request.form.get('for_parent'))))
        db.session.commit()
    return redirect(url_for('reinforce.mentor_student', rsid=rsid) + '#notes')


@reinforce_bp.route('/mentor/student/<int:rsid>/recs', methods=['POST'])
@staff_required
def mentor_recs(rsid):
    rs = _student_or_404(rsid)
    made = rf.generate_recommendations(rs)
    flash('%d new suggestion(s). Nothing is assigned until you approve it.' % len(made), 'success')
    return redirect(url_for('reinforce.mentor_student', rsid=rsid) + '#recs')


@reinforce_bp.route('/mentor/rec/<int:rid>/<action>', methods=['POST'])
@staff_required
def mentor_rec(rid, action):
    r = db.session.get(RfRecommendation, rid) or abort(404)
    rs = _student_or_404(r.student_id)
    if r.status != 'suggested':
        return redirect(url_for('reinforce.mentor_student', rsid=rs.id))
    if action == 'approve':
        a = rf.apply_recommendation(current_user, r)
        flash('Assigned: "%s".' % a.title, 'success')
    elif action == 'reject':
        r.status = 'rejected'
        db.session.commit()
    elif action == 'modify':
        return redirect(url_for('reinforce.assign', rec=r.id))
    return redirect(url_for('reinforce.mentor_student', rsid=rs.id) + '#recs')


# ---- assignments ----------------------------------------------------------------------------------------------------------------
@reinforce_bp.route('/mentor/assign', methods=['GET', 'POST'])
@staff_required
def assign():
    students = _staff_students().all()
    pre = {}
    src = db.session.get(RfAssignment, request.args.get('from', type=int) or 0) if request.args.get('from') else None
    rec = db.session.get(RfRecommendation, request.args.get('rec', type=int) or 0) if request.args.get('rec') else None
    if src:
        pre = {'title': src.title + ' (copy)', 'exam': src.exam, 'subject': src.subject, 'chapter': src.chapter, 'topic': src.topic, 'objective': src.objective, 'instructions': src.instructions, 'n': src.n_questions,
               'release': src.release, 'popup': src.popup, 'allow_remind': src.allow_remind, 'allow_back': src.allow_back, 'remind_hours': src.remind_hours, 'popup_hours': src.popup_hours, 'timed': src.timed}
    elif rec:
        pre = {'title': rec.title, 'exam': rec.student.exam, 'chapter': rec.chapter, 'objective': rec.why[:300], 'n': len(jl(rec.question_ids, [])) or 5, 'manual_ids': ','.join(str(i) for i in jl(rec.question_ids, [])), 'students': [rec.student_id]}
    if request.args.get('student', type=int):
        pre['students'] = [request.args.get('student', type=int)]
    if request.method == 'POST':
        f = request.form
        exam = 'UCEED' if f.get('exam') == 'UCEED' else 'JEE'
        sids = [int(x) for x in f.getlist('students') if x.isdigit()]
        if f.get('group'):
            sids += [s.id for s in students if s.group_name == f['group'] and s.exam == exam]
        ok = {s.id for s in students if s.exam == exam}
        bad = [i for i in set(sids) if i not in {s.id for s in students}]
        sids = [i for i in dict.fromkeys(sids) if i in ok]
        n = max(5, min(10, _int('n', 8)))
        errors = []
        if bad:
            errors.append('One or more selected students are not on your roster.')
        if not sids:
            errors.append('Choose at least one student (with the same exam track).')
        if not f.get('title', '').strip():
            errors.append('Give the assignment a title.')
        mix = {str(d): max(0, min(10, _int('mix%d' % d, 0))) for d in (1, 2, 3)}
        sel = f.get('selection') if f.get('selection') in ('manual', 'filter', 'recommended') else 'filter'
        picks = {}
        if sel in ('manual', 'recommended'):
            ids = [int(x) for x in f.get('manual_ids', '').replace(' ', '').split(',') if x.isdigit()]
            qs = [q for q in (db.session.get(RfQuestion, i) for i in ids) if q and q.status == 'approved' and q.exam == exam]
            if len(qs) < 5 or len(qs) > 10:
                errors.append('Choose between 5 and 10 approved %s questions (you chose %d).' % (exam, len(qs)))
            picks = {sid: qs for sid in sids}
            n = len(qs)
        else:
            picks = rf.pick_questions(exam, f.get('subject') or None, f.get('chapter') or None, f.get('topic') or None, n, mix, sids, distinct=bool(f.get('distinct')))
            short = [sid for sid in sids if len(picks.get(sid, [])) < min(n, 5)]
            if short:
                errors.append('The question bank has too few approved questions for this filter (need at least 5).')
        start_at, due_at = ist_dt(f.get('start_at')) or rf.now(), ist_dt(f.get('due_at'))
        if due_at and due_at <= start_at:
            errors.append('The due time must be after the start time.')
        if errors:
            for e in errors:
                flash(e, 'danger')
            pre = dict(pre, **{k: v for k, v in f.items()})
            pre['students'] = [int(x) for x in f.getlist('students') if x.isdigit()]
        else:
            a = rf.create_assignment(current_user, {'title': f['title'].strip(), 'exam': exam, 'subject': f.get('subject'), 'chapter': f.get('chapter'), 'topic': f.get('topic'), 'objective': f.get('objective'),
                                                    'instructions': f.get('instructions'), 'n': n, 'mix': mix, 'selection': sel, 'distinct': bool(f.get('distinct')), 'start_at': start_at, 'due_at': due_at,
                                                    'release': f.get('release') if f.get('release') in ('immediate', 'after_submit', 'scheduled', 'manual') else 'after_submit', 'release_at': ist_dt(f.get('release_at')),
                                                    'popup': f.get('popup') if f.get('popup') in ('mandatory', 'dismissible', 'time_limited') else 'dismissible', 'popup_hours': _int('popup_hours', 24, 1, 168),
                                                    'allow_remind': bool(f.get('allow_remind')), 'allow_back': bool(f.get('allow_back')), 'remind_hours': _int('remind_hours', 6, 1, 72), 'timed': bool(f.get('timed')),
                                                    'source_id': src.id if src else None, 'recommendation_id': rec.id if rec else None}, sids, picks)
            if rec:
                rec.status, rec.assignment_id = 'approved', a.id
                db.session.commit()
            flash('Assigned "%s" to %d student(s).' % (a.title, len(a.students.all())), 'success')
            return redirect(url_for('reinforce.assignment', aid=a.id))
    return render_template('reinforce/assign.html', students=students, pre=pre, tax=rf.taxonomy(), groups=sorted({s.group_name for s in students if s.group_name}), rf=rf, ist_now=(rf.now() + IST).strftime('%Y-%m-%dT%H:%M'))


@reinforce_bp.route('/mentor/assignments')
@staff_required
def assignments():
    q = RfAssignment.query.order_by(RfAssignment.id.desc())
    if not current_user.is_admin:
        mine = {s.id for s in _staff_students().all()}
        q = q.filter(db.or_(RfAssignment.created_by == current_user.id, RfAssignment.id.in_(db.session.query(RfAssignmentStudent.assignment_id).filter(RfAssignmentStudent.student_id.in_(mine or [0])))))
    rows = []
    for a in q.limit(60).all():
        st = a.students.all()
        rows.append({'a': a, 'n': len(st), 'done': sum(1 for s in st if s.status == 'completed'), 'late': sum(1 for s in st if s.status != 'completed' and rf.is_overdue(a))})
    return render_template('reinforce/assignments.html', rows=rows)


@reinforce_bp.route('/mentor/assignment/<int:aid>', methods=['GET', 'POST'])
@staff_required
def assignment(aid):
    a = _asg_or_404(aid)
    if request.method == 'POST':
        do = request.form.get('do')
        if do == 'release':
            a.release, a.release_at = 'manual', rf.now()
        elif do == 'close':
            a.status = 'closed'
        elif do == 'cancel':
            a.status = 'cancelled'
        db.session.commit()
        rf.audit(current_user.id, 'assignment_' + (do or ''), a.title)
        return redirect(url_for('reinforce.assignment', aid=aid))
    st = a.students.all()
    if not current_user.is_admin:
        st = [s for s in st if s.student.mentor_id == current_user.id]
    stats = {}
    for s in st:
        rows = RfAttempt.query.filter_by(assignment_id=a.id, student_id=s.student_id).all()
        stats[s.id] = {'n': len(rows), 'right': sum(1 for r in rows if r.correct), 'high_wrong': sum(1 for r in rows if r.confidence == 'H' and not r.correct)}
    return render_template('reinforce/assignment.html', a=a, st=st, stats=stats, rf=rf)


# ---- question bank ---------------------------------------------------------------------------------------------------------------
@reinforce_bp.route('/mentor/bank')
@staff_required
def bank():
    f = {k: request.args.get(k, '') for k in ('exam', 'subject', 'chapter', 'status', 'diff', 'q')}
    q = RfQuestion.query.filter_by(active=True)
    if f['exam']:
        q = q.filter_by(exam=f['exam'])
    if f['subject']:
        q = q.filter_by(subject=f['subject'])
    if f['chapter']:
        q = q.filter_by(chapter=f['chapter'])
    if f['status']:
        q = q.filter_by(status=f['status'])
    if f['diff'].isdigit():
        q = q.filter_by(difficulty=int(f['diff']))
    if f['q']:
        like = '%' + f['q'] + '%'
        q = q.filter(db.or_(RfQuestion.qid.ilike(like), RfQuestion.stem.ilike(like), RfQuestion.topic.ilike(like), RfQuestion.concept.ilike(like)))
    total = q.count()
    page = max(1, request.args.get('page', 1, type=int))
    rows = q.order_by(RfQuestion.id.desc()).offset((page - 1) * 40).limit(40).all()
    counts = dict(db.session.query(RfQuestion.status, db.func.count(RfQuestion.id)).filter_by(active=True).group_by(RfQuestion.status).all())
    return render_template('reinforce/bank.html', rows=rows, f=f, total=total, page=page, counts=counts, tax=rf.taxonomy(), rf=rf)


@reinforce_bp.route('/mentor/bank/export.csv')
@staff_required
def bank_export():
    q = RfQuestion.query.filter_by(active=True)
    if request.args.get('exam') in ('UCEED', 'JEE'):
        q = q.filter_by(exam=request.args['exam'])
    rf.audit(current_user.id, 'bank_export', request.args.get('exam', 'all'))
    return Response(rf.export_csv(q.order_by(RfQuestion.id).all()), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=edupulse-reinforcement-questions.csv'})


@reinforce_bp.route('/mentor/bank/import', methods=['POST'])
@staff_required
def bank_import():
    f = request.files.get('file')
    if not f:
        flash('Choose a CSV file.', 'danger')
        return redirect(url_for('reinforce.bank'))
    try:
        text = f.read(2_000_000).decode('utf-8-sig')
    except UnicodeDecodeError:
        flash('The file must be UTF-8 CSV.', 'danger')
        return redirect(url_for('reinforce.bank'))
    n, errs = rf.import_csv(text, current_user)
    if errs:
        for e in errs[:12]:
            flash(e, 'danger')
        flash('Nothing was imported: fix the rows above and upload again (%d problem%s).' % (len(errs), '' if len(errs) == 1 else 's'), 'danger')
    else:
        flash('%d question(s) imported as drafts.' % n, 'success')
    return redirect(url_for('reinforce.bank'))


def _qform(q):
    f = request.form
    qt = f.get('qtype') if f.get('qtype') in ('mcq', 'msq', 'nat') else 'mcq'
    exam = 'UCEED' if f.get('exam') == 'UCEED' else 'JEE'
    opts = [rf.sanitize(f.get('option_' + c, '')) for c in 'abcd']
    errs = []
    tx = RfTaxonomy.query.filter_by(exam=exam, subject=f.get('subject', ''), chapter=f.get('chapter', '')).first()
    if not tx:
        errs.append('Choose a subject and chapter from the taxonomy.')
    if not f.get('stem', '').strip():
        errs.append('The question text is required.')
    if qt == 'nat':
        try:
            key = [[float(f.get('answer_nat')), float(f.get('answer_nat_hi') or f.get('answer_nat'))]]
        except (TypeError, ValueError):
            errs.append('Enter the numerical answer.')
            key = None
        opts = []
    elif qt == 'msq':
        key = sorted(x for x in f.getlist('answer_msq') if x in ('A', 'B', 'C', 'D'))
        if not key:
            errs.append('Tick the correct options.')
    else:
        key = f.get('answer_mcq') if f.get('answer_mcq') in ('A', 'B', 'C', 'D') else None
        if not key:
            errs.append('Choose the correct option.')
    if qt != 'nat' and sum(1 for o in opts if o) < 2:
        errs.append('Give at least two options.')
    if qt != 'nat' and key and not isinstance(key, list) and not opts['ABCD'.index(key)]:
        errs.append('The correct option is empty.')
    return errs, dict(exam=exam, subject=f.get('subject'), chapter=f.get('chapter'), topic=f.get('topic', '')[:120] or f.get('chapter'), concept=f.get('concept', '')[:200], difficulty=max(1, min(3, int(f.get('difficulty') or 2))),
                      qtype=qt, stem=rf.sanitize(f.get('stem')), options_json=json.dumps(opts), answer_json=json.dumps(key), explanation=rf.sanitize(f.get('explanation')), misconception=rf.sanitize(f.get('misconception')),
                      marks=float(f.get('marks') or 4), neg_marks=float(f.get('neg_marks') or 0), est_sec=int(f.get('est_sec') or 90), source=f.get('source', '')[:200])


@reinforce_bp.route('/mentor/bank/new', methods=['GET', 'POST'])
@reinforce_bp.route('/mentor/bank/<int:qid>', methods=['GET', 'POST'])
@staff_required
def bank_edit(qid=None):
    q = db.session.get(RfQuestion, qid) if qid else None
    if qid and not q:
        abort(404)
    if q and q.status in ('approved', 'in_review') and not current_user.is_admin and q.author_id != current_user.id:
        flash('Only the author or an administrator can edit this question.', 'info')
    if request.method == 'POST':
        errs, d = _qform(q)
        if errs:
            for e in errs:
                flash(e, 'danger')
            return render_template('reinforce/bank_edit.html', q=q, form=request.form, tax=rf.taxonomy(), rf=rf)
        if q is None:
            code = request.form.get('qid', '').strip() or 'Q-%s-%05d' % (d['exam'], (db.session.query(db.func.max(RfQuestion.id)).scalar() or 0) + 1)
            if RfQuestion.query.filter_by(qid=code).first():
                flash('That question id already exists.', 'danger')
                return render_template('reinforce/bank_edit.html', q=q, form=request.form, tax=rf.taxonomy(), rf=rf)
            nq = RfQuestion(qid=code, version=1, author_id=current_user.id, status='draft', **d)
        else:
            q.active = False                                   # attempts keep pointing at the version that was answered
            nq = RfQuestion(qid=q.qid, version=(q.version or 1) + 1, author_id=q.author_id or current_user.id, status='draft', **d)
        db.session.add(nq)
        db.session.commit()
        rf.audit(current_user.id, 'question_saved', '%s v%d' % (nq.qid, nq.version))
        flash('Saved as %s version %d (draft). Submit it for review to make it assignable.' % (nq.qid, nq.version), 'success')
        return redirect(url_for('reinforce.bank_edit', qid=nq.id))
    return render_template('reinforce/bank_edit.html', q=q, form=None, tax=rf.taxonomy(), rf=rf)


@reinforce_bp.route('/mentor/bank/<int:qid>/status', methods=['POST'])
@staff_required
def bank_status(qid):
    q = db.session.get(RfQuestion, qid) or abort(404)
    to = request.form.get('to')
    if to == 'in_review' and q.status == 'draft':
        q.status = 'in_review'
    elif to in ('approved', 'draft') and q.status == 'in_review':
        if not current_user.is_admin and q.author_id == current_user.id:
            flash('A question must be approved by someone other than its author (or an administrator).', 'danger')
            return redirect(url_for('reinforce.bank_edit', qid=qid))
        q.status = to
        q.reviewer_id = current_user.id
    elif to == 'retired' and current_user.is_admin:
        q.status = 'retired'
    else:
        abort(400)
    db.session.commit()
    rf.audit(current_user.id, 'question_' + q.status, '%s v%d' % (q.qid, q.version))
    return redirect(url_for('reinforce.bank_edit', qid=qid))


# =================================================================================================================================
# admin
# =================================================================================================================================
@reinforce_bp.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    if request.method == 'POST':
        do = request.form.get('do')
        if do == 'settings':
            for k in rf.DEFAULTS:
                v = request.form.get(k, '').strip()
                try:
                    float(v)
                except ValueError:
                    continue
                row = db.session.get(RfSetting, k) or RfSetting(key=k)
                row.value = v
                db.session.add(row)
            db.session.commit()
            rf.audit(current_user.id, 'settings_saved')
            flash('Thresholds saved.', 'success')
        elif do == 'seed':
            n = rf.seed_bank()
            flash('Question bank loaded (%d new questions). Existing questions were kept.' % n, 'success')
        elif do == 'demo':
            from app.services import reinforce_demo
            flash(reinforce_demo.create_demo(current_user), 'success')
        return redirect(url_for('reinforce.admin'))
    counts = dict(db.session.query(RfQuestion.status, db.func.count(RfQuestion.id)).filter_by(active=True).group_by(RfQuestion.status).all())
    return render_template('reinforce/admin.html', settings=rf.settings(), help=rf.SETTING_HELP, counts=counts, review=RfQuestion.query.filter_by(status='in_review', active=True).order_by(RfQuestion.id).limit(30).all(),
                           tax=rf.taxonomy(), audit=RfAudit.query.order_by(RfAudit.id.desc()).limit(40).all(), n_students=RfStudent.query.count(), n_attempts=RfAttempt.query.count())


@reinforce_bp.route('/admin/attempts.csv')
@admin_required
def admin_attempts():
    import csv
    import io
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(['student_id', 'assignment_id', 'qid', 'exam', 'subject', 'chapter', 'topic', 'difficulty', 'confidence', 'correct', 'marks', 'seconds', 'answered_at'])
    for a in RfAttempt.query.join(RfStudent, RfStudent.id == RfAttempt.student_id).filter(RfStudent.demo == False).order_by(RfAttempt.id):  # noqa: E712
        w.writerow([a.student_id, a.assignment_id, a.qid, a.exam, a.subject, a.chapter, a.topic, a.difficulty, a.confidence, int(bool(a.correct)), a.marks, a.seconds, a.answered_at.isoformat()])
    rf.audit(current_user.id, 'attempts_export')
    return Response(out.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=reinforcement-attempts.csv'})


@reinforce_bp.route('/cron/events', methods=['GET', 'POST'])
def cron_events():
    token = os.environ.get('REINFORCE_CRON_TOKEN', '')
    if not token or request.values.get('token') != token:
        abort(404)
    return jsonify(ok=True, notices=rf.process_events())
