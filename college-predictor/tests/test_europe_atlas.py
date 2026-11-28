"""Members page /europe-admissions-atlas: the built report, access control, sandbox header and tile. Run from college-predictor/:  python tests/test_europe_atlas.py"""
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

# 1. the built report
page = open(os.path.join(ROOT, 'app', 'data', 'europe', 'atlas.html'), encoding='utf-8').read()
assert page.startswith('<!doctype html>') and 'data-theme="light"' in page and '/*DATA*/' not in page
data = json.loads(re.search(r'var D=(\{.*?\});\n', page, re.S).group(1).replace('<\\/', '</'))
assert len(data['unis']) == 18 and len(data['countries']) == 11
for u in data['unis']:
    assert u['sources'] and u['web'].startswith('http') and len(u['issues']) == 3 and all(u[k] for k in 'SWOT'), u['key']
    if u['totalU'] is not None:
        assert u['totalU'] == (u['tuiU'] + u['liveU'] + u['yeU']) * u['yrs'] + u['oneU'], u['key']
for banned in ('+971', 'gmail.com'):
    assert banned not in page, banned                                                      # India-only contact details

assert data['img'] == '/static/img/europe/'
for name in ['banner'] + [u['key'] for u in data['unis']]:
    f = os.path.join(ROOT, 'app', 'static', 'img', 'europe', name + '.jpg')
    assert os.path.exists(f) and open(f, 'rb').read(2) == b'\xff\xd8' and os.path.getsize(f) < 150000, name

# 2. access, wrapper and sandbox
app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Member', email='m@x.com', tier='elite', password_hash=pw()), User(name='Free', email='f@x.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


for url in ('/europe-admissions-atlas', '/europe-admissions-atlas/report'):
    with app.app_context():
        assert app.test_client().get(url).status_code in (302, 401, 403), url              # signed-out visitors
    with app.app_context():
        assert login('f@x.com').get(url).status_code in (302, 403), url                    # free accounts
with app.app_context():
    c = login('m@x.com')
    r = c.get('/europe-admissions-atlas')
    assert r.status_code == 200 and '/europe-admissions-atlas/report' in r.get_data(as_text=True) and 'img/europe/banner.jpg' in r.get_data(as_text=True)
    r = c.get('/europe-admissions-atlas/report')
    assert r.status_code == 200 and r.headers['Content-Security-Policy'].startswith('sandbox ') and 'allow-same-origin' not in r.headers['Content-Security-Policy']
    assert 'no-cache' in r.headers['Cache-Control']
    r.close()

from app.services import member_hub  # noqa: E402

assert 'main.europe_atlas' in open(member_hub.__file__, encoding='utf-8').read()
print('europe atlas checks passed')
