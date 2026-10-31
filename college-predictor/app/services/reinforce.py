"""EduPulse - Reinforcement: question bank, assignment delivery, grading, chapter analytics, the four learning patterns, recommendations and notices.

Confidence is analysed separately from correctness. The four primary patterns (Medium is kept as its own intermediate band):
  P1 secure          correct + High
  P2 unsure_right    correct + Low or Guess     (knows, lacks confidence, or lucky)
  P3 aware_gap       wrong   + Low or Guess     (a gap the student half-knows about)
  P4 overconfident   wrong   + High             (possible misconception)
These are diagnostic signals over repeated responses, not judgments about a student.
"""
import csv
import html as _html
import io
import json
import os
import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser

from sqlalchemy import func

from app.extensions import db
from app.models_reinforce import (RfQuestionImage, RfAssignment, RfAssignmentStudent, RfAttempt, RfAudit, RfDraft, RfItem, RfNotice, RfObservation, RfQuestion, RfRecommendation, RfSetting, RfStudent, RfTaxonomy, jl)

CONF = (('G', 'Guess'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'))
CONF_LABEL = dict(CONF)
PATTERNS = {
    'P1': ('Knows and is confident', 'Evidence of secure understanding for this question. Reinforce through spaced repetition, then try harder or differently worded questions.'),
    'P2': ('Knows but lacks confidence', 'May understand the concept but is unsure, or may have been lucky. Ask a related question with different wording and have the student explain the reasoning.'),
    'P3': ('Gap the student is aware of', 'A knowledge gap the student half-recognises. Check the prerequisite, give a simpler concept question, then reassess later.'),
    'P4': ('Overconfident error', 'A possible misconception. Review the answer with the student, use a contrasting question and schedule a follow-up.'),
}
STATUS_LABEL = {'none': 'Not assessed yet', 'insufficient': 'Building understanding', 'revise': 'Needs revision', 'priority': 'Priority review', 'improving': 'Improving', 'developing': 'Developing', 'strong': 'Strong evidence of understanding'}
MENTOR_STATUS_LABEL = dict(STATUS_LABEL, insufficient='Insufficient data')
DIFF_LABEL = {1: 'Easy', 2: 'Medium', 3: 'Challenging'}
DEFAULTS = {'min_distinct': 8, 'min_sessions': 2, 'strong_accuracy': 80, 'revise_accuracy': 50, 'improving_delta': 10, 'high_err_rate': 25, 'min_high_n': 3,
            'followup_days': 3, 'retention_days': 5, 'alert_high_errors': 2, 'recent_days': 14, 'min_recent': 4}
SETTING_HELP = {
    'min_distinct': 'Minimum distinct questions attempted in a chapter before any status other than "insufficient data" is shown',
    'min_sessions': 'Minimum number of separate assignments or days before a chapter can be called strong',
    'strong_accuracy': 'Accuracy (%) needed, with enough evidence and a delayed re-check, for "strong evidence of understanding"',
    'revise_accuracy': 'Accuracy (%) below which a chapter "needs revision"',
    'improving_delta': 'Recent accuracy must beat earlier accuracy by this many points to count as "improving"',
    'high_err_rate': 'High-confidence error rate (%) that makes a chapter a priority review',
    'min_high_n': 'Minimum High-confidence answers before the high-confidence error rate is used',
    'followup_days': 'Days before a follow-up question is scheduled after an overconfident error',
    'retention_days': 'Days that must pass before a repeat answer counts as a delayed re-check',
    'alert_high_errors': 'High-confidence errors in one chapter (within the recent window) that alert the mentor',
    'recent_days': 'Length of the "recent" window in days',
    'min_recent': 'Minimum recent attempts in a chapter before a recent-vs-earlier comparison is made',
}
PROTECTED = ('answer_json', 'explanation', 'misconception')


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ---- settings, audit -----------------------------------------------------------------------------------------------------------------
def setting(key):
    row = db.session.get(RfSetting, key)
    try:
        return float(row.value) if row and row.value not in (None, '') else DEFAULTS[key]
    except ValueError:
        return DEFAULTS[key]


def settings():
    return {k: setting(k) for k in DEFAULTS}


def audit(user_id, action, detail=''):
    try:
        db.session.add(RfAudit(user_id=user_id, action=action, detail=(detail or '')[:500]))
        db.session.commit()
    except Exception:
        db.session.rollback()


# ---- html safety (questions are authored by staff but rendered to students) ----------------------------------------------------------
_OK_TAGS = {'p', 'br', 'b', 'i', 'em', 'strong', 'sub', 'sup', 'span', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'img', 'div', 'code', 'u', 'small'}
_OK_ATTRS = {'img': {'src', 'alt', 'width', 'height'}, 'td': {'colspan', 'rowspan'}, 'th': {'colspan', 'rowspan'}}
_VOID = {'br', 'img'}


class _Clean(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.stack = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in _OK_TAGS:
            return
        keep = []
        for k, v in attrs:
            if k in _OK_ATTRS.get(tag, ()):
                v = v or ''
                if k == 'src' and not re.match(r'^(data:image/(png|jpeg|webp|gif);base64,[A-Za-z0-9+/=]+|/static/[\w./-]+|/edupulse-reinforce/qimg/[\w.-]+/[qs])$', v):
                    continue
                keep.append(' %s="%s"' % (k, _html.escape(v, quote=True)))
        if tag == 'img' and not any(a.startswith(' src=') for a in keep):
            return
        self.out.append('<%s%s>' % (tag, ''.join(keep)))
        if tag not in _VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append('</%s>' % t)
                if t == tag:
                    break

    def handle_data(self, data):
        self.out.append(_html.escape(data, quote=False))

    def handle_entityref(self, name):
        self.out.append('&%s;' % name if re.fullmatch(r'[A-Za-z0-9]{1,10}', name) else '')

    def handle_charref(self, name):
        self.out.append('&#%s;' % name if re.fullmatch(r'x?[0-9A-Fa-f]{1,6}', name) else '')


def sanitize(text):
    p = _Clean()
    p.feed(text or '')
    p.close()
    while p.stack:
        p.out.append('</%s>' % p.stack.pop())
    return ''.join(p.out)


# ---- taxonomy ------------------------------------------------------------------------------------------------------------------------
JEE_TAXONOMY = {
    'Mathematics': [('CNQ', 'Complex numbers & quadratics', None), ('SEQ', 'Sequences & series', None), ('PNC', 'Permutations, combinations & binomial', None), ('MAT', 'Matrices & determinants', None),
                    ('LCD', 'Limits & derivatives', None), ('INT', 'Integral calculus', 'LCD'), ('DEQ', 'Differential equations', 'INT'), ('COG', 'Coordinate geometry', None), ('VEC', 'Vectors & 3D geometry', 'COG'),
                    ('STP', 'Statistics & probability', 'PNC'), ('TRG', 'Trigonometry', None), ('SRF', 'Sets, relations & functions', None)],
    'Physics': [('UNM', 'Units & errors', None), ('KIN', 'Kinematics', 'UNM'), ('LOM', 'Laws of motion', 'KIN'), ('WEP', 'Work, energy & power', 'LOM'), ('ROT', 'Rotational motion', 'WEP'), ('GRA', 'Gravitation', 'LOM'),
                ('PMB', 'Properties of matter', 'LOM'), ('THM', 'Thermodynamics (physics)', 'PMB'), ('OSW', 'Oscillations & waves', 'LOM'), ('ELS', 'Electrostatics', None), ('CUR', 'Current electricity', 'ELS'),
                ('MAG', 'Magnetism & EMI', 'CUR'), ('OPT', 'Optics', None), ('DUA', 'Modern physics', None)],
    'Chemistry': [('MOL', 'Mole concept', None), ('ATS', 'Atomic structure', None), ('BON', 'Chemical bonding', 'ATS'), ('THE', 'Chemical thermodynamics', 'MOL'), ('EQU', 'Equilibrium & pH', 'THE'), ('RDX', 'Redox & electrochemistry', 'EQU'),
                  ('CKN', 'Chemical kinetics', 'MOL'), ('SOL', 'Solutions', 'MOL'), ('PER', 'Periodic properties', 'ATS'), ('COO', 'Coordination compounds', 'BON'), ('ORG', 'General organic chemistry', 'BON'),
                  ('HYD', 'Hydrocarbons', 'ORG'), ('HAL', 'Haloalkanes', 'HYD'), ('BIO', 'Biomolecules', 'ORG')],
}
UCEED_TAXONOMY = {'Design aptitude': [('OBS', 'Observation & counting', None), ('NUM', 'Numbers & logic', None), ('SPA', '3D & spatial', None), ('PAT', 'Patterns & transformations', 'OBS'),
                                      ('SCI', 'Everyday science', None), ('VIS', 'Visual design', None), ('CUL', 'Art, culture & language', None)]}


def seed_taxonomy():
    n = 0
    for exam, tax in (('JEE', JEE_TAXONOMY), ('UCEED', UCEED_TAXONOMY)):
        for subj, chs in tax.items():
            for pos, (code, name, pre) in enumerate(chs):
                if not RfTaxonomy.query.filter_by(exam=exam, subject=subj, chapter=name).first():
                    db.session.add(RfTaxonomy(exam=exam, subject=subj, chapter=name, code=code, prereq=pre, position=pos))
                    n += 1
    db.session.commit()
    return n


def taxonomy(exam=None):
    q = RfTaxonomy.query
    if exam:
        q = q.filter_by(exam=exam)
    return q.order_by(RfTaxonomy.exam, RfTaxonomy.subject, RfTaxonomy.position).all()


def chapter_row(exam, chapter):
    return RfTaxonomy.query.filter_by(exam=exam, chapter=chapter).first()


def chapters_of(exam, subject=None):
    q = RfTaxonomy.query.filter_by(exam=exam)
    if subject:
        q = q.filter_by(subject=subject)
    return [t.chapter for t in q.order_by(RfTaxonomy.position)]


def subjects_of(exam):
    return list(dict.fromkeys(t.subject for t in RfTaxonomy.query.filter_by(exam=exam).order_by(RfTaxonomy.id)))


# ---- question bank seeding (from the mock-centre papers: original questions with worked solutions) ------------------------------------------
_MOCK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def _seed_from(path, exam, tag, subj_of):
    n = 0
    try:
        d = json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        return 0
    for q in d['qs']:
        qid = '%s-%s-%03d' % (exam, tag, q['n'])
        if RfQuestion.query.filter_by(qid=qid).first():
            continue
        code = q.get('cat')
        tx = RfTaxonomy.query.filter_by(exam=exam, code=code).first()
        if not tx or q.get('img'):
            continue
        stem = q['stem'] + ('<div class="ofig">%s</div>' % q['fig'] if q.get('fig') else '')
        t = (q.get('t') or 'MCQ').lower()
        if t == 'nat':
            ans = q['acc']['ranges']
            opts = []
        elif t == 'msq':
            ans = sorted(q['acc']['sets'][0])
            opts = q['opts']
        else:
            ans = q['acc']['sets'][0]
            opts = q['opts']
        steps = ''.join('<li>%s</li>' % s for s in q.get('steps', []))
        expl = ('<ol>%s</ol>' % steps if steps else '') + ('<p>%s</p>' % q['note'] if q.get('note') else '')
        db.session.add(RfQuestion(qid=qid, exam=exam, subject=tx.subject, chapter=tx.chapter, topic=tx.chapter, concept=tx.chapter, difficulty=3 if t in ('nat', 'msq') else 2, qtype=t,
                                  stem=stem, options_json=json.dumps(opts), answer_json=json.dumps(ans), explanation=expl, misconception=q.get('trap') or '',
                                  marks=4, neg_marks=1 if exam == 'JEE' else 0, est_sec=120 if t == 'nat' else 90, source='EduAakashaa original (%s %s)' % (exam, tag), status='approved'))
        n += 1
    return n


def seed_guides():
    """Solved previous-year papers from the JEE mock centre (question and worked solution as images, EduAakashaA answers). Idempotent by qid.
    Questions with no valid printed option (key 'bonus') are left out: there is nothing to grade them against."""
    import base64
    data_dir = os.path.join(_MOCK, 'jee_mock', 'data')
    try:
        papers = json.load(open(os.path.join(data_dir, 'index.json'), encoding='utf-8'))['papers']
    except (OSError, ValueError):
        return 0
    n = 0
    for meta in papers:
        if not (meta.get('solved') and meta.get('ready')):
            continue
        try:
            d = json.load(open(os.path.join(data_dir, meta['y'] + '.json'), encoding='utf-8'))
        except (OSError, ValueError):
            continue
        for q in d['qs']:
            qid = 'JEE-%s-%03d' % (meta['y'], q['n'])
            if RfQuestion.query.filter_by(qid=qid).first() or (q.get('acc') or {}).get('bonus'):
                continue
            tx = RfTaxonomy.query.filter_by(exam='JEE', code=q.get('cat')).first()
            if not tx:
                continue
            if q['t'] == 'NAT':
                qt, opts, ans = 'nat', [], q['acc']['ranges']
            else:
                qt, opts, ans = 'mcq', ['1', '2', '3', '4'], q['acc']['sets'][0]          # options are printed as 1-4 inside the image
            for kind, key in (('q', 'img'), ('s', 'sol')):
                if q.get(key):
                    db.session.add(RfQuestionImage(qid=qid, kind=kind, data=base64.b64decode(q[key].split(',', 1)[1])))
            stem = '<img class="rf-qimg" src="/edupulse-reinforce/qimg/%s/q" alt="Question as printed in the paper">' % qid
            expl = '<img class="rf-qimg" src="/edupulse-reinforce/qimg/%s/s" alt="Worked solution">' % qid
            note = '; '.join((d.get('notes') or [])[:1])
            db.session.add(RfQuestion(qid=qid, exam='JEE', subject=tx.subject, chapter=tx.chapter, topic=q.get('chapter') or tx.chapter, concept=tx.chapter, difficulty=2, qtype=qt, stem=stem,
                                      options_json=json.dumps(opts), answer_json=json.dumps(ans), explanation=expl, misconception='', marks=4, neg_marks=1, est_sec=150 if qt == 'nat' else 100,
                                      source='%s, question %d (NTA ID %s). %s' % (meta['title'], q['n'], q.get('qid') or '-', note), status='approved'))
            n += 1
    db.session.commit()
    return n


EXAMS = ('JEE', 'UCEED', 'TN10')                          # TN10 = Tamil Nadu Class 10 (SSLC / Matriculation) Mathematics and Science, in English


def exam_of(value, default='JEE'):
    return value if value in EXAMS else default


def seed_recreated():
    """Recreated previous-year papers of the JEE mock centre (retyped text questions with worked steps, EduAakashaA-checked answers). Idempotent by qid.
    They enter as approved JEE questions tagged with their source paper; the explanation is the worked solution."""
    data_dir = os.path.join(_MOCK, 'jee_mock', 'data')
    try:
        papers = json.load(open(os.path.join(data_dir, 'index.json'), encoding='utf-8'))['papers']
    except (OSError, ValueError):
        return 0
    n = 0
    for meta in papers:
        if not (meta.get('recreated') and meta.get('ready')):
            continue
        try:
            d = json.load(open(os.path.join(data_dir, meta['y'] + '.json'), encoding='utf-8'))
        except (OSError, ValueError):
            continue
        for q in d['qs']:
            qid = 'JEE-%s-%03d' % (meta['y'], q['n'])
            if RfQuestion.query.filter_by(qid=qid).first():
                continue
            tx = RfTaxonomy.query.filter_by(exam='JEE', code=q.get('cat')).first()
            if not tx:
                continue
            if q['t'] == 'NAT':
                qt, opts, ans = 'nat', [], q['acc']['ranges']
            else:
                qt, opts, ans = 'mcq', [sanitize(o) for o in q['opts']], q['acc']['sets'][0]
            expl = '<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in q.get('steps', [])) if q.get('steps') else ''
            db.session.add(RfQuestion(qid=qid, exam='JEE', subject=tx.subject, chapter=tx.chapter, topic=tx.chapter, concept=tx.chapter, difficulty=2, qtype=qt, stem=sanitize(q['stem']),
                                      options_json=json.dumps(opts), answer_json=json.dumps(ans), explanation=sanitize(expl), misconception='', marks=4, neg_marks=1,
                                      est_sec=150 if qt == 'nat' else 100, source='%s, question %d (source question %s). %s' % (meta['title'], q['n'], q.get('src', '-'), '; '.join((d.get('notes') or [])[:1])),
                                      status='approved'))
            n += 1
    db.session.commit()
    return n


def seed_bank():
    """Idempotent: loads the original EduAakashaa mock questions (JEE M1-M5, UCEED M1-M5) into the bank as approved questions."""
    seed_taxonomy()
    n = 0
    for i in range(1, 6):
        n += _seed_from(os.path.join(_MOCK, 'jee_mock', 'data', 'M%d.json' % i), 'JEE', 'M%d' % i, None)
        n += _seed_from(os.path.join(_MOCK, 'uceed_mock', 'data', 'M%d.json' % i), 'UCEED', 'M%d' % i, None)
    db.session.commit()
    n += seed_guides()
    n += seed_recreated()
    from app.services import tn10
    n += tn10.seed_reinforcement()
    return n


# ---- grading -------------------------------------------------------------------------------------------------------------------------
def parse_answer(q, raw):
    """Normalise a submitted answer. Returns (value, error). mcq: 'A'-'D'; msq: sorted list of letters; nat: float."""
    if q.qtype == 'nat':
        try:
            return float(str(raw).replace('−', '-').strip()), None
        except ValueError:
            return None, 'Enter a number.'
    if q.qtype == 'msq':
        vals = sorted({str(x).upper() for x in (raw if isinstance(raw, list) else [raw]) if str(x).upper() in 'ABCD' and str(x)})
        return (vals or None), (None if vals else 'Choose at least one option.')
    v = str(raw or '').upper()
    return (v, None) if v in ('A', 'B', 'C', 'D') else (None, 'Choose an option.')


def grade(q, value):
    """Returns (correct, marks). msq needs the exact set; nat accepts any listed range; negative marks apply to wrong answers only."""
    key = q.answer
    if value is None:
        return False, 0.0
    if q.qtype == 'nat':
        ok = any(lo - 1e-9 <= value <= hi + 1e-9 for lo, hi in key)
    elif q.qtype == 'msq':
        ok = sorted(value) == sorted(key)
    else:
        ok = value == key
    return ok, (q.marks or 0) if ok else -(q.neg_marks or 0)


def pattern_of(correct, conf):
    if conf == 'H':
        return 'P1' if correct else 'P4'
    if conf in ('L', 'G'):
        return 'P2' if correct else 'P3'
    return None


# ---- selection and assignments -------------------------------------------------------------------------------------------------------
def approved(exam=None):
    q = RfQuestion.query.filter_by(status='approved', active=True)
    return q.filter_by(exam=exam) if exam else q


def pick_questions(exam, subject, chapter, topic, n, mix, student_ids, exclude_ids=(), distinct=False, rng=None):
    """Choose questions per student. Prefers questions the student has not answered correctly lately; honours the easy/medium/hard mix when set.
    Returns {student_id: [question, ...]}. With distinct=True, students get different questions where the bank allows."""
    import random
    rng = rng or random.Random()
    q = approved(exam)
    if subject:
        q = q.filter_by(subject=subject)
    if chapter:
        q = q.filter_by(chapter=chapter)
    if topic:
        q = q.filter(RfQuestion.topic == topic)
    pool = [x for x in q.all() if x.id not in set(exclude_ids)]
    out, used = {}, set()
    for sid in student_ids:
        seen = defaultdict(int)
        for qid, ok in db.session.query(RfAttempt.qid, RfAttempt.correct).filter(RfAttempt.student_id == sid).all():
            seen[qid] += 1 if ok else 0
        cand = pool[:]
        rng.shuffle(cand)
        cand.sort(key=lambda x: (seen.get(x.qid, 0), x.id in used if distinct else 0))
        chosen = []
        if mix and sum(int(v) for v in mix.values()) > 0:
            for d, k in sorted(mix.items()):
                chosen += [x for x in cand if x.difficulty == int(d) and x not in chosen][:int(k)]
        for x in cand:
            if len(chosen) >= n:
                break
            if x not in chosen:
                chosen.append(x)
        chosen = chosen[:n]
        rng.shuffle(chosen)
        used.update(x.id for x in chosen)
        out[sid] = chosen
    return out


def create_assignment(user, f, student_ids, picks):
    """f: dict of assignment fields. picks: {student_id: [RfQuestion]}. One RfAssignmentStudent per student; calling it twice cannot duplicate a student."""
    a = RfAssignment(title=f['title'][:160], exam=f['exam'], subject=f.get('subject') or None, chapter=f.get('chapter') or None, topic=f.get('topic') or None, objective=(f.get('objective') or '')[:300],
                     instructions=f.get('instructions') or '', n_questions=f.get('n') or 8, mix_json=json.dumps(f.get('mix') or {}), selection=f.get('selection', 'filter'),
                     distinct_per_student=bool(f.get('distinct')), start_at=f.get('start_at') or now(), due_at=f.get('due_at'), release=f.get('release', 'after_submit'), release_at=f.get('release_at'),
                     popup=f.get('popup', 'dismissible'), popup_hours=f.get('popup_hours') or 24, allow_remind=bool(f.get('allow_remind', True)), allow_back=bool(f.get('allow_back', True)),
                     remind_hours=f.get('remind_hours') or 6, timed=bool(f.get('timed', True)), source_id=f.get('source_id'), recommendation_id=f.get('recommendation_id'), created_by=user.id)
    db.session.add(a)
    db.session.flush()
    for sid in dict.fromkeys(student_ids):
        qs = picks.get(sid) or []
        if not qs:
            continue
        s = RfAssignmentStudent(assignment_id=a.id, student_id=sid)
        db.session.add(s)
        db.session.flush()
        for pos, qu in enumerate(qs, 1):
            db.session.add(RfItem(asg_student_id=s.id, question_id=qu.id, position=pos))
        st = db.session.get(RfStudent, sid)
        notify(st.user_id, 'assigned', 'New reinforcement: %s' % a.title, '/edupulse-reinforce/', 'asg-%d' % a.id)
    db.session.commit()
    audit(user.id, 'assignment_created', '%s (%d students)' % (a.title, len(a.students.all())))
    return a


def visible_assignments(rs):
    """Active assignments for a student that have started (start_at <= now) and are not completed."""
    t = now()
    rows = (RfAssignmentStudent.query.join(RfAssignment).filter(RfAssignmentStudent.student_id == rs.id, RfAssignment.status == 'active', RfAssignment.start_at <= t).all())
    return rows


def pending_for(rs):
    return [x for x in visible_assignments(rs) if x.status != 'completed']


def is_overdue(a):
    return bool(a.due_at and a.due_at < now())


def popup_candidates(rs):
    """Assignments that should pop up now: pending, not snoozed, within the popup window for time-limited ones."""
    t = now()
    out = []
    for x in pending_for(rs):
        a = x.assignment
        if x.dismissed_until and x.dismissed_until > t:
            continue
        if a.popup == 'time_limited' and a.start_at + timedelta(hours=a.popup_hours or 24) < t:
            continue
        out.append(x)
    return out


def released(asg_student):
    """May this student see answers and explanations for this assignment yet? Enforced on the server before any key leaves it."""
    a = asg_student.assignment
    if a.release == 'immediate':
        return True
    if a.release == 'after_submit':
        return asg_student.status == 'completed'
    if a.release == 'scheduled':
        return bool(a.release_at and a.release_at <= now() and asg_student.status == 'completed')
    if a.release == 'manual':
        return bool(a.release_at and a.release_at <= now())
    return False


def submit(asg_student):
    """Finalise: turn drafts into immutable attempts. Safe to call twice (a completed copy is never re-graded)."""
    if asg_student.status == 'completed':
        return False
    t = now()
    a = asg_student.assignment
    for it in asg_student.items.all():
        q = it.question
        d = RfDraft.query.filter_by(item_id=it.id).first()
        raw = jl(d.answer_json, None) if d and d.answer_json else None
        value, err = parse_answer(q, raw) if raw not in (None, '', []) else (None, 'blank')
        correct, marks = grade(q, value)
        db.session.add(RfAttempt(student_id=asg_student.student_id, assignment_id=a.id, question_id=q.id, qid=q.qid, exam=q.exam, subject=q.subject, chapter=q.chapter, topic=q.topic,
                                 difficulty=q.difficulty, answer_json=json.dumps(value), confidence=(d.confidence if d else None), correct=bool(correct) if value is not None else False,
                                 marks=marks, seconds=(d.seconds if d else 0), answered_at=t))
    asg_student.status = 'completed'
    asg_student.completed_at = t
    db.session.commit()
    rs = asg_student.student
    if rs.mentor_id:
        notify(rs.mentor_id, 'completed', '%s completed "%s"' % (rs.user.name, a.title), '/edupulse-reinforce/mentor/student/%d' % rs.id, 'done-%d-%d' % (a.id, rs.id))
    alert_high_confidence_errors(rs)
    return True


# ---- notices (in-portal first; deduplicated by key) --------------------------------------------------------------------------------------
def notify(user_id, kind, text, url=None, key=None):
    if not user_id:
        return False
    key = key or '%s-%s' % (kind, text[:60])
    if RfNotice.query.filter_by(user_id=user_id, dedupe_key=key).first():
        return False
    db.session.add(RfNotice(user_id=user_id, kind=kind, text=text[:300], url=url, dedupe_key=key))
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    return True


def process_events():
    """Due-soon and overdue notices. Cheap and idempotent: called on dashboard loads and by the cron endpoint."""
    t = now()
    n = 0
    for x in RfAssignmentStudent.query.join(RfAssignment).filter(RfAssignment.status == 'active', RfAssignmentStudent.status != 'completed', RfAssignment.due_at != None).all():  # noqa: E711
        a, rs = x.assignment, x.student
        if a.due_at < t:
            n += notify(rs.user_id, 'overdue', '"%s" is overdue. You can still finish it.' % a.title, '/edupulse-reinforce/do/%d' % x.id, 'overdue-%d' % x.id)
            if rs.mentor_id:
                n += notify(rs.mentor_id, 'overdue', '%s has not completed "%s"' % (rs.user.name, a.title), '/edupulse-reinforce/mentor/student/%d' % rs.id, 'm-overdue-%d' % x.id)
        elif a.due_at - timedelta(hours=a.remind_hours or 6) <= t and a.start_at <= t:
            n += notify(rs.user_id, 'due_soon', '"%s" is due %s' % (a.title, a.due_at.strftime('%d %b, %I:%M %p')), '/edupulse-reinforce/do/%d' % x.id, 'soon-%d' % x.id)
    return n


def alert_high_confidence_errors(rs):
    """Tell the mentor when one chapter has repeated High-confidence errors in the recent window."""
    if not rs.mentor_id:
        return
    since = now() - timedelta(days=int(setting('recent_days')))
    rows = (db.session.query(RfAttempt.chapter, func.count(RfAttempt.id)).filter(RfAttempt.student_id == rs.id, RfAttempt.confidence == 'H', RfAttempt.correct == False,  # noqa: E712
                                                                                    RfAttempt.answered_at >= since).group_by(RfAttempt.chapter).all())
    for ch, c in rows:
        if c >= setting('alert_high_errors'):
            notify(rs.mentor_id, 'alert', '%s: %d high-confidence errors in %s (review for a misconception)' % (rs.user.name, c, ch), '/edupulse-reinforce/mentor/student/%d?chapter=%s' % (rs.id, ch),
                   'hce-%d-%s-%d' % (rs.id, ch, c))


# ---- analytics -----------------------------------------------------------------------------------------------------------------------
def attempts_of(student_id, since=None):
    q = RfAttempt.query.filter_by(student_id=student_id)
    if since:
        q = q.filter(RfAttempt.answered_at >= since)
    return q.order_by(RfAttempt.answered_at).all()


def conf_matrix(rows):
    """Counts by confidence and correctness, plus the rates the spec asks for (each with its own denominator)."""
    m = {c: {'right': 0, 'wrong': 0} for c, _ in CONF}
    for a in rows:
        if a.confidence in m:
            m[a.confidence]['right' if a.correct else 'wrong'] += 1
    h = m['H']['right'] + m['H']['wrong']
    right = sum(v['right'] for v in m.values())
    low_all = sum(m[c]['right'] + m[c]['wrong'] for c in ('L', 'G'))
    pat = {'P1': m['H']['right'], 'P2': m['L']['right'] + m['G']['right'], 'P3': m['L']['wrong'] + m['G']['wrong'], 'P4': m['H']['wrong'], 'M_right': m['M']['right'], 'M_wrong': m['M']['wrong']}
    return {'m': m, 'pattern': pat, 'high_n': h, 'high_error_rate': round(100 * m['H']['wrong'] / h) if h else None,
            'low_correct_share': round(100 * (m['L']['right'] + m['G']['right']) / right) if right else None, 'low_n': low_all}


def _acc(rows):
    return round(100 * sum(1 for a in rows if a.correct) / len(rows)) if rows else None


def chapter_status(rows, s=None):
    """Transparent rules (all thresholds in settings). Returns (status_code, facts)."""
    s = s or settings()
    n = len(rows)
    if not n:
        return 'none', {'n': 0}
    distinct = len({a.qid for a in rows})
    sessions = len({a.assignment_id or a.answered_at.date() for a in rows})
    acc = _acc(rows)
    cm = conf_matrix(rows)
    t = now()
    recent = [a for a in rows if a.answered_at >= t - timedelta(days=int(s['recent_days']))]
    earlier = [a for a in rows if a.answered_at < t - timedelta(days=int(s['recent_days']))]
    first = {}
    delayed = False
    for a in rows:
        if a.qid in first:
            if (a.answered_at - first[a.qid]).days >= s['retention_days'] and a.correct:
                delayed = True
        else:
            first[a.qid] = a.answered_at
    facts = {'n': n, 'distinct': distinct, 'sessions': sessions, 'accuracy': acc, 'high_n': cm['high_n'], 'high_error_rate': cm['high_error_rate'], 'delayed_ok': delayed,
             'recent_n': len(recent), 'recent_acc': _acc(recent), 'earlier_acc': _acc(earlier), 'earlier_n': len(earlier)}
    if distinct < s['min_distinct']:
        return 'insufficient', facts
    if cm['high_n'] >= s['min_high_n'] and cm['high_error_rate'] is not None and cm['high_error_rate'] >= s['high_err_rate']:
        return 'priority', facts
    if acc < s['revise_accuracy']:
        return 'revise', facts
    if len(recent) >= s['min_recent'] and len(earlier) >= s['min_recent'] and facts['recent_acc'] - facts['earlier_acc'] >= s['improving_delta'] and acc < s['strong_accuracy']:
        return 'improving', facts
    if acc >= s['strong_accuracy'] and sessions >= s['min_sessions'] and delayed:
        return 'strong', facts
    return 'developing', facts


def chapter_table(student_id, exam=None):
    s = settings()
    rows = attempts_of(student_id)
    by = defaultdict(list)
    for a in rows:
        by[(a.subject, a.chapter)].append(a)
    out = []
    for (subj, ch), lst in by.items():
        if exam and lst[0].exam != exam:
            continue
        st, facts = chapter_status(lst, s)
        cm = conf_matrix(lst)
        out.append({'subject': subj, 'chapter': ch, 'status': st, 'facts': facts, 'conf': cm, 'last': lst[-1].answered_at, 'attempted': len(lst)})
    out.sort(key=lambda r: ({'priority': 0, 'revise': 1, 'developing': 2, 'insufficient': 3, 'improving': 4, 'strong': 5}.get(r['status'], 6), r['chapter']))
    return out


def streak(student_id):
    days = {d.date() for (d,) in db.session.query(RfAttempt.answered_at).filter(RfAttempt.student_id == student_id)}
    n, d = 0, now().date()
    if d not in days:
        d -= timedelta(days=1)
    while d in days:
        n += 1
        d -= timedelta(days=1)
    return n


def student_summary(rs):
    rows = attempts_of(rs.id)
    t = now()
    week = [a for a in rows if a.answered_at >= t - timedelta(days=7)]
    by_subject = defaultdict(list)
    for a in rows:
        by_subject[a.subject].append(a)
    sessions = defaultdict(list)
    for a in rows:
        sessions[a.assignment_id or 0].append(a)
    trend = [_acc(v) for k, v in sorted(sessions.items(), key=lambda kv: kv[1][0].answered_at)][-10:]
    tab = chapter_table(rs.id)
    return {'n': len(rows), 'accuracy': _acc(rows), 'week_n': len(week), 'week_acc': _acc(week), 'streak': streak(rs.id), 'trend': trend, 'conf': conf_matrix(rows),
            'subjects': {k: {'n': len(v), 'acc': _acc(v)} for k, v in by_subject.items()}, 'chapters': tab, 'last': rows[-1].answered_at if rows else None,
            'revisit': [c for c in tab if c['status'] in ('priority', 'revise')][:6], 'pending': len(pending_for(rs))}


# ---- recommendations (suggestions only: a mentor approves, edits or rejects) --------------------------------------------------------------
def _pick_for_chapter(rs, exam, chapter, n, difficulties=None, misconception_first=False, avoid=()):
    q = approved(exam).filter_by(chapter=chapter)
    pool = [x for x in q.all() if x.id not in set(avoid)]
    if difficulties:
        easier = [x for x in pool if x.difficulty in difficulties]
        pool = easier or pool
    last_wrong = {a.qid for a in attempts_of(rs.id) if a.chapter == chapter and not a.correct}
    pool.sort(key=lambda x: (0 if (misconception_first and x.misconception) else 1, 0 if x.qid not in last_wrong else 1, x.id))
    return pool[:n]


def generate_recommendations(rs):
    """Rule-based and explainable. Returns the new suggestions (existing open ones for the same rule+chapter are not duplicated)."""
    s = settings()
    made = []
    have = {(r.rule, r.chapter) for r in RfRecommendation.query.filter_by(student_id=rs.id, status='suggested').all()}
    tax = {t.chapter: t for t in RfTaxonomy.query.filter_by(exam=rs.exam).all()}
    code_name = {t.code: t.chapter for t in tax.values()}
    for row in chapter_table(rs.id, rs.exam):
        ch, st, f, cm = row['chapter'], row['status'], row['facts'], row['conf']
        ev = dict(f, confidence=cm['m'])
        def add(rule, title, why, qs, days=None):
            if (rule, ch) in have or not qs:
                return
            r = RfRecommendation(student_id=rs.id, rule=rule, chapter=ch, title=title, why=why, evidence_json=json.dumps(ev, default=str), question_ids=json.dumps([x.id for x in qs]),
                                 follow_up_days=days or int(s['followup_days']))
            db.session.add(r)
            made.append(r)
            have.add((rule, ch))
        if cm['pattern']['P4'] >= int(s['alert_high_errors']):
            add('misconception', 'Misconception check: %s' % ch, '%d answers were wrong despite High confidence (%d%% of High answers, n=%d). That can point to an incorrect mental model, so include questions that test the likely misconception and review the answers together.'
                % (cm['pattern']['P4'], cm['high_error_rate'] or 0, cm['high_n']), _pick_for_chapter(rs, rs.exam, ch, 5, misconception_first=True))
        if st == 'revise':
            pre = tax[ch].prereq if ch in tax else None
            qs = _pick_for_chapter(rs, rs.exam, ch, 5, difficulties={1, 2})
            add('targeted_review', 'Targeted review: %s' % ch, 'Accuracy is %d%% over %d distinct questions. Start with a short review%s, then a short follow-up set.' % (f['accuracy'], f['distinct'], ' of the prerequisite chapter %s' % code_name.get(pre, pre) if pre else ''), qs)
        low_share = cm['low_correct_share']
        if low_share is not None and low_share >= 40 and f['n'] >= 6:
            add('confidence_builder', 'Confidence builder: %s' % ch, '%d%% of the correct answers here were rated Guess or Low. Ask related questions in different wording and have the student explain their reasoning; do not label this a weakness.' % low_share,
                _pick_for_chapter(rs, rs.exam, ch, 5, avoid=[a.question_id for a in attempts_of(rs.id) if a.chapter == ch and a.correct]))
        if st in ('improving', 'developing', 'strong') and f['distinct'] >= s['min_distinct'] and not f['delayed_ok']:
            add('retention_check', 'Retention check: %s' % ch, 'No repeat of this chapter after %d or more days yet, so retention is not shown. A few repeat or similar questions would verify it.' % int(s['retention_days']),
                _pick_for_chapter(rs, rs.exam, ch, 5), days=int(s['retention_days']))
    db.session.commit()
    return made


def apply_recommendation(user, rec, student_ids=None):
    """Mentor approval: creates the assignment (never silently). Returns the assignment."""
    qs = [db.session.get(RfQuestion, i) for i in jl(rec.question_ids, [])]
    qs = [q for q in qs if q and q.status == 'approved']
    rs = rec.student
    ids = student_ids or [rs.id]
    picks = {sid: qs for sid in ids}
    a = create_assignment(user, {'title': rec.title, 'exam': rs.exam, 'chapter': rec.chapter, 'subject': qs[0].subject if qs else None, 'selection': 'recommended', 'n': len(qs), 'recommendation_id': rec.id,
                                  'due_at': now() + timedelta(days=2), 'objective': rec.why[:300]}, ids, picks)
    rec.status = 'approved'
    rec.assignment_id = a.id
    db.session.commit()
    return a


# ---- reports -------------------------------------------------------------------------------------------------------------------------
def parent_report(rs, days=7):
    t = now()
    since, prev_since = t - timedelta(days=days), t - timedelta(days=2 * days)
    rows = attempts_of(rs.id)
    cur = [a for a in rows if a.answered_at >= since]
    prev = [a for a in rows if prev_since <= a.answered_at < since]
    tab = chapter_table(rs.id)
    strengths = [c for c in tab if c['status'] in ('strong', 'improving') ][:4]
    gaps = [c for c in tab if c['status'] in ('revise', 'priority')][:4]
    notes = RfObservation.query.filter_by(student_id=rs.id, for_parent=True).order_by(RfObservation.id.desc()).limit(4).all()
    cm = conf_matrix(cur)
    days_active = len({a.answered_at.date() for a in cur})
    lines = []
    for c in strengths:
        lines.append('%s: answers are mostly correct and the evidence is building (%s).' % (c['chapter'], STATUS_LABEL[c['status']].lower()))
    for c in gaps:
        if c['conf']['pattern']['P4']:
            lines.append('%s: some answers are still incorrect despite high confidence. The mentor is reviewing the underlying concept and will reassess next week.' % c['chapter'])
        else:
            lines.append('%s: this chapter needs revision. The mentor will set a short review and a follow-up.' % c['chapter'])
    return {'student': rs, 'days': days, 'questions': len(cur), 'prev_questions': len(prev), 'accuracy': _acc(cur), 'prev_accuracy': _acc(prev), 'days_active': days_active, 'conf': cm,
            'strengths': strengths, 'gaps': gaps, 'lines': lines, 'notes': notes, 'since': since}


# ---- csv import / export ---------------------------------------------------------------------------------------------------------------
CSV_COLS = ['qid', 'exam', 'subject', 'chapter', 'topic', 'concept', 'difficulty', 'qtype', 'stem', 'option_a', 'option_b', 'option_c', 'option_d', 'answer', 'explanation', 'misconception', 'marks', 'neg_marks', 'est_sec', 'source']


def export_csv(questions):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(CSV_COLS)
    for q in questions:
        o = (q.options + ['', '', '', ''])[:4]
        ans = q.answer
        a = ','.join(ans) if q.qtype == 'msq' else (('%g' % ans[0][0]) if q.qtype == 'nat' and ans else ans)
        w.writerow([q.qid, q.exam, q.subject, q.chapter, q.topic, q.concept, q.difficulty, q.qtype, q.stem] + o + [a, q.explanation, q.misconception, q.marks, q.neg_marks, q.est_sec, q.source])
    return out.getvalue()


def import_csv(text, user):
    """Validate every row first; nothing is written unless all rows are valid. Returns (created, errors)."""
    rows = list(csv.DictReader(io.StringIO(text)))
    errs, seen = [], set()
    tax = {(t.exam, t.subject, t.chapter) for t in RfTaxonomy.query.all()}
    parsed = []
    for i, r in enumerate(rows, 2):
        r = {(k or '').strip().lower(): (v or '').strip() for k, v in r.items()}
        e = []
        qid = r.get('qid', '')
        if not qid:
            e.append('missing qid')
        elif qid in seen:
            e.append('duplicate qid in file')
        elif RfQuestion.query.filter_by(qid=qid, active=True).first():
            e.append('qid already exists (edit it in the bank to make a new version)')
        seen.add(qid)
        if (r.get('exam'), r.get('subject'), r.get('chapter')) not in tax:
            e.append('exam/subject/chapter is not in the taxonomy')
        qt = r.get('qtype', 'mcq').lower()
        if qt not in ('mcq', 'msq', 'nat'):
            e.append('qtype must be mcq, msq or nat')
        if not r.get('stem'):
            e.append('missing stem')
        ans = r.get('answer', '')
        opts = [r.get('option_' + c, '') for c in 'abcd']
        if not ans:
            e.append('missing answer')
        elif qt == 'mcq' and ans.upper() not in ('A', 'B', 'C', 'D'):
            e.append('mcq answer must be A-D')
        elif qt == 'msq' and not all(x.strip().upper() in ('A', 'B', 'C', 'D') for x in ans.split(',')):
            e.append('msq answer must be letters such as A,C')
        elif qt == 'nat':
            try:
                float(ans)
            except ValueError:
                e.append('nat answer must be a number')
        if qt in ('mcq', 'msq') and (sum(1 for o in opts if o) < 2 or (ans and qt == 'mcq' and ans.upper() in 'ABCD' and not opts['ABCD'.index(ans.upper())])):
            e.append('options are missing or the answer points at an empty option')
        try:
            d = int(r.get('difficulty') or 2)
            if d not in (1, 2, 3):
                raise ValueError
        except ValueError:
            e.append('difficulty must be 1, 2 or 3')
            d = 2
        if e:
            errs.append('Row %d (%s): %s' % (i, qid or '-', '; '.join(e)))
        else:
            parsed.append((qid, r, qt, opts, ans, d))
    if errs:
        return 0, errs
    for qid, r, qt, opts, ans, d in parsed:
        key = [[float(ans), float(ans)]] if qt == 'nat' else sorted(x.strip().upper() for x in ans.split(',')) if qt == 'msq' else ans.upper()
        db.session.add(RfQuestion(qid=qid, exam=r['exam'], subject=r['subject'], chapter=r['chapter'], topic=r.get('topic') or r['chapter'], concept=r.get('concept'), difficulty=d, qtype=qt,
                                  stem=sanitize(r['stem']), options_json=json.dumps([sanitize(o) for o in opts]) if qt != 'nat' else '[]', answer_json=json.dumps(key), explanation=sanitize(r.get('explanation')),
                                  misconception=sanitize(r.get('misconception')), marks=float(r.get('marks') or 4), neg_marks=float(r.get('neg_marks') or 0), est_sec=int(r.get('est_sec') or 90),
                                  source=r.get('source') or 'import', author_id=user.id, status='draft'))
    db.session.commit()
    audit(user.id, 'questions_imported', '%d rows' % len(parsed))
    return len(parsed), []
