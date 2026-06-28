"""
Membership / invoicing models — Phase 1 of the Apps Script → Flask migration.

Mirrors the legacy Google Sheet "Requests" tab (see
migration/LEGACY_APPS_SCRIPT_REFERENCE.md) but as proper relational tables in
PostgreSQL, with clean column names and transaction-safe invoice numbering.

To activate:
    1. `from app import models_membership  # noqa: F401` in app/__init__.py
       (right next to the existing `from app import models`).
    2. `python manage.py init_db` to create the tables.

Nothing imports this file yet, so adding it does not change current behaviour.
"""
from datetime import datetime, timezone
from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


# Membership paths offered on the premium-membership / members-registration page.
TIERS = ('Foundation Path', 'Aspirant Path', 'NRI / Global',
         'NRI · AI Report', 'NRI · Expert Guidance', 'Elite Mentorship')

# Application lifecycle
APP_STATUSES = ('New', 'Approved', 'Invoiced', 'Partially Paid', 'Paid')
PAYMENT_STATUSES = ('Unpaid', 'Partially Paid', 'Paid')


class MembershipApplication(db.Model):
    """One membership request — replaces a row in the Google Sheet 'Requests' tab."""
    __tablename__ = 'membership_applications'

    id = db.Column(db.Integer, primary_key=True)

    # Human-facing reference, e.g. EA-PREM-0007 (allocated transactionally)
    reference = db.Column(db.String(40), unique=True, index=True)

    # --- applicant (PII) ---
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(200), nullable=False, index=True)
    phone = db.Column(db.String(40))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))

    # --- selection & pricing (amounts stored in paise to avoid float errors) ---
    tier = db.Column(db.String(40))
    tier_price = db.Column(db.Integer, default=0)            # paise
    addons = db.Column(db.Text)                              # human-readable add-on summary
    addon_amount = db.Column(db.Integer, default=0)          # paise
    adhoc_items_json = db.Column(db.Text)                    # JSON list of {label, amount}
    adhoc_amount = db.Column(db.Integer, default=0)          # paise
    discount = db.Column(db.Integer, default=0)              # paise
    discount_reason = db.Column(db.String(255))

    # --- computed tax breakdown (GST inclusive, 18%) ---
    taxable_value = db.Column(db.Integer, default=0)         # paise
    cgst = db.Column(db.Integer, default=0)                  # paise
    sgst = db.Column(db.Integer, default=0)                  # paise
    igst = db.Column(db.Integer, default=0)                  # paise
    total_gst = db.Column(db.Integer, default=0)             # paise
    final_total = db.Column(db.Integer, default=0)           # paise, incl GST

    # --- status & audit ---
    status = db.Column(db.String(30), default='New', index=True)
    internal_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    invoice = db.relationship('MembershipInvoice', backref='application',
                              uselist=False, lazy='joined')

    def __repr__(self):
        return f'<MembershipApplication {self.reference} {self.email} {self.status}>'


class MembershipInvoice(db.Model):
    """A GST tax invoice issued for an application, plus its receipt once paid."""
    __tablename__ = 'membership_invoices'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer,
                              db.ForeignKey('membership_applications.id'),
                              nullable=False, index=True)

    # Unique, sequential, gap-free — allocated inside a DB transaction.
    invoice_no = db.Column(db.String(40), unique=True, index=True)
    invoice_date = db.Column(db.DateTime, default=_utcnow)
    invoice_pdf_path = db.Column(db.String(500))            # private path / object key (not a public link)

    # --- payment ---
    payment_status = db.Column(db.String(30), default='Unpaid')
    amount_paid = db.Column(db.Integer, default=0)          # paise
    balance_due = db.Column(db.Integer, default=0)          # paise
    payment_mode = db.Column(db.String(60))
    payment_ref = db.Column(db.String(120))
    payment_date = db.Column(db.DateTime, nullable=True)

    # --- receipt (issued when fully paid) ---
    receipt_no = db.Column(db.String(40), unique=True, index=True, nullable=True)
    receipt_pdf_path = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f'<MembershipInvoice {self.invoice_no} {self.payment_status}>'


class DocSequence(db.Model):
    """
    Monotonic counters for reference / invoice / receipt numbers.
    Replaces Apps Script PropertiesService (lastSeq / lastInv / lastRcpt).

    Allocate with a row-level lock so numbering is unique and gap-free:

        seq = (db.session.query(DocSequence)
               .filter_by(name='invoice').with_for_update().one())
        seq.value += 1
        db.session.commit()
    """
    __tablename__ = 'doc_sequences'

    name = db.Column(db.String(40), primary_key=True)   # 'reference' | 'invoice' | 'receipt'
    prefix = db.Column(db.String(20), default='')        # e.g. 'EA-PREM-', 'EA/', 'RCPT/'
    value = db.Column(db.Integer, default=0)

    def next_formatted(self, width=4):
        self.value += 1
        return f'{self.prefix}{str(self.value).zfill(width)}'
