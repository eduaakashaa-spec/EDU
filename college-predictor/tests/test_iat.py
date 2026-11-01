"""IISER Aptitude Test (IAT) page (public). Run from college-predictor/:  python tests/test_iat.py"""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import iat as d  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

assert len(d.IISERS) == 7 and sum(s[3] for s in d.IISERS) == 2013 and len(d.OTHERS) == 5 and len(d.SYLLABUS) == 4
# seats on the official page: BS-MS 300+300+280+30+275+288+320+250 = 2043, plus 40+75+80+55+50 = 300, total 2343
assert sum(s[3] for s in d.IISERS) + 30 + 300 == d.SEATS_TOTAL
assert all(t in d.TAGS for _q, t, _a in d.FAQ) and d.PATTERN[1][1].startswith('60 multiple-choice')
assert 'whatsapp' not in repr(vars(d)).lower()

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add(User(name='Prem', email='p@x.com', tier='premium', password_hash=pw()))
    db.session.commit()
anon, prem = app.test_client(), app.test_client()
assert prem.post('/login', data={'email': 'p@x.com', 'password': 'x'}).status_code == 302
URL = '/iiser-aptitude-test'
pages = {}
for who, c in (('public', anon), ('premium', prem)):
    r = c.get(URL)
    assert r.status_code == 200, who
    h = r.get_data(as_text=True)
    pages[who] = h
    assert '7 June 2026' in h and '240' in h and 'IISER Berhampur' in h and 'IACS' in h and 'IIEST' in h and '2,343' in h, who
    assert 'dg-alert' in h and 'premiumNotice' not in h and 'EduAakashaA Members Group' in h and 'iiseradmission.in' in h, who
    assert h.count('class="ia-pane"') == 4 and 'IAT mentorship programme' in h and '/mentorship/addons#iiser' in h or 'Sign in to request' in h, who
    low = re.sub(r'<[^>]+>', ' ', h).lower()
    assert 'whatsapp group' not in low and 'group chat' not in low, who
assert 'Join Premium Membership' in pages['public'] and 'Your Premium access is active' in pages['premium']
for a in ('/iat', '/iiser', '/iiser-admission'):
    assert anon.get(a).status_code == 301 and anon.get(a).headers['Location'].endswith(URL), a
assert URL in anon.get('/sitemap.xml').get_data(as_text=True) and URL in anon.get('/').get_data(as_text=True)
assert 'IISER Aptitude Test (IAT) guide' in prem.get('/member-home').get_data(as_text=True)
print('iat page checks passed')
