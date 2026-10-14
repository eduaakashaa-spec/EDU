"""Free guides: admin upload -> public tiles -> email-gated download -> leads.

Hermetic (sqlite, no mail transport). Run from college-predictor/:  python tests/test_free_guides.py
"""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
for k in ('RESEND_API_KEY', 'SMTP_HOST'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import FreeGuide, GuideDownload, PageLead, User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='admin@ea.com', tier='admin', password_hash=pw()),
                        User(name='Free', email='free@ex.com', tier='free', password_hash=pw()),
                        User(name='Maya', email='maya@ea.com', tier='ea_mentor', password_hash=pw())])
    db.session.commit()

PDF = b'%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n'
pub = app.test_client()

# empty state renders
assert pub.get('/free-guides').status_code == 200

# only admins can manage
assert pub.get('/admin/free-guides').status_code in (302, 401, 403)
fc = app.test_client(); fc.post('/login', data={'email': 'free@ex.com', 'password': 'x'})
assert fc.get('/admin/free-guides').status_code in (302, 403)
mc = app.test_client(); mc.post('/login', data={'email': 'maya@ea.com', 'password': 'x'})
assert mc.get('/admin/free-guides').status_code in (302, 403)        # EA mentors: not content admin

ac = app.test_client(); ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'})
assert ac.get('/admin/free-guides').status_code == 200

# upload validation: wrong type and fake pdf are rejected
r = ac.post('/admin/free-guides/upload', data={'title': 'Bad', 'file': (io.BytesIO(b'hello'), 'x.exe')},
            content_type='multipart/form-data', follow_redirects=True)
assert b'Upload a PDF' in r.data
r = ac.post('/admin/free-guides/upload', data={'title': 'Fake', 'file': (io.BytesIO(b'not a pdf'), 'x.pdf')},
            content_type='multipart/form-data', follow_redirects=True)
assert b'does not look like a valid' in r.data
with app.app_context():
    assert FreeGuide.query.count() == 0

# real upload
r = ac.post('/admin/free-guides/upload', data={
    'title': 'NRI Admission Guide 2027', 'category': 'NRI & DASA', 'description': 'DASA and CIWG explained',
    'sort_order': '10', 'file': (io.BytesIO(PDF), 'NRI guide.pdf')},
    content_type='multipart/form-data', follow_redirects=True)
assert r.status_code == 200 and b'is live' in r.data
with app.app_context():
    g = FreeGuide.query.one()
    gid = g.id
    assert g.file_size == len(PDF) and g.file_mime == 'application/pdf' and g.active

# public tiles show it, the file bytes are NOT exposed anywhere public
page = pub.get('/free-guides').get_data(as_text=True)
assert 'NRI Admission Guide 2027' in page and 'DASA and CIWG explained' in page and '%PDF' not in page
assert pub.get(f'/admin/free-guides/{gid}/file').status_code in (302, 401, 403)
assert pub.get('/free-guides/get/not-a-real-token').status_code == 404

# the emailed link goes out from info@eduaakashaa.com (replies too)
from app.services import mailer as _mailer
_sent = []
_mailer.send_async = lambda to, subject, text, html=None, **k: _sent.append({'to': to, 'subject': subject, **k})

# gated download: needs name + valid email
assert pub.post(f'/free-guides/{gid}/request', json={'name': '', 'email': 'a@b.com'}).status_code == 400
assert pub.post(f'/free-guides/{gid}/request', json={'name': 'Asha', 'email': 'nope'}).status_code == 400
r = pub.post(f'/free-guides/{gid}/request', json={'name': 'Asha Kumar', 'email': 'ASHA@Example.com', 'phone': '+971500000000'})
assert r.status_code == 200 and r.get_json()['ok']
url = r.get_json()['url']
f = pub.get(url)
assert f.status_code == 200 and f.data == PDF
assert 'attachment' in f.headers['Content-Disposition'] and f.mimetype == 'application/pdf'

assert len(_sent) == 1 and _sent[0]['to'] == 'asha@example.com', _sent
assert _sent[0]['from_addr'] == 'info@eduaakashaa.com' and _sent[0]['reply_to'] == 'info@eduaakashaa.com'
assert 'NRI Admission Guide 2027' in _sent[0]['subject']

# the lead is captured (normalised email) and counted
with app.app_context():
    d = GuideDownload.query.one()
    assert d.email == 'asha@example.com' and d.name == 'Asha Kumar' and d.guide_title == 'NRI Admission Guide 2027'
    assert db.session.get(FreeGuide, gid).download_count == 1
    assert PageLead.query.filter_by(source='free-guide').count() == 1

# honeypot: a bot filling the hidden field gets no lead
before = 0
with app.app_context():
    before = GuideDownload.query.count()
pub.post(f'/free-guides/{gid}/request', json={'name': 'Bot', 'email': 'bot@x.com', 'website': 'http://spam'})
with app.app_context():
    assert GuideDownload.query.count() == before

# admin: downloads list + csv, hide / show, edit & replace file, delete
assert b'asha@example.com' in ac.get('/admin/free-guides/downloads').data
csvr = ac.get('/admin/free-guides/downloads?csv=1')
assert csvr.mimetype == 'text/csv' and b'asha@example.com' in csvr.data
ac.post(f'/admin/free-guides/{gid}/toggle')
assert 'NRI Admission Guide 2027' not in pub.get('/free-guides').get_data(as_text=True)
assert pub.get(url).status_code == 404                   # hidden guides stop serving, even with a link
ac.post(f'/admin/free-guides/{gid}/toggle')
PDF2 = PDF + b'%v2\n'
ac.post(f'/admin/free-guides/{gid}/update', data={'title': 'NRI Admission Guide 2027 (v2)',
        'category': 'NRI & DASA', 'description': 'updated', 'sort_order': '5',
        'file': (io.BytesIO(PDF2), 'v2.pdf')}, content_type='multipart/form-data')
assert pub.get(url).data == PDF2
ac.post(f'/admin/free-guides/{gid}/delete')
with app.app_context():
    assert FreeGuide.query.count() == 0
    assert GuideDownload.query.count() == 1              # the lead survives the guide

# tile image: validated, shown on the tile, cached, removable, and cascades on delete
PNG = bytes([0x89]) + b'PNG' + bytes([0x0d, 0x0a, 0x1a, 0x0a]) + bytes(64)
JPG = bytes([0xff, 0xd8, 0xff, 0xe0]) + bytes(64)
r = ac.post('/admin/free-guides/upload', data={'title': 'With cover', 'category': 'General',
            'file': (io.BytesIO(PDF), 'a.pdf'), 'cover': (io.BytesIO(b'GIF89a-not-allowed'), 'c.gif')},
            content_type='multipart/form-data', follow_redirects=True)
assert b'JPG, PNG or WebP' in r.data
r = ac.post('/admin/free-guides/upload', data={'title': 'With cover', 'category': 'General',
            'file': (io.BytesIO(PDF), 'a.pdf'), 'cover': (io.BytesIO(b'x' * 2_000_000), 'big.png')},
            content_type='multipart/form-data', follow_redirects=True)
assert b'larger than 1 MB' in r.data
with app.app_context():
    assert FreeGuide.query.count() == 0
r = ac.post('/admin/free-guides/upload', data={'title': 'With cover', 'category': 'General',
            'file': (io.BytesIO(PDF), 'a.pdf'), 'cover': (io.BytesIO(PNG), 'c.png')},
            content_type='multipart/form-data', follow_redirects=True)
assert b'is live' in r.data
with app.app_context():
    cid = FreeGuide.query.one().id
c = pub.get(f'/free-guides/cover/{cid}')
assert c.status_code == 200 and c.data == PNG and c.mimetype == 'image/png'
assert 'max-age' in c.headers['Cache-Control'] and c.headers.get('ETag')
assert pub.get(f'/free-guides/cover/{cid}', headers={'If-None-Match': c.headers['ETag']}).status_code == 304
assert f'/free-guides/cover/{cid}' in pub.get('/free-guides').get_data(as_text=True)
assert '1200' in ac.get('/admin/free-guides').get_data(as_text=True)          # recommended size is shown
ac.post(f'/admin/free-guides/{cid}/update', data={'title': 'With cover', 'category': 'General',
        'cover': (io.BytesIO(JPG), 'new.jpg')}, content_type='multipart/form-data')
assert pub.get(f'/free-guides/cover/{cid}').mimetype == 'image/jpeg'
ac.post(f'/admin/free-guides/{cid}/update', data={'title': 'With cover', 'category': 'General', 'remove_cover': '1'})
assert pub.get(f'/free-guides/cover/{cid}').status_code == 404
ac.post(f'/admin/free-guides/{cid}/delete')

# linked from the site menu and footer
assert '/free-guides' in pub.get('/').get_data(as_text=True)

try:
    os.unlink(_db)
except OSError:
    pass
print('all free-guide checks passed')
