"""Registration document checklists on followed exams (member portal, Calendar tab).

Run from college-predictor/:  python tests/test_exam_docs.py
Covers: checklist only on followed exams, per-exam extra items, student-only ticking, confirm needs every
required item, unticking withdraws the confirmation, isolation between students, unknown keys ignored.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.models_mentorship import MsDocCheck, MsDocConfirm, MsEnrolment, MsExam, MsProgramme
from app.services import exam_docs as xd

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    for name, email, tier in (('DEMO Admin', 'admin@demo.test', 'admin'), ('DEMO Mentor', 'mentor@demo.test', 'ea_mentor'),
                              ('DEMO Mentor Two', 'mentor2@demo.test', 'ea_mentor'), ('DEMO Student One', 's1@demo.test', 'premium'),
                              ('DEMO Student Two', 's2@demo.test', 'premium'), ('DEMO Parent', 'p1@demo.test', 'free')):
        db.session.add(User(name=name, email=email, tier=tier, password_hash=pw))
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302, email
    return c


def post(c, url, **data):
    return c.post(url, data=data, follow_redirects=True)


admin, mentor, mentor2, s1, s2, p1 = (login(e) for e in ('admin@demo.test', 'mentor@demo.test', 'mentor2@demo.test',
                                                         's1@demo.test', 's2@demo.test', 'p1@demo.test'))
post(admin, '/mentorship/admin/load-default')
with app.app_context():
    pid = MsProgramme.query.filter_by(name='Grade 12 Engineering Mentorship').one().id
post(admin, '/mentorship/admin/enrol', student_email='s1@demo.test', programme_id=pid, mentor_email='mentor@demo.test')
post(admin, '/mentorship/admin/enrol', student_email='s2@demo.test', programme_id=pid, mentor_email='mentor2@demo.test')
post(admin, '/mentorship/admin/exams/load-default')
with app.app_context():
    E1 = MsEnrolment.query.join(User, MsEnrolment.student_id == User.id).filter(User.email == 's1@demo.test').one().id
    E2 = MsEnrolment.query.join(User, MsEnrolment.student_id == User.id).filter(User.email == 's2@demo.test').one().id
    ex = {x.name: x for x in MsExam.query.all()}
    UCEED, KCET = ex['UCEED 2027'].id, ex['KCET 2027'].id
    # per-exam extras: matched on whole-word starts, so UCEED does not pick up CEED's degree line
    keys = lambda n: [k for k, *_ in xd.items_for(ex[n])]
    assert 'degree' in keys('CEED 2027') and 'degree' not in keys('UCEED 2027')
    assert 'domicile' in keys('KCET 2027') and 'domicile' in keys('TG-EAPCET / AP-EAPCET 2027') and 'domicile' not in keys('BITSAT 2027')
    assert 'jee_main' in keys('JEE Advanced 2027') and keys('UCEED 2027')[-1] == 'nri'
    required_uceed = [k for k, _l, _h, req in xd.items_for(ex['UCEED 2027']) if req]
post(admin, '/mentorship/admin/parent', enrolment_id=E1, parent_email='p1@demo.test')
base = f'/mentorship/e/{E1}/exams'

# no checklist until the exam is followed; a ticks POST on an unfollowed exam is refused
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert 'Registration documents' not in cal
assert s1.post(f'{base}/{UCEED}/docs', data={'doc': 'photo'}).status_code == 404
post(s1, f'{base}/{UCEED}/focus', on='1')
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert cal.count('Registration documents') == 1 and f'0 / {len(required_uceed)} required ready' in cal
assert 'Confirm all documents are verified' in cal

# only the student ticks: mentor / parent get 403, another student's mentor 404
assert mentor.post(f'{base}/{UCEED}/docs', data={'doc': 'photo'}).status_code == 403
assert p1.post(f'{base}/{UCEED}/docs', data={'doc': 'photo'}).status_code == 403
assert mentor2.post(f'{base}/{UCEED}/docs', data={'doc': 'photo'}).status_code == 404
assert s2.post(f'{base}/{UCEED}/docs', data={'doc': 'photo'}).status_code == 404

# partial ticks save; unknown keys are ignored; confirming too early is refused but keeps the ticks
r = post(s1, f'{base}/{UCEED}/docs', doc=['photo', 'signature', 'bogus'])
assert 'checklist for UCEED 2027 saved' in r.get_data(as_text=True)
r = post(s1, f'{base}/{UCEED}/docs', doc=['photo', 'signature', 'class10'], confirm='1')
assert 'not confirmed' in r.get_data(as_text=True) and f'3 / {len(required_uceed)} required ready' in r.get_data(as_text=True)
with app.app_context():
    assert {c.item_key for c in MsDocCheck.query.filter_by(enrolment_id=E1, exam_id=UCEED)} == {'photo', 'signature', 'class10'}
    assert MsDocConfirm.query.count() == 0

# all required ticked (optional ones not needed) -> confirmed, audited; mentor and parent see it read-only
r = post(s1, f'{base}/{UCEED}/docs', doc=required_uceed, confirm='1')
t = r.get_data(as_text=True)
assert 'all required documents for UCEED 2027 are verified and ready' in t and 'All verified &amp; ready' in t
with app.app_context():
    assert MsDocConfirm.query.filter_by(enrolment_id=E1, exam_id=UCEED).count() == 1
    from app.models_mentorship import MsAudit
    assert MsAudit.query.filter_by(enrolment_id=E1, action='docs.confirmed').count() == 1
for viewer in (mentor, p1):
    v = viewer.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
    assert 'All verified &amp; ready' in v and 'Only the student can tick' in v and 'Confirm all documents' not in v

# unticking a required item withdraws the confirmation; optional items never block it
post(s1, f'{base}/{UCEED}/docs', doc=required_uceed[1:])
with app.app_context():
    assert MsDocConfirm.query.count() == 0
post(s1, f'{base}/{UCEED}/docs', doc=required_uceed + ['nri'], confirm='1')
with app.app_context():
    assert MsDocConfirm.query.count() == 1

# another student's record is untouched; checklists are per exam
post(s2, f'/mentorship/e/{E2}/exams/{UCEED}/focus', on='1')
assert '0 / ' in s2.get(f'/mentorship/e/{E2}/calendar').get_data(as_text=True)
post(s1, f'{base}/{KCET}/focus', on='1')
cal = s1.get(f'/mentorship/e/{E1}/calendar').get_data(as_text=True)
assert cal.count('Registration documents') == 2 and 'Domicile / nativity' in cal

try:
    os.unlink(_db)
except OSError:
    pass
print('exam document checklist checks passed')
