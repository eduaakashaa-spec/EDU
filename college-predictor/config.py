import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'

    # Neon (and most managed Postgres) hand out URLs starting with `postgres://`,
    # but SQLAlchemy 2.x requires the `postgresql://` scheme.
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url and _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = _db_url or (
        'sqlite:///' + os.path.join(basedir, 'instance', 'eduaakashaa.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
        'PHONE_UAE': os.environ.get('PHONE_UAE', '+971 50 516 8081'),
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
