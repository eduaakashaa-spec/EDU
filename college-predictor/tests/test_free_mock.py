"""EduPulse free sample mock tests: phone and email gate, one 10-question sample per exam, server-side grading, leads saved."""
import json
import os
import sys
os.environ.setdefault('FLASK_DEBUG', '1')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.extensions import db
from app.models import PageLead
from app.services import free_mock as fm

app = create_app()
with app.app_context():
    db.create_all()
    for e in fm.EXAMS:
        s = fm.sample(e['key'])
        assert len(s) == 10 and all(len(q['opts']) == 4 and 0 <= q['ans'] < 4 for q in s), e['key']
        assert len({q['id'] for q in s}) == 10, e['key']
        assert not any('ans' in q or 'why' in q for q in fm.public_view(e['key']))
    before = PageLead.query.filter_by(source='edupulse-free-mock').count()

c = app.test_client()
home = c.get('/edupulse-free-mock-tests/').get_data(as_text=True)
assert 'Unlock the free tests' in home and 'EduPulse' in home
assert c.get('/edupulse-free-mock-tests/jee').status_code == 302                        # locked until phone and email
assert c.post('/edupulse-free-mock-tests/start', data={'email': 'bad', 'phone': '123'}).status_code == 400
assert c.post('/edupulse-free-mock-tests/start', data={'email': 'a@b.co', 'phone': 'abc'}).status_code == 400
assert c.post('/edupulse-free-mock-tests/start', data={'email': 'a@b.co', 'phone': '98765 43210', 'website': 'spam'}).status_code == 302
assert c.get('/edupulse-free-mock-tests/jee').status_code == 302                        # honeypot did not unlock
r = c.post('/edupulse-free-mock-tests/start', data={'name': 'Test Visitor', 'email': 'fm-test@example.com', 'phone': '+91 98765-43210'})
assert r.status_code == 302
home = c.get('/edupulse-free-mock-tests/').get_data(as_text=True)
assert 'Start free sample' in home and 'Welcome, Test' in home
for e in fm.EXAMS:
    page = c.get('/edupulse-free-mock-tests/' + e['key'])
    assert page.status_code == 200, e['key']
    html = page.get_data(as_text=True)
    assert html.count('type="radio"') == 40 and 'Why:' not in html, e['key']
assert c.get('/edupulse-free-mock-tests/nope').status_code == 404
with app.app_context():
    s = fm.sample('tn10')
    form = {'a_' + q['id']: str(q['ans']) for q in s[:7]}
    form['a_' + s[7]['id']] = str((s[7]['ans'] + 1) % 4)
r = c.post('/edupulse-free-mock-tests/tn10', data=form)
html = r.get_data(as_text=True)
assert r.status_code == 200 and 'You scored 7 out of 10' in html and 'Why:' in html
assert 'Next: ' in html and '7/10' in c.get('/edupulse-free-mock-tests/').get_data(as_text=True)
with app.app_context():
    rows = PageLead.query.filter_by(source='edupulse-free-mock').order_by(PageLead.id).all()
    assert len(rows) == before + 2, len(rows) - before
    assert rows[-2].phone == '+919876543210' and rows[-2].email == 'fm-test@example.com'
    assert json.loads(rows[-1].payload_json)['right'] == 7
    for x in rows[before:]:
        db.session.delete(x)
    db.session.commit()
for u in ('/members-registration', '/'):
    assert c.get(u).status_code == 200
assert 'free_mock' not in c.get('/members-registration').get_data(as_text=True) or b'edupulse-free-mock-tests' in c.get('/members-registration').data
print('free mock checks passed')
