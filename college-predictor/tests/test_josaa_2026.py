"""JoSAA 2026 seat allotment and analytics page: data totals, premium access, the data file.
Run from college-predictor/:  python tests/test_josaa_2026.py"""
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

path = os.path.join(ROOT, 'app', 'static', 'data', 'josaa_2026.json')
D = json.load(open(path, encoding='utf-8'))
S = D['stats']
assert len(D['insts']) == 138 and S['institutes'] == 138 and S['nit_institutes'] == 32 and S['seats'] == 25162 and S['cells'] == 13292
assert S['never_cells'] == 336 and S['never_seats'] == 362 and [c['cells'] for c in S['coverage']] == [13292, 13047, 12989, 12968, 12936]
assert sum(sum(v) for v in S['seat_by'].values()) == 25162 and D['ap']['seats'] == 645
ncol = len(D['cols'].split(','))
assert all(len(r) == ncol for r in D['rows']) and sum(r[5] for r in D['rows']) == 25162
assert all(0 <= r[0] < 138 and 0 <= r[1] < len(D['progs']) and 0 <= r[3] < 10 and r[4] in (0, 1) for r in D['rows'])
for r in D['rows']:
    for v in r[6:16]:
        assert v is None or isinstance(v, (int, float)) or (isinstance(v, str) and v.endswith('P')), v
assert {x[2] for x in D['insts']} == {'IIT', 'IISc', 'NIT+', 'IIIT', 'GFTI'}
# a known cell: IIT BHU Architecture, AI, OPEN, gender-neutral: R1 15019 to 26220, R5 closing 28480
bhu = next(i for i, x in enumerate(D['insts']) if x[1] == 'Indian Institute of Technology (BHU) Varanasi')
arch = next(r for r in D['rows'] if r[0] == bhu and 'Architecture (5' in D['progs'][r[1]][1] and r[2] == 'AI' and r[3] == 0 and r[4] == 0)
assert (arch[6], arch[7], arch[15]) == (15019, 26220, 28480)

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
assert anon.get('/josaa-2026-analytics').status_code == 302 and free.get('/josaa-2026-analytics').status_code == 403
r = prem.get('/josaa-2026-analytics')
h = r.get_data(as_text=True)
assert r.status_code == 200 and 'dg-alert' in h and 'Cut-off explorer' in h and 'Rank finder' in h and 'data/josaa_2026.json' in h and 'Architecture and Planning' in h
assert prem.get('/static/data/josaa_2026.json').status_code == 200
mh = prem.get('/member-home').get_data(as_text=True)
assert 'JoSAA 2026 Seat Allotment and Analytics' in mh
print('josaa 2026 checks passed')
