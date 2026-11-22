"""TNEA analytics: builds the payload for /tnea-analytics from app/data/tnea_analytics.py (facts) and app/data/tnea/cutoffs.json (official 2026 closing marks).

A closing mark is the lowest TNEA cut-off (out of 200) allotted a seat in that community: a higher number means a harder seat. OC is the open list.
The 2026 "final" closing mark of a course is the lowest across the three rounds (seats left after a round are filled in the next one).
Top 20 = the 20 colleges whose best course has the smallest 2026 OC closing rank. The predictor runs in the browser on the full file,
served at /tnea-analytics/cutoffs.json.
"""
import json
import os
import re
from functools import lru_cache
from statistics import median

from app.data import tnea_analytics as D

CUTOFFS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tnea', 'cutoffs.json')
FAMILIES = [
    ('AI', r'artificial|machine learning|data scien|data visual|generative'),
    ('IT', r'information technology'),
    ('ELEC', r'electrical'),
    ('CSE', r'computer|cyber|internet of things|software|block ?chain'),
    ('ENTC', r'electronics|communication|instrumentation|vlsi|telecommunication'),
    ('MECH', r'mechanical|automobile|production|manufactur|mechatron|robot|aeronaut|aerospace|marine|industrial engineering|mining|metallurg|material'),
    ('CIVIL', r'civil|structural|environment|geo ?informatics'),
    ('CHEM', r'chemical|petro|polymer|plastic|bio|food|textile|fashion|apparel|handloom|leather|ceramic|pharma|rubber|agricult|chemistry'),
]


@lru_cache(maxsize=1)
def cutoffs():
    with open(CUTOFFS, encoding='utf-8') as f:
        return json.load(f)


def family(name):
    n = name.lower()
    for f, rx in FAMILIES:
        if re.search(rx, n):
            return f
    return 'OTHER'


def district(col):
    if col['c'] in D.NEW_DISTRICT:
        return D.NEW_DISTRICT[col['c']]
    d = (col.get('d') or '').strip().upper()
    return D.DISTRICT_FIX.get(d) or d.title() or None


def region(dist):
    for r, ds in D.REGIONS.items():
        if dist in ds:
            return r
    return 'Other'


def short(col):
    if col['c'] in D.SHORT:
        return D.SHORT[col['c']]
    n = col['n'].split(',')[0]
    n = re.sub(r'\s*\((autonomous|formerly[^)]*)\)\s*', ' ', n, flags=re.I)
    n = re.sub(r'\s+', ' ', n).strip(' .-')
    if n.isupper():
        n = ' '.join(w if len(w) <= 3 and '.' in w else w.capitalize() for w in n.split())
        n = re.sub(r'\b(Of|And|For|The)\b', lambda m: m.group().lower(), n)
    return n


def final(row, ci):
    """[mark, rank] of the lowest allotment in community index ci across the 2026 rounds, or None."""
    best = None
    for k in sorted(row['r']):
        v = row['r'][k][ci]
        if v and (best is None or v[0] < best[0] or (v[0] == best[0] and v[1] > best[1])):
            best = v
    return best


def ptile(v, q):
    s = sorted(v)
    return s[int(q * (len(s) - 1))]


@lru_cache(maxsize=1)
def summary():
    d = cutoffs()
    br = d['branches']
    oc = d['comms'].index('OC')
    cols = {c['c']: c for c in d['colleges']}
    by_col, fam, seats_fam, seats_round = {}, {}, {}, {1: 0, 2: 0, 3: 0}
    for row in d['rows']:
        f = family(br.get(row['b'], ''))
        fo = final(row, oc)
        rec = {'b': row['b'], 'n': br.get(row['b'], row['b']), 'f': f, 'fin': fo, 'rd': {k: (v[oc][0] if v[oc] else None) for k, v in row['r'].items()},
               'y25': (row.get('y25') or [None])[0]}
        by_col.setdefault(row['c'], []).append(rec)
        if fo:
            fam.setdefault(f, {}).setdefault('fin', []).append(fo[0])
        for k, v in rec['rd'].items():
            if v is not None:
                fam.setdefault(f, {}).setdefault(k, []).append(v)
        if rec['y25']:
            fam.setdefault(f, {}).setdefault('2025', []).append(rec['y25'])
        for k, v in row['r'].items():
            n = sum(x[2] for x in v if x)
            seats_round[int(k)] += n
            seats_fam.setdefault(f, {1: 0, 2: 0, 3: 0})[int(k)] += n
    colleges = []
    for code, c in cols.items():
        rows = by_col.get(code, [])
        ref = [r for r in rows if r['fin']]
        best = min(ref, key=lambda r: r['fin'][1]) if ref else None
        cs = [r['fin'][0] for r in ref if r['f'] in ('CSE', 'AI', 'IT')]
        t = D.TYPE_OF.get(c.get('t') or '', 'T3')
        dist = district(c)
        colleges.append({'c': code, 'n': short(c), 't': t, 'type': D.TYPES[t][0], 'district': dist, 'region': region(dist), 'nirf': D.NIRF.get(code),
                         'best': best, 'cs': max(cs) if cs else None, 'rows': sorted(rows, key=lambda r: r['fin'][1] if r['fin'] else 10 ** 7)})
    ranked = sorted([x for x in colleges if x['best']], key=lambda x: x['best']['fin'][1])
    top = ranked[:20]
    top_rank = {t['c']: k + 1 for k, t in enumerate(top)}
    fam_stats = {f: {y: {'n': len(v), 'med': round(median(v), 2), 'p90': round(ptile(v, 0.9), 2), 'p25': round(ptile(v, 0.25), 2)} for y, v in sorted(ys.items())}
                 for f, ys in fam.items()}
    bands = [(195, 201, '195+'), (190, 195, '190–195'), (180, 190, '180–190'), (170, 180, '170–180'), (150, 170, '150–170'), (120, 150, '120–150'), (0, 120, 'under 120')]
    allfin = [r['fin'][0] for x in colleges for r in x['rows'] if r['fin']]
    hist = [[lab, sum(1 for v in allfin if lo <= v < hi)] for lo, hi, lab in bands]
    seats = {code: sum(x[2] for row in d['rows'] if row['c'] == code for v in row['r'].values() for x in v if x) for code in cols}
    maprows = [[x['c'], x['n'], x['district'], x['t'], x['nirf'], x['best']['fin'][0] if x['best'] else None, x['best']['n'] if x['best'] else None,
                len(x['rows']), x['cs'], top_rank.get(x['c']), seats[x['c']]] for x in colleges]
    for t in top:   # keep the page payload small: top-20 detail rows only carry what the table shows
        t['rows'] = [{'n': r['n'], 'f': r['f'], 'fin': r['fin'], 'rd': r['rd'], 'y25': r['y25']} for r in t['rows']]
    return {'top': top, 'fam': fam_stats, 'hist': hist, 'map': maprows, 'seatsRound': seats_round, 'seatsFam': seats_fam, 'curve': d['curve'],
            'n_col': len(cols), 'n_rows': len(d['rows']), 'n_courses': len({r['b'] for r in d['rows']}), 'n_seats': sum(seats_round.values())}


def payload():
    s = summary()
    return {'verified': D.VERIFIED, 'src': D.SRC, 'dates': D.DATES, 'rounds26': D.ROUNDS_2026, 'ranklist': D.RANKLIST_2026, 'pattern': D.PATTERN,
            'elig': D.ELIGIBILITY, 'comms': D.COMMS, 'resvNote': D.RESERVATION_NOTE, 'types': D.TYPES, 'nirfNot': D.NIRF_NOT_TNEA,
            'famNames': D.FAMILY_NAMES, 'guide': D.BRANCH_GUIDE, 'regions': D.REGIONS, 'sites': D.SITES, **s}
