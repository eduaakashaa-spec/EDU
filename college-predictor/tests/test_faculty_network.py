"""Self-check for the Faculty Network front door + shared guide registration.

Faculty reuse the College Guide backend: /faculty-network is a GET-only branded
page whose form POSTs to /alumni-network with stage='faculty'. This proves the
refactor into _register_guide() still registers, and that a faculty signup
creates a tier='mentor' user + AlumniProfile(stage='faculty').

Hermetic: fresh SQLite, R2 + email stubbed. Touches nothing external.
Run:  ../.venv/bin/python tests/test_faculty_network.py   (from college-predictor/)
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
for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db
from app.models import AlumniProfile, User
from app.routes import alumni as A

# stub the two external side-effects the handler triggers
A.r2.is_configured = lambda: True
A.r2.upload = lambda data, key, mime: key
A.notify_admin = lambda *a, **k: None
A.send_async = lambda *a, **k: None

app = create_app()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()

c = app.test_client()

# 1) faculty landing renders and points its form at the shared endpoint
r = c.get('/faculty-network')
assert r.status_code == 200, r.status_code
body = r.get_data(as_text=True)
assert 'Faculty Network' in body
assert 'name="stage" value="faculty"' in body
assert '/alumni-network' in body      # form posts into the shared pipeline

# 2) a faculty signup flows through _register_guide -> mentor user + profile
resume = (io.BytesIO(b'%PDF-1.4 fake'), 'cv.pdf')
photo = (io.BytesIO(b'\xff\xd8\xff\xe0 fake jpg'), 'me.jpg')
r = c.post('/alumni-network', data={
    'name': 'Dr. R. Meenakshi', 'email': 'prof@college.edu',
    'password': 'secret6', 'university': 'PSG College of Technology',
    'current_role': 'Associate Professor', 'stage': 'faculty', 'consent': '1',
    'resume': resume, 'photo': photo,
}, headers={'Accept': 'application/json'}, content_type='multipart/form-data')
assert r.status_code == 200, (r.status_code, r.get_data(as_text=True))
assert r.get_json().get('ok') is True, r.get_json()

with app.app_context():
    prof = AlumniProfile.query.filter_by(email='prof@college.edu').first()
    assert prof is not None and prof.stage == 'faculty', prof
    assert prof.user_id and User.query.get(prof.user_id).tier == 'mentor'

# 3) the ordinary College Guide path still works after the refactor
r = c.post('/alumni-network', data={
    'name': 'Arun V', 'email': 'arun@ex.com', 'password': 'secret6',
    'university': 'NIT Trichy', 'stage': 'alumni', 'consent': '1',
    'resume': (io.BytesIO(b'%PDF-1.4 x'), 'r.pdf'),
    'photo': (io.BytesIO(b'\xff\xd8\xff\xe0 y'), 'p.jpg'),
}, headers={'Accept': 'application/json'}, content_type='multipart/form-data')
assert r.get_json().get('ok') is True, r.get_json()

os.unlink(_db)
print('OK  faculty network + shared guide registration')
