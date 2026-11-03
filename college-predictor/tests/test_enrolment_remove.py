"""Admin can remove an assigned programme from the member portal (soft, restorable)."""
import os
import sys
os.environ.setdefault('FLASK_DEBUG', '1')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.extensions import db
from app.models import User
from app.models_mentorship import MsEnrolment, MsProgramme
from app.services import mentorship as svc

app = create_app()
with app.app_context():
    db.create_all()
    adm = User.query.filter_by(email='rm-admin@test.local').first() or User(name='Rm Admin', email='rm-admin@test.local', tier='admin', password_hash='x')
    stu = User.query.filter_by(email='rm-stu@test.local').first() or User(name='Rm Student', email='rm-stu@test.local', tier='elite', password_hash='x')
    db.session.add_all([adm, stu]); db.session.flush()
    prog = MsProgramme.query.first() or MsProgramme(name='Rm Prog'); db.session.add(prog); db.session.flush()
    e = svc.enrol(stu, None, prog); db.session.commit()
    eid, aid, sid = e.id, adm.id, stu.id

def login(c, uid):
    with c.session_transaction() as s:
        s['_user_id'] = str(uid); s['_fresh'] = True

c = app.test_client(); login(c, aid)
r = c.post(f'/mentorship/admin/enrolment/{eid}/remove'); assert r.status_code == 302
with app.app_context():
    e = db.session.get(MsEnrolment, eid); assert e.status == 'Removed'
    assert svc.role_for(e, db.session.get(User, sid)) is None and svc.role_for(e, db.session.get(User, aid)) == 'admin'
cs = app.test_client(); login(cs, sid)
assert cs.get(f'/mentorship/e/{eid}/home').status_code in (403, 404)
assert b'Remove' in c.get('/mentorship/admin').data and b'Restore to member portal' in c.get('/mentorship/admin').data
c.post(f'/mentorship/admin/enrolment/{eid}/restore')
with app.app_context():
    e = db.session.get(MsEnrolment, eid); assert e.status == 'Active' and svc.role_for(e, db.session.get(User, sid)) == 'student'
    db.session.delete(e); db.session.commit()
    for em in ('rm-admin@test.local', 'rm-stu@test.local'):
        u = User.query.filter_by(email=em).first()
        if u: db.session.delete(u)
    db.session.commit()
print('enrolment remove checks passed')
