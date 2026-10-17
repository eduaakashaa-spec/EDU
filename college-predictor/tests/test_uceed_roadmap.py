"""UCEED 2027 roadmap (premium): access gate, verified facts, labels, links, hub tile, lead intake.
Run from college-predictor/:  python tests/test_uceed_roadmap.py"""
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
assert anon.get('/uceed-2027-roadmap').status_code in (302, 401)             # members only
assert free.get('/uceed-2027-roadmap').status_code == 403                    # upgrade page for non-premium

r = prem.get('/uceed-2027-roadmap')
t = r.get_data(as_text=True)
assert r.status_code == 200 and '{%' not in t and 'UCEED 2027: Your Roadmap to a' in t
# official facts (uceed.iitb.ac.in/2027, 17 Oct 2026)
for fact in ('17 Jan 2027', '9 am–12 noon', '6 Mar 2027', '15 Mar 2027', '21 Apr 2027', '1–31 Oct 2026'):
    assert fact in t, fact
for inst in ('IIT Bombay', 'IIT Delhi', 'IIT Guwahati', 'IIT Hyderabad', 'IIT Indore', 'IIT Roorkee', 'IIITDM Jabalpur'):
    assert t.count(inst) >= 2, inst                                          # in the overview and the institute table
# honesty: labels, no guarantees, no unsupported claims
assert 'uc-tag official' in t and 'uc-tag reported' in t and 'uc-tag plan' in t and 'uc-tag sample' in t
assert 'does not automatically guarantee admission' in t and 'No. Qualifying and ranking' in t
assert 'Not shown until verified' in t                                       # fees / seats / eligibility not invented per institute
assert 'KVPY' not in t and 'guaranteed admission' not in t and 'guarantee admission' not in t.replace('not automatically guarantee admission', '').replace('Does qualifying UCEED guarantee admission', '')
assert 'eduaakashaa.in' not in t and 'www.eduaakashaa.com' in t
# design-exam landscape section: official dates only where official; others labelled reported
assert 'id="design-exams"' in t and 'Prelims 20 Dec 2026' in t and '16 Mar 2027' in t
for ex in ('NID DAT', 'NIFT', 'SEED', 'CEED', 'Other institute tests'):
    assert ex in t, ex
# structure: 7 phases are built by the script; every id the script needs exists
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static/js/uceed_roadmap.js'), encoding='utf-8').read()
ids = set(re.findall(r"\$\('#([A-Za-z0-9_-]+)'\)", js))
missing = [i for i in sorted(ids) if f'id="{i}"' not in t]
assert not missing, missing
assert js.count("id: 'p") == 7
assert len(re.findall(r'<details><summary>', t)) >= 12                        # the 12 FAQs
assert prem.get('/static/js/uceed_roadmap.js').status_code == 200 and prem.get('/static/css/uceed_roadmap.css').status_code == 200
# nav anchors all resolve to a section id
for a in re.findall(r'href="#([a-z]+)"', t):
    assert f'id="{a}"' in t, a
# internal links work
for href in sorted(set(re.findall(r'href="(/[^"#]*)"', t))):
    if href.startswith('/static') or href == '/logout':
        continue
    assert prem.get(href).status_code in (200, 301, 302), href

# lead form posts to the existing intake; the member hub links to the page for premium and locks it for free users
res = prem.post('/api/leads?source=uceed-roadmap', json={'name': 'Asha', 'email': 'parent@x.com', 'class': 'Class 12', 'consent': True})
assert res.status_code in (200, 201)
with app.app_context():
    lead = PageLead.query.filter_by(source='uceed-roadmap').one()
    assert lead.email == 'parent@x.com'
assert '/uceed-2027-roadmap' in prem.get('/member-home').get_data(as_text=True)
assert 'UCEED 2027 Roadmap' in free.get('/member-home').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('uceed roadmap checks passed')
