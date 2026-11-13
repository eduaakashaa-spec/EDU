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

    # Google Analytics 4: the measurement ID of the www.eduaakashaa.com web stream (public by design; override or switch off with GA_MEASUREMENT_ID, empty = off).
    # Not loaded in debug or tests, and not for admins and staff, so our own visits do not count.
    @app.context_processor
    def inject_analytics():
        import os
        from flask import request
        from flask_login import current_user
        gid = os.environ.get('GA_MEASUREMENT_ID', 'G-L5HRKWL888').strip()
        if not gid or app.debug or app.testing:
            return {'ga_id': ''}
        ep = request.endpoint or ''
        if request.blueprint in ('admin_portal', 'impersonate') or ep.startswith('admin'):
            return {'ga_id': ''}
        if getattr(current_user, 'is_authenticated', False) and (getattr(current_user, 'is_admin', False) or getattr(current_user, 'is_staff', False)):
            return {'ga_id': ''}
        return {'ga_id': gid}

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
                              'onboarding', 'alumni', 'survey', 'api', 'assessments', 'memberhub', 'mentorship', 'pulse', 'futureready', 'wagroup', 'pulse_jee', 'pulse_tn10', 'iat', 'bitsat_mock', 'jeep2_mock', 'nid_mock', 'nift_mock', 'neet_mock', 'sat_mock', 'olympiad_mock', 'pcm12', 'pcb12', 'equivalency', 'hr', 'free_mock', 'explorer', 'impersonate', 'reinforce', 'portal_guide', 'planner'}
    NOTICE_SKIP_ENDPOINTS = {'main.members_registration', 'main.premium_membership',
                             'main.members_login', 'main.contact', 'main.contact_alias',
                             'main.contactus_alias', 'main.dasa_guide', 'main.nirf_ranking', 'main.josaa', 'main.iiits', 'main.annanri', 'main.nirf_analytic', 'main.tnea_colleges', 'main.dasa_2026', 'main.dasa_2026_analytics', 'main.josaa_ea_members', 'main.josaa_assessment', 'main.choice_builder_pro', 'main.tnea_expert', 'main.neet_2027', 'main.medicine', 'main.jee_registration', 'main.jee_paper2', 'main.iat', 'main.nid_papers', 'main.explorer_landing', 'main.nift_exam', 'main.neet_exam', 'main.sat_exam', 'main.olympiad_exam', 'main.school', 'main.neet_seats_2025', 'main.josaa_2026_analytics', 'static'}

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
        from app import models_hr  # noqa: F401 – HR letter templates and register
        from app import models_security  # noqa: F401 – sign-up log
        from app import models_planner  # noqa: F401 – Smart Study Planner tables
        from app.futureready import models as _fr_models  # noqa: F401 – FutureReady (Class 8-9) tables
        db.create_all()

    # Load JOSAA + NIRF data into memory once at startup
    from app.data.loader import load_data
    load_data()
    from app.data.loader import get_josaa_info
    app.jinja_env.globals['JOSAA'] = get_josaa_info          # {{ JOSAA().year }}: the admission year the predictor runs on

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

    from app.routes.free_mock import free_mock_bp
    app.register_blueprint(free_mock_bp)
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
    from app.routes.pulse_tn10 import pulse_tn10_bp
    app.register_blueprint(pulse_tn10_bp)
    from app.routes.pulse_iat import iat_bp
    app.register_blueprint(iat_bp)
    from app.routes.pulse_bitsat import bitsat_bp
    app.register_blueprint(bitsat_bp)
    from app.routes.pulse_jeep2 import jeep2_bp
    app.register_blueprint(jeep2_bp)
    from app.routes.pulse_nid import nid_bp
    app.register_blueprint(nid_bp)
    from app.routes.pulse_explorer import explorer_bp
    app.register_blueprint(explorer_bp)
    from app.routes.pulse_nift import nift_bp
    app.register_blueprint(nift_bp)
    from app.routes.pulse_neet import neet_bp
    app.register_blueprint(neet_bp)
    from app.routes.pulse_sat import sat_bp
    app.register_blueprint(sat_bp)
    from app.routes.pulse_olympiad import oly_bp
    app.register_blueprint(oly_bp)
    from app.routes.pcm12 import pcb_bp, pcm_bp
    app.register_blueprint(pcm_bp)
    app.register_blueprint(pcb_bp)
    from app.routes.hr import hr_bp
    app.register_blueprint(hr_bp)
    from app.routes.equivalency import equivalency_bp
    app.register_blueprint(equivalency_bp)
    from app.routes.impersonate import impersonate_bp
    app.register_blueprint(impersonate_bp)

    from app.routes.reinforce import reinforce_bp
    app.register_blueprint(reinforce_bp)

    from app.routes.portal_guide import portal_guide_bp
    app.register_blueprint(portal_guide_bp)

    from app.routes.planner import planner_bp
    app.register_blueprint(planner_bp)

    from app.routes.wagroup import wagroup_bp
    app.register_blueprint(wagroup_bp)
    from app.services import wagroup as _wg
    app.jinja_env.globals['wa_group'] = _wg.get
    from app.services import medicine_hub as _med
    app.jinja_env.globals['MEDICINE_PAGES'] = _med.PAGES
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

    # Static files: every url_for('static', ...) gets ?v=<file mtime>, and a request that carries v is cached for a
    # year (browser and Cloudflare). A changed file gets a new address, so nothing goes stale; un-versioned requests
    # (addresses written by hand in CSS / JS) keep Flask's revalidate-every-time default.
    import os
    _mtimes = {}

    @app.url_defaults
    def _static_version(endpoint, values):
        if endpoint == 'static' and 'filename' in values and 'v' not in values:
            fn = values['filename']
            if fn not in _mtimes or app.debug:
                try:
                    _mtimes[fn] = int(os.stat(os.path.join(app.static_folder, fn)).st_mtime)
                except OSError:
                    _mtimes[fn] = 0
            if _mtimes[fn]:
                values['v'] = _mtimes[fn]

    @app.after_request
    def _static_cache(resp):
        if request.endpoint == 'static' and request.args.get('v') and resp.status_code == 200:
            resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return resp

    # Baseline security headers on every response. frame-ancestors / X-Frame-Options stop the site
    # (including member and admin pages) being framed for clickjacking; the rest are cheap hardening.
    # ponytail: CSP intentionally only restricts framing/base/plugins — script-src is left open because
    # the pages use inline scripts and CDN libraries; tightening it needs per-script nonces (upgrade path).
    from flask import request as _rq

    @app.after_request
    def _security_headers(resp):
        resp.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
        resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
        resp.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        resp.headers.setdefault('Content-Security-Policy', "frame-ancestors 'self'; object-src 'none'; base-uri 'self'")
        if not app.debug and (_rq.is_secure or _rq.headers.get('X-Forwarded-Proto', '') == 'https'):
            resp.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        return resp

    # Defence-in-depth CSRF: cookies ride every request, so a form posted from another site would carry
    # the victim's session. SameSite=Lax already blocks that cross-site POST; this adds an Origin/Referer
    # same-site check for state-changing methods. It fails open when a browser sends neither header (rare),
    # leaving SameSite as the backstop, and so breaks no normal form or same-origin fetch().
    from urllib.parse import urlparse
    from flask import abort
    _CSRF_EXEMPT = {'pulse.cron_reports', 'reinforce.cron_events'}   # token-authenticated, called by schedulers (no Origin)

    @app.before_request
    def _csrf_same_origin():
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return None
        if (request.endpoint or '') in _CSRF_EXEMPT:
            return None
        stated = request.headers.get('Origin') or request.headers.get('Referer')
        if stated and urlparse(stated).netloc != request.host:
            abort(403, description='Cross-site request blocked.')
        return None

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

    # Custom on-brand line icons available in every template as ea_icon('name')
    # (block, 22px) and ea_icon_i('name') (inline, scales with text).
    _icons = app.jinja_env.get_template('_ea_icons.html').module
    app.jinja_env.globals['ea_icon'] = _icons.ic
    app.jinja_env.globals['ea_icon_i'] = _icons.ic_i

    return app
