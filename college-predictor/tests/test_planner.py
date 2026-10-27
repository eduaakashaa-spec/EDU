"""Smart Study Planner: level rules, plan generation, progress statistics, access control, EduPulse links, reports and PDFs.
Run from college-predictor/:  python tests/test_planner.py"""
import os
import sys
import tempfile
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_planner import SpPlan, SpTask  # noqa: E402
from app.models_reinforce import RfAttempt, RfStudent  # noqa: E402
from app.services import planner as P  # noqa: E402
from app.services import reinforce as rf  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
B = '/study-planner'

# ---- quotes, quiz ---------------------------------------------------------------------------------------------------------------------------------
assert len(P.QUOTES) >= 30 and len(set(P.QUOTES)) == len(P.QUOTES)
assert P.quote_of_the_day(date(2026, 10, 27)) == P.quote_of_the_day(date(2026, 10, 27)) and P.quote_of_the_day(date(2026, 10, 27)) != P.quote_of_the_day(date(2026, 10, 28))
assert P.quote_of_the_week(date(2026, 10, 26))[1] == P.quote_of_the_week(date(2026, 11, 1))[1] and P.quote_of_the_week(date(2026, 10, 26))[1] != P.quote_of_the_week(date(2026, 11, 2))[1]
assert P.level_quiz([0, 0, 1, 0, 0]) == 'beginner' and P.level_quiz([1, 1, 1, 1, 2]) == 'average' and P.level_quiz([2, 2, 2, 2, 2]) == 'top'

with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'), ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Free Kid', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    rf.seed_taxonomy()
    uid = {u.email: u.id for u in User.query.all()}
    db.session.add(RfStudent(user_id=uid['s1@x.com'], mentor_id=uid['m@x.com'], exam='JEE', grade='12'))
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, s2, free = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 's2@x.com', 'f@x.com'))
anon = app.test_client()

# ---- plan generation: the three levels behave differently ------------------------------------------------------------------------------------------
start = date(2026, 11, 2)                                                       # a Monday
with app.app_context():
    u1 = db.session.get(User, uid['s1@x.com'])
    plans = {lv: P.generate_plan(u1, 'JEE', lv, start, 8, mentor_id=uid['m@x.com']) for lv in P.LEVELS}
    info = {}
    for lv, p in plans.items():
        ts = p.tasks.all()
        work = [t for t in ts if t.task_type != 'rest']
        day_min = {}
        for t in work:
            day_min[t.day] = day_min.get(t.day, 0) + (t.minutes or 0)
        info[lv] = {'mocks': sum(1 for t in ts if t.task_type == 'mock'), 'avg_day': sum(day_min.values()) / len(day_min), 'errors': sum(1 for t in ts if t.task_type == 'error'),
                    'rest': [t.day.weekday() for t in ts if t.task_type == 'rest'], 'days': len({t.day for t in ts}), 'learn': sum(t.minutes for t in ts if t.task_type == 'learn'),
                    'practice': sum(t.minutes for t in ts if t.task_type == 'practice'), 'chapters': len({t.chapter for t in ts if t.chapter})}
        assert set(info[lv]['rest']) == {6} and info[lv]['days'] == 56                      # every Sunday is a rest day; every day has something
        assert all(t.day >= start and t.minutes is not None for t in ts)
    b, a, t_ = info['beginner'], info['average'], info['top']
    assert b['avg_day'] < a['avg_day'] < t_['avg_day']                                      # harder levels plan more time per day
    assert b['mocks'] < a['mocks'] < t_['mocks'] and b['mocks'] >= 3                         # mock frequency grows with level
    assert b['errors'] == 0 and a['errors'] > 0 and t_['errors'] > a['errors']               # error log: none for beginners, more for top
    assert b['learn'] / (b['practice'] or 1) > t_['learn'] / (t_['practice'] or 1)           # beginners learn more, top scorers practise more
    assert b['chapters'] < t_['chapters']                                                    # top scorers cover more chapters in the same time
    # EduPulse links: practice tasks for a rostered JEE student open Reinforcement; mocks open the JEE mock centre; rest and learn tasks have no link
    ts = plans['average'].tasks.all()
    assert {t.link_kind for t in ts if t.task_type == 'practice'} == {'reinforce'} and {t.link_kind for t in ts if t.task_type == 'mock'} == {'jee_mock'}
    assert all(t.link_kind is None for t in ts if t.task_type in ('learn', 'rest'))
    # an exam date ends the plan and makes the last two weeks mock-heavy (not for beginners)
    u2 = db.session.get(User, uid['s2@x.com'])
    pe = P.generate_plan(u2, 'UCEED', 'top', start, 12, exam_date=start + timedelta(days=41))
    assert max(t.day for t in pe.tasks.all()) <= start + timedelta(days=41)
    last2 = [t for t in pe.tasks.all() if t.day > start + timedelta(days=27) and t.task_type == 'mock']
    early = [t for t in pe.tasks.all() if t.day <= start + timedelta(days=27) and t.task_type == 'mock']
    assert len(last2) > len(early) / 2 and {t.link_kind for t in pe.tasks.all() if t.task_type == 'practice'} == {'pulse'}
    pn = P.generate_plan(u2, 'NEET', 'average', start, 4)
    assert {t.subject for t in pn.tasks.all() if t.subject} == {'Physics', 'Chemistry', 'Biology'} and all(t.link_kind is None for t in pn.tasks.filter(SpTask.task_type == 'practice'))
    for p in (pe, pn):
        p.status = 'archived'
    for p in plans.values():
        p.status = 'archived'
    db.session.commit()

# ---- web: access control ---------------------------------------------------------------------------------------------------------------------------
for u in (B + '/', B + '/plan', B + '/reports', B + '/templates', B + '/how-it-works', B + '/mentor', B + '/admin'):
    assert anon.get(u).status_code in (302, 401), u
assert free.get(B + '/').status_code in (302, 403) and free.get(B + '/mentor').status_code in (302, 403)      # premium only
assert free.get(B + '/templates').status_code == 200 and free.get(B + '/how-it-works').status_code == 200        # explanations and templates are open to every member
assert s1.get(B + '/mentor').status_code in (302, 403) and mentor.get(B + '/admin').status_code in (302, 403)
assert b'Build my plan' in s1.get(B + '/').data                                         # no plan yet: the welcome page
for u in (B + '/plan', B + '/download/week.pdf', B + '/download/progress.pdf', B + '/download/plan.csv', B + '/reports'):
    r = s1.get(u)
    assert r.status_code == 302, u                                                      # no plan yet: a friendly redirect, never "Not Found"
assert s1.get(B + '/plan', follow_redirects=True).status_code == 200

# ---- build a plan through the form ---------------------------------------------------------------------------------------------------------------------
r = s1.post(B + '/new', data={'exam': 'JEE', 'level': 'average', 'start': '2026-11-02', 'weeks': '4', 'hours': '4', 'focus': ['Kinematics']})
assert r.status_code == 302
with app.app_context():
    plan = SpPlan.query.filter_by(user_id=uid['s1@x.com'], status='active').one()
    PID = plan.id
    assert plan.level == 'average' and plan.weeks == 4 and plan.hours_per_day == 4 and 'Kinematics' in plan.focus_json
    ts = plan.tasks.order_by(SpTask.day, SpTask.id).all()
    TID = next(t.id for t in ts if t.task_type == 'practice')
    first_day = ts[0].day
h = s1.get(B + '/').get_data(as_text=True)
assert 'Today' in h and 'Today&#39;s thought' in h or "Today's thought" in h
assert 'How to do this' in s1.get(B + '/plan?week=2026-11-02').get_data(as_text=True)
assert s1.post(B + '/new', data={'exam': 'JEE', 'level': 'top', 'start': '2026-11-02', 'weeks': '3'}).status_code == 302
with app.app_context():
    assert SpPlan.query.filter_by(user_id=uid['s1@x.com'], status='active').count() == 1                      # a new plan archives the old one
    assert SpPlan.query.filter_by(id=PID).one().status == 'archived'
    plan = SpPlan.query.filter_by(user_id=uid['s1@x.com'], status='active').one()
    PID = plan.id
    TID = next(t.id for t in plan.tasks.order_by(SpTask.day, SpTask.id) if t.task_type == 'practice')

# ---- ticking tasks: owner, mentor and admin may; others may not --------------------------------------------------------------------------------------
assert s2.post('%s/task/%d/toggle' % (B, TID), json={'status': 'done'}).status_code == 404
assert mentor2.post('%s/task/%d/toggle' % (B, TID), json={'status': 'done'}).status_code == 404               # a mentor who does not work with this student
r = s1.post('%s/task/%d/toggle' % (B, TID), json={'status': 'done', 'minutes_done': 50})
assert r.get_json()['ok'] and r.get_json()['status'] == 'done'
with app.app_context():
    t = db.session.get(SpTask, TID)
    assert t.status == 'done' and t.minutes_done == 50 and t.done_at is not None
assert mentor.post('%s/task/%d/toggle' % (B, TID), json={'status': 'todo'}).get_json()['status'] == 'todo'      # the student's own mentor
assert s1.post('%s/task/%d/toggle' % (B, TID)).get_json()['status'] == 'done'                                  # no body: toggles

# ---- statistics --------------------------------------------------------------------------------------------------------------------------------------
with app.app_context():
    plan = db.session.get(SpPlan, PID)
    st = P.plan_stats(plan, upto=plan.start_date + timedelta(days=6))
    work = [t for t in plan.tasks.all() if t.task_type != 'rest' and t.day <= plan.start_date + timedelta(days=6)]
    assert st['due'] == len(work) and st['done'] == 1 and st['pct_due'] == round(100 / len(work))
    assert st['by_type']['practice']['completed'] == 1 and sum(v['tasks'] for v in st['by_subject'].values()) == len(work)
    # a three-day streak: finish one task on each of three consecutive days ending on `upto`
    for k, day in enumerate((plan.start_date + timedelta(days=2), plan.start_date + timedelta(days=3), plan.start_date + timedelta(days=4))):
        for t in plan.tasks.filter(SpTask.day == day, SpTask.task_type != 'rest').limit(1):
            t.status, t.minutes_done, t.done_at = 'done', t.minutes, datetime.utcnow()
    db.session.commit()
    assert P.plan_stats(plan, upto=plan.start_date + timedelta(days=4))['streak'] == 3
    assert P.plan_stats(plan, upto=plan.start_date + timedelta(days=6))['streak'] == 0                           # the streak breaks after a missed day
    assert P.plan_stats(plan, upto=plan.start_date + timedelta(days=6))['overdue']
    # EduPulse activity counts answers recorded in Reinforcement
    rs = RfStudent.query.filter_by(user_id=uid['s1@x.com']).one()
    now = datetime.utcnow()
    for i in range(3):
        db.session.add(RfAttempt(student_id=rs.id, assignment_id=None, question_id=1, qid='Q%d' % i, exam='JEE', subject='Physics', chapter='Kinematics', topic='t', difficulty=2, answer_json='"A"',
                                 confidence='M', correct=(i == 0), marks=4 if i == 0 else -1, seconds=30, answered_at=now))
    db.session.commit()
    act = P.edupulse_activity(uid['s1@x.com'], now - timedelta(days=1))
    assert act['reinforce_answers'] == 3 and act['questions'] == 3
    # suggestions: weak chapters from Reinforcement become revision tasks linked to EduPulse
    assert P.weak_chapters(uid['s1@x.com'], 'JEE') == [] or isinstance(P.weak_chapters(uid['s1@x.com'], 'JEE'), list)
    n = P.add_suggested_revision(plan, [('Physics', 'Kinematics'), ('Physics', 'Laws of motion')], start=P.today())
    assert n == 2 and P.add_suggested_revision(plan, [('Physics', 'Kinematics')], start=P.today()) == 0          # never duplicated
    assert SpTask.query.filter_by(plan_id=PID, added_by='suggestion', link_kind='reinforce').count() == 2

# ---- dashboards, reports, downloads ----------------------------------------------------------------------------------------------------------------
assert s1.get(B + '/').status_code == 200 and s1.get(B + '/reports').status_code == 200 and s1.get(B + '/reports?period=month').status_code == 200
with app.app_context():
    from app.models_reinforce import RfNotice
    assert RfNotice.query.filter_by(user_id=uid['s1@x.com'], kind='motivation').count() == 1                      # the weekly thought is added once
s1.get(B + '/')
with app.app_context():
    assert RfNotice.query.filter_by(user_id=uid['s1@x.com'], kind='motivation').count() == 1
for u in (B + '/download/template/beginner.pdf', B + '/download/template/average.pdf?exam=NEET', B + '/download/template/top.pdf?exam=UCEED', B + '/download/week.pdf', B + '/download/progress.pdf'):
    r = s1.get(u)
    assert r.status_code == 200 and r.data[:5] == b'%PDF-' and len(r.data) > 3000 and r.mimetype == 'application/pdf', u
assert free.get(B + '/download/template/top.pdf').data[:5] == b'%PDF-'                                          # templates are open to all members
assert s1.get(B + '/download/template/expert.pdf').status_code == 404 and free.get(B + '/download/week.pdf').status_code in (302, 403)
csvr = s1.get(B + '/download/plan.csv')
assert csvr.status_code == 200 and csvr.data.startswith(b'date,subject,chapter') and csvr.data.count(b'\n') > 20
assert s2.get(B + '/download/progress.pdf?uid=%d' % uid['s1@x.com']).status_code == 404                        # not someone else's report

# ---- mentor and admin ---------------------------------------------------------------------------------------------------------------------------------
h = mentor.get(B + '/mentor').get_data(as_text=True)
assert 'Stu One' in h and 'Export CSV' in h and 'Behind' in h or 'On track' in h
assert 'Stu One' not in mentor2.get(B + '/mentor').get_data(as_text=True)                                       # each mentor sees only their own students
assert mentor.get(B + '/mentor/student/%d' % uid['s1@x.com']).status_code == 200 and mentor2.get(B + '/mentor/student/%d' % uid['s1@x.com']).status_code == 404
assert mentor.get(B + '/mentor/export.csv').data.startswith(b'student,email,exam,level') and b'Stu One' in mentor.get(B + '/mentor/export.csv').data
assert b'Stu One' not in mentor2.get(B + '/mentor/export.csv').data
assert mentor.get(B + '/mentor?level=beginner').status_code == 200 and mentor.get(B + '/mentor?status=inactive').status_code == 200
assert mentor.get(B + '/mentor/new/%d' % uid['s1@x.com']).status_code == 200 and mentor2.get(B + '/mentor/new/%d' % uid['s1@x.com']).status_code == 404
r = mentor.post('%s/plan/add' % B, data={'plan_id': PID, 'title': 'Redo the 6 guessed questions', 'task_type': 'practice', 'minutes': '30', 'day': '2026-11-03'})
assert r.status_code == 302
with app.app_context():
    assert SpTask.query.filter_by(plan_id=PID, added_by='mentor', title='Redo the 6 guessed questions').count() == 1
assert s2.post('%s/plan/add' % B, data={'plan_id': PID, 'title': 'x'}).status_code == 404
ah = admin.get(B + '/admin').get_data(as_text=True)
assert 'Planner overview' in ah and 'Stu One' in ah and 'Export all plans' in ah
assert admin.get(B + '/admin/export.csv').data.count(b'\n') >= 2 and admin.get(B + '/mentor/student/%d' % uid['s1@x.com']).status_code == 200
assert mentor.post('%s/plan/%d/archive' % (B, PID)).status_code == 302

# ---- Member Home shows the thought of the day ----------------------------------------------------------------------------------------------------------
home = s2.get('/member-home').get_data(as_text=True)
assert 'sp-quote' in home and P.quote_of_the_day().replace("'", '&#39;') in home or P.quote_of_the_day() in home

print('study planner checks passed')
