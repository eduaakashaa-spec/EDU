"""Content for the public page /engineering-colleges-by-city: the best NIRF-ranked engineering colleges in each city region and state.
Ranking and score: NIRF Engineering list held on the portal's NIRF page (app/data/files/nirf_full.json). DASA seat counts: the DASA 2025 seat matrix on file.
Fees, entrance routes and NRI quota: read from the institutions' own pages and government notices by tools/cities/merge_eng.py; a blank means we found no official figure.
Nothing here promises a rank, a seat or an admission."""
import json
import os

UPDATED = '2 November 2026'
_HERE = os.path.dirname(os.path.abspath(__file__))

FACTS = [
    ('NIRF Engineering', 'ranks and scores from the portal’s NIRF Engineering page'),
    ('Top 10 a region', 'the ten best NIRF positions in each city region, fewer where fewer are ranked'),
    ('Fees and NRI', 'shown only where the college or an admission authority states them'),
]

ELIGIBILITY = [
    ('IITs', 'A rank in JEE Advanced after qualifying JEE Main, allotted through JoSAA. Class 12 criteria are in the JoSAA rules: Mathematics and Physics with Chemistry, Biology, Biotechnology or Computer Science, and 75% (65% for SC, ST, PwD) or the board’s top 20 percentile.'),
    ('NITs, IIITs and other centrally funded institutes', 'A JEE Main rank, allotted through JoSAA and CSAB. Class 12 with Mathematics, Physics and one of Chemistry, Biotechnology, Computer Science or Biology; at least 75% in the best five subjects (65% for SC, ST, PwD) or the board’s top 20 percentile.'),
    ('State colleges', 'Through the state’s counselling (for example TNEA, MHT-CET CAP, KEA, TS EAMCET, KEAM, WBJEE). Each state sets its own subject and marks rules: read the current prospectus.'),
    ('Private and deemed universities', 'Many run their own entrance (for example VITEEE, SRMJEEE, BITSAT) or accept JEE Main and state ranks. The college publishes the minimum marks and the seats it reserves.'),
]

NRI = [
    ('DASA', 'Direct Admission of Students Abroad fills supernumerary seats (up to 15 percent of an institute’s seats) at NITs, IIEST, IIITs and other centrally funded institutes for NRI, PIO, OCI and foreign students, on a JEE Main rank. IITs are not part of DASA.'),
    ('College quotas', 'Private and deemed universities usually run their own NRI or management quota with its own fee, often in US dollars. The size of the quota and the fee are the college’s decision: ask for it in writing.'),
    ('State colleges', 'Some states keep a small NRI quota in state colleges, others do not. Ask the state counselling authority for the current notice.'),
]

FAQ = [
    ('Why does a city show fewer than ten colleges?', 'Only institutions in the NIRF Engineering list are shown, so a region with fewer ranked colleges shows fewer. A college outside the list may still be recognised and good: check AICTE approval and the counselling authority.'),
    ('What does the NIRF band mean?', 'NIRF ranks the first 100 institutions one by one. After that it groups them in bands (101 to 150, 151 to 200, 201 to 300) without an exact rank.'),
    ('Why are some fees blank?', 'Fees change every year and vary by branch and category. We show a fee only when the college or an admission authority publishes it. For a blank, ask the admissions office for the fee head by head, in writing.'),
    ('Is the NRI quota the same as DASA?', 'No. DASA is the government route for centrally funded institutes. A college’s own NRI quota is a separate seat category set by that college or its state.'),
    ('Are the tile pictures photographs?', 'No. They are illustrations we drew, coloured by type of institution. They carry the college’s initials, not its logo.'),
]

SOURCES = [
    'NIRF Engineering list on the portal’s NIRF page',
    'DASA 2025 seat matrix and DASA 2026 brochure',
    'JoSAA 2026 brochure and business rules',
    'Each college’s own website and fee notices; state counselling notices',
]

TYPE_LABEL = {'IIT': 'IIT', 'NIT': 'NIT', 'IIIT': 'IIIT', 'BITS': 'BITS', 'University': 'University', 'Private': 'Private or deemed'}
GOVT_TYPES = ('IIT', 'NIT', 'IIIT')


def _load(name):
    with open(os.path.join(_HERE, name), encoding='utf-8') as f:
        return json.load(f)


def context():
    base = _load('eng_cities.json')
    try:
        rich = {c['key']: c for c in _load('eng_colleges.json')['colleges']}
    except OSError:
        rich = {}
    cols = {}
    for c in base['colleges']:
        e = dict(rich.get(c['key'], c))
        e['label'] = ('NIRF #%d' % c['rank']) if c['rank'] else ('NIRF ' + (c['band'] or '').replace('Rank ', '').replace(' to ', '–').replace('-', '–'))
        e['govt'] = c['type'] in GOVT_TYPES or bool(e.get('dasa'))
        cols[c['key']] = e
    ranked = [c for c in base['colleges'] if c['rank']]
    cities = []
    for g in base['cities']:
        top = [cols[k] for k in g['ids']]
        sc = [c['score'] for c in top if c.get('score')]
        cities.append(dict(key=g['key'], label=g['label'], state=g['state'], capital=g['capital'], n=g['n'], ids=g['ids'],
                           best=min([c['rank'] for c in top if c['rank']] or [0]) or None, avg=round(sum(sc) / len(sc), 1) if sc else None,
                           top100=sum(1 for c in top if c['rank']), dasa=sum(1 for c in top if c.get('dasa'))))
    states = [dict(s) for s in base['states']]
    return dict(cities=cities, states=states, colleges=cols, n_ranked=len(ranked), n_total=len(base['colleges']))
