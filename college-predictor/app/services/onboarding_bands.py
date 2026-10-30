"""Grade bands for the membership onboarding assessment.

The original instrument was written for Class 12 engineering aspirants. This module turns it into one grade-aware instrument without changing a stored answer:
the first questions ask the class (S61, as before), the board (S62) and, from Class 10, the career path the student leans to (S63). Every later question carries a
`when` gate, so each family sees only what fits.

    Explore  Class 7-9    stream selection: strengths, interests, how the student learns, what streams and careers exist, which stream to lean to
    Direct   Class 10-11  colleges, branches and the career goal: academics, interests, the path (engineering / medicine / law / management), colleges and options
    Senior   Class 12     the original engineering instrument, unchanged in substance; students on another path get that path's module instead

A `when` is {item_id: value} (all must match), a value may be a list (any of), and a LIST of such dicts means any one of them (OR).
`apply(ns)` is called once, at the bottom of onboarding_assessment.py, and edits its module lists in place.
"""
EXPLORE = ['Class 7', 'Class 8', 'Class 9']
DIRECT = ['Class 10', 'Class 11']
SENIOR = ['Class 12']
CLASSES = EXPLORE + DIRECT + SENIOR
SR = DIRECT + SENIOR                                  # Class 10 and above: asked about a career path, colleges and options
PATH_ENG, PATH_MED, PATH_LAW, PATH_MGT = 'Engineering', 'Medicine and health', 'Law', 'Management and business'
PATH_OTHER, PATH_NONE = 'Design, arts or something else', 'Not decided yet'
PATHS = [PATH_ENG, PATH_MED, PATH_LAW, PATH_MGT, PATH_OTHER, PATH_NONE]
NOT_ENG = [p for p in PATHS if p != PATH_ENG]
BAND_OF = {c: 'Explore' for c in EXPLORE} | {c: 'Direct' for c in DIRECT} | {c: 'Senior' for c in SENIOR}

# who sees what, written once
W_EXPLORE = {'S61': EXPLORE}
W_SR = {'S61': SR}
W_ENG = {'S61': SR, 'S63': PATH_ENG}                                      # engineering path, Class 10-12
W_ENG_SENIOR = {'S61': ['Class 11', 'Class 12'], 'S63': PATH_ENG}         # engineering path with the PCM-style academic block, Class 11-12
W_STAND = [{'S61': 'Class 10'}, {'S61': ['Class 11', 'Class 12'], 'S63': NOT_ENG}]   # the generic "where you stand" block (engineering Class 11-12 has its own)


def band_for(class_label):
    return BAND_OF.get(class_label, '')


def apply(ns):
    L, C, O, R, S, M = ns['_likert'], ns['_choice'], ns['_open'], ns['_rank'], ns['_sjt'], ns['_mcq']
    STU, PAR, KEY = ns['STUDENT_MODULES'], ns['PARENT_MODULES'], ns['ANSWER_KEY']

    def mcq(id, text, tag, options, answer, when):
        KEY[id] = answer
        return M(id, text, tag, options, when=when)

    def lk(id, text, tag, when, rev=False):
        it = L(id, text, tag, rev=rev)
        it['when'] = when
        return it

    def mk(id, text, tag, kind, when, **kw):
        it = {'id': id, 'type': kind, 'text': text, 'tag': tag, 'when': when}
        it.update(kw)
        return it

    def put(it, when):
        it['when'] = when
        return it

    def mostleast(id, options, tag, when):
        return mk(id, "Which would you most enjoy, and which least?", tag, 'mostleast', when, options=options)

    def num(id, text, fields, tag, when):
        return mk(id, text, tag, 'num', when, fields=fields)

    def fam(id, text, rows, tag, when):
        return mk(id, text, tag, 'likert_multi', when, rows=rows, scale='familiarity')

    # ------------------------------------------------------------------ gate the existing Class 11-12 engineering items
    def gate(modules, ids, when):
        for m in modules:
            for it in m['items']:
                if it['id'] in ids:
                    it['when'] = when if not it.get('when') else {**it['when'], **when}

    by = {m['key']: m for m in STU}
    a = by['A']
    a['items'] = [it for it in a['items'] if it['id'] != 'S61']               # the class question now opens the whole instrument
    a['title'] = 'Where you stand academically (engineering path, Class 11-12)'
    gate(STU, {'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'}, W_ENG_SENIOR)
    for it in by['A2']['items']:                                              # the NCERT diagnostic is for engineering students only
        it['when'] = {**it['when'], 'S63': PATH_ENG}
    gate(STU, {'S9', 'S10', 'S11', 'S12'}, W_ENG)
    gate(STU, {'S13', 'S14'}, W_SR)
    gate(STU, {f'S{n}' for n in range(15, 25)}, W_SR)                         # how you work
    gate(STU, {f'S{n}' for n in range(25, 33)}, W_ENG)                        # why engineering
    gate(STU, {f'S{n}' for n in range(33, 41)}, W_ENG)                        # branches
    gate(STU, {f'S{n}' for n in range(41, 51)}, W_SR)                         # hopes and constraints
    gate(STU, {'S51', 'S52', 'S53', 'S54', 'S56'}, W_SR)                      # preparing
    gate(STU, {'S55'}, W_ENG)
    gate(STU, {'S57', 'S58', 'S59', 'S60'}, W_SR)                             # brain-teasers
    for it in by['G']['items']:                                               # the money questions apply to every path
        if it['id'] == 'S46':
            it['text'] = "Do you know roughly what your family can spend on your college education?"
        if it['id'] == 'S47':
            it['text'] = "Your best guess of the total budget for the whole course (fees + hostel + everything):"
    by['D']['intro'] = "The honest version, please. This is the one section where 'because everyone said so' is a perfectly useful answer."

    # ------------------------------------------------------------------ module 0: about you (everyone)
    m0 = {'key': '0', 'title': 'About you',
          'intro': "Three quick questions so we ask you the right things. Your answers shape the rest of the form.",
          'items': [
              C('S61', "Which class are you in right now?", 'ACAD-CLASS', CLASSES),
              C('S62', "Which board do you study under?", 'ACAD-BOARD', ['CBSE', 'ICSE / ISC', 'State board', 'IB / Cambridge (IGCSE, A-levels)', 'NIOS or other']),
              put(C('S63', "Which career path are you most drawn to right now?", 'PATH-CHOICE', PATHS), W_SR),
          ]}

    # ------------------------------------------------------------------ Explore band, Class 7-9
    E = W_EXPLORE
    x1 = {'key': 'X1', 'title': 'How school is going',
          'intro': "Marks and confidence are different things, and we ask about both. Estimates are fine.",
          'items': [
              num('EX1', "In your most recent major exam, roughly what did you score?", ['Maths %', 'Science %', 'English %', 'Social Science %', 'Second language %'], 'ACAD-MARKS', E),
              mk('EX2', "Over the last year, each subject has been...", 'ACAD-TREND', 'choice_multi', E, rows=['Maths', 'Science', 'English', 'Social Science'], options=['Improving', 'Steady', 'Slipping']),
              lk('EX3', "If I meet a new kind of Maths problem, I can usually work it out if I try.", 'SELFEFF-MAT', E),
              lk('EX4', "If I meet a new kind of Science question, I can usually work it out if I try.", 'SELFEFF-SCI', E),
              lk('EX5', "I am comfortable reading, writing and speaking in English.", 'SELFEFF-LANG', E),
              put(C('EX6', "Which subject do you enjoy most?", 'ENJOY-SUBJ', ['Maths', 'Science', 'English and languages', 'Social Science', 'Computers and coding', 'Art, music or sport']), E),
              put(C('EX7', "Which subject feels hardest?", 'HARD-SUBJ', ['Maths', 'Science', 'English and languages', 'Social Science', 'Computers and coding', 'Art, music or sport']), E),
          ]}
    x2 = {'key': 'X2', 'title': 'What you enjoy',
          'intro': "Forget marks for a minute. These are about what you would enjoy. Pick honestly.",
          'items': [
              mostleast('EX8', ['Build a model or fix something that is broken', 'Find out why something works the way it does', 'Draw, design or make a video of your own idea'], 'RIASEC', E),
              mostleast('EX9', ['Help a friend understand a lesson', 'Lead your team in a competition or school event', 'Keep your notes, bag and class records neat and organised'], 'RIASEC', E),
              mostleast('EX10', ['Look after a plant, a pet or someone who is unwell', 'Debate and argue a point in class', 'Run a small stall at the school fair'], 'RIASEC', E),
              put(R('EX11', "Rank these six from 'most like me' (top) to 'least like me'.", 'RIASEC-ALL',
                    ['Making and fixing real things', 'Understanding how and why things work', 'Creating something original',
                     'Helping people learn or grow', 'Leading and organising people', 'Keeping things in order: lists, data, plans']), E),
              put(O('EX12', "What do you do where you lose track of time? What pulls you in?", 'RIASEC-OPEN'), E),
          ]}
    x3 = {'key': 'X3', 'title': 'How you learn',
          'intro': "Six quick statements. First instinct is best.",
          'items': [
              lk('EX13', "I like finding out more about a topic even when it will not be in the exam.", 'BIG5-O', E),
              lk('EX14', "I finish my homework without being reminded.", 'PREP-CONSIST', E),
              lk('EX15', "I find it hard to stay off my phone or games when I should be studying.", 'DISTRACT', E, rev=True),
              lk('EX16', "When I do not understand something, I ask my teacher or a friend.", 'HELP-SEEK', E),
              lk('EX17', "If I get a low mark, I try to find out what went wrong.", 'GROWTH', E),
              lk('EX18', "I like working in a team more than working alone.", 'BIG5-E', E),
          ]}
    x4 = {'key': 'X4', 'title': 'Careers you have heard of',
          'intro': "No wrong answers. We want to know how much of the world of work you have seen so far.",
          'items': [
              fam('EX19', "How well could you explain what people in these jobs do all day?",
                  ['Engineer', 'Doctor', 'Lawyer', 'Business manager or entrepreneur', 'Designer or architect', 'Scientist or researcher'], 'CAREER-AWARE', E),
              mk('EX20', "Which two careers are you most curious about? (pick two)", 'PATH-CURIOUS', 'pick', E, pick=2,
                 options=['Engineer', 'Doctor or health professional', 'Lawyer', 'Manager or entrepreneur', 'Designer, artist or architect', 'Scientist or researcher', 'Teacher', 'Government or civil services']),
              put(O('EX21', "Who do you look up to, and what is it about their work that you like?", 'PATH-ROLEMODEL'), E),
              put(C('EX22', "How much have you thought about what you want to do after school?", 'PATH-READY',
                    ['A lot: I have a clear idea', 'Some: a few ideas', 'A little', 'Not at all']), E),
          ]}
    x5 = {'key': 'X5', 'title': 'Choosing a stream',
          'intro': ("After Class 10, most students choose a stream (Science, Commerce or Humanities), and that choice decides which entrance exams and courses stay open. "
                    "Nothing to memorise here: we want to know what you already understand and where you lean."),
          'items': [
              mcq('EX23', "In most Indian schools, students choose a stream (Science, Commerce or Humanities) when they join:", 'STREAM-KNOW', ['Class 8', 'Class 9', 'Class 11', 'Class 12'], 'Class 11', E),
              mcq('EX24', "To prepare for engineering entrance exams such as JEE Main, a student usually studies Physics, Chemistry and:", 'STREAM-KNOW',
                  ['Biology', 'Mathematics', 'Accountancy', 'Economics'], 'Mathematics', E),
              mcq('EX25', "To study medicine (MBBS) through NEET, a student usually studies Physics, Chemistry and:", 'STREAM-KNOW',
                  ['Mathematics', 'Biology', 'Accountancy', 'History'], 'Biology', E),
              mcq('EX26', "A student from which stream can usually apply for undergraduate law programmes such as CLAT?", 'STREAM-KNOW',
                  ['Only Humanities', 'Only Commerce', 'Only Science', 'Any stream'], 'Any stream', E),
              put(C('EX27', "Right now, which stream do you lean towards?", 'STREAM-LEAN',
                    ['Science with Maths (PCM)', 'Science with Biology (PCB)', 'Science with both Maths and Biology', 'Commerce', 'Humanities or Arts', 'Not sure yet']), E),
              put(C('EX28', "How sure are you about that?", 'CAL-STREAM', ['Very sure', 'Fairly sure', 'Could easily change', 'No idea yet']), E),
              put(O('EX29', "What makes you lean that way: a subject you enjoy, a job you imagine, or advice from someone?", 'STREAM-WHY'), E),
              put(R('EX30', "What should matter most when you pick a stream? (top = most)", 'STREAM-FACTOR',
                    ['Subjects I enjoy', 'Subjects I am good at', 'The career I want', 'Which exams and courses it keeps open', 'What my family advises', 'What my friends choose']), E),
              put(S('EX31', "All your friends choose Commerce, but you enjoy Science most. What do you do, and why?", 'SJT-STREAM-HERD',
                    ['Follow my friends', 'Choose Science', 'Ask my parents and teachers first', 'Something else']), E),
          ]}
    x6 = {'key': 'X6', 'title': 'Four quick brain-teasers',
          'intro': "Tiny puzzles, 30 to 60 seconds each. They are a signal for your mentor, not a test score.",
          'items': [
              mcq('EX32', "Doctor is to Hospital as Teacher is to:", 'APT-VERBAL', ['Book', 'School', 'Student', 'Pen'], 'School', E),
              mcq('EX33', "A pencil costs 6 rupees. How many pencils can you buy with 75 rupees?", 'APT-NUM', ['10', '11', '12', '13'], '12', E),
              mcq('EX34', "2, 6, 12, 20, 30, ... what comes next?", 'APT-LOGIC', ['36', '40', '42', '44'], '42', E),
              mcq('EX35', "A cube is painted on all outside faces and cut into 8 equal small cubes (2 x 2 x 2). How many small cubes have paint on exactly 3 faces?", 'APT-SPATIAL',
                  ['4', '6', '8', '12'], '8', E),
          ]}
    x7 = {'key': 'X7', 'title': 'Your hopes',
          'intro': "Dream freely. There are no wrong answers.",
          'items': [
              put(O('EX36', "Describe a day in the life you imagine for yourself ten years from now.", 'ASPIRE-DAY'), E),
              put(O('EX37', "What worries you most about the next two years of school?", 'FEAR'), E),
              put(C('EX38', "Who helps you most when you think about your future?", 'ALIGN-SUPPORT', ['Parents', 'Teachers', 'Older cousins or friends', 'Coaching or a mentor', 'Nobody yet']), E),
              put(C('EX39', "When it comes to choosing a stream or career, you expect:", 'ALIGN-FREEDOM',
                    ["It will be fully my call", 'Mostly mine, parents advise', 'Truly joint', "Mostly my parents' call", "Fully my parents' call"]), E),
              put(O('EX40', "Is there anything about your plans you have not told your parents yet? It stays between you and your mentor.", 'HIDDEN', optional=True, confidential=True), E),
          ]}

    # ------------------------------------------------------------------ Direct and Senior: generic academics and interests for every path
    Y = W_STAND
    y1 = {'key': 'Y1', 'title': 'Where you stand academically',
          'intro': "Marks and confidence are different things, and we ask about both. Estimates are fine.",
          'items': [
              put(C('CX1', "Which subject group are you in, or planning to choose for Class 11?", 'STREAM-LEAN',
                    ['PCM (Physics, Chemistry, Maths)', 'PCB (Physics, Chemistry, Biology)', 'PCMB (all four)', 'Commerce with Maths', 'Commerce without Maths', 'Humanities or Arts', 'Not decided yet']), W_SR),
              num('CX2', "In your most recent major exam, roughly what did you score?", ['Maths %', 'Science %', 'English %', 'Social Science %'], 'ACAD-MARKS', {'S61': 'Class 10'}),
              put(C('CX3', "What do you expect to score in your Class 10 board exam?", 'ACAD-EXPECT',
                    ['90% and above', '80 to 90%', '70 to 80%', '60 to 70%', 'Below 60%', 'Not sure']), {'S61': 'Class 10'}),
              num('CX4', "In your most recent major exam, roughly what did you score?", ['Overall %', 'Your strongest subject %', 'Your weakest subject %'], 'ACAD-MARKS',
                  {'S61': ['Class 11', 'Class 12'], 'S63': NOT_ENG}),
              put(C('CX5', "Over the last year, your marks have been:", 'ACAD-TREND', ['Improving', 'Steady', 'Slipping']), Y),
              lk('CX6', "If I meet a completely new type of Maths problem, I can usually crack it if I put in the effort.", 'SELFEFF-MAT', Y),
              lk('CX7', "If I meet a completely new type of Science problem, I can usually crack it if I put in the effort.", 'SELFEFF-SCI', Y),
              lk('CX8', "I can write and speak clearly in English, even on a difficult topic.", 'SELFEFF-LANG', Y),
              put(C('CX9', "How sure are you about the three ratings you just gave?", 'CAL-SELFEFF', ['Very sure', 'Fairly sure', 'Honestly, guessing']), Y),
          ]}
    b2 = {'key': 'B2', 'title': 'What actually interests you',
          'intro': "Forget marks for a minute. These are about what you would enjoy. Pick honestly, not strategically.",
          'items': [
              mostleast('CX10', ['Build or fix a machine until it works', 'Work out why an experiment gave an odd result', 'Design a poster, a video or a product people love'], 'RIASEC', Y),
              mostleast('CX11', ['Teach someone a topic until it clicks', 'Persuade a panel to back your idea', 'Plan a fest schedule and budget so nothing slips'], 'RIASEC', Y),
              mostleast('CX12', ['Look after a patient, a plant or an animal', 'Argue a case with facts and reasons', 'Run a small business stall and beat a target'], 'RIASEC', Y),
          ]}
    # ------------------------------------------------------------------ path modules (Class 10-12)
    P = lambda path: {'S61': SR, 'S63': path}
    mdm = {'key': 'MD', 'title': 'Medicine and health: what you know and what draws you',
           'intro': "Honest answers only. 'Not sure' is useful information for your mentor.",
           'items': [
               mcq('MD1', "Admission to MBBS in India is mainly through which entrance exam?", 'MED-KNOW', ['JEE Main', 'NEET UG', 'CLAT', 'CUET only'], 'NEET UG', P(PATH_MED)),
               mcq('MD2', "NEET UG tests Physics, Chemistry and:", 'MED-KNOW', ['Mathematics', 'Biology (Botany and Zoology)', 'Accountancy', 'English'], 'Biology (Botany and Zoology)', P(PATH_MED)),
               lk('MD3', "I am ready to study for many years: medicine takes five years or more before you can start practising.", 'MED-STAMINA', P(PATH_MED)),
               lk('MD4', "I stay calm and focused around illness, injury or blood.", 'MED-TEMPER', P(PATH_MED)),
               lk('MD5', "I enjoy Biology, even the parts that need a lot of memorising.", 'MED-BIO', P(PATH_MED)),
               lk('MD6', "I would still be happy working in healthcare if I did not get an MBBS seat.", 'MED-BACKUP', P(PATH_MED)),
               put(R('MD7', "Rank these routes by your interest (top = most).", 'MED-ROUTE',
                     ['MBBS (doctor)', 'BDS (dentistry)', 'AYUSH (Ayurveda, Homeopathy, Unani and others)', 'Nursing, physiotherapy or allied health',
                      'Veterinary science', 'Biomedical or life-science research']), P(PATH_MED)),
               put(O('MD8', "What draws you to medicine? Is there a person or an event that inspired you?", 'MED-WHY'), P(PATH_MED)),
               put(S('MD9', "NEET does not give you an MBBS seat this year. What do you do, and why?", 'SJT-MED-PLANB',
                     ['Repeat a year and try again', 'Choose another health course', 'Choose a different field', 'Not sure']), P(PATH_MED)),
           ]}
    lwm = {'key': 'LW', 'title': 'Law: what you know and what draws you',
           'intro': "Honest answers only. 'Not sure' is useful information for your mentor.",
           'items': [
               mcq('LW1', "Admission to the National Law Universities (NLUs) is mainly through which entrance exam?", 'LAW-KNOW', ['CLAT', 'JEE Main', 'NEET UG', 'NATA'], 'CLAT', P(PATH_LAW)),
               mcq('LW2', "After Class 12, a common undergraduate route into law is:", 'LAW-KNOW',
                   ['A 3-year B.Tech', 'A 5-year integrated law degree (for example BA LLB)', 'A 2-year diploma', 'A 1-year certificate'], 'A 5-year integrated law degree (for example BA LLB)', P(PATH_LAW)),
               lk('LW3', "I enjoy reading long passages and newspapers and working out what they mean.", 'LAW-READ', P(PATH_LAW)),
               lk('LW4', "I like to argue a point with reasons, and I listen when someone disagrees.", 'LAW-ARGUE', P(PATH_LAW)),
               lk('LW5', "I follow current affairs and what governments and courts decide.", 'LAW-AFFAIRS', P(PATH_LAW)),
               lk('LW6', "I am comfortable writing a lot, often with very precise wording.", 'LAW-WRITE', P(PATH_LAW)),
               put(R('LW7', "Rank these areas by your interest (top = most).", 'LAW-AREA',
                     ['Corporate and business law', 'Criminal law and courts', 'Constitutional law and public policy', 'Technology and intellectual property',
                      'Human rights and social justice', 'Judiciary or civil services']), P(PATH_LAW)),
               put(O('LW8', "What draws you to law?", 'LAW-WHY'), P(PATH_LAW)),
           ]}
    mgm = {'key': 'MG', 'title': 'Management and business: what you know and what draws you',
           'intro': "Honest answers only. 'Not sure' is useful information for your mentor.",
           'items': [
               mcq('MG1', "A five-year Integrated Programme in Management (IPM) offered by several IIMs is taken:", 'MGT-KNOW',
                   ['After Class 10', 'After Class 12', "After a bachelor's degree", 'After two years of work'], 'After Class 12', P(PATH_MGT)),
               lk('MG2', "I enjoy leading a team or organising an event.", 'MGT-LEAD', P(PATH_MGT)),
               lk('MG3', "I am comfortable with numbers: budgets, percentages, simple spreadsheets.", 'MGT-NUM', P(PATH_MGT)),
               lk('MG4', "I like the idea of starting something of my own, even if it might fail.", 'MGT-VENTURE', P(PATH_MGT)),
               lk('MG5', "I can explain my ideas clearly and persuade other people.", 'MGT-COMM', P(PATH_MGT)),
               put(R('MG6', "Rank these areas by your interest (top = most).", 'MGT-AREA',
                     ['Finance and investing', 'Marketing and brand building', 'Entrepreneurship and start-ups', 'Consulting and strategy', 'Operations and analytics', 'People and HR']), P(PATH_MGT)),
               put(O('MG7', "What draws you to business or management?", 'MGT-WHY'), P(PATH_MGT)),
           ]}
    oth = {'key': 'UD', 'title': 'Exploring your options',
           'intro': "It is fine not to know yet. This helps your mentor plan what to show you first.",
           'items': [
               fam('UD1', "How well could you explain what studying and working in these paths involve?",
                   ['Engineering', 'Medicine and health', 'Law', 'Management and business', 'Design and architecture'], 'PATH-AWARE', P(PATH_NONE)),
               put(R('UD2', "Rank these paths by how curious you are about them (top = most).", 'PATH-RANK',
                     ['Engineering', 'Medicine and health', 'Law', 'Management and business', 'Design, arts or architecture', 'Something else']), P(PATH_NONE)),
               put(O('UD3', "What is stopping you from deciding?", 'PATH-BLOCK'), P(PATH_NONE)),
               put(O('UD4', "Tell us what you have in mind: a course, a career, or a subject you love.", 'PATH-OTHER'), P(PATH_OTHER)),
               put(C('UD5', "How much have you looked into the entrance exams or portfolio needed for it?", 'PATH-READY',
                     ['A lot', 'Some', 'A little', 'Not yet']), P(PATH_OTHER)),
           ]}
    col = {'key': 'CY', 'title': 'Colleges and your options',
           'intro': "Choosing a college is a decision of its own. We would like to see where you are starting from.",
           'items': [
               put(C('CY1', "How much have you researched colleges and courses for your path?", 'COLLEGE-RESEARCH', ['A lot', 'Some', 'A little', 'Not yet']), W_SR),
               fam('CY2', "Rate your familiarity:", ['The entrance exam(s) for my path', 'How admission counselling and seat allotment work', 'What different colleges are known for',
                                                    'How to compare colleges: rankings, fees, placements', 'Scholarships and education loans'], 'COLLEGE-KNOW', W_SR),
               put(R('CY3', "When choosing a college, rank what matters most (top = most).", 'COLLEGE-FACTOR',
                     ['The course or branch I want', 'College reputation and ranking', 'Fees and scholarships', 'Location and distance from home',
                      'Placements and career outcomes', 'Campus life and friends']), W_SR),
               put(O('CY4', "Name up to three colleges or courses you like so far, and why.", 'COLLEGE-LIST', optional=True), W_SR),
               put(C('CY5', "Would you consider studying abroad?", 'CONSTR-ABROAD', ['Yes, actively', 'Maybe later', 'Only in India', 'Not sure']), W_SR),
               put(S('CY6', "A famous college offers a course that only half-interests you. A lesser-known college offers exactly the course you want. Which do you choose, and why?",
                     'SJT-COLLEGE', ['The famous college', 'The exact course at the lesser-known college', "Genuinely can't say"]), W_SR),
           ]}

    # ------------------------------------------------------------------ arrange the student instrument
    keep = {m['key']: m for m in STU}
    order = [m0, x1, x2, x3, x4, x5, x6, x7, keep['A'], keep['A2'], y1, keep['B'], b2, keep['C'], keep['D'], keep['E'], mdm, lwm, mgm, oth, col,
             keep['F'], keep['G'], keep['H'], keep['I']]
    STU[:] = order

    # ------------------------------------------------------------------ parent instrument
    pk = {m['key']: m for m in PAR}
    PW = {'P35': EXPLORE}                                                    # the parent's own answer to "your child's class"
    PSR = {'P35': SR}
    PENG = {'P35': SR, 'P36': PATH_ENG}
    PNOT = {'P35': SR, 'P36': NOT_ENG}
    p0 = {'key': '0', 'title': 'About your child',
          'intro': "Two quick questions so we ask you the right things.",
          'items': [
              C('P35', "Which class is your child in right now?", 'ACAD-CLASS', CLASSES),
              put(C('P36', "Which path do you currently have in mind for your child?", 'PATH-CHOICE', PATHS), {}),
          ]}
    p0['items'][1].pop('when')

    def gate_p(ids, when):
        gate(PAR, ids, when)

    gate_p({'P4', 'P5'}, PENG)
    p1 = pk['1']
    p1['items'] += [
        put(R('P37', "Rank your child's school subjects by real strength (top = strongest).", 'ALIGN-STRENGTH',
              ['Maths', 'Science', 'English', 'Social Science', 'Second language']), {'P35': EXPLORE}),
        lk('P38', "My child is genuinely confident in the subjects this path needs.", 'ALIGN-STRENGTH', PNOT),
        lk('P39', "My child has shown a clear interest in a particular career or field.", 'ALIGN-MOTIV', {'P35': EXPLORE}),
        lk('P40', "This path was mainly my child's own idea.", 'ALIGN-MOTIV', PNOT),
    ]
    gate_p({'P1'}, PENG)
    gate_p({'P8', 'P9'}, PENG)
    gate_p({'P12', 'P13', 'P14', 'P15', 'P16'}, PENG)                       # the admissions landscape quiz is engineering-specific
    pk['3']['title'] = 'The engineering admissions landscape: honest self-check'
    gate_p({'P17', 'P18', 'P19', 'P20', 'P21'}, PSR)
    for it in pk['4']['items']:
        if it['id'] == 'P17':
            it['text'] = "Total budget you can realistically commit for the whole course (fees + hostel + everything):"
    gate_p({'P22', 'P25'}, PSR)
    gate_p({'P23', 'P24'}, {'P35': ['Class 11', 'Class 12']})
    gate_p({'P27'}, PSR)
    px = {'key': 'PX', 'title': 'Stream and career: your view',
          'intro': "After Class 10 a child chooses a stream. Your view now helps us plan the next two years.",
          'items': [
              put(C('PX1', "Which stream do you currently prefer for your child after Class 10?", 'STREAM-PREF-P',
                    ['Science with Maths (PCM)', 'Science with Biology (PCB)', 'Science with both Maths and Biology', 'Commerce', 'Humanities or Arts',
                     'Open to whatever fits my child', "I haven't thought about it yet"]), PW),
              put(C('PX2', "How fixed is that?", 'ALIGN-STREAM-FIXED',
                    ['Must be this stream', 'Strong preference, open to discussion', 'Mild preference', "Fully my child's choice"]), PW),
              fam('PX3', "Rate your familiarity:", ['How streams after Class 10 link to entrance exams and careers', 'NEET, JEE, CLAT, CUET and other entrance exams',
                                                  'Career options beyond engineering and medicine', 'Which subject combinations keep options open'], 'PARENT-KNOW-STREAM', PW),
              mcq('PX4', "Quick check: which stream is usually needed to apply for MBBS through NEET?", 'PARENT-KNOW-QUIZ',
                  ['Science with Biology', 'Commerce', 'Humanities', 'Any stream'], 'Science with Biology', PW),
              mcq('PX5', "Which of these usually needs Mathematics in Class 12?", 'PARENT-KNOW-QUIZ',
                  ['Engineering entrance exams such as JEE Main', 'MBBS through NEET', 'Law through CLAT', 'None of them'], 'Engineering entrance exams such as JEE Main', PW),
              put(R('PX6', "What matters most to you when your child picks a stream? (top = most)", 'PARENT-STREAM-FACTOR',
                    ["My child's interest", "My child's marks and strengths", 'Career prospects', 'Keeping options open', "Our family's expectations", 'School and friends\' advice']), PW),
              lk('PX7', "My child's own interest should decide the stream, even if it is not what I would choose.", 'PARENT-FLEX-STREAM', PW),
              put(C('PX8', "Have you thought about what you can spend on your child's higher education?", 'PARENT-BUDGET-AWARE', ['Yes, clearly', 'Roughly', 'Not yet']), PW),
              put(O('PX9', "What would you most like to understand about streams and careers in the next year?", 'PARENT-KNOW-OPEN'), PW),
          ]}
    pc = {'key': 'PC', 'title': 'Your path and colleges: your view',
          'intro': "A few questions about the path you have in mind and how ready you feel for the admission process.",
          'items': [
              mcq('PC1', "Which entrance exam is mainly used for MBBS admission in India?", 'PARENT-KNOW-QUIZ', ['JEE Main', 'NEET UG', 'CLAT', 'CUET'], 'NEET UG', {'P35': SR, 'P36': PATH_MED}),
              mcq('PC2', "Which entrance exam is mainly used for admission to the National Law Universities?", 'PARENT-KNOW-QUIZ', ['CLAT', 'NEET UG', 'JEE Main', 'NATA'], 'CLAT', {'P35': SR, 'P36': PATH_LAW}),
              mcq('PC3', "The Integrated Programme in Management (IPM) offered by several IIMs is taken after:", 'PARENT-KNOW-QUIZ',
                  ['Class 10', 'Class 12', "A bachelor's degree", 'Two years of work'], 'Class 12', {'P35': SR, 'P36': PATH_MGT}),
              fam('PC4', "Rate your familiarity:", ['The entrance exam(s) for this path', 'Counselling and seat allotment for this path', 'Good colleges and how to compare them',
                                                  'Fees, scholarships and education loans', 'What the career looks like after the degree'], 'PARENT-KNOW-ADM', PNOT),
              put(C('PC5', "If the first-choice route does not work out, how open are you to a related course?", 'PARENT-RISK-PLANB',
                    ['Very open', 'Somewhat open', 'Prefer to repeat and retry', 'Not open']), PNOT),
              put(O('PC6', "Which part of the admission process for this path feels most confusing or worrying right now?", 'PARENT-KNOW-OPEN'), PNOT),
          ]}
    PAR[:] = [p0, p1, pk['2'], px, pk['3'], pc, pk['4'], pk['5'], pk['6'], pk['7']]
    # P7/P10/P11 and module 6/7 stay open to every family; the second module's engineering-only items were gated above
    p2 = pk['2']
    p2['items'].append(put(O('P41', "What would you like your child to explore before choosing a path?", 'ALIGN-CAREER', optional=True), {'P35': EXPLORE}))
