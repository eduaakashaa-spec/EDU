"""Build app/data/cs_stream_tnea.json for the member page /computer-science-stream.

From the TNEA 2026 allotment file held by the portal (app/data/tnea/cutoffs.json: every college and every branch with allotments) it counts how many Tamil Nadu counselling colleges offer each
computer-stream branch family, and lists the computer-stream branches of a small set of NIRF-listed colleges (each pairing of NIRF name and TNEA college code checked by hand below).
Run from college-predictor/:  python tools/cs_stream/build_tnea.py
"""
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'app', 'data', 'tnea', 'cutoffs.json')
NIRF = os.path.join(ROOT, 'app', 'data', 'eng_colleges.json')
OUT = os.path.join(ROOT, 'app', 'data', 'cs_stream_tnea.json')

# TNEA branch code -> family (same families as the JoSAA file). (SS) codes are self-supported batches of the same branch.
FAMILY = {
    'core': ['CS', 'CM', 'CJ', 'XS', 'TS'],
    'it': ['IT', 'IM'],
    'aids': ['AD', 'AT', 'AI', 'AL', 'AM', 'CA', 'CF', 'CG', 'DS', 'DV', 'GL'],
    'cyber': ['CY', 'SC', 'SB'],
    'biz': ['CB', 'CU', 'CW'],
    'hybrid': ['CI', 'CO', 'CD', 'CV', 'EX', 'EF', 'EU', 'RI'],
}
CODE_FAMILY = {c: f for f, cs in FAMILY.items() for c in cs}

# NIRF Engineering name -> TNEA college code, each pair read side by side (same institution)
PAIRS = {
    'Anna University': 1,                                           # University Departments of Anna University, CEG campus
    'PSG College of Technology': 2006,
    'Coimbatore Institute of Technology': 2007,
    'Sri Krishna College of Engineering and Technology': 2718,
    'Kumaraguru College of Technology': 2712,
    'KPR Institute of Engineering and Technology': 2764,
    'Easwari Engineering College': 1304,
    'Sri Ramakrishna Engineering College': 2719,
    'Hindusthan College of Engineering and Technology': 2708,
    'K. Ramakrishnan College of Engineering': 3830,
    'K. Ramakrishnan College of Technology': 3701,
}


def main():
    t = json.load(open(SRC, encoding='utf-8'))
    names = t['branches']
    colleges = {c['c']: c for c in t['colleges']}
    by_col = defaultdict(set)
    for r in t['rows']:
        by_col[r['c']].add(r['b'])
    fam_cols = {f: set() for f in FAMILY}
    for cid, bs in by_col.items():
        for b in bs:
            if b in CODE_FAMILY:
                fam_cols[CODE_FAMILY[b]].add(cid)
    total = len([c for c in colleges if by_col.get(c)])
    L = {c['name']: c for c in json.load(open(NIRF, encoding='utf-8'))['colleges']}
    listed = []
    for nirf_name, cid in PAIRS.items():
        c = L.get(nirf_name)
        if not c or cid not in colleges:
            print('MISSING', nirf_name, cid)
            continue
        progs = sorted({names[b] for b in by_col.get(cid, ()) if b in CODE_FAMILY and not names[b].endswith('(SS)')} | {names[b].replace(' (SS)', '') for b in by_col.get(cid, ()) if b in CODE_FAMILY and names[b].endswith('(SS)')})
        fams = sorted({CODE_FAMILY[b] for b in by_col.get(cid, ()) if b in CODE_FAMILY}, key=list(FAMILY).index)
        listed.append({'name': nirf_name, 'tnea_college': colleges[cid]['n'].split(',')[0][:90], 'code': cid, 'nirf_rank': c['rank'], 'nirf_band': c['band'], 'city': c['city'], 'programmes': progs, 'families': fams})
    out = {'source': t['source'], 'colleges_with_allotments': total,
           'family_counts': {f: len(cs) for f, cs in fam_cols.items()}, 'listed': sorted(listed, key=lambda x: (x['nirf_rank'] is None, x['nirf_rank'] or 999, x['name']))}
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('colleges with allotments:', total)
    print('family counts:', out['family_counts'])
    for x in out['listed']:
        print(' ', x['nirf_rank'], x['name'], '|', x['programmes'])


if __name__ == '__main__':
    main()
