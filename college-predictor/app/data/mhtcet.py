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
    'cap1_2026': 'https://cappublicdocs2026.blob.core.windows.net/documents/2026ENGG_CAP1_MH_CutOff.pdf',
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
    ('CSE', 'Highest demand everywhere: in CAP Round I the open cut-off for Computer/CSE is the top branch at most colleges. Pick it at a lower-ranked college only if you would choose software work over the college brand.'),
    ('AI', 'AI, ML and Data Science seats grew fast since 2023 and usually close a little below Computer/CSE at the same college. The first two years overlap almost entirely with CSE.'),
    ('IT', 'Very close to CSE in courses and jobs, often 0.2 to 1 percentile lower at the same college: one of the best-value choices.'),
    ('ENTC', 'Electronics & Telecommunication keeps the door open to both hardware (VLSI, embedded) and software jobs; cut-offs sit between CSE and the core branches.'),
    ('ELEC', 'Electrical suits power, energy and electric-vehicle careers and government jobs (PSUs via GATE). Cut-offs rose every year from 2023 to 2026 at many colleges.'),
    ('MECH', 'Mechanical and allied branches (production, robotics, automation) are core engineering. Cut-offs rose sharply at most colleges from 2023 to 2026.'),
    ('CIVIL', 'Civil has the lowest cut-offs at most colleges: a strong choice at a top college for construction, infrastructure and government careers.'),
    ('CHEM', 'Chemical and process branches (ICT Mumbai is the leader) lead to pharma, food, polymer and process industries.'),
]

# ---------------------------------------------------------------------------
# District of each college, for the Maharashtra map (district names as in the map file, app/static/data/maharashtra-districts.geojson;
# Mumbai City and Mumbai Suburban are one "Mumbai"). Town -> district first; then a few institutes whose name has no town, matched by hand;
# anything left is shown as "district not identified" rather than guessed.
# ---------------------------------------------------------------------------
TOWN_DISTRICT = {
    'Mumbai': 'Mumbai', 'Andheri': 'Mumbai', 'Navi Mumbai': 'Thane', 'Thane': 'Thane', 'Ulhasnagar': 'Thane', 'Shahapur': 'Thane',
    'Palghar': 'Palghar', 'Boisar': 'Palghar', 'Raigad': 'Raigad', 'Panvel': 'Raigad', 'Ratnagiri': 'Ratnagiri', 'Sindhudurg': 'Sindhudurg', 'Kankavli': 'Sindhudurg',
    'Pune': 'Pune', 'Haveli': 'Pune', 'Avasari Khurd': 'Pune', 'Baramati': 'Pune', 'Lonavala': 'Pune', 'Indapur': 'Pune', 'Wagholi': 'Pune', 'Pisoli': 'Pune',
    'Sasewadi': 'Pune', 'Someshwar Nagar': 'Pune', 'Kuran': 'Pune', 'Dumbarwadi': 'Pune',
    'Satara': 'Satara', 'Karad': 'Satara', 'Sangli': 'Sangli', 'Miraj': 'Sangli', 'Yelur': 'Sangli',
    'Kolhapur': 'Kolhapur', 'Ichalkaranji': 'Kolhapur', 'Jaysingpur': 'Kolhapur', 'Gadhinglaj': 'Kolhapur', 'Warananagar': 'Kolhapur',
    'Solapur': 'Solapur', 'Barshi': 'Solapur', 'Pandharpur': 'Solapur', 'Akluj': 'Solapur', 'Sangola': 'Solapur', 'Paniv': 'Solapur',
    'Ahmednagar': 'Ahmednagar', 'Sangamner': 'Ahmednagar', 'Bota Sangamner': 'Ahmednagar', 'Malwadi-Bota': 'Ahmednagar', 'Kopargaon': 'Ahmednagar',
    'Shevgaon': 'Ahmednagar', 'Kashti Shrigondha': 'Ahmednagar',
    'Nashik': 'Nashik', 'Agaskhind Tal. Sinnar': 'Nashik', 'Jalgaon': 'Jalgaon', 'Bhusawal': 'Jalgaon', 'Chopda': 'Jalgaon', 'Faizpur': 'Jalgaon',
    'Dhule': 'Dhule', 'Shirpur': 'Dhule', 'Dondaicha': 'Dhule', 'Nandurbar': 'Nandurbar', 'Nadurbar': 'Nandurbar', 'Akkalkuwa': 'Nandurbar',
    'Aurangabad': 'Aurangabad', 'Jalna': 'Jalna', 'Beed': 'Beed', 'Ambejogai': 'Beed', 'A.P Phulepimpalgaon': 'Beed', 'Latur': 'Latur',
    'Osmanabad': 'Osmanabad', 'Tuljapur': 'Osmanabad', 'Nanded': 'Nanded', 'Parbhani': 'Parbhani',
    'Nagpur': 'Nagpur', 'Ramtek': 'Nagpur', 'Amravati': 'Amravati', 'Badnera': 'Amravati', 'Akola': 'Akola', 'Buldhana': 'Buldhana', 'Shegaon': 'Buldhana',
    'Washim': 'Washim', 'Yavatmal': 'Yavatmal', 'Pusad': 'Yavatmal', 'Wardha': 'Wardha', 'Sevagram': 'Wardha', 'Bhandara': 'Bhandara', 'Sakoli': 'Bhandara',
    'Chandrapur': 'Chandrapur', 'Ballarpur': 'Chandrapur', 'Bhadrawati': 'Chandrapur', 'Warora': 'Chandrapur',
    'Egaon': 'Pune', 'Bhima': 'Pune', 'Lakhewadi': 'Pune', 'Pal': 'Kolhapur', 'Wadwadi': 'Satara', 'Ohar': 'Aurangabad',  # Talegaon, Koregaon Bhima, Pal (Gargoti), Ohar (Aurangabad)
}
# towns with the same name in two districts: decided by the DTE region in the first two digits of the institute code
TOWN_BY_REGION = {('Karjat', '03'): 'Raigad', ('Karjat', '05'): 'Ahmednagar', ('Karjat', '06'): 'Ahmednagar',
                  ('Malegaon', '05'): 'Nashik', ('Malegaon', '06'): 'Pune', ('Ashti', '02'): 'Beed', ('Ashti', '04'): 'Wardha'}
INST_DISTRICT = {  # institute names without a town, matched by hand
    '01119': 'Buldhana', '02516': 'Aurangabad', '02771': 'Beed', '03025': 'Mumbai', '03202': 'Ratnagiri', '03209': 'Mumbai', '03220': 'Raigad',
    '03277': 'Thane', '03436': 'Thane', '03445': 'Thane', '03470': 'Sindhudurg', '03546': 'Thane', '04197': 'Wardha', '05239': 'Nandurbar',
    '05395': 'Ahmednagar', '05597': 'Ahmednagar', '06182': 'Pune', '06185': 'Pune', '06217': 'Kolhapur', '06274': 'Pune', '06313': 'Sangli',
    '06315': 'Kolhapur', '06324': 'Pune', '06326': 'Solapur', '06632': 'Pune', '06635': 'Pune', '06811': 'Kolhapur', '16354': 'Pune',
}
DTE_REGION = {'01': 'Amravati region', '02': 'Aurangabad region', '03': 'Mumbai region', '04': 'Nagpur region', '05': 'Nashik region', '06': 'Pune region', '16': 'Pune region'}

# official website of each institute, keyed by the CAP institute code; only links that were found and checked are listed
SITES = {  # checked 22-23 Nov 2026 (State CET Cell institute codes); a campus page on a group domain where an institute has no site of its own
    '01002': 'https://gcoea.ac.in/', '01005': 'https://www.sgbau.ac.in/', '01101': 'https://www.ssgmce.ac.in/',
    '01105': 'https://mitra.ac.in/', '01107': 'https://www.prpotepatilengg.ac.in/', '01114': 'https://sipnaengg.ac.in/',
    '01117': 'https://www.bncoepusad.ac.in/', '01119': 'https://aecc.ac.in/', '01120': 'https://www.jdiet.ac.in/',
    '01121': 'https://www.hvpmcoet.in/', '01125': 'https://www.rsce.ac.in/', '01127': 'https://jcoet.ac.in/',
    '01128': 'https://www.prmceam.ac.in/', '01130': 'https://plit.ac.in/', '01180': 'https://www.sanmati.edu.in/',
    '01265': 'https://www.mauligroup.org/', '01268': 'https://www.stc.org.in/', '02008': 'https://geca.ac.in/',
    '02020': 'https://www.sggs.ac.in/', '02021': 'https://www.bamu.ac.in/', '02032': 'https://www.ictmumbai.edu.in/',
    '02111': 'https://www.eescoet.org/', '02112': 'https://www.sycet.org/', '02113': 'https://mit.asia/',
    '02114': 'https://www.dietms.org/', '02127': 'https://www.mgmcen.ac.in/', '02129': 'https://www.msbecl.ac.in/',
    '02130': 'https://coeosmanabad.ac.in/', '02133': 'https://www.coea.ac.in/', '02134': 'https://pescoe.ac.in/',
    '02135': 'https://www.hitechengg.edu.in/', '02137': 'https://www.nhce.in/', '02138': 'http://www.msscetjalna.org/',
    '02189': 'https://www.viet.ac.in/', '02250': 'https://csmengineering.in/', '02252': 'https://ssiems.org.in/',
    '02516': 'https://iceemabad.com/', '02522': 'https://sandipani.ac.in/', '02533': 'https://www.csmssengg.org/',
    '02634': 'https://www.eaglewoodpoly.in/', '02771': 'https://www.amolakcoe.org/', '02779': 'https://nkspt.org/ioe/',
    '03012': 'https://vjti.ac.in/', '03014': 'https://www.spce.ac.in/', '03025': 'https://sbmp.ac.in/',
    '03033': 'https://dbatu.ac.in/', '03035': 'https://www.umit.ac.in/', '03036': 'https://www.ictmumbai.edu.in/',
    '03042': 'https://gcoer.ac.in/', '03135': 'https://www.mctrgit.ac.in/', '03139': 'https://vit.edu.in/',
    '03143': 'https://www.tsecmumbai.in/', '03146': 'https://www.acpce.org/', '03147': 'https://tasgaonkartech.com/',
    '03148': 'https://www.sakec.ac.in/', '03154': 'https://engineering.saraswatikharghar.edu.in/', '03176': 'https://www.tcetmumbai.in/',
    '03182': 'https://tsec.edu/', '03183': 'https://www.mhssce.ac.in/', '03184': 'https://frcrce.ac.in/',
    '03185': 'https://vesit.ves.ac.in/', '03187': 'https://dmce.ac.in/', '03188': 'https://www.pvppcoe.ac.in/',
    '03189': 'https://bvcoenm.edu.in/', '03190': 'https://ternaengg.ac.in/', '03192': 'https://sigce.edu.in/',
    '03194': 'https://vcet.edu.in/', '03196': 'https://ltce.in/', '03197': 'https://www.fcrit.ac.in/',
    '03198': 'https://kgce.edu.in/', '03199': 'https://www.djsce.ac.in/', '03200': 'https://famt.ac.in/',
    '03201': 'https://eng.rizvi.edu.in/', '03202': 'https://www.rmcet.com/', '03203': 'https://atharvacoe.ac.in/',
    '03204': 'https://www.sfit.ac.in/', '03206': 'https://www.sspmcoe.ac.in/', '03207': 'https://www.pce.ac.in/',
    '03208': 'https://www.dbit.in/', '03209': 'https://kjsit.somaiya.edu.in/', '03210': 'https://www.kccemsr.edu.in/',
    '03211': 'https://siesgst.edu.in/', '03212': 'https://www.watumull.edu/', '03214': 'https://xavier.ac.in/',
    '03215': 'https://www.spit.ac.in/', '03216': 'https://git-india.edu.in/', '03218': 'https://sjcem.edu.in/',
    '03219': 'https://armiet.in/', '03220': 'https://tasgaonkartech.com/', '03221': 'https://www.viva-technology.org/',
    '03222': 'https://www.theemcoe.org/', '03223': 'https://phcet.ac.in/', '03224': 'https://www.gvaiet.org/',
    '03257': 'https://vpmthane.org/', '03351': 'https://bharatenggcollege.com/', '03353': 'https://driems.in/',
    '03423': 'https://slrtce.in/', '03436': 'https://brharnetc.edu.in/', '03439': 'https://aiktc.ac.in/',
    '03440': 'https://www.mitm.ac.in/', '03445': 'https://www.amitr.edu.in/', '03447': 'https://gmvit.com/',
    '03460': 'https://universalcollegeofengineering.edu.in/', '03462': 'https://vpmmpcoe.org/', '03465': 'https://idealwada.com/',
    '03467': 'https://vishwaniketan.edu.in/', '03470': 'https://www.ybit.ac.in/', '03471': 'https://nhitm.ac.in/',
    '03475': 'https://www.apsit.edu.in/', '03477': 'https://csmit.in/', '03503': 'https://icoe.ac.in/',
    '04004': 'http://www.gcoec.ac.in/gcoec/', '04005': 'https://litu.edu.in/', '04025': 'https://www.gcoen.ac.in/',
    '04104': 'https://kits.edu/', '04115': 'https://www.rknec.edu/', '04116': 'https://ghrce.raisoni.net/',
    '04123': 'https://www.pcenagpur.edu.in/', '04133': 'https://www.srpce.ac.in/', '04135': 'https://gwcet.ac.in/',
    '04137': 'https://www.sbjit.edu.in/', '04138': 'https://jdcoem.ac.in/', '04139': 'https://www.jitnagpur.edu.in/',
    '04141': 'https://www.vdcet.in/', '04142': 'https://ghrcemn.raisoni.net/', '04144': 'https://nit.edu.in/',
    '04145': 'https://www.wcem.in/', '04147': 'https://www.kdkce.edu.in/', '04151': 'https://tgpcet.edu.in/',
    '04163': 'https://rcert.ac.in/', '04167': 'https://ycce.edu/', '04172': 'https://anjumanengg.edu.in/',
    '04174': 'https://www.stvincentngp.edu.in/', '04175': 'https://sspace.ac.in/', '04177': 'https://pbcoe.edu.in/',
    '04181': 'https://ssitngp.in/', '04188': 'https://www.bitedu.co.in/', '04192': 'https://nietm.in/',
    '04193': 'https://vitnagpur.edu.in/', '04197': 'https://www.acenagthana.ac.in/', '04302': 'https://mietbhandara.ac.in/',
    '04304': 'https://cumminscollege.edu.in/', '04613': 'https://www.scetngp.com/', '04648': 'http://rvparankar.in/',
    '04649': 'https://bitwardha.ac.in/', '04703': 'https://somayyainstituteoftechnology.com/', '05003': 'https://nmu.ac.in/Chemical_Technology',
    '05004': 'https://www.gcoej.ac.in/', '05103': 'https://www.ssvpsengg.ac.in/', '05104': 'https://www.sscoetjalgaon.ac.in/',
    '05106': 'https://coem.ac.in/', '05108': 'https://kbtcoe.org/', '05109': 'https://sitrc.sandipfoundation.org/',
    '05121': 'https://www.kkwagh.edu.in/engineering', '05124': 'https://sndcoe.ac.in/', '05125': 'https://svitnashik.in/',
    '05130': 'https://engineering.brahmavalley.edu.in/', '05139': 'https://www.pravaraengg.org.in/', '05151': 'https://metbkcengg.ac.in/',
    '05152': 'https://ghrcemj.raisoni.net/', '05160': 'https://www.sanjivanicoe.org.in/', '05162': 'https://www.avcoe.org/',
    '05164': 'https://coeshahada.ac.in/', '05168': 'https://www.jtmcoef.ac.in/', '05169': 'https://gangamaiengg.org.in/',
    '05170': 'https://www.ssgbcoet.com/', '05171': 'https://gfgcoe.ac.in/', '05172': 'https://www.rcpit.ac.in/',
    '05173': 'https://www.snjb.org/engineering/', '05177': 'https://engg.matoshri.edu.in/', '05181': 'https://ges-coengg.org/',
    '05182': 'https://lgnscoe.sapkalknowledgehub.org/', '05184': 'https://siernashik.org.in/', '05244': 'https://metbhujbalknowledgecity.ac.in/metpoly/',
    '05256': 'http://mapoly.co.in/', '05330': 'https://www.pvgcoenashik.org/', '05331': 'https://siem.sandipfoundation.org/',
    '05381': 'https://www.sjrit.ac.in/', '05399': 'https://engineering.shreemahavir.org/', '05408': 'https://vidyaniketanglobal.com/',
    '05409': 'https://www.rgcoe.org/', '05411': 'https://mmantc.edu.in/', '05418': 'https://ggsf.edu.in/',
    '05449': 'https://www.svkm-iot.ac.in/', '05545': 'https://svkmcoe.ac.in/', '06004': 'https://gcoeara.ac.in/',
    '06005': 'https://gcekarad.ac.in/', '06007': 'https://walchandsangli.ac.in/', '06028': 'https://apps.unishivaji.ac.in/',
    '06122': 'https://pvpittssm.edu.in/', '06138': 'https://www.pgmozecoepune.in/', '06139': 'https://moderncoe.edu.in/',
    '06141': 'https://jspmrscoe.edu.in/', '06144': 'https://www.gsmozecoe.org/', '06145': 'https://jspmjscoe.edu.in/',
    '06146': 'https://mitaoe.ac.in/', '06149': 'https://siddhantcoe.in/', '06155': 'https://ghrcemp.raisoni.net/',
    '06175': 'https://www.pccoepune.com/', '06177': 'https://scoe.sinhgad.edu/', '06178': 'https://cms.sinhgad.edu/sinhgad_engineering_institutes/skncoe_vadgaon/institute_details.aspx',
    '06179': 'https://indiraicem.ac.in/', '06182': 'https://cms.sinhgad.edu/sinhgad_engineering_institutes/sits_narhetechnicalcampus.aspx', '06183': 'https://www.alameencoe.com/',
    '06184': 'https://kjei.edu.in/', '06185': 'https://cms.sinhgad.edu/sinhgad_engineering_institutes/sit_lonavala/about_institute.aspx', '06187': 'https://cms.sinhgad.edu/sinhgad_engineering_institutes/saoe/about_us.aspx',
    '06203': 'https://mmit.edu.in/', '06206': 'https://www.pdeacoem.org/', '06207': 'https://engg.dypvp.edu.in/',
    '06214': 'https://www.ritindia.edu/', '06217': 'https://amgoi.edu.in/', '06219': 'https://www.bigce.in/',
    '06220': 'https://sveri.ac.in/', '06222': 'https://dkte.ac.in/', '06223': 'https://orchidengg.ac.in/',
    '06250': 'https://coek.dypgroup.edu.in/', '06265': 'https://witsolapur.org/', '06267': 'https://www.kitcoek.in/',
    '06268': 'https://tkietwarana.ac.in/', '06269': 'https://www.pvpitsangli.edu.in/', '06270': 'https://kbpcoes.edu.in/',
    '06271': 'https://pict.edu/', '06272': 'https://dypcoeakurdi.ac.in/', '06273': 'https://www.vit.edu/',
    '06274': 'https://www.pvgcoet.ac.in/', '06275': 'https://engg.svpm.org.in/', '06276': 'https://cumminscollege.org/',
    '06277': 'https://www.jjmcoe.ac.in/', '06278': 'https://aissmscoe.com/', '06281': 'https://mescoe.mespune.org/',
    '06282': 'https://aissmsioit.org/', '06283': 'https://www.adcet.ac.in/', '06284': 'https://vpkbiet.org/',
    '06285': 'https://coewpune.bharatividyapeeth.edu/', '06288': 'https://coekolhapur.bharatividyapeeth.edu/', '06289': 'https://www.viit.ac.in/',
    '06293': 'https://bmitsolapur.org/', '06298': 'https://zcoer.in/', '06303': 'https://dacoe.ac.in/',
    '06304': 'https://www.aitrcvita.edu.in/', '06305': 'https://www.sdncedu.com/', '06307': 'https://dpcoepune.edu.in/',
    '06308': 'https://agpit.edu.in/', '06310': 'https://www.nmiet.edu.in/', '06311': 'https://jspmbsiotr.edu.in/',
    '06315': 'https://www.seti.edu.in/', '06320': 'https://www.kjei.edu.in/kjcoemr/', '06322': 'https://spcoe.in/',
    '06324': 'https://rajgad.edu.in/rtc/engg/', '06325': 'https://www.alardcollegeofengineering.com/', '06326': 'https://www.karmayogi.org.in/',
    '06402': 'https://nitkop.in/', '06444': 'https://sietpaniv.org/', '06466': 'https://sietghogaon.org/',
    '06468': 'https://bsiet.org/', '06545': 'https://www.agce.edu.in/', '06609': 'https://jaihind.edu.in/jcoe/',
    '06622': 'https://www.isbmcoe.org/', '06625': 'https://www.ucoer.edu.in/', '06628': 'https://www.dattakala.edu.in/',
    '06632': 'https://navsahyadri.edu.in/', '06634': 'https://tae.kjei.edu.in/', '06635': 'https://samarthinstitute.edu.in/',
    '06640': 'https://www.sinhgadsolapur.org/', '06643': 'https://www.sknscoe.ac.in/', '06644': 'https://www.sbgimiraj.org/',
    '06649': 'https://tssm.edu.in/', '06715': 'https://dkkkpbpp.edu.in/', '06754': 'https://www.isquareit.edu.in/',
    '06755': 'https://www.jspmntc.edu.in/', '06756': 'https://www.ftccoe.ac.in/', '06757': 'https://www.yes.edu.in/',
    '06758': 'https://www.sahyadrivalleycollege.com/', '06759': 'https://www.srespune.org/', '06762': 'https://www.nmcoe.org.in/',
    '06766': 'https://www.coephaltan.edu.in/', '06767': 'https://www.srttc.ac.in/', '06768': 'https://www.pkinstitute.edu.in/',
    '06770': 'https://cms.sinhgad.edu/sinhgad_engineering_institutes/sknsits_lonavala/about_us.aspx', '06771': 'https://www.flora.ac.in/', '06780': 'https://foet.dypgroup.edu.in/',
    '06781': 'https://bitbarshi.edu.in/', '06782': 'https://www.smsmpitr.edu.in/', '06794': 'https://abmspcoerpune.org/',
    '06795': 'https://www.secsomeshwar.ac.in/', '06796': 'https://bvcoe.bharatividyapeeth.edu/', '06797': 'https://www.dnyanshree.edu.in/',
    '06799': 'https://www.shivgangavtc.org/', '06802': 'https://www.dypiemr.ac.in/', '06803': 'https://sgmcoe.com/',
    '06808': 'https://keystone.ac.in/', '06811': 'https://www.sginstitute.in/', '06815': 'https://www.vpscet.in/',
    '06822': 'https://www.pccoer.com/', '06834': 'https://www.dypcoei.edu.in/', '06839': 'https://dypsn.edu.in/',
    '06878': 'https://www.adshindecoe.edu.in/', '06901': 'https://mitcorer.edu.in/', '14005': 'https://litu.edu.in/',
    '16006': 'https://www.coeptech.ac.in/', '16121': 'https://abitkarcollegeofengineering.com/', '16126': 'https://tkietwarana.ac.in/',
    '16354': 'https://dvcoe.com/', '16355': 'https://asmnext.edu.in/', '16357': 'https://mlcoe.mespune.in/',
}
# institutes without a link (including those new in the 2026 list, not yet searched): no official site found in the search, a parked or hijacked domain, or a site that returned errors on every check
SITES_MISSING = ['01012', '01116', '01123', '01126', '01182', '01276', '02015', '02116', '02131', '02136', '02146', '02254', '02282', '02508', '02637', '02641', '02666', '02758', '02770', '02772', '02777', '03175', '03193', '03217', '03277', '03546', '03723', '03724', '03725', '03726', '04118', '04134', '04136', '04143', '04190', '04196', '04285', '04679', '05161', '05179', '05223', '05239', '05249', '05263', '05303', '05322', '05365', '05370', '05380', '05382', '05390', '05395', '05396', '05401', '05414', '05433', '05497', '05509', '05513', '05597', '06036', '06156', '06313', '06317', '06318', '06319', '06321', '06419', '06467', '06714', '06732', '06769', '06772', '06938', '06991', '16351', '16352', '02805', '04026', '04762', '05413', '05682', '05683', '05686', '06041', '06725', '06814', '16371', '16372']
