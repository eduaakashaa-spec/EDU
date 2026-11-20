"""JEE self-assessment gap map: a student's 0 to 4 ratings of 69 topics set against the JEE Main 2026 question analysis (19 shifts, 1,424 questions, chapter Tiers).

Why it matters (and how it is worked out, in plain words):
  * Each topic covers one or more chapters of app/data/jee_syllabus_2026.json. A chapter's weight is the number of questions it had in the 19 shifts of 2026; a chapter shared by two
    topics has its questions split between them. A paper has about 75 questions, so questions / 19 is what a chapter contributes to one paper, and 4 marks each.
  * What JEE Main needs: rating 3 ("comfortable with JEE Main level") for Tier 1 and Tier 2 topics, 2 ("knows the basics") for Tier 3, and 1 for topics with no question in 2026.
  * Gap = needed rating minus own rating (never below 0). Marks within reach per paper (the gap's cost) = questions per paper x 4 x gap / needed rating. It is a planning estimate, not a prediction.
  * Buckets: Fix first (2 or more marks within reach per paper), Fix next (0.8 or more), Maintain (no gap or very small), Park (no question in 2026: keep it for the end).
The same numbers set the order and time of a study plan: gaps with the most marks at risk come first, parked topics last.
"""
import json
import os
from functools import lru_cache

from app.data.jee_topics import SUBJECTS, TOPICS

NEED = {1: 3, 2: 3, 3: 2, 0: 1}                    # tier -> rating JEE Main needs (tier 0 = no question in the 2026 shifts)
TIER_LABEL = {1: 'Tier 1', 2: 'Tier 2', 3: 'Tier 3', 0: 'No 2026 question'}
TIER_WHY = {1: 'one of the most-asked chapters: it comes up in almost every shift',
            2: 'asked in most shifts, so a weak spot here shows up in most papers',
            3: 'asked now and then: enough to know the basics',
            0: 'not asked in any of the 19 shifts of 2026, so it can wait until the end'}
RATING_WORDS = ('never studied', 'heard of it', 'basics', 'comfortable at JEE Main level', 'confident at Advanced level')
FIX_FIRST, FIX_NEXT = 2.0, 0.8


@lru_cache(maxsize=1)
def _syllabus():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'jee_syllabus_2026.json'), encoding='utf-8') as f:
        data = json.load(f)
    chs = {c['ch']: c for c in data['chs']}
    return chs, int(data['stats']['NS']), int(data['stats']['NQ'])


def _tier_no(c):
    t = c.get('tier') or ''
    return int(t[-1]) if t.startswith('Tier') else 0


@lru_cache(maxsize=1)
def topics():
    """The 69 topics with their question weight, tier and what JEE Main needs. Independent of any student."""
    chs, shifts, nq = _syllabus()
    users = {}
    for code, _s, _n, names in TOPICS:
        for ch in names:
            users[ch] = users.get(ch, 0) + 1
    out = []
    for code, subj, name, names in TOPICS:
        cs = [chs[n] for n in names if n in chs]
        q = sum(c['n'] / users[c['ch']] for c in cs)
        tiers = [_tier_no(c) for c in cs if c['n'] > 0]
        tier = min(tiers) if tiers else 0
        lead = max(cs, key=lambda c: c['n']) if cs else {}
        out.append(dict(code=code, subject=subj, name=name, chapters=[c['ch'] for c in cs], q=round(q, 1), per_paper=q / shifts, share=100.0 * q / nq, tier=tier, need=NEED[tier],
                        hours=round(sum(c.get('hours', 0) for c in cs if c['n'] > 0) / max(1, sum(1 for c in cs if c['n'] > 0)), 1),
                        pre=lead.get('pre') or '', feeds=lead.get('feed') or ''))
    return out


def clean(ratings):
    """{code: 0..4} for the codes we know; anything else is ignored."""
    out = {}
    for t in topics():
        v = (ratings or {}).get(t['code'])
        try:
            v = int(v)
        except (TypeError, ValueError):
            continue
        if 0 <= v <= 4:
            out[t['code']] = v
    return out


def analyse(ratings):
    """The gap map. `ratings` is {code: 0..4}; unrated topics are left out of the maths and listed as `missing`."""
    r = clean(ratings)
    rows = []
    for t in topics():
        if t['code'] not in r:
            continue
        rating = r[t['code']]
        gap = max(0, t['need'] - rating)
        risk = t['per_paper'] * 4 * gap / t['need'] if t['need'] else 0
        if t['tier'] == 0:
            bucket = 'Park'
        elif risk >= FIX_FIRST:
            bucket = 'Fix first'
        elif risk >= FIX_NEXT:
            bucket = 'Fix next'
        else:
            bucket = 'Maintain'
        row = dict(t, rating=rating, gap=gap, risk=risk, bucket=bucket)
        row['why'] = why(row)
        rows.append(row)
    rows.sort(key=lambda x: (-x['risk'], -x['q'], x['code']))
    by_subject = {}
    for s in SUBJECTS:
        rs = [x for x in rows if x['subject'] == s]
        wt = sum(x['q'] for x in rs if x['need'] > 1) or 1
        ready = sum(x['q'] * min(x['rating'], x['need']) / x['need'] for x in rs if x['need'] > 1) / wt
        by_subject[s] = dict(subject=s, readiness=round(100 * ready), risk=sum(x['risk'] for x in rs), n=len(rs), fix_first=sum(1 for x in rs if x['bucket'] == 'Fix first'),
                             fix_next=sum(1 for x in rs if x['bucket'] == 'Fix next'), parked=sum(1 for x in rs if x['bucket'] == 'Park'), weak=sum(1 for x in rs if x['rating'] <= 1))
    total_risk = sum(x['risk'] for x in rows)
    top5 = sum(x['risk'] for x in rows[:5])
    wt = sum(x['q'] for x in rows if x['need'] > 1) or 1
    return dict(rows=rows, missing=[t['code'] for t in topics() if t['code'] not in r], by_subject=by_subject, total_risk=total_risk, top5_share=(100 * top5 / total_risk) if total_risk else 0,
                readiness=round(100 * sum(x['q'] * min(x['rating'], x['need']) / x['need'] for x in rows if x['need'] > 1) / wt), complete=len(r) == len(topics()),
                weak_count=sum(1 for x in rows if x['rating'] <= 1), parked_weak=[x for x in rows if x['bucket'] == 'Park' and x['rating'] <= 1],
                strengths=sorted([x for x in rows if x['rating'] >= 3 and x['tier'] in (1, 2)], key=lambda x: -x['q'])[:5])


def why(x):
    base = '%s: %s. ' % (TIER_LABEL[x['tier']], TIER_WHY[x['tier']][0].upper() + TIER_WHY[x['tier']][1:])
    if x['tier'] == 0:
        return base + 'You rated it %d (%s). Revisit it after the Tier 1 and Tier 2 gaps.' % (x['rating'], RATING_WORDS[x['rating']])
    s = '%s %d question%s in 19 shifts, about %.1f per paper (%.1f%% of all questions). ' % (base, round(x['q']), '' if round(x['q']) == 1 else 's', x['per_paper'], x['share'])
    if x['gap']:
        s += 'You rated it %d (%s) and JEE Main needs %d, so about %.1f marks per paper are within reach if you close the gap.' % (x['rating'], RATING_WORDS[x['rating']], x['need'], x['risk'])
    else:
        s += 'You rated it %d (%s): this is %s.' % (x['rating'], RATING_WORDS[x['rating']], 'a sure-mark topic: protect it with short revision' if x['tier'] in (1, 2) else 'enough for now')
    if x['gap'] and x['pre']:
        s += ' It builds on: %s.' % x['pre']
    if x['gap'] and x['feeds']:
        s += ' It feeds: %s.' % x['feeds']
    return s


def plan_order(analysis):
    """{subject: [(topic name, bucket, note)]}: the order and repetition a study plan should use. Fix-first topics appear twice (learn, then practise), Park topics once at the end."""
    out = {s: [] for s in SUBJECTS}
    for bucket in ('Fix first', 'Fix next', 'Maintain', 'Park'):
        for x in analysis['rows']:
            if x['bucket'] != bucket:
                continue
            note = 'Gap map: rated %d, JEE Main needs %d, %s, about %.1f marks per paper within reach.' % (x['rating'], x['need'], TIER_LABEL[x['tier']], x['risk']) if x['gap'] and x['need'] > 1 else \
                ('Gap map: no question in the 19 shifts of 2026, kept for the end.' if bucket == 'Park' else 'Gap map: already at the level JEE Main needs: short revision.')
            reps = 2 if bucket == 'Fix first' else 1
            for _ in range(reps):
                out[x['subject']].append((x['name'], bucket, note))
    return out
