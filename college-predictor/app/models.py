"""Database models."""
from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    tier = db.Column(db.String(20), nullable=False, default='free')  # free | premium | admin | mentor
    tier_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    predictions = db.relationship('Prediction', backref='user', lazy='dynamic')
    payments = db.relationship('Payment', backref='user', lazy='dynamic')

    @property
    def is_premium(self):
        if self.tier == 'admin':
            return True
        if self.tier != 'premium':
            return False
        if self.tier_expires_at is None:
            return True
        # The column has no timezone, so Postgres hands back naive datetimes;
        # treat stored values as UTC or the comparison raises TypeError.
        expires = self.tier_expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return expires > datetime.now(timezone.utc)

    @property
    def is_admin(self):
        return self.tier == 'admin'

    @property
    def is_mentor(self):
        return self.tier == 'mentor'


class DasaLead(db.Model):
    __tablename__ = 'dasa_leads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(200))
    rank = db.Column(db.Integer)
    quota = db.Column(db.String(50))
    branch = db.Column(db.String(100))
    institute = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    source = db.Column(db.String(50), default='dasa_predictor')


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    predictor = db.Column(db.String(30))  # josaa | dasa | tnea
    query_json = db.Column(db.Text)
    results_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    razorpay_order_id = db.Column(db.String(100))
    razorpay_payment_id = db.Column(db.String(100))
    amount = db.Column(db.Integer)  # paise
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20), default='created')  # created | paid | failed
    plan = db.Column(db.String(30))  # e.g. premium_monthly
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class PageLead(db.Model):
    """Generic lead/response captured from any page form or assessment.

    The full submitted payload is kept as JSON so nothing is lost; name/email/
    phone are extracted into columns for searching and admin display."""
    __tablename__ = 'page_leads'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(60), index=True)  # page slug, e.g. 'free-report'
    name = db.Column(db.String(150))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(40))
    payload_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    interested = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Announcement(db.Model):
    """Admin-posted notices shown on member dashboards (ports the
    Announcements tab of the legacy Apps Script member portal)."""
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    audience = db.Column(db.String(20), nullable=False, default='all')  # all | students | parents
    pinned = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ScheduleEvent(db.Model):
    """Exams / counselling events managed by admins and shown to members
    (ports the Schedule tab of the legacy Apps Script member portal)."""
    __tablename__ = 'schedule_events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(40), default='Exam')  # Exam | Counselling | Deadline | Webinar | Other
    location = db.Column(db.String(200))
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=True)
    important = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class AlumniProfile(db.Model):
    """Alumni & current students at top universities who join the EduAakashaa
    mentor network to share first-hand college experience with parents (paid
    per meeting). Collected via the public /alumni-network page and matched to
    parents by admins. Resume + photo are stored in the DB so they survive
    Render's ephemeral filesystem."""
    __tablename__ = 'alumni_profiles'

    id = db.Column(db.Integer, primary_key=True)

    # the mentor's login account (tier='mentor'); nullable so a profile can
    # exist without an account (e.g. admin-imported) and vice versa
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    user = db.relationship('User', backref=db.backref('alumni_profile', uselist=False))

    # identity / contact
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False, index=True)
    phone = db.Column(db.String(40))            # WhatsApp
    country = db.Column(db.String(80))          # current location
    city = db.Column(db.String(80))

    # academic — the matching keys
    university = db.Column(db.String(200), nullable=False)   # college attended
    program = db.Column(db.String(200))         # course / branch / major
    degree_level = db.Column(db.String(40))     # UG / PG / PhD / Diploma
    grad_year = db.Column(db.String(16))        # 2025, "2027 (expected)", …
    stage = db.Column(db.String(30))            # current-student | alumni | working
    admission_route = db.Column(db.String(160))  # JEE/JOSAA, DASA/CIWG, SAT, …
    current_role = db.Column(db.String(200))    # role @ company, if working
    linkedin = db.Column(db.String(300))
    languages = db.Column(db.String(200))       # languages they can mentor in
    bio = db.Column(db.Text)                     # what they can help parents with
    availability = db.Column(db.String(200))    # preferred times / weekly hours

    # resume — stored as an external link (Google Drive / Dropbox / etc.) to
    # keep multi-MB files out of Postgres. The legacy resume_data columns are
    # retained (nullable) so any pre-link uploads still download.
    resume_url = db.Column(db.String(500))
    resume_data = db.Column(db.LargeBinary)     # legacy — new rows use resume_url
    resume_name = db.Column(db.String(255))
    resume_mime = db.Column(db.String(100))
    # photo is kept in the DB but capped small (~200 KB); Render's disk is wiped
    # on every deploy so we can't rely on the filesystem for it.
    photo_data = db.Column(db.LargeBinary)
    photo_name = db.Column(db.String(255))
    photo_mime = db.Column(db.String(100))

    # referral programme
    referral_code = db.Column(db.String(16), unique=True, index=True)
    referred_by = db.Column(db.String(16), index=True)   # referrer's code

    # workflow
    status = db.Column(db.String(20), nullable=False, default='New')  # New | Verified | Active | Rejected
    admin_notes = db.Column(db.Text)
    consent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def has_resume(self):
        return bool(self.resume_url) or self.resume_data is not None

    @property
    def has_photo(self):
        return self.photo_data is not None


class MentorMeeting(db.Model):
    """A logged session (or referral bonus) for a mentor — the source of the
    mentor's 'calls attended' count and their INR payout ledger. Admins create
    these when a mentor completes a meeting with a parent."""
    __tablename__ = 'mentor_meetings'

    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'),
                          nullable=False, index=True)
    kind = db.Column(db.String(20), nullable=False, default='meeting')  # meeting | referral | bonus | adjustment
    # for auto-credited referral bonuses: which referred mentor triggered this
    # (a plain id, not an FK — used to credit the bonus exactly once per referral)
    referred_alumni_id = db.Column(db.Integer, nullable=True, index=True)
    parent_name = db.Column(db.String(150))     # who they met
    topic = db.Column(db.String(200))           # college / topic discussed
    meeting_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='Completed')  # Scheduled | Completed | No-show | Cancelled
    payout_amount = db.Column(db.Integer, nullable=False, default=0)  # whole INR (₹)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    paid_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    alumni = db.relationship('AlumniProfile',
                             backref=db.backref('meetings', lazy='dynamic',
                                                cascade='all, delete-orphan'))

    @property
    def counts_as_call(self):
        return self.kind == 'meeting' and self.status == 'Completed'


class MentorMessage(db.Model):
    """A message in the mentor ↔ admin thread. Mentors send from their portal;
    admins read/reply from the alumni detail page."""
    __tablename__ = 'mentor_messages'

    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'),
                          nullable=False, index=True)
    sender = db.Column(db.String(10), nullable=False)   # 'mentor' | 'admin'
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    alumni = db.relationship('AlumniProfile',
                             backref=db.backref('messages', lazy='dynamic',
                                                cascade='all, delete-orphan'))
