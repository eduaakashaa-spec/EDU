"""EduPulse-TN Class 10: mock tests and unit tests for Tamil Nadu Class 10 (SSLC / Matriculation) Mathematics and Science, in English.

Student (Premium member):  /edupulse-tn10/                 centre: full mocks, unit tests, history, confidence picture
                           /edupulse-tn10/test/<id>        the test page (questions without answers)
                           /edupulse-tn10/submit/<id>      POST: a finished attempt, marked on the server
                           /edupulse-tn10/result/<id>      report with the key and explanations: the student, their mentor, or an admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseProfile, PulseTn10Result
from app.routes.pulse import _ensure_profile
from app.services import tn10

pulse_tn10_bp = Blueprint('pulse_tn10', __name__, url_prefix='/edupulse-tn10')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@pulse_tn10_bp.route('/')
@premium_required
def home():
    sm = tn10.summary(current_user.id)
    done = {}
    for r in tn10.for_user(current_user.id):
        done.setdefault(r.mock, r)                                        # newest attempt of each test
    return render_template('pulse/tn10.html', sm=sm, mocks=tn10.mocks(), done=done, CONF=tn10.CONF, units=tn10.units())


@pulse_tn10_bp.route('/test/<mid>')
@premium_required
def take(mid):
    m = tn10.mock(mid) or abort(404)
    return render_template('pulse/tn10_take.html', m=m, paper=tn10.paper_for_browser(m), CONF=tn10.CONF, timed=request.args.get('mode') != 'practice')


@pulse_tn10_bp.route('/submit/<mid>', methods=['POST'])
@premium_required
def submit(mid):
    m = tn10.mock(mid) or abort(404)
    if (request.content_length or 0) > tn10.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = tn10.save_result(current_user.id, m, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('pulse_tn10.report', rid=r.id))


@pulse_tn10_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseTn10Result, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/tn10_report.html', r=r, an=tn10.analyse([r]), review=tn10.review(r), CONF_LABEL=tn10.CONF_LABEL, LETTERS=tn10.LETTERS, own=r.user_id == current_user.id)
