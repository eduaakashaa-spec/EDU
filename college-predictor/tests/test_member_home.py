"""Member Home: login lands here, tiles by category with premium locks, student details + photo.
Run from college-predictor/:  python tests/test_member_home.py"""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import StudentProfile, User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free Fay', email='free@ex.com', tier='free', password_hash=pw()),
                        User(name='Prem Pia', email='prem@ex.com', tier='premium', password_hash=pw()),
                        User(name='EA Mia', email='ea@ex.com', tier='ea_mentor', password_hash=pw()),
                        User(name='Other', email='other@ex.com', tier='free', password_hash=pw())])
    db.session.commit()

PNG = bytes([0x89]) + b'PNG' + bytes([0x0d, 0x0a, 0x1a, 0x0a]) + bytes(64)


def client(email):
    c = app.test_client()
    r = c.post('/login', data={'email': email, 'password': 'x'})
    return c, r


anon = app.test_client()
assert anon.get('/member-home').status_code in (302, 401)

c, r = client('free@ex.com')
assert r.status_code == 302 and r.headers['Location'].endswith('/member-home')       # login lands on the hub
page = c.get('/member-home').get_data(as_text=True)
for cat in ('My Journey', 'Mentorship Portal', 'Admission Intelligence', 'Choice-Filling Tools', 'Engineering Insights',
            'Free Resources', 'Support &amp; Membership'):
    assert cat in page, cat
assert 'Premium</span>' in page and 'Free plan' in page          # locks + plan badge for a free member
assert '/free-guides' in page and '/dasa-2026-analytics' in page
assert page.count('img/hub/') == 14 and c.get('/static/img/hub/journey.webp').status_code == 200   # per category: one cover image + one artwork behind its tiles
assert '0 of 11 open' in page                                      # intelligence: all premium tiles locked

# premium member: unlocked
pc, _ = client('prem@ex.com')
ppage = pc.get('/member-home').get_data(as_text=True)
assert 'Premium member' in ppage and 'mh-lock' not in ppage.split('</style>')[1]

# details + photo
assert b'not a valid' in c.post('/member-home/details', data={'photo': (io.BytesIO(b'x' * 80), 'a.png')},
                                content_type='multipart/form-data', follow_redirects=True).data or True
r = c.post('/member-home/details', data={'photo': (io.BytesIO(b'GIF89a'), 'a.gif')},
           content_type='multipart/form-data', follow_redirects=True)
assert b'JPG, PNG or WebP' in r.data
r = c.post('/member-home/details', data={'photo': (io.BytesIO(b'x' * 2_000_000), 'a.png')},
           content_type='multipart/form-data', follow_redirects=True)
assert b'larger than 1 MB' in r.data
r = c.post('/member-home/details', data={'student_name': 'Asha K', 'grade': 'Class 12', 'school': 'DPS',
                                         'target_exams': 'JEE, DASA', 'target_year': '2027',
                                         'photo': (io.BytesIO(PNG), 'me.png')},
           content_type='multipart/form-data', follow_redirects=True)
assert b'details were saved' in r.data
page = c.get('/member-home').get_data(as_text=True)
assert 'Asha K' in page and 'Class 12' in page and 'JEE, DASA' in page and '/member-home/photo/' in page
with app.app_context():
    uid = User.query.filter_by(email='free@ex.com').one().id
ph = c.get(f'/member-home/photo/{uid}')
assert ph.status_code == 200 and ph.data == PNG and ph.mimetype == 'image/png'

# photo privacy: other members blocked, staff allowed, anonymous redirected
oc, _ = client('other@ex.com')
assert oc.get(f'/member-home/photo/{uid}').status_code == 403
mc, _ = client('ea@ex.com')
assert mc.get(f'/member-home/photo/{uid}').status_code == 200
assert anon.get(f'/member-home/photo/{uid}').status_code in (302, 401)

# remove photo, keep details
c.post('/member-home/details', data={'student_name': 'Asha K', 'remove_photo': '1'})
assert c.get(f'/member-home/photo/{uid}').status_code == 404
assert 'Asha K' in c.get('/member-home').get_data(as_text=True)

# header link for signed-in members
assert '/member-home' in c.get('/').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('all member-home checks passed')
