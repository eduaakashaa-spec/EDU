"""Merge the four regional research files into app/data/arch_colleges.json.
Policy: only facts from the institution itself, the Council of Architecture, NIRF, JoSAA, DASA or a government notice are kept.
Anything that came from an aggregator or coaching site is dropped (fee, quota, seats, notes), and no source links are written to the file.
Placement, intake, students and the other NIRF factors are not stored here: they come from app/data/arch_nirf.json (the NIRF 2025 data sheets).
JoSAA 2026 closing ranks and the 2026 NIT+ seat matrix are attached from app/data/arch_josaa.json and arch_seats.json.
Usage: python tools/arch/merge_colleges.py <research dir> [out json]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..')
sys.path.insert(0, APP)
from app.data import arch_planning as ap  # noqa: E402

THIRD = re.compile(r'aggregat|collegedekho|careers360|collegedunia|shiksha|getmyuni|jagranjosh|pw\.live|silica|architecture\.live|iquanta|buddy4study|corpready|edufever|collegesearch|indcareer|coaching|unverified|per listing|listing', re.I)
HEDGE = re.compile(r'sources? (differ|disagree)|likely|per an older|older exam|not verified|unclear|not read|amounts? not|\?|treat ', re.I)
FILES = ['res_north.json', 'res_west.json', 'res_south.json', 'res_east.json']
GOV = ('Central govt', 'State govt', 'State university')

ALIASES = [
    (r'indian institute of technology.*roorkee', 1, 'Indian Institute of Technology Roorkee'),
    (r'indian institute of technology.*kharagpur', 3, 'Indian Institute of Technology Kharagpur'),
    (r'indian institute of engineering science', 4, 'Indian Institute of Engineering Science and Technology, Shibpur'),
    (r'jamia', 5, None), (r'^cept|cept university', 6, None),
    (r'national institute of technology.*rourkela', 7, 'National Institute of Technology, Rourkela'),
    (r'school of planning and architecture.*new delhi', 8, 'School of Planning & Architecture, New Delhi'),
    (r'national institute of technology.*tiruchirappalli', 9, 'National Institute of Technology, Tiruchirappalli'),
    (r'visvesvaraya', 10, 'Visvesvaraya National Institute of Technology, Nagpur'),
    (r'school of planning and architecture.*bhopal', 11, 'School of Planning & Architecture, Bhopal'),
    (r'malaviya', 12, 'Malaviya National Institute of Technology Jaipur'),
    (r'national institute of technology.*patna', 13, 'National Institute of Technology Patna'),
    (r'^chandigarh university', 14, None),
    (r'college of engineering,? trivandrum', 15, None), (r'jadavpur', 16, None),
    (r'maulana azad', 17, 'Maulana Azad National Institute of Technology Bhopal'),
    (r'srm institute', 18, None),
    (r'school of planning and architecture.*vijayawada', 19, 'School of Planning & Architecture: Vijayawada'),
    (r'bms college of architecture', 20, None), (r'manipal university jaipur', 21, None),
    (r'birla institute of technology', 22, None),
    (r'shri mata vaishno', 23, 'Shri Mata Vaishno Devi University, Katra, Jammu & Kashmir'),
    (r'lovely professional', 24, None), (r'amity university kolkata', 25, None), (r'aligarh', 26, None),
    (r'manipal school of architecture', 27, None), (r'^anna university', 28, None), (r'nirma', 29, None),
    (r'national institute of technology.*hamirpur', 30, 'National Institute of Technology Hamirpur'),
    (r'ramaiah', 31, None), (r'm\.? ?g\.? ?r', 32, None), (r'thiagarajar', 33, None), (r'^christ university', 34, None),
    (r'national institute of technology.*raipur', 35, 'National Institute of Technology Raipur'),
    (r'guru gobind', 36, None), (r'bms school of architecture', 37, None), (r'^chitkara', 38, None),
    (r'apj', 39, None), (r'^anant', 40, None),
    (r'national institute of technology.*calicut', 2, 'National Institute of Technology Calicut'),
    (r'national institute of technology.*kurukshetra', None, 'National Institute of Technology, Kurukshetra'),
    (r'islamic university of science', None, 'Islamic University of Science and Technology Kashmir'),
    (r'mizoram university', None, 'Mizoram University, Aizawl'),
]


def alias(name):
    n = name.lower().strip()
    for rx, nr, jn in ALIASES:
        if re.search(rx, n):
            return nr, jn
    return None, None


def last(arr):
    return [x for x in arr if x is not None][-1]


def clean(s):
    """None if the text leans on a third-party site or says it is unverified."""
    if not s:
        return None
    s = s.strip()
    if THIRD.search(s) or HEDGE.search(s) or s.lower().startswith(('not verified', 'no nri')):
        return None
    return s


def third_url(u):
    if isinstance(u, (list, tuple)):
        return any(third_url(x) for x in u)
    return bool(u) and bool(THIRD.search(str(u)))


def money(n):
    return '₹{:,}'.format(int(n))


def main(src, out):
    cols, notes = [], {}
    for f in FILES:
        p = os.path.join(src, f)
        if not os.path.exists(p):
            print('missing', f)
            continue
        d = json.load(open(p, encoding='utf-8'))
        for s, v in (d.get('state_notes') or {}).items():
            if not v:
                continue
            txt = clean(v.get('note') or v.get('text'))
            if txt and not third_url(v.get('source')):
                notes[s] = dict(text=txt)
        cols.extend(d.get('institutions') or d.get('colleges') or [])
    jo = ap.josaa()
    seats = json.load(open(os.path.join(APP, 'app', 'data', 'arch_seats.json'), encoding='utf-8'))
    res, seen = [], set()
    for c in cols:
        key = (c.get('name') or '').strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        e = dict(name=c['name'].strip(), city=c.get('city') or '', state=c.get('state') or '', type=c.get('type') or 'Private college',
                 programmes=[x for x in (c.get('programmes') or []) if not THIRD.search(x)], website=c.get('website'))
        e['has_plan'] = any('plan' in p.lower() for p in e['programmes'])
        route = clean(c.get('admission_route'))
        e['admission_route'] = route
        nr, jname = alias(e['name'])
        e['nirf_rank'] = nr
        ji = jo['institutes'].index(jname) if jname in jo['institutes'] else None
        if ji is not None:
            rows = [r for r in jo['rows'] if r['i'] == ji and r['s'] == 'OPEN' and r['g'] == 'N']
            parts = []
            for pg, lab in (('A', 'B.Arch'), ('P', 'B.Plan')):
                rs = [r for r in rows if r['p'] == pg]
                if rs:
                    parts.append(lab + ' OPEN ' + ', '.join('%s %s' % (r['q'], '{:,}'.format(last(r['c']))) for r in rs))
            e['josaa_text'] = ('; '.join(parts) + ' (final-round closing rank)') if parts else None
            for s_ in seats:
                if s_['inst'] == jname and s_['prog'] == 'A':
                    e['seats'] = s_['seats']
        # fee: a clean figure from the institution or a government notice only
        t = c.get('tuition_per_year_inr')
        e['tuition'] = None
        e['fee_text'] = None
        if t and not third_url(c.get('fee_source')):
            e['tuition'] = int(t)
            e['fee_text'] = money(t) + ' a year (tuition)'
        # NRI: the college's own words only
        nq = c.get('nri_quota') or {}
        txt = clean(nq.get('detail'))
        if txt and not third_url(nq.get('source')):
            e['nri_text'] = txt[:260]
        res.append(e)
    res.sort(key=lambda e: (e['state'], 0 if e['type'] in GOV else 1, e['nirf_rank'] or 99, e['name']))
    json.dump(dict(colleges=res, state_notes=notes), open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(res), 'colleges', len(notes), 'state notes')
    print('fee', sum(1 for e in res if e.get('fee_text')), 'nri', sum(1 for e in res if e.get('nri_text')), 'nirf', sum(1 for e in res if e['nirf_rank']), 'route', sum(1 for e in res if e['admission_route']), 'josaa', sum(1 for e in res if e.get('josaa_text')))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(APP, 'app', 'data', 'arch_colleges.json'))
