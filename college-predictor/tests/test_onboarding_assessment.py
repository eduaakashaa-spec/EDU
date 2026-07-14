"""Self-check for the onboarding assessment: question bank, class gate, pairing.

Covers the three things that silently corrupt a family's dossier if they break:
  1. the NCERT answer key must match the options actually rendered (a typo here
     marks every student wrong forever, and nobody would notice);
  2. the class gate — a class-11 student must never be shown, scored on, or have
     stored, a class-12 question;
  3. account pairing — the student's and the parent's halves land on one
     family_key iff they were filled from the same login.

Hermetic: fresh SQLite, no network, no SMTP.
Run:  ../.venv/bin/python tests/test_onboarding_assessment.py   (from college-predictor/)
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'

from app import create_app                                     # noqa: E402
from app.extensions import db, bcrypt                          # noqa: E402
from app.models import OnboardingResponse, User                # noqa: E402
from app.routes.onboarding import _when_met                    # noqa: E402
from app.services.onboarding_assessment import (ANSWER_KEY, items_for,  # noqa: E402
                                                modules_for)

app = create_app()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

STUDENT = {it['id']: it for it in items_for('student')}
PARENT = {it['id']: it for it in items_for('parent')}


# --------------------------------------------------------------------------- #
# 1. question bank
# --------------------------------------------------------------------------- #
def test_answer_key_matches_options():
    for iid, ans in ANSWER_KEY.items():
        assert iid in STUDENT, 'answer key for unknown item %s' % iid
        opts = STUDENT[iid]['options']
        assert ans in opts, '%s: keyed answer %r is not an option: %r' % (iid, ans, opts)


def test_item_ids_unique():
    ids = [it['id'] for it in items_for('student')] + [it['id'] for it in items_for('parent')]
    assert len(ids) == len(set(ids)), 'duplicate item ids'


def test_dropped_options_are_gone():
    # services we don't offer must not be orderable, and P28 lost its third option
    assert 'Work mainly with my child, keep me posted' not in PARENT['P28']['options']
    for gone in ('Budget and loan planning', 'Entrance-exam strategy'):
        assert gone not in PARENT['P27']['options'], '%s is still offered' % gone


# --------------------------------------------------------------------------- #
# 2. class gate
# --------------------------------------------------------------------------- #
def test_nine_ncert_questions_per_class():
    for cls, prefix in (('Class 11', 'N11'), ('Class 12', 'N12')):
        shown = [it for it in items_for('student') if _when_met(it, {'S61': cls})]
        quiz = [it for it in shown if it['id'].startswith(('N11', 'N12'))]
        assert len(quiz) == 9, '%s shows %d NCERT items, want 9' % (cls, len(quiz))
        assert all(it['id'].startswith(prefix) for it in quiz), '%s: wrong set' % cls
        for subj in ('PHY', 'CHE', 'MAT'):
            n = sum(1 for it in quiz if it['tag'] == 'NCERT-' + subj)
            assert n == 3, '%s %s: %d questions, want 3' % (cls, subj, n)
        assert all(it['id'] in ANSWER_KEY for it in quiz), '%s: an item has no key' % cls


def test_gate_depends_on_an_earlier_item():
    # _save reads items in bank order, so a gate must resolve before it is checked
    order = {it['id']: n for n, it in enumerate(items_for('student'))}
    for it in items_for('student'):
        for dep in (it.get('when') or {}):
            assert order[dep] < order[it['id']], \
                '%s gates on %s, which is asked later' % (it['id'], dep)


def test_ungated_items_always_shown():
    assert _when_met(STUDENT['S1'], {})
    assert not _when_met(STUDENT['N12P1'], {'S61': 'Class 11'})
    assert not _when_met(STUDENT['N12P1'], {}), 'no class answered -> must not be shown'


def test_class_11_submission_drops_class_12_answers():
    """The gate is enforced server-side: a forged post can't smuggle in the other
    class's answers (which would then be scored against the key)."""
    with app.app_context():
        db.create_all()
        _user('gate@ea.com')
    c = app.test_client()
    _login(c, 'gate@ea.com')
    form = _full_student_form(cls='Class 11')
    form['N12P1'] = '2 Ω'                     # not shown to a class-11 student
    r = c.post('/onboarding-assessment/student', data=form)
    assert r.status_code == 302, r.status_code
    with app.app_context():
        sub = OnboardingResponse.query.filter_by(email='gate@ea.com').first()
        assert sub.responses['S61'] == 'Class 11'
        assert sub.responses.get('N11P1') == '2 s', 'shown answer was dropped'
        assert 'N12P1' not in sub.responses, 'hidden class-12 answer was stored'


# --------------------------------------------------------------------------- #
# 3. account pairing
# --------------------------------------------------------------------------- #
def test_login_required():
    c = app.test_client()
    r = c.get('/onboarding-assessment/student')
    assert r.status_code == 302 and '/login' in r.headers['Location'], \
        'the form must be behind a login — pairing depends on it'


def test_same_account_pairs_both_halves():
    with app.app_context():
        db.create_all()
        _user('family@ea.com')
        _user('other@ea.com')

    c = app.test_client()
    _login(c, 'family@ea.com')
    # the student types their name one way, the parent another — used to break pairing
    c.post('/onboarding-assessment/student', data=_full_student_form(name='Ravi'))
    c.post('/onboarding-assessment/parent', data=_full_parent_form(name='Ravi Kumar'))
    # a different family on the same site must not join them
    c2 = app.test_client()
    _login(c2, 'other@ea.com')
    c2.post('/onboarding-assessment/parent', data=_full_parent_form(name='Ravi'))

    with app.app_context():
        rows = OnboardingResponse.query.filter_by(email='family@ea.com').all()
        assert len(rows) == 2, 'want both halves, got %d' % len(rows)
        keys = {r.family_key for r in rows}
        assert len(keys) == 1, 'halves did not pair despite one account: %r' % keys
        assert {r.role for r in rows} == {'student', 'parent'}

        stranger = OnboardingResponse.query.filter_by(email='other@ea.com').first()
        assert stranger.family_key not in keys, 'a different account joined the family'


def test_ai_bundle_marks_the_quiz():
    from app.routes.onboarding import _ai_bundle
    with app.app_context():
        db.create_all()
        student = OnboardingResponse(
            role='student', family_key='user:99', student_name='Ravi',
            email='b@ea.com',
            responses_json='{"S61": "Class 11", "N11P1": "2 s", "N11C1": "6"}')
        db.session.add(student)
        db.session.commit()
        text = _ai_bundle(student, None)

    assert 'N11P1' in text and '[correct: 2 s | RIGHT]' in text
    assert '[correct: 4 | wrong]' in text, 'a wrong answer must be marked wrong'
    assert 'N12P1' not in text, "the other class's questions must not reach the AI"
    assert 'not answered' in text


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _user(email):
    if not User.query.filter_by(email=email).first():
        db.session.add(User(name='T', email=email, tier='free',
                            password_hash=bcrypt.generate_password_hash('pw').decode()))
        db.session.commit()


def _login(client, email):
    r = client.post('/login', data={'email': email, 'password': 'pw'})
    assert r.status_code in (200, 302), 'login failed'


def _answer(it, form, cls):
    """Fill one item with any valid answer, using the same field names as the form."""
    from app.routes.onboarding import _slug
    iid, t = it['id'], it['type']
    if it.get('when') and not _when_met(it, {'S61': cls}):
        return
    if iid == 'S61':
        form[iid] = cls
    elif t == 'choice':
        form[iid] = it['options'][0]
    elif t == 'likert':
        form[iid] = '4'
    elif t == 'open':
        form[iid] = 'x'
    elif t == 'num':
        for f in it['fields']:
            form['%s__%s' % (iid, _slug(f))] = '70'
    elif t in ('choice_multi', 'likert_multi'):
        for row in it['rows']:
            form['%s__%s' % (iid, _slug(row))] = it['options'][0] if t == 'choice_multi' else '3'
    elif t == 'mostleast':
        form[iid + '__most'] = it['options'][0]
        form[iid + '__least'] = it['options'][1]
    elif t == 'pick':
        for o in it['options'][:it['pick']]:
            form['%s__%s' % (iid, _slug(o))] = '1'
    elif t == 'rank':
        for n, o in enumerate(it['options'], 1):
            form['%s__%s' % (iid, _slug(o))] = str(n)
    elif t == 'choice_pair':
        for g in it['groups']:
            form['%s__%s' % (iid, g['key'])] = g['options'][0]
    elif t == 'sjt':
        if it['options']:
            form[iid + '__choice'] = it['options'][0]
        form[iid + '__why'] = 'because'


def _full_student_form(cls='Class 11', name='Ravi'):
    form = {'student_name': name, 'respondent_name': name, 'phone': '9876543210'}
    for it in items_for('student'):
        _answer(it, form, cls)
    form['N11P1'] = '2 s'      # one known-right answer for the marking check
    form['N11C1'] = '6'        # and one known-wrong
    return form


def _full_parent_form(name='Ravi'):
    form = {'student_name': name, 'respondent_name': 'Parent', 'phone': '9876543210'}
    for it in items_for('parent'):
        _answer(it, form, None)
    return form


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    passed = 0
    for fname, fn in sorted(globals().items()):
        if fname.startswith('test_') and callable(fn):
            fn()
            passed += 1
            print('  ok  %s' % fname)
    print('\n%d checks passed — %d student items (%d shown per class), %d parent items'
          % (passed, len(items_for('student')),
             len([i for i in items_for('student') if _when_met(i, {'S61': 'Class 11'})]),
             len(items_for('parent'))))
    os.unlink(_db)
