"""EduPulse-Explorer: discovery tests, exam tasters and spaced practice for Grades 7 to 10 (engineering and design interests).

Student (logged in, free):  /explorer/                 centre: grade, interest check, Discovery Test, exam tasters, skill sets, Daily 10, streak and review cards
                            /explorer/test/<id>        the test page (questions without answers); id is D78, D910, X-JEE, X-UCD, X-NAT, X-IAT or K-<skill>
                            /explorer/daily            Daily 10: due review cards plus new questions from the weakest skills
                            /explorer/submit/<id>      POST: a finished attempt, marked on the server (one point a question, nothing deducted)
                            /explorer/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                            /explorer/progress         tracker: skill levels, exam-style picture, review boxes, streak and badges
                            /explorer/student/<uid>    the same tracker for a mentor or admin
                            /explorer/interests        the interest check (16 statements) and what it suggests
                            /explorer/make             creative challenges done at home, self-marked against a rubric
"""
import json

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models_pulse import PulseExpCreative, PulseExpResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import explorer as ex

explorer_bp = Blueprint('explorer', __name__, url_prefix='/explorer')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


def _grade():
    p = ex.profile(current_user.id)
    return p.grade if p and p.grade else None


@explorer_bp.route('/')
@login_required
def home():
    p = ex.profile(current_user.id)
    grade = p.grade if p and p.grade else None
    _, ints = ex.saved_interests(current_user.id)
    done = {}
    for r in ex.for_user(current_user.id):
        done.setdefault(r.mock, r)
    return render_template('pulse/explorer.html', grade=grade, goal=(p.weekly_goal if p else 3), tests=ex.catalogue(grade) if grade else [], tr=ex.tracker(current_user.id), ints=ints,
                           done=done, SKILLS=ex.SKILLS, FAMILIES=ex.FAMILIES, SKILL_BLURB=ex.SKILL_BLURB, creative=ex.creative())


@explorer_bp.route('/grade', methods=['POST'])
@login_required
def set_grade():
    try:
        g = int(request.form.get('grade', ''))
    except ValueError:
        g = 0
    if g not in (7, 8, 9, 10):
        flash('Choose Grade 7, 8, 9 or 10.', 'error')
        return redirect(url_for('explorer.home'))
    p = ex.profile(current_user.id, True)
    p.grade = g
    try:
        p.weekly_goal = max(1, min(7, int(request.form.get('goal', p.weekly_goal or 3))))
    except ValueError:
        pass
    db.session.commit()
    return redirect(url_for('explorer.home'))


def _take(t, timed):
    return render_template('pulse/explorer_take.html', t=t, paper=ex.paper_for_browser(t['qids']), CONF=ex.CONF, timed=timed)


@explorer_bp.route('/test/<tid>')
@login_required
def take(tid):
    g = _grade()
    if not g:
        return redirect(url_for('explorer.home'))
    n = PulseExpResult.query.filter_by(user_id=current_user.id, mock=tid).count()
    t = ex.compose(tid, g, current_user.id, n) or abort(404)
    return _take(t, request.args.get('mode') != 'practice')


@explorer_bp.route('/daily')
@login_required
def daily():
    g = _grade()
    if not g:
        return redirect(url_for('explorer.home'))
    return _take(ex.daily(current_user.id, g), False)


@explorer_bp.route('/submit/<tid>', methods=['POST'])
@login_required
def submit(tid):
    if (request.content_length or 0) > ex.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    g = _grade() or 8
    known = {x['id']: x for x in ex.catalogue(g)}
    if tid == 'DAILY':
        t = {'id': 'DAILY', 'title': 'Daily 10'}
    elif tid in known:
        t = known[tid]
    else:
        abort(404)
    _ensure_profile()
    r, err = ex.save_result(current_user.id, t, request.get_json(silent=True), g)
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('explorer.report', rid=r.id))


@explorer_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseExpResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    own = r.user_id == current_user.id
    return render_template('pulse/explorer_report.html', r=r, an=ex.analyse([r]), review=ex.review(r), CONF_LABEL=ex.CONF_LABEL, LETTERS=ex.LETTERS, own=own, FAMILIES=ex.FAMILIES,
                           due=ex.tracker(current_user.id)['due'] if own else 0)


@explorer_bp.route('/progress')
@login_required
def progress():
    return render_template('pulse/explorer_progress.html', tr=ex.tracker(current_user.id), SKILLS=ex.SKILLS, FAMILIES=ex.FAMILIES, grade=_grade(), student=current_user, own=True)


@explorer_bp.route('/student/<int:uid>')
@login_required
def student_progress(uid):
    from app.models import User
    prof = db.session.get(PulseProfile, uid)
    if not (current_user.is_admin or (current_user.is_staff and prof and prof.mentor_id == current_user.id)):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    p = ex.profile(uid)
    return render_template('pulse/explorer_progress.html', tr=ex.tracker(uid), SKILLS=ex.SKILLS, FAMILIES=ex.FAMILIES, grade=p.grade if p else None, student=u, own=False)


@explorer_bp.route('/interests', methods=['GET', 'POST'])
@login_required
def interests():
    if request.method == 'POST':
        try:
            ans = [int(request.form.get('q%d' % i, '')) for i in range(len(ex.INTEREST_ITEMS))]
        except ValueError:
            ans = []
        if not ex.save_interests(current_user.id, ans):
            flash('Please answer every statement.', 'error')
        return redirect(url_for('explorer.interests'))
    ans, res = ex.saved_interests(current_user.id)
    return render_template('pulse/explorer_interests.html', items=ex.INTEREST_ITEMS, ans=ans, res=res)


@explorer_bp.route('/make')
@login_required
def make():
    done = {c.cid: c for c in PulseExpCreative.query.filter_by(user_id=current_user.id).all()}
    return render_template('pulse/explorer_make.html', items=ex.creative(), done=done)


@explorer_bp.route('/make/<cid>', methods=['GET', 'POST'])
@login_required
def make_one(cid):
    c = next((x for x in ex.creative() if x['id'] == cid), None) or abort(404)
    if request.method == 'POST':
        try:
            scores = [int(request.form.get('s%d' % i, '')) for i in range(len(c['rubric']))]
        except ValueError:
            scores = None
        if scores is None or not ex.save_creative(current_user.id, cid, scores, request.form.get('note', '')):
            flash('Please mark every line within its marks.', 'error')
        else:
            flash('Saved. Show your work to your mentor or a parent.', 'ok')
        return redirect(url_for('explorer.make_one', cid=cid))
    row = PulseExpCreative.query.filter_by(user_id=current_user.id, cid=cid).first()
    return render_template('pulse/explorer_task.html', c=c, row=row, vals=json.loads(row.scores_json) if row else None, items=ex.creative())
