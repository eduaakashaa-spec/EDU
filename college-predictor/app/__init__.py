from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Load JOSAA + NIRF data into memory once at startup
    from app.data.loader import load_data
    load_data()

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.api import api_bp
    app.register_blueprint(api_bp)

    return app
