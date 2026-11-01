"""JEE Main 2027 Paper 2A / 2B guide (public + members).
Run from college-predictor/:  python tests/test_jee_paper2.py"""
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
from app.data import jee_paper2 as d  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

# content integrity
assert len(d.MATHS) == 14 and [m[0] for m in d.MATHS] == list(range(1, 15))
assert len(d.QUIZ) == 12 and all(0 <= q[3] < len(q[2]) == 4 for q in d.QUIZ)
assert len(d.INTEREST) == 12 and {a for _s, a in d.INTEREST} == set(d.AXES)
assert all(t in d.TAGS for _q, t, _a in d.FAQ) and len(d.DEADLINES) == 6
assert d.PATTERN[3] == ('Total', '77 questions, 400 marks', '100 questions, 400 marks')
assert 'No ' not in d.MARKING[1][1] and d.FEES[0][1:] == ('₹1,000', '₹5,000') and d.FEES[5][1:] == ('₹2,000', '₹10,000')
assert len(d.COLLEGES) == 18 and {c[3] for c in d.COLLEGES} == {g[0] for g in d.COLLEGE_GROUPS}
assert all(o <= c for _n, _c, _s, _g, pr in d.COLLEGES for rows in pr.values() for _q, o, c in rows)
assert d.FEE_CATS[0] == ('General, male', 1000, 5000, 2000, 10000) and all(e == 2 * b and c == 2 * a or w.startswith('Gen-EWS') for w, a, b, c, e in d.FEE_CATS)
assert 'whatsapp' not in repr(vars(d)).lower()

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


anon, prem = app.test_client(), login('p@x.com')
URL = '/jee-main-2027-paper-2-barch-bplanning'
pages = {}
for who, c in (('public', anon), ('premium', prem)):
    r = c.get(URL)
    assert r.status_code == 200, who
    h = r.get_data(as_text=True)
    pages[who] = h
    assert 'Paper 2A' in h and '22 November 2026' in h and '20, 21, 22, 23, 24 and 28 January 2027' in h and '2, 3, 4, 5, 6 and 7 April 2027' in h, who
    assert 'UNIT' not in h and h.count('class="pp-qz"') == 12 and h.count('class="pp-lk"') == 12 and h.count('class="q"') == len(d.FAQ), who
    assert h.count('class="fx-row"') == 4 and h.count('class="cl"') == 18 and 'id="colleges"' in h and 'SPA New Delhi' in h and 'Kharagpur' in h, who
    assert 'Water colours are not allowed' in h and 'id="assess"' in h and 'dg-alert' in h and 'premiumNotice' not in h, who
    assert 'EduAakashaA Members Group' in h and 'eduaakashaa-cube.webp' in h and 'nta.ac.in/Quiz' in h, who
    low = re.sub(r'<[^>]+>', ' ', h).lower()
    assert 'whatsapp group' not in low and 'group chat' not in low, who
    names = re.findall(r'name="([lq]\d+)"', h)
    assert len(set(names)) == 24, who                                    # every radio group has its own name
assert 'Join Premium Membership' in pages['public'] and 'Your Premium access is active' in pages['premium']
for a in ('/jee-paper-2', '/jee-main-paper-2', '/jee-barch-bplanning'):
    assert anon.get(a).status_code == 301 and anon.get(a).headers['Location'].endswith(URL), a
assert URL in anon.get('/sitemap.xml').get_data(as_text=True) and URL in anon.get('/').get_data(as_text=True)
assert 'JEE Paper 2: B.Arch and B.Planning guide' in prem.get('/member-home').get_data(as_text=True)
# the registration page still renders with the shared stylesheet partial
assert 'jr2-hero' in anon.get('/jee-main-2027-registration').get_data(as_text=True)

print('jee paper 2 checks passed')
