"""Class 12 PCM and PCB Analytics.

PCM, public:   /class12-pcm/                  hub: the four tools, a quick study plan, what members get
               /class12-pcm/eligibility       Eligibility Gap Closer (marks against 11 entrance routes)
               /class12-pcm/board-playbook    Board Score Playbook (levels, chapter focus, study plan)
               /class12-pcm/thumb-rules       Thumb Rules Handbook (37 chapter cards, flashcards)
               /class12-pcm/answer-lab        Answer Sheet Lab (marking-scheme answer sheets)
               /class12-pcm/quick-plan        POST: a plan for a visitor (nothing saved)
PCB, public:   /class12-pcb/                  hub: eligibility check, board playbook, thumb rules, answer lab, quick study plan
               /class12-pcb/eligibility       POST: marks against the PCB routes (nothing saved)
               /class12-pcb/quick-plan        POST: a plan for a visitor (nothing saved)
Members (Premium), for each stream:
               /class12-<stream>/dashboard        marks, test log, chapter ratings, route status and a week-by-week plan
               /class12-<stream>/dashboard/save   POST: save the profile, return the analysis
"""
import json

from flask import Blueprint, Response, abort, jsonify, render_template, request, url_for
from flask_login import current_user

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import Class12Profile
from app.services import pcm12

MAX_BODY = 60_000
TOOL_ENDPOINT = {'eligibility': 'pcm12.eligibility', 'board-playbook': 'pcm12.board_playbook', 'thumb-rules': 'pcm12.thumb_rules', 'answer-lab': 'pcm12.answer_lab'}


def _stream_routes(bp, stream, ep):
    """Quick plan, dashboard and save for one stream; `ep` is the blueprint name."""
    c = pcm12.cfg(stream)

    @bp.route('/quick-plan', methods=['POST'], endpoint='quick_plan')
    def quick_plan():
        d = request.get_json(silent=True) or {}
        try:
            level = int(d.get('level', 1))
        except (TypeError, ValueError):
            level = 1
        return jsonify(ok=True, **pcm12.quick_plan(level, d.get('exam_date'), d.get('hours_wd', 2), d.get('hours_we', 5), stream=stream))

    def _profile():
        row = Class12Profile.query.filter_by(user_id=current_user.id, stream=stream).first()
        try:
            return row, (json.loads(row.data_json) if row and row.data_json else {})
        except ValueError:
            return row, {}

    @bp.route('/dashboard', endpoint='dashboard')
    @premium_required
    def dashboard():
        _, prof = _profile()
        conf = {'stream': stream, 'name': c['name'], 'order': list(c['order']), 'subj': c['subj'], 'labels': c['labels'], 'marks': c['marks'], 'marks_order': list(c['marks']), 'test_max': c['test_max'], 'cats': c['cats'],
                'save': url_for(ep + '.save'), 'hub': url_for(ep + '.hub'),
                'links': {'thumb': url_for('pcm12.thumb_rules') if stream == 'pcm' else url_for('pcb12.hub') + '#rules', 'elig': url_for('pcm12.eligibility') if stream == 'pcm' else url_for('pcb12.hub') + '#eligibility'}}
        return render_template('pcm12_dashboard.html', conf=conf, profile=prof, analysis=pcm12.analyse(prof, stream=stream))

    @bp.route('/dashboard/save', methods=['POST'], endpoint='save')
    @premium_required
    def save():
        if (request.content_length or 0) > MAX_BODY:
            return jsonify(ok=False, error='too large'), 413
        d = request.get_json(silent=True)
        if not isinstance(d, dict):
            return jsonify(ok=False, error='bad payload'), 400
        keep = pcm12.clean_profile(d, stream)
        row = Class12Profile.query.filter_by(user_id=current_user.id, stream=stream).first()
        if row is None:
            row = Class12Profile(user_id=current_user.id, stream=stream)
            db.session.add(row)
        row.data_json = json.dumps(keep, separators=(',', ':'))
        db.session.commit()
        return jsonify(ok=True, analysis=pcm12.analyse(keep, stream=stream))


# ---- PCM ---------------------------------------------------------------------------------------------------------------------------------
pcm_bp = Blueprint('pcm12', __name__, url_prefix='/class12-pcm')


def _urls():
    u = {p: url_for(TOOL_ENDPOINT[p]) for p in pcm12.PAGES}
    u['_logo'] = url_for('static', filename='images/logo.png')
    u['_contact'] = url_for('main.contact')
    return u


def _strip():
    return ('<div style="background:#0A2560;color:#fff;font:600 13px \'Plus Jakarta Sans\',system-ui,sans-serif;padding:7px 16px;display:flex;gap:16px;flex-wrap:wrap;align-items:center">'
            '<a href="%s" style="color:#fff;text-decoration:none">&larr; EduAakashaA home</a>'
            '<a href="%s" style="color:#FFB27A;text-decoration:none">Class 12 PCM Analytics</a>'
            '<span style="opacity:.8">Checked against public sources; confirm every rule on the official notice. Members also get a saved dashboard and study plan.</span></div>'
            % (url_for('main.home'), url_for('pcm12.hub')))


@pcm_bp.route('/', endpoint='hub')
def pcm_hub():
    return render_template('pcm12_hub.html', pages=pcm12.PAGES, n_chapters=len(pcm12.chapters('pcm')), n_routes=len(pcm12.routes('pcm')))


def _tool(name):
    html = pcm12.page_html(name, _urls(), _strip())
    if html is None:
        abort(404)
    return Response(html, mimetype='text/html')


@pcm_bp.route('/eligibility')
def eligibility():
    return _tool('eligibility')


@pcm_bp.route('/board-playbook')
def board_playbook():
    return _tool('board-playbook')


@pcm_bp.route('/thumb-rules')
def thumb_rules():
    return _tool('thumb-rules')


@pcm_bp.route('/answer-lab')
def answer_lab():
    return _tool('answer-lab')


_stream_routes(pcm_bp, 'pcm', 'pcm12')

# ---- PCB ---------------------------------------------------------------------------------------------------------------------------------
pcb_bp = Blueprint('pcb12', __name__, url_prefix='/class12-pcb')


@pcb_bp.route('/', endpoint='hub')
def pcb_hub():
    from app.data import pcb12
    return render_template('pcb12_hub.html', **pcb12.context())


@pcb_bp.route('/eligibility', methods=['POST'], endpoint='eligibility')
def pcb_eligibility():
    d = request.get_json(silent=True) or {}
    return jsonify(ok=True, elig=pcm12.eligibility(d.get('marks') if isinstance(d.get('marks'), dict) else {}, d.get('cat', 'g'), 'pcb'))


_stream_routes(pcb_bp, 'pcb', 'pcb12')
