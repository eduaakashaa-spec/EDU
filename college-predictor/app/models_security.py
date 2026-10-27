"""Sign-up log used for rate limiting and for reviewing refused sign-ups (new table; created by db.create_all)."""
from datetime import datetime, timezone

from app.extensions import db


class SignupLog(db.Model):
    __tablename__ = 'signup_log'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), index=True)
    email = db.Column(db.String(200))
    reason = db.Column(db.String(30), index=True)           # created | honeypot | too_fast | expired | rate_limited | bad_name | disposable | duplicate
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), index=True)
