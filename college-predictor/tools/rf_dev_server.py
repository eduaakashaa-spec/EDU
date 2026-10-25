"""Local preview of EduPulse-Reinforcement with sample data (temp sqlite). Not used in production."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fd, path = tempfile.mkstemp(suffix='.db')
os.close(fd)
os.environ.update(DATABASE_URL='sqlite:///' + path, SECRET_KEY='dev', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.services import reinforce as rf, reinforce_demo  # noqa: E402

app = create_app()
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('demo1234').decode()
    admin = User(name='Admin', email='admin@edupulse.test', tier='admin', password_hash=pw)
    db.session.add(admin)
    db.session.commit()
    rf.seed_taxonomy()
    msg = reinforce_demo.create_demo(admin)
    demo = User.query.filter(User.email.like('demo.reinforce%')).one()
    demo.password_hash = pw
    db.session.commit()
    print('admin@edupulse.test / demo1234 ;', demo.email, '/ demo1234', flush=True)
app.run(port=5077, use_reloader=False)
