"""Member Home registry: categories -> tiles.

To add a feature, append a tile dict to a category (or add a category). Fields:
  title, desc, icon (emoji), endpoint (+ optional anchor),
  access: 'free' (any member) | 'premium' | 'soon' (placeholder, not clickable).
Tiles whose endpoint does not exist are skipped, so a removed page never breaks the hub.
"""
from datetime import date

from flask import url_for

CATEGORIES = [
    {'key': 'journey', 'title': 'My Journey', 'icon': '🧭', 'color': '#2563EB', 'tint': '#EAF1FF',
     'blurb': 'Your profile, sessions, documents and assessments.',
     'tiles': [
         {'title': 'Profile & sessions', 'desc': 'Counselling sessions and notes from your mentor.', 'icon': '👤', 'endpoint': 'members.profile', 'access': 'free'},
         {'title': 'Document verification', 'desc': 'Upload and track the documents requested from you.', 'icon': '📎', 'endpoint': 'members.profile', 'anchor': 'documents', 'access': 'free'},
         {'title': 'My assessments', 'desc': 'Every assessment result, shared with your mentor.', 'icon': '📝', 'endpoint': 'members.profile', 'anchor': 'assessments', 'access': 'free'},
         {'title': 'Stream selection', 'desc': 'Find the stream that fits your strengths.', 'icon': '🎯', 'endpoint': 'main.stream_selection', 'access': 'premium'},
     ]},
    {'key': 'mentorship', 'title': 'Mentorship Portal', 'icon': '🎯', 'color': '#EA580C', 'tint': '#FFEBDD',
     'blurb': 'Sessions, weekly plan, KPIs, branch fit, college preferences and your progress report.',
     'tiles': [
         {'title': 'My Mentorship', 'desc': 'Your journey, weekly plan, KPIs, reviews and reports (students and parents).', 'icon': '🧑\u200d🏫', 'endpoint': 'mentorship.index', 'access': 'premium'},
         {'title': 'Add-on programmes', 'desc': 'Ready-made mentoring for UCEED, NID, NIFT, IIT Delhi–Abu Dhabi, TNEA, state colleges, SRM, Amrita and VIT.', 'icon': '🧩', 'endpoint': 'mentorship.addons', 'access': 'free'},
         {'title': 'FutureReady (Class 8–9)', 'desc': 'Mentorship for Class 8–9 students: assessments, engineering exploration, action plan and reports.', 'icon': '🚀', 'endpoint': 'futureready.index', 'access': 'free'},
         {'title': 'Action tracker', 'desc': 'Meeting actions for every member: owner, due date, completion — share by email or WhatsApp.', 'icon': '📌', 'endpoint': 'mentorship.action_tracker', 'access': 'premium', 'staff': True},
         {'title': 'Mentor dashboard', 'desc': 'Assigned students, sessions, follow-ups and interventions.', 'icon': '📋', 'endpoint': 'mentorship.mentor_home', 'access': 'premium', 'staff': True},
     ]},
    {'key': 'intel', 'title': 'Admission Intelligence', 'icon': '📊', 'color': '#D97706', 'tint': '#FFF3DD',
     'blurb': 'Latest analytics and reports for the 2026–27 cycle.',
     'tiles': [
         {'title': 'DASA 2026 Analytics', 'desc': 'Round-wise closing-rank analytics.', 'icon': '📈', 'endpoint': 'main.dasa_2026_analytics', 'access': 'premium'},
         {'title': 'DASA prediction report', 'desc': 'Personalised DASA / CIWG outlook.', 'icon': '🔮', 'endpoint': 'main.dasa_prediction_report', 'access': 'premium'},
         {'title': 'JoSAA EA members', 'desc': 'Members-only JoSAA insights.', 'icon': '🇮🇳', 'endpoint': 'main.josaa_ea_members', 'access': 'premium'},
         {'title': 'UCEED 2027 Roadmap', 'desc': 'Design-entrance plan, planner and B.Des admission guide.', 'icon': '✏️', 'endpoint': 'main.uceed_2027_roadmap', 'access': 'premium'},
         {'title': 'Law Entrance 2027 Roadmap', 'desc': 'CLAT, AILET and SLAT plan, planner and law-school guide.', 'icon': '⚖️', 'endpoint': 'main.law_2027_roadmap', 'access': 'premium'},
         {'title': 'IPM 2027 Roadmap', 'desc': 'IIM five-year IPM: IPMAT, JIPMAT, planner and admission steps.', 'icon': '🏫', 'endpoint': 'main.ipm_2027_roadmap', 'access': 'premium'},
         {'title': 'JEE 2027 Roadmap', 'desc': 'The exam process, mapped step by step.', 'icon': '🗺️', 'endpoint': 'main.jee_2027_roadmap', 'access': 'premium'},
         {'title': 'TNEA expert', 'desc': 'Tamil Nadu engineering counselling guide.', 'icon': '🎓', 'endpoint': 'main.tnea_expert', 'access': 'premium'},
         {'title': 'Members report', 'desc': 'Reports prepared for members.', 'icon': '📑', 'endpoint': 'main.members_report', 'access': 'premium'},
     ]},
    {'key': 'edupulse', 'title': 'EduPulse AI Tools', 'icon': '🧠', 'color': '#EA580C', 'tint': '#FFEBDD',
     'blurb': 'Daily reinforcement, mock tests and previous-year papers with a confidence check on every answer.',
     'tiles': [
         {'title': 'EduPulse – Reinforcement', 'desc': 'Short daily practice from your mentor with a confidence check on every answer.', 'icon': '🔁', 'endpoint': 'reinforce.home', 'access': 'premium'},
         {'title': 'EduPulse-UCEED', 'desc': 'Chapter-wise MCQ practice with progress reports for you, your parent and mentor.', 'icon': '🎯', 'endpoint': 'pulse.home', 'access': 'premium'},
         {'title': 'UCEED Mock Test Centre', 'desc': 'Previous-year papers 2018–2026 and EduAakashaA mocks, timed or practice, with a confidence check and reports.', 'icon': '📝', 'endpoint': 'pulse.mock_home', 'access': 'premium'},
         {'title': 'EduPulse-JEE Mock Test Centre', 'desc': 'JEE Main mocks in the 2027 pattern with a confidence check, negative-marking tracker and reports.', 'icon': '🧮', 'endpoint': 'pulse_jee.home', 'access': 'premium'},
         {'title': 'Reinforcement mentor view', 'desc': 'Assign daily practice, see chapter-wise strengths and confidence patterns, approve next steps.', 'icon': '🧭', 'endpoint': 'reinforce.mentor_home', 'access': 'premium', 'staff': True},
         {'title': 'EduPulse mentor view', 'desc': 'Progress of students practising UCEED.', 'icon': '📈', 'endpoint': 'pulse.mentor_home', 'access': 'premium', 'staff': True},
     ]},
    {'key': 'gulf', 'title': 'Engineering in Gulf', 'icon': '🌴', 'color': '#0F766E', 'tint': '#E0F5F1', 'img': 'gulf.svg',
     'blurb': 'Routes, exams and guides for studying engineering in the UAE and the Gulf.',
     'tiles': [
         {'title': 'CAET · IIT Delhi – Abu Dhabi guide', 'desc': 'Eligibility checker, deadlines, pattern, practice paper, fees, seats, cut-offs and checklist.', 'icon': '🏛️', 'endpoint': 'main.gulf_caet_guide', 'access': 'premium'},
         {'title': 'IIT Delhi – Abu Dhabi mentoring', 'desc': 'Ready-made add-on programme: route check, CAET preparation, documents and decision.', 'icon': '🧑‍🏫', 'endpoint': 'mentorship.addons', 'anchor': 'iitd-ad', 'access': 'free'},
         {'title': 'DASA 2026 Analytics', 'desc': 'Round-wise closing-rank analytics for the DASA / CIWG route.', 'icon': '📈', 'endpoint': 'main.dasa_2026_analytics', 'access': 'premium'},
         {'title': 'NRI admission guide', 'desc': 'DASA, CIWG and NRI routes.', 'icon': '🌍', 'endpoint': 'main.nri_guide', 'access': 'free'},
     ]},
    {'key': 'tools', 'title': 'Choice-Filling Tools', 'icon': '🛠️', 'color': '#059669', 'tint': '#E3F7EF',
     'blurb': 'Simulate and personalise your choice list.',
     'tiles': [
         {'title': 'Choice Builder Simulator', 'desc': 'Build and test your choice-filling order.', 'icon': '🧩', 'endpoint': 'main.choice_builder_pro', 'access': 'premium'},
     ]},
    {'key': 'insights', 'title': 'Engineering Insights', 'icon': '💡', 'color': '#7C3AED', 'tint': '#F0EAFE',
     'blurb': 'Branch, location and campus-life analytics.',
     'tiles': [
         {'title': 'Why CSE?', 'desc': 'Branch demand and outcomes.', 'icon': '💻', 'endpoint': 'main.why_cse', 'access': 'premium'},
         {'title': 'Best location', 'desc': 'Compare cities and campuses.', 'icon': '📍', 'endpoint': 'main.best_location', 'access': 'premium'},
         {'title': 'Engineering insights', 'desc': 'Data-backed college insights.', 'icon': '🔬', 'endpoint': 'main.engineering_insights', 'access': 'premium'},
         {'title': 'Hostel & culture', 'desc': 'Campus life analytics.', 'icon': '🏠', 'endpoint': 'main.hostel_culture_analytics', 'access': 'premium'},
         {'title': 'Branch selection guide', 'desc': 'Choose the right branch.', 'icon': '🧠', 'endpoint': 'main.engineering_branch_selection_guide', 'access': 'premium'},
     ]},
    {'key': 'free', 'title': 'Free Resources', 'icon': '🎁', 'color': '#0891B2', 'tint': '#E0F5FA',
     'blurb': 'Open to every member.',
     'tiles': [
         {'title': 'Free student guides', 'desc': 'Download guides by email.', 'icon': '📥', 'endpoint': 'guides.library', 'access': 'free'},
         {'title': 'Exam schedule', 'desc': 'Key exam and counselling dates.', 'icon': '🗓️', 'endpoint': 'main.exam_schedule', 'access': 'free'},
         {'title': 'NRI admission guide', 'desc': 'DASA, CIWG and NRI routes.', 'icon': '🌍', 'endpoint': 'main.nri_guide', 'access': 'free'},
     ]},
    {'key': 'support', 'title': 'Support & Membership', 'icon': '🤝', 'color': '#DB2777', 'tint': '#FDE8F2',
     'blurb': 'Talk to us or manage your plan.',
     'tiles': [
         {'title': 'Portal guide', 'desc': 'Step-by-step instructions for members, parents, mentors and admins.', 'icon': '📖', 'endpoint': 'portal_guide.index', 'access': 'free'},
         {'title': 'Contact the team', 'desc': 'info@eduaakashaa.com · +91-80157 22706', 'icon': '✉️', 'endpoint': 'main.contact_alias', 'access': 'free'},
         {'title': 'Membership plans', 'desc': 'Upgrade or renew your access.', 'icon': '★', 'endpoint': 'main.members_registration', 'access': 'free'},
         {'title': 'More tools coming soon', 'desc': 'New member features land here.', 'icon': '✨', 'endpoint': None, 'access': 'soon'},
     ]},
]


# ---- presentation metadata for the dashboard (icons, labels, "New" window). Not business logic: access rules stay in each tile's `access`. ----
CATEGORY_ICON = {'journey': 'route', 'mentorship': 'cap', 'intel': 'bar', 'edupulse': 'target', 'gulf': 'globe', 'tools': 'sliders', 'insights': 'bulb', 'free': 'download', 'support': 'life-buoy'}
TILE_ICON = {
    'Profile & sessions': 'user', 'Document verification': 'file-check', 'My assessments': 'clipboard', 'Stream selection': 'compass',
    'My Mentorship': 'cap', 'Add-on programmes': 'puzzle', 'FutureReady (Class 8–9)': 'compass', 'Action tracker': 'check-square', 'Mentor dashboard': 'dashboard',
    'DASA 2026 Analytics': 'bar', 'DASA prediction report': 'trend', 'JoSAA EA members': 'users', 'EduPulse-UCEED': 'target', 'EduPulse mentor view': 'dashboard', 'EduPulse – Reinforcement': 'target', 'Reinforcement mentor view': 'dashboard',
    'EduPulse-JEE Mock Test Centre': 'calculator', 'UCEED Mock Test Centre': 'clipboard', 'UCEED 2027 Roadmap': 'map', 'Law Entrance 2027 Roadmap': 'scale', 'IPM 2027 Roadmap': 'briefcase', 'JEE 2027 Roadmap': 'map', 'TNEA expert': 'book', 'Members report': 'file-text',
    'IIT Delhi – Abu Dhabi mentoring': 'cap', 'NRI admission guide': 'globe', 'Choice Builder Simulator': 'sliders',
    'Why CSE?': 'code', 'Best location': 'pin', 'Engineering insights': 'bulb', 'Hostel & culture': 'home', 'Branch selection guide': 'branch',
    'Free student guides': 'download', 'Exam schedule': 'calendar', 'Contact the team': 'mail', 'Membership plans': 'star', 'Portal guide': 'book', 'More tools coming soon': 'sparkle',
}
# tiles added recently show a "New" label for 30 days after this date (real dates, no fabricated badges)
NEW_SINCE = {'IPM 2027 Roadmap': date(2026, 10, 18), 'Add-on programmes': date(2026, 10, 19), 'Action tracker': date(2026, 10, 20),
             'IIT Delhi – Abu Dhabi mentoring': date(2026, 10, 21), 'FutureReady (Class 8–9)': date(2026, 10, 23), 'UCEED Mock Test Centre': date(2026, 10, 24), 'EduPulse-JEE Mock Test Centre': date(2026, 10, 25), 'EduPulse – Reinforcement': date(2026, 10, 25)}
NEW_DAYS = 30


def _norm(x):
    return x.replace('–', '-').replace('—', '-').replace('�', '-')


_ICON_N = {_norm(k): v for k, v in TILE_ICON.items()}
_NEW_N = {_norm(k): v for k, v in NEW_SINCE.items()}


def _decorate(t, today=None):
    """Icon, type tag, action label and New flag for one resolved tile."""
    today = today or date.today()
    title = t['title']
    low = title.lower()
    key = _norm(title)
    t['ic'] = _ICON_N.get(key) or ('cap' if 'mentoring' in low else ('book' if 'guide' in low else 'grid'))
    if 'CAET' in title:
        t['ic'] = 'building'
    t['tag'] = 'roadmap' if 'roadmap' in low else ('report' if ('report' in low or 'assessment' in low) else '')
    if t['access'] == 'soon':
        t['action'] = 'Coming soon'
    elif t.get('locked'):
        t['action'] = 'Unlock with membership'
    elif t['tag'] == 'roadmap':
        t['action'] = 'View roadmap'
    elif t['tag'] == 'report':
        t['action'] = 'View report'
    elif 'guide' in low:
        t['action'] = 'Open guide'
    elif t.get('staff') or 'mentor' in low or 'sessions' in low or 'action tracker' in low or 'add-on' in low:
        t['action'] = 'Open workspace'
    else:
        t['action'] = 'Open tool'
    since = _NEW_N.get(key)
    t['new'] = bool(since and 0 <= (today - since).days <= NEW_DAYS)
    return t


def build(user, today=None):
    """Resolve URLs and lock state for this user; returns categories with resolved tiles."""
    out = []
    for cat in CATEGORIES:
        tiles = []
        for t in cat['tiles']:
            t = dict(t)
            if t.get('staff') and not user.is_staff:
                continue
            if t['access'] == 'soon':
                t['url'], t['locked'] = None, False
            else:
                try:
                    url = url_for(t['endpoint'])
                except Exception:       # endpoint removed/renamed: skip the tile, keep the hub alive
                    continue
                if t.get('anchor'):
                    url += '#' + t['anchor']
                t['url'] = url
                t['locked'] = t['access'] == 'premium' and not user.is_premium
            tiles.append(_decorate(t, today))
        if tiles:
            out.append({**cat, 'ic': CATEGORY_ICON.get(cat['key'], 'grid'), 'tiles': tiles,
                        'open': sum(1 for t in tiles if t['url'] and not t['locked'])})
    return out
