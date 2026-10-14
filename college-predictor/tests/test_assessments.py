"""Assessment results: capture -> member view -> admin/mentor view -> export -> import.

Hermetic (sqlite). Run from college-predictor/:  python tests/test_assessments.py
"""
import io
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
        User(name='Asha Parent', email='asha@ex.com', tier='free', password_hash=pw()),
        User(name='Other Family', email='other@ex.com', tier='free', password_hash=pw()),
    ])
    db.session.commit()

SUBMISSION = {
    'studentInfo': {'name': 'Rohan Kumar', 'age': '15', 'school': 'DPS', 'city': 'Dubai', 'board': 'CBSE', 'currentClass': '10'},
    'studentPreference': 'Commerce',
    'parentInfo': {'name': 'Asha Kumar', 'phone': '+971500000000', 'email': 'asha@ex.com', 'preferredStream': 'Science'},
    'personalityAns': {'p1': 0, 'p2': 2}, 'aptitudeAns': {'a1': 1}, 'applicationAns': {'q1': 3},
    'results': {'scores': {'Science': 60.5, 'Commerce': 30, 'Humanities': 20}, 'percentages': {'Science': 55, 'Commerce': 28, 'Humanities': 17},
                'recommended': 'Science', 'aptitudeScore': 9, 'aptitudeTotal': 15,
                'risks': [{'flag': 'Stream Preference Mismatch', 'detail': 'prefers Commerce', 'severity': 'warning'}],
                'radarData': {'Analytical': 90, 'Creative': 40}},
    'skillGap': [{'skill': 'Maths', 'current': 55, 'required': 80}],
    'topCareers': [{'title': 'Data Scientist'}], 'reportLang': 'en',
}

pub = app.test_client()

# 1) anonymous submission is stored with structured fields, and matched to the member by parent email
r = pub.post('/api/assessments?source=stream-selection', data=json.dumps(SUBMISSION), content_type='text/plain')
assert r.status_code == 200 and r.get_json()['ok'], r.get_data(as_text=True)
rid = r.get_json()['id']
with app.app_context():
    row = db.session.get(AssessmentResult, rid)
    assert row.student_name == 'Rohan Kumar' and row.parent_email == 'asha@ex.com'
    assert row.result_label == 'Science' and abs(row.result_score - 60.0) < 0.1, (row.result_label, row.result_score)
    assert row.scores['Science'] == 55 and row.school == 'DPS' and row.current_class == '10'
    assert row.user_id is not None                       # linked via the parent's email
    assert json.loads(row.payload_json)['personalityAns'] == {'p1': 0, 'p2': 2}   # raw answers kept

# 2) the parent sees it in their profile and can open it; another family cannot
mc = app.test_client(); mc.post('/login', data={'email': 'asha@ex.com', 'password': 'x'})
page = mc.get('/profile').get_data(as_text=True)
assert 'My assessments' in page and 'Stream Selection' in page and 'Rohan Kumar' in page
d = mc.get(f'/profile/assessments/{rid}'); assert d.status_code == 200
body = d.get_data(as_text=True)
assert 'Science' in body and 'Stream Preference Mismatch' in body and 'Data Scientist' in body
oc = app.test_client(); oc.post('/login', data={'email': 'other@ex.com', 'password': 'x'})
assert oc.get(f'/profile/assessments/{rid}').status_code == 404
assert 'Rohan Kumar' not in oc.get('/profile').get_data(as_text=True)
assert pub.get(f'/profile/assessments/{rid}').status_code in (302, 401)

# 3) a logged-in submission links to that account directly
r = mc.post('/api/assessments?source=stream-selection', json={**SUBMISSION, 'studentInfo': {'name': 'Meera'}, 'parentInfo': {}})
assert r.get_json()['linked'] is True and r.get_json()['view_url']

# 4) other assessment pages arrive through /api/leads and are structured too
pub.post('/api/leads?source=branch-fitness', json={'name': 'Kabir', 'email': 'kabir@ex.com', 'topBranch': 'Mechanical', 'score': 71})
with app.app_context():
    b = AssessmentResult.query.filter_by(source='branch-fitness').one()
    assert b.student_name == 'Kabir' and b.result_label == 'Mechanical' and b.result_score == 71
# stream-selection via /api/leads is NOT duplicated (it posts to /api/assessments directly)
pub.post('/api/leads?source=stream-selection', json={'student': {'name': 'X'}, 'results': {}})
with app.app_context():
    assert AssessmentResult.query.filter_by(source='stream-selection').count() == 2

# 5) admin / mentor: list, filter, detail, member record, export
ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})
lst = ac.get('/admin/assessments?source=stream-selection').get_data(as_text=True)
assert 'Rohan Kumar' in lst and 'Kabir' not in lst
assert 'Rohan Kumar' in ac.get(f'/admin/assessments/{rid}').get_data(as_text=True)
with app.app_context():
    asha_id = User.query.filter_by(email='asha@ex.com').one().id
rec = ac.get(f'/admin/documents/{asha_id}').get_data(as_text=True)
assert 'Assessment results' in rec and 'Rohan Kumar' in rec
x = ac.get('/admin/assessments/export.xlsx'); assert x.status_code == 200 and x.data[:2] == b'PK'
assert pub.get('/admin/assessments').status_code in (302, 401, 403)
assert mc.get('/admin/assessments').status_code in (302, 401, 403)

# 6) unlinked result -> admin links it by email
r = pub.post('/api/assessments?source=student-assessment', json={'name': 'Zoya', 'email': 'zoya@nowhere.com'})
zid = r.get_json()['id']
with app.app_context():
    assert db.session.get(AssessmentResult, zid).user_id is None
ac.post(f'/admin/assessments/{zid}/link', data={'email': 'other@ex.com'})
with app.app_context():
    assert db.session.get(AssessmentResult, zid).user_id is not None
assert 'Zoya' in oc.get('/profile').get_data(as_text=True)

# 7) import from a Google-Sheet CSV: idempotent, JSON cells unpacked, linked by email
csv_text = ('Timestamp,Student Name,Student Email,Recommended,Results\n'
            '2026-03-04 10:15:00,Imran,imran@ex.com,Commerce,"{""percentages"":{""Commerce"":61,""Science"":25}}"\n'
            '2026-03-05 11:00:00,Nadia,asha@ex.com,Humanities,\n')
for _ in range(2):
    resp = ac.post('/admin/assessments/import', data={'source': 'stream-selection',
                   'file': (io.BytesIO(csv_text.encode()), 'sheet.csv')}, content_type='multipart/form-data',
                   follow_redirects=True)
    assert resp.status_code == 200
with app.app_context():
    imp = AssessmentResult.query.filter_by(origin='import').all()
    assert len(imp) == 2, len(imp)                       # second run skipped both
    im = next(r for r in imp if r.student_name == 'Imran')
    assert im.created_at.year == 2026 and im.scores.get('Commerce') == 61
    assert next(r for r in imp if r.student_name == 'Nadia').user_id is not None   # matched by email

# 8) the stream-selection page no longer talks to Google
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'app', 'static', 'js', 'stream_selection.js'), encoding='utf-8').read()
assert 'script.google.com' not in js and '/api/assessments' in js

try:
    os.unlink(_db)
except OSError:
    pass
print('all assessment checks passed')
