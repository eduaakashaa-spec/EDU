"""Management commands — run with: python manage.py <command>"""
import sys
from app import create_app
from app.extensions import db, bcrypt
from app.models import User

app = create_app()


def init_db():
    """Create all tables."""
    with app.app_context():
        db.create_all()
        print('Database tables created.')


def create_admin(email, password, name='Admin'):
    """Create an admin user."""
    with app.app_context():
        if User.query.filter_by(email=email).first():
            print(f'User {email} already exists.')
            return
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password_hash=pw_hash, tier='admin')
        db.session.add(user)
        db.session.commit()
        print(f'Admin user created: {email}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('Usage: python manage.py [init_db | create_admin <email> <password> [name]]')
        sys.exit(1)

    cmd = args[0]
    if cmd == 'init_db':
        init_db()
    elif cmd == 'create_admin':
        if len(args) < 3:
            print('Usage: python manage.py create_admin <email> <password> [name]')
            sys.exit(1)
        name = args[3] if len(args) > 3 else 'Admin'
        create_admin(args[1], args[2], name)
    else:
        print(f'Unknown command: {cmd}')
        sys.exit(1)
