"""Self-check for the automated template emails:
  - survey submitted  -> 'Thank you — Survey' to the respondent + admin notified
  - payout marked paid -> 'Payout credited — Guide' to the guide
  - guide registered   -> admin notified

Hermetic: sqlite, email + R2 stubbed. Run from college-predictor/:
    ../.venv/bin/python tests/test_auto_emails.py
"""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
os.environ['FLASK_DEBUG'] = '0'
for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS', 'RESEND_API_KEY'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import AlumniProfile, MentorMeeting, User
from app.routes import alumni as AL
from app.routes import survey as SV
from app.services.email_templates import render_email

# --- unit: the registry renders server-side, filled + branded ---------------
subject, text, html = render_email('payment', {'name': 'Priya', 'amount': 1000})
assert subject == '₹1000 credited to you, Priya 💸', subject
assert 'payout of ₹1000 has been credited' in text
assert '<strong>₹1000</strong>' in html and 'Team EduAakashaa' in html
assert 'EduAakashaa' in html and 'font-family:Arial' in html          # branded shell applied

subject, text, html = render_email('ty_survey', {'name': 'Ravi', 'college': 'NIT Trichy'})
assert 'Ravi' in subject and 'NIT Trichy' in text and 'NIT Trichy' in html

# placeholder escaping: a hostile college name can't inject markup
_, _, html = render_email('ty_survey', {'name': 'X', 'college': '<script>bad()</script>'})
assert '<script>' not in html and '&lt;script&gt;' in html, 'html placeholders must be escaped'

try:
    render_email('nope-not-a-template', {})
    raise AssertionError('unknown key should raise')
except KeyError:
    pass

# --- app wiring -------------------------------------------------------------
sent, notes = [], []
AL.send_async = lambda *a, **k: sent.append(a)
AL.notify_admin = lambda *a, **k: notes.append(a)
SV.send_async = lambda *a, **k: sent.append(a)
SV.notify_admin = lambda *a, **k: notes.append(a)


class FakeR2:
    def is_configured(self): return True
    def upload(self, data, key, mime): return key
    def presigned_get(self, key, **k): return 'https://r2.example/' + key


AL.r2 = FakeR2()

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='admin@ea.com', tier='admin',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})

# 1) a College Guide registers -> admin notified
sent.clear(); notes.clear()
pc = app.test_client()
r = pc.post('/alumni-network', data={
    'name': 'Priya Sharma', 'email': 'priya@ex.com', 'university': 'NIT Trichy',
    'password': 'secret123', 'consent': '1', 'program': 'CSE', 'stage': 'alumni',
    'photo': (io.BytesIO(b'\xff\xd8\xff' + b'x' * 50), 'p.jpg'),
    'resume': (io.BytesIO(b'%PDF-1.7\n%%EOF'), 'cv.pdf'),
}, content_type='multipart/form-data')
assert r.status_code == 200 and r.get_json().get('ok') is True, r.get_json()
assert len(notes) == 1 and 'New College Guide' in notes[0][0], notes
assert 'priya@ex.com' in notes[0][1] and 'NIT Trichy' in notes[0][1]

# 2) admin marks a payout paid -> guide gets the 'Payout credited' template
with app.app_context():
    prof = AlumniProfile.query.filter_by(email='priya@ex.com').first()
    m = MentorMeeting(alumni_id=prof.id, kind='meeting', status='Completed',
                      payout_amount=1000, paid=False)
    db.session.add(m); db.session.commit()
    mid = m.id
# build from the url_map so a route rename can't silently skip this test
paid_url = f'/admin/meeting/{mid}/paid'
assert any(r.endpoint == 'alumni.admin_meeting_paid' and r.rule == '/admin/meeting/<int:meeting_id>/paid'
           for r in app.url_map.iter_rules()), 'mark-paid route moved — update paid_url'

sent.clear()
ac.post(paid_url, follow_redirects=True)
assert len(sent) == 1, sent
to, subj, body, html = sent[0]
assert to == 'priya@ex.com' and '1000' in subj and 'Priya' in subj
assert '₹1000' in html

# un-marking must NOT email again (it's a correction, not a credit)
sent.clear()
ac.post(paid_url, follow_redirects=True)
assert sent == [], 'un-marking a payout must not send an email'

# 3) someone fills the survey -> thank-you to them + admin notified
sent.clear(); notes.clear()
with app.app_context():
    required = [q['key'] for q in SV.REQUIRED_QUESTIONS]
form = {k: 'x' for k in required}
form.update({'name': 'Ravi Kumar', 'email': 'ravi@ex.com', 'institute': 'NIT Trichy',
             'overall_rating': 'Good', 'recommend_score': '9'})
r = pc.post('/college-survey', data=form, follow_redirects=False)
assert r.status_code in (302, 303), r.status_code

assert len(sent) == 1, sent
to, subj, body, html = sent[0]
assert to == 'ravi@ex.com' and 'Ravi' in subj
assert 'NIT Trichy' in body                       # college filled into the template

assert len(notes) == 1 and 'New college survey' in notes[0][0], notes
assert 'ravi@ex.com' in notes[0][1] and 'NIT Trichy' in notes[0][1]

os.unlink(_db)
print('all auto-email checks passed')
