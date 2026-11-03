"""EduPulse-NIFT: mock tests, previous-year practice and spaced reinforcement for the NIFT General Ability Test (GAT) and Creative Ability Test (CAT).

* Bank (app/data/nift/bank.json): questions from NIFT's previous GAT papers (2016 to 2023) that can be shown as plain text, each with the answer from the paper's key, cross-checked by an
  independent solve, and a short explanation we wrote. Questions that need a figure, or whose key we could not confirm, are left out. The 2024 and 2025 papers are used for the format
  analysis only (their questions are pictures).
* Maths and reasoning also come from generators (explorer_gen): computed answers, new numbers every attempt, at the level of the NIFT quantitative and analytical sections.
* Tests: GAT mocks per programme (the section mix of the 2025 papers), previous-year papers, section sets, and the Daily Review. The CAT / studio tasks are practised on paper and
  marked by the student against a rubric (a computer cannot mark a drawing).
* Marking follows the papers: +1 for a right answer, -0.25 for a wrong one, nothing for a blank. Marks are worked out on the server; the key never goes to the browser before submission.
* Reinforcement: every wrong answer, and every right answer rated Guess or Low, becomes a card in Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days). The Daily Review serves due cards
  (generated ideas return with new numbers) and tops up with the weakest sections.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models_pulse import PulseNiftCard, PulseNiftResult, PulseNiftStudio
from app.services import explorer_gen as gen

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'nift')
SEC = {'QA': 'Quantitative ability', 'ENG': 'Communication ability (English)', 'CMP': 'English comprehension', 'ANA': 'Analytical and logical ability', 'GK': 'General knowledge and current affairs'}
SEC_SHORT = {'QA': 'Quantitative', 'ENG': 'English', 'CMP': 'Comprehension', 'ANA': 'Analytical', 'GK': 'GK and CA'}
SEC_BLURB = {'QA': 'Percentages, ratio, profit and loss, time and work, speed, averages, interest, algebra and data: school maths at speed.',
             'ENG': 'Synonyms and antonyms, spelling, grammar and error spotting, idioms, one-word substitution, sentence correction.',
             'CMP': 'Passages followed by questions on meaning, inference, tone and vocabulary in context.',
             'ANA': 'Series, coding, blood relations, directions, ranking, seating, syllogisms, clocks and calendars.',
             'GK': 'Static general knowledge, current affairs, awards, books, sports, fashion, textiles, art and design awareness.'}
PROGS = {'BDES': 'B.Des', 'BFTECH': 'B.F.Tech', 'MDES': 'M.Des', 'MFM': 'M.F.M', 'MFTECH': 'M.F.Tech'}
PROG_LONG = {'BDES': 'Bachelor of Design', 'BFTECH': 'Bachelor of Fashion Technology', 'MDES': 'Master of Design', 'MFM': 'Master of Fashion Management', 'MFTECH': 'Master of Fashion Technology'}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
WRONG = 0.25
MAX_BODY = 400_000
MAX_Q = 160
MIN_RATED = 10
MIN_PER_Q = 1.2
INTERVALS = [0, 1, 3, 7, 14, 30]
DAILY_N = 10
SET_N = 15

# GAT mock recipes: sections and number of questions. Programme patterns follow the 2025 papers (case-study parts are written answers and are not in these mocks).
MOCKS = {
    'BDES': ('GAT mock, B.Des', [('ENG', 25), ('CMP', 15), ('QA', 20), ('ANA', 15), ('GK', 25)], 'The B.Des GAT: 100 questions in 120 minutes.'),
    'BFTECH': ('GAT mock, B.F.Tech Part A', [('ENG', 25), ('CMP', 15), ('QA', 20), ('ANA', 15), ('GK', 25)], 'Part A of the B.F.Tech GAT: the same four sections as B.Des.'),
    'BFTECH-B': ('GAT mock, B.F.Tech Part B (objective)', [('QA', 15), ('ANA', 15)], 'Part B quantitative and analytical questions. The case study (written) is not included.'),
    'MDES': ('GAT mock, M.Des', [('ENG', 30), ('CMP', 20), ('QA', 20), ('ANA', 25), ('GK', 25)], 'The M.Des GAT section mix, 120 questions.'),
    'MFM': ('GAT mock, M.F.M', [('ENG', 30), ('CMP', 20), ('QA', 20), ('ANA', 25), ('GK', 25)], 'M.F.M GAT objective sections. The written case study is not included.'),
    'MFTECH': ('GAT mock, M.F.Tech', [('ENG', 27), ('CMP', 18), ('QA', 30), ('ANA', 25), ('GK', 25)], 'M.F.Tech GAT objective sections. The written case study is not included.'),
}
GEN_FOR = {'QA': ['pcchg', 'ratio', 'speed', 'avg', 'lin2', 'consec', 'prob', 'ci', 'unit'], 'ANA': ['series', 'code', 'cal', 'rank', 'odd', 'walk', 'syl', 'clock']}
GEN_SHARE = {'QA': 0.45, 'ANA': 0.4}
YEAR_MIN = 25                       # a previous-year paper is offered when at least this many of its questions can be shown

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


def studio():
    if 'st' not in _cache:
        _cache['st'] = _read('studio.json')
    return _cache['st']


def analysis():
    if 'an' not in _cache:
        _cache['an'] = _read('analysis.json')
    return _cache['an']


def get(qid):
    bank()
    if qid in _cache['by_id']:
        return _cache['by_id'][qid]
    if isinstance(qid, str) and qid.startswith('g:'):
        q = gen.from_id(qid)
        if q:
            q = dict(q)
            q['sec'] = 'QA' if q['sec'] == 'MAT' else 'ANA'
        return q
    return None


def key_of(qid):
    return 'g:' + qid.split(':')[1] if qid.startswith('g:') else qid


def source_label(q):
    src = q.get('src')
    if isinstance(src, list) and src:
        return ', '.join('NIFT %s %s Q%s' % (y, PROGS.get(p, p), n) for y, p, n in src[:2])
    return 'EduAakashaA practice question (generated)'


def view(q):
    d = {'id': q['id'], 'sec': q['sec'], 'secname': SEC[q['sec']], 'text': q['q'], 'options': [{'t': o} for o in q['opts']]}
    if q.get('ctx'):
        d['passage'] = q['ctx']
    return d


# ---- composition -------------------------------------------------------------------------------------------------------------------------
def recent_ids(uid, k=4):
    seen = set()
    if not uid:
        return seen
    for r in PulseNiftResult.query.filter_by(user_id=uid).order_by(PulseNiftResult.finished_at.desc()).limit(k).all():
        for x in json.loads(r.payload_json or '[]'):
            seen.add(x['qid'])
    return seen


def _pick(sec, n, rng, used, avoid, with_gen=True):
    """n question ids for a section: bank questions (fresh ones first; comprehension in passage groups) plus generated ones for QA and ANA."""
    out = []
    n_gen = int(round(n * GEN_SHARE.get(sec, 0))) if with_gen and sec in GEN_FOR else 0
    gens = list(GEN_FOR.get(sec, []))
    rng.shuffle(gens)
    for k in range(n_gen):
        out.append('g:%s:%d' % (gens[k % len(gens)], rng.randint(1, 10 ** 6)))
    pool = [q for q in bank() if q['sec'] == sec and q['id'] not in used]
    rng.shuffle(pool)
    pool.sort(key=lambda q: q['id'] in avoid)
    if sec == 'CMP':
        groups = {}
        for q in pool:
            groups.setdefault(q.get('ctx', '')[:80], []).append(q)
        for g in sorted(groups.values(), key=lambda g: (any(q['id'] in avoid for q in g), rng.random())):
            for q in sorted(g, key=lambda q: q['id']):
                if len(out) >= n:
                    break
                out.append(q['id'])
                used.add(q['id'])
            if len(out) >= n:
                break
    else:
        for q in pool:
            if len(out) >= n:
                break
            out.append(q['id'])
            used.add(q['id'])
    k = 0
    while len(out) < n and gens:
        out.append('g:%s:%d' % (gens[k % len(gens)], rng.randint(1, 10 ** 6)))
        k += 1
    return out


def year_papers():
    """Previous-year papers with enough text questions: [{id, year, prog, n}] newest first."""
    if 'years' not in _cache:
        cnt = {}
        for q in bank():
            for y, p, n in q.get('src', []):
                cnt[(y, p)] = cnt.get((y, p), 0) + 1
        out = [{'id': 'Y-%d-%s' % (y, next(k for k, v in PROGS.items() if v == p)), 'year': y, 'prog': p, 'n': c} for (y, p), c in cnt.items() if c >= YEAR_MIN]
        out.sort(key=lambda r: (-r['year'], r['prog']))
        _cache['years'] = out
    return _cache['years']


def catalogue():
    out = []
    for pid, (title, spec, note) in MOCKS.items():
        n = sum(c for _, c in spec)
        out.append({'id': 'M-' + pid, 'title': title, 'kind': 'mock', 'prog': pid.split('-')[0], 'count': n, 'minutes': int(round(n * MIN_PER_Q)), 'note': note})
    for sec in SEC:
        out.append({'id': 'S-' + sec, 'title': SEC_SHORT[sec] + ' set', 'kind': 'set', 'sec': sec, 'count': SET_N, 'minutes': int(round(SET_N * MIN_PER_Q)), 'note': SEC_BLURB[sec]})
    for y in year_papers():
        out.append({'id': y['id'], 'title': 'NIFT %d %s GAT: questions that can be shown as text' % (y['year'], y['prog']), 'kind': 'year', 'year': y['year'], 'prog': y['prog'], 'count': y['n'],
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
        mine = [q for q in bank() if any(y == t['year'] and p == t['prog'] for y, p, _ in q.get('src', []))]
        mine.sort(key=lambda q: next(n for y, p, n in q['src'] if y == t['year'] and p == t['prog']))
        qids = [q['id'] for q in mine]
    return {**t, 'qids': qids, 'minutes': int(round(len(qids) * MIN_PER_Q))}


# ---- cards and Daily Review ---------------------------------------------------------------------------------------------------------------
def due_cards(uid, today=None):
    today = today or date.today()
    return PulseNiftCard.query.filter(PulseNiftCard.user_id == uid, PulseNiftCard.due <= today).order_by(PulseNiftCard.box, PulseNiftCard.due).all()


def daily(uid, today=None):
    today = today or date.today()
    n_done = PulseNiftResult.query.filter_by(user_id=uid, mock='DAILY').filter(PulseNiftResult.finished_at >= datetime.combine(today, datetime.min.time())).count()
    rng = random.Random('%s-daily-%s-%d' % (uid, today.isoformat(), n_done))
    qids, used = [], set()
    for c in due_cards(uid, today)[:6]:
        if c.qkey.startswith('g:'):
            qids.append('%s:%d' % (c.qkey, rng.randint(1, 10 ** 6)))
        elif get(c.qkey):
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
    """Mark {qids: [...], answers: {qid: {a, c, sec}}}: +1 right, -0.25 wrong, 0 blank. Returns (rows, error)."""
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
    return round(r - WRONG * w, 2)


def _update_cards(uid, rows, daily_run, today):
    tomorrow = today + timedelta(days=1)
    now = datetime.utcnow()
    for r in rows:
        if r['chosen'] is None:
            continue
        key = key_of(r['qid'])
        c = PulseNiftCard.query.filter_by(user_id=uid, qkey=key).first()
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
                c = PulseNiftCard(user_id=uid, qkey=key, sec=r['sec'], topic=r['topic'], box=0, seen=0, right_run=0, created_at=now)
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
    res = PulseNiftResult(user_id=uid, mock=t['id'], title=t['title'], prog=t.get('prog'), score=marks_of(rows), max_score=len(rows), right=right, wrong=len(att) - right,
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
            tl = (x.get('topic') or 'Other') if x['qid'].startswith('g:') else (x.get('topic') or 'Other')
            tv = topics.setdefault(tl, {'n': 0, 'right': 0, 'sec': x['sec']})
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
            rows.append({'sec': s, 'name': SEC.get(s, s), **v, 'wrong': v['n'] - v['right'], 'net': round(v['right'] - WRONG * (v['n'] - v['right']), 2), 'acc': acc,
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
        notes.append('Each wrong answer cost %s mark, so %d wrong answers took away %s marks. Answer when you can remove at least two options; leave the rest.' % (WRONG, wrong_n, round(WRONG * wrong_n, 2)))
    if blank and att and blank > att * 0.35:
        notes.append('%d question(s) were left blank. If many of them were GK or vocabulary, a daily review of missed words and facts is the quickest gain.' % blank)
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
    q = PulseNiftResult.query.filter_by(user_id=uid).order_by(PulseNiftResult.finished_at.desc())
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
    ('allsec', 'All five sections', 'Answer at least 10 questions in every GAT section.'),
    ('mock', 'Full mock', 'Finish a full GAT mock.'),
    ('comeback', 'Comeback', 'Bring a review card up to box 3 or higher.'),
    ('studio', 'Studio habit', 'Mark 3 CAT / studio tasks.'),
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
    cards = PulseNiftCard.query.filter_by(user_id=uid).all()
    boxes = [sum(1 for c in cards if c.box == b) for b in range(6)]
    st = PulseNiftStudio.query.filter_by(user_id=uid).count()
    rated = [x for x in rows if x.get('conf')]
    h = [x for x in rated if x['conf'] == 'H']
    g = [x for x in rated if x['conf'] == 'G']
    honest = len(rated) >= 30 and h and (not g or (sum(1 for x in h if x['right']) / len(h)) > (sum(1 for x in g if x['right']) / len(g)))
    earned = {'first': bool(res), 'streak3': best >= 3, 'streak7': best >= 7, 'hundred': len(rows) >= 100, 'allsec': all(secs[s]['n'] >= 10 for s in SEC),
              'mock': any(r.mock.startswith('M-') for r in res), 'comeback': any(c.box >= 3 for c in cards), 'studio': st >= 3, 'honest': bool(honest)}
    mocks = [{'date': r.finished_at.strftime('%d %b'), 'score': r.score, 'max': r.max_score, 'pct': round(100 * r.score / r.max_score) if r.max_score else 0, 'title': r.title}
             for r in reversed(res) if r.mock.startswith(('M-', 'Y-'))][-10:]
    return {'attempts': len(res), 'answers': len(rows), 'secs': secs, 'weak_topics': weak_topics, 'streak': streak, 'best_streak': best, 'cards': len(cards), 'boxes': boxes,
            'due': sum(1 for c in cards if c.due and c.due <= today), 'badges': [{'id': i, 'name': n, 'desc': dsc, 'got': earned[i]} for i, n, dsc in BADGES], 'mocks': mocks,
            'studio': st, 'recent': res[:8]}


# ---- studio ------------------------------------------------------------------------------------------------------------------------------
def save_studio(uid, tid, scores, note):
    t = next((x for x in studio() if x['id'] == tid), None)
    if not t or not isinstance(scores, list) or len(scores) != len(t['rubric']):
        return None
    vals = []
    for s, r in zip(scores, t['rubric']):
        if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= r['max']:
            return None
        vals.append(s)
    row = PulseNiftStudio.query.filter_by(user_id=uid, tid=tid).first() or PulseNiftStudio(user_id=uid, tid=tid)
    row.scores_json = json.dumps(vals)
    row.total = sum(vals)
    row.note = (note or '')[:400]
    row.done_at = datetime.utcnow()
    db.session.add(row)
    db.session.commit()
    return row
