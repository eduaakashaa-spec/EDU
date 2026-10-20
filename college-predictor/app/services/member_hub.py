"""Member Home registry: categories -> tiles.

To add a feature, append a tile dict to a category (or add a category). Fields:
  title, desc, icon (emoji), endpoint (+ optional anchor),
  access: 'free' (any member) | 'premium' | 'soon' (placeholder, not clickable).
Tiles whose endpoint does not exist are skipped, so a removed page never breaks the hub.
"""
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
         {'title': 'Action tracker', 'desc': 'Meeting actions for every member: owner, due date, completion — share by email or WhatsApp.', 'icon': '📌', 'endpoint': 'mentorship.action_tracker', 'access': 'premium', 'staff': True},
         {'title': 'Mentor dashboard', 'desc': 'Assigned students, sessions, follow-ups and interventions.', 'icon': '📋', 'endpoint': 'mentorship.mentor_home', 'access': 'premium', 'staff': True},
     ]},
    {'key': 'intel', 'title': 'Admission Intelligence', 'icon': '📊', 'color': '#D97706', 'tint': '#FFF3DD',
     'blurb': 'Latest analytics and reports for the 2026–27 cycle.',
     'tiles': [
         {'title': 'DASA 2026 Analytics', 'desc': 'Round-wise closing-rank analytics.', 'icon': '📈', 'endpoint': 'main.dasa_2026_analytics', 'access': 'premium'},
         {'title': 'DASA prediction report', 'desc': 'Personalised DASA / CIWG outlook.', 'icon': '🔮', 'endpoint': 'main.dasa_prediction_report', 'access': 'premium'},
         {'title': 'DASA expert portal', 'desc': 'Expert guidance for DASA choice filling.', 'icon': '🏛️', 'endpoint': 'main.expert_portal_dasa', 'access': 'premium'},
         {'title': 'JoSAA EA members', 'desc': 'Members-only JoSAA insights.', 'icon': '🇮🇳', 'endpoint': 'main.josaa_ea_members', 'access': 'premium'},
         {'title': 'EduPulse-UCEED', 'desc': 'Chapter-wise MCQ practice with progress reports for you, your parent and mentor.', 'icon': '🎯', 'endpoint': 'pulse.home', 'access': 'premium'},
         {'title': 'EduPulse mentor view', 'desc': 'Progress of students practising UCEED.', 'icon': '📈', 'endpoint': 'pulse.mentor_home', 'access': 'premium', 'staff': True},
         {'title': 'UCEED 2027 Roadmap', 'desc': 'Design-entrance plan, planner and B.Des admission guide.', 'icon': '✏️', 'endpoint': 'main.uceed_2027_roadmap', 'access': 'premium'},
         {'title': 'Law Entrance 2027 Roadmap', 'desc': 'CLAT, AILET and SLAT plan, planner and law-school guide.', 'icon': '⚖️', 'endpoint': 'main.law_2027_roadmap', 'access': 'premium'},
         {'title': 'IPM 2027 Roadmap', 'desc': 'IIM five-year IPM: IPMAT, JIPMAT, planner and admission steps.', 'icon': '🏫', 'endpoint': 'main.ipm_2027_roadmap', 'access': 'premium'},
         {'title': 'JEE 2027 Roadmap', 'desc': 'The exam process, mapped step by step.', 'icon': '🗺️', 'endpoint': 'main.jee_2027_roadmap', 'access': 'premium'},
         {'title': 'TNEA expert', 'desc': 'Tamil Nadu engineering counselling guide.', 'icon': '🎓', 'endpoint': 'main.tnea_expert', 'access': 'premium'},
         {'title': 'Members report', 'desc': 'Reports prepared for members.', 'icon': '📑', 'endpoint': 'main.members_report', 'access': 'premium'},
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
         {'title': 'Contact the team', 'desc': 'info@eduaakashaa.com · +91-80157 22706', 'icon': '✉️', 'endpoint': 'main.contact_alias', 'access': 'free'},
         {'title': 'Membership plans', 'desc': 'Upgrade or renew your access.', 'icon': '★', 'endpoint': 'main.members_registration', 'access': 'free'},
         {'title': 'More tools coming soon', 'desc': 'New member features land here.', 'icon': '✨', 'endpoint': None, 'access': 'soon'},
     ]},
]


def build(user):
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
            tiles.append(t)
        if tiles:
            out.append({**cat, 'tiles': tiles,
                        'open': sum(1 for t in tiles if t['url'] and not t['locked'])})
    return out
