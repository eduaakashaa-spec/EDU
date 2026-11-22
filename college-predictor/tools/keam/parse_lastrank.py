"""Parse a CEE Kerala KEAM engineering 'last rank' PDF into JSON.
usage: python -I parse_keam.py <in.pdf> <out.json>
Output: {"courses": {course: {college_code: {"name", "type", "ranks": {cat: int}, "other": {code: int}}}}, "colleges": {code: {"name","type"}},
         "cats": [...], "date": "dd/mm/yyyy", "problems": [...]}
"""
import json
import re
import sys

import pymupdf

CODE = re.compile(r'^([A-Z]{3})(?:\s+(.*))?$')
VAL = re.compile(r'^(\d+|-)$')
OTHER = re.compile(r'([A-Z]{2}):\s*(\d+)')
FOOT = re.compile(r'^(LAST RANK TABLE|COMMISSIONER FOR ENTRANCE EXAMINATIONS|OFFICE OF THE COMMISSIONER FOR ENTRANCE EXAMINATIONS.*|KEAM \d{4} - .*'
                  r'|(First|Second|Third|Fourth|Final|Mop-?up|Stray) Phase Allotment.*|Page \d+|\d{2}/\d{2}/\d{4})$', re.I)
DATEPAT = re.compile(r'^\d{2}/\d{2}/\d{4}$')


def lines(doc, dates):
    for page in doc:
        for ln in page.get_text().split('\n'):
            ln = ln.strip()
            if not ln:
                continue
            if FOOT.match(ln):
                if DATEPAT.match(ln) and not dates:
                    dates.append(ln)
                continue
            yield ln


def parse(path):
    doc = pymupdf.open(path)
    dates = []
    L = list(lines(doc, dates))
    out = {'courses': {}, 'colleges': {}, 'cats': [], 'problems': [], 'types': {}}
    i, n = 0, len(L)
    course, cats = None, None
    while i < n:
        ln = L[i]
        if ln == 'Name of College' and i > 0:
            prev = L[i - 1]
            # a course continued on a new page repeats only the header row: keep the current course
            if course is None or not (prev == 'Other Categories' or VAL.match(prev) or OTHER.search(prev) or re.fullmatch(r'[A-Z]', prev)):
                course = prev
            j = i + 1
            if j < n and L[j] == 'Type':
                j += 1
            cats = []
            while j < n and L[j] != 'Other Categories':
                cats.append(L[j]); j += 1
            for c in cats:
                if c not in out['cats']:
                    out['cats'].append(c)
            out['courses'].setdefault(course, {})
            i = j + 1
            continue
        if cats is None:
            i += 1; continue
        m = CODE.match(ln)
        if m:
            code = m.group(1)
            name_parts = [m.group(2)] if m.group(2) else []
            j = i + 1
            while j < n and not re.fullmatch(r'[A-Z]', L[j]) and len(name_parts) <= 6:
                name_parts.append(L[j]); j += 1
            if j >= n or not re.fullmatch(r'[A-Z]', L[j]):
                out['problems'].append(['no type', course, code, ' '.join(name_parts)[:60]]); i += 1; continue
            typ = L[j]; j += 1
            vals = []
            while j < n and len(vals) < len(cats) and VAL.match(L[j]):
                vals.append(L[j]); j += 1
            if len(vals) != len(cats):
                out['problems'].append(['values', course, code, len(vals), len(cats)])
            other = {}
            if j < n and OTHER.search(L[j]) and not CODE.match(L[j]):
                other = {a: int(b) for a, b in OTHER.findall(L[j])}; j += 1
            name = re.sub(r'\s+', ' ', ' '.join(name_parts)).strip().rstrip('.')
            out['courses'][course][code] = {'name': name, 'type': typ, 'ranks': {c: int(v) for c, v in zip(cats, vals) if v != '-'}, 'other': other}
            out['colleges'].setdefault(code, {'name': name, 'type': typ})
            out['types'][typ] = out['types'].get(typ, 0) + 1
            i = j
            continue
        i += 1
    out['date'] = dates[0] if dates else None
    return out


if __name__ == '__main__':
    d = parse(sys.argv[1])
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=0)
    nr = sum(len(v) for v in d['courses'].values())
    bogus = [c for c in d['courses'] if c.isupper() or not d['courses'][c]]
    print(sys.argv[1].replace('\\', '/').split('/')[-1], 'date', d['date'], 'courses', len(d['courses']), 'rows', nr, 'colleges', len(d['colleges']),
          'types', d['types'], 'problems', len(d['problems']), 'bogus', bogus)
    for p in d['problems'][:8]:
        print('  ', p)
