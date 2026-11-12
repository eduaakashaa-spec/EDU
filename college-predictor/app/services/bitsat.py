"""EduPulse-BITSAT: timed mock tests and practice sets from the BITSAT previous-year papers, for members.

* The question bank is app/data/bitsat/papers.json (what each year's paper holds: sections, reading passages, the questions to leave out) plus keys.json (the answer key
  of each year) and one picture per question under static/img/bitsat/<year>/ (qNNN.webp = the question and its four options as printed; pNNN_MMM.webp = a reading passage
  shared by questions NNN to MMM). The papers are the memory-based papers circulated after each sitting (BITS Pilani does not publish its question papers) and the
  keys are the ones published with them: they are practice material, not an official paper. Questions without a trustworthy picture or key are never used in a test.
* Tests: each year's paper as it was sat (150 questions up to 2021, 130 from 2022), full 130-question mocks in the current pattern drawn across the years, and subject sets.
* Grading happens on the server: the answer key never goes to the browser before submission.

Marking, as in the real BITSAT: +3 for a correct answer, -1 for a wrong answer, 0 for a blank. Guessing pays off only if you are right more than 1 time in 4.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
from datetime import datetime

from app.extensions import db
from app.models_pulse import PulseBitsatResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'bitsat')
SUBJECTS = [('PHY', 'Physics'), ('CHE', 'Chemistry'), ('ENG', 'English Proficiency'), ('LR', 'Logical Reasoning'), ('MAT', 'Mathematics')]
SUBJ_NAME = dict(SUBJECTS)
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
RIGHT, WRONG = 3, 1
BREAK_EVEN = 25
MAX_BODY = 200_000
MIN_RATED = 10
FULL_MINUTES = 180
PATTERN = {'PHY': 30, 'CHE': 30, 'ENG': 10, 'LR': 20, 'MAT': 40}          # the 130-question paper of 2022 onwards (390 marks)
SET_SIZE = {'PHY': 30, 'CHE': 30, 'ENG': 15, 'LR': 15, 'MAT': 30}

_cache = {}


def _load():
    if 'qs' in _cache:
        return
    qs, papers = [], {}
    try:
        with open(os.path.join(DATA_DIR, 'papers.json'), encoding='utf-8') as fh:
            meta = json.load(fh)
        with open(os.path.join(DATA_DIR, 'keys.json'), encoding='utf-8') as fh:
            keys = json.load(fh)
    except OSError:
        meta, keys = {}, {}
    for ys, m in meta.items():
        y = int(ys)
        key = keys.get(ys, {})
        skip = set(m.get('skip', []))
        passages = {}
        for lo, hi in m.get('passages', []):
            for n in range(lo, hi + 1):
                passages[n] = 'p%03d_%03d.webp' % (lo, hi)
        sec = {}
        for code, lo, hi in m['sections']:
            for n in range(lo, hi + 1):
                sec[n] = code
        papers[y] = {'year': y, 'total': m['n'], 'usable': 0, 'note': m.get('note', '')}
        for n in range(1, m['n'] + 1):
            a = key.get(str(n))
            q = {'qid': 'B%02d-%03d' % (y % 100, n), 'year': y, 'n': n, 'sj': sec.get(n), 'img': 'q%03d.webp' % n, 'passage': passages.get(n),
                 'ans': LETTERS.index(a) if a in tuple(LETTERS) else None}
            q['subject'] = SUBJ_NAME.get(q['sj'], '')
            q['usable'] = n not in skip and q['ans'] is not None and q['sj'] is not None
            papers[y]['usable'] += 1 if q['usable'] else 0
            qs.append(q)
    _cache['qs'] = qs
    _cache['by_id'] = {q['qid']: q for q in qs}
    _cache['papers'] = papers


def bank():
    _load()
    return _cache['qs']


def by_id():
    _load()
    return _cache['by_id']


def usable():
    return [q for q in bank() if q['usable']]


def papers():
    """Years held, newest first, with how many of their questions are usable in tests."""
    _load()
    return [_cache['papers'][y] for y in sorted(_cache['papers'], reverse=True)]


def tests():
    """All tests: each year's paper, full 130-question mocks and subject sets. [{id, title, kind, qids, minutes, note}]"""
    if 'tests' in _cache:
        return _cache['tests']
    pool = {sj: sorted([q for q in usable() if q['sj'] == sj], key=lambda q: (q['year'], q['n'])) for sj, _n in SUBJECTS}
    out = []
    ks = [len(pool[sj]) // c for sj, c in PATTERN.items()]
    k = min(ks) if ks else 0
    for m in range(k):                                    # full mocks: the 130-question pattern, never the same question twice, spread over the years
        ids = []
        for sj, _n in SUBJECTS:
            ids += [q['qid'] for q in pool[sj][m::k][:PATTERN[sj]]]
        out.append({'id': 'F%d' % (m + 1), 'title': 'BITSAT Full Mock %d' % (m + 1), 'kind': 'full', 'qids': ids, 'minutes': FULL_MINUTES,
                    'note': '%d questions · 5 sections · +3 and −1 · mixed years' % len(ids)})
    for p in papers():
        ids = [q['qid'] for q in usable() if q['year'] == p['year']]
        if len(ids) < 30:
            continue
        out.append({'id': 'Y%d' % p['year'], 'title': 'BITSAT %d paper' % p['year'], 'kind': 'year', 'qids': ids, 'minutes': FULL_MINUTES,
                    'note': '%d of the %d questions of the %d paper' % (p['usable'], p['total'], p['year'])})
    for sj, name in SUBJECTS:
        rows, size = pool[sj], SET_SIZE[sj]
        for i in range(0, len(rows) - size + 1, size):
            ids = [q['qid'] for q in rows[i:i + size]]
            mins = max(10, round(len(ids) * FULL_MINUTES / 130))
            out.append({'id': 'S-%s%d' % (sj, i // size + 1), 'title': '%s set %d' % (name, i // size + 1), 'kind': 'section', 'subject': name, 'qids': ids, 'minutes': mins,
                        'note': '%d questions · %d min' % (len(ids), mins)})
    _cache['tests'] = out
    _cache['test_by_id'] = {t['id']: t for t in out}
    return out


def test(tid):
    tests()
    return _cache['test_by_id'].get(tid)


def asset(q, fname=None):
    return '/static/img/bitsat/%d/%s' % (q['year'], fname or q['img'])


def paper_for_browser(t):
    """The questions of a test as the browser sees them: picture addresses only, no answers."""
    ids = by_id()
    out = []
    for qid in t['qids']:
        q = ids[qid]
        out.append({'id': qid, 'subject': q['subject'], 'sj': q['sj'], 'n': q['n'], 'year': q['year'], 'stem': asset(q),
                    'passage': asset(q, q['passage']) if q['passage'] else None})
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
        rows.append({'qid': qid, 'sj': q['sj'], 'chosen': ch, 'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None,
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
    r = PulseBitsatResult(user_id=user_id, mock=t['id'], title=t['title'], score=score, max_score=RIGHT * len(rows), right=right, wrong=wrong, blank=len(rows) - len(att),
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
    """Subject picture, the effect of negative marking, and confidence patterns over one or more attempts."""
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    subj = {sj: {'n': 0, 'right': 0, 'wrong': 0, 'blank': 0} for sj, _n in SUBJECTS}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = subj.get(x['sj'])
            if s is None:
                continue
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            if x['right']:
                s['right'] += 1
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
    srows = []
    for sj, name in SUBJECTS:
        s = subj[sj]
        acc = round(100 * s['right'] / s['n']) if s['n'] else None
        srows.append({'sj': sj, 'subject': name, **s, 'acc': acc, 'marks': RIGHT * s['right'] - WRONG * s['wrong'], 'band': band(acc or 0, s['n'])})
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
        elif wrong and right and WRONG * wrong >= 0.25 * RIGHT * right:
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
    weak = [r['subject'] for r in sorted((r for r in srows if r['n'] >= 3), key=lambda r: r['acc'] if r['acc'] is not None else 101) if r['band'] == 'Needs reinforcement'][:3]
    return {'right': right, 'wrong': wrong, 'blank': blank, 'attempted': att, 'acc': acc, 'rated': rated, 'pat': pat, 'conf': conf, 'subjects': srows, 'notes': notes,
            'weak': weak, 'enough': rated >= MIN_RATED, 'marks': RIGHT * right - WRONG * wrong}


def for_user(user_id, limit=None):
    q = PulseBitsatResult.query.filter_by(user_id=user_id).order_by(PulseBitsatResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    an = analyse(rows)
    pcts = [round(100 * r.score / r.max_score) for r in rows if r.max_score]
    return {'attempts': len(rows), 'rows': rows[:10], 'avg_pct': round(sum(pcts) / len(pcts)) if pcts else None, 'best': max(pcts) if pcts else None, 'an': an}


def review(result):
    """Per-question rows of one attempt joined to the bank (picture, key) for the report page."""
    ids = by_id()
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = ids.get(x['qid'])
        if q and q['usable']:
            out.append({**x, 'subject': q['subject'], 'year': q['year'], 'n': q['n'], 'stem': asset(q), 'passage': asset(q, q['passage']) if q['passage'] else None, 'ans': q['ans']})
    return out
