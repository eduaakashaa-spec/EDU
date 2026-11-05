"""Content for the public page /school: tools for Class 8 to 12 students and parents, grouped by class and stream.

Each card is (badge, title, description, endpoint, anchor). Badge is 'Free' (open to everyone), 'Guide' (open guide page) or 'Members' (Premium or a members' page that sends a visitor to log in or join).
Endpoints are resolved with url_for when the page is built, so a removed page drops out of the list instead of breaking it.
"""
from flask import current_app, url_for

STAGES = [
    {'id': 'c8-10', 'tab': 'Class 8 to 10', 'title': 'Class 8 to 10: build habits and keep options open',
     'lead': 'Practice, mentoring and early stream choice for Grades 7 to 10, including Tamil Nadu Class 10.',
     'cards': [
         ('Free', 'Grade 7 to 10 Explorer', 'EduPulse-Explorer: exam families, spaced review and six free questions for Grades 7 to 10.', 'main.explorer_landing', ''),
         ('Free', 'Free sample mock tests', 'A free ten-question sample for TN Class 10, with an explanation for every answer.', 'free_mock.home', ''),
         ('Members', 'EduPulse-TN Class 10 mock test centre', 'Maths and Science mocks in the TN pattern, textbook-unit sets and a daily review.', 'pulse_tn10.home', ''),
         ('Members', 'FutureReady (Class 8 and 9)', 'Mentorship with assessments, engineering exploration, an action plan and reports.', 'futureready.index', ''),
         ('Free', 'Olympiad foundation mentorship', 'Sixteen weekly sessions for Classes 8 to 10: maths and junior science habits for IOQM and NSEJS.', 'mentorship.addons', 'olympiad-jr'),
         ('Guide', 'Olympiad exams guide', 'IOQM, NSEJS and the later stages, with 2026-27 dates and eligibility from official pages.', 'main.olympiad_exam', ''),
         ('Members', 'Stream selection', 'Choose between PCM, PCB, commerce and humanities with evidence, after Class 10.', 'main.stream_selection', ''),
         ('Members', 'Smart study planner', 'A weekly plan built from your exam, level and hours.', 'planner.home', ''),
     ]},
    {'id': 'c12-pcm', 'tab': 'Class 11 and 12: PCM', 'title': 'Class 11 and 12 PCM: boards and engineering entrance',
     'lead': 'Your marks against 11 entrance routes plus the Maharashtra, Delhi, Kerala, Andhra Pradesh and NRI rules, the board playbook and a study plan.',
     'cards': [
         ('Free', 'Class 12 PCM Analytics', 'The hub: four tools and a quick study plan counted back from your first paper.', 'pcm12.hub', ''),
         ('Free', 'Eligibility Gap Closer', 'Enter your marks, see the gap for every route, and a plan to close it.', 'pcm12.eligibility', ''),
         ('Free', 'Board Score Playbook', 'What to study first at your level, chapter focus by marks and the 2026-27 calendar.', 'pcm12.board_playbook', ''),
         ('Free', 'Thumb Rules Handbook', 'Rules, memory hooks and traps for 37 chapters, with flashcards.', 'pcm12.thumb_rules', ''),
         ('Free', 'Answer Sheet Lab', 'The same question answered three ways, with the examiner\'s marks.', 'pcm12.answer_lab', ''),
         ('Members', 'My PCM dashboard', 'Marks, test log, chapter ratings and a week-by-week plan saved to your account.', 'pcm12.dashboard', ''),
         ('Guide', 'JEE Main 2027 registration guide', 'Eligibility, dates and the registration steps.', 'main.jee_registration', ''),
         ('Members', 'JEE Main syllabus map and formulas', 'The syllabus by chapter with the formulas that matter.', 'main.jee_syllabus_map', ''),
         ('Members', 'EduPulse-JEE mock test centre', 'JEE Main mocks, chapter sets and a daily review.', 'pulse_jee.home', ''),
         ('Members', 'JEE 2027 roadmap', 'A plan from now to the exam.', 'main.jee_2027_roadmap', ''),
         ('Free', 'Olympiad senior mentorship', 'Twenty weekly sessions for Classes 11 and 12: IOQM to INMO maths and NSE physics, chemistry and biology.', 'mentorship.addons', 'olympiad-sr'),
     ]},
    {'id': 'c12-pcb', 'tab': 'Class 11 and 12: PCB', 'title': 'Class 11 and 12 PCB: boards and NEET',
     'lead': 'Your marks against NEET and state medical routes with sources, Biology thumb rules, marked answer sheets and a study plan.',
     'cards': [
         ('Free', 'Class 12 PCB Analytics', 'The hub: eligibility check, board playbook, thumb rules for 37 chapters, answer lab and study plan.', 'pcb12.hub', ''),
         ('Members', 'My PCB dashboard', 'Marks, test log, chapter ratings and a week-by-week plan saved to your account.', 'pcb12.dashboard', ''),
         ('Free', 'NEET 2027 guide', 'What the National Testing Agency has announced, pattern, eligibility and counselling.', 'main.neet_2027', ''),
         ('Free', 'Medicine exams', 'NEET and the other medicine entrance exams in one place.', 'main.medicine', ''),
         ('Guide', 'NEET papers analysed', 'Nine papers, 2018 to 2026: questions by year, subject and topic, with free questions.', 'main.neet_exam', ''),
         ('Members', 'EduPulse-NEET mock test centre', 'Full 180-question mocks, earlier-paper questions and a daily review.', 'neet_mock.home', ''),
         ('Members', 'NEET MBBS seat analytics', 'Every MBBS college in the NMC seat matrix, by state and management.', 'main.neet_seats_2025', ''),
         ('Free', 'NEET (UG) mentorship', 'Sixteen weekly sessions: Physics, Chemistry, Botany and Zoology, mocks and counselling.', 'mentorship.addons', 'neet'),
     ]},
]
ALSO = [
    ('Guide', 'SAT exam guidelines', 'Studying abroad? Dates, fees, ID, format and scoring from College Board pages.', 'main.sat_exam', ''),
    ('Members', 'EduPulse-SAT practice centre', 'A full practice SAT with fresh Math numbers every attempt.', 'sat_mock.home', ''),
    ('Free', 'Free sample mock tests', 'Ten free questions each for nine exams, scored with explanations.', 'free_mock.home', ''),
    ('Free', 'Student assessment', 'A stream and career that actually fits you.', 'main.student_assessment', ''),
]


def _cards(cards):
    out = []
    for badge, title, desc, endpoint, anchor in cards:
        if endpoint not in current_app.view_functions:
            continue
        url = url_for(endpoint) + ('#' + anchor if anchor else '')
        out.append({'badge': badge, 'title': title, 'desc': desc, 'url': url})
    return out


def context():
    stages = [dict(s, cards=_cards(s['cards'])) for s in STAGES]
    return {'stages': stages, 'also': _cards(ALSO)}
