"""Email sender (stdlib only — no new dependencies).

Two transports, picked automatically:

  1. Resend HTTP API  (preferred; used whenever RESEND_API_KEY is set)
         RESEND_API_KEY   re_xxxxxxxx
         MAIL_FROM        noreply@eduaakashaa.com  (the domain here MUST be the one
                                                    verified in Resend, or it 403s)
  2. SMTP              (fallback, for local dev)
         SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASS, SMTP_FROM

Why: Render's free tier blocks outbound SMTP entirely (connecting to
smtp.gmail.com:587 fails with "Network is unreachable"), so production must send
over HTTPS. Resend's API is plain JSON over port 443, which is not blocked.

Never raises into a request: send_async logs failures instead. send_now raises,
so the admin Email Test page can show the real error.
"""
import json
import logging
import os
import smtplib
import threading
import urllib.error
import urllib.request
from email.message import EmailMessage
from email.utils import formataddr

log = logging.getLogger(__name__)

RESEND_ENDPOINT = 'https://api.resend.com/emails'
DEFAULT_FROM = 'noreply@eduaakashaa.com'   # must match the domain verified in Resend
USER_AGENT = 'EduAakashaa/1.0'


def _resend_cfg():
    key = os.environ.get('RESEND_API_KEY')
    if not key:
        return None
    return {'key': key, 'from': os.environ.get('MAIL_FROM', DEFAULT_FROM)}


def _smtp_cfg():
    host = os.environ.get('SMTP_HOST')
    user = os.environ.get('SMTP_USER')
    pwd = os.environ.get('SMTP_PASS')
    if not (host and user and pwd):
        return None
    return {
        'host': host, 'port': int(os.environ.get('SMTP_PORT', '587')),
        'user': user, 'pwd': pwd,
        'from': os.environ.get('SMTP_FROM', user),
    }


def transport():
    """Which transport will actually be used: 'resend' | 'smtp' | None.

    MAIL_TRANSPORT forces one ('resend' or 'smtp'); leave it unset for auto —
    Resend when it's configured, else SMTP. Both configs can coexist: Resend is
    the free path that works on Render today, SMTP becomes usable if the host
    ever allows outbound SMTP (e.g. a paid Render instance) — then just set
    MAIL_TRANSPORT=smtp, no key deletion and no redeploy of code."""
    forced = (os.environ.get('MAIL_TRANSPORT') or '').strip().lower()
    if forced == 'resend':
        return 'resend' if _resend_cfg() else None
    if forced == 'smtp':
        return 'smtp' if _smtp_cfg() else None
    if _resend_cfg():
        return 'resend'
    if _smtp_cfg():
        return 'smtp'
    return None


def is_configured():
    return transport() is not None


def config_status():
    """What the app can see — for the admin diagnostics page. Never exposes the
    API key or SMTP password, only whether one is set."""
    resend, smtp = _resend_cfg(), _smtp_cfg()
    return {
        'transport': transport() or '(none)',
        'forced': os.environ.get('MAIL_TRANSPORT') or 'auto',
        'resend_ready': bool(resend),
        'smtp_ready': bool(smtp),
        'configured': is_configured(),
        # Resend
        'resend_key_set': bool(resend),
        'mail_from': (resend or {}).get('from') or os.environ.get('MAIL_FROM') or f'{DEFAULT_FROM} (default)',
        # SMTP (fallback / local)
        'host': os.environ.get('SMTP_HOST') or '(not set)',
        'port': os.environ.get('SMTP_PORT', '587 (default)'),
        'user': os.environ.get('SMTP_USER') or '(not set)',
        'from': os.environ.get('SMTP_FROM') or os.environ.get('SMTP_USER') or '(not set)',
        'password_set': bool(os.environ.get('SMTP_PASS')),
    }


def _send_resend(cfg, to, subject, text, html, from_name):
    payload = {'from': formataddr((from_name, cfg['from'])), 'to': [to],
               'subject': subject, 'text': text}
    if html:
        payload['html'] = html
    req = urllib.request.Request(
        RESEND_ENDPOINT, data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': 'Bearer ' + cfg['key'],
                 'Content-Type': 'application/json',
                 # Resend sits behind Cloudflare, which 403s urllib's default
                 # "Python-urllib/x.y" UA as a bot signature (error code 1010).
                 # Any ordinary UA passes.
                 'User-Agent': USER_AGENT},
        method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            json.loads(resp.read() or b'{}')
        return True
    except urllib.error.HTTPError as e:
        # surface Resend's own message (e.g. domain not verified) — it's the
        # difference between a useful error and a blank 4xx
        detail = (e.read() or b'').decode('utf-8', 'replace')[:400]
        raise RuntimeError(f'Resend API {e.code}: {detail}') from None


def _send_smtp(cfg, to, subject, text, html, from_name):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = formataddr((from_name, cfg['from']))
    msg['To'] = to
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype='html')
    with smtplib.SMTP(cfg['host'], cfg['port'], timeout=15) as s:
        s.starttls()
        s.login(cfg['user'], cfg['pwd'])
        s.send_message(msg)
    return True


def _send(to, subject, text, html, from_name='EduAakashaa'):
    if not to:
        return False
    chosen = transport()          # honours MAIL_TRANSPORT, so both configs can coexist
    if chosen == 'resend':
        return _send_resend(_resend_cfg(), to, subject, text, html, from_name)
    if chosen == 'smtp':
        return _send_smtp(_smtp_cfg(), to, subject, text, html, from_name)
    return False


def send_now(to, subject, text, html=None, from_name='EduAakashaa'):
    """Synchronous send that RAISES on failure — used by the admin email test so
    the real error reaches the screen instead of being swallowed."""
    return _send(to, subject, text, html, from_name)


def send_async(to, subject, text, html=None, from_name='EduAakashaa'):
    """Best-effort background send — never blocks or raises into the request.

    Failures must not break the request, but they MUST be visible: everything is
    logged (recipient + subject only, never credentials) so a broken config shows
    up in the platform logs instead of silently dropping mail."""
    if not to:
        log.warning('Email skipped: no recipient (subject=%r)', subject)
        return
    if not is_configured():
        log.warning('Email skipped: no transport configured (set RESEND_API_KEY, '
                    'or SMTP_HOST/USER/PASS) — would have sent %r to %s', subject, to)
        return

    def worker():
        try:
            _send(to, subject, text, html, from_name)
            log.info('Email sent to %s via %s (subject=%r)', to, transport(), subject)
        except Exception:
            log.exception('Email FAILED to %s via %s (subject=%r)', to, transport(), subject)
    threading.Thread(target=worker, daemon=True).start()
