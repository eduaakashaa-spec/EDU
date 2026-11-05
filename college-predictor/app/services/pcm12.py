"""Class 12 PCM Analytics: the data and the logic behind /class12-pcm.

* Four stand-alone EduAakashaA pages (app/data/pcm12/pages): Eligibility Gap Closer, Board Score Playbook, Thumb Rules Handbook, Answer Sheet Lab. They are served as supplied, with their links
  pointed at the portal. Their eligibility rules were read from public coaching and news pages, not the official brochures, and each row carries its own confidence label on the page.
* Chapters (app/data/pcm12/chapters.json): the 37 PCM chapters from the Board Score Playbook with indicative marks, the Core / Build / Later class for each of the four levels, and the rule, hook and
  trap from the Thumb Rules Handbook. Only the unit-group marks are official; chapter marks are indicative.
* Routes (app/data/pcm12/routes.json): the 11 entrance routes of the Eligibility Gap Closer with the Class 12 percentage each asks for, by category (g general, s SC/ST/PwD or reserved, b TN BC/MBC/DNC),
  as [low, high] where sources disagree.
* analyse(profile) works out, for the members dashboard: PCM and 5-subject percentages, the status of every route, the level of each subject from the test log, a priority order for the chapters and a
  week-by-week study plan counted back from the first paper, with tasks that can be ticked off. quick_plan() is the same plan for a visitor who is not logged in (nothing saved).
"""
import json
import os
import re
from datetime import date, datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pcm12')
SUBJ = {'P': 'Physics', 'C': 'Chemistry', 'M': 'Mathematics'}
LEVELS = ['Needs support', 'Average', 'Good', 'Excellent']
PAGES = {'eligibility': 'Eligibility Gap Closer', 'board-playbook': 'Board Score Playbook', 'thumb-rules': 'Thumb Rules Handbook', 'answer-lab': 'Answer Sheet Lab'}
ARTIFACT_PAGE = {'Jc292a1ouMx6Hds1VFT1nj': 'eligibility', '6Qu8BNPhQd1AQJJK8PJPM8': 'board-playbook', '5RpsotpWjtxPsNAGw2koXJ': 'thumb-rules', 'R39jk652ZTvWJjyBWyNJLn': 'answer-lab'}
MAX_MARKS = {'Pt': 70, 'Pp': 30, 'Ct': 70, 'Cp': 30, 'Mt': 80, 'Mi': 20, 'En': 100, 'Fi': 100}
DEFAULT_MARKS = {'Pt': 0, 'Pp': 0, 'Ct': 0, 'Cp': 0, 'Mt': 0, 'Mi': 0, 'En': 0, 'Fi': 0}
PHASES = {0: [.45, .30, .15, .10], 1: [.40, .30, .20, .10], 2: [.30, .30, .25, .15], 3: [.20, .30, .30, .20]}
PHASE_NAMES = ['Close concepts', 'Practise by chapter', 'Timed papers', 'Final revision']
MAX_TESTS = 120
_cache = {}


def _read(name):
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)


def chapters():
    if 'ch' not in _cache:
        _cache['ch'] = _read('chapters.json')
        _cache['ch_by'] = {c['id']: c for c in _cache['ch']}
    return _cache['ch']


def chapter(cid):
    chapters()
    return _cache['ch_by'].get(cid)


def routes():
    if 'rt' not in _cache:
        _cache['rt'] = _read('routes.json')
    return _cache['rt']


# ---- the four supplied pages -------------------------------------------------------------------------------------------------------------
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


def _judge(have, lo, hi, denom, total):
    need = int(-(-(hi * denom / 100.0 - total - 1e-9) // 1))
    if have >= hi - 1e-9:
        return 'meets', 0
    if lo < hi and have >= lo - 1e-9:
        return 'check', max(need, 0)
    return 'short', max(need, 0)


def eligibility(marks, cat='g'):
    m = {k: _num((marks or {}).get(k), v) for k, v in MAX_MARKS.items()}
    P, C, M = m['Pt'] + m['Pp'], m['Ct'] + m['Cp'], m['Mt'] + m['Mi']
    pcm_sum = P + C + M
    pcm, agg = pcm_sum / 3.0, (pcm_sum + m['En'] + m['Fi']) / 5.0
    cat = cat if cat in ('g', 's', 'b') else 'g'
    rows = []
    for e in routes():
        lo, hi = e['th'][cat]
        if e['basis'] == 'agg5':
            have, denom, total, basis = agg, 500, pcm_sum + m['En'] + m['Fi'], '5-subject'
        elif e['basis'] == 'min':
            if agg < pcm:
                have, denom, total, basis = agg, 500, pcm_sum + m['En'] + m['Fi'], '5-subject (lower)'
            else:
                have, denom, total, basis = pcm, 300, pcm_sum, 'PCM (lower)'
        else:
            have, denom, total, basis = pcm, 300, pcm_sum, 'PCM'
        status, add = _judge(have, lo, hi, denom, total)
        floor = []
        if e['basis'] == 'pcmsub60':
            floor = [{'subject': n, 'short': int(-(-(60 - v - 1e-9) // 1))} for n, v in (('Physics', P), ('Chemistry', C), ('Maths', M)) if v < 60]
            if floor:
                status, add = 'short', max(add if status != 'meets' else 0, sum(f['short'] for f in floor))
        rows.append({'id': e['id'], 'name': e['name'], 'need': [lo, hi], 'basis': basis, 'have': round(have, 1), 'status': status, 'add': add, 'denom': denom, 'floor': floor})
    tnea = m['Mt'] + m['Mi'] + (P + C) / 2.0
    return {'pcm': round(pcm, 1), 'agg': round(agg, 1), 'pcm_sum': round(pcm_sum, 1), 'tnea': round(tnea, 1), 'routes': rows, 'entered': pcm_sum > 0,
            'P': round(P, 1), 'C': round(C, 1), 'M': round(M, 1)}


# ---- levels and chapter priority ---------------------------------------------------------------------------------------------------------
def band(pct):
    return 0 if pct < 50 else 1 if pct < 65 else 2 if pct < 80 else 3


def clean_tests(tests):
    out = []
    for t in (tests or [])[:MAX_TESTS]:
        if not isinstance(t, dict) or t.get('subj') not in SUBJ:
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


def subject_levels(tests, marks, level_override=None):
    """Level of each subject: the average of its last three tests, else the board-style marks entered, else 'Average'. A level the student chose wins."""
    out = {}
    m = {k: _num((marks or {}).get(k), v) for k, v in MAX_MARKS.items()}
    theory = {'P': 100 * m['Pt'] / 70.0 if m['Pt'] else None, 'C': 100 * m['Ct'] / 70.0 if m['Ct'] else None, 'M': 100 * m['Mt'] / 80.0 if m['Mt'] else None}
    for s in SUBJ:
        mine = [t for t in tests if t['subj'] == s]
        mine.sort(key=lambda t: t['date'] or '')
        last = mine[-3:]
        if last:
            pct, src = sum(t['pct'] for t in last) / len(last), 'last %d test%s' % (len(last), '' if len(last) == 1 else 's')
        elif theory[s] is not None:
            pct, src = theory[s], 'marks entered'
        else:
            pct, src = None, 'not enough data'
        b = band(pct) if pct is not None else 1
        if level_override and isinstance(level_override.get(s), int) and 0 <= level_override[s] <= 3:
            b, src = level_override[s], 'chosen by you'
        out[s] = {'name': SUBJ[s], 'pct': round(pct, 1) if pct is not None else None, 'band': b, 'level': LEVELS[b], 'source': src, 'tests': len(mine)}
    return out


def priorities(levels, ratings):
    """Every chapter with its class for the subject's level (Core, Build, Later), the student's rating (1 weak to 5 strong, default 3) and a priority score: marks x (6 - rating) x class weight."""
    weight = {'Core': 1.0, 'Build': 0.7, 'Later': 0.3}
    out = []
    for c in chapters():
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


def build_plan(levels, prio, exam, wd, we, today=None, done=None):
    today = today or date.today()
    exam = parse_date(exam)
    days = (exam - today).days if exam else 0
    weeks = max(0, int(round(days / 7.0)))
    wd, we = _num(wd, 14), _num(we, 24)
    hpw = 5 * wd + 2 * we
    info = {'weeks': weeks, 'hours_week': round(hpw, 1), 'hours_total': int(round(hpw * weeks)), 'exam': exam.isoformat() if exam else '', 'days': days}
    if not exam or days <= 0 or weeks < 1:
        return info, [], []
    mean_band = int(round(sum(v['band'] for v in levels.values()) / 3.0))
    ph = _alloc(weeks, PHASES[mean_band])
    weakest = min(levels, key=lambda s: (levels[s]['pct'] if levels[s]['pct'] is not None else 60))
    share = {'P': 70 / 220.0, 'C': 70 / 220.0, 'M': 80 / 220.0}
    for k in share:
        share[k] += .08 if k == weakest else -.04
    info.update({'phase_weeks': ph, 'phase_names': PHASE_NAMES, 'phase_level': LEVELS[mean_band], 'subject_hours': {k: round(hpw * share[k], 1) for k in share}, 'weakest': SUBJ[weakest]})
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
                for c in batches[w]:
                    tasks.append({'id': 'p1-' + c['id'], 'text': 'Study %s: read the rule card, work the NCERT solved examples, make a one-page formula and unit sheet.' % c['name'], 'subj': c['subj'], 'chapter': c['id']})
            elif pi == 1:
                for c in batches[w]:
                    tasks.append({'id': 'p2-' + c['id'], 'text': 'Practise %s: a chapter test or exemplar set, then log every error as concept, calculation, reading or time.' % c['name'], 'subj': c['subj'], 'chapter': c['id']})
            elif pi == 2:
                k = w + 1
                tasks = [{'id': 'p3-%d-a' % k, 'text': 'Two timed section drills (Section A, then one long-answer section) against the clock.', 'subj': '', 'chapter': ''},
                         {'id': 'p3-%d-b' % k, 'text': 'One full paper under exam conditions in %s, then mark it against the marking scheme.' % SUBJ['PCM'[(w + (0 if weakest == 'P' else 1 if weakest == 'C' else 2)) % 3]],
                          'subj': '', 'chapter': ''},
                         {'id': 'p3-%d-c' % k, 'text': 'Rewrite two low-scoring answers in full marking-scheme style (see the Answer Sheet Lab).', 'subj': '', 'chapter': ''}]
            else:
                k = w + 1
                tasks = [{'id': 'p4-%d-a' % k, 'text': 'Revise the rule cards of one subject, in rotation, and say each rule aloud.', 'subj': '', 'chapter': ''},
                         {'id': 'p4-%d-b' % k, 'text': 'Close the weakest chapter in %s before adding anything new.' % SUBJ[weakest], 'subj': weakest, 'chapter': ''},
                         {'id': 'p4-%d-c' % k, 'text': 'Simulate the full paper and aim to finish 20 minutes early for review; keep time for practical records and viva.', 'subj': '', 'chapter': ''}]
            for t in tasks:
                t['done'] = bool(done.get(t['id']))
            weeks_out.append({'n': n, 'start': start.isoformat(), 'phase': pi + 1, 'phase_name': PHASE_NAMES[pi], 'tasks': tasks})
    return info, weeks_out, todo


def analyse(profile, today=None):
    p = profile if isinstance(profile, dict) else {}
    tests = clean_tests(p.get('tests'))
    marks = {k: _num((p.get('marks') or {}).get(k), v) for k, v in MAX_MARKS.items()}
    ratings = {k: v for k, v in (p.get('ratings') or {}).items() if chapter(k) and isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 5} if isinstance(p.get('ratings'), dict) else {}
    chapters()
    override = p.get('levels') if isinstance(p.get('levels'), dict) else None
    levels = subject_levels(tests, marks, override)
    prio = priorities(levels, ratings)
    done = {k: bool(v) for k, v in (p.get('done') or {}).items() if isinstance(k, str) and len(k) < 24} if isinstance(p.get('done'), dict) else {}
    info, weeks, todo = build_plan(levels, prio, p.get('exam_date'), p.get('hours_wd', 2), p.get('hours_we', 5), today, done)
    ntasks = sum(len(w['tasks']) for w in weeks)
    ndone = sum(1 for w in weeks for t in w['tasks'] if t['done'])
    trend = {s: [{'date': t['date'], 'pct': t['pct']} for t in sorted((x for x in tests if x['subj'] == s), key=lambda x: x['date'] or '')][-12:] for s in SUBJ}
    return {'elig': eligibility(marks, p.get('cat', 'g')), 'levels': levels, 'chapters': prio, 'plan': info, 'weeks': weeks, 'progress': {'tasks': ntasks, 'done': ndone, 'pct': round(100 * ndone / ntasks) if ntasks else 0},
            'tests': tests, 'trend': trend, 'rated': len(ratings)}


def quick_plan(level, exam_date, wd, we, today=None):
    """A visitor's plan: one level for every subject, no chapter ratings, nothing saved. Returns the plan summary and the first chapters to start."""
    b = level if isinstance(level, int) and 0 <= level <= 3 else 1
    levels = {s: {'name': SUBJ[s], 'pct': None, 'band': b, 'level': LEVELS[b], 'source': 'chosen by you', 'tests': 0} for s in SUBJ}
    prio = priorities(levels, {})
    info, weeks, todo = build_plan(levels, prio, exam_date, wd, we, today)
    first = [{'name': c['name'], 'subj': SUBJ[c['subj']], 'cls': c['cls'], 'marks': c['marks']} for c in prio[:8]]
    return {'plan': info, 'level': LEVELS[b], 'first': first}
