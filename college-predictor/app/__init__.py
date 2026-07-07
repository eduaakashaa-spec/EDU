from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    # Ensure instance folder exists (for SQLite DB)
    import os
    os.makedirs(app.instance_path, exist_ok=True)

    # Init extensions
    from app.extensions import db, login_manager, bcrypt
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Make WhatsApp click-to-chat + key contact details available to every template,
    # so CTAs across the site stay consistent and point to one number.
    @app.context_processor
    def inject_contact_globals():
        from urllib.parse import quote
        company = app.config.get('COMPANY', {})
        num_in = company.get('PHONE_IN', '+91 80157 22706')
        num_uae = company.get('PHONE_UAE', '+971 50 516 8081')
        digits = ''.join(c for c in num_in if c.isdigit())
        msg = ("Hi EduAakashaa, I'd like to know more about your mentorship "
               "and college-admission guidance.")
        from datetime import date
        return {
            'WHATSAPP_NUMBER': num_in,
            'WHATSAPP_NUMBER_UAE': num_uae,
            'WHATSAPP_URL': f'https://wa.me/{digits}?text={quote(msg)}',
            'CURRENT_YEAR': date.today().year,
        }

    # Create tables if they don't exist
    with app.app_context():
        from app import models  # noqa: F401 – ensure all models are imported
        from app import models_membership  # noqa: F401 – membership/invoice tables
        db.create_all()

    # Load JOSAA + NIRF data into memory once at startup
    from app.data.loader import load_data
    load_data()

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.api import api_bp
    app.register_blueprint(api_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.membership import membership_bp
    app.register_blueprint(membership_bp)

    from app.routes.admin_portal import admin_portal_bp
    app.register_blueprint(admin_portal_bp)

    from app.routes.alumni import alumni_bp
    app.register_blueprint(alumni_bp)

    from app.routes.survey import survey_bp
    app.register_blueprint(survey_bp)

    # A body over MAX_CONTENT_LENGTH (an oversized upload) is rejected before
    # the view runs — answer the alumni form's fetch() with JSON, everyone
    # else with a short message rather than a stack trace.
    from flask import jsonify, request

    @app.errorhandler(413)
    def too_large(_err):
        limit_mb = app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)
        msg = f'Upload too large. Please keep files under {limit_mb} MB total.'
        wants_json = ('application/json' in request.headers.get('Accept', '')
                      or request.path.startswith('/alumni'))
        if wants_json:
            return jsonify({'ok': False, 'error': msg}), 413
        return msg, 413

    return app
