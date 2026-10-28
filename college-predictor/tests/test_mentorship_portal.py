"""Mentorship Portal — end-to-end acceptance checks on DEMO data (sqlite, hermetic).

Run from college-predictor/:  python tests/test_mentorship_portal.py
Covers the 22 acceptance workflows in MENTORSHIP_PORTAL.md (enrolment, 10+ sessions, weekly check-in,
action engine, KPIs, reviews, branch fit, preferences, parent view, isolation between students,
calendar source/verification, report + PDF, cancelled != completed, persistence).
"""
import io
import os
import sys
import tempfile
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.models_mentorship import (MsAction, MsAudit, MsEnrolment, MsEvent, MsKpi, MsMessage, MsParentLink,
                                   MsPrefEntry, MsPrefList, MsReport, MsReview, MsSession, MsCheckin)
from app.services import mentorship as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()


def mk(name, email, tier):
    u = User(name=name, email=email, tier=tier, password_hash=pw())
    db.session.add(u)
    return u


with app.app_context():
    db.create_all()
    mk('DEMO Admin', 'admin@demo.test', 'admin')
    mk('DEMO Mentor', 'mentor@demo.test', 'ea_mentor')
    mk('DEMO Other Mentor', 'mentor2@demo.test', 'ea_mentor')
    mk('DEMO Student One', 's1@demo.test', 'elite')
    mk('DEMO Student Two', 's2@demo.test', 'elite')
    mk('DEMO Free Student', 'free@demo.test', 'free')
    mk('DEMO Parent One', 'p1@demo.test', 'free')
    mk('DEMO Parent Two', 'p2@demo.test', 'free')
    db.session.commit()


def login(email):
    c = app.test_client()
    r = c.post('/login', data={'email': email, 'password': 'x'})
    assert r.status_code == 302, email
    return c


admin, mentor, mentor2 = login('admin@demo.test'), login('mentor@demo.test'), login('mentor2@demo.test')
s1, s2, free, p1, p2 = (login(e) for e in ('s1@demo.test', 's2@demo.test', 'free@demo.test', 'p1@demo.test', 'p2@demo.test'))
anon = app.test_client()


def post(c, url, **data):
    return c.post(url, data=data, follow_redirects=True)


def uid(email):
    with app.app_context():
        return User.query.filter_by(email=email).one().id


# ---- 0. access gates before anything exists ------------------------------------------------------------------
assert anon.get('/mentorship/').status_code in (302, 401)
assert b'not enrolled' in s1.get('/mentorship/').data
assert mentor.get('/mentorship/mentor').status_code == 200
assert s1.get('/mentorship/mentor').status_code in (302, 403)          # students never reach the mentor dashboard
assert s1.get('/mentorship/admin').status_code in (302, 403)

# ---- 1. admin loads the standard programme (10 sessions) and enrols a student ---------------------------------------------
r = post(admin, '/mentorship/admin/load-default')
assert b'10-session' in r.data
with app.app_context():
    from app.models_mentorship import MsProgramme
    prog = MsProgramme.query.filter_by(name='Grade 12 Engineering Mentorship').one()
    assert prog.templates.count() == 10 and prog.templates[0].title.startswith('Onboarding')
    pid = prog.id
r = post(admin, '/mentorship/admin/enrol', student_email='s1@demo.test', programme_id=pid, mentor_email='mentor@demo.test',
         start_date=str(svc.today()), extra_quota='1')
assert b'enrolled with 10 core sessions' in r.data
post(admin, '/mentorship/admin/enrol', student_email='s2@demo.test', programme_id=pid, mentor_email='mentor2@demo.test')
with app.app_context():
    e1 = MsEnrolment.query.filter_by(student_id=uid('s1@demo.test')).one()
    e2 = MsEnrolment.query.filter_by(student_id=uid('s2@demo.test')).one()
    E1, E2 = e1.id, e2.id
    assert e1.mentor.email == 'mentor@demo.test' and e1.sessions.count() == 10
post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='p1@demo.test', relation='Mother')
post(admin, '/mentorship/admin/parent', enrolment_id=E2, parent_email='p2@demo.test')

# non-EA-mentor cannot be assigned
r = post(admin, '/mentorship/admin/enrol', student_email='free@demo.test', programme_id=pid, mentor_email='s2@demo.test')
assert b'EA Mentor role' in r.data

# ---- 2/3. student sees the right journey -----------------------------------------------------------------------------------
home = s1.get('/mentorship/', follow_redirects=True)
assert home.status_code == 200 and b'Onboarding and Baseline Assessment' in home.data and b'0 of 10 core sessions' in home.data
sess = s1.get(f'/mentorship/e/{E1}/sessions').get_data(as_text=True)
assert 'Final Journey Review and Next Steps' in sess and 'Private mentor notes' not in sess      # staff-only form hidden
assert b'Mentor view' not in home.data

# ---- 4/5. mentor schedules session 1, adds an 11th session without code changes --------------------------------------------------
when = (svc.utcnow() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
with app.app_context():
    first = MsSession.query.filter_by(enrolment_id=E1, position=1).one().id
r = post(mentor, f'/mentorship/e/{E1}/sessions/{first}/update', status='Planned', title='Onboarding and Baseline Assessment',
         planned_at=when, duration_min='60', shared_summary='Welcome!', mentor_notes='PRIVATE-NOTE-XYZ', parent_visible='1')
assert b'Session saved' in r.data
assert b'Welcome!' in s1.get(f'/mentorship/e/{E1}/sessions').data and b'PRIVATE-NOTE-XYZ' not in s1.get(f'/mentorship/e/{E1}/sessions').data
assert b'PRIVATE-NOTE-XYZ' not in p1.get(f'/mentorship/e/{E1}/sessions').data
r = post(mentor, f'/mentorship/e/{E1}/sessions/add', title='Extra: mock debrief', kind='extra', agenda='Debrief', duration_min='45')
assert b'Extra session added' in r.data
r = post(mentor, f'/mentorship/e/{E1}/sessions/add', title='Second extra', kind='extra')           # quota is 1
assert b'all are used' in r.data
r = post(admin, f'/mentorship/e/{E1}/sessions/add', title='Admin override intervention', kind='intervention')
assert b'Extra session added' in r.data
with app.app_context():
    assert MsSession.query.filter_by(enrolment_id=E1).count() == 12 and MsSession.query.filter_by(enrolment_id=E1, kind='core').count() == 10

# admin adds an 11th CORE session to the programme template; a new enrolment gets it
post(admin, f'/mentorship/admin/programme/{pid}/session', title='Parent Q&A', topics='Questions', deliverable='Notes')
with app.app_context():
    assert MsProgramme.query.get(pid).templates.count() == 11

# ---- 19. cancelled never counts as completed; planned vs actual dates separate -------------------------------------------
with app.app_context():
    ids = [s.id for s in MsSession.query.filter_by(enrolment_id=E1, kind='core').order_by(MsSession.position)]
post(mentor, f'/mentorship/e/{E1}/sessions/{ids[0]}/update', status='Completed', title='Onboarding and Baseline Assessment', planned_at=when)
post(mentor, f'/mentorship/e/{E1}/sessions/{ids[1]}/update', status='Cancelled', title='Personal Study Strategy')
with app.app_context():
    st = svc.session_stats(db.session.get(MsEnrolment, E1))
    assert st['core_done'] == 1 and st['core_total'] == 9 and st['cancelled'] == 1       # cancelled leaves the denominator
    s_ = db.session.get(MsSession, ids[0])
    assert s_.actual_at is not None and s_.planned_at is not None and s_.actual_at != s_.planned_at
    assert db.session.get(MsSession, ids[1]).actual_at is None

# ---- 6/7/8. weekly action plan + check-in + review ----------------------------------------------------------------------------
yesterday = str(svc.today() - timedelta(days=1))
r = post(mentor, f'/mentorship/e/{E1}/actions/add', title='Finish Physics chapter 3', purpose='Core mechanics base', priority='High',
         due_date=str(svc.today() + timedelta(days=2)), session_id=ids[0], parent_visible='1')
assert b'Action added' in r.data
post(mentor, f'/mentorship/e/{E1}/actions/add', title='Overdue sample task', due_date=yesterday, parent_visible='1')
post(mentor, f'/mentorship/e/{E1}/actions/add', title='Mentor-only prep', owner='mentor', parent_visible='0')
with app.app_context():
    a1 = MsAction.query.filter_by(title='Finish Physics chapter 3').one()
    a2 = MsAction.query.filter_by(title='Overdue sample task').one()
    A1, A2 = a1.id, a2.id
    assert svc.action_state(a2) == 'Overdue' and svc.action_state(a1) in ('Due soon', 'Open')
    # session completion is independent of action completion
    assert db.session.get(MsSession, ids[0]).status == 'Completed' and a1.status == 'Not Started'

# a student cannot touch another student's action, or a mentor-owned one
assert s2.post(f'/mentorship/e/{E1}/actions/{A1}/update', data={'status': 'Completed'}).status_code == 404
with app.app_context():
    mine = MsAction.query.filter_by(title='Mentor-only prep').one().id
assert s1.post(f'/mentorship/e/{E1}/actions/{mine}/update', data={'status': 'Completed'}).status_code == 403

weekly = s1.get(f'/mentorship/e/{E1}/weekly').get_data(as_text=True)
assert 'Finish Physics chapter 3' in weekly and 'Weekly check-in' in weekly
r = post(s1, f'/mentorship/e/{E1}/checkin', confidence='2', went_well='Revised optics', difficult='Rotational motion',
         barriers='Too many mocks', help_needed='Need a plan', next_priority='Rotation', **{f'out_{A1}': 'completed', f'out_{A2}': 'blocked'}, submit='1')
assert b'submitted to your mentor' in r.data
with app.app_context():
    assert db.session.get(MsAction, A1).status == 'Completed' and db.session.get(MsAction, A1).completed_at          # 8. pending → completed
    assert db.session.get(MsAction, A2).status == 'Blocked'
    assert svc.action_stats(db.session.get(MsEnrolment, E1))['done'] == 1
assert b'Already submitted' not in s1.get(f'/mentorship/e/{E1}/weekly').data
assert b'Submitted' in s1.get(f'/mentorship/e/{E1}/weekly').data
draft_again = post(s1, f'/mentorship/e/{E1}/checkin', confidence='5', submit='0')
assert b'already submitted' in draft_again.data

# mentor reviews the check-in; attention reasons appear (blocked + low confidence)
with app.app_context():
    cid = MsCheckin.query.filter_by(enrolment_id=E1).one().id
    level, reasons = svc.attention(db.session.get(MsEnrolment, E1))
    assert level in ('watch', 'attention') and any('Low confidence' in x for x in reasons)
r = post(mentor, f'/mentorship/e/{E1}/checkin/{cid}/review', mentor_comment='Good honesty. Let us cut mocks to 1/week.',
         parent_summary='Working on a balanced plan.', share_parent='1')
assert b'Review saved' in r.data
assert b'cut mocks' in s1.get(f'/mentorship/e/{E1}/weekly').data
pw_ = p1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)
assert 'Working on a balanced plan.' in pw_ and 'Rotational motion' not in pw_ and 'Too many mocks' not in pw_   # reflections stay private
assert p1.get(f'/mentorship/e/{E1}/weekly').status_code == 404                                          # parents have no weekly tab
# mentor re-prioritises: new deadline + feedback
post(mentor, f'/mentorship/e/{E1}/actions/{A2}/update', status='In Progress', due_date=str(svc.today() + timedelta(days=5)),
     mentor_feedback='Moved by 5 days', priority='Medium')
with app.app_context():
    a = db.session.get(MsAction, A2)
    assert a.status == 'In Progress' and a.mentor_feedback == 'Moved by 5 days'

# ---- 9. KPIs: create, baseline, target, update; effort vs outcome ---------------------------------------------------------------------
r = post(mentor, f'/mentorship/e/{E1}/kpis/add', name='Weekly revision target completion', category='Preparation', direction='higher',
         unit='%', baseline='40', target='90', method='Planner review', frequency='Weekly')
assert b'KPI added' in r.data
post(mentor, f'/mentorship/e/{E1}/kpis/add', name='Mock-test percentage (outcome)', category='Performance', direction='higher', unit='%', baseline='55', target='75')
post(mentor, f'/mentorship/e/{E1}/kpis/add', name='Silly-mistake rate', category='Performance', direction='lower', unit='%', baseline='20', target='8')
with app.app_context():
    k1 = MsKpi.query.filter_by(name='Weekly revision target completion').one()
    k2 = MsKpi.query.filter_by(name='Mock-test percentage (outcome)').one()
    k3 = MsKpi.query.filter_by(name='Silly-mistake rate').one()
    K1, K3 = k1.id, k3.id
    assert k2.outcome_metric and not k1.outcome_metric
    assert svc.kpi_view(k1)['current'] == 40
post(mentor, f'/mentorship/e/{E1}/kpis/{K1}/observe', value='65', note='Week 3 planner')
post(mentor, f'/mentorship/e/{E1}/kpis/{K3}/observe', value='14')
with app.app_context():
    v = svc.kpi_view(db.session.get(MsKpi, K1))
    assert v['current'] == 65 and v['trend'] == 'up' and v['pct'] == 50 and v['status'] == 'On track'
    v3 = svc.kpi_view(db.session.get(MsKpi, K3))
    assert v3['trend'] == 'down' and v3['improving'] is True and v3['pct'] == 50
assert s1.post(f'/mentorship/e/{E1}/kpis/add', data={'name': 'x'}).status_code == 403                      # students cannot create KPIs
assert b'Weekly revision target completion' in p1.get(f'/mentorship/e/{E1}/kpis').data

# ---- 10. quarterly review pre-populates and moves through the workflow -----------------------------------------------------------
r = post(mentor, f'/mentorship/e/{E1}/reviews/new', label='Quarter 1')
assert b'pre-filled' in r.data
with app.app_context():
    rv = MsReview.query.filter_by(enrolment_id=E1).one()
    snap = svc.jload(rv.snapshot_json)
    assert snap['sessions']['core_done'] == 1 and snap['actions']['total'] >= 3 and len(snap['kpis']) == 3 and snap['checkins_submitted'] == 1
    RV = rv.id
post(mentor, f'/mentorship/e/{E1}/reviews/{RV}/update', status='Awaiting input', parent_requested='1', strengths='Honest reflection')
assert b'Your mentor is preparing this review' in s1.get(f'/mentorship/e/{E1}/reviews').data
assert b'Your mentor is preparing this review' in p1.get(f'/mentorship/e/{E1}/reviews').data
post(s1, f'/mentorship/e/{E1}/reviews/{RV}/input', text='I want to improve rotation')
post(p1, f'/mentorship/e/{E1}/reviews/{RV}/input', text='Please focus on rest too')
with app.app_context():
    rv = db.session.get(MsReview, RV)
    assert rv.student_reflection and rv.parent_feedback
assert p2.post(f'/mentorship/e/{E1}/reviews/{RV}/input', data={'text': 'hack'}).status_code == 404
post(mentor, f'/mentorship/e/{E1}/reviews/{RV}/update', status='Finalised', strengths='Honest reflection', next_targets='Hit 90% revision')
assert b'Honest reflection' not in s1.get(f'/mentorship/e/{E1}/reviews').data              # finalised ≠ shared
post(mentor, f'/mentorship/e/{E1}/reviews/{RV}/update', status='Shared', strengths='Honest reflection', next_targets='Hit 90% revision',
     next_review_date=str(svc.today() + timedelta(days=90)))
assert b'Hit 90% revision' in s1.get(f'/mentorship/e/{E1}/reviews').data and b'Hit 90% revision' in p1.get(f'/mentorship/e/{E1}/reviews').data

# ---- 11. branch fit ------------------------------------------------------------------------------------------------------------------
assert b'Computer Science and Engineering' in s1.get(f'/mentorship/e/{E1}/branch').data
post(s1, f'/mentorship/e/{E1}/branch/profile', interests='Robots, coding', career_areas='Software', openness='4',
     w_interest='3', w_readiness='1', w_feasibility='1', w_family='1', submit='1')
post(s1, f'/mentorship/e/{E1}/branch/rate', branch='Computer Science and Engineering', interest='5', family='4', student_note='Love it')
post(mentor, f'/mentorship/e/{E1}/branch/rate', branch='Computer Science and Engineering', readiness='3', feasibility='2', mentor_note='Rank-dependent')
post(p1, f'/mentorship/e/{E1}/branch/rate', branch='Mechanical Engineering', family='2', family_concern='Prefers software')
bpage = mentor.get(f'/mentorship/e/{E1}/branch').get_data(as_text=True)
assert 'Rank-dependent' in bpage and 'Prefers software' in bpage and 'Submitted' in bpage
assert 'Σ(weight × rating)' in bpage                                                         # transparent methodology, not an opaque score
assert s1.post(f'/mentorship/e/{E1}/branch/profile', data={'mentor_summary': 'x'}).status_code in (200, 302)
with app.app_context():
    from app.models_mentorship import MsBranchRating
    r_ = MsBranchRating.query.filter_by(enrolment_id=E1, branch='Computer Science and Engineering').one()
    assert (r_.interest, r_.readiness, r_.feasibility, r_.family) == (5, 3, 2, 4)           # four dimensions stored separately

# ---- 12. college preferences / choice-filling ----------------------------------------------------------------------------------------
post(s1, f'/mentorship/e/{E1}/prefs/list/new', name='DEMO JoSAA draft')
with app.app_context():
    L = MsPrefList.query.filter_by(enrolment_id=E1).one().id
post(s1, f'/mentorship/e/{E1}/prefs/{L}/entry/add', college='DEMO College A', branch='CSE', route='JoSAA', tier='Target', interest='5')
post(s1, f'/mentorship/e/{E1}/prefs/{L}/entry/add', college='DEMO College B', branch='ECE', route='JoSAA', tier='Backup')
with app.app_context():
    xs = [x.id for x in MsPrefList.query.get(L).entries]
post(s1, f'/mentorship/e/{E1}/prefs/entry/{xs[1]}/move', dir='up')
with app.app_context():
    assert [x.college for x in MsPrefList.query.get(L).entries.order_by(MsPrefEntry.position)] == ['DEMO College B', 'DEMO College A']
post(mentor, f'/mentorship/e/{E1}/prefs/entry/{xs[0]}/update', mentor_reco='Good target', review_status='Reviewed', eligibility='Needs verification',
     data_note='Closing rank 4200', data_year='2025', data_source='JoSAA official')
ppage = mentor.get(f'/mentorship/e/{E1}/prefs').get_data(as_text=True)
assert 'Good target' in ppage and '2025' in ppage and 'JoSAA official' in ppage and 'does not submit choices' in ppage
post(p1, f'/mentorship/e/{E1}/prefs/entry/{xs[0]}/update', parent_comment='We like this one')
assert b'We like this one' in s1.get(f'/mentorship/e/{E1}/prefs').data
# status rules: parent can only approve; student cannot self-mark "Ready for official portal entry"
assert p1.post(f'/mentorship/e/{E1}/prefs/{L}/status', data={'status': 'Mentor review pending'}).status_code == 403
assert s1.post(f'/mentorship/e/{E1}/prefs/{L}/status', data={'status': 'Ready for official portal entry'}).status_code == 403
post(p1, f'/mentorship/e/{E1}/prefs/{L}/status', status='Approved by family', is_final='1')
post(mentor, f'/mentorship/e/{E1}/prefs/{L}/status', status='Ready for official portal entry')
with app.app_context():
    lst = MsPrefList.query.get(L)
    assert lst.is_final and lst.status == 'Ready for official portal entry'
    assert MsAudit.query.filter(MsAudit.enrolment_id == E1, MsAudit.action.like('pref.%')).count() >= 6      # change history kept

# ---- 17. calendar: sources + verification, programme template events ------------------------------------------------------------------------
post(admin, '/mentorship/admin/event', programme_id=pid, title='DEMO JEE Main Session 1', category='JEE Main',
     starts_on=str(svc.today() + timedelta(days=10)), source='https://jeemain.nta.nic.in', verified_on=str(svc.today()))
post(admin, '/mentorship/admin/event', programme_id=pid, title='DEMO Board practical', category='Board exam', starts_on=str(svc.today() + timedelta(days=12)))
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert 'DEMO JEE Main Session 1' in cal and 'jeemain.nta.nic.in' in cal and 'Verified' in cal
assert 'DEMO Board practical' in cal and 'unverified' in cal
assert 'Finish Physics chapter 3' in cal                                                         # task due dates appear
assert 'DEMO JEE Main Session 1' in s2.get(f'/mentorship/e/{E2}/calendar').get_data(as_text=True)
with app.app_context():
    level, reasons = svc.attention(db.session.get(MsEnrolment, E1))
    assert any('Exam within' in r for r in reasons)                                                  # exam soon + open actions → attention rule

# ---- 15. messages: private notes stay private -----------------------------------------------------------------------------------------------
post(mentor, f'/mentorship/e/{E1}/messages/post', audience='internal', body='INTERNAL-ONLY-NOTE')
post(mentor, f'/mentorship/e/{E1}/messages/post', audience='student', body='Hello student')
post(mentor, f'/mentorship/e/{E1}/messages/post', audience='parent', body='Hello parent')
post(mentor, f'/mentorship/e/{E1}/messages/post', audience='all', body='Holiday notice', announcement='1')
post(s1, f'/mentorship/e/{E1}/messages/post', body='Question from student')
stud = s1.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
par = p1.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
assert 'Hello student' in stud and 'Holiday notice' in stud and 'INTERNAL-ONLY-NOTE' not in stud and 'Hello parent' not in stud
assert 'Hello parent' in par and 'Holiday notice' in par and 'INTERNAL-ONLY-NOTE' not in par and 'Question from student' not in par
assert 'INTERNAL-ONLY-NOTE' in mentor.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
assert b'not connected' in mentor.post(f'/mentorship/e/{E1}/messages/post', data={'body': 'x'}, follow_redirects=True).data   # no fake delivery claims

# ---- 13/14/15/16. isolation ------------------------------------------------------------------------------------------------------------------
for tab in ('home', 'sessions', 'weekly', 'kpis', 'messages', 'reports', 'prefs'):
    assert s2.get(f'/mentorship/e/{E1}/{tab}').status_code == 404, tab                           # student ≠ other student
    assert p2.get(f'/mentorship/e/{E1}/{tab}').status_code == 404, tab                           # parent ≠ unrelated student
    assert mentor2.get(f'/mentorship/e/{E1}/{tab}').status_code == 404, tab                      # mentor ≠ unassigned student
    assert free.get(f'/mentorship/e/{E1}/{tab}').status_code == 404, tab
    assert anon.get(f'/mentorship/e/{E1}/{tab}').status_code in (302, 401), tab
assert mentor.get(f'/mentorship/e/{E2}/home').status_code == 404
assert admin.get(f'/mentorship/e/{E2}/home').status_code == 200                                   # administrators can open any record
assert p1.get(f'/mentorship/e/{E1}/history').status_code == 404 and s1.get(f'/mentorship/e/{E1}/history').status_code == 404
assert mentor.get(f'/mentorship/e/{E1}/history').status_code == 200
assert s2.post(f'/mentorship/e/{E1}/sessions/add', data={'title': 'x'}).status_code == 404
assert s1.post(f'/mentorship/e/{E1}/sessions/add', data={'title': 'x'}).status_code == 403
assert p1.post(f'/mentorship/e/{E1}/reports/generate').status_code == 403
# mentor dashboards only list their own students
md = mentor.get('/mentorship/mentor').get_data(as_text=True)
assert 'DEMO Student One' in md and 'DEMO Student Two' not in md
assert 'DEMO Student Two' in admin.get('/mentorship/mentor').get_data(as_text=True)
for f in ('upcoming', 'document', 'followup', 'overdue', 'attention', 'review', 'parent_report', 'checkin_review', 'deadline'):
    assert mentor.get(f'/mentorship/mentor?f={f}').status_code == 200
# a lapsed (free) student account is gated by Premium
with app.app_context():
    u = User.query.filter_by(email='s2@demo.test').one()
    u.tier = 'free'
    db.session.commit()
assert s2.get(f'/mentorship/e/{E2}/home').status_code == 403
with app.app_context():
    u = User.query.filter_by(email='s2@demo.test').one()
    u.tier = 'elite'
    db.session.commit()

# ---- 18. report: missing data labelled, review → approve → share, PDF ----------------------------------------------------------------------------
post(mentor, f'/mentorship/e/{E1}/reports/generate')
with app.app_context():
    rep = MsReport.query.filter_by(enrolment_id=E1).one()
    RP = rep.id
    d = svc.jload(rep.data_json)
    assert d['snapshot']['sessions']['cancelled'] == 1 and d['preferences']['list'] == 'DEMO JoSAA draft'
assert s1.get(f'/mentorship/e/{E1}/reports/{RP}').status_code == 404                              # drafts are staff-only
view = mentor.get(f'/mentorship/e/{E1}/reports/{RP}').get_data(as_text=True)
assert 'Not recorded' in view and 'does not guarantee' in view
assert b'not available' in post(mentor, f'/mentorship/e/{E1}/reports/{RP}/share').data           # must approve first
post(mentor, f'/mentorship/e/{E1}/reports/{RP}/approve')
post(mentor, f'/mentorship/e/{E1}/reports/{RP}/share')
assert s1.get(f'/mentorship/e/{E1}/reports/{RP}').status_code == 200 and p1.get(f'/mentorship/e/{E1}/reports/{RP}').status_code == 200
assert p2.get(f'/mentorship/e/{E1}/reports/{RP}').status_code == 404
pdf = s1.get(f'/mentorship/e/{E1}/reports/{RP}.pdf')
if pdf.mimetype == 'application/pdf':
    assert pdf.data[:4] == b'%PDF' and len(pdf.data) > 1500
    print('  pdf generated:', len(pdf.data), 'bytes')
else:
    print('  (reportlab not installed — PDF falls back to print view)')

# ---- 20/21. member hub tile + persistence -------------------------------------------------------------------------------------------------------
hub = s1.get('/member-home').get_data(as_text=True)
assert 'Mentorship Portal' in hub and '/mentorship/' in hub
assert b'Mentor dashboard' not in s1.get('/member-home').data and b'Mentor dashboard' in mentor.get('/member-home').data
assert free.get('/member-home').get_data(as_text=True).count('is-locked') >= 1
assert s1.get('/static/css/mentorship.css').status_code == 200
with app.app_context():
    db.session.remove()
    db.engine.dispose()
    assert MsSession.query.filter_by(enrolment_id=E1).count() == 12 and MsAction.query.filter_by(enrolment_id=E1).count() == 3

# ---- exam catalogue: follow, share (.ics / email), new-exam and schedule-change alerts -------------------------------------------------
from app.services import mailer as _mailer, exam_calendar as xc
from app.models_mentorship import MsExam, MsExamFocus, MsAlert
post(admin, '/mentorship/admin/exams/load-default')
with app.app_context():
    assert MsExam.query.count() >= 20 and MsAlert.query.count() == 0               # starter list is a seed, not news
    uceed = MsExam.query.filter_by(name='UCEED 2027').one().id
    jee1 = MsExam.query.filter_by(name='JEE Main 2027 — Session 1').one().id
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert 'Choose the exams to focus on' in cal and 'UCEED 2027' in cal and 'Confirmed' in cal and 'Tentative' in cal
assert 'Add to Google Calendar' in cal and 'Email delivery is not configured' in cal       # honest about email not being set up
filtered = s1.get(f'/mentorship/e/{E1}/calendar?q=nata').get_data(as_text=True).split('Exams you can follow')[1].split('Share the calendar')[0]
assert 'UCEED 2027' not in filtered and 'NATA 2027' in filtered
# follow: student and mentor can, parent/stranger cannot
assert b'Follow at least one exam' in s1.get(f'/mentorship/e/{E1}/calendar.ics', follow_redirects=True).data
post(s1, f'/mentorship/e/{E1}/exams/{uceed}/focus', on='1')
post(mentor, f'/mentorship/e/{E1}/exams/{jee1}/focus', on='1')
assert p1.post(f'/mentorship/e/{E1}/exams/{uceed}/focus', data={'on': '1'}).status_code == 403
assert p2.post(f'/mentorship/e/{E1}/exams/{uceed}/focus', data={'on': '1'}).status_code == 404
assert mentor2.post(f'/mentorship/e/{E1}/exams/{uceed}/focus', data={'on': '1'}).status_code == 404
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert cal.count('✓ Following') == 2 and '2 exam(s) you follow' in cal
agenda = cal.split('Add to calendar')[0]
assert 'JEE Main 2027 — Session 1' in agenda and 'January 2027' in agenda                 # followed exams join the agenda
assert '✓ Following' in p1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True) or 'Followed' in p1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
# .ics
ics = s1.get(f'/mentorship/e/{E1}/calendar.ics')
body = ics.data.decode()
assert ics.mimetype == 'text/calendar' and body.startswith('BEGIN:VCALENDAR') and body.count('BEGIN:VEVENT') == 2
assert 'DTSTART;VALUE=DATE:20270117' in body and 'DTEND;VALUE=DATE:20270118' in body and f'UID:exam-{uceed}@eduaakashaa.com' in body
assert 'STATUS:CONFIRMED' in body and 'STATUS:TENTATIVE' in body and 'SEQUENCE:0' in body
assert p1.get(f'/mentorship/e/{E1}/calendar.ics').status_code == 200 and p2.get(f'/mentorship/e/{E1}/calendar.ics').status_code == 404
assert s1.get(f'/mentorship/e/{E1}/exams/{uceed}.ics').data.count(b'BEGIN:VEVENT') == 1
# email the invite: refuses honestly when not configured, then sends with an .ics attachment from info@ (rate-limited)
assert b'not configured' in post(s1, f'/mentorship/e/{E1}/calendar/email', email='me@personal.test').data
_sent2, _orig = [], (_mailer.is_configured, _mailer.send_async, _mailer.send_bulk)
_mailer.is_configured = lambda: True
_mailer.send_async = lambda to, subject, text, html=None, **k: _sent2.append({'to': to, 'subject': subject, **k})
_bulk = []
_mailer.send_bulk = lambda rec, subject, text, html=None, **k: (_bulk.append({'rec': list(rec), 'subject': subject, **k}), len(list(rec)))[1]
assert b'valid email' in post(s1, f'/mentorship/e/{E1}/calendar/email', email='nope').data
assert b'queued to me@personal.test' in post(s1, f'/mentorship/e/{E1}/calendar/email', email='me@personal.test').data
m_ = _sent2[0]
assert m_['to'] == 'me@personal.test' and m_['from_addr'] == 'info@eduaakashaa.com'
assert m_['attachments'][0][0].endswith('.ics') and m_['attachments'][0][2] == 'text/calendar' and b'BEGIN:VEVENT' in m_['attachments'][0][1]
for _ in range(4):
    post(s1, f'/mentorship/e/{E1}/calendar/email', email='me@personal.test')
assert b'several invitations' in post(s1, f'/mentorship/e/{E1}/calendar/email', email='me@personal.test').data      # 6th in an hour blocked
assert len(_sent2) == 5

# new exam → alert for everyone with a mentorship role (and an email from info@), with an "Add" action
r = post(admin, '/mentorship/admin/exams/save', name='DEMO Test Exam 2027', category='Admission deadline', stream='B.Tech/B.E.',
         starts_on='2027-03-05', ends_on='2027-03-06', status='Confirmed', source='https://example.test/notice', verified_on=str(svc.today()))
assert b'Alert posted' in r.data and b'email(s) queued from info@' in r.data
assert _bulk and set(_bulk[-1]['rec']) >= {'s1@demo.test', 'p1@demo.test', 'mentor@demo.test', 's2@demo.test', 'p2@demo.test', 'mentor2@demo.test'}
assert 'free@demo.test' not in _bulk[-1]['rec'] and _bulk[-1]['from_addr'] == 'info@eduaakashaa.com'
with app.app_context():
    demo = MsExam.query.filter_by(name='DEMO Test Exam 2027').one().id
for who, c, eid in (('student', s1, E1), ('parent', p1, E1), ('mentor', mentor, E1), ('student2', s2, E2)):
    page = c.get(f'/mentorship/e/{eid}/home').get_data(as_text=True)
    assert 'New exam added: DEMO Test Exam 2027' in page, who
assert 'New exam added' not in free.get('/member-home').get_data(as_text=True)
assert 'New exam added: DEMO Test Exam 2027' in mentor.get('/mentorship/mentor').get_data(as_text=True)
assert 'Add to my calendar' in s1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)
assert 'Add to my calendar' not in p1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)         # parents are alerted but cannot follow
with app.app_context():
    aid_new = MsAlert.query.filter_by(kind='new').one().id
r = post(s1, f'/mentorship/e/{E1}/exams/{demo}/focus', on='1', alert_id=str(aid_new))
assert b'Now following' in r.data
with app.app_context():
    assert MsExamFocus.query.filter_by(enrolment_id=E1, exam_id=demo).count() == 1
assert 'New exam added: DEMO Test Exam 2027' not in s1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)    # acted on → cleared for this user
assert 'New exam added: DEMO Test Exam 2027' in p1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)        # others still see it
post(p1, '/mentorship/alerts/read', alert_id=str(aid_new), next=f'/mentorship/e/{E1}/home')
assert 'New exam added: DEMO Test Exam 2027' not in p1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)

# schedule change → "changed" alert to everyone, with before → after; unchanged re-save is silent; ICS SEQUENCE bumps
_bulk.clear()
SAVE = dict(id=str(demo), name='DEMO Test Exam 2027', category='Admission deadline', stream='B.Tech/B.E.', source='https://example.test/notice',
            verified_on=str(svc.today()))
r = post(admin, '/mentorship/admin/exams/save', starts_on='2027-03-12', ends_on='2027-03-13', status='Tentative', **SAVE)
assert b'Alert posted' in r.data
with app.app_context():
    ch = MsAlert.query.filter_by(kind='changed').one()
    assert '05' in ch.detail and '12' in ch.detail and 'Confirmed → Tentative' in ch.detail
    assert db.session.get(MsExam, demo).version == 2
for c, eid in ((s1, E1), (p1, E1), (mentor, E1), (s2, E2)):
    assert 'Schedule change: DEMO Test Exam 2027' in c.get(f'/mentorship/e/{eid}/home').get_data(as_text=True)
assert 'You follow this exam' in s1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)
assert _bulk and 'Schedule change' in _bulk[-1]['subject']
assert 'SEQUENCE:1' in s1.get(f'/mentorship/e/{E1}/exams/{demo}.ics').get_data(as_text=True)         # calendar clients update the entry
_bulk.clear()
r = post(admin, '/mentorship/admin/exams/save', starts_on='2027-03-12', ends_on='2027-03-13', status='Tentative', **SAVE)
assert b'nobody was alerted' in r.data and not _bulk
# only admins manage the catalogue
assert s1.post('/mentorship/admin/exams/save', data={'name': 'x', 'starts_on': '2027-01-01'}).status_code in (302, 403)
assert mentor.post('/mentorship/admin/exams/save', data={'name': 'x', 'starts_on': '2027-01-01'}).status_code in (302, 403)
# removal → alert, gone from catalogue
post(admin, '/mentorship/admin/exams/save', starts_on='2027-03-12', status='Tentative', active='0', **{k: v for k, v in SAVE.items() if k != 'source'})
assert 'Exam removed: DEMO Test Exam 2027' in s1.get(f'/mentorship/e/{E1}/home').get_data(as_text=True)
assert 'DEMO Test Exam 2027' not in s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True).split('Exams you can follow')[1].split('Share the calendar')[0]
_mailer.is_configured, _mailer.send_async, _mailer.send_bulk = _orig

# ---- admin: link a parent who has no account yet (the account is created and emailed) --------------------------------------------------
from app.routes import admin_portal as _AP
_mails = []
_ap_orig = (_AP.send_async, _AP.mail_configured)
_AP.send_async = lambda to, subject, text, html=None, **k: _mails.append((to, subject, text))
import app.services.mailer as _ml
_ml_orig = _ml.is_configured
_ml.is_configured = lambda: True
_AP.mail_configured = lambda: True
nolink = post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='newparent@demo.test', relation='Father')
assert b'has no EduAakashaA account yet' in nolink.data and not _mails                         # clear message, nothing created
assert b'valid parent email' in post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='nope', create='1').data
assert b'not found' in post(admin, '/mentorship/admin/parent', enrolment_id='9999', parent_email='x@y.com', create='1').data
r = post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='NewParent@Demo.test', parent_name='Ravi Kumar', relation='Father', create='1')
assert b'Parent account created for newparent@demo.test and linked' in r.data and b'Login details were emailed' in r.data
assert len(_mails) == 1 and _mails[0][0] == 'newparent@demo.test' and 'Password' in _mails[0][2]
with app.app_context():
    npar = User.query.filter_by(email='newparent@demo.test').one()
    assert npar.name == 'Ravi Kumar' and npar.tier == 'free' and MsParentLink.query.filter_by(enrolment_id=E1, parent_id=npar.id).count() == 1
pw_sent = _mails[0][2].split('Password   : ')[1].split('\n')[0]
newp = app.test_client()
assert newp.post('/login', data={'email': 'newparent@demo.test', 'password': pw_sent}).status_code == 302   # the emailed password works
assert newp.get(f'/mentorship/e/{E1}/home').status_code == 200 and newp.get(f'/mentorship/e/{E2}/home').status_code == 404
assert b'already linked' in post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='newparent@demo.test', create='1').data
assert b'student' in post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='s1@demo.test', create='1').data.lower()   # not the student's own account
_AP.send_async, _AP.mail_configured = _ap_orig
_ml.is_configured = _ml_orig

# ---- parent onboarding assessment: invitation email is tied to the student; only the linked parent can answer ----------------------------
from app.routes import mentorship as _MR
from app.models_mentorship import MsParentAssessment
_sent = []
_mr_orig = (_MR.mailer.send_async, _MR.mailer.is_configured)
_MR.mailer.send_async = lambda to, subject, text, html=None, **k: _sent.append((to, subject, text, html))
_MR.mailer.is_configured = lambda: True
_AP.mail_configured = lambda: True
_AP.send_async = lambda *a, **k: None
r = post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='second@demo.test', parent_name='Sita Rao', relation='Mother', create='1')
assert b'assessment invitation was emailed' in r.data and len(_sent) == 1
to, subj, txt, html = _sent[0]
assert to == 'second@demo.test' and 'Parent assessment for' in subj
assert f'/mentorship/e/{E1}/parent-assessment' in txt and f'/mentorship/e/{E1}/home' in txt and 'www.eduaakashaa.com' in txt     # links are tied to this student
with app.app_context():
    sec = User.query.filter_by(email='second@demo.test').one()
    pa = MsParentAssessment.query.filter_by(enrolment_id=E1, parent_id=sec.id).one()
    assert pa.invited_at is not None and pa.submitted_at is None
sec_c = app.test_client()
# the new parent's temporary password is not in these mails; reset it to sign in for the test
with app.app_context():
    from app.extensions import bcrypt as _bc
    User.query.filter_by(email='second@demo.test').one().password_hash = _bc.generate_password_hash('x').decode()
    db.session.commit()
sec_c.post('/login', data={'email': 'second@demo.test', 'password': 'x'})
page = sec_c.get(f'/mentorship/e/{E1}/parent-assessment')
assert page.status_code == 200 and b'Parent onboarding assessment' in page.data
assert b'parent assessment' in sec_c.get(f'/mentorship/e/{E1}/home').data                        # dashboard nudge while pending
assert sec_c.get(f'/mentorship/e/{E2}/parent-assessment').status_code == 404                     # a different student: no access
ok = sec_c.post(f'/mentorship/e/{E1}/parent-assessment', data={'goals': 'Good CS seat', 'budget': '2–5 lakh', 'documents': ['Passport', 'bogus'], 'routes': 'JoSAA'})
assert ok.status_code == 302
with app.app_context():
    pa = MsParentAssessment.query.filter_by(enrolment_id=E1, parent_id=sec.id).one()
    import json as _j
    a = _j.loads(pa.answers)
    assert pa.submitted_at and a['goals'] == 'Good CS seat' and a['documents'] == ['Passport'] and a['budget'] == '2–5 lakh'
assert b'parent assessment' not in sec_c.get(f'/mentorship/e/{E1}/home').data.replace(b'Parent assessment', b'')     # nudge gone once submitted
assert b'Good CS seat' in admin.get(f'/mentorship/e/{E1}/parent-assessment').data                # staff can read it
st = app.test_client()
st.post('/login', data={'email': 's1@demo.test', 'password': 'x'})
assert st.get(f'/mentorship/e/{E1}/parent-assessment').status_code == 403                        # the student cannot see parent answers
assert b'assessment submitted' in admin.get('/mentorship/admin').data
with app.app_context():
    from app.models_mentorship import MsParentLink as _PL
    _lid = _PL.query.filter_by(enrolment_id=E1, parent_id=sec.id).one().id
n = len(_sent)
assert b'emailed to second@demo.test' in post(admin, '/mentorship/admin/parent/%d/invite' % _lid).data and len(_sent) == n + 1      # resend invite
assert app.test_client().get(f'/mentorship/e/{E1}/parent-assessment').status_code in (302, 401)
_MR.mailer.send_async, _MR.mailer.is_configured = _mr_orig

# rules are admin-editable
post(admin, '/mentorship/admin/rules', due_soon_days='5', overdue_attention='2', checkin_gap_days='14', low_confidence='1', exam_window_days='30')
with app.app_context():
    assert svc.rule('due_soon_days') == 5 and svc.rule('exam_window_days') == 30

try:
    os.unlink(_db)
except OSError:
    pass
print('all mentorship-portal checks passed')
