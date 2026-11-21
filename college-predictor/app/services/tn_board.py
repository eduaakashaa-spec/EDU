"""TN State Board Class 12 syllabus analytics against JEE Main and NEET: builds the payload for /tn-board-12-analytics.

Tiers (one scale for both exams, from how often a chapter is asked):
  JEE Main: questions in the 19 shifts of 2026, Tier 1 >= 22, Tier 2 13-21, Tier 3 8-12, Tier 4 <= 7 (includes chapters not tested)
  NEET:     average questions a paper, Tier 1 >= 3.5, Tier 2 2.5-3, Tier 3 1.5-2, Tier 4 <= 1
Coverage: '12' and '11' count fully, 'P' counts half, 'N' not at all. "Board coverage" counts only '12' (what the +2 exam itself examines).
"""
import json
import os
from functools import lru_cache

from app.data import tn_board as D

_JEE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'jee_syllabus_2026.json')
SUBJ = ['Mathematics', 'Physics', 'Chemistry']
WEIGHT = {'12': 1.0, '11': 1.0, 'P': 0.5, 'N': 0.0}


def jee_tier(n):
    return 1 if n >= 22 else 2 if n >= 13 else 3 if n >= 8 else 4


def neet_tier(q):
    return 1 if q >= 3.5 else 2 if q >= 2.5 else 3 if q >= 1.5 else 4


def _coverage(rows, wkey):
    tot = sum(r[wkey] for r in rows) or 1
    def pct(f):
        return round(100 * sum(r[wkey] * f(r) for r in rows) / tot, 1)
    return {
        'chapters': len(rows),
        'board12': pct(lambda r: 1 if r['st'] == '12' else 0),
        'tn11_12': pct(lambda r: WEIGHT[r['st']]),
        'gap': pct(lambda r: 1 - WEIGHT[r['st']]),
        'n12': sum(1 for r in rows if r['st'] == '12'), 'n11': sum(1 for r in rows if r['st'] == '11'),
        'nP': sum(1 for r in rows if r['st'] == 'P'), 'nN': sum(1 for r in rows if r['st'] == 'N'),
    }


@lru_cache(maxsize=1)
def jee_rows():
    with open(_JEE, encoding='utf-8') as f:
        chs = json.load(f)['chs']
    rows = []
    for c in chs:
        st, tn, note = D.JEE_MAP[c['ch']]
        rows.append({'sub': SUBJ[c['s']], 'cls': c['cls'], 'ch': c['ch'], 'q': c['n'], 'tier': jee_tier(c['n']), 'st': st, 'tn': tn, 'note': note,
                     'e': c['e'], 'm': c['m'], 'h': c['h'], 'hours': c.get('hours', 0), 'topics': c.get('topics', [])[:4]})
    return rows


@lru_cache(maxsize=1)
def neet_rows():
    return [{'sub': s, 'cls': cl, 'ch': ch, 'q': q, 'tier': neet_tier(q), 'st': st, 'tn': tn, 'note': note} for s, cl, ch, q, st, tn, note in D.NEET]


def coverage():
    j, n = jee_rows(), neet_rows()
    out = {'jee': {'all': _coverage(j, 'q')}, 'neet': {'all': _coverage(n, 'q')}}
    for s in SUBJ:
        out['jee'][s] = _coverage([r for r in j if r['sub'] == s], 'q')
    for s in ('Physics', 'Chemistry', 'Biology'):
        out['neet'][s] = _coverage([r for r in n if r['sub'] == s], 'q')
    return out


def calendar():
    """Events offered in the calendar picker: TN board dates plus the PCM / PCB entrance exams from the /exam-schedule data."""
    from app.services import exam_page
    ev = [{'id': i, 'name': nm, 'start': a, 'end': b, 'status': st, 'note': note, 'group': 'board', 'when': ''} for i, nm, a, b, st, note in D.TN_EVENTS]
    seen = set()
    for grp in ('pcm', 'pcb'):
        for xid in D.CAL_PICK[grp]:
            row = exam_page.find(xid)
            if not row or xid in seen or not row[6]:
                continue
            seen.add(xid)
            in_both = xid in D.CAL_PICK['pcm'] and xid in D.CAL_PICK['pcb']
            ev.append({'id': xid, 'name': row[1], 'start': row[6], 'end': row[7] or row[6], 'status': row[4], 'note': row[5][:260], 'when': row[3],
                       'group': 'both' if in_both else grp})
    ev.sort(key=lambda e: e['start'])
    return ev


def payload():
    return {'jee': jee_rows(), 'neet': neet_rows(), 'cov': coverage(), 'tn': {f'{k[0]}|{k[1]}': v for k, v in D.TN_CHAPTERS.items()},
            'boardOnly': D.BOARD_ONLY, 'areas': D.AREAS, 'cal': calendar(), 'verified': D.VERIFIED}
