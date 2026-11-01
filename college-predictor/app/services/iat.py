"""EduPulse-IAT: timed mock tests and practice sets for the IISER Aptitude Test, built from the released IAT papers 2021 to 2026.

* The question bank (app/data/iat/q<year>.json) holds each question as images cut from the official PDF (stem and four options) with a worked solution.
  The released papers are answer-key editions in which option (a) is always the correct answer, so the options are shuffled here, with a seed from the
  question id, before they reach the browser. Questions whose layout cannot be split safely (for example options that are bare pictures) are kept for
  review but never used in a test.
* The tests: full 60-question mocks (15 per subject, 180 minutes), year practice sets, and subject sectionals.
* Grading happens on the server: the answer key never goes to the browser before submission.

Marking, as in the real IAT: +4 for a correct answer, -1 for a wrong answer, 0 for a blank. Guessing pays off only if you are right more than 1 time in 5.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import datetime

from app.extensions import db
from app.models_pulse import PulseIatResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'iat')
SUBJECTS = [('BIO', 'Biology'), ('CHE', 'Chemistry'), ('MAT', 'Mathematics'), ('PHY', 'Physics')]
SUBJ_NAME = dict(SUBJECTS)
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
RIGHT, WRONG = 4, 1
BREAK_EVEN = 20
MAX_BODY = 200_000
MIN_RATED = 10
MIN_PER_Q = 3                  # 180 minutes for 60 questions
FULL_MOCKS = 4
SECT_SIZE = 15

_cache = {}


def _load():
    if 'qs' in _cache:
        return
    qs = []
    try:
        names = sorted(f for f in os.listdir(DATA_DIR) if f.startswith('q') and f.endswith('.json'))
    except OSError:
        names = []
    for f in names:
        with open(os.path.join(DATA_DIR, f), encoding='utf-8') as fh:
            qs.extend(json.load(fh))
    for q in qs:
        q['qid'] = 'IAT%s-%s%02d' % (str(q['year'])[2:], q['sj'], q['n'])
        q['subject'] = SUBJ_NAME[q['sj']]
        q['usable'] = bool(q.get('ok')) and q.get('agree', True) and len(q.get('opts') or []) == 4
        if q['usable']:
            order = [0, 1, 2, 3]
            random.Random(q['qid']).shuffle(order)
            q['order'] = order                              # order[k] = index in the printed options shown at position k
            q['ans'] = order.index(0)                       # the printed first option is the correct one
    _cache['qs'] = qs
    _cache['by_id'] = {q['qid']: q for q in qs}


def bank():
    _load()
    return _cache['qs']


def by_id():
    _load()
    return _cache['by_id']


def usable():
    return [q for q in bank() if q['usable']]


def papers():
    """Years held, with how many of their questions are usable in tests."""
    out = {}
    for q in bank():
        r = out.setdefault(q['year'], {'year': q['year'], 'total': 0, 'usable': 0})
        r['total'] += 1
        r['usable'] += 1 if q['usable'] else 0
    return [out[y] for y in sorted(out, reverse=True)]


def tests():
    """All tests: full mocks, year practice sets and subject sectionals. [{id, title, kind, qids, minutes, note}]"""
    if 'tests' in _cache:
        return _cache['tests']
    pool = {sj: sorted([q for q in usable() if q['sj'] == sj], key=lambda q: (q['year'], q['n'])) for sj, _n in SUBJECTS}
    out = []
    # full mocks: 15 per subject, never the same question twice, spread over the years by taking every k-th question
    k = min(FULL_MOCKS, min(len(v) for v in pool.values()) // 15)
    for m in range(k):
        ids = []
        for sj, _n in SUBJECTS:
            rows = pool[sj]
            pick = [r for i, r in enumerate(rows) if i % k == m][:15]
            if len(pick) < 15:
                pick += [r for r in rows if r not in pick and r not in [x for mm in range(m) for x in rows[mm::k]]][:15 - len(pick)]
            ids += [q['qid'] for q in pick]
        out.append({'id': 'F%d' % (m + 1), 'title': 'IAT Full Mock %d' % (m + 1), 'kind': 'full', 'qids': ids, 'minutes': len(ids) * MIN_PER_Q,
                    'note': '%d questions · 4 subjects · +4 and −1' % len(ids)})
    for p in papers():
        ids = [q['qid'] for q in usable() if q['year'] == p['year']]
        out.append({'id': 'Y%d' % p['year'], 'title': 'IAT %d practice set' % p['year'], 'kind': 'year', 'qids': ids, 'minutes': len(ids) * MIN_PER_Q,
                    'note': '%d of the %d questions of the %d paper' % (p['usable'], p['total'], p['year'])})
    for sj, name in SUBJECTS:
        rows = pool[sj]
        for i in range(0, len(rows) - SECT_SIZE + 1, SECT_SIZE):
            ids = [q['qid'] for q in rows[i:i + SECT_SIZE]]
            out.append({'id': 'S-%s%d' % (sj, i // SECT_SIZE + 1), 'title': '%s section %d' % (name, i // SECT_SIZE + 1), 'kind': 'section', 'subject': name,
                        'qids': ids, 'minutes': len(ids) * MIN_PER_Q, 'note': '%d questions · %d min' % (len(ids), len(ids) * MIN_PER_Q)})
    _cache['tests'] = out
    _cache['test_by_id'] = {t['id']: t for t in out}
    return out


def test(tid):
    tests()
    return _cache['test_by_id'].get(tid)


def asset(q, fname):
    return '/static/img/iat/%d/%s' % (q['year'], fname)


def paper_for_browser(t):
    """The questions of a test as the browser sees them: image addresses only, options in shuffled order, no answers or solutions."""
    ids = by_id()
    out = []
    for qid in t['qids']:
        q = ids[qid]
        out.append({'id': qid, 'subject': q['subject'], 'sj': q['sj'], 'stem': asset(q, q['stem'][0]), 'options': [asset(q, q['opts'][i]) for i in q['order']]})
    return out


# ---- grading -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade(t, d):
    """Mark a submission {answers: {qid: {a: 0-3 or null, c: G/L/M/H or null, sec: n}}, timed: bool, seconds}. Returns (rows, error)."""
    if not isinstance(d, dict) or not isinstance(d.get('answers'), dict):
        return None, 'bad payload'
    ids = by_id()
    rows = []
    for qid in t['qids']:
        a = d['answers'].get(qid) or {}
        ch = a.get('a')
        ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        q = ids[qid]
        rows.append({'qid': qid, 'sj': q['sj'], 'topic': q.get('topic', ''), 'chosen': ch, 'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None,
                     'sec': _num(a.get('sec'), 0, 3600)})
    return rows, None


def marks(rows):
    right = sum(1 for r in rows if r['right'])
    wrong = sum(1 for r in rows if r['chosen'] is not None and not r['right'])
    return RIGHT * right - WRONG * wrong, right, wrong


def save_result(user_id, t, d):
    rows, err = grade(t, d)
    if err:
        return None, err
    score, right, wrong = marks(rows)
    att = [r for r in rows if r['chosen'] is not None]
    r = PulseIatResult(user_id=user_id, mock=t['id'], title=t['title'], score=score, max_score=RIGHT * len(rows), right=right, wrong=wrong, blank=len(rows) - len(att),
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
    return 'Secure' if pct >= 75 else 'Developing' if pct >= 45 else 'Needs reinforcement'


def analyse(results):
    """Subject and topic picture, the effect of negative marking, and confidence patterns over one or more attempts."""
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    subj = {sj: {'n': 0, 'right': 0, 'wrong': 0, 'blank': 0} for sj, _n in SUBJECTS}
    topics = {}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = subj[x['sj']]
            tp = topics.setdefault((x['sj'], x.get('topic') or 'Other'), {'n': 0, 'right': 0, 'sure_wrong': 0})
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            tp['n'] += 1
            if x['right']:
                s['right'] += 1
                tp['right'] += 1
            else:
                s['wrong'] += 1
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
                        tp['sure_wrong'] += 1
    srows = []
    for sj, name in SUBJECTS:
        s = subj[sj]
        acc = round(100 * s['right'] / s['n']) if s['n'] else None
        srows.append({'sj': sj, 'subject': name, **s, 'acc': acc, 'marks': RIGHT * s['right'] - WRONG * s['wrong'], 'band': band(acc or 0, s['n'])})
    trows = []
    for (sj, name), t in topics.items():
        pct = round(100 * t['right'] / t['n']) if t['n'] else None
        trows.append({'sj': sj, 'subject': SUBJ_NAME[sj], 'topic': name, 'n': t['n'], 'right': t['right'], 'pct': pct, 'sure_wrong': t['sure_wrong'], 'band': band(pct or 0, t['n'])})
    trows.sort(key=lambda r: (r['pct'] if r['pct'] is not None else 101, -r['n']))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    right = sum(s['right'] for s in subj.values())
    wrong = sum(s['wrong'] for s in subj.values())
    blank = sum(s['blank'] for s in subj.values())
    att = right + wrong
    acc = round(100 * right / att) if att else None
    notes = []
    if att:
        if acc is not None and acc < BREAK_EVEN:
            notes.append('Your accuracy on attempted questions is %d%%, below the %d%% break-even: on average each attempt costs marks. Attempt fewer questions, and only those where you can remove at least one option.' % (acc, BREAK_EVEN))
        elif wrong and RIGHT * right > 0 and WRONG * wrong >= 0.25 * RIGHT * right:
            notes.append('Wrong answers cost you %d marks, about %d%% of what your right answers earned. Skip the questions you would rate Guess.' % (WRONG * wrong, round(100 * WRONG * wrong / (RIGHT * right))))
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer in the next test.')
    else:
        if pat['P4']:
            notes.append('%d answers were wrong although you rated them High: check these first, they point to a wrong method or a misunderstood idea.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answers were right but rated Guess or Low: the idea is not secure yet.' % pat['P2'])
        if pat['P3']:
            notes.append('%d answers were wrong and rated Guess or Low: you knew where the gaps were. Learn the textbook section, then try again.' % pat['P3'])
    weak = [r['topic'] for r in trows if r['band'] == 'Needs reinforcement'][:4]
    return {'right': right, 'wrong': wrong, 'blank': blank, 'attempted': att, 'acc': acc, 'rated': rated, 'pat': pat, 'conf': conf, 'subjects': srows, 'topics': trows, 'notes': notes,
            'weak': weak, 'enough': rated >= MIN_RATED, 'marks': RIGHT * right - WRONG * wrong}


def for_user(user_id, limit=None):
    q = PulseIatResult.query.filter_by(user_id=user_id).order_by(PulseIatResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    an = analyse(rows)
    pcts = [round(100 * r.score / r.max_score) for r in rows if r.max_score]
    return {'attempts': len(rows), 'rows': rows[:10], 'avg_pct': round(sum(pcts) / len(pcts)) if pcts else None, 'best': max(pcts) if pcts else None, 'an': an}


def review(result):
    """Per-question rows of one attempt joined to the bank (images, key, solution) for the report page, options in the order the student saw them."""
    ids = by_id()
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = ids.get(x['qid'])
        if q and q['usable']:
            out.append({**x, 'subject': q['subject'], 'year': q['year'], 'n': q['n'], 'stem': asset(q, q['stem'][0]), 'options': [asset(q, q['opts'][i]) for i in q['order']],
                        'ans': q['ans'], 'why': q.get('why', ''), 'topic': q.get('topic', '')})
    return out
