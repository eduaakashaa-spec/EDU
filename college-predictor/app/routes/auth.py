"""Auth Blueprint — Login · Register · Logout · Contact form handler."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models import User, ContactInquiry

auth_bp = Blueprint('auth', __name__)


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
            next_page = request.args.get('next')
            flash('Logged in successfully.', 'success')
            return redirect(next_page or url_for('main.home'))

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
            return render_template('auth/register.html')

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password_hash=pw_hash, tier='free')
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Account created! Welcome to EduAakashaA.', 'success')
        return redirect(url_for('main.home'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html')


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
