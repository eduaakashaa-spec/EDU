"""EduPulse reinforcement options for the weekly plan.

options(user) lists what a student may choose to add to this week, from three sources:
  * weak chapters that EduPulse Reinforcement already flags for the student (JEE and UCEED, when the student is on a mentor's roster),
  * the student's own assessment results (Stream Selection and the other assessments they completed): the recommended path and, when it is low, the aptitude score,
  * the chapters the student rated 1 or 2 on a Class 12 PCM or PCB dashboard.
choose() records the pick as a request for the mentor. Nothing is assigned until the mentor approves it (decide), so a student can never start an assignment on their own and the mentor stays
in control of the next step, as in the rest of EduPulse Reinforcement.
"""
import json
import re
from datetime import timedelta

from app.extensions import db
from app.models import User
from app.models_reinforce import RfChoice, RfStudent, RfTaxonomy

MAX_OPTIONS = 6
MAX_PER_WEEK = 3


def _slug(s):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')[:40]


def _assessment_options(user):
    from app.services import assessments
    out = []
    try:
        rows = [r for r in assessments.for_user(user).limit(6).all()]
    except Exception:
        return out
    if not rows:
        return out
    latest = rows[0]
    label = (latest.result_label or '').strip()
    low = label.lower()
    scores = latest.scores if hasattr(latest, 'scores') else {}
    shown = ', '.join('%s %s%%' % (k, int(float(v))) for k, v in list(scores.items())[:3]) if scores else ''
    base = 'Your %s result recommends: %s.%s' % (assessments.label_for(latest.source), label, (' Scores: ' + shown + '.') if shown else '')
    if label and any(w in low for w in ('pcm', 'engineer', 'maths', 'mathematics', 'physics')):
        out.append({'key': 'a:track-jee', 'source': 'assessment', 'target': 'reinforce', 'exam': 'JEE', 'subject': '', 'chapter': '', 'title': 'Starter set for your engineering path: mixed Maths, Physics and Chemistry',
                    'why': base + ' A short mixed set shows which chapters need work first; your mentor then picks the chapters.'})
    elif label and any(w in low for w in ('pcb', 'medical', 'neet', 'biology', 'doctor')):
        out.append({'key': 'a:track-neet', 'source': 'assessment', 'target': 'mock', 'exam': 'NEET', 'subject': '', 'chapter': '', 'title': 'Practise for your medical path: an EduPulse-NEET subject set',
                    'why': base + ' A subject set in EduPulse-NEET shows where marks are lost; your mentor reviews the result.'})
    apt = latest.result_score
    if apt is not None and apt < 60:
        out.append({'key': 'a:aptitude', 'source': 'assessment', 'target': 'mock', 'exam': 'JEE', 'subject': '', 'chapter': '', 'title': 'Build reasoning and speed with short daily sets',
                    'why': 'Your aptitude score was %d%%. Short, regular sets build speed and accuracy; your mentor can set the pace.' % int(apt)})
    return out


def _weak_options(user):
    from app.services import planner
    out = []
    for subject, chapter in planner.weak_chapters(user.id, 'JEE')[:3]:
        out.append({'key': 'w:JEE:' + _slug(chapter), 'source': 'weak', 'target': 'reinforce', 'exam': 'JEE', 'subject': subject, 'chapter': chapter, 'title': 'Targeted review: ' + chapter,
                    'why': 'EduPulse Reinforcement marks %s (%s) as needing revision from your own answers.' % (chapter, subject)})
    return out


def _dashboard_options(user):
    from app.models_pulse import Class12Profile
    from app.services import pcm12
    out = []
    for row in Class12Profile.query.filter_by(user_id=user.id).all():
        try:
            prof = json.loads(row.data_json or '{}')
        except ValueError:
            continue
        stream = row.stream if row.stream in pcm12.STREAMS else 'pcm'
        weak = []
        for cid, r in (prof.get('ratings') or {}).items():
            ch = pcm12.chapter(cid, stream)
            if ch and isinstance(r, int) and r <= 2:
                weak.append((r, -ch['marks'], ch))
        weak.sort(key=lambda x: (x[0], x[1]))
        for r, _m, ch in weak[:2]:
            out.append({'key': 'd:%s:%s' % (stream, ch['id']), 'source': 'dashboard', 'target': 'mock', 'exam': 'NEET' if stream == 'pcb' else 'JEE', 'subject': pcm12.cfg(stream)['subj'][ch['subj']], 'chapter': ch['name'],
                        'title': 'Chapter practice: %s' % ch['name'],
                        'why': 'You rated %s %d out of 5 on your Class 12 %s dashboard (about %s marks in the board paper).' % (ch['name'], r, pcm12.cfg(stream)['name'], ch['marks'])})
    return out


def options(user, week=None):
    """The options this student may choose now: [{key, source, target, exam, subject, chapter, title, why, state}] where state is '' or the status of an earlier choice this week."""
    seen, out = set(), []
    for o in _weak_options(user) + _assessment_options(user) + _dashboard_options(user):
        if o['key'] in seen:
            continue
        seen.add(o['key'])
        out.append(dict(o, state=''))
    if week is not None:
        mine = {c.key: c for c in RfChoice.query.filter_by(user_id=user.id, week_start=week).all()}
        for o in out:
            if o['key'] in mine:
                o['state'] = mine[o['key']].status
                o['choice_id'] = mine[o['key']].id
    return out[:MAX_OPTIONS]


def mentor_of(user):
    from app.models_mentorship import MsEnrolment
    e = MsEnrolment.query.filter_by(student_id=user.id).order_by(MsEnrolment.id.desc()).first()
    if e and e.mentor_id:
        return e.mentor_id
    rs = RfStudent.query.filter_by(user_id=user.id).first()
    return rs.mentor_id if rs else None


def choose(user, key, week):
    """Record the student's pick as a request. Returns (choice, error). Only keys currently offered can be chosen; at most MAX_PER_WEEK a week."""
    opt = next((o for o in options(user, week) if o['key'] == key), None)
    if not opt:
        return None, 'That option is not available any more.'
    if opt['state']:
        return RfChoice.query.filter_by(user_id=user.id, key=key, week_start=week).first(), None
    if RfChoice.query.filter_by(user_id=user.id, week_start=week).filter(RfChoice.status != 'declined').count() >= MAX_PER_WEEK:
        return None, 'You can ask for up to %d reinforcement options a week. Withdraw one or wait for your mentor.' % MAX_PER_WEEK
    c = RfChoice(user_id=user.id, mentor_id=mentor_of(user), key=key, source=opt['source'], target=opt['target'], exam=opt['exam'], subject=opt['subject'] or None, chapter=opt['chapter'] or None,
                 title=opt['title'][:200], why=opt['why'], week_start=week)
    db.session.add(c)
    db.session.commit()
    if c.mentor_id:
        from app.services import reinforce as rf
        rf.notify(c.mentor_id, 'choice', '%s asked for EduPulse reinforcement: %s' % (user.name, c.title), '/mentorship/', 'rfchoice-%d' % c.id)
    return c, None


def withdraw(user, cid):
    c = db.session.get(RfChoice, cid)
    if not c or c.user_id != user.id or c.status != 'requested':
        return False
    db.session.delete(c)
    db.session.commit()
    return True


def for_week(user, week):
    return RfChoice.query.filter_by(user_id=user.id, week_start=week).order_by(RfChoice.id).all()


def pending_for(enrolment):
    """Requests from this enrolment's student that wait for a decision."""
    return RfChoice.query.filter_by(user_id=enrolment.student_id, status='requested').order_by(RfChoice.created_at).all()


def decide(choice, mentor, approve, note=''):
    """Mentor decision. Approving creates the assignment when the student is on the reinforcement roster and the bank has questions for the chapter or subject; otherwise the choice is approved and the note
    says the mentor will set the work. Returns a short message for the mentor."""
    from app.services import reinforce as rf
    from app.models_reinforce import RfQuestion
    from datetime import datetime
    choice.status = 'approved' if approve else 'declined'
    choice.mentor_note = (note or '')[:400]
    choice.decided_at = datetime.utcnow()
    msg = 'Declined.'
    if approve:
        msg = 'Approved. Please set the work for this student in EduPulse Reinforcement or the mock centre.'
        rs = RfStudent.query.filter_by(user_id=choice.user_id, active=True).first()
        if rs and choice.target == 'reinforce' and choice.exam in ('JEE', 'UCEED'):
            q = rf.approved(choice.exam)
            if choice.subject:
                q = q.filter_by(subject=choice.subject)
            if choice.chapter:
                q = q.filter_by(chapter=choice.chapter)
            if q.count() >= 3:
                picks = rf.pick_questions(choice.exam, choice.subject or None, choice.chapter or None, None, 8, None, [rs.id])
                a = rf.create_assignment(mentor, {'title': choice.title, 'exam': choice.exam, 'subject': choice.subject, 'chapter': choice.chapter, 'selection': 'recommended', 'n': 8,
                                                  'due_at': rf.now() + timedelta(days=3), 'objective': (choice.why or '')[:300]}, [rs.id], picks)
                choice.assignment_id = a.id
                msg = 'Approved and assigned: %s.' % a.title
    db.session.commit()
    rf.notify(choice.user_id, 'choice', ('Your mentor approved: %s' if approve else 'Your mentor declined: %s') % choice.title + ((' (%s)' % note[:80]) if note else ''), '/mentorship/', 'rfdec-%d' % choice.id)
    return msg
