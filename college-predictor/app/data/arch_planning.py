"""Content for the public Architecture and Planning pages: the guide (/architecture-planning-india) and the analytics (/architecture-planning-analytics).
Sources, all read on 2 November 2026: NATA 2026 brochure (Council of Architecture), JoSAA 2026 brochure and its round-wise rank workbook (rounds 1 to 5),
DASA 2026 brochure and the DASA 2025/2026 closing-rank workbook, NIRF India Rankings 2025 (Architecture and Planning list page) and the NIRF engineering metrics paper.
College fees, placements and quota rules for individual colleges live in app/data/arch_colleges.json (researched, each fact with its own source link; blank where not verified).
Nothing here promises a rank, a seat or an admission."""
import json
import os

UPDATED = '2 November 2026'
_HERE = os.path.dirname(os.path.abspath(__file__))

FACTS = [
    ('About 369', 'institutions teach architecture in India, as recognised by the Council of Architecture (NATA 2026 brochure)'),
    ('5 + 4', 'years: B.Arch is five years, B.Planning is four years (JoSAA 2026)'),
    ('20', 'JoSAA institutes filled B.Arch or B.Planning seats in 2026, across 5 rounds'),
    ('1 + 1', 'two tests, two worlds: JEE Main Paper 2 for JoSAA seats, NATA for most other colleges'),
]

ROUTES = [
    ('JEE Main Paper 2A / 2B through JoSAA', 'NTA ranks, JoSAA counselling',
     'B.Arch and B.Planning at the three Schools of Planning and Architecture (Delhi, Bhopal, Vijayawada), NITs, IIEST Shibpur and other centrally funded institutes. Seats are filled in rounds by rank, category and quota (All India, Home State, Other State).',
     'josaa.nic.in'),
    ('JEE Advanced and the Architecture Aptitude Test (AAT)', 'IIT organising institute, JoSAA counselling',
     'B.Arch at IIT Kharagpur, IIT Roorkee and IIT (BHU) Varanasi. In 2026 the AAT result came after JEE Advanced, and candidates who qualified filled their AAT choices from 7 June 2026.',
     'jeeadv.ac.in'),
    ('NATA, then state or college counselling', 'Council of Architecture test; each state or college admits',
     'Most state government, private and deemed university colleges. NATA is only the qualifying aptitude test: the Council does not admit anyone, the state authority or the institute does (NATA 2026 brochure, section 2.0).',
     'nata.in'),
    ('DASA for NRI, PIO, OCI and foreign nationals', 'CSAB and DASA',
     'Supernumerary seats (up to 15 percent) at NITs, SPAs and IIEST on the basis of Paper 2A or 2B (DASA 2026 brochure). See the NRI section below.',
     'dasa.education.gov.in'),
    ('College own tests, portfolio and management seats', 'Each institute',
     'Some universities and private colleges run their own entrance, a portfolio review or an interview. Rules, fees and quotas differ for each one, so confirm them in that college’s prospectus.',
     'The college website'),
]

ELIGIBILITY = [
    ('B.Arch: Council of Architecture rule', 'Passed 10+2 with Physics and Mathematics, plus one of Chemistry, Biology, a technical vocational subject, Computer Science, Information Technology, Informatics Practices, Engineering Graphics or Business Studies, with at least 45% in aggregate. Or a 10+3 Diploma with Mathematics, at least 45% in aggregate.', 'NATA 2026 brochure, 5.2'),
    ('B.Arch through JoSAA and DASA', 'Physics, Chemistry and Mathematics in 10+2 (or a 10+3 diploma with Mathematics), and 75% in the best five subjects (65% for SC, ST and PwD) or being in the top 20 percentile of your board. A valid Paper 2A rank.', 'JoSAA 2026 and DASA 2026 brochures'),
    ('B.Planning through JoSAA and DASA', 'Passed 10+2 with Mathematics, with the same 75% (65% for SC, ST, PwD) or top 20 percentile rule. A valid Paper 2B rank.', 'JoSAA 2026 and DASA 2026 brochures'),
    ('Appearing students', 'You may apply while appearing in Class 12, but you must show the result by the date the counselling authority sets (DASA 2026: final results by 30 September 2026).', 'NATA and DASA 2026 brochures'),
    ('No fixed age rule for JoSAA B.Arch', 'DASA 2026 required candidates to be born on or after 1 October 2001. JoSAA and state counselling publish their own age rules each year.', 'DASA 2026 brochure'),
]

NATA = dict(
    title='NATA 2026 at a glance',
    rows=[
        ('Run by', 'Council of Architecture (CoA), set up under the Architects Act, 1972'),
        ('Phase 1', 'Fridays and Saturdays from 4 April to 13 June 2026, up to two attempts. Used for centralised counselling. Percentile-based score from the best raw score.'),
        ('Phase 2', '7 and 8 August 2026, one attempt, raw score only. Used for seats left vacant after counselling.'),
        ('Pattern', 'Part A: drawing and composition on paper, 90 minutes, 80 marks (3 questions). Part B: computer-based adaptive test, 90 minutes, 120 marks (42 MCQ and 8 no-choice questions). Total 200.'),
        ('Fee (per test)', '₹1,750 General and OBC-NCL; ₹1,250 SC, ST, EWS and PwD; ₹1,000 transgender; ₹15,000 outside India'),
        ('Qualifying', 'No minimum raw score is set. Admission authorities may rank by raw score or percentile.'),
        ('Validity', 'The 2026 score is valid for the 2026-27 session. A 2025 score stayed valid for 2026-27 only if the candidate took no second 2026 attempt.'),
        ('2027 cycle', 'Not announced in the sources we hold. Treat the 2026 cycle as a guide to the shape of the year, and check nata.in.'),
    ],
)

JOSAA_STEPS = [
    ('Get a rank', 'JEE Main Paper 2A for B.Arch or Paper 2B for B.Planning (and JEE Advanced with the AAT for the IIT B.Arch seats).'),
    ('Register and fill choices', 'Free of cost. Register on josaa.nic.in and rank your programmes. Only the choices you fill can be allotted, and you get one seat.'),
    ('Mock allocations', 'Two mock allocations were shown before the choices locked, so you can reorder them.'),
    ('Seat allocation by rounds', 'Round 1 on 13 June 2026 and Round 5 on 16 July 2026. Your seat is decided by rank, category, gender pool and quota.'),
    ('Accept the seat', 'Pay the seat acceptance fee (₹30,000, or ₹15,000 for SC, ST and PwD categories, of which ₹5,000 is JoSAA’s processing charge), upload documents and report online. Then choose Freeze, Float or Slide in the next round.'),
    ('Report to the institute', 'The institute checks your original documents and collects its own admission fee. The acceptance fee, less the ₹5,000, is adjusted against it.'),
]
JOSAA_DATES = [
    ('2 Jun 2026', 'Registration and choice filling opens'),
    ('11 Jun 2026', 'Choice filling ends'),
    ('13 Jun 2026', 'Round 1 allocation'),
    ('30 Jun 2026', 'Round 2 allocation'),
    ('6 Jul 2026', 'Round 3 allocation'),
    ('10 Jul 2026', 'Round 4 allocation'),
    ('16 Jul 2026', 'Round 5, final round for IITs'),
]
JOSAA_NOTE = ('These are the 2026 dates, kept as a guide. The 2027 JoSAA brochure and JEE Main 2027 schedule decide your year: see the JEE Paper 2 page and josaa.nic.in.')

NRI = dict(
    intro=('NRI, PIO, OCI and foreign-national students reach architecture seats by two doors: the government door (DASA) and the college door (an NRI or management quota that a private college or state sets for itself).'),
    dasa=[
        ('Seats', 'Supernumerary, up to 15 percent of the programme’s seats at each participating institute. One third of DASA seats (5 percent) are kept for Children of Indian Workers in the Gulf (CIWG).'),
        ('Qualifying exam', 'JEE Main 2026 Paper 2A for B.Arch and Paper 2B for B.Planning.'),
        ('Institutes with architecture or planning in DASA 2025 and 2026', 'NIT Calicut, NIT Tiruchirappalli, VNIT Nagpur, MANIT Bhopal, SPA New Delhi, SPA Bhopal and SPA Vijayawada. NIT Hamirpur, NIT Raipur and MNIT Jaipur appear in 2025 only (DASA 2025 and 2026 report).'),
        ('Residence rule', 'Two years of study abroad (Classes 11 and 12) in the last eight years for Indian nationals, with the qualifying exam passed from abroad. All foreign nationals are eligible.'),
        ('Enrolment fee', 'US$ 300 non-refundable registration plus first-semester tuition: ₹62,500 for CIWG, US$ 4,000 for Non-SAARC (total US$ 4,300), US$ 2,000 for SAARC nationals (total US$ 2,300). Parents in India may pay in INR. Balance tuition and hostel fees are set by each institute.'),
        ('Candidates who also took JoSAA', 'Allowed, as long as the candidate keeps within DASA’s rule on retained seats (see the DASA 2026 brochure).'),
    ],
    college=[
        'Private and deemed universities usually advertise an NRI or management quota. The size of the quota, the fee (often in US dollars) and whether NATA or a test is required are the college’s own decisions. A letter or prospectus line from the college is the only proof.',
        'State government colleges follow the state’s rules. Many states reserve a small number of NRI seats in state colleges, others do not. Ask the state counselling authority for the current notice.',
        'The Council of Architecture sets the minimum academic standards and the aptitude test. It does not set fee or quota rules, so a quota offered by a college is not a recognition issue, but the college must be CoA-approved for your degree to count.',
        'Never pay a quota fee to an agent. Pay only into the college’s own account against a receipt, and check approval on coa.gov.in first.',
    ],
    links=[('NRI Admission Guide', 'main.nri_admission'), ('DASA 2027 guide', 'main.dasa_2026')],
)

# the 28 institutions that sit in this order of NIRF 2025 Architecture and Planning rank. scores: TLR, RPC, GO, OI, Perception
NIRF = [
    (1, 'Indian Institute of Technology Roorkee', 'Roorkee', 'Uttarakhand', 83.95, (80.06, 95.65, 89.28, 75.20, 74.22)),
    (2, 'National Institute of Technology Calicut', 'Kozhikode', 'Kerala', 77.89, (89.46, 59.45, 84.65, 74.59, 58.26)),
    (3, 'Indian Institute of Technology Kharagpur', 'Kharagpur', 'West Bengal', 77.38, (69.49, 84.36, 89.51, 66.92, 81.24)),
    (4, 'Indian Institute of Engineering Science and Technology, Shibpur', 'Howrah', 'West Bengal', 68.37, (72.83, 54.69, 79.15, 66.36, 58.26)),
    (5, 'Jamia Millia Islamia', 'New Delhi', 'Delhi', 67.15, (69.01, 46.44, 91.42, 86.17, 33.48)),
    (6, 'Centre for Environmental Planning and Technology University', 'Ahmedabad', 'Gujarat', 65.73, (72.22, 47.68, 78.06, 65.14, 51.81)),
    (7, 'National Institute of Technology Rourkela', 'Rourkela', 'Odisha', 65.72, (63.86, 66.34, 74.77, 66.12, 53.52)),
    (8, 'School of Planning and Architecture New Delhi', 'New Delhi', 'Delhi', 65.11, (65.89, 37.73, 70.47, 71.24, 100.00)),
    (9, 'National Institute of Technology Tiruchirappalli', 'Tiruchirappalli', 'Tamil Nadu', 64.30, (55.94, 50.92, 80.46, 75.40, 81.24)),
    (10, 'Visvesvaraya National Institute of Technology, Nagpur', 'Nagpur', 'Maharashtra', 61.22, (56.11, 53.54, 88.04, 69.83, 34.81)),
    (11, 'School of Planning and Architecture Bhopal', 'Bhopal', 'Madhya Pradesh', 60.69, (68.75, 22.83, 75.69, 76.45, 58.26)),
    (12, 'Malaviya National Institute of Technology', 'Jaipur', 'Rajasthan', 60.48, (51.81, 68.54, 82.01, 72.04, 24.45)),
    (13, 'National Institute of Technology Patna', 'Patna', 'Bihar', 60.16, (58.54, 61.79, 73.33, 65.04, 32.10)),
    (14, 'Chandigarh University', 'Mohali', 'Punjab', 59.70, (68.30, 47.19, 69.26, 75.76, 15.06)),
    (15, 'College of Engineering Trivandrum', 'Thiruvananthapuram', 'Kerala', 59.63, (62.64, 39.71, 88.70, 58.20, 30.68)),
    (16, 'Jadavpur University', 'Kolkata', 'West Bengal', 59.30, (60.10, 47.70, 75.96, 52.58, 52.67)),
    (17, 'Maulana Azad National Institute of Technology', 'Bhopal', 'Madhya Pradesh', 58.80, (66.05, 38.44, 80.01, 64.20, 22.73)),
    (18, 'S.R.M. Institute of Science and Technology', 'Chennai', 'Tamil Nadu', 58.63, (62.28, 61.04, 69.84, 56.30, 19.07)),
    (19, 'School of Planning & Architecture, Vijayawada', 'Vijayawada', 'Andhra Pradesh', 58.49, (57.81, 30.35, 80.42, 69.63, 62.52)),
    (20, 'BMS College of Architecture', 'Bengaluru', 'Karnataka', 58.10, (66.58, 13.91, 80.83, 65.52, 59.73)),
    (21, 'Manipal University Jaipur', 'Jaipur', 'Rajasthan', 56.83, (65.57, 44.74, 73.00, 59.94, 10.62)),
    (22, 'Birla Institute of Technology', 'Ranchi', 'Jharkhand', 56.76, (65.82, 43.26, 59.31, 59.42, 39.76)),
    (23, 'Shri Mata Vaishno Devi University', 'Katra', 'Jammu and Kashmir', 56.47, (72.80, 43.90, 56.46, 53.65, 19.07)),
    (24, 'Lovely Professional University', 'Phagwara', 'Punjab', 56.11, (64.40, 41.41, 65.30, 63.97, 26.10)),
    (25, 'Amity University', 'North Twenty Four Parganas', 'West Bengal', 55.49, (72.06, 5.39, 79.65, 83.69, 12.89)),
    (26, 'Aligarh Muslim University', 'Aligarh', 'Uttar Pradesh', 55.11, (47.01, 75.26, 75.51, 38.94, 22.73)),
    (27, 'Manipal School of Architecture and Planning, MAHE', 'Udupi', 'Karnataka', 54.68, (63.70, 20.98, 73.11, 66.38, 37.36)),
    (28, 'Anna University', 'Chennai', 'Tamil Nadu', 54.60, (53.19, 47.36, 51.24, 53.12, 82.93)),
    (29, 'Nirma University', 'Ahmedabad', 'Gujarat', 54.24, (62.98, 39.47, 64.30, 60.29, 22.73)),
    (30, 'National Institute of Technology Hamirpur', 'Hamirpur', 'Himachal Pradesh', 54.00, (50.73, 34.00, 82.23, 68.48, 36.11)),
    (31, 'M. S. Ramaiah Institute of Technology', 'Bengaluru', 'Karnataka', 53.54, (59.87, 27.96, 76.39, 56.51, 30.68)),
    (32, 'Dr. M. G. R. Educational and Research Institute', 'Chennai', 'Tamil Nadu', 53.26, (66.14, 25.65, 68.02, 75.08, 5.64)),
    (33, 'Thiagarajar College of Engineering', 'Madurai', 'Tamil Nadu', 52.56, (55.37, 32.92, 71.08, 51.90, 44.17)),
    (34, 'Christ University', 'Bengaluru', 'Karnataka', 51.79, (67.40, 25.25, 50.66, 70.41, 26.10)),
    (35, 'National Institute of Technology, Raipur', 'Raipur', 'Chhattisgarh', 51.30, (54.21, 46.13, 60.98, 62.81, 19.07)),
    (36, 'Guru Gobind Singh Indraprastha University', 'New Delhi', 'Delhi', 51.00, (47.40, 33.35, 83.20, 56.62, 30.68)),
    (37, 'BMS School of Architecture, Yelahanka', 'Bengaluru', 'Karnataka', 48.45, (55.50, 24.85, 65.88, 51.78, 29.21)),
    (38, 'Chitkara University', 'Rajpura', 'Punjab', 48.16, (51.87, 31.25, 72.30, 56.45, 10.62)),
    (39, 'Faculty of Architecture and Planning, Dr APJ Abdul Kalam Technical University', 'Lucknow', 'Uttar Pradesh', 47.94, (57.82, 4.87, 77.64, 50.95, 32.10)),
    (40, 'Anant National University', 'Ahmedabad', 'Gujarat', 47.61, (63.75, 6.63, 72.53, 57.14, 5.64)),
]
NIRF_PARAMS = [
    ('TLR', 'Teaching, Learning and Resources', 0.40),
    ('RPC', 'Research and Professional Practice', 0.20),
    ('GO', 'Graduation Outcomes', 0.20),
    ('OI', 'Outreach and Inclusivity', 0.10),
    ('PR', 'Perception', 0.10),
]
NIRF_NOTE = ('Ranks and the five scores are copied from the NIRF 2025 Architecture and Planning list. For this list the weights are 0.40, 0.20, 0.20, 0.10 and 0.10: '
             'we worked them out from the published scores, which they reproduce to two decimals. The NIRF engineering paper uses different weights (0.30, 0.30, 0.20, 0.10, 0.10), so do not read this list with those. '
             'Each institute’s own data sheet (placement, median salary, intake) is linked on nirfindia.org and is the source to trust for those numbers. 40 institutions were ranked in 2025.')

# institute facts for the JoSAA 2026 file: short name, city, state, group
INST_META = {
    'Indian Institute of Engineering Science and Technology, Shibpur': ('IIEST Shibpur', 'Howrah', 'West Bengal', 'IIEST'),
    'Indian Institute of Technology (BHU) Varanasi': ('IIT (BHU) Varanasi', 'Varanasi', 'Uttar Pradesh', 'IIT'),
    'Indian Institute of Technology Kharagpur': ('IIT Kharagpur', 'Kharagpur', 'West Bengal', 'IIT'),
    'Indian Institute of Technology Roorkee': ('IIT Roorkee', 'Roorkee', 'Uttarakhand', 'IIT'),
    'Islamic University of Science and Technology Kashmir': ('IUST Kashmir', 'Awantipora', 'Jammu and Kashmir', 'Other GFTI'),
    'Malaviya National Institute of Technology Jaipur': ('MNIT Jaipur', 'Jaipur', 'Rajasthan', 'NIT'),
    'Maulana Azad National Institute of Technology Bhopal': ('MANIT Bhopal', 'Bhopal', 'Madhya Pradesh', 'NIT'),
    'Mizoram University, Aizawl': ('Mizoram University', 'Aizawl', 'Mizoram', 'Other GFTI'),
    'National Institute of Technology Calicut': ('NIT Calicut', 'Kozhikode', 'Kerala', 'NIT'),
    'National Institute of Technology Hamirpur': ('NIT Hamirpur', 'Hamirpur', 'Himachal Pradesh', 'NIT'),
    'National Institute of Technology Patna': ('NIT Patna', 'Patna', 'Bihar', 'NIT'),
    'National Institute of Technology Raipur': ('NIT Raipur', 'Raipur', 'Chhattisgarh', 'NIT'),
    'National Institute of Technology, Kurukshetra': ('NIT Kurukshetra', 'Kurukshetra', 'Haryana', 'NIT'),
    'National Institute of Technology, Rourkela': ('NIT Rourkela', 'Rourkela', 'Odisha', 'NIT'),
    'National Institute of Technology, Tiruchirappalli': ('NIT Tiruchirappalli', 'Tiruchirappalli', 'Tamil Nadu', 'NIT'),
    'School of Planning & Architecture, Bhopal': ('SPA Bhopal', 'Bhopal', 'Madhya Pradesh', 'SPA'),
    'School of Planning & Architecture, New Delhi': ('SPA New Delhi', 'New Delhi', 'Delhi', 'SPA'),
    'School of Planning & Architecture: Vijayawada': ('SPA Vijayawada', 'Vijayawada', 'Andhra Pradesh', 'SPA'),
    'Shri Mata Vaishno Devi University, Katra, Jammu & Kashmir': ('SMVDU Katra', 'Katra', 'Jammu and Kashmir', 'Other GFTI'),
    'Visvesvaraya National Institute of Technology, Nagpur': ('VNIT Nagpur', 'Nagpur', 'Maharashtra', 'NIT'),
}

READING = [
    ('Different rank lists', 'B.Arch seats at NITs, SPAs and IIEST use the JEE Main Paper 2A rank, B.Planning uses Paper 2B. IIT B.Arch seats follow the JEE Advanced and AAT route. DASA seats have their own, much smaller, rank cut-offs. Never compare an engineering rank with these numbers.'),
    ('Closing rank is the last seat filled', 'If your rank is lower (a smaller number) than the closing rank of a category in a round, a seat of that kind was still allotted at that rank. It is not a promise for next year. Seat numbers and applicants change every year.'),
    ('Quota matters as much as rank', 'HS is Home State, OS is Other State, AI is All India. At an NIT you are compared only with candidates in your own pool. The same college can look easy for its home state and hard for outsiders.'),
    ('Gender-neutral and female-only pools', 'Female-only seats have their own ranks. A woman can compete in both pools, and the more favourable result applies.'),
    ('Opening to closing', 'Opening rank is the best rank allotted in the pool in that round, closing is the last. The gap tells you how the pool is filled, not what you should expect.'),
]

FAQ = [
    ('Do I need NATA if I write JEE Main Paper 2?', 'For JoSAA seats (SPAs, NITs, IIEST) the Paper 2A rank is enough. For most state and private colleges, NATA is the accepted test. Many students write both, because the two cover different sets of colleges.'),
    ('Is a B.Arch degree from any college valid?', 'Only if the college is approved by the Council of Architecture for that session. Check coa.gov.in before paying any fee.'),
    ('How many attempts does NATA give?', 'For 2026: up to two in Phase 1 or one in Phase 2, not both. Confirm the 2027 rule in the new brochure.'),
    ('Can I get B.Planning without B.Arch?', 'Yes. B.Planning is a four-year degree in its own right and uses Paper 2B. The SPAs and MANIT Bhopal offered it through JoSAA in 2026.'),
    ('What if my college does not publish fees or placements?', 'Take the NIRF data sheet if it has one, then ask the admissions office to put the fee head by head and last year’s placement count in writing. This page leaves a field blank when we could not find a source.'),
    ('Does a higher NIRF rank mean a better studio experience?', 'It means better scores on the NIRF parameters (teaching resources, research, graduate outcomes, outreach, perception). Visit, speak to students and look at student work.'),
]

SOURCES = [
    ('NATA 2026 information brochure (Council of Architecture)', 'https://www.nata.in'),
    ('JoSAA 2026 information brochure and business rules', 'https://josaa.nic.in'),
    ('JoSAA 2026 opening and closing ranks, rounds 1 to 5', 'https://josaa.nic.in'),
    ('DASA 2026 (UG) information brochure, 27 May 2026', 'https://dasa.education.gov.in'),
    ('NIRF India Rankings 2025: Architecture and Planning', 'https://www.nirfindia.org/Rankings/2025/ArchitectureRanking.html'),
    ('NIRF 2025 ranking methodology (engineering metrics paper)', 'https://www.nirfindia.org'),
    ('Council of Architecture', 'https://www.coa.gov.in'),
]

TAGS = 'architecture colleges india, B.Arch admission, B.Planning, NIRF architecture ranking 2025, JoSAA 2026 B.Arch cutoff, NATA 2026, DASA architecture, NRI quota architecture'


def josaa():
    with open(os.path.join(_HERE, 'arch_josaa.json'), encoding='utf-8') as f:
        return json.load(f)


def colleges():
    """Researched college directory (may be missing early in the build)."""
    p = os.path.join(_HERE, 'arch_colleges.json')
    if not os.path.exists(p):
        return dict(colleges=[], state_notes={})
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def _last(a):
    v = [x for x in a if x is not None]
    return v[-1] if v else None


def _first(a):
    v = [x for x in a if x is not None]
    return v[0] if v else None


def _short(name):
    return INST_META[name][0] if name in INST_META else name


def guide_context():
    j = josaa()
    cd = colleges()
    cols = cd['colleges']
    states = sorted({c['state'] for c in cols if c['state']})
    by_state = {s: [c for c in cols if c['state'] == s] for s in states}
    seats = {}
    try:
        with open(os.path.join(_HERE, 'arch_seats.json'), encoding='utf-8') as f:
            for r in json.load(f):
                seats[(r['inst'], r['prog'])] = r['seats']
    except OSError:
        pass
    # JoSAA table: OPEN, gender-neutral, per institute x programme x quota
    jr = []
    for r in j['rows']:
        if r['s'] != 'OPEN' or r['g'] != 'N':
            continue
        name = j['institutes'][r['i']]
        m = INST_META.get(name, (name, '', '', ''))
        jr.append(dict(name=m[0], city=m[1], state=m[2], prog='B.Arch' if r['p'] == 'A' else 'B.Planning', quota={'AI': 'All India', 'HS': 'Home State', 'OS': 'Other State'}[r['q']],
                       c1=_first(r['c']), c5=_last(r['c']), seats=seats.get((name, r['p'])) if r['q'] == 'HS' else None, iit=m[3] == 'IIT'))
    jr.sort(key=lambda x: (x['iit'], x['name'], x['prog'], x['quota']))
    gov = ('Central govt', 'State govt', 'State university')
    fee_rows = sorted([c for c in cols if c.get('tuition')], key=lambda c: c['tuition'])
    fee_summary = []
    if fee_rows:
        g = [c['tuition'] for c in fee_rows if c['type'] in gov]
        p = [c['tuition'] for c in fee_rows if c['type'] not in gov]
        if g:
            fee_summary.append(('\u20b9{:,} to \u20b9{:,}'.format(min(g), max(g)), 'tuition a year at %d government institutions with a verified figure' % len(g)))
        if p:
            fee_summary.append(('\u20b9{:,} to \u20b9{:,}'.format(min(p), max(p)), 'tuition a year at %d private or deemed institutions with a verified figure' % len(p)))
        fee_summary.append((str(len(fee_rows)), 'of %d listed colleges have a fee we could verify' % len(cols)))
    placement_rows = [c for c in cols if c.get('pl_pack')]
    nri_rows = [c for c in cols if c.get('nri_text')]
    ver = sum(1 for c in cols if c.get('tuition'))
    cov = ('This list has %d of the roughly 369 Council-approved institutions: all 40 NIRF-ranked ones, the JoSAA institutes and a selection of state and private colleges. '
           'It is not the full Council list; check coa.gov.in for every approved college. Fee figures marked unverified come from aggregator sites. '
           'NIRF data sheets (placement, median salary, intake) could not be read for most institutions, so placement is shown only where we hold the sheet.') % len(cols)
    return dict(colleges=cols, states=states, by_state=by_state, state_notes=cd['state_notes'], josaa_rows=jr, josaa_n=len(j['institutes']),
                fee_rows=fee_rows, fee_summary=fee_summary, placement_rows=placement_rows, nri_rows=nri_rows, coverage_note=cov)


def analytics_context():
    j = josaa()
    meta = {n: list(INST_META.get(n, (n, '', '', ''))) for n in j['institutes']}
    by_inst = {}
    for r in j['rows']:
        by_inst.setdefault(r['i'], 0)
        by_inst[r['i']] += 1
    seat_rows = []
    try:
        with open(os.path.join(_HERE, 'arch_seats.json'), encoding='utf-8') as f:
            for r in json.load(f):
                q = r['quota']
                seat_rows.append(dict(name=_short(r['inst']), prog=r['prog'], seats=r['seats'], hs=q.get('Home State', 0), os=q.get('Other State', 0)))
    except OSError:
        pass
    nirf = [[r[0], r[1], r[2], r[3], r[4], list(r[5])] for r in NIRF]
    data = dict(inst=j['institutes'], meta=meta, rows=j['rows'], dasa=j['dasa'], seats=seat_rows, nirf=nirf, params=[list(p) for p in NIRF_PARAMS], byInst=by_inst)
    # findings, computed from the rows
    rows = [r for r in j['rows'] if r['s'] == 'OPEN' and r['g'] == 'N' and INST_META.get(j['institutes'][r['i']], ('', '', '', ''))[3] != 'IIT' and _last(r['c'])]
    f = []
    if rows:
        arch = [r for r in rows if r['p'] == 'A']
        low = min(arch, key=lambda r: _last(r['c']))
        high = max(arch, key=lambda r: _last(r['c']))
        f.append(('Hardest B.Arch pool', '%s, %s: OPEN closed at %s in the last round' % (_short(j['institutes'][low['i']]), {'AI': 'All India', 'HS': 'Home State', 'OS': 'Other State'}[low['q']], '{:,}'.format(_last(low['c'])))))
        f.append(('Widest B.Arch pool', '%s, %s: OPEN closed at %s in the last round' % (_short(j['institutes'][high['i']]), {'AI': 'All India', 'HS': 'Home State', 'OS': 'Other State'}[high['q']], '{:,}'.format(_last(high['c'])))))
        mv = max(rows, key=lambda r: _last(r['c']) - _first(r['c']))
        f.append(('Biggest slide from Round 1', '%s %s %s: closing rank went from %s to %s as seats were freed' % (_short(j['institutes'][mv['i']]), 'B.Arch' if mv['p'] == 'A' else 'B.Planning', {'AI': 'All India', 'HS': 'Home State', 'OS': 'Other State'}[mv['q']], '{:,}'.format(_first(mv['c'])), '{:,}'.format(_last(mv['c'])))))
        pairs = {}
        for r in rows:
            pairs.setdefault((r['i'], r['p']), {})[r['q']] = _last(r['c'])
        hs_os = [(k, v['HS'], v['OS']) for k, v in pairs.items() if 'HS' in v and 'OS' in v]
        if hs_os:
            easier = sum(1 for k, h, o in hs_os if h > o)
            f.append(('Home State advantage', 'At %d of %d NIT and IIEST programmes, the Home State OPEN pool closed at a larger rank than the Other State pool' % (easier, len(hs_os))))
    dr = []
    for d in sorted(j['dasa'], key=lambda d: (d['f26'] or d['f25'] or 10 ** 9)):
        prog = 'B.Planning' if d['prog'].startswith('Planning (4') else 'B.Arch'
        if d['f25'] and d['f26']:
            ch = d['f26'] - d['f25']
            pct = round(100.0 * ch / d['f25'])
            cls, txt = ('up', 'Easier by %d%%' % pct) if ch > 0 else ('dn', 'Tougher by %d%%' % abs(pct)) if ch < 0 else ('', 'Same')
        else:
            cls, txt = '', ('2025 only' if d['f25'] else '2026 only')
        dr.append(dict(inst=d['inst'].replace('School of Planning & Architecture:', 'School of Planning & Architecture,'), prog=prog, quota=d['quota'].replace('DASA-', 'DASA '), f25=d['f25'], f26=d['f26'], change=txt, cls=cls))
    return dict(data=data, findings=f, n_rows=len(j['rows']), n_inst=len(j['institutes']), n_dasa=len(j['dasa']), dasa_rows=dr)
