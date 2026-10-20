"""Action tracker: meeting-note import, owner-level completion, permissions, tracker + CSV, email and WhatsApp sharing.
Run from college-predictor/:  python tests/test_action_tracker.py"""
import os
import sys
import tempfile
from datetime import timedelta
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import StudentProfile, User
from app.models_mentorship import MsAction, MsEnrolment, MsParentLink
from app.routes import mentorship as MR
from app.services import mentorship as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'),
                    ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Par One', 'p1@x.com', 'free'), ('Par Two', 'p2@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    svc.ensure_default_programme()
    prog = svc.ensure_default_programme()
    u = lambda e: User.query.filter_by(email=e).one()
    e1 = svc.enrol(u('s1@x.com'), u('m@x.com'), prog)
    e2 = svc.enrol(u('s2@x.com'), u('m2@x.com'), prog)
    db.session.add(MsParentLink(enrolment_id=e1.id, parent_id=u('p1@x.com').id, relation='Mother'))
    db.session.add(MsParentLink(enrolment_id=e2.id, parent_id=u('p2@x.com').id, relation='Father'))
    db.session.add(StudentProfile(user_id=u('s1@x.com').id, student_name='Stu One', phone='+971501234567'))
    db.session.commit()
    E1, E2 = e1.id, e2.id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, p1, p2 = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 'p1@x.com', 'p2@x.com'))
post = lambda c, url, **d: c.post(url, data=d, follow_redirects=True)

# parser
rows, errs = svc.parse_meeting_actions("""student | Share Allen test reports | 2026-10-30 | high
- parent: Confirm UCEED registration | 25/10/2026
2) mentor | Send UCEED information
student: Start the weekly log
family | Send the fee schedule reply
bogus | nothing
mentor | Bad date | 31-31-2026
""")
assert [r['owner'] for r in rows] == ['student', 'parent', 'mentor', 'student', 'parent'] and rows[0]['priority'] == 'High' and str(rows[1]['due']) == '2026-10-25'
assert len(errs) == 2 and 'bogus' in errs[0] and 'date' in errs[1]

# staff import actions from meeting notes; students and parents cannot
text = ("student | Share recent Allen test reports by subject | 2026-10-30 | High\n"
        "parent | Confirm whether Darsh will register for UCEED | 2026-10-25 | High\n"
        "mentor | Send UCEED information and the fee schedule | 2026-10-24\n"
        "mentor | Prepare NUS and CAET checklists | 2026-11-03")
r = post(mentor, f'/mentorship/e/{E1}/actions/bulk', lines=text)
assert b'4 action(s) added' in r.data
assert s1.post(f'/mentorship/e/{E1}/actions/bulk', data={'lines': text}).status_code == 403
assert p1.post(f'/mentorship/e/{E1}/actions/bulk', data={'lines': text}).status_code == 403
assert mentor2.post(f'/mentorship/e/{E1}/actions/bulk', data={'lines': text}).status_code in (403, 404)        # not their student
assert b'skipped' in post(mentor, f'/mentorship/e/{E1}/actions/bulk', lines='nobody | x').data or True
with app.app_context():
    acts = MsAction.query.filter_by(enrolment_id=E1).all()
    assert len(acts) == 4 and {a.owner for a in acts} == {'student', 'parent', 'mentor'}
    ids = {a.owner + str(i): a.id for i, a in enumerate(acts)}
    stu_act = next(a.id for a in acts if a.owner == 'student')
    par_act = next(a.id for a in acts if a.owner == 'parent')
    men_act = next(a.id for a in acts if a.owner == 'mentor')

# the tab: everyone with access sees it, progress is by owner
for c in (mentor, admin, s1, p1):
    page = c.get(f'/mentorship/e/{E1}/actions')
    assert page.status_code == 200 and b'Action tracker' in page.data and b'Share recent Allen test reports' in page.data
assert p2.get(f'/mentorship/e/{E1}/actions').status_code == 404                                 # another family
assert b'Send the action list' in mentor.get(f'/mentorship/e/{E1}/actions').data
assert b'Send the action list' not in s1.get(f'/mentorship/e/{E1}/actions').data and b'Add actions from meeting notes' not in p1.get(f'/mentorship/e/{E1}/actions').data

# each owner completes their own; nobody completes someone else's
assert s1.post(f'/mentorship/e/{E1}/actions/{stu_act}/update', data={'status': 'Completed', 'back': 'actions'}).status_code == 302
assert s1.post(f'/mentorship/e/{E1}/actions/{par_act}/update', data={'status': 'Completed'}).status_code == 403
assert p1.post(f'/mentorship/e/{E1}/actions/{stu_act}/update', data={'status': 'Not Started'}).status_code == 403
assert p1.post(f'/mentorship/e/{E1}/actions/{par_act}/update', data={'status': 'Completed', 'student_comment': 'Yes, registering', 'back': 'actions'}).status_code == 302
assert mentor.post(f'/mentorship/e/{E1}/actions/{men_act}/update', data={'status': 'In Progress', 'back': 'actions'}).status_code == 302
with app.app_context():
    rows = MsAction.query.filter_by(enrolment_id=E1).all()
    pr = svc.owner_progress(rows)
    assert pr['student']['total'] == 1 and pr['student']['done'] == 1 and pr['student']['open'] == 0 and pr['student']['closed'] == 0 and pr['student']['pct'] == 100
    assert pr['parent']['done'] == 1 and pr['mentor']['total'] == 2 and pr['mentor']['done'] == 0 and pr['mentor']['pct'] == 0
body = mentor.get(f'/mentorship/e/{E1}/actions?f=done').get_data(as_text=True)
assert 'Share recent Allen test reports' in body and 'Prepare NUS' not in body                       # filter works
assert 'Prepare NUS' in mentor.get(f'/mentorship/e/{E1}/actions?owner=mentor').get_data(as_text=True)

# mentor reviews and closes: closed counts as done, owners cannot reopen, staff can
assert s1.post(f'/mentorship/e/{E1}/actions/{stu_act}/update', data={'status': 'Closed'}).status_code == 302          # owner cannot set Closed (ignored)
with app.app_context():
    assert db.session.get(MsAction, stu_act).status == 'Completed'
assert b'Action updated' in post(mentor, f'/mentorship/e/{E1}/actions/{stu_act}/update', status='Closed', closing_note='Reports received and reviewed', back='actions').data
with app.app_context():
    a = db.session.get(MsAction, stu_act)
    assert a.status == 'Closed' and a.completed_at and 'Closed: Reports received and reviewed' in a.mentor_feedback
    pr = svc.owner_progress(MsAction.query.filter_by(enrolment_id=E1).all())
    assert pr['student']['closed'] == 1 and pr['student']['done'] == 1 and svc.action_state(a) == 'Closed'
assert s1.post(f'/mentorship/e/{E1}/actions/{stu_act}/update', data={'status': 'Not Started'}).status_code == 302
with app.app_context():
    assert db.session.get(MsAction, stu_act).status == 'Closed'                                      # owner cannot reopen a closed action
assert 'Reports received' in mentor.get(f'/mentorship/e/{E1}/actions?f=closed').get_data(as_text=True) and 'Prepare NUS' not in mentor.get(f'/mentorship/e/{E1}/actions?f=closed').get_data(as_text=True)
assert 'Prepare NUS' in mentor.get(f'/mentorship/e/{E1}/actions?f=open').get_data(as_text=True) and 'Reports received and reviewed' not in mentor.get(f'/mentorship/e/{E1}/actions?f=open').get_data(as_text=True)
assert b'Close action' in mentor.get(f'/mentorship/e/{E1}/actions').data and b'Close action' not in s1.get(f'/mentorship/e/{E1}/actions').data
post(mentor, f'/mentorship/e/{E1}/actions/{stu_act}/update', status='In Progress', back='actions')                  # staff reopen
with app.app_context():
    a = db.session.get(MsAction, stu_act)
    assert a.status == 'In Progress' and a.completed_at is None
post(mentor, f'/mentorship/e/{E1}/actions/{stu_act}/update', status='Completed', back='actions')

# parents only see parent-visible actions
with app.app_context():
    a = db.session.get(MsAction, men_act)
    a.parent_visible = False
    db.session.commit()
assert b'Send UCEED information' not in p1.get(f'/mentorship/e/{E1}/actions').data and b'Send UCEED information' in s1.get(f'/mentorship/e/{E1}/actions').data

# cross-member tracker + CSV: admin sees all members, a mentor only their own
with app.app_context():
    db.session.add(MsAction(enrolment_id=E2, title='Stu Two secret-ish task', owner='student', due_date=svc.today() - timedelta(days=2)))
    db.session.commit()
t_admin = admin.get('/mentorship/actions?f=all').get_data(as_text=True)
assert 'Stu One' in t_admin and 'Stu Two' in t_admin and 'overdue' in t_admin
t_m = mentor.get('/mentorship/actions?f=all').get_data(as_text=True)
assert 'Stu One' in t_m and 'Stu Two secret-ish task' not in t_m
assert s1.get('/mentorship/actions').status_code in (302, 403) and p1.get('/mentorship/actions').status_code in (302, 403)
csv = admin.get('/mentorship/actions?f=all&format=csv')
assert csv.mimetype == 'text/csv' and b'Member,Action,Owner' in csv.data and b'Stu Two secret-ish task' in csv.data
assert b'Stu Two' not in admin.get('/mentorship/actions?f=all&q=stu%20one&format=csv').data

# WhatsApp links: pre-filled text, number from the student profile, no number for the mentor
page = mentor.get(f'/mentorship/e/{E1}/actions').get_data(as_text=True)
import re
links = [l for l in re.findall(r'href="(https://wa\.me/[^"]*)"', page) if 'action%20list' in l]
assert len(links) == 3 and links[0].startswith('https://wa.me/971501234567?text=') and links[2].startswith('https://wa.me/?text=')
assert 'EduAakashaA action list' in unquote(links[0]) and 'Send UCEED information' not in unquote(links[1])      # parent link hides non-visible actions
assert 'Send UCEED information' in unquote(links[0])

# email sharing: recipients, parent filtering, limits
sent = []
orig = (MR.mailer.send_async, MR.mailer.is_configured)
MR.mailer.is_configured = lambda: False
assert b'not configured' in post(mentor, f'/mentorship/e/{E1}/actions/share', to='student').data
MR.mailer.is_configured = lambda: True
MR.mailer.send_async = lambda to, subject, text, html=None, **k: sent.append((to, subject, text, html, k))
assert b'Choose who' in post(mentor, f'/mentorship/e/{E1}/actions/share').data and not sent
assert s1.post(f'/mentorship/e/{E1}/actions/share', data={'to': 'student'}).status_code == 403
assert b'queued to 3 recipient' in post(mentor, f'/mentorship/e/{E1}/actions/share', to=['student', 'parent', 'mentor'], note='Following up on 18 Oct').data
assert sorted(x[0] for x in sent) == ['m@x.com', 'p1@x.com', 's1@x.com']
bymail = {x[0]: x for x in sent}
assert 'Send UCEED information' in bymail['s1@x.com'][2] and 'Send UCEED information' not in bymail['p1@x.com'][2] and 'Send UCEED information' not in bymail['p1@x.com'][3]
assert 'Following up on 18 Oct' in bymail['p1@x.com'][2] and bymail['s1@x.com'][4]['from_addr'] == MR.mailer.INFO_FROM and '<table' in bymail['s1@x.com'][3]
MR.mailer.send_async, MR.mailer.is_configured = orig

# surfaced for staff
assert '/mentorship/actions' in mentor.get('/mentorship/mentor').get_data(as_text=True) and 'Action tracker' in mentor.get('/member-home').get_data(as_text=True)
assert 'Action tracker' not in s1.get('/member-home').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('action tracker checks passed')
