"""HR Admin role and HR letters: access, issuing offer / experience / relieving letters, reference numbers, compensation maths, validation, PDF, register, void and templates.
Run from college-predictor/:  python tests/test_hr_letters.py"""
import os
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_hr import HrLetter  # noqa: E402
from app.services import hr_letters as hl  # noqa: E402

# ---- pure helpers -------------------------------------------------------------------------------------------------------------------------
assert hl.indian(840000) == '8,40,000' and hl.indian(65333) == '65,333' and hl.indian(1234567) == '12,34,567' and hl.indian(999) == '999' and hl.indian(0) == '0'
assert hl.parse_money('8,40,000') == 840000 and hl.parse_money('INR 3,36,000') == 336000
for bad in ('', 'abc', '-5', '1.2.3'):
    try:
        hl.parse_money(bad)
        raise AssertionError(bad)
    except ValueError:
        pass
assert hl.fy_of(date(2026, 3, 31)) == 2025 and hl.fy_of(date(2026, 4, 1)) == 2026
assert hl.make_ref('offer', 2026, 42) == 'EA/HR/OFFER/2026/0042' and hl.make_ref('relieving', 2026, 9) == 'EA/HR/REL/2026/0009' and hl.make_ref('experience', 2026, 17) == 'EA/HR/EXP/2026/0017'
rows = hl.comp_rows(dict(basic_annual=336000, hra_annual=168000, special_annual=252000, bonus_annual=28000, pf_annual=40320, gratuity_annual=15680))
assert [(r[1], r[2]) for r in rows] == [(28000, 336000), (14000, 168000), (21000, 252000), (2333, 28000), (65333, 784000), (3360, 40320), (1307, 15680), (70000, 840000)]   # the pack's sample figures
assert not hl.validate_body(hl.DEFAULTS['offer']) and not hl.validate_body(hl.DEFAULTS['experience']) and not hl.validate_body(hl.DEFAULTS['relieving'])
assert hl.validate_body('Hello {{nope}}') and hl.validate_body('@wow x')
for k, d in hl.DEFAULTS.items():                                                                          # every placeholder in a default template is a known field
    assert not hl.validate_body(d), k
assert 'office hours' not in ' '.join(hl.DEFAULTS.values()).lower()

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    for n, e, t in (('Admin', 'a@t.test', 'admin'), ('Hira HR', 'hr@t.test', 'hr_admin'), ('Mentor', 'm@t.test', 'ea_mentor'), ('Elite', 'e@t.test', 'elite'), ('Free', 'f@t.test', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw))
    db.session.commit()
    u = User.query.filter_by(email='hr@t.test').one()
    assert u.is_hr and u.is_hr_admin and not u.is_admin and not u.is_staff and not u.is_premium
    assert User.query.filter_by(email='a@t.test').one().is_hr and not User.query.filter_by(email='m@t.test').one().is_hr


def login(email):
    c = app.test_client()
    r = c.post('/login', data={'email': email, 'password': 'x'}, follow_redirects=False)
    assert r.status_code in (302, 303), (email, r.status_code)
    return c, r


# ---- access --------------------------------------------------------------------------------------------------------------------------------
anon = app.test_client()
assert anon.get('/hr/').status_code in (302, 303) and '/login' in anon.get('/hr/').headers['Location']
for email in ('m@t.test', 'e@t.test', 'f@t.test'):
    c, _ = login(email)
    for url in ('/hr/', '/hr/new/offer', '/hr/letters', '/hr/letters.csv', '/hr/templates', '/hr/templates/offer', '/hr/letters/1', '/hr/letters/1.pdf'):
        assert c.get(url).status_code == 403, (email, url)
    assert c.post('/hr/new/offer', data={}).status_code == 403 and c.post('/hr/letters/1/void', data={'reason': 'x'}).status_code == 403
hr, r = login('hr@t.test')
assert r.headers['Location'].endswith('/hr/'), r.headers['Location']                                      # HR Admin lands on the HR section
adm, _ = login('a@t.test')
for c in (hr, adm):
    for url in ('/hr/', '/hr/new/offer', '/hr/new/experience', '/hr/new/relieving', '/hr/letters', '/hr/templates', '/hr/templates/offer', '/hr/templates/experience', '/hr/templates/relieving'):
        t = c.get(url).get_data(as_text=True)
        assert c.get(url).status_code == 200, url
    assert 'data-how="hr-home"' in c.get('/hr/').get_data(as_text=True)
assert hr.get('/hr/new/bogus').status_code == 404 and hr.get('/hr/letters/999').status_code == 404
assert hr.get('/admin/users').status_code == 403                                                          # HR Admin is not an Admin: no member management
with app.test_request_context():
    from flask import url_for
    HOME = url_for('memberhub.home')
for c, want in ((hr, True), (adm, True)):
    assert ('HR letters' in c.get(HOME).get_data(as_text=True)) == want                                    # the Member Home tile
assert 'HR letters' not in login('e@t.test')[0].get(HOME).get_data(as_text=True)
nav = hr.get('/').get_data(as_text=True)
assert '/hr/' in nav                                                                                       # HR link in the header

# ---- issuing -------------------------------------------------------------------------------------------------------------------------------
OFFER = dict(issue_date='2026-11-17', candidate_full_name='Priya Ramesh', designation='Senior Admissions Counsellor', office_location='Coimbatore', date_of_joining='2026-12-01',
             working_hours='Monday to Friday, 9:00 AM to 6:00 PM', basic_annual='3,36,000', hra_annual='168000', special_annual='252000', bonus_annual='28000', pf_annual='40320', gratuity_annual='15680',
             reporting_manager_name='Arjun Krishnan', reporting_manager_designation='Head of Admissions', authorized_signatory_name='Dr. Muruganandam', authorized_signatory_designation='Founder & Director')
r = hr.post('/hr/new/offer', data=dict(OFFER, basic_annual=''))
assert r.status_code == 200 and 'Please fix' in r.get_data(as_text=True)
with app.app_context():
    assert HrLetter.query.count() == 0
r = hr.post('/hr/new/offer', data=OFFER, follow_redirects=False)
assert r.status_code == 302, r.get_data(as_text=True)[:400]
with app.app_context():
    o = HrLetter.query.one()
    OID = o.id
    assert o.ref_no == 'EA/HR/OFFER/2026/0001' and o.fy == 2026 and o.person_name == 'Priya Ramesh' and o.status == 'issued' and o.created_by == User.query.filter_by(email='hr@t.test').one().id
    assert o.values['annual_ctc'] == '8,40,000' and o.values['gross_monthly'] == '65,333' and o.values['total_monthly'] == '70,000' and o.values['issue_date'] == '17 November 2026'
    assert o.values['candidate_first_name'] == 'Priya'                                                      # defaults to the first word of the full name
page = hr.get('/hr/letters/%d' % OID).get_data(as_text=True)
for want in ('EA/HR/OFFER/2026/0001', 'Dear Priya,', '17 November 2026', 'INR 8,40,000', '3,36,000', '65,333', 'Candidate Acceptance', 'Dr. Muruganandam', 'Founder &amp; Director', 'Annexure A'):
    assert want in page, want
assert '{{' not in page.split('hl-page', 1)[1] and 'eduaakashaa.com' in page
pdf = hr.get('/hr/letters/%d.pdf' % OID)
assert pdf.status_code == 200 and pdf.data[:4] == b'%PDF' and pdf.mimetype == 'application/pdf' and len(pdf.data) > 3000 and b'EA-HR-OFFER-2026-0001.pdf' in str(pdf.headers).encode()

# validation: dates and amounts
bad = dict(OFFER, basic_annual='abc')
assert hr.post('/hr/new/offer', data=bad).status_code == 200
EXP = dict(issue_date='2026-11-02', employee_full_name='Priya Ramesh', designation='Senior Admissions Counsellor', office_location='Coimbatore', date_of_joining='2024-03-15', date_of_leaving='2026-10-31',
           key_responsibilities='student admissions counselling and parent engagement', reporting_manager='Arjun Krishnan, Head of Admissions', conduct_adjective_1='dedicated', conduct_adjective_2='collaborative',
           conduct_adjective_3='highly professional', last_drawn_ctc='7,20,000', authorized_signatory_name='Dr. Muruganandam', authorized_signatory_designation='Founder & Director')
assert hr.post('/hr/new/experience', data=dict(EXP, date_of_leaving='2023-01-01')).status_code == 200            # leaving before joining
assert hr.post('/hr/new/experience', data=dict(EXP, key_responsibilities='')).status_code == 200                # a required field
REL = dict(issue_date='2026-11-14', employee_full_name='Priya Ramesh', designation='Senior Admissions Counsellor', date_of_joining='2024-03-15', resignation_date='2026-10-15', last_working_day='2026-11-14',
           notice_period_served='30 days', handover_recipient='the HR team', authorized_signatory_name='Dr. Muruganandam', authorized_signatory_designation='Founder & Director')
assert hr.post('/hr/new/relieving', data=dict(REL, last_working_day='2026-10-01')).status_code == 200            # last working day before resignation
with app.app_context():
    assert HrLetter.query.count() == 1                                                                      # none of the invalid forms saved a letter
assert hr.post('/hr/new/experience', data=EXP).status_code == 302
assert hr.post('/hr/new/relieving', data=REL).status_code == 302
assert hr.post('/hr/new/experience', data=dict(EXP, employee_full_name='Karthik S', issue_date='2027-03-31')).status_code == 302       # FY 2026-27 still
assert hr.post('/hr/new/experience', data=dict(EXP, employee_full_name='Meena R', issue_date='2027-04-02')).status_code == 302          # new FY: serial restarts
with app.app_context():
    refs = {r.person_name: r.ref_no for r in HrLetter.query.all()}
    assert refs['Karthik S'] == 'EA/HR/EXP/2026/0002' and refs['Meena R'] == 'EA/HR/EXP/2027/0001', refs
    assert [r.ref_no for r in HrLetter.query.filter_by(kind='relieving')] == ['EA/HR/REL/2026/0001']
    assert len({r.ref_no for r in HrLetter.query.all()}) == HrLetter.query.count() == 5
    eid = HrLetter.query.filter_by(kind='experience').order_by(HrLetter.id).first().id
    rid = HrLetter.query.filter_by(kind='relieving').one().id
t = hr.get('/hr/letters/%d' % eid).get_data(as_text=True)
assert 'EXPERIENCE CERTIFICATE' in t and 'TO WHOMSOEVER IT MAY CONCERN' in t and 'dedicated, collaborative and highly professional' in t and 'INR 7,20,000' in t and '15 March 2024 to 31 October 2026' in t
t = hr.get('/hr/letters/%d' % rid).get_data(as_text=True)
assert 'RELIEVING LETTER' in t and 'Dear Priya,' in t and 'EA/HR/REL/2026/0001' in t and 'notice period of 30 days' in t and 'the HR team' in t
for i in (eid, rid):
    assert hr.get('/hr/letters/%d.pdf' % i).data[:4] == b'%PDF'

# copy to a new letter pre-fills the form
t = hr.get('/hr/new/offer?copy=%d' % OID).get_data(as_text=True)
assert 'Priya Ramesh' in t and '336000' in t and 'value="2026-12-01"' in t

# ---- register ------------------------------------------------------------------------------------------------------------------------------
t = hr.get('/hr/letters').get_data(as_text=True)
assert t.count('EA/HR/') >= 5 and 'Meena R' in t
assert 'Meena R' not in hr.get('/hr/letters?kind=offer').get_data(as_text=True) and 'Priya Ramesh' in hr.get('/hr/letters?kind=offer').get_data(as_text=True)
assert 'Karthik S' in hr.get('/hr/letters?q=karthik').get_data(as_text=True) and 'Meena R' not in hr.get('/hr/letters?q=karthik').get_data(as_text=True)
assert 'Meena R' in hr.get('/hr/letters?fy=2027').get_data(as_text=True) and 'Karthik S' not in hr.get('/hr/letters?fy=2027').get_data(as_text=True)
csv = hr.get('/hr/letters.csv')
body = csv.get_data(as_text=True)
assert csv.status_code == 200 and csv.mimetype == 'text/csv' and body.splitlines()[0].lstrip('﻿').startswith('Reference,Type') and 'EA/HR/OFFER/2026/0001' in body and 'Hira HR' in body

# ---- void ----------------------------------------------------------------------------------------------------------------------------------
assert hr.post('/hr/letters/%d/void' % OID, data={'reason': ''}, follow_redirects=True).status_code == 200
with app.app_context():
    assert db.session.get(HrLetter, OID).status == 'issued'                                                  # a reason is required
hr.post('/hr/letters/%d/void' % OID, data={'reason': 'Wrong joining date'})
with app.app_context():
    row = db.session.get(HrLetter, OID)
    assert row.status == 'void' and row.void_reason == 'Wrong joining date' and row.voided_by and row.voided_at
t = hr.get('/hr/letters/%d' % OID).get_data(as_text=True)
assert 'Wrong joining date' in t and 'hl-void' in t
assert hr.get('/hr/letters/%d.pdf' % OID).data[:4] == b'%PDF'
assert hr.post('/hr/new/offer', data=dict(OFFER, candidate_full_name='Next Candidate')).status_code == 302
with app.app_context():
    assert HrLetter.query.filter_by(person_name='Next Candidate').one().ref_no == 'EA/HR/OFFER/2026/0002'    # the voided number 0001 is not reused

# ---- templates -----------------------------------------------------------------------------------------------------------------------------------
t = hr.get('/hr/templates/experience').get_data(as_text=True)
assert 'EXPERIENCE CERTIFICATE' in t and 'Sample preview' in t and 'Priya Ramesh' in t
body = hl.DEFAULTS['experience'].replace('We wish {{employee_full_name}} the very best in all future endeavours.', 'We thank {{employee_full_name}} and wish them every success.')
bad = hr.post('/hr/templates/experience', data={'action': 'save', 'body': body + '\nHello {{salary_secret}}'})
assert bad.status_code == 200 and 'Unknown placeholder' in bad.get_data(as_text=True)
assert hr.post('/hr/templates/experience', data={'action': 'save', 'body': ''}).status_code == 200
assert hr.post('/hr/templates/experience', data={'action': 'save', 'body': body}).status_code == 302
with app.app_context():
    assert hl.template('experience').version == 2 and 'wish them every success' in hl.template('experience').body
assert hr.post('/hr/new/experience', data=dict(EXP, employee_full_name='After Edit')).status_code == 302
with app.app_context():
    after = HrLetter.query.filter_by(person_name='After Edit').one()
    assert after.template_version == 2
new_page = hr.get('/hr/letters/%d' % after.id).get_data(as_text=True)
old_page = hr.get('/hr/letters/%d' % eid).get_data(as_text=True)
assert 'wish them every success' in new_page and 'the very best in all future endeavours' in old_page         # an issued letter keeps the text it was issued with
hr.post('/hr/templates/experience', data={'action': 'reset'})
with app.app_context():
    assert hl.template('experience').version == 3 and hl.template('experience').body == hl.DEFAULTS['experience']

# ---- admin can give someone the HR Admin role ------------------------------------------------------------------------------------------------------
with app.app_context():
    fid = User.query.filter_by(email='f@t.test').one().id
r = adm.post('/admin/users/%d/update' % fid, data={'tier': 'hr_admin'}, follow_redirects=True)
with app.app_context():
    assert User.query.get(fid).tier == 'hr_admin'
c, _ = login('f@t.test')
assert c.get('/hr/').status_code == 200

low = hr.get('/hr/').get_data(as_text=True).lower()
assert 'office hours' not in low and 'working hours' not in low
print('hr letters checks passed')
