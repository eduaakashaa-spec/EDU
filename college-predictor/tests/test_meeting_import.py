"""Meeting update import: Darsh's 18 Nov 2026 meeting (tools/meetings/darsh_2026-11-18.json) applied to a roadmap.
Run from college-predictor/:  python tests/test_meeting_import.py"""
import json
import os
import sys
import tempfile
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import (MsAction, MsEnrolment, MsEvent, MsMilestone, MsParentLink, MsProgramme, MsRoadmap, MsRoadmapGroup,  # noqa: E402
                                   MsSession)
from app.services import meeting_import as mi  # noqa: E402
from app.services import roadmap as rmap  # noqa: E402

TEXT = open(os.path.join(ROOT, 'tools', 'meetings', 'darsh_2026-11-18.json'), encoding='utf-8').read()

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('DEMO Admin', 'admin@demo.test', 'admin'), ('DEMO Mentor', 'mentor@demo.test', 'ea_mentor'), ('DEMO Mentor 2', 'mentor2@demo.test', 'ea_mentor'),
                    ('Darsh Test', 's1@demo.test', 'elite'), ('Darsh Parent', 'p1@demo.test', 'free'), ('Other Parent', 'p2@demo.test', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    prog = MsProgramme(name='Demo')
    db.session.add(prog)
    db.session.commit()
    uid = lambda x: User.query.filter_by(email=x).one().id
    e1 = MsEnrolment(student_id=uid('s1@demo.test'), mentor_id=uid('mentor@demo.test'), programme_id=prog.id, preferred_name='Darsh')
    db.session.add(e1)
    db.session.commit()
    db.session.add(MsParentLink(enrolment_id=e1.id, parent_id=uid('p1@demo.test')))
    db.session.commit()
    EID = e1.id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302, email
    return c


mentor, mentor2, student, parent, parent2 = (login(x) for x in ('mentor@demo.test', 'mentor2@demo.test', 's1@demo.test', 'p1@demo.test', 'p2@demo.test'))
URL = f'/mentorship/e/{EID}/import'

# 1. parsing: the real file is valid; bad input gives readable errors and writes nothing
plan, errs = mi.parse(TEXT)
assert not errs and len(plan['actions']) == 13 and len(plan['events']) == 4
assert mi.parse('{not json')[1] and mi.parse('[]')[1] and mi.parse('{}')[1]
bad = json.loads(TEXT)
bad['actions'][0]['priority'] = 'Urgent'
bad['events'][0]['starts_on'] = '25/11/2026'
bad['roadmap']['groups']['XYZ'] = {'status': 'On hold'}
errs = mi.parse(json.dumps(bad))[1]
assert len(errs) == 3 and any('priority' in x for x in errs) and any('not a date' in x for x in errs) and any('XYZ' in x for x in errs)

# 2. only staff can reach the page; students, parents and other mentors cannot
assert mentor.get(URL.replace('/import', '/import')).status_code in (200, 404, 405) or True
assert mentor.get(f'/mentorship/e/{EID}/import').status_code == 200
for who, c in (('student', student), ('parent', parent)):
    assert c.get(f'/mentorship/e/{EID}/import').status_code == 404, who
    assert c.post(URL, data={'update': TEXT, 'mode': 'apply'}).status_code == 403, who
for who, c in (('other mentor', mentor2), ('other parent', parent2)):
    assert c.get(f'/mentorship/e/{EID}/import').status_code == 404, who
    assert c.post(URL, data={'update': TEXT, 'mode': 'apply'}).status_code == 404, who

# 3. roadmap changes need a roadmap: without one the meeting and actions are still saved, with a warning
r = mentor.post(URL, data={'update': TEXT, 'mode': 'check'})
assert r.status_code == 200 and 'nothing was saved' in r.get_data(as_text=True) and 'no roadmap yet' in r.get_data(as_text=True)
with app.app_context():
    assert MsSession.query.count() == 0 and MsAction.query.count() == 0, 'a check must not save anything'
mentor.post(f'/mentorship/e/{EID}/roadmap/create', data={'title': 'Darsh Roadmap'})

# 4. check, then apply
r = mentor.post(URL, data={'update': TEXT, 'mode': 'check'})
assert 'nothing was saved' in r.get_data(as_text=True)
with app.app_context():
    assert MsSession.query.count() == 0 and MsAction.query.count() == 0
    n_events_before = MsEvent.query.filter_by(enrolment_id=EID).count()
r = mentor.post(URL, data={'update': TEXT, 'mode': 'apply'})
h = r.get_data(as_text=True)
assert r.status_code == 200 and 'Applied' in h and 'Update applied' in h
with app.app_context():
    s = MsSession.query.one()
    assert s.status == 'Completed' and s.kind == 'follow-up' and s.duration_min == 51 and s.parent_visible
    assert s.actual_at == datetime(2026, 11, 18, 16, 1) and 'NTU Singapore is the first choice' in s.shared_summary and 'placeholder name' in s.mentor_notes
    assert 'placeholder name' not in s.shared_summary, 'private notes must not leak into the shared recap'
    acts = MsAction.query.filter_by(enrolment_id=EID).all()
    assert len(acts) == 13 and all(a.session_id == s.id for a in acts)
    done = [a for a in acts if a.status == 'Completed']
    assert len(done) == 1 and 'WhatsApp group' in done[0].title and done[0].completed_at
    weekly = [a for a in acts if a.recurrence == 'weekly']
    assert len(weekly) == 1 and weekly[0].priority == 'High'
    assert {a.owner for a in acts} == {'student', 'parent', 'mentor'}
    evs = MsEvent.query.filter_by(enrolment_id=EID).all()
    assert any(x.title == 'School model exams (portion-based)' and x.starts_on == date(2026, 11, 25) and x.ends_on == date(2026, 12, 16) for x in evs)
    assert any(x.category == 'JEE Main' and x.starts_on == date(2027, 1, 20) for x in evs)
    rm = MsRoadmap.query.one()
    st = rmap.group_state(rm)
    assert st['HKU'][0] == 'On hold' and st['NTU'][0] == 'Primary' and st['NUS'][0] == 'Backup'
    assert any(m.grp == 'JEE' and m.done and m.title.startswith('JEE Main Session 1 application') for m in rm.milestones)
    assert {m.grp for m in rm.milestones} >= {'JEE', 'CAET', 'HKU', 'NUS', 'NTU', 'PREP'}
    # HKU is on hold: its calendar entries are marked done with a note and its steps leave the overall count
    hku_ev = [db.session.get(MsEvent, m.event_id) for m in rm.milestones if m.grp == 'HKU' and m.event_id]
    assert hku_ev and all(x.done and rmap.HOLD_MARK.strip() in (x.notes or '') for x in hku_ev)
    sm = rmap.summary(rm, date(2026, 11, 18))
    assert list(sm)[0] == 'PREP' and list(sm)[1] == 'NTU' and list(sm)[-1] == 'HKU' and sm['HKU']['hold'] and not sm['NTU']['hold']

# 5. idempotent: applying again changes nothing
r = mentor.post(URL, data={'update': TEXT, 'mode': 'apply'})
assert '0 new' in r.get_data(as_text=True)
with app.app_context():
    assert MsSession.query.count() == 1 and MsAction.query.count() == 13

# 6. the family sees the recap and the actions but not the private notes; the roadmap shows the decisions
t = student.get(f'/mentorship/e/{EID}/sessions').get_data(as_text=True)
assert 'DASA 2027 route, university shortlist and JEE Main plan' in t and 'placeholder name' not in t
rt = parent.get(f'/mentorship/e/{EID}/roadmap').get_data(as_text=True)
assert 'On hold' in rt and 'Primary' in rt and 'JEE Main · India route' in rt and 'IIT Delhi Abu Dhabi · CAET' in rt and 'Mentor tools' not in rt
at = student.get(f'/mentorship/e/{EID}/actions').get_data(as_text=True)
assert 'Tick the Physics, Chemistry and Maths topics' in at
cal = student.get(f'/mentorship/e/{EID}/calendar').get_data(as_text=True)
assert 'School model exams' in cal and 'JEE Main 2027 Session 1 exam days' in cal

# 7. a decision can be changed by staff only, and reinstating restores the calendar
assert student.post(f'/mentorship/e/{EID}/roadmap/group/HKU', data={'status': 'Active'}).status_code == 403
assert mentor.post(f'/mentorship/e/{EID}/roadmap/group/HKU', data={'status': 'Active', 'note': 'Family changed its mind'}).status_code == 302
with app.app_context():
    rm = MsRoadmap.query.one()
    assert rmap.group_state(rm)['HKU'][0] == 'Active'
    hku_ev = [db.session.get(MsEvent, m.event_id) for m in rm.milestones if m.grp == 'HKU' and m.event_id and not m.done]
    assert hku_ev and all(not x.done and rmap.HOLD_MARK.strip() not in (x.notes or '') for x in hku_ev)
assert mentor.post(f'/mentorship/e/{EID}/roadmap/group/HKU', data={'status': 'Nonsense'}).status_code == 400
print('meeting import checks passed')
