"""EduPulse-Olympiad: subject mocks, official-paper practice, subject sets and spaced reinforcement for the Indian Olympiads.

Student (Premium member):  /olympiad-mock/                 centre: subject mocks, official papers, subject sets, Daily Review, progress
                           /olympiad-mock/test/<id>        the test page (questions without answers); id is M-<subject>, P-<exam>-<year> or S-<subject>
                           /olympiad-mock/daily            Daily Review: due review cards plus new questions from the weakest subjects
                           /olympiad-mock/submit/<id>      POST: a finished attempt, marked on the server (+3 right, -1 wrong for multiple choice)
                           /olympiad-mock/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                           /olympiad-mock/progress         tracker: subject levels, mock trend, review boxes, streak and badges
                           /olympiad-mock/student/<uid>    the same tracker for a mentor or admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseOlyResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import olympiad

oly_bp = Blueprint('olympiad_mock', __name__, url_prefix='/olympiad-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@oly_bp.route('/')
@premium_required
def home():
    done = {}
    for r in olympiad.for_user(current_user.id):
        done.setdefault(r.mock, r)
    cat = olympiad.catalogue()
    return render_template('pulse/olympiad.html', mocks=[t for t in cat if t['kind'] == 'mock'], sets=[t for t in cat if t['kind'] == 'set'], papers=[t for t in cat if t['kind'] == 'paper'],
                           done=done, tr=olympiad.tracker(current_user.id), SEC=olympiad.SEC, st={'n': len(olympiad.bank())}, RIGHT_MARKS=olympiad.RIGHT_MARKS, WRONG=olympiad.WRONG_MCQ)


def _take(t, timed):
    return render_template('pulse/olympiad_take.html', t=t, paper=olympiad.paper_for_browser(t['qids']), CONF=olympiad.CONF, timed=timed)


@oly_bp.route('/test/<tid>')
@premium_required
def take(tid):
    n = PulseOlyResult.query.filter_by(user_id=current_user.id, mock=tid).count()
    t = olympiad.compose(tid, current_user.id, n) or abort(404)
    return _take(t, request.args.get('mode') != 'practice')


@oly_bp.route('/daily')
@premium_required
def daily():
    return _take(olympiad.daily(current_user.id), False)


@oly_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    if (request.content_length or 0) > olympiad.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    known = {x['id']: x for x in olympiad.catalogue()}
    if tid == 'DAILY':
        t = {'id': 'DAILY', 'title': 'Daily Review'}
    elif tid in known:
        t = known[tid]
    else:
        abort(404)
    _ensure_profile()
    r, err = olympiad.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('olympiad_mock.report', rid=r.id))


@oly_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseOlyResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    own = r.user_id == current_user.id
    return render_template('pulse/olympiad_report.html', r=r, an=olympiad.analyse([r]), review=olympiad.review(r), CONF_LABEL=olympiad.CONF_LABEL, LETTERS=olympiad.LETTERS, own=own,
                           due=olympiad.tracker(current_user.id)['due'] if own else 0, RIGHT_MARKS=olympiad.RIGHT_MARKS, WRONG=olympiad.WRONG_MCQ)


@oly_bp.route('/progress')
@premium_required
def progress():
    return render_template('pulse/olympiad_progress.html', tr=olympiad.tracker(current_user.id), SEC=olympiad.SEC, student=current_user, own=True)


@oly_bp.route('/student/<int:uid>')
@login_required
def student_progress(uid):
    from app.models import User
    prof = db.session.get(PulseProfile, uid)
    if not (current_user.is_admin or (current_user.is_staff and prof and prof.mentor_id == current_user.id)):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    return render_template('pulse/olympiad_progress.html', tr=olympiad.tracker(uid), SEC=olympiad.SEC, student=u, own=False)
