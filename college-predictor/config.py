import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Default OFF: a debug-enabled production process exposes the Werkzeug
    # console. Local dev opts in explicitly via FLASK_DEBUG=1 in .env.
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

    # Fail closed: with a known fallback key anyone can forge a session cookie
    # (i.e. log in as any admin), so only dev gets a throwaway default. In
    # production this stays None and create_app refuses to start.
    SECRET_KEY = os.environ.get('SECRET_KEY') or (
        'dev-key-change-in-production' if DEBUG else None
    )

    # Session cookie hardening. SameSite=Lax is today's browser default, but
    # pinning it here means we don't inherit a weaker default; Secure is off in
    # dev because local runs are plain http.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = not DEBUG

    # Neon (and most managed Postgres) hand out URLs starting with `postgres://`,
    # but SQLAlchemy 2.x requires the `postgresql://` scheme.
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url and _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = _db_url or (
        'sqlite:///' + os.path.join(basedir, 'instance', 'eduaakashaa.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Neon (serverless Postgres) drops idle connections, so pooled connections
    # can go stale and raise `SSL connection has been closed unexpectedly`.
    # Validate each connection before use and recycle below Neon's idle timeout.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,   # validate connections before use (fixes Neon SSL drops)
        'pool_recycle': 280,     # recycle below Neon's idle timeout
    }

    # Cap request bodies. The only large uploads are alumni resume (≤5 MB) +
    # photo (≤3 MB); 10 MB leaves headroom for the rest of the multipart form
    # and stops oversized bodies before they reach a view. A 413 is handled
    # gracefully (see app/__init__.py).
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # ---------------------------------------------------------------------
    # Membership / invoicing (migrated from the Apps Script CONFIG block).
    # Fill the sensitive values via environment variables / .env — never commit.
    # ---------------------------------------------------------------------
    HOME_STATE = os.environ.get('HOME_STATE', 'Tamil Nadu')          # place of supply
    GST_RATE = float(os.environ.get('GST_RATE', '0.18'))             # 18%, prices GST-inclusive
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@eduaakashaa.com')

    COMPANY = {
        'LEGAL_NAME': os.environ.get('COMPANY_LEGAL_NAME', 'EDUAAKASHAA EDUCATIONAL SERVICES PRIVATE LIMITED'),
        'BRAND_NAME': 'EduAakashaa',
        'TAGLINE': 'Guiding students towards the right future',
        'PAN': os.environ.get('COMPANY_PAN', ''),
        'GSTIN': os.environ.get('GSTIN', ''),
        'ADDRESS': os.environ.get('COMPANY_ADDRESS', 'Palani, Tamil Nadu 624615, India'),
        'PHONE_IN': os.environ.get('PHONE_IN', '+91 80157 22706'),
        'EMAIL': os.environ.get('ADMIN_EMAIL', 'info@eduaakashaa.com'),
        'WEBSITE': 'www.eduaakashaa.in',
        'LOGO_URL': os.environ.get('LOGO_URL', ''),
        'BANK_AC_NAME': os.environ.get('BANK_AC_NAME', ''),
        'BANK_AC_NO': os.environ.get('BANK_AC_NO', ''),
        'BANK_IFSC': os.environ.get('BANK_IFSC', ''),
        'BANK_NAME': os.environ.get('BANK_NAME', ''),
        'BANK_BRANCH': os.environ.get('BANK_BRANCH', ''),
    }

    # Where generated invoice/receipt PDFs are stored (private, not link-shared).
    PDF_STORAGE_DIR = os.environ.get(
        'PDF_STORAGE_DIR', os.path.join(basedir, 'instance', 'documents')
    )
