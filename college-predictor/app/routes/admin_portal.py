"""EA Admin Control Panel — ports (and extends) the legacy Apps Script
admin portal that lived at eduaakashaa.in/ea-admin-portal.

Legacy tabs → in-app equivalents:
    Members        → /admin/users  (list in membership.py; the mutating
                     actions — add / tier & validity / password / delete —
                     live here)
    Announcements  → /admin/announcements (CRUD; shown on member dashboards)
    Schedule       → /admin/schedule      (CRUD; shown on member dashboards)
    Messages       → /admin/messages      (template library; per-member
                     WhatsApp / email drafts with placeholders resolved)
    DASA Review    → dropped (Jul 2026): /counsellor-dashboard read a Google
                     Sheet nothing on this site writes to. DASA leads live in
                     the DB (/admin/leads).
    Documents      → needs member file uploads; on the roadmap

Every route requires the admin tier (same RBAC as the rest of /admin).
"""
from datetime import datetime, timedelta, timezone

from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user

from app.decorators import admin_required, safe_next
from app.extensions import db, bcrypt
from app.models import (AlumniProfile, Announcement, CollegeSurvey,
                        ContactInquiry, DasaLead, MentorMeeting, PageLead,
                        Payment, Prediction, ScheduleEvent, User)
from app.services import mailer
from app.services.mailer import is_configured as mail_configured
from app.services.mailer import send_async
from app.models_membership import (APP_STATUSES, MembershipApplication,
                                   MembershipInvoice)
from app.services.email_templates import (EMAIL_TEMPLATES, LOGO_URL, PHONE_UAE,
                                          SENDER_EMAIL, SITE, WHATSAPP_NUMBER)
from app.services.queries import count_if as _n, sum_if as _sum_if

admin_portal_bp = Blueprint('admin_portal', __name__)

TIERS = ('free', 'premium', 'admin')
AUDIENCES = ('all', 'students', 'parents')
EVENT_TYPES = ('Exam', 'Counselling', 'Deadline', 'Webinar', 'Other')


IST = timezone(timedelta(hours=5, minutes=30))


def _utcnow_naive():
    """Stored datetimes are timezone-naive UTC (the columns carry no tz)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _now_ist_naive():
    """Schedule events are entered (and shown) as IST wall-clock times, so
    upcoming/past checks must compare against IST 'now', not UTC."""
    return datetime.now(IST).replace(tzinfo=None)


def _parse_date(value):
    """'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM' → naive datetime, else None."""
    value = (value or '').strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _parse_expiry(value):
    """Like _parse_date, but a date-only value means 'valid THROUGH that day'
    (that's what the admin promises the member), so store end-of-day."""
    parsed = _parse_date(value)
    if parsed is not None and len((value or '').strip()) == 10:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    return parsed


# --------------------------------------------------------------------------- #
# Overview — the control panel home
# --------------------------------------------------------------------------- #
@admin_portal_bp.route('/admin')
@admin_required
def home():
    now = _utcnow_naive()
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    # --- Members (one aggregate query) ---
    (users_total, users_free, users_premium, users_admin, users_guides,
     premium_active, premium_expired, users_new_7d, users_new_30d) = db.session.query(
        db.func.count(User.id),
        _n(User.tier == 'free'),
        _n(User.tier == 'premium'),
        _n(User.tier == 'admin'),
        _n(User.tier == 'mentor'),
        _n(db.and_(User.tier == 'premium',
                   db.or_(User.tier_expires_at.is_(None), User.tier_expires_at > now))),
        _n(db.and_(User.tier == 'premium', User.tier_expires_at.isnot(None),
                   User.tier_expires_at <= now)),
        _n(User.created_at >= d7),
        _n(User.created_at >= d30),
    ).one()

    # --- Membership pipeline & revenue (amounts stored in paise) ---
    status_counts = dict(db.session.query(MembershipApplication.status,
                                          db.func.count(MembershipApplication.id))
                         .group_by(MembershipApplication.status).all())
    apps_by_status = {s: status_counts.get(s, 0) for s in APP_STATUSES}
    apps_total = sum(status_counts.values())
    apps_new_7d = db.session.query(
        db.func.count(MembershipApplication.id)).filter(
        MembershipApplication.created_at >= d7).scalar()
    revenue_paise, pending_paise = db.session.query(
        db.func.coalesce(db.func.sum(MembershipInvoice.amount_paid), 0),
        db.func.coalesce(db.func.sum(MembershipInvoice.balance_due), 0)).one()
    revenue_inr = int(revenue_paise) // 100
    pending_inr = int(pending_paise) // 100

    # --- Leads & inquiries ---
    page_leads, page_leads_7d = db.session.query(
        db.func.count(PageLead.id), _n(PageLead.created_at >= d7)).one()
    dasa_leads, dasa_leads_7d = db.session.query(
        db.func.count(DasaLead.id), _n(DasaLead.timestamp >= d7)).one()
    leads_total = page_leads + dasa_leads
    leads_new_7d = page_leads_7d + dasa_leads_7d
    inquiries_total = db.session.query(db.func.count(ContactInquiry.id)).scalar()

    # --- College Guides (alumni network) ---
    guides_total, guides_active, guides_new, guides_referred = db.session.query(
        db.func.count(AlumniProfile.id),
        _n(AlumniProfile.status == 'Active'),
        _n(AlumniProfile.status == 'New'),
        _n(AlumniProfile.referred_by.isnot(None)),
    ).one()
    completed = MentorMeeting.status == 'Completed'
    sessions_done, payout_total, payout_paid = db.session.query(
        _n(db.and_(MentorMeeting.kind.in_(('meeting', 'video')), completed)),
        _sum_if(MentorMeeting.payout_amount, completed),
        _sum_if(MentorMeeting.payout_amount,
                db.and_(completed, MentorMeeting.paid.is_(True))),
    ).one()
    payout_total, payout_paid = int(payout_total), int(payout_paid)
    payout_pending = payout_total - payout_paid

    # --- Surveys ---
    surveys_total, survey_colleges, survey_want_guide, avg_rec = db.session.query(
        db.func.count(CollegeSurvey.id),
        db.func.count(db.distinct(CollegeSurvey.institute)),
        _n(CollegeSurvey.wants_to_mentor.is_(True)),
        db.func.avg(CollegeSurvey.recommend_score),
    ).one()
    survey_avg_rec = round(float(avg_rec), 1) if avg_rec is not None else None

    # --- Chart 1: activity over the last 8 weeks (users / leads / surveys) ---
    weeks = 8
    start = now - timedelta(weeks=weeks)

    def bucket(rows):
        counts = [0] * weeks
        for (dt,) in rows:
            if dt is None:
                continue
            wk = int((dt - start).days // 7)
            if 0 <= wk < weeks:
                counts[wk] += 1
        return counts

    users_series = bucket(User.query.with_entities(User.created_at)
                          .filter(User.created_at >= start).all())
    leads_series = [a + b for a, b in zip(
        bucket(PageLead.query.with_entities(PageLead.created_at)
               .filter(PageLead.created_at >= start).all()),
        bucket(DasaLead.query.with_entities(DasaLead.timestamp)
               .filter(DasaLead.timestamp >= start).all()))]
    surveys_series = bucket(CollegeSurvey.query.with_entities(CollegeSurvey.created_at)
                            .filter(CollegeSurvey.created_at >= start).all())
    week_labels = [(start + timedelta(weeks=i)).strftime('%d %b') for i in range(weeks)]

    # --- Chart 3: leads by source (top 8) ---
    src_rows = (db.session.query(PageLead.source, db.func.count(PageLead.id))
                .group_by(PageLead.source)
                .order_by(db.func.count(PageLead.id).desc()).limit(8).all())

    charts = {
        'weeks': {'labels': week_labels, 'users': users_series,
                  'leads': leads_series, 'surveys': surveys_series},
        'tiers': {'labels': ['Free', 'Premium', 'Admin', 'College Guide'],
                  'values': [users_free, users_premium, users_admin, users_guides]},
        'apps': {'labels': list(APP_STATUSES),
                 'values': [apps_by_status[s] for s in APP_STATUSES]},
        'sources': {'labels': [s or '(none)' for s, _ in src_rows],
                    'values': [c for _, c in src_rows]},
    }

    # --- recent activity ---
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    recent_leads = PageLead.query.order_by(PageLead.created_at.desc()).limit(6).all()
    recent_apps = (MembershipApplication.query
                   .order_by(MembershipApplication.created_at.desc()).limit(6).all())
    recent_surveys = CollegeSurvey.query.order_by(CollegeSurvey.created_at.desc()).limit(6).all()
    recent_guides = AlumniProfile.query.order_by(AlumniProfile.created_at.desc()).limit(6).all()
    upcoming = (ScheduleEvent.query.filter(ScheduleEvent.starts_at >= _now_ist_naive())
                .order_by(ScheduleEvent.starts_at.asc()).limit(6).all())
    live_announcements = (Announcement.query.filter_by(active=True)
                          .order_by(Announcement.pinned.desc(),
                                    Announcement.created_at.desc())
                          .limit(5).all())

    stats = {
        'users_total': users_total, 'users_free': users_free,
        'users_premium': users_premium, 'users_admin': users_admin,
        'users_guides': users_guides, 'premium_active': premium_active,
        'premium_expired': premium_expired, 'users_new_7d': users_new_7d,
        'users_new_30d': users_new_30d,
        'apps_total': apps_total, 'apps_new': apps_by_status['New'],
        'apps_paid': apps_by_status['Paid'], 'apps_new_7d': apps_new_7d,
        'revenue_inr': revenue_inr, 'pending_inr': pending_inr,
        'page_leads': page_leads, 'dasa_leads': dasa_leads,
        'leads_total': leads_total, 'inquiries_total': inquiries_total,
        'leads_new_7d': leads_new_7d,
        'guides_total': guides_total, 'guides_active': guides_active,
        'guides_new': guides_new, 'guides_referred': guides_referred,
        'sessions_done': sessions_done, 'payout_total': payout_total,
        'payout_paid': payout_paid, 'payout_pending': payout_pending,
        'surveys_total': surveys_total, 'survey_colleges': survey_colleges,
        'survey_want_guide': survey_want_guide, 'survey_avg_rec': survey_avg_rec,
    }

    return render_template('admin/portal_home.html', admin_tab='overview',
                           stats=stats, charts=charts,
                           recent_users=recent_users, recent_leads=recent_leads,
                           recent_apps=recent_apps, recent_surveys=recent_surveys,
                           recent_guides=recent_guides, upcoming=upcoming,
                           live_announcements=live_announcements)


# --------------------------------------------------------------------------- #
# Members — mutating actions (list lives at membership.admin_users)
# --------------------------------------------------------------------------- #
def _users_url():
    return safe_next(request.form.get('next')) or url_for('membership.admin_users')


@admin_portal_bp.route('/admin/email-test', methods=['GET', 'POST'])
@admin_required
def email_test():
    """Self-service SMTP diagnostics: sends synchronously and shows the real
    error on screen, so email can be debugged without a shell."""
    if request.method == 'POST':
        to = (request.form.get('to') or '').strip() or current_user.email
        if not mailer.is_configured():
            flash('No email transport configured — set RESEND_API_KEY (production), or '
                  'SMTP_HOST / SMTP_USER / SMTP_PASS (local dev). Check the Environment '
                  'tab on your host.', 'danger')
            return redirect(url_for('admin_portal.email_test'))
        try:
            mailer.send_now(
                to, 'EduAakashaa SMTP test ✅',
                'If you can read this, your SMTP settings work and automated '
                'emails (member logins, document verification, invoices) will send.')
            flash(f'Test email sent to {to}. If it does not arrive within a minute, '
                  f'check the spam folder.', 'success')
        except Exception as exc:                      # surface the real reason
            flash(f'SEND FAILED — {type(exc).__name__}: {exc}', 'danger')
        return redirect(url_for('admin_portal.email_test'))

    return render_template('admin/email_test.html', admin_tab='templates',
                           status=mailer.config_status())


def _email_new_member(user, password):
    """Send a new member their login details. Best-effort (no-op without SMTP);
    the admin-set password is emailed in plaintext so the member can sign in —
    the account has no self-service flow otherwise."""
    first = user.name.split(' ')[0] if user.name else 'there'
    login_url = SITE + url_for('auth.login')
    validity = ('No expiry' if user.tier_expires_at is None
                else user.tier_expires_at.strftime('%d %b %Y'))
    send_async(
        user.email,
        'Your EduAakashaa account is ready 🎓',
        (f"Hi {first},\n\nAn EduAakashaa account has been created for you. Here are your "
         f"login details:\n\n"
         f"  Login page : {login_url}\n"
         f"  Email      : {user.email}\n"
         f"  Password   : {password}\n"
         f"  Plan       : {user.tier.capitalize()}\n"
         f"  Valid until: {validity}\n\n"
         f"Please keep this email safe. For any help, WhatsApp us at {WHATSAPP_NUMBER}.\n\n"
         f"— Team EduAakashaa"),
        (f"<p>Hi {first},</p><p>An <strong>EduAakashaa</strong> account has been created for "
         f"you. Here are your login details:</p>"
         "<table style='border-collapse:collapse;font-size:14px'>"
         f"<tr><td style='padding:4px 12px 4px 0;color:#666'>Login page</td><td><a href='{login_url}'>{login_url}</a></td></tr>"
         f"<tr><td style='padding:4px 12px 4px 0;color:#666'>Email</td><td><strong>{user.email}</strong></td></tr>"
         f"<tr><td style='padding:4px 12px 4px 0;color:#666'>Password</td><td><strong>{password}</strong></td></tr>"
         f"<tr><td style='padding:4px 12px 4px 0;color:#666'>Plan</td><td>{user.tier.capitalize()}</td></tr>"
         f"<tr><td style='padding:4px 12px 4px 0;color:#666'>Valid until</td><td>{validity}</td></tr>"
         "</table>"
         f"<p style='margin:22px 0'><a href='{login_url}' style='background:#0E3A8A;color:#fff;"
         "text-decoration:none;padding:12px 26px;border-radius:8px;font-weight:700'>Log in →</a></p>"
         f"<p style='color:#666;font-size:13px'>Please keep this email safe. Need help? "
         f"WhatsApp us at {WHATSAPP_NUMBER}.</p><p>— Team EduAakashaa</p>"))


@admin_portal_bp.route('/admin/users/add', methods=['POST'])
@admin_required
def user_add():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    tier = request.form.get('tier') or 'free'
    password = request.form.get('password') or ''
    expires = _parse_expiry(request.form.get('tier_expires_at'))
    notify = request.form.get('notify') == '1'   # "Email login details" checkbox (checked by default)

    if not name or not email:
        flash('Name and email are required.', 'danger')
        return redirect(_users_url())
    if tier not in TIERS:
        flash('Invalid tier.', 'danger')
        return redirect(_users_url())
    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'danger')
        return redirect(_users_url())
    if User.query.filter_by(email=email).first():
        flash(f'A user with email {email} already exists.', 'danger')
        return redirect(_users_url())

    user = User(name=name, email=email, tier=tier, tier_expires_at=expires,
                password_hash=bcrypt.generate_password_hash(password).decode())
    db.session.add(user)
    db.session.commit()

    msg = f'Member {name} ({email}) created on the {tier} tier.'
    if notify:
        _email_new_member(user, password)
        msg += (' Login details emailed.' if mail_configured()
                else ' (Email not sent — SMTP is not configured.)')
    flash(msg, 'success')
    return redirect(_users_url())


@admin_portal_bp.route('/admin/users/<int:user_id>/update', methods=['POST'])
@admin_required
def user_update(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(_users_url())

    tier = request.form.get('tier') or user.tier
    expires = _parse_expiry(request.form.get('tier_expires_at'))
    clear_expiry = request.form.get('clear_expiry') == '1'

    if tier not in TIERS:
        flash('Invalid tier.', 'danger')
        return redirect(_users_url())

    # Lockout guard: an admin cannot remove their own admin tier.
    if user.id == current_user.id and tier != 'admin':
        flash('You cannot remove your own admin access.', 'danger')
        return redirect(_users_url())

    user.tier = tier
    if clear_expiry:
        user.tier_expires_at = None
    elif expires is not None:
        user.tier_expires_at = expires
    db.session.commit()

    expiry_txt = ('no expiry' if user.tier_expires_at is None
                  else 'expires ' + user.tier_expires_at.strftime('%d %b %Y'))
    flash(f'{user.email} → {user.tier} ({expiry_txt}).', 'success')
    return redirect(_users_url())


@admin_portal_bp.route('/admin/users/<int:user_id>/password', methods=['POST'])
@admin_required
def user_password(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(_users_url())

    password = request.form.get('password') or ''
    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'danger')
        return redirect(_users_url())

    user.password_hash = bcrypt.generate_password_hash(password).decode()
    db.session.commit()
    flash(f'Password updated for {user.email}.', 'success')
    return redirect(_users_url())


@admin_portal_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def user_delete(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(_users_url())
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(_users_url())
    if user.is_admin:
        flash('Demote the admin to free/premium before deleting.', 'danger')
        return redirect(_users_url())

    # Child rows first — the FKs have no ON DELETE CASCADE.
    Prediction.query.filter_by(user_id=user.id).delete()
    Payment.query.filter_by(user_id=user.id).delete()
    email = user.email
    db.session.delete(user)
    db.session.commit()
    flash(f'Deleted {email} (and their saved predictions/payments).', 'success')
    return redirect(_users_url())


# --------------------------------------------------------------------------- #
# Announcements
# --------------------------------------------------------------------------- #
@admin_portal_bp.route('/admin/announcements', methods=['GET', 'POST'])
@admin_required
def announcements():
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        body = (request.form.get('body') or '').strip()
        audience = request.form.get('audience') or 'all'
        pinned = request.form.get('pinned') == '1'
        if not title or not body:
            flash('Title and message are required.', 'danger')
        else:
            if audience not in AUDIENCES:
                audience = 'all'
            db.session.add(Announcement(title=title, body=body,
                                        audience=audience, pinned=pinned))
            db.session.commit()
            flash('Announcement published.', 'success')
        return redirect(url_for('admin_portal.announcements'))

    rows = (Announcement.query
            .order_by(Announcement.pinned.desc(), Announcement.created_at.desc())
            .all())
    return render_template('admin/announcements.html', admin_tab='announcements',
                           rows=rows, audiences=AUDIENCES)


@admin_portal_bp.route('/admin/announcements/<int:ann_id>/toggle', methods=['POST'])
@admin_required
def announcement_toggle(ann_id):
    ann = db.session.get(Announcement, ann_id)
    if ann is None:
        flash('Announcement not found.', 'danger')
    else:
        field = request.form.get('field')
        if field == 'pinned':
            ann.pinned = not ann.pinned
        else:
            ann.active = not ann.active
        db.session.commit()
        flash('Announcement updated.', 'success')
    return redirect(url_for('admin_portal.announcements'))


@admin_portal_bp.route('/admin/announcements/<int:ann_id>/delete', methods=['POST'])
@admin_required
def announcement_delete(ann_id):
    ann = db.session.get(Announcement, ann_id)
    if ann is not None:
        db.session.delete(ann)
        db.session.commit()
        flash('Announcement deleted.', 'success')
    return redirect(url_for('admin_portal.announcements'))


# --------------------------------------------------------------------------- #
# Schedule (exams / events)
# --------------------------------------------------------------------------- #
@admin_portal_bp.route('/admin/schedule', methods=['GET', 'POST'])
@admin_required
def schedule():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        starts_at = _parse_date(request.form.get('starts_at'))
        if not name or starts_at is None:
            flash('Event name and a valid start date are required.', 'danger')
        else:
            event_type = request.form.get('event_type') or 'Exam'
            if event_type not in EVENT_TYPES:
                event_type = 'Other'
            db.session.add(ScheduleEvent(
                name=name,
                description=(request.form.get('description') or '').strip(),
                event_type=event_type,
                location=(request.form.get('location') or '').strip(),
                starts_at=starts_at,
                ends_at=_parse_date(request.form.get('ends_at')),
                important=request.form.get('important') == '1'))
            db.session.commit()
            flash('Event added to the schedule.', 'success')
        return redirect(url_for('admin_portal.schedule'))

    rows = ScheduleEvent.query.order_by(ScheduleEvent.starts_at.asc()).all()
    return render_template('admin/schedule.html', admin_tab='schedule',
                           rows=rows, event_types=EVENT_TYPES, now=_now_ist_naive())


@admin_portal_bp.route('/admin/schedule/<int:event_id>/delete', methods=['POST'])
@admin_required
def schedule_delete(event_id):
    ev = db.session.get(ScheduleEvent, event_id)
    if ev is not None:
        db.session.delete(ev)
        db.session.commit()
        flash('Event deleted.', 'success')
    return redirect(url_for('admin_portal.schedule'))


# --------------------------------------------------------------------------- #
# Messages — template library (WhatsApp / email drafts, no SMTP needed)
# --------------------------------------------------------------------------- #
MESSAGE_TEMPLATES = {
    'welcome': {
        'label': 'Welcome / onboarding',
        'subject': 'Welcome to EduAakashaa Premium, {firstName}!',
        'body': ('Hi {firstName},\n\n'
                 'Welcome to EduAakashaa! Your {plan} membership is active'
                 '{validity}. You now have access to every premium tool — '
                 'predictors, expert reports and counsellor support.\n\n'
                 'Start here: https://www.eduaakashaa.in/dashboard\n\n'
                 'Questions? Just reply to this message.\n— Team EduAakashaa'),
    },
    'renewal': {
        'label': 'Renewal reminder',
        'subject': 'Your EduAakashaa membership{validity_short}',
        'body': ('Hi {firstName},\n\n'
                 'A quick reminder that your {plan} membership{validity}. '
                 'Renew in time to keep uninterrupted access to the premium '
                 'predictors and expert reports during counselling season.\n\n'
                 'Renew: https://www.eduaakashaa.in/members-registration\n'
                 '— Team EduAakashaa'),
    },
    'counselling': {
        'label': 'Counselling check-in',
        'subject': 'How is your counselling preparation going, {firstName}?',
        'body': ('Hi {firstName},\n\n'
                 'Counselling season is moving fast — have you finalised your '
                 'choice list? Book a session with a counsellor and we\'ll '
                 'review it together before you lock.\n\n'
                 'WhatsApp us any time: +91 80157 22706\n— Team EduAakashaa'),
    },
    'docs': {
        'label': 'Document reminder',
        'subject': 'Documents pending for your EduAakashaa profile',
        'body': ('Hi {firstName},\n\n'
                 'We are still missing a few documents needed to prepare your '
                 'report. Please send them over WhatsApp or reply to this '
                 'email so we can proceed.\n\n— Team EduAakashaa'),
    },
}


def _fill_template(tpl, user):
    first = (user.name or '').split(' ')[0] or 'there'
    if user.tier_expires_at:
        validity = ' (valid until %s)' % user.tier_expires_at.strftime('%d %b %Y')
        validity_short = ' — valid until %s' % user.tier_expires_at.strftime('%d %b %Y')
    else:
        validity = ''
        validity_short = ''
    mapping = {'firstName': first, 'name': user.name or '',
               'plan': user.tier, 'memberId': f'EA-{user.id:04d}',
               'validity': validity, 'validity_short': validity_short}
    subject = tpl['subject']
    body = tpl['body']
    for k, v in mapping.items():
        subject = subject.replace('{%s}' % k, str(v))
        body = body.replace('{%s}' % k, str(v))
    return subject, body


@admin_portal_bp.route('/admin/messages')
@admin_required
def messages():
    tpl_key = request.args.get('template') or 'welcome'
    if tpl_key not in MESSAGE_TEMPLATES:
        tpl_key = 'welcome'
    group = request.args.get('group') or 'premium'

    now = _utcnow_naive()
    query = User.query
    if group == 'premium':
        query = query.filter(User.tier == 'premium')
    elif group == 'expired':
        query = query.filter(User.tier == 'premium',
                             User.tier_expires_at.isnot(None),
                             User.tier_expires_at <= now)
    elif group == 'free':
        query = query.filter(User.tier == 'free')
    users = query.order_by(User.created_at.desc()).limit(200).all()

    tpl = MESSAGE_TEMPLATES[tpl_key]
    prepared = []
    for u in users:
        subject, body = _fill_template(tpl, u)
        prepared.append({'user': u, 'subject': subject, 'body': body})

    return render_template('admin/messages.html', admin_tab='messages',
                           templates=MESSAGE_TEMPLATES, tpl_key=tpl_key,
                           group=group, prepared=prepared)


# --------------------------------------------------------------------------- #
# Email templates — pick a template, fill placeholders, open a ready draft
# (Gmail compose / mailto) from eduaakashaa@gmail.com. Nothing is auto-sent.
# The registry itself lives in app/services/email_templates.py.
# --------------------------------------------------------------------------- #


def _recipient_directory():
    """Everyone the admin might email, deduped by address: members first (their
    tier matters most), then College Guides, page leads and inquiries. Only
    name/email/kind/hint go to the browser — nothing sensitive."""
    people, seen = [], set()

    def add(name, email, kind, hint=''):
        email = (email or '').strip().lower()
        if '@' not in email or email in seen:
            return
        seen.add(email)
        people.append({'name': (name or '').strip() or email.split('@')[0],
                       'email': email, 'kind': kind, 'hint': (hint or '').strip()})

    for name, email, tier in (User.query
                              .with_entities(User.name, User.email, User.tier)
                              .order_by(User.created_at.desc()).limit(500)):
        add(name, email, 'guide' if tier == 'mentor' else 'member', tier)
    for name, email, univ in (AlumniProfile.query
                              .with_entities(AlumniProfile.name, AlumniProfile.email,
                                             AlumniProfile.university)
                              .order_by(AlumniProfile.created_at.desc()).limit(300)):
        add(name, email, 'guide', univ)
    for name, email, source in (PageLead.query
                                .with_entities(PageLead.name, PageLead.email,
                                               PageLead.source)
                                .filter(PageLead.email.isnot(None),
                                        PageLead.email != '')
                                .order_by(PageLead.created_at.desc()).limit(300)):
        add(name, email, 'lead', source)
    for first, last, email in (ContactInquiry.query
                               .with_entities(ContactInquiry.first_name,
                                              ContactInquiry.last_name,
                                              ContactInquiry.email)
                               .order_by(ContactInquiry.created_at.desc()).limit(200)):
        add(' '.join(p for p in (first, last) if p), email, 'inquiry')
    return people


@admin_portal_bp.route('/admin/templates')
@admin_required
def templates():
    categories = []
    for t in EMAIL_TEMPLATES:
        if t['category'] not in categories:
            categories.append(t['category'])
    return render_template('admin/templates.html', admin_tab='templates',
                           email_templates=EMAIL_TEMPLATES, categories=categories,
                           recipients=_recipient_directory(), sender=SENDER_EMAIL,
                           logo_url=LOGO_URL, site=SITE,
                           whatsapp=WHATSAPP_NUMBER, phone_uae=PHONE_UAE)
