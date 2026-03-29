from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('home.html')


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


@main_bp.route('/tnea2026')
def tnea2026():
    return render_template('tnea2026.html')


@main_bp.route('/tneamatrix')
def tneamatrix():
    return render_template('tneamatrix.html')


@main_bp.route('/tneapc')
def tneapc():
    return render_template('tneapc.html')


@main_bp.route('/tnea-cutoff')
def tnea_cutoff():
    return render_template('tnea_cutoff.html')


@main_bp.route('/professional-exam')
def professional_exam():
    return render_template('professional_exam.html')


@main_bp.route('/internship-programs')
def internship():
    return render_template('internship.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


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
