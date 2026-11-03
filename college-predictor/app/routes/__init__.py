import json
import os
from functools import lru_cache

from flask import Blueprint, redirect, render_template, url_for, Response

from app.decorators import admin_required, premium_required

main_bp = Blueprint('main', __name__)


# Lightweight keep-alive endpoint — no DB, no templates, no data load.
# An external scheduler pings this so the Render free instance doesn't sleep.
@main_bp.route('/ping')
def ping():
    return Response('ok', mimetype='text/plain')


@main_bp.route('/robots.txt')
def robots_txt():
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /dashboard',
        f'Sitemap: {url_for("main.sitemap_xml", _external=True)}',
    ]
    return Response('\n'.join(lines) + '\n', mimetype='text/plain')


@main_bp.route('/sitemap.xml')
def sitemap_xml():
    from flask import current_app
    urls = []
    for rule in current_app.url_map.iter_rules():
        if (rule.endpoint.startswith('main.')
                and 'GET' in rule.methods
                and not rule.arguments
                and not rule.endpoint.endswith('_alias')
                and rule.endpoint not in ('main.ping', 'main.robots_txt', 'main.sitemap_xml')):
            urls.append(url_for(rule.endpoint, _external=True))
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(set(urls)):
        body.append(f'  <url><loc>{u}</loc></url>')
    body.append('</urlset>')
    return Response('\n'.join(body), mimetype='application/xml')


def render_reference_page(filename: str, fallback_template: str, **context):
    # Every page is now a proper, styled Jinja template (clean HTML, no Hostinger
    # iframes), so we render the template directly. `filename` is kept only as a
    # label of the original live-site page this template was migrated from.
    return render_template(fallback_template, **context)


# =============================================================
# Core pages
# =============================================================
@main_bp.route('/')
def home():
    return render_reference_page('homepage.html', 'home.html')


# URL parity with the legacy Hostinger site
@main_bp.route('/homepage')
def homepage_alias():
    return render_reference_page('homepage.html', 'home.html')


@main_bp.route('/nri-admissions-guide')
def nri_guide():
    # one maintained guide: same page as /nri-admission (the old copy had drifted)
    return render_reference_page('nri-admission.html', 'nri_admission.html')


@main_bp.route('/josaa')
def josaa():
    return render_reference_page('josaa.html', 'josaa.html')


@main_bp.route('/iiits')
def iiits():
    return render_reference_page('iiits.html', 'iiits.html')


@main_bp.route('/annanri')
def annanri():
    return render_reference_page('annanri.html', 'annanri.html')


@main_bp.route('/dasa-seat-matrix')
def dasa_seat_matrix():
    return render_reference_page('dasa-seat-matrix.html', 'dasa_seat_matrix.html')


@main_bp.route('/dasa-admissions-guide')
def dasa_guide():
    return render_reference_page('dasa-admissions-guide.html', 'dasa_guide.html')


@main_bp.route('/nirf-ranking')
def nirf_ranking():
    return render_reference_page('nirf-ranking.html', 'nirf_ranking.html')


# =============================================================
# TNEA cluster
# =============================================================
@main_bp.route('/tnea2026')
def tnea2026():
    return render_reference_page('tnea2026.html', 'tnea2026.html')


# /tnea on the legacy site mirrors /tnea2026 content
@main_bp.route('/tnea')
def tnea_alias():
    return render_reference_page('tnea.html', 'tnea2026.html')


@main_bp.route('/tneamatrix')
def tneamatrix():
    return render_reference_page('tneamatrix.html', 'tneamatrix.html')


@main_bp.route('/tneapc')
def tneapc():
    return render_reference_page('tneapc.html', 'tneapc.html')


@main_bp.route('/tnea-cutoff')
def tnea_cutoff():
    return render_reference_page('tnea-cutoff.html', 'tnea_cutoff.html')


@main_bp.route('/tnea-simulator')
def tnea_simulator():
    return render_reference_page('tnea-simulator.html', 'tnea_simulator.html')


# =============================================================
# Professional & content pages
# =============================================================
@main_bp.route('/professional-exam')
def professional_exam():
    return render_reference_page('professional-exam.html', 'professional_exam.html')


@main_bp.route('/contact')
def contact():
    return render_reference_page('contact-us.html', 'contact.html')


# Legacy URL used on Hostinger
@main_bp.route('/contact-us')
def contact_alias():
    return render_reference_page('contact-us.html', 'contact.html')


@main_bp.route('/mbamca-program')
def mbamca():
    return render_reference_page('mbamca-program.html', 'mbamca.html')


@main_bp.route('/tancet')
def tancet():
    return render_reference_page('tancet.html', 'tancet.html')


@main_bp.route('/ea-library')
def ea_library():
    return render_reference_page('ea-library.html', 'ea_library.html')


@main_bp.route('/tancet-pulse')
def tancet_pulse():
    return render_reference_page('tancet-pulse.html', 'tancet_pulse.html')


@main_bp.route('/viteee-for-nri')
def viteee_nri():
    return render_reference_page('viteee-for-nri.html', 'viteee_nri.html')


# =============================================================
# Newly implemented pages (parity with Hostinger legacy)
# =============================================================
@main_bp.route('/amrita-aeee')
def amrita_aeee():
    return render_reference_page('amrita-aeee.html', 'amrita_aeee.html')


@main_bp.route('/nata')
def nata():
    return render_reference_page('nata.html', 'nata.html')


@main_bp.route('/nid')
def nid():
    return render_reference_page('nid.html', 'nid.html')


@main_bp.route('/cat')
def cat():
    return render_reference_page('cat.html', 'cat.html')


@main_bp.route('/josaa-assessment')
def josaa_assessment():
    return render_reference_page('josaa-assessment.html', 'josaa_assessment.html')


@main_bp.route('/student-assessment')
def student_assessment():
    return render_reference_page('student-assessment.html', 'student_assessment.html')


@main_bp.route('/conflict-assessment')
def conflict_assessment():
    return render_reference_page('conflict-assessment.html', 'conflict_assessment.html')


@main_bp.route('/stream-selection')
@premium_required
def stream_selection():
    return render_reference_page('stream-selection.html', 'stream_selection.html')


@main_bp.route('/exam-schedule')
def exam_schedule():
    from app.services import exam_page
    return render_template('exam_schedule.html', cats=exam_page.CATEGORIES, stats=exam_page.counts(),
                           milestones=exam_page.MILESTONES, filters=exam_page.FILTERS, verified=exam_page.VERIFIED,
                           tdata=exam_page.timeline_data(), dl={r[0]: exam_page.deadlines_for(r[0]) for _c, r in exam_page.all_exams()})


@main_bp.route('/exam-schedule.ics')
def exam_schedule_ics():
    from flask import Response
    from app.services import exam_page
    return Response(exam_page.all_ics(), mimetype='text/calendar', headers={
        'Content-Disposition': 'attachment; filename="India-Entrance-Exams-2026-27-EduAakashaa.ics"'})


@main_bp.route('/exam-schedule/deadlines.ics')
def exam_schedule_deadlines_ics():
    from flask import Response
    from app.services import exam_page
    return Response(exam_page.deadlines_ics(), mimetype='text/calendar', headers={
        'Content-Disposition': 'attachment; filename="Entrance-Exam-Deadlines-2026-27-EduAakashaa.ics"'})


@main_bp.route('/exam-schedule/<exam_id>.ics')
def exam_schedule_one_ics(exam_id):
    from flask import Response, abort
    from app.services import exam_calendar, exam_page
    ev = exam_page.as_event(exam_page.find(exam_id)) if exam_page.find(exam_id) else None
    if not ev:
        abort(404)
    return Response(exam_calendar.make_ics([ev] + exam_page.milestone_events(exam_id), ev.name), mimetype='text/calendar', headers={
        'Content-Disposition': f'attachment; filename="{exam_id}-eduaakashaa.ics"'})


@main_bp.route('/join-our-team')
def join_our_team():
    return render_reference_page('join-our-team.html', 'join_our_team.html')


# Gated portals – require login to view content
@main_bp.route('/stream-selectionea')
def stream_selection_ea():
    return render_reference_page('stream-selectionea.html', 'stream_selection_ea.html')


@main_bp.route('/josaaea-members')
@premium_required
def josaa_ea_members():
    return render_reference_page('josaaea-members.html', 'josaa_ea_members.html')


# =============================================================
# New pages (from eduaakashaa.in navigation)
# =============================================================
@main_bp.route('/dasa-predictor')
def dasa_predictor_alias():
    # Live site uses /dasa-predictor for the same predictor experience
    return render_reference_page('dasa-predictor.html', 'dasa_guide.html')


@main_bp.route('/mbamca')
def mbamca_alias():
    # Live site uses /mbamca in navigation
    return render_reference_page('mbamca-program.html', 'mbamca.html')


@main_bp.route('/per-assessment')
def per_assessment():
    return render_reference_page('per-assessment.html', 'per_assessment.html')


@main_bp.route('/career-path')
def career_path():
    return render_reference_page('career-path.html', 'career_path.html')


@main_bp.route('/members-report')
@premium_required
def members_report():
    return render_reference_page('members-report.html', 'members_report.html')


@main_bp.route('/tnea-expert-guidance')
def tnea_expert_guidance():
    return render_reference_page('tnea-expert-guidance.html', 'tnea_expert_guidance.html')


@main_bp.route('/videos-library')
def videos_library():
    return render_reference_page('videos-library.html', 'videos_library.html')


@main_bp.route('/nri-admission')
def nri_admission():
    return render_reference_page('nri-admission.html', 'nri_admission.html')


# =============================================================
# New public content pages (eduaakashaa.in nav parity) — built from live captures
# =============================================================
@main_bp.route('/dasa-2026')
@main_bp.route('/dasa-2027')
def dasa_2026():
    return render_reference_page('dasa-2026.html', 'dasa_2026.html')


@main_bp.route('/dasa-2025-vs-2026')
def dasa_2025_vs_2026():
    return render_reference_page('dasa-2025-vs-2026.html', 'dasa_2025_vs_2026.html')


@main_bp.route('/dasa-strategic-approach')
def dasa_strategic_approach():
    return render_reference_page('dasa-strategic-approach.html', 'dasa_strategic_approach.html')


@main_bp.route('/dasa2025-ranks')
def dasa2025_ranks():
    return render_reference_page('dasa2025-ranks.html', 'dasa2025_ranks.html')


@main_bp.route('/dasa2026-schedule')
def dasa2026_schedule():
    return render_reference_page('dasa2026-schedule.html', 'dasa2026_schedule.html')


@main_bp.route('/enggcolleges-india')
def enggcolleges_india():
    return render_reference_page('enggcolleges-india.html', 'enggcolleges_india.html')


@main_bp.route('/nirf-analytic')
def nirf_analytic():
    return render_reference_page('nirf-analytic.html', 'nirf_analytic.html')


@main_bp.route('/tnea-colleges')
def tnea_colleges():
    return render_reference_page('tnea-colleges.html', 'tnea_colleges.html')


@main_bp.route('/free-report')
def free_report():
    return render_reference_page('free-report.html', 'free_report.html')


@main_bp.route('/branch-fitness-assessment')
def branch_fitness_assessment():
    return render_reference_page('branch-fitness-assessment.html', 'branch_fitness_assessment.html')


@main_bp.route('/about')
def about():
    return render_reference_page('about.html', 'about.html')


# =============================================================
# Membership / member-facing pages (wired to auth + membership system)
# =============================================================
@main_bp.route('/members-registration')
def members_registration():
    # Public premium-membership page with the application form (posts to membership.apply)
    return render_template('members_registration.html')


# Legacy alias used in live nav
@main_bp.route('/premium-membership')
def premium_membership():
    return redirect(url_for('main.members_registration'))


@main_bp.route('/members-login')
def members_login():
    return redirect(url_for('auth.login'))


# =============================================================
# EA Team / Counsellor Portal — internal staff tools (admin only).
#
# The interactive tools still run on the existing Google Apps Script /
# Sheets backend. We gate ENTRY with our own RBAC (admin tier) and hand
# off to the live tool; each body is swapped for an in-app version as it
# is migrated (Choice Builder PRO code pending from the team).
# =============================================================


def _portal_tool(title, desc, live_url, features):
    return render_template('portal_tool.html', tool_title=title,
                           tool_desc=desc, live_url=live_url, features=features)


@main_bp.route('/ea-admin-portal')
@admin_required
def ea_admin_portal():
    # The in-app EA Admin Control Panel replaces the legacy Apps Script portal.
    return redirect(url_for('admin_portal.home'))


@main_bp.route('/choice-builder')
def choice_builder_alias():
    # short URL for the Choice Builder PRO tool (which itself requires Premium access)
    return redirect(url_for('main.choice_builder_pro'), code=301)


@main_bp.route('/choice-builder-pro')
@premium_required        # included in Premium Portal Access (admins pass too)
def choice_builder_pro():
    # The full DASA 2026 Choice Builder PRO + Allotment Analyzer tool, migrated
    # in-app from the team's build (client-side D3 / Chart.js, no backend).
    return render_template('choice_builder_pro.html')


@main_bp.route('/dasa2026-expert-report')
@admin_required
def dasa2026_expert_report():
    return _portal_tool(
        'DASA 2026 Expert Report',
        'Generate the personalised DASA/CIWG decision-matrix report for a student.',
        url_for('main.dasa_prediction_report'),     # the DASA expert portal page was removed; the prediction report is the nearest tool
        [{'icon': '\U0001F3AF', 'title': 'College predictor', 'text': 'NITs & IIITs decision-matrix tuned to the JEE rank.'},
         {'icon': '\U0001F9ED', 'title': 'Choice strategy', 'text': 'CIWG vs Non-CIWG option analysis and ordering.'},
         {'icon': '\U0001F468‍\U0001F3EB', 'title': 'Expert guidance', 'text': 'Counsellor support through choice filling.'}])


# =============================================================
# Premium member tools / analyses (premium tier required)
# =============================================================
def _premium(title, desc, features):
    return render_template('premium_tool.html', tool_title=title,
                           tool_desc=desc, features=features)


@main_bp.route('/dasa-prediction-report')
@premium_required
def dasa_prediction_report():
    return _premium('DASA Prediction Report', 'Your personalised DASA/CIWG college-prediction report, member edition.',
                    [{'icon': '\U0001F3AF', 'title': 'Personalised choice-filling report', 'text': 'Colleges and branches matched to your DASA rank and quota, in the order to fill them.'},
                     {'icon': '\U0001F4CA', 'title': 'Chance analysis', 'text': 'Safe / moderate / reach classification for every option.'},
                     {'icon': '\U0001F4DD', 'title': 'Counsellor notes', 'text': 'Expert commentary added to your report before delivery.'}])


# The pages below are full ports of the live-site premium content
# (migrated from the Hostinger embeds; see migration/ notes).
@main_bp.route('/mentorship-templates')
@admin_required
def mentorship_templates():
    from app.data.mentorship_templates import GROUPS, GUIDELINES
    from app.services.company import fill_bank_details
    return render_template('mentorship_templates.html', groups=fill_bank_details(GROUPS), guidelines=GUIDELINES)


# Legacy eduaakashaa.in paths (printed QR codes, old links) that now live elsewhere
@main_bp.route('/tnea-2026')
def tnea_2026_legacy():
    return redirect(url_for('main.tnea2026'), code=301)


@main_bp.route('/services')
def services_legacy():
    return redirect(url_for('main.premium_membership'), code=301)


@main_bp.route('/internship-programs')
def internship_programs_legacy():
    return redirect(url_for('main.contact'), code=301)


@main_bp.route('/josaa-2026-analytics')
@premium_required
def josaa_2026_analytics():
    # premium page: JoSAA 2026 seats and Round 1 to 5 ranks (data: app/static/data/josaa_2026.json, built by tools/josaa2026/build.py)
    return render_template('josaa_2026_analytics.html')


@main_bp.route('/dasa-2026-analytics')
@premium_required
def dasa_2026_analytics():
    return render_template('dasa_2026_analytics.html')


@main_bp.route('/medicine')
def medicine():
    # overview of every medicine entrance-exam page (the list lives in services/medicine_hub.py)
    from app.services import medicine_hub
    return render_template('medicine_hub.html', pages=medicine_hub.PAGES)


@main_bp.route('/neet-2027')
@main_bp.route('/neet-ug-2027')
def neet_2027():
    # public page: what is and is not announced for NEET UG 2027, pattern, eligibility, counselling and a preparation plan (keep dates in step with the NTA notice)
    return render_template('neet_2027.html')


@main_bp.route('/jee-main-2027-registration')
def jee_registration():
    # public page for members and visitors: JEE Main 2027 registration, from the EduAakashaA NRI registration guide (31 Oct 2026); keep dates in step with the NTA notice
    from app.data import jee_registration as d
    return render_template('jee_registration.html', d=d)


@main_bp.route('/jee-registration')
@main_bp.route('/jee-main-registration')
def jee_registration_alias():
    return redirect(url_for('main.jee_registration'), code=301)


@main_bp.route('/jee-main-2027-paper-2-barch-bplanning')
def jee_paper2():
    # public page: JEE Main 2027 Paper 2A (B.Arch) and 2B (B.Planning): deadlines, pattern, syllabus, interest check; from NTA's 2027 bulletin and syllabus, keep in step with NTA notices
    from app.data import jee_paper2 as d
    return render_template('jee_paper2.html', d=d)


@main_bp.route('/jee-paper-2')
@main_bp.route('/jee-main-paper-2')
@main_bp.route('/jee-barch-bplanning')
def jee_paper2_alias():
    return redirect(url_for('main.jee_paper2'), code=301)


@main_bp.route('/nid-papers-analysis')
def nid_papers():
    # public page: NID DAT past papers analysed (format by year, topic mix, open-task themes), free sample questions, links to the mock centre and the NID add-on; data in app/data/nid_papers.py and app/data/nid/analysis.json
    from app.data import nid_papers as d
    return render_template('nid_papers.html', d=d, **d.context())


@main_bp.route('/nid-previous-papers')
@main_bp.route('/nid-mock-test')
@main_bp.route('/nid-dat-papers')
def nid_papers_alias():
    return redirect(url_for('main.nid_papers'), code=301)


@main_bp.route('/nift-papers-analysis')
def nift_exam():
    # public page: NIFT GAT / CAT past papers analysed (format by year, section mix, CAT themes), free sample questions, links to the mock centre; data in app/data/nift_exam.py and app/data/nift/analysis.json
    from app.data import nift_exam as d
    return render_template('nift_exam.html', **d.context())


@main_bp.route('/nift-previous-papers')
@main_bp.route('/nift-mock-test')
@main_bp.route('/nift-gat-papers')
def nift_exam_alias():
    return redirect(url_for('main.nift_exam'), code=301)


@main_bp.route('/explorer-test')
def explorer_landing():
    # public page: EduPulse-Explorer for Grades 7 to 10 (what it is, exam families, spaced review, six free questions); data in app/data/explorer_landing.py
    from app.data import explorer_landing as d
    return render_template('explorer_landing.html', **d.context())


@main_bp.route('/grade-7-10-mock-test')
@main_bp.route('/discovery-test-grade-7-10')
def explorer_alias():
    return redirect(url_for('main.explorer_landing'), code=301)


@main_bp.route('/engineering-colleges-by-city')
def engineering_cities():
    # public page: top NIRF-ranked engineering colleges per city region and state with fee, eligibility and NRI quota; data in app/data/eng_cities.py, eng_cities.json, eng_colleges.json
    from app.data import eng_cities as d
    ctx = d.context()
    eng = dict(cities=ctx['cities'], states=ctx['states'], colleges=ctx['colleges'], tile=url_for('static', filename='img/colleges/'), types=d.TYPE_LABEL)
    return render_template('engineering_cities.html', d=d, cities=ctx['cities'], states=ctx['states'], colleges=ctx['colleges'], eng=eng)


@main_bp.route('/top-engineering-colleges')
@main_bp.route('/engineering-colleges-by-state')
@main_bp.route('/engineering-colleges-city')
def engineering_cities_alias():
    return redirect(url_for('main.engineering_cities'), code=301)


@main_bp.route('/architecture-planning-india')
def architecture_planning():
    # public page: B.Arch and B.Planning colleges state by state, admission routes, fees, placements, NRI quota, NIRF 2025, JoSAA 2026; data in app/data/arch_planning.py and arch_colleges.json
    from app.data import arch_planning as d
    return render_template('architecture_planning.html', d=d, **d.guide_context())


@main_bp.route('/architecture-planning-analytics')
def architecture_analytics():
    # public page: charts and a rank finder from the JoSAA 2026 rounds, NIRF 2025 Architecture list, DASA 2025/2026 and the NIT+ seat matrix
    from app.data import arch_planning as d
    return render_template('architecture_analytics.html', d=d, **d.analytics_context())


@main_bp.route('/architecture-colleges')
@main_bp.route('/barch-colleges')
@main_bp.route('/architecture-planning')
def architecture_planning_alias():
    return redirect(url_for('main.architecture_planning'), code=301)


@main_bp.route('/barch-bplanning-mentorship')
@premium_required
def barch_mentorship():
    # members: B.Arch and B.Planning mentorship programme (sessions live in app/data/mentorship_addons.py, keys barch and bplan)
    from app.data import barch_programme as p
    from app.data.mentorship_addons import ADDONS
    by = {x['key']: x for x in ADDONS}
    return render_template('barch_mentorship.html', p=p, barch=by['barch'], bplan=by['bplan'])


@main_bp.route('/iiser-aptitude-test')
def iat():
    # public page: IISER Aptitude Test (IAT): pattern, dates, eligibility, institutes, syllabus, past papers; from the IAT 2026 brochure and iiseradmission.in; keep in step with that site
    from app.data import iat as d
    from app.data.mentorship_addons import ADDONS
    addon = next(x for x in ADDONS if x['key'] == 'iiser')
    return render_template('iat.html', d=d, addon=addon, mock=_iat_mock_ready())


def _iat_mock_ready():
    try:
        from app.services import iat as svc
        return bool(svc.papers())
    except ImportError:
        return False


@main_bp.route('/iat')
@main_bp.route('/iiser')
@main_bp.route('/iiser-admission')
def iat_alias():
    return redirect(url_for('main.iat'), code=301)


@main_bp.route('/jee-2027-roadmap')
@premium_required
def jee_2027_roadmap():
    return render_template('jee_2027_roadmap.html')


@lru_cache(maxsize=1)
def _jee_syllabus_data():
    # chapter weightage from the 19 JEE Main 2026 shifts (app/data/jee_syllabus_2026.json) joined to the formula sheet (app/data/jee_formulas.py)
    from app.data.jee_formulas import FORMULAS
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'jee_syllabus_2026.json'), encoding='utf-8') as f:
        data = json.load(f)
    for c in data['chs']:
        c['tier_n'] = int(c['tier'][-1]) if c['tier'].startswith('Tier') else 0
        c['formulas'] = FORMULAS.get(c['ch'], [])
        c['search'] = ' '.join([c['nat'], c.get('pre', ''), c.get('feed', '')] + c.get('topics', []) + [lbl for lbl, _ in c['formulas']]).lower()
    return data


@main_bp.route('/jee-main-2026-syllabus-map')
@premium_required
def jee_syllabus_map():
    data = _jee_syllabus_data()
    class11 = sum(c['n'] for c in data['chs'] if c['cls'] == 11)
    return render_template('jee_syllabus_map.html', chapters=sorted(data['chs'], key=lambda c: -c['n']), stats=data['stats'], papers=data['papers'], nj=data['nj'],
                           subjects=('Mathematics', 'Physics', 'Chemistry'), class11_pct=round(100 * class11 / data['stats']['NQ']))


# Institutes listed on the official UCEED 2027 site (uceed.iitb.ac.in/2027, checked 17 Oct 2026)
UCEED_INSTITUTES = [
    ('IIT Bombay', 'Mumbai', 'https://www.iitb.ac.in'), ('IIT Delhi', 'New Delhi', 'https://home.iitd.ac.in'),
    ('IIT Guwahati', 'Guwahati', 'https://www.iitg.ac.in'), ('IIT Hyderabad', 'Hyderabad', 'https://iith.ac.in'),
    ('IIT Indore', 'Indore', 'https://www.iiti.ac.in'), ('IIT Roorkee', 'Roorkee', 'https://www.iitr.ac.in'),
    ('IIITDM Jabalpur', 'Jabalpur', 'https://www.iiitdmj.ac.in'),
]


# The 26 National Law Universities listed as Consortium members on consortiumofnlus.ac.in (checked 17 Oct 2026)
CLAT_NLUS = [
    ('NLSIU', 'Bengaluru'), ('NALSAR', 'Hyderabad'), ('NLIU', 'Bhopal'), ('WBNUJS', 'Kolkata'), ('NLU Jodhpur', 'Jodhpur'),
    ('HNLU', 'Raipur'), ('GNLU', 'Gandhinagar'), ('RMLNLU', 'Lucknow'), ('RGNUL', 'Patiala'), ('CNLU', 'Patna'),
    ('NUALS', 'Kochi'), ('NLUO', 'Cuttack'), ('NUSRL', 'Ranchi'), ('NLUJA', 'Guwahati'), ('DSNLU', 'Visakhapatnam'),
    ('TNNLU', 'Tiruchirappalli'), ('MNLU Mumbai', 'Mumbai'), ('MNLU Nagpur', 'Nagpur'), ('MNLU Aurangabad', 'Chhatrapati Sambhajinagar'),
    ('HPNLU', 'Shimla'), ('DNLU', 'Jabalpur'), ('DBRANLU', 'Sonipat'), ('NLU Tripura', 'Agartala'), ('RPNLU', 'Prayagraj'),
    ('IIULER', 'Goa'), ('NLU Meghalaya', 'Shillong'),
]


@main_bp.route('/law-2027-roadmap')
@premium_required
def law_2027_roadmap():
    from app.services import roadmap_cfg
    return render_template('law_roadmap.html', cfg=roadmap_cfg.LAW, nlus=CLAT_NLUS)


# IIMs reported to run a five-year IPM (sources conflict on the full list; routes are reported, not confirmed — checked 18 Oct 2026)
IPM_IIMS = [
    ('IIM Indore', 'Indore', 'IPMAT Indore'), ('IIM Rohtak', 'Rohtak', 'IPMAT Rohtak'),
    ('IIM Ranchi', 'Ranchi', 'IPMAT Indore score (reported)'), ('IIM Bodh Gaya', 'Bodh Gaya', 'JIPMAT'), ('IIM Jammu', 'Jammu', 'JIPMAT'),
]


@main_bp.route('/ipm-2027-roadmap')
@premium_required
def ipm_2027_roadmap():
    from app.services import roadmap_cfg
    return render_template('ipm_roadmap.html', cfg=roadmap_cfg.IPM, iims=IPM_IIMS)


@main_bp.route('/engineering-in-gulf/caet-iit-delhi-abu-dhabi')
@premium_required
def gulf_caet_guide():
    return render_template('gulf_caet.html')


@main_bp.route('/engineering-in-gulf/caet-iit-delhi-abu-dhabi/guide')
@premium_required
def gulf_caet_guide_file():
    """The self-contained CAET guide (bundled page). Served from a members-only route and sandboxed: it runs in its own opaque origin,
    so its scripts can never read this site's cookies or pages."""
    import os
    from flask import current_app, send_file
    path = os.path.join(current_app.root_path, 'data', 'gulf', 'caet-iitd-abu-dhabi.html')
    resp = send_file(path, mimetype='text/html', max_age=0)
    resp.headers['Content-Security-Policy'] = 'sandbox allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads allow-forms'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Cache-Control'] = 'private, no-cache'
    return resp


@main_bp.route('/uceed-2027-roadmap')
@premium_required
def uceed_2027_roadmap():
    from app.services import roadmap_cfg
    return render_template('uceed_roadmap.html', institutes=UCEED_INSTITUTES, cfg=roadmap_cfg.UCEED)


@main_bp.route('/why-cse')
@premium_required
def why_cse():
    return render_template('why_cse.html')


@main_bp.route('/best-location')
@premium_required
def best_location():
    return render_template('best_location.html')


@main_bp.route('/engineering-insights')
@premium_required
def engineering_insights():
    return render_template('engineering_insights.html')


@main_bp.route('/hostel-and-culture-analytics')
@premium_required
def hostel_culture_analytics():
    return render_template('hostel_culture_analytics.html')


@main_bp.route('/tnea-expert')
@premium_required
def tnea_expert():
    return render_template('tnea_expert.html')


@main_bp.route('/engineering-branch-selection-guide')
@premium_required
def engineering_branch_selection_guide():
    return render_reference_page('engineering-branch-selection-guide.html', 'engineering_branch_selection_guide.html')


# =============================================================
# Legacy / duplicate slug aliases (eduaakashaa.in URL parity)
# =============================================================
@main_bp.route('/ea-home')
@main_bp.route('/eahome')
@main_bp.route('/eahomepage')
def home_alias():
    return redirect(url_for('main.home'))


@main_bp.route('/josaa-2026')
@main_bp.route('/josaa-predictor')
def josaa_alias():
    return redirect(url_for('main.josaa'))


@main_bp.route('/contactus')
def contactus_alias():
    return redirect(url_for('main.contact'))


@main_bp.route('/dasaseatmatrix')
def dasaseatmatrix_alias():
    return redirect(url_for('main.dasa_seat_matrix'))
