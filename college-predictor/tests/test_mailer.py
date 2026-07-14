"""Self-check for the mailer transport logic (Resend HTTP API + SMTP fallback).

Hermetic: no network — the Resend call is stubbed at urllib. Run from college-predictor/:
    ../.venv/bin/python tests/test_mailer.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for k in ('RESEND_API_KEY', 'MAIL_FROM', 'SMTP_HOST', 'SMTP_USER', 'SMTP_PASS',
          'SMTP_FROM', 'MAIL_TRANSPORT'):
    os.environ.pop(k, None)

from app.services import mailer

# --- transport selection ----------------------------------------------------
assert mailer.transport() is None and not mailer.is_configured()

os.environ.update({'SMTP_HOST': 'smtp.gmail.com', 'SMTP_USER': 'u@x.com', 'SMTP_PASS': 'p'})
assert mailer.transport() == 'smtp', 'SMTP alone should select smtp'

os.environ['RESEND_API_KEY'] = 're_test123'
assert mailer.transport() == 'resend', 'Resend must win over SMTP when both are set'
assert mailer.is_configured()

# --- MAIL_TRANSPORT override (both configs coexist) -------------------------
# both are configured at this point (resend + smtp)
os.environ['MAIL_TRANSPORT'] = 'smtp'
assert mailer.transport() == 'smtp', 'MAIL_TRANSPORT=smtp must override auto-pick'
os.environ['MAIL_TRANSPORT'] = 'resend'
assert mailer.transport() == 'resend'
os.environ['MAIL_TRANSPORT'] = 'auto'          # anything unrecognised = auto
assert mailer.transport() == 'resend'
os.environ.pop('MAIL_TRANSPORT')
assert mailer.transport() == 'resend'

# forcing a transport that isn't configured reports None rather than silently
# falling back to the other one (so the Email Test page tells the truth)
os.environ['MAIL_TRANSPORT'] = 'smtp'
saved = {k: os.environ.pop(k) for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS')}
assert mailer.transport() is None and not mailer.is_configured()
os.environ.update(saved)
os.environ.pop('MAIL_TRANSPORT')

# --- config_status never leaks the key/password -----------------------------
st = mailer.config_status()
blob = json.dumps(st)
assert 're_test123' not in blob and "'p'" not in blob, 'secrets must not appear in status'
assert st['transport'] == 'resend' and st['resend_key_set'] is True
assert st['mail_from'] == mailer.DEFAULT_FROM          # default when MAIL_FROM unset
assert st['password_set'] is True                      # smtp fallback reported separately

# --- Resend request shape (stub urllib, no network) -------------------------
captured = {}


class _Resp:
    def read(self): return b'{"id":"abc-123"}'
    def __enter__(self): return self
    def __exit__(self, *a): return False


def fake_urlopen(req, timeout=None):
    captured['url'] = req.full_url
    captured['headers'] = {k.lower(): v for k, v in req.headers.items()}
    captured['body'] = json.loads(req.data.decode())
    captured['method'] = req.get_method()
    return _Resp()


mailer.urllib.request.urlopen = fake_urlopen

os.environ['MAIL_FROM'] = 'noreply@eduaakashaa.in'
assert mailer.send_now('priya@ex.com', 'Subj', 'plain text', '<b>html</b>') is True
assert captured['url'] == 'https://api.resend.com/emails'
assert captured['method'] == 'POST'
assert captured['headers']['authorization'] == 'Bearer re_test123'
assert captured['headers']['content-type'] == 'application/json'
# Regression: Resend is behind Cloudflare, which 403s ("error code: 1010") on
# urllib's default Python-urllib/x.y UA. A real UA must always be sent.
ua = captured['headers'].get('user-agent', '')
assert ua == mailer.USER_AGENT and 'python-urllib' not in ua.lower(), ua
b = captured['body']
assert b['from'] == 'EduAakashaa <noreply@eduaakashaa.in>', b['from']
assert b['to'] == ['priya@ex.com'] and b['subject'] == 'Subj'
assert b['text'] == 'plain text' and b['html'] == '<b>html</b>'

# text-only send omits html
mailer.send_now('a@b.com', 'S', 'only text')
assert 'html' not in captured['body']

# --- Resend API errors surface a readable message ---------------------------
import urllib.error


def fake_urlopen_403(req, timeout=None):
    raise urllib.error.HTTPError(
        req.full_url, 403, 'Forbidden', {},
        __import__('io').BytesIO(b'{"message":"The eduaakashaa.in domain is not verified"}'))


mailer.urllib.request.urlopen = fake_urlopen_403
try:
    mailer.send_now('x@y.com', 'S', 'T')
    raise AssertionError('should have raised')
except RuntimeError as e:
    assert 'Resend API 403' in str(e) and 'not verified' in str(e), str(e)

# --- send_async never raises, even when the transport blows up --------------
mailer.send_async('x@y.com', 'S', 'T')      # must not raise
print('all mailer checks passed')
