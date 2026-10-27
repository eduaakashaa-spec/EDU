"""Keeps bots out of the sign-up form and finds the ones that got in.

Sign-up checks (all server-side): a hidden honeypot field, a signed form timestamp (too fast or stale is refused), a per-address limit on sign-ups and attempts,
a name check for random-looking strings, and a short list of disposable e-mail domains. Every refusal is written to `signup_log` so it can be reviewed.

Clean-up: `suspect_reason(user)` flags free accounts that look automated, `has_activity(user_id)` says whether anything in the database points at an account
(found from the schema, so new tables are covered automatically), and `delete_unused(ids)` removes only free accounts with no activity at all.
"""
import re
from datetime import datetime, timedelta, timezone

from flask import current_app
from itsdangerous import BadSignature, URLSafeTimedSerializer

from app.extensions import db
from app.models import User
from app.models_security import SignupLog

MIN_SECONDS = 3
MAX_SECONDS = 2 * 3600
MAX_ACCOUNTS_PER_HOUR = 3
MAX_ATTEMPTS_PER_HOUR = 12
DISPOSABLE = {'mailinator.com', 'guerrillamail.com', 'guerrillamail.net', 'sharklasers.com', '10minutemail.com', 'tempmail.com', 'temp-mail.org', 'yopmail.com', 'trashmail.com',
              'getnada.com', 'dispostable.com', 'maildrop.cc', 'throwawaymail.com', 'fakeinbox.com', 'mintemail.com', 'mohmal.com'}


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _ser():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='signup-form')


def form_token():
    return _ser().dumps(int(_now().timestamp()))


def token_problem(token):
    """None when the token is valid and was issued between MIN_SECONDS and MAX_SECONDS ago."""
    try:
        issued = _ser().loads(token or '', max_age=MAX_SECONDS)
    except BadSignature:
        return 'expired'
    age = _now().timestamp() - int(issued)
    return 'too_fast' if age < MIN_SECONDS else None


def looks_random(name):
    """A single long token with many lower-to-upper switches ('FoSkRKDmUEHTyqAj') is not a name; 'McDonald' and 'DeShawn' have one switch."""
    name = (name or '').strip()
    if ' ' in name or len(name) < 10:
        return False
    return len(re.findall(r'[a-z][A-Z]', name)) >= 3


def name_problem(name):
    n = (name or '').strip()
    if len(n) < 2 or len(n) > 80:
        return 'bad_name'
    if re.search(r'https?://|www\.|@|<|>', n, re.I) or looks_random(n):
        return 'bad_name'
    return None


def email_problem(email):
    dom = (email or '').rsplit('@', 1)[-1].lower()
    return 'disposable' if dom in DISPOSABLE else None


def client_ip(request):
    fwd = (request.headers.get('X-Forwarded-For') or '').split(',')[0].strip()
    return (fwd or request.remote_addr or '')[:64]


def log(ip, email, reason):
    db.session.add(SignupLog(ip=ip, email=(email or '')[:200], reason=reason))
    db.session.commit()


def blocked_reason(form, ip):
    """Returns a short reason code when the sign-up should be refused, else None."""
    if (form.get('website') or '').strip():                                     # honeypot: people never see this field
        return 'honeypot'
    t = token_problem(form.get('ft'))
    if t:
        return t
    hour = _now() - timedelta(hours=1)
    if SignupLog.query.filter(SignupLog.ip == ip, SignupLog.created_at >= hour).count() >= MAX_ATTEMPTS_PER_HOUR:
        return 'rate_limited'
    if SignupLog.query.filter(SignupLog.ip == ip, SignupLog.reason == 'created', SignupLog.created_at >= hour).count() >= MAX_ACCOUNTS_PER_HOUR:
        return 'rate_limited'
    return name_problem(form.get('name')) or email_problem((form.get('email') or '').strip().lower())


# ---- finding and removing accounts that look automated -------------------------------------------------------------------------------------
def suspect_reason(user):
    """Why a free account looks automated, or None."""
    if user.tier != 'free':
        return None
    if looks_random(user.name):
        return 'random-looking name'
    local, _, dom = (user.email or '').lower().partition('@')
    if dom in DISPOSABLE:
        return 'disposable e-mail domain'
    if dom in ('gmail.com', 'googlemail.com') and local.count('.') >= 4:
        return 'e-mail with many dots'
    return None


_FK_COLS = None


def _fk_columns():
    """Every (table, column) in the schema that points at users.id."""
    global _FK_COLS
    if _FK_COLS is None:
        cols = []
        for t in db.metadata.sorted_tables:
            if t.name == 'users':
                continue
            for c in t.columns:
                if any(fk.column.table.name == 'users' for fk in c.foreign_keys):
                    cols.append((t, c))
        _FK_COLS = cols
    return _FK_COLS


def has_activity(user_id):
    """True when any table references this account (predictions, payments, profiles, attempts, enrolments, messages...)."""
    for t, c in _fk_columns():
        if db.session.query(t.c[c.name]).filter(t.c[c.name] == user_id).first() is not None:
            return True
    return False


def delete_unused(user_ids, actor_id=None):
    """Delete free accounts that nothing points at. Returns (deleted_emails, skipped [(email, why)])."""
    deleted, skipped = [], []
    for u in User.query.filter(User.id.in_(list(user_ids) or [0])).all():
        if u.id == actor_id:
            skipped.append((u.email, 'your own account'))
        elif u.tier != 'free':
            skipped.append((u.email, 'not a free account'))
        elif has_activity(u.id):
            skipped.append((u.email, 'has activity or linked records'))
        else:
            deleted.append(u.email)
            db.session.delete(u)
    db.session.commit()
    return deleted, skipped
