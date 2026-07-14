"""Self-check for announcement emailing (Broadcast → Announcements).

Hermetic: sqlite, bulk sender stubbed. Run from college-predictor/:
    ../.venv/bin/python tests/test_announcement_email.py
"""
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

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
from app.models import Announcement, User
from app.routes import admin_portal as AP

blasts = []
AP.send_bulk = lambda recips, subject, text, html=None, **k: (
    blasts.append({'to': list(recips), 'subject': subject, 'text': text, 'html': html}),
    len(recips))[1]
AP.mail_configured = lambda: True

app = create_app()
app.config['TESTING'] = True
now = datetime.now(timezone.utc).replace(tzinfo=None)
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    db.session.add_all([
        User(name='Admin', email='admin@ea.com', tier='admin', password_hash=pw),
        User(name='Free', email='free@ex.com', tier='free', password_hash=pw),
        User(name='Prem', email='prem@ex.com', tier='premium', password_hash=pw),
        User(name='PremForever', email='prem2@ex.com', tier='premium', password_hash=pw,
             tier_expires_at=None),
        User(name='PremExpired', email='expired@ex.com', tier='premium', password_hash=pw,
             tier_expires_at=now - timedelta(days=1)),
        User(name='Guide', email='guide@ex.com', tier='mentor', password_hash=pw),
    ])
    db.session.commit()

ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})


def post(**over):
    data = {'title': 'T', 'body': 'B', 'audience': 'all', 'pinned': '0', 'email_scope': 'none'}
    data.update(over)
    return ac.post('/admin/announcements', data=data, follow_redirects=True)


# 1) default: publishes, emails nobody
blasts.clear()
r = post(title='Dashboard only', body='no mail')
assert r.status_code == 200 and blasts == [], blasts
with app.app_context():
    assert Announcement.query.filter_by(title='Dashboard only').count() == 1

# 2) premium scope: only currently-valid premium; no free, no guide, no expired
blasts.clear()
post(title='Prem blast', body='hello premium', email_scope='premium')
assert len(blasts) == 1, blasts
to = set(blasts[0]['to'])
assert to == {'prem@ex.com', 'prem2@ex.com'}, to
assert 'expired@ex.com' not in to, 'expired premium must not be emailed'
assert 'guide@ex.com' not in to and 'free@ex.com' not in to

# 3) all scope: every member except College Guides
blasts.clear()
post(title='All blast', body='hello all', email_scope='all')
to = set(blasts[0]['to'])
assert 'guide@ex.com' not in to, 'guides have their own portal — exclude'
assert {'free@ex.com', 'prem@ex.com', 'expired@ex.com', 'admin@ea.com'} <= to, to

# 4) the email carries the announcement, branded + escaped
blasts.clear()
post(title='Round-1 <out>', body='Line one\nLine two', email_scope='premium')
b = blasts[0]
assert b['subject'] == 'Round-1 <out>'
assert b['text'] == 'Line one\nLine two'                 # plain text stays raw
assert '&lt;out&gt;' in b['html'] and '<out>' not in b['html'], 'html must be escaped'
assert 'Team EduAakashaa' in b['html'], 'branded shell applied'
assert 'Dubai' not in b['html'] and '971' not in b['html'], 'no UAE traces'

# 5) a bad scope value can't trigger a blast
blasts.clear()
post(title='X', body='Y', email_scope='everyone-lol')
assert blasts == [], 'unknown scope must not send'

# 6) invalid announcement neither publishes nor emails
blasts.clear()
post(title='', body='', email_scope='all')
assert blasts == []
with app.app_context():
    assert Announcement.query.filter_by(title='').count() == 0

# 7) page renders templates + counts; non-admin blocked
r = ac.get('/admin/announcements')
assert r.status_code == 200 and b'Start from a template' in r.data
assert b'Also email it?' in r.data and b'Premium members (2)' in r.data, 'live count wrong'
fc = app.test_client(); fc.post('/login', data={'email': 'free@ex.com', 'password': 'x'})
assert fc.get('/admin/announcements').status_code in (302, 401, 403)

os.unlink(_db)
print('all announcement-email checks passed')
