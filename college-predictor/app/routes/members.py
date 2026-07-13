"""Premium member area + document verification.

Member-facing:
    GET  /profile                              — member profile: meetings, notes, documents
    POST /profile/documents/<id>/upload        — upload a file for a requested document
    POST /profile/documents/submit             — submit uploaded docs for review (emails admin)

Admin (admin tier) — the "Document Verify" tab:
    GET  /admin/documents                      — premium members + their doc-verification status
    GET  /admin/documents/<user_id>            — one member: request docs, review, log meetings
    POST /admin/documents/<user_id>/request    — request selected documents (emails member)
    POST /admin/documents/doc/<id>/review      — approve / reject with comment (emails member)
    GET  /admin/documents/doc/<id>/file        — open an uploaded doc via a private R2 link
    POST /admin/documents/<user_id>/meeting    — log a counselling session + notes
    POST /admin/documents/meeting/<id>/delete  — remove a mis-logged meeting

The whole request→upload→review cycle repeats until every requested document is
Approved, at which point the member gets an "all verified" email.
"""
import os
import uuid
from datetime import datetime, timezone

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.decorators import admin_required
from app.extensions import db
from app.models import DocVerification, MemberMeeting, User
from app.services import r2
from app.services.email_templates import SITE
from app.services.mailer import send_async

members_bp = Blueprint('members', __name__)

# Where "documents submitted" notifications go (the team inbox). Spec: the Gmail.
NOTIFY_EMAIL = os.environ.get('DOC_NOTIFY_EMAIL', 'eduaakashaa@gmail.com')

# Documents the team can request during admissions / counselling. Curated for
# Indian college admissions + DASA / study-abroad; admins can also add a custom
# one. Grouped only for display; the stored value is the plain label.
DOC_TYPES = [
    ('Academics', [
        '10th (SSLC) Marksheet', '12th (HSC) Marksheet', 'Transfer Certificate (TC)',
        'Migration Certificate', 'Provisional / Degree Certificate',
        'Consolidated Marksheet', 'Bonafide / Study Certificate',
    ]),
    ('Entrance & Test Scores', [
        'JEE / NEET / TANCET Scorecard', 'SAT / ACT Scorecard',
        'IELTS / TOEFL / Duolingo Scorecard', 'Rank / Allotment Letter',
    ]),
    ('Identity & Proof', [
        'Passport', 'Aadhaar Card', 'PAN Card', 'Passport-size Photograph',
        'Birth Certificate',
    ]),
    ('Category & Financial', [
        'Community / Caste Certificate', 'Income Certificate',
        'Nativity / Domicile Certificate', 'Bank Statement / Financial Proof',
        'Scholarship Documents',
    ]),
    ('Application', [
        'Statement of Purpose (SOP)', 'Letter of Recommendation (LOR)',
        'Resume / CV', 'Gap Certificate / Affidavit', 'Medical Certificate',
    ]),
]
# flat set of the known labels, for validation
_KNOWN_TYPES = {name for _, names in DOC_TYPES for name in names}

DOC_STATUSES = ('Requested', 'Submitted', 'Approved', 'Rejected')
MEETING_STATUSES = ('Scheduled', 'Completed', 'Cancelled')

# Uploaded documents: certificates are usually PDF or a phone photo; allow Word
# too. Validated by extension + magic bytes + size (public-ish upload) and only
# ever served back as a private, short-lived R2 link.
DOC_EXT = {'pdf', 'jpg', 'jpeg', 'png', 'webp', 'doc', 'docx'}
DOC_MAX = 8 * 1024 * 1024
DOC_MAGIC = {
    b'%PDF-': 'application/pdf',
    b'\xff\xd8\xff': 'image/jpeg',
    b'\x89PNG\r\n\x1a\n': 'image/png',
    b'PK\x03\x04': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'application/msword',
}


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _ext(filename):
    return filename.rsplit('.', 1)[-1].lower() if filename and '.' in filename else ''


def _validate_doc(storage):
    """→ (data, mime, error). Mirrors alumni._validate_resume but a bit more
    permissive (images allowed, since certificates are often photographed)."""
    if storage is None or not storage.filename:
        return None, None, 'Please choose a file to upload.'
    if _ext(storage.filename) not in DOC_EXT:
        return None, None, 'File must be a PDF, image (JPG/PNG/WebP) or Word document.'
    data = storage.read(DOC_MAX + 1)
    if len(data) > DOC_MAX:
        return None, None, 'File is larger than 8 MB. Please upload a smaller scan.'
    if not data:
        return None, None, 'The file was empty.'
    if data[:12].startswith(b'RIFF') and data[8:12] == b'WEBP':
        return data, 'image/webp', None
    for magic, mime in DOC_MAGIC.items():
        if data.startswith(magic):
            return data, mime, None
    return None, None, 'That file does not look like a valid PDF, image or Word document.'


# --------------------------------------------------------------------------- #
# Automated emails (best-effort; no-op when SMTP unconfigured — see mailer.py).
# URLs are built here inside the request context, then passed as plain strings.
# --------------------------------------------------------------------------- #
def _profile_url():
    return SITE + url_for('members.profile')


def _admin_doc_url(user_id):
    return SITE + url_for('members.admin_doc_detail', user_id=user_id)


def _email_docs_requested(user, doc_labels):
    items = ''.join(f'<li>{d}</li>' for d in doc_labels)
    items_txt = '\n'.join(f'  • {d}' for d in doc_labels)
    send_async(
        user.email,
        'Action needed: upload your documents for verification',
        (f"Hi {user.name.split(' ')[0]},\n\nOur team needs the following document(s) "
         f"to continue your admissions process:\n\n{items_txt}\n\n"
         f"Please log in and upload them here: {_profile_url()}\n\n— Team EduAakashaa"),
        (f"<p>Hi {user.name.split(' ')[0]},</p><p>Our team needs the following "
         f"document(s) to continue your admissions process:</p><ul>{items}</ul>"
         f"<p><a href='{_profile_url()}'>Log in and upload your documents →</a></p>"
         "<p>— Team EduAakashaa</p>"))


def _email_docs_submitted(user, docs):
    items = '\n'.join(f'  • {d.doc_type} ({d.file_name})' for d in docs)
    send_async(
        NOTIFY_EMAIL,
        f'Documents submitted for review — {user.name}',
        (f"{user.name} ({user.email}) submitted {len(docs)} document(s) for verification:\n\n"
         f"{items}\n\nReview them here: {_admin_doc_url(user.id)}"))


def _email_doc_reviewed(user, doc):
    approved = doc.status == 'Approved'
    head = ('A document was approved ✅' if approved
            else 'A document needs to be re-uploaded')
    note = (f"\n\nReviewer comment: {doc.admin_comment}" if doc.admin_comment else '')
    body = ("has been approved" if approved
            else "could not be verified and needs to be uploaded again")
    send_async(
        user.email,
        f'{doc.doc_type}: {"approved" if approved else "needs resubmission"}',
        (f"Hi {user.name.split(' ')[0]},\n\nYour '{doc.doc_type}' {body}.{note}\n\n"
         f"View status / re-upload: {_profile_url()}\n\n— Team EduAakashaa"),
        (f"<p>Hi {user.name.split(' ')[0]},</p><p><strong>{head}</strong></p>"
         f"<p>Your <strong>{doc.doc_type}</strong> {body}.</p>"
         + (f"<p style='background:#faf3e0;padding:10px 14px;border-radius:8px'>"
            f"<strong>Reviewer comment:</strong> {doc.admin_comment}</p>" if doc.admin_comment else '')
         + f"<p><a href='{_profile_url()}'>View status / re-upload →</a></p>"
         "<p>— Team EduAakashaa</p>"))


def _email_all_verified(user):
    send_async(
        user.email,
        'All your documents are verified 🎉',
        (f"Hi {user.name.split(' ')[0]},\n\nGreat news — every document we requested has "
         f"been verified. You're all set for the next step. Our team will be in touch.\n\n"
         f"— Team EduAakashaa"),
        (f"<p>Hi {user.name.split(' ')[0]},</p><p>Great news — <strong>every document we "
         "requested has been verified.</strong> You're all set for the next step; our team "
         f"will be in touch.</p><p><a href='{_profile_url()}'>Open your profile →</a></p>"
         "<p>— Team EduAakashaa</p>"))


# --------------------------------------------------------------------------- #
# Member-facing
# --------------------------------------------------------------------------- #
@members_bp.route('/profile')
@login_required
def profile():
    # College Guides have their own portal.
    if current_user.is_mentor:
        return redirect(url_for('alumni.mentor_dashboard'))

    from datetime import timedelta
    from app.models import Announcement, ScheduleEvent

    meetings = (current_user.member_meetings
                .order_by(MemberMeeting.meeting_date.desc().nullslast(),
                          MemberMeeting.created_at.desc()).all())
    docs = (current_user.doc_verifications
            .order_by(DocVerification.requested_at.asc()).all())
    can_submit = any(d.status == 'Submitted' for d in docs)

    announcements = (Announcement.query.filter_by(active=True)
                     .order_by(Announcement.pinned.desc(), Announcement.created_at.desc())
                     .limit(5).all())
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist).replace(tzinfo=None)
    events = (ScheduleEvent.query.filter(ScheduleEvent.starts_at >= now)
              .order_by(ScheduleEvent.important.desc(), ScheduleEvent.starts_at.asc())
              .limit(5).all())

    return render_template('members/profile.html', meetings=meetings, docs=docs,
                           can_submit=can_submit, announcements=announcements,
                           events=events)


def _my_doc(doc_id):
    """Fetch a document owned by the current user, or 404 — stops one member
    from touching another's documents."""
    doc = db.session.get(DocVerification, doc_id) or abort(404)
    if doc.user_id != current_user.id:
        abort(404)
    return doc


@members_bp.route('/profile/documents/<int:doc_id>/upload', methods=['POST'])
@login_required
def upload_document(doc_id):
    doc = _my_doc(doc_id)
    if doc.status == 'Approved':
        flash('That document is already verified.', 'info')
        return redirect(url_for('members.profile') + '#documents')

    data, mime, err = _validate_doc(request.files.get('file'))
    if err:
        flash(err, 'danger')
        return redirect(url_for('members.profile') + '#documents')
    if not r2.is_configured():
        flash('Uploads are temporarily unavailable. Please try again shortly.', 'danger')
        return redirect(url_for('members.profile') + '#documents')

    storage = request.files.get('file')
    key = 'documents/%d/%s-%s' % (
        current_user.id, uuid.uuid4().hex,
        secure_filename(storage.filename)[:120] or 'document')
    try:
        r2.upload(data, key, mime)
    except Exception:
        flash('We could not store your file just now. Please try again shortly.', 'danger')
        return redirect(url_for('members.profile') + '#documents')

    doc.file_key = key
    doc.file_name = secure_filename(storage.filename)[:255] or 'document'
    doc.file_mime = mime
    doc.status = 'Submitted'
    doc.submitted_at = _now()
    doc.admin_comment = None          # clear a previous rejection reason
    doc.reviewed_at = None
    db.session.commit()
    flash(f'Uploaded “{doc.doc_type}”. Click “Submit for verification” when you\'ve added them all.', 'success')
    return redirect(url_for('members.profile') + '#documents')


@members_bp.route('/profile/documents/submit', methods=['POST'])
@login_required
def submit_documents():
    submitted = current_user.doc_verifications.filter_by(status='Submitted').all()
    if not submitted:
        flash('Upload at least one requested document before submitting.', 'info')
        return redirect(url_for('members.profile') + '#documents')
    _email_docs_submitted(current_user, submitted)
    flash('Submitted for verification — our team has been notified and will review your documents.', 'success')
    return redirect(url_for('members.profile') + '#documents')


# --------------------------------------------------------------------------- #
# Admin — Document Verify
# --------------------------------------------------------------------------- #
def _doc_counts(user_id):
    rows = (db.session.query(DocVerification.status, db.func.count(DocVerification.id))
            .filter(DocVerification.user_id == user_id)
            .group_by(DocVerification.status).all())
    counts = {s: 0 for s in DOC_STATUSES}
    for status, n in rows:
        counts[status] = n
    counts['total'] = sum(counts[s] for s in DOC_STATUSES)
    return counts


@members_bp.route('/admin/documents')
@admin_required
def admin_doc_list():
    q = (request.args.get('q') or '').strip()
    page = request.args.get('page', 1, type=int)

    # premium members (admins can request docs from paying members)
    query = User.query.filter(User.tier == 'premium')
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    pagination = (query.order_by(User.created_at.desc())
                  .paginate(page=page, per_page=25, error_out=False))
    counts = {u.id: _doc_counts(u.id) for u in pagination.items}
    return render_template('admin/documents_list.html', admin_tab='documents',
                           pagination=pagination, rows=pagination.items,
                           counts=counts, q=q)


@members_bp.route('/admin/documents/<int:user_id>')
@admin_required
def admin_doc_detail(user_id):
    user = db.session.get(User, user_id) or abort(404)
    docs = user.doc_verifications.order_by(DocVerification.requested_at.asc()).all()
    meetings = (user.member_meetings
                .order_by(MemberMeeting.meeting_date.desc().nullslast(),
                          MemberMeeting.created_at.desc()).all())
    requested_types = {d.doc_type for d in docs}
    return render_template('admin/documents_detail.html', admin_tab='documents',
                           member=user, docs=docs, meetings=meetings,
                           doc_groups=DOC_TYPES, requested_types=requested_types,
                           counts=_doc_counts(user.id),
                           meeting_statuses=MEETING_STATUSES)


@members_bp.route('/admin/documents/<int:user_id>/request', methods=['POST'])
@admin_required
def admin_request_docs(user_id):
    user = db.session.get(User, user_id) or abort(404)
    existing = {d.doc_type for d in user.doc_verifications}

    # selected known types + any custom labels (comma/newline separated)
    picked = [t for t in request.form.getlist('doc_types') if t in _KNOWN_TYPES]
    custom_raw = (request.form.get('custom') or '').replace('\n', ',')
    picked += [c.strip()[:120] for c in custom_raw.split(',') if c.strip()]

    added = []
    for label in picked:
        if label in existing or label in added:
            continue           # don't duplicate an already-requested document
        db.session.add(DocVerification(user_id=user.id, doc_type=label, status='Requested'))
        added.append(label)

    if not added:
        flash('No new documents to request (they were blank or already requested).', 'info')
        return redirect(url_for('members.admin_doc_detail', user_id=user.id))

    db.session.commit()
    _email_docs_requested(user, added)
    flash(f'Requested {len(added)} document(s) — {user.name} has been emailed.', 'success')
    return redirect(url_for('members.admin_doc_detail', user_id=user.id))


@members_bp.route('/admin/documents/doc/<int:doc_id>/review', methods=['POST'])
@admin_required
def admin_review_doc(doc_id):
    doc = db.session.get(DocVerification, doc_id) or abort(404)
    decision = request.form.get('decision')
    comment = (request.form.get('comment') or '').strip()[:2000]

    if decision == 'approve':
        doc.status = 'Approved'
    elif decision == 'reject':
        if not comment:
            flash('Please add a comment explaining what the member needs to fix.', 'danger')
            return redirect(url_for('members.admin_doc_detail', user_id=doc.user_id))
        doc.status = 'Rejected'
    else:
        abort(400)

    doc.admin_comment = comment or None
    doc.reviewed_at = _now()
    db.session.commit()
    _email_doc_reviewed(doc.user, doc)

    # once every requested document is Approved, tell the member they're done
    remaining = doc.user.doc_verifications.filter(
        DocVerification.status != 'Approved').count()
    if remaining == 0:
        _email_all_verified(doc.user)
        flash(f'{doc.doc_type} approved — all documents verified, member emailed. 🎉', 'success')
    else:
        flash(f'{doc.doc_type} {doc.status.lower()} — member emailed.', 'success')
    return redirect(url_for('members.admin_doc_detail', user_id=doc.user_id))


@members_bp.route('/admin/documents/doc/<int:doc_id>/file')
@admin_required
def admin_doc_file(doc_id):
    doc = db.session.get(DocVerification, doc_id) or abort(404)
    if not doc.file_key:
        abort(404)
    if not r2.is_configured():
        abort(503)
    return redirect(r2.presigned_get(doc.file_key, download_name=doc.file_name or 'document'))


@members_bp.route('/admin/documents/<int:user_id>/meeting', methods=['POST'])
@admin_required
def admin_add_meeting(user_id):
    user = db.session.get(User, user_id) or abort(404)
    title = (request.form.get('title') or '').strip()[:200]
    if not title:
        flash('Please add a title / topic for the session.', 'danger')
        return redirect(url_for('members.admin_doc_detail', user_id=user.id))
    status = request.form.get('status')
    status = status if status in MEETING_STATUSES else 'Completed'
    raw_date = (request.form.get('meeting_date') or '').strip()
    try:
        mdate = datetime.fromisoformat(raw_date) if raw_date else None
    except ValueError:
        mdate = None
    db.session.add(MemberMeeting(
        user_id=user.id, title=title,
        counsellor=(request.form.get('counsellor') or '').strip()[:120],
        meeting_date=mdate, status=status,
        notes=(request.form.get('notes') or '').strip()[:8000]))
    db.session.commit()
    flash('Session logged.', 'success')
    return redirect(url_for('members.admin_doc_detail', user_id=user.id) + '#meetings')


@members_bp.route('/admin/documents/meeting/<int:mid>/delete', methods=['POST'])
@admin_required
def admin_delete_meeting(mid):
    meeting = db.session.get(MemberMeeting, mid) or abort(404)
    uid = meeting.user_id
    db.session.delete(meeting)
    db.session.commit()
    flash('Session removed.', 'info')
    return redirect(url_for('members.admin_doc_detail', user_id=uid) + '#meetings')
