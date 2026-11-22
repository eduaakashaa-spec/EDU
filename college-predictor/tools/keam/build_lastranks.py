"""Build app/data/keam/lastranks.json from the official CEE Kerala KEAM engineering last-rank PDFs.

Sources (download, then parse each with parse_lastrank.py):
  2025 Phase 1  https://cee.kerala.gov.in/keam2025/list/lastrank/p1_last_rank_final.pdf
  2025 Phase 2  https://cee.kerala.gov.in/keam2025/list/lastrank/last_rank_engg_p2_final.pdf
  2026 Phase 1  https://cee.kerala.gov.in/keam2026/list/lastrank/lastrank_p1.pdf
  2026 Phase 2  https://cee.kerala.gov.in/keam2026/list/lastrank/lastrank_engg_p2.pdf
usage:
  python -I tools/keam/parse_lastrank.py lastrank_p1.pdf 2026_p1.json        (once per file)
  python -I tools/keam/build_lastranks.py 2025_p1.json 2025_p2.json 2026_p1.json 2026_p2.json
File names must start with <year>_p<phase>. Output (read by app/services/keam.py):
  rounds   [{id: "2026-1", year, phase, date}]
  cats     category codes in a fixed order (SM, EZ, MU, BH, LA, DV, VK, BX, KN, KU, SC, ST, EW)
  colleges [{c, n, t (G govt/aided, N govt-controlled self-financing, S private self-financing)}]
  rows     [{c (college), n (course), f (branch family), r: {round_id: [last rank per category or null, ...]}, o: {round_id: {other category: rank}}}]
"""
import json
import os
import re
import sys

CATS = ['SM', 'EZ', 'MU', 'BH', 'LA', 'DV', 'VK', 'BX', 'KN', 'KU', 'SC', 'ST', 'EW']
URLS = {'2025-1': 'https://cee.kerala.gov.in/keam2025/list/lastrank/p1_last_rank_final.pdf',
        '2025-2': 'https://cee.kerala.gov.in/keam2025/list/lastrank/last_rank_engg_p2_final.pdf',
        '2026-1': 'https://cee.kerala.gov.in/keam2026/list/lastrank/lastrank_p1.pdf',
        '2026-2': 'https://cee.kerala.gov.in/keam2026/list/lastrank/lastrank_engg_p2.pdf'}
FAMILIES = [
    ('AI', r'artificial|machine learning|data science'),
    ('CSE', r'computer|cyber|block ?chain|internet of things|business systems'),
    ('IT', r'information technology'),
    ('ELEC', r'electrical'),
    ('ENTC', r'electronics|instrumentation|communication|vlsi'),
    ('MECH', r'mechanical|automobile|production|mechatronic|robotic|automation|aeronautical|industrial|naval|metallurg|safety|printing'),
    ('CIVIL', r'civil'),
    ('CHEM', r'chemical|polymer|bio ?technology|biochemical|food|dairy|agricultur|bio ?medical'),
]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'keam', 'lastranks.json')


CANON = {}   # slug -> display name (the longest spelling seen)


def slug(n):
    return re.sub(r'[^a-z]', '', re.sub(r'\bengineering\b', '', n.lower()))


def norm_course(n):
    n = re.sub(r'\s+', ' ', n.replace('&', 'and')).strip().rstrip('.')
    n = re.sub(r'\bEngg\b\.?', 'Engineering', n)
    n = re.sub(r'\bNaval Arch\.?(?=\s)', 'Naval Architecture', n)
    n = re.sub(r'^Mechanical \(', 'Mechanical Engineering (', n)
    if n.count('(') > n.count(')'):
        n += ')'
    if re.search(r'(?i)agri|agrl', n):
        return 'Agricultural Engineering'
    s = slug(n)
    if s not in CANON or len(n) > len(CANON[s]):
        CANON[s] = n
    return s


def family(n):
    s = n.lower()
    if re.search(r'electronics', s) and re.search(r'computer', s):
        return 'CSE'
    for f, rx in FAMILIES:
        if re.search(rx, s):
            return f
    return 'OTHER'


def main(paths):
    rounds, data = [], {}
    for p in paths:
        m = re.match(r'(20\d\d)_p(\d)', os.path.basename(p))
        rid = f'{m.group(1)}-{m.group(2)}'
        with open(p, encoding='utf-8') as f:
            data[rid] = json.load(f)
        rounds.append({'id': rid, 'year': int(m.group(1)), 'phase': int(m.group(2)), 'date': data[rid]['date'], 'url': URLS.get(rid)})
    rounds.sort(key=lambda r: r['id'])
    colleges, rows = {}, {}
    for r in rounds:
        d = data[r['id']]
        for course, cols in d['courses'].items():
            cn = norm_course(course)
            for code, v in cols.items():
                colleges[code] = {'c': code, 'n': v['name'], 't': v['type']}      # latest name wins
                key = (code, cn)
                row = rows.setdefault(key, {'c': code, 'n': cn, 'f': family(cn), 'r': {}, 'o': {}})
                row['r'][r['id']] = [v['ranks'].get(c) for c in CATS]
                if v['other']:
                    row['o'][r['id']] = v['other']
    for row in rows.values():                       # slug -> one display name for every spelling of a course
        row['n'] = CANON.get(row['n'], row['n'])
        row['f'] = family(row['n'])
    out = {'rounds': rounds, 'cats': CATS, 'colleges': sorted(colleges.values(), key=lambda x: x['c']),
           'rows': sorted(rows.values(), key=lambda x: (x['c'], x['n'])),
           'source': 'Commissioner for Entrance Examinations, Kerala: KEAM engineering allotment last ranks'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print('rounds', [r['id'] for r in rounds], 'colleges', len(colleges), 'course rows', len(rows), 'bytes', os.path.getsize(OUT))


if __name__ == '__main__':
    main(sys.argv[1:])
