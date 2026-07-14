"""College Experience Survey — the detailed one.

A free, public, deliberately exhaustive survey where students / alumni of any
college give an honest read of their college across every angle we can think
of: academics, placements, infrastructure, hostel & food, amenities, campus
life, administration, location and a final verdict. No payment involved. It
doubles as a soft funnel into the paid mentor network (routes/alumni.py).

The entire question set lives in SECTIONS below (single source of truth for
rendering the form, validating the POST and displaying a response in admin).
Answers are stored in CollegeSurvey.responses_json keyed by question id, except
a few first-class columns (name/email/phone/institute/branch/batch/
overall_rating/recommend_score/wants_to_mentor).

Public:
    GET/POST /college-survey            — the survey + thank-you state
Admin (admin tier):
    GET /admin/surveys                  — searchable / filterable list
    GET /admin/surveys/<id>             — a single response
"""
import json
import threading
import time

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)

from app.data.loader import get_branch_names, get_college_names
from app.decorators import admin_required
from app.extensions import db
from app.models import CollegeSurvey
from app.services.email_templates import SITE, render_email
from app.services.mailer import notify_admin, send_async
from app.services.queries import count_if

survey_bp = Blueprint('survey', __name__)

RATING_CHOICES = ['Excellent', 'Good', 'Average', 'Poor']


# question builders -> plain dicts (keeps SECTIONS readable) ------------------ #
def _rate(key, label):                      return {'key': key, 'type': 'rating', 'label': label}
def _choice(key, label, options):           return {'key': key, 'type': 'choice', 'label': label, 'options': options}
def _short(key, label, ph='', required=False):   return {'key': key, 'type': 'short', 'label': label, 'ph': ph, 'required': required}
def _long(key, label, ph='', required=False):    return {'key': key, 'type': 'long', 'label': label, 'ph': ph, 'required': required}
def _scale(key, label):                     return {'key': key, 'type': 'scale', 'label': label}   # 0–10
def _check(key, label):                     return {'key': key, 'type': 'check', 'label': label}
def _text(key, label, ph='', required=False, col=True):
    return {'key': key, 'type': 'short', 'label': label, 'ph': ph, 'required': required, 'col': col}
def _datalist(key, label, source, ph='', required=False, col=True):
    # a text input backed by a <datalist> (dropdown suggestions + free text)
    return {'key': key, 'type': 'short', 'label': label, 'ph': ph,
            'required': required, 'col': col, 'datalist': source}


# The survey. Each section: a title, an optional note, and a list of questions.
SECTIONS = [
    {'title': 'About you & admission', 'note': 'Fields marked * are required.', 'questions': [
        _text('name', 'Your name', 'Full name', required=True),
        _text('email', 'Email', 'you@example.com', required=True),
        _text('phone', 'Phone / WhatsApp', '+91…', required=True),
        _datalist('institute', 'College / Institute', 'colleges', 'Start typing your college…', required=True),
        _short('campus_city', 'Campus city / location', 'e.g. Tiruchirappalli, TN'),
        _datalist('branch', 'Course / Branch / Major', 'branches', 'Start typing your branch…'),
        _choice('degree_level', 'Degree level', ['B.Tech / B.E.', 'M.Tech / M.E.', 'B.Sc / M.Sc', 'MBA / Management', 'Diploma', 'PhD / Research', 'Other']),
        _text('batch', 'Batch / Graduation year', 'e.g. 2024'),
        _choice('status', 'Your status', ['Current student', 'Recent graduate (0–2 yrs)', 'Alumnus — working', 'Alumnus — higher studies']),
        _choice('year_of_study', 'Current / final year', ['1st year', '2nd year', '3rd year', '4th year', '5th year', 'Graduated']),
        _choice('admission_route', 'How you got admission', ['JEE / JOSAA', 'DASA / CIWG', 'State counselling (TNEA etc.)', 'Management / NRI quota', 'SAT / Direct', 'Lateral entry', 'Other']),
        _short('entrance_exam', 'Entrance exam & rank / percentile', 'e.g. JEE Main 98.2%ile', required=True),
        _short('home_state', 'Your home state / country', 'e.g. Kerala'),
        _choice('category', 'Category (optional)', ['General', 'OBC', 'SC', 'ST', 'EWS', 'NRI / Foreign', 'Prefer not to say']),
    ]},

    {'title': 'Academics', 'questions': [
        _rate('academics_overall', 'Overall academic quality'),
        _rate('faculty', 'Faculty & teaching quality'),
        _rate('faculty_access', 'Faculty accessibility & mentorship'),
        _rate('syllabus', 'Syllabus — relevant & up to date'),
        _rate('labs', 'Labs & equipment'),
        _rate('projects', 'Projects & hands-on work'),
        _rate('research', 'Research opportunities'),
        _rate('electives', 'Choice of electives / specializations'),
        _rate('industry', 'Industry exposure (guest lectures, workshops)'),
        _rate('exams', 'Exams & evaluation fairness'),
        _choice('teaching_style', 'Teaching leans towards', ['Mostly theory', 'Balanced', 'Mostly practical']),
        _choice('grading', 'Grading is', ['Lenient', 'Fair', 'Strict']),
        _short('attendance', 'Attendance policy', 'e.g. 75% mandatory, strictly enforced'),
        _short('exams_per_sem', 'How many exams per semester?', 'e.g. 2 mid-terms + 1 end-sem'),
        _short('workload_notes', 'Assignments, labs & overall workload', 'e.g. weekly assignments, heavy lab load'),
    ]},

    {'title': 'Placements & careers', 'questions': [
        _rate('placements', 'Placement support & opportunities'),
        _rate('internships', 'Internship support'),
        _rate('higher_studies', 'Higher-studies support (GRE / GATE / CAT)'),
        _rate('entrepreneurship', 'Startup / entrepreneurship support'),
        _rate('alumni_network', 'Alumni network strength'),
        _rate('alumni_help', 'Alumni helpfulness (referrals, guidance)'),
        _short('placement_percent', '% of students placed (approx)', 'e.g. 85%'),
        _short('avg_package', 'Average package (if known)', 'e.g. ₹8 LPA'),
        _short('highest_package', 'Highest package (if known)', 'e.g. ₹45 LPA'),
        _short('top_recruiters', 'Top recruiters', 'e.g. TCS, Amazon, Zoho'),
    ]},

    {'title': 'Infrastructure & campus', 'questions': [
        _rate('infrastructure', 'Overall infrastructure'),
        _rate('classrooms', 'Classrooms'),
        _rate('library', 'Library'),
        _rate('wifi', 'Wi-Fi / internet'),
        _rate('it', 'Computer / IT facilities'),
        _rate('campus', 'Campus size & greenery'),
        _rate('cleanliness', 'Cleanliness & maintenance'),
        _rate('utilities', 'Power backup & water supply'),
    ]},

    {'title': 'Hostel & food', 'questions': [
        _choice('hostel_available', 'Hostel availability', ['Yes — for all', 'Limited seats', 'No hostel']),
        _rate('hostel', 'Hostel facilities overall'),
        _rate('rooms', 'Room quality'),
        _rate('mess', 'Mess / food quality'),
        _rate('food_hygiene', 'Food hygiene & variety'),
        _rate('hostel_wifi', 'Hostel Wi-Fi'),
        _rate('laundry', 'Laundry & housekeeping'),
        _choice('room_type', 'Room type', ['AC', 'Non-AC', 'Both options', 'N/A']),
        _choice('occupancy', 'Room occupancy', ['Single', 'Double sharing', 'Triple+ sharing', 'N/A']),
        _choice('food_type', 'Mess food', ['Veg only', 'Veg & non-veg', 'N/A']),
        _choice('hostel_rules', 'Hostel rules', ['Relaxed', 'Moderate', 'Very strict']),
        _short('curfew', 'Hostel curfew timing (if any)', 'e.g. 10 PM'),
        _short('hostel_fees', 'Approx hostel + mess fees (₹ per year)', 'e.g. ₹1,20,000 per year'),
    ]},

    {'title': 'Amenities', 'questions': [
        _rate('sports', 'Sports facilities'),
        _rate('gym', 'Gym / fitness'),
        _rate('canteen', 'Canteen / cafeteria'),
        _rate('medical', 'Medical / health centre'),
        _rate('bank_atm', 'Bank / ATM on campus'),
        _rate('shops', 'Stationery / shops on campus'),
        _rate('transport', 'College transport (buses)'),
        _rate('auditorium', 'Auditorium / seminar halls'),
    ]},

    {'title': 'Campus life, culture & safety', 'questions': [
        _rate('culture', 'Overall campus culture'),
        _rate('clubs', 'Clubs & societies'),
        _rate('fests', 'Fests & events'),
        _rate('diversity', 'Cultural / regional diversity'),
        _rate('peers', 'Peer group quality'),
        _rate('seniors', 'Seniors — supportive'),
        _rate('antiragging', 'Anti-ragging measures'),
        _rate('freedom', 'Freedom & flexibility'),
        _rate('girls_safety', 'Safety for girls'),
        _rate('overall_safety', 'Overall safety & security'),
        _choice('ragging', 'Ragging on campus', ['None — safe', 'Rare & mild', 'Occasional', 'Serious problem']),
        _choice('gender_ratio', 'Gender ratio (approx)', ['Balanced', 'More boys', 'Mostly boys', 'More girls']),
        _choice('groupism', 'Regional / political groupism', ['None', 'A little', 'Noticeable', 'A lot']),
    ]},

    {'title': 'Administration & support', 'questions': [
        _rate('administration', 'Administration responsiveness'),
        _rate('fee_transparency', 'Fee transparency'),
        _rate('paperwork', 'Certificates / documentation process'),
        _rate('grievance', 'Grievance handling'),
        _rate('financial_aid', 'Scholarship / financial-aid support'),
        _rate('counseling', 'Mental-health / counselling support'),
        _short('annual_fees', 'Approx tuition fees (₹ per year)', 'e.g. ₹1,50,000 per year'),
        _choice('scholarship', 'Did you get a scholarship?', ['Yes', 'No', 'N/A']),
    ]},

    {'title': 'Location & surroundings', 'questions': [
        _rate('local_transport', 'Local transport (outside campus)'),
        _rate('nearby_medical', 'Nearby hospitals / medical'),
        _rate('nearby_shopping', 'Nearby markets / shopping'),
        _rate('nearby_food', 'Nearby restaurants / food'),
        _rate('area_safety', 'Safety of the surrounding area'),
        _rate('emergency', 'Emergency-services access'),
        _short('nearest_airport', 'Nearest airport & distance', 'e.g. Trichy — 15 km'),
        _short('nearest_railway', 'Nearest railway station & distance', 'e.g. Trichy Jn — 8 km'),
        _short('weather', 'Local weather / climate', 'e.g. hot & humid'),
        _choice('connectivity', 'Connectivity to your hometown', ['Very easy', 'Manageable', 'Difficult']),
    ]},

    {'title': 'Your verdict', 'questions': [
        _rate('value', 'Value for money'),
        {'key': 'overall_rating', 'type': 'rating', 'label': 'Overall, how would you rate your college?', 'col': True},
        _scale('recommend_score', 'How likely are you to recommend it? (0 = never, 10 = absolutely)'),
        _choice('would_choose_again', 'Would you choose this college again?', ['Definitely yes', 'Probably yes', 'Not sure', 'Probably not', 'Definitely not']),
        _long('best_things', 'Best things about your college', 'What genuinely stands out.'),
        _long('worst_things', 'Worst things / biggest drawbacks', 'What you wish someone had told you.'),
        _long('hidden_costs', 'Any hidden costs or surprises?', 'Fees, deposits, mandatory expenses…'),
        _long('advice_parent', 'Your advice to a parent considering this college'),
        _long('advice_student', 'Your advice to a student joining'),
        _long('extra', 'Anything else you want to share?'),
    ]},
]

# derived lookups
ALL_QUESTIONS = [q for sec in SECTIONS for q in sec['questions']]
QUESTION_BY_KEY = {q['key']: q for q in ALL_QUESTIONS}
REQUIRED_QUESTIONS = [q for q in ALL_QUESTIONS if q.get('required')]
COLUMN_KEYS = {'name', 'email', 'phone', 'institute', 'branch', 'batch',
               'overall_rating', 'recommend_score', 'wants_to_mentor'}


# ---- lightweight per-IP throttle (public, unauthenticated endpoint) -------- #
_RATE_LOCK = threading.Lock()
_RATE_HITS = {}
RATE_WINDOW = 3600      # 1 hour
RATE_MAX = 20           # submissions per IP per window


def _client_ip():
    xff = request.headers.get('X-Forwarded-For', '')
    return xff.split(',')[0].strip() if xff else (request.remote_addr or 'unknown')


def _rate_ok(ip):
    now = time.time()
    with _RATE_LOCK:
        hits = [t for t in _RATE_HITS.get(ip, []) if now - t < RATE_WINDOW]
        if len(hits) >= RATE_MAX:
            _RATE_HITS[ip] = hits
            return False
        hits.append(now)
        _RATE_HITS[ip] = hits
        if len(_RATE_HITS) > 5000:                       # bound memory
            for k in list(_RATE_HITS):
                _RATE_HITS[k] = [t for t in _RATE_HITS[k] if now - t < RATE_WINDOW]
                if not _RATE_HITS[k]:
                    del _RATE_HITS[k]
        return True


# ---- parse one posted answer according to its question type ---------------- #
def _clean(q, raw):
    """Return a normalised value for question q, or None to skip it."""
    t = q['type']
    if t == 'rating':
        return raw if raw in RATING_CHOICES else None
    if t == 'choice':
        return raw if raw in q['options'] else None
    if t == 'scale':
        try:
            n = int(raw)
        except (TypeError, ValueError):
            return None
        return n if 0 <= n <= 10 else None
    if t in ('short', 'long'):
        v = (raw or '').strip()
        return v[:4000] if v else None
    return None


# --------------------------------------------------------------------------- #
# Public
# --------------------------------------------------------------------------- #
def _render_form(form, done, code=200):
    return render_template('college_survey.html', sections=SECTIONS,
                           choices=RATING_CHOICES, form=form, done=done,
                           college_options=get_college_names(),
                           branch_options=get_branch_names()), code


def _email_survey_thanks(survey):
    """Thank the respondent (and nudge them to become a Guide) — the
    'Thank you — Survey' template, sent automatically on submit."""
    if not survey.email:
        return
    first = (survey.name or '').strip().split(' ')[0] or 'there'
    subject, text, html = render_email(
        'ty_survey', {'name': first, 'college': survey.institute or 'your college'})
    send_async(survey.email, subject, text, html)


def _notify_admin_survey(survey):
    """Tell the team a survey came in, with the headline answers."""
    link = SITE + url_for('survey.admin_list')
    notify_admin(
        f'New college survey — {survey.institute or "unknown college"}',
        (f'{survey.name} ({survey.email or "no email"}) reviewed '
         f'{survey.institute or "—"}.\n\n'
         f'  Branch    : {survey.branch or "—"}\n'
         f'  Batch     : {survey.batch or "—"}\n'
         f'  Overall   : {survey.overall_rating or "—"}\n'
         f'  Recommend : {survey.recommend_score if survey.recommend_score is not None else "—"}/10\n'
         f'  Wants to guide: {"yes" if survey.wants_to_mentor else "no"}\n\n'
         f'Read the full response: {link}'))


@survey_bp.route('/college-survey', methods=['GET', 'POST'])
def college_survey():
    if request.method == 'GET':
        html, _ = _render_form(None, request.args.get('done') == '1')
        return html

    f = request.form
    name = (f.get('name') or '').strip()
    institute = (f.get('institute') or '').strip()

    def reshow(msg, code):
        flash(msg, 'error')
        return _render_form(f, False, code)

    # every question flagged required must be non-empty
    missing = [q['label'] for q in REQUIRED_QUESTIONS if not (f.get(q['key']) or '').strip()]
    if missing:
        return reshow('Please fill in the required field(s): ' + ', '.join(missing) + '.', 400)
    email = (f.get('email') or '').strip()
    if '@' not in email or '.' not in email.split('@')[-1]:
        return reshow('Please enter a valid email address.', 400)
    if not _rate_ok(_client_ip()):
        return reshow('Too many submissions from your network. Please try again later.', 429)

    survey = CollegeSurvey(name=name[:150], institute=institute[:200])
    responses = {}
    for q in ALL_QUESTIONS:
        key = q['key']
        if key in ('name', 'institute'):
            continue
        if q['type'] == 'check':
            val = bool(f.get(key))
        else:
            val = _clean(q, f.get(key))
        if val is None:
            continue
        if key in COLUMN_KEYS:
            if key == 'email':
                survey.email = str(val).lower()[:200]
            elif key == 'phone':
                survey.phone = str(val)[:40]
            elif key == 'branch':
                survey.branch = str(val)[:200]
            elif key == 'batch':
                survey.batch = str(val)[:16]
            elif key == 'overall_rating':
                survey.overall_rating = val
            elif key == 'recommend_score':
                survey.recommend_score = val
        else:
            responses[key] = val

    survey.wants_to_mentor = bool(f.get('wants_to_mentor'))
    survey.responses_json = json.dumps(responses) if responses else None
    db.session.add(survey)
    db.session.commit()
    _email_survey_thanks(survey)
    _notify_admin_survey(survey)
    return redirect(url_for('survey.college_survey', done=1) + '#top')


# --------------------------------------------------------------------------- #
# Admin
# --------------------------------------------------------------------------- #
@survey_bp.route('/admin/surveys')
@admin_required
def admin_list():
    q = (request.args.get('q') or '').strip()

    query = CollegeSurvey.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(CollegeSurvey.name.ilike(like),
                                    CollegeSurvey.institute.ilike(like),
                                    CollegeSurvey.branch.ilike(like),
                                    CollegeSurvey.email.ilike(like)))
    rows = query.order_by(CollegeSurvey.created_at.desc()).all()

    # group responses by college; colleges ordered by most responses, then name
    by_college = {}
    for r in rows:
        by_college.setdefault(r.institute or '—', []).append(r)
    grouped = sorted(by_college.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))

    total, colleges, mentor_leads = db.session.query(
        db.func.count(CollegeSurvey.id),
        db.func.count(db.distinct(CollegeSurvey.institute)),
        count_if(CollegeSurvey.wants_to_mentor.is_(True))).one()
    stats = {'total': total, 'colleges': colleges, 'mentor_leads': mentor_leads}
    return render_template('admin/surveys_list.html', admin_tab='surveys',
                           grouped=grouped, shown=len(rows), stats=stats, q=q)


@survey_bp.route('/admin/surveys/<int:survey_id>')
@admin_required
def admin_detail(survey_id):
    s = db.session.get(CollegeSurvey, survey_id) or abort(404)
    return render_template('admin/survey_detail.html', admin_tab='surveys',
                           s=s, sections=SECTIONS, column_keys=COLUMN_KEYS)
