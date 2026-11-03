"""EduPulse-NID: mock tests and practice for the NID Design Aptitude Test (B.Des Prelims and M.Des CDAT Paper 1 formats).

Student (Premium member):  /nid-mock/                 centre: B.Des and M.Des mocks, NID official sample papers, section sets, studio practice, history, confidence picture
                           /nid-mock/test/<id>        the test page (questions without answers)
                           /nid-mock/submit/<id>      POST: a finished attempt, marked on the server (marks printed on each question, nothing deducted)
                           /nid-mock/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                           /nid-mock/studio           the open drawing and studio tasks with a self-assessment rubric (no marking here)
"""
from flask import Blueprint, abort, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseNidResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import nid

nid_bp = Blueprint('nid_mock', __name__, url_prefix='/nid-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@nid_bp.route('/')
@premium_required
def home():
    sm = nid.summary(current_user.id)
    done = {}
    for r in nid.for_user(current_user.id):
        done.setdefault(r.mock, r)                                        # newest attempt of each test
    return render_template('pulse/nid.html', sm=sm, tests=nid.tests(), done=done, CONF=nid.CONF, tasks=nid.tasks(), ana=nid.analysis(), SEC=nid.SEC)


@nid_bp.route('/test/<tid>')
@premium_required
def take(tid):
    t = nid.test(tid) or abort(404)
    return render_template('pulse/nid_take.html', t=t, paper=nid.paper_for_browser(t), CONF=nid.CONF, timed=request.args.get('mode') != 'practice')


@nid_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    t = nid.test(tid) or abort(404)
    if (request.content_length or 0) > nid.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = nid.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('nid_mock.report', rid=r.id))


@nid_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseNidResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/nid_report.html', r=r, an=nid.analyse([r]), review=nid.review(r), CONF_LABEL=nid.CONF_LABEL, LETTERS=nid.LETTERS, own=r.user_id == current_user.id)


@nid_bp.route('/studio')
@premium_required
def studio():
    return render_template('pulse/nid_studio.html', tasks=nid.tasks())


@nid_bp.route('/studio/<tid>')
@premium_required
def studio_task(tid):
    t = next((x for x in nid.tasks() if x['id'] == tid), None) or abort(404)
    return render_template('pulse/nid_task.html', t=t, tasks=nid.tasks())
