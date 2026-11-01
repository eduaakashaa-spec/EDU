"""EduPulse-IAT: mock tests and practice sets for the IISER Aptitude Test (IAT), built from the released papers 2021 to 2026.

Student (Premium member):  /iiser-mock/                 centre: full mocks, year practice sets, subject sections, history, confidence picture
                           /iiser-mock/test/<id>        the test page (questions without answers)
                           /iiser-mock/submit/<id>      POST: a finished attempt, marked on the server (+4, -1, 0)
                           /iiser-mock/result/<id>      report with the key and worked solutions: the student, their mentor, or an admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseIatResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import iat

iat_bp = Blueprint('iat', __name__, url_prefix='/iiser-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@iat_bp.route('/')
@premium_required
def home():
    sm = iat.summary(current_user.id)
    done = {}
    for r in iat.for_user(current_user.id):
        done.setdefault(r.mock, r)                                        # newest attempt of each test
    return render_template('pulse/iat.html', sm=sm, tests=iat.tests(), done=done, CONF=iat.CONF, papers=iat.papers(), SUBJECTS=iat.SUBJECTS)


@iat_bp.route('/solutions/<int:year>')
@premium_required
def solutions(year):
    """Every question of a released paper with its worked solution, as printed (the first option is the official answer)."""
    qs = [q for q in iat.bank() if q['year'] == year] or abort(404)
    return render_template('pulse/iat_solutions.html', year=year, qs=qs, subjects=iat.SUBJECTS, asset=iat.asset, papers=iat.papers())


@iat_bp.route('/test/<tid>')
@premium_required
def take(tid):
    t = iat.test(tid) or abort(404)
    return render_template('pulse/iat_take.html', t=t, paper=iat.paper_for_browser(t), CONF=iat.CONF, timed=request.args.get('mode') != 'practice')


@iat_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    t = iat.test(tid) or abort(404)
    if (request.content_length or 0) > iat.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = iat.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('iat.report', rid=r.id))


@iat_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseIatResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/iat_report.html', r=r, an=iat.analyse([r]), review=iat.review(r), CONF_LABEL=iat.CONF_LABEL, LETTERS=iat.LETTERS, own=r.user_id == current_user.id)
