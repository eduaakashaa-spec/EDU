"""EduPulse-NEET: full and half mocks, previous-year practice and spaced reinforcement for NEET (UG).

Student (Premium member):  /neet-mock/                 centre: mocks, previous-year papers, subject sets, Daily Review, progress
                           /neet-mock/test/<id>        the test page (questions without answers); id is M-<mock>, S-<subject> or Y-<year>
                           /neet-mock/daily            Daily Review: due review cards plus new questions from the weakest subjects
                           /neet-mock/submit/<id>      POST: a finished attempt, marked on the server (+4 right, -1 wrong)
                           /neet-mock/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                           /neet-mock/progress         tracker: subject levels, mock trend, review boxes, streak and badges
                           /neet-mock/student/<uid>    the same tracker for a mentor or admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseNeetResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import neet

neet_bp = Blueprint('neet_mock', __name__, url_prefix='/neet-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@neet_bp.route('/')
@premium_required
def home():
    done = {}
    for r in neet.for_user(current_user.id):
        done.setdefault(r.mock, r)
    cat = neet.catalogue()
    return render_template('pulse/neet.html', mocks=[t for t in cat if t['kind'] == 'mock'], sets=[t for t in cat if t['kind'] == 'set'], years=[t for t in cat if t['kind'] == 'year'],
                           done=done, tr=neet.tracker(current_user.id), SEC=neet.SEC, ana=neet.analysis(), RIGHT_MARKS=neet.RIGHT_MARKS, WRONG=neet.WRONG)


def _take(t, timed):
    return render_template('pulse/neet_take.html', t=t, paper=neet.paper_for_browser(t['qids']), CONF=neet.CONF, timed=timed)


@neet_bp.route('/test/<tid>')
@premium_required
def take(tid):
    n = PulseNeetResult.query.filter_by(user_id=current_user.id, mock=tid).count()
    t = neet.compose(tid, current_user.id, n) or abort(404)
    return _take(t, request.args.get('mode') != 'practice')


@neet_bp.route('/daily')
@premium_required
def daily():
    return _take(neet.daily(current_user.id), False)


@neet_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    if (request.content_length or 0) > neet.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    known = {x['id']: x for x in neet.catalogue()}
    if tid == 'DAILY':
        t = {'id': 'DAILY', 'title': 'Daily Review'}
    elif tid in known:
        t = known[tid]
    else:
        abort(404)
    _ensure_profile()
    r, err = neet.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('neet_mock.report', rid=r.id))


@neet_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseNeetResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    own = r.user_id == current_user.id
    return render_template('pulse/neet_report.html', r=r, an=neet.analyse([r]), review=neet.review(r), CONF_LABEL=neet.CONF_LABEL, LETTERS=neet.LETTERS, own=own,
                           due=neet.tracker(current_user.id)['due'] if own else 0, WRONG=neet.WRONG, RIGHT_MARKS=neet.RIGHT_MARKS)


@neet_bp.route('/progress')
@premium_required
def progress():
    return render_template('pulse/neet_progress.html', tr=neet.tracker(current_user.id), SEC=neet.SEC, student=current_user, own=True)


@neet_bp.route('/student/<int:uid>')
@login_required
def student_progress(uid):
    from app.models import User
    prof = db.session.get(PulseProfile, uid)
    if not (current_user.is_admin or (current_user.is_staff and prof and prof.mentor_id == current_user.id)):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    return render_template('pulse/neet_progress.html', tr=neet.tracker(uid), SEC=neet.SEC, student=u, own=False)
