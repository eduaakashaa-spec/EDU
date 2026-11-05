"""EduPulse-SAT: practice tests and spaced reinforcement for the Digital SAT (Reading and Writing, Math).

* Questions are original EduAakashaA practice questions, not College Board questions. Reading and Writing (app/data/sat/rw_bank.json, 199 questions): written for the eight skill groups of the
  College Board's published content domains and kept only when an independent blind solve gave the same answer. Math (app/services/sat_gen.py): built by code from the answer, so each is correct
  by construction; a new set of numbers is drawn for every attempt, and about a third of the questions are student-produced response (type the number).
* Tests: a full practice SAT (54 Reading and Writing + 44 Math questions in the official domain shares, 134 minutes), a Reading and Writing half (64 minutes), a Math half (70 minutes),
  domain sets and the Daily Review. These practice tests are NOT adaptive and carry no official scaled score; results are shown as questions right and percent right.
* No negative marking: a right answer counts one, a wrong or blank answer counts nothing (the real SAT also does not subtract for wrong answers).
* Reinforcement: every wrong answer, and every right answer rated Guess or Low, becomes a card in Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days). A Reading and Writing card returns as the same
  question; a Math card returns as a fresh question of the same kind.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models_pulse import PulseSatCard, PulseSatResult
from app.services import sat_gen

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sat')
SEC = {'RW': 'Reading and Writing', 'MATH': 'Math'}
RW_DOMAINS = ['Information and Ideas', 'Craft and Structure', 'Expression of Ideas', 'Standard English Conventions']
MATH_DOMAINS = list(sat_gen.DOMAINS)
DOM_SEC = {**{d: 'RW' for d in RW_DOMAINS}, **{d: 'MATH' for d in MATH_DOMAINS}}
DOM_CODE = {'II': RW_DOMAINS[0], 'CS': RW_DOMAINS[1], 'EI': RW_DOMAINS[2], 'SEC': RW_DOMAINS[3], 'ALG': MATH_DOMAINS[0], 'ADV': MATH_DOMAINS[1], 'PSDA': MATH_DOMAINS[2], 'GEO': MATH_DOMAINS[3]}
DOM_BLURB = {
    'Information and Ideas': 'Central ideas and details, command of evidence (text and data) and inferences.',
    'Craft and Structure': 'Words in context, text structure and purpose, and connections between two texts.',
    'Expression of Ideas': 'Rhetorical synthesis (use notes for a goal) and transitions.',
    'Standard English Conventions': 'Sentence boundaries, punctuation, verb and pronoun forms, and sentence structure.',
    'Algebra': 'Linear equations, linear functions, systems and linear inequalities.',
    'Advanced Math': 'Equivalent expressions, quadratic and exponential equations and nonlinear functions.',
    'Problem-Solving and Data Analysis': 'Ratios, rates, percentages, statistics, probability and data tables.',
    'Geometry and Trigonometry': 'Area and volume, lines and angles, right triangles, trigonometry and circles.',
}
# The official domain shares of a section; counts for a 54-question and a 44-question paper.
FULL_RW = [('Information and Ideas', 13), ('Craft and Structure', 15), ('Expression of Ideas', 11), ('Standard English Conventions', 15)]
FULL_MATH = [('Algebra', 15), ('Advanced Math', 15), ('Problem-Solving and Data Analysis', 7), ('Geometry and Trigonometry', 7)]
RW_MIN_PER_Q = 64 / 54.0
MATH_MIN_PER_Q = 70 / 44.0
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
MAX_BODY = 300_000
MAX_Q = 120
MIN_RATED = 10
INTERVALS = [0, 1, 3, 7, 14, 30]
DAILY_N = 10
SET_N = 15

MOCKS = {
    'FULL': ('Full practice SAT', 'Reading and Writing (54 questions) then Math (44 questions), 134 minutes in all. One clock for the whole paper; the real test has four timed modules and a break.'),
    'RW': ('Reading and Writing half', '54 questions, 64 minutes: the two Reading and Writing modules as one paper.'),
    'MATH': ('Math half', '44 questions, 70 minutes: the two Math modules as one paper. A calculator is allowed.'),
}

_cache = {}


def bank():
    if 'bank' not in _cache:
        with open(os.path.join(DATA_DIR, 'rw_bank.json'), encoding='utf-8') as f:
            qs = json.load(f)
        _cache['bank'] = qs
        _cache['by_id'] = {q['id']: q for q in qs}
    return _cache['bank']


def get(qid):
    """A question dict by id: 'rw:012' from the bank or 'g:<family>:<seed>' built by the Math generator."""
    if not isinstance(qid, str):
        return None
    if qid.startswith('g:'):
        q = sat_gen.from_id(qid)
        return q
    bank()
    return _cache['by_id'].get(qid)


def card_key(qid):
    """A generated question is reviewed as its family, so a Math card returns with fresh numbers."""
    if qid.startswith('g:'):
        return 'g:' + qid.split(':')[1]
    return qid


def view(q):
    """What the browser may see: no answer, no explanation."""
    base = {'id': q['id'], 'sec': q['sec'], 'secname': SEC[q['sec']], 'domain': q['domain'], 'text': q['stem'], 'passage': q.get('passage', '')}
    if q.get('kind') == 'spr':
        return {**base, 'spr': True, 'options': []}
    return {**base, 'spr': False, 'options': [{'t': o} for o in q['opts']]}


def stats():
    n = len(bank())
    return {'rw': n, 'math_families': len(sat_gen.FAMILIES)}


def source_label(q):
    return 'EduAakashaA original question' + (' (generated)' if q['id'].startswith('g:') else '')


# ---- composition -------------------------------------------------------------------------------------------------------------------------
def minutes_for(qids):
    m = 0.0
    for i in qids:
        m += RW_MIN_PER_Q if i.startswith('rw:') else MATH_MIN_PER_Q
    return int(round(m))


def recent_ids(uid, k=4):
    seen = set()
    if not uid:
        return seen
    for r in PulseSatResult.query.filter_by(user_id=uid).order_by(PulseSatResult.finished_at.desc()).limit(k).all():
        for x in json.loads(r.payload_json or '[]'):
            seen.add(x['qid'])
    return seen


def _pick(domain, n, rng, used, avoid):
    """n question ids for a domain: new R&W questions first (then the least recently seen), a fresh draw for Math; never a repeat inside one paper."""
    out = []
    if DOM_SEC[domain] == 'RW':
        pool = [q for q in bank() if q['domain'] == domain and q['id'] not in used]
        rng.shuffle(pool)
        pool.sort(key=lambda q: q['id'] in avoid)
        out = [q['id'] for q in pool[:n]]
    else:
        guard = 0
        while len(out) < n and guard < n * 20:
            guard += 1
            qid = sat_gen.pick(domain, rng)
            if qid not in used and qid not in out:
                out.append(qid)
    used.update(out)
    return out


def catalogue():
    out = []
    for mid, (title, note) in MOCKS.items():
        n = {'FULL': 98, 'RW': 54, 'MATH': 44}[mid]
        mins = {'FULL': 134, 'RW': 64, 'MATH': 70}[mid]
        out.append({'id': 'M-' + mid, 'title': title, 'kind': 'mock', 'count': n, 'minutes': mins, 'note': note})
    for code, dom in DOM_CODE.items():
        per = RW_MIN_PER_Q if DOM_SEC[dom] == 'RW' else MATH_MIN_PER_Q
        out.append({'id': 'S-' + code, 'title': dom + ' set', 'kind': 'set', 'dom': dom, 'sec': DOM_SEC[dom], 'count': SET_N, 'minutes': int(round(SET_N * per)), 'note': DOM_BLURB[dom]})
    return out


def compose(tid, uid, attempt):
    t = next((x for x in catalogue() if x['id'] == tid), None)
    if not t:
        return None
    rng = random.Random('%s-%s-%s' % (uid, tid, attempt))
    used, qids = set(), []
    avoid = recent_ids(uid)
    if t['kind'] == 'mock':
        if tid in ('M-FULL', 'M-RW'):
            for dom, n in FULL_RW:
                qids += _pick(dom, n, rng, used, avoid)
        if tid in ('M-FULL', 'M-MATH'):
            for dom, n in FULL_MATH:
                qids += _pick(dom, n, rng, used, avoid)
    else:
        qids = _pick(t['dom'], SET_N, rng, used, avoid)
    return {**t, 'qids': qids, 'minutes': t['minutes'] if t['kind'] == 'mock' else minutes_for(qids)}


# ---- cards and Daily Review --------------------------------------------------------------------------------------------------------------
def due_cards(uid, today=None):
    today = today or date.today()
    return PulseSatCard.query.filter(PulseSatCard.user_id == uid, PulseSatCard.due <= today).order_by(PulseSatCard.box, PulseSatCard.due).all()


def daily(uid, today=None):
    today = today or date.today()
    n_done = PulseSatResult.query.filter_by(user_id=uid, mock='DAILY').filter(PulseSatResult.finished_at >= datetime.combine(today, datetime.min.time())).count()
    rng = random.Random('%s-daily-%s-%d' % (uid, today.isoformat(), n_done))
    qids, used = [], set()
    for c in due_cards(uid, today)[:6]:
        if c.qkey.startswith('g:'):
            fam = c.qkey.split(':')[1]
            if fam in sat_gen.FAMILIES:
                qid = 'g:%s:%d' % (fam, rng.randint(1, 10 ** 6))
                qids.append(qid)
                used.add(qid)
        elif get(c.qkey):
            qids.append(c.qkey)
            used.add(c.qkey)
    n_cards = len(qids)
    avoid = recent_ids(uid)
    secs = tracker(uid)['secs']
    order = [s for s, _ in sorted(((s, v['acc'] if v['acc'] is not None else -1) for s, v in secs.items()), key=lambda x: x[1])]
    doms = {'RW': RW_DOMAINS, 'MATH': MATH_DOMAINS}
    k = 0
    while len(qids) < DAILY_N and k < 60:
        sec = order[k % len(order)]
        dom = doms[sec][(k // len(order)) % 4]
        k += 1
        qids += [q for q in _pick(dom, 1, rng, used, avoid) if q not in qids]
    qids = qids[:DAILY_N]
    return {'id': 'DAILY', 'title': 'Daily Review', 'kind': 'daily', 'qids': qids, 'minutes': minutes_for(qids), 'cards': n_cards, 'note': '%d review + %d new' % (n_cards, len(qids) - n_cards)}


def paper_for_browser(qids):
    return [view(get(i)) for i in qids]


# ---- marking -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade_paper(d):
    """Mark {qids: [...], answers: {qid: {a, c, sec}}}: one for a right answer, nothing otherwise. a is the option index (0-3) or, for a student-produced response, the typed text."""
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
        if q.get('kind') == 'spr':
            ch = ch.strip()[:12] if isinstance(ch, str) and ch.strip() else None
            right = ch is not None and sat_gen.is_correct(q, ch)
        else:
            ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
            right = ch is not None and ch == q['ans']
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        rows.append({'qid': qid, 'sec': q['sec'], 'dom': q['domain'], 'topic': q.get('skill', ''), 'spr': q.get('kind') == 'spr', 'chosen': ch, 'right': bool(right),
                     'conf': cf if ch is not None else None, 'secs': _num(a.get('sec'), 0, 3600)})
    return rows, None


def _update_cards(uid, rows, daily_run, today):
    tomorrow = today + timedelta(days=1)
    now = datetime.utcnow()
    for r in rows:
        if r['chosen'] is None:
            continue
        key = card_key(r['qid'])
        c = PulseSatCard.query.filter_by(user_id=uid, qkey=key).first()
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
                c = PulseSatCard(user_id=uid, qkey=key, sec=r['sec'], topic=r['topic'], box=0, seen=0, right_run=0, created_at=now)
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
    res = PulseSatResult(user_id=uid, mock=t['id'], title=t['title'], score=right, max_score=len(rows), right=right, wrong=len(att) - right, blank=len(rows) - len(att),
                         rated=sum(1 for x in att if x['conf']), sure_wrong=sum(1 for x in att if not x['right'] and x['conf'] == 'H'),
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
    dm = {}
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
            dv = dm.setdefault(x.get('dom') or 'Other', {'n': 0, 'right': 0, 'sec': x['sec']})
            dv['n'] += 1
            dv['right'] += 1 if x['right'] else 0
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
            rows.append({'sec': s, 'name': SEC.get(s, s), **v, 'wrong': v['n'] - v['right'], 'acc': acc, 'avg_secs': round(v['secs'] / v['n']) if v['n'] else None, 'level': level(acc, v['n'])})
    rows.sort(key=lambda r: (r['acc'] if r['acc'] is not None else 101))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    att = sum(v['n'] for v in sc.values())
    right = sum(v['right'] for v in sc.values())
    blank = sum(v['blank'] for v in sc.values())
    wrong_n = att - right
    doms = sorted([{'dom': k, **v, 'acc': round(100 * v['right'] / v['n'])} for k, v in dm.items()], key=lambda r: (r['acc'], -r['n']))
    notes = []
    if blank and att:
        notes.append('%d question(s) were left blank. The SAT has no penalty for a wrong answer, so always choose an answer; after removing one or two options a guess is worth making.' % blank)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer next time.')
    else:
        if pat['P4']:
            notes.append('%d answer(s) were wrong although you rated them High: a misunderstanding rather than a slip. They are now in your review cards.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answer(s) were right but rated Guess or Low: the idea is not secure yet, so they are in your review cards too.' % pat['P2'])
    return {'right': right, 'wrong': wrong_n, 'blank': blank, 'attempted': att, 'acc': round(100 * right / att) if att else None, 'rated': rated, 'pat': pat, 'conf': conf, 'secs': rows,
            'doms': doms, 'weak_doms': [d for d in doms if d['n'] >= 2 and d['acc'] < 75][:4], 'notes': notes,
            'weak': [r for r in rows if r['level'] in ('Starting', 'Growing')][:3], 'strong': [r for r in reversed(rows) if r['level'] == 'Strong'][:3]}


def for_user(uid, limit=None):
    q = PulseSatResult.query.filter_by(user_id=uid).order_by(PulseSatResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def review(result):
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = get(x['qid'])
        if not q:
            continue
        out.append({**x, 'view': view(q), 'ans': q.get('ans') if q.get('kind') != 'spr' else None, 'ans_text': q.get('ans_text') if q.get('kind') == 'spr' else None,
                    'why': q.get('why', ''), 'secname': SEC[q['sec']], 'source': source_label(q)})
    return out


# ---- tracker -----------------------------------------------------------------------------------------------------------------------------
BADGES = [
    ('first', 'First paper', 'Finish your first test.'),
    ('streak3', 'Three-day streak', 'Practise on three days in a row.'),
    ('streak7', 'Seven-day streak', 'Practise on seven days in a row.'),
    ('hundred', 'Hundred answers', 'Answer 100 questions.'),
    ('both', 'Both sections', 'Answer at least 10 questions in Reading and Writing and in Math.'),
    ('mock', 'Full practice SAT', 'Finish a full practice SAT.'),
    ('spr', 'Type it in', 'Answer 10 student-produced response (type the number) questions.'),
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
    dd = {}
    for x in rows:
        v = dd.setdefault(x.get('dom') or 'Other', {'n': 0, 'right': 0, 'sec': x['sec']})
        v['n'] += 1
        v['right'] += 1 if x['right'] else 0
    doms = sorted([{'dom': k, **v, 'acc': round(100 * v['right'] / v['n'])} for k, v in dd.items() if v['n'] >= 3], key=lambda r: (r['acc'], -r['n']))
    days = sorted({r.finished_at.date() for r in res})
    streak = 0
    d = today if today in days else today - timedelta(days=1)
    while d in days:
        streak += 1
        d -= timedelta(days=1)
    best = run = 0
    for i, dy in enumerate(days):
        run = run + 1 if i and (dy - days[i - 1]).days == 1 else 1
        best = max(best, run)
    cards = PulseSatCard.query.filter_by(user_id=uid).all()
    boxes = [sum(1 for c in cards if c.box == b) for b in range(6)]
    rated = [x for x in rows if x.get('conf')]
    h = [x for x in rated if x['conf'] == 'H']
    g = [x for x in rated if x['conf'] == 'G']
    honest = len(rated) >= 30 and h and (not g or (sum(1 for x in h if x['right']) / len(h)) > (sum(1 for x in g if x['right']) / len(g)))
    earned = {'first': bool(res), 'streak3': best >= 3, 'streak7': best >= 7, 'hundred': len(rows) >= 100, 'both': all(secs[s]['n'] >= 10 for s in SEC),
              'mock': any(r.mock == 'M-FULL' for r in res), 'spr': sum(1 for x in rows if x.get('spr')) >= 10, 'comeback': any(c.box >= 3 for c in cards), 'honest': bool(honest)}
    mocks = [{'date': r.finished_at.strftime('%d %b'), 'score': r.score, 'max': r.max_score, 'pct': round(100 * r.score / r.max_score) if r.max_score else 0, 'title': r.title}
             for r in reversed(res) if r.mock.startswith('M-')][-10:]
    return {'attempts': len(res), 'answers': len(rows), 'secs': secs, 'doms': doms, 'streak': streak, 'best_streak': best, 'cards': len(cards), 'boxes': boxes,
            'due': sum(1 for c in cards if c.due and c.due <= today), 'badges': [{'id': i, 'name': n, 'desc': dsc, 'got': earned[i]} for i, n, dsc in BADGES], 'mocks': mocks, 'recent': res[:8]}
