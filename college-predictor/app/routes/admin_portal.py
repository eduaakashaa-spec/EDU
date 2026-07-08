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
    DASA Review    → covered by /counsellor-dashboard (in-app tool)
    Documents      → needs member file uploads; on the roadmap

Every route requires the admin tier (same RBAC as the rest of /admin).
"""
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user

from app.decorators import admin_required
from app.extensions import db, bcrypt
from app.models import (AlumniProfile, Announcement, CollegeSurvey,
                        ContactInquiry, DasaLead, MentorMeeting, PageLead,
                        Payment, Prediction, ScheduleEvent, User)
from app.models_membership import (APP_STATUSES, MembershipApplication,
                                   MembershipInvoice)

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
def _sum(col, *filters):
    """Return coalesced SUM(col) over the given filters as a plain int."""
    q = db.session.query(db.func.coalesce(db.func.sum(col), 0))
    for f in filters:
        q = q.filter(f)
    return int(q.scalar() or 0)


@admin_portal_bp.route('/admin')
@admin_required
def home():
    now = _utcnow_naive()
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    # --- Members ---
    users_total = User.query.count()
    users_free = User.query.filter_by(tier='free').count()
    users_premium = User.query.filter_by(tier='premium').count()
    users_admin = User.query.filter_by(tier='admin').count()
    users_guides = User.query.filter_by(tier='mentor').count()
    premium_active = User.query.filter(
        User.tier == 'premium',
        db.or_(User.tier_expires_at.is_(None), User.tier_expires_at > now)).count()
    premium_expired = User.query.filter(
        User.tier == 'premium', User.tier_expires_at.isnot(None),
        User.tier_expires_at <= now).count()
    users_new_7d = User.query.filter(User.created_at >= d7).count()
    users_new_30d = User.query.filter(User.created_at >= d30).count()

    # --- Membership pipeline & revenue (amounts stored in paise) ---
    apps_total = MembershipApplication.query.count()
    apps_by_status = {s: MembershipApplication.query.filter_by(status=s).count()
                      for s in APP_STATUSES}
    apps_new_7d = MembershipApplication.query.filter(
        MembershipApplication.created_at >= d7).count()
    revenue_inr = _sum(MembershipInvoice.amount_paid) // 100
    pending_inr = _sum(MembershipInvoice.balance_due) // 100

    # --- Leads & inquiries ---
    page_leads = PageLead.query.count()
    dasa_leads = DasaLead.query.count()
    leads_total = page_leads + dasa_leads
    inquiries_total = ContactInquiry.query.count()
    leads_new_7d = (PageLead.query.filter(PageLead.created_at >= d7).count()
                    + DasaLead.query.filter(DasaLead.timestamp >= d7).count())

    # --- College Guides (alumni network) ---
    guides_total = AlumniProfile.query.count()
    guides_active = AlumniProfile.query.filter_by(status='Active').count()
    guides_new = AlumniProfile.query.filter_by(status='New').count()
    guides_referred = AlumniProfile.query.filter(
        AlumniProfile.referred_by.isnot(None)).count()
    sessions_done = MentorMeeting.query.filter(
        MentorMeeting.kind.in_(('meeting', 'video')),
        MentorMeeting.status == 'Completed').count()
    payout_total = _sum(MentorMeeting.payout_amount, MentorMeeting.status == 'Completed')
    payout_paid = _sum(MentorMeeting.payout_amount, MentorMeeting.status == 'Completed',
                       MentorMeeting.paid.is_(True))
    payout_pending = payout_total - payout_paid

    # --- Surveys ---
    surveys_total = CollegeSurvey.query.count()
    survey_colleges = db.session.query(CollegeSurvey.institute).distinct().count()
    survey_want_guide = CollegeSurvey.query.filter_by(wants_to_mentor=True).count()
    avg_rec = db.session.query(db.func.avg(CollegeSurvey.recommend_score)).scalar()
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
    # Only follow 'next' when it is a bare same-app path — anything with a
    # scheme/host (or a scheme-relative '//host') would be an open redirect.
    nxt = request.form.get('next') or ''
    parsed = urlparse(nxt)
    if nxt.startswith('/') and not nxt.startswith('//') and not parsed.scheme and not parsed.netloc:
        return nxt
    return url_for('membership.admin_users')


@admin_portal_bp.route('/admin/users/add', methods=['POST'])
@admin_required
def user_add():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    tier = request.form.get('tier') or 'free'
    password = request.form.get('password') or ''
    expires = _parse_expiry(request.form.get('tier_expires_at'))

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
    flash(f'Member {name} ({email}) created on the {tier} tier.', 'success')
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
