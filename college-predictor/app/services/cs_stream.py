"""Page data for /computer-science-stream: the editorial content (app/data/cs_stream_content.py) joined to the college data files built by tools/cs_stream/.

payload() returns one JSON-ready dict for the page script. Nothing here invents a figure: every count is taken from the data files, and a file that is missing is skipped (the page then says so)."""
import json
import os

from app.data import cs_stream_content as C
from app.services.cs_family import family as _family

_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
_ENG = os.path.join(_DATA, 'eng_colleges.json')


def _load(name):
    try:
        with open(os.path.join(_DATA, name), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _nirf_by_name():
    """{NIRF name: [entries]}: a few names (for example Amity University) are listed once per campus."""
    try:
        with open(_ENG, encoding='utf-8') as f:
            out = {}
            for c in json.load(f)['colleges']:
                out.setdefault(c['name'], []).append(c)
            return out
    except (OSError, ValueError, KeyError):
        return {}


def _pick(cands, city):
    """The NIRF entry for a university: the one in the named city, else the best-ranked."""
    if not cands:
        return None
    if city:
        for c in cands:
            if (c.get('city') or '').lower() == city.lower():
                return c
    return sorted(cands, key=lambda c: (c.get('rank') is None, c.get('rank') or 9999))[0]


def josaa():
    """JoSAA institutes with their computer-stream programmes: [{n, t, s, r, b, p: [[name, family, years, close]]}], compact for the page."""
    d = _load('cs_stream_josaa.json')
    if not d:
        return [], {}
    out = []
    for i in d['institutes']:
        out.append({'n': i['name'], 't': i['type'], 's': i['state'], 'r': i['nirf_rank'], 'b': i['nirf_band'],
                    'p': [[p['name'], p['family'], p['years'], p['close']] for p in i['programmes']]})
    return out, {'source': d['source'], 'rank_rule': d['rank_rule'], 'families': d['families']}


def _band_start(b):
    """First number of a NIRF band such as 'Rank 101-150' (so banded institutions sort after the ranked ones, in band order)."""
    import re
    m = re.search(r'(\d+)', b or '')
    return int(m.group(1)) if m else 9999


def private():
    """Private universities with the branches read from their own sites (cs_stream_private.json, verified entries only), joined to NIRF."""
    d = _load('cs_stream_private.json')
    if not d:
        return [], None, None
    nirf = _nirf_by_name()
    out = []
    for u in d.get('universities', []):
        if not u.get('verified') or not u.get('programmes'):
            continue
        c = _pick(nirf.get(u.get('nirf_name') or ''), u.get('nirf_city'))
        out.append({'n': u['name'], 'campus': u.get('campus'), 'city': (c or {}).get('city'), 'state': (c or {}).get('state'), 'r': (c or {}).get('rank'), 'b': (c or {}).get('band'),
                    'p': [[name, _family(name)] for name in u['programmes']], 'entrance': u.get('entrance'), 'caveat': u.get('caveat'), 'partial': bool(u.get('partial')), 'url': (u.get('source_urls') or [None])[0]})
    out.sort(key=lambda x: (x['r'] is None, x['r'] or _band_start(x['b']), x['n']))
    return out, d.get('checked_on'), d.get('note')


def payload():
    inst, jmeta = josaa()
    priv, checked, pnote = private()
    tnea = _load('cs_stream_tnea.json')
    fams = [list(f) for f in jmeta.get('families', [])]
    n_prog = sum(len(i['p']) for i in inst)
    return {
        'updated': C.UPDATED,
        'families': fams,
        'branches': C.BRANCHES,
        'subject_cols': C.SUBJECT_COLS,
        'subjects': [list(s) for s in C.SUBJECTS],
        'journey': C.JOURNEY,
        'placement_notes': [list(x) for x in C.PLACEMENT_NOTES],
        'internship_path': [list(x) for x in C.INTERNSHIP_PATH],
        'why_leaders': [list(x) for x in C.WHY_LEADERS],
        'when': [list(x) for x in C.WHEN_TO_CHOOSE],
        'higher': [list(x) for x in C.HIGHER_STUDIES],
        'ai_tasks': C.AI_TASKS,
        'future_jobs': C.FUTURE_JOBS,
        'skills': C.SKILLS,
        'ask': C.ASK_COLLEGES,
        'faq': [list(x) for x in C.FAQ],
        'sources': C.SOURCES,
        'josaa': inst,
        'josaa_meta': dict({k: v for k, v in jmeta.items() if k != 'families'}, nirf_source='NIRF Engineering list held on the portal'),
        'n_programmes': n_prog,
        'private': priv,
        'private_checked': checked,
        'private_note': pnote,
        'tnea': ({'source': tnea['source'], 'total': tnea['colleges_with_allotments'], 'counts': tnea['family_counts'], 'listed': tnea['listed']} if tnea else None),
    }
