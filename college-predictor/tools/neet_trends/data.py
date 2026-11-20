"""NEET UG 2023-2025 trend data: NEET score statistics, MBBS seat matrix, MCC seat allotment.
Every figure comes from a published source (named in SOURCES); figures that sources disagree on are listed in NOTES.
Edit here, then run:  python tools/neet_trends/build.py"""
YEARS = [2023, 2024, 2025]

SOURCES = [
    ('NEET 2023 results (NTA press release 13 Jun 2023)', 'https://medicaldialogues.in/pdf_upload/neet-ug-2023-results-211822.pdf'),
    ('NEET 2024 re-revised results (NTA press release 26 Jul 2024)', 'https://medicaldialogues.in/pdf_upload/neet-2024-re-revised-result-out-245312.pdf'),
    ('NEET 2025 highlights (Medical Dialogues, from the NTA notice)', 'https://medicaldialogues.in/amp/news/education/medical-admissions/neet-2025-highlights-check-out-results-toppers-key-statistics-150038'),
    ('NEET 2025 result (Careers360)', 'https://news.careers360.com/neet-result-2025-12-36-lakh-qualify-for-mbbs-bds-admission-up-performs-best-maharashtra-kota-bihar-tougher-lower-cut-off-link'),
    ('NEET 2025 marks vs rank (Careers360)', 'https://medicine.careers360.com/articles/neet-result-marks-vs-rank'),
    ('MBBS seats 2023-24 by state (Lok Sabha reply, Medical Dialogues)', 'https://medicaldialogues.in/news/education/108940-mbbs-70645-pg-medical-seats-in-india-maximum-medical-colleges-in-tamil-nadu-karnataka-offers-most-seats-123962'),
    ('MBBS seats 2024-25 by state (Lok Sabha reply, Aug 2025)', 'https://medicaldialogues.in/news/education/india-has-115900-mbbs-seats-across-780-medical-colleges-health-ministry-gives-breakup-152854'),
    ('MBBS seats 2025-26 by state (Lok Sabha reply, Dec 2025)', 'https://medicaldialogues.in/news/education/altogether-128875-mbbs-80291-pg-medical-seats-in-india-for-2025-26-health-minister-tells-parliament-160593'),
    ('MBBS seats 2021-22 to 2025-26 (NMC data via Lok Sabha, Apr 2026)', 'https://medicaldialogues.in/news/education/128976-mbbs-68175-pg-medical-seats-in-india-highest-in-karnataka-health-ministry-gives-breakup-in-parliament-167906'),
    ('Vacant UG seats in government colleges (Lok Sabha, 1 Aug 2025)', 'https://educationbytes.in/?p=40175'),
]

# ---- NEET score statistics -------------------------------------------------
HEADLINE = {  # registered, appeared, absent, qualified
    2023: (2087462, 2038596, 48866, 1145976),
    2024: (2406079, 2333297, 72782, 1315853),
    2025: (2276069, 2209318, 66751, 1236531),
}
CATEGORY = {  # (registered, appeared, qualified)
    2023: {'UR': (607131, 592110, 312405), 'EWS': (154373, 152197, 98322), 'OBC': (890150, 873173, 525194), 'SC': (303318, 294995, 153674), 'ST': (132490, 126121, 56381)},
    2024: {'UR': (647260, 625446, 333929), 'EWS': (190700, 186908, 116157), 'OBC': (1054277, 1026321, 618525), 'SC': (356727, 344309, 178741), 'ST': (157115, 150178, 68501)},
    2025: {'UR': (689366, 665853, 338728), 'EWS': (154326, 151586, 97085), 'OBC': (948507, 925739, 564611), 'SC': (333646, 322538, 168873), 'ST': (150224, 143602, 67234)},
}
GENDER = {  # registered, appeared, qualified
    2023: {'Male': (902936, 881967, 490374), 'Female': (1184513, 1156618, 655599), 'Third gender': (13, 11, 3)},
    2024: {'Male': (1029198, 998205, 546566), 'Female': (1376863, 1334940, 769277), 'Third gender': (18, 17, 10)},
    2025: {'Male': (965996, 937411, 514063), 'Female': (1310062, 1271896, 722462), 'Third gender': (11, 11, 6)},
}
CUTOFF = {  # class: (percentile, {year: (top of range, cut-off marks, candidates qualified in class)})
    'UR / EWS': (50, {2023: (720, 137, 1014372), 2024: (720, 162, 1165334), 2025: (686, 144, 1101151)}),
    'OBC': (40, {2023: (136, 107, 88592), 2024: (161, 127, 100876), 2025: (143, 113, 88692)}),
    'SC': (40, {2023: (136, 107, 29918), 2024: (161, 127, 34420), 2025: (143, 113, 31995)}),
    'ST': (40, {2023: (136, 107, 12437), 2024: (161, 127, 14414), 2025: (143, 113, 13940)}),
    'UR / EWS PwBD': (45, {2023: (136, 121, 405), 2024: (161, 144, 473), 2025: (143, 127, 472)}),
}
EXAM = {  # date, questions to attempt, centres, cities, candidates at AIR 1, top score
    2023: ('7 May 2023', 180, 4097, 499, 2, 720),
    2024: ('5 May 2024', 180, 4750, 571, 17, 720),
    2025: ('4 May 2025', 180, 5468, 552, 1, 686),
}
STATES = {  # (registered, appeared, qualified), top 10 states by qualified
    2023: {'Uttar Pradesh': (273572, 267383, 139961), 'Maharashtra': (277903, 273819, 131008), 'Rajasthan': (148364, 145824, 100316), 'Tamil Nadu': (147583, 144516, 78693), 'Kerala': (137396, 133450, 75362), 'Karnataka': (134381, 131318, 75248), 'Bihar': (121647, 118533, 64916), 'West Bengal': (104923, 102557, 59053), 'Gujarat': (79040, 73180, 49915), 'Madhya Pradesh': (104265, 102161, 49324)},
    2024: {'Uttar Pradesh': (344599, 334983, 165015), 'Maharashtra': (282051, 275442, 142829), 'Rajasthan': (178756, 174880, 121166), 'Tamil Nadu': (158449, 152919, 89198), 'Karnataka': (155148, 150170, 88887), 'Kerala': (144811, 136974, 86713), 'Bihar': (154461, 149494, 74716), 'West Bengal': (120070, 116104, 63251), 'Madhya Pradesh': (136098, 131525, 60065), 'Gujarat': (88022, 86410, 57232)},
    2025: {'Uttar Pradesh': (341491, 333088, 170684), 'Maharashtra': (248201, 242858, 125727), 'Rajasthan': (180637, 176181, 119865), 'Karnataka': (147782, 142369, 83582), 'Bihar': (164186, 159167, 80954), 'Tamil Nadu': (140158, 135715, 76181), 'Kerala': (127442, 121516, 73328), 'Madhya Pradesh': (121501, 118244, 60346), 'West Bengal': (110399, 106675, 59018), 'Gujarat': (81605, 80151, 50040)},
}
BANDS_2025 = [('144-200', 303040), ('201-250', 198346), ('251-300', 157952), ('301-350', 126935), ('351-400', 105578), ('401-450', 88239),
              ('451-500', 69503), ('501-550', 39521), ('551-600', 10658), ('601-650', 1259), ('651-686', 73)]
# Approximate All India Rank at a score (secondary sources; None = no reliable source found)
MARKS_RANK = {
    650: {2023: 7228, 2024: 27368, 2025: 77},
    600: {2023: 29348, 2024: 77972, 2025: 1300},
    550: {2023: None, 2024: 138178, 2025: 12000},
    500: {2023: 103769, 2024: 205888, 2025: 51500},
    450: {2023: 160895, 2024: 283571, 2025: 121000},
    400: {2023: None, 2024: 375396, 2025: 209000},
}

# ---- MBBS seat matrix ------------------------------------------------------
SEAT_TOTAL = {
    2023: {'seats': 109115, 'colleges': 706, 'govt_seats': 56300, 'pvt_seats': 52640, 'govt_colleges': 389, 'pvt_colleges': 317},
    2024: {'seats': 117756, 'colleges': 780, 'govt_seats': 60422, 'pvt_seats': 57715, 'govt_colleges': 431, 'pvt_colleges': 349},
    2025: {'seats': 128976, 'colleges': 818, 'govt_seats': 63682, 'pvt_seats': 65193, 'govt_colleges': 455, 'pvt_colleges': 363},
}
SEAT_HISTORY = {2021: 92065, 2022: 99463, 2023: 109115, 2024: 117756, 2025: 128976}   # academic year starting
VACANT_GOVT = {2021: 2012, 2022: 4146, 2023: 2959, 2024: 2849}   # UG seats vacant in government colleges, excluding AIIMS and JIPMER
STATE_SEATS = {  # state: (seats 23-24, 24-25, 25-26, colleges 23-24, 24-25, 25-26)
    'Andaman & Nicobar': (114, 114, 114, 1, 1, 1), 'Andhra Pradesh': (6485, 6785, 7215, 37, 38, 39), 'Arunachal Pradesh': (50, 100, 100, 1, 1, 1),
    'Assam': (1550, 1650, 1975, 13, 14, 16), 'Bihar': (2765, 2995, 3545, 21, 22, 25), 'Chandigarh': (150, 150, 150, 1, 1, 1),
    'Chhattisgarh': (2005, 2455, 2455, 14, 16, 16), 'Dadra & Nagar Haveli': (177, 177, 177, 1, 1, 1), 'Delhi': (1497, 1498, 1396, 10, 10, 11),
    'Goa': (180, 200, 200, 1, 1, 1), 'Gujarat': (7150, 7250, 7525, 40, 41, 43), 'Haryana': (2185, 2185, 2710, 15, 15, 17),
    'Himachal Pradesh': (920, 920, 970, 8, 8, 8), 'Jammu & Kashmir': (1339, 1347, 1676, 12, 12, 12), 'Jharkhand': (1055, 1055, 1255, 9, 9, 10),
    'Karnataka': (11745, 12396, 13944, 70, 73, 72), 'Kerala': (4655, 4755, 5404, 33, 34, 36), 'Madhya Pradesh': (4800, 5200, 5725, 27, 31, 35),
    'Maharashtra': (10845, 11846, 12824, 68, 80, 85), 'Manipur': (525, 525, 525, 4, 4, 4), 'Meghalaya': (50, 200, 200, 1, 2, 3),
    'Mizoram': (100, 100, 100, 1, 1, 1), 'Nagaland': (100, 100, 100, 1, 1, 1), 'Odisha': (2525, 2725, 3025, 17, 19, 21),
    'Puducherry': (1830, 1830, 1873, 9, 9, 9), 'Punjab': (1800, 1701, 1899, 12, 13, 13), 'Rajasthan': (5575, 6506, 7330, 35, 43, 49),
    'Sikkim': (150, 150, 150, 1, 1, 1), 'Tamil Nadu': (11650, 12050, 13050, 74, 77, 78), 'Telangana': (8490, 9065, 9540, 56, 65, 66),
    'Tripura': (225, 400, 450, 2, 3, 3), 'Uttar Pradesh': (9903, 12475, 13425, 68, 86, 88), 'Uttarakhand': (1150, 1350, 1450, 8, 10, 10),
    'West Bengal': (5275, 5501, 6499, 35, 38, 41),
}
STATE_SPLIT = {  # state: (govt 23-24, private 23-24, govt 25-26, private 25-26); the 2024-25 split was not published
    'Karnataka': (3750, 7995, 4249, 9695), 'Tamil Nadu': (5275, 6375, 5250, 7800), 'Uttar Pradesh': (4303, 5600, 5925, 7500),
    'Maharashtra': (5125, 5720, 6075, 6749), 'Telangana': (3890, 4600, 4390, 5150), 'Rajasthan': (3925, 1650, 4630, 2700),
    'Andhra Pradesh': (3235, 3250, 3415, 3800), 'Gujarat': (4250, 2900, 4325, 3200), 'Kerala': (1755, 2900, 1855, 3549),
    'West Bengal': (3825, 1450, 4149, 2250), 'Madhya Pradesh': (2400, 2400, 3025, 2700), 'Bihar': (1615, 1150, 1645, 1900),
}

NOTES = [
    '2024 registered: NTA 24,06,079 (one outlet prints 24,08,079, a typo). 2024 appeared 23,33,297 includes 135 unfair-means cases (23,33,162 without). 2024 qualified is the re-revised 13,15,853; the original 4 June result gave 13,16,268.',
    '2025 figures are taken from Careers360 and Medical Dialogues reproducing the NTA notice; the NTA 2025 press release itself was not retrieved. The 2025 score bands sum to 11,01,104 against 11,01,151 UR/EWS qualifiers.',
    'Marks versus rank figures are from news portals, not NTA, and are approximate. 2024 values may predate the 26 July 2024 re-revision.',
    'Seat totals differ by source and date: 2023-24 1,08,940 (Dec 2023 and Feb 2024 replies) or 1,09,115 (NMC data); 2024-25 1,18,137, 1,17,756, 1,17,750 or 1,15,900; 2025-26 1,28,875, 1,28,976 or 1,29,026. This report uses the NMC series 1,09,115 / 1,17,756 / 1,28,976. State rows are as published in the Parliament replies and do not add exactly to these totals.',
    'The 2025-26 government and private seat totals in the Dec 2025 reply are printed the wrong way round; the state rows (63,682 government, 65,193 private) are used here.',
    'The AIQ 15 per cent pool is not published as a separate series; the state-wise government and private split of 2024-25 was not found.',
]

# ---- MCC seat allotment (MBBS) -----------------------------------------------
# Counted by us from the official MCC result and vacancy PDFs (https://mcc.nic.in/archive-ug/); MCC does not publish these totals.
ROUNDS = ['Round 1', 'Round 2', 'Round 3', 'Stray', 'Special stray']
ALLOTTED = {  # MBBS seats allotted per round: (allotted, upgraded)
    2023: [(19848, 0), (9468, 1029), (6079, 2111), (1629, None), (157, None)],
    2024: [(21995, 0), (10776, 1158), (5748, 2447), (670, None), (74, None)],
    2025: [(22149, 0), (13571, 2295), (8333, 3533), (802, None), (66, None)],
}
OFFERED = {  # MBBS seats offered (clear + virtual vacancy); Round 1 not extracted; later rounds are lower bounds
    2023: [None, 14679, 12633, 1641, None],
    2024: [None, 15899, 13289, 677, 76],
    2025: [None, 17832, 13533, None, None],
}
QUOTA_MIX = {  # MBBS allotments by quota: (AIQ 15%, Deemed, NRI)
    2023: [(10072, 7643, 550), (6958, 2081, 272), (4592, 1184, 189)],
    2024: [(10425, 9103, 898), (7209, 3024, 391), (4690, 691, 252)],
    2025: [(10887, 9242, 540), (8004, 4897, 379), (5085, 2528, 268)],
}
R1_STATUS = {  # R1 MBBS seats as of the Round 2 file: reported, not reported, surrendered
    2023: (11574, 8051, 221), 2024: (13157, 8526, 306), 2025: (12257, 9659, 231),
}
# Last (closing) All India Rank, AIQ general category, final after all rounds: {college: {year: rank}}
CLOSING = {
    'AIIMS Delhi': {2023: 56, 2024: 47, 2025: 47}, 'MAMC Delhi': {2023: 87, 2024: 151, 2025: 103},
    'VMMC Safdarjung': {2023: 113, 2024: 141, 2025: 132}, 'UCMS Delhi': {2023: 304, 2024: 390, 2025: 559},
    'LHMC Delhi': {2023: 627, 2024: 826, 2025: 1129}, 'Seth GS Mumbai': {2023: 737, 2024: 1010, 2025: 1126},
    'JIPMER Puducherry': {2023: 269, 2024: 350, 2025: 260}, 'AIIMS Jodhpur': {2023: 534, 2024: 374, 2025: 392},
    'KGMU Lucknow': {2023: 2199, 2024: 2059, 2025: 2588}, 'AIIMS Raipur': {2023: 1369, 2024: 1180, 2025: 1376},
    'AIIMS Patna': {2023: 1944, 2024: 1476, 2025: 1939},
    'Kasturba Manipal (deemed)': {2023: 72304, 2024: 57207, 2025: 57121},
}
LAST_GOVT_GENERAL = {2023: 23674, 2024: 25124, 2025: 27332}     # last general-category AIR allotted a government AIQ MBBS seat, any round
LAST_GOVT_ANY = {2023: 169088, 2024: 168888, 2025: 164804}      # last any-category AIR (SC/ST/OBC included), government AIQ MBBS
LAST_GOVT_BY_ROUND = {  # government 15% AIQ, general category last AIR after each round
    2023: [19396, 22104, 22636, 23562, 23674], 2024: [19603, 22995, 24842, 25032, 25124], 2025: [21190, 24940, 26072, 27332, 27095],
}
LAST_DEEMED = {2023: 1221896, 2024: 1332973, 2025: 918801}      # last AIR in deemed/paid quota, any category; 2023-24 not validated

NOTES += [
    'MCC allotment counts are our own count of MBBS rows in the official MCC result PDFs; MCC publishes no such totals. Round 1 seats offered, seats left vacant at the end, and joined/resigned counts per round are not in MCC files and are not shown. Upgrades are the MCC remark Upgraded.',
    'Closing ranks are the highest All India Rank among non-PwD General candidates holding an Open-category MBBS seat in the 15% AIQ (Open Seat Quota for AIIMS and JIPMER) after the stray rounds. Colleges with few general seats in the AIQ (Seth GS, KGMU) swing a lot between rounds. Deemed ranks run into lakhs and the 2023 and 2024 deemed last ranks are not validated.',
    'Round 3 seats offered are the initial matrix and a lower bound; seats were added later. 2025 special-stray offered seats were not found.',
]
