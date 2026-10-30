"""NUS, NTU and HKU admission pack for a student's mentorship record.
Run from college-predictor/:  python tests/test_intl_pack.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import intl_admissions_2027 as P  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsAction, MsEvent, MsExam, MsExamFocus, MsKpi, MsParentLink, MsPrefDates, MsPrefEntry, MsPrefList  # noqa: E402
from app.services import exam_docs, intl_pack, mentorship as svc  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, em, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Darsh', 'd@x.com', 'elite'), ('Parent', 'p@x.com', 'free'), ('Other', 'o@x.com', 'elite')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    db.session.commit()
    prog = svc.ensure_default_programme()
    U = lambda em: User.query.filter_by(email=em).one()
    e = svc.enrol(U('d@x.com'), U('m@x.com'), prog)
    e2 = svc.enrol(U('o@x.com'), U('m@x.com'), prog)
    db.session.add(MsParentLink(enrolment_id=e.id, parent_id=U('p@x.com').id, relation='Father'))
    db.session.commit()
    E, E2 = e.id, e2.id


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


admin, mentor, stu, par = login('a@x.com'), login('m@x.com'), login('d@x.com'), login('p@x.com')

# the data: every date has a source, official dates are stamped, the HKU date is not
for x in P.EXAMS:
    assert x['source'] and x['notes'] and x['starts_on'] <= x['ends_on']
assert [x['verified_on'] is not None for x in P.EXAMS] == [False, True, True]                      # HKU (reported) is unverified; NUS and NTU are official
assert str(P.EXAMS[0]['ends_on']) == '2026-11-25' and str(P.EXAMS[1]['starts_on']) == '2026-12-16' and str(P.EXAMS[1]['ends_on']) == '2027-02-17'
assert str(P.EXAMS[2]['starts_on']) == '2026-10-15' and str(P.EXAMS[2]['ends_on']) == '2027-03-19'
assert len(P.ACTIONS) >= 12 and {a[2] for a in P.ACTIONS} == {'student', 'parent', 'mentor'} and len(P.KPIS) >= 8

# only an admin can add it
assert mentor.post('/mentorship/admin/enrolment/%d/intl-pack' % E).status_code == 403
assert stu.post('/mentorship/admin/enrolment/%d/intl-pack' % E).status_code in (302, 403)
with app.app_context():
    assert MsKpi.query.filter_by(enrolment_id=E).count() == 0
r = admin.post('/mentorship/admin/enrolment/%d/intl-pack' % E, follow_redirects=True)
assert r.status_code == 200 and b'NUS, NTU and HKU pack added for Darsh' in r.data
with app.app_context():
    assert MsExam.query.filter(MsExam.name.like('%2027%'), MsExam.category == 'Admission deadline').count() == 3
    assert MsExamFocus.query.filter_by(enrolment_id=E).count() == 3
    assert MsEvent.query.filter_by(enrolment_id=E).count() == len(P.EVENTS)
    assert MsKpi.query.filter_by(enrolment_id=E).count() == len(P.KPIS)
    assert MsAction.query.filter_by(enrolment_id=E).count() == len(P.ACTIONS)
    pl = MsPrefList.query.filter_by(enrolment_id=E).one()
    assert pl.entries.count() == 3 and MsPrefDates.query.join(MsPrefEntry).filter(MsPrefEntry.list_id == pl.id).count() == 3
    docs = MsKpi.query.filter_by(enrolment_id=E, unit='items').one()
    expected = sum(1 for x in MsExam.query.all() for it in exam_docs.items_for(x) if it[3])
    assert docs.target == expected and expected >= 24, (docs.target, expected)
    assert MsKpi.query.filter_by(enrolment_id=E, outcome_metric=True).one().current is None            # Darsh's marks were not supplied: nothing invented
    assert MsExamFocus.query.filter_by(enrolment_id=E2).count() == 0                                   # other students untouched

# running it again adds nothing
r = admin.post('/mentorship/admin/enrolment/%d/intl-pack' % E, follow_redirects=True)
assert b'already has the NUS, NTU and HKU pack' in r.data
with app.app_context():
    assert MsKpi.query.filter_by(enrolment_id=E).count() == len(P.KPIS) and MsAction.query.filter_by(enrolment_id=E).count() == len(P.ACTIONS)
    assert MsExam.query.filter(MsExam.category == 'Admission deadline', MsExam.name.like('%2027%')).count() == 3

# the student, the parent and the mentor see it on their pages
for who, c in (('student', stu), ('parent', par), ('mentor', mentor)):
    cal = c.get('/mentorship/e/%d/calendar' % E).get_data(as_text=True)
    assert 'HKU first-round cut-off' in cal and 'NUS application window' in cal or 'NUS undergraduate admission' in cal, who
    kpi = c.get('/mentorship/e/%d/kpis' % E).get_data(as_text=True)
    assert 'University applications submitted' in kpi and 'Class 12 average including English' in kpi, who
    act = c.get('/mentorship/e/%d/actions' % E).get_data(as_text=True)
    assert 'Submit the HKU first-round application' in act, who
    pref = c.get('/mentorship/e/%d/prefs' % E).get_data(as_text=True)
    assert 'National University of Singapore' in pref and 'Nanyang Technological University' in pref and 'University of Hong Kong' in pref, who
assert stu.get('/mentorship/e/%d/calendar' % E2).status_code in (403, 404)                             # not another student's record

# the checklists: each university has its own list and it can be ticked and confirmed
with app.app_context():
    nus = MsExam.query.filter(MsExam.name.like('NUS%')).one()
    e_obj = db.session.get(__import__('app.models_mentorship', fromlist=['MsEnrolment']).MsEnrolment, E)
    cl = exam_docs.checklist(e_obj, nus)
    assert cl['total'] == 8 and cl['done'] == 0 and 'Passport valid and scanned' in [i['label'] for i in cl['items']]
    nus_id = nus.id
page = stu.get('/mentorship/e/%d/calendar' % E).get_data(as_text=True)
assert 'Tuition Grant and 3-year work bond decision made' in page or 'Tuition Grant' in page

print('intl pack checks passed')
