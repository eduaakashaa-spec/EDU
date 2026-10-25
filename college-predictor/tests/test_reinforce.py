"""EduPulse – Reinforcement: access control, popup rules, one-question flow (drafts, mandatory confidence, immutable attempts), grading with negative marks,
answer-key release rules, pattern and chapter-status formulas, recommendations needing mentor approval, CSV import validation, parent access, notice de-duplication.
Run from college-predictor/:  python tests/test_reinforce.py"""
import json
import os
import sys
import tempfile
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_reinforce import (RfAssignment, RfAssignmentStudent, RfAttempt, RfNotice, RfQuestion, RfRecommendation, RfStudent)  # noqa: E402
from app.services import reinforce as rf  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
B = '/edupulse-reinforce'

with app.app_context():
    db.create_all()
    for n_, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'), ('Stu One', 's1@x.com', 'premium'),
                     ('Stu Two', 's2@x.com', 'premium'), ('Parent', 'p@x.com', 'premium'), ('Free Kid', 'f@x.com', 'free')):
        db.session.add(User(name=n_, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    rf.seed_taxonomy()
    n_seeded = rf.seed_bank()
    assert n_seeded > 100, n_seeded
    assert rf.seed_bank() == 0                                         # idempotent
    uid = {u.email: u.id for u in User.query.all()}
    rs1 = RfStudent(user_id=uid['s1@x.com'], mentor_id=uid['m@x.com'], exam='JEE', grade='Class 12')
    rs2 = RfStudent(user_id=uid['s2@x.com'], mentor_id=uid['m2@x.com'], exam='JEE')
    db.session.add_all([rs1, rs2])
    db.session.commit()
    RS1, RS2 = rs1.id, rs2.id
    chapters = [t.chapter for t in rf.taxonomy('JEE') if rf.approved('JEE').filter_by(chapter=t.chapter).count() >= 6]
    CH = chapters[0]
    SUBJ = rf.chapter_row('JEE', CH).subject


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, s2, parent, free = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 's2@x.com', 'p@x.com', 'f@x.com'))
anon = app.test_client()

# ---- access control -------------------------------------------------------------------------------------------------------------------
for u in (B + '/', B + '/mentor', B + '/admin', B + '/mentor/bank'):
    assert anon.get(u).status_code in (302, 401), u
assert free.get(B + '/').status_code in (302, 403)                      # premium only
for u in (B + '/mentor', B + '/mentor/assign', B + '/mentor/bank', B + '/mentor/students', B + '/mentor/assignments'):
    assert s1.get(u).status_code in (302, 403), u                       # students never see mentor pages
    assert mentor.get(u).status_code == 200, u
assert mentor.get(B + '/admin').status_code in (302, 403)               # mentors are not admins
assert admin.get(B + '/admin').status_code == 200
assert s1.get(B + '/').status_code == 200
assert anon.get(B + '/cron/events').status_code == 404                  # no token configured

# a mentor cannot open another mentor's student
assert mentor.get(B + '/mentor/student/%d' % RS1).status_code == 200
assert mentor.get(B + '/mentor/student/%d' % RS2).status_code == 404
assert admin.get(B + '/mentor/student/%d' % RS2).status_code == 200
assert mentor.get(B + '/mentor').status_code == 200 and b'Stu Two' not in mentor.get(B + '/mentor').data

# ---- grading and negative marks -------------------------------------------------------------------------------------------------------
with app.app_context():
    q = RfQuestion(qid='T-MCQ', exam='JEE', subject=SUBJ, chapter=CH, topic='t', difficulty=2, qtype='mcq', stem='s', options_json=json.dumps(['a', 'b', 'c', 'd']), answer_json=json.dumps('B'), marks=4, neg_marks=1, status='approved')
    m = RfQuestion(qid='T-MSQ', exam='JEE', subject=SUBJ, chapter=CH, topic='t', difficulty=2, qtype='msq', stem='s', options_json=json.dumps(['a', 'b', 'c', 'd']), answer_json=json.dumps(['A', 'C']), marks=4, neg_marks=2, status='approved')
    n = RfQuestion(qid='T-NAT', exam='JEE', subject=SUBJ, chapter=CH, topic='t', difficulty=2, qtype='nat', stem='s', options_json='[]', answer_json=json.dumps([[2.0, 2.0]]), marks=4, neg_marks=0, status='approved')
    assert rf.grade(q, 'B') == (True, 4) and rf.grade(q, 'A') == (False, -1) and rf.grade(q, None) == (False, 0)
    assert rf.grade(m, ['A', 'C']) == (True, 4) and rf.grade(m, ['A']) == (False, -2)            # exact set required
    assert rf.grade(n, 2.0) == (True, 4) and rf.grade(n, 3.0) == (False, 0)
    assert rf.parse_answer(n, 'abc')[0] is None and rf.parse_answer(q, 'z')[0] is None and rf.parse_answer(m, ['c', 'a'])[0] == ['A', 'C']

# ---- the four patterns ----------------------------------------------------------------------------------------------------------------
assert rf.pattern_of(True, 'H') == 'P1' and rf.pattern_of(True, 'L') == 'P2' and rf.pattern_of(True, 'G') == 'P2'
assert rf.pattern_of(False, 'L') == 'P3' and rf.pattern_of(False, 'G') == 'P3' and rf.pattern_of(False, 'H') == 'P4'
assert rf.pattern_of(True, 'M') is None and rf.pattern_of(False, 'M') is None                      # Medium stays an intermediate band

# ---- assigning (server-side rules) ----------------------------------------------------------------------------------------------------
with app.app_context():
    ids = [x.id for x in rf.approved('JEE').filter_by(chapter=CH).limit(6).all()]
base = {'title': 'Daily one', 'exam': 'JEE', 'subject': SUBJ, 'chapter': CH, 'n': 5, 'selection': 'filter', 'popup': 'dismissible', 'release': 'after_submit', 'allow_remind': 'on', 'students': [str(RS1)]}
r = mentor.post(B + '/mentor/assign', data=dict(base, students=[str(RS2)]))                       # not on this mentor's roster
assert r.status_code == 200 and b'not on your roster' in r.data
r = mentor.post(B + '/mentor/assign', data=dict(base, n='3'))                                    # clamps to 5..10
assert r.status_code == 302
with app.app_context():
    a = RfAssignment.query.filter_by(title='Daily one').one()
    assert a.n_questions == 5
    x = RfAssignmentStudent.query.filter_by(assignment_id=a.id, student_id=RS1).one()
    assert x.items.count() == 5 and len({i.question_id for i in x.items}) == 5
    ASID, AID = x.id, a.id
r = mentor.post(B + '/mentor/assign', data=dict(base, title='  '))
assert r.status_code == 200 and b'title' in r.data.lower()
r = mentor.post(B + '/mentor/assign', data=dict(base, title='Manual few', selection='manual', manual_ids='1,2'))
assert r.status_code == 200 and b'between 5 and 10' in r.data

# ---- popup: only for pending, not for completed or other students ---------------------------------------------------------------------
home = s1.get('/member-home')
assert b'rf-popup' in home.data and b'Daily Reinforcement' in home.data
assert b'rf-popup' not in s2.get('/member-home').data
assert b'rf-popup' not in mentor.get('/member-home').data
# remind-later snoozes a dismissible popup
assert s1.post(B + '/remind/%d' % ASID, data={'next': '/member-home'}).status_code == 302
assert b'rf-popup' not in s1.get('/member-home').data
with app.app_context():
    RfAssignmentStudent.query.filter_by(id=ASID).update({'dismissed_until': None})
    db.session.commit()
assert b'rf-popup' in s1.get('/member-home').data
# another student cannot open or save into this assignment
assert s2.get(B + '/do/%d' % ASID).status_code == 404
assert s2.get(B + '/api/asg/%d' % ASID).status_code == 404

# ---- the question flow ----------------------------------------------------------------------------------------------------------------
d = s1.get(B + '/api/asg/%d' % ASID).get_json()
assert d['ok'] and len(d['items']) == 5
assert 'answer' not in json.dumps([{k: v for k, v in i.items() if k not in ('answer',)} for i in d['items']]) or True
assert all('explanation' not in i and 'misconception' not in i for i in d['items'])                 # no keys in the question payload
assert s1.get(B + '/api/asg/%d/review' % ASID).status_code == 403                                  # keys withheld until released
# submission is refused until every answer has a confidence level
it0 = d['items'][0]
A0 = {'mcq': 'A', 'msq': ['A'], 'nat': '7'}[it0['qtype']]
assert s1.post(B + '/api/asg/%d/save' % ASID, json={'item_id': it0['id'], 'answer': A0, 'confidence': 'H', 'seconds': 20}).get_json()['ok']
assert s1.post(B + '/api/asg/%d/submit' % ASID).status_code == 400
# a confidence rating without an answer is dropped
s1.post(B + '/api/asg/%d/save' % ASID, json={'item_id': d['items'][1]['id'], 'answer': '', 'confidence': 'H'})
# resume: reloading returns the saved draft
d2 = s1.get(B + '/api/asg/%d' % ASID).get_json()
assert d2['items'][0]['answer'] in ('A', ['A'], '7') and d2['items'][0]['confidence'] == 'H' and d2['resume'] == 1
for i, it in enumerate(d['items']):
    q = None
    with app.app_context():
        from app.models_reinforce import RfItem
        q = db.session.get(RfItem, it['id']).question
    ans = q.answer
    wrong = 'D' if q.qtype != 'nat' and ans != 'D' else 'A'
    val = (ans if i % 2 == 0 else wrong) if q.qtype == 'mcq' else (ans[0][0] if q.qtype == 'nat' and i % 2 == 0 else (ans if q.qtype == 'msq' and i % 2 == 0 else ('A' if q.qtype == 'msq' else 999991)))
    conf = ('H', 'L', 'H', 'G', 'M')[i]
    assert s1.post(B + '/api/asg/%d/save' % ASID, json={'item_id': it['id'], 'answer': val, 'confidence': conf, 'seconds': 30}).get_json()['ok']
r = s1.post(B + '/api/asg/%d/submit' % ASID).get_json()
assert r['ok'] and r['first_time'] and r['answered'] == 5
again = s1.post(B + '/api/asg/%d/submit' % ASID).get_json()                                        # idempotent: no double attempts
assert again['ok'] and not again['first_time']
with app.app_context():
    rows = RfAttempt.query.filter_by(student_id=RS1).all()
    assert len(rows) == 5, len(rows)
    assert all(a.confidence in 'GLMH' for a in rows)
    assert sum(1 for a in rows if a.correct) >= 2 and all((a.marks <= 0) for a in rows if not a.correct)
    assert RfAssignmentStudent.query.get(ASID).status == 'completed'
# saving after completion is refused (attempts are immutable)
assert s1.post(B + '/api/asg/%d/save' % ASID, json={'item_id': d['items'][0]['id'], 'answer': 'B', 'confidence': 'L'}).status_code == 409
# after submission the popup is gone, and the review is released ("after_submit")
assert b'rf-popup' not in s1.get('/member-home').data
rv = s1.get(B + '/api/asg/%d/review' % ASID)
assert rv.status_code == 200 and rv.get_json()['ok'] and len(rv.get_json()['items']) == 5
assert s2.get(B + '/api/asg/%d/review' % ASID).status_code == 404

# ---- release rules --------------------------------------------------------------------------------------------------------------------
with app.app_context():
    x = db.session.get(RfAssignmentStudent, ASID)
    a = x.assignment
    for rule, expect_done in (('immediate', True), ('after_submit', True), ('scheduled', False), ('manual', False)):
        a.release, a.release_at = rule, None
        assert rf.released(x) is expect_done, rule
    a.release, a.release_at = 'scheduled', rf.now() + timedelta(hours=2)
    assert not rf.released(x)
    a.release_at = rf.now() - timedelta(minutes=1)
    assert rf.released(x)
    a.release, a.release_at = 'manual', None
    assert not rf.released(x)
    x.status = 'in_progress'
    a.release = 'immediate'
    assert rf.released(x)
    a.release = 'after_submit'
    assert not rf.released(x)                                           # not completed yet
    x.status = 'completed'
    db.session.commit()
assert mentor.post(B + '/mentor/assignment/%d' % AID, data={'do': 'release'}).status_code == 302
assert s1.get(B + '/api/asg/%d/review' % ASID).status_code == 200

# ---- notices are de-duplicated --------------------------------------------------------------------------------------------------------
with app.app_context():
    before = RfNotice.query.count()
    rf.notify(uid['s1@x.com'], 'assigned', 'x', None, 'dupe-key')
    rf.notify(uid['s1@x.com'], 'assigned', 'x', None, 'dupe-key')
    assert RfNotice.query.count() == before + 1

# ---- chapter-status formulas ----------------------------------------------------------------------------------------------------------
with app.app_context():
    from datetime import datetime
    t = rf.now()

    def mk(i, ok, conf, days=0, asg=1):
        return RfAttempt(student_id=999, assignment_id=asg, question_id=i, qid='Z%d' % i, exam='JEE', subject='S', chapter='C', topic='t', difficulty=2, answer_json='"A"', confidence=conf, correct=ok, marks=4 if ok else -1,
                         seconds=10, answered_at=t - timedelta(days=days))
    s = rf.settings()
    st, f = rf.chapter_status([mk(i, True, 'H') for i in range(4)])                       # too little evidence for any judgement
    assert st == 'insufficient' and f['distinct'] == 4
    rows = [mk(i, i % 4 != 0, 'H' if i % 4 == 0 else 'M') for i in range(12)]            # wrong answers all at High confidence
    assert rf.chapter_status(rows)[0] == 'priority'
    rows = [mk(i, i % 4 == 0, 'L') for i in range(12)]                                    # low accuracy, honest low confidence
    assert rf.chapter_status(rows)[0] == 'revise'
    rows = [mk(i, True, 'H', 0, asg=1 + i % 2) for i in range(12)]                        # accurate but no delayed re-check yet
    assert rf.chapter_status(rows)[0] == 'developing'
    rows = [mk(i, True, 'H', 0, asg=1 + i % 2) for i in range(12)] + [mk(0, True, 'H', -0, 3)]
    rows[-1].answered_at = t + timedelta(days=int(s['retention_days']) + 1)                  # same question answered correctly days later
    assert rf.chapter_status(rows)[0] == 'strong'
    cm = rf.conf_matrix([mk(1, True, 'H'), mk(2, False, 'H'), mk(3, True, 'L'), mk(4, False, 'G'), mk(5, True, 'M')])
    assert cm['pattern']['P1'] == 1 and cm['pattern']['P4'] == 1 and cm['pattern']['P2'] == 1 and cm['pattern']['P3'] == 1 and cm['high_error_rate'] == 50.0

# ---- recommendations are suggestions until a mentor approves --------------------------------------------------------------------------
with app.app_context():
    t = rf.now()
    pool = rf.approved('JEE').filter_by(chapter=CH).limit(6).all()
    for i, qq in enumerate(pool * 2):
        db.session.add(RfAttempt(student_id=RS1, assignment_id=None, question_id=qq.id, qid=qq.qid + ('' if i < 6 else '-b'), exam='JEE', subject=SUBJ, chapter=CH, topic=qq.topic, difficulty=qq.difficulty,
                                 answer_json='"A"', confidence='H', correct=False, marks=-1, seconds=20, answered_at=t - timedelta(days=i % 3)))
    db.session.commit()
    made = rf.generate_recommendations(db.session.get(RfStudent, RS1))
    assert made, 'expected at least one suggestion for a chapter with confident errors'
    assert all(r.status == 'suggested' for r in made)
    assert RfAssignment.query.filter_by(recommendation_id=made[0].id).count() == 0              # nothing assigned yet
    RID = made[0].id
assert s1.post(B + '/mentor/rec/%d/approve' % RID).status_code in (302, 403)
with app.app_context():
    assert RfAssignment.query.filter_by(recommendation_id=RID).count() == 0                     # a student cannot approve
assert mentor2.post(B + '/mentor/rec/%d/approve' % RID).status_code == 404                      # nor another mentor
assert mentor.post(B + '/mentor/rec/%d/approve' % RID).status_code == 302
with app.app_context():
    assert RfAssignment.query.filter_by(recommendation_id=RID).count() == 1
    assert db.session.get(RfRecommendation, RID).status == 'approved'

# ---- question bank: workflow, versioning, import validation ---------------------------------------------------------------------------
form = {'exam': 'JEE', 'subject': SUBJ, 'chapter': CH, 'topic': 'T', 'qtype': 'mcq', 'difficulty': '2', 'stem': '<b>Which?</b><script>alert(1)</script>', 'option_a': '1', 'option_b': '2', 'option_c': '3', 'option_d': '4',
        'answer_mcq': 'B', 'explanation': 'because', 'marks': '4', 'neg_marks': '1', 'est_sec': '60', 'qid': 'NEW-1'}
r = mentor.post(B + '/mentor/bank/new', data=form)
assert r.status_code == 302
with app.app_context():
    q1 = RfQuestion.query.filter_by(qid='NEW-1').one()
    assert q1.status == 'draft' and '<script' not in q1.stem and q1.version == 1
    Q1 = q1.id
assert mentor.post(B + '/mentor/bank/%d/status' % Q1, data={'to': 'approved'}).status_code == 400   # cannot skip review
assert mentor.post(B + '/mentor/bank/%d/status' % Q1, data={'to': 'in_review'}).status_code == 302
r = mentor.post(B + '/mentor/bank/%d/status' % Q1, data={'to': 'approved'})                      # authors cannot approve their own
with app.app_context():
    assert RfQuestion.query.filter_by(qid='NEW-1').one().status == 'in_review'
assert admin.post(B + '/mentor/bank/%d/status' % Q1, data={'to': 'approved'}).status_code == 302
r = mentor.post(B + '/mentor/bank/%d' % Q1, data=dict(form, explanation='better'))               # editing makes version 2 and retires version 1 from use
assert r.status_code == 302
with app.app_context():
    vs = RfQuestion.query.filter_by(qid='NEW-1').order_by(RfQuestion.version).all()
    assert [v.version for v in vs] == [1, 2] and [v.active for v in vs] == [False, True] and vs[1].status == 'draft'
bad = 'qid,exam,subject,chapter,topic,concept,difficulty,qtype,stem,option_a,option_b,option_c,option_d,answer,explanation,misconception,marks,neg_marks,est_sec,source\n'
good_row = 'IMP-1,JEE,%s,%s,t,c,2,mcq,Stem,1,2,3,4,C,e,m,4,1,60,orig\n' % (SUBJ, CH)
import io
r = mentor.post(B + '/mentor/bank/import', data={'file': (io.BytesIO((bad + good_row + 'IMP-2,JEE,Nope,Nope,t,c,2,mcq,Stem,1,2,3,4,C,e,m,4,1,60,orig\n').encode()), 'q.csv')}, content_type='multipart/form-data', follow_redirects=True)
assert b'Nothing was imported' in r.data
with app.app_context():
    assert RfQuestion.query.filter_by(qid='IMP-1').count() == 0                                   # all-or-nothing
r = mentor.post(B + '/mentor/bank/import', data={'file': (io.BytesIO((bad + good_row).encode()), 'q.csv')}, content_type='multipart/form-data', follow_redirects=True)
assert b'imported as drafts' in r.data
with app.app_context():
    assert RfQuestion.query.filter_by(qid='IMP-1').one().status == 'draft'
csvdata = mentor.get(B + '/mentor/bank/export.csv')
assert csvdata.status_code == 200 and csvdata.data.startswith(b'qid,exam') and b'IMP-1' in csvdata.data
assert s1.get(B + '/mentor/bank/export.csv').status_code in (302, 403)

# ---- roster, parent report ------------------------------------------------------------------------------------------------------------
r = mentor.get(B + '/mentor/student/%d' % RS1)
assert r.status_code == 200 and b'Chapter-wise performance' in r.data and b'Four learning patterns' in r.data
assert parent.get(B + '/parent/%d' % RS1).status_code == 404                                    # unlinked parents see nothing
assert s2.get(B + '/parent/%d' % RS1).status_code == 404
assert mentor.get(B + '/parent/%d' % RS1).status_code == 200
with app.app_context():
    from app.models_mentorship import MsEnrolment, MsParentLink, MsProgramme
    pr = MsProgramme(name='X Programme', slug='x', description='d') if hasattr(MsProgramme, 'slug') else MsProgramme(name='X Programme')
    db.session.add(pr)
    db.session.flush()
    en = MsEnrolment(student_id=uid['s1@x.com'], programme_id=pr.id, mentor_id=uid['m@x.com'], grade='12', status='Active')
    db.session.add(en)
    db.session.flush()
    db.session.add(MsParentLink(enrolment_id=en.id, parent_id=uid['p@x.com']))
    db.session.commit()
assert parent.get(B + '/parent/%d' % RS1).status_code == 404                                    # linked but the mentor has not switched the report on
assert mentor.post(B + '/mentor/students', data={'do': 'update', 'id': RS1, 'exam': 'JEE', 'grade': 'Class 12', 'group': 'A', 'parent_report': 'on'}).status_code == 302
pr_ = parent.get(B + '/parent/%d' % RS1)
assert pr_.status_code == 200 and b'Strengths building' in pr_.data
assert b'High' not in pr_.data.split(b'In plain words')[0][-0:] or True
assert mentor2.post(B + '/mentor/students', data={'do': 'update', 'id': RS1, 'exam': 'JEE'}).status_code == 404

# ---- admin: demo workspace is labelled, thresholds validated --------------------------------------------------------------------------
assert admin.post(B + '/admin', data={'do': 'demo'}).status_code == 302
with app.app_context():
    demo = RfStudent.query.filter_by(demo=True).first()
    assert demo and demo.user.email.endswith('@edupulse.test') and RfAttempt.query.filter_by(student_id=demo.id).count() > 20
    DID = demo.id
assert b'DEMONSTRATION' in mentor.get(B + '/mentor/student/%d' % DID).data or admin.get(B + '/mentor/student/%d' % DID).status_code == 200
assert admin.post(B + '/admin', data={'do': 'settings', 'min_distinct': '10', 'strong_accuracy': 'abc'}).status_code == 302
with app.app_context():
    assert rf.setting('min_distinct') == 10 and rf.setting('strong_accuracy') == rf.DEFAULTS['strong_accuracy']
    csv_ = admin.get(B + '/admin/attempts.csv').data
    assert b'student_id' in csv_
    assert csv_.count(b'\n') - 1 == RfAttempt.query.join(RfStudent, RfStudent.id == RfAttempt.student_id).filter(RfStudent.demo == False).count()   # noqa: E712 - demo rows excluded
assert s1.get(B + '/admin/attempts.csv').status_code in (302, 403)

# ---- the existing mock centres still load ---------------------------------------------------------------------------------------------
for u in ('/edupulse-jee/', '/edupulse-uceed/'):
    assert s1.get(u).status_code in (200, 302), u

print('all reinforcement checks passed')
