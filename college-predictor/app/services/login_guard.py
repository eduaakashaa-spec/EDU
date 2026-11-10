"""Throttle sign-in against online password guessing (brute-force / credential stuffing).

bcrypt makes each guess slow, but nothing stopped an attacker trying thousands of passwords against a known
e-mail, or one password against many e-mails. We count recent *failed* logins in the `login_attempts` table
(DB-backed, so it holds across the several gunicorn workers) and refuse once either the IP or the e-mail passes
a threshold inside the window. A successful login clears that account's failures, so a real user who finally
remembers their password is never left locked out.
"""
from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models_security import LoginAttempt

WINDOW_MIN = 15           # how far back we count
MAX_PER_IP = 20           # failures from one IP in the window
MAX_PER_EMAIL = 8         # failures against one e-mail in the window (stops targeted guessing)
_PRUNE_HOURS = 24


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def client_ip(request):
    fwd = (request.headers.get('X-Forwarded-For') or '').split(',')[0].strip()
    return (fwd or request.remote_addr or '')[:64]


def blocked(ip, email):
    """True when sign-in should be refused right now for this IP or e-mail."""
    since = _now() - timedelta(minutes=WINDOW_MIN)
    email = (email or '').strip().lower()
    by_email = (LoginAttempt.query.filter(LoginAttempt.email == email, LoginAttempt.created_at >= since).count()
                if email else 0)
    if by_email >= MAX_PER_EMAIL:
        return True
    by_ip = LoginAttempt.query.filter(LoginAttempt.ip == ip, LoginAttempt.created_at >= since).count() if ip else 0
    return by_ip >= MAX_PER_IP


def record_failure(ip, email):
    db.session.add(LoginAttempt(ip=ip, email=(email or '').strip().lower()[:200]))
    # opportunistic cleanup so the table can't grow without bound
    db.session.query(LoginAttempt).filter(LoginAttempt.created_at < _now() - timedelta(hours=_PRUNE_HOURS)).delete()
    db.session.commit()


def clear(ip, email):
    """Forget this account's recent failures after a correct password."""
    email = (email or '').strip().lower()
    q = LoginAttempt.query.filter(db.or_(LoginAttempt.email == email, LoginAttempt.ip == ip))
    q.delete(synchronize_session=False)
    db.session.commit()
