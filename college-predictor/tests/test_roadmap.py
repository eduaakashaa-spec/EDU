"""Student roadmap ("Darsh Roadmap"): created from the NUS / NTU / HKU template, private to the student, linked parents,
assigned mentor and admins, milestone ticks, calendar dates.
Run from college-predictor/:  python tests/test_roadmap.py"""
import os
import sys
import tempfile
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsEnrolment, MsEvent, MsMilestone, MsParentLink, MsProgramme, MsRoadmap  # noqa: E402
from app.services import mentorship as svc  # noqa: E402
from app.services import roadmap as rmap  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()

with app.app_context():
    db.create_all()
    for n, e, t in (('DEMO Admin', 'admin@demo.test', 'admin'), ('DEMO Mentor', 'mentor@demo.test', 'ea_mentor'),
                    ('DEMO Other Mentor', 'mentor2@demo.test', 'ea_mentor'), ('Darsh Test', 's1@demo.test', 'elite'),
                    ('Other Student', 's2@demo.test', 'elite'), ('Darsh Parent', 'p1@demo.test', 'free'),
                    ('Other Parent', 'p2@demo.test', 'free'), ('Free Member', 'free@demo.test', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    prog = MsProgramme(name='Demo programme')
    db.session.add(prog)
    db.session.commit()
    uid = lambda email: User.query.filter_by(email=email).one().id
    e1 = MsEnrolment(student_id=uid('s1@demo.test'), mentor_id=uid('mentor@demo.test'), programme_id=prog.id, preferred_name='Darsh')
    e2 = MsEnrolment(student_id=uid('s2@demo.test'), mentor_id=uid('mentor2@demo.test'), programme_id=prog.id)
    db.session.add_all([e1, e2])
    db.session.commit()
    db.session.add(MsParentLink(enrolment_id=e1.id, parent_id=uid('p1@demo.test')))
    db.session.add(MsParentLink(enrolment_id=e2.id, parent_id=uid('p2@demo.test')))
    db.session.commit()
    EID, EID2 = e1.id, e2.id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302, email
    return c


admin, mentor, mentor2, student, student2, parent, parent2, free = (login(x) for x in (
    'admin@demo.test', 'mentor@demo.test', 'mentor2@demo.test', 's1@demo.test', 's2@demo.test', 'p1@demo.test', 'p2@demo.test', 'free@demo.test'))
anon = app.test_client()
URL = f'/mentorship/e/{EID}/roadmap'
HKU_T = 'HKU first round closes (noon Hong Kong time)'
NUS_T = 'NUS window closes (11:59 pm Singapore time)'
NTU_T = 'NTU window closes: form, fee, declarations and programme choices'

# 1. before it exists: the student and parent do not even get the tab; staff see the create form
assert student.get(URL).status_code == 404 and parent.get(URL).status_code == 404
r = mentor.get(URL)
assert r.status_code == 200 and 'Create roadmap' in r.get_data(as_text=True)

# 2. only staff can create it; a student, a parent and strangers cannot
for c in (student, parent):
    assert c.post(URL + '/create').status_code == 403
for c in (student2, parent2, mentor2, free):
    assert c.post(URL + '/create').status_code == 404
assert anon.post(URL + '/create').status_code in (302, 401)
with app.app_context():
    assert MsRoadmap.query.count() == 0
r = mentor.post(URL + '/create', data={'title': 'Darsh Roadmap'}, follow_redirects=True)
assert r.status_code == 200 and 'Darsh Roadmap' in r.get_data(as_text=True)
assert 'already exists' in mentor.post(URL + '/create', follow_redirects=True).get_data(as_text=True)

# 3. content: three universities, a final "admission complete" milestone each, the key dates
h = mentor.get(URL).get_data(as_text=True)
for t in ('HKU · Hong Kong', 'NUS · Singapore', 'NTU · Singapore', 'HKU admission complete', 'NUS admission complete', 'NTU admission complete',
          HKU_T, NUS_T, NTU_T):
    assert t in h, t
with app.app_context():
    rm = MsRoadmap.query.one()
    ms = rm.milestones
    for g in rmap.UNIVERSITIES:
        assert sum(1 for m in ms if m.grp == g and m.final) == 1
    byt = {m.title: m for m in ms}
    assert byt[HKU_T].due_on == date(2026, 11, 25)
    assert byt[NUS_T].due_on == date(2027, 2, 17)
    assert byt[NTU_T].due_on == date(2027, 3, 19)
    # dated external milestones are in the student's calendar with their source
    evs = MsEvent.query.filter_by(enrolment_id=EID).all()
    titles = {x.title: x for x in evs}
    assert titles['HKU: ' + HKU_T].category == 'Admission deadline'
    assert any(x.category == 'Board exam' for x in evs)
    assert all(x.source for x in evs if x.category == 'Admission deadline')
    assert all(byt[t].event_id for t in (HKU_T, NUS_T, NTU_T))
    MID = byt[HKU_T].id
    FINAL = [m.id for m in ms if m.grp == 'NUS' and m.final][0]

# 4. the roadmap and its dates show for the student and the parent, under the roadmap's name
for c in (student, parent):
    t = c.get(URL).get_data(as_text=True)
    assert 'Darsh Roadmap' in t and 'HKU · Hong Kong' in t and 'Mentor tools' not in t and 'Remove</button>' not in t
    cal = c.get(f'/mentorship/e/{EID}/calendar').get_data(as_text=True)
    assert 'HKU first round closes' in cal and 'NTU window closes' in cal and 'CBSE Class 12 board exams' in cal
assert 'Darsh Roadmap' in student.get(f'/mentorship/e/{EID}/home').get_data(as_text=True)

# 5. NOT visible to anyone else
for who, c in (('other student', student2), ('other parent', parent2), ('other mentor', mentor2), ('free member', free)):
    assert c.get(URL).status_code == 404, who
    assert c.get(f'/mentorship/e/{EID}/calendar').status_code == 404, who
    assert c.post(f'{URL}/m/{MID}/toggle').status_code == 404, who
assert anon.get(URL).status_code in (302, 401)
# another student's own record cannot reach this one through a milestone id
assert student2.post(f'/mentorship/e/{EID2}/roadmap/m/{MID}/toggle').status_code == 404
with app.app_context():
    assert not db.session.get(MsMilestone, MID).done
assert admin.get(URL).status_code == 200

# 6. ticks: student, parent, mentor and admin can tick; the calendar event follows; unticking works
for c in (student, parent, mentor, admin):
    assert c.post(f'{URL}/m/{MID}/toggle').status_code == 302
    with app.app_context():
        m = db.session.get(MsMilestone, MID)
        assert m.done is True and db.session.get(MsEvent, m.event_id).done is True
    assert c.post(f'{URL}/m/{MID}/toggle').status_code == 302
    with app.app_context():
        assert db.session.get(MsMilestone, MID).done is False
mentor.post(f'{URL}/m/{FINAL}/toggle')
assert 'Admission complete' in student.get(URL).get_data(as_text=True)
with app.app_context():
    sm = rmap.summary(MsRoadmap.query.one(), svc.today())
    assert sm['NUS']['done'] == 1 and sm['NUS']['complete'] is True and sm['HKU']['complete'] is False
    assert 0 < sm['NUS']['pct'] < 100

# 7. staff can add and remove; students and parents cannot
assert student.post(f'{URL}/add', data={'title': 'x'}).status_code == 403
assert parent.post(f'{URL}/m/{MID}/delete').status_code == 403
mentor.post(f'{URL}/add', data={'title': 'Visa interview slot booked', 'grp': 'NUS', 'owner': 'parent', 'due_on': '2027-06-01',
                                'calendar': '1', 'source': 'ICA'})
with app.app_context():
    new = MsMilestone.query.filter_by(title='Visa interview slot booked').one()
    assert new.event_id and db.session.get(MsEvent, new.event_id).starts_on == date(2027, 6, 1)
    NID = new.id
mentor.post(f'{URL}/m/{NID}/delete')
with app.app_context():
    assert db.session.get(MsMilestone, NID) is None and MsEvent.query.filter_by(title='NUS: Visa interview slot booked').count() == 0

# 8. only an admin can delete the whole roadmap
assert mentor.post(URL + '/delete').status_code == 403
assert admin.post(URL + '/delete').status_code == 302
with app.app_context():
    assert MsRoadmap.query.count() == 0 and MsMilestone.query.count() == 0
    assert MsEvent.query.filter(MsEvent.enrolment_id == EID, MsEvent.category == 'Admission deadline').count() == 0
print('roadmap checks passed')
