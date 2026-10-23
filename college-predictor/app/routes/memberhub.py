"""Member Home — the landing page after login: student photo + details and the tile hub."""
from flask import Blueprint, Response, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import StudentProfile
from app.services import member_hub

memberhub_bp = Blueprint('memberhub', __name__)

PHOTO_MAX = 1024 * 1024
PHOTO_TYPES = [(b'\xff\xd8\xff', 'image/jpeg'), (b'\x89PNG\r\n\x1a\n', 'image/png')]
FIELDS = {'student_name': 150, 'grade': 60, 'school': 200, 'board': 60, 'city': 100, 'country': 80,
          'target_exams': 200, 'target_year': 20, 'phone': 40, 'parent_name': 150}


def _read_photo(storage):
    """-> (data, mime, error); no file is not an error."""
    if storage is None or not storage.filename:
        return None, None, None
    ext = storage.filename.rsplit('.', 1)[-1].lower() if '.' in storage.filename else ''
    if ext not in ('jpg', 'jpeg', 'png', 'webp'):
        return None, None, 'Photo must be a JPG, PNG or WebP.'
    data = storage.read(PHOTO_MAX + 1)
    if not data:
        return None, None, 'The photo file was empty.'
    if len(data) > PHOTO_MAX:
        return None, None, 'Photo is larger than 1 MB — please use a smaller one.'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return data, 'image/webp', None
    for magic, mime in PHOTO_TYPES:
        if data.startswith(magic):
            return data, mime, None
    return None, None, 'That does not look like a valid JPG, PNG or WebP image.'


@memberhub_bp.route('/member-home')
@login_required
def home():
    if current_user.is_mentor:
        return redirect(url_for('alumni.mentor_dashboard'))
    sp = current_user.student_profile
    try:                                  # unread schedule alerts for the bell; the dashboard works without them
        from app.services import exam_calendar as xc
        alerts = xc.unread_alerts(current_user)
    except Exception:
        alerts = []
    return render_template('members/home.html', categories=member_hub.build(current_user), sp=sp, alerts=alerts,
                           has_photo=bool(sp and sp.photo_size),
                           complete=bool(sp and sp.student_name and sp.grade and sp.target_exams))


@memberhub_bp.route('/member-home/details', methods=['POST'])
@login_required
def save_details():
    data, mime, err = _read_photo(request.files.get('photo'))
    if err:
        flash(err, 'danger')
        return redirect(url_for('memberhub.home') + '#details')
    sp = current_user.student_profile
    if sp is None:
        sp = StudentProfile(user_id=current_user.id)
        db.session.add(sp)
    for f, n in FIELDS.items():
        setattr(sp, f, (request.form.get(f) or '').strip()[:n] or None)
    if data:
        sp.photo_mime, sp.photo_data, sp.photo_size = mime, data, len(data)
    elif request.form.get('remove_photo') == '1':
        sp.photo_mime = sp.photo_data = None
        sp.photo_size = 0
    db.session.commit()
    flash('Your details were saved.', 'success')
    return redirect(url_for('memberhub.home'))


@memberhub_bp.route('/member-home/photo/<int:uid>')
@login_required
def photo(uid):
    if uid != current_user.id and not current_user.is_staff:
        abort(403)
    sp = db.session.get(StudentProfile, uid)
    if sp is None or not sp.photo_size:
        abort(404)
    resp = Response(sp.photo_data, mimetype=sp.photo_mime)
    resp.headers['Cache-Control'] = 'private, max-age=300'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp
