"""Ready-made add-on programmes for the Mentorship Portal.

Each add-on becomes a normal `MsProgramme` (tier = 'Add-on') with its own session templates, so enrolling a student,
tracking sessions/actions/KPIs, reports and parent visibility all work exactly as for the base programme. Admins can edit
every session afterwards (Admin → Mentorship → Programmes).

Content rules: sessions describe WHAT to do and WHERE to verify. They never state dates, fees, cut-offs, seat counts or
rules as facts — those change every year and must be read from the official notice for the current cycle.
"""

TIER = 'Add-on'

ADDONS = [
    {
        'key': 'uceed', 'icon': '✏️', 'title': 'UCEED (B.Des at IITs)', 'weeks': 12,
        'audience': 'Class 11–12 and drop-year students aiming for B.Des through UCEED.',
        'blurb': 'Design aptitude, drawing and visualisation practice, mock-test analysis and B.Des institute selection.',
        'verify': 'UCEED dates, pattern and participating institutes: uceed.iitb.ac.in (current year).',
        'sessions': [
            ('Orientation, eligibility and baseline', 'UCEED and the B.Des institutes that use it\nEligibility and attempt rules from the current brochure\nBaseline sketch and aptitude check\nWeekly time plan around school', 'Readiness note and 12-week plan'),
            ('Design aptitude: visualisation and reasoning', 'Spatial and visual reasoning\nDesign thinking and problem framing\nObservation and general awareness of design\nBuilding a daily sketch habit', 'Practice set and sketch log'),
            ('Drawing and sketching fundamentals', 'Perspective, proportion and shading\nObject, memory and imagination drawing\nColour basics\nTimed sketching drills', 'Sketchbook review checklist'),
            ('Numerical, logical and language sections', 'Reasoning and basic quantitative practice\nLanguage and comprehension for design\nQuestion types in the current pattern (read the brochure)\nError-log method', 'Topic-wise accuracy tracker'),
            ('Mock tests and time management', 'Full-length mock in the current format\nSection-wise time split\nMistake analysis and re-attempt\nScore-trend review', 'Mock analysis report'),
            ('Final revision and exam-day plan', 'Revision priorities from the error log\nAdmit card, centre and exam-day rules\nSleep and confidence routine', 'Final readiness checklist'),
            ('Results, B.Des application and institute comparison', 'Result and rank vs the separate B.Des application\nInstitute comparison: curriculum, location, fees, outcomes\nDocuments and deadlines\nCounselling steps from the official notice', 'Institute comparison matrix'),
            ('Parent briefing and decision review', 'Timeline, costs and risks for the family\nBackup options (NID, NIFT, universities)\nDecision checklist', 'Parent summary note'),
        ],
    },
    {
        'key': 'nid', 'icon': '🎨', 'title': 'NID DAT (B.Des / M.Des)', 'weeks': 10,
        'audience': 'Students targeting the National Institute of Design through the Design Aptitude Test.',
        'blurb': 'Prelims practice, studio-test and portfolio-style preparation, interview readiness and NID application planning.',
        'verify': 'NID admission notice, handbook and dates for the current year (admissions.nid.edu).',
        'sessions': [
            ('Orientation and programme choice', 'NID programmes and campuses\nB.Des vs other design routes\nEligibility from the current handbook\nPersonal creative baseline', 'Goal note and plan'),
            ('Prelims: aptitude and reasoning practice', 'Visual, logical and comprehension questions\nDesign awareness and observation\nTimed practice sets and error log', 'Prelims practice tracker'),
            ('Drawing, colour and 2D/3D composition', 'Sketching from observation and imagination\nColour harmony and composition\nSimple 3D model-making materials and ideas', 'Weekly studio-task log'),
            ('Mains: studio test strategy', 'Typical studio-test task types (confirm in the handbook)\nIdea generation under time pressure\nPresentation of ideas', 'Two timed studio tasks reviewed'),
            ('Portfolio and interview readiness', 'Choosing and presenting work\nExplaining your process\nMock interview and feedback', 'Portfolio checklist and interview notes'),
            ('Application, documents and deadlines', 'Registration, fee and document checklist\nDeadline calendar\nFinal-year school balance', 'Application tracker'),
            ('Results, counselling and backup plan', 'Result stages and offers\nComparison with UCEED / NIFT / university options\nDecision checklist for the family', 'Decision brief'),
        ],
    },
    {
        'key': 'nift', 'icon': '🧵', 'title': 'NIFT (B.Des / B.FTech)', 'weeks': 10,
        'audience': 'Students targeting NIFT design (B.Des) or fashion technology (B.FTech) programmes.',
        'blurb': 'General and creative ability preparation, situation test, and NIFT campus and programme selection.',
        'verify': 'NIFT bulletin of information and dates for the current year (nift.ac.in).',
        'sessions': [
            ('Orientation and programme fit', 'B.Des vs B.FTech\nEligibility and test components from the current bulletin\nCampus overview\nBaseline assessment', 'Programme-fit note'),
            ('General ability: quant, reasoning, English, GK', 'Quantitative and analytical ability\nCommunication and English comprehension\nCurrent and general awareness\nTimed practice and error log', 'Section-wise tracker'),
            ('Creative ability: drawing and design thinking', 'Sketching, colour and composition\nStory/idea-based design prompts\nDaily creative practice', 'Creative practice log'),
            ('Situation test and model-making', 'What the situation test assesses (confirm in the bulletin)\nMaterials, planning and time\nPractice builds and critique', 'Two practice builds reviewed'),
            ('Mock tests and exam-day plan', 'Written and creative mocks\nTime allocation\nAdmit card and rules', 'Mock report and checklist'),
            ('Application, results and counselling', 'Application and fee steps\nResult stages and counselling\nCampus and branch preference list', 'Preference matrix'),
            ('Backup options and family briefing', 'Design and fashion alternatives\nCosts and timelines\nDecision checklist', 'Parent summary note'),
        ],
    },
    {
        'key': 'iitd-ad', 'icon': '🌍', 'title': 'IIT Delhi – Abu Dhabi admission', 'weeks': 8,
        'audience': 'Students (including NRI / Gulf-based) considering the IIT Delhi – Abu Dhabi campus.',
        'blurb': 'Understanding the campus and admission route, eligibility checks, documents, budget and comparison with other options.',
        'verify': 'The admission route, eligibility, fees, visa and residence rules change — confirm every item on the official IIT Delhi – Abu Dhabi website and notices.',
        'sessions': [
            ('Orientation: what the campus offers', 'Programmes available and how they differ from the Delhi campus\nWho the programme is aimed at\nStudent profile and goals', 'Fit note'),
            ('Admission route and eligibility', 'Current admission route(s) from the official notice\nEligibility, age, subject and qualification rules\nDeadlines and what is still unannounced', 'Eligibility and deadline checklist'),
            ('Preparing for the entrance route', 'Study plan for the exam the route depends on\nMock tests and error analysis\nTime plan with school boards', 'Prep tracker'),
            ('Documents, application and fees', 'Passport / residence / transcript documents\nApplication and fee steps\nBudget planning including living costs', 'Document and budget sheet'),
            ('Comparison with other options', 'Compare with IITs in India, DASA/CIWG and other international options\nCosts, outcomes, mobility\nRisk and backup list', 'Comparison matrix'),
            ('Offer, acceptance and family decision', 'Reading an offer and acceptance deadlines\nVisa and relocation checklist\nDecision review', 'Decision brief'),
        ],
    },
    {
        'key': 'tnea', 'icon': '🎓', 'title': 'TNEA (Tamil Nadu engineering counselling)', 'weeks': 10,
        'audience': 'Tamil Nadu and nearby students preparing for TNEA counselling after Class 12.',
        'blurb': 'Rank-list understanding, document readiness, college and branch shortlisting, choice-filling and round strategy.',
        'verify': 'TNEA schedule, rules, reservations and seat matrix: tneaonline.org and the DoTE notices for the current year.',
        'sessions': [
            ('Orientation: how TNEA works', 'Eligibility and registration steps\nRank-list basis and tie-breaking from the current notice\nCategories and reservations that may apply\nTimeline of the process', 'Process map and checklist'),
            ('Documents and certificates', 'Community, income, nativity and other certificates\nSpecial-reservation proofs, if applicable\nVerification and upload steps', 'Document checklist'),
            ('Know your rank and cut-offs', 'Calculating the cut-off from the published rule\nUsing past-year data carefully (trends, not promises)\nSafe, match and reach categories', 'Rank-band note'),
            ('Branch fit and career mapping', 'Interest, aptitude and job-market view\nBranch vs college trade-off\nRelocation and budget', 'Branch-priority list'),
            ('College research and shortlist', 'Accreditation, placements data (verify source)\nLocation, hostel, fees and scholarships\nBuilding the shortlist', 'College comparison matrix'),
            ('Choice filling strategy', 'Ordering choices across rounds\nCommon mistakes and how to avoid them\nTrial choice list', 'Draft choice list'),
            ('Rounds, allotment and decisions', 'Allotment, acceptance, upgrade/freeze rules from the notice\nFee payment and reporting deadlines\nWhat to do if the allotment is unsatisfactory', 'Round-by-round action plan'),
            ('Parent briefing and final review', 'Cost and timeline summary\nBackup plans (other states, private universities)\nFinal decision checklist', 'Parent summary note'),
        ],
    },
    {
        'key': 'state', 'icon': '🗺️', 'title': 'State-specific college admission', 'weeks': 10,
        'audience': 'Families applying through a state entrance test or state counselling (for example KCET, MHT CET, KEAM, EAPCET, WBJEE and others).',
        'blurb': 'A reusable framework: domicile and quota rules, state exam and counselling steps, documents, college shortlist and choice filling.',
        'verify': 'Every state has its own rules and dates — use the state authority\'s notice for the current year.',
        'sessions': [
            ('Choose your state route', 'States and exams you are eligible for\nDomicile, residence and quota rules\nHow state and national routes overlap', 'State-route shortlist'),
            ('Understand the state process', 'Registration, entrance exam, rank list, counselling\nRelevant authority and official portal\nDeadline calendar', 'Process timeline'),
            ('Exam preparation plan', 'State exam pattern and syllabus (current notice)\nStudy plan and mock tests\nBoard-marks interaction with the rank', 'Study tracker'),
            ('Documents and certificates', 'Domicile, category, income and other certificates\nValidity dates and attestation\nUploads and originals', 'Document checklist'),
            ('College and branch shortlist', 'Government and private colleges in the state\nFees, hostel, location and scholarships\nSafe, match and reach lists', 'Comparison matrix'),
            ('Choice filling and rounds', 'Ordering choices; round-wise strategy\nFreeze/float/upgrade rules from the notice\nFee payment and reporting', 'Draft choice list'),
            ('Backups and family decision', 'Out-of-state, private-university and management/NRI-quota options\nCosts and risks\nDecision checklist', 'Decision brief'),
        ],
    },
    {
        'key': 'srm', 'icon': '🏛️', 'title': 'SRM admission (SRMJEEE)', 'weeks': 6,
        'audience': 'Students considering SRM Institute of Science and Technology.',
        'blurb': 'Exam and slot planning, campus and branch choice, scholarships and counselling steps.',
        'verify': 'SRMJEEE schedule, slots, fees, scholarships and counselling: srmist.edu.in / the official admissions notice.',
        'sessions': [
            ('Orientation and fit', 'SRM campuses and programmes\nCompare with other options in your list\nEligibility and test format from the current notice', 'Fit note'),
            ('SRMJEEE preparation', 'Syllabus and section plan\nMock tests and error log\nSlot and phase planning', 'Prep tracker'),
            ('Application and documents', 'Registration, fee and document checklist\nDeadline calendar', 'Application tracker'),
            ('Branch, campus and scholarships', 'Branch fit and campus comparison\nScholarship routes (verify each condition)\nBudget planning', 'Preference matrix'),
            ('Counselling and seat decision', 'Rank-based counselling steps\nFee and reporting deadlines\nBackup plan', 'Decision brief'),
            ('Parent briefing', 'Costs, timeline, risks\nFinal checklist', 'Parent summary note'),
        ],
    },
    {
        'key': 'amrita', 'icon': '🪷', 'title': 'Amrita admission (AEEE)', 'weeks': 6,
        'audience': 'Students considering Amrita Vishwa Vidyapeetham.',
        'blurb': 'AEEE preparation, campus and programme choice, scholarship awareness and counselling steps.',
        'verify': 'AEEE schedule, phases, fees, scholarships and counselling: amrita.edu admissions notice for the current year.',
        'sessions': [
            ('Orientation and fit', 'Amrita campuses and programmes\nCompare with other options\nEligibility and test details from the current notice', 'Fit note'),
            ('AEEE preparation', 'Syllabus and section plan\nMocks and error analysis\nPhase planning', 'Prep tracker'),
            ('Application and documents', 'Registration, fee and documents\nDeadline calendar', 'Application tracker'),
            ('Campus, branch and scholarships', 'Branch and campus comparison\nScholarship conditions (verify)\nBudget planning', 'Preference matrix'),
            ('Counselling and seat decision', 'Counselling steps\nFee and reporting deadlines\nBackup plan', 'Decision brief'),
            ('Parent briefing', 'Costs, timeline, risks\nFinal checklist', 'Parent summary note'),
        ],
    },
    {
        'key': 'vit', 'icon': '🏫', 'title': 'VIT admission (VITEEE)', 'weeks': 6,
        'audience': 'Students considering Vellore Institute of Technology and its campuses.',
        'blurb': 'VITEEE preparation, slot choice, campus and branch selection, and counselling steps.',
        'verify': 'VITEEE schedule, slots, fees, counselling and scholarships: viteee.vit.ac.in / vit.ac.in for the current year.',
        'sessions': [
            ('Orientation and fit', 'VIT campuses and programmes\nCompare with other options\nEligibility and test format from the current notice', 'Fit note'),
            ('VITEEE preparation', 'Syllabus and section plan\nMocks and error log\nSlot planning', 'Prep tracker'),
            ('Application and documents', 'Registration, fee and documents\nDeadline calendar', 'Application tracker'),
            ('Campus, branch and scholarships', 'Branch and campus comparison\nScholarship conditions (verify)\nBudget planning', 'Preference matrix'),
            ('Counselling and seat decision', 'Rank-based counselling steps\nCategory-wise choice and fee deadlines\nBackup plan', 'Decision brief'),
            ('Parent briefing', 'Costs, timeline, risks\nFinal checklist', 'Parent summary note'),
        ],
    },
]


def by_name():
    """Programme name used in the database → add-on definition."""
    return {a['title']: a for a in ADDONS}
