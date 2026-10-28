"""Ready-made mentorship add-on programmes: seeding, enrolment, catalogue, requests, honesty. Run: python tests/test_mentorship_addons.py"""
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
from app.data.mentorship_addons import ADDONS, TIER
from app.extensions import bcrypt, db
from app.models import PageLead, User
from app.models_mentorship import MsEnrolment, MsProgramme, MsSession
from app.services import mentorship as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='a@x.com', tier='admin', password_hash=pw()),
                        User(name='Stu', email='s@x.com', tier='elite', password_hash=pw()),
                        User(name='Free', email='f@x.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'x'})
    return c


admin, stu, free, anon = login('a@x.com'), login('s@x.com'), login('f@x.com'), app.test_client()

# the content itself: nine programmes, unique keys, no invented figures
titles = ' '.join(a['title'] for a in ADDONS)
for need in ('UCEED', 'NID', 'NIFT', 'Abu Dhabi', 'TNEA', 'State-specific', 'SRM', 'Amrita', 'VIT'):
    assert need in titles, need
assert len(ADDONS) == 9 and len({a['key'] for a in ADDONS}) == 9 and all(len(a['sessions']) >= 6 and a['verify'] for a in ADDONS)
blob = json.dumps(ADDONS)
assert not re.search(r'₹|\bRs\.?\s?\d|\b\d+\s?lakh|\bcut-?off of \d|guaranteed', blob, re.I)

# the IIT Delhi - Abu Dhabi add-on is built around CAET (and the JEE Advanced route for Indian nationals)
iitd = next(a for a in ADDONS if a['key'] == 'iitd-ad')
txt = json.dumps(iitd, ensure_ascii=False)
assert 'CAET' in txt and 'JEE Advanced' in txt and 'admissions.abudhabi.iitd.ac.in' in txt and 'Indian expatriate' in txt

# seeding is idempotent and does not disturb the standard programme
with app.app_context():
    old = MsProgramme(name='IIT Delhi – Abu Dhabi admission', tier=TIER, description='old')      # a site that loaded the first version
    db.session.add(old)
    db.session.commit()
    assert svc.ensure_addon_programmes() == 8                                                      # renamed in place, no duplicate
    assert MsProgramme.query.filter_by(name=iitd['title']).count() == 1 and MsProgramme.query.filter_by(name='IIT Delhi – Abu Dhabi admission').count() == 0
    assert MsProgramme.query.filter_by(name=iitd['title']).one().templates.count() == 7 and 'CAET' in MsProgramme.query.filter_by(name=iitd['title']).one().description
    assert svc.ensure_addon_programmes() == 0
    assert MsProgramme.query.filter_by(tier=TIER).count() == 9
    base = svc.ensure_default_programme()                                   # add-ons exist first: the standard programme must still be created
    assert base.tier == 'Elite Mentorship' and MsProgramme.query.count() == 10
    assert svc.ensure_default_programme().id == base.id
    tn = MsProgramme.query.filter_by(name='TNEA (Tamil Nadu engineering counselling)').one()
    assert tn.templates.count() == 8 and 'tneaonline.org' in tn.description

# admin button
assert admin.post('/mentorship/admin/addons/load').status_code == 302
assert free.post('/mentorship/admin/addons/load').status_code in (302, 403)
r = admin.get('/mentorship/admin')
assert r.status_code == 200 and b'Ready-made add-on programmes' in r.data and b'UCEED (B.Des at IITs)' in r.data

# enrolment into an add-on works like any programme (sessions copied from the template)
with app.app_context():
    pid = MsProgramme.query.filter_by(name='UCEED (B.Des at IITs)').one().id
r = admin.post('/mentorship/admin/enrol', data={'student_email': 's@x.com', 'programme_id': pid}, follow_redirects=True)
assert b'enrolled with 8 core sessions' in r.data
with app.app_context():
    e = MsEnrolment.query.filter_by(programme_id=pid).one()
    assert MsSession.query.filter_by(enrolment_id=e.id).count() == 8
    eid = e.id
assert stu.get(f'/mentorship/e/{eid}/home').status_code == 200

# catalogue: sign-in required, shows all nine, marks the enrolled one
assert anon.get('/mentorship/addons').status_code in (302, 401)
page = free.get('/mentorship/addons').get_data(as_text=True)
assert all(a['title'] in page.replace('&amp;', '&') or a['title'].split(' (')[0] in page for a in ADDONS) and 'do not guarantee admission' in page
assert 'You are enrolled' in stu.get('/mentorship/addons').get_data(as_text=True)
assert 'Request this programme' in free.get('/mentorship/addons').get_data(as_text=True)

# request: stored once per user per add-on
assert free.post('/mentorship/addons/tnea/request', data={'note': 'Class 12, Chennai'}).status_code == 302
assert free.post('/mentorship/addons/tnea/request').status_code == 302
assert free.post('/mentorship/addons/bogus/request').status_code == 404
with app.app_context():
    rows = PageLead.query.filter_by(source='mentorship-addon').all()
    assert len(rows) == 1 and rows[0].email == 'f@x.com' and json.loads(rows[0].payload_json)['addon'] == 'tnea'
assert 'Request received' in free.get('/mentorship/addons').get_data(as_text=True)

# branch catalogue now includes architecture, NID and NIFT programmes, added to existing catalogues too
from app.models_mentorship import MsBranch
with app.app_context():
    svc.ensure_branches()
    n = MsBranch.query.count()
    names = [b.name for b in MsBranch.query.all()]
    assert any(x.startswith('Architecture') for x in names) and sum(x.startswith('NID B.Des') for x in names) >= 5 and sum(x.startswith('NIFT') for x in names) >= 3
    assert 'Computer Science and Engineering' in names and len(set(names)) == n
    svc.ensure_branches()
    assert MsBranch.query.count() == n                                   # idempotent
    MsBranch.query.filter(MsBranch.name.like('NIFT%')).delete(synchronize_session=False)
    db.session.commit()
    svc.ensure_branches()                                                # a catalogue loaded before this release gets the missing ones
    assert MsBranch.query.count() == n
body = stu.get(f'/mentorship/e/{eid}/branch').get_data(as_text=True)
assert 'Architecture (B.Arch)' in body and 'NIFT B.Des: Fashion Design' in body

# hub tile for everyone signed in
assert 'Add-on programmes' in free.get('/member-home').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('mentorship add-on checks passed')
