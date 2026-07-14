"""Every automated customer-facing email must render through the one branded
shell (logo header, accent bar, signature, footer) — not ad-hoc HTML.

Hermetic: sqlite, sending stubbed. Run from college-predictor/:
    ../.venv/bin/python tests/test_email_branding.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
os.environ['FLASK_DEBUG'] = '0'
for k in ('RESEND_API_KEY', 'SMTP_HOST', 'SMTP_USER', 'SMTP_PASS'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import DocVerification, User
from app.routes import admin_portal as AP
from app.routes import members as M
from app.routes import invoices as INV
from app.services.email_templates import LOGO_URL

app = create_app()
app.config['TESTING'] = True

sent = []
AP.send_async = lambda *a, **k: sent.append(a)
M.send_async = lambda *a, **k: sent.append(a)
INV.send_async = lambda *a, **k: sent.append(a)


def branded(html, who):
    """The markers that prove the shared shell wrapped this body."""
    assert html, f'{who}: no html part at all'
    assert LOGO_URL in html, f'{who}: no logo'
    assert 'Team EduAakashaa' in html, f'{who}: no signature'
    assert 'Evidence-based college guidance' in html, f'{who}: no footer'
    assert '#0E3A8A' in html, f'{who}: no navy header'
    assert 'Dubai' not in html and '971' not in html, f'{who}: UAE trace'
    # the shell owns the sign-off — bodies must not repeat it
    assert html.count('Team EduAakashaa') == 1, f'{who}: duplicated sign-off'


with app.test_request_context():
    db.create_all()
    u = User(name='Priya Sharma', email='priya@ex.com', tier='premium',
             password_hash=bcrypt.generate_password_hash('x').decode())
    db.session.add(u)
    db.session.commit()

    # 1) member welcome (login details)
    sent.clear()
    AP._email_new_member(u, 'S3cretPass')
    to, subj, text, html = sent[0]
    branded(html, 'welcome')
    assert 'S3cretPass' in html and 'Log in' in html

    # 2) documents requested
    sent.clear()
    M._email_docs_requested(u, ['Passport', '10th (SSLC) Marksheet'])
    branded(sent[0][3], 'docs requested')
    assert 'Passport' in sent[0][3]

    # 3) document reviewed — both outcomes
    for status, comment, word in [('Approved', None, 'Approved'),
                                  ('Rejected', 'Blurry scan', 'Needs re-upload')]:
        d = DocVerification(user_id=u.id, doc_type='Passport', status=status,
                            admin_comment=comment)
        db.session.add(d); db.session.commit()
        sent.clear()
        M._email_doc_reviewed(u, d)
        branded(sent[0][3], f'doc {status}')
        assert word in sent[0][3]
        if comment:
            assert 'Blurry scan' in sent[0][3]

    # 4) all verified
    sent.clear()
    M._email_all_verified(u)
    branded(sent[0][3], 'all verified')

    # 5) invoice email
    from app.models_membership import Invoice
    import json, secrets
    from app.services.company import company_profile
    inv = Invoice(invoice_no='EA/0002', customer_name='Priya Sharma',
                  customer_email='priya@ex.com',
                  items_json=json.dumps([{'desc': 'premium membership', 'qty': 1, 'rate': 7000000}]),
                  discount=1120000, gst_rate=0.18, subtotal=7000000, taxable_value=5880000,
                  igst=1058400, total_gst=1058400, total=6938400, payment_status='Unpaid',
                  seller_json=json.dumps(company_profile()), public_token=secrets.token_urlsafe(24))
    db.session.add(inv); db.session.commit()
    subject, text, html = INV._invoice_email(inv)
    branded(html, 'invoice')
    assert 'EA/0002' in html
    assert 'premium membership' in html
    assert '69,384.00' in html and '58,800.00' in html          # totals survive
    assert 'View / download invoice' in html

    # hostile item description cannot inject markup into the email
    inv.items_json = json.dumps([{'desc': '<script>x()</script>', 'qty': 1, 'rate': 100}])
    db.session.commit()
    _, _, html = INV._invoice_email(inv)
    assert '<script>' not in html and '&lt;script&gt;' in html, 'invoice items must be escaped'

os.unlink(_db)
print('all email-branding checks passed')
