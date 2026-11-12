"""EduPulse-BITSAT: mock tests and practice sets for the BITSAT, built from the previous-year papers (memory-based papers with the published keys).

Student (Premium member):  /bitsat-mock/                 centre: each year's paper, full 130-question mocks, subject sets, history, confidence picture
                           /bitsat-mock/test/<id>        the test page (questions without answers)
                           /bitsat-mock/submit/<id>      POST: a finished attempt, marked on the server (+3, -1, 0)
                           /bitsat-mock/result/<id>      report with the key: the student, their mentor, or an admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseBitsatResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import bitsat

bitsat_bp = Blueprint('bitsat_mock', __name__, url_prefix='/bitsat-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@bitsat_bp.route('/')
@premium_required
def home():
    sm = bitsat.summary(current_user.id)
    done = {}
    for r in bitsat.for_user(current_user.id):
        done.setdefault(r.mock, r)                                        # newest attempt of each test
    return render_template('pulse/bitsat.html', sm=sm, tests=bitsat.tests(), done=done, CONF=bitsat.CONF, papers=bitsat.papers(), SUBJECTS=bitsat.SUBJECTS)


@bitsat_bp.route('/test/<tid>')
@premium_required
def take(tid):
    t = bitsat.test(tid) or abort(404)
    return render_template('pulse/bitsat_take.html', t=t, paper=bitsat.paper_for_browser(t), CONF=bitsat.CONF, timed=request.args.get('mode') != 'practice')


@bitsat_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    t = bitsat.test(tid) or abort(404)
    if (request.content_length or 0) > bitsat.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = bitsat.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('bitsat_mock.report', rid=r.id))


@bitsat_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseBitsatResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/bitsat_report.html', r=r, an=bitsat.analyse([r]), review=bitsat.review(r), CONF_LABEL=bitsat.CONF_LABEL, LETTERS=bitsat.LETTERS, own=r.user_id == current_user.id)
