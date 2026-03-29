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
    return render_template('placeholder.html', title='IIITs', heading='IIITs Information')


@main_bp.route('/annanri')
def annanri():
    return render_template('placeholder.html', title='Anna NRI', heading='Anna University NRI Admission')


@main_bp.route('/dasa-seat-matrix')
def dasa_seat_matrix():
    return render_template('placeholder.html', title='DASA Seat Matrix', heading='DASA Seat Matrix')


@main_bp.route('/dasa-admissions-guide')
def dasa_guide():
    return render_template('placeholder.html', title='DASA/CIWG Guide', heading='DASA & CIWG Admissions Guide')


@main_bp.route('/nirf-ranking')
def nirf_ranking():
    return render_template('placeholder.html', title='NIRF Ranking', heading='NIRF Engineering Rankings')


@main_bp.route('/tnea2026')
def tnea2026():
    return render_template('placeholder.html', title='TNEA 2026', heading='TNEA 2026 Admissions')


@main_bp.route('/tneamatrix')
def tneamatrix():
    return render_template('placeholder.html', title='TNEA Matrix', heading='TNEA Seat Matrix')


@main_bp.route('/tneapc')
def tneapc():
    return render_template('placeholder.html', title='TNEA PC', heading='TNEA Preference Calculator')


@main_bp.route('/tnea-cutoff')
def tnea_cutoff():
    return render_template('placeholder.html', title='TNEA Cutoff', heading='TNEA Cutoff Analysis')


@main_bp.route('/professional-exam')
def professional_exam():
    return render_template('placeholder.html', title='Professional Exam', heading='Professional Exam Guide')


@main_bp.route('/internship-programs')
def internship():
    return render_template('placeholder.html', title='Internship Programs', heading='Internship Programs')


@main_bp.route('/contact')
def contact():
    return render_template('placeholder.html', title='Contact', heading='Contact EduAakashaa')


@main_bp.route('/mbamca-program')
def mbamca():
    return render_template('placeholder.html', title='MBA/MCA Program', heading='MBA & MCA Program Guide')


@main_bp.route('/tancet')
def tancet():
    return render_template('placeholder.html', title='TANCET', heading='TANCET Exam Guide')


@main_bp.route('/ea-library')
def ea_library():
    return render_template('placeholder.html', title='EA Library', heading='EduAakashaa Library')


@main_bp.route('/tancet-pulse')
def tancet_pulse():
    return render_template('placeholder.html', title='TANCET PULSE', heading='TANCET PULSE')


@main_bp.route('/viteee-for-nri')
def viteee_nri():
    return render_template('placeholder.html', title='VITEEE for NRI', heading='VITEEE for NRI Students')
