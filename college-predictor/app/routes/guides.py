"""Free student guides — a public library of downloadable files, gated by email.

Public:
    GET  /free-guides                         tiles of every active guide
    POST /free-guides/<id>/request            name + email -> a personal download link
    GET  /free-guides/get/<token>             the file (token is signed, 48 h)

Admin (admin tier):
    GET  /admin/free-guides                   upload + manage (tiles)
    POST /admin/free-guides/upload            new guide
    POST /admin/free-guides/<id>/update       edit details / replace the file
    POST /admin/free-guides/<id>/toggle       show / hide
    POST /admin/free-guides/<id>/delete
    GET  /admin/free-guides/<id>/file         preview / download as admin
    GET  /admin/free-guides/downloads         who downloaded what (+ ?csv=1)
"""
import csv
import io
import re

from flask import (Blueprint, Response, abort, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.decorators import admin_required
from app.extensions import db
from app.models import FreeGuide, GuideDownload, PageLead

guides_bp = Blueprint('guides', __name__)

CATEGORIES = ['General', 'NRI & DASA', 'JEE & JoSAA', 'TNEA & State', 'Boards & Exams',
              'Stream & Career', 'Design & Architecture', 'MBA & PG']
ALLOWED = {
    'pdf': ('application/pdf', b'%PDF-'),
    'docx': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', b'PK\x03\x04'),
    'xlsx': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', b'PK\x03\x04'),
    'pptx': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', b'PK\x03\x04'),
}
MAX_BYTES = 9 * 1024 * 1024
_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]{2,}$')
TOKEN_AGE = 48 * 3600


def _serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='free-guide-download')


def _read_upload(storage):
    """-> (data, mime, filename, error)"""
    if storage is None or not storage.filename:
        return None, None, None, 'Choose a file to upload.'
    ext = storage.filename.rsplit('.', 1)[-1].lower() if '.' in storage.filename else ''
    if ext not in ALLOWED:
        return None, None, None, 'Upload a PDF (or a Word / Excel / PowerPoint file).'
    data = storage.read(MAX_BYTES + 1)
    if not data:
        return None, None, None, 'The file was empty.'
    if len(data) > MAX_BYTES:
        return None, None, None, 'File is larger than 9 MB — please compress it.'
    mime, magic = ALLOWED[ext]
    if not data.startswith(magic):
        return None, None, None, f'That file does not look like a valid .{ext}.'
    safe = re.sub(r'[^A-Za-z0-9._ -]+', '_', storage.filename)[:200] or f'guide.{ext}'
    return data, mime, safe, None


def _size_label(n):
    n = n or 0
    return f'{n / 1024:.0f} KB' if n < 1024 * 1024 else f'{n / (1024 * 1024):.1f} MB'


# --------------------------------------------------------------------------- #
# public
# --------------------------------------------------------------------------- #
@guides_bp.route('/free-guides')
def library():
    guides = (FreeGuide.query.filter_by(active=True)
              .order_by(FreeGuide.sort_order.asc(), FreeGuide.created_at.desc()).all())
    cats = []
    for g in guides:
        if g.category and g.category not in cats:
            cats.append(g.category)
    return render_template('guides/library.html', guides=guides, cats=cats, size_label=_size_label)


@guides_bp.route('/free-guides/<int:gid>/request', methods=['POST'])
def request_download(gid):
    g = db.session.get(FreeGuide, gid)
    if g is None or not g.active:
        return jsonify({'ok': False, 'error': 'This guide is no longer available.'}), 404
    data = request.get_json(silent=True) or request.form
    if (data.get('website') or '').strip():            # honeypot — bots fill every field
        return jsonify({'ok': True, 'url': url_for('guides.library')})
    name = (data.get('name') or '').strip()[:150]
    email = (data.get('email') or '').strip().lower()[:200]
    phone = (data.get('phone') or '').strip()[:40]
    if not name:
        return jsonify({'ok': False, 'error': 'Please tell us your name.'}), 400
    if not _EMAIL.match(email):
        return jsonify({'ok': False, 'error': 'Please enter a valid email address.'}), 400

    db.session.add(GuideDownload(guide_id=g.id, guide_title=g.title, name=name, email=email, phone=phone))
    g.download_count = (g.download_count or 0) + 1
    # also surface it in the existing Leads inbox
    import json as _json
    db.session.add(PageLead(source='free-guide', name=name, email=email, phone=phone,
                            payload_json=_json.dumps({'guide': g.title, 'guide_id': g.id}, ensure_ascii=False)))
    db.session.commit()

    token = _serializer().dumps({'g': g.id, 'e': email})
    url = url_for('guides.get_file', token=token)
    _email_link(g, name, email, url)
    return jsonify({'ok': True, 'url': url, 'title': g.title})


def _email_link(guide, name, email, path):
    """Best-effort: email the same link so they can come back to it later."""
    try:
        from app.services import mailer
        from app.services.email_templates import branded_shell, SITE, _btn
        link = SITE + path
        first = (name.split(' ')[0] if name else 'there')
        html = branded_shell(
            f'<p>Hi {first},</p><p>Thanks for downloading <strong>{guide.title}</strong>. '
            f'You can get it again any time in the next 48 hours:</p>'
            + _btn(link, 'Download the guide')
            + '<p>Want a mentor to turn this into a plan for your child? Reply to this email '
              'or WhatsApp us — the first conversation is free.</p>')
        text = (f'Hi {first},\n\nThanks for downloading "{guide.title}". Download it again (valid 48 hours):\n'
                f'{link}\n\nQuestions? Reply to this email.\n\n— Team EduAakashaA')
        # guide emails go out from the public info@ address, and replies come back to it
        mailer.send_async(email, f'Your free guide: {guide.title}', text, html,
                          from_addr=mailer.INFO_FROM, reply_to=mailer.INFO_FROM)
    except Exception:                                    # never block the download
        current_app.logger.exception('free-guide email failed')


@guides_bp.route('/free-guides/get/<token>')
def get_file(token):
    try:
        info = _serializer().loads(token, max_age=TOKEN_AGE)
    except SignatureExpired:
        flash('That download link has expired — request the guide again.', 'info')
        return redirect(url_for('guides.library'))
    except BadSignature:
        abort(404)
    g = db.session.get(FreeGuide, info.get('g'))
    if g is None or not g.active or not g.data:
        abort(404)
    return _send(g)


def _send(g):
    resp = Response(g.data, mimetype=g.file_mime or 'application/octet-stream')
    resp.headers['Content-Disposition'] = f'attachment; filename="{g.file_name}"'
    resp.headers['Cache-Control'] = 'private, no-store'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


# --------------------------------------------------------------------------- #
# admin
# --------------------------------------------------------------------------- #
@guides_bp.route('/admin/free-guides')
@admin_required
def admin_list():
    rows = FreeGuide.query.order_by(FreeGuide.sort_order.asc(), FreeGuide.created_at.desc()).all()
    total_dl = db.session.query(db.func.coalesce(db.func.sum(FreeGuide.download_count), 0)).scalar()
    return render_template('admin/guides_list.html', admin_tab='guides', rows=rows, cats=CATEGORIES,
                           size_label=_size_label, total_downloads=total_dl,
                           exts=', '.join('.' + e for e in ALLOWED))


@guides_bp.route('/admin/free-guides/upload', methods=['POST'])
@admin_required
def admin_upload():
    title = (request.form.get('title') or '').strip()[:160]
    if not title:
        flash('Give the guide a title.', 'danger')
        return redirect(url_for('guides.admin_list'))
    data, mime, fname, err = _read_upload(request.files.get('file'))
    if err:
        flash(err, 'danger')
        return redirect(url_for('guides.admin_list'))
    g = FreeGuide(title=title, description=(request.form.get('description') or '').strip(),
                  category=(request.form.get('category') or 'General').strip()[:60] or 'General',
                  file_name=fname, file_mime=mime, file_size=len(data), data=data,
                  sort_order=request.form.get('sort_order', type=int) or 100, active=True)
    db.session.add(g)
    db.session.commit()
    flash(f'"{title}" is live on the Free Guides page.', 'success')
    return redirect(url_for('guides.admin_list'))


@guides_bp.route('/admin/free-guides/<int:gid>/update', methods=['POST'])
@admin_required
def admin_update(gid):
    g = db.session.get(FreeGuide, gid) or abort(404)
    g.title = (request.form.get('title') or g.title).strip()[:160]
    g.description = (request.form.get('description') or '').strip()
    g.category = (request.form.get('category') or g.category or 'General').strip()[:60]
    so = request.form.get('sort_order', type=int)
    if so is not None:
        g.sort_order = so
    f = request.files.get('file')
    if f is not None and f.filename:
        data, mime, fname, err = _read_upload(f)
        if err:
            flash(err, 'danger')
            return redirect(url_for('guides.admin_list'))
        g.data, g.file_mime, g.file_name, g.file_size = data, mime, fname, len(data)
    db.session.commit()
    flash('Guide updated.', 'success')
    return redirect(url_for('guides.admin_list'))


@guides_bp.route('/admin/free-guides/<int:gid>/toggle', methods=['POST'])
@admin_required
def admin_toggle(gid):
    g = db.session.get(FreeGuide, gid) or abort(404)
    g.active = not g.active
    db.session.commit()
    flash(f'"{g.title}" is now {"visible" if g.active else "hidden"}.', 'success')
    return redirect(url_for('guides.admin_list'))


@guides_bp.route('/admin/free-guides/<int:gid>/delete', methods=['POST'])
@admin_required
def admin_delete(gid):
    g = db.session.get(FreeGuide, gid) or abort(404)
    db.session.delete(g)
    db.session.commit()
    flash('Guide deleted.', 'success')
    return redirect(url_for('guides.admin_list'))


@guides_bp.route('/admin/free-guides/<int:gid>/file')
@admin_required
def admin_file(gid):
    g = db.session.get(FreeGuide, gid) or abort(404)
    return _send(g)


@guides_bp.route('/admin/free-guides/downloads')
@admin_required
def admin_downloads():
    q = (request.args.get('q') or '').strip()
    query = GuideDownload.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(GuideDownload.name.ilike(like), GuideDownload.email.ilike(like),
                                    GuideDownload.guide_title.ilike(like)))
    query = query.order_by(GuideDownload.created_at.desc())
    if request.args.get('csv'):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(['Date (UTC)', 'Guide', 'Name', 'Email', 'Phone'])
        for r in query.all():
            w.writerow([r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '',
                        r.guide_title, r.name, r.email, r.phone])
        return Response(buf.getvalue(), mimetype='text/csv',
                        headers={'Content-Disposition': 'attachment; filename=free_guide_downloads.csv'})
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=40, error_out=False)
    return render_template('admin/guide_downloads.html', admin_tab='guides', pagination=pagination,
                           rows=pagination.items, q=q)
