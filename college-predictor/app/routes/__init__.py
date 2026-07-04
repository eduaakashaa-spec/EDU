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
    return render_reference_page('dasa-admissions-guide.html', 'nri_guide.html')


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


@main_bp.route('/internship-programs')
def internship():
    return render_reference_page('internship-programs.html', 'internship.html')


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
    return render_reference_page('exam-schedule.html', 'exam_schedule.html')


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


@main_bp.route('/expert-portaldasa')
@premium_required
def expert_portal_dasa():
    return render_reference_page('expert-portaldasa.html', 'expert_portal_dasa.html')


@main_bp.route('/tnea-expert-guidance')
def tnea_expert_guidance():
    return render_reference_page('tnea-expert-guidance.html', 'tnea_expert_guidance.html')


@main_bp.route('/videos-library')
def videos_library():
    return render_reference_page('videos-library.html', 'videos_library.html')


@main_bp.route('/training')
def training():
    return render_reference_page('training.html', 'training.html')


@main_bp.route('/nri-admission')
def nri_admission():
    return render_reference_page('nri-admission.html', 'nri_admission.html')


@main_bp.route('/nriarabic-foundation')
def nriarabic_foundation():
    return render_reference_page('nriarabic-foundation.html', 'nriarabic_foundation.html')


@main_bp.route('/nriarabicgr')
def nriarabicgr():
    return render_reference_page('nriarabicgr.html', 'nriarabicgr.html')


# =============================================================
# New public content pages (eduaakashaa.in nav parity) — built from live captures
# =============================================================
@main_bp.route('/dasa-2026')
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
_LIVE_SITE = 'https://www.eduaakashaa.in'


def _portal_tool(title, desc, live_url, features):
    return render_template('portal_tool.html', tool_title=title,
                           tool_desc=desc, live_url=live_url, features=features)


@main_bp.route('/counsellor-dashboard')
@admin_required
def counsellor_dashboard():
    return _portal_tool(
        'Counsellor Dashboard',
        'Review student DASA 2026 preference submissions, sort by confidence and export as CSV.',
        f'{_LIVE_SITE}/counsellor-dashboard',
        [{'icon': '\U0001F4CB', 'title': 'Student submissions', 'text': 'Every DASA 2026 preference list submitted through Choice Builder.'},
         {'icon': '\U0001F522', 'title': 'Sort & triage', 'text': 'Order by newest or by confidence to prioritise outreach.'},
         {'icon': '\U0001F4E4', 'title': 'CSV export', 'text': 'Download the full submission set for offline review.'}])


@main_bp.route('/ea-admin-portal')
@admin_required
def ea_admin_portal():
    # Our Flask membership admin replaces the legacy Apps Script admin portal.
    return redirect(url_for('membership.admin_list'))


@main_bp.route('/choice-builder-pro')
@admin_required
def choice_builder_pro():
    return _portal_tool(
        'Choice Builder PRO',
        'Guided DASA 2026 preference-list builder — rank colleges and submit for counsellor review.',
        f'{_LIVE_SITE}/choice-builder-pro',
        [{'icon': '\U0001F9F1', 'title': 'Smart ordering', 'text': 'Safe / match / reach ordering tuned to rank and quota.'},
         {'icon': '✅', 'title': 'Validation', 'text': 'Catch gaps, duplicates and risky ordering before submitting.'},
         {'icon': '\U0001F4DD', 'title': 'Counsellor review', 'text': 'Submissions land in the Counsellor Dashboard.'}])


@main_bp.route('/choice-builder-pro-2')
@admin_required
def choice_builder_pro_2():
    return _portal_tool(
        'Choice Builder PRO 2',
        'Second-round DASA 2026 choice-builder variant for revised preference lists.',
        f'{_LIVE_SITE}/choice-builder-pro-2',
        [{'icon': '\U0001F501', 'title': 'Round 2 lists', 'text': 'Rebuild preferences for later counselling rounds.'},
         {'icon': '\U0001F9ED', 'title': 'Revised strategy', 'text': 'Adjust ordering after Round 1 allotment results.'},
         {'icon': '\U0001F4DD', 'title': 'Counsellor review', 'text': 'Submissions land in the Counsellor Dashboard.'}])


@main_bp.route('/dasa2026-expert-report')
@admin_required
def dasa2026_expert_report():
    return _portal_tool(
        'DASA 2026 Expert Report',
        'Generate the personalised DASA/CIWG decision-matrix report for a student.',
        f'{_LIVE_SITE}/dasa2026-expert-report',
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
                    [{'icon': '\U0001F3AF', 'title': 'Personalised list', 'text': 'Colleges and branches matched to your DASA rank and quota.'},
                     {'icon': '\U0001F4CA', 'title': 'Chance analysis', 'text': 'Safe / moderate / reach classification for every option.'},
                     {'icon': '\U0001F4DD', 'title': 'Counsellor notes', 'text': 'Expert commentary added to your report before delivery.'}])


@main_bp.route('/why-cse')
@premium_required
def why_cse():
    return _premium('Why CSE?', 'Data-driven analysis of the Computer Science branch — demand, placements, and fit.',
                    [{'icon': '\U0001F4BB', 'title': 'Demand & placements', 'text': 'Branch-level placement and salary trends across top institutes.'},
                     {'icon': '\U0001F9ED', 'title': 'Is CSE right for you?', 'text': 'Aptitude and interest mapping against the CSE curriculum.'},
                     {'icon': '\U0001F4CA', 'title': 'Alternatives compared', 'text': 'CSE vs allied branches (AI/DS, ECE, IT) with trade-offs.'}])


@main_bp.route('/best-location')
@premium_required
def best_location():
    return _premium('Best Location Analyzer', 'Compare colleges by city, cost of living, climate and opportunity.',
                    [{'icon': '\U0001F4CD', 'title': 'City comparison', 'text': 'Weigh metros vs tier-2 cities on cost, safety and exposure.'},
                     {'icon': '\U0001F4B0', 'title': 'Cost of living', 'text': 'Realistic hostel, food and travel estimates per location.'},
                     {'icon': '\U0001F91D', 'title': 'Opportunity index', 'text': 'Internships, industry presence and alumni networks by region.'}])


@main_bp.route('/engineering-insights')
@premium_required
def engineering_insights():
    return _premium('Engineering Insights', 'Curated branch, college and career insights for confident decisions.',
                    [{'icon': '\U0001F50D', 'title': 'Branch deep-dives', 'text': 'What each branch actually studies and leads to.'},
                     {'icon': '\U0001F3DB️', 'title': 'College intel', 'text': 'Placement, faculty and infrastructure signals that matter.'},
                     {'icon': '\U0001F4C8', 'title': 'Career mapping', 'text': 'Where each path leads — roles, sectors and growth.'}])


@main_bp.route('/hostel-and-culture-analytics')
@premium_required
def hostel_culture_analytics():
    return _premium('Hostel & Culture Analytics', 'Campus life, hostel quality and culture — the factors brochures hide.',
                    [{'icon': '\U0001F3E0', 'title': 'Hostel quality', 'text': 'Rooms, mess, facilities and real student feedback.'},
                     {'icon': '\U0001F389', 'title': 'Campus culture', 'text': 'Clubs, fests, diversity and day-to-day student life.'},
                     {'icon': '⚖️', 'title': 'Fit assessment', 'text': 'Match campus environment to the student’s personality.'}])


@main_bp.route('/tnea-expert')
@premium_required
def tnea_expert():
    return _premium('TNEA Expert', 'End-to-end TNEA counselling — cutoff, choice filling and allotment strategy.',
                    [{'icon': '\U0001F4D0', 'title': 'Cutoff mastery', 'text': 'Your cutoff, category analysis and realistic targets.'},
                     {'icon': '\U0001F9F1', 'title': 'Choice filling', 'text': 'College-code strategy and lookalike-college guidance.'},
                     {'icon': '\U0001F4DE', 'title': 'Allotment support', 'text': 'Round-by-round guidance until you confirm a seat.'}])


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
