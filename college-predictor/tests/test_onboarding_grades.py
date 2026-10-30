"""Grade-banded membership onboarding assessment: Class 7-9 (stream selection), Class 10-11 (colleges, branch, career goal), Class 12 (the original).
Run from college-predictor/:  python tests/test_onboarding_grades.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import OnboardingResponse, User  # noqa: E402
from app.routes.onboarding import _when_met  # noqa: E402
from app.services import onboarding_assessment as oa  # noqa: E402

# ---- the bank itself ------------------------------------------------------------------------------------------------------------------------------------
for role in ('student', 'parent'):
    items = oa.items_for(role)
    ids = [i['id'] for i in items]
    assert len(ids) == len(set(ids)), 'duplicate item id in %s' % role
    seen = set()
    for it in items:
        w = it.get('when') or {}
        for g in (w if isinstance(w, list) else [w]):
            assert set(g) <= seen, (it['id'], 'gate refers to a later or unknown item', set(g) - seen)
        seen.add(it['id'])
        if it['type'] in ('choice', 'rank', 'pick', 'mostleast'):
            assert it.get('options'), it['id']
for k, v in oa.ANSWER_KEY.items():
    it = next(i for i in oa.items_for('student') + oa.items_for('parent') if i['id'] == k)
    assert v in it['options'], (k, v)                                     # every scored answer is one of the options

PATH = {'eng': 'Engineering', 'med': 'Medicine and health', 'law': 'Law', 'mgt': 'Management and business', 'oth': 'Design, arts or something else', 'none': 'Not decided yet'}


def shown(role, cls, path=None):
    """Item ids this respondent would be asked, simulating the form (answers given to the gate questions only)."""
    ans, out = {}, []
    k = ('S61', 'S63') if role == 'student' else ('P35', 'P36')
    for it in oa.items_for(role):
        if it['id'] == k[0]:
            ans[k[0]] = cls
        if it['id'] == k[1] and path:
            ans[k[1]] = PATH[path]
        if _when_met(it, ans):
            out.append(it['id'])
    return set(out)


# ---- Class 7-9: stream selection ----------------------------------------------------------------------------------------------------------------------------
for c in ('Class 7', 'Class 8', 'Class 9'):
    s = shown('student', c)
    assert {'S61', 'S62', 'EX1', 'EX20', 'EX23', 'EX27', 'EX30', 'EX35', 'EX39'} <= s, c
    assert not (s & {'S63', 'S1', 'S9', 'S15', 'S25', 'S33', 'CX1', 'CY1', 'MD1', 'N11P1', 'S57'}), c      # no colleges, branches or Class 11-12 content
    assert 25 <= len(s) <= 50, (c, len(s))
    p = shown('parent', c)
    assert {'P35', 'P36', 'PX1', 'PX3', 'PX6', 'P7', 'P26'} <= p and not (p & {'P12', 'P17', 'P8', 'PC1'}), c

# ---- Class 10-11: colleges, branch, career goal ------------------------------------------------------------------------------------------------------------------
s = shown('student', 'Class 10', 'eng')
assert {'S63', 'CX1', 'CX2', 'CX3', 'CX10', 'S15', 'S25', 'S33', 'CY1', 'CY3', 'S45', 'S57'} <= s and not (s & {'S1', 'N11P1', 'MD1', 'EX1'})
s = shown('student', 'Class 11', 'eng')
assert {'S1', 'S9', 'N11P1', 'S25', 'S33', 'S55', 'CY2'} <= s and not (s & {'CX2', 'CX4', 'CX10', 'N12P1', 'MD1'})   # engineering Class 11 keeps the original blocks
for c in ('Class 10', 'Class 11', 'Class 12'):
    assert {'MD1', 'MD7', 'CY1', 'CX1'} <= shown('student', c, 'med') and not (shown('student', c, 'med') & {'S25', 'S33', 'LW1', 'MG1', 'S55'}), c
    assert {'LW1', 'LW7'} <= shown('student', c, 'law') and not (shown('student', c, 'law') & {'MD1', 'MG1', 'S25'}), c
    assert {'MG1', 'MG6'} <= shown('student', c, 'mgt') and not (shown('student', c, 'mgt') & {'MD1', 'LW1', 'S25'}), c
    assert {'UD1', 'UD3', 'CY1'} <= shown('student', c, 'none') and not (shown('student', c, 'none') & {'MD1', 'S25'}), c
    assert {'UD4', 'UD5'} <= shown('student', c, 'oth'), c
assert 'CX4' in shown('student', 'Class 12', 'med') and 'CX2' not in shown('student', 'Class 12', 'med')
p = shown('parent', 'Class 10', 'med')
assert {'P38', 'P17', 'P22', 'PC1', 'PC4', 'PC5'} <= p and not (p & {'P12', 'P8', 'P1', 'PX1', 'PC2'})
p = shown('parent', 'Class 11', 'eng')
assert {'P1', 'P8', 'P12', 'P14', 'P17', 'P23', 'P24'} <= p and not (p & {'PC4', 'PX1', 'P38'})

# ---- Class 12 engineering: the original instrument, nothing lost -------------------------------------------------------------------------------------------------
s = shown('student', 'Class 12', 'eng')
assert all(('S%d' % n) in s for n in range(1, 61)), sorted(set('S%d' % n for n in range(1, 61)) - s)
assert {'N12P1', 'N12M3', 'S63'} <= s and not (s & {'N11P1', 'MD1', 'EX1'})
p = shown('parent', 'Class 12', 'eng')
assert all(('P%d' % n) in p for n in range(1, 35) if n not in (35,)), sorted(set('P%d' % n for n in range(1, 35)) - p)

# ---- the form and the saved answers -----------------------------------------------------------------------------------------------------------------------------
app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='a@x.com', tier='admin', password_hash=bcrypt.generate_password_hash('x').decode()),
                        User(name='Fam', email='f@x.com', tier='free', password_hash=bcrypt.generate_password_hash('x').decode())])
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


fam, admin = login('f@x.com'), login('a@x.com')
page = fam.get('/onboarding-assessment/student').get_data(as_text=True)
assert 'Class 7' in page and 'Management and business' in page and 'EX23' in page and 'data-when' in page
assert 'Class 7' in fam.get('/onboarding-assessment/parent').get_data(as_text=True)
assert 'Class 7' in fam.get('/onboarding-assessment').get_data(as_text=True)

r = fam.post('/onboarding-assessment/student', data={'student_name': 'Asha K', 'phone': '+919999999999', 'S61': 'Class 8', 'S62': 'CBSE', 'S63': 'Law',
                                                    'EX27': 'Commerce', 'EX23': 'Class 11', 'EX25': 'Mathematics', 'CX1': 'PCM (Physics, Chemistry, Maths)', 'S1_Physics__': '90'})
assert r.status_code in (200, 302), r.status_code
with app.app_context():
    sub = OnboardingResponse.query.filter_by(role='student').one()
    got = sub.responses
    assert got['S61'] == 'Class 8' and got['EX27'] == 'Commerce' and got['EX23'] == 'Class 11'
    assert 'S63' not in got and 'CX1' not in got                         # asked of Class 10 and above only, so dropped for a Class 8 student
    sid = sub.id
page = admin.get('/admin/onboarding/%d' % sid)
assert page.status_code == 200 and b'Asha K' in page.data and b'Class 8' in page.data
dl = admin.get('/admin/onboarding/%d/download' % sid)
assert dl.status_code == 200 and b'EX27' in dl.data and b'[correct:' in dl.data

# ---- admin view: class and path, suggested programme, only the questions that applied ---------------------------------------------------------------------------------
lst = admin.get('/admin/onboarding').get_data(as_text=True)
assert 'Class 8' in lst and 'Explore' in lst
det = admin.get('/admin/onboarding/%d' % sid).get_data(as_text=True)
assert 'Suggested programme' in det and 'Stream and Career Explorer' in det
assert 'EX27' in det and 'S25' not in det and 'N11P1' not in det                      # engineering and Class 11 items did not apply, so they are not listed as unanswered
assert 'Band: Explore' in dl.get_data(as_text=True) and 'DELIVERABLE 2B' in dl.get_data(as_text=True)

# ---- programmes ---------------------------------------------------------------------------------------------------------------------------------------------------
from app.models_mentorship import MsProgramme  # noqa: E402
from app.services import mentorship as msvc, mentorship_grades as mg  # noqa: E402
with app.app_context():
    default = msvc.ensure_default_programme()
    assert mg.ensure_grade_programmes() == 2 and mg.ensure_grade_programmes() == 0
    assert msvc.ensure_default_programme().id == default.id and default.tier == 'Elite Mentorship'          # the new programmes never become the default
    for name in (mg.EXPLORE_PROGRAMME, mg.DIRECT_PROGRAMME):
        pr = MsProgramme.query.filter_by(name=name).one()
        assert pr.templates.count() == 12
    assert mg.suggested_programme('Class 9', '')[0] == mg.EXPLORE_PROGRAMME
    assert mg.suggested_programme('Class 11', 'Law')[0] == mg.DIRECT_PROGRAMME
    assert mg.suggested_programme('Class 12', 'Engineering')[0] == 'Grade 12 Engineering Mentorship'
    assert mg.suggested_programme('Class 12', 'Medicine and health')[0] == mg.DIRECT_PROGRAMME
assert admin.get('/mentorship/admin').status_code == 200

print('onboarding grade-band checks passed')
