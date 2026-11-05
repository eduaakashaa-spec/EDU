"""EduPulse-SAT: practice SATs, section halves, domain sets and spaced reinforcement for the Digital SAT.

Student (Premium member):  /sat-mock/                 centre: practice SATs, domain sets, Daily Review, progress
                           /sat-mock/test/<id>        the test page (questions without answers); id is M-<mock> or S-<domain>
                           /sat-mock/daily            Daily Review: due review cards plus new questions from the weakest subjects
                           /sat-mock/submit/<id>      POST: a finished attempt, marked on the server (one mark per right answer)
                           /sat-mock/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                           /sat-mock/progress         tracker: subject levels, mock trend, review boxes, streak and badges
                           /sat-mock/student/<uid>    the same tracker for a mentor or admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseSatResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import sat

sat_bp = Blueprint('sat_mock', __name__, url_prefix='/sat-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@sat_bp.route('/')
@premium_required
def home():
    done = {}
    for r in sat.for_user(current_user.id):
        done.setdefault(r.mock, r)
    cat = sat.catalogue()
    return render_template('pulse/sat.html', mocks=[t for t in cat if t['kind'] == 'mock'], sets=[t for t in cat if t['kind'] == 'set'],
                           done=done, tr=sat.tracker(current_user.id), SEC=sat.SEC, st=sat.stats())


def _take(t, timed):
    return render_template('pulse/sat_take.html', t=t, paper=sat.paper_for_browser(t['qids']), CONF=sat.CONF, timed=timed)


@sat_bp.route('/test/<tid>')
@premium_required
def take(tid):
    n = PulseSatResult.query.filter_by(user_id=current_user.id, mock=tid).count()
    t = sat.compose(tid, current_user.id, n) or abort(404)
    return _take(t, request.args.get('mode') != 'practice')


@sat_bp.route('/daily')
@premium_required
def daily():
    return _take(sat.daily(current_user.id), False)


@sat_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    if (request.content_length or 0) > sat.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    known = {x['id']: x for x in sat.catalogue()}
    if tid == 'DAILY':
        t = {'id': 'DAILY', 'title': 'Daily Review'}
    elif tid in known:
        t = known[tid]
    else:
        abort(404)
    _ensure_profile()
    r, err = sat.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('sat_mock.report', rid=r.id))


@sat_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseSatResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    own = r.user_id == current_user.id
    return render_template('pulse/sat_report.html', r=r, an=sat.analyse([r]), review=sat.review(r), CONF_LABEL=sat.CONF_LABEL, LETTERS=sat.LETTERS, own=own,
                           due=sat.tracker(current_user.id)['due'] if own else 0)


@sat_bp.route('/progress')
@premium_required
def progress():
    return render_template('pulse/sat_progress.html', tr=sat.tracker(current_user.id), SEC=sat.SEC, student=current_user, own=True)


@sat_bp.route('/student/<int:uid>')
@login_required
def student_progress(uid):
    from app.models import User
    prof = db.session.get(PulseProfile, uid)
    if not (current_user.is_admin or (current_user.is_staff and prof and prof.mentor_id == current_user.id)):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    return render_template('pulse/sat_progress.html', tr=sat.tracker(uid), SEC=sat.SEC, student=u, own=False)
