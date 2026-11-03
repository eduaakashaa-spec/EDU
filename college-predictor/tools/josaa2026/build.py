"""Build app/static/data/josaa_2026.json for the JoSAA 2026 seat allotment and analytics page.

Usage: python tools/josaa2026/build.py <folder with JoSAA_2026_Consolidated.xlsx and JoSAA_2026_Architecture_Planning.xlsx>
Rank cells come from the Consolidated sheet (one row per institute x programme x quota x seat type x gender pool, Rounds 1 to 5, seats for the 32 NIT+ institutes).
Every headline figure is computed here from those rows and asserted against the figures printed on the workbook's own Summary tab, so the page cannot drift from the file.
Ranks with a "P" suffix are preparatory-course ranks: kept as text, left out of every numeric calculation.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

import openpyxl

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'static', 'data', 'josaa_2026.json')
TYPES = ['IIT', 'IISc', 'NIT+', 'IIIT', 'GFTI']
SEAT_TYPES = ['OPEN', 'OPEN (PwD)', 'EWS', 'EWS (PwD)', 'OBC-NCL', 'OBC-NCL (PwD)', 'SC', 'SC (PwD)', 'ST', 'ST (PwD)']
QUOTA_NAMES = {'AI': 'All India', 'HS': 'Home State', 'OS': 'Other State', 'GO': 'Goa', 'JK': 'Jammu and Kashmir', 'LA': 'Ladakh'}


def short(name):
    """Short display name: IIT X, NIT X (any 'National Institute of Technology' name), IIIT X; others unchanged."""
    n = name.strip()
    m = re.search(r'National Institute of Technology,?\s*(.*)$', n)
    if m and not n.startswith('Indian Institute'):
        return 'NIT ' + m.group(1).strip()
    n = re.sub(r'^Indian Institute of Technology\s*', 'IIT ', n)
    n = re.sub(r'^Indian Institute of Information Technology,?\s*', 'IIIT ', n)
    n = re.sub(r'^IIIT \(IIIT\)\s*,?\s*', 'IIIT ', n)
    n = re.sub(r'^IIIT,\s*', 'IIIT ', n)
    return n.strip()


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def read_sheet(wb, name):
    rows = list(wb[name].iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def build(folder):
    cons = openpyxl.load_workbook(os.path.join(folder, 'JoSAA_2026_Consolidated.xlsx'), read_only=True, data_only=True)
    ap = openpyxl.load_workbook(os.path.join(folder, 'JoSAA_2026_Architecture_Planning.xlsx'), read_only=True, data_only=True)
    data = read_sheet(cons, 'Consolidated')

    insts, inst_ix = [], {}
    progs, prog_ix = [], {}
    rows = []
    for r in data:
        key = r['Institute']
        if key not in inst_ix:
            inst_ix[key] = len(insts)
            insts.append([short(key), key, r['Institute Type']])
        pk = (r['Programme'], r['Branch'], r['Degree'], r['Duration (Yrs)'])
        if pk not in prog_ix:
            prog_ix[pk] = len(progs)
            progs.append([r['Branch'], r['Programme'], r['Degree'], r['Duration (Yrs)']])
        st = r['Seat Type']
        gp = 1 if str(r['Gender Pool']).startswith('Female') else 0
        ranks = []
        for k in range(1, 6):
            ranks += [r['R%d Opening' % k], r['R%d Closing' % k]]
        rows.append([inst_ix[key], prog_ix[pk], r['Quota'], SEAT_TYPES.index(st), gp, r['Seats (NIT+ only)'] or 0] + ranks + [r['Rounds Reported (of 5)'], r['Status'], r['Direction']])

    # ---- analytics computed from the rows
    ntype = {i: insts[i][2] for i in range(len(insts))}
    with_ranks = [r for r in rows if r[16] and r[16] > 0]
    seats_total = sum(r[5] for r in rows)
    never = [r for r in rows if r[17] == 'Never allotted']
    cov = []
    for k in range(5):
        have = [r for r in rows if r[7 + 2 * k] is not None]
        nit = [r for r in have if ntype[r[0]] == 'NIT+']
        cov.append({'round': k + 1, 'cells': len(have), 'nit_cells': len(nit), 'nit_seats': sum(r[5] for r in nit)})
    drift = {}
    for t in TYPES + ['All']:
        sel = [r for r in data if t == 'All' or r['Institute Type'] == t]
        sh = [r['Shift %'] for r in sel if isinstance(r['Shift %'], (int, float))]
        dr = Counter(r['Direction'] for r in sel if r['Direction'])
        n = sum(dr.values())
        drift[t] = {'institutes': len({r['Institute'] for r in sel}), 'programmes': len({(r['Institute'], r['Programme']) for r in sel}), 'cells': sum(1 for r in sel if (r['Rounds Reported (of 5)'] or 0) > 0),
                    'seats': sum(r['Seats (NIT+ only)'] or 0 for r in sel), 'avg_shift': round(sum(sh) / len(sh), 4) if sh else None,
                    'relaxed': round(dr['Relaxed'] / n, 4) if n else None, 'tightened': round(dr['Tightened'] / n, 4) if n else None, 'unchanged': round(dr['Unchanged'] / n, 4) if n else None}
    seat_by = {s: [0, 0] for s in SEAT_TYPES}
    quota_seats = Counter()
    for r in rows:
        seat_by[SEAT_TYPES[r[3]]][r[4]] += r[5]
        quota_seats[r[2]] += r[5] if ntype[r[0]] == 'NIT+' else 0
    never_by = {s: [0, 0] for s in SEAT_TYPES}
    for r in never:
        never_by[SEAT_TYPES[r[3]]][0] += 1
        never_by[SEAT_TYPES[r[3]]][1] += r[5]
    by_inst = []
    for i, (sn, full, t) in enumerate(insts):
        mine = [r for r in rows if r[0] == i]
        sh = [d['Shift %'] for d in data if d['Institute'] == full and isinstance(d['Shift %'], (int, float))]
        by_inst.append({'i': i, 'type': t, 'programmes': len({r[1] for r in mine}), 'seats': sum(r[5] for r in mine), 'cells': sum(1 for r in mine if r[16]), 'never': sum(1 for r in mine if r[17] == 'Never allotted'),
                        'shift': round(sum(sh) / len(sh), 4) if sh else None})

    # ---- Architecture and Planning workbook
    ap_rows = [r for r in read_sheet(ap, 'By Institute') if r.get('Institute')]
    ap_inst = [{'type': r['Institute Type'], 'inst': short(r['Institute']), 'prog': r['Programme'], 'seats': r['Seats (NIT+ only)'] if isinstance(r['Seats (NIT+ only)'], (int, float)) else None,
                'cells': r['Allotment Cells'], 'r1': r['Cells with Ranks in R1'], 'r5': r['Cells with Ranks in R5'], 'never': r['Seat Cells Never Allotted'] if isinstance(r['Seat Cells Never Allotted'], (int, float)) else None} for r in ap_rows]
    ap_open = []
    for r in [x for x in read_sheet(ap, 'OPEN Cutoffs') if x.get('Institute')]:
        ap_open.append({'type': r['Institute Type'], 'inst': short(r['Institute']), 'prog': r['Programme'], 'quota': r['Quota'], 'r1o': r['OPEN-GN R1 Opening'], 'r1c': r['OPEN-GN R1 Closing'], 'r5c': r['OPEN-GN R5 Closing'],
                        'shift': r['Closing Shift R1→R5'], 'f1c': r.get('OPEN Female-only R1 Closing')})
    ap_seats = sum(r['seats'] or 0 for r in ap_inst)

    # ---- checks against the workbook's own Summary tab
    assert len(insts) == 138 and seats_total == 25162 and len(with_ranks) == 13292 and len(never) == 336 and sum(r[5] for r in never) == 362, (len(insts), seats_total, len(with_ranks), len(never))
    assert [c['cells'] for c in cov] == [13292, 13047, 12989, 12968, 12936] and [c['nit_cells'] for c in cov] == [6754, 6668, 6656, 6649, 6642], cov
    assert [seat_by[s][0] + seat_by[s][1] for s in SEAT_TYPES] == [9623, 498, 2349, 131, 6214, 328, 3538, 184, 2194, 103], seat_by
    assert drift['IIT']['cells'] == 3395 and drift['NIT+']['cells'] == 6754 and drift['GFTI']['cells'] == 1647 and drift['IIIT']['cells'] == 1456 and drift['IISc']['cells'] == 40
    assert abs(drift['NIT+']['avg_shift'] - 0.1686) < 0.001 and abs(drift['All']['relaxed'] - 0.7453) < 0.001, drift
    out = {'built': '2 Nov 2026', 'insts': insts, 'progs': progs, 'seat_types': SEAT_TYPES, 'quotas': QUOTA_NAMES,
           'rows': rows, 'cols': 'inst,prog,quota,seat,gender,seats,r1o,r1c,r2o,r2c,r3o,r3c,r4o,r4c,r5o,r5c,rounds,status,direction',
           'stats': {'institutes': len(insts), 'nit_institutes': drift['NIT+']['institutes'], 'programmes': drift['All']['programmes'], 'cells': len(with_ranks), 'seats': seats_total,
                     'seat_cells': sum(1 for r in rows if r[5] > 0), 'never_cells': len(never), 'never_seats': sum(r[5] for r in never), 'coverage': cov, 'drift': drift,
                     'seat_by': seat_by, 'quota_seats': dict(quota_seats), 'never_by': never_by, 'female_seats': sum(v[1] for v in seat_by.values())},
           'by_inst': by_inst,
           'ap': {'inst': ap_inst, 'open': ap_open, 'seats': ap_seats}}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB;', len(rows), 'rows;', len(insts), 'institutes;', len(progs), 'programmes; A&P seats', ap_seats)


if __name__ == '__main__':
    build(sys.argv[1])
