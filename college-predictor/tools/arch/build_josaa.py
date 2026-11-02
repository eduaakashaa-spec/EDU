"""Build app/data/arch_josaa.json from the JoSAA 2026 round workbook and the DASA 2025/2026 workbook.
Only Architecture (B.Arch) and Planning (B.Plan) programmes are kept; Naval Architecture (B.Tech) is left out.
Usage: python tools/arch/build_josaa.py <JoSAA xlsx> <DASA xlsx> [out json]
Row layout in the output: i = institute index, p = programme (A or P), q = quota, s = seat type, g = gender (N neutral, F female-only),
o = opening rank per round, c = closing rank per round (None where the seat was not offered in that round)."""
import json
import os
import sys
import warnings

warnings.filterwarnings('ignore')
import openpyxl  # noqa: E402

ROUNDS = ['Round1', 'Round2', 'Round3', 'Round4', 'Round5']
GENDER = {'Gender-Neutral': 'N'}


def keep(prog):
    return prog and ('Architecture (5 Years' in prog or 'Planning (4 Years' in prog)


def gender(g):
    return 'N' if g == 'Gender-Neutral' else 'F'


def main(josaa, dasa, out):
    wb = openpyxl.load_workbook(josaa, read_only=True, data_only=True)
    rows = {}
    for ri, sh in enumerate(ROUNDS):
        for r in wb[sh].iter_rows(min_row=2, values_only=True):
            if not r[0] or not keep(r[1]):
                continue
            key = (r[0], 'A' if 'Architecture' in r[1] else 'P', r[2], r[3], gender(r[4]))
            e = rows.setdefault(key, dict(o=[None] * 5, c=[None] * 5))
            e['o'][ri] = r[5]
            e['c'][ri] = r[6]
    inst = sorted({k[0] for k in rows})
    idx = {n: i for i, n in enumerate(inst)}
    data = []
    for k, v in sorted(rows.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3], kv[0][4])):
        data.append(dict(i=idx[k[0]], p=k[1], q=k[2], s=k[3], g=k[4], o=v['o'], c=v['c']))
    wd = openpyxl.load_workbook(dasa, read_only=True, data_only=True)
    ws = wd['Comparison']
    das = []
    for r in ws.iter_rows(values_only=True):
        if len(r) > 12 and isinstance(r[3], str) and r[4] == 'Architecture/Planning':
            das.append(dict(inst=r[1], quota=r[2], prog=r[3], status=r[6], r1_25=r[7], r1_26=r[8], f25=r[10], f26=r[11]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(dict(institutes=inst, rows=data, dasa=das), open(out, 'w', encoding='utf-8'), separators=(',', ':'))
    print(len(inst), 'institutes', len(data), 'rows', len(das), 'dasa rows', os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'data', 'arch_josaa.json'))
