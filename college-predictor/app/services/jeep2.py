"""EduPulse-JEE Paper 2: timed mocks and practice sets for JEE (Main) Paper 2A (B.Arch) and Paper 2B (B.Planning), from the NTA question papers with the official final answer keys.

* app/data/jee_p2/papers.json describes each paper (sections, the questions left out); keys.json holds the NTA key (MCQ: index 0-3 of the option as lettered A-D in the picture;
  numerical: the value; 'bonus': the question NTA dropped, full marks to everyone). One picture per question under static/img/jee_p2/<paper id>/qNNN.webp.
* Paper 2A = Mathematics (20 MCQ + numerical), Aptitude (50). Its Drawing test (2 questions) is marked by hand and is not in the mocks. Paper 2B = Mathematics, Aptitude (50), Planning (25).
* Tests: each paper as it was sat, each section of a paper, and mixed Aptitude mocks of 50 questions drawn across the papers. Where a numerical section says 'attempt any 5 of 10', only the
  first 5 answered (by question number) are marked, as in the real paper.
* Grading happens on the server: the key never goes to the browser before submission.

Marking, as in the real paper: +4 for a correct answer, -1 for a wrong answer, 0 for a blank (numerical questions too). Guessing pays only if you are right more than 1 time in 5.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
from datetime import datetime

from app.extensions import db
from app.models_pulse import PulseJeeP2Result

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'jee_p2')
SUBJECTS = [('MATH', 'Mathematics'), ('APT', 'Aptitude'), ('PLAN', 'Planning')]
SUBJ_NAME = dict(SUBJECTS)
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
RIGHT, WRONG = 4, 1
BREAK_EVEN = 20
MAX_BODY = 200_000
MIN_RATED = 10
MIX_SIZE = 50

_cache = {}


def _load():
    if 'qs' in _cache:
        return
    try:
        with open(os.path.join(DATA_DIR, 'papers.json'), encoding='utf-8') as fh:
            meta = json.load(fh)
        with open(os.path.join(DATA_DIR, 'keys.json'), encoding='utf-8') as fh:
            keys = json.load(fh)
    except OSError:
        meta, keys = {}, {}
    qs, papers = [], {}
    for pid, m in meta.items():
        skip = set(m.get('skip', []))
        key = keys.get(pid, {})
        sec_of, choose = {}, {}
        for s in m['sections']:
            for n in range(s['lo'], s['hi'] + 1):
                sec_of[n] = (s['sec'], s['t'])
            if s.get('choose'):
                choose[(s['sec'], s['t'])] = s['choose']
        papers[pid] = {**m, 'id': pid, 'usable': 0, 'choose': choose}
        for n in range(1, m['n'] + 1):
            if n not in sec_of:
                continue
            sec, typ = sec_of[n]
            k = key.get(str(n))
            q = {'qid': '%s-%03d' % (pid, n), 'paper_id': pid, 'paper': m['paper'], 'year': m['year'], 'n': n, 'sj': sec, 'subject': SUBJ_NAME[sec], 't': typ, 'key': k}
            q['usable'] = n not in skip and k is not None
            papers[pid]['usable'] += 1 if q['usable'] else 0
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
    """Papers held, newest first: id, title, paper (2A/2B), usable question count."""
    _load()
    return sorted(_cache['papers'].values(), key=lambda p: (-p['year'], p['id']), reverse=False)


def tests():
    """All tests: [{id, title, kind: paper|section|mix, qids, minutes, note, paper?}]"""
    if 'tests' in _cache:
        return _cache['tests']
    _load()
    out = []
    for p in papers():
        ids = [q['qid'] for q in usable() if q['paper_id'] == p['id']]
        out.append({'id': 'P-' + p['id'], 'title': p['title'], 'kind': 'paper', 'paper': p['paper'], 'qids': ids, 'minutes': p['minutes'],
                    'note': '%d questions · Mathematics, Aptitude%s · +4 and −1' % (len(ids), ', Planning' if p['paper'] == '2B' else '')})
    for p in papers():
        for sj, name in SUBJECTS:
            ids = [q['qid'] for q in usable() if q['paper_id'] == p['id'] and q['sj'] == sj]
            if len(ids) >= 10:
                mins = {'MATH': 60, 'APT': 60, 'PLAN': 30}[sj]
                out.append({'id': 'S-%s-%s' % (sj, p['id']), 'title': '%s · %s %s' % (name, p['date'], p['paper']), 'kind': 'section', 'paper': p['paper'], 'subject': name, 'qids': ids,
                            'minutes': mins, 'note': '%d questions · %d min' % (len(ids), mins)})
    apt = sorted([q for q in usable() if q['sj'] == 'APT'], key=lambda q: (q['year'], q['paper_id'], q['n']))
    k = len(apt) // MIX_SIZE
    for m in range(k):
        ids = [q['qid'] for q in apt[m::k][:MIX_SIZE]]
        out.append({'id': 'M-APT%d' % (m + 1), 'title': 'Aptitude mixed mock %d' % (m + 1), 'kind': 'mix', 'subject': 'Aptitude', 'qids': ids, 'minutes': 60,
                    'note': '%d questions · drawn across all papers · 60 min' % len(ids)})
    _cache['tests'] = out
    _cache['test_by_id'] = {t['id']: t for t in out}
    return out


def test(tid):
    tests()
    return _cache['test_by_id'].get(tid)


def asset(q):
    return '/static/img/jee_p2/%s/q%03d.webp' % (q['paper_id'], q['n'])


def paper_for_browser(t):
    """The questions of a test as the browser sees them: picture addresses only, no keys."""
    ids = by_id()
    out = []
    for qid in t['qids']:
        q = ids[qid]
        out.append({'id': qid, 'subject': q['subject'], 'sj': q['sj'], 't': q['t'], 'n': q['n'], 'tag': '%s Q%d' % (q['paper_id'], q['n']), 'stem': asset(q)})
    return out


# ---- grading -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def _value(v):
    try:
        s = str(v).strip().replace(',', '')
        return float(s) if s not in ('', '-', '.') else None
    except (TypeError, ValueError):
        return None


def grade(t, d):
    """Mark a submission {answers: {qid: {a: 0-3 | number | null, c: G/L/M/H | null, sec: n}}, timed, seconds}. Returns (rows, error)."""
    if not isinstance(d, dict) or not isinstance(d.get('answers'), dict):
        return None, 'bad payload'
    ids = by_id()
    _load()
    rows, nat_seen = [], {}
    for qid in t['qids']:
        q = ids[qid]
        a = d['answers'].get(qid) or {}
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        ans = a.get('a')
        chosen, right = None, False
        if q['key'] == 'bonus':
            chosen = ans if (isinstance(ans, int) and not isinstance(ans, bool) and 0 <= ans <= 3) or _value(ans) is not None else None
            right = True                                                   # NTA dropped the question: full marks to everyone
        elif q['t'] == 'MCQ':
            chosen = ans if isinstance(ans, int) and not isinstance(ans, bool) and 0 <= ans <= 3 else None
            right = chosen is not None and chosen == q['key']
        else:
            v = _value(ans)
            if v is not None:
                chosen = v
                right = abs(v - float(q['key'])) <= 0.01
        ignored = False
        lim = _cache['papers'][q['paper_id']]['choose'].get((q['sj'], q['t']))
        if lim and chosen is not None and q['key'] != 'bonus':
            c = nat_seen[(q['paper_id'], q['sj'])] = nat_seen.get((q['paper_id'], q['sj']), 0) + 1
            if c > lim:
                ignored, right = True, False                                # attempt any 5: the first 5 answered count
        rows.append({'qid': qid, 'sj': q['sj'], 'chosen': chosen, 'right': right, 'conf': cf if chosen is not None else None, 'sec': _num(a.get('sec'), 0, 3600),
                     'ignored': ignored, 'bonus': q['key'] == 'bonus'})
    return rows, None


def counted(r):
    return r['chosen'] is not None and not r.get('ignored')


def marks(rows):
    right = sum(1 for r in rows if r['right'] and (counted(r) or r.get('bonus')))
    wrong = sum(1 for r in rows if counted(r) and not r['right'])
    return RIGHT * right - WRONG * wrong, right, wrong


def max_marks(t):
    """Marks available: 4 per question, but only `choose` of a 'attempt any N' numerical section."""
    ids = by_id()
    _load()
    n, per = 0, {}
    for qid in t['qids']:
        q = ids[qid]
        lim = _cache['papers'][q['paper_id']]['choose'].get((q['sj'], q['t']))
        if lim:
            k = (q['paper_id'], q['sj'])
            per[k] = per.get(k, 0) + 1
            if per[k] > lim:
                continue
        n += 1
    return RIGHT * n


def save_result(user_id, t, d):
    rows, err = grade(t, d)
    if err:
        return None, err
    score, right, wrong = marks(rows)
    att = [r for r in rows if counted(r)]
    r = PulseJeeP2Result(user_id=user_id, mock=t['id'], title=t['title'], score=score, max_score=max_marks(t), right=right, wrong=wrong, blank=len(rows) - len(att),
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
    """Subject picture, the effect of negative marking and confidence patterns over one or more attempts."""
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    subj = {sj: {'n': 0, 'right': 0, 'wrong': 0, 'blank': 0} for sj, _n in SUBJECTS}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = subj.get(x['sj'])
            if s is None or x.get('ignored'):
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
        if not (s['n'] or s['blank']):
            continue
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
            notes.append('%d answers were wrong and rated Guess or Low: you knew where the gaps were. Learn the section, then try again.' % pat['P3'])
    weak = [r['subject'] for r in sorted((r for r in srows if r['n'] >= 3), key=lambda r: r['acc'] if r['acc'] is not None else 101) if r['band'] == 'Needs reinforcement'][:3]
    return {'right': right, 'wrong': wrong, 'blank': blank, 'attempted': att, 'acc': acc, 'rated': rated, 'pat': pat, 'conf': conf, 'subjects': srows, 'notes': notes,
            'weak': weak, 'enough': rated >= MIN_RATED, 'marks': RIGHT * right - WRONG * wrong}


def for_user(user_id, limit=None):
    q = PulseJeeP2Result.query.filter_by(user_id=user_id).order_by(PulseJeeP2Result.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    an = analyse(rows)
    pcts = [round(100 * r.score / r.max_score) for r in rows if r.max_score]
    return {'attempts': len(rows), 'rows': rows[:10], 'avg_pct': round(sum(pcts) / len(pcts)) if pcts else None, 'best': max(pcts) if pcts else None, 'an': an}


def display_key(q):
    k = q['key']
    if k == 'bonus':
        return 'dropped by NTA: full marks to all'
    return LETTERS[k] if q['t'] == 'MCQ' else ('%g' % k)


def display_chosen(x, q):
    if x['chosen'] is None:
        return None
    return LETTERS[x['chosen']] if q['t'] == 'MCQ' and isinstance(x['chosen'], int) else '%g' % x['chosen']


def review(result):
    """Per-question rows of one attempt joined to the bank (picture, key) for the report page."""
    ids = by_id()
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = ids.get(x['qid'])
        if q and q['usable']:
            out.append({**x, 'subject': q['subject'], 'tag': '%s Q%d' % (q['paper_id'], q['n']), 'stem': asset(q), 'key': display_key(q), 'yours': display_chosen(x, q), 't': q['t']})
    return out
