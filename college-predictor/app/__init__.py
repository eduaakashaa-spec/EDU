from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    # config.Config leaves this None outside debug rather than falling back to a
    # committed default, so a missing SECRET_KEY stops the deploy instead of
    # silently shipping forgeable session cookies.
    if not app.config['SECRET_KEY']:
        raise RuntimeError(
            'SECRET_KEY is not set. Set it in the environment (Render sets it '
            'automatically via render.yaml), or use FLASK_DEBUG=1 for local dev.'
        )

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
        num_in = company.get('PHONE_IN', '+91-80157 22706')
        digits = ''.join(c for c in num_in if c.isdigit())
        msg = ("Hi EduAakashaa, I'd like to know more about your mentorship "
               "and college-admission guidance.")
        from datetime import date
        return {
            'WHATSAPP_NUMBER': num_in,
            'WHATSAPP_URL': f'https://wa.me/{digits}?text={quote(msg)}',
            'CURRENT_YEAR': date.today().year,
        }

    # Short "data is not updated periodically -> go Premium" notice, shown on the
    # public information pages. Hidden on membership / account / admin pages, on
    # contact pages, and for members who already have Premium.
    NOTICE_SKIP_BLUEPRINTS = {'membership', 'admin_portal', 'auth', 'members', 'invoices',
                              'onboarding', 'alumni', 'survey', 'api', 'assessments', 'memberhub', 'mentorship', 'pulse', 'futureready', 'wagroup', 'pulse_jee', 'reinforce'}
    NOTICE_SKIP_ENDPOINTS = {'main.members_registration', 'main.premium_membership',
                             'main.members_login', 'main.contact', 'main.contact_alias',
                             'main.contactus_alias', 'main.dasa_guide', 'main.nirf_ranking', 'main.josaa', 'main.iiits', 'main.annanri', 'main.nirf_analytic', 'main.tnea_colleges', 'main.dasa_2026', 'main.dasa_2026_analytics', 'main.josaa_ea_members', 'main.josaa_assessment', 'main.choice_builder_pro', 'static'}

    @app.context_processor
    def inject_premium_notice():
        from flask import request
        from flask_login import current_user
        ep = request.endpoint or ''
        if (request.blueprint in NOTICE_SKIP_BLUEPRINTS or ep in NOTICE_SKIP_ENDPOINTS
                or not ep):
            return {'show_premium_notice': False}
        member = bool(getattr(current_user, 'is_authenticated', False)
                      and getattr(current_user, 'is_premium', False))
        return {'show_premium_notice': not member}

    # Create tables if they don't exist
    with app.app_context():
        from app import models  # noqa: F401 – ensure all models are imported
        from app import models_membership  # noqa: F401 – membership/invoice tables
        from app import models_mentorship  # noqa: F401 – mentorship portal tables
        from app import models_pulse  # noqa: F401 – EduPulse-UCEED question bank + progress
        from app import models_reinforce  # noqa: F401 – EduPulse-Reinforcement tables
        from app.futureready import models as _fr_models  # noqa: F401 – FutureReady (Class 8-9) tables
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

    from app.routes.assessments import assessments_bp
    app.register_blueprint(assessments_bp)

    from app.routes.guides import guides_bp
    app.register_blueprint(guides_bp)

    from app.routes.memberhub import memberhub_bp
    app.register_blueprint(memberhub_bp)

    from app.routes.mentorship import mentorship_bp
    app.register_blueprint(mentorship_bp)

    from app.routes.pulse import pulse_bp
    app.register_blueprint(pulse_bp)

    from app.futureready.routes import fr_bp
    app.register_blueprint(fr_bp)

    from app.routes.pulse_jee import pulse_jee_bp
    app.register_blueprint(pulse_jee_bp)

    from app.routes.reinforce import reinforce_bp
    app.register_blueprint(reinforce_bp)

    from app.routes.wagroup import wagroup_bp
    app.register_blueprint(wagroup_bp)
    from app.services import wagroup as _wg
    app.jinja_env.globals['wa_group'] = _wg.get
    app.jinja_env.globals['wa_group_can_edit'] = _wg.can_manage

    # The legacy eduaakashaa.in domain forwards to eduaakashaa.com (path and query
    # kept), so old links, QR codes and bookmarks land on the live site.
    from flask import redirect, request
    legacy_hosts = {'eduaakashaa.in', 'www.eduaakashaa.in'}
    canonical = app.config.get('CANONICAL_URL', 'https://www.eduaakashaa.com')

    @app.before_request
    def _legacy_domain_redirect():
        host = (request.host or '').split(':')[0].lower()
        if host in legacy_hosts:
            return redirect(canonical + request.full_path.rstrip('?'), code=301)

    from app.routes.onboarding import onboarding_bp
    app.register_blueprint(onboarding_bp)

    from app.routes.members import members_bp
    app.register_blueprint(members_bp)

    from app.routes.invoices import invoices_bp
    app.register_blueprint(invoices_bp)

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

    # Custom on-brand line icons available in every template as ea_icon('name').
    app.jinja_env.globals['ea_icon'] = (
        app.jinja_env.get_template('_ea_icons.html').module.ic)

    return app
