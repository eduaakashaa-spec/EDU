"""Build app/data/mhtcet/cutoffs.json from the official MHT CET CAP Round I cut-off lists (State CET Cell, Maharashtra).

Sources (download the PDFs, then parse each with parse_cap.py):
  2023  https://fe2025.mahacet.org/2023/2023ENGG_CAP1_CutOff.pdf
  2024  https://fe2025.mahacet.org/2024/2024ENGG_CAP1_CutOff.pdf
  2025  https://fe2026.mahacet.org/2025/2025ENGG_CAP1_CutOff.pdf  (also embedded in fe2025.mahacet.org/ViewPublicDocument.aspx?MenuId=2449)
  2026  https://cappublicdocs2026.blob.core.windows.net/documents/2026ENGG_CAP1_MH_CutOff.pdf

usage:
  python -I tools/mhtcet/parse_cap.py 2025.pdf cap1_2025.json      (once per year)
  python -I tools/mhtcet/build_cutoffs.py cap1_2023.json cap1_2024.json cap1_2025.json cap1_2026.json

Output (compact, read by app/services/mhtcet.py):
  years   [2023, 2024, 2025, 2026]
  cats    base category codes, e.g. GOPEN, LOBC, TFWS (the S/H/O seat-level letter is removed)
  inst    [{c, n, city, st (status), hu (home university), k (kind), br: [{c, n, f (branch family), y: {year: {S|H|O: [[cat_index, percentile*1e4 int], ...]}}}]}]
  curve   {year: [[percentile, state merit rank], ...]} from every (rank, percentile) pair printed in that year's list
Seat levels: S state level (autonomous institutes), H home-university seats for home-university candidates, O other-than-home-university seats.
"""
import json
import os
import re
import sys

KEEP = ['GOPEN', 'GOBC', 'GSC', 'GST', 'GVJ', 'GNT1', 'GNT2', 'GNT3', 'GSEBC',
        'LOPEN', 'LOBC', 'LSC', 'LST', 'LVJ', 'LNT1', 'LNT2', 'LNT3', 'LSEBC',
        'EWS', 'TFWS', 'MI', 'PWDOPEN', 'DEFOPEN', 'ORPHAN']
NOSUFFIX = {'EWS', 'TFWS', 'MI', 'ORPHAN'}
FAMILIES = [
    ('AI', r'artificial|machine learning|data science|\bai\b|aiml|aids'),
    ('CSE', r'computer|software|cyber|internet of things|\biot\b|block ?chain'),
    ('IT', r'information technology'),
    ('ENTC', r'electronics|telecommunication|e\s*&\s*tc|vlsi|communication|instrumentation'),
    ('ELEC', r'electrical'),
    ('MECH', r'mechanical|production|automobile|mechatronic|robotic|automation|manufactur|aeronaut|aerospace'),
    ('CIVIL', r'civil|structural|construction|environment'),
    ('CHEM', r'chemical|petro|polymer|oil|paint|dyestuff|textile|fibres|plastic|food|pharma|biotech|bio[- ]?technology|surfactant|oleo'),
]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'mhtcet', 'cutoffs.json')


def family(name):
    n = name.lower()
    for f, rx in FAMILIES:
        if re.search(rx, n):
            # "Electronics and Computer Science" etc. stay with electronics only when no computer word
            if f == 'ENTC' and re.search(r'computer', n):
                return 'CSE'
            return f
    return 'OTHER'


def split_code(code, section):
    """GOPENS -> ('GOPEN', 'S'); TFWS -> ('TFWS', section level)."""
    if code in NOSUFFIX:
        return code, {'S': 'S', 'HH': 'H'}.get(section, 'O')
    if code[-1] in 'SHO' and code[:-1] in KEEP:
        return code[:-1], code[-1]
    return None, None


def kind(status):
    s = (status or '').lower()
    if s.startswith('government-aided'):
        return 'aided'
    if s.startswith('government'):
        return 'govt'
    if s.startswith('university') or s.startswith('deemed'):
        return 'univ'
    return 'pvt'


CITIES = ['Navi Mumbai', 'Mumbai', 'Thane', 'Kalyan', 'Dombivli', 'Badlapur', 'Bhiwandi', 'Vasai', 'Virar', 'Palghar', 'Panvel', 'Raigad', 'Lonere', 'Ratnagiri', 'Sindhudurg',
          'Pune', 'Pimpri', 'Chinchwad', 'Lonavala', 'Baramati', 'Satara', 'Karad', 'Sangli', 'Kolhapur', 'Ichalkaranji', 'Solapur', 'Pandharpur', 'Ahmednagar', 'Ahilyanagar',
          'Nashik', 'Dhule', 'Jalgaon', 'Nandurbar', 'Shirpur', 'Aurangabad', 'Chhatrapati Sambhajinagar', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Dharashiv', 'Nanded',
          'Parbhani', 'Hingoli', 'Amravati', 'Akola', 'Buldhana', 'Shegaon', 'Washim', 'Yavatmal', 'Wardha', 'Nagpur', 'Bhandara', 'Gondia', 'Chandrapur', 'Gadchiroli', 'Ballarpur']
NORM_CITY = {'Chinchwad': 'Pune', 'Pimpri': 'Pune', 'Chhatrapati Sambhajinagar': 'Aurangabad', 'Ahilyanagar': 'Ahmednagar', 'Dharashiv': 'Osmanabad', 'Dombivli': 'Thane',
             'Kalyan': 'Thane', 'Badlapur': 'Thane', 'Bhiwandi': 'Thane', 'Lonere': 'Raigad', 'Virar': 'Palghar', 'Vasai': 'Palghar', 'Andheri': 'Mumbai', 'Bandra': 'Mumbai', 'Chembur': 'Mumbai', 'Vashi': 'Navi Mumbai'}
KNOWN = {'16006': 'Pune', '06006': 'Pune'}


def city(name, code=''):
    if code in KNOWN:
        return KNOWN[code]
    best = None
    for c in CITIES:
        for m in re.finditer(r'\b' + re.escape(c) + r'\b', name, flags=re.I):
            if best is None or m.start() > best[0]:
                best = (m.start(), c)
    if best:
        return NORM_CITY.get(best[1], best[1])
    # fallback: the place after the last comma, e.g. "..., Tuljapur" or "..., Dist. Latur"
    parts = [p.strip(' .') for p in name.split(',') if p.strip(' .')]
    if len(parts) > 1:
        c = re.sub(r'^(Dist\.?|District|Tal\.?|Taluka|At\.?|Post)\s*', '', parts[-1], flags=re.I).strip(' .()')
        if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{2,24}", c):
            return NORM_CITY.get(c.title(), c.title())
    return ''


def norm_name(n):
    return re.sub(r'[^a-z]', '', n.lower())


OLD_YEARS_KEEP = {'GOPEN', 'LOPEN', 'GOBC', 'GSC', 'GST', 'EWS', 'TFWS'}


def main(paths):
    years = []
    raw = {}
    for p in paths:
        y = int(re.search(r'(20\d\d)', os.path.basename(p)).group(1))
        years.append(y)
        with open(p, encoding='utf-8') as f:
            raw[y] = json.load(f)
    years.sort()
    cat_ix = {c: i for i, c in enumerate(KEEP)}
    insts = {}
    pairs = {y: [] for y in years}
    latest = years[-1]
    # an institute that changed its code keeps one record under its latest code (matched on the same name)
    alias = {}
    by_name = {}
    for y in reversed(years):
        for ic, inst in raw[y].items():
            key = norm_name(inst['name'])
            if key in by_name and by_name[key] != ic:
                alias[ic] = by_name[key]
            else:
                by_name.setdefault(key, ic)
    for y in years:
        for ic0, inst in raw[y].items():
            ic = alias.get(ic0, ic0)
            rec = insts.setdefault(ic, {'c': ic, 'n': inst['name'], 'st': inst['status'], 'hu': '', 'br': {}})
            rec['n'] = inst['name']            # latest name wins
            rec['st'] = inst['status'] or rec['st']
            if inst.get('hu'):
                rec['hu'] = inst['hu']
            for bc0, br in inst['branches'].items():
                # same branch under a new institute code: match on name plus any letter suffix of the course code
                suffix = re.sub(r'^\d+', '', bc0)
                bkey = norm_name(br['name']) + '|' + suffix
                bc = next((k for k, v in rec['br'].items() if v.get('key') == bkey), None) or (ic + bc0[5:] if ic != ic0 else bc0)
                b = rec['br'].setdefault(bc, {'c': bc, 'n': br['name'], 'y': {}, 'key': bkey})
                b['n'] = br['name']
                out = {}
                for section, cats in br['levels'].items():
                    for code, (rank, pct) in cats.items():
                        if pct is None:
                            continue
                        if rank:
                            pairs[y].append((pct, rank))
                        base, lv = split_code(code, section)
                        if base is None:
                            continue
                        if y != latest and base not in OLD_YEARS_KEEP:
                            continue                 # earlier years: main categories only, to keep the file small
                        lvd = out.setdefault(lv, {})
                        if base not in lvd:          # first value wins (primary section comes first)
                            lvd[base] = pct
                if out:
                    b['y'][str(y)] = {lv: sorted([[cat_ix[c], int(round(v * 10000))] for c, v in d.items()]) for lv, d in out.items()}
    inst_list = []
    for ic in sorted(insts):
        r = insts[ic]
        brs = [{'c': b['c'], 'n': b['n'], 'f': family(b['n']), 'y': b['y']} for b in r['br'].values() if b['y']]
        if not brs:
            continue
        inst_list.append({'c': ic, 'n': r['n'], 'city': city(r['n'], ic), 'st': r['st'], 'hu': r['hu'], 'k': kind(r['st']), 'br': sorted(brs, key=lambda b: b['c'])})
    # percentile -> state merit rank curve: for each percentile threshold, the largest merit number printed at or above it
    curve = {}
    for y in years:
        ps = sorted(pairs[y], key=lambda t: -t[0])
        pts = []
        best = 0
        for pct, rank in ps:
            best = max(best, rank)
            pts.append((pct, best))
        grid = [100 - x / 100 for x in range(0, 101)] + [99 - x / 10 for x in range(1, 91)] + [90 - x for x in range(1, 90)]
        table = []
        j = 0
        for g in grid:
            while j < len(pts) and pts[j][0] >= g:
                j += 1
            table.append([round(g, 2), pts[j - 1][1] if j else 1])
        curve[str(y)] = table
    data = {'years': years, 'cats': KEEP, 'inst': inst_list, 'curve': curve,
            'source': 'State CET Cell, Maharashtra: CAP Round I cut-off lists for Maharashtra and minority seats, B.E./B.Tech'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    nb = sum(len(i['br']) for i in inst_list)
    print('institutes', len(inst_list), 'branches', nb, 'bytes', os.path.getsize(OUT))


if __name__ == '__main__':
    main(sys.argv[1:])
