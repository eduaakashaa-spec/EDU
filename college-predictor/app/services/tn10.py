"""EduPulse for Tamil Nadu Class 10 (SSLC / Matriculation) Mathematics and Science, in English.

* the question bank (app/data/tn10/maths.py and science.py) built into plain dicts with the options shuffled by question id;
* the mock tests (full-syllabus mocks and unit tests) drawn from that bank;
* grading of a finished attempt on the server (the answer key never goes to the browser before submission), the confidence analysis and the unit-wise picture;
* the same questions seeded into EduPulse Reinforcement as the exam track 'TN10'.

Marking: 1 mark per question, no negative marking (the board's own objective questions carry none). Confidence codes: G guess, L low, M medium, H high.
Patterns, as in the other EduPulse tools: sure and right, right but unsure (possible lucky guess), wrong and unsure (aware gap), wrong and sure (a misconception to fix first).
"""
import html
import json
import random
from datetime import datetime

from app.data.tn10 import maths, science
from app.extensions import db
from app.models_pulse import PulseTn10Result

EXAM = 'TN10'
SUBJECTS = {'M': 'Mathematics', 'S': 'Science'}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
MAX_BODY = 60_000
MIN_RATED = 10
FULL = {'M': dict(n=3, minutes=60), 'S': dict(n=3, minutes=75)}       # three full-syllabus mocks per subject
UNIT_MINUTES_PER_Q = 1.5

_cache = {}


def _plain(s):
    return html.unescape(s)


def units():
    """{unit code: (subject name, unit title)} for both subjects, in textbook order."""
    out = {}
    for code, title in maths.UNITS:
        out[code] = ('Mathematics', title)
    for code, title in science.UNITS:
        out[code] = ('Science', title)
    return out


def bank():
    """All questions as dicts: qid, unit, subject, chapter, stem, options (4), ans (0-3), why, diff. Options are shuffled with a seed from the qid, so the order is stable."""
    if 'bank' in _cache:
        return _cache['bank']
    names = units()
    out, seen = [], {}
    for rows in (maths.Q, science.Q):
        for unit, stem, right, wrong, why, diff in rows:
            seen[unit] = seen.get(unit, 0) + 1
            qid = 'TN10-%s-%03d' % (unit, seen[unit])
            opts = [right] + list(wrong)
            random.Random(qid).shuffle(opts)
            out.append({'qid': qid, 'unit': unit, 'n': seen[unit], 'subject': names[unit][0], 'chapter': names[unit][1], 'stem': _plain(stem),
                        'options': [_plain(o) for o in opts], 'ans': opts.index(right), 'why': _plain(why), 'diff': diff})
    _cache['bank'] = out
    _cache['by_id'] = {q['qid']: q for q in out}
    return out


def by_id():
    bank()
    return _cache['by_id']


def mocks():
    """The mock tests: [{id, title, subject, kind ('full' | 'unit'), qids, minutes}], full mocks first. Full mock k takes every third question of every unit, offset k."""
    if 'mocks' in _cache:
        return _cache['mocks']
    qs = bank()
    out = []
    for s, spec in FULL.items():
        subj = SUBJECTS[s]
        for k in range(spec['n']):
            ids = [q['qid'] for q in qs if q['unit'].startswith(s) and (q['n'] - 1) % spec['n'] == k]
            out.append({'id': '%s-F%d' % (s, k + 1), 'title': '%s Full Mock %d' % (subj, k + 1), 'subject': subj, 'kind': 'full', 'qids': ids, 'minutes': spec['minutes']})
    for code, (subj, title) in units().items():
        ids = [q['qid'] for q in qs if q['unit'] == code]
        out.append({'id': '%s-U%s' % (code[0], code[1:]), 'title': 'Unit %s: %s' % (code[1:], title), 'subject': subj, 'kind': 'unit', 'qids': ids,
                    'minutes': int(round(len(ids) * UNIT_MINUTES_PER_Q))})
    _cache['mocks'] = out
    _cache['mock_by_id'] = {m['id']: m for m in out}
    return out


def mock(mid):
    mocks()
    return _cache['mock_by_id'].get(mid)


def paper_for_browser(m):
    """The questions of a mock without the answers or explanations."""
    ids = by_id()
    return [{'id': q, 'unit': ids[q]['unit'], 'chapter': ids[q]['chapter'], 'stem': ids[q]['stem'], 'options': ids[q]['options']} for q in m['qids']]


# ---- grading -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade(m, d):
    """Mark a submission {answers: {qid: {a: 0-3 or null, c: G/L/M/H or null, sec: n}}, timed: bool, startedAt, finishedAt}. Returns (rows, error); rows follow the paper's order."""
    if not isinstance(d, dict) or not isinstance(d.get('answers'), dict):
        return None, 'bad payload'
    ids = by_id()
    rows = []
    for qid in m['qids']:
        a = d['answers'].get(qid) or {}
        ch = a.get('a')
        ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        q = ids[qid]
        rows.append({'qid': qid, 'unit': q['unit'], 'chosen': ch, 'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None, 'sec': _num(a.get('sec'), 0, 3600)})
    return rows, None


def save_result(user_id, m, d):
    rows, err = grade(m, d)
    if err:
        return None, err
    att = [r for r in rows if r['chosen'] is not None]
    r = PulseTn10Result(user_id=user_id, mock=m['id'], title=m['title'], subject=m['subject'], score=sum(1 for x in rows if x['right']), total=len(rows), attempted=len(att),
                        rated=sum(1 for x in att if x['conf']), sure_wrong=sum(1 for x in att if not x['right'] and x['conf'] == 'H'),
                        lucky=sum(1 for x in att if x['right'] and x['conf'] in ('G', 'L')), duration_sec=_num(d.get('seconds'), 0, 20000), timed=bool(d.get('timed')),
                        finished_at=datetime.utcnow(), payload_json=json.dumps(rows, separators=(',', ':')))
    db.session.add(r)
    db.session.commit()
    return r, None


# ---- analysis ----------------------------------------------------------------------------------------------------------------------------
def band(pct, n):
    if n < 3:
        return 'Too few questions'
    return 'Secure' if pct >= 80 else 'Developing' if pct >= 50 else 'Needs reinforcement'


def analyse(results):
    """Confidence patterns and the unit-wise picture over one or more attempts."""
    names = units()
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    unit = {}
    right = wrong = blank = 0
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            u = unit.setdefault(x['unit'], {'n': 0, 'right': 0, 'sure_wrong': 0})
            if x['chosen'] is None:
                blank += 1
                continue
            u['n'] += 1
            u['right'] += 1 if x['right'] else 0
            if x['right']:
                right += 1
            else:
                wrong += 1
            c = x.get('conf')
            if c:
                rated += 1
                conf[c]['n'] += 1
                conf[c]['right'] += 1 if x['right'] else 0
                if x['right']:
                    pat['P1' if c in ('H', 'M') else 'P2'] += 1
                else:
                    pat['P4' if c == 'H' else 'P3'] += 1
                    if c == 'H':
                        u['sure_wrong'] += 1
    rows = []
    for code, u in unit.items():
        pct = round(100 * u['right'] / u['n']) if u['n'] else None
        rows.append({'unit': code, 'subject': names[code][0], 'title': names[code][1], 'n': u['n'], 'right': u['right'], 'pct': pct, 'sure_wrong': u['sure_wrong'], 'band': band(pct or 0, u['n'])})
    rows.sort(key=lambda r: (r['pct'] if r['pct'] is not None else 101, -r['n']))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    notes = []
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer in the next test.')
    else:
        if pat['P4']:
            notes.append('%d answers were wrong although you rated them High: check these first, they point to a wrong method or a misunderstood idea.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answers were right but rated Guess or Low: the idea is not secure yet, so revise it before it costs marks.' % pat['P2'])
        if pat['P3']:
            notes.append('%d answers were wrong and rated Guess or Low: you know where the gaps are. Learn the textbook section, then try again.' % pat['P3'])
    weak = [r['title'] for r in rows if r['band'] == 'Needs reinforcement'][:3]
    return {'right': right, 'wrong': wrong, 'blank': blank, 'rated': rated, 'pat': pat, 'conf': conf, 'units': rows, 'notes': notes, 'weak': weak, 'enough': rated >= MIN_RATED}


def for_user(user_id, limit=None):
    q = PulseTn10Result.query.filter_by(user_id=user_id).order_by(PulseTn10Result.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    an = analyse(rows)
    pcts = [round(100 * r.score / r.total) for r in rows if r.total]
    return {'attempts': len(rows), 'rows': rows[:10], 'avg_pct': round(sum(pcts) / len(pcts)) if pcts else None, 'best': max(pcts) if pcts else None, 'an': an}


def review(result):
    """Per-question rows of one attempt joined to the bank (stem, options, key, explanation) for the report page."""
    ids = by_id()
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = ids.get(x['qid'])
        if q:
            out.append({**x, 'stem': q['stem'], 'options': q['options'], 'ans': q['ans'], 'why': q['why'], 'chapter': q['chapter']})
    return out


# ---- EduPulse Reinforcement: the same questions as exam track TN10 -----------------------------------------------------------------------------------------------
def taxonomy():
    """{subject: [(code, chapter, prereq)]} for the Reinforcement taxonomy."""
    out = {'Mathematics': [], 'Science': []}
    for code, title in maths.UNITS:
        out['Mathematics'].append((code, title, None))
    for code, title in science.UNITS:
        out['Science'].append((code, title, None))
    return out


def seed_reinforcement():
    """Idempotent: add the bank to EduPulse Reinforcement as approved questions of the TN10 track. Returns how many were added."""
    from app.models_reinforce import RfQuestion, RfTaxonomy
    n = 0
    for subj, rows in taxonomy().items():
        for pos, (code, name, pre) in enumerate(rows):
            if not RfTaxonomy.query.filter_by(exam=EXAM, subject=subj, chapter=name).first():
                db.session.add(RfTaxonomy(exam=EXAM, subject=subj, chapter=name, code=code, prereq=pre, position=pos))
    db.session.flush()
    for q in bank():
        if RfQuestion.query.filter_by(qid=q['qid']).first():
            continue
        db.session.add(RfQuestion(qid=q['qid'], exam=EXAM, subject=q['subject'], chapter=q['chapter'], topic=q['chapter'], concept=q['chapter'], difficulty=q['diff'], qtype='mcq',
                                  stem=html.escape(q['stem'], quote=False), options_json=json.dumps([html.escape(o, quote=False) for o in q['options']]),
                                  answer_json=json.dumps(LETTERS[q['ans']]), explanation='<p>%s</p>' % html.escape(q['why'], quote=False), misconception='', marks=1, neg_marks=0,
                                  est_sec=75, source='EduAakashaa original (TN Class 10 %s, unit %s)' % (q['subject'], q['unit'][1:]), status='approved'))
        n += 1
    db.session.commit()
    return n
