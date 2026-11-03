"""Local preview of EduPulse-Explorer with a demo student (temp sqlite). Not used in production."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
fd, path = tempfile.mkstemp(suffix='.db')
os.close(fd)
os.environ.update(DATABASE_URL='sqlite:///' + path, SECRET_KEY='dev', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

app = create_app()
with app.app_context():
    db.create_all()
    db.session.add(User(name='Demo Student', email='demo@explorer.test', tier='free', password_hash=bcrypt.generate_password_hash('demo1234').decode()))
    db.session.commit()
    print('demo@explorer.test / demo1234', flush=True)
app.run(port=5078, use_reloader=False)
