"""TNEA (Tamil Nadu Engineering Admissions, DOTE Chennai): facts behind /tnea-analytics, checked 22 Nov 2026.

Cut-offs are in app/data/tnea/cutoffs.json, built by tools/tnea/build_cutoffs.py from the official TNEA 2026 Round 1, 2 and 3 general academic
allotment lists (closing aggregate mark and rank per college, branch and allotted community) and the official vacancy list after Round 1
(college and branch names). The official cut-off site (cutoff.tneaonline.org) was not reachable in Nov 2026, so earlier years could not be re-checked:
the 2025 column comes from the portal's own "TNEA 2025 Final Cutoff" sheet and is labelled as such on the page.
Update this file when DOTE publishes the TNEA 2027 schedule or information brochure.
"""

VERIFIED = '22 Nov 2026'
O, R, E = 'Official', 'Reported', 'Expected'

SRC = {
    'tnea': 'https://www.tneaonline.org/',
    'schedule': 'https://static.tneaonline.org/docs/2026_tentative_schedule.pdf',
    'cutoff': 'https://cutoff.tneaonline.org/',
    'dge': 'https://dge.tn.gov.in/',
}

# (id, title, start, end, status, detail). 2027 rows follow the official 2026 schedule until DOTE announces 2027.
DATES = [
    ('hsc-prac', 'TN +2 (HSC) practical exams', '2027-02-08', '2027-02-18', O, 'DGE Tamil Nadu timetable released 14 Oct 2026; schools fix the exact day.'),
    ('hsc-theory', 'TN +2 (HSC) public exams, theory', '2027-03-03', '2027-03-29', O, 'DGE timetable. Mathematics, Physics and Chemistry make your TNEA cut-off, so these papers decide your rank.'),
    ('hsc-result', 'TN +2 results', '2027-05-07', '2027-05-07', E, 'Reported tentative date; DGE confirms closer to the time.'),
    ('apply', 'TNEA 2027 online registration and certificate upload', '2027-05-03', '2027-06-05', E, 'In 2026 registration opened on 3 May and closed on 5 Jun (official schedule). Apply only on tneaonline.org.'),
    ('random', 'Random number assigned', '2027-06-10', '2027-06-10', E, 'Used only to break ties between candidates with the same cut-off, after Mathematics, Physics and date of birth (10 Jun in 2026).'),
    ('verify', 'Online certificate verification at TNEA Facilitation Centres', '2027-06-08', '2027-06-29', E, '8–29 Jun in 2026.'),
    ('rank', 'TNEA rank list', '2027-07-01', '2027-07-01', E, 'Published on 1 Jul in 2026; grievances could be raised until 6 Jul.'),
    ('special', 'Special reservation counselling (differently abled, ex-servicemen, sports)', '2027-07-13', '2027-07-18', E, 'Govt school 7.5% special categories on 13–14 Jul and general special categories on 15–18 Jul in 2026.'),
    ('general', 'General counselling: academic, Govt school 7.5% and vocational, three rounds', '2027-07-20', '2027-08-30', E, '20 Jul – 30 Aug in 2026. Each round invites a band of cut-off marks; see the round table below.'),
    ('supp', 'Supplementary and SCA-to-SC counselling', '2027-09-01', '2027-09-10', E, 'Dates are announced after the +2 supplementary exam results.'),
]

# official 2026 rounds of general academic counselling: (round, cut-off from, cut-off to, rank from, rank to, allotment date)
ROUNDS_2026 = [
    (1, 200.0, 171.333, 1, 37976, '3 Aug 2026'),
    (2, 171.0, 135.75, 37977, 131093, '17 Aug 2026'),
    (3, 135.5, 77.5, 131094, 233812, '31 Aug 2026'),
]
RANKLIST_2026 = 233812   # last rank invited to general academic counselling in 2026 (official schedule)

PATTERN = [
    ('No entrance exam', 'TNEA ranks you on your Class 12 marks alone: there is no separate test.'),
    ('Cut-off out of 200', 'Mathematics (out of 100) + Physics/2 + Chemistry/2. Mathematics counts as much as Physics and Chemistry together.'),
    ('Ties', 'Equal cut-offs are separated by the Mathematics mark, then Physics, then the fourth optional subject, then date of birth (older first), then the random number.'),
    ('Rounds', 'General academic counselling runs in three rounds by cut-off band. You pay the fee, fill choices, see a tentative allotment and then confirm.'),
    ('Confirming a seat', 'Accept and join; accept and ask for an upward move; decline and ask for an upward move; or decline and move to the next round. Not confirming in time costs you the seat.'),
    ('Govt school 7.5%', 'Students who studied Class 6 to 12 in Tamil Nadu government schools have 7.5% of seats set aside for them, with fees paid by the state.'),
]

ELIGIBILITY = [
    ('Subjects', 'Pass +2 (HSC or an equivalent board) with Mathematics, Physics and Chemistry. The information brochure lists allowed substitutes for Chemistry.'),
    ('Minimum marks', 'At least 45% in Mathematics, Physics and Chemistry together for OC; 40% for BC, BCM, MBC/DNC, SC, SCA and ST (TNEA 2026 information brochure as summarised; check the 2027 brochure).'),
    ('Who can apply', 'Tamil Nadu candidates as defined in the information brochure (by nativity or by study in Tamil Nadu). Candidates from other states should read the brochure\'s rules before applying.'),
    ('Community certificate', 'Upload a permanent community certificate issued by Tamil Nadu: without it you are counted as OC.'),
    ('First graduate', 'If no one in your family has a degree, you can claim the first-graduate tuition fee concession (certificate needed).'),
    ('Vocational stream', 'Students from the +2 vocational stream have a separate rank list and seat share.'),
]

# communities as allotted in TNEA, with the Tamil Nadu reservation share (69% reservation)
COMMS = [
    ('OC', 'Open competition', '31%', 'Open to everyone in merit order, whatever their community'),
    ('BC', 'Backward Class', '26.5%', 'Backward Classes other than Muslims'),
    ('BCM', 'Backward Class Muslim', '3.5%', ''),
    ('MBC', 'Most Backward Class and Denotified Communities', '20%', 'Includes MBC(V) and DNC'),
    ('SC', 'Scheduled Caste', '15%', ''),
    ('SCA', 'Scheduled Caste (Arunthathiyar)', '3%', 'Unfilled SCA seats go to SC in the SCA-to-SC round'),
    ('ST', 'Scheduled Tribe', '1%', ''),
]
RESERVATION_NOTE = ('Every candidate is first considered for an OC seat in merit order; a reserved candidate who misses OC is then considered for their own '
                    'community\'s seats. That is why the community closing mark is usually lower than the OC one. The 7.5% Govt school share runs '
                    'within each community.')

# college type keys: from the type column of the 2025 sheet; colleges new in 2026 are 'N'
TYPES = {
    'U': ('Anna University and university colleges', 'CEG, ACT, MIT, SAP and the university constituent and regional campus colleges, plus Annamalai University: low fees'),
    'G': ('Government and aided', 'Government engineering colleges, government-aided colleges and central institutes such as CIPET and CECRI: the lowest fees'),
    'T1': ('Self-financing, Tier 1', 'Tier as given in the TNEA cut-off data: the smallest group, mostly long-established autonomous colleges'),
    'T2': ('Self-financing, Tier 2', 'Tier 2 in the TNEA cut-off data'),
    'T3': ('Self-financing, Tier 3', 'Tier 3 in the TNEA cut-off data: most private colleges'),
    'N': ('Self-financing, new in 2026', 'Colleges first in counselling in 2026'),
}
TYPE_OF = {'CEG DEPTS': 'U', 'UNIV CONSTITUENT COLLEGES': 'U', 'ANNAMALAI UNIV': 'U', 'GOVERNMENT ENGG COLLEGES': 'G', 'GOVERNMENT AIDED COLLEGES': 'G',
           'CENTRAL GOVERNMENT ENGG COLLEGES COLLEGES': 'G', 'SELF FINANCING COLLEGES TIER 1': 'T1', 'SELF FINANCING COLLEGES TIER 2': 'T2',
           'SELF FINANCING COLLEGES TIER 3': 'T3', '': 'N'}

# NIRF India Rankings 2025, Engineering (app/data/files/nirf_full.json), for colleges in TNEA counselling. Anna University is ranked as one university.
NIRF = {1: '20 (Anna Univ.)', 2: '20 (Anna Univ.)', 3: '20 (Anna Univ.)', 4: '20 (Anna Univ.)', 2006: '67', 2718: '100',
        1399: '101–150', 2007: '101–150', 1304: '101–150', 2711: '101–150', 2764: '101–150', 2377: '101–150', 1211: '101–150', 5008: '101–150',
        2712: '151–200', 4960: '151–200', 1113: '151–200', 2618: '151–200', 2719: '151–200', 1419: '151–200',
        5: '201–300', 3806: '201–300', 2708: '201–300', 3830: '201–300', 3701: '201–300', 2750: '201–300', 2710: '201–300', 2608: '201–300',
        4962: '201–300', 1210: '201–300', 1414: '201–300', 5910: '201–300', 1128: '201–300', 1112: '201–300', 1432: '201–300', 2329: '201–300',
        1216: '201–300', 2726: '201–300', 2739: '201–300', 1219: '201–300', 1149: '201–300', 1317: '201–300'}
NIRF_NOT_TNEA = ['IIT Madras (1, JEE Advanced)', 'NIT Tiruchirappalli (9, JEE Main via JoSAA)', 'SRM Institute of Science and Technology (14, own exam)',
                 'Vellore Institute of Technology (16, VITEEE)', 'Amrita Vishwa Vidyapeetham (23, own exam)', 'Kalasalingam (33), SASTRA (40), Saveetha Institute (45), Sathyabama (67) and other deemed universities: own admissions',
                 'Sri Sivasubramaniya Nadar (SSN) College of Engineering (47): not in the TNEA 2026 allotment lists']

FAMILY_NAMES = {'CSE': 'Computer / CSE', 'AI': 'AI, ML & Data Science', 'IT': 'Information Technology', 'ENTC': 'Electronics & Communication', 'ELEC': 'Electrical',
                'MECH': 'Mechanical & allied', 'CIVIL': 'Civil', 'CHEM': 'Chemical, bio, food & textile', 'OTHER': 'Architecture, design & other'}

BRANCH_GUIDE = [
    ('CSE', 'The highest cut-offs at nearly every college: in 2026, Computer Science at CEG closed at 200 for OC. A Computer seat at a middle college and Electronics at a top college are often open to the same mark.'),
    ('AI', 'AI & Data Science and the CSE specialisations (AI & ML, Cyber Security, IoT) now run at most private colleges and close just behind CSE.'),
    ('ENTC', 'Electronics and Communication keeps hardware and software routes open; at Anna University and the top government colleges it closes within a few marks of CSE.'),
    ('ELEC', 'Electrical and Electronics suits power, energy, TANGEDCO and PSU careers; it closes several marks after CSE and ECE.'),
    ('MECH', 'Mechanical, Automobile and Production are core branches with lower cut-offs: a way into a top government college for marks that miss CSE there.'),
    ('CIVIL', 'Civil usually has the lowest cut-off at a college: a route into CEG, GCT Coimbatore or a government college for public works and government jobs.'),
]

# district of the colleges new in 2026 (no row in the 2025 sheet), from the address in the official name
NEW_DISTRICT = {1111: 'Chennai', 1121: 'Thiruvallur', 2323: 'Tiruppur', 2368: 'Coimbatore', 2378: 'Tiruppur', 3555: 'Cuddalore', 3838: 'Thanjavur',
                4747: 'Tenkasi', 4911: 'Kanyakumari', 4979: 'Virudhunagar', 5924: 'Ramanathapuram'}
# district spellings in the 2025 sheet -> district names in the map file (Mayiladuthurai is not a separate district in the map file)
DISTRICT_FIX = {'CHENGALPET': 'Chengalpattu', 'MAYILADUTHURAI': 'Nagapattinam', 'THE NILGIRIS': 'Nilgiris', 'SIVAGANGAI': 'Sivaganga', 'THIRUPATHUR': 'Tirupathur',
                'THIRUVANNAMALAI': 'Tiruvannamalai', 'TIRUCHIRAPALLI': 'Tiruchirappalli', 'TRICHIRAPPALLI': 'Tiruchirappalli', 'TUTICORIN': 'Thoothukkudi'}
REGIONS = {
    'North (Chennai belt)': ['Chennai', 'Thiruvallur', 'Chengalpattu', 'Kancheepuram', 'Vellore', 'Ranipet', 'Tirupathur', 'Tiruvannamalai', 'Viluppuram', 'Kallakurichi', 'Cuddalore'],
    'West (Kongu)': ['Coimbatore', 'Tiruppur', 'Erode', 'Salem', 'Namakkal', 'Nilgiris', 'Dharmapuri', 'Krishnagiri', 'Karur'],
    'Central (Delta)': ['Tiruchirappalli', 'Thanjavur', 'Thiruvarur', 'Nagapattinam', 'Pudukkottai', 'Perambalur', 'Ariyalur'],
    'South': ['Madurai', 'Dindigul', 'Theni', 'Sivaganga', 'Ramanathapuram', 'Virudhunagar', 'Thoothukkudi', 'Tirunelveli', 'Tenkasi', 'Kanyakumari'],
}

# short names for colleges whose official name has no comma (address runs on)
SHORT = {1: 'CEG Campus, Anna University (Guindy)', 2: 'ACT Campus, Anna University (Guindy)', 3: 'School of Architecture and Planning, Anna University',
         4: 'MIT Campus, Anna University (Chromepet)', 5: 'Annamalai University, Faculty of Engineering', 1013: 'University College of Engineering, Villupuram',
         1014: 'University College of Engineering, Tindivanam', 1015: 'University College of Engineering, Arni', 1026: 'University College of Engineering, Kancheepuram',
         1321: 'CIPET, Guindy (Central Institute of Petrochemicals Engg & Tech)', 1399: 'Chennai Institute of Technology', 1516: 'Thanthai Periyar Govt Institute of Technology, Vellore',
         2005: 'Government College of Technology (GCT), Coimbatore', 2006: 'PSG College of Technology, Coimbatore', 2007: 'Coimbatore Institute of Technology (CIT)',
         2025: 'Anna University Regional Campus, Coimbatore', 2343: 'Indian Institute of Handloom Technology, Salem', 2350: 'Jairupa College of Engineering',
         2369: 'Government College of Engineering, Dharmapuri', 2603: 'Government College of Engineering, Bargur', 2615: 'Government College of Engineering, Salem',
         2709: 'Government College of Engineering, Erode (IRTT)', 3011: 'University College of Engineering, Tiruchirappalli (BIT Campus)',
         3016: 'University College of Engineering, Ariyalur', 3018: 'University College of Engineering, Thirukkuvalai', 3019: 'University College of Engineering, Panruti',
         3021: 'University College of Engineering, Pattukkottai', 3464: 'Government College of Engineering, Thanjavur', 3465: 'Government College of Engineering, Srirangam',
         3795: 'SRM TRP Engineering College, Tiruchirappalli', 4020: 'Anna University Regional Campus, Tirunelveli', 4023: 'University College of Engineering, Nagercoil',
         4024: 'University V.O.C. College of Engineering, Thoothukudi', 4964: 'PSN College of Engineering and Technology, Tirunelveli',
         4974: 'Government College of Engineering, Tirunelveli', 5008: 'Thiagarajar College of Engineering, Madurai', 5009: 'Government College of Engineering, Bodinayakkanur',
         5010: 'Anna University Regional Campus, Madurai', 5012: 'CECRI, Karaikudi (Central Electrochemical Research Institute)', 5017: 'University College of Engineering, Ramanathapuram',
         5022: 'University College of Engineering, Dindigul', 5901: 'Alagappa Chettiar Govt College of Engg & Tech, Karaikudi',
         1111: 'Rajalakshmi Engineering College (Off Campus), Perungudi', 1203: 'Madras Engineering College'}

# official college websites, keyed by TNEA college code (none collected yet)
SITES = {}
