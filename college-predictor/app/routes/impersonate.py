"""Admin "View as": sign in as a student, parent or mentor to see exactly what they see and troubleshoot, then return to the admin account.

  /admin/view-as                 pick a person (search, role filters)
  POST /admin/users/<id>/view-as start; read-only by default (every change is refused) unless "allow changes" is ticked
  POST /impersonate/stop         back to the admin account (always allowed)
  /admin/users/<id>/diagnose     what that person can open and why (plan, expiry, admin exceptions, enrolments)

Safeguards: only admins; never another admin; one at a time; passwords, sign-in and e-mail changes are refused even when changes are allowed; a banner on every page;
every session is logged (AdminImpersonation). The admin's own login is kept in the signed session and restored on stop.
"""
from datetime import datetime

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user

from app.decorators import admin_required
from app.extensions import db
from app.models import User
from app.models_security import AdminImpersonation
from app.services import tool_access

impersonate_bp = Blueprint('impersonate', __name__)
SAFE = ('GET', 'HEAD', 'OPTIONS')
ROLE_FILTERS = {'student': ('free', 'premium', 'elite'), 'mentor': ('ea_mentor', 'mentor'), 'all': ('free', 'premium', 'elite', 'ea_mentor', 'mentor')}


def state():
    """The active "View as" session ({'admin': id, 'ro': bool, 'log': id}) or None."""
    return session.get('imp')


@impersonate_bp.before_app_request
def _guard():
    imp = state()
    if not imp:
        return None
    ep = request.endpoint or ''
    if ep == 'static':
        return None
    if not current_user.is_authenticated:                         # signed out while viewing: forget the session
        session.pop('imp', None)
        return None
    admin = db.session.get(User, imp.get('admin') or 0)
    if admin is None or not admin.is_admin or current_user.id == admin.id:
        session.pop('imp', None)
        return None
    if request.method not in SAFE and ep != 'impersonate.stop':
        if request.blueprint == 'auth' or ep in ('members.change_email', 'members.change_password'):
            return _refuse('Passwords, sign-in and e-mail cannot be changed while you are viewing as someone else.')
        if imp.get('ro', True):
            return _refuse('Read-only view: nothing can be changed while you are viewing as %s. Stop viewing and sign back in, or start again with "allow changes".' % current_user.name)
    return None


def _refuse(msg):
    if request.is_json or 'application/json' in (request.headers.get('Accept') or ''):
        return jsonify(ok=False, error=msg), 403
    return render_template('impersonate_blocked.html', message=msg), 403


@impersonate_bp.app_context_processor
def _banner():
    imp = state()
    if not imp or not getattr(current_user, 'is_authenticated', False):
        return {'impersonating': None}
    return {'impersonating': {'name': current_user.name, 'email': current_user.email, 'tier': current_user.tier, 'readonly': imp.get('ro', True)}}


def _people(q, role, page):
    query = User.query.filter(User.tier.in_(ROLE_FILTERS.get(role, ROLE_FILTERS['all'])))
    if q:
        like = '%' + q + '%'
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    return query.order_by(User.name).paginate(page=page, per_page=25, error_out=False)


@impersonate_bp.route('/admin/view-as')
@admin_required
def picker():
    role = request.args.get('role') if request.args.get('role') in ROLE_FILTERS else 'student'
    q = (request.args.get('q') or '').strip()
    pagination = _people(q, role, request.args.get('page', 1, type=int))
    recent = (AdminImpersonation.query.filter_by(admin_id=current_user.id).order_by(AdminImpersonation.started_at.desc()).limit(8).all())
    return render_template('admin/view_as.html', admin_tab='users', pagination=pagination, rows=pagination.items, q=q, role=role, recent=recent, users={u.id: u for u in User.query.filter(User.id.in_([r.target_id for r in recent] or [0])).all()})


@impersonate_bp.route('/admin/users/<int:user_id>/view-as', methods=['POST'])
@admin_required
def start(user_id):
    target = db.session.get(User, user_id) or abort(404)
    if state():
        flash('Stop the current "View as" session first.', 'info')
        return redirect(url_for('memberhub.home'))
    if target.is_admin or target.id == current_user.id:
        flash('You can only view as a member, parent or mentor account, not as an admin.', 'danger')
        return redirect(url_for('impersonate.picker'))
    ro = request.form.get('allow_changes') != '1'
    log = AdminImpersonation(admin_id=current_user.id, target_id=target.id, readonly=ro, ip=(request.headers.get('X-Forwarded-For') or request.remote_addr or '')[:64])
    db.session.add(log)
    db.session.commit()
    admin_id = current_user.id
    login_user(target, remember=False)
    session['imp'] = {'admin': admin_id, 'ro': ro, 'log': log.id}
    flash('You are now viewing as %s (%s)%s.' % (target.name, target.tier, ', read-only' if ro else ', changes allowed'), 'info')
    return redirect(request.form.get('next') if (request.form.get('next') or '').startswith('/') and not (request.form.get('next') or '').startswith('//') else url_for('memberhub.home'))


@impersonate_bp.route('/impersonate/stop', methods=['POST'])
@login_required
def stop():
    imp = state()
    if not imp:
        return redirect(url_for('memberhub.home'))
    admin = db.session.get(User, imp.get('admin') or 0)
    log = db.session.get(AdminImpersonation, imp.get('log') or 0)
    if log and not log.ended_at:
        log.ended_at = datetime.utcnow()
        db.session.commit()
    session.pop('imp', None)
    if admin is None or not admin.is_admin:
        from flask_login import logout_user
        logout_user()
        return redirect(url_for('auth.login'))
    login_user(admin, remember=False)
    flash('Back to your admin account.', 'success')
    return redirect(url_for('membership.admin_users'))


@impersonate_bp.route('/admin/users/<int:user_id>/diagnose')
@admin_required
def diagnose(user_id):
    from app.models_membership import UserToolAccess
    from app.models_mentorship import MsEnrolment, MsParentLink
    from app.models_pulse import PulseProfile
    from app.services import member_hub as mh
    u = db.session.get(User, user_id) or abort(404)
    groups = []
    for cat in mh.CATEGORIES:
        rows = []
        for t in cat['tiles']:
            ok, why = tool_access.explain(u, t)
            rows.append({'title': t['title'], 'access': t.get('access'), 'staff': bool(t.get('staff')), 'ok': ok, 'why': why, 'endpoint': t.get('endpoint', '')})
        groups.append({'title': cat['title'], 'rows': rows})
    try:
        from app.models_reinforce import RfStudent
        rf = RfStudent.query.filter_by(user_id=u.id).first()
    except Exception:
        rf = None
    info = {
        'enrolments': MsEnrolment.query.filter_by(student_id=u.id).all(),
        'mentoring': MsEnrolment.query.filter_by(mentor_id=u.id).count(),
        'parent_of': MsParentLink.query.filter_by(parent_id=u.id).count(),
        'exceptions': UserToolAccess.query.filter_by(user_id=u.id).all(),
        'pulse': db.session.get(PulseProfile, u.id), 'rf': rf,
        'viewed': AdminImpersonation.query.filter_by(target_id=u.id).order_by(AdminImpersonation.started_at.desc()).limit(5).all(),
    }
    return render_template('admin/diagnose.html', admin_tab='users', u=u, groups=groups, info=info)
