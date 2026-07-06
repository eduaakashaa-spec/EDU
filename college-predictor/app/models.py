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
    tier = db.Column(db.String(20), nullable=False, default='free')  # free | premium | admin
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
