"""Public landing page for EduPulse-Explorer (Grades 7 to 10): what it is, which exams ask what, how reinforcement works, and six free sample questions."""
from app.services import explorer as ex
from app.services import explorer_gen as gen

UPDATED = '3 Nov 2026'

HOW = [
    ('Discover', 'A Discovery Test with every skill (maths reasoning, science, engineering thinking, logic, spatial, design sense, language) and a 16-statement interest check show what you enjoy and where you are strong.'),
    ('Meet the exams', 'Short tasters in the style of JEE, UCEED / NID / NIFT, NATA and JEE Paper 2, and IISER IAT and olympiads. After each question you see how the exam would ask it.'),
    ('Build each skill', 'Twelve-question skill sets. Maths and logic questions are generated, so the numbers are new each time and you can repeat a set without remembering answers.'),
    ('Reinforce', 'Every wrong answer, and every right answer you rated Guess or Low, becomes a review card. It returns in your Daily 10 after 0, 1, 3, 7, 14 and 30 days as you get it right, and goes back to the start if you miss it.'),
    ('Track', 'Skill levels from your last 20 answers, a picture by exam style, your confidence pattern, streak, weekly goal and badges. Mentors can see the same picture.'),
    ('Make things', 'Twelve creative challenges for home: draw, build, observe and fix, marked by you against a rubric. Design exams test these abilities and a computer cannot mark them.'),
]

BOXES = [('Box 0', 'new or just missed', 'today'), ('Box 1', 'right once', 'next day'), ('Box 2', 'right twice', '3 days'), ('Box 3', 'settling', '1 week'), ('Box 4', 'secure', '2 weeks'), ('Box 5', 'long-term', '1 month')]

FAQ = [
    ('Is this a selection test?', 'No. It is for exploring: to meet the style of questions, find strengths and gaps early, and build the habit of daily practice. Scores are practice guidance, not a prediction of any entrance result.'),
    ('Are these the real exam questions?', 'No. All questions are original EduAakashaA practice questions written at school level for the thinking each exam family uses. The exams belong to their organisers; check each exam’s current notice for its real pattern.'),
    ('Which grade should I choose?', 'Grade 7 and 8 get questions at their level; Grade 9 and 10 get harder ones and the extra topics of Class 9 and 10. You can switch any time.'),
    ('Why rate my confidence?', 'A wrong answer you were sure about shows a misunderstanding; a right answer you guessed is not yet yours. Both go into your review cards so you can fix them.'),
    ('How accurate are the answers?', 'Maths and logic answers are computed by code. The other questions were written with AI assistance and each was solved again independently. If you doubt one, tell your mentor.'),
    ('What does it cost?', 'The practice centre is free with a login. Mentorship for Class 8 to 12 pathways is separate: see FutureReady and the programmes on the site.'),
]


def samples():
    picks = ['g:pcchg:4', 'g:series:12', 'XV-MIRRO-02']
    qs = [gen.from_id(picks[0]), gen.from_id(picks[1])]
    bank = ex.bank()
    for sk, topic_prefix in (('SCI', 'Physics'), ('ENG', 'Mechanisms'), ('DES', 'Colour')):
        pool = [q for q in bank if q['skill'] == sk and q['grade'] in ('7-8', 'all') and q['diff'] <= 2 and q['topic'].startswith(topic_prefix) and not q.get('svg')]
        if not pool:
            pool = [q for q in bank if q['skill'] == sk and q['grade'] in ('7-8', 'all') and not q.get('svg')]
        qs.append(pool[0])
    qs.append(ex.get(picks[2]))
    out = []
    for q in qs:
        out.append({'skill': ex.SKILLS[q.get('skill') or q['sec']], 'q': q['q'], 'svg': q.get('svg'), 'opts': [({'svg': o['svg']} if isinstance(o, dict) and o.get('svg') else {'t': o['t'] if isinstance(o, dict) else o}) for o in q['opts']],
                    'ans': q['ans'], 'why': q['why'], 'style': q.get('style', '')})
    return out


def context():
    return {'how': HOW, 'boxes': BOXES, 'faq': FAQ, 'samples': samples(), 'families': ex.FAMILIES, 'skills': ex.SKILLS, 'blurb': ex.SKILL_BLURB, 'n_bank': len(ex.bank()), 'updated': UPDATED}
