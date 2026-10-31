"""JEE Main 2027 registration page (public + members).
Run from college-predictor/:  python tests/test_jee_registration.py"""
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
from app.data import jee_registration as d  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

# content integrity
assert sum(len(g['qs']) for g in d.FAQ) == 36 and [q[0] for g in d.FAQ for q in g['qs']] == list(range(1, 37))
assert all(q[1] in d.TAGS for g in d.FAQ for q in g['qs']) and all(t in d.TAGS for _a, _b, t in d.NATIONALITY)
assert len(d.STEPS) == 8 and len(d.CHECKLIST) == 10 and len(d.MYTHS) == 12 and len(d.FEES) == 5 and len(d.OPEN_QS) == 8
assert d.FEES[0] == ('General · male', '₹1,000', '₹5,000')
text = repr(vars(d)).lower()
for banned in ('whatsapp', 'group chat', 'chat group', 'parents\' group', 'whatsapp group'):
    assert banned not in text, banned                                  # families are named only as the EduAakashaA Members Group

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
URL = '/jee-main-2027-registration'
pages = {}
for who, c in (('public', anon), ('free', free), ('premium', prem)):
    r = c.get(URL)
    assert r.status_code == 200, who
    h = r.get_data(as_text=True)
    pages[who] = h
    assert 'JEE Main 2027' in h and '24 Oct to 22 Nov' in h and '₹5,000' in h and 'Q36' in h and 'Q01' in h and h.count('class="q"') == 36, who
    assert 'EduAakashaA Members Group' in h and 'eduaakashaa-cube.webp' in h, who
    low = re.sub(r'<[^>]+>', ' ', h).lower()
    assert 'whatsapp group' not in low and 'group chat' not in low and 'chat group' not in low, who
    assert 'premiumNotice' not in h, who                                   # the page carries its own alert, not the generic "data not updated" notice
    assert 'jeemain.nta.nic.in' in h and 'dg-alert' in h and 'id="checklist"' in h, who
assert 'Join Premium Membership' in pages['public'] and 'Join the Members Group' in pages['public'] and 'Your Premium access is active' not in pages['public']
assert 'Your Premium access is active' in pages['premium'] and 'Open Member Home' in pages['premium'] and 'Join Premium Membership' not in pages['premium']
assert anon.get('/jee-registration').status_code == 301 and anon.get('/jee-main-registration').headers['Location'].endswith(URL)
assert anon.get('/static/img/mascot/eduaakashaa-cube.webp').status_code == 200
assert URL in anon.get('/sitemap.xml').get_data(as_text=True) and URL in anon.get('/').get_data(as_text=True)         # in the sitemap and the JEE / JOSAA menu
hub = prem.get('/member-home').get_data(as_text=True)
assert 'JEE Main 2027 registration guide' in hub

print('jee registration checks passed')
