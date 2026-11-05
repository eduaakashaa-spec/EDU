"""EduPulse-Olympiad: practice tests and spaced reinforcement for the Indian Olympiads (Mathematics, Physics, Chemistry, Biology, Junior Science).

* Bank (app/data/olympiad/bank.json): questions that can be shown as plain text and have one checkable answer. Two kinds of source:
    - Official questions from HBCSE and Mathematical Association of India papers (IOQM and PRMO integer-answer questions; INBO Section A and INJSO multiple-choice questions). Each answer is the one
      in the organisers' published key for that paper; a question is kept only when an independent solve agreed with the key. Explanations are written by EduAakashaA with AI assistance.
    - Original EduAakashaA questions (Physics and Chemistry, in the style of the stage-1 multiple-choice papers), kept only when an independent blind solve agreed with the intended answer.
  Long-answer problems (RMO, INMO, INPhO, INChO, INAO and the other stage-2 papers) cannot be marked automatically and are not in the bank.
* Tests: a full mock per subject (30 questions), official-paper practice (the usable questions of one paper, in paper order), subject sets and the Daily Review.
* Marking: multiple choice +3 for a right answer and -1 for a wrong one (as in Part A of the NSE papers and in INBO Section A and INJSO Section I); integer-answer (Mathematics) +3 and no negative marking (as in IOQM and
  PRMO Part A, which carry no negative marks). Marks are worked out on the server; the key never goes to the browser before submission. These are practice rules, not the marking of any particular year.
* Reinforcement: every wrong answer, and every right answer rated Guess or Low, becomes a card in Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days). The Daily Review serves due cards and tops up with the
  weakest subjects.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models_pulse import PulseOlyCard, PulseOlyResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'olympiad')
SEC = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry', 'BIO': 'Biology', 'JS': 'Junior Science'}
SEC_BLURB = {'MATH': 'Number theory, algebra, combinatorics and geometry with integer answers (00 to 99), in the style of IOQM and PRMO Part A.',
             'PHY': 'Mechanics, waves and heat, electricity and magnetism, optics and modern physics.',
             'CHEM': 'Physical, inorganic and organic chemistry at stage-1 level.',
             'BIO': 'Cell biology, plant and animal physiology, genetics, ecology and evolution: INBO Section A style.',
             'JS': 'Physics, chemistry, biology and mathematics for Classes 9 and 10: INJSO style.'}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
RIGHT_MARKS = 3
WRONG_MCQ = 1
MAX_BODY = 300_000
MAX_Q = 120
MIN_RATED = 10
INTERVALS = [0, 1, 3, 7, 14, 30]
DAILY_N = 10
SET_N = 15
MOCK_N = 30
PAPER_MIN = 10                       # an official paper is offered when at least this many of its questions can be shown
MIN_PER_Q = {'MATH': 6.0, 'PHY': 2.0, 'CHEM': 2.0, 'BIO': 2.0, 'JS': 2.0}   # IOQM allows 3 hours for 30 questions; the NSE gives 2 hours for 60 (2 minutes a question)

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


def get(qid):
    bank()
    return _cache['by_id'].get(qid)


def secs_available():
    """Subjects that have at least a set's worth of questions, in display order."""
    return [s for s in SEC if sum(1 for q in bank() if q['sec'] == s) >= SET_N]


def source_label(q):
    src = q.get('src')
    return '%s %s Q%s' % (src[0], src[1], src[2]) if src else 'EduAakashaA original question'


def view(q):
    base = {'id': q['id'], 'sec': q['sec'], 'secname': SEC[q['sec']], 'domain': q.get('topic', ''), 'text': q['q'], 'passage': ''}
    if q['kind'] == 'int':
        return {**base, 'spr': True, 'options': []}
    return {**base, 'spr': False, 'options': [{'t': o} for o in q['opts']]}


def minutes_for(qids):
    m = 0.0
    for i in qids:
        q = get(i)
        m += MIN_PER_Q[q['sec']] if q else 2.0
    return int(round(m))


# ---- composition -------------------------------------------------------------------------------------------------------------------------
def recent_ids(uid, k=4):
    seen = set()
    if not uid:
        return seen
    for r in PulseOlyResult.query.filter_by(user_id=uid).order_by(PulseOlyResult.finished_at.desc()).limit(k).all():
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


def official_papers():
    """Official papers with enough usable questions: [{id, exam, year, n, sec}] newest first."""
    if 'papers' not in _cache:
        cnt = {}
        for q in bank():
            s = q.get('src')
            if s:
                k = (s[0], s[1])
                cnt.setdefault(k, {'n': 0, 'sec': q['sec']})['n'] += 1
        out = [{'id': 'P-%s-%s' % k, 'exam': k[0], 'year': k[1], 'n': v['n'], 'sec': v['sec']} for k, v in cnt.items() if v['n'] >= PAPER_MIN]
        out.sort(key=lambda r: (-int(r['year']), r['exam']))
        _cache['papers'] = out
    return _cache['papers']


def catalogue():
    out = []
    for sec in secs_available():
        n = min(MOCK_N, sum(1 for q in bank() if q['sec'] == sec))
        out.append({'id': 'M-' + sec, 'title': SEC[sec] + ' full mock', 'kind': 'mock', 'sec': sec, 'count': n, 'minutes': int(round(n * MIN_PER_Q[sec])), 'note': SEC_BLURB[sec]})
    for sec in secs_available():
        out.append({'id': 'S-' + sec, 'title': SEC[sec] + ' set', 'kind': 'set', 'sec': sec, 'count': SET_N, 'minutes': int(round(SET_N * MIN_PER_Q[sec])), 'note': '%d questions on mixed topics.' % SET_N})
    for p in official_papers():
        out.append({'id': p['id'], 'title': '%s %s: usable questions' % (p['exam'], p['year']), 'kind': 'paper', 'sec': p['sec'], 'exam': p['exam'], 'year': p['year'], 'count': p['n'],
                    'minutes': int(round(p['n'] * MIN_PER_Q[p['sec']])), 'note': 'Questions from the %s %s paper, in paper order.' % (p['exam'], p['year'])})
    return out


def compose(tid, uid, attempt):
    t = next((x for x in catalogue() if x['id'] == tid), None)
    if not t:
        return None
    rng = random.Random('%s-%s-%s' % (uid, tid, attempt))
    used = set()
    avoid = recent_ids(uid)
    if t['kind'] in ('mock', 'set'):
        qids = _pick(t['sec'], t['count'], rng, used, avoid)
    else:
        mine = [q for q in bank() if q.get('src') and q['src'][0] == t['exam'] and str(q['src'][1]) == str(t['year'])]
        mine.sort(key=lambda q: q['src'][2])
        qids = [q['id'] for q in mine]
    return {**t, 'qids': qids, 'minutes': minutes_for(qids)}


# ---- cards and Daily Review --------------------------------------------------------------------------------------------------------------
def due_cards(uid, today=None):
    today = today or date.today()
    return PulseOlyCard.query.filter(PulseOlyCard.user_id == uid, PulseOlyCard.due <= today).order_by(PulseOlyCard.box, PulseOlyCard.due).all()


def daily(uid, today=None):
    today = today or date.today()
    n_done = PulseOlyResult.query.filter_by(user_id=uid, mock='DAILY').filter(PulseOlyResult.finished_at >= datetime.combine(today, datetime.min.time())).count()
    rng = random.Random('%s-daily-%s-%d' % (uid, today.isoformat(), n_done))
    qids, used = [], set()
    for c in due_cards(uid, today)[:6]:
        if get(c.qkey):
            qids.append(c.qkey)
            used.add(c.qkey)
    n_cards = len(qids)
    avoid = recent_ids(uid)
    secs = tracker(uid)['secs']
    order = [s for s, _ in sorted(((s, v['acc'] if v['acc'] is not None else -1) for s, v in secs.items() if s in secs_available()), key=lambda x: x[1])]
    k = 0
    while len(qids) < DAILY_N and k < 60 and order:
        sec = order[k % len(order)]
        k += 1
        qids += [q for q in _pick(sec, 1, rng, used, avoid) if q not in qids]
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


def _as_int(text):
    t = str(text).strip().replace(' ', '')
    if not t or len(t) > 6 or not t.lstrip('+-').isdigit():
        return None
    return int(t)


def grade_paper(d):
    """Mark {qids: [...], answers: {qid: {a, c, sec}}}. a is the option index (0-3) or, for an integer-answer question, the typed number."""
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
        if q['kind'] == 'int':
            v = _as_int(ch) if isinstance(ch, (str, int)) and not isinstance(ch, bool) else None
            ch = str(v) if v is not None else None
            right = v is not None and v == int(q['ans'])
        else:
            ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
            right = ch is not None and ch == q['ans']
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        rows.append({'qid': qid, 'sec': q['sec'], 'dom': SEC[q['sec']], 'topic': q.get('topic', ''), 'kind': q['kind'], 'chosen': ch, 'right': bool(right),
                     'conf': cf if ch is not None else None, 'secs': _num(a.get('sec'), 0, 3600)})
    return rows, None


def marks_of(rows):
    total = 0
    for x in rows:
        if x['right']:
            total += RIGHT_MARKS
        elif x['chosen'] is not None and x['kind'] == 'mcq':
            total -= WRONG_MCQ
    return total


def _update_cards(uid, rows, daily_run, today):
    tomorrow = today + timedelta(days=1)
    now = datetime.utcnow()
    for r in rows:
        if r['chosen'] is None:
            continue
        c = PulseOlyCard.query.filter_by(user_id=uid, qkey=r['qid']).first()
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
                c = PulseOlyCard(user_id=uid, qkey=r['qid'], sec=r['sec'], topic=r['topic'], box=0, seen=0, right_run=0, created_at=now)
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
    res = PulseOlyResult(user_id=uid, mock=t['id'], title=t['title'], score=marks_of(rows), max_score=RIGHT_MARKS * len(rows), right=right, wrong=len(att) - right,
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
    sc = {s: {'n': 0, 'right': 0, 'blank': 0, 'secs': 0, 'mcq_wrong': 0} for s in SEC}
    topics = {}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = sc.setdefault(x['sec'], {'n': 0, 'right': 0, 'blank': 0, 'secs': 0, 'mcq_wrong': 0})
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            s['right'] += 1 if x['right'] else 0
            s['secs'] += x.get('secs', 0)
            if not x['right'] and x.get('kind') == 'mcq':
                s['mcq_wrong'] += 1
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
            rows.append({'sec': s, 'name': SEC.get(s, s), **v, 'wrong': v['n'] - v['right'], 'net': RIGHT_MARKS * v['right'] - WRONG_MCQ * v['mcq_wrong'], 'acc': acc,
                         'avg_secs': round(v['secs'] / v['n']) if v['n'] else None, 'level': level(acc, v['n'])})
    rows.sort(key=lambda r: (r['acc'] if r['acc'] is not None else 101))
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    att = sum(v['n'] for v in sc.values())
    right = sum(v['right'] for v in sc.values())
    blank = sum(v['blank'] for v in sc.values())
    wrong_n = att - right
    mcq_wrong = sum(v['mcq_wrong'] for v in sc.values())
    weak_topics = sorted([{'topic': k, **v, 'acc': round(100 * v['right'] / v['n'])} for k, v in topics.items() if v['n'] >= 2 and v['right'] < v['n']], key=lambda r: (r['acc'], -r['n']))[:6]
    notes = []
    if mcq_wrong:
        notes.append('Each wrong multiple-choice answer cost %d mark, so %d wrong choices took away %d marks and the %d they could have earned. Answer a multiple-choice question when you can remove at least two options.'
                     % (WRONG_MCQ, mcq_wrong, WRONG_MCQ * mcq_wrong, RIGHT_MARKS * mcq_wrong))
    if blank and att and blank > att * 0.35:
        notes.append('%d question(s) were left blank. Check whether they cluster in one subject or topic.' % blank)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer next time.')
    else:
        if pat['P4']:
            notes.append('%d answer(s) were wrong although you rated them High: a misunderstanding rather than a slip. They are now in your review cards.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answer(s) were right but rated Guess or Low: the idea is not secure yet, so they are in your review cards too.' % pat['P2'])
    return {'right': right, 'wrong': wrong_n, 'blank': blank, 'attempted': att, 'acc': round(100 * right / att) if att else None, 'rated': rated, 'pat': pat, 'conf': conf, 'secs': rows,
            'weak_topics': weak_topics, 'notes': notes, 'weak': [r for r in rows if r['level'] in ('Starting', 'Growing')][:3], 'strong': [r for r in reversed(rows) if r['level'] == 'Strong'][:3]}


def for_user(uid, limit=None):
    q = PulseOlyResult.query.filter_by(user_id=uid).order_by(PulseOlyResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def review(result):
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = get(x['qid'])
        if not q:
            continue
        out.append({**x, 'view': view(q), 'ans': q['ans'] if q['kind'] == 'mcq' else None, 'ans_text': str(int(q['ans'])) if q['kind'] == 'int' else None,
                    'why': q.get('why', ''), 'secname': SEC[q['sec']], 'source': source_label(q)})
    return out


# ---- tracker -----------------------------------------------------------------------------------------------------------------------------
BADGES = [
    ('first', 'First paper', 'Finish your first test.'),
    ('streak3', 'Three-day streak', 'Practise on three days in a row.'),
    ('streak7', 'Seven-day streak', 'Practise on seven days in a row.'),
    ('hundred', 'Hundred answers', 'Answer 100 questions.'),
    ('allsec', 'All subjects', 'Answer at least 10 questions in every subject.'),
    ('mock', 'Full mock', 'Finish a full subject mock.'),
    ('paper', 'Real paper', 'Finish an official-paper practice test.'),
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
    for i, dy in enumerate(days):
        run = run + 1 if i and (dy - days[i - 1]).days == 1 else 1
        best = max(best, run)
    cards = PulseOlyCard.query.filter_by(user_id=uid).all()
    boxes = [sum(1 for c in cards if c.box == b) for b in range(6)]
    rated = [x for x in rows if x.get('conf')]
    h = [x for x in rated if x['conf'] == 'H']
    g = [x for x in rated if x['conf'] == 'G']
    honest = len(rated) >= 30 and h and (not g or (sum(1 for x in h if x['right']) / len(h)) > (sum(1 for x in g if x['right']) / len(g)))
    earned = {'first': bool(res), 'streak3': best >= 3, 'streak7': best >= 7, 'hundred': len(rows) >= 100, 'allsec': all(secs[s]['n'] >= 10 for s in SEC),
              'mock': any(r.mock.startswith('M-') for r in res), 'paper': any(r.mock.startswith('P-') for r in res), 'comeback': any(c.box >= 3 for c in cards), 'honest': bool(honest)}
    mocks = [{'date': r.finished_at.strftime('%d %b'), 'score': r.score, 'max': r.max_score, 'pct': round(100 * r.score / r.max_score) if r.max_score else 0, 'title': r.title}
             for r in reversed(res) if r.mock.startswith(('M-', 'P-'))][-10:]
    return {'attempts': len(res), 'answers': len(rows), 'secs': secs, 'weak_topics': weak_topics, 'streak': streak, 'best_streak': best, 'cards': len(cards), 'boxes': boxes,
            'due': sum(1 for c in cards if c.due and c.due <= today), 'badges': [{'id': i, 'name': n, 'desc': dsc, 'got': earned[i]} for i, n, dsc in BADGES], 'mocks': mocks, 'recent': res[:8]}
