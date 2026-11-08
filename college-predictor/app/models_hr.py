"""HR letters: editable letter templates and the register of letters issued (offer, experience, relieving).

A letter keeps the template text and the values it was issued with, so a reprint is identical even if the template is edited later.
Access is limited to the HR Admin and Admin roles (see decorators.hr_required)."""
import json
from datetime import datetime, timezone

from app.extensions import db


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class HrLetterTemplate(db.Model):
    __tablename__ = 'hr_letter_templates'

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(20), unique=True, nullable=False)       # offer | experience | relieving
    body = db.Column(db.Text, nullable=False)                           # letter markup, see services/hr_letters.py
    version = db.Column(db.Integer, nullable=False, default=1)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=_now)


class HrLetterEmail(db.Model):
    """One attempt to email a letter (the PDF is attached). Kept so HR can see what was sent, to whom and when."""
    __tablename__ = 'hr_letter_emails'

    id = db.Column(db.Integer, primary_key=True)
    letter_id = db.Column(db.Integer, db.ForeignKey('hr_letters.id'), nullable=False, index=True)
    to_addr = db.Column(db.String(400), nullable=False)
    cc_addr = db.Column(db.String(400))
    from_addr = db.Column(db.String(200))
    subject = db.Column(db.String(200), nullable=False)
    ok = db.Column(db.Boolean, nullable=False, default=False)
    error = db.Column(db.String(300))
    sent_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sent_at = db.Column(db.DateTime, default=_now)


class HrLetter(db.Model):
    __tablename__ = 'hr_letters'
    __table_args__ = (db.UniqueConstraint('kind', 'fy', 'serial', name='uq_hr_letter_serial'),)

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(20), nullable=False, index=True)
    fy = db.Column(db.Integer, nullable=False)                          # Indian financial year, by its starting year (FY 2026-27 = 2026)
    serial = db.Column(db.Integer, nullable=False)                      # running number within kind and fy, never reused
    ref_no = db.Column(db.String(40), nullable=False, unique=True)
    person_name = db.Column(db.String(160), nullable=False, index=True)
    designation = db.Column(db.String(160))
    issue_date = db.Column(db.Date, nullable=False)
    values_json = db.Column(db.Text, nullable=False, default='{}')
    body_snapshot = db.Column(db.Text, nullable=False)
    template_version = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(10), nullable=False, default='issued')  # issued | void
    void_reason = db.Column(db.String(300))
    voided_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    voided_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=_now)

    @property
    def values(self):
        try:
            return json.loads(self.values_json or '{}')
        except ValueError:
            return {}
