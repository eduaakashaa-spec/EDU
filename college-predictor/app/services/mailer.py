"""Minimal SMTP sender (stdlib only). No-op when SMTP isn't configured, so it's
safe locally and in any env without credentials — the form never fails because
of email. Configure in prod via env:

    SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASS,
    SMTP_FROM (default SMTP_USER)

For Gmail (eduaakashaa@gmail.com) use an App Password as SMTP_PASS.
"""
import os
import smtplib
import threading
from email.message import EmailMessage
from email.utils import formataddr


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
    """Best-effort background send — never blocks or raises into the request."""
    if not is_configured() or not to:
        return
    def worker():
        try:
            _send(to, subject, text, html, from_name)
        except Exception:
            pass  # best-effort; a failed confirmation email must not break anything
    threading.Thread(target=worker, daemon=True).start()
