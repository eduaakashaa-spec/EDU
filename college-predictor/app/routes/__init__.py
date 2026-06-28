from pathlib import Path

from flask import Blueprint, Response, abort, current_app, redirect, render_template, url_for

main_bp = Blueprint('main', __name__)


def render_reference_page(filename: str, fallback_template: str | None = None, **context):
    ref_dir = Path(current_app.root_path).parent / 'reference' / 'live_pages' / 'html'
    ref_file = ref_dir / filename
    if ref_file.exists():
        return Response(ref_file.read_text(encoding='utf-8'), mimetype='text/html')
    if fallback_template:
        return render_template(fallback_template, **context)
    abort(404)


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
def members_report():
    return render_reference_page('members-report.html', 'members_report.html')


@main_bp.route('/expert-portaldasa')
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
