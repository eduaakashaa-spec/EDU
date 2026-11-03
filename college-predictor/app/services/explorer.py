"""EduPulse-Explorer: a discovery and practice centre for Grades 7 to 10 (engineering and design interests).

* Purpose: meet the kinds of questions later exams ask (JEE, UCEED / NID / NIFT, NATA and JEE Paper 2, IISER IAT and olympiads, general aptitude) at school level, find where a
  student is strong, and reinforce the rest by spaced practice.
* Content (app/data/explorer/bank.json + explorer_gen.py): original authored questions (re-solved independently), visual and spatial questions built by code, and maths and
  reasoning questions generated with computed answers (new numbers every time). Creative challenges are done at home and marked against a rubric.
* Tests are composed per student and attempt; the server marks the submitted question ids (generated ids carry their seed). One point per question, nothing deducted.
* Reinforcement: every wrong answer, and every right answer rated Guess or Low, becomes a card in Leitner boxes 0 to 5 (intervals 0, 1, 3, 7, 14, 30 days). The Daily 10 serves due cards
  (generated ideas return with new numbers) and tops up with the weakest skills. Mastery per skill is the accuracy of the last 20 answers.
* It is exploration, not selection: scores are practice guidance, not a prediction of any entrance result.
Confidence codes: G guess, L low, M medium, H high.
"""
import json
import os
import random
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models_pulse import PulseExpCard, PulseExpCreative, PulseExpProfile, PulseExpResult
from app.services import explorer_gen as gen

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'explorer')
SKILLS = {'MAT': 'Maths reasoning', 'SCI': 'Science sense', 'ENG': 'Engineering thinking', 'LOG': 'Logic and patterns', 'SPA': 'Spatial and visual', 'DES': 'Design sense', 'LAN': 'Language and reading'}
SKILL_BLURB = {'MAT': 'Number sense, ratio, equations, geometry and chance, the way JEE-foundation and olympiad papers ask them.',
               'SCI': 'Physics, chemistry, biology and earth science explained through everyday situations.',
               'ENG': 'How things work: levers, gears, structures, circuits, energy, computing and making.',
               'LOG': 'Series, codes, directions, ordering and deduction: the core of every aptitude section.',
               'SPA': 'Mirror images, rotations, folding, cubes and views: the heart of UCEED, NID and NATA.',
               'DES': 'Colour, form, products, materials, crafts, users and spaces: design literacy.',
               'LAN': 'Reading passages and word sense, as in design-entrance language sections.'}
FAMILIES = {'JEE': ('JEE style', 'Engineering entrance (JEE Main and Advanced): concept plus a short calculation or reasoning.'),
            'UCD': ('UCEED, NID and NIFT style', 'Design entrances: visual, spatial and design-awareness questions, plus drawing and idea tasks.'),
            'NAT': ('NATA and JEE Paper 2 style', 'Architecture entrances: spatial sense, 3D thinking, geometry and observation.'),
            'IAT': ('IISER IAT and olympiad style', 'Science-reasoning questions that ask you to explain or predict.'),
            'APT': ('General aptitude style', 'Reasoning and verbal sections common to many entrance tests.')}
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
LETTERS = 'ABCD'
MAX_BODY = 250_000
MIN_RATED = 8
MIN_PER_Q = 1.3
INTERVALS = [0, 1, 3, 7, 14, 30]
DAILY_N = 10
MAX_Q = 60

GEN_BY_BAND = {
    '7-8': {'MAT': ['pcchg', 'ratio', 'speed', 'avg', 'area', 'lin', 'unit'], 'LOG': ['series', 'code', 'cal', 'rank', 'odd']},
    '9-10': {'MAT': ['lin2', 'consec', 'poly', 'prob', 'ci', 'pcchg', 'speed'], 'LOG': ['walk', 'syl', 'clock', 'series', 'code']},
}
GEN_SHARE = {'MAT': 0.8, 'LOG': 0.55}

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


def creative():
    if 'cr' not in _cache:
        _cache['cr'] = _read('creative.json')
    return _cache['cr']


def band_of(grade):
    return '9-10' if grade and int(grade) >= 9 else '7-8'


def get(qid):
    """A question by id: a bank id, or a generated id g:<generator>:<seed>."""
    bank()
    if qid in _cache['by_id']:
        return _cache['by_id'][qid]
    if isinstance(qid, str) and qid.startswith('g:'):
        return gen.from_id(qid)
    return None


def key_of(qid):
    """The reinforcement key: a generated question returns as a new variant of the same idea."""
    return 'g:' + qid.split(':')[1] if qid.startswith('g:') else qid


def view(q):
    """A question as the browser sees it: no answer, no explanation."""
    opts = [({'svg': o['svg']} if isinstance(o, dict) and o.get('svg') else {'t': o['t'] if isinstance(o, dict) else o}) for o in q['opts']]
    d = {'id': q['id'], 'sec': q['sec'] if 'sec' in q else q['skill'], 'secname': SKILLS[q.get('skill') or q['sec']], 'marks': 1, 'text': q['q'], 'options': opts}
    if q.get('svg'):
        d['svg'] = q['svg']
    if q.get('passage'):
        d['passage'] = q['passage']
    return d


def _norm(q):
    """Generated questions use `sec` for the skill; bank questions use `skill`."""
    if 'skill' not in q:
        q['skill'] = q['sec']
    return q


# ---- composition -------------------------------------------------------------------------------------------------------------------------
def _pool(skill, band, fam=None):
    p = [q for q in bank() if q['skill'] == skill and q['grade'] in (band, 'all')]
    if fam:
        f = [q for q in p if fam in q['fam']]
        p = f if len(f) >= 3 else p
    return p


def _pick(skill, n, band, rng, used, fam=None):
    """n question ids for a skill: authored or visual bank questions (nearest to the target difficulty first) plus generated ones for MAT and LOG."""
    out = []
    share = GEN_SHARE.get(skill, 0)
    n_gen = int(round(n * share)) if skill in GEN_BY_BAND[band] else 0
    gens = list(GEN_BY_BAND[band].get(skill, []))
    rng.shuffle(gens)
    for k in range(n_gen):
        g = gens[k % len(gens)]
        out.append('g:%s:%d' % (g, rng.randint(1, 10 ** 6)))
    target = 1.7 if band == '7-8' else 2.3
    pool = [q for q in _pool(skill, band, fam) if q['id'] not in used]
    rng.shuffle(pool)
    pool.sort(key=lambda q: abs(q['diff'] - target) + rng.random() * 1.2)
    groups = set()
    for q in pool:
        if len(out) >= n:
            break
        if q.get('group'):
            if q['group'] in groups:
                continue
            groups.add(q['group'])
        out.append(q['id'])
        used.add(q['id'])
    k = 0
    while len(out) < n and gens:                                       # a thin pool: fill with more generated variants
        out.append('g:%s:%d' % (gens[k % len(gens)], rng.randint(1, 10 ** 6)))
        k += 1
    return out


TASTERS = {
    'X-JEE': ('JEE-style taster', 'JEE', [('MAT', 5), ('SCI', 4), ('ENG', 4), ('LOG', 2)]),
    'X-UCD': ('UCEED, NID and NIFT taster', 'UCD', [('SPA', 6), ('DES', 5), ('LOG', 2), ('LAN', 3)]),
    'X-NAT': ('NATA and JEE Paper 2 taster', 'NAT', [('SPA', 6), ('DES', 3), ('MAT', 3), ('ENG', 2)]),
    'X-IAT': ('IISER IAT and olympiad taster', 'IAT', [('SCI', 6), ('MAT', 4), ('LOG', 3), ('ENG', 2)]),
}


def catalogue(grade):
    """The tests offered to a student of this grade: [{id, title, kind, note, count, minutes}]."""
    band = band_of(grade)
    n_each = 4 if band == '7-8' else 5
    out = [{'id': 'D78' if band == '7-8' else 'D910', 'title': 'Discovery Test, Grades %s' % band.replace('-', ' to '), 'kind': 'discovery', 'count': n_each * len(SKILLS),
            'note': 'Every skill in one test: %d questions each. Start here to get your skill map.' % n_each}]
    for tid, (title, fam, spec) in TASTERS.items():
        out.append({'id': tid, 'title': title, 'kind': 'taster', 'count': sum(n for _, n in spec), 'fam': fam, 'note': FAMILIES[fam][1]})
    for sk, name in SKILLS.items():
        out.append({'id': 'K-' + sk, 'title': name + ' set', 'kind': 'skill', 'sec': sk, 'count': 12, 'note': SKILL_BLURB[sk]})
    for t in out:
        t['minutes'] = int(round(t['count'] * MIN_PER_Q))
    return out


def compose(tid, grade, uid, attempt):
    """A fresh paper for this student and attempt: {id, title, qids, minutes, kind}. Daily 10 is composed by daily()."""
    band = band_of(grade)
    t = next((x for x in catalogue(grade) if x['id'] == tid), None)
    if not t:
        return None
    rng = random.Random('%s-%s-%s-%s' % (uid, tid, grade, attempt))
    used, qids = set(), []
    if t['kind'] == 'discovery':
        n = 4 if band == '7-8' else 5
        for sk in SKILLS:
            qids += _pick(sk, n, band, rng, used)
    elif t['kind'] == 'taster':
        _, fam, spec = TASTERS[tid]
        for sk, n in spec:
            qids += _pick(sk, n, band, rng, used, fam)
    else:
        qids = _pick(t['sec'], 12, band, rng, used)
    return {**t, 'qids': qids, 'minutes': int(round(len(qids) * MIN_PER_Q))}


# ---- cards and Daily 10 ------------------------------------------------------------------------------------------------------------------
def due_cards(uid, today=None):
    today = today or date.today()
    return PulseExpCard.query.filter(PulseExpCard.user_id == uid, PulseExpCard.due <= today).order_by(PulseExpCard.box, PulseExpCard.due).all()


def daily(uid, grade, today=None):
    """Today's Daily 10: up to six due cards (generated ideas with new numbers), then new questions from the weakest skills."""
    today = today or date.today()
    band = band_of(grade)
    n_done = PulseExpResult.query.filter_by(user_id=uid, mock='DAILY').filter(PulseExpResult.finished_at >= datetime.combine(today, datetime.min.time())).count()
    rng = random.Random('%s-daily-%s-%d' % (uid, today.isoformat(), n_done))
    qids, used = [], set()
    for c in due_cards(uid, today)[:6]:
        if c.qkey.startswith('g:'):
            qids.append('%s:%d' % (c.qkey, rng.randint(1, 10 ** 6)))
        elif get(c.qkey):
            qids.append(c.qkey)
            used.add(c.qkey)
    n_cards = len(qids)
    order = [s for s, _ in sorted(((s, v['acc'] if v['acc'] is not None else -1) for s, v in tracker(uid)['skills'].items()), key=lambda x: x[1])]
    k = 0
    while len(qids) < DAILY_N:
        sk = order[k % len(order)]
        k += 1
        new = [q for q in _pick(sk, 1, band, rng, used) if q not in qids]
        qids += new
        if k > 60:
            break
    return {'id': 'DAILY', 'title': 'Daily 10', 'kind': 'daily', 'qids': qids[:DAILY_N], 'minutes': int(round(DAILY_N * MIN_PER_Q)), 'cards': n_cards, 'note': '%d review + %d new' % (n_cards, len(qids[:DAILY_N]) - n_cards)}


def paper_for_browser(qids):
    return [view(_norm(get(i))) for i in qids]


# ---- marking -----------------------------------------------------------------------------------------------------------------------------
def _num(v, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return lo


def grade_paper(d):
    """Mark {qids: [...], answers: {qid: {a, c, sec}}}. Returns (rows, error)."""
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
        q = _norm(q)
        a = d['answers'].get(qid) or {}
        ch = a.get('a')
        ch = ch if isinstance(ch, int) and not isinstance(ch, bool) and 0 <= ch <= 3 else None
        cf = a.get('c') if a.get('c') in CONF_LABEL else None
        rows.append({'qid': qid, 'skill': q['skill'], 'topic': q.get('topic', ''), 'fam': q.get('fam', []), 'diff': q.get('diff', 2), 'chosen': ch,
                     'right': ch is not None and ch == q['ans'], 'conf': cf if ch is not None else None, 'secs': _num(a.get('sec'), 0, 3600)})
    return rows, None


def _update_cards(uid, rows, daily_run, today):
    tomorrow = today + timedelta(days=1)
    now = datetime.utcnow()
    for r in rows:
        if r['chosen'] is None:
            continue
        key = key_of(r['qid'])
        c = PulseExpCard.query.filter_by(user_id=uid, qkey=key).first()
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
                c = PulseExpCard(user_id=uid, qkey=key, skill=r['skill'], topic=r['topic'], box=0, seen=0, right_run=0, created_at=now)
                db.session.add(c)
            c.seen = (c.seen or 0) + 1
            if r['right']:                                               # right but unsure: keep it, a short step up
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


def save_result(uid, t, d, grade):
    rows, err = grade_paper(d)
    if err:
        return None, err
    right = sum(1 for r in rows if r['right'])
    att = [r for r in rows if r['chosen'] is not None]
    res = PulseExpResult(user_id=uid, mock=t['id'], title=t['title'], grade=grade, score=right, max_score=len(rows), right=right, wrong=len(att) - right, blank=len(rows) - len(att),
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
    return 'Strong' if acc >= 75 else 'Growing' if acc >= 50 else 'Starting'


def analyse(results):
    """Skill and exam-style picture of one or more attempts, plus confidence patterns."""
    pat = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
    conf = {c: {'n': 0, 'right': 0} for c, _ in CONF}
    sk = {s: {'n': 0, 'right': 0, 'blank': 0} for s in SKILLS}
    fm = {f: {'n': 0, 'right': 0} for f in FAMILIES}
    rated = 0
    for r in results:
        for x in json.loads(r.payload_json or '[]'):
            s = sk.setdefault(x['skill'], {'n': 0, 'right': 0, 'blank': 0})
            if x['chosen'] is None:
                s['blank'] += 1
                continue
            s['n'] += 1
            s['right'] += 1 if x['right'] else 0
            for f in x.get('fam', []):
                if f in fm:
                    fm[f]['n'] += 1
                    fm[f]['right'] += 1 if x['right'] else 0
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
    for s, v in sk.items():
        if v['n'] or v['blank']:
            acc = round(100 * v['right'] / v['n']) if v['n'] else None
            rows.append({'skill': s, 'name': SKILLS.get(s, s), **v, 'acc': acc, 'level': level(acc, v['n'])})
    rows.sort(key=lambda r: (r['acc'] if r['acc'] is not None else 101))
    fams = [{'fam': f, 'name': FAMILIES[f][0], **v, 'acc': round(100 * v['right'] / v['n']) if v['n'] else None} for f, v in fm.items() if v['n']]
    for v in conf.values():
        v['pct'] = round(100 * v['right'] / v['n']) if v['n'] else None
    att = sum(v['n'] for v in sk.values())
    right = sum(v['right'] for v in sk.values())
    blank = sum(v['blank'] for v in sk.values())
    notes = []
    if blank and att:
        notes.append('%d question(s) were left blank. Nothing is deducted here, so try every question: an informed guess teaches you something.' % blank)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to read your pattern. Rate every answer next time.')
    else:
        if pat['P4']:
            notes.append('%d answers were wrong although you rated them High: these point to a wrong method or a mix-up. They are now in your review cards.' % pat['P4'])
        if pat['P2']:
            notes.append('%d answers were right but rated Guess or Low: the idea is not secure yet, so they are in your review cards too.' % pat['P2'])
        if pat['P3']:
            notes.append('%d answers were wrong and rated Guess or Low: you knew where the gaps were. Learn the idea, then try the skill set.' % pat['P3'])
    weak = [r for r in rows if r['level'] in ('Starting', 'Growing') and r['acc'] is not None][:3]
    strong = [r for r in reversed(rows) if r['level'] == 'Strong'][:3]
    return {'right': right, 'wrong': att - right, 'blank': blank, 'attempted': att, 'acc': round(100 * right / att) if att else None, 'rated': rated, 'pat': pat, 'conf': conf,
            'skills': rows, 'fams': fams, 'notes': notes, 'weak': weak, 'strong': strong, 'enough': rated >= MIN_RATED}


def for_user(uid, limit=None):
    q = PulseExpResult.query.filter_by(user_id=uid).order_by(PulseExpResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def review(result):
    out = []
    for x in json.loads(result.payload_json or '[]'):
        q = get(x['qid'])
        if not q:
            continue
        q = _norm(q)
        out.append({**x, 'view': view(q), 'ans': q['ans'], 'why': q.get('why', ''), 'style': q.get('style', ''), 'secname': SKILLS[q['skill']]})
    return out


# ---- tracker -----------------------------------------------------------------------------------------------------------------------------
BADGES = [
    ('first', 'First steps', 'Finish your first test.'),
    ('streak3', 'Three-day streak', 'Practise on three days in a row.'),
    ('streak7', 'Seven-day streak', 'Practise on seven days in a row.'),
    ('hundred', 'Hundred answers', 'Answer 100 questions.'),
    ('allround', 'All-rounder', 'Answer at least 5 questions in every one of the seven skills.'),
    ('honest', 'Honest rater', 'Rate 30 answers with your confidence, with High answers right more often than Guess answers.'),
    ('comeback', 'Comeback', 'Bring a review card up to box 3 or higher.'),
    ('maker', 'Maker', 'Finish 3 creative challenges.'),
    ('goal', 'Weekly goal met', 'Practise on as many days this week as your goal.'),
]


def tracker(uid, today=None):
    today = today or date.today()
    res = for_user(uid)
    rows = []
    for r in reversed(res):                                              # oldest first
        for x in json.loads(r.payload_json or '[]'):
            if x['chosen'] is not None:
                rows.append({**x, 'day': r.finished_at.date()})
    skills = {}
    for s in SKILLS:
        mine = [x for x in rows if x['skill'] == s]
        last = mine[-20:]
        prev = mine[-40:-20]
        acc = round(100 * sum(1 for x in last if x['right']) / len(last)) if last else None
        pacc = round(100 * sum(1 for x in prev if x['right']) / len(prev)) if len(prev) >= 5 else None
        skills[s] = {'name': SKILLS[s], 'n': len(mine), 'acc': acc, 'level': level(acc, len(last)), 'delta': (acc - pacc) if acc is not None and pacc is not None else None}
    fams = {}
    for f in FAMILIES:
        mine = [x for x in rows if f in x.get('fam', [])]
        fams[f] = {'name': FAMILIES[f][0], 'n': len(mine), 'acc': round(100 * sum(1 for x in mine if x['right']) / len(mine)) if mine else None}
    tp = {}
    for x in rows:
        t_ = x.get('topic') or 'Other'
        label = t_ if x['qid'].startswith('g:') else t_.split(':')[0].strip()
        v = tp.setdefault(label or 'Other', {'n': 0, 'right': 0, 'skill': x['skill']})
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
    prof = db.session.get(PulseExpProfile, uid)
    goal = (prof.weekly_goal if prof and prof.weekly_goal else 3)
    week = len([x for x in days if (today - x).days < 7])
    cards = PulseExpCard.query.filter_by(user_id=uid).all()
    boxes = [sum(1 for c in cards if c.box == b) for b in range(6)]
    cr = PulseExpCreative.query.filter_by(user_id=uid).count()
    rated = [x for x in rows if x.get('conf')]
    h = [x for x in rated if x['conf'] == 'H']
    g = [x for x in rated if x['conf'] == 'G']
    honest = len(rated) >= 30 and h and (not g or (sum(1 for x in h if x['right']) / len(h)) > (sum(1 for x in g if x['right']) / len(g)))
    earned = {
        'first': bool(res), 'streak3': best >= 3, 'streak7': best >= 7, 'hundred': len(rows) >= 100,
        'allround': all(skills[s]['n'] >= 5 for s in SKILLS), 'honest': bool(honest), 'comeback': any(c.box >= 3 for c in cards), 'maker': cr >= 3, 'goal': week >= goal,
    }
    line = [{'date': r.finished_at.strftime('%d %b'), 'pct': round(100 * r.score / r.max_score) if r.max_score else 0, 'title': r.title} for r in reversed(res[:15])]
    return {'attempts': len(res), 'answers': len(rows), 'skills': skills, 'fams': fams, 'weak_topics': weak_topics, 'streak': streak, 'best_streak': best, 'week': week, 'goal': goal,
            'cards': len(cards), 'boxes': boxes, 'due': sum(1 for c in cards if c.due and c.due <= today), 'badges': [{'id': i, 'name': n, 'desc': dsc, 'got': earned[i]} for i, n, dsc in BADGES],
            'line': line, 'creative': cr, 'recent': res[:8]}


# ---- profile, interests, creative ------------------------------------------------------------------------------------------------------
def profile(uid, create=False):
    p = db.session.get(PulseExpProfile, uid)
    if not p and create:
        p = PulseExpProfile(user_id=uid, grade=8, weekly_goal=3)
        db.session.add(p)
        db.session.flush()
    return p


CLUSTERS = {
    'MEC': ('Mechanical, civil and aerospace engineering', 'E', 'Machines, vehicles, structures and flight.', 'JEE Main and Advanced'),
    'ELE': ('Electrical and electronics engineering', 'E', 'Circuits, power, sensors and communication.', 'JEE Main and Advanced'),
    'COM': ('Computer science and data', 'E', 'Programs, games, data and intelligent systems.', 'JEE Main and Advanced'),
    'CHE': ('Chemical and materials engineering', 'E', 'Processes, new materials, energy and food.', 'JEE Main and Advanced'),
    'BIO': ('Bio, environment and health engineering', 'E', 'Biotechnology, environment, water and medical devices.', 'JEE Main and Advanced, and biology-linked routes'),
    'PRD': ('Product and industrial design', 'D', 'Everyday objects, tools, vehicles and furniture made for people.', 'UCEED, NID DAT'),
    'VIS': ('Communication and visual design', 'D', 'Posters, books, signs, interfaces and brands.', 'UCEED, NID DAT'),
    'FAS': ('Fashion and textile design', 'D', 'Clothing, fabric, colour and craft.', 'NIFT entrance, NID DAT'),
    'ARC': ('Architecture and spaces', 'D', 'Buildings, interiors and towns.', 'NATA, JEE Main Paper 2'),
    'ANI': ('Animation, film and games', 'D', 'Moving images, characters and play.', 'UCEED, NID DAT'),
}
INTEREST_ITEMS = [
    ('I like taking toys or gadgets apart to see how they work.', ['MEC', 'ELE', 'PRD']),
    ('I enjoy drawing or sketching what I see around me.', ['VIS', 'PRD', 'ARC']),
    ('I like writing small programs, scripts or making games.', ['COM', 'ANI']),
    ('I wonder how bridges, buildings and roads are planned and built.', ['MEC', 'ARC']),
    ('Experiments with chemicals, colours changing or new materials excite me.', ['CHE', 'BIO']),
    ('I care about plants, animals, water and the environment.', ['BIO']),
    ('I like working with batteries, bulbs, motors and circuits.', ['ELE']),
    ('I notice patterns on clothes, fabrics and colour combinations.', ['FAS', 'VIS']),
    ('Puzzles with numbers, patterns and logic are fun for me.', ['COM', 'ELE', 'MEC']),
    ('I like making posters, comics, lettering or greeting cards.', ['VIS', 'ANI']),
    ('I often think how an everyday object could be easier or nicer to use.', ['PRD', 'MEC']),
    ('I enjoy building models with cardboard, clay or blocks.', ['ARC', 'PRD', 'MEC']),
    ('I am curious how cartoons, animated films or video games are made.', ['ANI', 'VIS', 'COM']),
    ('I want to know how water, electricity or waste reaches and leaves our homes.', ['MEC', 'ELE', 'BIO']),
    ('I like finding solutions to problems that people around me face.', ['PRD', 'BIO', 'ARC']),
    ('Solving a hard maths problem gives me a good feeling.', ['COM', 'ELE', 'MEC', 'CHE']),
]


def interest_result(answers):
    """answers: list of 16 ints 1-5. Returns clusters ranked by the weighted agreement, or None when the list is not valid."""
    if not isinstance(answers, list) or len(answers) != len(INTEREST_ITEMS) or not all(isinstance(a, int) and not isinstance(a, bool) and 1 <= a <= 5 for a in answers):
        return None
    score = {k: 0.0 for k in CLUSTERS}
    cnt = {k: 0 for k in CLUSTERS}
    for a, (_, cl) in zip(answers, INTEREST_ITEMS):
        for c in cl:
            score[c] += a - 3
            cnt[c] += 1
    rank = sorted(CLUSTERS, key=lambda k: -(score[k] / cnt[k] if cnt[k] else -9))
    rows = [{'key': k, 'name': CLUSTERS[k][0], 'kind': CLUSTERS[k][1], 'blurb': CLUSTERS[k][2], 'exams': CLUSTERS[k][3], 'score': round(score[k] / cnt[k], 2) if cnt[k] else 0} for k in rank]
    eng = [r for r in rows if r['kind'] == 'E'][:2]
    des = [r for r in rows if r['kind'] == 'D'][:2]
    e_avg = sum(r['score'] for r in rows if r['kind'] == 'E') / 5
    d_avg = sum(r['score'] for r in rows if r['kind'] == 'D') / 5
    lean = 'engineering' if e_avg - d_avg > 0.25 else 'design' if d_avg - e_avg > 0.25 else 'both engineering and design'
    return {'rows': rows, 'eng': eng, 'des': des, 'lean': lean}


def save_interests(uid, answers):
    r = interest_result(answers)
    if not r:
        return None
    p = profile(uid, True)
    p.interests_json = json.dumps(answers)
    p.updated_at = datetime.utcnow()
    db.session.commit()
    return r


def saved_interests(uid):
    p = db.session.get(PulseExpProfile, uid)
    if p and p.interests_json:
        try:
            a = json.loads(p.interests_json)
            return a, interest_result(a)
        except ValueError:
            pass
    return None, None


def save_creative(uid, cid, scores, note):
    c = next((x for x in creative() if x['id'] == cid), None)
    if not c or not isinstance(scores, list) or len(scores) != len(c['rubric']):
        return None
    vals = []
    for s, r in zip(scores, c['rubric']):
        if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= r['marks']:
            return None
        vals.append(s)
    row = PulseExpCreative.query.filter_by(user_id=uid, cid=cid).first() or PulseExpCreative(user_id=uid, cid=cid)
    row.scores_json = json.dumps(vals)
    row.total = sum(vals)
    row.note = (note or '')[:400]
    row.done_at = datetime.utcnow()
    db.session.add(row)
    db.session.commit()
    return row
