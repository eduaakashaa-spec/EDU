"""B.Arch and B.Planning mentorship programme page (members). Run from college-predictor/:  python tests/test_barch_mentorship.py"""
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
from app.data import barch_programme as p  # noqa: E402
from app.data.mentorship_addons import ADDONS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

by = {a['key']: a for a in ADDONS}
assert len(by['barch']['sessions']) == 14 and len(by['bplan']['sessions']) == 10
# the phase map must cover every session of each track exactly once
assert sorted(n for ph in p.PHASES for n in ph[3]) == list(range(1, 15)) and sorted(n for ph in p.PHASES for n in ph[4]) == list(range(1, 11))
blob = repr(vars(p)) + repr(by['barch']) + repr(by['bplan'])
assert not re.search(r'guarantee(d)?\b(?!.*\bnot\b)', ' '.join(by['barch']['blurb'].split())) and 'whatsapp' not in blob.lower()
assert 'Paper 2A' in blob and 'Paper 2B' in blob and 'NATA' in blob and 'JoSAA' in blob and 'CSAB' not in blob

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
URL = '/barch-bplanning-mentorship'
assert anon.get(URL).status_code == 302 and free.get(URL).status_code == 403              # members only
h = prem.get(URL).get_data(as_text=True)
assert prem.get(URL).status_code == 200 and 'B.Arch and B.Planning' in h and 'dg-alert' in h and 'Your Premium access is active' in h
assert h.count('<li><strong>') >= 24 and 'NATA' in h and 'Paper 2B' in h and 'EduAakashaA Members Group' in h and 'eduaakashaa-cube.webp' in h
assert '/mentorship/addons#barch' in h and '/mentorship/addons#bplan' in h and 'premiumNotice' not in h
assert '22 Nov 2026' in h and '2 to 7 Apr 2027' in h and 'Reference' in h
# the add-on catalogue lists both programmes
cat = prem.get('/mentorship/addons').get_data(as_text=True)
assert 'id="barch"' in cat and 'id="bplan"' in cat and 'B.Arch (JEE Main Paper 2A, NATA' in cat
assert 'B.Arch and B.Planning mentorship' in prem.get('/member-home').get_data(as_text=True)
print('barch mentorship checks passed')
