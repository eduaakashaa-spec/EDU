"""Merge the NIRF Engineering list (app/data/eng_cities.json), the DASA 2025 seat matrix and the regional research files into app/data/eng_colleges.json.
Policy (same as the architecture pages): only the institution itself, the admission authority, NIRF, JoSAA or DASA are used. Anything from an aggregator, coaching or
news site is dropped, free text that hedges is dropped, and no source links are written. A blank means we could not find an official figure.
Usage: python tools/cities/merge_eng.py <research dir>"""
import collections
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
THIRD = re.compile(r'aggregat|collegedekho|careers360|collegedunia|shiksha|getmyuni|jagranjosh|wikipedia|coaching|unverified|per listing|listing|news', re.I)
HEDGE = re.compile(r'sources? (differ|disagree)|likely|not verified|unclear|not read|amounts? not|\?|treat |approximately|reportedly', re.I)

JOSAA_ELIG = ('Class 12 with Mathematics, Physics and one of Chemistry, Biotechnology, Computer Science or Biology, with at least 75% in the best five subjects '
              '(65% for SC, ST and PwD) or being in your board’s top 20 percentile (JoSAA 2026 rules).')
IIT_ELIG = ('A rank in JEE Advanced after qualifying JEE Main, then the Class 12 criteria in the JoSAA 2026 rules: Mathematics and Physics with Chemistry, Biology, Biotechnology or Computer Science, '
            'and 75% (65% for SC, ST and PwD) or the board’s top 20 percentile.')


FEE_SKIP = ('jamia-millia-islamia', 'puducherry-technological', 'coep-technological', 'kumaraguru', 'vel-tech')


def norm(s):
    s = re.sub(r'\(.*?\)', ' ', s)
    return re.sub(r'[^a-z0-9 ]', ' ', s.lower().replace('&', ' and '))


STOP = {'of', 'and', 'the', 'a', 'in', 'for', 'institute', 'technology', 'indian', 'college', 'engineering', 'science', 'deemed', 'be', 'to', 'campus', 'delhi', 'new', 'allahabad'}


def toks(s):
    return {t for t in norm(s).split() if t not in STOP}


def parity(a, b):
    for w in ('national', 'information', 'maritime', 'university', 'indian'):
        if (w in norm(a).split()) != (w in norm(b).split()) and w in ('national', 'information', 'maritime', 'indian'):
            return False
    return True


def dasa_match(c, inst):
    if c['type'] == 'IIT' or 'indian institute of technology' in c['name'].lower():
        return None
    best, bs = None, 0
    for e in inst.values():
        a, b = toks(c['name']), toks(e['name'])
        if not a or not b or not parity(c['name'], e['name']):
            continue
        j = len(a & b) / float(len(a | b))
        same_state = e['state'].lower()[:5] == c['state'].lower()[:5] or {e['state'].lower(), c['state'].lower()} <= {'puducherry', 'pondicherry'}
        if (j >= 0.8 or (j >= 0.5 and len(a & b) >= 2 and same_state and (a <= b or b <= a))) and j > bs:
            best, bs = e, j
    return best


def clean(s):
    if not s:
        return None
    s = str(s).strip()
    if THIRD.search(s) or HEDGE.search(s):
        return None
    return s


def main(src):
    base = json.load(open(os.path.join(APP, 'data', 'eng_cities.json'), encoding='utf-8'))
    rows = list(csv.DictReader(open(os.path.join(APP, 'data', 'files', 'dasa_seat_matrix.csv'), encoding='utf-8')))
    inst = collections.OrderedDict()
    for r in rows:
        e = inst.setdefault(r['institute'], dict(name=r['institute'], city=r['city'], state=r['state'], seats=0, progs=0, ciwg=0))
        e['seats'] += int(r['dasa_total'] or 0)
        e['ciwg'] += int(r['ciwg'] or 0)
        e['progs'] += 1
    res = {}
    for g in 'ABCDE':
        p = os.path.join(src, 'res_%s.json' % g)
        if os.path.exists(p):
            for r in json.load(open(p, encoding='utf-8')):
                res[r['key']] = r
        else:
            print('missing', p)
    out = []
    for c in base['colleges']:
        r = res.get(c['key'], {})
        e = dict(key=c['key'], name=c['name'], city=c['city'], state=c['state'], type=c['type'], rank=c['rank'], band=c['band'], score=c['score'])
        w = r.get('website')
        e['website'] = w if w and w.startswith('http') else None
        d = dasa_match(c, inst)
        if d:
            e['dasa'] = dict(seats=d['seats'], programmes=d['progs'])
        # entrance / route
        ex = [x for x in (r.get('entrance_exams') or []) if clean(x)]
        e['exams'] = ex or None
        # eligibility
        el = clean(r.get('eligibility'))
        if c['type'] == 'IIT':
            e['eligibility'] = IIT_ELIG
            e['elig_src'] = 'JoSAA 2026 rules'
        elif d or c['type'] == 'NIT':
            e['eligibility'] = JOSAA_ELIG
            e['elig_src'] = 'JoSAA 2026 rules'
        else:
            e['eligibility'] = el
            e['elig_src'] = 'the college or its counselling authority' if el else None
        # fee: a figure the college or admission authority publishes, as first-year tuition. Figures the researchers flagged as doubtful or not plain tuition are left out.
        fee = r.get('fee_btech_per_year_inr')
        ev = r.get('evidence') or []
        ok = isinstance(fee, (int, float)) and fee and not any(THIRD.search(u) for u in ev) and not any(c['key'].startswith(b) for b in FEE_SKIP)
        e['fee'] = int(fee) if ok else None
        note = clean((r.get('fee_note') or '')[:200]) if ok else None
        e['fee_note'] = note
        e['fee_year'] = r.get('fee_year') if ok else None
        rawnote = r.get('fee_note') or ''
        e['fee_from'] = bool(ok) and bool(re.search(r'annual fees from|ranges?|lowest|by branch|branch-wise', rawnote, re.I))
        # NRI
        nq = r.get('nri_quota') or {}
        t = clean(nq.get('detail'))
        e['nri'] = t[:240] if t else None
        e['nri_flag'] = nq.get('available') if t else None
        out.append(e)
    json.dump(dict(colleges=out), open(os.path.join(APP, 'data', 'eng_colleges.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), 'colleges')
    print('fee', sum(1 for e in out if e['fee']), '| nri text', sum(1 for e in out if e['nri']), '| dasa', sum(1 for e in out if e.get('dasa')), '| exams', sum(1 for e in out if e['exams']), '| eligibility', sum(1 for e in out if e['eligibility']), '| website', sum(1 for e in out if e['website']))
    bad = [e['name'] for e in out if e.get('dasa') and ('Indian Institute of Technology' in e['name'])]
    print('dasa matches:', [(e['name'][:34], e['dasa']['seats']) for e in out if e.get('dasa')][:60])


if __name__ == '__main__':
    main(sys.argv[1])
