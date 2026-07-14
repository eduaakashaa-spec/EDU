"""Self-check for "Send now" on the Email Templates page.

Hermetic: sqlite + stubbed transport (no network, no real email).
Run from college-predictor/:  ../.venv/bin/python tests/test_templates_send.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
os.environ['FLASK_DEBUG'] = '0'
for k in ('RESEND_API_KEY', 'SMTP_HOST', 'SMTP_USER', 'SMTP_PASS', 'MAIL_TRANSPORT'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.routes import admin_portal as AP

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    for name, email, tier in [('Admin', 'admin@ea.com', 'admin'), ('Free', 'free@ex.com', 'free')]:
        db.session.add(User(name=name, email=email, tier=tier,
                            password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})


def send(payload):
    r = ac.post('/admin/templates/send', data=json.dumps(payload),
                content_type='application/json')
    return r.status_code, r.get_json()


# 1) no transport configured -> 503 with a helpful message, nothing sent
code, body = send({'to': 'a@b.com', 'subject': 'S', 'text': 'T'})
assert code == 503 and 'RESEND_API_KEY' in body['error'], (code, body)

# --- stub the transport from here on --------------------------------------
sent = []
AP.mailer.send_now = lambda to, subject, text, html=None, **k: sent.append(
    {'to': to, 'subject': subject, 'text': text, 'html': html})
AP.mailer.is_configured = lambda: True
AP.mailer.transport = lambda: 'resend'

# 2) validation: bad address / no subject / no body are rejected before sending
for bad, why in [
    ({'to': 'not-an-email', 'subject': 'S', 'text': 'T'}, 'invalid address'),
    ({'to': 'a@b.com', 'subject': '', 'text': 'T'}, 'no subject'),
    ({'to': 'a@b.com', 'subject': 'S', 'text': '', 'html': ''}, 'no body'),
]:
    code, body = send(bad)
    assert code == 400 and body['ok'] is False, (why, code, body)
assert sent == [], 'nothing may be sent when validation fails'

# 3) happy path -> sends exactly what was composed
code, body = send({'to': 'priya@ex.com', 'subject': 'Welcome 🎓',
                   'text': 'plain body', 'html': '<p>branded body</p>'})
assert code == 200 and body['ok'] is True and body['to'] == 'priya@ex.com', (code, body)
assert body['via'] == 'resend'
assert len(sent) == 1 and sent[0]['to'] == 'priya@ex.com'
assert sent[0]['subject'] == 'Welcome 🎓'
assert sent[0]['text'] == 'plain body' and sent[0]['html'] == '<p>branded body</p>'

# 4) a transport failure surfaces the real error, as 502
def boom(*a, **k):
    raise RuntimeError('Resend API 403: domain is not verified')


AP.mailer.send_now = boom
code, body = send({'to': 'a@b.com', 'subject': 'S', 'text': 'T'})
assert code == 502 and 'not verified' in body['error'], (code, body)

# 5) non-admins cannot send
fc = app.test_client(); fc.post('/login', data={'email': 'free@ex.com', 'password': 'x'})
r = fc.post('/admin/templates/send', data=json.dumps({'to': 'a@b.com', 'subject': 'S', 'text': 'T'}),
            content_type='application/json')
assert r.status_code in (302, 401, 403), r.status_code
anon = app.test_client()
r = anon.post('/admin/templates/send', data=json.dumps({'to': 'a@b.com', 'subject': 'S', 'text': 'T'}),
              content_type='application/json')
assert r.status_code in (302, 401, 403), r.status_code

# 6) the page renders the Send button
r = ac.get('/admin/templates')
assert r.status_code == 200 and b'Send now' in r.data

os.unlink(_db)
print('all templates-send checks passed')
