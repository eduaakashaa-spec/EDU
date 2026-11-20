"""Darsh meeting update of 20 Nov 2026: calendar, KPIs, actions, study plan and profile. Run from college-predictor/:  python tests/test_darsh_pack.py"""
import os
import sys
import tempfile
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import darsh_jee_plan as plan  # noqa: E402
from app.data.meeting_updates import PACKS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsAction, MsEvent, MsKpi, MsSession  # noqa: E402
from app.models_planner import SpPlan, SpTask  # noqa: E402
from app.services import meeting_update, mentorship as svc  # noqa: E402

pack = PACKS['darsh-2026-11-20']
tasks = plan.build()
days = defaultdict(int)
for t in tasks:
    days[t['day']] += t['minutes']
    assert t['task_type'] in ('learn', 'practice', 'revise', 'mock', 'error', 'rest') and len(t['title']) <= 200 and len(t.get('note') or '') <= 300 and len(t.get('chapter') or '') <= 120
# every day from 21 Nov 2026 to 9 Apr 2027 has a task and no day is overloaded
d = plan.START
while d <= plan.END:
    assert d in days, d
    assert days[d] <= 8 * 60, (d, days[d])
    d = date.fromordinal(d.toordinal() + 1)
# the schedule facts the family sent are in the plan
for dd in plan.PART_TESTS:
    assert any(t['day'] == dd and t['task_type'] == 'mock' for t in tasks)
assert sum(1 for t in tasks if t['task_type'] == 'mock' and 'previous-year paper' in t['title'] and t['day'] <= date(2027, 1, 15)) == 10
assert any(t['day'] == date(2027, 2, 16) and 'Physics' in t['title'] for t in tasks) and any(t['day'] == date(2027, 3, 31) and 'Computer Science' in t['title'] for t in tasks)
# Darsh's own ratings: the weakest topics are scheduled and given extra time
assert sum(1 for v in plan.RATINGS.values() if v <= 1) == 11 and len(plan.RATINGS) == 69
assert any('no question came from this topic' in t['title'] and t['minutes'] == 30 for t in tasks) and any('self-rated 1' in t['title'] and 'Gap map: Tier' in t['note'] for t in tasks)
assert not any('self-rated' in t['title'] and t['chapter'] in ('States of matter', 'Mathematical reasoning') for t in tasks)             # topics with no 2026 question never get a start-from-basics block
subs = defaultdict(int)
for t in tasks:
    if t['task_type'] in ('learn', 'practice', 'revise') and t['day'] < date(2027, 1, 20):
        subs[t['subject']] += t['minutes']
assert subs['Chemistry'] > subs['Mathematics'] > 0 and subs['Physics'] > subs['Mathematics'] and abs(subs['Chemistry'] - subs['Physics']) < 0.12 * subs['Physics']   # Maths stays last; the gap map gives Physics the extra time its gaps need
blob = repr(pack).lower()
assert 'whatsapp' not in blob and 'password' not in blob and 'darsh@' not in blob and 'drive.google' not in blob      # the Drive folder link is entered in the portal, never kept in code
assert {a[2] for a in pack['actions']} <= {'student', 'parent', 'mentor'}
for k in pack['kpis']:
    assert len(k) == 13 and k[0] in ('Preparation', 'Readiness', 'Mentorship', 'Performance') and k[5] in ('higher', 'lower')

from app.services import meeting_import  # noqa: E402
_plan, _errs = meeting_import.parse(open(os.path.join(ROOT, 'tools', 'meetings', 'darsh_2026-11-20.json'), encoding='utf-8').read())
assert not _errs and len(_plan['milestones']) >= 9 and _plan['groups']['JEE']['status'] == 'Primary'

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    for n, em, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Darsh Agarwal', 'd@x.com', 'elite')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    db.session.commit()
    U = lambda em: User.query.filter_by(email=em).one()  # noqa: E731
    e = svc.enrol(U('d@x.com'), U('m@x.com'), svc.ensure_default_programme())
    db.session.add(SpPlan(user_id=e.student_id, title='Older plan', exam='JEE', level='average', start_date=date(2026, 11, 1), weeks=4, status='active'))
    db.session.commit()
    E, SID = e.id, e.student_id

with app.app_context():
    e = db.session.get(type(e), E)
    n = meeting_update.apply(e, pack, 1)
    assert n['kpis'] == len(pack['kpis']) and n['actions'] == len(pack['actions']) and n['events'] == len(pack['events']) and n['sessions'] == 1 and n['profile'] == 1 and n['assessment'] == 1
    assert n['plan_tasks'] == len(tasks)
    p = SpPlan.query.filter_by(user_id=SID, status='active').one()
    assert p.title.startswith('Darsh: JEE Main 2027') and p.tasks.count() == len(tasks) and SpPlan.query.filter_by(user_id=SID, title='Older plan').one().status == 'archived'
    assert 'CBSE board exams' in db.session.get(type(e), E).goals and 'Gap map' in db.session.get(type(e), E).goals
    from app.models_planner import SpAssessment
    assert SpAssessment.query.filter_by(user_id=SID).one().ratings['P07'] == 1
    again = meeting_update.apply(e, pack, 1)                                                              # a second press adds nothing
    assert not any(again.values()), again
    assert SpTask.query.filter_by(plan_id=p.id).count() == len(tasks) and MsEvent.query.filter_by(enrolment_id=E).count() == len(pack['events'])
    assert MsEvent.query.filter_by(enrolment_id=E, title='CBSE board: Physics').one().starts_on == date(2027, 2, 16)

c = app.test_client()
assert c.post('/login', data={'email': 'd@x.com', 'password': 'x'}).status_code == 302
assert c.get('/study-planner/plan?week=2026-11-30').status_code in (200, 302)
print('darsh pack checks passed')
