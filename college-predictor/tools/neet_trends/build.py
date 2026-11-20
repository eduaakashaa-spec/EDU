"""Builds the NEET UG 2023-2025 comparison workbook (Excel) and the data file used by the web page.
Run from college-predictor/:  python tools/neet_trends/build.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import data as d  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

XLSX = os.path.join(ROOT, 'app', 'static', 'data', 'neet_trends_2023_2025.xlsx')
JS = os.path.join(ROOT, 'app', 'static', 'js', 'neet_trends_data.js')
Y = d.YEARS
NAVY, ORANGE = '0E3A8A', 'FF6B0A'


def pct(a, b):
    return round((b - a) * 100.0 / a, 1) if a else None


def build_json():
    h = d.HEADLINE
    out = {
        'years': Y,
        'headline': {str(y): dict(zip(['registered', 'appeared', 'absent', 'qualified'], h[y])) for y in Y},
        'category': {str(y): {k: dict(zip(['registered', 'appeared', 'qualified'], v)) for k, v in d.CATEGORY[y].items()} for y in Y},
        'gender': {str(y): {k: dict(zip(['registered', 'appeared', 'qualified'], v)) for k, v in d.GENDER[y].items()} for y in Y},
        'cutoff': {k: {'percentile': p, 'years': {str(y): {'max': v[0], 'cutoff': v[1], 'qualified': v[2]} for y, v in ys.items()}} for k, (p, ys) in d.CUTOFF.items()},
        'exam': {str(y): dict(zip(['date', 'questions', 'centres', 'cities', 'air1', 'top'], v)) for y, v in d.EXAM.items()},
        'states': {str(y): {k: dict(zip(['registered', 'appeared', 'qualified'], v)) for k, v in d.STATES[y].items()} for y in Y},
        'bands2025': d.BANDS_2025,
        'marksRank': {str(m): {str(y): v for y, v in ys.items()} for m, ys in d.MARKS_RANK.items()},
        'seatTotal': {str(y): v for y, v in d.SEAT_TOTAL.items()},
        'seatHistory': {str(y): v for y, v in d.SEAT_HISTORY.items()},
        'vacantGovt': {str(y): v for y, v in d.VACANT_GOVT.items()},
        'stateSeats': {k: dict(zip(['s23', 's24', 's25', 'c23', 'c24', 'c25'], v)) for k, v in d.STATE_SEATS.items()},
        'stateSplit': {k: dict(zip(['g23', 'p23', 'g25', 'p25'], v)) for k, v in d.STATE_SPLIT.items()},
        'rounds': d.ROUNDS,
        'allotted': {str(y): [{'allotted': a, 'upgraded': u} for a, u in v] for y, v in d.ALLOTTED.items()},
        'offered': {str(y): v for y, v in d.OFFERED.items()},
        'quotaMix': {str(y): [dict(zip(['aiq', 'deemed', 'nri'], r)) for r in v] for y, v in d.QUOTA_MIX.items()},
        'r1Status': {str(y): dict(zip(['reported', 'notReported', 'surrendered'], v)) for y, v in d.R1_STATUS.items()},
        'closing': {k: {str(y): v for y, v in ys.items()} for k, ys in d.CLOSING.items()},
        'lastGovtGeneral': {str(y): v for y, v in d.LAST_GOVT_GENERAL.items()},
        'lastGovtAny': {str(y): v for y, v in d.LAST_GOVT_ANY.items()},
        'lastGovtByRound': {str(y): v for y, v in d.LAST_GOVT_BY_ROUND.items()},
        'lastDeemed': {str(y): v for y, v in d.LAST_DEEMED.items()},
        'notes': d.NOTES,
        'sources': d.SOURCES,
    }
    return out


def sheet(wb, title, header, rows, widths=None, note=None, num_cols=None):
    ws = wb.create_sheet(title)
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(italic=True, color='5A6278')
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(len(header), 4))
        ws.cell(1, 1).alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[1].height = 42
        r0 = 3
    for j, hd in enumerate(header, 1):
        c = ws.cell(r0, j, hd)
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical='center')
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(i, j, v)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                c.number_format = '0.0' if isinstance(v, float) else '#,##0'
    for j in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(j, 16 if j > 1 else 34)
    ws.freeze_panes = ws.cell(r0 + 1, 2)
    return ws, r0


def build_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Read me'
    lines = [('NEET UG 2023, 2024, 2025: score statistics, MBBS seat matrix and MCC seat allotment', True),
             ('Prepared by EduAakashaA from published sources. Check neet.nta.nic.in, nmc.org.in and mcc.nic.in for the official figures.', False), ('', False),
             ('Sheets', True),
             ('Summary: the three years side by side with year-on-year change (formulas).', False),
             ('NEET score: registered, appeared, qualified, by category, gender, cut-off and top states; score bands and marks versus rank.', False),
             ('MBBS seats: national totals, seats and colleges by state, government and private split.', False),
             ('MCC allotment: MBBS seats allotted per round, quota mix, closing ranks and the last rank allotted.', False), ('', False),
             ('Notes on the data (please read)', True)] + [(n, False) for n in d.NOTES] + [('', False), ('Sources', True)] + [(f'{a}: {b}', False) for a, b in d.SOURCES]
    for i, (t, b) in enumerate(lines, 1):
        c = ws.cell(i, 1, t)
        c.font = Font(bold=b, size=13 if i == 1 else 11, color=NAVY if b else '000000')
        c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.column_dimensions['A'].width = 130

    # Summary with formulas
    s = wb.create_sheet('Summary')
    hd = ['Measure', '2023', '2024', '2025', 'Change 2023 to 2024 (%)', 'Change 2024 to 2025 (%)']
    for j, t in enumerate(hd, 1):
        c = s.cell(1, j, t)
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True)
    h, st, ut = d.HEADLINE, d.SEAT_TOTAL, d.ALLOTTED
    rows = [
        ('Registered', *[h[y][0] for y in Y]), ('Appeared', *[h[y][1] for y in Y]), ('Qualified', *[h[y][3] for y in Y]),
        ('General (UR/EWS) qualifying cut-off, marks', *[d.CUTOFF['UR / EWS'][1][y][1] for y in Y]),
        ('Top score', *[d.EXAM[y][5] for y in Y]),
        ('MBBS seats (NMC series, academic year starting in that year)', *[st[y]['seats'] for y in Y]),
        ('Medical colleges', *[st[y]['colleges'] for y in Y]),
        ('Government MBBS seats', *[st[y]['govt_seats'] for y in Y]), ('Private MBBS seats', *[st[y]['pvt_seats'] for y in Y]),
        ('MBBS seats allotted in MCC Round 1', *[ut[y][0][0] for y in Y]), ('MBBS seats allotted in MCC Round 2', *[ut[y][1][0] for y in Y]),
        ('MBBS seats allotted in MCC Round 3', *[ut[y][2][0] for y in Y]),
        ('Last general AIR allotted a government AIQ MBBS seat', *[d.LAST_GOVT_GENERAL[y] for y in Y]),
        ('AIIMS Delhi closing AIR (general, AIQ)', *[d.CLOSING['AIIMS Delhi'][y] for y in Y]),
    ]
    for i, r in enumerate(rows, 2):
        for j, v in enumerate(r, 1):
            c = s.cell(i, j, v)
            if j > 1:
                c.number_format = '#,##0'
        s.cell(i, 5, f'=ROUND((C{i}-B{i})*100/B{i},1)')
        s.cell(i, 6, f'=ROUND((D{i}-C{i})*100/C{i},1)')
    i = len(rows) + 2
    s.cell(i, 1, 'Qualified as a share of appeared (%)')
    for j, col in enumerate('BCD', 2):
        s.cell(i, j, f'=ROUND({col}4*100/{col}3,1)')
    s.cell(i + 1, 1, 'Government share of MBBS seats (%)')
    for j, col in enumerate('BCD', 2):
        s.cell(i + 1, j, f'=ROUND({col}9*100/({col}9+{col}10),1)')
    s.column_dimensions['A'].width = 56
    for col in 'BCDEF':
        s.column_dimensions[col].width = 18
    s.freeze_panes = 'B2'

    # NEET score
    sheet(wb, 'NEET headline', ['Measure', '2023', '2024', '2025'], [
        ['Registered', *[h[y][0] for y in Y]], ['Appeared', *[h[y][1] for y in Y]], ['Absent', *[h[y][2] for y in Y]], ['Qualified', *[h[y][3] for y in Y]],
        ['Exam date', *[d.EXAM[y][0] for y in Y]], ['Questions to attempt', *[d.EXAM[y][1] for y in Y]], ['Exam centres', *[d.EXAM[y][2] for y in Y]],
        ['Exam cities', *[d.EXAM[y][3] for y in Y]], ['Candidates at AIR 1', *[d.EXAM[y][4] for y in Y]], ['Top score', *[d.EXAM[y][5] for y in Y]]],
        note='Source: NTA press releases (2023, 2024); 2025 from the NTA notice as reproduced by Careers360 and Medical Dialogues.')
    rows = [[f'{k}', y, *v] for k in ('UR', 'EWS', 'OBC', 'SC', 'ST') for y in Y for v in [d.CATEGORY[y][k]]]
    sheet(wb, 'NEET by category', ['Category', 'Year', 'Registered', 'Appeared', 'Qualified'], rows)
    rows = [[k, y, *d.GENDER[y][k]] for k in ('Male', 'Female', 'Third gender') for y in Y]
    sheet(wb, 'NEET by gender', ['Gender', 'Year', 'Registered', 'Appeared', 'Qualified'], rows)
    rows = []
    for k, (p, ys) in d.CUTOFF.items():
        for y in Y:
            rows.append([k, p, y, f'{ys[y][0]}-{ys[y][1]}', ys[y][1], ys[y][2]])
    sheet(wb, 'NEET cut-offs', ['Class', 'Percentile', 'Year', 'Marks range', 'Cut-off marks', 'Candidates qualified'], rows)
    rows = [[k, y, *d.STATES[y][k]] for y in Y for k in d.STATES[y]]
    sheet(wb, 'NEET top states', ['State', 'Year', 'Registered', 'Appeared', 'Qualified'], rows, note='Top 10 states by qualified candidates in each year.')
    sheet(wb, 'NEET 2025 bands', ['Score band', 'Candidates (UR/EWS qualifiers)'], [list(b) for b in d.BANDS_2025])
    sheet(wb, 'Marks vs rank', ['Marks', 'AIR 2023', 'AIR 2024', 'AIR 2025'], [[m, *[d.MARKS_RANK[m][y] for y in Y]] for m in d.MARKS_RANK],
          note='Approximate All India Rank at a score, from news portals (not NTA). Blank = no reliable source.')

    # seats
    rows = [[f'{y}-{str(y + 1)[2:]}', d.SEAT_HISTORY[y], None, d.VACANT_GOVT.get(y)] for y in sorted(d.SEAT_HISTORY)]
    ws, r0 = sheet(wb, 'MBBS seats national', ['Academic year', 'MBBS seats', 'Added over previous year', 'Vacant UG seats in government colleges (excl. AIIMS, JIPMER)'], rows, widths={1: 16, 2: 16, 3: 22, 4: 34})
    for i in range(r0 + 2, r0 + 1 + len(rows)):
        ws.cell(i, 3, f'=B{i}-B{i - 1}').number_format = '#,##0'
    sheet(wb, 'MBBS govt vs private', ['Academic year', 'Government seats', 'Private seats', 'Government colleges', 'Private colleges', 'Total colleges'],
          [[f'{y}-{str(y + 1)[2:]}', st[y]['govt_seats'], st[y]['pvt_seats'], st[y]['govt_colleges'], st[y]['pvt_colleges'], st[y]['colleges']] for y in Y],
          note='Government and private seats come from Parliament replies and do not add exactly to the NMC total in the previous sheet.')
    rows = [[k, *v] for k, v in sorted(d.STATE_SEATS.items())]
    ws, r0 = sheet(wb, 'MBBS seats by state', ['State / UT', 'Seats 2023-24', 'Seats 2024-25', 'Seats 2025-26', 'Colleges 2023-24', 'Colleges 2024-25', 'Colleges 2025-26', 'Seat change 2023-24 to 2025-26', 'Change %'], rows, widths={8: 20, 9: 12})
    for i in range(r0 + 1, r0 + 1 + len(rows)):
        ws.cell(i, 8, f'=D{i}-B{i}').number_format = '#,##0'
        ws.cell(i, 9, f'=ROUND((D{i}-B{i})*100/B{i},1)')
    n = r0 + len(rows) + 1
    ws.cell(n, 1, 'Total (sum of states)').font = Font(bold=True)
    for j in range(2, 8):
        col = get_column_letter(j)
        ws.cell(n, j, f'=SUM({col}{r0 + 1}:{col}{n - 1})').number_format = '#,##0'
    sheet(wb, 'MBBS govt-pvt by state', ['State', 'Government 2023-24', 'Private 2023-24', 'Government 2025-26', 'Private 2025-26'], [[k, *v] for k, v in d.STATE_SPLIT.items()],
          note='Twelve largest states. The 2024-25 split was not published.')

    # allotment
    rows = []
    for y in Y:
        for k, rn in enumerate(d.ROUNDS):
            a, u = d.ALLOTTED[y][k]
            rows.append([y, rn, a, u, d.OFFERED[y][k]])
    sheet(wb, 'MCC allotment', ['Year', 'Round', 'MBBS seats allotted', 'of which upgraded', 'MBBS seats offered (clear + virtual vacancy)'], rows, widths={1: 8, 2: 16, 3: 20, 4: 18, 5: 30},
          note='Our count from the official MCC result and vacancy PDFs. Round 1 seats offered and Round 3 completeness: see Read me notes. Upgrade counts exist only for Rounds 2 and 3.')
    rows = [[y, f'Round {i + 1}', *d.QUOTA_MIX[y][i]] for y in Y for i in range(3)]
    sheet(wb, 'MCC quota mix', ['Year', 'Round', 'AIQ 15% and Open seat quota', 'Deemed / paid', 'NRI'], rows, note='MBBS allotments by quota. ESIC, Delhi University and IP University quotas are not shown.')
    rows = [[k, *[v[y] for y in Y]] for k, v in d.CLOSING.items()]
    sheet(wb, 'Closing ranks', ['Institute', 'Last AIR 2023', 'Last AIR 2024', 'Last AIR 2025'], rows,
          note='Highest All India Rank among General, non-PwD candidates holding an open-category MBBS seat in the 15% AIQ (open seat quota for AIIMS and JIPMER) after all rounds.')
    rows = []
    for y in Y:
        for k, rn in enumerate(d.ROUNDS):
            rows.append([y, rn, d.LAST_GOVT_BY_ROUND[y][k]])
    sheet(wb, 'Last govt AIR by round', ['Year', 'Round', 'Last general AIR, government AIQ MBBS'], rows)
    sheet(wb, 'Last rank overall', ['Year', 'Last general AIR, government MBBS', 'Last any-category AIR, government MBBS', 'Last AIR, deemed (any category)'],
          [[y, d.LAST_GOVT_GENERAL[y], d.LAST_GOVT_ANY[y], d.LAST_DEEMED[y]] for y in Y])
    wb.save(XLSX)


def main():
    os.makedirs(os.path.dirname(XLSX), exist_ok=True)
    build_xlsx()
    with open(JS, 'w', encoding='utf-8') as f:
        f.write('/* NEET UG 2023-2025 trends. Built by tools/neet_trends/build.py from tools/neet_trends/data.py; edit there, not here. */\nwindow.EA_NT = ')
        json.dump(build_json(), f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    print('wrote', XLSX, os.path.getsize(XLSX), 'bytes;', JS, os.path.getsize(JS), 'bytes')


if __name__ == '__main__':
    main()
