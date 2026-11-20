"""Day-by-day study plan for Darsh (Grade 12 CBSE, Dubai): JEE Main 2027 and the CBSE board exams, 21 Nov 2026 to 9 Apr 2027.

Built only from what the family and the mentors supplied (school schedule PDFs, the ALLEN SCORE test series image, the 18 Nov 2026 mentor meeting and the WhatsApp group):
  * school model exams 25 Nov to 7 Dec, pre-boards 4 to 28 Jan, CBSE practicals 11 to 20 Jan (Delhi Private School Dubai), no school on other days,
  * ALLEN Overseas SCORE-I: 11 SCORE tests and 10 previous-year-paper (PYP) days, 30 Nov to 17 Jan,
  * JEE Main Session 1 in the window of 20 to 31 Jan 2027 (sources differ on the exact days: the admit card decides) and Session 2 in early April (to be notified),
  * CBSE Class 12 theory exams 16 Feb to 9 Apr 2027 (Physics 16 Feb, Chemistry 27 Feb, English 5 Mar, Mathematics 9 Mar, Computer Science 31 Mar, as reported on 6 Nov 2026; confirm on cbse.gov.in),
  * the mentors' strategy of 18 Nov: Chemistry first, then Physics, Mathematics last and only the sure questions; no guessing (negative marking).
Darsh's own topic ratings (the self-assessment he returned on 20 Nov 2026) are set against the JEE Main 2026 chapter Tiers by the gap map (services/jee_gap.py): topics with the most marks within reach come first and get extra minutes, confident ones (rated 4) and topics with no 2026 question only a short revision.
Subject shares of study time: Chemistry 40%, Physics 35%, Mathematics 25% (Mathematics limited to basics and the quicker questions until the January tests).
The plan is rule-based: the same inputs give the same plan. build() returns a list of task dicts for the Smart Study Planner (sp_tasks).
"""
from datetime import date, timedelta

START = date(2026, 11, 21)
END = date(2027, 4, 9)
JEE_S1_FROM = date(2027, 1, 20)
JEE_S1_TO = date(2027, 1, 31)

SCHOOL_EXAMS = {date(2026, 11, 25): 'English', date(2026, 11, 27): 'Physics', date(2026, 11, 30): 'Mathematics', date(2026, 12, 1): 'Computer Science', date(2026, 12, 7): 'Chemistry',
                date(2027, 1, 4): 'Physics', date(2027, 1, 8): 'English', date(2027, 1, 22): 'Chemistry', date(2027, 1, 25): 'Mathematics', date(2027, 1, 28): 'Computer Science'}
SCHOOL_PRACTICAL = {date(2026, 12, 8): 'Physics pre-board practical'}
PRACTICAL_WINDOW = (date(2027, 1, 11), date(2027, 1, 20))
BOARDS = {date(2027, 2, 16): 'Physics', date(2027, 2, 27): 'Chemistry', date(2027, 3, 5): 'English', date(2027, 3, 9): 'Mathematics', date(2027, 3, 31): 'Computer Science'}

# ALLEN SCORE part tests: date -> (name, {subject: [chapters]})
PART_TESTS = {
    date(2026, 11, 30): ('SCORE Test 01 (Part Test 1)', {
        'Physics': ['Modern Physics', 'KTG and Thermodynamics', 'Calorimetry, heat transfer, thermal expansion', 'Elasticity and fluids', 'Heat engine, heat pump and entropy', 'Semiconductors'],
        'Chemistry': ['Thermodynamics and thermochemistry', 'Chemical bonding', 'p-block elements'],
        'Mathematics': ['Complex numbers', 'Matrices and determinants', 'Fundamentals of mathematics', 'Straight line', 'Circle']}),
    date(2026, 12, 4): ('SCORE Test 02 (Part Test 2)', {
        'Physics': ['Electrostatics', 'Gravitation', 'Mechanics up to momentum'],
        'Chemistry': ['Coordination compounds', 'Aromatic compounds', 'Biomolecules and amino acids', 'Practical organic chemistry'],
        'Mathematics': ['Parabola, ellipse, hyperbola', 'Compound angles', 'Quadratic equations', 'Sequence and series']}),
    date(2026, 12, 6): ('SCORE Test 03 (Part Test 3)', {
        'Physics': ['EMI and AC', 'Magnetism and magnetic effects of current', 'SHM, damped and forced oscillations'],
        'Chemistry': ['Atomic structure', 'Chemical kinetics', 'Carboxylic acid and derivatives', 'Amines and nitrogen compounds', 'Name reactions and nucleophilic addition to carbonyls'],
        'Mathematics': ['Binomial theorem', 'Logarithm', 'Permutation and combination', 'Probability', 'Statistics']}),
    date(2026, 12, 14): ('SCORE Test 04 (Part Test 4)', {
        'Physics': ['Rigid body dynamics', 'Geometrical optics', 'Microscope and telescope'],
        'Chemistry': ['Liquid solutions', 'Chemical equilibrium', 'Ionic equilibrium', 'Salt analysis'],
        'Mathematics': ['Vectors', '3D geometry', 'Sets, relations and functions', 'Inverse trigonometric functions']}),
    date(2026, 12, 21): ('SCORE Test 05 (Part Test 5)', {
        'Physics': ['Current electricity', 'Error analysis', 'Capacitors', 'Fluids'],
        'Chemistry': ['Periodic table', 'd-block and f-block', 'Oxidation and reduction of alcohols and ethers', 'Alkyl halides: substitution and elimination'],
        'Mathematics': ['Limits, continuity and differentiability', 'Method of differentiation', 'Application of derivatives']}),
    date(2026, 12, 29): ('SCORE Test 06 (Part Test 6)', {
        'Physics': ['Waves on a string and sound waves', 'Wave optics', 'EM waves and polarisation', 'Diffraction and resolving power'],
        'Chemistry': ['Electrochemistry', 'Redox and mole concept', 'Isomerism', 'GOC', 'Separation techniques and IUPAC naming', 'Hydrocarbons and attacking reagents'],
        'Mathematics': ['Indefinite integration', 'Definite integration', 'Differential equations', 'Area under the curve']}),
}
FULL_TESTS = [date(2027, 1, 3), date(2027, 1, 6), date(2027, 1, 10), date(2027, 1, 13), date(2027, 1, 17)]   # SCORE Tests 07 to 11, full syllabus
PYP_DAYS = [date(2026, 12, 3), date(2026, 12, 9), date(2026, 12, 11), date(2026, 12, 17), date(2026, 12, 24), date(2027, 1, 2), date(2027, 1, 5), date(2027, 1, 8), date(2027, 1, 12), date(2027, 1, 15)]

# Full-syllabus rotation after the part tests, ordered by what the mentors said matters most (Chemistry first, Physics Term 1 topics weak, Mathematics basics and calculus).
REVISION_ROTATION = {
    'Chemistry': ['Chemical bonding', 'Thermodynamics and thermochemistry', 'Ionic equilibrium', 'Coordination compounds', 'p-block elements', 'GOC and isomerism', 'Electrochemistry', 'Chemical kinetics',
                  'Aldehydes, ketones and acids', 'Alcohols, phenols, ethers and haloalkanes', 'Atomic structure and periodicity', 'Mole concept and redox', 'Hydrocarbons', 'Salt analysis and d-block', 'States of matter', 's-block elements and hydrogen'],
    'Physics': ['Laws of motion and friction', 'Work, energy and power', 'Rotational motion', 'Heat and thermodynamics', 'Current electricity', 'Electrostatics', 'Ray optics', 'Magnetism and EMI',
                'Waves and SHM', 'Modern physics', 'Gravitation and fluids', 'Experimental skills and semiconductors'],
    'Mathematics': ['Quadratic equations and sequences', 'Straight line and circle', 'Limits and differentiation basics', 'Matrices and determinants', 'Permutation, combination and probability',
                    'Vectors and 3D', 'Definite integrals basics', 'Conic sections', 'Complex numbers', 'Binomial theorem', 'Mathematical reasoning'],
}
BOARD_CHAPTERS = {
    'Physics': ['Electric charges and fields', 'Electrostatic potential and capacitance', 'Current electricity', 'Moving charges and magnetism', 'Electromagnetic induction and AC', 'Optics', 'Dual nature and atoms', 'Nuclei and semiconductors'],
    'Chemistry': ['Solutions and electrochemistry', 'Chemical kinetics and d- and f-block', 'Coordination compounds', 'Haloalkanes and alcohols', 'Aldehydes, ketones and amines', 'Biomolecules and named reactions'],
    'English': ['Reading and writing skills practice', 'Flamingo prose and poetry', 'Vistas', 'Letter, notice and report writing'],
    'Mathematics': ['Relations, functions and inverse trigonometry', 'Matrices and determinants', 'Continuity, differentiability and applications', 'Integrals and differential equations', 'Vectors and 3D geometry', 'Linear programming and probability'],
    'Computer Science': ['Python revision and file handling', 'Data structures and stack', 'SQL and interface with Python', 'Computer networks'],
}
SHARES = (('Chemistry', .40), ('Physics', .35), ('Mathematics', .25))

# Darsh's own ratings from the JEE self-assessment he returned on 20 Nov 2026 (0 never studied, 1 cannot solve, 2 basics, 3 comfortable at JEE Main level, 4 confident at Advanced level).
RATINGS = {
    'P01': 3, 'P02': 3, 'P03': 2, 'P04': 2, 'P05': 2, 'P06': 2, 'P07': 1, 'P08': 1, 'P09': 1, 'P10': 2, 'P11': 1, 'P12': 2, 'P13': 3, 'P14': 2, 'P15': 3, 'P16': 4, 'P17': 3, 'P18': 3, 'P19': 3, 'P20': 2, 'P21': 4, 'P22': 3,
    'C01': 4, 'C02': 3, 'C03': 3, 'C04': 0, 'C05': 2, 'C06': 2, 'C07': 2, 'C08': 3, 'C09': 3, 'C10': 3, 'C11': 3, 'C12': 2, 'C13': 1, 'C14': 1, 'C15': 3, 'C16': 3, 'C17': 1, 'C18': 3, 'C19': 2, 'C20': 3, 'C21': 4, 'C22': 3, 'C23': 3,
    'C24': 4, 'C25': 2, 'C26': 2,
    'M01': 2, 'M02': 1, 'M03': 2, 'M04': 2, 'M05': 2, 'M06': 2, 'M07': 3, 'M08': 2, 'M09': 3, 'M10': 2, 'M11': 2, 'M12': 3, 'M13': 3, 'M14': 3, 'M15': 3, 'M16': 2, 'M17': 2, 'M18': 2, 'M19': 2, 'M20': 1, 'M21': 0,
}
# plan chapter label -> self-assessment topic codes (the lowest rating of the codes is used)
CHAPTER_CODES = {
    'Modern Physics': 'P19 P20', 'KTG and Thermodynamics': 'P09', 'Calorimetry, heat transfer, thermal expansion': 'P08', 'Elasticity and fluids': 'P07', 'Heat engine, heat pump and entropy': 'P09', 'Semiconductors': 'P21',
    'Electrostatics': 'P12', 'Gravitation': 'P06', 'Mechanics up to momentum': 'P03 P04 P05', 'EMI and AC': 'P15', 'Magnetism and magnetic effects of current': 'P14', 'SHM, damped and forced oscillations': 'P10',
    'Rigid body dynamics': 'P05', 'Geometrical optics': 'P17', 'Microscope and telescope': 'P17', 'Current electricity': 'P13', 'Error analysis': 'P01', 'Capacitors': 'P12', 'Fluids': 'P07',
    'Waves on a string and sound waves': 'P11', 'Wave optics': 'P18', 'EM waves and polarisation': 'P16 P18', 'Diffraction and resolving power': 'P18',
    'Thermodynamics and thermochemistry': 'C05', 'Chemical bonding': 'C03', 'p-block elements': 'C14', 'Coordination compounds': 'C16', 'Aromatic compounds': 'C20', 'Biomolecules and amino acids': 'C25',
    'Practical organic chemistry': 'C26', 'Atomic structure': 'C02', 'Chemical kinetics': 'C11', 'Carboxylic acid and derivatives': 'C23', 'Amines and nitrogen compounds': 'C24',
    'Name reactions and nucleophilic addition to carbonyls': 'C23', 'Liquid solutions': 'C09', 'Chemical equilibrium': 'C06', 'Ionic equilibrium': 'C07', 'Salt analysis': 'C17 C26', 'Periodic table': 'C12',
    'd-block and f-block': 'C15', 'Oxidation and reduction of alcohols and ethers': 'C22', 'Alkyl halides: substitution and elimination': 'C21', 'Electrochemistry': 'C10', 'Redox and mole concept': 'C08 C01',
    'Isomerism': 'C19', 'GOC': 'C18', 'Separation techniques and IUPAC naming': 'C19 C26', 'Hydrocarbons and attacking reagents': 'C20 C18',
    'Complex numbers': 'M02', 'Matrices and determinants': 'M07', 'Fundamentals of mathematics': 'M01 M03', 'Straight line': 'M09', 'Circle': 'M10', 'Parabola, ellipse, hyperbola': 'M11', 'Compound angles': 'M08',
    'Quadratic equations': 'M03', 'Sequence and series': 'M04', 'Binomial theorem': 'M06', 'Logarithm': 'M03', 'Permutation and combination': 'M05', 'Probability': 'M19', 'Statistics': 'M20', 'Vectors': 'M17',
    '3D geometry': 'M18', 'Sets, relations and functions': 'M01', 'Inverse trigonometric functions': 'M08', 'Limits, continuity and differentiability': 'M12', 'Method of differentiation': 'M13',
    'Application of derivatives': 'M13', 'Indefinite integration': 'M14', 'Definite integration': 'M15', 'Differential equations': 'M16', 'Area under the curve': 'M15',
    # full-revision rotation
    'Laws of motion and friction': 'P03', 'Work, energy and power': 'P04', 'Rotational motion': 'P05', 'Heat and thermodynamics': 'P08 P09', 'Ray optics': 'P17', 'Magnetism and EMI': 'P14 P15', 'Waves and SHM': 'P10 P11',
    'Gravitation and fluids': 'P06 P07', 'Experimental skills and semiconductors': 'P22 P21', 'GOC and isomerism': 'C18 C19', 'Aldehydes, ketones and acids': 'C23', 'Alcohols, phenols, ethers and haloalkanes': 'C21 C22',
    'Atomic structure and periodicity': 'C02 C12', 'Mole concept and redox': 'C01 C08', 'Hydrocarbons': 'C20', 'Salt analysis and d-block': 'C17 C15', 'Quadratic equations and sequences': 'M03 M04',
    'Straight line and circle': 'M09 M10', 'Limits and differentiation basics': 'M12 M13', 'Permutation, combination and probability': 'M05 M19', 'Vectors and 3D': 'M17 M18', 'Definite integrals basics': 'M15',
    'Conic sections': 'M11', 'Modern physics': 'P19 P20', 'States of matter': 'C04', 's-block elements and hydrogen': 'C13', 'Mathematical reasoning': 'M21',
}


def _gap():
    from app.services import jee_gap
    return {x['code']: x for x in jee_gap.analyse(RATINGS)['rows']}


_GAP = {}


def gap_info(chapter):
    """What the JEE gap map (services/jee_gap.py: his ratings against the 2026 chapter Tiers) says about a plan chapter:
    (bucket, rating, tier, marks within reach per paper). Chapters with no mapped topic count as Maintain."""
    if not _GAP:
        _GAP.update(_gap())
    rows = [_GAP[c] for c in (CHAPTER_CODES.get(chapter) or '').split() if c in _GAP]
    if not rows:
        return 'Maintain', 2, 2, 0.0
    order = ('Fix first', 'Fix next', 'Maintain', 'Park')
    bucket = min((r['bucket'] for r in rows), key=order.index)
    live = [r for r in rows if r['bucket'] != 'Park']
    pool = live or rows
    return bucket, min(r['rating'] for r in pool), min((r['tier'] for r in pool if r['tier']), default=0), max(r['risk'] for r in rows)


def rating(chapter):
    return gap_info(chapter)[1]


def risk(chapter):
    bucket, _r, _t, rk = gap_info(chapter)
    return -1 if bucket == 'Park' else rk


for _s in REVISION_ROTATION:                                                # biggest gap first (marks within reach), no-question topics last
    REVISION_ROTATION[_s].sort(key=lambda c: -risk(c))


def _next_test_day(d):
    c = [t for t in PART_TESTS if t > d]
    return min(c) if c else None


def _task(day, subject, chapter, ttype, title, minutes, note=''):
    return dict(day=day, subject=subject, chapter=chapter, task_type=ttype, title=title, minutes=int(minutes), note=note)


def _blocks(day, minutes, chapter_for, seen):
    """Three subject blocks plus a 30-minute error log; `chapter_for(subject)` picks the chapter. Mathematics keeps to basics and the quicker questions.
    The gap map decides the time: Fix first = 30 extra minutes and a start from the basics when rated 0 or 1; Park (no question in 2026) = a short revision; confident (rated 4) = short revision."""
    out = []
    for subject, share in SHARES:
        ch = chapter_for(subject)
        bucket, r, tier, rk = gap_info(ch)
        n = seen.get((subject, ch), 0)
        seen[(subject, ch)] = n + 1
        ttype = 'learn' if n == 0 else ('practice' if n == 1 else 'revise')
        if r >= 4 or bucket == 'Park':
            ttype = 'revise'
        mins = max(30, round(minutes * share / 15) * 15)
        note = 'Attempt a question only when you are sure: a wrong answer costs 1 mark.' if ttype != 'learn' else ''
        if bucket == 'Fix first':
            mins += 30
            how = ('Start from the basics (self-rated %d): concept notes, 5 solved examples, then 10 easy questions' % r) if (ttype == 'learn' and r <= 1) else \
                  ('Concept notes, then the solved examples yourself' if ttype == 'learn' else '15 JEE Main level questions; write every mistake in the error log')
            note = 'Gap map: Tier %d, rated %d, JEE Main needs 3, about %.1f marks per paper within reach.' % (tier, r, rk)
        elif bucket == 'Park':
            how = 'Short revision only: no question came from this topic in the 19 JEE Main 2026 shifts'
            note = 'Gap map: no 2026 question, so it waits until the Tier 1 and Tier 2 gaps are closed.'
        elif subject == 'Mathematics':
            how = {'learn': 'Concept and 6 basic solved examples', 'practice': 'Attempt only the quick, sure questions (8 to 10); skip long ones', 'revise': 'Formula sheet and 6 quick questions'}[ttype]
            if r >= 3 and ttype == 'practice':
                how = 'A strong topic (self-rated %d): practise 12 questions here, these are your sure marks' % r
        elif ttype == 'learn':
            how = 'Concept notes, then the solved examples yourself'
        elif ttype == 'practice':
            how = '20 JEE Main level questions, then check every answer'
        else:
            how = 'Formula and reaction revision, then 12 previous-year questions' if r < 4 else 'Quick revision of formulas and 5 previous-year questions (self-rated 4)'
        if r >= 4 or bucket == 'Park':
            mins = 30
        out.append(_task(day, subject, ch, ttype, f'{ch}: {how}', mins, note))
    out.append(_task(day, None, None, 'error', 'Error log: write every mistake of the day, its cause and the fix', 30))
    return out


def build():
    seen, tasks = {}, []
    rot = {s: 0 for s in REVISION_ROTATION}
    pending_review = {}                                                    # day -> (title) after a mock
    d = START
    while d <= END:
        wd = d.weekday()                                                   # 5 = Saturday, 6 = Sunday
        if d in pending_review:
            tasks.append(_task(d, None, None, 'error', pending_review.pop(d), 75, 'Mark each question: sure and right, sure and wrong, guessed. Wrong-but-sure ones go in the error log.'))
        # ---- phase 4 and 5: boards ----
        if d >= date(2027, 1, 31):
            tasks += _board_day(d, rot)
            d += timedelta(days=1)
            continue
        # ---- JEE Main Session 1 window ----
        if JEE_S1_FROM <= d <= JEE_S1_TO:
            tasks.append(_task(d, None, None, 'rest' if d != JEE_S1_FROM else 'revise', 'JEE Main Session 1 window: sit the exam on the day and slot of the admit card; on other days one hour of formulas and the error log only', 60,
                               'Not attempted: any question you are not sure of. Check the admit card the evening before.'))
            if d in SCHOOL_EXAMS:
                tasks.append(_task(d, SCHOOL_EXAMS[d], None, 'revise', f'School pre-board: {SCHOOL_EXAMS[d]} (confirm with the school if it clashes with the JEE slot)', 90))
            d += timedelta(days=1)
            continue
        # ---- mock days ----
        if d in PART_TESTS:
            name = PART_TESTS[d][0]
            tasks.append(_task(d, None, None, 'mock', f'ALLEN {name}, 5:30 to 8:30 PM GST (part syllabus)', 180, 'Order: Chemistry, then Physics, then Mathematics (sure ones only).'))
            pending_review[d + timedelta(days=1)] = f'Review of {name}: re-do every wrong and skipped question'
        if d in FULL_TESTS:
            tasks.append(_task(d, None, None, 'mock', f'ALLEN SCORE full-syllabus test ({FULL_TESTS.index(d) + 7:02d}), JEE Main pattern', 180, 'Order: Chemistry, then Physics, then Mathematics (sure ones only).'))
            pending_review[d + timedelta(days=1)] = f'Review of SCORE test {FULL_TESTS.index(d) + 7:02d}: re-do every wrong and skipped question'
        if d in PYP_DAYS:
            tasks.append(_task(d, None, None, 'mock', f'ALLEN previous-year paper {PYP_DAYS.index(d) + 1:02d}, Slot 1 (1:30 to 4:30 PM GST); use Slot 2 (9:30 PM) if school is busy', 180, 'Treat it as the real exam: no breaks, same attempt order.'))
            pending_review[d + timedelta(days=1)] = f'Review of previous-year paper {PYP_DAYS.index(d) + 1:02d}: tag every wrong answer by cause'
        # ---- school ----
        if d in SCHOOL_EXAMS:
            tasks.append(_task(d, SCHOOL_EXAMS[d], None, 'revise', f'School exam today: {SCHOOL_EXAMS[d]} (CBSE portion)', 90))
        nxt = [x for x in sorted(SCHOOL_EXAMS) if x == d + timedelta(days=1)]
        if nxt:
            tasks.append(_task(d, SCHOOL_EXAMS[nxt[0]], None, 'revise', f'Revise for tomorrow\'s school exam: {SCHOOL_EXAMS[nxt[0]]}', 75))
        if d in SCHOOL_PRACTICAL:
            tasks.append(_task(d, 'Physics', None, 'revise', SCHOOL_PRACTICAL[d] + ': practical file and viva', 60))
        if PRACTICAL_WINDOW[0] <= d <= PRACTICAL_WINDOW[1] and not (d in PART_TESTS or d in FULL_TESTS or d in PYP_DAYS):
            tasks.append(_task(d, None, None, 'revise', 'CBSE practical window: attend on the day the school gives; otherwise 45 minutes of practical file and viva', 45))
        # ---- study blocks ----
        mock_day = d in PART_TESTS or d in FULL_TESTS or d in PYP_DAYS
        if mock_day:                                                       # the mock is the study for the day; the review comes the next day
            d += timedelta(days=1)
            continue
        busy = d in SCHOOL_EXAMS or d in SCHOOL_PRACTICAL
        reviewing = any(t['day'] == d and t['task_type'] == 'error' and t['minutes'] == 75 for t in tasks[-6:])
        minutes = 150 if busy else (210 if reviewing else (240 if wd == 5 else 300))   # lighter on Saturdays and after a mock
        tdate = _next_test_day(d)
        if tdate and d < date(2026, 12, 29):
            def chapter_for(subject, tdate=tdate, d=d):
                chs = PART_TESTS[tdate][1][subject]
                k = sum(1 for t in tasks if t['subject'] == subject and t['task_type'] in ('learn', 'practice', 'revise') and t['day'] > d - timedelta(days=8) and t['chapter'] in chs)
                return chs[k % len(chs)]                                   # rotate through the next test's chapters
        else:
            def chapter_for(subject):
                lst = REVISION_ROTATION[subject]
                ch = lst[rot[subject] % len(lst)]
                rot[subject] += 1
                return ch
        tasks += _blocks(d, minutes, chapter_for, seen)
        d += timedelta(days=1)
    return tasks


def _board_day(d, rot):
    """31 Jan to 9 Apr: CBSE board preparation (the next board paper first), JEE Session 2 practice kept alive. One rest day a week."""
    out = []
    upcoming = [x for x in sorted(BOARDS) if x >= d]
    if not upcoming:
        out.append(_task(d, None, None, 'revise', 'JEE Main Session 2 window (expected in early April, NTA to notify): one hour of formulas and the error log; sit the paper on the admit-card day if Session 2 is attempted', 60,
                         'Not attempted: any question you are not sure of.'))
        return out
    nxt = upcoming[0]
    sub = BOARDS[nxt]
    if d in BOARDS:
        out.append(_task(d, sub, None, 'mock', f'CBSE board exam today: {sub}, 10:30 AM to 1:30 PM (carry admit card and school ID)', 180, 'Confirm the date and Gulf timing on cbse.gov.in.'))
        later = [x for x in sorted(BOARDS) if x > d]
        if later:
            out.append(_task(d, BOARDS[later[0]], None, 'revise', f'Light revision for the next paper: {BOARDS[later[0]]}', 60))
        return out
    if d.weekday() == 6 and (nxt - d).days > 3:
        out.append(_task(d, None, None, 'rest', 'Rest day: no new study; check the week\'s plan and the admit card, sleep early', 30))
        return out
    k = (nxt - d).days
    chs = BOARD_CHAPTERS[sub]
    idx = (rot.setdefault('b' + sub, 0)) % len(chs)
    rot['b' + sub] += 1
    paper_day = k in (3, 6, 9)
    s2_day = date(2027, 3, 21) <= d <= date(2027, 4, 7) and d.weekday() in (5, 6)
    if not paper_day:
        mins = 90 if s2_day else (180 if k > 2 else 150)
        out.append(_task(d, sub, chs[idx], 'learn' if k > 7 else 'practice', f'Board {sub}: {chs[idx]}' + (' (NCERT exemplar and last 5 years of CBSE papers)' if k <= 7 else ''), mins))
    if k in (3, 6, 9):
        out.append(_task(d, sub, None, 'mock', f'Board {sub}: one full sample paper in 3 hours, then self-mark', 180))
    elif k <= 10:
        out.append(_task(d, sub, None, 'revise', f'Board {sub}: formulas, diagrams and the marking scheme', 45))
    other = [x for x in sorted(BOARDS) if x > nxt]
    if other and k > 3 and not s2_day:
        o = BOARDS[other[0]]
        oc = BOARD_CHAPTERS[o]
        out.append(_task(d, o, oc[rot.setdefault('b' + o, 0) % len(oc)], 'revise', f'Board {o}: one chapter ({oc[rot["b" + o] % len(oc)]})', 60))
        rot['b' + o] += 1
    if s2_day:
        out.append(_task(d, None, None, 'mock', 'JEE Main Session 2 practice: one timed 3-hour paper (only if Session 2 is attempted); dates to be notified by NTA', 180, 'Decide after the Session 1 result.'))
    out.append(_task(d, None, None, 'error', 'Error log: mistakes of the day and the fix', 20))
    return [t for t in out if t['minutes'] > 0]
