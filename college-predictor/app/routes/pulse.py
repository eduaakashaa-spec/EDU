"""EduPulse-UCEED — chapter-wise MCQ practice, progress dashboard, mentor view, question-bank admin and e-mail reports.

Student (Premium member):  /edupulse-uceed/              dashboard · register · start a set · attempt · result
Mentor / admin:            /edupulse-uceed/mentor        linked students' progress
Admin:                     /edupulse-uceed/admin         question bank (add / import / publish), students, report sending
Scheduler:                 /edupulse-uceed/cron/reports  token-protected; call weekly (see EDUPULSE_UCEED.md)
"""
import hmac
import os

from flask import (Blueprint, Response, abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required

from app.decorators import admin_required, premium_required, staff_required
from app.extensions import db
from app.models import User
from app.models_pulse import (PulseAnswer, PulseAttempt, PulseChapter, PulseProfile, PulseQuestion)
from app.services import mailer
from app.services import pulse as svc

pulse_bp = Blueprint('pulse', __name__, url_prefix='/edupulse-uceed')

MAX_IMG = 500 * 1024
IMG_TYPES = [(b'\xff\xd8\xff', 'image/jpeg'), (b'\x89PNG\r\n\x1a\n', 'image/png')]


def _s(name, n=2000):
    return (request.form.get(name) or '').strip()[:n]


def _chapter_by_key(key):
    return PulseChapter.query.filter_by(key=key, active=True).first()


# --------------------------------------------------------------------------- #
# student
# --------------------------------------------------------------------------- #
@pulse_bp.route('/')
@premium_required
def home():
    svc.ensure_chapters()
    prof = db.session.get(PulseProfile, current_user.id)
    rows = svc.chapter_stats(current_user.id)
    ov = svc.overall(current_user.id)
    published = PulseQuestion.query.filter_by(status='published').count()
    return render_template('pulse/home.html', prof=prof, rows=rows, ov=ov, streak=svc.streak(current_user.id), tips=svc.advice(rows, ov),
                           recent=list(reversed(ov['list']))[:8], published=published, SET_SIZES=svc.SET_SIZES, mail_ready=mailer.is_configured(),
                           practice_score=svc.practice_score)


@pulse_bp.route('/register', methods=['POST'])
@premium_required
def register():
    prof = db.session.get(PulseProfile, current_user.id) or PulseProfile(user_id=current_user.id)
    prof.student_class = _s('student_class', 30) or prof.student_class
    pe = _s('parent_email', 200).lower()
    if pe and ('@' not in pe or '.' not in pe.split('@')[-1]):
        flash('Enter a valid parent email, or leave it blank.', 'danger')
        return redirect(url_for('pulse.home') + '#settings')
    prof.parent_email = pe or None
    prof.parent_consent = bool(pe) and request.form.get('parent_consent') == '1'
    prof.frequency = request.form.get('frequency') if request.form.get('frequency') in ('weekly', 'monthly', 'off') else 'weekly'
    prof.email_results = request.form.get('email_results') == '1'
    if prof.mentor_id is None:                                    # link the EA mentor from the mentorship record, if there is one
        try:
            from app.models_mentorship import MsEnrolment
            e = MsEnrolment.query.filter_by(student_id=current_user.id, status='Active').first()
            if e and e.mentor_id:
                prof.mentor_id = e.mentor_id
        except Exception:
            pass
    db.session.add(prof)
    db.session.commit()
    flash('EduPulse settings saved.' + (' Parent emails are ON.' if prof.parent_consent else ''), 'success')
    return redirect(url_for('pulse.home'))


@pulse_bp.route('/start', methods=['POST'])
@premium_required
def start():
    svc.ensure_chapters()
    if db.session.get(PulseProfile, current_user.id) is None:
        flash('Please register for EduPulse first (one short form).', 'info')
        return redirect(url_for('pulse.home') + '#settings')
    key = request.form.get('chapter', 'mixed')
    chapter = None if key == 'mixed' else _chapter_by_key(key)
    if key != 'mixed' and chapter is None:
        abort(404)
    n = request.form.get('count', type=int)
    n = n if n in svc.SET_SIZES else 10
    mode = 'timed' if request.form.get('mode') == 'timed' else 'practice'
    att = svc.start_attempt(current_user, chapter, n, mode, request.form.get('difficulty'))
    if att is None:
        flash('No published questions match yet. Try another chapter or difficulty — or ask the team to add more.', 'info')
        return redirect(url_for('pulse.home'))
    return redirect(url_for('pulse.attempt', aid=att.id))


def _own_attempt(aid):
    att = db.session.get(PulseAttempt, aid) or abort(404)
    if att.user_id != current_user.id:
        abort(404)
    return att


@pulse_bp.route('/attempt/<int:aid>')
@premium_required
def attempt(aid):
    att = _own_attempt(aid)
    if att.submitted_at:
        return redirect(url_for('pulse.result', aid=att.id))
    items = att.answers.order_by(PulseAnswer.position).all()            # the correct answers are NOT rendered in this page
    return render_template('pulse/attempt.html', att=att, items=items)


@pulse_bp.route('/attempt/<int:aid>/submit', methods=['POST'])
@premium_required
def submit(aid):
    att = _own_attempt(aid)
    if att.submitted_at:
        return redirect(url_for('pulse.result', aid=att.id))
    svc.submit_attempt(att, request.form)
    svc.send_result_email(att)
    return redirect(url_for('pulse.result', aid=att.id))


@pulse_bp.route('/attempt/<int:aid>/result')
@premium_required
def result(aid):
    att = _own_attempt(aid)
    if not att.submitted_at:
        return redirect(url_for('pulse.attempt', aid=att.id))
    items = att.answers.order_by(PulseAnswer.position).all()
    by_ch = {}
    for a in items:
        d = by_ch.setdefault(a.question.chapter.title, [0, 0])
        d[1] += 1
        d[0] += 1 if a.is_correct else 0
    return render_template('pulse/result.html', att=att, items=items, by_ch=by_ch, score=svc.practice_score(att))


@pulse_bp.route('/q/<int:qid>/image')
@login_required
def question_image(qid):
    q = db.session.get(PulseQuestion, qid)
    if not q or not q.has_image or (q.status != 'published' and not current_user.is_staff):
        abort(404)
    resp = Response(q.image_data, mimetype=q.image_mime)
    resp.headers['Cache-Control'] = 'private, max-age=600'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


# --------------------------------------------------------------------------- #
# mentor / admin views of student progress
# --------------------------------------------------------------------------- #
def _my_students():
    q = PulseProfile.query
    if not current_user.is_admin:
        q = q.filter(PulseProfile.mentor_id == current_user.id)
    return q.all()


@pulse_bp.route('/mentor')
@staff_required
def mentor_home():
    rows = []
    for p in _my_students():
        ov = svc.overall(p.user_id)
        ch = svc.chapter_stats(p.user_id)
        from app.services import pulse_mock as pm
        rows.append({'p': p, 'ov': ov, 'weak': [r for r in ch if r['level'] == 'weak'], 'streak': svc.streak(p.user_id), 'mock': pm.summary(p.user_id)})
    rows.sort(key=lambda r: (r['ov']['last'] is None, r['ov']['last'] and -r['ov']['last'].timestamp()))
    return render_template('pulse/mentor.html', rows=rows)


@pulse_bp.route('/mentor/<int:uid>')
@staff_required
def mentor_student(uid):
    p = db.session.get(PulseProfile, uid) or abort(404)
    if not current_user.is_admin and p.mentor_id != current_user.id:
        abort(404)
    rows, ov = svc.chapter_stats(uid), svc.overall(uid)
    from app.services import pulse_mock as pm
    return render_template('pulse/mentor_student.html', mock=pm.summary(uid), CONF=pm.CONF, p=p, rows=rows, ov=ov, streak=svc.streak(uid), tips=svc.advice(rows, ov),
                           recent=list(reversed(ov['list']))[:15], practice_score=svc.practice_score)


# --------------------------------------------------------------------------- #
# admin: question bank, students, reports
# --------------------------------------------------------------------------- #
@pulse_bp.route('/admin')
@admin_required
def admin_home():
    svc.ensure_chapters()
    chapters = PulseChapter.query.order_by(PulseChapter.position).all()
    ch = request.args.get('chapter')
    status = request.args.get('status')
    q = PulseQuestion.query
    if ch:
        q = q.filter(PulseQuestion.chapter_id == int(ch)) if ch.isdigit() else q
    if status in ('draft', 'published'):
        q = q.filter(PulseQuestion.status == status)
    counts = {c.id: (c.questions.filter_by(status='published').count(), c.questions.count()) for c in chapters}
    students = PulseProfile.query.all()
    mentors = User.query.filter(User.tier.in_(['ea_mentor', 'admin'])).order_by(User.name).all()
    return render_template('admin/pulse_admin.html', admin_tab='pulse', chapters=chapters, counts=counts, questions=q.order_by(PulseQuestion.id.desc()).limit(200).all(),
                           ch=ch, status=status, students=students, mentors=mentors, mail_ready=mailer.is_configured(), csv_cols=svc.CSV_COLUMNS,
                           starter=len(svc.STARTER))


@pulse_bp.route('/admin/seed', methods=['POST'])
@admin_required
def admin_seed():
    n = svc.seed_starter()
    flash(f'{n} original practice question(s) added and published.' if n else 'The starter bank is already loaded.', 'success')
    return redirect(url_for('pulse.admin_home'))


@pulse_bp.route('/admin/import', methods=['POST'])
@admin_required
def admin_import():
    f = request.files.get('file')
    if not f or not f.filename.lower().endswith('.csv'):
        flash('Upload a .csv file.', 'danger')
        return redirect(url_for('pulse.admin_home'))
    raw = f.read(2_000_000)
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        flash('The file must be UTF-8 encoded.', 'danger')
        return redirect(url_for('pulse.admin_home'))
    n, errors = svc.import_csv(text)
    if errors:
        flash('Nothing was imported. ' + ' · '.join(errors), 'danger')
    else:
        flash(f'{n} question(s) imported as drafts — review and publish them.', 'success')
    return redirect(url_for('pulse.admin_home'))


@pulse_bp.route('/admin/export.csv')
@admin_required
def admin_export():
    return Response(svc.export_csv(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename="edupulse-uceed-questions.csv"'})


@pulse_bp.route('/admin/question', methods=['GET', 'POST'], defaults={'qid': None})
@pulse_bp.route('/admin/question/<int:qid>', methods=['GET', 'POST'])
@admin_required
def admin_question(qid):
    q = db.session.get(PulseQuestion, qid) if qid else None
    if qid and not q:
        abort(404)
    chapters = PulseChapter.query.order_by(PulseChapter.position).all()
    if request.method == 'POST':
        corr = _s('correct', 1).upper()
        opts = [_s(f'option_{k}', 400) for k in 'abcd']
        ch = db.session.get(PulseChapter, request.form.get('chapter_id', type=int) or 0)
        if not (_s('stem') and all(opts) and corr in 'ABCD' and corr and ch):
            flash('Chapter, question, four options and the correct answer are required.', 'danger')
            return render_template('admin/pulse_question.html', admin_tab='pulse', q=q, chapters=chapters, form=request.form)
        q = q or PulseQuestion()
        q.chapter_id, q.stem, q.correct = ch.id, _s('stem'), corr
        q.option_a, q.option_b, q.option_c, q.option_d = opts
        q.explanation, q.source, q.year = _s('explanation'), _s('source', 160) or 'EduAakashaA original practice question', _s('year', 8) or None
        q.difficulty = request.form.get('difficulty') if request.form.get('difficulty') in ('Easy', 'Medium', 'Hard') else 'Medium'
        q.status = 'published' if request.form.get('publish') == '1' else 'draft'
        img = request.files.get('image')
        if img and img.filename:
            data = img.read(MAX_IMG + 1)
            mime = next((m for sig, m in IMG_TYPES if data.startswith(sig)), None) or ('image/webp' if data[:4] == b'RIFF' and data[8:12] == b'WEBP' else None)
            if not data or len(data) > MAX_IMG or not mime:
                flash('The image must be a JPG, PNG or WebP under 500 KB.', 'danger')
                return render_template('admin/pulse_question.html', admin_tab='pulse', q=q, chapters=chapters, form=request.form)
            q.image_data, q.image_mime = data, mime
        elif request.form.get('remove_image') == '1':
            q.image_data, q.image_mime = None, None
        db.session.add(q)
        db.session.commit()
        flash('Question saved.' + (' It is live for students.' if q.status == 'published' else ' It is a draft — publish it when ready.'), 'success')
        return redirect(url_for('pulse.admin_home', chapter=q.chapter_id))
    return render_template('admin/pulse_question.html', admin_tab='pulse', q=q, chapters=chapters, form=None)


@pulse_bp.route('/admin/question/<int:qid>/<op>', methods=['POST'])
@admin_required
def admin_question_op(qid, op):
    q = db.session.get(PulseQuestion, qid) or abort(404)
    if op == 'toggle':
        q.status = 'draft' if q.status == 'published' else 'published'
    elif op == 'delete':
        if PulseAnswer.query.filter_by(question_id=q.id).count():
            q.status = 'draft'                                          # keep history intact: hide instead of deleting answered questions
            flash('This question has student answers, so it was unpublished instead of deleted.', 'info')
        else:
            db.session.delete(q)
    else:
        abort(404)
    db.session.commit()
    return redirect(request.referrer or url_for('pulse.admin_home'))


@pulse_bp.route('/admin/mentor', methods=['POST'])
@admin_required
def admin_assign_mentor():
    p = db.session.get(PulseProfile, request.form.get('user_id', type=int) or 0) or abort(404)
    m = db.session.get(User, request.form.get('mentor_id', type=int) or 0) if request.form.get('mentor_id') else None
    if m and not (m.is_ea_mentor or m.is_admin):
        flash('That account is not an EA Mentor.', 'danger')
    else:
        p.mentor_id = m.id if m else None
        db.session.commit()
        flash('Mentor updated.', 'success')
    return redirect(url_for('pulse.admin_home') + '#students')


@pulse_bp.route('/admin/send-reports', methods=['POST'])
@admin_required
def admin_send_reports():
    if not mailer.is_configured():
        flash('Email sending is not configured on this server (set RESEND_API_KEY or SMTP). Nothing was sent.', 'danger')
        return redirect(url_for('pulse.admin_home') + '#students')
    uid = request.form.get('user_id', type=int)
    if uid:
        p = db.session.get(PulseProfile, uid) or abort(404)
        sent = svc.send_digest(p)
        flash('Progress report queued to: ' + (', '.join(sent) or 'nobody'), 'success')
    else:
        flash(f'{svc.send_due_reports()} due report(s) queued.', 'success')
    return redirect(url_for('pulse.admin_home') + '#students')


@pulse_bp.route('/cron/reports', methods=['GET', 'POST'])
def cron_reports():
    """Call weekly from a scheduler: GET /edupulse-uceed/cron/reports?token=…  (env PULSE_CRON_TOKEN)."""
    token = os.environ.get('PULSE_CRON_TOKEN', '')
    given = request.args.get('token') or request.headers.get('X-Cron-Token', '')
    if not token or not hmac.compare_digest(token, given):
        abort(404)
    if not mailer.is_configured():
        return {'ok': False, 'sent': 0, 'note': 'mail transport not configured'}, 200
    return {'ok': True, 'sent': svc.send_due_reports()}


# --------------------------------------------------------------------------- #
# UCEED Mock Test Centre (previous-year papers + EduAakashaa practice papers, confidence check, reports)
# --------------------------------------------------------------------------- #
_MOCK_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'uceed_mock')
_mock_html = {}


def _can_see_mock(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


def _ensure_profile():
    """Taking a mock makes the student visible to their mentor, without turning on any e-mail digests they did not ask for."""
    prof = db.session.get(PulseProfile, current_user.id)
    if prof is None:
        prof = PulseProfile(user_id=current_user.id, frequency='off', email_results=False, parent_consent=False)
        try:
            from app.models_mentorship import MsEnrolment
            e = MsEnrolment.query.filter_by(student_id=current_user.id, status='Active').first()
            if e and e.mentor_id:
                prof.mentor_id = e.mentor_id
        except Exception:
            pass
        db.session.add(prof)
        db.session.commit()
    return prof


@pulse_bp.route('/mock')
@premium_required
def mock_home():
    from app.services import pulse_mock as pm
    sm = pm.summary(current_user.id)
    return render_template('pulse/mock.html', sm=sm, CONF=pm.CONF, CONF_LABEL=pm.CONF_LABEL)


@pulse_bp.route('/mock/app')
@premium_required
def mock_app():
    """The Mock Test Centre page (one HTML file). The member name and the results endpoint are injected so every attempt is saved to the account."""
    import json
    if 'html' not in _mock_html:
        with open(os.path.join(_MOCK_DIR, 'app.html'), encoding='utf-8') as f:
            _mock_html['html'] = f.read()
    cfg = {'memberName': current_user.name or '', 'memberId': 'EA%d' % current_user.id, 'resultsEndpoint': url_for('pulse.mock_results'),
           'dataPath': url_for('pulse.mock_data', name='x.json').rsplit('/', 1)[0] + '/'}
    tag = '<script>window.EA_CONFIG = window.EA_CONFIG || {};</script>'
    inject = '<script>window.EA_CONFIG = ' + json.dumps(cfg).replace('</', '<\/') + ';</script>'
    html = _mock_html['html'].replace(tag, inject, 1)
    resp = Response(html, mimetype='text/html')
    resp.headers['Cache-Control'] = 'private, no-store'
    return resp


@pulse_bp.route('/mock/data/<name>')
@premium_required
def mock_data(name):
    import re
    from flask import send_from_directory
    if not re.fullmatch(r'(20(1[89]|2[0-6])|M[1-5])\.json', name):
        abort(404)
    resp = send_from_directory(os.path.join(_MOCK_DIR, 'data'), name, mimetype='application/json', max_age=3600)
    resp.headers['Cache-Control'] = 'private, max-age=3600'
    return resp


@pulse_bp.route('/mock/results', methods=['POST'])
@premium_required
def mock_results():
    from flask import jsonify
    from app.services import pulse_mock as pm
    if (request.content_length or 0) > pm.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    _ensure_profile()
    r, err = pm.save_result(current_user.id, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id)


@pulse_bp.route('/mock/result/<int:rid>')
@login_required
def mock_report(rid):
    from app.models_pulse import PulseMockResult
    from app.services import pulse_mock as pm
    r = db.session.get(PulseMockResult, rid) or abort(404)
    if not _can_see_mock(r):
        abort(404)
    import json
    return render_template('pulse/mock_report.html', r=r, p=json.loads(r.payload_json or '{}'), an=pm.analyse([r]), CONF=pm.CONF, own=r.user_id == current_user.id)


@pulse_bp.route('/mock/result/<int:rid>.pdf')
@login_required
def mock_report_pdf(rid):
    from app.models_pulse import PulseMockResult
    from app.services import pulse_mock as pm
    r = db.session.get(PulseMockResult, rid) or abort(404)
    if not _can_see_mock(r):
        abort(404)
    return Response(pm.pdf(r, r.user.name), mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename=uceed-mock-%s-%d.pdf' % (r.paper, r.id)})
