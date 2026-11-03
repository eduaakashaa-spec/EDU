"""Build app/data/files/josaa_cutoffs_2026.xlsx, the file the JoSAA predictor reads, from JoSAA_2026_Consolidated.xlsx.

Usage: python tools/josaa2026/build_predictor.py <folder with JoSAA_2026_Consolidated.xlsx>
Same seven columns as the 2025 file (Institute, Academic Program Name, Quota, Seat Type, Gender, Minimum Opening Rank, Maximum Closing Rank): one row per institute x programme x
quota x seat type x gender pool, with the lowest opening rank and the highest closing rank over Rounds 1 to 5 (Round 6 was not in the files supplied). A "P" suffix (a
preparatory-course rank) is stripped, as the loader always did; if that leaves an opening rank above the closing rank the two are swapped.
"""
import os
import sys

import openpyxl
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'files', 'josaa_cutoffs_2026.xlsx')


def rank(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip().rstrip('Pp')
    return int(s) if s.isdigit() else None


def main(folder):
    wb = openpyxl.load_workbook(os.path.join(folder, 'JoSAA_2026_Consolidated.xlsx'), read_only=True, data_only=True)
    rows = list(wb['Consolidated'].iter_rows(values_only=True))
    head = rows[0]
    ix = {h: i for i, h in enumerate(head)}
    out, swapped = [], 0
    for r in rows[1:]:
        opens = [rank(r[ix['R%d Opening' % k]]) for k in range(1, 6)]
        closes = [rank(r[ix['R%d Closing' % k]]) for k in range(1, 6)]
        opens, closes = [x for x in opens if x is not None], [x for x in closes if x is not None]
        if not opens or not closes:
            continue
        lo, hi = min(opens), max(closes)
        if lo > hi:
            lo, hi, swapped = hi, lo, swapped + 1
        out.append([r[ix['Institute']], r[ix['Programme']], r[ix['Quota']], r[ix['Seat Type']], r[ix['Gender Pool']], lo, hi])
    df = pd.DataFrame(out, columns=['Institute', 'Academic Program Name', 'Quota', 'Seat Type', 'Gender', 'Minimum Opening Rank', 'Maximum Closing Rank'])
    assert len(df) == 13292 and df['Institute'].nunique() == 138, (len(df), df['Institute'].nunique())
    assert (df['Minimum Opening Rank'] <= df['Maximum Closing Rank']).all()
    df.to_excel(OUT, index=False)
    print('wrote', OUT, len(df), 'rows,', df['Institute'].nunique(), 'institutes;', swapped, 'rows had opening above closing after stripping P and were swapped')


if __name__ == '__main__':
    main(sys.argv[1])
