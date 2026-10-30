"""Grade-band mentorship programmes: Class 7-9 (stream selection) and Class 10-11 (colleges, branch, career goal), plus the onboarding-to-programme suggestion.

Kept in its own module so services/mentorship.py stays the portal engine. The programmes are ordinary MsProgramme rows with session templates: admins edit them
in Admin -> Mentorship like any other. `ensure_grade_programmes()` is idempotent and never overwrites an admin's edit.
"""
from app.extensions import db
from app.models_mentorship import MsProgramme, MsSessionTemplate

EXPLORE_TIER = 'Grade 7-9 Mentorship'
EXPLORE_PROGRAMME = 'Class 7-9 Stream and Career Explorer Mentorship'
DIRECT_TIER = 'Grade 10-11 Mentorship'
DIRECT_PROGRAMME = 'Class 10-11 College and Career Mentorship'
GRADE_TIERS = (EXPLORE_TIER, DIRECT_TIER)

EXPLORE_SESSIONS = [
    ('Kick-off and baseline', 'Meet the student and parent\nReview the onboarding assessment\nAgree three goals for the year', 'Agreed goals and first-term plan'),
    ('Strengths and study habits', 'Marks versus confidence by subject\nHow the student learns best\nOne habit to build', 'Habit action plan'),
    ('Interests and how you learn', 'Interest map from the assessment\nWhat the student does when nobody is directing them\nTwo things to try this term', 'Interest map and two experiments'),
    ('Careers around you', 'What engineers, doctors, lawyers, managers and designers do in a day\nTalk to one person in a career of interest', 'Career conversation notes'),
    ('Streams explained', 'Science (PCM, PCB, both), Commerce, Humanities\nWhich entrance exams and courses each keeps open\nCommon myths about streams', 'One-page stream map'),
    ('Subject foundations', 'Maths and Science gaps found in the baseline\nTargeted practice plan', 'Foundation practice plan'),
    ('Quarterly review 1', 'Progress against goals\nParent conversation\nWhat has changed in interests', 'Quarterly report'),
    ('Stream scenarios', 'If I choose each stream: subjects, exams, courses, careers\nWhat stays open and what closes\nBackup routes', 'Scenario comparison'),
    ('Exposure project', 'Choose a mini project, a visit or an interview with a professional\nHow it will be reviewed', 'Project plan'),
    ('Parent and student alignment', 'Compare the parent and student views on stream and career\nAgree how the decision will be made', 'Alignment note'),
    ('Quarterly review 2', 'Growth compared with the baseline\nUpdate goals\nStream shortlist', 'Quarterly report'),
    ('Year-end review and stream roadmap', 'Annual summary\nCurrent stream lean and how sure it is\nSteps to the stream decision after Class 10', 'Year-end report and stream roadmap'),
]

DIRECT_SESSIONS = [
    ('Kick-off and baseline', 'Meet the student and parent\nReview the onboarding assessment\nAgree goals for the year', 'Agreed goals and first-term plan'),
    ('Academics and subject strategy', 'Board marks and subject group\nEntrance preparation alongside school\nStudy plan', 'Academic and study plan'),
    ('Career path deep-dive', 'Engineering, medicine, law, management: a day in the life and the routes in\nWhy this path, and what would change the mind', 'Path summary'),
    ('Entrance exam map', 'The exams for the chosen path (for example JEE, NEET, CLAT, IPM) and their timeline\nWhat to do in the next 12 months', 'Exam map and calendar'),
    ('Branch and course exploration', 'Engineering branches, medical routes, law specialisations or management areas\nStudent view versus parent view', 'Ranked course shortlist'),
    ('Quarterly review 1', 'Progress against goals\nParent conversation\nWhat has changed', 'Quarterly report'),
    ('College landscape', 'Types of institutions, rankings and what they do and do not tell you\nFees, location and placements\nBuild a long list', 'Long list of colleges'),
    ('Preparation plan', 'Coaching, school or self-study\nMock and revision plan\nProtecting board marks', 'Preparation plan'),
    ('Exposure', 'Campus visits or online sessions\nTalk to students and alumni\nA small project in the chosen field', 'Exposure notes'),
    ('Parent briefing: budget, location, backup', 'Budget and loans\nDistance from home\nBackup routes if the first choice does not work', 'Parent briefing summary'),
    ('Quarterly review 2', 'Refine the shortlist\nUpdate the exam plan', 'Quarterly report'),
    ('Year-end review and next steps', 'Path decision\nCollege target list version 1\nPlan for the next year', 'Year-end report and college list'),
]


def ensure_grade_programmes():
    """Create the Class 7-9 and Class 10-11 programmes if missing, so they can be chosen in Admin -> Enrolment. Returns how many were created."""
    made = 0
    for name, tier, desc, sessions in (
            (EXPLORE_PROGRAMME, EXPLORE_TIER,
             'Mentorship for Class 7-9 students, centred on choosing a stream: strengths, interests, careers around them, what each stream keeps open, and a stream roadmap.',
             EXPLORE_SESSIONS),
            (DIRECT_PROGRAMME, DIRECT_TIER,
             'Mentorship for Class 10-11 students: the career goal (engineering, medicine, law or management), entrance exams, courses and branches, colleges, and a college list.',
             DIRECT_SESSIONS)):
        if MsProgramme.query.filter_by(name=name).first():
            continue
        prog = MsProgramme(name=name, tier=tier, active=True, description=desc)
        db.session.add(prog)
        db.session.flush()
        for i, (title, topics, deliverable) in enumerate(sessions, 1):
            db.session.add(MsSessionTemplate(programme_id=prog.id, position=i, title=title, topics=topics, deliverable=deliverable, duration_min=60))
        made += 1
    if made:
        db.session.commit()
    return made


def suggested_programme(cls, path):
    """Which programme fits a family, from the onboarding answers: (programme name, why). Nothing is enrolled automatically."""
    if cls in ('Class 7', 'Class 8', 'Class 9'):
        return EXPLORE_PROGRAMME, 'Class 7-9: stream selection (FutureReady can be added for Class 8-9 assessments and reports).'
    if cls in ('Class 10', 'Class 11'):
        return DIRECT_PROGRAMME, 'Class 10-11: colleges, branch and the career goal.'
    if cls == 'Class 12':
        if path in (None, '', 'Engineering', 'Not decided yet'):
            return 'Grade 12 Engineering Mentorship', 'Class 12: the Elite engineering programme (admissions strategy, branch fit, choice filling).'
        return DIRECT_PROGRAMME, 'Class 12 on a non-engineering path: use the College and Career programme and add the path-specific entrance exam add-on.'
    return '', ''
