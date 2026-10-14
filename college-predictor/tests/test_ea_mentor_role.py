"""EA mentor role: staff access to student records, no access to money / admin;
alumni mentors (College Guides) remain a different role.

Hermetic (sqlite). Run from college-predictor/:  python tests/test_ea_mentor_role.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import AssessmentResult, User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([
        User(name='Admin', email='admin@ea.com', tier='admin', password_hash=pw()),
        User(name='Maya Mentor', email='maya@ea.com', tier='ea_mentor', password_hash=pw()),
        User(name='Alum Guide', email='guide@college.edu', tier='mentor', password_hash=pw()),
        User(name='Asha Parent', email='asha@ex.com', tier='premium', password_hash=pw()),
        User(name='Free User', email='free@ex.com', tier='free', password_hash=pw()),
    ])
    db.session.commit()

# one student assessment to look at
pub = app.test_client()
rid = pub.post('/api/assessments?source=stream-selection', json={
    'studentInfo': {'name': 'Rohan'}, 'parentInfo': {'email': 'asha@ex.com'},
    'results': {'recommended': 'Science', 'percentages': {'Science': 60}}}).get_json()['id']

with app.app_context():
    maya = User.query.filter_by(email='maya@ea.com').one()
    guide = User.query.filter_by(email='guide@college.edu').one()
    assert maya.is_ea_mentor and maya.is_staff and not maya.is_admin and not maya.is_mentor
    assert guide.is_mentor and not guide.is_ea_mentor and not guide.is_staff    # alumni role is separate
    assert maya.is_premium                       # staff can open member tools
    asha_id = User.query.filter_by(email='asha@ex.com').one().id


def login(email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'x'})
    return c


mc = login('maya@ea.com')

# --- EA mentor CAN work with student records ---------------------------------
assert mc.get('/mentor-desk').status_code == 200
assert 'Rohan' in mc.get('/admin/assessments').get_data(as_text=True)
d = mc.get(f'/admin/assessments/{rid}')
assert d.status_code == 200 and 'Link to member' not in d.get_data(as_text=True)   # read-only for mentors
assert mc.get('/admin/documents').status_code == 200
assert mc.get(f'/admin/documents/{asha_id}').status_code == 200
assert mc.get('/admin/onboarding').status_code == 200
assert mc.post(f'/admin/documents/{asha_id}/meeting',
               data={'title': 'Stream chat', 'status': 'Completed'}).status_code in (302, 303)
# nav shows the reduced mentor menu, not the admin one
nav = mc.get('/admin/assessments').get_data(as_text=True)
assert 'Mentor sections' in nav and 'Admin sections' not in nav

# --- ...but NOT admin-only areas ----------------------------------------------
for path in ['/admin', '/admin/users', '/admin/membership', '/admin/invoices', '/admin/templates',
             '/admin/announcements', '/admin/assessments/export.xlsx', '/admin/assessments/import',
             '/mentorship-templates']:
    r = mc.get(path)
    assert r.status_code in (302, 403, 404), (path, r.status_code)
assert mc.post(f'/admin/assessments/{rid}/link', data={'email': 'asha@ex.com'}).status_code in (302, 403)
assert mc.post(f'/admin/assessments/{rid}/delete').status_code in (302, 403)
with app.app_context():
    assert db.session.get(AssessmentResult, rid) is not None           # nothing was deleted
# cannot promote themselves or others
assert mc.post('/admin/users/1/update', data={'tier': 'admin'}).status_code in (302, 403)
with app.app_context():
    assert User.query.filter_by(email='maya@ea.com').one().tier == 'ea_mentor'

# --- alumni mentors and ordinary members have NO staff access -----------------
for who in ('guide@college.edu', 'asha@ex.com', 'free@ex.com'):
    c = login(who)
    for path in ['/mentor-desk', '/admin/assessments', '/admin/documents', f'/admin/documents/{asha_id}', '/admin/onboarding']:
        r = c.get(path)
        assert r.status_code in (302, 403), (who, path, r.status_code)

# --- admin still has everything, and can assign the role ---------------------
ac = login('admin@ea.com')
assert ac.get('/admin/assessments/export.xlsx').status_code == 200
assert ac.get('/admin/users').status_code == 200
assert 'ea_mentor' in ac.get('/admin/users').get_data(as_text=True)
with app.app_context():
    uid = User.query.filter_by(email='free@ex.com').one().id
ac.post(f'/admin/users/{uid}/update', data={'tier': 'ea_mentor'})
with app.app_context():
    assert User.query.get(uid).tier == 'ea_mentor'
assert 'Admin sections' in ac.get('/admin/assessments').get_data(as_text=True)

# --- member blasts never go to staff or alumni mentors ------------------------
from app.routes import admin_portal as AP
with app.app_context():
    emails = AP._announcement_recipients('all')
    assert 'asha@ex.com' in emails and 'maya@ea.com' not in emails and 'guide@college.edu' not in emails

# --- login lands an EA mentor on their desk -----------------------------------
c = app.test_client()
r = c.post('/login', data={'email': 'maya@ea.com', 'password': 'x'})
assert r.status_code == 302 and r.headers['Location'].endswith('/mentor-desk'), r.headers.get('Location')

try:
    os.unlink(_db)
except OSError:
    pass
print('all ea-mentor role checks passed')
