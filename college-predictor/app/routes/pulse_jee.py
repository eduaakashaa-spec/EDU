"""EduPulse-JEE: JEE Main mock test centre (EduAakashaa practice mocks + NTA previous-year papers once their answer keys are added).

Student (Premium member):  /edupulse-jee/            centre, history, confidence and negative-marking summary
                           /edupulse-jee/app          the test page (served with the member's name and the results endpoint injected)
                           /edupulse-jee/data/<name>  paper files (members only; never under /static)
                           /edupulse-jee/results      POST: a finished attempt
                           /edupulse-jee/result/<id>  report (+ .pdf): student, their mentor, or admin
"""
import json
import os

from flask import Blueprint, Response, abort, jsonify, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseJeeResult, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import pulse_jee as pj

pulse_jee_bp = Blueprint('pulse_jee', __name__, url_prefix='/edupulse-jee')
_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'jee_mock')
_html = {}


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@pulse_jee_bp.route('/')
@premium_required
def home():
    sm = pj.summary(current_user.id)
    return render_template('pulse/jee.html', sm=sm, CONF=pj.CONF, CONF_LABEL=pj.CONF_LABEL, SUBJ=pj.SUBJ, BREAK_EVEN=pj.BREAK_EVEN, papers=pj.papers())


@pulse_jee_bp.route('/app')
@premium_required
def app_page():
    if 'html' not in _html:
        with open(os.path.join(_DIR, 'app.html'), encoding='utf-8') as f:
            _html['html'] = f.read()
    cfg = {'memberName': current_user.name or '', 'memberId': 'EA%d' % current_user.id, 'resultsEndpoint': url_for('pulse_jee.results'),
           'dataPath': url_for('pulse_jee.data', name='x.json').rsplit('/', 1)[0] + '/'}
    tag = '<script>window.EA_CONFIG = window.EA_CONFIG || {};</script>'
    html = _html['html'].replace(tag, '<script>window.EA_CONFIG = ' + json.dumps(cfg).replace('</', '<\\/') + ';</script>', 1)
    resp = Response(html, mimetype='text/html')
    resp.headers['Cache-Control'] = 'private, no-store'
    return resp


@pulse_jee_bp.route('/data/<name>')
@premium_required
def data(name):
    stem = name[:-5] if name.endswith('.json') else ''
    if stem != 'index' and stem not in pj.valid_papers():
        abort(404)                                             # unknown papers, and previous-year papers whose answer key has not been added
    resp = send_from_directory(os.path.join(_DIR, 'data'), name, mimetype='application/json', max_age=3600)
    resp.headers['Cache-Control'] = 'private, max-age=3600'
    return resp


@pulse_jee_bp.route('/results', methods=['POST'])
@premium_required
def results():
    if (request.content_length or 0) > pj.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = pj.save_result(current_user.id, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id)


@pulse_jee_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseJeeResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return render_template('pulse/jee_report.html', r=r, p=json.loads(r.payload_json or '{}'), an=pj.analyse([r]), CONF=pj.CONF, SUBJ=pj.SUBJ, BREAK_EVEN=pj.BREAK_EVEN, own=r.user_id == current_user.id)


@pulse_jee_bp.route('/result/<int:rid>.pdf')
@login_required
def report_pdf(rid):
    r = db.session.get(PulseJeeResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    return Response(pj.pdf(r, r.user.name), mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename=jee-mock-%s-%d.pdf' % (r.paper, r.id)})
