"""EduPulse-NID: timed mock tests and practice sets for the NID Design Aptitude Test (B.Des Prelims and M.Des CDAT Paper 1 formats).

* The question bank (app/data/nid/bank.json) is original EduAakashaA material: visual and spatial questions built by code (the answer is computed), and text questions
  written for the exam's topics and checked by an independent solve. Each question has marks (1 or 2) and an explanation.
* Official practice: NID's own sample papers (2024 and 2025, B.Des and M.Des) cut into question images, with answers and explanations worked out by us
  (NID prints no answer key). Their option letters are part of the picture.
* Tests: B.Des mocks of 20 questions for 25 marks (15 x 1 mark and 5 x 2 marks, as in NID's sample), M.Des CDAT mocks of 18 questions for 20 marks, official sample
  papers, and section sets by topic. The open drawing and studio tasks are practised in the Studio section (self-assessed against a rubric: they are not marked here).
* Marking follows the printed papers: the marks on the question, nothing deducted for a wrong answer (the sample papers print no negative marking; confirm in the
  current NID handbook). Grading happens on the server: the key never goes to the browser before submission.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
from datetime import datetime

from app.extensions import db
from app.models_pulse import PulseNidResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'nid')
SEC = {'VIS': 'Visual reasoning', 'SPA': 'Spatial reasoning', 'LOG': 'Logical reasoning', 'CLR': 'Colour theory', 'PRI': 'Design principles', 'AWR': 'Design awareness',
       'HIS': 'Design history', 'CRF': 'Indian crafts and culture', 'MAT': 'Materials and printing', 'ERG': 'Ergonomics', 'SUS': 'Sustainability', 'SCI': 'Science and objects',
       'GKN': 'General knowledge', 'LAN': 'Language', 'CRT': 'Critical thinking'}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
MAX_BODY = 200_000
MIN_RATED = 8
MINUTES_PER_MARK = 1.2          # our practice time: NID's sample papers print no duration

_cache = {}

# test recipes: (group of sections, marks of the question). DES groups the design-knowledge sections.
GROUPS = {'DES': ('PRI', 'CLR', 'ERG', 'SUS', 'HIS'), 'LOGIC': ('LOG',), 'SPA': ('SPA',), 'VIS': ('VIS',), 'AWR': ('AWR',), 'CRF': ('CRF', 'HIS'), 'MAT': ('MAT',), 'SCI': ('SCI',),
          'GKN': ('GKN',), 'LAN': ('LAN',), 'CRT': ('CRT',), 'ANY': tuple(SEC)}
B_SPEC = [('SPA', 1), ('SPA', 1), ('VIS', 1), ('LOGIC', 1), ('DES', 1), ('DES', 1), ('AWR', 1), ('AWR', 1), ('CRF', 1), ('CRF', 1), ('MAT', 1), ('SCI', 1), ('GKN', 1), ('LAN', 1), ('LAN', 1),
          ('SPA', 2), ('VIS', 2), ('VIS', 2), ('LOGIC', 2), ('DES', 2)]
M_SPEC = [('CRT', 1), ('CRT', 1), ('CRT', 1), ('CRT', 1), ('LOGIC', 1), ('LOGIC', 1), ('LOGIC', 1), ('DES', 1), ('DES', 1), ('DES', 1), ('DES', 1), ('MAT', 1), ('AWR', 1),
          ('SCI', 1), ('GKN', 1), ('LAN', 1), ('LOGIC', 2), ('DES', 2)]
FULL_MOCKS = 4
SET_SIZE = 12


def _read(name):
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)


def bank():
    if 'bank' not in _cache:
        qs = _read('bank.json')
        for q in qs:
            q['progs'] = ('B',) if q['level'] == 'B' else ('M',) if q['level'] == 'M' else ('B', 'M')
        _cache['bank'] = qs
        _cache['by_id'] = {q['id']: q for q in qs}
    return _cache['bank']


def by_id():
    bank()
    return _cache['by_id']


def official():
    """Official sample papers: {'papers': [...], 'questions': [...] with 'ans' and 'why' where a key is present}."""
    if 'off' not in _cache:
        d = _read('official.json')
        try:
            keys = {(k['paper'], k['n']): k for k in _read('official_keys.json')}
        except OSError:
            keys = {}
        for q in d['questions']:
            k = keys.get((q['paper'], q['n']))
            q['id'] = '%s-%02d' % (q['paper'], q['n'])
            q['ans'] = 'ABCD'.index(k['ans']) if k and k.get('ans') in LETTERS else None
            q['why'] = (k or {}).get('why', '')
            q['topic'] = (k or {}).get('topic', '')
            q['usable'] = q['ans'] is not None
        _cache['off'] = d
        _cache['off_by_id'] = {q['id']: q for q in d['questions']}
    return _cache['off']


def off_by_id():
    official()
    return _cache['off_by_id']


def tasks():
    if 'tasks' not in _cache:
        _cache['tasks'] = _read('tasks.json')
    return _cache['tasks']


def analysis():
    if 'ana' not in _cache:
        try:
            _cache['ana'] = _read('analysis.json')
        except OSError:
            _cache['ana'] = {}
    return _cache['ana']


def _pick(spec, prog, m):
    """One question per slot of the recipe, never repeating a question inside a test or across the full mocks of the same programme where the bank allows it."""
    used = _cache.setdefault('used_' + prog, set())
    out, here = [], set()
    for grp, marks in spec:
        secs = GROUPS[grp]
        pool = [q for q in bank() if q['sec'] in secs and prog in q['progs'] and q['marks'] == marks and q['id'] not in here]
        if not pool:
            pool = [q for q in bank() if q['sec'] in secs and prog in q['progs'] and q['id'] not in here]
        if not pool:                                           # no question of this kind at this level: take one from the neighbouring level
            pool = [q for q in bank() if q['sec'] in secs and q['marks'] == marks and q['id'] not in here] or [q for q in bank() if q['sec'] in secs and q['id'] not in here]
        fresh = [q for q in pool if q['id'] not in used] or pool
        # rotate through the sections of a group so a mock mixes them; the mock number moves the starting point
        fresh.sort(key=lambda q: (q['id']))
        q = fresh[(m * 7) % len(fresh)] if len(fresh) > 1 else fresh[0]
        out.append(q)
        here.add(q['id'])
        used.add(q['id'])
    return out


def tests():
    """[{id, title, kind, qids, minutes, note, marks, prog, source}]"""
    if 'tests' in _cache:
        return _cache['tests']
    out = []
    _cache.pop('used_B', None)
    _cache.pop('used_M', None)
    for m in range(FULL_MOCKS):
        qs = _pick(B_SPEC, 'B', m)
        mk = sum(q['marks'] for q in qs)
        out.append({'id': 'B%d' % (m + 1), 'title': 'B.Des Prelims mock %d' % (m + 1), 'kind': 'full', 'prog': 'B', 'qids': [q['id'] for q in qs], 'marks': mk,
                    'minutes': int(round(mk * MINUTES_PER_MARK)), 'source': 'bank', 'note': '%d questions · %d marks · objective part of the B.Des paper' % (len(qs), mk)})
    for m in range(FULL_MOCKS):
        qs = _pick(M_SPEC, 'M', m)
        mk = sum(q['marks'] for q in qs)
        out.append({'id': 'M%d' % (m + 1), 'title': 'M.Des CDAT Paper 1 mock %d' % (m + 1), 'kind': 'full', 'prog': 'M', 'qids': [q['id'] for q in qs], 'marks': mk,
                    'minutes': int(round(mk * MINUTES_PER_MARK)), 'source': 'bank', 'note': '%d questions · %d marks · reasoning and design literacy' % (len(qs), mk)})
    for p in official()['papers']:
        qs = [q for q in official()['questions'] if q['paper'] == p['code'] and q['usable']]
        if qs:
            mk = sum(q['marks'] for q in qs)
            out.append({'id': 'O-' + p['code'], 'title': p['title'], 'kind': 'official', 'prog': 'B' if p['programme'] == 'B.Des' else 'M', 'qids': [q['id'] for q in qs], 'marks': mk,
                        'minutes': int(round(mk * MINUTES_PER_MARK)), 'source': 'official', 'note': '%d of the %d objective questions · %d marks · NID’s own paper' % (len(qs), p['questions'], mk)})
    secs = [('SPA', 'Spatial reasoning'), ('VIS', 'Visual reasoning'), ('LOG', 'Logical reasoning'), ('LAN', 'Language'), ('CRT', 'Critical thinking'), ('CLR', 'Colour theory'),
            ('PRI', 'Design principles'), ('ERG', 'Ergonomics'), ('AWR', 'Design awareness'), ('HIS', 'Design history'), ('CRF', 'Indian crafts and culture'), ('MAT', 'Materials and printing'),
            ('SUS', 'Sustainability'), ('SCI', 'Science and objects'), ('GKN', 'General knowledge')]
    for sj, name in secs:
        rows = sorted([q for q in bank() if q['sec'] == sj], key=lambda q: q['id'])
        n = max(1, (len(rows) + SET_SIZE - 1) // SET_SIZE)
        size = (len(rows) + n - 1) // n
        for i in range(n):
            chunk = rows[i * size:(i + 1) * size]
            if chunk:
                mk = sum(q['marks'] for q in chunk)
                out.append({'id': 'S-%s%d' % (sj, i + 1), 'title': '%s set %d' % (name, i + 1) if n > 1 else name, 'kind': 'section', 'sec': sj, 'section': name,
                            'prog': 'M' if sj == 'CRT' else 'B' if sj in ('SPA', 'VIS') else 'BM', 'qids': [q['id'] for q in chunk], 'marks': mk, 'minutes': int(round(mk * MINUTES_PER_MARK)),
                            'source': 'bank', 'note': '%d questions · %d marks' % (len(chunk), mk)})
    _cache['tests'] = out
    _cache['test_by_id'] = {t['id']: t for t in out}
    return out


def test(tid):
    tests()
    return _cache['test_by_id'].get(tid)


def _question(q, official_q=False):
    if official_q:
        return {'id': q['id'], 'sec': 'Official sample', 'secname': 'Official sample', 'marks': q['marks'], 'img': '/static/' + q['img'], 'options': [{'t': L} for L in LETTERS]}
    d = {'id': q['id'], 'sec': q['sec'], 'secname': SEC[q['sec']], 'marks': q['marks'], 'text': q['q'], 'options': [({'svg': o['svg']} if o.get('svg') else {'t': o.get('t')}) for o in q['opts']]}
    if q.get('svg'):
        d['svg'] = q['svg']
    if q.get('passage'):
        d['passage'] = q['passage']
    return d


def paper_for_browser(t):
    """The questions of a test as the browser sees them: no answers, no explanations."""
    out = []
    for qid in t['qids']:
        if t['source'] == 'official':
            out.append(_question(off_by_id()[qid], True))
        else:
            out.append(_question(by_id()[qid]))
    return out


# ---- grading -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade(t, d):
    """Mark a submission {answers: {qid: {a: 0-3 or null, c: G/L/M/H or null, sec: n}}, timed, seconds}. Returns (rows, error)."""
    if not isinstance(d, dict) or not isinstance(d.get('answers'), dict):
        return None, 'bad payload'
    rows = []
    for qid in t['qids']:
        a = d['answers'].get(qid) or {}
        ch = a.get('a')
        ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        q = off_by_id()[qid] if t['source'] == 'official' else by_id()[qid]
        sec = 'OFF' if t['source'] == 'official' else q['sec']
        rows.append({'qid': qid, 'sec': sec, 'topic': q.get('topic', ''), 'marks': q['marks'], 'chosen': ch, 'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None,
                     'secs': _num(a.get('sec'), 0, 3600)})
    return rows, None


def marks_of(rows):
    return sum(r['marks'] for r in rows if r['right']), sum(1 for r in rows if r['right']), sum(1 for r in rows if r['chosen'] is not None and not r['right'])


def save_result(user_id, t, d):
    rows, err = grade(t, d)
    if err:
        return None, err
    score, right, wrong = marks_of(rows)
    att = [r for r in rows if r['chosen'] is not None]
    r = PulseNidResult(user_id=user_id, mock=t['id'], title=t['title'], score=score, max_score=sum(x['marks'] for x in rows), right=right, wrong=wrong, blank=len(rows) - len(att),
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
    """Section picture, marks, and confidence patterns over one or more attempts."""
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    secs = {}
    rated = 0
    gained = lost = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = secs.setdefault(x['sec'], {'n': 0, 'right': 0, 'blank': 0, 'marks': 0, 'max': 0})
            s['max'] += x.get('marks', 1)
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            if x['right']:
                s['right'] += 1
                s['marks'] += x.get('marks', 1)
                gained += x.get('marks', 1)
            else:
                lost += x.get('marks', 1)
            c = x.get('conf')
            if c:
                rated += 1
                conf[c]['n'] += 1
                conf[c]['right'] += 1 if x['right'] else 0
                if x['right']:
                    pat['P1' if c in ('H', 'M') else 'P2'] += 1
                else:
                    pat['P4' if c == 'H' else 'P3'] += 1
    rows = []
    for sj, s in secs.items():
        acc = round(100 * s['right'] / s['n']) if s['n'] else None
        rows.append({'sec': sj, 'name': SEC.get(sj, 'Official sample paper'), **s, 'acc': acc, 'band': band(acc or 0, s['n'])})
    rows.sort(key=lambda r: (r['acc'] if r['acc'] is not None else 101, -r['n']))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    right = sum(s['right'] for s in secs.values())
    att = sum(s['n'] for s in secs.values())
    blank = sum(s['blank'] for s in secs.values())
    acc = round(100 * right / att) if att else None
    notes = []
    if blank and att:
        notes.append('You left %d question(s) blank. With no marks deducted for a wrong answer in the printed sample papers, an informed guess costs nothing: attempt every question, then use the confidence rating to see which guesses to learn from.' % blank)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer in the next test.')
    else:
        if pat['P4']:
            notes.append('%d answers were wrong although you rated them High: check these first, they point to a wrong method or a misunderstood idea.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answers were right but rated Guess or Low: the idea is not secure yet.' % pat['P2'])
        if pat['P3']:
            notes.append('%d answers were wrong and rated Guess or Low: you knew where the gaps were. Learn the topic, then try the section set again.' % pat['P3'])
    weak = [r['name'] for r in rows if r['band'] == 'Needs reinforcement'][:4]
    return {'right': right, 'wrong': att - right, 'blank': blank, 'attempted': att, 'acc': acc, 'rated': rated, 'pat': pat, 'conf': conf, 'sections': rows, 'notes': notes, 'weak': weak,
            'enough': rated >= MIN_RATED, 'marks': gained, 'lost': lost}


def for_user(user_id, limit=None):
    q = PulseNidResult.query.filter_by(user_id=user_id).order_by(PulseNidResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    an = analyse(rows)
    pcts = [round(100 * r.score / r.max_score) for r in rows if r.max_score]
    return {'attempts': len(rows), 'rows': rows[:10], 'avg_pct': round(sum(pcts) / len(pcts)) if pcts else None, 'best': max(pcts) if pcts else None, 'an': an}


def review(result):
    """Per-question rows of one attempt joined to the bank (question, key, explanation) for the report page."""
    out = []
    for x in json.loads(result.payload_json or '[]'):
        qid = x['qid']
        if qid in off_by_id():
            q = off_by_id()[qid]
            out.append({**x, 'view': _question(q, True), 'ans': q['ans'], 'why': q.get('why', ''), 'topic': q.get('topic', ''), 'secname': 'Official sample paper'})
        elif qid in by_id():
            q = by_id()[qid]
            out.append({**x, 'view': _question(q), 'ans': q['ans'], 'why': q.get('why', ''), 'topic': q.get('topic', ''), 'secname': SEC[q['sec']]})
    return out
