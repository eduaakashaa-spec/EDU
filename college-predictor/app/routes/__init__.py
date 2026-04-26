from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)


# =============================================================
# Core pages
# =============================================================
@main_bp.route('/')
def home():
    return render_template('home.html')


# URL parity with the legacy Hostinger site
@main_bp.route('/homepage')
def homepage_alias():
    return redirect(url_for('main.home'), code=301)


@main_bp.route('/nri-admissions-guide')
def nri_guide():
    return render_template('nri_guide.html')


@main_bp.route('/josaa')
def josaa():
    return render_template('josaa.html')


@main_bp.route('/iiits')
def iiits():
    return render_template('iiits.html')


@main_bp.route('/annanri')
def annanri():
    return render_template('annanri.html')


@main_bp.route('/dasa-seat-matrix')
def dasa_seat_matrix():
    return render_template('dasa_seat_matrix.html')


@main_bp.route('/dasa-admissions-guide')
def dasa_guide():
    return render_template('dasa_guide.html')


@main_bp.route('/nirf-ranking')
def nirf_ranking():
    return render_template('nirf_ranking.html')


# =============================================================
# TNEA cluster
# =============================================================
@main_bp.route('/tnea2026')
def tnea2026():
    return render_template('tnea2026.html')


# /tnea on the legacy site mirrors /tnea2026 content
@main_bp.route('/tnea')
def tnea_alias():
    return redirect(url_for('main.tnea2026'), code=301)


@main_bp.route('/tneamatrix')
def tneamatrix():
    return render_template('tneamatrix.html')


@main_bp.route('/tneapc')
def tneapc():
    return render_template('tneapc.html')


@main_bp.route('/tnea-cutoff')
def tnea_cutoff():
    return render_template('tnea_cutoff.html')


@main_bp.route('/tnea-simulator')
def tnea_simulator():
    return render_template('tnea_simulator.html')


# =============================================================
# Professional & content pages
# =============================================================
@main_bp.route('/professional-exam')
def professional_exam():
    return render_template('professional_exam.html')


@main_bp.route('/internship-programs')
def internship():
    return render_template('internship.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


# Legacy URL used on Hostinger
@main_bp.route('/contact-us')
def contact_alias():
    return redirect(url_for('main.contact'), code=301)


@main_bp.route('/mbamca-program')
def mbamca():
    return render_template('mbamca.html')


@main_bp.route('/tancet')
def tancet():
    return render_template('tancet.html')


@main_bp.route('/ea-library')
def ea_library():
    return render_template('ea_library.html')


@main_bp.route('/tancet-pulse')
def tancet_pulse():
    return render_template('tancet_pulse.html')


@main_bp.route('/viteee-for-nri')
def viteee_nri():
    return render_template('viteee_nri.html')


# =============================================================
# Newly implemented pages (parity with Hostinger legacy)
# =============================================================
@main_bp.route('/amrita-aeee')
def amrita_aeee():
    return render_template('amrita_aeee.html')


@main_bp.route('/nata')
def nata():
    return render_template('nata.html')


@main_bp.route('/nid')
def nid():
    return render_template('nid.html')


@main_bp.route('/cat')
def cat():
    return render_template('cat.html')


@main_bp.route('/josaa-assessment')
def josaa_assessment():
    return render_template('josaa_assessment.html')


@main_bp.route('/student-assessment')
def student_assessment():
    return render_template('student_assessment.html')


@main_bp.route('/conflict-assessment')
def conflict_assessment():
    return render_template('conflict_assessment.html')


@main_bp.route('/stream-selection')
def stream_selection():
    return render_template('stream_selection.html')


@main_bp.route('/exam-schedule')
def exam_schedule():
    return render_template('exam_schedule.html')


@main_bp.route('/join-our-team')
def join_our_team():
    return render_template('join_our_team.html')


# Gated portals – require login to view content
@main_bp.route('/stream-selectionea')
def stream_selection_ea():
    return render_template('stream_selection_ea.html')


@main_bp.route('/josaaea-members')
def josaa_ea_members():
    return render_template('josaa_ea_members.html')
