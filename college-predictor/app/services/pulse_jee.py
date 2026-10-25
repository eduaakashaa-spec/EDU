"""EduPulse-JEE: saving finished JEE Main mocks and the negative-marking / confidence analysis used by the student, mentor and PDF reports.

Marking (JEE Main 2027, Paper 1): +4 correct, -1 wrong, 0 blank, in both MCQ and numerical sections. An answer pays off on average only if it is
right more than 1 time in 5 (4p - (1 - p) > 0), so the break-even accuracy is 20%.
Confidence codes: G guess, L low, M medium, H high. 'Avoidable' = wrong answers rated Guess or Low. 'Sure but wrong' = wrong answers rated High.
"""
import json
import os
import re
from datetime import datetime
from io import BytesIO

from app.extensions import db
from app.models_pulse import PulseJeeResult

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'jee_mock', 'data')
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}
BREAK_EVEN = 20
MAX_BODY = 300_000
MIN_RATED = 10
RIGHT, WRONG = 4, 1


def papers():
    try:
        with open(os.path.join(DATA_DIR, 'index.json'), encoding='utf-8') as f:
            return json.load(f)['papers']
    except (OSError, ValueError):
        return []


def valid_papers():
    return {p['y']: p for p in papers() if p.get('ready')}


def _num(v, default=0.0, lo=-1e6, hi=1e6):
    try:
        return max(lo, min(hi, float(v)))
    except (TypeError, ValueError):
        return default


def _dt(s):
    try:
        return datetime.fromisoformat(str(s).replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        return None


def ev(p):
    """Expected marks of one attempt that is right with probability p (0-1)."""
    return round(RIGHT * p - WRONG * (1 - p), 2)


def clean_payload(d):
    if not isinstance(d, dict):
        return None, 'bad payload'
    paper = str(d.get('paper') or '')
    meta = valid_papers().get(paper)
    if not meta:
        return None, 'unknown paper'
    qs = d.get('questions') or {}
    if not isinstance(qs, dict) or len(qs) > 80:
        return None, 'bad questions'
    out = {}
    for k, q in qs.items():
        if not isinstance(q, dict) or not re.fullmatch(r'\d{1,2}', str(k)):
            continue
        st = q.get('status') if q.get('status') in ('right', 'wrong', 'blank', 'bonus') else 'blank'
        cf = q.get('confidence') if q.get('confidence') in ('G', 'L', 'M', 'H') else None
        topic = q.get('topic') if isinstance(q.get('topic'), str) and re.fullmatch(r'[A-Z]{3}', q['topic']) else None
        out[str(k)] = {'type': 'NAT' if q.get('type') == 'NAT' else 'MCQ', 'subj': q.get('subj') if q.get('subj') in SUBJ else None, 'topic': topic,
                       'answer': None if q.get('answer') is None else str(q.get('answer'))[:20], 'official': str(q.get('official') or '')[:30], 'status': st,
                       'marks': round(_num(q.get('marks'), 0, -5, 5), 2), 'confidence': cf, 'sec': int(_num(q.get('sec'), 0, 0, 7200))}
    secs = []
    for s in (d.get('sections') or [])[:8]:
        if isinstance(s, dict):
            secs.append({'type': 'NAT' if s.get('type') == 'NAT' else 'MCQ', 'subj': s.get('subj') if s.get('subj') in SUBJ else None, 'score': round(_num(s.get('score')), 2),
                         'max': round(_num(s.get('max')), 2), 'right': int(_num(s.get('right'))), 'wrong': int(_num(s.get('wrong'))), 'blank': int(_num(s.get('blank')))})
    return {'paper': paper, 'paperTitle': meta['title'][:80], 'mode': 'mock' if d.get('mode') == 'mock' else 'practice', 'score': round(_num(d.get('score'), 0, -75, 300), 2),
            'max': float(meta.get('max') or 300), 'sections': secs, 'questions': out, 'startedAt': d.get('startedAt'), 'finishedAt': d.get('finishedAt'),
            'autoSubmitted': bool(d.get('autoSubmitted'))}, None


def save_result(user_id, d):
    p, err = clean_payload(d)
    if err:
        return None, err
    qs = list(p['questions'].values())
    right = [q for q in qs if q['status'] in ('right', 'bonus')]
    wrong = [q for q in qs if q['status'] == 'wrong']
    subj_score = {k: round(sum(q['marks'] for q in qs if q['subj'] == k), 2) for k in SUBJ}
    s, f = _dt(p['startedAt']), _dt(p['finishedAt']) or datetime.utcnow()
    r = PulseJeeResult(user_id=user_id, paper=p['paper'], paper_title=p['paperTitle'], mode=p['mode'], score=p['score'], max_score=p['max'],
                       attempted=len(right) + len(wrong), right=len(right), wrong=len(wrong), blank=sum(1 for q in qs if q['status'] == 'blank'),
                       gained=sum(q['marks'] for q in qs if q['marks'] > 0), lost=-sum(q['marks'] for q in qs if q['marks'] < 0),
                       avoidable=sum(1 for q in wrong if q['confidence'] in ('G', 'L')), sure_wrong=sum(1 for q in wrong if q['confidence'] == 'H'),
                       rated=sum(1 for q in qs if q['confidence'] and q['status'] != 'blank'), math_score=subj_score['MATH'], phy_score=subj_score['PHY'], chem_score=subj_score['CHEM'],
                       duration_sec=int((f - s).total_seconds()) if s else None, auto_submitted=p['autoSubmitted'], started_at=s, finished_at=f,
                       payload_json=json.dumps(p, separators=(',', ':')))
    db.session.add(r)
    db.session.commit()
    return r, None


def analyse(rows):
    """Negative-marking, confidence, subject and chapter analysis over one or more attempts."""
    conf = {c: {'n': 0, 'right': 0, 'wrong': 0, 'net': 0.0} for c, _ in CONF}
    subj = {k: {'att': 0, 'right': 0, 'wrong': 0, 'blank': 0, 'gain': 0.0, 'loss': 0.0} for k in SUBJ}
    chap, kind = {}, {'MCQ': {'att': 0, 'wrong': 0, 'loss': 0.0}, 'NAT': {'att': 0, 'wrong': 0, 'loss': 0.0}}
    unrated_wrong = 0
    wrong_secs, right_secs = [], []
    for r in rows:
        p = json.loads(r.payload_json or '{}')
        for q in (p.get('questions') or {}).values():
            st, sb = q['status'], q.get('subj')
            if sb in subj:
                a = subj[sb]
                if st in ('right', 'bonus'):
                    a['att'] += 1; a['right'] += 1
                elif st == 'wrong':
                    a['att'] += 1; a['wrong'] += 1
                else:
                    a['blank'] += 1
                if q['marks'] > 0:
                    a['gain'] += q['marks']
                elif q['marks'] < 0:
                    a['loss'] += -q['marks']
            if st == 'blank':
                continue
            ok, bad = st in ('right', 'bonus'), st == 'wrong'
            k = kind[q['type']]
            k['att'] += 1
            if bad:
                k['wrong'] += 1; k['loss'] += -q['marks']
                (wrong_secs if q.get('sec') else []).append(q['sec'])
            elif ok and q.get('sec'):
                right_secs.append(q['sec'])
            c = q['confidence']
            if c:
                x = conf[c]
                x['n'] += 1; x['right'] += 1 if ok else 0; x['wrong'] += 1 if bad else 0; x['net'] += q['marks']
            elif bad:
                unrated_wrong += 1
            if q.get('topic'):
                t = chap.setdefault(q['topic'], {'n': 0, 'right': 0, 'wrong': 0, 'sure_wrong': 0, 'score': 0.0, 'subj': sb})
                t['n'] += 1; t['right'] += 1 if ok else 0; t['wrong'] += 1 if bad else 0; t['score'] += q['marks']
                t['sure_wrong'] += 1 if (bad and c == 'H') else 0
    for x in conf.values():
        x['pct'] = round(100 * x['right'] / x['n']) if x['n'] else None
        x['ev'] = ev(x['right'] / x['n']) if x['n'] else None
        x['net'] = round(x['net'], 2)
    for a in subj.values():
        a['acc'] = round(100 * a['right'] / a['att']) if a['att'] else None
        a['gain'], a['loss'] = round(a['gain'], 2), round(a['loss'], 2)
    rated = sum(c['n'] for c in conf.values())
    gl = conf['G']['n'] + conf['L']['n']
    gl_net = round(conf['G']['net'] + conf['L']['net'], 2)
    avoidable = conf['G']['wrong'] + conf['L']['wrong']
    sure_wrong = conf['H']['wrong']
    total_loss = round(sum(a['loss'] for a in subj.values()), 2)
    total_gain = round(sum(a['gain'] for a in subj.values()), 2)
    notes = []
    if total_loss:
        notes.append('Negative marking took %s marks (%d%% of the marks you earned).' % (('%g' % total_loss), round(100 * total_loss / total_gain)) if total_gain else 'Negative marking took %g marks and you earned none.' % total_loss)
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to judge guessing. Rate every answer in the next mock.')
    else:
        if gl >= 4:
            if gl_net > 0:
                notes.append('Your %d Guess/Low answers scored %+g overall. Guessing helped, but only keep it where you can rule out at least one option.' % (gl, gl_net))
            elif gl_net < 0:
                notes.append('Your %d Guess/Low answers scored %+g overall, so they cost marks. Leave a question blank unless you can rule out at least two options.' % (gl, gl_net))
            else:
                notes.append('Your %d Guess/Low answers broke even (%+g).' % (gl, gl_net))
        if conf['H']['n'] >= 4 and conf['H']['pct'] is not None and conf['H']['pct'] < 70:
            notes.append('High-confidence answers were right only %d%% of the time. Revisit the %d confident mistakes first: they point to a wrong method or concept, not bad luck.' % (conf['H']['pct'], sure_wrong))
        low = [c for c in ('L', 'G') if conf[c]['n'] >= 3 and conf[c]['pct'] is not None and conf[c]['pct'] < BREAK_EVEN]
        if low:
            notes.append('Your %s answers were right less than %d%% of the time, which is below break-even for +4/−1 marking.' % (' and '.join(CONF_LABEL[c] for c in low), BREAK_EVEN))
    if kind['NAT']['wrong'] >= 2:
        notes.append('%d wrong numerical answers cost %g marks. A numerical answer has no lucky guess, so attempt it only after checking the working.' % (kind['NAT']['wrong'], kind['NAT']['loss']))
    weak = [k for k, t in sorted(chap.items(), key=lambda kv: kv[1]['score'] / max(kv[1]['n'], 1)) if t['n'] >= 3 and t['score'] / t['n'] < 1.5][:3]
    return {'conf': conf, 'subj': subj, 'chap': chap, 'kind': kind, 'rated': rated, 'avoidable': avoidable, 'sure_wrong': sure_wrong, 'gl_net': gl_net, 'gl_n': gl, 'unrated_wrong': unrated_wrong,
            'gain': total_gain, 'loss': total_loss, 'notes': notes, 'weak': weak, 'enough': rated >= MIN_RATED,
            'sec_wrong': round(sum(wrong_secs) / len(wrong_secs)) if wrong_secs else None, 'sec_right': round(sum(right_secs) / len(right_secs)) if right_secs else None}


def for_user(user_id, limit=None):
    q = PulseJeeResult.query.filter_by(user_id=user_id).order_by(PulseJeeResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    if not rows:
        return {'attempts': 0, 'rows': [], 'best': None, 'avg_pct': None, 'trend': [], 'an': analyse([]), 'avoidable_rate': None, 'loss_total': 0}
    pct = [round(100 * r.score / r.max_score) for r in reversed(rows) if r.max_score]
    att = sum(r.attempted or 0 for r in rows)
    return {'attempts': len(rows), 'rows': rows, 'best': max(rows, key=lambda r: (r.score or 0)), 'avg_pct': round(sum(pct) / len(pct)) if pct else None, 'trend': pct[-10:], 'an': analyse(rows),
            'avoidable_rate': round(100 * sum(r.avoidable or 0 for r in rows) / att) if att else None, 'loss_total': round(sum(r.lost or 0 for r in rows), 2)}


def pdf(result, student_name):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    an = analyse([result])
    ss = getSampleStyleSheet()
    H = ParagraphStyle('h', parent=ss['Heading1'], textColor=colors.HexColor('#0E3A8A'), fontSize=19, spaceAfter=4)
    H2 = ParagraphStyle('h2', parent=ss['Heading2'], textColor=colors.HexColor('#0E3A8A'), fontSize=12.5, spaceBefore=10, spaceAfter=4)
    P = ParagraphStyle('p', parent=ss['BodyText'], fontSize=9.5, leading=13, textColor=colors.HexColor('#0E1B3D'))
    SM = ParagraphStyle('sm', parent=P, fontSize=8, textColor=colors.HexColor('#5A6278'))
    esc = lambda t: str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def table(rows, widths, head):
        t = Table([head] + rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0E3A8A')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                               ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5EFDF')]), ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E8DFC8'))]))
        return t

    el = [Paragraph('EduAakashaa · EduPulse-JEE Mock Test Centre', SM), Paragraph(esc(result.paper_title) + ' · mock report', H),
          Paragraph('%s · %s · %s' % (esc(student_name), 'timed mock' if result.mode == 'mock' else 'practice', (result.finished_at or datetime.utcnow()).strftime('%d %b %Y')), P), Spacer(1, 6),
          Paragraph('<b>Score: %g / %g</b> · %d right · %d wrong · %d blank · marks gained %g, marks lost to negative marking %g' %
                    (result.score, result.max_score, result.right, result.wrong, result.blank, result.gained or 0, result.lost or 0), P)]
    el += [Paragraph('By subject', H2), table([[SUBJ[k], a['att'], a['right'], a['wrong'], ('%d%%' % a['acc']) if a['acc'] is not None else '-', '+%g' % a['gain'], '-%g' % a['loss'], '%+g' % (a['gain'] - a['loss'])] for k, a in an['subj'].items()],
                                              [32 * mm, 22 * mm, 18 * mm, 18 * mm, 22 * mm, 20 * mm, 20 * mm, 20 * mm], ['Subject', 'Attempted', 'Right', 'Wrong', 'Accuracy', 'Gained', 'Lost', 'Net'])]
    el += [Paragraph('Confidence and negative marking', H2),
           table([[CONF_LABEL[c], an['conf'][c]['n'], an['conf'][c]['right'], an['conf'][c]['wrong'], ('%d%%' % an['conf'][c]['pct']) if an['conf'][c]['pct'] is not None else '-', ('%+g' % an['conf'][c]['ev']) if an['conf'][c]['ev'] is not None else '-', '%+g' % an['conf'][c]['net']]
                  for c, _ in CONF], [32 * mm, 24 * mm, 22 * mm, 22 * mm, 24 * mm, 30 * mm, 24 * mm], ['Rated', 'Attempted', 'Right', 'Wrong', 'Accuracy', 'Average per answer', 'Net marks'])]
    for n in an['notes']:
        el.append(Paragraph('• ' + esc(n), P))
    el.append(Paragraph('Average per answer = 4 × accuracy − 1 × (1 − accuracy); positive only above %d%% accuracy.' % BREAK_EVEN, SM))
    el += [Spacer(1, 8), Paragraph('Mock scores are practice guidance only. They do not predict the JEE Main score, percentile or rank. EduAakashaa · info@eduaakashaa.com · +91-80157 22706 · www.eduaakashaa.com', SM)]
    buf = BytesIO()
    SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title='JEE Main mock report').build(el)
    return buf.getvalue()
