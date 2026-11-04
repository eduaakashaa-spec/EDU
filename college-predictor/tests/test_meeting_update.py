"""Remove the NUS, NTU and HKU pack from a student, and apply a meeting update (Yusra, 2 Nov 2026).
Run from college-predictor/:  python tests/test_meeting_update.py"""
import os
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import intl_admissions_2027 as P  # noqa: E402
from app.data.meeting_updates import PACKS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import (MsAction, MsAudit, MsEvent, MsExam, MsExamFocus, MsKpi, MsPrefEntry, MsPrefList, MsProgramme, MsSession)  # noqa: E402
from app.services import intl_pack, meeting_update, mentorship as svc  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    for n, em, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Yusra Kazi', 'y@x.com', 'elite'), ('Other', 'o@x.com', 'elite')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    db.session.commit()
    U = lambda em: User.query.filter_by(email=em).one()  # noqa: E731
    elite = svc.ensure_default_programme()
    svc.ensure_addon_programmes()
    barch = MsProgramme.query.filter(MsProgramme.name.like('B.Arch%')).one()
    uceed = MsProgramme.query.filter(MsProgramme.name.like('UCEED%')).one()
    e = svc.enrol(U('y@x.com'), U('m@x.com'), elite)
    eb = svc.enrol(U('y@x.com'), U('m@x.com'), barch)
    eu = svc.enrol(U('y@x.com'), U('m@x.com'), uceed)
    other = svc.enrol(U('o@x.com'), U('m@x.com'), elite)
    # one KPI and one action that are not part of any pack: they must survive
    db.session.add(MsKpi(enrolment_id=e.id, category='Preparation', name='My own KPI', unit='x', direction='higher'))
    db.session.add(MsAction(enrolment_id=e.id, title='My own action', owner='student'))
    db.session.commit()
    E, EB, EU, EO = e.id, eb.id, eu.id, other.id


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


admin, mentor = login('a@x.com'), login('m@x.com')

# ---- remove the NUS, NTU and HKU pack ----------------------------------------------------------------------------------------------------
with app.app_context():
    assert not intl_pack.present(db.session.get(type(e), E))
r = admin.post('/mentorship/admin/enrolment/%d/intl-pack' % E, follow_redirects=True)
assert r.status_code == 200 and b'pack added' in r.data
with app.app_context():
    ee = db.session.get(type(e), E)
    assert intl_pack.present(ee)
    n_k, n_a = MsKpi.query.filter_by(enrolment_id=E).count(), MsAction.query.filter_by(enrolment_id=E).count()
    assert n_k == len(P.KPIS) + 1 and n_a == len(P.ACTIONS) + 1 and MsPrefList.query.filter_by(enrolment_id=E).count() == 1
# the same pack on another student, to show it stays untouched
admin.post('/mentorship/admin/enrolment/%d/intl-pack' % EO)
assert mentor.post('/mentorship/admin/enrolment/%d/intl-pack/remove' % E).status_code == 403
with app.app_context():
    assert MsKpi.query.filter_by(enrolment_id=E).count() == n_k                               # a mentor cannot remove it
r = admin.post('/mentorship/admin/enrolment/%d/intl-pack/remove' % E, follow_redirects=True)
assert r.status_code == 200 and b'pack removed from Yusra Kazi' in r.data
with app.app_context():
    assert not intl_pack.present(db.session.get(type(e), E))
    assert [k.name for k in MsKpi.query.filter_by(enrolment_id=E).all()] == ['My own KPI']
    assert [a.title for a in MsAction.query.filter_by(enrolment_id=E).all()] == ['My own action']
    assert MsPrefList.query.filter_by(enrolment_id=E).count() == 0 and MsPrefEntry.query.count() == len(P.LIST)           # the other student's entries remain
    assert MsExamFocus.query.filter_by(enrolment_id=E).count() == 0 and MsEvent.query.filter_by(enrolment_id=E).count() == 0
    assert MsExam.query.filter(MsExam.name.in_([x['name'] for x in P.EXAMS])).count() == len(P.EXAMS)                    # the shared catalogue stays
    assert MsKpi.query.filter_by(enrolment_id=EO).count() == len(P.KPIS) and MsAction.query.filter_by(enrolment_id=EO).count() == len(P.ACTIONS)
    assert MsAudit.query.filter_by(enrolment_id=E, action='intl_pack.removed').count() == 1
r = admin.post('/mentorship/admin/enrolment/%d/intl-pack/remove' % E, follow_redirects=True)
assert b'does not have the NUS, NTU and HKU pack' in r.data                                                                # a second press does nothing
with app.app_context():
    assert intl_pack.remove(db.session.get(type(e), E))['kpis'] == 0

# ---- the meeting update: the data ---------------------------------------------------------------------------------------------------------
elite_pack, addon_pack = PACKS['yusra-2026-11-02-elite'], PACKS['yusra-2026-11-02-addons']
assert len(elite_pack['kpis']) >= 10 and len(elite_pack['actions']) >= 15 and len(elite_pack['sessions']) >= 5
assert {a[2] for a in elite_pack['actions']} == {'student', 'parent', 'mentor'}
blob = repr(elite_pack) + repr(addon_pack)
assert 'WhatsApp group chat' not in blob and 'whatsapp group chat' not in blob.lower()                                   # portal wording rule
for k in elite_pack['kpis']:
    assert len(k) == 13 and k[1] and k[0] in ('Preparation', 'Readiness', 'Mentorship', 'Performance')
text_for_family = repr(elite_pack['meeting']['summary']) + repr(elite_pack['actions']) + repr(elite_pack['sessions'])
assert 'first instalment' not in text_for_family and 'pays the first' not in text_for_family                              # payment stays in the private notes

# ---- the Elite enrolment ------------------------------------------------------------------------------------------------------------------
with app.app_context():
    # an older UCEED action and KPI and a session-slot action, to be retired by the update
    db.session.add(MsAction(enrolment_id=E, title='Start the UCEED registration with Yusra', owner='mentor', priority='High'))
    db.session.add(MsAction(enrolment_id=E, title='Block fixed weekly study slots around tuition', owner='student'))
    db.session.add(MsAction(enrolment_id=E, title='Pull Class 11 unit-test marks by subject', owner='parent'))
    db.session.add(MsKpi(enrolment_id=E, category='Readiness', name='UCEED registration completed by 31 Oct', unit='done', direction='milestone'))
    db.session.commit()
r = mentor.post('/mentorship/admin/enrolment/%d/meeting-update' % E, data={'pack': elite_pack['key']})
assert r.status_code == 403
r = admin.post('/mentorship/admin/enrolment/%d/meeting-update' % E, data={'pack': elite_pack['key']}, follow_redirects=True)
assert r.status_code == 200 and b'meeting logged' in r.data and b'KPIs added' in r.data
with app.app_context():
    ee = db.session.get(type(e), E)
    s = ee.sessions.filter(MsSession.title.like('Follow-up call with Navid%')).one()
    assert s.status == 'Completed' and s.kind == 'follow-up' and s.actual_at.date() == date(2026, 11, 2) and s.duration_min == 48
    assert 'UCEED is dropped' in s.shared_summary and 'first instalment' in s.mentor_notes and 'first instalment' not in s.shared_summary
    planned = ee.sessions.filter(MsSession.status == 'Planned', MsSession.kind == 'extra').all()
    assert len(planned) == len(elite_pack['sessions']) and all(x.agenda and x.deliverable for x in planned)
    names = {k.name: k for k in MsKpi.query.filter_by(enrolment_id=E).all()}
    assert 'EduPulse practice time' in names and names['Pre-board marks (Physics, Chemistry, Maths)'].baseline == 56.8 and names['Pre-board marks (Physics, Chemistry, Maths)'].outcome_metric
    assert names['UCEED registration completed by 31 Oct'].status == 'Archived' and 'UCEED is dropped' in names['UCEED registration completed by 31 Oct'].notes
    assert names['My own KPI'].status == 'Active'
    acts = {a.title: a for a in MsAction.query.filter_by(enrolment_id=E).all()}
    assert acts['Start the UCEED registration with Yusra'].status == 'Cancelled' and 'not interested in UI/UX' in acts['Start the UCEED registration with Yusra'].mentor_feedback
    assert acts['Block fixed weekly study slots around tuition'].status == 'Cancelled'
    assert acts['Pull Class 11 unit-test marks by subject'].status != 'Cancelled' and 'pre-board marks' in acts['Pull Class 11 unit-test marks by subject'].mentor_feedback
    assert acts['My own action'].status == 'Not Started'
    assert acts['Post your physics, chemistry and maths topics as easy, medium or hard'].due_date == date(2026, 11, 17) and acts['Start EduPulse daily practice and weekly reinforcement'].recurrence == 'weekly'
    assert MsEvent.query.filter_by(enrolment_id=E).count() == len(elite_pack['events'])
    before = (ee.sessions.count(), MsKpi.query.filter_by(enrolment_id=E).count(), MsAction.query.filter_by(enrolment_id=E).count())
r = admin.post('/mentorship/admin/enrolment/%d/meeting-update' % E, data={'pack': elite_pack['key']}, follow_redirects=True)
assert b'nothing new to add' in r.data
with app.app_context():
    ee = db.session.get(type(e), E)
    assert (ee.sessions.count(), MsKpi.query.filter_by(enrolment_id=E).count(), MsAction.query.filter_by(enrolment_id=E).count()) == before          # safe to repeat
    assert MsAudit.query.filter_by(enrolment_id=E, action='meeting_update.applied').count() == 2

# ---- the add-on enrolments ----------------------------------------------------------------------------------------------------------------
with app.app_context():
    paper2 = db.session.get(type(e), EB).sessions.filter(MsSession.title.like('Paper 2A mathematics%')).one()
    old_agenda = paper2.agenda
r = admin.post('/mentorship/admin/enrolment/%d/meeting-update' % EB, data={'pack': addon_pack['key']}, follow_redirects=True)
assert r.status_code == 200 and b'session details updated' in r.data
with app.app_context():
    eb2 = db.session.get(type(e), EB)
    p2 = eb2.sessions.filter(MsSession.title.like('Paper 2A mathematics%')).one()
    assert p2.agenda.startswith(old_agenda or '') and 'Update 2 Nov 2026: ' in p2.agenda and 'topic comfort map' in p2.agenda
    cal = eb2.sessions.filter(MsSession.title.like('Application calendar%')).one()
    assert 'Remove UCEED' in cal.agenda
    assert eb2.sessions.filter(MsSession.status == 'Cancelled').count() == 0                                                        # a B.Arch add-on is not cancelled
    n_notes = sum(s.agenda.count('Update 2 Nov 2026: ') for s in eb2.sessions.all() if s.agenda)
    assert n_notes == 9 and all(s.agenda.count('Update 2 Nov 2026: ') <= 1 for s in eb2.sessions.all() if s.agenda)      # nine rules, one session each
r = admin.post('/mentorship/admin/enrolment/%d/meeting-update' % EB, data={'pack': addon_pack['key']}, follow_redirects=True)
assert b'nothing new to add' in r.data
with app.app_context():
    eb2 = db.session.get(type(e), EB)
    assert sum(s.agenda.count('Update 2 Nov 2026: ') for s in eb2.sessions.all() if s.agenda) == n_notes                          # appended once
r = admin.post('/mentorship/admin/enrolment/%d/meeting-update' % EU, data={'pack': addon_pack['key']}, follow_redirects=True)
assert b'sessions cancelled' in r.data
with app.app_context():
    eu2 = db.session.get(type(e), EU)
    assert eu2.sessions.filter(MsSession.status == 'Planned').count() == 0 and eu2.sessions.filter(MsSession.status == 'Cancelled').count() == eu2.sessions.count() > 0
    assert 'not interested in UI/UX' in eu2.sessions.first().mentor_notes
# the admin screen offers both buttons
page = admin.get('/mentorship/admin').get_data(as_text=True)
assert 'Remove NUS, NTU and HKU admission pack' in page and 'Apply meeting update' in page and 'yusra-2026-11-02-elite' in page
assert admin.post('/mentorship/admin/enrolment/%d/meeting-update' % E, data={'pack': 'nope'}, follow_redirects=True).status_code == 200
try:
    os.remove(_db)
except OSError:
    pass
print('meeting update checks passed')
