"""Build app/data/tnea/cutoffs.json for /tnea-analytics from official TNEA 2026 documents (Directorate of Technical Education, Chennai).

Sources (tneaonline.org, downloaded Nov 2026):
  round 1, 2 and 3 general academic provisional allotment lists -> closing (lowest allotted) aggregate mark and rank per college, branch and allotted community
  general academic vacancy position after round 1               -> official college and branch names for every college-branch in counselling
Optional: the portal's "TNEA 2025 Final Cutoff.xlsx" (sheet "2025 cutoff"), kept as a separate, clearly labelled 2025 reference.

usage:
  python -I tools/tnea/build_cutoffs.py vacancy.pdf r1.pdf r2.pdf r3.pdf [2025.xlsx]

Only aggregates are written: application numbers are read to keep the 8-field rhythm of each allotment row and then discarded.
Output:
  rounds   [1, 2, 3]
  comms    ['OC','BC','BCM','MBC','SC','SCA','ST']
  colleges [{c, n, d (district, from the 2025 file), t (college type, from the 2025 file)}]
  branches {code: name}
  rows     [{c, b, r: {round: [[mark, rank, seats] or null per community]}, y25: [marks per community] (when in the 2025 file)}]
  curve    [[mark, typical rank], ...] from every allotted candidate in the three rounds (median rank near each half mark)
"""
import json
import os
import re
import sys

import pymupdf

HDR = {'S NO', 'APPLN NO', 'COMMUNITY', 'AGGREGATE', 'MARK', 'RANK', 'COLLEGE', 'CODE', 'BRANCH', 'ALLOTTED'}
COMMS_ALL = {'OC', 'BC', 'BCM', 'MBC', 'MBCDNC', 'MBCV', 'DNC', 'SC', 'SCA', 'ST'}
COMMS = ['OC', 'BC', 'BCM', 'MBC', 'SC', 'SCA', 'ST']
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'tnea', 'cutoffs.json')
HEAD = ('TAMILNADU ENGINEERING', 'DIRECTORATE OF TECHNICAL', 'GENERAL ACADEMIC', 'GOVT', 'Page ')


def lines(path):
    for page in pymupdf.open(path):
        for ln in page.get_text().split('\n'):
            ln = ln.strip()
            if ln:
                yield ln


def allotments(path):
    t = [ln for ln in lines(path) if ln not in HDR and not ln.startswith(HEAD)]
    recs, i, last = [], 0, 0
    while i + 7 < len(t):
        sno, appl, comm, mark, rank, col, br, ac = t[i:i + 8]
        if (sno.isdigit() and appl.isdigit() and comm in COMMS_ALL and re.fullmatch(r'\d{1,3}\.\d+', mark) and re.fullmatch(r'\d+[A-Z]?', rank)
                and col.isdigit() and re.fullmatch(r'[A-Z]{2}', br) and ac in COMMS_ALL and int(sno) == last + 1):
            recs.append((int(col), br, ac, float(mark), int(re.match(r'\d+', rank).group())))
            last = int(sno)
            i += 8
        else:
            i += 1
    return recs, last


def vacancy_lines(path):
    """Body lines of each page: everything after the column header that ends with SCA, ST (BC and SC are also branch codes, so only the header is skipped)."""
    for page in pymupdf.open(path):
        t = [ln.strip() for ln in page.get_text().split('\n') if ln.strip()]
        k = next((i for i in range(1, len(t)) if t[i] == 'ST' and t[i - 1] == 'SCA'), -1)
        for ln in t[k + 1:]:
            if not ln.startswith(HEAD):
                yield ln


def vacancy(path):
    """college code -> name, branch code -> name, from the vacancy list (code, name lines, branch code, branch name lines, 7 numbers)."""
    t = list(vacancy_lines(path))
    cols, brs, pairs = {}, {}, set()
    i = 0
    while i < len(t):
        if not t[i].isdigit():
            i += 1
            continue
        code = int(t[i])
        j = i + 1
        name = []
        while j < len(t) and not re.fullmatch(r'[A-Z]{2}', t[j]) and len(name) < 7:
            name.append(t[j])
            j += 1
        if j >= len(t) or not re.fullmatch(r'[A-Z]{2}', t[j]) or not name:
            i += 1
            continue
        bc = t[j]
        j += 1
        bname = []
        while j < len(t) and not t[j].isdigit() and len(bname) < 6:
            bname.append(t[j])
            j += 1
        nums = t[j:j + 7]
        if len(nums) == 7 and all(x.isdigit() for x in nums):
            cols[code] = re.sub(r'\s+', ' ', ' '.join(name)).strip()
            brs.setdefault(bc, re.sub(r'\s+', ' ', ' '.join(bname)).strip())
            pairs.add((code, bc))
            i = j + 7
        else:
            i += 1
    return cols, brs, pairs


def y2025(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)['2025 cutoff']
    out, info = {}, {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if not r[0] or not r[4]:
            continue
        info[int(r[0])] = (re.sub(r'\s+', ' ', str(r[1])).strip(), str(r[2] or '').strip(), str(r[3] or '').strip())
        vals = [r[k] for k in (6, 7, 8, 9, 10, 11, 12)]
        out[(int(r[0]), str(r[4]).strip())] = [round(float(v), 3) if isinstance(v, (int, float)) and v else None for v in vals]
    return out, info


def title(s):
    """Branch names arrive in capitals: Title Case with small words lower and acronyms kept."""
    small = {'and', 'of', 'for', 'in', 'the', 'with', '&'}
    keep = {'ai': 'AI', 'ar/vr': 'AR/VR', 'vlsi': 'VLSI', 'ss': 'SS', 'sw': 'SW', 'b.plan': 'B.Plan', 'm.tech.': 'M.Tech.', 'iot': 'IoT'}
    out = []
    s = re.sub(r'(\w)\(', r'\1 (', s)
    for k, w in enumerate(s.lower().split()):
        core = w.strip('()')
        if core in keep:
            out.append(w.replace(core, keep[core]))
        elif core in small and k:
            out.append(w)
        else:
            out.append(re.sub(r'[a-z]', lambda m: m.group().upper(), w, count=1))
    return re.sub(r'\s+', ' ', ' '.join(out)).replace('Bussiness', 'Business').replace('Structutural', 'Structural')


def main(args):
    vac, rounds = args[0], args[1:4]
    x25 = args[4] if len(args) > 4 else None
    cols, brs, pairs = vacancy(vac)
    print('vacancy list: colleges', len(cols), 'branch codes', len(brs), 'college-branch pairs', len(pairs))
    agg, pts = {}, []
    for k, p in enumerate(rounds, 1):
        recs, n = allotments(p)
        print(os.path.basename(p), 'records', len(recs), 'last S NO', n)
        for col, br, ac, mark, rank in recs:
            pts.append((mark, rank))
            if ac not in COMMS:
                continue
            cell = agg.setdefault((col, br), {}).setdefault(k, {}).setdefault(ac, [mark, rank, 0])
            if mark < cell[0] or (mark == cell[0] and rank > cell[1]):
                cell[0], cell[1] = mark, rank
            cell[2] += 1
    y25, info = y2025(x25) if x25 else ({}, {})
    for c, (n, _d, _t) in info.items():
        cols.setdefault(c, n)
    live = {k[0] for k in agg}
    keys = sorted(set(agg) | {k for k in y25 if k[0] in live})
    rows = []
    for key in keys:
        row = {'c': key[0], 'b': key[1], 'r': {}}
        for k, d in sorted(agg.get(key, {}).items()):
            row['r'][str(k)] = [d.get(c) for c in COMMS]
        if key in y25:
            row['y25'] = y25[key]
        rows.append(row)
    missing = sorted({r['c'] for r in rows} - set(cols))
    print('rows', len(rows), 'colleges without a name in the vacancy list', missing)
    nob = sorted({r['b'] for r in rows} - set(brs))
    print('branch codes without a name', nob)
    # mark -> typical rank: median rank of allotted candidates within 0.25 of each half-mark step (a few odd ranks do not distort it), kept monotonic
    from bisect import bisect_left, bisect_right
    from statistics import median
    pts.sort()
    marks = [m for m, _ in pts]
    curve, prev = [], 0
    for x in range(0, 301):                       # 200 down to 50 in steps of 0.5
        g = round(200 - x * 0.5, 1)
        lo, hi = bisect_left(marks, g - 0.25), bisect_right(marks, g + 0.25)
        r = int(median(rk for _, rk in pts[lo:hi])) if hi > lo else prev
        prev = max(prev, r)
        curve.append([g, prev])
    data = {'rounds': [1, 2, 3], 'comms': COMMS,
            'colleges': [{'c': c, 'n': cols[c], 'd': info.get(c, ('', '', ''))[1], 't': info.get(c, ('', '', ''))[2]} for c in sorted({r['c'] for r in rows}) if c in cols],
            'branches': {b: title(n) for b, n in sorted(brs.items())}, 'rows': [r for r in rows if r['c'] in cols], 'curve': curve,
            'source': 'TNEA 2026 (DOTE Chennai): Round 1-3 general academic provisional allotment lists and the vacancy position after Round 1'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print('colleges', len(data['colleges']), 'branches', len(data['branches']), 'rows', len(data['rows']), 'bytes', os.path.getsize(OUT))


if __name__ == '__main__':
    main(sys.argv[1:])
