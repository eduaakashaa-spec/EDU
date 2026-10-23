"""Seeding and scoring. Scoring is deterministic and rule-based (no hidden model), so every result can be explained.

Bands for objective skills: Secure >= 80%, Developing 50-79%, Needs reinforcement < 50%, and 'Too few items' when a skill has fewer
than MIN_ITEMS answered items (we do not label a skill from a single question). Self-report items stay separate (mean 1-5) and are
described as "how you see yourself", never as ability. Open-text and practical tasks are rated by a mentor against a visible rubric.
"""
import json
from datetime import date

from app.extensions import db
from app.futureready.content import assessments as A
from app.futureready.content import branches as BR
from app.futureready.content import extra as X
from app.futureready.models import (FrAdmission, FrAssessment, FrAttempt, FrBranch, FrQuestion, FrResource, FrSkillScore, _now, jl)

MIN_ITEMS = 2
SECURE, DEVELOPING = 80, 50

SKILL_LABELS = {
    'math': 'Mathematics', 'science': 'Science', 'reading': 'Reading', 'data': 'Data interpretation', 'sci_reason': 'Scientific reasoning',
    'numerical': 'Numerical reasoning', 'logical': 'Logical reasoning', 'patterns': 'Pattern recognition', 'verbal': 'Verbal reasoning',
    'spatial': 'Spatial reasoning', 'decomposition': 'Problem decomposition', 'decision': 'Decision-making', 'mechanical': 'Mechanical reasoning',
    'scientific': 'Scientific reasoning', 'digital': 'Digital logic', 'ai_use': 'Responsible AI use', 'safety': 'Digital safety',
    'evaluate': 'Evaluating information', 'verify': 'Verifying AI output', 'awareness': 'Entrance-system awareness',
    'planning': 'Planning', 'concentration': 'Concentration', 'time': 'Time management', 'revision': 'Revision', 'notes': 'Note-making',
    'questions': 'Asking questions', 'mistakes': 'Learning from mistakes', 'exam_prep': 'Exam preparation', 'help': 'Seeking help', 'consistency': 'Consistency',
    'social': 'Social energy', 'structure': 'Preference for structure', 'curiosity': 'Curiosity', 'regulation': 'Emotional regulation', 'empathy': 'Empathy',
    'analytical': 'Analytical approach', 'intuitive': 'Intuitive approach', 'evidence': 'Use of evidence',
    'listening': 'Listening', 'explaining': 'Explaining ideas', 'asking': 'Asking questions', 'teamwork': 'Teamwork', 'feedback': 'Using feedback', 'disagree': 'Handling disagreement',
    'selfmgmt': 'Self-management',
    'build': 'Building and making', 'design': 'Designing and drawing', 'puzzle': 'Solving puzzles', 'tech': 'Programming and technology',
    'people': 'Helping people', 'organise': 'Organising projects', 'investigate': 'Investigating how things work', 'communicate': 'Communicating ideas',
    'nature': 'Nature and sustainability',
    'understand': 'Understanding the problem', 'ideas': 'Generating ideas', 'creativity': 'Creativity', 'practical': 'Practicality',
    'reasoning': 'Explaining reasoning', 'reflection': 'Reflection and improvement',
    'confidence': 'Confidence', 'clarity': 'Self-understanding', 'support': 'Support', 'pressure': 'Felt pressure',
}


def label(skill):
    return SKILL_LABELS.get(skill, (skill or '').replace('_', ' ').capitalize())


def band(pct, n):
    if n < MIN_ITEMS:
        return 'Too few items'
    return 'Secure' if pct >= SECURE else 'Developing' if pct >= DEVELOPING else 'Needs reinforcement'


# ---- seeding ------------------------------------------------------------------------------------------------------------------
def _put_questions(a, items, start=0):
    have = {q.code for q in FrQuestion.query.filter_by(assessment_id=a.id).all()}
    pos = start
    for q in items:
        pos += 1
        if q['code'] in have:
            continue
        opts = q['options']
        db.session.add(FrQuestion(assessment_id=a.id, code=q['code'], position=pos, qtype=q['qtype'], prompt=q['prompt'], options_json=json.dumps(opts),
                                  answer_json=json.dumps(q['answer']) if q['answer'] is not None else None, explanation=q['explanation'],
                                  distractor_json=json.dumps(q['distractors']), skill=q['skill'], reverse=bool(q['reverse']), level=q['level'],
                                  grade_min=q['grade_min'], grade_max=q['grade_max'], meta_json=json.dumps(q['meta'])))


def seed_content():
    """Idempotent. Creates missing assessments, questions, branches, admissions and resources; never overwrites an administrator's edit."""
    n = 0
    pack = list(A.CORE) + [X.A11, X.A12, X.A_REFLECT, X.SAMPLER]
    for pos, d in enumerate(pack, 1):
        a = FrAssessment.query.filter_by(key=d['key']).first()
        if not a:
            a = FrAssessment(key=d['key'], number=d['number'], group=d['group'], title=d['title'], purpose=d['purpose'], instructions=d['instructions'],
                             minutes=d['minutes'], kind=d['kind'], interpretation=d['interpretation'], accessibility=d['accessibility'], position=pos,
                             review_date=date(2026, 10, 1))
            db.session.add(a)
            db.session.flush()
            n += 1
        _put_questions(a, d['questions'])
        meta = d.get('meta')
        if meta and not getattr(a, '_meta_set', False):
            pass
    for pos, b in enumerate(BR.BRANCHES, 1):
        if not FrBranch.query.filter_by(key=b['key']).first():
            db.session.add(FrBranch(key=b['key'], family=b['family'], name=b['name'], studies=b['studies'], problems=b['problems'], projects=b['projects'],
                                    foundations=b['foundations'], skills=b['skills'], activities=b['activities'], related=b['related'], environment=b['environment'],
                                    tags_json=json.dumps(b['tags']), position=pos, last_reviewed=date(2026, 10, 1)))
    for pos, a in enumerate(BR.ADMISSIONS, 1):
        if not FrAdmission.query.filter_by(key=a['key']).first():
            db.session.add(FrAdmission(key=a['key'], name=a['name'], classification=a['classification'], summary=a['summary'], how_it_works=a['how_it_works'],
                                       official_url=a['official_url'], status='needs_verification', position=pos))
    for r in BR.RESOURCES:
        if not FrResource.query.filter_by(key=r['key']).first():
            db.session.add(FrResource(**r))
    db.session.commit()
    return n


def rubric_meta(assessment_key='creativity'):
    for d in A.CORE:
        if d['key'] == assessment_key:
            return d.get('meta') or {}
    return {}


def foundations():
    return BR.FOUNDATIONS


# ---- scoring ------------------------------------------------------------------------------------------------------------------
def _qs(attempt):
    a = attempt.assessment
    qs = FrQuestion.query.filter_by(assessment_id=a.id, active=True).order_by(FrQuestion.position).all()
    if attempt.set_key and ':' in attempt.set_key:
        skill, level = attempt.set_key.split(':')
        qs = [q for q in qs if q.skill == skill and str(q.level) == level]
    if attempt.audience == 'parent':
        return [q for q in qs if (q.meta.get('audience') or 'both') in ('both', 'parent')]
    return qs


def questions_for(attempt):
    return _qs(attempt)


def score_attempt(attempt):
    """Score the saved responses; stores `result_json`, flat FrSkillScore rows, and returns the result dict."""
    resp = attempt.responses
    qs = _qs(attempt)
    obj, lik, tags, text, review = {}, {}, {}, {}, []
    answered = 0
    for q in qs:
        v = resp.get(q.code)
        if v in (None, '', []):
            continue
        answered += 1
        if q.qtype == 'mcq':
            ok = (int(v) == q.answer)
            s = obj.setdefault(q.skill, [0, 0]); s[1] += 1; s[0] += 1 if ok else 0
            opts = q.options
            review.append(dict(code=q.code, prompt=q.prompt, ok=ok, chosen=opts[int(v)] if 0 <= int(v) < len(opts) else '', right=opts[q.answer] if q.answer is not None else '',
                               why=q.explanation, hint=q.distractors.get(str(v)) if not ok else ''))
        elif q.qtype == 'multi' and q.answer is not None:
            ok = sorted(int(i) for i in v) == sorted(q.answer)
            s = obj.setdefault(q.skill, [0, 0]); s[1] += 1; s[0] += 1 if ok else 0
            opts = q.options
            review.append(dict(code=q.code, prompt=q.prompt, ok=ok, chosen='; '.join(opts[int(i)] for i in v if int(i) < len(opts)),
                               right='; '.join(opts[i] for i in q.answer), why=q.explanation, hint=''))
        elif q.qtype == 'likert':
            x = int(v)
            x = 6 - x if q.reverse else x
            lik.setdefault(q.skill, []).append(x)
        elif q.qtype == 'choice':
            opts = q.options
            if q.skill == 'challenge':
                text[q.code] = opts[int(v)] if isinstance(opts[int(v)], str) else opts[int(v)].get('t')
                continue
            ch = opts[int(v)] if 0 <= int(v) < len(opts) else None
            if ch and isinstance(ch, dict):
                for t, w in ch.get('tags', {}).items():
                    tags[t] = tags.get(t, 0) + w
        elif q.qtype == 'multi':
            opts = q.options
            text[q.code] = [opts[int(i)] for i in v if int(i) < len(opts)]
        elif q.qtype == 'text':
            text[q.code] = str(v)
    skills = {}
    for sk, (c, n) in obj.items():
        pct = round(100.0 * c / n, 0) if n else 0
        skills[sk] = dict(kind='objective', label=label(sk), correct=c, n=n, pct=pct, band=band(pct, n))
    for sk, vals in lik.items():
        m = round(sum(vals) / len(vals), 2)
        skills[sk] = dict(kind='self', label=label(sk), n=len(vals), mean=m, band='Strong tendency' if m >= 4 else 'Mixed' if m >= 3 else 'Less like me')
    total_n = sum(s['n'] for s in skills.values() if s['kind'] == 'objective')
    total_c = sum(s['correct'] for s in skills.values() if s['kind'] == 'objective')
    res = dict(answered=answered, total=len(qs), skills=skills, interest_tags=tags, text=text, review=review,
               overall_pct=round(100.0 * total_c / total_n, 0) if total_n else None, overall_n=total_n,
               note=attempt.assessment.interpretation or '')
    attempt.result_json = json.dumps(res)
    FrSkillScore.query.filter_by(attempt_id=attempt.id).delete()
    for sk, s in skills.items():
        db.session.add(FrSkillScore(profile_id=attempt.profile_id, attempt_id=attempt.id, assessment_key=attempt.assessment.key, skill=sk,
                                    kind=s['kind'], value=s.get('pct') if s['kind'] == 'objective' else s.get('mean'), n=s['n']))
    return res


def rate_rubric(attempt, ratings):
    """Mentor ratings 1-4 for each criterion of the practical task -> stored with a percentage and written to FrSkillScore."""
    meta = rubric_meta(attempt.assessment.key)
    keys = [k for k, _ in meta.get('criteria', [])]
    clean = {k: max(1, min(4, int(ratings.get(k)))) for k in keys if ratings.get(k) not in (None, '')}
    attempt.rubric_json = json.dumps(dict(ratings=clean, feedback=ratings.get('feedback', ''), rated_at=_now().isoformat()))
    FrSkillScore.query.filter_by(attempt_id=attempt.id, kind='rubric').delete()
    for k, v in clean.items():
        db.session.add(FrSkillScore(profile_id=attempt.profile_id, attempt_id=attempt.id, assessment_key=attempt.assessment.key, skill=k, kind='rubric',
                                    value=round(100.0 * (v - 1) / 3, 0), n=1))
    return clean


def latest_attempt(profile_id, key, audience='student', set_key=None, submitted=True):
    q = FrAttempt.query.join(FrAssessment).filter(FrAttempt.profile_id == profile_id, FrAssessment.key == key, FrAttempt.audience == audience)
    if set_key:
        q = q.filter(FrAttempt.set_key == set_key)
    if submitted:
        q = q.filter(FrAttempt.status == 'submitted')
    return q.order_by(FrAttempt.id.desc()).first()


def interest_profile(profile_id):
    """Combine the Interests Explorer (likert, 1-5 per domain) and the Branch Interest Map (scenario tally) into one 0-100 score per domain."""
    dom = {}
    a5 = latest_attempt(profile_id, 'interests')
    if a5:
        for k, s in a5.result.get('skills', {}).items():
            if s['kind'] == 'self':
                dom[k] = dom.get(k, 0) + (s['mean'] - 1) / 4 * 60
    a11 = latest_attempt(profile_id, 'eng_interest')
    tags = a11.result.get('interest_tags', {}) if a11 else {}
    top = max(tags.values()) if tags else 0
    for k, w in tags.items():
        dom[k] = dom.get(k, 0) + (w / top * 40 if top else 0)
    return {k: round(v) for k, v in sorted(dom.items(), key=lambda kv: -kv[1])}


def branch_matches(profile_id, limit=6):
    """Branches whose tag mix overlaps the student's interests the most. Returned as 'explore next' with the reasons, never as a ranking of fit."""
    prof = interest_profile(profile_id)
    if not prof:
        return []
    out = []
    for b in FrBranch.query.filter_by(active=True).all():
        tg = jl(b.tags_json, {})
        score, why = 0, []
        for k, w in tg.items():
            if prof.get(k):
                score += prof[k] * w
                if w >= 2 and prof[k] >= 40:
                    why.append(label(k))
        if score:
            out.append(dict(branch=b, score=score, why=why[:3]))
    out.sort(key=lambda r: -r['score'])
    mx = out[0]['score'] if out else 1
    for r in out:
        r['pct'] = round(100.0 * r['score'] / mx)
    return out[:limit]
