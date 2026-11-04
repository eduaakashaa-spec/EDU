"""EduPulse-NEET: mock tests, previous-year practice and spaced reinforcement for NEET (UG).

* Bank (app/data/neet/bank.json): questions from NEET (UG) papers 2018 to 2025 that can be shown as plain text. Each answer is the one in the National Testing Agency's published answer key
  for that paper's booklet code; a question is kept only when an independent solve agreed with the key. Explanations are written by EduAakashaA with AI assistance. Questions that need a
  figure, graph or drawn structure, and questions the key does not settle (dropped or two accepted options), are left out.
* Tests: a full mock (45 questions each in Physics, Chemistry, Botany and Zoology, 180 minutes), a Physics + Chemistry half and a Biology half, previous-year papers (the text questions
  of each year, in paper order), subject sets and the Daily Review. Each mock is a fresh paper drawn from the bank, avoiding recent questions.
* Marking follows NEET: +4 for a right answer, -1 for a wrong one, nothing for a blank. Marks are worked out on the server; the key never goes to the browser before submission.
* Reinforcement: every wrong answer, and every right answer rated Guess or Low, becomes a card in Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days). The Daily Review serves due cards and
  tops up with the weakest subjects.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models_pulse import PulseNeetCard, PulseNeetResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'neet')
SEC = {'PHY': 'Physics', 'CHEM': 'Chemistry', 'BOT': 'Botany', 'ZOO': 'Zoology'}
SEC_BLURB = {'PHY': 'Mechanics, waves, thermodynamics, electricity and magnetism, optics, modern physics and electronics.',
             'CHEM': 'Physical, inorganic and organic chemistry: mole concept, equilibrium, thermodynamics, periodic table, bonding, coordination compounds and named reactions.',
             'BOT': 'Plant diversity, morphology and anatomy, plant physiology, cell biology, genetics, biotechnology and ecology.',
             'ZOO': 'Animal diversity, structural organisation, human physiology, reproduction, genetics and evolution, human health, biotechnology and environment.'}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
RIGHT_MARKS = 4
WRONG = 1
MAX_BODY = 400_000
MAX_Q = 200
MIN_RATED = 10
MIN_PER_Q = 1.0
INTERVALS = [0, 1, 3, 7, 14, 30]
DAILY_N = 10
SET_N = 20
YEAR_MIN = 40                       # a previous-year paper is offered when at least this many of its questions can be shown

# Mock recipes: subjects and number of questions each. The full mock has the NEET shape (45 per subject, 180 minutes).
MOCKS = {
    'FULL': ('NEET full mock', [('PHY', 45), ('CHEM', 45), ('BOT', 45), ('ZOO', 45)], 'Physics, Chemistry, Botany and Zoology, 45 questions each, 180 minutes. +4 right, -1 wrong.'),
    'PC': ('Physics + Chemistry half mock', [('PHY', 45), ('CHEM', 45)], 'The two physical-science sections, 90 questions, 90 minutes.'),
    'BIO': ('Biology half mock', [('BOT', 45), ('ZOO', 45)], 'Botany and Zoology, 90 questions, 90 minutes.'),
}

_cache = {}


def _read(name):
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)


def bank():
    if 'bank' not in _cache:
        qs = _read('bank.json')
        _cache['bank'] = qs
        _cache['by_id'] = {q['id']: q for q in qs}
    return _cache['bank']


def analysis():
    if 'an' not in _cache:
        _cache['an'] = _read('analysis.json')
    return _cache['an']


def get(qid):
    bank()
    return _cache['by_id'].get(qid)


def key_of(qid):
    return qid


def source_label(q):
    src = q.get('src') or []
    return ', '.join('NEET %s Q%s' % (y, n) for y, n in src[:2]) or 'EduAakashaA question bank'


def view(q):
    return {'id': q['id'], 'sec': q['sec'], 'secname': SEC[q['sec']], 'text': q['q'], 'options': [{'t': o} for o in q['opts']]}


# ---- composition -------------------------------------------------------------------------------------------------------------------------
def recent_ids(uid, k=4):
    seen = set()
    if not uid:
        return seen
    for r in PulseNeetResult.query.filter_by(user_id=uid).order_by(PulseNeetResult.finished_at.desc()).limit(k).all():
        for x in json.loads(r.payload_json or '[]'):
            seen.add(x['qid'])
    return seen


def _pick(sec, n, rng, used, avoid):
    """n question ids for a subject: fresh questions first, then the least recently seen, never a repeat inside one paper."""
    pool = [q for q in bank() if q['sec'] == sec and q['id'] not in used]
    rng.shuffle(pool)
    pool.sort(key=lambda q: q['id'] in avoid)
    out = [q['id'] for q in pool[:n]]
    used.update(out)
    return out


def year_papers():
    """Previous-year papers with enough text questions: [{id, year, n}] newest first."""
    if 'years' not in _cache:
        cnt = {}
        for q in bank():
            for y, n in q.get('src', []):
                cnt[y] = cnt.get(y, 0) + 1
        out = [{'id': 'Y-%d' % y, 'year': y, 'n': c} for y, c in cnt.items() if c >= YEAR_MIN]
        out.sort(key=lambda r: -r['year'])
        _cache['years'] = out
    return _cache['years']


def available(sec):
    return sum(1 for q in bank() if q['sec'] == sec)


def catalogue():
    out = []
    for mid, (title, spec, note) in MOCKS.items():
        n = sum(c for _, c in spec)
        out.append({'id': 'M-' + mid, 'title': title, 'kind': 'mock', 'count': n, 'minutes': int(round(n * MIN_PER_Q)), 'note': note})
    for sec in SEC:
        out.append({'id': 'S-' + sec, 'title': SEC[sec] + ' set', 'kind': 'set', 'sec': sec, 'count': SET_N, 'minutes': int(round(SET_N * MIN_PER_Q)), 'note': SEC_BLURB[sec]})
    for y in year_papers():
        out.append({'id': y['id'], 'title': 'NEET %d: questions that can be shown as text' % y['year'], 'kind': 'year', 'year': y['year'], 'count': y['n'],
                    'minutes': int(round(y['n'] * MIN_PER_Q)), 'note': 'Questions from the %d paper, in paper order.' % y['year']})
    return out


def compose(tid, uid, attempt):
    t = next((x for x in catalogue() if x['id'] == tid), None)
    if not t:
        return None
    rng = random.Random('%s-%s-%s' % (uid, tid, attempt))
    used, qids = set(), []
    avoid = recent_ids(uid)
    if t['kind'] == 'mock':
        for sec, n in MOCKS[tid[2:]][1]:
            qids += _pick(sec, n, rng, used, avoid)
    elif t['kind'] == 'set':
        qids = _pick(t['sec'], SET_N, rng, used, avoid)
    else:
        mine = [q for q in bank() if any(y == t['year'] for y, _ in q.get('src', []))]
        mine.sort(key=lambda q: next(n for y, n in q['src'] if y == t['year']))
        qids = [q['id'] for q in mine]
    return {**t, 'qids': qids, 'minutes': int(round(len(qids) * MIN_PER_Q))}


# ---- cards and Daily Review ---------------------------------------------------------------------------------------------------------------
def due_cards(uid, today=None):
    today = today or date.today()
    return PulseNeetCard.query.filter(PulseNeetCard.user_id == uid, PulseNeetCard.due <= today).order_by(PulseNeetCard.box, PulseNeetCard.due).all()


def daily(uid, today=None):
    today = today or date.today()
    n_done = PulseNeetResult.query.filter_by(user_id=uid, mock='DAILY').filter(PulseNeetResult.finished_at >= datetime.combine(today, datetime.min.time())).count()
    rng = random.Random('%s-daily-%s-%d' % (uid, today.isoformat(), n_done))
    qids, used = [], set()
    for c in due_cards(uid, today)[:6]:
        if get(c.qkey):
            qids.append(c.qkey)
            used.add(c.qkey)
    n_cards = len(qids)
    avoid = recent_ids(uid)
    order = [s for s, _ in sorted(((s, v['acc'] if v['acc'] is not None else -1) for s, v in tracker(uid)['secs'].items()), key=lambda x: x[1])]
    k = 0
    while len(qids) < DAILY_N and k < 60:
        sec = order[k % len(order)]
        k += 1
        qids += [q for q in _pick(sec, 1, rng, used, avoid) if q not in qids]
    return {'id': 'DAILY', 'title': 'Daily Review', 'kind': 'daily', 'qids': qids[:DAILY_N], 'minutes': int(round(DAILY_N * MIN_PER_Q)), 'cards': n_cards,
            'note': '%d review + %d new' % (n_cards, len(qids[:DAILY_N]) - n_cards)}


def paper_for_browser(qids):
    return [view(get(i)) for i in qids]


# ---- marking -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade_paper(d):
    """Mark {qids: [...], answers: {qid: {a, c, sec}}}: +4 right, -1 wrong, 0 blank. Returns (rows, error)."""
    if not isinstance(d, dict) or not isinstance(d.get('answers'), dict) or not isinstance(d.get('qids'), list):
        return None, 'bad payload'
    qids = []
    for i in d['qids']:
        if isinstance(i, str) and i not in qids:
            qids.append(i)
    if not qids or len(qids) > MAX_Q:
        return None, 'bad paper'
    rows = []
    for qid in qids:
        q = get(qid)
        if not q:
            return None, 'unknown question'
        a = d['answers'].get(qid) or {}
        ch = a.get('a')
        ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        rows.append({'qid': qid, 'sec': q['sec'], 'topic': q.get('topic', ''), 'chosen': ch, 'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None,
                     'secs': _num(a.get('sec'), 0, 3600)})
    return rows, None


def marks_of(rows):
    r = sum(1 for x in rows if x['right'])
    w = sum(1 for x in rows if x['chosen'] is not None and not x['right'])
    return RIGHT_MARKS * r - WRONG * w


def _update_cards(uid, rows, daily_run, today):
    tomorrow = today + timedelta(days=1)
    now = datetime.utcnow()
    for r in rows:
        if r['chosen'] is None:
            continue
        c = PulseNeetCard.query.filter_by(user_id=uid, qkey=r['qid']).first()
        unsure = r['conf'] in ('G', 'L')
        if r['right'] and not unsure:
            if c:
                c.box = min(5, c.box + 1)
                c.seen = (c.seen or 0) + 1
                c.due = today + timedelta(days=INTERVALS[c.box])
                c.right_run = (c.right_run or 0) + 1
                c.last_right = True
        else:
            if not c:
                c = PulseNeetCard(user_id=uid, qkey=r['qid'], sec=r['sec'], topic=r['topic'], box=0, seen=0, right_run=0, created_at=now)
                db.session.add(c)
            c.seen = (c.seen or 0) + 1
            if r['right']:
                c.box = max(1, min(c.box or 0, 2))
                c.due = today + timedelta(days=INTERVALS[c.box])
                c.last_right = True
            else:
                c.box = 0
                c.right_run = 0
                c.due = tomorrow if daily_run else today
                c.last_right = False
        if c is not None:
            c.updated_at = now


def save_result(uid, t, d):
    rows, err = grade_paper(d)
    if err:
        return None, err
    right = sum(1 for r in rows if r['right'])
    att = [r for r in rows if r['chosen'] is not None]
    res = PulseNeetResult(user_id=uid, mock=t['id'], title=t['title'], score=marks_of(rows), max_score=RIGHT_MARKS * len(rows), right=right, wrong=len(att) - right,
                          blank=len(rows) - len(att), rated=sum(1 for x in att if x['conf']), sure_wrong=sum(1 for x in att if not x['right'] and x['conf'] == 'H'),
                          lucky=sum(1 for x in att if x['right'] and x['conf'] in ('G', 'L')), duration_sec=_num(d.get('seconds'), 0, 20000), timed=bool(d.get('timed')),
                          finished_at=datetime.utcnow(), payload_json=json.dumps(rows, separators=(',', ':')))
    db.session.add(res)
    _update_cards(uid, rows, t['id'] == 'DAILY', date.today())
    db.session.commit()
    return res, None


# ---- analysis ----------------------------------------------------------------------------------------------------------------------------
def level(acc, n):
    if n < 5 or acc is None:
        return 'Not enough yet'
    return 'Strong' if acc >= 75 else 'Growing' if acc >= 55 else 'Starting'


def analyse(results):
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    sc = {s: {'n': 0, 'right': 0, 'blank': 0, 'secs': 0} for s in SEC}
    topics = {}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = sc.setdefault(x['sec'], {'n': 0, 'right': 0, 'blank': 0, 'secs': 0})
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            s['right'] += 1 if x['right'] else 0
            s['secs'] += x.get('secs', 0)
            tv = topics.setdefault(x.get('topic') or 'Other', {'n': 0, 'right': 0, 'sec': x['sec']})
            tv['n'] += 1
            tv['right'] += 1 if x['right'] else 0
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
    for s, v in sc.items():
        if v['n'] or v['blank']:
            acc = round(100 * v['right'] / v['n']) if v['n'] else None
            rows.append({'sec': s, 'name': SEC.get(s, s), **v, 'wrong': v['n'] - v['right'], 'net': RIGHT_MARKS * v['right'] - WRONG * (v['n'] - v['right']), 'acc': acc,
                         'avg_secs': round(v['secs'] / v['n']) if v['n'] else None, 'level': level(acc, v['n'])})
    rows.sort(key=lambda r: (r['acc'] if r['acc'] is not None else 101))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    att = sum(v['n'] for v in sc.values())
    right = sum(v['right'] for v in sc.values())
    blank = sum(v['blank'] for v in sc.values())
    wrong_n = att - right
    weak_topics = sorted([{'topic': k, **v, 'acc': round(100 * v['right'] / v['n'])} for k, v in topics.items() if v['n'] >= 2 and v['right'] < v['n']], key=lambda r: (r['acc'], -r['n']))[:6]
    notes = []
    if wrong_n and att:
        notes.append('Each wrong answer cost %d mark and each right answer earns %d, so %d wrong answers took away %d marks and also the %d they could have earned. '
                     'Answer when you can remove at least two options; leave the rest.' % (WRONG, RIGHT_MARKS, wrong_n, WRONG * wrong_n, RIGHT_MARKS * wrong_n))
    if blank and att and blank > att * 0.35:
        notes.append('%d question(s) were left blank. Check whether they cluster in one subject: a few focused chapters can recover many of them.' % blank)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer next time.')
    else:
        if pat['P4']:
            notes.append('%d answer(s) were wrong although you rated them High. With negative marking these cost most; they are now in your review cards.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answer(s) were right but rated Guess or Low: the idea is not secure yet, so they are in your review cards too.' % pat['P2'])
        if pat['P3']:
            notes.append('%d answer(s) were wrong and rated Guess or Low. You knew where the gaps were: skipping such questions would have saved marks.' % pat['P3'])
    return {'right': right, 'wrong': wrong_n, 'blank': blank, 'attempted': att, 'acc': round(100 * right / att) if att else None, 'rated': rated, 'pat': pat, 'conf': conf, 'secs': rows,
            'weak_topics': weak_topics, 'notes': notes, 'weak': [r for r in rows if r['level'] in ('Starting', 'Growing')][:3], 'strong': [r for r in reversed(rows) if r['level'] == 'Strong'][:3]}


def for_user(uid, limit=None):
    q = PulseNeetResult.query.filter_by(user_id=uid).order_by(PulseNeetResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def review(result):
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = get(x['qid'])
        if not q:
            continue
        out.append({**x, 'view': view(q), 'ans': q['ans'], 'why': q.get('why', ''), 'secname': SEC[q['sec']], 'source': source_label(q)})
    return out


# ---- tracker -----------------------------------------------------------------------------------------------------------------------------
BADGES = [
    ('first', 'First paper', 'Finish your first test.'),
    ('streak3', 'Three-day streak', 'Practise on three days in a row.'),
    ('streak7', 'Seven-day streak', 'Practise on seven days in a row.'),
    ('hundred', 'Hundred answers', 'Answer 100 questions.'),
    ('allsec', 'All four subjects', 'Answer at least 10 questions in each of Physics, Chemistry, Botany and Zoology.'),
    ('mock', 'Full mock', 'Finish a full NEET mock.'),
    ('comeback', 'Comeback', 'Bring a review card up to box 3 or higher.'),
    ('honest', 'Honest rater', 'Rate 30 answers with your confidence, with High answers right more often than Guess answers.'),
]


def tracker(uid, today=None):
    today = today or date.today()
    res = for_user(uid)
    rows = []
    for r in reversed(res):
        for x in json.loads(r.payload_json or '[]'):
            if x['chosen'] is not None:
                rows.append({**x, 'day': r.finished_at.date()})
    secs = {}
    for s in SEC:
        mine = [x for x in rows if x['sec'] == s]
        last, prev = mine[-20:], mine[-40:-20]
        acc = round(100 * sum(1 for x in last if x['right']) / len(last)) if last else None
        pacc = round(100 * sum(1 for x in prev if x['right']) / len(prev)) if len(prev) >= 5 else None
        secs[s] = {'name': SEC[s], 'n': len(mine), 'acc': acc, 'level': level(acc, len(last)), 'delta': (acc - pacc) if acc is not None and pacc is not None else None}
    tp = {}
    for x in rows:
        v = tp.setdefault(x.get('topic') or 'Other', {'n': 0, 'right': 0, 'sec': x['sec']})
        v['n'] += 1
        v['right'] += 1 if x['right'] else 0
    weak_topics = sorted([{'topic': k, **v, 'acc': round(100 * v['right'] / v['n'])} for k, v in tp.items() if v['n'] >= 3], key=lambda r: (r['acc'], -r['n']))[:6]
    days = sorted({r.finished_at.date() for r in res})
    streak = 0
    d = today if today in days else today - timedelta(days=1)
    while d in days:
        streak += 1
        d -= timedelta(days=1)
    best = run = 0
    for i, dd in enumerate(days):
        run = run + 1 if i and (dd - days[i - 1]).days == 1 else 1
        best = max(best, run)
    cards = PulseNeetCard.query.filter_by(user_id=uid).all()
    boxes = [sum(1 for c in cards if c.box == b) for b in range(6)]
    rated = [x for x in rows if x.get('conf')]
    h = [x for x in rated if x['conf'] == 'H']
    g = [x for x in rated if x['conf'] == 'G']
    honest = len(rated) >= 30 and h and (not g or (sum(1 for x in h if x['right']) / len(h)) > (sum(1 for x in g if x['right']) / len(g)))
    earned = {'first': bool(res), 'streak3': best >= 3, 'streak7': best >= 7, 'hundred': len(rows) >= 100, 'allsec': all(secs[s]['n'] >= 10 for s in SEC),
              'mock': any(r.mock == 'M-FULL' for r in res), 'comeback': any(c.box >= 3 for c in cards), 'honest': bool(honest)}
    mocks = [{'date': r.finished_at.strftime('%d %b'), 'score': r.score, 'max': r.max_score, 'pct': round(100 * r.score / r.max_score) if r.max_score else 0, 'title': r.title}
             for r in reversed(res) if r.mock.startswith(('M-', 'Y-'))][-10:]
    return {'attempts': len(res), 'answers': len(rows), 'secs': secs, 'weak_topics': weak_topics, 'streak': streak, 'best_streak': best, 'cards': len(cards), 'boxes': boxes,
            'due': sum(1 for c in cards if c.due and c.due <= today), 'badges': [{'id': i, 'name': n, 'desc': dsc, 'got': earned[i]} for i, n, dsc in BADGES], 'mocks': mocks,
            'recent': res[:8]}
