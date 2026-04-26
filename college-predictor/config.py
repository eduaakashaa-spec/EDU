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
