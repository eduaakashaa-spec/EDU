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


def seed_sequences():
    """Create the document-number counters (reference / invoice / receipt)."""
    with app.app_context():
        from app.models_membership import DocSequence
        defaults = [('reference', 'EA-PREM-'), ('invoice', 'EA/'), ('receipt', 'RCPT/')]
        for name, prefix in defaults:
            if db.session.get(DocSequence, name) is None:
                db.session.add(DocSequence(name=name, prefix=prefix, value=0))
        db.session.commit()
        print('Document sequences seeded: reference, invoice, receipt.')


def seed_demo():
    """Insert a few sample membership applications so the admin page isn't empty."""
    with app.app_context():
        from app.models_membership import MembershipApplication, DocSequence
        seed_sequences()
        samples = [
            ('Aarav Sharma', 'aarav@example.com', '9000000001', 'Coimbatore', 'Tamil Nadu', 'Aspirant Path'),
            ('Diya Nair', 'diya@example.com', '9000000002', 'Dubai', 'UAE', 'NRI / Global'),
            ('Rohan Gupta', 'rohan@example.com', '9000000003', 'Chennai', 'Tamil Nadu', 'Foundation Path'),
        ]
        seq = db.session.query(DocSequence).filter_by(name='reference').first()
        for name, email, phone, city, state, tier in samples:
            seq.value += 1
            db.session.add(MembershipApplication(
                reference=f'{seq.prefix}{str(seq.value).zfill(4)}',
                name=name, email=email, phone=phone, city=city, state=state,
                tier=tier, status='New',
            ))
        db.session.commit()
        print(f'Inserted {len(samples)} demo applications.')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('Usage: python manage.py [init_db | create_admin <email> <password> [name] | seed_sequences | seed_demo]')
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
    elif cmd == 'seed_sequences':
        seed_sequences()
    elif cmd == 'seed_demo':
        seed_demo()
    else:
        print(f'Unknown command: {cmd}')
        sys.exit(1)
