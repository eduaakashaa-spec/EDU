"""Build app/data/cs_stream_josaa.json for the member page /computer-science-stream.

From the portal's JoSAA 2026 file (Rounds 1 to 5; app/data/files/josaa_cutoffs_2026.xlsx) it lists, for every IIT, NIT, IIIT and other JoSAA institute, the computer-stream programmes it offers, grouped
into families, with the Open category closing rank (all-India or other-state quota, gender-neutral pool, highest closing rank over the rounds). Each institute is joined to its NIRF Engineering
position from app/data/eng_colleges.json. Nothing is guessed: a programme appears only if the JoSAA file lists it; an institute with no NIRF match says so.

Run from college-predictor/:  python tools/cs_stream/build_colleges.py
"""
import json
import os
import re
import sys
import unicodedata
from difflib import SequenceMatcher

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'app', 'data', 'files', 'josaa_cutoffs_2026.xlsx')
NIRF = os.path.join(ROOT, 'app', 'data', 'eng_colleges.json')
OUT = os.path.join(ROOT, 'app', 'data', 'cs_stream_josaa.json')

FAMILIES = [
    ('core', 'Core CSE'),
    ('it', 'Information Technology'),
    ('aids', 'AI, ML and Data Science'),
    ('cyber', 'Cyber Security'),
    ('mnc', 'Mathematics and Computing'),
    ('biz', 'Computer + Business'),
    ('hybrid', 'Computing hybrids (IoT, robotics, computational engineering)'),
]
FAMILY_KEYS = [k for k, _ in FAMILIES]

# JoSAA spelling -> NIRF spelling, each pair checked by hand (the same institute under two names). Anything not listed or not an exact match is left unmatched on purpose:
# a near match is not safe (for example IIIT Bhopal is not IIIT Guwahati, and NIT Andhra Pradesh is not NIT Arunachal Pradesh).
ALIAS = {
    'indian institute of technology bhu varanasi': 'indian institute of technology banaras hindu university varanasi',
    'indian institute of technology ism dhanbad': 'indian institute of technology indian school of mines',
    'atal bihari vajpayee indian institute of information technology and management gwalior': 'atal bihari vajpayee indian institute of information technology and management',
    'malaviya national institute of technology jaipur': 'malaviya national institute of technology',
    'maulana azad national institute of technology bhopal': 'maulana azad national institute of technology',
    'motilal nehru national institute of technology allahabad': 'motilal nehru national institute of technology',
    'sardar vallabhbhai national institute of technology surat': 'sardar vallabhbhai national institute of technology',
    'pt dwarka prasad mishra indian institute of information technology design and manufacture jabalpur': 'pandit dwarka prasad mishra indian institute of information technology design and manufacturing iiitdm jabalpur',
}


def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('&', ' and ')
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def itype(name):
    if re.search(r'Indian Institute of Technology', name, re.I) and not re.search(r'Information', name, re.I):
        return 'IIT'
    if re.search(r'National Institute of Technology', name, re.I):
        return 'NIT'
    if re.search(r'Indian Institute of Information Technology', name, re.I) or re.search(r'\bIIIT\b', name, re.I):
        return 'IIIT'
    return 'Other'


sys.path.insert(0, ROOT)
from app.services.cs_family import clean_program, duration, family  # noqa: E402


def load_josaa():
    wb = openpyxl.load_workbook(SRC, read_only=True)
    rows = list(wb[wb.sheetnames[0]].iter_rows(values_only=True))
    h = rows[0]
    out = []
    for r in rows[1:]:
        d = dict(zip(h, r))
        if d['Seat Type'] != 'OPEN' or d['Gender'] != 'Gender-Neutral':
            continue
        try:
            close = int(str(d['Maximum Closing Rank']).rstrip('P'))
            open_ = int(str(d['Minimum Opening Rank']).rstrip('P'))
        except ValueError:
            continue
        out.append((d['Institute'], d['Academic Program Name'], d['Quota'], open_, close))
    return out


def nirf_index():
    L = json.load(open(NIRF, encoding='utf-8'))['colleges']
    return {norm(c['name']): c for c in L}, L


def match_nirf(name, idx, L):
    n = norm(name)
    n = ALIAS.get(n, n)
    return (idx[n], 'exact') if n in idx else (None, 'none')


def main():
    rows = load_josaa()
    idx, L = nirf_index()
    inst = {}
    for name, prog, quota, o, c in rows:
        fam = family(prog)
        if not fam:
            continue
        yrs, deg = duration(prog)
        rec = inst.setdefault(name, {'name': name, 'type': itype(name), 'programmes': {}})
        key = clean_program(prog) + '|' + str(yrs) + '|' + deg
        pr = rec['programmes'].setdefault(key, {'name': clean_program(prog), 'family': fam, 'years': yrs, 'degree': deg, 'close_ai': None, 'close_other': None})
        slot = 'close_ai' if quota in ('AI', 'OS') else ('close_other' if quota == 'HS' else None)
        if slot and (pr[slot] is None or c > pr[slot]):
            pr[slot] = c
    result, unmatched = [], []
    for name, rec in sorted(inst.items()):
        c, how = match_nirf(name, idx, L)
        if not c:
            unmatched.append(name)
        progs = sorted(rec['programmes'].values(), key=lambda p: (FAMILY_KEYS.index(p['family']), p['name'], p['years'] or 0))
        for p in progs:
            p['close'] = p['close_ai'] if p['close_ai'] is not None else p['close_other']
            p.pop('close_ai')
            p.pop('close_other')
        result.append({'name': name, 'type': rec['type'], 'state': c['state'] if c else None, 'city': c['city'] if c else None, 'nirf_rank': c['rank'] if c else None, 'nirf_band': c['band'] if c else None,
                       'nirf_match': how, 'website': (c or {}).get('website'), 'programmes': progs})
    out = {'source': 'JoSAA 2026 opening and closing ranks, Rounds 1 to 5 (app/data/files/josaa_cutoffs_2026.xlsx)', 'rank_rule': 'Open category, gender-neutral pool, all-India or other-state quota where the institute has one, highest closing rank over the rounds',
           'nirf_source': 'NIRF Engineering list held in app/data/eng_colleges.json', 'families': FAMILIES, 'institutes': result}
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('institutes with computer-stream programmes:', len(result), '| programmes:', sum(len(r['programmes']) for r in result))
    print('matched to NIRF:', sum(1 for r in result if r['nirf_rank'] or r['nirf_band']), '| unmatched:', len(unmatched))
    print('  unmatched sample:', unmatched[:40])


if __name__ == '__main__':
    sys.exit(main())
