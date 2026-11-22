"""MHT CET analytics: builds the payload for /mht-cet-analytics from app/data/mhtcet.py (facts) and app/data/mhtcet/cutoffs.json (official CAP Round I cut-offs).

Open cut-off of a course = GOPEN at State level, else GOPEN on Home University seats; a women-only college has only LOPEN, which is then used and flagged.
Top 20 = the 20 institutes with the highest open cut-off in any course in the latest year (demand in CAP Round I), shown with their NIRF 2025 engineering rank.
The college predictor runs in the browser on the full cut-off file served at /mht-cet-analytics/cutoffs.json.
"""
import json
import os
from functools import lru_cache
from statistics import median

from app.data import mhtcet as D

CUTOFFS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'mhtcet', 'cutoffs.json')


@lru_cache(maxsize=1)
def cutoffs():
    with open(CUTOFFS, encoding='utf-8') as f:
        return json.load(f)


def district(inst):
    """District as named in the Maharashtra map file, or None when the college name gives no town we can place."""
    c = inst['c']
    return D.INST_DISTRICT.get(c) or D.TOWN_BY_REGION.get((inst.get('city') or '', c[:2])) or D.TOWN_DISTRICT.get(inst.get('city') or '')


def region(city):
    for r, cities in D.REGIONS.items():
        if city in cities:
            return r
    return 'Other'


def open_cut(branch, year, cats):
    """(percentile, seat label) for a course in a year, or (None, None)."""
    y = branch['y'].get(str(year)) or {}
    gi, li = cats.index('GOPEN'), cats.index('LOPEN')
    for lv, ix, label in (('S', gi, 'State'), ('H', gi, 'Home Univ'), ('S', li, 'Women, State'), ('H', li, 'Women, Home Univ')):
        for ci, p in y.get(lv, []):
            if ci == ix:
                return p / 1e4, label
    return None, None


def short_name(n):
    rep = [("Veermata Jijabai Technological Institute(VJTI), Matunga, Mumbai", 'VJTI Mumbai'), ('Institute of Chemical Technology, Matunga, Mumbai', 'ICT Mumbai'),
           ("Bhartiya Vidya Bhavan's Sardar Patel Institute of Technology , Andheri, Mumbai", 'Sardar Patel Institute of Technology (SPIT), Mumbai'),
           ("Shri Vile Parle Kelvani Mandal's Dwarkadas J. Sanghvi College of Engineering, Vile Parle,Mumbai", 'DJ Sanghvi College of Engineering, Mumbai'),
           ('Pimpri Chinchwad Education Trust, Pimpri Chinchwad College of Engineering, Pune', 'Pimpri Chinchwad College of Engineering (PCCOE), Pune'),
           ("Bansilal Ramnath Agarawal Charitable Trust's Vishwakarma Institute of Technology, Bibwewadi, Pune", 'Vishwakarma Institute of Technology (VIT), Pune'),
           ("MKSSS's Cummins College of Engineering for Women, Karvenagar,Pune", 'Cummins College of Engineering for Women, Pune'),
           ('Pune Institute of Computer Technology', 'Pune Institute of Computer Technology (PICT)'),
           ('Shri Guru Gobind Singhji Institute of Engineering and Technology, Nanded', 'SGGS Institute of Engineering & Technology, Nanded')]
    for a, b in rep:
        if n.strip() == a:
            return b
    return n.strip()


def kind_label(k, st):
    return {'govt': 'Government', 'aided': 'Government-aided', 'univ': 'University / deemed'}.get(k, 'Private unaided') + (' · autonomous' if 'Autonomous' in (st or '') else '') \
        + (' · minority' if 'Minority' in (st or '') else '')


@lru_cache(maxsize=1)
def summary():
    d = cutoffs()
    cats, years = d['cats'], d['years']
    last = years[-1]
    insts = []
    fam = {}
    for i in d['inst']:
        rows = []
        for b in i['br']:
            cuts = {y: open_cut(b, y, cats) for y in years}
            rows.append({'c': b['c'], 'n': b['n'], 'f': b['f'], 'cut': {str(y): (round(v[0], 4) if v[0] is not None else None) for y, v in cuts.items()},
                         'seat': cuts[last][1]})
            for y, (p, label) in cuts.items():
                if p is not None and label in ('State', 'Home Univ'):
                    fam.setdefault(b['f'], {}).setdefault(y, []).append(p)
        best = max((r for r in rows if r['cut'][str(last)] is not None), key=lambda r: r['cut'][str(last)], default=None)
        nirf = D.NIRF.get(i['c'])
        insts.append({'c': i['c'], 'n': short_name(i['n']), 'full': i['n'], 'city': {'Andheri': 'Mumbai'}.get(i['city'], i['city'] or ''), 'region': region(i['city']), 'kind': kind_label(i['k'], i['st']),
                      'hu': i['hu'], 'nirf': (nirf[0] or nirf[1]) if nirf else None, 'best': best, 'rows': rows})
    ranked = sorted([x for x in insts if x['best']], key=lambda x: -x['best']['cut'][str(last)])
    top = ranked[:20]
    fam_stats = {}
    for f, ys in fam.items():
        fam_stats[f] = {str(y): {'n': len(v), 'med': round(median(v), 2), 'p90': round(sorted(v)[int(0.9 * (len(v) - 1))], 2), 'p25': round(sorted(v)[int(0.25 * (len(v) - 1))], 2)} for y, v in sorted(ys.items())}
    nb = sum(len(i['br']) for i in d['inst'])
    # map and infographics: one compact row per institute
    # [code, short name, district, kind, autonomous, nirf, best latest-year open cut, best course, courses, best latest-year Computer/IT/AI open cut, top-20 rank]
    top_rank = {t['c']: k + 1 for k, t in enumerate(top)}
    raw = {i['c']: i for i in d['inst']}
    rows = []
    for x in insts:
        i = raw[x['c']]
        cs = [r['cut'][str(last)] for r in x['rows'] if r['f'] in ('CSE', 'IT', 'AI') and r['cut'][str(last)] is not None and (r['seat'] or '').find('Women') < 0]
        rows.append([x['c'], x['n'], district(i), i['k'], 'Autonomous' in (i['st'] or ''), x['nirf'], x['best']['cut'][str(last)] if x['best'] else None,
                     x['best']['n'] if x['best'] else None, len(x['rows']), max(cs) if cs else None, top_rank.get(x['c'])])
    bands = [(99, 100.01, '99+'), (97, 99, '97–99'), (95, 97, '95–97'), (90, 95, '90–95'), (80, 90, '80–90'), (60, 80, '60–80'), (40, 60, '40–60'), (0, 40, 'under 40')]
    allcuts = [r['cut'][str(last)] for x in insts for r in x['rows'] if r['cut'][str(last)] is not None]
    hist = [[lab, sum(1 for v in allcuts if lo <= v < hi)] for lo, hi, lab in bands]
    return {'years': years, 'top': top, 'fam': fam_stats, 'curve': d['curve'], 'n_inst': len(d['inst']), 'n_br': nb,
            'n_nirf': sum(1 for x in insts if x['nirf']), 'nirf_cap': [x for x in ranked if x['nirf']], 'map': rows, 'hist': hist}


def payload():
    s = summary()
    return {'verified': D.VERIFIED, 'src': D.SRC, 'dates': D.DATES, 'pattern': D.PATTERN, 'candidates': D.CANDIDATES, 'elig': D.ELIGIBILITY, 'cand': D.CANDIDATURE,
            'seats': D.SEATS, 'resv': D.RESERVATION, 'resvNote': D.RESERVATION_NOTE, 'stats26': D.STATS_2026, 'marks': D.MARKS_PCT, 'nirfNotCap': D.NIRF_NOT_CAP,
            'unis': D.UNIVERSITIES, 'regions': list(D.REGIONS) + ['Other'], 'regionMap': D.REGIONS, 'famNames': D.FAMILY_NAMES, 'guide': D.BRANCH_GUIDE, 'sites': D.SITES, **s}
