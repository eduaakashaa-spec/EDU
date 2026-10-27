"""Auth Blueprint — Login · Register · Logout · Contact form handler."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import safe_next
from app.extensions import db, bcrypt
from app.models import User, ContactInquiry
from app.services import signup_guard

auth_bp = Blueprint('auth', __name__)


def _mentor_landing(user):
    """Where each kind of mentor starts: EA mentors on their desk, alumni guides on their portal."""
    if user.is_ea_mentor:
        return url_for('members.mentor_desk')
    if user.is_mentor:
        return url_for('alumni.mentor_dashboard')
    return url_for('main.home')


@auth_bp.route('/mentor-login', methods=['GET', 'POST'])
def mentor_login():
    """Dedicated sign-in for mentors (EA mentors and alumni College Guides)."""
    if current_user.is_authenticated:
        return redirect(_mentor_landing(current_user))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not (user.is_mentor or user.is_ea_mentor):
                flash('This account is not registered as a mentor. Please use the member login.', 'danger')
                return render_template('auth/mentor_login.html')
            login_user(user, remember=request.form.get('remember'))
            flash('Logged in successfully.', 'success')
            return redirect(safe_next(request.args.get('next')) or _mentor_landing(user))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/mentor_login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember'))
            next_page = safe_next(request.args.get('next'))
            flash('Logged in successfully.', 'success')
            if not next_page and (user.is_ea_mentor or user.is_mentor):
                return redirect(_mentor_landing(user))
            return redirect(next_page or url_for('memberhub.home'))

        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm = request.form.get('confirm') or ''

        ip = signup_guard.client_ip(request)
        why = signup_guard.blocked_reason(request.form, ip)
        if why:
            signup_guard.log(ip, email, why)
            if why == 'honeypot':                                  # a bot: look like it worked, create nothing
                return redirect(url_for('auth.login'))
            msg = {'rate_limited': 'Too many sign-up attempts from this connection. Please try again later or contact us.',
                   'bad_name': 'Please enter your real full name.', 'disposable': 'Please use a permanent e-mail address.'}.get(why, 'Please check your details and try again.')
            flash(msg, 'danger')
            return render_template('auth/register.html', form_token=signup_guard.form_token())

        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            signup_guard.log(ip, email, 'duplicate' if any('already exists' in e for e in errors) else 'invalid')
            return render_template('auth/register.html', form_token=signup_guard.form_token())

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password_hash=pw_hash, tier='free')
        db.session.add(user)
        db.session.commit()
        signup_guard.log(ip, email, 'created')

        login_user(user)
        flash('Account created! Welcome to EduAakashaA.', 'success')
        return redirect(url_for('main.home'))

    return render_template('auth/register.html', form_token=signup_guard.form_token())


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    # The dashboard was replaced by the member profile page; keep the old URL
    # working for bookmarks / existing links.
    return redirect(url_for('members.profile'))


@auth_bp.route('/contact', methods=['POST'])
def contact_submit():
    inquiry = ContactInquiry(
        first_name=(request.form.get('firstName') or '').strip(),
        last_name=(request.form.get('lastName') or '').strip(),
        email=(request.form.get('email') or '').strip().lower(),
        interested=request.form.get('interested'),
        message=(request.form.get('message') or '').strip(),
    )
    db.session.add(inquiry)
    db.session.commit()
    flash('Thank you! We will get back to you soon.', 'success')
    return redirect(url_for('main.contact'))
