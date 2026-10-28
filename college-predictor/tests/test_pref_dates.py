"""College list: pick an exam the student follows, record application open / deadline / exam date, show on the list and the calendar.
Run from college-predictor/:  python tests/test_pref_dates.py"""
import os
import re
import sys
import tempfile
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import User
from app.models_mentorship import MsExam, MsExamFocus, MsParentLink, MsPrefDates, MsPrefEntry, MsPrefList
from app.services import mentorship as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Stu', 's@x.com', 'elite'), ('Par', 'p@x.com', 'free'), ('Other', 'o@x.com', 'elite')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    prog = svc.ensure_default_programme()
    u = lambda e: User.query.filter_by(email=e).one()
    en = svc.enrol(u('s@x.com'), u('m@x.com'), prog)
    db.session.add(MsParentLink(enrolment_id=en.id, parent_id=u('p@x.com').id))
    today = date.today()
    followed = MsExam(name='UCEED 2027', category='Other', starts_on=today + timedelta(days=90), status='Confirmed', source='uceed.iitb.ac.in')
    other = MsExam(name='JEE Main 2027 Session 1', category='JEE Main', starts_on=today + timedelta(days=60), status='Tentative')
    db.session.add_all([followed, other])
    db.session.commit()
    db.session.add(MsExamFocus(enrolment_id=en.id, exam_id=followed.id))
    lst = MsPrefList(enrolment_id=en.id, name='Draft')
    db.session.add(lst)
    db.session.commit()
    E, L, FX, OX = en.id, lst.id, followed.id, other.id
    exam_day = followed.starts_on


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


mentor, stu, par, oth = login('m@x.com'), login('s@x.com'), login('p@x.com'), login('o@x.com')
post = lambda c, url, **d: c.post(url, data=d, follow_redirects=True)

# the form offers only exams the student follows
page = mentor.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True)
assert 'UCEED 2027' in page and 'JEE Main 2027 Session 1' not in page and 'Entrance exam and application dates' in page

# add a choice with an exam from the list and dates
dl = today + timedelta(days=10)
r = post(mentor, f'/mentorship/e/{E}/prefs/{L}/entry/add', college='IIT Bombay', branch='B.Des', route='Other', tier='Aspirational',
         exam_id=str(FX), app_open=str(today - timedelta(days=5)), app_deadline=str(dl), dates_source='official brochure, checked today')
assert r.status_code == 200
with app.app_context():
    x = MsPrefEntry.query.filter_by(college='IIT Bombay').one()
    d = x.dates
    assert d.exam_id == FX and d.exam_date == exam_day and d.app_deadline == dl and d.source.startswith('official')   # exam date from the catalogue
    assert d.exam_name == 'UCEED 2027'
    XID = x.id
page = mentor.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True)
assert 'UCEED 2027' in page and 'Closes in 10 days' in page and 'official brochure' in page
assert 'Closes in 10 days' in par.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True)                  # parents see the dates
assert 'Add dates' not in par.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True) and 'Edit dates' not in par.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True)

# an exam the student does not follow cannot be linked; typed exams work
post(mentor, f'/mentorship/e/{E}/prefs/{L}/entry/add', college='NIT X', exam_id=str(OX), exam_label='JEE Main', app_deadline=str(today - timedelta(days=3)))
with app.app_context():
    d2 = MsPrefEntry.query.filter_by(college='NIT X').one().dates
    assert d2.exam_id is None and d2.exam_label == 'JEE Main' and d2.exam_date is None
    X2 = d2.entry_id
assert 'Closed 3 days ago' in mentor.get(f'/mentorship/e/{E}/prefs').get_data(as_text=True)

# a choice without any dates stores nothing
post(mentor, f'/mentorship/e/{E}/prefs/{L}/entry/add', college='No dates college')
with app.app_context():
    assert MsPrefEntry.query.filter_by(college='No dates college').one().dates is None

# edit dates: student and mentor can; parent and other students cannot
assert stu.post(f'/mentorship/e/{E}/prefs/entry/{XID}/dates', data={'exam_label': 'UCEED', 'app_open': str(today - timedelta(days=5)), 'app_deadline': str(dl + timedelta(days=5))}).status_code == 302
with app.app_context():
    assert MsPrefEntry.query.get(XID).dates.app_deadline == dl + timedelta(days=5)
assert par.post(f'/mentorship/e/{E}/prefs/entry/{XID}/dates', data={'app_deadline': '2030-01-01'}).status_code == 403
assert oth.post(f'/mentorship/e/{E}/prefs/entry/{XID}/dates', data={'app_deadline': '2030-01-01'}).status_code == 404
# clearing every field removes the row
post(mentor, f'/mentorship/e/{E}/prefs/entry/{X2}/dates')
with app.app_context():
    assert MsPrefEntry.query.get(X2).dates is None

# the dates reach the calendar (deadline + open; exam date only when the exam is not already followed)
with app.app_context():
    en = db.session.get(__import__('app.models_mentorship', fromlist=['MsEnrolment']).MsEnrolment, E)
    titles = [i['title'] for i in svc.events_for(en)]
assert 'Application deadline: IIT Bombay' in titles and 'Applications open: IIT Bombay' in titles
assert not [t for t in titles if t.startswith('Exam: UCEED')]                                              # already on the calendar via the followed exam
page = stu.get(f'/mentorship/e/{E}/calendar').get_data(as_text=True)
assert 'Application deadline: IIT Bombay' in page

# deleting an entry removes its dates
assert mentor.post(f'/mentorship/e/{E}/prefs/entry/{XID}/delete').status_code in (200, 302)
with app.app_context():
    assert MsPrefDates.query.count() == 0

assert svc.deadline_label(None) == ('', '') and svc.deadline_label(date(2026, 1, 20), date(2026, 1, 1))[1] == 'ok' and svc.deadline_label(date(2026, 1, 1), date(2026, 1, 1))[0] == 'Closes today'

try:
    os.unlink(_db)
except OSError:
    pass
print('pref dates checks passed')
