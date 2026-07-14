"""EduAakashaa membership onboarding assessment — the question bank as data.

Single source of truth (like survey.py's SECTIONS): this drives the public form,
server-side validation, admin display, and the "copy for AI" bundle. The full
design, scoring rubric and dossier template live in ONBOARDING_ASSESSMENT.md.

Responses are stored keyed by item id (S1…S60, P1…P34) so the AI rubric — which
references those exact ids — can be run verbatim on a stored submission.

Item types (what the browser renders and what gets stored):
    likert        1–5 scale            → int
    likert_multi  several 1–5 rows     → {row_label: int}
    choice        one option           → option label (str)
    choice_multi  one option per row   → {row_label: option label}
    mostleast     pick most + least    → {"most": label, "least": label}
    pick          pick exactly N       → [label, …]
    rank          order all options    → [label, …] (best first)
    choice_pair   two labelled selects → {group_key: label}
    num           one or more numbers  → {field_label: number|""}
    sjt           one option + "why"   → {"choice": label, "why": text}
    open          free text            → str
"""

# --- scales -----------------------------------------------------------------
AGREE = ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']
FAMILIARITY = ['Never heard of it', 'Heard the name', 'Broadly aware',
               'Fairly confident', 'Could explain it to another parent']


# --- item builders (keep the data below readable) ---------------------------
def _likert(id, text, tag, rev=False, scale=None):
    it = {'id': id, 'type': 'likert', 'text': text, 'tag': tag, 'rev': rev}
    if scale:
        it['scale'] = scale
    return it


def _choice(id, text, tag, options, optional=False, other=False):
    return {'id': id, 'type': 'choice', 'text': text, 'tag': tag,
            'options': options, 'optional': optional, 'other': other}


def _open(id, text, tag, optional=False, confidential=False):
    return {'id': id, 'type': 'open', 'text': text, 'tag': tag,
            'optional': optional, 'confidential': confidential}


def _sjt(id, text, tag, options=None):
    return {'id': id, 'type': 'sjt', 'text': text, 'tag': tag,
            'options': options or []}


def _rank(id, text, tag, options, other=False):
    return {'id': id, 'type': 'rank', 'text': text, 'tag': tag,
            'options': options, 'other': other}


def _mcq(id, text, tag, options, when=None):
    """A knowledge question with one correct answer. `when` gates the item on an
    earlier answer ({item_id: value}) — the form hides it and skips it in the
    step count when the condition isn't met."""
    it = {'id': id, 'type': 'choice', 'text': text, 'tag': tag,
          'options': options, 'optional': False, 'other': False}
    if when:
        it['when'] = when
    return it


# ===========================================================================
# STUDENT INSTRUMENT
# ===========================================================================
STUDENT_INTRO = ("This helps your counsellor understand the real you — not just "
                 "your marks. There are no right answers, and nothing here is shared "
                 "without your OK. Answer for yourself, not for who you think you "
                 "should be. It takes about 20 minutes.")

STUDENT_MODULES = [
    {'key': 'A', 'title': 'Where you stand academically',
     'intro': "Quick reality check — marks and confidence are different things, and we ask about both.",
     'items': [
        _choice('S61', "Which class are you in right now?", 'ACAD-CLASS',
                ['Class 11', 'Class 12']),
        {'id': 'S1', 'type': 'num', 'tag': 'ACAD-MARKS',
         'text': "In your most recent major exam (school/term test), roughly what did you score? Estimates are fine.",
         'fields': ['Physics %', 'Chemistry %', 'Maths %']},
        {'id': 'S2', 'type': 'choice_multi', 'tag': 'ACAD-TREND',
         'text': "Over the last year, each subject has been…",
         'rows': ['Physics', 'Chemistry', 'Maths'],
         'options': ['Improving', 'Steady', 'Slipping']},
        _likert('S3', "If I meet a completely new type of Physics problem, I can usually crack it if I put in the effort.", 'SELFEFF-PHY'),
        _likert('S4', "If I meet a completely new type of Chemistry problem, I can usually crack it if I put in the effort.", 'SELFEFF-CHE'),
        _likert('S5', "If I meet a completely new type of Maths problem, I can usually crack it if I put in the effort.", 'SELFEFF-MAT'),
        _choice('S6', "How sure are you about the three ratings you just gave?", 'CAL-SELFEFF',
                ['Very sure', 'Fairly sure', 'Honestly, guessing']),
        _choice('S7', "Right now, which feels more under control?", 'ACAD-GAP',
                ['Board exams', 'Entrance exams (JEE/state)', 'Both about equal', 'Honestly, neither']),
        _choice('S8', "In recent JEE Main / entrance mocks, your typical score band:", 'ACAD-ENTR',
                ['90+ percentile', '80–90', '70–80', '50–70', 'Below 50', "Haven't taken proper mocks yet"]),
     ]},
    {'key': 'A2', 'title': 'Nine questions from your NCERT syllabus',
     'intro': ("Three each from Physics, Chemistry and Maths — straight from your NCERT "
               "textbook, at board level. No negative marking, no timer, and your counsellor "
               "sees this as a diagnostic, never a verdict. Please don't look anything up: a "
               "wrong answer here is more useful to us than a googled right one."),
     'items': [
        # ---- Class 11 ----
        _mcq('N11P1', "A ball is thrown at 20 m/s at 30° above the horizontal. Taking g = 10 m/s², its total time of flight is:",
             'NCERT-PHY', ['1 s', '2 s', '2.5 s', '4 s'], when={'S61': 'Class 11'}),
        _mcq('N11P2', "A 5 kg block rests on a rough floor (μ = 0.2) and is pushed by a horizontal 20 N force. Taking g = 10 m/s², its acceleration is:",
             'NCERT-PHY', ['0', '2 m/s²', '4 m/s²', '6 m/s²'], when={'S61': 'Class 11'}),
        _mcq('N11P3', "Escape velocity at Earth's surface is about 11.2 km/s. For a planet of the same density but twice Earth's radius, escape velocity would be about:",
             'NCERT-PHY', ['5.6 km/s', '11.2 km/s', '22.4 km/s', '44.8 km/s'], when={'S61': 'Class 11'}),
        _mcq('N11C1', "How many moles of oxygen atoms are present in 88 g of CO₂? (C = 12, O = 16)",
             'NCERT-CHE', ['2', '3', '4', '6'], when={'S61': 'Class 11'}),
        _mcq('N11C2', "Which of these has the largest atomic radius?",
             'NCERT-CHE', ['Na', 'Mg', 'Al', 'Si'], when={'S61': 'Class 11'}),
        _mcq('N11C3', "The hybridisation of the central atom in BF₃ is:",
             'NCERT-CHE', ['sp', 'sp²', 'sp³', 'sp³d'], when={'S61': 'Class 11'}),
        _mcq('N11M1', "The sum of the first 20 terms of the AP 3, 7, 11, … is:",
             'NCERT-MAT', ['800', '820', '840', '860'], when={'S61': 'Class 11'}),
        _mcq('N11M2', "How many 3-digit numbers can be formed from the digits 1–9 if no digit is repeated?",
             'NCERT-MAT', ['84', '504', '648', '729'], when={'S61': 'Class 11'}),
        _mcq('N11M3', "The value of lim(x→0) sin(3x)/x is:",
             'NCERT-MAT', ['0', '1/3', '1', '3'], when={'S61': 'Class 11'}),
        # ---- Class 12 ----
        _mcq('N12P1', "Three 6 Ω resistors are connected in parallel. The equivalent resistance is:",
             'NCERT-PHY', ['2 Ω', '3 Ω', '9 Ω', '18 Ω'], when={'S61': 'Class 12'}),
        _mcq('N12P2', "A converging lens of focal length 20 cm forms an image of an object placed 30 cm in front of it. The image distance is:",
             'NCERT-PHY', ['12 cm', '20 cm', '60 cm', '−60 cm'], when={'S61': 'Class 12'}),
        _mcq('N12P3', "A parallel-plate capacitor has capacitance C. The plate separation is halved and a dielectric of constant 2 fills the gap. The new capacitance is:",
             'NCERT-PHY', ['C', '2C', '4C', '8C'], when={'S61': 'Class 12'}),
        _mcq('N12C1', "Which 0.1 m aqueous solution has the highest boiling point?",
             'NCERT-CHE', ['Glucose', 'Urea', 'NaCl', 'CaCl₂'], when={'S61': 'Class 12'}),
        _mcq('N12C2', "The oxidation state of cobalt in [Co(NH₃)₆]Cl₃ is:",
             'NCERT-CHE', ['+1', '+2', '+3', '+6'], when={'S61': 'Class 12'}),
        _mcq('N12C3', "For a first-order reaction, the half-life is:",
             'NCERT-CHE', ['Directly proportional to the initial concentration',
                           'Inversely proportional to the initial concentration',
                           'Independent of the initial concentration',
                           'Proportional to the square of the initial concentration'],
             when={'S61': 'Class 12'}),
        _mcq('N12M1', "If A is a 3×3 matrix with |A| = 2, then |2A| is:",
             'NCERT-MAT', ['4', '8', '16', '32'], when={'S61': 'Class 12'}),
        _mcq('N12M2', "The value of ∫₀^(π/2) cos x dx is:",
             'NCERT-MAT', ['0', '1', '−1', 'π/2'], when={'S61': 'Class 12'}),
        _mcq('N12M3', "The function f(x) = x³ − 3x has a local maximum at:",
             'NCERT-MAT', ['x = −1', 'x = 0', 'x = 1', 'x = 3'], when={'S61': 'Class 12'}),
     ]},
    {'key': 'B', 'title': 'What actually interests you',
     'intro': "Forget marks for a minute. These are about what you'd enjoy — pick honestly, not strategically.",
     'items': [
        {'id': 'S9', 'type': 'mostleast', 'tag': 'RIASEC', 'text': "Which would you most enjoy — and least?",
         'options': ['Assemble and fine-tune a drone till it flies right',
                     'Figure out why a circuit fails when heated',
                     'Design how an app looks and feels']},
        {'id': 'S10', 'type': 'mostleast', 'tag': 'RIASEC', 'text': "Which would you most enjoy — and least?",
         'options': ['Teach a junior a topic until it finally clicks',
                     "Convince a panel to fund your team's idea",
                     "Organise a fest's schedule, budgets and lists so nothing slips"]},
        {'id': 'S11', 'type': 'mostleast', 'tag': 'RIASEC', 'text': "Which would you most enjoy — and least?",
         'options': ['Strip and rebuild a two-wheeler engine',
                     'Run a stall and beat a sales target',
                     'Spend a free afternoon on a maths/physics puzzle nobody assigned']},
        {'id': 'S12', 'type': 'mostleast', 'tag': 'RIASEC', 'text': "Which would you most enjoy — and least?",
         'options': ['Write/design the college magazine',
                     "Keep a lab's records so precise anyone can rely on them",
                     'Be the person friends come to with problems']},
        _rank('S13', "Rank these six from 'most like me' (top) to 'least like me'.", 'RIASEC-ALL',
              ['Making and fixing real things',
               'Understanding how and why things work',
               'Creating something original',
               'Helping people learn or grow',
               'Leading, pitching, building a venture',
               'Bringing order — systems, data, checklists']),
        _open('S14', "What's something you do where you lose track of time? What exactly pulls you in?", 'RIASEC-OPEN'),
     ]},
    {'key': 'C', 'title': 'How you work',
     'intro': "Ten quick statements. First instinct is best.",
     'items': [
        _likert('S15', "I enjoy exploring ideas even when they're outside the syllabus.", 'BIG5-O'),
        _likert('S16', "I prefer sticking to methods I already know rather than trying new ways.", 'BIG5-O', rev=True),
        _likert('S17', "I finish my study plan even when nobody is checking on me.", 'BIG5-C'),
        _likert('S18', "I tend to leave things to the last minute.", 'BIG5-C', rev=True),
        _likert('S19', "Group work energises me more than working alone.", 'BIG5-E'),
        _likert('S20', "After a day with lots of people, I need quiet time to recharge.", 'BIG5-E', rev=True),
        _likert('S21', "I adjust easily when a friend wants to do things differently.", 'BIG5-A'),
        _likert('S22', "People say I keep arguing my point even when it upsets others.", 'BIG5-A', rev=True),
        _likert('S23', "Small setbacks (a bad mock, one poor mark) can spoil my whole day.", 'BIG5-N'),
        _likert('S24', "I stay steady even when an exam goes badly.", 'BIG5-N', rev=True),
     ]},
    {'key': 'D', 'title': 'Why engineering — and what matters to you',
     'intro': "The honest version, please — this is the one section where 'because everyone said so' is a perfectly useful answer.",
     'items': [
        _rank('S25', "Rank these reasons for doing engineering, from most true for you (top) to least.", 'MOTIV-RANK',
              ['I genuinely enjoy this kind of problem-solving',
               'It fits what I want to do with my life',
               "I'd feel ashamed/guilty backing out now",
               'The status and respect it brings',
               'My parents/family expect it',
               'The salary and settled life it promises']),
        _likert('S26', "Choosing engineering was mainly my own decision.", 'MOTIV-AUTONOMY'),
        _likert('S27', "If it were completely up to me, I might have chosen a different path.", 'MOTIV-AUTONOMY', rev=True),
        _choice('S28', "Imagine every stream guaranteed you a good college seat. You would:", 'MOTIV-AUTONOMY',
                ['Still pick engineering, no doubt', 'Probably still engineering',
                 'Seriously consider something else', 'Pick something else']),
        _open('S29', "If engineering didn't exist, what would you study or become instead? ('no idea' is a fine answer)", 'MOTIV-OPEN'),
        _rank('S30', "Rank what matters most in your future work life (top = most).", 'VALUE-RANK',
              ['Stability and security', 'Being clearly excellent at something',
               'Freedom to decide how I work', 'Making a difference to people',
               'Building/creating new things', 'Recognition and prestige']),
        _choice('S31', "Pick one:", 'VALUE-FC',
                ['A stable, respected job that rarely changes',
                 'An exciting, changing role where some years are uncertain']),
        _choice('S32', "Pick one:", 'VALUE-FC',
                ['₹25 LPA doing work that bores you',
                 '₹12 LPA doing work you genuinely enjoy']),
     ]},
    {'key': 'E', 'title': 'Branches — what you know and want',
     'intro': "No trick questions. 'Not sure' is genuinely useful information for your counsellor.",
     'items': [
        _rank('S33', "Rank these branch groups by your current preference (top = first choice).", 'BRANCH-PREF',
              ['CSE / IT / AI-DS', 'ECE / EEE', 'Mechanical / Aerospace / Auto',
               'Civil / Environmental', 'Chemical / Biotech', 'Something else'], other=True),
        _choice('S34', "How settled is your #1 choice?", 'CAL-BRANCH',
                ['Fully settled', 'Fairly settled', 'Could easily change', 'I ranked almost at random']),
        _open('S35', "In your own words: what does a software (CSE) engineer actually do on a normal working day?", 'BRANCH-AWARE-CSE'),
        _open('S36', "Same question for your #1 branch (skip if it's CSE): what does that engineer do all day?", 'BRANCH-AWARE-TOP', optional=True),
        _open('S37', "What makes your #1 branch right for you specifically?", 'BRANCH-HERD'),
        {'id': 'S38', 'type': 'choice_multi', 'tag': 'BRANCH-MYTH',
         'text': "True, False or Not sure?",
         'rows': ['Only CSE/IT students can get software jobs',
                  'The "highest package" in college ads is what a typical student gets',
                  'Mechanical/Civil careers often peak through GATE, PSUs and higher studies rather than campus mass-hiring',
                  'A top NAAC grade guarantees strong placements'],
         'options': ['True', 'False', 'Not sure']},
        _sjt('S39', "You get your dream branch at a lower-ranked college, and a branch you dislike at a famous college. Which do you take — and why?", 'SJT-BRANCH',
             ['Dream branch, lower college', 'Famous college, disliked branch', "Genuinely can't say"]),
        _sjt('S40', "Your closest friends all lock CSE, but you keep thinking about Mechanical. What do you actually do — and why?", 'SJT-HERD',
             ['Follow CSE — safer together', 'Pick Mechanical anyway',
              'Try to talk myself out of Mechanical', 'Something else']),
     ]},
    {'key': 'F', 'title': 'Where you hope this goes',
     'intro': "Dream freely here — there are no wrong answers.",
     'items': [
        _open('S41', "Describe your ideal working day ten years from now — where you wake up, the work you do, the people around you.", 'ASPIRE-DAY'),
        _choice('S42', "Which feels most like 'I've made it' at 30?", 'ASPIRE-DEF',
                ['A senior, stable role in a strong company', 'My own startup/venture',
                 'Research or higher studies (IISc/IIT/abroad)',
                 'A high-paying job even if the work is routine',
                 'Being the respected expert people call first']),
        _open('S43', "What worries you most about the next 12 months?", 'FEAR'),
        _open('S44', "What do you think your parents want for you? Is it the same as what you want?", 'ALIGN-CAREER'),
     ]},
    {'key': 'G', 'title': 'Real-life constraints',
     'intro': "Practical realities shape good advice. This stays with your counsellor.",
     'items': [
        _choice('S45', "For college, you would honestly prefer:", 'CONSTR-LOC',
                ['Stay in/near my home town', 'Anywhere in my state',
                 'Anywhere in India — distance no bar', "I'd rather not move, but I will if needed"]),
        _choice('S46', "Do you know roughly what your family can spend on your engineering?", 'CONSTR-BUDGET-AWARE',
                ['Yes, clearly', 'Roughly', "No idea — we've never discussed it"]),
        _choice('S47', "Your best guess of the total 4-year budget (fees + hostel + everything):", 'CONSTR-BUDGET-EST',
                ['Under ₹4 L', '₹4–8 L', '₹8–12 L', '₹12–20 L', '₹20–30 L', 'Above ₹30 L', 'Truly no idea']),
        _choice('S48', "In the final college decision, how much say do you expect to have?", 'ALIGN-FREEDOM',
                ["It'll be fully my call", 'Mostly mine, parents advise', 'Truly joint',
                 "Mostly my parents' call", "Fully my parents' call"]),
        _likert('S49', "College/exam discussions at home often end in tension.", 'PRESSURE'),
        _open('S50', "Is there anything about your preferences you haven't told your parents yet? It stays between you and your counsellor.", 'HIDDEN', optional=True, confidential=True),
     ]},
    {'key': 'H', 'title': "How you're preparing",
     'intro': "A quick read on your prep style and exam temperament.",
     'items': [
        _choice('S51', "Your main prep mode right now:", 'PREP-MODE',
                ['Classroom coaching + school', 'Online coaching', 'Mostly self-study', 'School alone, no extra prep']),
        _likert('S52', "I follow a fixed weekly study routine.", 'PREP-CONSIST'),
        _likert('S53', "Honestly, I study seriously only when an exam is close.", 'PREP-CONSIST', rev=True),
        _choice('S54', "In the actual exam hall, compared to mocks/practice, you usually perform:", 'PREP-TEMPER',
                ['Better', 'About the same', 'Worse', 'Totally unpredictable']),
        _sjt('S55', "Two weeks before boards, your JEE mock scores suddenly drop. What do you actually do first — and why?", 'SJT-PRESSURE'),
        _choice('S56', "Do you have a written week-by-week plan up to your exams?", 'PREP-PLAN',
                ['Yes, and I mostly follow it', 'A rough plan in my head', 'No plan yet']),
     ]},
    {'key': 'I', 'title': 'Four quick brain-teasers',
     'intro': "Tiny puzzles, 30–60 seconds each. They're a signal for your counsellor, not a test score.",
     'items': [
        _choice('S57', "Blueprint is to Building as Recipe is to:", 'APT-VERBAL',
                ['Kitchen', 'Chef', 'Dish', 'Menu']),
        _choice('S58', "Pump A fills a tank in 6 hours; pump B in 3. Together they take:", 'APT-NUM',
                ['2 h', '2.5 h', '3 h', '4.5 h']),
        _choice('S59', "5, 9, 17, 33, … what comes next?", 'APT-LOGIC',
                ['49', '57', '65', '66']),
        _choice('S60', "A cube is painted on all sides, then cut into 27 identical small cubes. How many have paint on exactly two faces?", 'APT-SPATIAL',
                ['6', '8', '12', '24']),
     ]},
]

# answer key for every scored item — aptitude samplers + the NCERT diagnostic.
# Counsellor-side only: it reaches the admin view and the AI bundle, never the form.
ANSWER_KEY = {
    'S57': 'Dish', 'S58': '2 h', 'S59': '65', 'S60': '12',
    # class 11
    'N11P1': '2 s', 'N11P2': '2 m/s²', 'N11P3': '22.4 km/s',
    'N11C1': '4', 'N11C2': 'Na', 'N11C3': 'sp²',
    'N11M1': '820', 'N11M2': '504', 'N11M3': '3',
    # class 12
    'N12P1': '2 Ω', 'N12P2': '60 cm', 'N12P3': '4C',
    'N12C1': 'CaCl₂', 'N12C2': '+3', 'N12C3': 'Independent of the initial concentration',
    'N12M1': '16', 'N12M2': '1', 'N12M3': 'x = −1',
}


# ===========================================================================
# PARENT INSTRUMENT
# ===========================================================================
PARENT_INTRO = ("You know your child in ways no test can capture. This helps your "
                "counsellor combine your knowledge with your child's own answers. "
                "Please fill it independently — don't compare answers; the differences "
                "are exactly what we'll work on together. Answer honestly, not ideally. "
                "It takes about 12 minutes.")

PARENT_MODULES = [
    {'key': '1', 'title': 'Your child, as you see them',
     'intro': "First, your read on your child — before you see any of their answers.",
     'items': [
        _rank('P1', "Rank your child's school subjects by real strength (top = strongest).", 'ALIGN-STRENGTH',
              ['Physics', 'Chemistry', 'Maths']),
        _open('P2', "Outside studies, what does your child most enjoy doing — and what do they do when nobody is directing them?", 'ALIGN-INTEREST'),
        {'id': 'P3', 'type': 'pick', 'tag': 'ALIGN-INTEREST', 'pick': 2,
         'text': "Which two of these would your child most enjoy? (pick two)",
         'options': ['Making/fixing real things', 'Figuring out why things work',
                     'Creating/designing something original', 'Helping and teaching people',
                     'Leading and persuading', 'Organising things perfectly']},
        _likert('P4', "My child is genuinely confident in Maths and Physics.", 'ALIGN-STRENGTH'),
        _likert('P5', "Engineering was mainly my child's own idea.", 'ALIGN-MOTIV'),
        _choice('P6', "How sure are you about your answers so far?", 'CAL-P',
                ['Very sure', 'Fairly sure', 'Honestly, guessing a bit']),
     ]},
    {'key': '2', 'title': "Your hopes — and your child's",
     'intro': "Your aspirations, and your read on what your child actually wants.",
     'items': [
        _open('P7', "Describe the life you hope your child has at 30 — work, place, lifestyle.", 'ALIGN-CAREER'),
        {'id': 'P8', 'type': 'choice_pair', 'tag': 'ALIGN-BRANCH',
         'text': "Which branch do you prefer for your child, and how fixed is that?",
         'groups': [
            {'key': 'branch', 'label': 'Preferred branch',
             'options': ['CSE / IT', 'ECE / EEE', 'Mechanical', 'Civil', 'Chemical / Biotech', 'No preference']},
            {'key': 'fixed', 'label': 'How fixed',
             'options': ['Must be this branch', 'Strong preference, open to discussion',
                         'Mild preference', "Fully my child's choice"]}]},
        _choice('P9', "About CSE specifically:", 'PARENT-CSE',
                ['Only CSE makes sense to me', 'CSE preferred, others acceptable',
                 'Whatever fits my child', 'I actually prefer a non-CSE branch']),
        _open('P10', "Independently of your hopes — what do you believe your child wants?", 'ALIGN-CAREER'),
        _choice('P11', "The final college decision should be:", 'ALIGN-FREEDOM',
                ['My/our call as parents', 'Parents decide after hearing the child',
                 'Truly joint', 'Child decides after hearing us', "Fully my child's call"]),
     ]},
    {'key': '3', 'title': 'The admissions landscape — honest self-check',
     'intro': "Nobody knows all of this — that's what we're for. Your honest ratings become your session agenda. (1 = never heard of it · 5 = could explain it to another parent.)",
     'items': [
        {'id': 'P12', 'type': 'likert_multi', 'tag': 'PARENT-KNOW-ADM', 'scale': 'familiarity',
         'text': "Rate your familiarity:",
         'rows': ['JEE Main vs JEE Advanced — what each is for',
                  'JoSAA counselling — rounds, choice filling, NIT/IIIT/GFTI routes',
                  'Your home-state counselling (e.g. TNEA) — how seats are allotted',
                  'Private-university exams (BITSAT, VITEEE, SRMJEEE, COMEDK…)',
                  'Management / NRI quota — how it works and what it costs']},
        {'id': 'P13', 'type': 'likert_multi', 'tag': 'PARENT-KNOW-ECO', 'scale': 'familiarity',
         'text': "Rate your familiarity:",
         'rows': ['Deemed vs autonomous vs affiliated colleges',
                  "NAAC / NBA accreditation — what it does and doesn't tell you",
                  'Branch-vs-college trade-offs',
                  'Placement realities — median vs "highest package"',
                  'Education loans and scholarships']},
        _choice('P14', "Quick check — in JoSAA counselling, NIT seats are allotted mainly on:", 'PARENT-KNOW-QUIZ',
                ['JEE Advanced rank', 'JEE Main rank', 'Class 12 marks alone', 'College interviews']),
        _choice('P15', "True or False: 'The highest package a college advertises is a good estimate of what a typical student there earns.'", 'PARENT-KNOW-QUIZ',
                ['True', 'False']),
        _open('P16', "Which part of the whole admissions process feels most confusing or worrying right now?", 'PARENT-KNOW-OPEN'),
     ]},
    {'key': '4', 'title': 'Budget — the practical picture',
     'intro': "A realistic budget shapes the entire strategy. This stays confidential.",
     'items': [
        _choice('P17', "Total 4-year budget you can realistically commit (fees + hostel + everything):", 'PARENT-BUDGET',
                ['Under ₹4 L', '₹4–8 L', '₹8–12 L', '₹12–20 L', '₹20–30 L', 'Above ₹30 L', 'Not yet decided']),
        _choice('P18', "An education loan is:", 'PARENT-LOAN',
                ["Something we'd take comfortably", 'Acceptable if genuinely needed',
                 'A last resort', 'Not an option for us']),
        _choice('P19', "Does your child know this budget?", 'ALIGN-BUDGET-AWARE',
                ['Yes, exactly', 'Roughly', "No — we haven't discussed money with them"]),
        _choice('P20', "Your honest starting position:", 'PARENT-BUDGET-TYPE',
                ['Government/aided colleges only', 'Prefer government, private if clearly better',
                 'Open to any college that fits', 'Prefer reputed private colleges']),
        _sjt('P21', "The college that fits your child best costs ~30% more than your budget. What would you actually do — and why?", 'SJT-P-BUDGET'),
     ]},
    {'key': '5', 'title': 'Risk appetite',
     'intro': "How much uncertainty you're comfortable with.",
     'items': [
        _choice('P22', "How far are you comfortable sending your child?", 'ALIGN-LOC',
                ['Day-scholar distance only', 'Within our state', 'Anywhere in India',
                 'Depends entirely on the college']),
        _sjt('P23', "If forced to choose: the right branch at a less famous college, or the famous college whatever branch it offers — and why?", 'PARENT-RISK-BC',
             ['Right branch, less famous college', 'Famous college, any branch']),
        _sjt('P24', "Results day: your child's rank is well below hope. Your instinct — and why?", 'PARENT-RISK-REPEAT',
             ['Take the best seat available this year', 'A repeat year for a better rank', 'Depends']),
        _likert('P25', "A well-known college near home is always the safer choice than a better-fit college far away.", 'PARENT-RISK-SAFE', rev=True),
     ]},
    {'key': '6', 'title': 'Working with us',
     'intro': "So we tailor the membership to what you actually need.",
     'items': [
        _open('P26', "Twelve months from now, what would make you say this membership was completely worth it?", 'PARENT-EXPECT'),
        _rank('P27', "Rank what you need most from us (top = highest).", 'PARENT-EXPECT-RANK',
              ['Building the right college list', 'Branch guidance for my child',
               'Forms, deadlines and counselling-round execution',
               'Helping my child and me get on the same page']),
        _choice('P28', "Your preferred involvement:", 'PARENT-EXPECT-INVOLVE',
                ['Involve me in every step', 'Key decisions only',
                 'Guide us, but we decide everything ourselves']),
     ]},
    {'key': '7', 'title': 'The home front',
     'intro': "The household reality. Honest answers help us help you; nothing is judged.",
     'items': [
        _likert('P29', "College/exam discussions at home often end in tension.", 'ALIGN-PRESSURE'),
        _likert('P30', "Opinions of relatives and family friends carry real weight in this decision.", 'PRESSURE-EXT'),
        _likert('P31', "My child ends up being compared with siblings/cousins on academics.", 'PRESSURE-COMP'),
        _likert('P32', "Whichever branch my child finally chooses, I will back it.", 'PARENT-FLEX-BRANCH', rev=True),
        _likert('P33', "Honestly, without my push, my child would not take this decision seriously.", 'ALIGN-MOTIV', rev=True),
        _open('P34', "Is there anything about this decision you haven't been able to discuss openly with your child? It stays with your counsellor.", 'HIDDEN-P', optional=True, confidential=True),
     ]},
]


# --- lookups ---------------------------------------------------------------
ROLES = ('student', 'parent')
_MODULES = {'student': STUDENT_MODULES, 'parent': PARENT_MODULES}
_INTRO = {'student': STUDENT_INTRO, 'parent': PARENT_INTRO}


def modules_for(role):
    return _MODULES.get(role, [])


def intro_for(role):
    return _INTRO.get(role, '')


def items_for(role):
    """Flat list of all items for a role, in order."""
    return [it for mod in modules_for(role) for it in mod['items']]


def item_count(role):
    return len(items_for(role))
