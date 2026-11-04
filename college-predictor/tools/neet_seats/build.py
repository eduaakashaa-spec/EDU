"""Build app/static/data/neet_seats_2025.json for the NEET MBBS seat matrix analytics page.

Usage: python tools/neet_seats/build.py <folder with 'MCC AIQ Total MBBS Seat 2025.pdf' (matrix as on 29 Oct 2025) and 'AIQ Total colleges list 2025.pdf' (matrix as on 10 Oct 2025)>
Both files are National Medical Commission seat matrices for MBBS, academic year 2025-26, with the seats of AY 2024-25 beside them, including AIIMS, other institutes of national
importance and JIPMER. Each row is read from the PDF text (row number, state, college, management, seats 2024-25, seats 2025-26, remarks). The builder checks every row number runs
without a gap, that no state or management type is unknown, and that the column totals equal the totals printed on the last page of each notice, so the page cannot drift from the file.
"""
import json
import os
import re
import sys
from collections import Counter

import pymupdf

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'static', 'data', 'neet_seats_2025.json')
STATES = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Chhattisgarh', 'Dadra & Nagar Haveli and Daman & Diu', 'Dadra and Nagar Haveli', 'Daman & Diu', 'Delhi', 'Goa',
          'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
          'Mizoram', 'Nagaland', 'Odisha', 'Pondicherry', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
STATE_KEY = {re.sub(r'\W+', '', s).lower(): s for s in STATES}
MGMT = {'Govt.': 'Government', 'Trust': 'Trust', 'Private': 'Private', 'Society': 'Society', 'Govt. (Society)': 'Government (society)', 'Deemed': 'Deemed university',
        'Deemed-to-be University': 'Deemed university', 'Deemed University': 'Deemed university', 'Central Govt.': 'Central government', 'Govt. (Trust)': 'Government (trust)'}
MGMT.update({'Company': 'Company'})
MGMT_UP = {k.upper(): v for k, v in MGMT.items()}
is_mg = lambda l: l.upper() in MGMT_UP  # noqa: E731
HEAD = re.compile(r'^(S\.No\.|State/UT|Name of college|Management of|college|No\. of seats|during AY|2024-25|for AY 2025-|26|Remarks|SEAT MATRIX AS ON.*|\d+ of \d+|Approval for New|Establishment|during AY:2025-26)$')

SKEY = lambda text: re.sub(r'\W+', '', text).lower()  # noqa: E731


def lines_of(pdf):
    d = pymupdf.open(pdf)
    out = []
    for p in d:
        out += [l.strip() for l in p.get_text().split('\n')]
    return out


def state_at(L, i):
    """Number of lines (1 to 3) that spell a state or UT at L[i:], else 0."""
    for m in (1, 2, 3):
        if i + m <= len(L) and re.sub(r'\W+', '', ' '.join(L[i:i + m])).lower() in STATE_KEY:
            return m
    return 0


def complete(L, a, b):
    """True when L[a:b] already holds a management type and two seat numbers, so the row is finished."""
    return any(is_mg(L[x]) and L[x + 1].isdigit() and L[x + 2].isdigit() for x in range(a, b - 2))


def read(pdf):
    L = [l for l in lines_of(pdf) if l and not HEAD.match(l)]
    fixed = []
    for l in L:                                         # two oddities: a management type glued to the name, and '-' meaning no seats
        if l.endswith(' Govt. (Society)') and len(l) > 20:
            fixed += [l[:-len(' Govt. (Society)')], 'Govt. (Society)']
        elif l == '-' and fixed and is_mg(fixed[-1]):
            fixed.append('0')
        else:
            fixed.append(l)
    L = fixed
    split = []
    for k, l in enumerate(L):                           # a row number, then 'State College name' on one line: split state from name
        hit = next((st for st in sorted(STATES, key=len, reverse=True) if l.startswith(st + ' ') and k and L[k - 1].isdigit() and len(L[k - 1]) <= 4), None)
        split += [hit, l[len(hit) + 1:]] if hit else [l]
    L = split
    is_total = lambda x: L[x].isdigit() and len(L[x]) >= 6 and x + 1 < len(L) and L[x + 1].isdigit() and len(L[x + 1]) >= 6  # noqa: E731  (a pin code inside a name is not a total)
    end = next(x for x in range(len(L)) if is_total(x))
    totals = [int(L[end]), int(L[end + 1])]
    # a row starts at an optional row number followed by a state; a few rows lose their number in the text layer, so the state is the anchor
    starts, printed_last = [], 0
    for i in range(end):
        if starts and starts[-1] == i - 1 and L[i - 1].isdigit():
            continue                                    # the state line right after a row number
        if starts and not complete(L, starts[-1], i):
            continue                                    # still inside the previous row
        if L[i].isdigit() and len(L[i]) <= 4 and state_at(L, i + 1):
            starts.append(i)
            printed_last = int(L[i])
        elif starts and state_at(L, i):
            starts.append(i)
    parsed = []
    for k, a in enumerate(starts):
        r = L[a:(starts[k + 1] if k + 1 < len(starts) else end)]
        if r[0].isdigit():
            r = r[1:]
        j = next(x for x in range(len(r) - 2) if is_mg(r[x]) and r[x + 1].isdigit() and r[x + 2].isdigit())
        head, mg, s24, s25, rest = r[:j], r[j], int(r[j + 1]), int(r[j + 2]), r[j + 3:]
        m = state_at(head, 0)
        assert m, head
        st = STATE_KEY[SKEY(' '.join(head[:m]))]
        name = re.sub(r'\s+', ' ', ' '.join(head[m:])).replace(' ,', ',').strip()
        parsed.append({'n': k + 1, 'state': {'Chattisgarh': 'Chhattisgarh', 'Pondicherry': 'Puducherry', 'Dadra and Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu', 'Dadra & Nagar Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu', 'Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'}.get(st, st), 'college': name, 'mgmt': MGMT_UP[mg.upper()], 's24': s24, 's25': s25,
                       'remark': ' '.join(rest).strip()})
    assert 0 <= len(parsed) - printed_last <= 3, (printed_last, len(parsed))      # a row or two in the PDF carries no serial number; the column totals are checked in build()
    return parsed, totals


def build(folder):
    new, tot_new = read(os.path.join(folder, 'MCC AIQ Total MBBS Seat 2025.pdf'))
    old, tot_old = read(os.path.join(folder, 'AIQ Total colleges list 2025.pdf'))
    for rows, tot, label in ((new, tot_new, '29 Oct'), (old, tot_old, '10 Oct')):
        a, b = sum(r['s24'] for r in rows), sum(r['s25'] for r in rows)
        print(label, len(rows), a, b, 'printed totals', tot)
        assert tot and [a, b] == tot, (label, a, b, tot)
    states = sorted({r['state'] for r in new})
    key = lambda r: (r['state'], re.sub(r'\W+', '', r['college']).lower())  # noqa: E731
    oldkey = {key(r): r for r in old}
    changed = []
    for r in new:
        o = oldkey.get(key(r))
        r['s25_oct10'] = o['s25'] if o else None
        if o is None or o['s25'] != r['s25']:
            changed.append({'state': r['state'], 'college': r['college'], 'mgmt': r['mgmt'], 'oct10': o['s25'] if o else None, 'oct29': r['s25']})
    out = {'built': '4 Nov 2026', 'asof': '29 October 2025', 'asof_old': '10 October 2025', 'states': states, 'rows': new,
           'totals': {'s24': tot_new[0], 's25': tot_new[1], 's25_oct10': tot_old[1], 'colleges': len(new), 'colleges_oct10': len(old)}, 'changed_since_oct10': changed}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB;', len(new), 'colleges;', len(states), 'states;', Counter(r['mgmt'] for r in new), 'changed since 10 Oct:', len(changed))


if __name__ == '__main__':
    build(sys.argv[1])
