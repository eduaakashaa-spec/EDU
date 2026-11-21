"""MHT CET (PCM) and Maharashtra engineering admissions (CAP): facts behind /mht-cet-analytics, checked 21 Nov 2026.

Every fact names its source and whether it is official (State CET Cell, CAP portal, MSBSHSE, NIRF) or reported (news and coaching sites).
Cut-offs are in app/data/mhtcet/cutoffs.json, built by tools/mhtcet/build_cutoffs.py from the official CAP Round I lists.
Update this file when the CET Cell publishes the 2027 brochure, the CAP 2027 schedule or new cut-offs.
"""

VERIFIED = '21 Nov 2026'
O, R, E = 'Official', 'Reported', 'Expected'

SRC = {
    'cet_2027': 'https://cetcell.mahacet.org/wp-content/uploads/2026/11/DATES-OF-COMMENCEMENT-OF-MAHA-CET-2027-16-NOV-2026.pdf',
    'brochure': 'https://cetcell.mahacet.org/wp-content/uploads/2023/12/MHT-CET-2026-Information-Brochure-Updated-on-10.02.2026.pdf',
    'fe_brochure': 'https://fe2026.mahacet.org/PublicPages/Information_Brochure_UG_PG_2026_27_dt_2_7_2026_DHG_1_Display.pdf',
    'cap_notice': 'https://cetcell.mahacet.org/wp-content/uploads/2026/07/BE-BTECH-CAP-AY-26-27-Schedule-Notice-No.1-Upto-Merit-List.pdf',
    'method': 'https://cetcell.mahacet.org/wp-content/uploads/2023/12/MHT-CET-2026-Result-Processing-Methodology.pdf',
    'hsc': 'https://news.careers360.com/maharashtra-hsc-timetable-2027-out-exams-from-february-8-check-subject-wise-class-12-exam-dates',
    'cap1_2025': 'https://fe2026.mahacet.org/2025/2025ENGG_CAP1_CutOff.pdf',
    'cap1_2024': 'https://fe2025.mahacet.org/2024/2024ENGG_CAP1_CutOff.pdf',
    'cap1_2023': 'https://fe2025.mahacet.org/2023/2023ENGG_CAP1_CutOff.pdf',
    'nirf': 'https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html',
    'marks': 'https://engineering.careers360.com/articles/mht-cet-marks-vs-rank',
}

# key dates for the 2027 cycle: (id, title, start, end, status, detail)
DATES = [
    ('hsc-prac', 'Maharashtra HSC (Class 12) practicals, orals and internals', '2027-01-20', '2027-02-06', R, 'Board timetable released 7 Nov 2026 (reported); schools fix the exact day.'),
    ('hsc-theory', 'Maharashtra HSC (Class 12) theory exams', '2027-02-08', '2027-03-11', R,
     'Start 8 Feb 2027 (reported). The end date differs between reports (9 or 11 Mar). Physics 12 Feb, Chemistry 16 Feb, Mathematics & Statistics 20 Feb (reported). Confirm on mahahsscboard.in.'),
    ('cet-pcm-1', 'MHT CET 2027 PCM, attempt 1 (compulsory)', '2027-04-16', '2027-04-26', O, 'CET Cell press release of 16 Nov 2026; the dates are marked tentative.'),
    ('cet-pcm-2', 'MHT CET 2027 PCM, attempt 2 (optional)', '2027-05-10', '2027-05-15', O, 'The better total percentile of the two attempts counts (same press release).'),
    ('hsc-result', 'Maharashtra HSC result', '2027-05-01', '2027-05-10', E, 'Early May in recent years (2 May 2026, 5 May 2025).'),
    ('cet-result', 'MHT CET 2027 result', '2027-06-10', '2027-06-25', E, 'In 2026: 15 Jun (attempt 1) and 18 Jun (attempt 2).'),
    ('cap-reg', 'CAP registration, document verification and merit lists', '2027-07-01', '2027-07-28', E,
     'In 2026: registration 2–19 Jul (extended), provisional merit list 22 Jul, final merit list 27 Jul.'),
    ('cap-1', 'CAP Round I option form and allotment', '2027-07-28', '2027-08-05', E, 'In 2026: options 28–30 Jul, allotment 2 Aug, reporting 3–5 Aug.'),
    ('cap-2', 'CAP Round II', '2027-08-07', '2027-08-17', E, 'In 2026: options 7–9 Aug, allotment 13 Aug, reporting to 16/17 Aug.'),
    ('cap-3', 'CAP Round III', '2027-08-20', '2027-08-28', E, 'In 2026: options 20–22 Aug, allotment 24 Aug, reporting 25–28 Aug.'),
    ('cap-4', 'CAP Round IV, then institute-level admissions', '2027-08-30', '2027-09-15', E, 'In 2026: Round IV allotment 3 Sep; institute level 8–15 Sep; admissions closed 15 Sep.'),
]

PATTERN = [
    ('Questions', '150 multiple-choice questions, 4 options each: Physics 50, Chemistry 50, Mathematics 50'),
    ('Marks', 'Physics and Chemistry 1 mark a question, Mathematics 2 marks: 200 marks in all'),
    ('Time', '3 hours in two blocks: Physics and Chemistry in the first 90 minutes (auto-submitted), Mathematics in the next 90'),
    ('Negative marking', 'None: answer every question'),
    ('Syllabus', 'Maharashtra State Board Class 11 and 12; about 20% Class 11 and 80% Class 12 (reported)'),
    ('Mode and language', 'Computer-based, centres in Maharashtra only; English, Marathi or Urdu'),
    ('Percentile', 'Worked out per session: 100 × candidates in your session with a raw score at or below yours ÷ candidates who appeared in that session, to 7 decimals'),
    ('Two attempts (from 2027)', 'Attempt 1 is compulsory, attempt 2 optional; the better total percentile counts, not the better subject percentiles'),
]

CANDIDATES = [  # (year, registered, appeared, note)
    (2024, 410377, 379800, 'PCM group'),
    (2025, 464263, 422663, 'PCM group; 22 at 100 percentile'),
    (2026, 479332, 454069, 'PCM attempt 1 (attempt 2: 2,85,121 appeared)'),
]

ELIGIBILITY = [
    ('Subjects', 'Pass Class 12 with Physics and Mathematics compulsory, plus Chemistry or one of Biotechnology, Biology, a technical vocational subject, Computer Science, IT, Informatics Practices, Agriculture, Engineering Graphics, Business Studies, Electronics or Entrepreneurship.'),
    ('Minimum marks', 'At least 45% in those three subjects taken together (Open); 40% for reserved categories, EWS and PwD candidates of Maharashtra. 44.50 to 44.99 rounds to 45.'),
    ('MHT CET score', 'Appear in all PCM papers of MHT CET with a non-zero score. MHT CET is compulsory for Maharashtra State and minority candidates.'),
    ('All India candidates', 'Need a non-zero JEE Main or MHT CET PCM score; JEE Main is preferred for the All India quota (15% of seats in private colleges).'),
    ('Merit', 'CAP merit is on the MHT CET percentile. Class 12 marks only decide eligibility and break ties (CET Maths, Physics, Chemistry, then board PCM, Maths, Physics, aggregate).'),
    ('Age', 'No age limit.'),
    ('PCB students', 'With Physics and Chemistry plus Biology and the PCB group score, only nine courses are open: Agriculture, Biotechnology, Food, Leather, Packaging, Pharmaceutical, Printing, Fashion Technology and Textile Chemistry.'),
]

CANDIDATURE = [
    ('Type A', 'Passed SSC and HSC (or equivalent) from Maharashtra, or domiciled in or born in Maharashtra.'),
    ('Type B', 'Not Type A, but a parent is domiciled in Maharashtra (with certificate).'),
    ('Type C', 'Parent is an employee of the Government of India or its undertaking, posted in Maharashtra.'),
    ('Type D', 'Parent is an employee or retired employee of the Government of Maharashtra or its undertaking.'),
    ('Type E', 'Maharashtra–Karnataka border area candidates (listed villages), with the linguistic minority rules.'),
    ('All India', 'Indian nationals not claiming Maharashtra candidature: All India seats only, on JEE Main (preferred) or MHT CET.'),
]

SEATS = [
    ('Government and aided, non-autonomous', '70% Home University (HU) candidates, 30% Other than HU'),
    ('Government and aided, autonomous', '100% State Level'),
    ('Private unaided, non-autonomous', '45.5% HU, 19.5% Other than HU, 15% All India, 20% institute quota (includes 5% NRI)'),
    ('Private unaided, autonomous', '65% State Level, 15% All India, 20% institute quota'),
    ('Minority institutions', 'At least 51% of seats for the minority community through CAP (the MI column)'),
    ('TFWS', 'Tuition Fee Waiver Scheme: up to 5% extra seats, family income under ₹8 lakh, Maharashtra candidates only'),
]

RESERVATION = [('SC', 13), ('ST', 7), ('VJ/DT (NT-A)', 3), ('NT-B', 2.5), ('NT-C', 3.5), ('NT-D', 2), ('OBC', 19), ('SEBC', 10), ('Open', 40)]
RESERVATION_NOTE = 'Of Maharashtra State CAP seats (FE brochure 2026-27). EWS 10% is over and above the intake; women 30% within each category; PwD 5%; Defence 5%; Orphan 1%; TFWS up to 5% supernumerary. SEBC is subject to the High Court decision.'

STATS_2026 = [
    ('Engineering seats in the Round I matrix', '2,16,552 in 380 colleges (reported)'),
    ('Admitted at the end of CAP', '1,81,927 in 387 colleges; 29,042 seats vacant (reported)'),
]

# reported marks -> percentile estimate (Careers360, for 2026); the CET Cell does not publish such a table
MARKS_PCT = [(200, 100.0), (160, 99.56), (149, 99.0), (135, 98.0), (120, 96.0), (100, 92.0), (75, 82.0), (60, 70.0), (45, 50.0), (30, 25.0), (0, 0.0)]

# NIRF India Rankings 2025, Engineering (app/data/files/nirf_full.json) -> CAP institute code
NIRF = {
    '03036': ('41', 'Rank 1–100'), '16006': ('90', 'Rank 1–100'),
    '03012': (None, '101–150'), '06273': (None, '101–150'),
    '04167': (None, '151–200'), '04115': (None, '151–200'), '06141': (None, '151–200'), '06207': (None, '151–200'),
    '04116': (None, '201–300'), '06276': (None, '201–300'), '06175': (None, '201–300'), '03199': (None, '201–300'), '06007': (None, '201–300'),
}
NIRF_NOT_CAP = ['IIT Bombay (3, JEE Advanced)', 'VNIT Nagpur (44, JEE Main via JoSAA)', 'Symbiosis International (46, own test)', 'DIAT Pune (92, GATE/own)',
                'MIT World Peace University (101–150, own process)', 'NMIMS Mumbai (101–150, own test)', 'Bharati Vidyapeeth (151–200, own test)', 'Army Institute of Technology (201–300, Army wards via JEE Main)']

# home universities offered in the predictor (as printed in the CAP lists)
UNIVERSITIES = ['Mumbai University', 'Savitribai Phule Pune University', 'Rashtrasant Tukadoji Maharaj Nagpur University', 'Shivaji University',
                'Dr. Babasaheb Ambedkar Marathwada University', 'Sant Gadge Baba Amravati University', 'Kavayitri Bahinabai Chaudhari North Maharashtra University, Jalgaon',
                'Punyashlok Ahilyadevi Holkar Solapur University', 'Swami Ramanand Teerth Marathwada University, Nanded', 'Gondwana University', "SNDT Women's University"]

REGIONS = {
    'Mumbai & Konkan': ['Mumbai', 'Andheri', 'Navi Mumbai', 'Thane', 'Palghar', 'Raigad', 'Panvel', 'Karjat', 'Ratnagiri', 'Sindhudurg'],
    'Pune': ['Pune', 'Haveli', 'Satara', 'Karad', 'Baramati', 'Lonavala', 'Avasari Khurd'],
    'Western Maharashtra': ['Kolhapur', 'Sangli', 'Ichalkaranji', 'Solapur', 'Barshi', 'Pandharpur'],
    'North Maharashtra': ['Nashik', 'Jalgaon', 'Dhule', 'Nandurbar', 'Shirpur', 'Ahmednagar'],
    'Marathwada': ['Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Nanded', 'Parbhani', 'Hingoli'],
    'Vidarbha': ['Nagpur', 'Amravati', 'Akola', 'Buldhana', 'Shegaon', 'Washim', 'Yavatmal', 'Pusad', 'Wardha', 'Bhandara', 'Gondia', 'Chandrapur', 'Gadchiroli', 'Ballarpur'],
}

FAMILY_NAMES = {'CSE': 'Computer / CSE', 'AI': 'AI, ML & Data Science', 'IT': 'Information Technology', 'ENTC': 'Electronics & Telecom', 'ELEC': 'Electrical',
                'MECH': 'Mechanical & allied', 'CIVIL': 'Civil', 'CHEM': 'Chemical & process', 'OTHER': 'Other'}

BRANCH_GUIDE = [
    ('CSE', 'Highest demand everywhere: in 2025 the Round I open cut-off for Computer/CSE was the top branch at most colleges. Pick it at a lower-ranked college only if you would choose software work over the college brand.'),
    ('AI', 'AI, ML and Data Science seats grew fast since 2023 and usually close a little below Computer/CSE at the same college. The first two years overlap almost entirely with CSE.'),
    ('IT', 'Very close to CSE in courses and jobs, often 0.2 to 1 percentile lower at the same college: one of the best-value choices.'),
    ('ENTC', 'Electronics & Telecommunication keeps the door open to both hardware (VLSI, embedded) and software jobs; cut-offs sit between CSE and the core branches.'),
    ('ELEC', 'Electrical suits power, energy and electric-vehicle careers and government jobs (PSUs via GATE). Cut-offs rose from 2023 to 2025 at many colleges.'),
    ('MECH', 'Mechanical and allied branches (production, robotics, automation) are core engineering. Cut-offs rose sharply at most colleges from 2023 to 2025.'),
    ('CIVIL', 'Civil has the lowest cut-offs at most colleges: a strong choice at a top college for construction, infrastructure and government careers.'),
    ('CHEM', 'Chemical and process branches (ICT Mumbai is the leader) lead to pharma, food, polymer and process industries.'),
]
