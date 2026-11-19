"""Neikkarapatti & Palani complimentary membership: public landing page (English / Tamil), registration form, admin verification and activation.
Run from college-predictor/:  python tests/test_nkp_campaign.py"""
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_membership import CampaignRegistration  # noqa: E402
from app.services import campaign as cp  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='admin@x.test', tier='admin', password_hash=pw()),
                        User(name='Free', email='free@x.test', tier='free', password_hash=pw()),
                        User(name='Existing Free', email='existing@x.test', tier='free', password_hash=pw()),
                        User(name='Paid Premium', email='paid@x.test', tier='premium', tier_expires_at=datetime.utcnow() + timedelta(days=900), password_hash=pw()),
                        User(name='Staff Mentor', email='staff@x.test', tier='ea_mentor', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302, email
    return c


admin, free = login('admin@x.test'), login('free@x.test')
anon = app.test_client()


def form(**over):
    d = dict(studentName='Karthik Raja', school='Guruvappa Higher Secondary School', stream='PCM', admissions=['JEE Main / Advanced', 'TNEA'],
             mobile='+919876543210', email='karthik@x.test', parentName='Raja Murugan', parentMobile='', guidanceLanguage='Tamil', code='nkp',
             consent=True, pageLanguage='ta')
    d.update(over)
    return d


def post(data, ip='10.0.0.1'):
    return anon.post('/neikkarapatti-palani/register', json=data, headers={'X-Forwarded-For': ip})


# 1. the public page: no login needed, announcement, code, both languages, the form
r = anon.get('/neikkarapatti-palani')
h = r.get_data(as_text=True)
assert r.status_code == 200
for t in ('Special announcement', 'Complimentary', 'NKP', 'id="regForm"', 'data-lang="ta"', 'Neikkarapatti', 'id="formErr"', 'css/nkp_landing.css', 'js/nkp_landing.js', 'img/nkp/palani.jpg'):
    assert t in h, t
assert 'data:image' not in h and 'og:title' in h
for a in ('/nkp', '/palani', '/neikkarapatti'):
    rr = anon.get(a)
    assert rr.status_code == 301 and rr.headers['Location'].endswith('/neikkarapatti-palani'), a
css = anon.get('/static/css/nkp_landing.css').get_data(as_text=True)
js = anon.get('/static/js/nkp_landing.js').get_data(as_text=True)
assert not re.search(r'(^|\})\s*(html|body)\s*\{', css) and 'நெய்க்காரப்பட்டி' in js and '/neikkarapatti-palani/register' in js
assert anon.get('/static/img/nkp/palani.jpg').status_code == 200

# 2. validation: every problem gives a readable message in English and Tamil and saves nothing
cases = [dict(code='XYZ'), dict(consent=False), dict(mobile='12345'), dict(email='nope'), dict(studentName='K'), dict(stream='XX'), dict(admissions=[]),
         dict(parentName=''), dict(parentMobile='123'), dict(school='ab')]
for i, c in enumerate(cases):
    rr = post(form(**c), ip=f'10.1.0.{i}')
    j = rr.get_json()
    assert rr.status_code == 400 and j['ok'] is False and j['error'] and j['error_ta'], c
assert anon.post('/neikkarapatti-palani/register', data='not json', headers={'X-Forwarded-For': '10.2.0.1'}).status_code == 400
assert anon.post('/neikkarapatti-palani/register', json=[1, 2], headers={'X-Forwarded-For': '10.2.0.2'}).status_code == 400
with app.app_context():
    assert CampaignRegistration.query.count() == 0

# 3. a good registration is stored as New and gives no access by itself
rr = post(form())
j = rr.get_json()
assert rr.status_code == 200 and j['ok'] and j['reference'] == 'EA-NKP-0001' and j['existing'] is False
with app.app_context():
    r0 = CampaignRegistration.query.one()
    assert r0.status == 'New' and r0.mobile == '+919876543210' and r0.admissions == 'JEE Main / Advanced, TNEA' and r0.consent and r0.page_language == 'ta'
    assert User.query.filter_by(email='karthik@x.test').count() == 0, 'registering must not create an account'
# the same email or mobile again returns the first registration
j2 = post(form(studentName='Karthik R', email='KARTHIK@x.test'), ip='10.0.0.9').get_json()
assert j2['ok'] and j2['reference'] == 'EA-NKP-0001' and j2['existing'] is True
assert post(form(email='other@x.test'), ip='10.0.0.8').get_json()['reference'] == 'EA-NKP-0001'
with app.app_context():
    assert CampaignRegistration.query.count() == 1
# numbers move on for a different student; a +91 or 0 prefix is accepted
j3 = post(form(studentName='Meena Devi', email='meena@x.test', mobile='09123456789', school='Crescent Matriculation School', stream='PCB',
               admissions=['NEET UG']), ip='10.0.0.7').get_json()
assert j3['ok'] and j3['reference'] == 'EA-NKP-0002'
# unknown admissions are ignored, throttle stops a flood from one address
for i in range(cp.RATE_MAX + 1):
    last = post(form(email=f'flood{i}@x.test', mobile=f'98765{i:05d}'), ip='10.9.9.9')
assert last.status_code == 429 and last.get_json()['error_ta']

# 4. only admins can see or act
for who, c in (('anon', anon), ('member', free)):
    assert c.get('/admin/campaigns').status_code in (302, 401, 403), who
    assert c.post('/admin/campaigns/1/activate').status_code in (302, 401, 403), who
page = admin.get('/admin/campaigns').get_data(as_text=True)
assert 'Karthik Raja' in page and 'EA-NKP-0001' in page and 'Meena Devi' in page and 'Campaign registrations' in page
assert 'Karthik' in admin.get('/admin/campaigns?q=guruvappa').get_data(as_text=True) and 'Meena Devi' not in admin.get('/admin/campaigns?q=guruvappa').get_data(as_text=True)

# 5. activate: account created with complimentary Premium for the chosen days, the temporary password works, nothing is invoiced
with app.app_context():
    rid = CampaignRegistration.query.filter_by(reference='EA-NKP-0001').one().id
resp = admin.post(f'/admin/campaigns/{rid}/activate', data={'days': '200', 'notify': '1'}, follow_redirects=True)
t = resp.get_data(as_text=True)
assert resp.status_code == 200 and 'Account created for karthik@x.test' in t and 'Temporary password' in t
tmp = re.search(r'Temporary password \(shown once\): ([A-Za-z0-9]+)', t).group(1)
with app.app_context():
    u = User.query.filter_by(email='karthik@x.test').one()
    assert u.tier == 'premium' and u.is_premium
    days = (u.tier_expires_at - datetime.utcnow()).days
    assert 198 <= days <= 200, days
    reg = db.session.get(CampaignRegistration, rid)
    assert reg.status == 'Activated' and reg.user_id == u.id and reg.access_until == u.tier_expires_at
    from app.models_membership import MembershipInvoice
    assert MembershipInvoice.query.count() == 0
assert app.test_client().post('/login', data={'email': 'karthik@x.test', 'password': tmp}).status_code == 302

# 6. existing accounts: a free one is upgraded, a paid one is never shortened, staff are untouched
def reg_for(email, name, mobile):
    out = post(form(studentName=name, email=email, mobile=mobile), ip='10.3.0.' + mobile[-2:]).get_json()
    with app.app_context():
        return CampaignRegistration.query.filter_by(reference=out['reference']).one().id

r_free = reg_for('existing@x.test', 'Existing Free', '9000000011')
t = admin.post(f'/admin/campaigns/{r_free}/activate', data={'days': '365'}, follow_redirects=True).get_data(as_text=True)
assert 'upgraded' in t and 'Temporary password' not in t
with app.app_context():
    u = User.query.filter_by(email='existing@x.test').one()
    assert u.tier == 'premium' and u.is_premium
r_paid = reg_for('paid@x.test', 'Paid Premium', '9000000022')
with app.app_context():
    before = User.query.filter_by(email='paid@x.test').one().tier_expires_at
admin.post(f'/admin/campaigns/{r_paid}/activate', data={'days': '30'})
with app.app_context():
    assert User.query.filter_by(email='paid@x.test').one().tier_expires_at >= before
r_staff = reg_for('staff@x.test', 'Staff Mentor', '9000000033')
assert 'staff account' in admin.post(f'/admin/campaigns/{r_staff}/activate', follow_redirects=True).get_data(as_text=True)
with app.app_context():
    assert User.query.filter_by(email='staff@x.test').one().tier == 'ea_mentor'

# 7. reject and reopen; bad status is refused; only admins
with app.app_context():
    rid2 = CampaignRegistration.query.filter_by(reference='EA-NKP-0002').one().id
assert free.post(f'/admin/campaigns/{rid2}/status', data={'status': 'Rejected'}).status_code in (302, 401, 403)
assert admin.post(f'/admin/campaigns/{rid2}/status', data={'status': 'Active'}).status_code == 400
admin.post(f'/admin/campaigns/{rid2}/status', data={'status': 'Rejected', 'note': 'School not in Palani'})
with app.app_context():
    x = db.session.get(CampaignRegistration, rid2)
    assert x.status == 'Rejected' and x.note == 'School not in Palani' and x.user_id is None
admin.post(f'/admin/campaigns/{rid2}/status', data={'status': 'New'})
with app.app_context():
    assert db.session.get(CampaignRegistration, rid2).status == 'New'
# a cross-site post is blocked by the portal-wide check
assert anon.post('/neikkarapatti-palani/register', json=form(email='x@x.test'), headers={'Origin': 'https://evil.example', 'X-Forwarded-For': '10.4.0.1'}).status_code == 403
print('nkp campaign checks passed')
