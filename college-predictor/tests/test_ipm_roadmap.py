"""IPM 2027 roadmap (premium): gate, honesty labels, instructions, config, hub tile, lead intake.
Run from college-predictor/:  python tests/test_ipm_roadmap.py"""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import PageLead, User
from app.routes import IPM_IIMS
from app.services import roadmap_cfg

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Prem', email='p@x.com', tier='premium', password_hash=pw()),
                        User(name='Free', email='f@x.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'x'})
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/ipm-2027-roadmap').status_code in (302, 401)
assert free.get('/ipm-2027-roadmap').status_code == 403

r = prem.get('/ipm-2027-roadmap')
t = r.get_data(as_text=True)
assert r.status_code == 200 and '{%' not in t and 'Five-Year IPM 2027' in t
for fact in ('4 May 2026', 'IPMAT Indore', 'IPMAT Rohtak', 'JIPMAT', 'Documents checklist', 'Common mistakes to avoid', 'ipmadmissions@iimidr.ac.in'):
    assert fact in t, fact
for abbr, _city, _route in IPM_IIMS:
    assert t.count(abbr) >= 2, abbr                                                  # in the table and in the private matrix
# honesty: no invented 2027 dates, no guarantees
assert 'uc-tag official' in t and 'uc-tag reported' in t and 'uc-tag plan' in t and 'uc-tag sample' in t
assert 'Dates awaited' in t and 'No official 2027' in t and 'Not shown until verified' in t
assert 'guaranteed admission' not in t and 'eduaakashaa.in' not in t and 'www.eduaakashaa.com' in t
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static/js/roadmap_engine.js'), encoding='utf-8').read()
assert not [i for i in sorted(set(re.findall(r"\$\('#([A-Za-z0-9_-]+)'\)", js))) if f'id="{i}"' not in t]
cfg = json.loads(re.search(r'<script type="application/json" id="rm-cfg">(.*?)</script>', t, re.S).group(1)
                 .replace('\\u003c', '<').replace('\\u003e', '>').replace('\\u0026', '&').replace('\\u0027', "'"))
assert cfg['key'] not in (roadmap_cfg.UCEED['key'], roadmap_cfg.LAW['key']) and cfg['examName'] == 'IPMAT 2027' and len(cfg['phases']) == 7 and cfg['mock']['b'] is None
assert [x['official'] for x in cfg['targets']] == [False] * 4 and all('planning assumption' in x['label'] for x in cfg['targets'])
assert 'id="pf-target"' in t and 'id="mk-b"' not in t and 'Score (%)' in t
assert len(re.findall(r'<details><summary>', t)) >= 12
for a in re.findall(r'href="#([a-z-]+)"', t):
    assert f'id="{a}"' in t, a
for href in sorted(set(re.findall(r'href="(/[^"#]*)"', t))):
    if href.startswith('/static') or href == '/logout':
        continue
    assert prem.get(href).status_code in (200, 301, 302), href

assert prem.post('/api/leads?source=ipm-roadmap', json={'name': 'Ria', 'email': 'p@x.com', 'consent': True}).status_code in (200, 201)
with app.app_context():
    assert PageLead.query.filter_by(source='ipm-roadmap').count() == 1
assert '/ipm-2027-roadmap' in prem.get('/member-home').get_data(as_text=True)
assert 'IPM 2027 Roadmap' in free.get('/member-home').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('ipm roadmap checks passed')
