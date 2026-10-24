"""WhatsApp group per member: who can edit, link validation, and the send-to-group buttons in staff message sections.
Run from college-predictor/:  python tests/test_wa_group.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.futureready import engine
from app.futureready.models import FrProfile
from app.models import User
from app.models_mentorship import MemberWaGroup
from app.services import mentorship as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'),
                    ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Par One', 'p1@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    u = lambda e: User.query.filter_by(email=e).one()
    prog = svc.ensure_default_programme()
    e1 = svc.enrol(u('s1@x.com'), u('m@x.com'), prog)
    e2 = svc.enrol(u('s2@x.com'), u('m2@x.com'), prog)
    engine.seed_content()
    db.session.add(FrProfile(user_id=u('s2@x.com').id, mentor_id=u('m2@x.com').id, grade=8))
    db.session.commit()
    E1, S1, S2 = e1.id, u('s1@x.com').id, u('s2@x.com').id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1 = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com'))
LINK = 'https://chat.whatsapp.com/AbCdEfGh12345678'
save = lambda c, uid, **d: c.post(f'/wagroup/{uid}', data=d, follow_redirects=True)

# validation: only official invite links are accepted
r = save(mentor, S1, group_name='Bad', invite_link='https://evil.example.com/x', next='/')
assert b'invite link' in r.data
with app.app_context():
    assert MemberWaGroup.query.count() == 0
# permissions: students, other mentors and anonymous cannot edit; the member's own mentor and admin can
assert s1.post(f'/wagroup/{S1}', data={'invite_link': LINK}).status_code == 403
assert mentor2.post(f'/wagroup/{S1}', data={'invite_link': LINK}).status_code == 403
assert app.test_client().post(f'/wagroup/{S1}', data={'invite_link': LINK}).status_code in (302, 401)
assert mentor.post(f'/wagroup/{S1}', data={'group_name': 'Stu One mentoring', 'invite_link': 'chat.whatsapp.com/AbCdEfGh12345678', 'note': 'Student, parent, mentor'}).status_code == 302
with app.app_context():
    g = MemberWaGroup.query.filter_by(user_id=S1).one()
    assert g.invite_link == LINK and g.group_name == 'Stu One mentoring'
assert mentor.post(f'/wagroup/{S2}', data={'invite_link': LINK}).status_code == 403     # not their member
assert mentor2.post(f'/wagroup/{S2}', data={'group_name': 'FR group', 'invite_link': LINK}).status_code == 302   # FutureReady mentor
assert admin.post(f'/wagroup/{S1}', data={'group_name': 'Renamed', 'invite_link': LINK}).status_code == 302
with app.app_context():
    assert MemberWaGroup.query.filter_by(user_id=S1).one().group_name == 'Renamed' and MemberWaGroup.query.count() == 2

# message sections show the buttons to staff only
post_msg = mentor.post(f'/mentorship/e/{E1}/messages/post', data={'audience': 'all', 'body': 'Hello families, session on Friday'}, follow_redirects=True)
msgs = mentor.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
assert 'wag-send' in msgs and LINK in msgs and 'data-wag-source="#ms-msg-body"' in msgs and 'To group' in msgs
assert 'Open group' in msgs
st = s1.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
assert 'wag-send' not in st and LINK not in st and 'WhatsApp group' not in st               # students never see the group card or buttons
acts = mentor.get(f'/mentorship/e/{E1}/actions').get_data(as_text=True)
assert 'wag-send' in acts and LINK in acts
# internal notes get no group button
mentor.post(f'/mentorship/e/{E1}/messages/post', data={'audience': 'internal', 'body': 'INTERNAL-ONLY-NOTE'})
page = mentor.get(f'/mentorship/e/{E1}/messages').get_data(as_text=True)
i = page.index('INTERNAL-ONLY-NOTE')
assert 'wag-send' not in page[i:i + 300].split('ms-msg')[0]
# admin messages page
r = admin.get('/admin/messages?template=welcome&group=all')
assert r.status_code == 200 and b'wag-send' in r.data and b'To group' in r.data
# FutureReady mentor workspace
with app.app_context():
    PID = FrProfile.query.filter_by(user_id=S2).one().id
fr = mentor2.get(f'/futureready/s/{PID}/mentor').get_data(as_text=True)
assert 'WhatsApp group' in fr and 'wag-send' in fr and LINK in fr
assert app.test_client().get('/static/js/wa_group.js').status_code == 200
print('WhatsApp group checks passed')
