"""Access-control decorators used across blueprints.

Two tiers gate the member-facing and staff-facing areas migrated from the
legacy Hostinger site, which used a separate password on every page. Here that
is replaced by our own RBAC:

    premium_required  — Premium Membership pages (member perks / tools)
    admin_required    — EA Team / Counsellor Portal (internal staff tools)

`is_premium` already returns True for admins (see app.models.User), so admins
can open premium pages too.
"""
from functools import wraps

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user


def admin_required(f):
    """Allow only logged-in users with the 'admin' tier."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to continue.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapped


def mentor_required(f):
    """Allow only logged-in mentor-tier users (the alumni mentor portal)."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to your mentor account.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        if not current_user.is_mentor:
            abort(403)
        return f(*args, **kwargs)
    return wrapped


def premium_required(f):
    """Allow only Premium (or admin) members.

    Anonymous visitors are sent to log in; logged-in non-premium members get a
    friendly upgrade page (HTTP 403) instead of a raw error, so the gate also
    works as a conversion prompt.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access premium member tools.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        if not current_user.is_premium:
            return render_template('premium_locked.html'), 403
        return f(*args, **kwargs)
    return wrapped
