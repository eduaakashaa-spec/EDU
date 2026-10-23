"""Server-side access rules for FutureReady. Every route resolves a profile and calls `role_for`; nothing is decided in templates or JS.

admin  : full access, content management, audit
mentor : (`ea_mentor` tier) only students assigned to them
student: only their own profile
parent : only linked students, and never the mentor-private notes
"""
from functools import wraps

from flask import abort, flash, redirect, request, url_for
from flask_login import current_user

from app.extensions import db
from app.futureready.models import FrAudit, FrNotice, FrParentLink, FrProfile

STAFF = ('admin', 'mentor')


def role_for(profile, user=None):
    user = user or current_user
    if not user or not user.is_authenticated:
        return None
    if user.is_admin:
        return 'admin'
    if profile.mentor_id == user.id and user.is_ea_mentor:
        return 'mentor'
    if profile.user_id == user.id:
        return 'student'
    if FrParentLink.query.filter_by(profile_id=profile.id, parent_id=user.id).first():
        return 'parent'
    return None


def profile_or_403(pid, roles=None):
    """Load a profile and the caller's role; 404 for unknown, 403 when the caller has no relationship to it."""
    p = db.session.get(FrProfile, pid)
    if not p:
        abort(404)
    role = role_for(p)
    if role is None or (roles and role not in roles):
        abort(403)
    return p, role


def my_profiles(user=None):
    """Profiles the user can see, as [(profile, role)]."""
    user = user or current_user
    out, seen = [], set()
    if user.is_admin:
        for p in FrProfile.query.order_by(FrProfile.id.desc()).all():
            out.append((p, 'admin')); seen.add(p.id)
        return out
    if user.is_ea_mentor:
        for p in FrProfile.query.filter_by(mentor_id=user.id).all():
            out.append((p, 'mentor')); seen.add(p.id)
    own = FrProfile.query.filter_by(user_id=user.id).first()
    if own and own.id not in seen:
        out.append((own, 'student')); seen.add(own.id)
    for l in FrParentLink.query.filter_by(parent_id=user.id).all():
        p = db.session.get(FrProfile, l.profile_id)
        if p and p.id not in seen:
            out.append((p, 'parent')); seen.add(p.id)
    return out


def login_needed(f):
    @wraps(f)
    def w(*a, **k):
        if not current_user.is_authenticated:
            flash('Please log in to open FutureReady.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        return f(*a, **k)
    return w


def audit(action, profile=None, detail='', role=None):
    try:
        db.session.add(FrAudit(user_id=getattr(current_user, 'id', None), role=role, profile_id=getattr(profile, 'id', profile), action=action, detail=(detail or '')[:500]))
        db.session.commit()
    except Exception:
        db.session.rollback()


def notify(user_id, text, url=None, profile_id=None):
    if user_id:
        db.session.add(FrNotice(user_id=user_id, profile_id=profile_id, text=text[:300], url=url))


def consent_ok(profile):
    """Assessments stay locked until a parent/guardian has given consent for this child (also required by the onboarding flow)."""
    return bool(profile.consent_at)
