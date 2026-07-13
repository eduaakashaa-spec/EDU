"""End-to-end self-check for the invoice feature + GST maths.

Hermetic: fresh SQLite, email stubbed. Run from college-predictor/:
    ../.venv/bin/python tests/test_invoices.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.models_membership import Invoice, Setting
from app.routes import invoices as INV
from app.services.pricing import compute_invoice_totals

# --- unit: GST maths (exclusive, on top) ------------------------------------
# 2×500 + 1000 = 2000; -200 discount +100 fee = 1900 taxable; 18% = 342; total 2242
t = compute_invoice_totals(
    [{'qty': 2, 'rate': 50000}, {'qty': 1, 'rate': 100000}],   # paise
    discount=20000, additional_fee=10000, customer_state='Tamil Nadu',
    home_state='Tamil Nadu', gst_rate=0.18)
assert t.subtotal == 200000, t.subtotal
assert t.taxable_value == 190000, t.taxable_value
assert t.total_gst == 34200 and t.total == 224200, (t.total_gst, t.total)
assert t.cgst == 17100 and t.sgst == 17100 and t.igst == 0, t   # intra-state split
# inter-state → IGST only
t2 = compute_invoice_totals([{'qty': 1, 'rate': 100000}], customer_state='Kerala',
                            home_state='Tamil Nadu', gst_rate=0.18)
assert t2.igst == 18000 and t2.cgst == 0, t2

# --- app wiring -------------------------------------------------------------
sent = []
INV.send_async = lambda *a, **k: sent.append(a)
app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='admin@ea.com', tier='admin',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

ac = app.test_client()
ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'}, follow_redirects=True)

# 1) settings: set the GSTIN once (edit later)
ac.post('/admin/invoice-settings', data={
    'brand_name': 'EduAakashaa', 'legal_name': 'EDUAAKASHAA PVT LTD',
    'gstin': '33ABCDE1234F1Z5', 'pan': 'ABCDE1234F', 'home_state': 'Tamil Nadu',
    'gst_pct': '18', 'address': 'Palani, TN', 'bank_ac_no': '123456789',
    'bank_ifsc': 'HDFC0001234'}, follow_redirects=True)
with app.app_context():
    assert db.session.get(Setting, 'gstin').value == '33ABCDE1234F1Z5'
    assert db.session.get(Setting, 'gst_rate').value == '0.18'   # % converted to fraction

# 2) create an invoice with two line items + discount + fee
r = ac.post('/admin/invoices/new', data={
    'customer_name': 'Priya Sharma', 'customer_email': 'priya@ex.com',
    'customer_gstin': '', 'customer_state': 'Kerala',
    'item_desc': ['Counselling session', 'Document review'],
    'item_qty': ['2', '1'], 'item_rate': ['500', '1000'],
    'discount': '200', 'additional_fee': '100', 'additional_fee_label': 'Processing',
    'gst_pct': '18', 'payment_status': 'Unpaid', 'payment_mode': '', 'payment_ref': ''},
    follow_redirects=True)
assert r.status_code == 200
with app.app_context():
    inv = Invoice.query.first()
    assert inv.invoice_no.startswith('EA/'), inv.invoice_no
    assert inv.subtotal == 200000 and inv.taxable_value == 190000
    assert inv.total_gst == 34200 and inv.total == 224200
    assert inv.igst == 34200 and inv.cgst == 0        # Kerala → inter-state
    assert len(inv.items) == 2 and inv.items[0]['qty'] == 2
    assert inv.seller.get('gstin') == '33ABCDE1234F1Z5'   # seller snapshot frozen on the invoice
    inv_id, token = inv.id, inv.public_token

# 3) admin detail renders the printable invoice
r = ac.get(f'/admin/invoices/{inv_id}')
assert r.status_code == 200 and b'Tax Invoice' in r.data and b'33ABCDE1234F1Z5' in r.data
assert b'Processing' in r.data and b'2,242.00' in r.data

# 4) email to customer (stubbed) -> recipient is the customer
sent.clear()
ac.post(f'/admin/invoices/{inv_id}/email', follow_redirects=True)
assert sent and sent[-1][0] == 'priya@ex.com', sent
with app.app_context():
    assert db.session.get(Invoice, inv_id).emailed_at is not None

# 5) mark paid -> amount_paid == total
ac.post(f'/admin/invoices/{inv_id}/payment',
        data={'payment_status': 'Paid', 'payment_mode': 'UPI', 'payment_ref': 'UTR9988'},
        follow_redirects=True)
with app.app_context():
    inv = db.session.get(Invoice, inv_id)
    assert inv.payment_status == 'Paid' and inv.amount_paid == inv.total

# 6) public tokenised view works without login and hides admin actions
pub = app.test_client()
r = pub.get(f'/invoice/{token}')
assert r.status_code == 200 and b'Priya Sharma' in r.data
assert b'Email to customer' not in r.data and b'Delete' not in r.data
assert pub.get('/invoice/wrong-token').status_code == 404

# 7) list + stats; non-admin blocked
r = ac.get('/admin/invoices')
assert r.status_code == 200 and b'EA/' in r.data
anon = app.test_client()
assert anon.get('/admin/invoices').status_code in (302, 401, 403)

# 8) later edit of the GSTIN does NOT change the already-issued invoice
ac.post('/admin/invoice-settings', data={'gstin': '33NEWGST9999Z5', 'gst_pct': '18'},
        follow_redirects=True)
with app.app_context():
    assert db.session.get(Invoice, inv_id).seller.get('gstin') == '33ABCDE1234F1Z5'

# 9) delete
ac.post(f'/admin/invoices/{inv_id}/delete', follow_redirects=True)
with app.app_context():
    assert Invoice.query.count() == 0

# 10) create-form and settings pages render (catch Jinja errors)
r = ac.get('/admin/invoices/new')
assert r.status_code == 200 and b'New invoice' in r.data and b'Add item' in r.data
r = ac.get('/admin/invoice-settings')
assert r.status_code == 200 and b'GSTIN' in r.data and b'33NEWGST9999Z5' in r.data

os.unlink(_db)
print('all invoice E2E checks passed')
