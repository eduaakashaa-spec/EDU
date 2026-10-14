"""Assessment results — one structured store for every assessment the site runs.

Replaces the per-page Google Sheets / Apps Script backends. Every submission,
whatever page it came from, becomes one `AssessmentResult` row:

    identity    student / parent name, email, phone, school, city, board, class
    outcome     result_label (headline), result_score, scores_json (normalised)
    raw         payload_json (the complete submission, answers included)

That gives members and mentors one place to read results and gives analysis a
flat, queryable table (see the Excel export in routes/assessments.py).
"""
import hashlib
import json
import re
from datetime import datetime, timezone

from app.extensions import db
from app.models import AssessmentResult, User

# slug -> human label (also the filter list in the admin UI)
SOURCES = {
    'stream-selection': 'Stream Selection',
    'student-assessment': 'Student Assessment',
    'josaa-assessment': 'JoSAA Assessment',
    'per-assessment': 'Personal Evaluation',
    'branch-fitness': 'Branch Fitness',
    'conflict-assessment': 'Parent–Student Conflict',
    'free-report': 'Free Report',
    'tnea_expert': 'TNEA Expert',
    'tnea-expert': 'TNEA Expert',
}
# /api/leads sources that are assessments (everything else stays a plain lead)
ASSESSMENT_SOURCES = set(SOURCES)

_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
MAX_PAYLOAD = 300_000


def label_for(source):
    return SOURCES.get(source) or (source or 'Assessment').replace('-', ' ').replace('_', ' ').title()


# --------------------------------------------------------------------------- #
# field extraction helpers
# --------------------------------------------------------------------------- #
def _norm_key(k):
    return re.sub(r'[^a-z0-9]', '', str(k).lower())


def dig(data, aliases, depth=4):
    """First non-empty scalar found under any alias key (case/punct-insensitive),
    searching nested dicts breadth-first up to `depth` levels."""
    want = {_norm_key(a) for a in aliases}
    level = [data]
    for _ in range(depth):
        nxt = []
        for node in level:
            if not isinstance(node, dict):
                continue
            for k, v in node.items():
                if _norm_key(k) in want and isinstance(v, (str, int, float)) and str(v).strip():
                    return str(v).strip()
            nxt.extend(v for v in node.values() if isinstance(v, dict))
        level = nxt
    return ''


def _section(data, names):
    """The first nested dict stored under one of `names`, else {}."""
    want = {_norm_key(n) for n in names}
    for k, v in (data or {}).items():
        if _norm_key(k) in want and isinstance(v, dict):
            return v
    return {}


def _clip(v, n):
    return (str(v).strip() if v is not None else '')[:n]


def _email(v):
    v = _clip(v, 200).lower()
    return v if _EMAIL.match(v) else ''


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# per-source normalisation
# --------------------------------------------------------------------------- #
def _extract(source, data):
    """-> dict of column values for AssessmentResult (never raises)."""
    stu = _section(data, ['studentInfo', 'student', 'studentDetails'])
    par = _section(data, ['parentInfo', 'parent', 'parentDetails'])
    res = _section(data, ['results', 'result', 'summary', 'report'])

    out = {
        'student_name': dig(stu or data, ['studentName', 'name', 'fullName', 'candidateName']),
        'student_email': dig(stu or data, ['studentEmail', 'email', 'candidateEmail']),
        'student_phone': dig(stu or data, ['studentPhone', 'phone', 'mobile', 'studentMobile']),
        'parent_name': dig(par or data, ['parentName', 'guardianName', 'name']) if par else dig(data, ['parentName', 'guardianName']),
        'parent_email': dig(par or data, ['parentEmail', 'guardianEmail', 'email']) if par else dig(data, ['parentEmail', 'guardianEmail']),
        'parent_phone': dig(par or data, ['parentPhone', 'parentMobile', 'phone', 'mobile']) if par else dig(data, ['parentPhone', 'parentMobile']),
        'school': dig(stu or data, ['school', 'schoolName', 'institution']),
        'city': dig(stu or data, ['city', 'location']),
        'board': dig(stu or data, ['board', 'boardName']),
        'current_class': dig(stu or data, ['currentClass', 'class', 'grade', 'standard']),
        'lang': dig(data, ['reportLang', 'lang', 'language'])[:8],
    }

    label, score, scores = '', None, {}
    if res:
        label = dig(res, ['recommended', 'recommendedStream', 'topStream', 'stream', 'recommendation', 'topMatch',
                          'bestFit', 'branch', 'verdict'])
        pct = res.get('percentages') or res.get('percent') or res.get('scores')
        if isinstance(pct, dict):
            scores = {str(k): v for k, v in pct.items() if _to_float(v) is not None}
        apt = _to_float(res.get('aptitudeScore'))
        tot = _to_float(res.get('aptitudeTotal')) or 15
        if apt is not None:
            score = round(apt / tot * 100, 1)
    if not label:
        label = dig(data, ['recommended', 'recommendedStream', 'topStream', 'recommendation', 'topBranch', 'verdict', 'result'])
    if score is None:
        score = _to_float(dig(data, ['score', 'totalScore', 'overallScore', 'readiness', 'fitScore']))
    out.update(result_label=label, result_score=score, scores=scores)
    return out


# --------------------------------------------------------------------------- #
# ingest / lookup
# --------------------------------------------------------------------------- #
def _link_user(user, ex):
    """The member this belongs to: the logged-in user, else an email match."""
    if user is not None and getattr(user, 'is_authenticated', False):
        return user
    for key in ('student_email', 'parent_email'):
        em = _email(ex.get(key))
        if em:
            u = User.query.filter(db.func.lower(User.email) == em).first()
            if u:
                return u
    return None


def ingest(source, data, user=None, origin='web', source_ref=None, created_at=None, commit=True):
    """Store one assessment submission. Returns the row, or the existing row for a
    repeated import (same source + source_ref)."""
    source = _clip(source or 'unknown', 60).lower().replace(' ', '-')
    if not isinstance(data, dict):
        data = {'value': data}
    payload = json.dumps(data, ensure_ascii=False, default=str)
    if len(payload) > MAX_PAYLOAD:
        payload = json.dumps({'truncated': True, 'original_size': len(payload)})
    if source_ref:
        existing = AssessmentResult.query.filter_by(source=source, source_ref=str(source_ref)[:80]).first()
        if existing:
            return existing

    ex = _extract(source, data)
    member = _link_user(user, ex)
    row = AssessmentResult(
        user_id=member.id if member is not None else None,
        source=source,
        student_name=_clip(ex['student_name'], 150),
        student_email=_email(ex['student_email']) or None,
        student_phone=_clip(ex['student_phone'], 40),
        parent_name=_clip(ex['parent_name'], 150),
        parent_email=_email(ex['parent_email']) or None,
        parent_phone=_clip(ex['parent_phone'], 40),
        school=_clip(ex['school'], 200), city=_clip(ex['city'], 120),
        board=_clip(ex['board'], 60), current_class=_clip(ex['current_class'], 40),
        result_label=_clip(ex['result_label'], 200),
        result_score=ex['result_score'],
        scores_json=json.dumps(ex['scores'], ensure_ascii=False) if ex['scores'] else None,
        payload_json=payload, lang=ex['lang'], origin=origin,
        source_ref=str(source_ref)[:80] if source_ref else None,
    )
    if created_at is not None:
        row.created_at = created_at
    db.session.add(row)
    if commit:
        db.session.commit()
    return row


def for_user(user):
    """Everything belonging to this member: linked by account, or by the same
    email on the student/parent side (results captured before they registered)."""
    em = (user.email or '').strip().lower()
    cond = [AssessmentResult.user_id == user.id]
    if em:
        cond += [db.func.lower(AssessmentResult.student_email) == em,
                 db.func.lower(AssessmentResult.parent_email) == em]
    return (AssessmentResult.query.filter(db.or_(*cond))
            .order_by(AssessmentResult.created_at.desc()))


def can_view(user, row):
    if getattr(user, 'is_staff', False):
        return True
    if row.user_id == user.id:
        return True
    em = (user.email or '').strip().lower()
    return bool(em) and em in {(row.student_email or '').lower(), (row.parent_email or '').lower()}


# --------------------------------------------------------------------------- #
# display model
# --------------------------------------------------------------------------- #
_SKIP_FACT_KEYS = {'answers', 'responses', 'personalityans', 'aptitudeans', 'applicationans', 'confidencedata',
                   'payload', 'value', 'questions', 'raw', 'html'}


def _scalar_facts(d, prefix='', limit=40):
    facts = []
    for k, v in (d or {}).items():
        if _norm_key(k) in _SKIP_FACT_KEYS:
            continue
        if isinstance(v, (str, int, float)) and str(v).strip() and len(str(v)) <= 300:
            facts.append((prefix + str(k), v))
        elif isinstance(v, dict):
            facts.extend(_scalar_facts(v, prefix + str(k) + ' › ', limit))
        if len(facts) >= limit:
            break
    return facts[:limit]


def summarize(row):
    """Structured, template-friendly view of one result."""
    data = row.payload
    res = _section(data, ['results', 'result'])
    risks = []
    for r in (res.get('risks') or []):
        if isinstance(r, dict):
            risks.append({'flag': r.get('flag', ''), 'detail': r.get('detail', ''), 'severity': r.get('severity', 'info')})
    gap = []
    for g in (data.get('skillGap') or res.get('skillGap') or []):
        if isinstance(g, dict) and 'skill' in g:
            gap.append(g)
    radar = res.get('radarData') if isinstance(res.get('radarData'), dict) else {}
    scores = row.scores
    pref = dig(data, ['studentPreference', 'preferredStream']) if row.source == 'stream-selection' else ''
    par_pref = dig(_section(data, ['parentInfo', 'parent']), ['preferredStream'])
    careers = data.get('topCareers') if isinstance(data.get('topCareers'), list) else []
    return {
        'title': label_for(row.source),
        'headline': row.result_label,
        'score': row.result_score,
        'scores': sorted(scores.items(), key=lambda kv: -(_to_float(kv[1]) or 0)),
        'radar': sorted(radar.items(), key=lambda kv: -(_to_float(kv[1]) or 0)),
        'risks': risks,
        'skill_gap': gap,
        'student_pref': pref,
        'parent_pref': par_pref,
        'careers': [c.get('title') for c in careers if isinstance(c, dict) and c.get('title')][:8],
        'facts': _scalar_facts({k: v for k, v in data.items()
                                if _norm_key(k) not in ('studentinfo', 'parentinfo', 'results', 'skillgap', 'topcareers', 'streaminfo')}),
        'answered': {k: len(v) for k, v in data.items()
                     if _norm_key(k) in ('personalityans', 'aptitudeans', 'applicationans') and isinstance(v, dict)},
    }


def content_hash(obj):
    return hashlib.sha1(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode('utf-8')).hexdigest()[:40]
