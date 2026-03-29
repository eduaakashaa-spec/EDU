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
        return self.tier_expires_at > datetime.now(timezone.utc)

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


class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    interested = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
