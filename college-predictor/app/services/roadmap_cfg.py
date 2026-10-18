"""Configuration for the interactive exam-roadmap pages (UCEED 2027, Law 2027).

One front-end engine (static/js/roadmap_engine.js) renders the roadmap, dashboard and weekly planner from a config
like these; the template embeds it as JSON. Add another exam by writing another config + a template.
Facts here were checked 17 Oct 2026 — keep dates in step with the official notices.
"""

LEVEL_WEIGHTS = {
    'beginner': [0.08, 0.26, 0.26, 0.16, 0.16, 0.08],
    'intermediate': [0.07, 0.20, 0.22, 0.20, 0.21, 0.10],
    'advanced': [0.05, 0.14, 0.18, 0.22, 0.30, 0.11],
}

UCEED = {
    'key': 'ea-uceed27-v1', 'examName': 'UCEED 2027', 'leadSource': 'uceed-roadmap', 'page': 'uceed-2027-roadmap',
    'targets': None, 'exam': '2027-01-17', 'examText': '17 Jan 2027', 'regClose': '2026-10-31',
    'regText': '31 Oct 2026', 'regNote': 'check uceed.iitb.ac.in for any late-fee window',
    'official': [['Registration closes', '2026-10-31', '31 Oct 2026'], ['UCEED 2027 exam', '2027-01-17', '17 Jan 2027 · 9 am–12 noon'],
                 ['Results', '2027-03-06', '6 Mar 2027'], ['B.Des application', '2027-03-15', '15 Mar 2027'], ['Admission rounds', '2027-04-21', 'From 21 Apr 2027']],
    'afterText': 'After the exam — results 6 Mar, B.Des application 15 Mar, admission rounds from 21 Apr 2027 (official)',
    'weights': LEVEL_WEIGHTS,
    'types': {'aptitude': 'Aptitude practice', 'drawing': 'Drawing exercise', 'pyq': 'Previous-year questions', 'revision': 'Revision',
              'mock': 'Mock test', 'error': 'Error-log review', 'off': 'School exam / holiday'},
    'mixes': {'beginner': [['aptitude', .34], ['drawing', .34], ['pyq', .08], ['revision', .12], ['error', .06], ['mock', .06]],
              'intermediate': [['aptitude', .26], ['drawing', .28], ['pyq', .14], ['revision', .12], ['error', .08], ['mock', .12]],
              'advanced': [['aptitude', .16], ['drawing', .22], ['pyq', .18], ['revision', .12], ['error', .10], ['mock', .22]]},
    'mock': {'a': {'label': 'Part A marks (/200)', 'max': 200}, 'b': {'label': 'Part B self-score (/100)', 'max': 100}},
    'log': {'name': 'Drawing', 'noun': 'drawing sessions'},
    'copy': {'roadTitle': 'Seven phases from first step to B.Des admission', 'topicTitle': 'Topic-wise aptitude progress', 'logPh': 'e.g. Perspective', 'beginner': 'New to design / drawing'},
    'sample': {
        'mocks': [{'ago': 21, 'a': 78, 'b': 52, 'acc': 61, 'unf': 6, 'weak': 'Spatial reasoning'}, {'ago': 14, 'a': 91, 'b': 55, 'acc': 66, 'unf': 4, 'weak': 'Spatial reasoning'},
                  {'ago': 7, 'a': 104, 'b': 61, 'acc': 72, 'unf': 3, 'weak': 'Patterns'}],
        'logs': [{'ago': 1, 'min': 40, 'subject': 'Object sketching'}, {'ago': 3, 'min': 35, 'subject': 'Perspective'}],
        'planner': [[0, 'aptitude', 'Spatial reasoning set', 60, True], [1, 'drawing', 'Perspective sketches', 45, False], [3, 'pyq', 'Previous-year paper section', 60, False], [5, 'mock', 'Sectional mock test', 90, False]],
        'feedback': 'SAMPLE: Good consistency on sketching. Prioritise spatial-reasoning practice this week and review your error log on Sunday.',
    },
    'phases': [
        {'id': 'p1', 't': 'Orientation and baseline assessment', 'd': 'Personalised UCEED readiness report', 'tasks': [
            'Read the UCEED 2027 brochure and understand the admission process', 'Check eligibility requirements in the official brochure',
            'Take a baseline aptitude check (observation, spatial, logical, creative, general awareness)', 'List strengths and improvement areas', 'Set a realistic weekly study target']},
        {'id': 'p2', 't': 'Build core design aptitude', 'd': 'Topic-wise progress dashboard and practice checklist', 'topic': True, 'tasks': [
            'Visual perception and observation', 'Spatial reasoning and visualisation', 'Patterns, shapes and transformations', 'Logical and analytical reasoning',
            'Everyday design awareness', 'Problem-solving and lateral thinking', 'Materials, objects and functionality basics', 'Creativity and interpreting visual information']},
        {'id': 'p3', 't': 'Develop drawing and visual communication', 'd': 'Weekly drawing portfolio and self-review checklist',
         'note': 'Practise according to the current official syllabus and question format — do not assume every earlier drawing task will appear in 2027.', 'tasks': [
            'Observation-based sketching', 'Perspective and proportion', 'Objects, environments and human figures', 'Composition and visual storytelling',
            'Light, shadow, form and spatial relationships', 'Communicating ideas through drawings', 'Timed drawing exercises']},
        {'id': 'p4', 't': 'Structured practice and problem solving', 'd': 'Accuracy dashboard, error log and improvement plan', 'tasks': [
            'Topic-wise questions', 'Timed practice sessions', 'Previous-year question papers', 'Error analysis', 'Track accuracy and time management', 'Revise weak concepts', 'Review recurring mistakes weekly']},
        {'id': 'p5', 't': 'Mock tests and exam readiness', 'd': 'Mock-test analysis report and final revision checklist', 'tasks': [
            'Untimed diagnostic practice where needed', 'Timed sectional tests', 'Full-length mock tests in the verified format', 'Analyse mistakes, not just marks',
            'Track speed, accuracy, question selection and unfinished questions', 'Revise weak areas with a personalised plan', 'Practise exam-day time management']},
        {'id': 'p6', 't': 'Final revision and examination', 'd': 'Final readiness report', 'rev': True, 'tasks': [
            'Revise high-priority concepts', 'Review frequently repeated error patterns', 'Practise under realistic time conditions',
            'Check admit-card instructions on the official site', 'Plan exam-day travel and logistics', 'Set a sleep, revision and confidence routine']},
        {'id': 'p7', 't': 'Results, counselling and B.Des admission', 'after': True, 'd': 'Institute comparison matrix and admission action tracker',
         'note': 'Exam registration, the separate B.Des application, and counselling / seat allocation are different steps.', 'tasks': [
            'Track the official result announcement (6 Mar 2027)', 'Understand rank and qualifying criteria', "Verify each institute's separate B.Des application requirements",
            'Submit applications within official deadlines (B.Des application: 15 Mar 2027)', 'Compare institutes: seats, eligibility, fees, curriculum, location, career fit',
            'Understand counselling and seat allocation (rounds from 21 Apr 2027)', 'Track documents, deadlines, offers and acceptance']},
    ],
}

# Law: CLAT (Consortium of NLUs), AILET (NLU Delhi), SLAT (Symbiosis) … The next-cycle target is a planning assumption only.
LAW = {
    'key': 'ea-law27-v1', 'examName': 'CLAT 2027', 'leadSource': 'law-roadmap', 'page': 'law-2027-roadmap',
    'targets': [
        {'id': 'clat27', 'label': 'CLAT 2027 — 6 Dec 2026 (announced)', 'date': '2026-12-06', 'official': True},
        {'id': 'ailet27', 'label': 'AILET 2027 — 13 Dec 2026 (announced)', 'date': '2026-12-13', 'official': True},
        {'id': 'slat27', 'label': 'SLAT 2027 — 19 / 26 Dec 2026 (reported)', 'date': '2026-12-19', 'official': True},
        {'id': 'next', 'label': 'Next cycle (CLAT 2028) — date not announced; planning assumption: first Sunday of Dec 2027', 'date': '2027-12-05', 'official': False},
    ],
    'exam': '2026-12-06', 'examText': '6 Dec 2026', 'regClose': '2026-10-31', 'regText': '31 Oct 2026', 'regNote': 'check consortiumofnlus.ac.in for any extension',
    'official': [['CLAT registration closes', '2026-10-31', '31 Oct 2026'], ['CLAT 2027 exam', '2026-12-06', '6 Dec 2026 · 2–4 pm'],
                 ['AILET 2027 exam', '2026-12-13', '13 Dec 2026 · 2–4 pm'], ['SLAT 2027 tests', '2026-12-19', '19 & 26 Dec 2026 (reported)'],
                 ['SLAT registration closes', '2026-12-04', '4 Dec 2026 (reported)']],
    'afterText': 'After the exam — results, merit lists and counselling dates are announced by each exam body (CLAT counselling schedule awaited)',
    'weights': LEVEL_WEIGHTS,
    'types': {'reading': 'Reading & comprehension', 'legal': 'Legal reasoning', 'logic': 'Logical reasoning & quant', 'current': 'Current affairs & GK',
              'pyq': 'Previous-year papers', 'revision': 'Revision', 'mock': 'Mock test', 'error': 'Error-log review', 'off': 'School exam / holiday'},
    'mixes': {'beginner': [['reading', .26], ['legal', .16], ['logic', .14], ['current', .16], ['pyq', .06], ['revision', .08], ['error', .06], ['mock', .08]],
              'intermediate': [['reading', .20], ['legal', .16], ['logic', .13], ['current', .13], ['pyq', .10], ['revision', .08], ['error', .08], ['mock', .12]],
              'advanced': [['reading', .12], ['legal', .14], ['logic', .12], ['current', .10], ['pyq', .14], ['revision', .08], ['error', .10], ['mock', .20]]},
    'mock': {'a': {'label': 'Score (/120)', 'max': 120}, 'b': None},
    'log': {'name': 'Reading', 'noun': 'reading sessions'},
    'copy': {'roadTitle': 'Seven phases from first step to law-school admission', 'topicTitle': 'Topic-wise skill progress', 'logPh': 'e.g. Editorial reading', 'beginner': 'New to law-entrance preparation'},
    'sample': {
        'mocks': [{'ago': 21, 'a': 62, 'acc': 58, 'unf': 12, 'weak': 'Legal reasoning'}, {'ago': 14, 'a': 71, 'acc': 63, 'unf': 9, 'weak': 'Legal reasoning'},
                  {'ago': 7, 'a': 80, 'acc': 69, 'unf': 6, 'weak': 'Quantitative'}],
        'logs': [{'ago': 1, 'min': 45, 'subject': 'Editorial reading'}, {'ago': 3, 'min': 30, 'subject': 'Legal passages'}],
        'planner': [[0, 'reading', 'Two RC passages + summary', 45, True], [1, 'legal', 'Legal reasoning set', 60, False], [3, 'current', 'Weekly current-affairs notes', 40, False], [5, 'mock', 'Sectional mock test', 90, False]],
        'feedback': 'SAMPLE: Reading stamina is improving. Spend this week on legal-reasoning principles and review your error log on Sunday.',
    },
    'phases': [
        {'id': 'p1', 't': 'Orientation and baseline assessment', 'd': 'Personalised law-entrance readiness report', 'tasks': [
            'Understand CLAT, AILET, SLAT and other law-entrance routes', 'Check each exam\'s eligibility (marks, qualifying year) in its official notice',
            'Take a baseline test across English, current affairs, legal, logical and quantitative areas', 'List strengths and gaps',
            'Choose your target exams and note every registration deadline', 'Set a realistic weekly study target']},
        {'id': 'p2', 't': 'Build the five core skill areas', 'd': 'Topic-wise progress dashboard and practice checklist', 'topic': True, 'tasks': [
            'English: reading comprehension and vocabulary in context', 'Current affairs and general knowledge — a daily habit', 'Legal reasoning: applying principles to facts',
            'Logical reasoning: arguments and critical reasoning', 'Quantitative techniques: data interpretation and basic maths', 'Reading speed and stamina on long passages',
            'Basic civics and legal awareness (Constitution, institutions)']},
        {'id': 'p3', 't': 'Build a reading and reasoning habit', 'd': 'Weekly reading log and self-review checklist',
         'note': 'Follow the current official pattern for each exam — CLAT, AILET and SLAT differ, and patterns can change between years.', 'tasks': [
            'Read a quality newspaper or editorial every day', 'Summarise passages in your own words', 'Learn vocabulary from what you read',
            'Practise long legal-style passages', 'Keep short notes on current affairs', 'Timed reading-comprehension sets']},
        {'id': 'p4', 't': 'Structured practice and problem solving', 'd': 'Accuracy dashboard, error log and improvement plan', 'tasks': [
            'Topic-wise question sets', 'Timed practice sessions', 'Previous-year papers (CLAT, AILET, SLAT)', 'Error analysis', 'Track accuracy and time per section',
            'Revise weak areas', 'Review recurring mistakes weekly']},
        {'id': 'p5', 't': 'Mock tests and exam readiness', 'd': 'Mock-test analysis report and final revision checklist', 'tasks': [
            'Untimed diagnostic practice where needed', 'Timed sectional tests', 'Full-length mocks in each exam\'s verified format (including OMR practice for CLAT)',
            'Analyse mistakes, not just marks', 'Practise question selection and skipping', 'Track speed, accuracy and unfinished questions', 'Revise weak areas with a personalised plan']},
        {'id': 'p6', 't': 'Final revision and examinations', 'd': 'Final readiness report', 'rev': True, 'tasks': [
            'Revise high-priority concepts and notes', 'Review repeated error patterns', 'Practise under realistic time conditions',
            'Check admit-card and exam-day rules for each exam on its official site', 'Plan travel and logistics for each exam date', 'Set a sleep, revision and confidence routine']},
        {'id': 'p7', 't': 'Results, counselling and law-school admission', 'after': True, 'd': 'Law-school comparison matrix and admission action tracker',
         'note': 'Taking the exam, qualifying, getting a rank, counselling and receiving a seat offer are separate steps.', 'tasks': [
            'Track official result announcements', 'Understand rank, merit lists and cut-offs', 'Learn each university\'s separate application and counselling steps',
            'Prepare documents (marksheets, category and domicile certificates) before deadlines', 'Compare law schools: fees, curriculum, location, facilities, outcomes',
            'Understand counselling, seat allocation and fee-payment deadlines', 'Track offers and acceptances']},
    ],
}

# IPM: five-year Integrated Programme in Management at IIMs — IPMAT Indore, IPMAT Rohtak, JIPMAT (NTA).
# No official 2027 dates exist yet: every target below is a planning assumption based on the 2026 cycle (IIM Indore held IPMAT on 4 May 2026).
IPM = {
    'key': 'ea-ipm27-v1', 'examName': 'IPMAT 2027', 'leadSource': 'ipm-roadmap', 'page': 'ipm-2027-roadmap',
    'targets': [
        {'id': 'indore27', 'label': 'IPMAT Indore 2027 — planning assumption: early May 2027 (not announced)', 'date': '2027-05-03', 'official': False},
        {'id': 'rohtak27', 'label': 'IPMAT Rohtak 2027 — planning assumption: mid May 2027 (not announced)', 'date': '2027-05-10', 'official': False},
        {'id': 'jipmat27', 'label': 'JIPMAT 2027 — planning assumption: April–June 2027 (not announced)', 'date': '2027-05-01', 'official': False},
        {'id': 'next', 'label': 'Next cycle (2028) — planning assumption: early May 2028', 'date': '2028-05-01', 'official': False},
    ],
    'exam': '2027-05-03', 'examText': 'early May 2027 (assumed)', 'regClose': '2027-03-16', 'regText': 'mid-March 2027 (assumed from the 2026 cycle)',
    'regNote': 'official 2027 dates are not announced yet — watch iimidr.ac.in/ipm and exams.nta.nic.in/jipmat',
    'official': [['IPMAT 2026 held at IIM Indore (last cycle)', '2026-05-04', '4 May 2026 · 120 min'], ['IPMAT 2026 application window closed (last cycle)', '2026-03-17', '17 Mar 2026']],
    'afterText': 'After the exam — results, shortlists, WAT / personal interview and offers are announced by each IIM (2027 dates awaited)',
    'weights': LEVEL_WEIGHTS,
    'types': {'quant': 'Quantitative ability', 'verbal': 'Verbal ability & reading', 'lrdi': 'Logical reasoning & data interpretation', 'current': 'Business awareness & GK',
              'wat': 'Writing ability & interview practice', 'pyq': 'Previous-year papers', 'revision': 'Revision', 'mock': 'Mock test', 'error': 'Error-log review', 'off': 'School exam / holiday'},
    'mixes': {'beginner': [['quant', .24], ['verbal', .22], ['lrdi', .10], ['current', .06], ['wat', .06], ['pyq', .06], ['revision', .08], ['error', .08], ['mock', .10]],
              'intermediate': [['quant', .20], ['verbal', .18], ['lrdi', .10], ['current', .05], ['wat', .06], ['pyq', .10], ['revision', .08], ['error', .08], ['mock', .15]],
              'advanced': [['quant', .14], ['verbal', .14], ['lrdi', .10], ['current', .04], ['wat', .08], ['pyq', .14], ['revision', .07], ['error', .10], ['mock', .19]]},
    'mock': {'a': {'label': 'Score (%)', 'max': 100}, 'b': None},
    'log': {'name': 'Practice', 'noun': 'practice sessions'},
    'copy': {'roadTitle': 'Seven phases from first step to IIM admission', 'topicTitle': 'Topic-wise skill progress', 'logPh': 'e.g. Reading comprehension set', 'beginner': 'New to IPM preparation'},
    'sample': {
        'mocks': [{'ago': 21, 'a': 38, 'acc': 55, 'unf': 14, 'weak': 'Quantitative ability'}, {'ago': 14, 'a': 46, 'acc': 61, 'unf': 10, 'weak': 'Quantitative ability'},
                  {'ago': 7, 'a': 55, 'acc': 67, 'unf': 7, 'weak': 'Verbal ability'}],
        'logs': [{'ago': 1, 'min': 50, 'subject': 'Arithmetic'}, {'ago': 3, 'min': 35, 'subject': 'Reading comprehension'}],
        'planner': [[0, 'quant', 'Percentages and ratio set', 50, True], [1, 'verbal', 'Reading comprehension: 2 passages', 40, False], [3, 'lrdi', 'Data interpretation set', 45, False], [5, 'mock', 'Sectional mock test', 90, False]],
        'feedback': 'SAMPLE: Quant accuracy is improving. Spend this week on verbal reading speed and review your error log on Sunday.',
    },
    'phases': [
        {'id': 'p1', 't': 'Orientation and baseline assessment', 'd': 'Personalised IPM readiness report', 'tasks': [
            'Understand what the five-year IPM is and how it differs from a BBA or a 3-year degree', 'Learn the three exams: IPMAT Indore, IPMAT Rohtak and JIPMAT',
            "Check each IIM's eligibility (age, Class 10 / 12 marks, qualifying year) in its own notice", 'Take a baseline test in quantitative and verbal ability',
            'Decide your target IIMs and note every registration deadline', 'Set a realistic weekly study target']},
        {'id': 'p2', 't': 'Build the core skill areas', 'd': 'Topic-wise progress dashboard and practice checklist', 'topic': True, 'tasks': [
            'Quantitative: arithmetic, algebra, number systems, geometry, mensuration', 'Quantitative: permutation-combination, probability, data handling',
            'Verbal: reading comprehension, para-jumbles, sentence correction, vocabulary', 'Logical reasoning and data interpretation (where the exam tests it)',
            'Reading speed and stamina on long passages', 'Basic business awareness and current affairs for the interview round']},
        {'id': 'p3', 't': 'Build a reading and numeracy habit', 'd': 'Weekly reading log and self-review checklist',
         'note': 'Patterns differ — IPMAT Indore, IPMAT Rohtak and JIPMAT are not identical. Always follow the current official pattern for each.', 'tasks': [
            'Read an editorial or long-form article every day', 'Summarise what you read in your own words', 'Daily mental-maths and speed practice',
            'Maintain a formula and vocabulary notebook', 'Timed reading-comprehension sets', 'Revisit Class 9–12 maths foundations']},
        {'id': 'p4', 't': 'Structured practice and problem solving', 'd': 'Accuracy dashboard, error log and improvement plan', 'tasks': [
            'Topic-wise question sets', 'Timed sectional practice', 'Previous-year papers of IPMAT and JIPMAT', 'Error analysis', 'Track accuracy and time per section',
            'Learn question selection (including short-answer / non-MCQ items where the exam has them)', 'Review recurring mistakes weekly']},
        {'id': 'p5', 't': 'Mock tests and exam readiness', 'd': 'Mock-test analysis report and final revision checklist', 'tasks': [
            'Timed sectional tests', "Full-length mocks in each exam's verified format", 'Analyse mistakes, not just marks', 'Practise skipping and negative-marking strategy',
            'Track speed, accuracy and unattempted questions', 'Revise weak areas with a personalised plan']},
        {'id': 'p6', 't': 'Final revision and examinations', 'd': 'Final readiness report', 'rev': True, 'tasks': [
            'Revise high-priority concepts and notes', 'Review repeated error patterns', 'Practise under realistic time conditions',
            'Check admit-card and exam-day rules on the official site', 'Plan travel and logistics for the test centre', 'Set a sleep, revision and confidence routine']},
        {'id': 'p7', 't': 'Results, WAT / interview and IIM admission', 'after': True, 'd': 'IIM comparison matrix and admission action tracker',
         'note': 'Taking the exam, being shortlisted, the WAT / personal interview, the final merit list and accepting a seat are separate steps.', 'tasks': [
            'Track the official result and shortlist announcements', 'Prepare for the written ability test (WAT) and personal interview', 'Prepare documents (marksheets, category and PwD certificates) before deadlines',
            "Understand each IIM's weightage of exam score, school marks, WAT and interview", 'Compare IIMs: fees, location, curriculum, exit options, outcomes',
            'Understand fee payment and seat-acceptance deadlines', 'Track offers and acceptances']},
    ],
}
