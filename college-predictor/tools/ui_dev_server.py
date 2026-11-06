"""Local UI preview with demo people and data (temp sqlite). Not used in production.

Logins (password demo1234): student s1@demo.test, parent p1@demo.test, mentor m@demo.test, admin a@demo.test.
It has an enrolled student with a dozen mentor actions, a weekly check-in, a study plan, a reinforcement roster entry, an assessment result and a saved PCM and PCB dashboard.
"""
import json
import os
import sys
import tempfile
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fd, path = tempfile.mkstemp(suffix='.db')
os.close(fd)
os.environ.update(DATABASE_URL='sqlite:///' + path, SECRET_KEY='dev', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsAction, MsParentLink  # noqa: E402
from app.models_pulse import Class12Profile  # noqa: E402
from app.services import assessments as asv, mentorship as svc, planner  # noqa: E402

app = create_app()
pw = lambda: bcrypt.generate_password_hash('demo1234').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@demo.test', 'admin'), ('Meera Mentor', 'm@demo.test', 'ea_mentor'), ('Aarav Kumar', 's1@demo.test', 'elite'), ('Priya Kumar', 'p1@demo.test', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    u = lambda e: User.query.filter_by(email=e).one()  # noqa: E731
    prog = svc.ensure_default_programme()
    enr = svc.enrol(u('s1@demo.test'), u('m@demo.test'), prog, preferred_name='Aarav')
    db.session.add(MsParentLink(enrolment_id=enr.id, parent_id=u('p1@demo.test').id, relation='Mother'))
    d = date.today()
    rows = [('Finish Electrostatics chapter test and log the errors', 'student', -2, 'High', 'Not Started', 'Concept gaps show up fastest in a timed test.'),
            ('Rewrite the two Section C answers from last paper in full marking-scheme style', 'student', 1, 'High', 'In Progress', 'Step marks are the cheapest marks.'),
            ('Share the school unit-test marksheet with the mentor', 'parent', -1, 'Medium', 'Not Started', 'Needed to set the baseline.'),
            ('Send the JoSAA documents checklist', 'mentor', 2, 'Medium', 'Not Started', ''),
            ('Do 10 questions a day from the EduPulse set', 'student', 3, 'Medium', 'Not Started', 'Spaced practice beats cramming.'),
            ('Attend the Saturday mock under exam conditions', 'student', 5, 'High', 'Not Started', ''),
            ('Book the career counselling call', 'parent', 6, 'Low', 'Not Started', ''),
            ('Prepare the mock analysis note', 'mentor', 4, 'Medium', 'In Progress', ''),
            ('Maths: Matrices worksheet', 'student', -6, 'Low', 'Completed', ''),
            ('Chemistry: organic reactions table', 'student', -4, 'Medium', 'Completed', ''),
            ('Physics: Gauss law derivation twice on paper', 'student', -3, 'Medium', 'Completed', ''),
            ('Confirm the school practical dates', 'parent', -5, 'Low', 'Completed', ''),
            ('Review last month goals with the family', 'mentor', 8, 'Low', 'Not Started', ''),
            ('Read NCERT Chemistry line by line: Solutions', 'student', 7, 'Medium', 'Not Started', '')]
    for title, owner, off, pri, status, why in rows:
        a = MsAction(enrolment_id=enr.id, title=title, owner=owner, due_date=d + timedelta(days=off), priority=pri, status=status, purpose=why, est_minutes=45, parent_visible=True,
                     instruction='Work in a quiet spot, keep the paper, and note the time it took.' if owner == 'student' else None)
        if status == 'Completed':
            from datetime import datetime
            a.completed_at = datetime.utcnow()
        db.session.add(a)
    db.session.commit()
    try:
        asv.ingest('stream-selection', {'studentInfo': {'name': 'Aarav Kumar', 'email': 's1@demo.test', 'currentClass': '12', 'board': 'CBSE'},
                                        'results': {'recommended': 'Science (PCM)', 'percentages': {'Science': 62, 'Commerce': 21, 'Humanities': 17}, 'aptitudeScore': 9, 'aptitudeTotal': 15}}, user=u('s1@demo.test'), commit=True)
    except Exception as ex:                                  # the preview still works without the assessment
        print('assessment seed skipped:', ex, flush=True)
    try:
        planner.generate_plan(u('s1@demo.test'), 'JEE', 'average', planner.week_start(d), 4, mentor_id=u('m@demo.test').id, created_by=u('s1@demo.test').id)
        db.session.commit()
    except Exception as ex:
        print('plan seed skipped:', ex, flush=True)
    try:
        from app.models_reinforce import RfStudent
        from app.services import reinforce as rf
        rf.seed_taxonomy()
        db.session.add(RfStudent(user_id=u('s1@demo.test').id, mentor_id=u('m@demo.test').id, exam='JEE', grade='Class 12'))
        db.session.commit()
    except Exception as ex:
        print('reinforcement seed skipped:', ex, flush=True)
    uid = u('s1@demo.test').id
    for stream, ratings in (('pcm', {'P01': 2, 'P03': 4, 'C02': 1, 'M05': 2}), ('pcb', {'B04': 2, 'B05': 1, 'C02': 3})):
        db.session.add(Class12Profile(user_id=uid, stream=stream, data_json=json.dumps({'exam_date': str(d + timedelta(days=100)), 'hours_wd': 2, 'hours_we': 5, 'cat': 'g', 'ratings': ratings,
                                                                                         'marks': {'Pt': 44, 'Pp': 22, 'Ct': 50, 'Cp': 25, 'Mt' if stream == 'pcm' else 'Bt': 48, 'Mi' if stream == 'pcm' else 'Bp': 15, 'En': 70, 'Fi': 70},
                                                                                         'tests': [{'subj': 'P', 'date': str(d - timedelta(days=10)), 'got': 33, 'max': 70}, {'subj': 'C', 'date': str(d - timedelta(days=8)), 'got': 50, 'max': 70}]})))
    db.session.commit()
    print('student s1@demo.test / parent p1@demo.test / mentor m@demo.test / admin a@demo.test, password demo1234', flush=True)
app.run(port=5079, use_reloader=False)
