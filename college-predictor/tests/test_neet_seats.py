"""NEET MBBS seat matrix analytics: data integrity (totals equal the figures printed in the NMC notices), premium access and the page.
Run from college-predictor/:  python tests/test_neet_seats.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

with open(os.path.join(ROOT, 'app', 'static', 'data', 'neet_seats_2025.json'), encoding='utf-8') as f:
    D = json.load(f)
R = D['rows']
assert len(R) == 819 == D['totals']['colleges'] and D['totals']['colleges_oct10'] == 813
assert sum(r['s24'] for r in R) == 117750 == D['totals']['s24'] and sum(r['s25'] for r in R) == 128875 == D['totals']['s25'] and D['totals']['s25_oct10'] == 126600
assert [r['n'] for r in R] == list(range(1, 820))
assert all(r['state'] in D['states'] and r['college'] and r['mgmt'] and r['s24'] >= 0 and r['s25'] >= 0 for r in R)
assert len(D['states']) >= 30 and 'Tamil Nadu' in D['states'] and 'Uttar Pradesh' in D['states']
mg = {r['mgmt'] for r in R}
assert mg <= {'Government', 'Trust', 'Private', 'Society', 'Government (society)', 'Deemed university', 'Central government', 'Government (trust)', 'Company'}, mg
news = [r for r in R if r['s24'] == 0 and r['s25'] > 0]
assert len(news) == 43 and sum(r['s25'] for r in news) == 3600
assert sum(r['s24'] - r['s25'] for r in R if r['s25'] < r['s24']) == 456      # the notice says 456 seats were reduced during renewal
assert D['changed_since_oct10'] and sum(1 for r in R if r['s25_oct10'] not in (None, r['s25'])) + sum(1 for r in R if r['s25_oct10'] is None) == len(D['changed_since_oct10'])
blob = json.dumps(R, ensure_ascii=False).lower()
for bad in ('prepp', 'collegedekho', 'careers360', 'collegedunia', 'getmyuni', 'toprankers', 'whatsapp', 'http'):
    assert bad not in blob, bad

app = create_app()
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw)])
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
for c in (anon, free):
    assert c.get('/neet-mbbs-seats-2025-analytics').status_code in (301, 302, 403)
r = prem.get('/neet-mbbs-seats-2025-analytics')
page = r.get_data(as_text=True)
assert r.status_code == 200 and 'MBBS seat matrix and analytics' in page and 'dg-alert' in page and 'neet_seats_2025.json' in page
for tab in ('ov', 'st', 'gr', 'ex', 'me'):
    assert 'data-p="%s"' % tab in page, tab
assert 'cannot say what rank a college closed at' in page
assert prem.get('/static/data/neet_seats_2025.json').status_code == 200
home = prem.get('/member-home').get_data(as_text=True)
assert 'NEET MBBS seat matrix analytics' in home
try:
    os.remove(_db)
except OSError:
    pass
print('neet seats checks passed')
