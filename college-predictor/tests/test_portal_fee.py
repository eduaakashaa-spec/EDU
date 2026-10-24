"""Premium Portal Access path: list price, admin repricing, access grant on payment.

Hermetic (sqlite). Run from college-predictor/:  python tests/test_portal_fee.py
"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
for k in ('RESEND_API_KEY', 'SMTP_HOST'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.models_membership import MembershipApplication, PORTAL_TIER, TIER_PRICES, TIERS

assert PORTAL_TIER in TIERS and TIER_PRICES[PORTAL_TIER] == 15_000_00

app = create_app(); app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='admin@ea.com', tier='admin',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.add(User(name='Asha', email='asha@ex.com', tier='free',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

pub = app.test_client()
# the public page lists the path and its price
page = pub.get('/members-registration').get_data(as_text=True)
assert 'Premium Portal Access' in page and '15,000' in page

# 1) applying pre-fills the list price (GST inclusive) -> total ₹15,000
r = pub.post('/membership/apply', json={'name': 'Asha', 'email': 'asha@ex.com',
                                        'tier': 'Premium Portal Access', 'state': 'Kerala'})
assert r.status_code == 200 and r.get_json()['ok']
with app.app_context():
    a = MembershipApplication.query.filter_by(email='asha@ex.com').one()
    app_id = a.id
    assert a.tier_price == 15_000_00 and a.final_total == 15_000_00, (a.tier_price, a.final_total)
    assert a.taxable_value + a.total_gst == a.final_total and a.igst == a.total_gst  # inter-state

ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})

# 2) admin issues the invoice and records a PART payment -> no access yet
assert ac.post(f'/admin/membership/{app_id}/invoice').status_code in (302, 303)
ac.post(f'/admin/membership/{app_id}/payment', data={'amount': '4000', 'payment_mode': 'UPI', 'payment_ref': 'a1'})
with app.app_context():
    assert db.session.query(User).filter_by(email='asha@ex.com').one().tier == 'free'

# 3) the balance clears the invoice -> portal access switches on for 12 months
ac.post(f'/admin/membership/{app_id}/payment', data={'amount': '11000', 'payment_mode': 'UPI', 'payment_ref': 'a2'})
with app.app_context():
    u = User.query.filter_by(email='asha@ex.com').one()
    assert u.tier == 'premium' and u.is_premium, u.tier
    days = (u.tier_expires_at - __import__('datetime').datetime.utcnow()).days
    assert 363 <= days <= 366, days

# 4) re-pricing: switching the path moves the price; a custom amount is kept
r = pub.post('/membership/apply', json={'name': 'Ravi', 'email': 'ravi@ex.com', 'tier': 'Aspirant Path'})
with app.app_context():
    rid = MembershipApplication.query.filter_by(email='ravi@ex.com').one().id
    assert MembershipApplication.query.get(rid).tier_price == 30_000_00
ac.post(f'/admin/membership/{rid}/update', data={'name': 'Ravi', 'tier': 'Premium Portal Access',
                                                 'tier_price': '30000', 'status': 'New'})
with app.app_context():
    assert MembershipApplication.query.get(rid).tier_price == 15_000_00
ac.post(f'/admin/membership/{rid}/update', data={'name': 'Ravi', 'tier': 'Elite Mentorship',
                                                 'tier_price': '8000', 'status': 'New'})   # custom -> kept
with app.app_context():
    assert MembershipApplication.query.get(rid).tier_price == 8000_00

# 5) manual grant works; an unknown email is reported, not crashed
assert ac.post(f'/admin/membership/{rid}/grant-access').status_code in (302, 303)   # no account for ravi
# 6) the member can now open the simulator; a free user cannot
mc = app.test_client(); mc.post('/login', data={'email': 'asha@ex.com', 'password': 'x'})
assert mc.get('/choice-builder-pro').status_code == 200
with app.app_context():
    db.session.add(User(name='F', email='f@ex.com', tier='free',
                        password_hash=bcrypt.generate_password_hash('x').decode())); db.session.commit()
fc = app.test_client(); fc.post('/login', data={'email': 'f@ex.com', 'password': 'x'})
assert fc.get('/choice-builder-pro').status_code == 403

try:
    os.unlink(_db)
except OSError:
    pass
print('all portal-fee checks passed')
