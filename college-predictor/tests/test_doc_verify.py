"""End-to-end self-check for the document-verification cycle + member profile.

Hermetic: fresh SQLite DB, R2 and email stubbed (touches nothing external).
Run:  ../.venv/bin/python tests/test_doc_verify.py   (from college-predictor/)
"""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import User, DocVerification
from app.routes import members as M

# --- stubs: capture emails, fake R2 (module globals members.py looks up) ------
sent = []
M.send_async = lambda *a, **k: sent.append(a)


class FakeR2:
    store = {}
    def is_configured(self):
        return True
    def upload(self, data, key, mime):
        self.store[key] = (data, mime)
        return key
    def presigned_get(self, key, **k):
        return 'https://r2.example/' + key


M.r2 = FakeR2()

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    db.create_all()
    mk = lambda n, e, t: User(name=n, email=e, tier=t,
                              password_hash=bcrypt.generate_password_hash('x').decode())
    admin, priya, mallory = mk('Admin', 'admin@ea.com', 'admin'), \
        mk('Priya Sharma', 'priya@ex.com', 'premium'), mk('Mallory', 'mal@ex.com', 'premium')
    db.session.add_all([admin, priya, mallory])
    db.session.commit()
    PRIYA = priya.id


def login(c, email):
    c.post('/login', data={'email': email, 'password': 'x'}, follow_redirects=True)


def pdf(name):
    return (io.BytesIO(b'%PDF-1.7\n%%EOF'), name)


ac = app.test_client(); login(ac, 'admin@ea.com')
pc = app.test_client(); login(pc, 'priya@ex.com')
mc = app.test_client(); login(mc, 'mal@ex.com')

# 1) admin requests 3 documents (2 known + 1 custom) -> rows + email to member
sent.clear()
ac.post(f'/admin/documents/{PRIYA}/request',
        data={'doc_types': ['Passport', '10th (SSLC) Marksheet'], 'custom': 'Sponsor Letter'},
        follow_redirects=True)
with app.app_context():
    docs = DocVerification.query.filter_by(user_id=PRIYA).order_by(DocVerification.id).all()
    dids = [d.id for d in docs]
    assert len(docs) == 3, len(docs)
    assert {d.status for d in docs} == {'Requested'}
    assert {d.doc_type for d in docs} == {'Passport', '10th (SSLC) Marksheet', 'Sponsor Letter'}
assert sent and sent[-1][0] == 'priya@ex.com', 'request email should go to the member'

# 2) dedup: re-requesting Passport adds nothing
ac.post(f'/admin/documents/{PRIYA}/request', data={'doc_types': ['Passport']}, follow_redirects=True)
with app.app_context():
    assert DocVerification.query.filter_by(user_id=PRIYA).count() == 3

# 3) ownership: mallory cannot upload to priya's document
r = mc.post(f'/profile/documents/{dids[0]}/upload',
            data={'file': pdf('x.pdf')}, content_type='multipart/form-data')
assert r.status_code == 404, r.status_code

# 4) bad file type rejected
r = pc.post(f'/profile/documents/{dids[0]}/upload',
            data={'file': (io.BytesIO(b'MZbad'), 'virus.exe')},
            content_type='multipart/form-data', follow_redirects=True)
with app.app_context():
    assert db.session.get(DocVerification, dids[0]).status == 'Requested'

# 5) member uploads doc0 -> Submitted + file stored
pc.post(f'/profile/documents/{dids[0]}/upload',
        data={'file': pdf('passport.pdf')}, content_type='multipart/form-data', follow_redirects=True)
with app.app_context():
    d0 = db.session.get(DocVerification, dids[0])
    assert d0.status == 'Submitted' and d0.file_key and d0.file_name == 'passport.pdf'

# 6) submit -> notifies the team inbox (NOTIFY_EMAIL)
sent.clear()
pc.post('/profile/documents/submit', follow_redirects=True)
assert sent and sent[-1][0] == M.NOTIFY_EMAIL, 'submit should notify the team inbox'

# 7) admin approves doc0, rejects doc1 with a comment (emails member each time)
ac.post(f'/admin/documents/doc/{dids[0]}/review', data={'decision': 'approve'}, follow_redirects=True)
pc.post(f'/profile/documents/{dids[1]}/upload',
        data={'file': pdf('10th.pdf')}, content_type='multipart/form-data', follow_redirects=True)
ac.post(f'/admin/documents/doc/{dids[1]}/review',
        data={'decision': 'reject', 'comment': 'Blurry — please re-scan'}, follow_redirects=True)
with app.app_context():
    assert db.session.get(DocVerification, dids[0]).status == 'Approved'
    d1 = db.session.get(DocVerification, dids[1])
    assert d1.status == 'Rejected' and 'Blurry' in d1.admin_comment

# 8) reject with no comment is blocked
ac.post(f'/admin/documents/doc/{dids[1]}/review', data={'decision': 'reject', 'comment': ''},
        follow_redirects=True)
with app.app_context():
    assert db.session.get(DocVerification, dids[1]).status == 'Rejected'  # unchanged

# 9) member re-uploads rejected doc -> Submitted, comment cleared
pc.post(f'/profile/documents/{dids[1]}/upload',
        data={'file': pdf('10th-v2.pdf')}, content_type='multipart/form-data', follow_redirects=True)
with app.app_context():
    d1 = db.session.get(DocVerification, dids[1])
    assert d1.status == 'Submitted' and d1.admin_comment is None

# 10) approve the rest -> the LAST approval fires the "all verified" email
pc.post(f'/profile/documents/{dids[2]}/upload',
        data={'file': pdf('sponsor.pdf')}, content_type='multipart/form-data', follow_redirects=True)
ac.post(f'/admin/documents/doc/{dids[1]}/review', data={'decision': 'approve'}, follow_redirects=True)
sent.clear()
ac.post(f'/admin/documents/doc/{dids[2]}/review', data={'decision': 'approve'}, follow_redirects=True)
with app.app_context():
    assert DocVerification.query.filter_by(user_id=PRIYA).filter(
        DocVerification.status != 'Approved').count() == 0
# two emails on the final approve: the per-doc email + the all-verified email
assert any('verified' in ' '.join(map(str, a)).lower() for a in sent), sent

# 11) admin logs a session; the member sees it on their profile
ac.post(f'/admin/documents/{PRIYA}/meeting',
        data={'title': 'Shortlisting call', 'counsellor': 'Ravi', 'status': 'Completed',
              'notes': 'Discussed 5 colleges'}, follow_redirects=True)
r = pc.get('/profile')
assert b'Shortlisting call' in r.data and b'Discussed 5 colleges' in r.data

# 12) profile renders; old /dashboard redirects to /profile
assert b'Document verification' in pc.get('/profile').data
r = pc.get('/dashboard')
assert r.status_code in (301, 302) and '/profile' in r.headers['Location']

# 13) admin templates render (list + detail), and non-admins are blocked
r = ac.get('/admin/documents')
assert r.status_code == 200 and b'Priya' in r.data and b'All verified' in r.data
r = ac.get(f'/admin/documents/{PRIYA}')
assert r.status_code == 200 and b'Request documents' in r.data and b'Shortlisting call' in r.data
assert pc.get('/admin/documents').status_code == 403      # premium member can't reach admin

os.unlink(_db)
print('all doc-verify E2E checks passed')
