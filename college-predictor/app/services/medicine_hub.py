"""Medicine exam pages: one registry used by the site menu ("Medicine" tab), the /medicine overview page and Member Home.

To add a medicine exam page (NEET PG, AIIMS nursing, state paramedical entrances, ...): build the page, then add ONE entry to PAGES.
The menu and the overview page update on their own. Also add a Member Home tile for it in the "medicine" category of services/member_hub.py
(tests/test_portal_guide.py fails if a page listed here has no Member Home tile) and describe it in services/portal_guide.py.
"""
PAGES = [
    {'title': 'NEET UG 2027', 'endpoint': 'main.neet_2027', 'tag': 'MBBS · BDS · AYUSH · B.Sc. Nursing',
     'desc': 'What NTA has and has not announced, recent exam dates, pattern, eligibility, counselling and a month-by-month preparation plan.', 'status': 'Guide live'},
]
