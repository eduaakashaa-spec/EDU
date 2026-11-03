"""EduPulse free sample mock tests (public): one fixed 10-question sample for each exam, built from the exam banks the member mock centres already use.

Every sample question is normalised to {id, sec, stem, fig, passage, opts, ans, why}: stem/fig/passage/why are HTML (plain text is escaped here), each option is {'h': html} or {'img': url}.
The selection is seeded, so a sample is the same for everyone and for every visit. Answers stay on the server; the page only receives the questions.
"""
import json
import os
import random

from markupsafe import escape

_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
_cache = {}

EXAMS = [
    {'key': 'jee', 'name': 'JEE Main', 'tag': 'Maths, Physics, Chemistry', 'minutes': 20, 'marks': '+4 right, -1 wrong',
     'blurb': 'Ten multiple-choice questions from an EduAakashaA JEE Main mock: 4 maths, 3 physics, 3 chemistry.'},
    {'key': 'uceed', 'name': 'UCEED', 'tag': 'Design aptitude', 'minutes': 20, 'marks': '+3 right, -0.71 wrong',
     'blurb': 'Ten design-aptitude questions: visual patterns, spatial reasoning, observation and design awareness.'},
    {'key': 'nid', 'name': 'NID DAT', 'tag': 'Visual and logical reasoning', 'minutes': 15, 'marks': '+1 right, no negative',
     'blurb': 'Ten NID-style questions: mirror images, patterns, visual reasoning, language and general awareness.'},
    {'key': 'nift', 'name': 'NIFT GAT', 'tag': 'Quant, English, GK, reasoning', 'minutes': 15, 'marks': '+1 right, -0.25 wrong',
     'blurb': 'Ten questions from the GAT sections: quantitative ability, reasoning, English, comprehension and general knowledge.'},
    {'key': 'iat', 'name': 'IISER Aptitude Test', 'tag': 'Bio, Chem, Maths, Physics', 'minutes': 20, 'marks': '+4 right, -1 wrong',
     'blurb': 'Ten IAT-style questions across biology, chemistry, mathematics and physics, shown as in the paper.'},
    {'key': 'tn10', 'name': 'TN Class 10', 'tag': 'Maths and Science', 'minutes': 15, 'marks': '1 mark each',
     'blurb': 'Ten Tamil Nadu Class 10 questions, five maths and five science, from the textbook units.'},
]
BY_KEY = {e['key']: e for e in EXAMS}
SIZE = 10


def _json(*parts):
    with open(os.path.join(_DIR, *parts), encoding='utf-8') as f:
        return json.load(f)


def _t(s):
    return str(escape(s or ''))


def _pick(rows, n, seed):
    rows = list(rows)
    random.Random(seed).shuffle(rows)
    return rows[:n]


def _letter(d):
    return 'ABCDEFGH'.index(str(d)[:1].upper())


def _jee():
    qs = [q for q in _json('jee_mock', 'data', 'M1.json')['qs'] if q.get('t') == 'MCQ' and not (q.get('fig') or q.get('svg')) and len(q.get('opts') or []) == 4]
    names = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}
    out = []
    for subj, n in (('MATH', 4), ('PHY', 3), ('CHEM', 3)):
        for q in _pick([x for x in qs if x['subj'] == subj], n, 'jee' + subj):
            out.append({'id': 'JEE-%s-%s' % (subj, q['n']), 'sec': names[subj], 'stem': q['stem'], 'fig': '', 'passage': '',
                        'opts': [{'h': o} for o in q['opts']], 'ans': _letter(q['disp']), 'why': ' '.join(q.get('steps') or [])})
    return out


def _uceed():
    qs = [q for q in _json('uceed_mock', 'data', 'M1.json')['qs'] if q.get('t') == 'MCQ' and len(q.get('opts') or []) == 4]
    names = {'PAT': 'Patterns', 'SCI': 'Science and design', 'VIS': 'Visual', 'CUL': 'Culture and design', 'SPA': 'Spatial', 'NUM': 'Numbers', 'OBS': 'Observation'}
    return [{'id': 'UCEED-%s' % q['n'], 'sec': names.get(q['cat'], q['cat']), 'stem': q['stem'], 'fig': q.get('fig') or q.get('svg') or '', 'passage': '',
             'opts': [{'h': o} for o in q['opts']], 'ans': _letter(q['disp']), 'why': ' '.join(q.get('steps') or [])} for q in _pick(qs, SIZE, 'uceed')]


def _nid():
    names = {'VIS': 'Visual', 'SPA': 'Spatial', 'CLR': 'Colour', 'LAN': 'Language', 'LOG': 'Logic', 'CRF': 'Craft', 'MAT': 'Materials', 'CRT': 'Creativity',
             'PRI': 'Printing', 'HIS': 'History', 'ERG': 'Ergonomics', 'AWR': 'Awareness', 'SUS': 'Sustainability', 'SCI': 'Science', 'GKN': 'General knowledge'}
    rows = _json('nid', 'bank.json')
    out = []
    for src, n in (('visual', 5), ('text', 5)):
        pool = [q for q in rows if q.get('src') == src and len(q.get('opts') or []) == 4]
        for q in _pick(pool, n, 'nid' + src):
            opts = [{'h': o.get('svg') if isinstance(o, dict) else _t(o)} for o in q['opts']]
            out.append({'id': q.get('id') or 'NID-%d' % len(out), 'sec': names.get(q['sec'], q['sec']), 'stem': _t(q['q']), 'fig': q.get('svg') or '', 'passage': '',
                        'opts': opts, 'ans': q['ans'], 'why': _t(q.get('why'))})
    return out


def _nift():
    names = {'QA': 'Quantitative ability', 'ANA': 'Analytical ability', 'ENG': 'English', 'GK': 'General knowledge', 'CMP': 'Comprehension'}
    rows = [q for q in _json('nift', 'bank.json') if len(q.get('opts') or []) == 4 and not str(q['id']).startswith('G')]
    out = []
    for sec in ('QA', 'ANA', 'ENG', 'GK', 'CMP'):
        pool = [q for q in rows if q['sec'] == sec and (sec != 'CMP' or (q.get('ctx') and len(q['ctx']) < 900))]
        for q in _pick(pool, 2, 'nift' + sec):
            out.append({'id': q['id'], 'sec': names[sec], 'stem': _t(q['q']), 'fig': '', 'passage': _t(q.get('ctx')),
                        'opts': [{'h': _t(o)} for o in q['opts']], 'ans': q['ans'], 'why': _t(q.get('why'))})
    return out


def _iat():
    from app.services import iat
    names = dict(iat.SUBJECTS)
    pool = iat.usable()
    out = []
    for sj, n in (('BIO', 3), ('CHE', 3), ('MAT', 2), ('PHY', 2)):
        for q in _pick([x for x in pool if x['sj'] == sj], n, 'iat' + sj):
            out.append({'id': q['qid'], 'sec': names[sj], 'stem': '', 'fig': '<img src="%s" alt="Question" style="max-width:100%%;height:auto;background:#fff;border-radius:6px">' % iat.asset(q, q['stem'][0]),
                        'passage': '', 'opts': [{'img': iat.asset(q, q['opts'][i])} for i in q['order']], 'ans': q['ans'], 'why': _t(q.get('why'))})
    return out


def _tn10():
    from app.services import tn10
    pool = tn10.bank()
    out = []
    for subj in sorted({q['subject'] for q in pool}):
        for q in _pick([x for x in pool if x['subject'] == subj], SIZE // 2, 'tn10' + subj):
            out.append({'id': q['qid'], 'sec': q['subject'] + ': ' + q['chapter'], 'stem': _t(q['stem']), 'fig': '', 'passage': '',
                        'opts': [{'h': _t(o)} for o in q['options']], 'ans': q['ans'], 'why': _t(q['why'])})
    return out


_BUILD = {'jee': _jee, 'uceed': _uceed, 'nid': _nid, 'nift': _nift, 'iat': _iat, 'tn10': _tn10}


def sample(key):
    """The fixed sample for an exam: a list of normalised questions with the answers (keep on the server)."""
    if key not in _BUILD:
        return None
    if key not in _cache:
        _cache[key] = _BUILD[key]()
    return _cache[key]


def public_view(key):
    """The same sample without answers or explanations, for the page."""
    return [{k: v for k, v in q.items() if k not in ('ans', 'why')} for q in sample(key)]


def grade(key, answers):
    """answers: {question id: chosen option index}. Returns the score and a per-question review."""
    qs = sample(key)
    right = wrong = blank = 0
    rows = []
    for q in qs:
        try:
            pick = int(answers.get(q['id']))
        except (TypeError, ValueError):
            pick = None
        if pick is None or not 0 <= pick < len(q['opts']):
            blank += 1
            state = 'blank'
        elif pick == q['ans']:
            right += 1
            state = 'right'
        else:
            wrong += 1
            state = 'wrong'
        rows.append({'q': q, 'pick': pick, 'state': state})
    return {'right': right, 'wrong': wrong, 'blank': blank, 'total': len(qs), 'rows': rows}
