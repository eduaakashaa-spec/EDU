"""Class 12 PCM Analytics.

Public:   /class12-pcm/                  hub: the four tools, a quick study plan, what members get
          /class12-pcm/eligibility       Eligibility Gap Closer (marks against 11 entrance routes)
          /class12-pcm/board-playbook    Board Score Playbook (levels, chapter focus, study plan)
          /class12-pcm/thumb-rules       Thumb Rules Handbook (37 chapter cards, flashcards)
          /class12-pcm/answer-lab        Answer Sheet Lab (marking-scheme answer sheets)
          /class12-pcm/quick-plan        POST: a plan for a visitor (nothing saved)
Members:  /class12-pcm/dashboard         PCM Analytics dashboard (Premium): marks, test log, chapter ratings, route status and a week-by-week plan
          /class12-pcm/dashboard/save    POST: save the profile, return the analysis
"""
import json

from flask import Blueprint, Response, abort, jsonify, render_template, request, url_for
from flask_login import current_user

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import Pcm12Profile
from app.services import pcm12

pcm_bp = Blueprint('pcm12', __name__, url_prefix='/class12-pcm')
MAX_BODY = 60_000


ENDPOINT = {'eligibility': 'pcm12.eligibility', 'board-playbook': 'pcm12.board_playbook', 'thumb-rules': 'pcm12.thumb_rules', 'answer-lab': 'pcm12.answer_lab'}


def _urls():
    u = {p: url_for(ENDPOINT[p]) for p in pcm12.PAGES}
    u['_logo'] = url_for('static', filename='images/logo.png')
    u['_contact'] = url_for('main.contact')
    return u


def _strip():
    return ('<div style="background:#0A2560;color:#fff;font:600 13px \'Plus Jakarta Sans\',system-ui,sans-serif;padding:7px 16px;display:flex;gap:16px;flex-wrap:wrap;align-items:center">'
            '<a href="%s" style="color:#fff;text-decoration:none">&larr; EduAakashaA home</a>'
            '<a href="%s" style="color:#FFB27A;text-decoration:none">Class 12 PCM Analytics</a>'
            '<span style="opacity:.8">Checked against public sources; confirm every rule on the official notice. Members also get a saved dashboard and study plan.</span></div>'
            % (url_for('main.home'), url_for('pcm12.hub')))


@pcm_bp.route('/')
def hub():
    return render_template('pcm12_hub.html', pages=pcm12.PAGES, n_chapters=len(pcm12.chapters()), n_routes=len(pcm12.routes()))


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


@pcm_bp.route('/quick-plan', methods=['POST'])
def quick_plan():
    d = request.get_json(silent=True) or {}
    try:
        level = int(d.get('level', 1))
    except (TypeError, ValueError):
        level = 1
    return jsonify(ok=True, **pcm12.quick_plan(level, d.get('exam_date'), d.get('hours_wd', 2), d.get('hours_we', 5)))


def _profile():
    row = Pcm12Profile.query.filter_by(user_id=current_user.id).first()
    try:
        return row, (json.loads(row.data_json) if row and row.data_json else {})
    except ValueError:
        return row, {}


@pcm_bp.route('/dashboard')
@premium_required
def dashboard():
    _, prof = _profile()
    return render_template('pcm12_dashboard.html', profile=prof, analysis=pcm12.analyse(prof), SUBJ=pcm12.SUBJ, LEVELS=pcm12.LEVELS, MAX=pcm12.MAX_MARKS)


@pcm_bp.route('/dashboard/save', methods=['POST'])
@premium_required
def save():
    if (request.content_length or 0) > MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    d = request.get_json(silent=True)
    if not isinstance(d, dict):
        return jsonify(ok=False, error='bad payload'), 400
    keep = {'exam_date': str(d.get('exam_date') or '')[:10], 'hours_wd': pcm12._num(d.get('hours_wd'), 14), 'hours_we': pcm12._num(d.get('hours_we'), 24), 'cat': d.get('cat') if d.get('cat') in ('g', 's', 'b') else 'g',
            'marks': {k: pcm12._num((d.get('marks') or {}).get(k), v) for k, v in pcm12.MAX_MARKS.items()} if isinstance(d.get('marks'), dict) else {},
            'tests': pcm12.clean_tests(d.get('tests')),
            'levels': {s: v for s, v in (d.get('levels') or {}).items() if s in pcm12.SUBJ and isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 3} if isinstance(d.get('levels'), dict) else {},
            'ratings': {k: v for k, v in (d.get('ratings') or {}).items() if pcm12.chapter(k) and isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 5} if isinstance(d.get('ratings'), dict) else {},
            'done': {k: True for k, v in (d.get('done') or {}).items() if v and isinstance(k, str) and len(k) < 24} if isinstance(d.get('done'), dict) else {}}
    row = Pcm12Profile.query.filter_by(user_id=current_user.id).first()
    if row is None:
        row = Pcm12Profile(user_id=current_user.id)
        db.session.add(row)
    row.data_json = json.dumps(keep, separators=(',', ':'))
    db.session.commit()
    return jsonify(ok=True, analysis=pcm12.analyse(keep))
