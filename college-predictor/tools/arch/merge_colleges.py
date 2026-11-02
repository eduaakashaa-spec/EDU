"""Merge the four regional research files into app/data/arch_colleges.json.
Each research file: {meta, state_notes: {state: {note, source}}, institutions: [..]} (see the research brief).
Rules: a fee, placement, seat count or quota is shown only with a source link; figures that come only from aggregator sites are shown as 'unverified'.
JoSAA 2026 closing ranks and the 2026 NIT+ seat matrix are attached from app/data/arch_josaa.json and arch_seats.json; NIRF 2025 rank from app/data/arch_planning.py.
Usage: python tools/arch/merge_colleges.py <research dir> [out json]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..')
sys.path.insert(0, APP)
from app.data import arch_planning as ap  # noqa: E402

AGGR = ('careers360', 'collegedekho', 'shiksha', 'collegedunia', 'getmyuni', 'jagranjosh', 'pw.live', 'silica', 'architecture.live', 'iquanta', 'buddy4study', 'edufever', 'collegesearch', 'indcareer')
FILES = ['res_north.json', 'res_west.json', 'res_south.json', 'res_east.json']
GOV = ('Central govt', 'State govt', 'State university')


def norm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', (s or '').lower().replace('&', ' and ')).split()


def toks(s):
    return set(norm(s)) - {'of', 'and', 'the', 'institute', 'national', 'university', 'technology', 'college', 'for', 'in', 'school'}


def match(name, options):
    """options: list of (key, name). Best token-overlap match, requiring the distinctive tokens of the shorter name to be inside the other."""
    a = toks(name)
    best, score = None, 0
    for key, n in options:
        b = toks(n)
        if not a or not b:
            continue
        inter = len(a & b)
        if inter >= min(len(a), len(b)) and inter > score:
            best, score = key, inter
    return best


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


def unverified(url):
    return bool(url) and any(a in url for a in AGGR)


def money(n):
    return '₹{:,}'.format(int(n))


def last(arr):
    return [x for x in arr if x is not None][-1]


def main(src, out):
    cols, notes = [], {}
    for f in FILES:
        p = os.path.join(src, f)
        if not os.path.exists(p):
            print('missing', f)
            continue
        d = json.load(open(p, encoding='utf-8'))
        for s, v in (d.get('state_notes') or {}).items():
            if v and (v.get('note') or v.get('text')):
                notes[s] = dict(text=v.get('note') or v.get('text'), source=v.get('source'))
        cols.extend(d.get('institutions') or d.get('colleges') or [])
    jo = ap.josaa()
    seats = json.load(open(os.path.join(APP, 'app', 'data', 'arch_seats.json'), encoding='utf-8'))
    jo_opts = [(i, n) for i, n in enumerate(jo['institutes'])]
    nirf_opts = [(r[0], r[1]) for r in ap.NIRF]
    res, seen = [], set()
    for c in cols:
        key = (c.get('name') or '').strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        e = dict(name=c['name'].strip(), city=c.get('city') or '', state=c.get('state') or '', type=c.get('type') or 'Private college',
                 programmes=c.get('programmes') or [], website=c.get('website'), admission_route=c.get('admission_route'),
                 sources=[u for u in (c.get('source_urls') or []) if u])
        e['has_plan'] = any('plan' in p.lower() for p in e['programmes'])
        e['confidence'] = c.get('confidence')
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
                    e['seats_note'] = '2026 JoSAA seat matrix'
        # fee: a clean figure only; free-text aggregator notes are dropped
        fs = c.get('fee_source')
        t = c.get('tuition_per_year_inr')
        e['tuition'] = None
        e['fee_text'] = None
        if t:
            if unverified(fs):
                e['fee_text'] = 'about ' + money(t) + ' a year (aggregator site: unverified)'
            else:
                e['fee_text'] = money(t) + ' a year (tuition)'
                e['tuition'] = int(t)
                e['fee_note'] = (c.get('fee_note') or '')[:200]
        if c.get('intake') and not e.get('seats'):
            e['intake'] = c['intake']
        # placement
        pl = c.get('placement') or {}
        if pl.get('median_or_avg_package_lpa') or pl.get('placed_or_pct'):
            bits = []
            if pl.get('median_or_avg_package_lpa'):
                bits.append('median/average ₹%s lakh a year' % pl['median_or_avg_package_lpa'])
            if pl.get('placed_or_pct'):
                bits.append('placed: %s' % pl['placed_or_pct'])
            e['placement_text'] = '%s%s' % (', '.join(bits), (' (%s)' % pl['year']) if pl.get('year') else '')
            e.update(pl_year=pl.get('year'), pl_pack=(('₹%s lakh' % pl['median_or_avg_package_lpa']) if pl.get('median_or_avg_package_lpa') else ''),
                     pl_note=str(pl.get('placed_or_pct') or '') + (' ' + pl['note'] if pl.get('note') and 'blocked' not in pl['note'].lower() and 'not ' not in pl['note'].lower() else ''))
            if c.get('placement_source'):
                e['sources'].append(c['placement_source'])
        # NRI
        nq = c.get('nri_quota') or {}
        dl = (nq.get('detail') or '').strip().lower()
        if dl.startswith(('not verified', 'no nri')):
            nq = dict(nq, detail=None)
        if nq.get('detail') and nq.get('available') is not False:
            e['nri_text'] = nq['detail'][:260] + (' (unverified)' if unverified(nq.get('source')) else '')
        elif nq.get('available') is False and nq.get('detail'):
            e['nri_text'] = nq['detail'][:200]
        if nq.get('source'):
            e['sources'].append(nq['source'])
        if fs:
            e['sources'].insert(0, fs)
        e['sources'] = list(dict.fromkeys(e['sources']))
        res.append(e)
    # IIT Roorkee: NIRF 2025 data sheet supplied by the user (23 Nov file JoSAA_2026_Architecture_Planning.xlsx, a PDF)
    for e in res:
        if 'roorkee' in e['name'].lower() and 'indian institute of technology' in e['name'].lower():
            e['placement_text'] = '2023-24: 10 of 22 graduates placed, median ₹10,00,000 a year, 11 went to higher studies (NIRF 2025 data sheet)'
            e.update(pl_year='2023-24', pl_pack='₹10,00,000', pl_note='10 of 22 graduating placed, 11 in higher studies (NIRF 2025 data sheet; B.Arch 5-year programme)')
            e['intake'] = None
    res.sort(key=lambda e: (e['state'], 0 if e['type'] in GOV else 1, e['nirf_rank'] or 99, e['name']))
    json.dump(dict(colleges=res, state_notes=notes), open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(res), 'colleges', len(notes), 'state notes')
    print('with fee', sum(1 for e in res if e.get('fee_text')), 'placement', sum(1 for e in res if e.get('placement_text')), 'nri', sum(1 for e in res if e.get('nri_text')), 'nirf', sum(1 for e in res if e['nirf_rank']), 'josaa', sum(1 for e in res if e.get('josaa_text')))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(APP, 'app', 'data', 'arch_colleges.json'))
