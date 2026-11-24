"""Meeting update import: new KPIs and KPI readings. Also dry-runs Darsh's 23 Nov update when the private file is present. Run from college-predictor/:  python tests/test_meeting_kpis.py"""
import json
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
from app.data.meeting_updates import PACKS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsKpi, MsKpiObs, MsEnrolment, MsProgramme  # noqa: E402
from app.services import meeting_import as mi, meeting_update, roadmap as rmap  # noqa: E402

DOC = {'version': 1, 'kpis': [
    {'category': 'Preparation', 'name': 'Daily practice questions', 'unit': 'a day', 'direction': 'higher', 'baseline': 0, 'target': 8, 'frequency': 'Daily', 'owner': 'Student'},
    {'category': 'Mentorship', 'name': 'Student feedback', 'direction': 'qualitative'}],
    'kpi_updates': [{'name_contains': 'daily practice', 'value': 5, 'note': 'first week', 'observed_on': '2026-12-05'},
                    {'name_contains': 'student feedback', 'text': 'Good', 'observed_on': '2026-12-05'},
                    {'name_contains': 'no such kpi', 'value': 1}]}

# parse: good file, bad file
plan, errs = mi.parse(json.dumps(DOC))
assert not errs and len(plan['kpis']) == 2 and len(plan['kpi_updates']) == 3, errs
bad = json.loads(json.dumps(DOC))
bad['kpis'][0]['category'] = 'Wellness'
bad['kpis'][0]['baseline'] = 'lots'
bad['kpi_updates'][0]['value'] = 'x'
errs = mi.parse(json.dumps(bad))[1]
assert len(errs) >= 3 and any('category' in x for x in errs) and any('not a number' in x for x in errs), errs
assert mi.parse(json.dumps({'version': 1, 'kpis': [{'category': 'Readiness'}]}))[1], 'a KPI needs a name'

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
    uid = U('m@x.com').id

    lines, n = mi.apply(e, plan, uid, dry=True)
    assert n['created'] == 4 and MsKpi.query.count() == 0, 'a check saves nothing'
    lines, n = mi.apply(e, plan, uid)
    ks = {k.name: k for k in MsKpi.query.filter_by(enrolment_id=e.id)}
    assert set(ks) == {'Daily practice questions', 'Student feedback'}, ks
    k = ks['Daily practice questions']
    assert k.current == 5 and k.target == 8 and k.frequency == 'Daily' and k.owner == 'Student', (k.current, k.target)
    assert ks['Student feedback'].qualitative == 'Good' and ks['Student feedback'].direction == 'qualitative'
    assert any(kind == 'warn' and 'no such kpi' in x for kind, x in lines)
    obs = k.observations.all()
    assert [(o.value, o.note) for o in obs] == [(0.0, 'Baseline'), (5.0, 'first week')]
    before = (MsKpi.query.count(), MsKpiObs.query.count())
    mi.apply(e, plan, uid)
    assert before == (MsKpi.query.count(), MsKpiObs.query.count()), 'applying twice adds nothing'

    # Darsh's real 23 Nov update (kept out of git): applied after the 20 Nov pack and the earlier updates
    PRIVATE = os.path.join(ROOT, 'tools', 'meetings', 'private', 'darsh_2026-11-23.json')
    if os.path.exists(PRIVATE):
        e2 = MsEnrolment(student_id=U('d@x.com').id, mentor_id=uid, programme_id=prog.id, preferred_name='Darsh 2')
        db.session.add(e2)
        db.session.commit()
        rmap.create(e2, user_id=uid)
        meeting_update.apply(e2, PACKS['darsh-2026-11-20'], uid)
        for name in ('darsh_2026-11-18.json', 'darsh_2026-11-20.json', 'darsh_2026-11-22.json'):
            p, er = mi.parse(open(os.path.join(ROOT, 'tools', 'meetings', name), encoding='utf-8').read())
            assert not er, (name, er)
            mi.apply(e2, p, uid)
        p, er = mi.parse(open(PRIVATE, encoding='utf-8').read())
        assert not er, er
        assert len(p['actions']) == 12 and len(p['kpis']) == 5 and len(p['kpi_updates']) == 2 and len(p['milestones']) == 5 and p['session']['duration_min'] == 48
        lines, n = mi.apply(e2, p, uid)
        warns = [x for kind, x in lines if kind == 'warn']
        assert not warns, warns
        chk = {k.name: k for k in MsKpi.query.filter_by(enrolment_id=e2.id)}
        assert chk['Weekly mentor check-ins held'].current == 1.0 and chk['Student feedback on the mentoring'].qualitative.startswith('Good')
        again = mi.apply(e2, p, uid)[1]
        assert again['created'] == 0, again
        print('  Darsh 23 Nov update: %d new, then %d on a second apply' % (n['created'], again['created']))
print('meeting KPI import checks passed')
