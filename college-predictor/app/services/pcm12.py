"""Class 12 PCM and PCB Analytics: the data and the logic behind /class12-pcm and /class12-pcb.

A stream is the set of three board subjects: 'pcm' (Physics, Chemistry, Mathematics) or 'pcb' (Physics, Chemistry, Biology). STREAMS holds, for each, its subjects, board mark limits, chapters file and routes file.

* PCM: four stand-alone EduAakashaA pages (app/data/pcm12/pages): Eligibility Gap Closer, Board Score Playbook, Thumb Rules Handbook, Answer Sheet Lab, served as supplied with links pointed at the portal.
  Their eligibility rules were read from public coaching and news pages, not the official brochures; each row carries its own confidence label on the page.
* Chapters (chapters.json for PCM, chapters_pcb.json for PCB): the PCM chapters from the Board Score Playbook, and for PCB the same Physics and Chemistry chapters with 13 Biology chapters. Each has
  indicative marks (only the unit-group marks are official), the Core / Build / Later class for each of the four levels, and a rule, hook and trap.
* Routes (routes.json, routes_pcb.json): the entrance routes with the Class 12 percentage each asks for, by category (g general, s reserved, b third category), as [low, high] where sources disagree.
* analyse(profile, stream) works out, for the members dashboard: core-subject and 5-subject percentages, the status of every route, the level of each subject from the test log, a priority order for the
  chapters and a week-by-week study plan counted back from the first paper, with tasks that can be ticked off. quick_plan() is the same plan for a visitor who is not logged in (nothing saved).
"""
import json
import os
import re
from datetime import date, datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pcm12')
LEVELS = ['Needs support', 'Average', 'Good', 'Excellent']
PAGES = {'eligibility': 'Eligibility Gap Closer', 'board-playbook': 'Board Score Playbook', 'thumb-rules': 'Thumb Rules Handbook', 'answer-lab': 'Answer Sheet Lab'}
ARTIFACT_PAGE = {'Jc292a1ouMx6Hds1VFT1nj': 'eligibility', '6Qu8BNPhQd1AQJJK8PJPM8': 'board-playbook', '5RpsotpWjtxPsNAGw2koXJ': 'thumb-rules', 'R39jk652ZTvWJjyBWyNJLn': 'answer-lab'}
PHASES = {0: [.45, .30, .15, .10], 1: [.40, .30, .20, .10], 2: [.30, .30, .25, .15], 3: [.20, .30, .30, .20]}
PHASE_NAMES = ['Close concepts', 'Practise by chapter', 'Timed papers', 'Final revision']
MAX_TESTS = 120

STREAMS = {
    'pcm': {'name': 'PCM', 'subj': {'P': 'Physics', 'C': 'Chemistry', 'M': 'Mathematics'}, 'order': 'PCM',
            'marks': {'Pt': 70, 'Pp': 30, 'Ct': 70, 'Cp': 30, 'Mt': 80, 'Mi': 20, 'En': 100, 'Fi': 100},
            'labels': {'Pt': 'Physics theory', 'Pp': 'Physics practical', 'Ct': 'Chemistry theory', 'Cp': 'Chemistry practical', 'Mt': 'Maths theory', 'Mi': 'Maths internal', 'En': 'English', 'Fi': 'Fifth subject'},
            'theory': {'P': ('Pt', 70), 'C': ('Ct', 70), 'M': ('Mt', 80)}, 'weights': {'P': 70, 'C': 70, 'M': 80}, 'chapters': 'chapters.json', 'routes': 'routes.json', 'test_max': {'P': 70, 'C': 70, 'M': 80},
            'cats': [('g', 'General, EWS or OBC-NCL (OC in Tamil Nadu)'), ('s', 'SC, ST or PwD'), ('b', 'Tamil Nadu BC, MBC or DNC')]},
    'pcb': {'name': 'PCB', 'subj': {'P': 'Physics', 'C': 'Chemistry', 'B': 'Biology'}, 'order': 'PCB',
            'marks': {'Pt': 70, 'Pp': 30, 'Ct': 70, 'Cp': 30, 'Bt': 70, 'Bp': 30, 'En': 100, 'Fi': 100},
            'labels': {'Pt': 'Physics theory', 'Pp': 'Physics practical', 'Ct': 'Chemistry theory', 'Cp': 'Chemistry practical', 'Bt': 'Biology theory', 'Bp': 'Biology practical', 'En': 'English', 'Fi': 'Fifth subject'},
            'theory': {'P': ('Pt', 70), 'C': ('Ct', 70), 'B': ('Bt', 70)}, 'weights': {'P': 70, 'C': 70, 'B': 70}, 'chapters': 'chapters_pcb.json', 'routes': 'routes_pcb.json', 'test_max': {'P': 70, 'C': 70, 'B': 70},
            'cats': [('g', 'General, UR or EWS'), ('s', 'SC, ST or OBC-NCL'), ('b', 'UR with a benchmark disability (PwBD)')]},
}
# kept for the PCM-only callers and tests
SUBJ = STREAMS['pcm']['subj']
MAX_MARKS = STREAMS['pcm']['marks']
_cache = {}


def cfg(stream):
    return STREAMS.get(stream) or STREAMS['pcm']


def _read(name):
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)


def chapters(stream='pcm'):
    c = cfg(stream)
    k = c['chapters']
    if k not in _cache:
        _cache[k] = _read(k)
        _cache[k + ':by'] = {x['id']: x for x in _cache[k]}
    return _cache[k]


def chapter(cid, stream='pcm'):
    chapters(stream)
    return _cache[cfg(stream)['chapters'] + ':by'].get(cid)


def state_facts():
    """Official facts for the state routes (Maharashtra, Delhi, Kerala, Andhra Pradesh), each with its source page, and what could not be confirmed."""
    if 'state_facts' not in _cache:
        try:
            _cache['state_facts'] = _read('state_facts.json')
        except (OSError, ValueError):
            _cache['state_facts'] = {'states': [], 'notes': []}
    return _cache['state_facts']


def routes(stream='pcm'):
    k = cfg(stream)['routes']
    if k not in _cache:
        _cache[k] = _read(k)
    return _cache[k]


# ---- the four supplied PCM pages ---------------------------------------------------------------------------------------------------------
def page_html(name, urls, strip_html):
    """The supplied page with its cross-links pointed at the portal. `urls` maps a page name to its portal URL."""
    if name not in PAGES:
        return None
    with open(os.path.join(DATA_DIR, 'pages', name + '.html'), encoding='utf-8') as f:
        s = f.read()
    for aid, page in ARTIFACT_PAGE.items():
        s = re.sub(r'<a ([^>]*?)href="https://claude\.ai/artifact/%s"([^>]*)>' % aid, lambda m, p=page: '<a %shref="%s"%s>' % (re.sub(r'\s*(target|rel)="[^"]*"', '', m.group(1)), urls[p],
                   re.sub(r'\s*(target|rel)="[^"]*"', '', m.group(2))), s)
    s = s.replace('./eduaakashaa_logo.png', urls['_logo'])
    s = s.replace('href="#contact">Talk to a counsellor', 'href="%s">Talk to a counsellor' % urls['_contact'])
    s = s.replace('<a id="top"></a>', '<a id="top"></a>' + strip_html, 1)
    return s


# ---- eligibility -------------------------------------------------------------------------------------------------------------------------
def _num(v, hi):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(float(hi), x))


def _ceil(x):
    return int(-(-x // 1))


def _judge(have, lo, hi, denom, total):
    need = _ceil(hi * denom / 100.0 - total - 1e-9)
    if have >= hi - 1e-9:
        return 'meets', 0
    if lo < hi and have >= lo - 1e-9:
        return 'check', max(need, 0)
    return 'short', max(need, 0)


def clean_marks(marks, stream='pcm'):
    return {k: _num((marks or {}).get(k), v) for k, v in cfg(stream)['marks'].items()}


def eligibility(marks, cat='g', stream='pcm'):
    c = cfg(stream)
    m = clean_marks(marks, stream)
    keys = c['order']
    tot = {}
    for s in keys:
        t, p = [k for k in c['marks'] if k[0] == s][:2]
        tot[s] = m[t] + m[p]
    core_sum = sum(tot.values())
    core, agg = core_sum / 3.0, (core_sum + m['En'] + m['Fi']) / 5.0
    cat = cat if cat in ('g', 's', 'b') else 'g'
    rows = []
    for e in routes(stream):
        lo, hi = e['th'][cat]
        b = e['basis']
        if b == 'agg5':
            have, denom, total, basis = agg, 500, core_sum + m['En'] + m['Fi'], '5-subject'
        elif b == 'min':
            if agg < core:
                have, denom, total, basis = agg, 500, core_sum + m['En'] + m['Fi'], '5-subject (lower)'
            else:
                have, denom, total, basis = core, 300, core_sum, c['name'] + ' (lower)'
        elif b == 'core_eng':
            have, denom, total, basis = (core_sum + m['En']) / 4.0, 400, core_sum + m['En'], c['name'] + ' and English'
        else:                                                   # 'pcm', 'pcb', 'core', 'core_sub60': the three core subjects over 300
            have, denom, total, basis = core, 300, core_sum, c['name']
        status, add = _judge(have, lo, hi, denom, total)
        floor = []
        if b == 'pcmsub60' or b == 'core_sub60':
            floor = [{'subject': c['subj'][s], 'short': _ceil(60 - tot[s] - 1e-9)} for s in keys if tot[s] < 60]
            if floor:
                status, add = 'short', max(add if status != 'meets' else 0, sum(f['short'] for f in floor))
        rows.append({'id': e['id'], 'name': e['name'], 'need': [lo, hi], 'basis': basis, 'have': round(have, 1), 'status': status, 'add': add, 'denom': denom, 'floor': floor,
                     'note': e.get('note', ''), 'source': e.get('source', ''), 'confidence': e.get('confidence', '')})
    tnea = (m['Mt'] + m['Mi'] + (tot['P'] + tot['C']) / 2.0) if stream == 'pcm' else None
    return {'core': round(core, 1), 'pcm': round(core, 1), 'agg': round(agg, 1), 'core_sum': round(core_sum, 1), 'pcm_sum': round(core_sum, 1), 'tnea': round(tnea, 1) if tnea is not None else None,
            'routes': rows, 'entered': core_sum > 0, 'label': c['name'], 'totals': {s: round(v, 1) for s, v in tot.items()}}


# ---- levels and chapter priority ---------------------------------------------------------------------------------------------------------
def band(pct):
    return 0 if pct < 50 else 1 if pct < 65 else 2 if pct < 80 else 3


def clean_tests(tests, stream='pcm'):
    subj = cfg(stream)['subj']
    out = []
    for t in (tests or [])[:MAX_TESTS]:
        if not isinstance(t, dict) or t.get('subj') not in subj:
            continue
        mx = _num(t.get('max'), 1000)
        got = _num(t.get('got'), 1000)
        if mx <= 0 or got > mx:
            continue
        d = str(t.get('date') or '')[:10]
        try:
            datetime.strptime(d, '%Y-%m-%d')
        except ValueError:
            d = ''
        out.append({'date': d, 'subj': t['subj'], 'got': got, 'max': mx, 'pct': round(100 * got / mx, 1), 'note': str(t.get('note') or '')[:80]})
    return out


def subject_levels(tests, marks, level_override=None, stream='pcm'):
    """Level of each subject: the average of its last three tests, else the board-style marks entered, else 'Average'. A level the student chose wins."""
    c = cfg(stream)
    out = {}
    m = clean_marks(marks, stream)
    for s, name in c['subj'].items():
        key, mx = c['theory'][s]
        theory = 100 * m[key] / float(mx) if m[key] else None
        mine = sorted((t for t in tests if t['subj'] == s), key=lambda t: t['date'] or '')
        last = mine[-3:]
        if last:
            pct, src = sum(t['pct'] for t in last) / len(last), 'last %d test%s' % (len(last), '' if len(last) == 1 else 's')
        elif theory is not None:
            pct, src = theory, 'marks entered'
        else:
            pct, src = None, 'not enough data'
        b = band(pct) if pct is not None else 1
        if level_override and isinstance(level_override.get(s), int) and not isinstance(level_override.get(s), bool) and 0 <= level_override[s] <= 3:
            b, src = level_override[s], 'chosen by you'
        out[s] = {'name': name, 'pct': round(pct, 1) if pct is not None else None, 'band': b, 'level': LEVELS[b], 'source': src, 'tests': len(mine)}
    return out


def priorities(levels, ratings, stream='pcm'):
    """Every chapter with its class for the subject's level (Core, Build, Later), the student's rating (1 weak to 5 strong, default 3) and a priority score: marks x (6 - rating) x class weight."""
    weight = {'Core': 1.0, 'Build': 0.7, 'Later': 0.3}
    out = []
    for c in chapters(stream):
        b = levels[c['subj']]['band']
        cls = c['levels'][b]
        r = (ratings or {}).get(c['id'])
        r = r if isinstance(r, int) and 1 <= r <= 5 else 3
        out.append({'id': c['id'], 'subj': c['subj'], 'name': c['name'], 'unit': c['unit'], 'marks': c['marks'], 'cls': cls, 'rating': r, 'rated': (ratings or {}).get(c['id']) is not None,
                    'score': round(c['marks'] * (6 - r) * weight.get(cls, 1.0), 1)})
    out.sort(key=lambda x: (-x['score'], -x['marks'], x['name']))
    for i, x in enumerate(out):
        x['rank'] = i + 1
    return out


# ---- the study plan ----------------------------------------------------------------------------------------------------------------------
def _alloc(total, fr):
    raw = [f * total for f in fr]
    base = [int(r) for r in raw]
    if total >= 4:
        base = [max(1, b) for b in base]
    left = total - sum(base)
    order = sorted(range(4), key=lambda i: -(raw[i] - int(raw[i])))
    k = 0
    while left > 0:
        base[order[k % 4]] += 1
        left -= 1
        k += 1
    while left < 0:
        j = base.index(max(base))
        base[j] -= 1
        left += 1
    return base


def parse_date(v):
    try:
        return datetime.strptime(str(v)[:10], '%Y-%m-%d').date()
    except ValueError:
        return None


def build_plan(levels, prio, exam, wd, we, today=None, done=None, stream='pcm'):
    c = cfg(stream)
    today = today or date.today()
    exam = parse_date(exam)
    days = (exam - today).days if exam else 0
    weeks = max(0, int(round(days / 7.0)))
    wd, we = _num(wd, 14), _num(we, 24)
    hpw = 5 * wd + 2 * we
    info = {'weeks': weeks, 'hours_week': round(hpw, 1), 'hours_total': int(round(hpw * weeks)), 'exam': exam.isoformat() if exam else '', 'days': days}
    if not exam or days <= 0 or weeks < 1:
        return info, [], []
    keys = c['order']
    mean_band = int(round(sum(v['band'] for v in levels.values()) / 3.0))
    ph = _alloc(weeks, PHASES[mean_band])
    weakest = min(levels, key=lambda s: (levels[s]['pct'] if levels[s]['pct'] is not None else 60))
    tw = float(sum(c['weights'].values()))
    share = {k: c['weights'][k] / tw for k in keys}
    for k in share:
        share[k] += .08 if k == weakest else -.04
    info.update({'phase_weeks': ph, 'phase_names': PHASE_NAMES, 'phase_level': LEVELS[mean_band], 'subject_hours': {k: round(hpw * share[k], 1) for k in share}, 'weakest': c['subj'][weakest]})
    todo = [p for p in prio if p['cls'] != 'Later' or p['rating'] <= 2]
    if len(todo) < 8:
        todo = list(prio)
    done = done or {}
    weeks_out, n = [], 0
    for pi in range(4):
        pw = ph[pi]
        if pi < 2:
            per = max(1, -(-len(todo) // pw)) if pw else 0
            batches = [todo[i * per:(i + 1) * per] for i in range(pw)]
        for w in range(pw):
            n += 1
            start = today + timedelta(days=7 * (n - 1))
            tasks = []
            if pi == 0:
                for ch in batches[w]:
                    tasks.append({'id': 'p1-' + ch['id'], 'text': 'Study %s: read the rule card, work the NCERT solved examples, make a one-page %s.' % (ch['name'], 'labelled-diagram and keyword sheet' if ch['subj'] == 'B' else 'formula and unit sheet'),
                                  'subj': ch['subj'], 'chapter': ch['id']})
            elif pi == 1:
                for ch in batches[w]:
                    tasks.append({'id': 'p2-' + ch['id'], 'text': 'Practise %s: a chapter test or exemplar set, then log every error as concept, calculation, reading or time.' % ch['name'], 'subj': ch['subj'], 'chapter': ch['id']})
            elif pi == 2:
                k = w + 1
                subj_cycle = keys[(w + keys.index(weakest)) % 3]
                tasks = [{'id': 'p3-%d-a' % k, 'text': 'Two timed section drills (Section A, then one long-answer section) against the clock.', 'subj': '', 'chapter': ''},
                         {'id': 'p3-%d-b' % k, 'text': 'One full paper under exam conditions in %s, then mark it against the marking scheme.' % c['subj'][subj_cycle], 'subj': '', 'chapter': ''},
                         {'id': 'p3-%d-c' % k, 'text': 'Rewrite two low-scoring answers in full marking-scheme style (see the Answer Sheet Lab).', 'subj': '', 'chapter': ''}]
            else:
                k = w + 1
                tasks = [{'id': 'p4-%d-a' % k, 'text': 'Revise the rule cards of one subject, in rotation, and say each rule aloud.', 'subj': '', 'chapter': ''},
                         {'id': 'p4-%d-b' % k, 'text': 'Close the weakest chapter in %s before adding anything new.' % c['subj'][weakest], 'subj': weakest, 'chapter': ''},
                         {'id': 'p4-%d-c' % k, 'text': 'Simulate the full paper and aim to finish 20 minutes early for review; keep time for practical records and viva.', 'subj': '', 'chapter': ''}]
            for t in tasks:
                t['done'] = bool(done.get(t['id']))
            weeks_out.append({'n': n, 'start': start.isoformat(), 'phase': pi + 1, 'phase_name': PHASE_NAMES[pi], 'tasks': tasks})
    return info, weeks_out, todo


def clean_profile(d, stream='pcm'):
    """The parts of a posted profile that are kept: bad keys, out-of-range values and unknown chapters are dropped."""
    c = cfg(stream)
    d = d if isinstance(d, dict) else {}

    def okint(v, lo, hi):
        return isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi
    lv = d.get('levels') if isinstance(d.get('levels'), dict) else {}
    rt = d.get('ratings') if isinstance(d.get('ratings'), dict) else {}
    dn = d.get('done') if isinstance(d.get('done'), dict) else {}
    return {'exam_date': str(d.get('exam_date') or '')[:10], 'hours_wd': _num(d.get('hours_wd'), 14), 'hours_we': _num(d.get('hours_we'), 24), 'cat': d.get('cat') if d.get('cat') in ('g', 's', 'b') else 'g',
            'marks': clean_marks(d.get('marks'), stream) if isinstance(d.get('marks'), dict) else {}, 'tests': clean_tests(d.get('tests'), stream),
            'levels': {s: v for s, v in lv.items() if s in c['subj'] and okint(v, 0, 3)}, 'ratings': {k: v for k, v in rt.items() if chapter(k, stream) and okint(v, 1, 5)},
            'done': {k: True for k, v in dn.items() if v and isinstance(k, str) and len(k) < 24}}


def analyse(profile, today=None, stream='pcm'):
    c = cfg(stream)
    raw = profile if isinstance(profile, dict) else {}
    p = clean_profile(profile, stream)
    tests = p['tests']
    marks = p['marks']
    levels = subject_levels(tests, marks, p['levels'], stream)
    prio = priorities(levels, p['ratings'], stream)
    info, weeks, todo = build_plan(levels, prio, p['exam_date'], p['hours_wd'] if raw.get('hours_wd') is not None else 2, p['hours_we'] if raw.get('hours_we') is not None else 5, today, p['done'], stream)
    ntasks = sum(len(w['tasks']) for w in weeks)
    ndone = sum(1 for w in weeks for t in w['tasks'] if t['done'])
    trend = {s: [{'date': t['date'], 'pct': t['pct']} for t in sorted((x for x in tests if x['subj'] == s), key=lambda x: x['date'] or '')][-12:] for s in c['subj']}
    return {'elig': eligibility(marks, p['cat'], stream), 'levels': levels, 'chapters': prio, 'plan': info, 'weeks': weeks, 'progress': {'tasks': ntasks, 'done': ndone, 'pct': round(100 * ndone / ntasks) if ntasks else 0},
            'tests': tests, 'trend': trend, 'rated': len(p['ratings'])}


def quick_plan(level, exam_date, wd, we, today=None, stream='pcm'):
    """A visitor's plan: one level for every subject, no chapter ratings, nothing saved. Returns the plan summary and the first chapters to start with."""
    c = cfg(stream)
    b = level if isinstance(level, int) and not isinstance(level, bool) and 0 <= level <= 3 else 1
    levels = {s: {'name': n, 'pct': None, 'band': b, 'level': LEVELS[b], 'source': 'chosen by you', 'tests': 0} for s, n in c['subj'].items()}
    prio = priorities(levels, {}, stream)
    info, weeks, todo = build_plan(levels, prio, exam_date, wd, we, today, None, stream)
    first = [{'name': x['name'], 'subj': c['subj'][x['subj']], 'cls': x['cls'], 'marks': x['marks']} for x in prio[:8]]
    return {'plan': info, 'level': LEVELS[b], 'first': first}
