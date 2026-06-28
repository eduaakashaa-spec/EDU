import os
from dotenv import load_dotenv
from app import create_app

# Load local .env if present (development only). Values from the environment
# (e.g. Render) still take precedence.
load_dotenv()

app = create_app()


if __name__ == '__main__':
    # Respect PORT and FLASK_DEBUG env vars so behavior matches local vs prod.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    # When in debug mode enable the reloader so the server restarts on file changes.
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=debug)
