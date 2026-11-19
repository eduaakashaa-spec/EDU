"""EduPulse App (/app/): installable, mobile-first app for students, parents and mentors.

Same accounts and data as the portal. The sign-in screen has three doors (Student, Parent, Mentor); the chosen view is kept
in the session and can be switched on the Me screen when one account has several roles (a mentor who is also a parent).
Deep links open the full portal pages, which check access again.
"""
from datetime import datetime, timedelta, timezone

from flask import (Blueprint, Response, flash, redirect, render_template, request, send_from_directory,
                   session, url_for, current_app)
from flask_login import current_user, login_required, login_user, logout_user

from app.decorators import safe_next
from app.extensions import bcrypt
from app.models import User
from app.services import edupulse_app as svc
from app.services import login_guard

edupulse_app_bp = Blueprint('edupulse_app', __name__, url_prefix='/app')

_IST = timezone(timedelta(hours=5, minutes=30))
_THROTTLE_MSG = 'Too many sign-in attempts. Please wait a few minutes and try again, or reset your password.'


def _role():
    role = svc.resolve_role(current_user, session.get('ep_role'))
    session['ep_role'] = role
    return role


def _ctx(active, role, **kw):
    return dict(active=active, role=role, roles=svc.roles_for(current_user), ROLE_LABEL=svc.ROLE_LABEL,
                short_title=svc.short_title, **kw)


# --------------------------------------------------------------------------- #
# Welcome and sign-in
# --------------------------------------------------------------------------- #
@edupulse_app_bp.route('/', methods=['GET'])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('edupulse_app.home'))
    role = request.args.get('as') if request.args.get('as') in svc.ROLES else 'student'
    return render_template('edupulse_app/welcome.html', pick=role, ROLE_LABEL=svc.ROLE_LABEL)


@edupulse_app_bp.route('/login', methods=['POST'])
def login():
    role = request.form.get('role') if request.form.get('role') in svc.ROLES else 'student'
    email = (request.form.get('email') or '').strip().lower()
    password = request.form.get('password') or ''
    ip = login_guard.client_ip(request)
    if login_guard.blocked(ip, email):
        flash(_THROTTLE_MSG, 'danger')
        return render_template('edupulse_app/welcome.html', pick=role, ROLE_LABEL=svc.ROLE_LABEL, email=email), 429
    user = User.query.filter_by(email=email).first()
    if not (user and bcrypt.check_password_hash(user.password_hash, password)):
        login_guard.record_failure(ip, email)
        flash('Invalid email or password.', 'danger')
        return render_template('edupulse_app/welcome.html', pick=role, ROLE_LABEL=svc.ROLE_LABEL, email=email), 401
    ok, msg = svc.login_allowed(user, role)
    if not ok:
        flash(msg, 'danger')
        return render_template('edupulse_app/welcome.html', pick=role, ROLE_LABEL=svc.ROLE_LABEL, email=email), 403
    login_guard.clear(ip, email)
    login_user(user, remember=bool(request.form.get('remember')))
    session['ep_role'] = svc.resolve_role(user, role)
    if msg:
        flash(msg, 'info')
    return redirect(safe_next(request.args.get('next')) or url_for('edupulse_app.home'))


@edupulse_app_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('ep_role', None)
    logout_user()
    flash('You have signed out.', 'success')
    return redirect(url_for('edupulse_app.welcome'))


@edupulse_app_bp.route('/role', methods=['POST'])
@login_required
def switch_role():
    wanted = request.form.get('role')
    if wanted in svc.roles_for(current_user):
        session['ep_role'] = wanted
    return redirect(url_for('edupulse_app.home'))


# --------------------------------------------------------------------------- #
# Screens
# --------------------------------------------------------------------------- #
def _enrolments(role):
    if role == 'mentor':
        return svc.mentor_enrolments(current_user)
    if role == 'parent':
        return svc.parent_enrolments(current_user)
    return svc.student_enrolments(current_user)


@edupulse_app_bp.route('/home')
@login_required
def home():
    role = _role()
    ens = _enrolments(role)
    cards = [svc.card(e, role, current_user) for e in ens]
    now = datetime.now(_IST)
    ctx = _ctx('home', role, cards=cards, greeting=svc.greeting(now.hour), today=now,
               notices=svc.announcements(role), practice=svc.practice_tiles(current_user, role)[:6])
    if role == 'mentor':
        cards = svc.sort_for_mentor(cards)
        ctx.update(cards=cards, overview=svc.mentor_overview(cards), alumni_only=current_user.is_mentor)
        return render_template('edupulse_app/home_mentor.html', **ctx)
    if role == 'parent':
        pick = request.args.get('child', type=int)
        child = next((c for c in cards if c['id'] == pick), cards[0] if cards else None)
        ctx.update(child=child)
        return render_template('edupulse_app/home_parent.html', **ctx)
    ctx.update(card=cards[0] if cards else None, agenda=svc.calendar(ens)[:5],
               done_week=svc.week_sessions_done(ens))
    return render_template('edupulse_app/home_student.html', **ctx)


@edupulse_app_bp.route('/plan')
@login_required
def plan():
    role = _role()
    items = svc.calendar(_enrolments(role), days=90)
    groups, cur = [], None
    for i in items:
        label = 'Today' if i['days'] == 0 else ('Tomorrow' if i['days'] == 1 else
                ('This week' if i['days'] < 7 else ('Next 30 days' if i['days'] < 30 else 'Later')))
        if i['days'] < 0:
            continue
        if label != cur:
            groups.append({'label': label, 'items': []})
            cur = label
        groups[-1]['items'].append(i)
    return render_template('edupulse_app/plan.html', **_ctx('plan', role, groups=groups, total=sum(len(g['items']) for g in groups)))


@edupulse_app_bp.route('/practice')
@login_required
def practice():
    role = _role()
    return render_template('edupulse_app/practice.html', **_ctx('practice', role, tiles=svc.practice_tiles(current_user, role)))


@edupulse_app_bp.route('/explore')
@login_required
def explore():
    role = _role()
    cats = [c for c in svc.tool_categories(current_user) if role == 'mentor' or c['key'] != 'staff']
    return render_template('edupulse_app/explore.html', **_ctx('explore', role, cats=cats))


@edupulse_app_bp.route('/me')
@login_required
def me():
    role = _role()
    return render_template('edupulse_app/me.html', **_ctx('me', role, enrolments=_enrolments(role)))


# --------------------------------------------------------------------------- #
# PWA plumbing: manifest and service worker served from /app/ so the worker's scope is the app
# --------------------------------------------------------------------------- #
@edupulse_app_bp.route('/manifest.webmanifest')
def manifest():
    body = render_template('edupulse_app/manifest.json')
    return Response(body, mimetype='application/manifest+json')


@edupulse_app_bp.route('/sw.js')
def service_worker():
    resp = send_from_directory(current_app.static_folder, 'js/edupulse_sw.js', mimetype='application/javascript')
    resp.headers['Service-Worker-Allowed'] = '/app/'
    resp.headers['Cache-Control'] = 'no-cache'
    return resp


@edupulse_app_bp.route('/offline')
def offline():
    return render_template('edupulse_app/offline.html')

