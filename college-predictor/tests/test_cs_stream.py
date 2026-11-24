"""Members page /computer-science-stream: data files, family classification, access and the page itself. Run from college-predictor/:  python tests/test_cs_stream.py"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'cs_stream'))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

import build_colleges as B  # noqa: E402
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.services import cs_stream  # noqa: E402

# 1. family classification: computer-stream programmes land in the right family, other branches are left out
CASES = {
    'Computer Science and Engineering (4 Years, Bachelor of Technology)': 'core',
    'Computer Science and Engineering (Cyber Security) (4 Years, Bachelor of Technology)': 'cyber',
    'Computer Science and Engineering (Artificial Intelligence and Machine Learning) (4 Years, Bachelor of Technology)': 'aids',
    'Artificial Intelligence and Data Science (4 Years, Bachelor of Technology)': 'aids',
    'Data Science and Engineering (4 Years, Bachelor of Technology)': 'aids',
    'Information Technology (4 Years, Bachelor of Technology)': 'it',
    'Computer Science and Business (4 Years, Bachelor of Technology)': 'biz',
    'Information Technology-Business Informatics (4 Years, Bachelor of Technology)': 'biz',
    'Mathematics and Computing (4 Years, Bachelor of Technology)': 'mnc',
    'Electronics Communication and Artificial Intelligence (4 Years, Bachelor of Technology)': 'aids',
    'Industrial Internet of Things (4 Years, Bachelor of Technology)': 'hybrid',
    'Biotechnology and Biochemical Engineering (4 Years, Bachelor of Technology)': None,
    'Chemical Engineering with Data Analytics (4 Years, Bachelor of Technology)': None,
    'Architecture (5 Years, Bachelor of Architecture)': None,
    'Mechanical Engineering (4 Years, Bachelor of Technology)': None,
}
for name, want in CASES.items():
    assert B.family(name) == want, (name, B.family(name), want)

# 2. the data files
p = cs_stream.payload()
assert len(p['josaa']) >= 100 and p['n_programmes'] >= 250, (len(p['josaa']), p['n_programmes'])
fam_keys = {f[0] for f in p['families']}
assert fam_keys == {'core', 'it', 'aids', 'cyber', 'mnc', 'biz', 'hybrid'}
for i in p['josaa']:
    assert i['p'], i['n']
    for name, fam, yrs, close in i['p']:
        assert fam in fam_keys and (close is None or close > 0), (i['n'], name)
iit = [i for i in p['josaa'] if i['t'] == 'IIT']
assert len(iit) >= 22 and all(any(x[1] == 'core' for x in i['p']) for i in iit if 'Science, Bangalore' not in i['n']), 'every IIT lists core CSE'
madras = next(i for i in p['josaa'] if i['n'] == 'Indian Institute of Technology Madras')
assert madras['r'] == 1 and any(x[1] == 'aids' for x in madras['p'])
bombay = next(i for i in p['josaa'] if i['n'] == 'Indian Institute of Technology Bombay')
assert bombay['r'] == 3 and {x[1] for x in bombay['p']} == {'core'}                       # the leading institutes keep the computer family small
# near-name NIRF matches that are wrong must stay unmatched
for bad in ('Indian Institute of Information Technology Bhopal', 'National Institute of Technology, Andhra Pradesh', 'International Institute of Information Technology, Bhubaneswar'):
    row = next(i for i in p['josaa'] if i['n'] == bad)
    assert row['r'] is None, bad
assert len(p['private']) >= 10 and all(u['p'] and (u['r'] or u['b']) and u['city'] for u in p['private']), 'every private entry has programmes, a NIRF rank or band and a city'
assert all(fam in fam_keys for u in p['private'] for _n, fam in u['p'] if fam), 'private programme families are known'
assert len({u['n'] for u in p['private']}) == len(p['private']), 'no university listed twice'
assert p['tnea'] and p['tnea']['total'] > 300 and p['tnea']['counts']['core'] > 300 and p['tnea']['listed']
assert all(x['programmes'] for x in p['tnea']['listed'])
assert len(p['branches']) == 7 and all(b['overlap'] in (1, 2, 3, 4, 5) for b in p['branches'])
for s in p['subjects']:
    assert len(s[1]) == len(p['subject_cols']) and all(v in (0, 1, 2, 3) for v in s[1]), s
blob = json.dumps(p).lower()
for banned in ('lpa', 'lakh', 'crore', 'package of', '100% placement'):
    assert banned not in blob, banned                                                      # no salary or placement-rate claims

# 3. access and the page
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


with app.app_context():
    r = app.test_client().get('/computer-science-stream')
    assert r.status_code in (302, 401, 403), r.status_code                                # signed-out visitors are sent to log in
with app.app_context():
    r = login('f@x.com').get('/computer-science-stream')
    assert r.status_code in (302, 403), r.status_code                                     # free accounts do not get the members page
with app.app_context():
    c = login('m@x.com')
    r = c.get('/computer-science-stream')
    assert r.status_code == 200, r.status_code
    html = r.get_data(as_text=True)
    for tab in ('Start here', 'The branches', 'Subjects', 'Projects and jobs', 'Colleges', 'Why the offer differs', 'Choose and study ahead', 'AI and future jobs'):
        assert tab in html, tab
    m = re.search(r'<script type="application/json" id="cs-data">(.*?)</script>', html, re.S)
    data = json.loads(m.group(1).replace('\\u003c', '<').replace('\\u003e', '>').replace('\\u0026', '&').replace('\\u0027', "'"))
    assert len(data['josaa']) == len(p['josaa']) and data['private'] and data['tnea']
    assert 'js/cs_stream.js' in html and 'css/cs_stream.css' in html
    assert 'Computer science stream explained' in c.get('/members').get_data(as_text=True) or c.get('/members/home').status_code in (200, 302, 404)
print('cs stream checks passed')
