"""Clearly-labelled demonstration workspace for EduPulse - Reinforcement: a sample student (demo=True, *.test e-mail, excluded from exports) with three weeks of
sample attempts that show every learning pattern, plus one pending assignment so the login popup can be tried. Passwords are random and shown once."""
import json
import random
import secrets
from datetime import timedelta

from app.extensions import bcrypt, db
from app.models import User
from app.models_reinforce import RfAssignment, RfAssignmentStudent, RfAttempt, RfItem, RfObservation, RfStudent
from app.services import reinforce as rf

# chapter -> (probability right, confidence mix when right, confidence mix when wrong)  [sample data, not real results]
PROFILE = {
    'Laws of motion': (0.9, 'HHHM', 'LG'),
    'Work, energy & power': (0.45, 'HHM', 'HHHL'),          # wrong despite high confidence -> priority review
    'Electrostatics': (0.35, 'LGM', 'LGL'),                 # aware gaps
    'Current electricity': (0.72, 'MMLH', 'ML'),
    'Kinematics': (0.8, 'LLMH', 'LG'),                       # right but unsure
}


def create_demo(admin):
    rf.seed_bank()
    rng = random.Random(25)
    tag = secrets.token_hex(2)
    pw = secrets.token_urlsafe(9)
    u = User(name='Demo Aarav (sample student)', email='demo.reinforce.%s@edupulse.test' % tag, tier='premium', password_hash=bcrypt.generate_password_hash(pw).decode())
    db.session.add(u)
    db.session.flush()
    rs = RfStudent(user_id=u.id, mentor_id=admin.id, exam='JEE', grade='Class 12', group_name='Demo group', parent_report=True, demo=True)
    db.session.add(rs)
    db.session.flush()
    t0 = rf.now()
    day = 21
    for chapter, (p, hi_right, hi_wrong) in PROFILE.items():
        qs = [q for q in rf.approved('JEE').filter_by(chapter=chapter).all()]
        if len(qs) < 9:
            continue
        for k in range(2):                                    # two sessions per chapter, a few days apart
            chunk = qs[:8] if k == 0 else qs[-8:]             # the second session re-uses some questions: a delayed re-check
            when = t0 - timedelta(days=day - k * 6)
            a = RfAssignment(title='%s practice %d (sample data)' % (chapter, k + 1), exam='JEE', subject=chunk[0].subject, chapter=chapter, n_questions=len(chunk), start_at=when, due_at=when + timedelta(days=1),
                             created_by=admin.id, status='active')
            db.session.add(a)
            db.session.flush()
            s = RfAssignmentStudent(assignment_id=a.id, student_id=rs.id, status='completed', started_at=when, completed_at=when + timedelta(minutes=14))
            db.session.add(s)
            db.session.flush()
            for pos, q in enumerate(chunk, 1):
                db.session.add(RfItem(asg_student_id=s.id, question_id=q.id, position=pos))
                ok = rng.random() < p + (0.08 * k if chapter != 'Work, energy & power' else 0)
                conf = rng.choice(hi_right if ok else hi_wrong)
                ans = q.answer if ok else ('A' if q.qtype == 'mcq' and q.answer != 'A' else q.answer)
                db.session.add(RfAttempt(student_id=rs.id, assignment_id=a.id, question_id=q.id, qid=q.qid, exam='JEE', subject=q.subject, chapter=q.chapter, topic=q.topic, difficulty=q.difficulty,
                                         answer_json=json.dumps(ans), confidence=conf, correct=ok, marks=q.marks if ok else -(q.neg_marks or 0), seconds=rng.randint(40, 160), answered_at=when + timedelta(minutes=pos)))
        day -= 3
    # one pending assignment for today: the login popup
    qs = [q for q in rf.approved('JEE').filter_by(chapter='Work, energy & power').all()][-8:]
    a = RfAssignment(title='Work, energy & power: misconception check (sample)', exam='JEE', subject='Physics', chapter='Work, energy & power', n_questions=len(qs), start_at=t0 - timedelta(hours=1), due_at=t0 + timedelta(hours=30),
                     created_by=admin.id, popup='dismissible', release='after_submit', instructions='Take your time. Rate how sure you are before moving on.')
    db.session.add(a)
    db.session.flush()
    s = RfAssignmentStudent(assignment_id=a.id, student_id=rs.id)
    db.session.add(s)
    db.session.flush()
    for pos, q in enumerate(qs, 1):
        db.session.add(RfItem(asg_student_id=s.id, question_id=q.id, position=pos))
    db.session.add(RfObservation(student_id=rs.id, author_id=admin.id, chapter='Work, energy & power', body='Sample note: confident answers here need a closer look at the work-energy theorem.', for_parent=True))
    db.session.commit()
    rf.generate_recommendations(rs)
    rf.notify(u.id, 'assigned', 'New reinforcement: %s' % a.title, '/edupulse-reinforce/', 'asg-%d' % a.id)
    return 'Demo workspace created (all data is sample data). Student login %s / %s. It is flagged demo and excluded from exports. Save the password now: it is not shown again.' % (u.email, pw)
