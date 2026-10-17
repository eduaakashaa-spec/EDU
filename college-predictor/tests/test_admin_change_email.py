"""Admin → Members: change a member's login email. Run from college-predictor/:  python tests/test_admin_change_email.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.routes import admin_portal as AP
from app.services import mailer

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('secret1').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='admin@ea.com', tier='admin', password_hash=pw()),
                        User(name='Asha Kumar', email='asha@old.com', tier='premium', password_hash=pw()),
                        User(name='Ben', email='ben@ex.com', tier='free', password_hash=pw()),
                        User(name='Cara', email='cara@ex.com', tier='free', password_hash=pw())])
    db.session.commit()
    ids = {u.email: u.id for u in User.query.all()}

sent = []
AP.send_async = lambda to, subject, text, html=None, **k: sent.append({'to': to, 'subject': subject, 'html': html or '', **k})
mailer_orig = AP.mail_configured
AP.mail_configured = lambda: True


def login(e):
    c = app.test_client()
    c.post('/login', data={'email': e, 'password': 'secret1'})
    return c


admin, member, anon = login('admin@ea.com'), login('ben@ex.com'), app.test_client()
url = f"/admin/users/{ids['asha@old.com']}/email"

assert b'Change email' in admin.get('/admin/users').data                              # the option is on the Members page
assert member.post(url, data={'email': 'x@y.com'}).status_code in (302, 403)            # members cannot change emails
assert anon.post(url, data={'email': 'x@y.com'}).status_code in (302, 401, 403)

assert b'valid email' in admin.post(url, data={'email': 'not-an-email'}, follow_redirects=True).data
assert b'already belongs to another member' in admin.post(url, data={'email': 'BEN@ex.com'}, follow_redirects=True).data   # case-insensitive uniqueness
assert b'already this' in admin.post(url, data={'email': 'asha@old.com'}, follow_redirects=True).data
with app.app_context():
    assert db.session.get(User, ids['asha@old.com']).email == 'asha@old.com'

r = admin.post(url, data={'email': '  Asha.New@Example.com ', 'notify': '1'}, follow_redirects=True)
assert b'asha@old.com' in r.data and b'asha.new@example.com' in r.data and b'Both addresses were notified' in r.data
with app.app_context():
    u = db.session.get(User, ids['asha@old.com'])
    assert u.email == 'asha.new@example.com' and u.tier == 'premium' and bcrypt.check_password_hash(u.password_hash, 'secret1')   # password and plan untouched
assert sorted(m['to'] for m in sent) == ['asha.new@example.com', 'asha@old.com'] and all(m['from_addr'] == 'info@eduaakashaa.com' for m in sent)
assert all('asha@old.com' in m['html'] and 'asha.new@example.com' in m['html'] for m in sent)

# the member signs in with the new address, not the old one
assert app.test_client().post('/login', data={'email': 'asha.new@example.com', 'password': 'secret1'}).status_code == 302
bad = app.test_client().post('/login', data={'email': 'asha@old.com', 'password': 'secret1'})
assert b'Invalid email or password' in bad.data

# without the notify box nothing is mailed; with no mail transport the admin is told
sent.clear()
admin.post(f"/admin/users/{ids['cara@ex.com']}/email", data={'email': 'cara2@ex.com'})
assert not sent
AP.mail_configured = lambda: False
assert b'not configured' in admin.post(f"/admin/users/{ids['ben@ex.com']}/email", data={'email': 'ben2@ex.com', 'notify': '1'}, follow_redirects=True).data
assert admin.post('/admin/users/9999/email', data={'email': 'z@z.com'}, follow_redirects=True).data.count(b'not found') >= 1
AP.mail_configured = mailer_orig

try:
    os.unlink(_db)
except OSError:
    pass
print('admin change-email checks passed')
