"""EduPulse Reinforcement from the JEE gap map: default question sets, and the study plan's button opening the right set. Run from college-predictor/:  python tests/test_rf_gap.py"""
import json
import os
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import darsh_jee_plan as plan  # noqa: E402
from app.data.jee_topics import RF_CHAPTER, TOPICS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_planner import SpAssessment, SpPlan, SpTask  # noqa: E402
from app.models_reinforce import RfAssignment, RfQuestion, RfStudent  # noqa: E402
from app.services import planner as P, reinforce as rf, rf_gap  # noqa: E402

# every self-assessment topic is mapped, and every mapped chapter exists in the bank taxonomy
assert set(RF_CHAPTER) == {t[0] for t in TOPICS}
bank_chapters = {c[1] for chs in rf.JEE_TAXONOMY.values() for c in chs}
assert {v for v in RF_CHAPTER.values() if v} <= bank_chapters, {v for v in RF_CHAPTER.values() if v} - bank_chapters

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    rf.seed_taxonomy()
    for n, em, t in (('Mentor', 'm@x.com', 'ea_mentor'), ('Darsh', 'd@x.com', 'elite')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    db.session.commit()
    mentor, stu = User.query.filter_by(email='m@x.com').one(), User.query.filter_by(email='d@x.com').one()

    # no assessment yet: nothing is assigned
    assert rf_gap.assign_defaults(stu, mentor)['no_assessment'] is True and RfAssignment.query.count() == 0

    db.session.add(SpAssessment(user_id=stu.id, ratings_json=json.dumps(plan.RATINGS)))
    db.session.commit()
    assert rf_gap.assign_defaults(stu, mentor)['bank_empty'] is True and RfAssignment.query.count() == 0       # an unloaded bank is reported, not silently ignored
    rows, missing = rf_gap.targets(stu.id)
    assert rows and rows == sorted(rows, key=lambda r: -r['risk'])
    assert any(m['code'] == 'C14' for m in missing)                       # p-block has no bank chapter yet: reported, never silently dropped
    top = rows[0]['chapter']

    # a bank with 12 approved questions for the top chapter and only 2 for the second
    def add(ch, subj, k):
        for i in range(k):
            db.session.add(RfQuestion(qid='%s-%d' % (ch[:6], i), exam='JEE', subject=subj, chapter=ch, topic=ch, difficulty=1 + i % 3, stem='<p>q</p>', options_json='["A","B","C","D"]',
                                      answer_json='"A"', status='approved', active=True))
    add(top, rows[0]['subject'], 12)
    add(rows[1]['chapter'], rows[1]['subject'], 2)
    db.session.commit()

    r = rf_gap.assign_defaults(stu, mentor)
    assert r['made'] == ['Gap map: ' + top], r
    assert rows[1]['chapter'] in r['thin'] and 'p-block elements' in r['missing']
    rs = RfStudent.query.filter_by(user_id=stu.id).one()
    assert rs.mentor_id == mentor.id and rs.exam == 'JEE'
    a = RfAssignment.query.one()
    assert a.chapter == top and a.n_questions in (8, 10) and a.mix and a.created_by == mentor.id
    assert rf_gap.assign_defaults(stu, mentor)['made'] == [] and RfAssignment.query.count() == 1        # repeating adds nothing

    # the plan's practice task opens that set; other tasks keep the general link
    p = SpPlan(user_id=stu.id, title='t', exam='JEE', level='average', start_date=date(2026, 11, 21), weeks=4, status='active')
    db.session.add(p)
    db.session.flush()
    topic_name = next(t[2] for t in TOPICS if RF_CHAPTER[t[0]] == top)
    t1 = SpTask(plan_id=p.id, day=date(2026, 11, 22), task_type='practice', title='Practise', chapter=topic_name, link_kind='reinforce')
    t2 = SpTask(plan_id=p.id, day=date(2026, 11, 22), task_type='practice', title='Practise', chapter='p-block elements', link_kind='reinforce')
    t3 = SpTask(plan_id=p.id, day=date(2026, 11, 22), task_type='learn', title='Learn', chapter=topic_name)
    db.session.add_all([t1, t2, t3])
    db.session.commit()
    with app.test_request_context('/'):
        lk = P.task_link(t1)
        assert lk and lk[0].startswith('Start ') and '/do/' in lk[1], lk
        assert P.task_link(t2) == P.link_url('reinforce') and P.task_link(t3) is None
print('rf gap checks passed')
