"""Self-check for the DASA counsellor-dashboard proxy + login redirect safety.

Covers the hole this replaced: the Apps Script URL + access key used to sit in
static/js/counsellor_dashboard.js, which Flask serves to anyone — so the admin
gate on the page was cosmetic and every student's PII was one anonymous GET
away. Hermetic: fresh SQLite, Apps Script stubbed (touches nothing external).
Run:  ../.venv/bin/python tests/test_counsellor_proxy.py   (from college-predictor/)
"""
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
os.environ['DASA_SCRIPT_URL'] = 'https://script.example/exec'
os.environ['DASA_SCRIPT_KEY'] = 'super-secret-key'

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.decorators import safe_next
from app import routes as R

# --- stub the Apps Script: record what we send, never leave the process ------
calls = []
ROWS = [{'_row': 2, 'Name': 'Aarav', 'Email': 'a@ex.com', 'Status': 'New'}]


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def fake_urlopen(req, timeout=None):
    url = req if isinstance(req, str) else req.full_url
    body = None if isinstance(req, str) else (req.data or b'').decode()
    calls.append({'url': url, 'body': body})
    if body:  # doPost — status write-back
        return FakeResp(b'OK')
    return FakeResp(json.dumps({'rows': ROWS}).encode())


R.urlopen = fake_urlopen

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    db.create_all()
    mk = lambda n, e, t: User(name=n, email=e, tier=t,
                              password_hash=bcrypt.generate_password_hash('x').decode())
    db.session.add_all([mk('Admin', 'admin@ea.com', 'admin'),
                        mk('Priya', 'priya@ex.com', 'premium')])
    db.session.commit()


def login(c, email):
    c.post('/login', data={'email': email, 'password': 'x'}, follow_redirects=True)


ac = app.test_client(); login(ac, 'admin@ea.com')   # admin
pc = app.test_client(); login(pc, 'priya@ex.com')   # logged in, NOT admin
anon = app.test_client()                            # not logged in

# 1) the regression itself: the public JS must carry no URL and no key.
js = anon.get('/static/js/counsellor_dashboard.js')
assert js.status_code == 200, js.status_code
body = js.get_data(as_text=True)
assert 'script.google.com' not in body, 'Apps Script URL leaked into public JS'
assert 'super-secret-key' not in body and '111023' not in body, 'key leaked into public JS'

# 2) anonymous cannot read submissions — must bounce to login, never serve PII.
r = anon.get('/counsellor-dashboard/data')
assert r.status_code == 302 and '/login' in r.headers['Location'], r.status_code
assert b'Aarav' not in r.data

# 3) logged-in non-admin is forbidden.
assert pc.get('/counsellor-dashboard/data').status_code == 403

# 4) admin gets the rows, and the key travels server-side only.
calls.clear()
r = ac.get('/counsellor-dashboard/data')
assert r.status_code == 200, r.status_code
assert r.get_json()['rows'] == ROWS
assert 'super-secret-key' in calls[0]['url'], 'server must authenticate to Apps Script'
assert 'super-secret-key' not in r.get_data(as_text=True), 'key must not reach the browser'

# 5) status write-back: admin only, and validated before it hits the Sheet.
calls.clear()
r = ac.post('/counsellor-dashboard/status', json={'row': 2, 'status': 'Contacted'})
assert r.status_code == 200, r.status_code
sent = json.loads(calls[0]['body'])
assert sent == {'action': 'updateStatus', 'key': 'super-secret-key',
                'row': 2, 'status': 'Contacted'}, sent

assert anon.post('/counsellor-dashboard/status',
                 json={'row': 2, 'status': 'Contacted'}).status_code == 302
assert pc.post('/counsellor-dashboard/status',
               json={'row': 2, 'status': 'Contacted'}).status_code == 403

calls.clear()
for bad in ({'row': 2, 'status': 'Deleted'},      # not a status we render
            {'row': 1, 'status': 'New'},          # header row
            {'row': '2', 'status': 'New'},        # not an int
            {'row': True, 'status': 'New'},       # bool is an int subclass
            {}):
    assert ac.post('/counsellor-dashboard/status', json=bad).status_code == 400, bad
assert not calls, 'rejected writes must never reach the Sheet'

# 6) unconfigured deploy degrades to 503, not a 500 or a silent leak.
_url = app.config['DASA_SCRIPT_URL']
app.config['DASA_SCRIPT_URL'] = ''
assert ac.get('/counsellor-dashboard/data').status_code == 503
app.config['DASA_SCRIPT_URL'] = _url

# 7) login ?next= must not bounce users off-site (open redirect / phishing).
for evil in ('https://evil.example/phish', '//evil.example', '/\\evil.example',
             'javascript:alert(1)', 'http:/evil.example'):
    assert safe_next(evil) is None, evil
for ok in ('/profile', '/admin/users?tab=1'):
    assert safe_next(ok) == ok, ok

# login reads ?next= from the query string (that is what the decorators set).
ec = app.test_client()
r = ec.post('/login?next=https://evil.example/phish',
            data={'email': 'admin@ea.com', 'password': 'x'})
assert r.status_code == 302, r.status_code
assert 'evil.example' not in r.headers['Location'], r.headers['Location']

# ...and a legitimate ?next= still works (the decorators depend on it).
gc = app.test_client()
r = gc.post('/login?next=/counsellor-dashboard',
            data={'email': 'admin@ea.com', 'password': 'x'})
assert r.headers['Location'].endswith('/counsellor-dashboard'), r.headers['Location']

print('counsellor proxy + redirect self-check: all passed')
