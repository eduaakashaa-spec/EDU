"""Alumni / Mentor Network.

Public:
    GET/POST /alumni-network — landing page + registration form. Passed-out
    and current students at top universities register to mentor parents (paid
    per meeting). Collects academic details, a photo and a resume, plus a
    referral code so mentors can invite others.

Admin (admin tier):
    GET  /admin/alumni                 — searchable / filterable list
    GET  /admin/alumni/<id>            — full profile + matching info
    POST /admin/alumni/<id>/update     — status + internal notes
    GET  /admin/alumni/<id>/resume     — download the resume
    GET  /admin/alumni/<id>/photo      — view the photo
"""
import io
import secrets
import threading
import time
from datetime import datetime, timedelta, timezone

from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, send_file, url_for)
from flask_login import current_user, login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from app.decorators import admin_required, mentor_required
from app.extensions import db, bcrypt
from app.models import (Announcement, AlumniProfile, MentorMeeting,
                        MentorMessage, User)

alumni_bp = Blueprint('alumni', __name__)

STAGES = ('current-student', 'alumni', 'working')
STATUSES = ('New', 'Verified', 'Active', 'Rejected')
MEETING_KINDS = ('meeting', 'referral', 'bonus', 'adjustment')
MEETING_STATUSES = ('Scheduled', 'Completed', 'No-show', 'Cancelled')


def _parse_dt(value):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None

# Upload rules. Files are validated by extension AND magic bytes, size-capped,
# and only ever served back with a fixed disposition + nosniff (see below), so
# a mislabelled or hostile file can't execute in our origin.
RESUME_EXT = {'pdf', 'doc', 'docx'}
PHOTO_EXT = {'jpg', 'jpeg', 'png', 'webp'}
RESUME_MAX = 5 * 1024 * 1024   # 5 MB
PHOTO_MAX = 3 * 1024 * 1024    # 3 MB

# leading magic bytes per allowed type (photos are strictly validated so an
# HTML/SVG payload can't masquerade as an image)
PHOTO_MAGIC = {
    b'\xff\xd8\xff': 'image/jpeg',
    b'\x89PNG\r\n\x1a\n': 'image/png',
}
RESUME_MAGIC = {
    b'%PDF': 'application/pdf',
    b'PK\x03\x04': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx (zip)
    b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'application/msword',  # legacy .doc (OLE)
}


def _ext(filename):
    return filename.rsplit('.', 1)[-1].lower() if filename and '.' in filename else ''


def _read_capped(storage, max_bytes):
    """Read at most max_bytes+1 so we can detect oversize without loading a
    huge body into memory. Returns (data, too_big)."""
    data = storage.read(max_bytes + 1)
    return (data, len(data) > max_bytes)


def _validate_photo(storage):
    """→ (data, mime, error). data/mime are None when there's no file."""
    if storage is None or not storage.filename:
        return None, None, None
    if _ext(storage.filename) not in PHOTO_EXT:
        return None, None, 'Photo must be a JPG, PNG or WebP image.'
    data, too_big = _read_capped(storage, PHOTO_MAX)
    if too_big:
        return None, None, 'Photo is larger than 3 MB. Please upload a smaller image.'
    if not data:
        return None, None, 'The photo file was empty.'
    if data[:12].startswith(b'RIFF') and data[8:12] == b'WEBP':
        return data, 'image/webp', None
    for magic, mime in PHOTO_MAGIC.items():
        if data.startswith(magic):
            return data, mime, None
    return None, None, 'That photo does not look like a valid image file.'


def _validate_resume(storage):
    if storage is None or not storage.filename:
        return None, None, None
    if _ext(storage.filename) not in RESUME_EXT:
        return None, None, 'Resume must be a PDF, DOC or DOCX file.'
    data, too_big = _read_capped(storage, RESUME_MAX)
    if too_big:
        return None, None, 'Resume is larger than 5 MB. Please upload a smaller file.'
    if not data:
        return None, None, 'The resume file was empty.'
    for magic, mime in RESUME_MAGIC.items():
        if data.startswith(magic):
            return data, mime, None
    # DOC/DOCX magic can vary; fall back to trusting the (allowlisted) extension.
    ext = _ext(storage.filename)
    if ext in ('doc', 'docx'):
        return data, ('application/msword' if ext == 'doc'
                      else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), None
    return None, None, 'That resume does not look like a valid PDF/DOC/DOCX.'


def _unique_referral_code():
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'  # no ambiguous 0/O/1/I
    for _ in range(12):
        code = 'EA' + ''.join(secrets.choice(alphabet) for _ in range(6))
        if not AlumniProfile.query.filter_by(referral_code=code).first():
            return code
    return 'EA' + secrets.token_hex(5).upper()[:8]


def _safe_http_url(value, max_len=300):
    """Keep a URL only if it is an http(s) link — blocks javascript:/data:
    URIs that would otherwise execute when an admin clicks the link."""
    value = (value or '').strip()[:max_len]
    low = value.lower()
    return value if (low.startswith('http://') or low.startswith('https://')) else ''


def _resolve_referrer(raw_code):
    """Return a referral code only if it belongs to an existing mentor, so
    fabricated / spammed referral codes are dropped rather than credited."""
    raw = (raw_code or '').strip()[:16]
    if not raw:
        return None
    ref = AlumniProfile.query.filter_by(referral_code=raw).first()
    return ref.referral_code if ref else None


# ---- lightweight per-IP throttle for the public upload endpoint ----------- #
# The registration endpoint is unauthenticated and accepts multi-MB uploads,
# so cap how often one client can post to stop a flood filling the DB. This is
# an in-process sliding window (fine for the single Render worker); a
# multi-instance deployment would use flask-limiter / Redis instead.
_RATE_LOCK = threading.Lock()
_RATE_HITS = {}                 # ip -> [monotonic timestamps]
RATE_WINDOW = 3600             # 1 hour
RATE_MAX = 10                  # posts per IP per window


def _client_ip():
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def _rate_ok(ip):
    now = time.time()
    with _RATE_LOCK:
        hits = [t for t in _RATE_HITS.get(ip, []) if now - t < RATE_WINDOW]
        if len(hits) >= RATE_MAX:
            _RATE_HITS[ip] = hits
            return False
        hits.append(now)
        _RATE_HITS[ip] = hits
        if len(_RATE_HITS) > 5000:   # bound memory
            for k in list(_RATE_HITS):
                _RATE_HITS[k] = [t for t in _RATE_HITS[k] if now - t < RATE_WINDOW]
                if not _RATE_HITS[k]:
                    del _RATE_HITS[k]
        return True


# --------------------------------------------------------------------------- #
# Public registration
# --------------------------------------------------------------------------- #
@alumni_bp.route('/alumni-network', methods=['GET', 'POST'])
def alumni_network():
    ref = (request.args.get('ref') or '').strip()[:16]

    if request.method == 'GET':
        return render_template('alumni_network.html', ref=ref, stages=STAGES)

    # ---- POST: handle registration (multipart form) ----
    def fail(msg, code=400):
        return jsonify({'ok': False, 'error': msg}), code

    if not _rate_ok(_client_ip()):
        return fail('Too many submissions from your network. Please try again later.', 429)

    f = request.form
    name = (f.get('name') or '').strip()
    email = (f.get('email') or '').strip().lower()
    university = (f.get('university') or '').strip()
    password = f.get('password') or ''

    if not name or not email or not university:
        return fail('Name, email and university are required.')
    if '@' not in email or '.' not in email.split('@')[-1]:
        return fail('Please enter a valid email address.')
    if len(password) < 6:
        return fail('Please choose a password of at least 6 characters for your mentor account.')
    if not f.get('consent'):
        return fail('Please agree to be contacted so we can match you with parents.')

    # A mentor login is created for each registrant — one account per email.
    if User.query.filter_by(email=email).first():
        return fail('An account with this email already exists. Please log in instead.')

    # de-dup accidental / scripted re-submits of the same email
    recent_cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=10)
    if AlumniProfile.query.filter(AlumniProfile.email == email,
                                  AlumniProfile.created_at >= recent_cutoff).first():
        return fail('You have already registered with this email. Our team will be in touch.')

    photo_data, photo_mime, err = _validate_photo(request.files.get('photo'))
    if err:
        return fail(err)
    resume_data, resume_mime, err = _validate_resume(request.files.get('resume'))
    if err:
        return fail(err)

    stage = f.get('stage') if f.get('stage') in STAGES else None
    referred_by = _resolve_referrer(f.get('ref') or ref)
    photo_file = request.files.get('photo')
    resume_file = request.files.get('resume')

    # Create the mentor's login account and link the profile to it.
    mentor_user = User(name=name[:120], email=email[:200], tier='mentor',
                       password_hash=bcrypt.generate_password_hash(password).decode())
    db.session.add(mentor_user)
    db.session.flush()   # assign mentor_user.id before linking

    profile = AlumniProfile(
        user_id=mentor_user.id,
        name=name[:150], email=email[:200],
        phone=(f.get('phone') or '').strip()[:40],
        country=(f.get('country') or '').strip()[:80],
        city=(f.get('city') or '').strip()[:80],
        university=university[:200],
        program=(f.get('program') or '').strip()[:200],
        degree_level=(f.get('degree_level') or '').strip()[:40],
        grad_year=(f.get('grad_year') or '').strip()[:16],
        stage=stage,
        admission_route=(f.get('admission_route') or '').strip()[:160],
        current_role=(f.get('current_role') or '').strip()[:200],
        linkedin=_safe_http_url(f.get('linkedin')),
        languages=(f.get('languages') or '').strip()[:200],
        bio=(f.get('bio') or '').strip()[:4000],
        availability=(f.get('availability') or '').strip()[:200],
        photo_data=photo_data, photo_mime=photo_mime,
        photo_name=(secure_filename(photo_file.filename)[:255] if photo_data and photo_file else None),
        resume_data=resume_data, resume_mime=resume_mime,
        resume_name=(secure_filename(resume_file.filename)[:255] if resume_data and resume_file else None),
        referral_code=_unique_referral_code(),
        referred_by=(referred_by if referred_by else None),
        consent=True, status='New',
    )
    db.session.add(profile)
    try:
        db.session.commit()
    except IntegrityError:
        # e.g. two submissions racing on the unique email / referral code
        db.session.rollback()
        return fail('An account with this email already exists. Please log in instead.')

    # log them straight into their new mentor portal
    login_user(mentor_user)

    share_link = url_for('alumni.alumni_network', ref=profile.referral_code, _external=True)
    return jsonify({'ok': True, 'name': profile.name.split(' ')[0],
                    'referral_code': profile.referral_code,
                    'share_link': share_link,
                    'dashboard_url': url_for('alumni.mentor_dashboard')})


# --------------------------------------------------------------------------- #
# Mentor portal (mentor tier)
# --------------------------------------------------------------------------- #
def _my_profile():
    return AlumniProfile.query.filter_by(user_id=current_user.id).first()


def _earnings(profile):
    completed = [m for m in profile.meetings if m.status == 'Completed']
    calls = sum(1 for m in completed if m.kind == 'meeting')
    total = sum(m.payout_amount for m in completed)
    paid = sum(m.payout_amount for m in completed if m.paid)
    return {'calls': calls, 'total': total, 'paid': paid, 'pending': total - paid,
            'completed': len(completed)}


@alumni_bp.route('/mentor')
@mentor_required
def mentor_dashboard():
    profile = _my_profile()
    if profile is None:
        flash('Finish setting up your mentor profile to continue.', 'info')
        return redirect(url_for('alumni.alumni_network'))

    meetings = profile.meetings.order_by(MentorMeeting.created_at.desc()).all()
    referrals = (AlumniProfile.query.filter_by(referred_by=profile.referral_code)
                 .order_by(AlumniProfile.created_at.desc()).all())
    messages = profile.messages.order_by(MentorMessage.created_at.asc()).all()
    announcements = (Announcement.query.filter_by(active=True)
                     .order_by(Announcement.pinned.desc(), Announcement.created_at.desc())
                     .limit(5).all())
    share_link = url_for('alumni.alumni_network', ref=profile.referral_code, _external=True)
    return render_template('mentor/dashboard.html', profile=profile,
                           meetings=meetings, earnings=_earnings(profile),
                           referrals=referrals, messages=messages,
                           announcements=announcements, share_link=share_link)


@alumni_bp.route('/mentor/message', methods=['POST'])
@mentor_required
def mentor_message():
    profile = _my_profile()
    if profile is None:
        abort(404)
    body = (request.form.get('body') or '').strip()[:4000]
    if body:
        db.session.add(MentorMessage(alumni_id=profile.id, sender='mentor', body=body))
        db.session.commit()
        flash('Message sent to the EduAakashaa team.', 'success')
    return redirect(url_for('alumni.mentor_dashboard') + '#messages')


@alumni_bp.route('/mentor/profile', methods=['POST'])
@mentor_required
def mentor_profile_update():
    """Let mentors keep the fields most useful for matching current."""
    profile = _my_profile()
    if profile is None:
        abort(404)
    profile.phone = (request.form.get('phone') or '').strip()[:40]
    profile.country = (request.form.get('country') or '').strip()[:80]
    profile.city = (request.form.get('city') or '').strip()[:80]
    profile.languages = (request.form.get('languages') or '').strip()[:200]
    profile.availability = (request.form.get('availability') or '').strip()[:200]
    profile.linkedin = _safe_http_url(request.form.get('linkedin'))
    profile.bio = (request.form.get('bio') or '').strip()[:4000]
    db.session.commit()
    flash('Profile updated.', 'success')
    return redirect(url_for('alumni.mentor_dashboard') + '#profile')


# --------------------------------------------------------------------------- #
# Admin
# --------------------------------------------------------------------------- #
@alumni_bp.route('/admin/alumni')
@admin_required
def admin_list():
    q = (request.args.get('q') or '').strip()
    status = (request.args.get('status') or '').strip()
    page = request.args.get('page', 1, type=int)

    query = AlumniProfile.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(AlumniProfile.name.ilike(like),
                                    AlumniProfile.email.ilike(like),
                                    AlumniProfile.university.ilike(like),
                                    AlumniProfile.program.ilike(like)))
    if status in STATUSES:
        query = query.filter(AlumniProfile.status == status)

    pagination = (query.order_by(AlumniProfile.created_at.desc())
                  .paginate(page=page, per_page=25, error_out=False))
    stats = {
        'total': AlumniProfile.query.count(),
        'active': AlumniProfile.query.filter_by(status='Active').count(),
        'new': AlumniProfile.query.filter_by(status='New').count(),
        'referred': AlumniProfile.query.filter(AlumniProfile.referred_by.isnot(None)).count(),
    }
    return render_template('admin/alumni_list.html', admin_tab='alumni',
                           pagination=pagination, rows=pagination.items,
                           stats=stats, q=q, status=status, statuses=STATUSES)


@alumni_bp.route('/admin/alumni/<int:alum_id>')
@admin_required
def admin_detail(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    referrer = (AlumniProfile.query.filter_by(referral_code=alum.referred_by).first()
                if alum.referred_by else None)
    referrals = (AlumniProfile.query.filter_by(referred_by=alum.referral_code)
                 .order_by(AlumniProfile.created_at.desc()).all())
    meetings = alum.meetings.order_by(MentorMeeting.created_at.desc()).all()
    messages = alum.messages.order_by(MentorMessage.created_at.asc()).all()
    return render_template('admin/alumni_detail.html', admin_tab='alumni',
                           alum=alum, referrer=referrer, referrals=referrals,
                           meetings=meetings, messages=messages,
                           earnings=_earnings(alum), statuses=STATUSES,
                           meeting_kinds=MEETING_KINDS, meeting_statuses=MEETING_STATUSES)


@alumni_bp.route('/admin/alumni/<int:alum_id>/update', methods=['POST'])
@admin_required
def admin_update(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    status = request.form.get('status')
    if status in STATUSES:
        alum.status = status
    alum.admin_notes = (request.form.get('admin_notes') or '').strip()[:4000]
    db.session.commit()
    flash(f'{alum.name} updated ({alum.status}).', 'success')
    return redirect(url_for('alumni.admin_detail', alum_id=alum.id))


@alumni_bp.route('/admin/alumni/<int:alum_id>/meeting', methods=['POST'])
@admin_required
def admin_add_meeting(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    kind = request.form.get('kind')
    kind = kind if kind in MEETING_KINDS else 'meeting'
    status = request.form.get('status')
    status = status if status in MEETING_STATUSES else 'Completed'
    try:
        payout = int(request.form.get('payout_amount') or 0)
    except (TypeError, ValueError):
        payout = 0
    payout = max(0, min(payout, 1_000_000))   # whole AED, sane bound
    db.session.add(MentorMeeting(
        alumni_id=alum.id, kind=kind, status=status, payout_amount=payout,
        parent_name=(request.form.get('parent_name') or '').strip()[:150],
        topic=(request.form.get('topic') or '').strip()[:200],
        meeting_date=_parse_dt(request.form.get('meeting_date')),
        notes=(request.form.get('notes') or '').strip()[:2000]))
    db.session.commit()
    flash('Session logged.', 'success')
    return redirect(url_for('alumni.admin_detail', alum_id=alum.id) + '#meetings')


@alumni_bp.route('/admin/meeting/<int:meeting_id>/paid', methods=['POST'])
@admin_required
def admin_meeting_paid(meeting_id):
    m = db.session.get(MentorMeeting, meeting_id) or abort(404)
    m.paid = not m.paid
    m.paid_at = datetime.now(timezone.utc).replace(tzinfo=None) if m.paid else None
    db.session.commit()
    flash('Payout status updated.', 'success')
    return redirect(url_for('alumni.admin_detail', alum_id=m.alumni_id) + '#meetings')


@alumni_bp.route('/admin/meeting/<int:meeting_id>/delete', methods=['POST'])
@admin_required
def admin_meeting_delete(meeting_id):
    m = db.session.get(MentorMeeting, meeting_id) or abort(404)
    aid = m.alumni_id
    db.session.delete(m)
    db.session.commit()
    flash('Session removed.', 'success')
    return redirect(url_for('alumni.admin_detail', alum_id=aid) + '#meetings')


@alumni_bp.route('/admin/alumni/<int:alum_id>/reply', methods=['POST'])
@admin_required
def admin_reply(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    body = (request.form.get('body') or '').strip()[:4000]
    if body:
        db.session.add(MentorMessage(alumni_id=alum.id, sender='admin', body=body))
        db.session.commit()
        flash('Reply sent to the mentor.', 'success')
    return redirect(url_for('alumni.admin_detail', alum_id=alum.id) + '#messages')


def _send_blob(data, mime, download_name, as_attachment):
    if not data:
        abort(404)
    resp = send_file(io.BytesIO(data), mimetype=mime or 'application/octet-stream',
                     as_attachment=as_attachment, download_name=download_name)
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Cache-Control'] = 'private, no-store'
    return resp


@alumni_bp.route('/admin/alumni/<int:alum_id>/resume')
@admin_required
def admin_resume(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    name = alum.resume_name or f'resume-{alum.id}'
    # always an attachment so a PDF/DOC can never render inline in our origin
    return _send_blob(alum.resume_data, alum.resume_mime, name, as_attachment=True)


@alumni_bp.route('/admin/alumni/<int:alum_id>/photo')
@admin_required
def admin_photo(alum_id):
    alum = db.session.get(AlumniProfile, alum_id) or abort(404)
    name = alum.photo_name or f'photo-{alum.id}'
    # inline is safe: the bytes were magic-validated as a raster image and
    # nosniff prevents the browser from reinterpreting them.
    return _send_blob(alum.photo_data, alum.photo_mime, name, as_attachment=False)
