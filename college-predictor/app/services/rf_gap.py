"""EduPulse Reinforcement set from a student's JEE self-assessment (the gap map).

targets(user_id)          -> the bank chapters to practise, most marks within reach first, each with the reason from the gap map
assign_defaults(...)      -> default question sets for those chapters, one assignment per chapter, released a few days apart so the student is not flooded
open_assignment(...)      -> the student's open assignment for a study-plan task, so the plan's button opens the right question set

Only chapters the question bank covers can be assigned (data/jee_topics.RF_CHAPTER); the rest are returned as `missing` so a mentor knows where questions still have to be written.
"""
from datetime import timedelta

from flask import g

from app.extensions import db
from app.data.jee_topics import RF_CHAPTER, TOPICS
from app.models_planner import SpAssessment
from app.models_reinforce import RfAssignment, RfAssignmentStudent, RfStudent
from app.services import jee_gap as G
from app.services import reinforce as rf

MIN_QUESTIONS = 3                    # fewest approved questions a chapter needs before a set is made
TITLE = 'Gap map: '                  # every default set starts with this, which also keeps the call repeatable
_NAME_TO_CODE = {t[2]: t[0] for t in TOPICS}


def latest_assessment(user_id):
    return SpAssessment.query.filter_by(user_id=user_id).order_by(SpAssessment.id.desc()).first()


def targets(user_id, buckets=('Fix first', 'Fix next')):
    """[{chapter, subject, bucket, risk, rating, topics, why}] one row per bank chapter, strongest first; [] without an assessment. `missing` topics have no bank chapter."""
    asm = latest_assessment(user_id)
    if not asm:
        return [], []
    by_ch, missing = {}, []
    for x in G.analyse(asm.ratings)['rows']:
        if x['bucket'] not in buckets:
            continue
        ch = RF_CHAPTER.get(x['code'])
        if not ch:
            missing.append(x)
            continue
        row = by_ch.setdefault(ch, dict(chapter=ch, subject=x['subject'], bucket=x['bucket'], risk=0.0, rating=x['rating'], topics=[], why=x['why']))
        row['risk'] += x['risk']
        row['rating'] = min(row['rating'], x['rating'])
        row['topics'].append(x['name'])
        if x['bucket'] == 'Fix first':
            row['bucket'] = 'Fix first'
    return sorted(by_ch.values(), key=lambda r: -r['risk']), missing


def _mix(row):
    """Difficulty counts of (easy, medium, hard): a weak topic starts easy and builds up; a topic nearer the target gets more medium and hard."""
    n = 10 if row['bucket'] == 'Fix first' else 8
    if row['rating'] <= 1:
        e, h = round(n * .4), round(n * .1)
    else:
        e, h = round(n * .2), round(n * .3)
    return n, {'1': e, '2': n - e - h, '3': h}


def roster(user, mentor_id):
    """The student's place on the Reinforcement roster (created on first use)."""
    rs = RfStudent.query.filter_by(user_id=user.id).first()
    if not rs:
        rs = RfStudent(user_id=user.id, mentor_id=mentor_id, exam='JEE', grade='12', active=True)
        db.session.add(rs)
        db.session.flush()
    elif not rs.active:
        rs.active = True
    if mentor_id and not rs.mentor_id:
        rs.mentor_id = mentor_id
    return rs


def assign_defaults(user, mentor, limit=8, gap_days=3):
    """Create the default sets. Returns {'made': [titles], 'skipped': [titles already assigned], 'thin': [chapters with too few questions], 'missing': [topics without a bank chapter]}."""
    rows, missing = targets(user.id)
    out = {'made': [], 'skipped': [], 'thin': [], 'missing': [m['name'] for m in missing], 'no_assessment': latest_assessment(user.id) is None, 'bank_empty': rf.approved('JEE').count() == 0}
    if out['no_assessment'] or out['bank_empty']:
        return out                     # nothing to assign from: the bank is loaded by an admin (EduPulse Reinforcement, Admin, Load question bank)
    rs = roster(user, mentor.id if mentor else None)
    have = {a.title for a in db.session.query(RfAssignment).join(RfAssignmentStudent, RfAssignmentStudent.assignment_id == RfAssignment.id).filter(RfAssignmentStudent.student_id == rs.id)}
    start = rf.now()
    made = 0
    for row in rows:
        if made >= limit:
            break
        title = TITLE + row['chapter']
        if title in have:
            out['skipped'].append(title)
            continue
        if rf.approved('JEE').filter_by(chapter=row['chapter']).count() < MIN_QUESTIONS:
            out['thin'].append(row['chapter'])
            continue
        n, mix = _mix(row)
        picks = rf.pick_questions('JEE', row['subject'], row['chapter'], None, n, mix, [rs.id])
        if not picks.get(rs.id):
            out['thin'].append(row['chapter'])
            continue
        when = start + timedelta(days=gap_days * made)
        objective = '%s: %s' % (row['bucket'], '; '.join(row['topics']))[:300]
        rf.create_assignment(mentor or user, {'title': title, 'exam': 'JEE', 'subject': row['subject'], 'chapter': row['chapter'], 'objective': objective,
                                              'instructions': 'Chosen from your JEE self-assessment: %s Check each answer and rate your confidence before you move on.' % row['why'],
                                              'n': n, 'mix': mix, 'selection': 'recommended', 'start_at': when, 'due_at': when + timedelta(days=gap_days + 4), 'popup': 'dismissible'},
                             [rs.id], picks)
        out['made'].append(title)
        made += 1
    return out


def rf_chapter_of(task_chapter):
    """The bank chapter for a study-plan task's chapter, which is a self-assessment topic name or already a bank chapter."""
    code = _NAME_TO_CODE.get(task_chapter)
    return RF_CHAPTER.get(code) if code else task_chapter


def _open(user_id):
    """{bank chapter: (assignment_student, assignment)} for the student's started, unfinished sets; read once per request."""
    cache = g.__dict__.setdefault('_rf_open', {})
    if user_id not in cache:
        out = {}
        rs = RfStudent.query.filter_by(user_id=user_id, active=True).first()
        if rs:
            now = rf.now()
            q = (db.session.query(RfAssignmentStudent, RfAssignment).join(RfAssignment, RfAssignment.id == RfAssignmentStudent.assignment_id)
                 .filter(RfAssignmentStudent.student_id == rs.id, RfAssignmentStudent.status != 'completed', RfAssignment.status == 'active', RfAssignment.start_at <= now)
                 .order_by(RfAssignment.start_at))
            for x, a in q.all():
                out.setdefault(a.chapter, (x, a))
        cache[user_id] = out
    return cache[user_id]


def open_assignment(user_id, task_chapter):
    """(assignment_student, assignment, question_count) for a plan task, or None."""
    try:
        hit = _open(user_id).get(rf_chapter_of(task_chapter))
    except Exception:
        return None
    if not hit:
        return None
    x, a = hit
    return x, a, x.items.count()
