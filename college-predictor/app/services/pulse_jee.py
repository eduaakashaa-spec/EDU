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
    if not isinstance(qs, dict) or len(qs) > 100:
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
    """EduAakashaA report template (see app/services/ea_pdf.py)."""
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Spacer

    from app.services import ea_pdf as E

    an = analyse([result])
    att = (result.right or 0) + (result.wrong or 0)
    acc = round(100 * (result.right or 0) / att) if att else 0
    when = (result.finished_at or datetime.utcnow()).strftime('%d %b %Y')
    mode = 'timed mock' if result.mode == 'mock' else 'practice set'
    meta = {'eyebrow': 'EduPulse-JEE Mock Test Centre', 'title_lines': [('JEE Main mock', False), ('report', True)], 'title': 'JEE Main mock report',
            'subtitle': [result.paper_title or 'JEE Main mock', '%s  \u00b7  %s  \u00b7  %s' % (student_name, mode, when)],
            'cover_stats': [('Score', '%g / %g' % (result.score, result.max_score)), ('Accuracy', '%d%%' % acc), ('Right / wrong', '%d / %d' % (result.right or 0, result.wrong or 0)),
                            ('Lost to negatives', '%g' % (result.lost or 0))],
            'footer_left': 'EduPulse-JEE Mock Test Centre', 'running_head': 'JEE Main mock report \u00b7 ' + (result.paper_title or '')}

    el = E.heading('Your result', 'How this <i>mock</i> went')
    el += [E.P('%s took <b>%s</b> as a %s on %s. Marking is +4 for a correct answer, \u22121 for a wrong one and 0 for a blank, in both the multiple-choice and numerical sections. '
               'Accuracy is measured on the questions attempted.' % (E.esc(student_name), E.esc(result.paper_title or 'the paper'), mode, when)), Spacer(1, 4),
           E.kpis([('Score', '%g' % result.score, 'navy'), ('Accuracy', '%d%%' % acc, 'orange'), ('Right', result.right or 0, 'green'), ('Wrong', result.wrong or 0, 'red'),
                   ('Blank', result.blank or 0, 'navy'), ('Lost to negatives', '%g' % (result.lost or 0), 'red')]),
           E.P('By subject', 'h2'),
           E.data_table(['Subject', 'Attempted', 'Right', 'Wrong', 'Accuracy', 'Gained', 'Lost', 'Net'],
                        [[SUBJ[k], a['att'], a['right'], a['wrong'], ('%d%%' % a['acc']) if a['acc'] is not None else '-', '+%g' % a['gain'], '-%g' % a['loss'], '%+g' % (a['gain'] - a['loss'])]
                         for k, a in an['subj'].items()], [34 * mm, 24 * mm, 20 * mm, 20 * mm, 24 * mm, 20 * mm, 20 * mm, 20 * mm]), Spacer(1, 6)]
    top = max((a['gain'] for a in an['subj'].values()), default=0) or 1
    el.append(E.Bars([(SUBJ[k], max(0, round(100 * (a['gain'] - a['loss']) / top)), '%+g net' % (a['gain'] - a['loss']), E.NAVY) for k, a in an['subj'].items()], label_w=36 * mm))
    el += [Spacer(1, 4), E.P('Bars show net marks per subject (gained minus lost to negative marking), scaled to the highest gain.', 'small'), Spacer(1, 6),
           E.callout('<b>Read this score as practice guidance.</b> A mock score does not predict the JEE Main score, percentile or rank. Use it to see where marks were gained, and where they leaked.', 'navy'),
           PageBreak()]

    el += E.heading('Negative marking and confidence', 'Where the marks <i>leaked</i>')
    el += [E.P('Every answer was rated Guess, Low, Medium or High. With +4/\u22121 marking an attempt pays off on average only if it is right more than %d%% of the time, '
               'so confidence ratings show which attempts were worth making.' % BREAK_EVEN), Spacer(1, 4)]
    tone = {'H': E.NAVY, 'M': E.NAVY, 'L': E.ORANGE, 'G': E.ORANGE}
    el.append(E.Bars([(CONF_LABEL[c], an['conf'][c]['pct'], ('%d%%  (%d of %d)' % (an['conf'][c]['pct'], an['conf'][c]['right'], an['conf'][c]['n'])) if an['conf'][c]['pct'] is not None else 'no answers', tone[c])
                      for c, _ in CONF], row_h=9 * mm))
    el += [Spacer(1, 4), E.P('Bars show the share of answers that were right at each confidence level. Break-even for +4/\u22121 marking is %d%%.' % BREAK_EVEN, 'small'), Spacer(1, 6),
           E.data_table(['Rated', 'Attempted', 'Right', 'Wrong', 'Accuracy', 'Average per answer', 'Net marks'],
                        [[CONF_LABEL[c], an['conf'][c]['n'], an['conf'][c]['right'], an['conf'][c]['wrong'], ('%d%%' % an['conf'][c]['pct']) if an['conf'][c]['pct'] is not None else '-',
                          ('%+g' % an['conf'][c]['ev']) if an['conf'][c]['ev'] is not None else '-', '%+g' % an['conf'][c]['net']] for c, _ in CONF],
                        [28 * mm, 24 * mm, 20 * mm, 20 * mm, 24 * mm, 36 * mm, 24 * mm]),
           E.P('Average per answer = 4 \u00d7 accuracy \u2212 1 \u00d7 (1 \u2212 accuracy); positive only above %d%% accuracy.' % BREAK_EVEN, 'small'), Spacer(1, 6)]
    for n in an['notes']:
        el += [E.callout(E.esc(n)), Spacer(1, 4)]
    chap = sorted(an['chap'].items(), key=lambda kv: (kv[1]['right'] / kv[1]['n']) if kv[1]['n'] else 1)[:8]
    if chap:
        el += [E.P('Chapters to look at first', 'h2'),
               E.Bars([(str(k)[:34], round(100 * t['right'] / t['n']), '%d%%  (%d)' % (round(100 * t['right'] / t['n']), t['n']),
                        E.GREEN if t['right'] / t['n'] >= .7 else (E.ORANGE if t['right'] / t['n'] >= .5 else E.RED)) for k, t in chap], label_w=52 * mm, row_h=7.4 * mm)]
    el.append(PageBreak())

    el += E.heading('Next steps', 'What to do <i>this week</i>')
    nxt = []
    if an['sure_wrong']:
        nxt.append(('Re-solve the confident mistakes first', '%d wrong answers were given with High confidence. They usually point to a wrong method or concept, not bad luck.' % an['sure_wrong']))
    if an['avoidable']:
        nxt.append(('Decide your guessing rule', '%d wrong answers were rated Guess or Low. Attempt such a question only if you can rule out at least two options; otherwise leave it blank.' % an['avoidable']))
    if an['kind']['NAT']['wrong'] >= 2:
        nxt.append(('Check numerical answers before moving on', '%d wrong numerical answers cost %g marks. There is no lucky guess in a numerical question, so verify the working.' %
                    (an['kind']['NAT']['wrong'], an['kind']['NAT']['loss'])))
    if an['weak']:
        nxt.append(('Give short, regular sessions to weaker chapters', '%s earned little. Two or three 25-minute sessions through the week work better than one long one.' % ', '.join(str(w) for w in an['weak'])))
    nxt += [('Rate every answer in the next mock', 'Confidence ratings are what make this report useful. Answers without a rating are left out of the calibration.'),
            ('Repeat after 7 to 10 days', 'Take another paper, or practise the same chapters through EduPulse Reinforcement daily sets, and compare the two reports.'),
            ('Share this report with your mentor', 'Your EduAakashaA mentor can turn these patterns into a plan for the weeks ahead.')]
    el += [E.steps(nxt), Spacer(1, 10),
           E.callout('<b>Please note.</b> This report is generated automatically from your recorded mock attempt. Scores and percentages are practice guidance and depend on how many questions were attempted; '
                     'they are not a prediction of the JEE Main score, percentile, rank or admission, and are not a guarantee of any outcome. Questions in the EduAakashaA mocks are original; '
                     'official papers are NTA material used for practice.', 'orange')]
    return E.build_report(meta, el)

