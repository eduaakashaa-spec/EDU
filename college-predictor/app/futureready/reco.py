"""Rule-based recommendations. Every suggestion carries its evidence (which result triggered it, on how many items) and who must review it.
There is no hidden model: the same results always give the same suggestions, and a mentor approves them before the family sees them."""
import json

from app.extensions import db
from app.futureready import engine
from app.futureready.models import FrAction, FrAttempt, FrRecommendation, FrResource, FrSkillScore

HABIT_SKILLS = {'planning', 'concentration', 'time', 'revision', 'notes', 'questions', 'mistakes', 'exam_prep', 'help', 'consistency', 'selfmgmt'}
SKILL_TO_RES = {'sci_reason': 'sci_reason', 'scientific': 'sci_reason', 'numerical': 'numerical', 'patterns': 'patterns', 'logical': 'logical',
                'verbal': 'reading', 'reading': 'reading', 'spatial': 'build', 'mechanical': 'build', 'decomposition': 'decomposition',
                'decision': 'decomposition', 'digital': 'tech', 'ai_use': 'ai_use', 'verify': 'verify', 'evaluate': 'evaluate', 'safety': 'safety',
                'awareness': 'awareness', 'math': 'math', 'science': 'science', 'data': 'data'}
MAX_RECS = 8


def _resources_for(skill):
    k = SKILL_TO_RES.get(skill, skill)
    return [r for r in FrResource.query.filter_by(active=True).all() if k in (r.skills or '').split(',') or skill in (r.skills or '').split(',')]


def latest_skills(profile_id):
    """Latest value per (assessment, skill) across submitted attempts."""
    rows = (FrSkillScore.query.join(FrAttempt, FrAttempt.id == FrSkillScore.attempt_id)
            .filter(FrSkillScore.profile_id == profile_id, FrAttempt.status == 'submitted', FrAttempt.audience == 'student')
            .order_by(FrSkillScore.id).all())
    out = {}
    for r in rows:
        out[(r.assessment_key, r.skill)] = r
    return out


def generate(profile):
    """Create new suggestions from the latest results. Existing rules are not duplicated; dismissed ones stay dismissed."""
    have = {r.rule_key for r in FrRecommendation.query.filter_by(profile_id=profile.id).all()}
    made = []

    def add(rule, res, title, why, evidence, learn=None):
        if rule in have or len(made) + len(have) >= MAX_RECS * 3:
            return
        have.add(rule)
        r = FrRecommendation(profile_id=profile.id, rule_key=rule, resource_key=res.key if res else None, title=title or (res.title if res else ''), why=why,
                             learn=learn or (res.body if res else ''), minutes=res.minutes if res else None, materials=res.materials if res else '',
                             assessed_by=res.assessed_by if res else 'Discussed in the next mentor session.',
                             next_step='Do it this week, then show or tell your mentor.' if res else 'Mentor will guide the conversation.',
                             evidence_json=json.dumps(evidence))
        db.session.add(r)
        made.append(r)

    sk = latest_skills(profile.id)
    # 1. objective gaps
    gaps = sorted([(v.value, k, v) for k, v in sk.items() if v.kind == 'objective' and v.n >= engine.MIN_ITEMS and v.value < engine.SECURE], key=lambda t: t[0])
    for val, (akey, skill), v in gaps[:4]:
        for res in _resources_for(skill)[:1]:
            tone = 'Needs reinforcement' if val < engine.DEVELOPING else 'Developing'
            add(f'gap:{akey}:{skill}', res, None, f'Your {engine.label(skill)} result was {int(val)}% on {v.n} question(s) ({tone}). A short practice task is the quickest way to strengthen it. One short set is only a snapshot, so we will check again.',
                dict(assessment=akey, skill=skill, value=val, n=v.n, kind='objective'))
    # 2. habits (self-reported)
    for (akey, skill), v in sorted(sk.items(), key=lambda kv: kv[1].value or 9):
        if v.kind == 'self' and skill in HABIT_SKILLS and v.value is not None and v.value < 3:
            for res in _resources_for(skill)[:1]:
                add(f'habit:{skill}', res, None, f'You said {engine.label(skill).lower()} is “less like me” right now (average {v.value:.1f} out of 5). That is your own view, and habits change quickly with practice.',
                    dict(assessment=akey, skill=skill, value=v.value, n=v.n, kind='self'))
                break
        if sum(1 for r in made if r.rule_key.startswith('habit:')) >= 2:
            break
    # 3. interests -> projects
    prof = engine.interest_profile(profile.id)
    for dom, sc in list(prof.items())[:2]:
        if sc < 40:
            continue
        for res in _resources_for(dom)[:1]:
            add(f'interest:{dom}', res, None, f'{engine.label(dom)} showed up as one of your stronger interests. A hands-on project is the best way to find out whether you enjoy it in practice.',
                dict(domain=dom, score=sc, kind='interest'))
    # 4. digital literacy
    for (akey, skill), v in sk.items():
        if akey == 'ai_literacy' and v.kind == 'objective' and v.n >= 2 and v.value < engine.SECURE:
            res = next(iter(_resources_for('ai_use' if skill in ('ai_use', 'verify', 'evaluate') else 'safety')), None)
            if res:
                add(f'ai:{skill}', res, None, f'Your {engine.label(skill)} result was {int(v.value)}% on {v.n} question(s). Safe, critical use of AI tools is worth practising early.',
                    dict(assessment=akey, skill=skill, value=v.value, n=v.n, kind='objective'))
    # 5. alignment gap
    from app.futureready import reports
    al = reports.alignment(profile)
    if al and al.get('gaps'):
        add('family:alignment', None, 'Family conversation: where your views differ',
            'You and your parent answered some questions differently: ' + '; '.join(al['gaps'][:3]) + '. Differences are normal and useful to talk about.',
            dict(kind='alignment', gaps=al['gaps']), learn='Each of you shares one thing you noticed in the other’s answers. Listen first, then share your own view. Bring one question to your mentor.')
    db.session.commit()
    return made


def visible_to_family(profile_id):
    return FrRecommendation.query.filter_by(profile_id=profile_id, approved=True).filter(FrRecommendation.status != 'Dismissed').order_by(FrRecommendation.id.desc()).all()


def accept_as_action(rec, profile, owner='student'):
    """Turn an approved recommendation into an action the student can track."""
    a = FrAction(profile_id=profile.id, title=rec.title, detail=rec.learn, why=rec.why[:300] if rec.why else '', owner=owner, source='recommendation',
                 resource_key=rec.resource_key)
    rec.status = 'Accepted'
    db.session.add(a)
    return a
