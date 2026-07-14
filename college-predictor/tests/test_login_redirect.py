"""Self-check for login ?next= redirect safety (app.decorators.safe_next).

Login used to pass ?next= straight to redirect(), so a link like
/login?next=https://evil/phish bounced a user who had just authenticated on our
real domain out to an attacker's look-alike. Hermetic: fresh SQLite, no network.
Run:  ../.venv/bin/python tests/test_login_redirect.py   (from college-predictor/)
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.decorators import safe_next

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='admin@ea.com', tier='admin',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

# 1) off-site targets are refused, however they are spelled.
for evil in ('https://evil.example/phish',
             '//evil.example',                 # scheme-relative
             '/\\evil.example',                # Chrome/Safari read '\' as '/'
             'javascript:alert(1)',
             'http:/evil.example',
             '  https://evil.example'):        # leading whitespace
    assert safe_next(evil) is None, evil

# 2) same-app paths still pass through (the decorators depend on this).
for ok in ('/profile', '/admin/users?tab=1', '/dashboard#section'):
    assert safe_next(ok) == ok, ok

assert safe_next(None) is None and safe_next('') is None

# 3) end-to-end: the login route honours a safe ?next= and drops a hostile one.
c = app.test_client()
r = c.post('/login?next=https://evil.example/phish',
           data={'email': 'admin@ea.com', 'password': 'x'})
assert r.status_code == 302, r.status_code
assert 'evil.example' not in r.headers['Location'], r.headers['Location']

c2 = app.test_client()
r = c2.post('/login?next=/profile', data={'email': 'admin@ea.com', 'password': 'x'})
assert r.headers['Location'].endswith('/profile'), r.headers['Location']

print('login redirect self-check: all passed')
