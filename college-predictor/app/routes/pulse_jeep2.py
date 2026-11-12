"""EduPulse-JEE Paper 2: mock tests and practice sets for JEE (Main) Paper 2A (B.Arch) and 2B (B.Planning), from the NTA papers with the official keys.

Student (Premium member):  /jee-paper2-mock/                 centre: each paper, sections, mixed Aptitude mocks, history, confidence picture
                           /jee-paper2-mock/test/<id>        the test page (questions without keys)
                           /jee-paper2-mock/submit/<id>      POST: a finished attempt, marked on the server (+4, -1, 0)
                           /jee-paper2-mock/result/<id>      report with the key: the student, their mentor, or an admin
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseJeeP2Result, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import jeep2

jeep2_bp = Blueprint('jeep2_mock', __name__, url_prefix='/jee-paper2-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@jeep2_bp.route('/')
@premium_required
def home():
    sm = jeep2.summary(current_user.id)
    done = {}
    for r in jeep2.for_user(current_user.id):
        done.setdefault(r.mock, r)                                        # newest attempt of each test
    return render_template('pulse/jeep2.html', sm=sm, tests=jeep2.tests(), done=done, CONF=jeep2.CONF, papers=jeep2.papers())


@jeep2_bp.route('/test/<tid>')
@premium_required
def take(tid):
    t = jeep2.test(tid) or abort(404)
    return render_template('pulse/jeep2_take.html', t=t, paper=jeep2.paper_for_browser(t), CONF=jeep2.CONF, timed=request.args.get('mode') != 'practice', max_marks=jeep2.max_marks(t))


@jeep2_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    t = jeep2.test(tid) or abort(404)
    if (request.content_length or 0) > jeep2.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = jeep2.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('jeep2_mock.report', rid=r.id))


@jeep2_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseJeeP2Result, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/jeep2_report.html', r=r, an=jeep2.analyse([r]), review=jeep2.review(r), CONF_LABEL=jeep2.CONF_LABEL, own=r.user_id == current_user.id)
