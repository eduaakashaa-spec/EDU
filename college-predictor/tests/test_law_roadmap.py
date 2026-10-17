"""Law 2027 roadmap (premium): gate, announced dates + labels, comparison, links, config, hub tile, lead intake.
Run from college-predictor/:  python tests/test_law_roadmap.py"""
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
from app.routes import CLAT_NLUS
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
assert anon.get('/law-2027-roadmap').status_code in (302, 401)
assert free.get('/law-2027-roadmap').status_code == 403

r = prem.get('/law-2027-roadmap')
t = r.get_data(as_text=True)
assert r.status_code == 200 and '{%' not in t and 'Law Entrance Exams 2027: Your Roadmap to a' in t
for fact in ('6 Dec 2026', '13 Dec 2026', '19 &amp; 26 Dec 2026', '3 Aug – 31 Oct 2026', '26 National Law Universities'):
    assert fact in t, fact
assert len(CLAT_NLUS) == 26 and len({a for a, _ in CLAT_NLUS}) == 26
for abbr, _city in CLAT_NLUS:
    assert t.count(abbr) >= 2, abbr                                              # in the table and in the private matrix
# honesty
assert 'uc-tag official' in t and 'uc-tag reported' in t and 'uc-tag plan' in t and 'uc-tag sample' in t
assert 'A rank is not a seat' in t and 'Not shown until verified' in t and 'could not confirm 2027 dates' in t
assert 'guaranteed admission' not in t and 'eduaakashaa.in' not in t and 'www.eduaakashaa.com' in t
assert 'Dates awaited' in t                                                        # CLAT counselling not invented
# engine config: every id the script needs is present; 7 phases; targets include the assumed next cycle (flagged)
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static/js/roadmap_engine.js'), encoding='utf-8').read()
assert not [i for i in sorted(set(re.findall(r"\$\('#([A-Za-z0-9_-]+)'\)", js))) if f'id="{i}"' not in t]
cfg = json.loads(re.search(r'<script type="application/json" id="rm-cfg">(.*?)</script>', t, re.S).group(1)
                 .replace('\\u003c', '<').replace('\\u003e', '>').replace('\\u0026', '&').replace('\\u0027', "'"))
assert cfg['key'] != roadmap_cfg.UCEED['key'] and cfg['examName'] == 'CLAT 2027' and len(cfg['phases']) == 7 and cfg['mock']['b'] is None
assert [x['official'] for x in cfg['targets']] == [True, True, True, False]
assert 'planning assumption' in cfg['targets'][-1]['label']
assert 'id="pf-target"' in t and 'id="mk-b"' not in t and 'Score (/120)' in t
assert len(re.findall(r'<details><summary>', t)) >= 12
for a in re.findall(r'href="#([a-z-]+)"', t):
    assert f'id="{a}"' in t, a
for href in sorted(set(re.findall(r'href="(/[^"#]*)"', t))):
    if href.startswith('/static') or href == '/logout':
        continue
    assert prem.get(href).status_code in (200, 301, 302), href

# exam schedule page agrees with the announced dates
es = app.test_client().get('/exam-schedule').get_data(as_text=True)
assert 'Sunday 13 Dec 2026' in es and '19 &amp; 26 Dec 2026' in es

assert prem.post('/api/leads?source=law-roadmap', json={'name': 'Ria', 'email': 'p@x.com', 'consent': True}).status_code in (200, 201)
with app.app_context():
    assert PageLead.query.filter_by(source='law-roadmap').count() == 1
assert '/law-2027-roadmap' in prem.get('/member-home').get_data(as_text=True)
assert 'Law Entrance 2027 Roadmap' in free.get('/member-home').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('law roadmap checks passed')
