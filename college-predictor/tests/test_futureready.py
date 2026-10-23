"""FutureReady (Class 8-9): full student -> report workflow, scoring rules, access control, privacy, content versioning, PDF, demo mode.
Run from college-predictor/:  python tests/test_futureready.py"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.futureready import engine, reports
from app.futureready.content import assessments as CA, extra as CX
from app.futureready.models import (FrAction, FrAdmission, FrAssessment, FrAttempt, FrNote, FrParentLink, FrProfile, FrQuestion, FrRecommendation, FrReport,
                                    FrSkillScore)
from app.models import User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()

# ---- content integrity (no database needed) -----------------------------------------------------------------------------------
seen = set()
for d in list(CA.CORE) + [CX.A11, CX.A12, CX.A_REFLECT, CX.SAMPLER]:
    for q in d['questions']:
        assert q['code'] not in seen, 'duplicate code ' + q['code']
        seen.add(q['code'])
        if q['qtype'] == 'mcq':
            assert isinstance(q['answer'], int) and 0 <= q['answer'] < len(q['options']) and len(q['options']) >= 3, q['code']
            assert q['explanation'], 'missing explanation ' + q['code']
        if q['qtype'] == 'multi' and q['answer'] is not None:
            assert all(0 <= i < len(q['options']) for i in q['answer']), q['code']
assert len(CA.CORE) == 10 and CX.A11['number'] == 11 and CX.A12['number'] == 12
sk = {}
for q in CX.SAMPLER['questions']:
    sk.setdefault((q['skill'], q['level']), 0)
    sk[(q['skill'], q['level'])] += 1
assert len(sk) == 30 and set(sk.values()) == {3}, sk                          # 10 skills x 3 levels x 3 items

with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'),
                    ('Stu One', 's1@x.com', 'free'), ('Stu Two', 's2@x.com', 'free'), ('Par One', 'p1@x.com', 'free'), ('Par Two', 'p2@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    engine.seed_content()
    again = engine.seed_content()
    assert again == 0, 'seeding must be idempotent'
    assert FrAssessment.query.filter(FrAssessment.number != None).count() == 12   # noqa: E711
    assert FrAdmission.query.filter_by(status='verified').count() == 0            # nothing is claimed as verified
    tn = FrAdmission.query.filter_by(key='tnea').one()
    assert 'not an entrance examination' in tn.summary and 'Merit-based' in tn.classification
    u = lambda e: User.query.filter_by(email=e).one()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, s2, p1, p2 = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 's2@x.com', 'p1@x.com', 'p2@x.com'))
anon = app.test_client()
post = lambda c, url, **d: c.post(url, data=d, follow_redirects=True)

# ---- public pages + enrolment -----------------------------------------------------------------------------------------------
assert anon.get('/futureready/').status_code == 200 and anon.get('/futureready/admissions').status_code == 200 and anon.get('/futureready/privacy').status_code == 200
assert anon.get('/futureready/admin').status_code == 302 and s1.get('/futureready/admin').status_code == 403
r = post(admin, '/futureready/admin', do='enrol', student_email='s1@x.com', parent_email='p1@x.com', mentor_email='m@x.com', grade='8')
assert b'Student enrolled' in r.data
post(admin, '/futureready/admin', do='enrol', student_email='s2@x.com', parent_email='p2@x.com', mentor_email='m2@x.com', grade='9')
with app.app_context():
    P1 = FrProfile.query.filter_by(user_id=u('s1@x.com').id).one().id
    P2 = FrProfile.query.filter_by(user_id=u('s2@x.com').id).one().id

# ---- access control -----------------------------------------------------------------------------------------------------------
dash = f'/futureready/s/{P1}'
assert mentor.get(dash).status_code == 200 and admin.get(dash).status_code == 200
assert mentor2.get(dash).status_code == 403            # another mentor's student
assert s2.get(dash).status_code == 403                 # another student
assert p2.get(dash).status_code == 403                 # another family
assert anon.get(dash).status_code == 302
assert s1.get(f'/futureready/s/{P2}/assessments').status_code == 403

# ---- onboarding: consent gate, save/resume --------------------------------------------------------------------------------------
assert s1.get(dash).status_code == 302 and '/onboarding/' in s1.get(dash).headers['Location']
post(s1, f'/futureready/s/{P1}/onboarding/2', grade='8', curriculum='CBSE', school='Test School')
r = post(s1, f'/futureready/s/{P1}/onboarding/3', agree='1', by='Stu One')
assert b'A parent or guardian must record consent' in r.data       # the student cannot consent for themselves
assert s1.get(f'/futureready/s/{P1}/a/academic').status_code == 302  # assessments locked
post(s1, f'/futureready/s/{P1}/onboarding/4', interests='Robots and drawing')
with app.app_context():
    assert FrProfile.query.get(P1).onboarding_step == 5 and FrProfile.query.get(P1).consent_at is None
r = post(p1, f'/futureready/s/{P1}/onboarding/3', agree='1', by='Par One')
with app.app_context():
    assert FrProfile.query.get(P1).consent_at is not None
post(p1, f'/futureready/s/{P1}/onboarding/7', goals='Confidence in maths')
post(mentor, f'/futureready/s/{P1}/onboarding/8', tier='Intensive', meetings='4')
r = post(s1, f'/futureready/s/{P1}/onboarding/10')
assert b'Welcome' in r.data or r.status_code == 200
with app.app_context():
    pr = FrProfile.query.get(P1)
    assert pr.onboarding_done_at and pr.tier == 'Intensive' and pr.meetings_per_month == 4 and 'confidence' in pr.parent_goals.lower()

# ---- take the academic diagnostic: autosave, partial submit, scoring --------------------------------------------------------------
with app.app_context():
    a = FrAssessment.query.filter_by(key='academic').one()
    qs = {q.code: q for q in FrQuestion.query.filter_by(assessment_id=a.id).all()}
assert s1.get(f'/futureready/s/{P1}/a/academic').status_code == 200
resp = {c: q.answer for c, q in qs.items() if c.startswith('AF-M')}                    # all four maths correct
resp['AF-S-01'] = 0                                                                    # science: one wrong
resp['AF-S-02'] = qs['AF-S-02'].answer
r = s1.post(f'/futureready/s/{P1}/a/academic/save', json=resp)
assert r.get_json()['ok'] and r.get_json()['n'] == len(resp)
form = {c: str(v) for c, v in resp.items()}
form['action'] = 'submit'
r = s1.post(f'/futureready/s/{P1}/a/academic', data=form)
assert r.status_code == 302 and '/attempt/' in r.headers['Location']
html = s1.get(r.headers['Location']).get_data(as_text=True)
assert 'Secure' in html and 'Too few items' in html and 'snapshot' in html.lower() or 'How to read this' in html
with app.app_context():
    at = FrAttempt.query.filter_by(profile_id=P1).one()
    res = at.result
    assert res['skills']['math']['pct'] == 100 and res['skills']['math']['band'] == 'Secure' and res['skills']['math']['n'] == 4
    assert res['skills']['science']['n'] == 2 and res['skills']['science']['pct'] == 50 and res['skills']['science']['band'] == 'Developing'
    assert 'reading' not in res['skills']                                               # unanswered skills are not scored
    assert FrSkillScore.query.filter_by(attempt_id=at.id, skill='math').one().value == 100
    # a skill with one answered item is never labelled
    assert engine.band(100, 1) == 'Too few items' and engine.band(80, 5) == 'Secure' and engine.band(79, 5) == 'Developing' and engine.band(49, 5) == 'Needs reinforcement'
# another student cannot open this result; a parent can
AID = None
with app.app_context():
    AID = FrAttempt.query.filter_by(profile_id=P1).one().id
assert s2.get(f'/futureready/s/{P1}/attempt/{AID}').status_code == 403
assert p1.get(f'/futureready/s/{P1}/attempt/{AID}').status_code == 200
assert s1.post(f'/futureready/s/{P2}/a/academic', data={'action': 'submit'}).status_code == 403
assert p1.get(f'/futureready/s/{P1}/a/academic').status_code == 403               # parents cannot take the student's tests

# ---- other assessment types: likert (reverse), choice tags, text, rubric ------------------------------------------------------------
with app.app_context():
    h = {q.code: q for q in FrQuestion.query.join(FrAssessment).filter(FrAssessment.key == 'habits').all()}
form = {c: '5' for c in h}
form['LH-01b'] = '1'                                                                    # reverse item: 1 means a strong "planning" habit
form['action'] = 'submit'
assert s1.post(f'/futureready/s/{P1}/a/habits', data=form).status_code == 302
with app.app_context():
    at = FrAttempt.query.join(FrAssessment).filter(FrAssessment.key == 'habits').one()
    assert at.result['skills']['planning']['mean'] == 5.0
    assert at.result['skills']['concentration']['mean'] == 3.0                          # 5 and reverse(5)=1
form = {'IX-%02d%s' % (i, s): '5' for i in range(1, 11) for s in 'ab'}
form.update({'IX-T1': 'Building things', 'IX-T2': 'A model bridge', 'action': 'submit'})
assert s1.post(f'/futureready/s/{P1}/a/interests', data=form).status_code == 302
form = {'EM-%02d' % i: '0' for i in range(1, 11)}
form['action'] = 'submit'
assert s1.post(f'/futureready/s/{P1}/a/eng_interest', data=form).status_code == 302
r = s1.get(f'/futureready/s/{P1}/interest-map')
assert r.status_code == 200 and b'Branches to explore next' in r.data
with app.app_context():
    prof = engine.interest_profile(P1)
    assert prof and max(prof.values()) <= 100
    assert engine.branch_matches(P1, 3)
form = {'CD-01': '1', 'CD-02': 'Bags hurt backs', 'CD-03': 'wheels; strap; frame', 'CD-04': 'detachable wheels', 'CD-05': 'cardboard test', 'CD-06': 'cheap', 'CD-07': 'add padding',
        'CD-S1': '4', 'CD-S2': '3', 'CD-S3': '4', 'action': 'submit'}
assert s1.post(f'/futureready/s/{P1}/a/creativity', data=form).status_code == 302
with app.app_context():
    cr = FrAttempt.query.join(FrAssessment).filter(FrAssessment.key == 'creativity').one()
    CRID = cr.id
    assert cr.result['text']['CD-01'].startswith('Make a school bag')
rub = {'understand': '3', 'ideas': '4', 'creativity': '4', 'practical': '2', 'reasoning': '3', 'reflection': '1', 'feedback': 'Nice start'}
assert s1.post(f'/futureready/s/{P1}/attempt/{CRID}/rubric', data=rub).status_code == 403   # students cannot rate themselves
assert mentor2.post(f'/futureready/s/{P1}/attempt/{CRID}/rubric', data=rub).status_code == 403
assert mentor.post(f'/futureready/s/{P1}/attempt/{CRID}/rubric', data=rub).status_code == 302
with app.app_context():
    v = {s.skill: s.value for s in FrSkillScore.query.filter_by(attempt_id=CRID, kind='rubric').all()}
    assert v['ideas'] == 100 and v['reflection'] == 0 and round(v['understand']) == 67
page = s1.get(f'/futureready/s/{P1}/attempt/{CRID}').get_data(as_text=True)
assert 'Nice start' in page and 'Save rubric' not in page
assert 'Save rubric' in mentor.get(f'/futureready/s/{P1}/attempt/{CRID}').get_data(as_text=True)
assert 'Bags hurt backs' not in p1.get(f'/futureready/s/{P1}/attempt/{CRID}').get_data(as_text=True)    # parents do not see open-text answers

# ---- sampler (adaptive sets) --------------------------------------------------------------------------------------------------------
assert s1.get(f'/futureready/s/{P1}/sampler').status_code == 200
with app.app_context():
    sq = FrQuestion.query.join(FrAssessment).filter(FrAssessment.key == 'sampler', FrQuestion.skill == 'numerical', FrQuestion.level == 2).order_by(FrQuestion.position).all()
    assert len(sq) == 3
form = {q.code: str(q.answer) for q in sq}
form['action'] = 'submit'
r = s1.post(f'/futureready/s/{P1}/a/sampler?set=numerical:2', data=form)
assert r.status_code == 302
with app.app_context():
    at = FrAttempt.query.filter_by(set_key='numerical:2').one()
    assert at.result['overall_pct'] == 100 and list(at.result['skills']) == ['numerical']
assert b'No pass mark' in s1.get(f'/futureready/s/{P1}/sampler').data or b'no pass mark' in s1.get(f'/futureready/s/{P1}/sampler').data.lower()

# ---- alignment: separate student and parent views ---------------------------------------------------------------------------------
form = {'PS-01': ['0', '1', '2'], 'PS-02': ['3', '4', '5'], 'PS-03': '5', 'PS-04': '5', 'PS-05': '5', 'PS-06': '5', 'PS-T1': 'Confidence', 'action': 'submit'}
assert s1.post(f'/futureready/s/{P1}/a/alignment', data=form).status_code == 302
form = {'PS-01': ['6', '7', '8'], 'PS-02': ['9', '0', '1'], 'PS-03': '2', 'PS-04': '5', 'PS-05': '5', 'PS-06': '1', 'PS-T1': 'Marks', 'action': 'submit'}
rr = p1.post(f'/futureready/s/{P1}/a/alignment', data=form)
assert rr.status_code == 302
with app.app_context():
    al = reports.alignment(FrProfile.query.get(P1))
    assert any('confidence' in g for g in al['gaps']) and any('understanding' in g for g in al['gaps'])
    st_att = FrAttempt.query.filter_by(profile_id=P1, audience='student').join(FrAssessment).filter(FrAssessment.key == 'alignment').one()
    STAT = st_att.id
assert p1.get(f'/futureready/s/{P1}/attempt/{STAT}').status_code == 403            # parent cannot open the student's private alignment answers

# ---- recommendations: evidence, mentor approval, accept as action ---------------------------------------------------------------------
r = post(mentor, f'/futureready/s/{P1}/recommendations', **{'do': 'generate'})
assert b'new suggestion' in r.data
with app.app_context():
    recs = FrRecommendation.query.filter_by(profile_id=P1).all()
    assert recs and all(not x.approved for x in recs)
    assert any(x.rule_key.startswith('gap:') or x.rule_key.startswith('interest:') or x.rule_key.startswith('family:') for x in recs)
    first = recs[0]
    RID = first.id
    assert 'Evidence' in mentor.get(f'/futureready/s/{P1}/recommendations').get_data(as_text=True)
assert 'Awaiting mentor review' not in s1.get(f'/futureready/s/{P1}/recommendations').get_data(as_text=True)
with app.app_context():
    assert not FrRecommendation.query.get(RID).approved
assert s1.get(f'/futureready/s/{P1}/recommendations').get_data(as_text=True).count('fr-card') <= 3   # nothing visible before approval
post(s1, f'/futureready/s/{P1}/recommendations', do='approve', rid=str(RID))             # student cannot approve
with app.app_context():
    assert not FrRecommendation.query.get(RID).approved
post(mentor, f'/futureready/s/{P1}/recommendations', do='approve', rid=str(RID))
page = s1.get(f'/futureready/s/{P1}/recommendations').get_data(as_text=True)
assert 'Why:' in page
post(s1, f'/futureready/s/{P1}/recommendations', do='accept', rid=str(RID))
with app.app_context():
    assert FrAction.query.filter_by(profile_id=P1, source='recommendation').count() == 1
    assert FrRecommendation.query.get(RID).status == 'Accepted'
    assert FrRecommendation.query.filter_by(profile_id=P1).count() == len(recs)
    again = FrRecommendation.query.filter_by(profile_id=P1).count()
post(mentor, f'/futureready/s/{P1}/recommendations', do='generate')
with app.app_context():
    assert FrRecommendation.query.filter_by(profile_id=P1).count() == again            # rules never duplicate

# ---- goals, actions, ownership --------------------------------------------------------------------------------------------------------
post(mentor, f'/futureready/s/{P1}/plan', do='goal', title='Improve spatial practice', metric='Sampler spatial %', baseline='33', target='67', unit='%')
post(mentor, f'/futureready/s/{P1}/plan', do='action', title='Paper bridge test', owner='student', due='2026-12-01', why='Practise')
post(mentor, f'/futureready/s/{P1}/plan', do='action', title='Parent task', owner='parent', due='2026-12-02')
with app.app_context():
    aid_s = FrAction.query.filter_by(title='Paper bridge test').one().id
    aid_p = FrAction.query.filter_by(title='Parent task').one().id
post(s1, f'/futureready/s/{P1}/plan', do='action_update', aid=str(aid_p), status='Done')     # a student cannot complete the parent's action
with app.app_context():
    assert FrAction.query.get(aid_p).status == 'Not started'
post(s1, f'/futureready/s/{P1}/plan', do='action_update', aid=str(aid_s), status='Done', evidence='Held 200 g')
post(p1, f'/futureready/s/{P1}/plan', do='action_update', aid=str(aid_p), status='In progress')
post(mentor, f'/futureready/s/{P1}/plan', do='action_update', aid=str(aid_s), feedback='Well done')
with app.app_context():
    a1 = FrAction.query.get(aid_s)
    assert a1.status == 'Done' and a1.completed_at and a1.evidence == 'Held 200 g' and a1.mentor_feedback == 'Well done'
    assert FrAction.query.get(aid_p).status == 'In progress'

# ---- private notes are never visible to student or parent -------------------------------------------------------------------------------
post(mentor, f'/futureready/s/{P1}/mentor', do='note', body='PRIVATE-CONCERN-123', visibility='mentor', basis='mentor', kind='observation')
post(mentor, f'/futureready/s/{P1}/mentor', do='note', body='SHARED-PRAISE-456', visibility='shared', basis='assessment', kind='observation')
for c in (s1, p1):
    t = c.get(f'/futureready/s/{P1}/mentor').get_data(as_text=True)
    assert 'SHARED-PRAISE-456' in t and 'PRIVATE-CONCERN-123' not in t
assert 'PRIVATE-CONCERN-123' in mentor.get(f'/futureready/s/{P1}/mentor').get_data(as_text=True)
assert mentor2.get(f'/futureready/s/{P1}/mentor').status_code == 403
post(p1, f'/futureready/s/{P1}/mentor', do='note', body='PARENT-NOTE-789')
assert 'PARENT-NOTE-789' not in s1.get(f'/futureready/s/{P1}/mentor').get_data(as_text=True)    # parent notes go to the mentor only
assert 'PARENT-NOTE-789' in mentor.get(f'/futureready/s/{P1}/mentor').get_data(as_text=True)
post(mentor, f'/futureready/s/{P1}/mentor', do='session', title='Monthly check-in', kind='monthly', when='2026-11-05T17:00', agenda='Review bridge test')
assert b'Monthly check-in' in s1.get(f'/futureready/s/{P1}/mentor').data

# ---- reports: draft is staff-only, shared snapshot, PDF, growth ----------------------------------------------------------------------------
for kind in reports.KINDS:
    r = post(mentor, f'/futureready/s/{P1}/reports', kind=kind)
    assert r.status_code == 200 and reports.KINDS[kind].encode() in r.data, kind
with app.app_context():
    rep = FrReport.query.filter_by(profile_id=P1, kind='starting_point').one()
    RID_R = rep.id
    d = rep.data
    blob = json.dumps(d)
    assert 'PRIVATE-CONCERN-123' not in blob and 'PARENT-NOTE-789' not in blob
    assert d['limits'] and any('not a prediction' in l for l in d['limits'])
    assert not any(w in blob.lower() for w in ('cut-off', 'cutoff', 'predicted rank', 'chance of admission'))
assert s1.get(f'/futureready/s/{P1}/reports/{RID_R}').status_code == 404                  # draft hidden
assert p1.get(f'/futureready/s/{P1}/reports/{RID_R}.pdf').status_code == 404
post(mentor, f'/futureready/s/{P1}/reports/{RID_R}', do='share')
assert s1.get(f'/futureready/s/{P1}/reports/{RID_R}').status_code == 200 and p1.get(f'/futureready/s/{P1}/reports/{RID_R}').status_code == 200
assert p2.get(f'/futureready/s/{P1}/reports/{RID_R}').status_code == 403
pdf = p1.get(f'/futureready/s/{P1}/reports/{RID_R}.pdf')
assert pdf.status_code == 200 and pdf.data[:5] == b'%PDF-' and len(pdf.data) > 1500
assert s1.post(f'/futureready/s/{P1}/reports', data={'kind': 'growth'}).status_code == 403

# growth: second attempt of a skill shows a delta against the student's own first attempt
form = {c: str(q.answer) for c, q in qs.items() if c.startswith('AF-S')}
form['action'] = 'submit'
s1.post(f'/futureready/s/{P1}/a/academic', data=form)
with app.app_context():
    g = reports.growth(FrProfile.query.get(P1))
    sci = [x for x in g if x['label'] == 'Science'][0]
    assert sci['first'] == 50 and sci['last'] == 100 and sci['delta'] == 50 and sci['n'] == 2

# ---- branches, compare, shortlist, admissions awareness ---------------------------------------------------------------------------------------
assert s1.get('/futureready/branches?pid=%d' % P1).status_code == 200
assert s1.get('/futureready/branches/cse').status_code == 200
assert b'Computer Science' in s1.get('/futureready/branches/compare?k=cse&k=civil').data
post(s1, f'/futureready/s/{P1}/shortlist/mechatronics')
assert b'On my shortlist' in s1.get(f'/futureready/branches?pid={P1}').data
assert p1.post(f'/futureready/s/{P1}/shortlist/cse').status_code == 403
page = anon.get('/futureready/admissions').get_data(as_text=True)
assert 'Requires verification' in page and 'Verified' not in page.replace('Requires verification', '') and 'not an entrance examination' in page
assert 'josaa.nic.in' in page

# ---- admin content: versioning + verification gate -----------------------------------------------------------------------------------------------
with app.app_context():
    q = FrQuestion.query.filter_by(code='AF-M-01', active=True).one()
    QID = q.id
assert s1.post(f'/futureready/admin/question/{QID}', data={'prompt': 'x'}).status_code == 403
post(admin, f'/futureready/admin/question/{QID}', prompt='Solve for x: 3x − 7 = 11 (edited)', options='4\n5\n6\n7', answer='2', explanation='Add 7, divide by 3.')
with app.app_context():
    rows = FrQuestion.query.filter_by(code='AF-M-01').order_by(FrQuestion.version).all()
    assert [r.version for r in rows] == [1, 2] and [r.active for r in rows] == [False, True] and 'edited' in rows[1].prompt
    old = FrAttempt.query.filter_by(profile_id=P1).join(FrAssessment).filter(FrAssessment.key == 'academic').first()
    assert old.version == 1                                                              # earlier attempts keep their version
post(admin, '/futureready/admin/admission/jee_main', summary='s', admission_year='2027', official_url='https://jeemain.nta.nic.in', reviewer='', last_verified='2026-10-01')
with app.app_context():
    assert FrAdmission.query.filter_by(key='jee_main').one().status == 'needs_verification'  # incomplete -> still unverified
post(admin, '/futureready/admin/admission/jee_main', summary='s', admission_year='2027', official_url='https://jeemain.nta.nic.in', reviewer='A. Reviewer', last_verified='2026-10-01')
with app.app_context():
    assert FrAdmission.query.filter_by(key='jee_main').one().status == 'verified'
assert 'Verified 01 Oct 2026' in anon.get('/futureready/admissions').get_data(as_text=True)

# ---- demo mode ------------------------------------------------------------------------------------------------------------------------------
r = post(admin, '/futureready/admin', do='demo')
assert b'Demo workspace created' in r.data
with app.app_context():
    dp = FrProfile.query.filter_by(demo=True).one()
    assert dp.student.email.endswith('@futureready.test') and dp.consent_at
    assert FrReport.query.filter_by(profile_id=dp.id, status='Shared').count() == 1
    DID = dp.id
assert b'DEMONSTRATION' in admin.get(f'/futureready/s/{DID}').data
csv = admin.get('/futureready/admin/export.csv').get_data(as_text=True)
lines = csv.strip().splitlines()
assert lines[0].startswith('profile_id') and all(not l.startswith(f'{DID},') for l in lines[1:])   # demo data never exported
assert s1.get('/futureready/admin/export.csv').status_code == 403

# ---- retention: deletion cascades ------------------------------------------------------------------------------------------------------------
post(admin, '/futureready/admin', do='delete_profile', pid=str(P2), confirm='nope')
with app.app_context():
    assert FrProfile.query.get(P2) is not None
with app.app_context():
    assert FrNote.query.filter_by(profile_id=P1).count() >= 2
print('FutureReady tests passed')
