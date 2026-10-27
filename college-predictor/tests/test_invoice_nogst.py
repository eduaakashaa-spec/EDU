"""Invoices and payment receipts with and without GST.
Run from college-predictor/:  python tests/test_invoice_nogst.py"""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_membership import Invoice, InvoiceReceipt  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='a@x.com', tier='admin', password_hash=pw()), User(name='Stu', email='s@x.com', tier='premium', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, student = login('a@x.com'), login('s@x.com')
anon = app.test_client()


def new_invoice(**over):
    d = {'customer_name': 'Asha Kumar', 'customer_email': 'asha@example.com', 'customer_state': 'Tamil Nadu', 'customer_gstin': '33ABCDE1234F1Z5', 'item_desc': ['Counselling'], 'item_qty': ['1'],
         'item_rate': ['5000'], 'gst_mode': 'with', 'gst_pct': '18', 'payment_status': 'Unpaid'}
    d.update(over)
    r = admin.post('/admin/invoices/new', data=d)
    assert r.status_code == 302, r.data[:300]
    return int(re.search(r'/admin/invoices/(\d+)', r.headers['Location']).group(1))


# ---- access: only admins -----------------------------------------------------------------------------------------------------------------------------
for u in ('/admin/receipts', '/admin/receipts/new', '/admin/invoices/new'):
    assert anon.get(u).status_code in (302, 401, 403) and student.get(u).status_code in (302, 403), u
assert b'Without GST' in admin.get('/admin/invoices/new').data and b'Without GST' in admin.get('/admin/receipts/new').data
assert b'Payment receipts' in admin.get('/admin/invoices').data                                     # menu link

# ---- an invoice WITH GST is unchanged -------------------------------------------------------------------------------------------------------------
gid = new_invoice()
with app.app_context():
    g = db.session.get(Invoice, gid)
    assert g.gst_rate == 0.18 and not g.no_gst and g.total_gst == 90000 and g.total == 590000 and g.cgst == 45000 and g.sgst == 45000 and g.customer_gstin
gh = admin.get('/admin/invoices/%d' % gid).get_data(as_text=True)
assert 'Tax Invoice' in gh and 'Taxable value' in gh and 'CGST' in gh and 'GSTIN: 33ABCDE1234F1Z5' in gh and 'GST is not charged' not in gh

# ---- an invoice WITHOUT GST ----------------------------------------------------------------------------------------------------------------------
nid = new_invoice(gst_mode='none', item_rate=['5000'], discount='500')
with app.app_context():
    n = db.session.get(Invoice, nid)
    assert n.gst_rate == 0 and n.no_gst and n.total_gst == 0 and n.cgst == n.sgst == n.igst == 0 and n.total == 450000 and n.customer_gstin == ''   # 5000 - 500, nothing added
    NTOKEN = n.public_token
nh = admin.get('/admin/invoices/%d' % nid).get_data(as_text=True)
assert 'Tax Invoice' not in nh and 'Taxable value' not in nh and 'CGST' not in nh and 'IGST' not in nh and 'GST is not charged' not in nh and '33ABCDE1234F1Z5' not in nh
assert 'GSTIN' not in anon.get('/invoice/' + NTOKEN).get_data(as_text=True).split('Bill to')[0] and anon.get('/invoice/' + NTOKEN).status_code == 200
from app.routes.invoices import _invoice_email  # noqa: E402
with app.test_request_context():
    with app.app_context():
        subj, text, html = _invoice_email(db.session.get(Invoice, nid))
    assert 'GST (' not in html and 'Subtotal' in html
    with app.app_context():
        assert 'GST (18' in _invoice_email(db.session.get(Invoice, gid))[2]

# ---- bank details: shown on invoices once saved, including invoices issued before they were entered ---------------------------------------------------
assert 'Bank details are not saved yet' in nh and 'A/C:' not in nh
admin.post('/admin/invoice-settings', data={'gst_pct': '18', 'legal_name': 'EduAakashaA', 'bank_ac_name': 'EduAakashaA', 'bank_name': 'Test Bank', 'bank_branch': 'Coimbatore', 'bank_ac_no': '1234567890123', 'bank_ifsc': 'TEST0001234'})
nh2 = admin.get('/admin/invoices/%d' % nid).get_data(as_text=True)
assert 'Bank details for payment' in nh2 and 'A/C: 1234567890123' in nh2 and 'IFSC: TEST0001234' in nh2 and 'Bank details are not saved yet' not in nh2 and 'GST is not charged' not in nh2
assert 'A/C: 1234567890123' in anon.get('/invoice/' + NTOKEN).get_data(as_text=True)                  # the customer's copy too
with app.app_context():
    from app.routes.invoices import _invoice_email as _ie  # noqa: E402
    with app.test_request_context():
        em = _ie(db.session.get(Invoice, nid))[2]
        assert '1234567890123' in em and 'Bank details for payment' in em                                # unpaid invoice e-mail carries the bank details

# ---- receipts: every payment gets its own, numbered in one series ----------------------------------------------------------------------------------
assert b'none yet' in admin.get('/admin/invoices/%d' % nid).data
r = admin.post('/admin/invoices/%d/payment' % nid, data={'payment_status': 'Partially Paid', 'payment_mode': 'UPI', 'payment_ref': 'UTR1', 'amount_received': '1000'}, follow_redirects=True)
assert b'Receipt RCPT/' in r.data
with app.app_context():
    n = db.session.get(Invoice, nid)
    rs = n.receipts.all()
    assert n.amount_paid == 100000 and n.payment_status == 'Partially Paid' and len(rs) == 1
    assert rs[0].amount == 100000 and rs[0].no_gst and rs[0].total_gst == 0 and rs[0].balance_after == 350000 and rs[0].payment_mode == 'UPI' and rs[0].invoice_no == n.invoice_no
r = admin.post('/admin/invoices/%d/payment' % nid, data={'payment_status': 'Paid', 'payment_mode': 'Cash', 'amount_received': '3500'}, follow_redirects=True)   # the balance
with app.app_context():
    n = db.session.get(Invoice, nid)
    rs = n.receipts.all()
    assert n.amount_paid == n.total == 450000 and n.payment_status == 'Paid' and [x.amount for x in rs] == [100000, 350000] and rs[1].balance_after == 0
    nos = [x.receipt_no for x in rs]
    assert nos[0] != nos[1] and nos[0].startswith('RCPT/') and int(nos[1].split('/')[1]) == int(nos[0].split('/')[1]) + 1
    RID, RTOKEN = rs[1].id, rs[1].public_token
admin.post('/admin/invoices/%d/payment' % nid, data={'payment_status': 'Paid'})                    # saving again does not issue a duplicate receipt
with app.app_context():
    assert db.session.get(Invoice, nid).receipts.count() == 2
# marking a GST invoice Paid with no amount entered issues a receipt for the whole total, with the GST split inside it
admin.post('/admin/invoices/%d/payment' % gid, data={'payment_status': 'Paid', 'payment_mode': 'Bank Transfer'})
with app.app_context():
    g = db.session.get(Invoice, gid)
    r1 = g.receipts.one()
    assert g.amount_paid == 590000 and r1.amount == 590000 and not r1.no_gst and r1.taxable_value == 500000 and r1.total_gst == 90000 and r1.cgst == 45000 and r1.sgst == 45000 and r1.igst == 0
rh = admin.get('/admin/receipts/%d' % RID).get_data(as_text=True)
assert 'Payment receipt' in rh and 'GST is not charged on this receipt' in rh and 'CGST' not in rh and 'Against invoice' in rh
gr = admin.get('/admin/receipts').get_data(as_text=True)
assert 'No GST' in gr and '18%' in gr and 'RCPT/' in gr
pub = anon.get('/receipt/' + RTOKEN)
assert pub.status_code == 200 and b'Payment receipt' in pub.data and anon.get('/receipt/nope').status_code == 404
# created already paid
pid = new_invoice(gst_mode='none', payment_status='Paid', payment_mode='UPI', item_rate=['1200'])
with app.app_context():
    p = db.session.get(Invoice, pid)
    assert p.amount_paid == 120000 and p.receipts.count() == 1 and p.receipts.one().no_gst

# ---- a receipt on its own (no invoice) ---------------------------------------------------------------------------------------------------------------
r = admin.post('/admin/receipts/new', data={'customer_name': 'Ravi', 'customer_email': 'ravi@example.com', 'description': 'Counselling fee', 'amount': '2500', 'gst_mode': 'none', 'payment_mode': 'Cash'})
assert r.status_code == 302
with app.app_context():
    sr = InvoiceReceipt.query.filter_by(customer_name='Ravi').one()
    assert sr.invoice_id is None and sr.amount == 250000 and sr.no_gst and sr.total_gst == 0 and sr.description == 'Counselling fee' and sr.balance_after is None
r = admin.post('/admin/receipts/new', data={'customer_name': 'Meena', 'description': 'Course fee', 'amount': '1180', 'gst_mode': 'with', 'gst_pct': '18', 'customer_state': 'Kerala'})
with app.app_context():
    gr_ = InvoiceReceipt.query.filter_by(customer_name='Meena').one()
    assert gr_.amount == 118000 and gr_.taxable_value == 100000 and gr_.total_gst == 18000 and gr_.igst == 18000 and gr_.cgst == 0         # other state: IGST
    GID = gr_.id
assert b'IGST' in admin.get('/admin/receipts/%d' % GID).data
assert b'Enter the payer' in admin.post('/admin/receipts/new', data={'customer_name': '', 'amount': '0'}).data
assert admin.post('/admin/receipts/%d/email' % GID, follow_redirects=True).status_code == 200                                              # no email on file: a message, not an error

# ---- deleting an invoice keeps its receipts ----------------------------------------------------------------------------------------------------------
with app.app_context():
    PNO = db.session.get(Invoice, pid).invoice_no
admin.post('/admin/invoices/%d/delete' % pid)
with app.app_context():
    assert db.session.get(Invoice, pid) is None
    assert InvoiceReceipt.query.filter_by(invoice_no=PNO).count() == 1                                  # the receipt is kept as a record
assert admin.post('/admin/receipts/%d/delete' % GID, follow_redirects=True).status_code == 200

print('invoice and receipt checks passed')
