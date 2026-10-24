"""Bank-transfer details in the Elite Mentorship scope templates: placeholders when unset, saved company details when set.
Run from college-predictor/:  python tests/test_bank_in_templates.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import User
from app.models_membership import Setting
from app.services.company import fill_bank_details
from app.services.email_templates import EMAIL_TEMPLATES

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='a@x.com', tier='admin', password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

c = app.test_client()
assert c.post('/login', data={'email': 'a@x.com', 'password': 'x'}).status_code == 302
page = c.get('/mentorship-templates').get_data(as_text=True)
assert 'BANK TRANSFER DETAILS' in page and '[Account Number]' in page and '[IFSC]' in page          # nothing invented when unset
adm = c.get('/admin/templates').get_data(as_text=True)
assert 'bank_ifsc' in adm and '[IFSC]' in adm

with app.app_context():
    for k, v in (('bank_ac_name', 'EduAakashaa Test Pvt Ltd'), ('bank_name', 'Test Bank'), ('bank_branch', 'Chennai'), ('bank_ac_no', '1234567890'), ('bank_ifsc', 'TEST0001234')):
        db.session.add(Setting(key=k, value=v))
    db.session.commit()
page = c.get('/mentorship-templates').get_data(as_text=True)
assert '1234567890' in page and 'TEST0001234' in page and '[Account Number]' not in page and 'EduAakashaa Test Pvt Ltd' in page
adm = c.get('/admin/templates').get_data(as_text=True)
assert '1234567890' in adm and 'TEST0001234' in adm
with app.app_context():
    t = next(t for t in EMAIL_TEMPLATES if t['key'] == 'mp_scope')
    v = t['versions'][0]
    assert 'Bank transfer details'.upper() in v['text'] and '{bank_ac_no}' in v['text'] and '{bank_ac_no}' in v['wa']
    filled = fill_bank_details(t)
    assert {f['key']: f['default'] for f in filled['versions'][0]['fields']}['bank_ifsc'] == 'TEST0001234'
    assert next(f for f in v['fields'] if f['key'] == 'bank_ifsc')['default'] == '[IFSC]'                # original registry untouched
print('bank details in templates: checks passed')
