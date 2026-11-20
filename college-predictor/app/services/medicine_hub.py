"""Medicine exam pages: one registry used by the site menu ("Medicine" tab), the /medicine overview page and Member Home.

To add a medicine exam page (NEET PG, AIIMS nursing, state paramedical entrances, ...): build the page, then add ONE entry to PAGES.
The menu and the overview page update on their own. Also add a Member Home tile for it in the "medicine" category of services/member_hub.py
(tests/test_portal_guide.py fails if a page listed here has no Member Home tile) and describe it in services/portal_guide.py.
"""
PAGES = [
    {'title': 'NEET UG 2027', 'endpoint': 'main.neet_2027', 'tag': 'MBBS · BDS · AYUSH · B.Sc. Nursing',
     'desc': 'What NTA has and has not announced, recent exam dates, pattern, eligibility, counselling and a month-by-month preparation plan.', 'status': 'Guide live'},
    {'title': 'NEET Papers Analysed', 'endpoint': 'main.neet_exam', 'tag': 'NEET UG · past papers',
     'desc': 'Past NEET question papers analysed chapter by chapter: what is asked most, marks by subject and topic trends.', 'status': 'Analysis live'},
    {'title': 'NEET MBBS Seat Analytics', 'endpoint': 'main.neet_seats_2025', 'tag': 'MBBS · seats · colleges', 'premium': True,
     'desc': 'All MBBS colleges in the NMC seat matrix for 2025-26: seats by state and management, new colleges, seat cuts and a college explorer.', 'status': 'Members'},
    {'title': 'NIRF Medical Ranking Analytics', 'endpoint': 'main.nirf_medical', 'tag': 'NIRF 2026 · top 50 medical institutes',
     'desc': 'The NIRF top 50 medical institutes taken apart: scores on the five parameters, top 10, state view and side-by-side compare.', 'status': 'Analysis live'},
    {'title': 'NIRF Pharmacy Ranking Analytics', 'endpoint': 'main.nirf_pharmacy', 'tag': 'NIRF 2026 · top 100 pharmacy institutes',
     'desc': 'The NIRF top 100 pharmacy institutes taken apart: parameter scores, heatmap, the seven NIPERs, state view and side-by-side compare.', 'status': 'Analysis live'},
    {'title': 'NEET 2023-2025 Trends', 'endpoint': 'main.neet_trends', 'tag': 'scores · MBBS seats · MCC allotment',
     'desc': 'Three years of NEET UG side by side: candidates and cut-offs, MBBS seats by state, MCC allotment by round and college closing ranks, with an Excel download.', 'status': 'Analysis live'},
]
