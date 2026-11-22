"""KEAM analytics: builds the payload for /keam-analytics from app/data/keam.py (facts) and app/data/keam/lastranks.json (official CEE last ranks).

A last rank is the rank of the last candidate allotted a seat in that category: a smaller number means a harder seat. State Merit (SM) is the open list.
Top 20 = the 20 colleges with the smallest 2026 Phase 1 State Merit last rank in any course. The predictor runs in the browser on the full file,
served at /keam-analytics/lastranks.json.
"""
import json
import os
import re
from functools import lru_cache
from statistics import median

from app.data import keam as D

LASTRANKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'keam', 'lastranks.json')
REF = '2026-1'


@lru_cache(maxsize=1)
def lastranks():
    with open(LASTRANKS, encoding='utf-8') as f:
        return json.load(f)


def district(name):
    best = None
    for town, dist in D.TOWN_DISTRICT:
        for m in re.finditer(re.escape(town), name):
            if best is None or m.start() > best[0]:
                best = (m.start(), dist)
    return best[1] if best else None


def region(dist):
    for r, ds in D.REGIONS.items():
        if dist in ds:
            return r
    return 'Other'


def short(n):
    n = re.sub(r'\s*,\s*', ', ', n).strip()
    return {'College of Engineering, Thiruvananthapuram': 'College of Engineering Trivandrum (CET)',
            'College of Engineering,Thiruvananthapuram': 'College of Engineering Trivandrum (CET)'}.get(n, n)


@lru_cache(maxsize=1)
def summary():
    d = lastranks()
    rids = [r['id'] for r in d['rounds']]
    sm = d['cats'].index('SM')
    cols = {c['c']: c for c in d['colleges']}
    by_col = {}
    fam = {}
    for row in d['rows']:
        by_col.setdefault(row['c'], []).append(row)
        for rid, ranks in row['r'].items():
            if ranks[sm] is not None:
                fam.setdefault(row['f'], {}).setdefault(rid, []).append(ranks[sm])
    colleges = []
    for code, c in cols.items():
        rows = by_col.get(code, [])
        out_rows = [{'n': r['n'], 'f': r['f'], 'sm': {rid: (r['r'].get(rid) or [None] * 13)[sm] for rid in rids}} for r in rows]
        ref = [r for r in out_rows if r['sm'].get(REF) is not None]
        best = min(ref, key=lambda r: r['sm'][REF]) if ref else None
        cs = [r['sm'][REF] for r in out_rows if r['f'] in ('CSE', 'AI', 'IT') and r['sm'].get(REF) is not None]
        dist = district(c['n'])
        colleges.append({'c': code, 'n': short(c['n']), 't': c['t'], 'type': D.TYPES[c['t']][0], 'district': dist, 'region': region(dist),
                         'nirf': D.NIRF.get(code), 'best': best, 'cs': min(cs) if cs else None, 'rows': sorted(out_rows, key=lambda r: r['sm'].get(REF) or 10 ** 6)})
    ranked = sorted([x for x in colleges if x['best']], key=lambda x: x['best']['sm'][REF])
    top = ranked[:20]
    top_rank = {t['c']: k + 1 for k, t in enumerate(top)}
    fam_stats = {f: {rid: {'n': len(v), 'med': int(median(v)), 'p10': int(sorted(v)[int(0.1 * (len(v) - 1))])} for rid, v in sorted(ys.items())} for f, ys in fam.items()}
    bands = [(0, 1000, 'up to 1k'), (1000, 5000, '1k–5k'), (5000, 10000, '5k–10k'), (10000, 20000, '10k–20k'), (20000, 40000, '20k–40k'), (40000, 10 ** 7, 'over 40k')]
    allsm = [r['sm'][REF] for x in colleges for r in x['rows'] if r['sm'].get(REF) is not None]
    hist = [[lab, sum(1 for v in allsm if lo < v <= hi)] for lo, hi, lab in bands]
    maprows = [[x['c'], x['n'], x['district'], x['t'], x['nirf'], x['best']['sm'][REF] if x['best'] else None, x['best']['n'] if x['best'] else None,
                len(x['rows']), x['cs'], top_rank.get(x['c'])] for x in colleges]
    return {'rounds': d['rounds'], 'ref': REF, 'top': top, 'fam': fam_stats, 'hist': hist, 'map': maprows,
            'n_col': len(cols), 'n_rows': len(d['rows']), 'n_courses': len({r['n'] for r in d['rows']})}


def payload():
    s = summary()
    return {'verified': D.VERIFIED, 'src': D.SRC, 'dates': D.DATES, 'pattern': D.PATTERN, 'elig': D.ELIGIBILITY, 'cats': D.CATS, 'otherCats': D.OTHER_CATS,
            'resvNote': D.RESERVATION_NOTE, 'types': D.TYPES, 'stats': D.STATS, 'ranklist': D.RANKLIST_2026, 'nirfNot': D.NIRF_NOT_KEAM,
            'famNames': D.FAMILY_NAMES, 'guide': D.BRANCH_GUIDE, 'regions': D.REGIONS, 'sites': D.SITES, **s}
