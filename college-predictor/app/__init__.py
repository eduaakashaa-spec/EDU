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

    # Create tables if they don't exist
    with app.app_context():
        from app import models  # noqa: F401 – ensure all models are imported
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

    return app
