"""Darsh's meeting report of 22 Nov 2026 (tools/meetings/darsh_2026-11-22.json), applied after the 18 and 20 Nov updates. Run from college-predictor/:  python tests/test_darsh_1122.py"""
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
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsAction, MsEnrolment, MsEvent, MsMilestone, MsProgramme, MsSession  # noqa: E402
from app.services import meeting_import as mi  # noqa: E402
from app.services import roadmap as rmap  # noqa: E402


def load(name):
    return open(os.path.join(ROOT, 'tools', 'meetings', name), encoding='utf-8').read()


T18, T20, T22 = load('darsh_2026-11-18.json'), load('darsh_2026-11-20.json'), load('darsh_2026-11-22.json')
plan, errs = mi.parse(T22)
assert not errs, errs
assert len(plan['actions']) == 12 and len(plan['events']) == 8 and len(plan['milestones']) == 11 and plan['groups']['HKU']['status'] == 'On hold' and plan['groups']['NTU']['status'] == 'Primary'
assert 'WhatsApp' not in plan['session']['shared_summary'] and 'password' not in T22.lower() and 'drive.google' not in T22.lower()        # family text keeps to the portal wording; nothing secret
assert not plan['session']['mentor_notes'] and 'transfer' not in T22.lower() and 'deposit is' not in T22.lower()      # the repo copy carries no private payment notes
PRIVATE = os.path.join(ROOT, 'tools', 'meetings', 'private', 'darsh_2026-11-22.full.json')       # the mentor's full copy is kept out of git
if os.path.exists(PRIVATE):
    _pp, _pe = mi.parse(open(PRIVATE, encoding='utf-8').read())
    assert not _pe and _pp['session']['mentor_notes'].startswith('PRIVATE') and len(_pp['actions']) == 13

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    for n, em, t in (('Mentor', 'm@x.com', 'ea_mentor'), ('Darsh', 'd@x.com', 'elite')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    prog = MsProgramme(name='Demo')
    db.session.add(prog)
    db.session.commit()
    U = lambda em: User.query.filter_by(email=em).one()  # noqa: E731
    e = MsEnrolment(student_id=U('d@x.com').id, mentor_id=U('m@x.com').id, programme_id=prog.id, preferred_name='Darsh')
    db.session.add(e)
    db.session.commit()
    rmap.create(e, user_id=U('m@x.com').id)
    for text in (T18, T20, T22):
        p, er = mi.parse(text)
        assert not er, er
        mi.apply(e, p, U('m@x.com').id)
    db.session.commit()

    sess = MsSession.query.filter_by(enrolment_id=e.id, title=plan['session']['title']).one()
    assert sess.status == 'Completed' and sess.parent_visible and 'HKU' in sess.shared_summary
    titles = {a.title for a in MsAction.query.filter_by(enrolment_id=e.id)}
    assert 'HKU decision: apply in the first round or formally drop it' in titles
    hku = MsAction.query.filter_by(enrolment_id=e.id).filter(MsAction.title.like('HKU decision%')).one()
    assert hku.owner == 'parent' and hku.priority == 'High' and hku.due_date.isoformat() == '2026-11-24'
    ev = {x.title for x in MsEvent.query.filter_by(enrolment_id=e.id)}
    assert 'HKU decision due: apply or drop' in ev and 'NUS: application window opens' in ev

    # applying the same report again adds nothing
    before = (MsSession.query.count(), MsAction.query.count(), MsEvent.query.count(), MsMilestone.query.count())
    p, er = mi.parse(T22)
    mi.apply(e, p, U('m@x.com').id)
    db.session.commit()
    assert before == (MsSession.query.count(), MsAction.query.count(), MsEvent.query.count(), MsMilestone.query.count()), 'a second apply must add nothing'
print('darsh 22 nov report checks passed')
