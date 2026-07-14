"""Minimal SMTP sender (stdlib only). No-op when SMTP isn't configured, so it's
safe locally and in any env without credentials — the form never fails because
of email. Configure in prod via env:

    SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASS,
    SMTP_FROM (default SMTP_USER)

For Gmail (eduaakashaa@gmail.com) use an App Password as SMTP_PASS.
"""
import logging
import os
import smtplib
import threading
from email.message import EmailMessage
from email.utils import formataddr

log = logging.getLogger(__name__)


def _cfg():
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


def is_configured():
    return _cfg() is not None


def config_status():
    """What the app can see of the SMTP config — for the admin diagnostics page.
    Never returns the password itself, only whether one is set."""
    return {
        'host': os.environ.get('SMTP_HOST') or '(not set)',
        'port': os.environ.get('SMTP_PORT', '587 (default)'),
        'user': os.environ.get('SMTP_USER') or '(not set)',
        'from': os.environ.get('SMTP_FROM') or os.environ.get('SMTP_USER') or '(not set)',
        'password_set': bool(os.environ.get('SMTP_PASS')),
        'configured': is_configured(),
    }


def send_now(to, subject, text, html=None, from_name='EduAakashaa'):
    """Synchronous send that RAISES on failure — used by the admin email test so
    the real SMTP error reaches the screen instead of being swallowed."""
    return _send(to, subject, text, html, from_name)


def _send(to, subject, text, html, from_name='EduAakashaa'):
    c = _cfg()
    if not c or not to:
        return False
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = formataddr((from_name, c['from']))
    msg['To'] = to
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype='html')
    with smtplib.SMTP(c['host'], c['port'], timeout=15) as s:
        s.starttls()
        s.login(c['user'], c['pwd'])
        s.send_message(msg)
    return True


def send_async(to, subject, text, html=None, from_name='EduAakashaa'):
    """Best-effort background send — never blocks or raises into the request.

    Failures must not break the request, but they MUST be visible: everything is
    logged (recipient + subject only, never credentials) so a misconfigured SMTP
    shows up in the platform logs instead of silently dropping mail."""
    if not to:
        log.warning('Email skipped: no recipient (subject=%r)', subject)
        return
    if not is_configured():
        log.warning('Email skipped: SMTP is not configured (SMTP_HOST/USER/PASS) '
                    '— would have sent %r to %s', subject, to)
        return

    def worker():
        try:
            _send(to, subject, text, html, from_name)
            log.info('Email sent to %s (subject=%r)', to, subject)
        except Exception:
            # keep best-effort semantics, but leave a full traceback behind
            log.exception('Email FAILED to %s (subject=%r)', to, subject)
    threading.Thread(target=worker, daemon=True).start()
