"""Engineering in Gulf category + CAET (IIT Delhi - Abu Dhabi) guide: members-only, sandboxed, linked from Member Home.
Run from college-predictor/:  python tests/test_gulf_guide.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Prem', email='p@x.com', tier='premium', password_hash=pw()), User(name='Free', email='f@x.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'x'})
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
PAGE, FILE = '/engineering-in-gulf/caet-iit-delhi-abu-dhabi', '/engineering-in-gulf/caet-iit-delhi-abu-dhabi/guide'
for url in (PAGE, FILE):
    assert anon.get(url).status_code in (302, 401) and free.get(url).status_code == 403, url      # members only, including the raw file

r = prem.get(PAGE)
t = r.get_data(as_text=True)
assert r.status_code == 200 and 'CAET · IIT Delhi – Abu Dhabi' in t and f'src="{FILE}"' in t and 'Open full screen' in t and '/mentorship/addons#iitd-ad' in t

f = prem.get(FILE)
assert f.status_code == 200 and f.mimetype == 'text/html' and len(f.data) > 3_000_000 and b'CAET' in f.data
csp = f.headers['Content-Security-Policy']
assert csp.startswith('sandbox ') and 'allow-scripts' in csp and 'allow-same-origin' not in csp        # runs in an opaque origin
assert f.headers['X-Content-Type-Options'] == 'nosniff' and 'private' in f.headers['Cache-Control']

hub = prem.get('/member-home').get_data(as_text=True)
assert 'Engineering in Gulf' in hub and 'CAET · IIT Delhi – Abu Dhabi guide' in hub and PAGE in hub and 'img/hub/gulf.svg' in hub
assert prem.get('/static/img/hub/gulf.svg').status_code == 200
fhub = free.get('/member-home').get_data(as_text=True)
assert 'Engineering in Gulf' in fhub and 'Premium' in fhub                                              # visible to everyone, locked for free members

try:
    os.unlink(_db)
except OSError:
    pass
print('gulf guide checks passed')
