"""EduPulse-UCEED — question selection, scoring, progress statistics and e-mail reports.

Important: the starter bank below is ORIGINAL practice material written by EduAakashaA (text-only, one question each on
core reasoning/awareness skills). It is NOT a set of UCEED previous-year questions. Real papers are copyrighted —
only add them through the admin import if you hold the rights, and label them with their source and year.
"""
import csv
import io
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import func

from app.extensions import db
from app.models import User
from app.models_pulse import (PulseAnswer, PulseAttempt, PulseChapter, PulseProfile, PulseQuestion, PulseReport)
from app.services import mailer
from app.services.email_templates import SITE, branded_shell

NEG_MARK = 1 / 3          # practice scoring only: +1 correct, −1/3 wrong. Not the official UCEED marking scheme.
SET_SIZES = (5, 10, 15, 20)
SEC_PER_Q = 90            # timed mode: 90 seconds per question
WEAK_BELOW, STRONG_FROM, MIN_ANSWERED = 60, 80, 5

CHAPTERS = [
    ('perception', 'Visual perception & observation', 'Symmetry, counting figures, mirror images and the way we see.'),
    ('spatial', 'Spatial reasoning & visualisation', '3-D thinking: cubes, folding, faces and edges.'),
    ('patterns', 'Patterns, shapes & transformations', 'Series, rotations, reflections and shape counting.'),
    ('logic', 'Logical & analytical reasoning', 'Deduction, ordering, coding and relationships.'),
    ('awareness', 'Everyday design awareness', 'Design history, colour, type and usability ideas.'),
    ('problem', 'Problem-solving & lateral thinking', 'Puzzles that reward a different angle.'),
    ('materials', 'Materials, objects & functionality', 'How things are made and why they work.'),
    ('interpret', 'Interpreting visual information & creativity', 'Charts, scales, plans and the design process.'),
]

# (chapter, stem, [A, B, C, D], correct, explanation, difficulty)
STARTER = [
    ('perception', 'Which regular shape has the greatest number of lines of symmetry?', ['Square', 'Regular pentagon', 'Regular hexagon', 'Equilateral triangle'], 'C', 'A regular n-sided polygon has n lines of symmetry: hexagon 6, pentagon 5, square 4, triangle 3.', 'Easy'),
    ('perception', 'Three straight lines are drawn from vertex A of triangle ABC to points on the opposite side BC, dividing BC into 4 segments. How many triangles are there in the figure?', ['4', '6', '8', '10'], 'D', 'Every triangle uses A and two of the 5 points on BC. Choosing 2 of 5 points gives 10 triangles.', 'Medium'),
    ('perception', 'In a mirror, a wall clock appears to show 3:00. What is the actual time?', ['3:00', '6:00', '9:00', '12:00'], 'C', 'A mirror reverses left and right, so the hands at 3 appear where 9 would be: the real time is 9:00.', 'Easy'),
    ('perception', 'On the traditional red–yellow–blue colour wheel, which colour is complementary to blue?', ['Green', 'Orange', 'Purple', 'Red'], 'B', 'Complementary colours sit opposite each other. Opposite blue is orange (red + yellow).', 'Easy'),
    ('perception', 'The Gestalt principle that makes us see objects placed close together as a group is called', ['Similarity', 'Closure', 'Proximity', 'Continuity'], 'C', 'Proximity: elements near each other are perceived as belonging together.', 'Easy'),

    ('spatial', 'A cube painted red on all faces is cut into 64 equal small cubes (4 × 4 × 4). How many small cubes have exactly one face painted?', ['8', '16', '24', '32'], 'C', 'Each face has (4 − 2)² = 4 such cubes; 4 × 6 faces = 24.', 'Medium'),
    ('spatial', 'On a standard die, opposite faces add up to 7. If 1 is on top, what number is on the bottom?', ['3', '4', '5', '6'], 'D', 'The face opposite 1 is 7 − 1 = 6.', 'Easy'),
    ('spatial', 'A square paper is folded in half vertically and then in half horizontally, giving a small square in which one corner is the original centre of the paper. A single hole is punched exactly at that corner. How many holes appear after unfolding completely?', ['1', '2', '4', '8'], 'A', 'All four layers meet at the original centre, so the hole goes through the one centre point only.', 'Hard'),
    ('spatial', 'How many edges does a triangular prism have?', ['6', '8', '9', '12'], 'C', 'Two triangular faces contribute 3 + 3 edges and three vertical edges join them: 9.', 'Easy'),
    ('spatial', 'A cuboid measures 4 cm × 3 cm × 2 cm. How many of its faces have an area of 12 cm²?', ['1', '2', '4', '6'], 'B', 'The 4 × 3 faces have area 12 cm², and there are two of them (top and bottom).', 'Medium'),

    ('patterns', 'Find the next number: 2, 6, 12, 20, 30, ?', ['36', '40', '42', '48'], 'C', 'The terms are n(n + 1): 1·2, 2·3, 3·4, 4·5, 5·6, so the next is 6·7 = 42.', 'Medium'),
    ('patterns', 'Find the next letter: A, C, F, J, O, ?', ['S', 'T', 'U', 'V'], 'C', 'The jumps are +2, +3, +4, +5, +6. O is the 15th letter; 15 + 6 = 21, which is U.', 'Medium'),
    ('patterns', 'An arrow points north. It turns 90° clockwise and then 180° anticlockwise. Which way does it point now?', ['North', 'South', 'East', 'West'], 'D', 'North → East after 90° clockwise. Turning 180° anticlockwise from East points it West.', 'Easy'),
    ('patterns', 'The letter b is flipped left-to-right, as if reflected in a mirror held beside it. What does it look like?', ['p', 'q', 'd', 'b'], 'C', 'A left–right reflection of b gives d (a vertical flip would give p).', 'Easy'),
    ('patterns', 'How many squares of all sizes are there in a 3 × 3 grid of unit squares?', ['9', '12', '14', '16'], 'C', '9 (1×1) + 4 (2×2) + 1 (3×3) = 14.', 'Medium'),

    ('logic', 'All prototypes are models. No model is final. Which conclusion must be true?', ['Some prototypes are final', 'No prototype is final', 'All models are prototypes', 'Some models are prototypes only'], 'B', 'Every prototype is a model, and no model is final, so no prototype is final.', 'Easy'),
    ('logic', 'A is taller than B, B is taller than C, and D is shorter than C. Who is the shortest?', ['A', 'B', 'C', 'D'], 'D', 'Order from tallest: A > B > C > D.', 'Easy'),
    ('logic', 'If COLOUR is coded as DPMPVS (each letter moved one step forward), how is SKETCH coded?', ['TLFUDI', 'TKFUDI', 'TLGUDI', 'SLFUDI'], 'A', 'Move every letter one step forward: S→T, K→L, E→F, T→U, C→D, H→I.', 'Medium'),
    ('logic', 'Pointing to a photograph, Mira says, "He is the son of my mother\'s only brother." The man in the photograph is Mira\'s', ['Brother', 'Uncle', 'Cousin', 'Nephew'], 'C', 'Her mother\'s brother is her maternal uncle; his son is her cousin.', 'Medium'),
    ('logic', 'What is the smaller angle between the hands of a clock at 3:15?', ['0°', '7.5°', '15°', '22.5°'], 'B', 'Minute hand: 15 × 6° = 90°. Hour hand: 3 × 30° + 15 × 0.5° = 97.5°. Difference = 7.5°.', 'Hard'),

    ('awareness', 'The Bauhaus school of design was founded in 1919 by', ['Le Corbusier', 'Walter Gropius', 'Charles Eames', 'Dieter Rams'], 'B', 'Walter Gropius founded the Staatliches Bauhaus in Weimar in 1919.', 'Medium'),
    ('awareness', 'The phrase "form follows function" is most closely associated with the architect', ['Louis Sullivan', 'Philippe Starck', 'Jony Ive', 'Raymond Loewy'], 'A', 'Louis Sullivan wrote that form ever follows function, a guiding idea of modern design.', 'Medium'),
    ('awareness', 'Colour printing mainly uses which set of subtractive primaries (plus black)?', ['Red, green, blue', 'Cyan, magenta, yellow', 'Red, yellow, blue', 'Orange, green, violet'], 'B', 'CMYK printing uses cyan, magenta and yellow inks, with black (K) added for depth.', 'Easy'),
    ('awareness', 'Which of these is a serif typeface?', ['Arial', 'Helvetica', 'Times New Roman', 'Verdana'], 'C', 'Times New Roman has serifs — small strokes at the ends of letters. The others are sans-serif.', 'Easy'),
    ('awareness', 'In design, the term "affordance" refers to', ['The manufacturing cost of a product', 'Cues that suggest how an object can be used', 'The colour palette of a product', 'The packaging of a product'], 'B', 'An affordance is a perceived possibility for action — a handle suggests pulling, a button suggests pressing.', 'Medium'),

    ('problem', 'You have an empty 3-litre jug and an empty 5-litre jug and an unlimited water supply. What is the minimum number of operations (fill, empty or pour) needed to get exactly 4 litres in the 5-litre jug?', ['4', '5', '6', '8'], 'C', 'Fill 5; pour into 3 (2 left); empty 3; pour the 2 into 3; fill 5; pour into 3 until full (1 needed) leaving 4. That is 6 operations.', 'Hard'),
    ('problem', 'A rope is cut into 3 equal parts and then each part is cut into 4 equal pieces. How many cuts are made in all?', ['9', '10', '11', '12'], 'C', '2 cuts make 3 parts; each part needs 3 more cuts (3 × 3 = 9). Total 11.', 'Medium'),
    ('problem', 'A farmer has 17 sheep and all but 9 die. How many sheep are left?', ['8', '9', '17', '0'], 'B', '"All but 9" means 9 survive.', 'Easy'),
    ('problem', 'Which is the odd one out?', ['Pencil', 'Pen', 'Brush', 'Eraser'], 'D', 'The pencil, pen and brush all make marks; the eraser removes them.', 'Easy'),
    ('problem', 'A bat and a ball cost ₹110 together. The bat costs ₹100 more than the ball. How much does the ball cost?', ['₹10', '₹5', '₹15', '₹20'], 'B', 'Ball = x, bat = x + 100, so 2x + 100 = 110 and x = ₹5.', 'Medium'),

    ('materials', 'Which of these materials is a thermoplastic that can be softened by heating again and again?', ['Bakelite', 'Polyethylene', 'Cured epoxy resin', 'Vulcanised rubber'], 'B', 'Polyethylene is a thermoplastic. Bakelite, cured epoxy and vulcanised rubber are set permanently.', 'Medium'),
    ('materials', 'In a first-class lever (like a seesaw), the fulcrum is placed', ['At the load end', 'Between the effort and the load', 'At the effort end', 'Beyond the load'], 'B', 'First-class levers have the fulcrum between the effort and the load.', 'Easy'),
    ('materials', 'Which of these is the best thermal insulator?', ['Copper', 'Aluminium', 'Glass wool', 'Steel'], 'C', 'Glass wool traps air and conducts heat poorly; the metals are good conductors.', 'Easy'),
    ('materials', 'A screw is an application of which simple machine?', ['Pulley', 'Lever', 'An inclined plane wound around a cylinder', 'Wheel and axle'], 'C', 'A screw thread is an inclined plane wrapped around a cylinder.', 'Medium'),
    ('materials', 'Why are bicycle handle grips usually made of rubber?', ['To make the handle heavier', 'To increase friction and cushioning', 'To conduct heat away', 'To save steel'], 'B', 'Rubber grips the hand and absorbs vibration.', 'Easy'),

    ('interpret', 'In a pictogram, one icon stands for 20 visitors. Monday shows 3.5 icons. How many visitors came on Monday?', ['60', '65', '70', '75'], 'C', '3.5 × 20 = 70.', 'Easy'),
    ('interpret', 'A bar chart shows sales of 40 (Jan), 55 (Feb), 45 (Mar) and 70 (Apr). In which month was the increase over the previous month the largest?', ['February', 'March', 'April', 'January'], 'C', 'Feb +15, Mar −10, Apr +25. April has the largest increase.', 'Medium'),
    ('interpret', 'On a map, 1 cm represents 5 km. Two towns are 7.2 cm apart on the map. What is the actual distance?', ['30 km', '32 km', '36 km', '40 km'], 'C', '7.2 × 5 = 36 km.', 'Easy'),
    ('interpret', 'A floor plan is drawn at a scale of 1 : 50. A wall that is 4 m long is drawn how long on the plan?', ['4 cm', '8 cm', '20 cm', '80 cm'], 'B', '4 m = 400 cm; 400 ÷ 50 = 8 cm.', 'Medium'),
    ('interpret', 'In the design-thinking process, the "Empathise" stage is mainly about', ['Producing final drawings', 'Understanding the needs, feelings and context of users', 'Choosing materials', 'Testing a finished prototype'], 'B', 'Empathise means learning about the people you are designing for before defining the problem.', 'Easy'),
]

CSV_COLUMNS = ['chapter', 'stem', 'option_a', 'option_b', 'option_c', 'option_d', 'correct', 'explanation', 'difficulty', 'source', 'year']


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def ensure_chapters():
    have = {c.key for c in PulseChapter.query.all()}
    for i, (key, title, desc) in enumerate(CHAPTERS, 1):
        if key not in have:
            db.session.add(PulseChapter(key=key, title=title, description=desc, position=i))
    db.session.commit()


def seed_starter():
    """Idempotent by question text. Returns the number added (published immediately; they are original practice items)."""
    ensure_chapters()
    chapters = {c.key: c for c in PulseChapter.query.all()}
    have = {q.stem for q in PulseQuestion.query.all()}
    added = 0
    for key, stem, opts, correct, expl, diff in STARTER:
        if stem in have:
            continue
        db.session.add(PulseQuestion(chapter_id=chapters[key].id, stem=stem, option_a=opts[0], option_b=opts[1], option_c=opts[2],
                                     option_d=opts[3], correct=correct, explanation=expl, difficulty=diff, status='published'))
        added += 1
    db.session.commit()
    return added


def import_csv(text):
    """Validate every row first; import nothing if any row is bad. Returns (added, errors)."""
    ensure_chapters()
    chapters = {c.key: c for c in PulseChapter.query.all()}
    chapters.update({c.title.lower(): c for c in chapters.values()})
    rows, errors = [], []
    reader = csv.DictReader(io.StringIO(text.lstrip('﻿')))
    missing = [c for c in CSV_COLUMNS[:7] if c not in (reader.fieldnames or [])]
    if missing:
        return 0, [f'Missing column(s): {", ".join(missing)}']
    for n, r in enumerate(reader, start=2):
        ch = chapters.get((r.get('chapter') or '').strip().lower())
        corr = (r.get('correct') or '').strip().upper()
        if not ch:
            errors.append(f'Row {n}: unknown chapter “{r.get("chapter")}”')
        elif corr not in ('A', 'B', 'C', 'D'):
            errors.append(f'Row {n}: correct must be A, B, C or D')
        elif not (r.get('stem') or '').strip() or not all((r.get(k) or '').strip() for k in ('option_a', 'option_b', 'option_c', 'option_d')):
            errors.append(f'Row {n}: the question and all four options are required')
        else:
            diff = (r.get('difficulty') or 'Medium').strip().title()
            rows.append(PulseQuestion(chapter_id=ch.id, stem=r['stem'].strip(), option_a=r['option_a'].strip()[:400], option_b=r['option_b'].strip()[:400],
                                      option_c=r['option_c'].strip()[:400], option_d=r['option_d'].strip()[:400], correct=corr,
                                      explanation=(r.get('explanation') or '').strip(), difficulty=diff if diff in ('Easy', 'Medium', 'Hard') else 'Medium',
                                      source=((r.get('source') or '').strip() or 'Imported')[:160], year=(r.get('year') or '').strip()[:8] or None,
                                      status='draft'))
    if errors:
        return 0, errors[:20]
    db.session.add_all(rows)
    db.session.commit()
    return len(rows), []


def export_csv():
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(CSV_COLUMNS)
    for q in PulseQuestion.query.order_by(PulseQuestion.chapter_id, PulseQuestion.id).all():
        w.writerow([q.chapter.key, q.stem, q.option_a, q.option_b, q.option_c, q.option_d, q.correct, q.explanation or '', q.difficulty, q.source or '', q.year or ''])
    return out.getvalue()


# --------------------------------------------------------------------------- #
# attempts
# --------------------------------------------------------------------------- #
def pick_questions(user_id, chapter, n, difficulty=None):
    """Prefer questions the student has not seen, then ones they got wrong, then the rest — random within each group."""
    q = PulseQuestion.query.filter_by(status='published')
    if chapter is not None:
        q = q.filter(PulseQuestion.chapter_id == chapter.id)
    if difficulty in ('Easy', 'Medium', 'Hard'):
        q = q.filter(PulseQuestion.difficulty == difficulty)
    pool = q.all()
    seen, wrong = {}, set()
    for qid, chosen, ok in (db.session.query(PulseAnswer.question_id, PulseAnswer.chosen, PulseAnswer.is_correct)
                            .join(PulseAttempt, PulseAttempt.id == PulseAnswer.attempt_id)
                            .filter(PulseAttempt.user_id == user_id, PulseAttempt.submitted_at != None)):  # noqa: E711
        seen[qid] = True
        if chosen and not ok:
            wrong.add(qid)
    groups = ([x for x in pool if x.id not in seen], [x for x in pool if x.id in wrong], [x for x in pool if x.id in seen and x.id not in wrong])
    chosen_q = []
    for g in groups:
        random.shuffle(g)
        chosen_q += g
    return chosen_q[:n]


def start_attempt(user, chapter, n, mode='practice', difficulty=None):
    qs = pick_questions(user.id, chapter, n, difficulty)
    if not qs:
        return None
    att = PulseAttempt(user_id=user.id, chapter_id=chapter.id if chapter else None, mode=mode, total=len(qs),
                       limit_sec=len(qs) * SEC_PER_Q if mode == 'timed' else None)
    db.session.add(att)
    db.session.flush()
    for i, qq in enumerate(qs, 1):
        db.session.add(PulseAnswer(attempt_id=att.id, question_id=qq.id, position=i))
    db.session.commit()
    return att


def submit_attempt(att, form):
    """Record answers once. `form` maps 'q<answer_id>' -> 'A'..'D'. Returns the attempt."""
    if att.submitted_at:
        return att
    correct = wrong = skipped = 0
    for a in att.answers.all():
        v = (form.get(f'q{a.id}') or '').strip().upper()
        if v in ('A', 'B', 'C', 'D'):
            a.chosen = v
            a.is_correct = (v == a.question.correct)
            correct += a.is_correct
            wrong += not a.is_correct
        else:
            a.chosen, a.is_correct = None, False
            skipped += 1
    att.correct, att.wrong, att.skipped = correct, wrong, skipped
    att.submitted_at = utcnow()
    att.duration_sec = max(1, int((att.submitted_at - att.started_at).total_seconds()))
    db.session.commit()
    return att


def practice_score(att):
    """EduAakashaA practice scoring (+1 / −1/3). Informational, not the official UCEED marking."""
    return round((att.correct or 0) - (att.wrong or 0) * NEG_MARK, 2)


# --------------------------------------------------------------------------- #
# statistics
# --------------------------------------------------------------------------- #
def chapter_stats(user_id, since=None):
    q = (db.session.query(PulseQuestion.chapter_id, func.count(PulseAnswer.id),
                          func.sum(db.case((PulseAnswer.is_correct == True, 1), else_=0)),  # noqa: E712
                          func.count(func.distinct(PulseAnswer.question_id)))
         .join(PulseAnswer, PulseAnswer.question_id == PulseQuestion.id)
         .join(PulseAttempt, PulseAttempt.id == PulseAnswer.attempt_id)
         .filter(PulseAttempt.user_id == user_id, PulseAttempt.submitted_at != None, PulseAnswer.chosen != None))  # noqa: E711
    if since:
        q = q.filter(PulseAttempt.submitted_at >= since)
    got = {cid: (n, int(c or 0), d) for cid, n, c, d in q.group_by(PulseQuestion.chapter_id)}
    rows = []
    for ch in PulseChapter.query.filter_by(active=True).order_by(PulseChapter.position).all():
        total = ch.questions.filter_by(status='published').count()
        n, c, d = got.get(ch.id, (0, 0, 0))
        acc = round(100 * c / n) if n else None
        level = 'new' if n < MIN_ANSWERED else ('weak' if acc < WEAK_BELOW else ('strong' if acc >= STRONG_FROM else 'ok'))
        rows.append({'chapter': ch, 'total': total, 'answered': n, 'correct': c, 'seen': d, 'accuracy': acc, 'coverage': round(100 * d / total) if total else 0, 'level': level})
    return rows


def overall(user_id, since=None, until=None):
    q = PulseAttempt.query.filter(PulseAttempt.user_id == user_id, PulseAttempt.submitted_at != None)  # noqa: E711
    if since:
        q = q.filter(PulseAttempt.submitted_at >= since)
    if until:
        q = q.filter(PulseAttempt.submitted_at < until)
    atts = q.order_by(PulseAttempt.submitted_at).all()
    answered = sum(a.answered for a in atts)
    correct = sum(a.correct or 0 for a in atts)
    secs = sum(a.duration_sec or 0 for a in atts)
    return {'attempts': len(atts), 'answered': answered, 'correct': correct, 'skipped': sum(a.skipped or 0 for a in atts),
            'accuracy': round(100 * correct / answered) if answered else None,
            'sec_per_q': round(secs / sum(a.total for a in atts)) if atts and sum(a.total for a in atts) else None,
            'trend': [a.accuracy for a in atts if a.accuracy is not None][-12:], 'last': atts[-1].submitted_at if atts else None, 'list': atts}


def streak(user_id):
    days = {d.date() for (d,) in db.session.query(PulseAttempt.submitted_at).filter(PulseAttempt.user_id == user_id, PulseAttempt.submitted_at != None)}  # noqa: E711
    n, d = 0, utcnow().date()
    if d not in days:
        d -= timedelta(days=1)
    while d in days:
        n += 1
        d -= timedelta(days=1)
    return n


def advice(rows, ov):
    """Plain-language next steps from the numbers (guidance, not a prediction)."""
    out = []
    weak = [r for r in rows if r['level'] == 'weak']
    new = [r for r in rows if r['answered'] == 0 and r['total']]
    if weak:
        w = min(weak, key=lambda r: r['accuracy'])
        out.append(f"Revisit “{w['chapter'].title}” — accuracy is {w['accuracy']}% over {w['answered']} questions.")
    if new:
        out.append(f"Try “{new[0]['chapter'].title}” — you have not attempted it yet.")
    if ov['attempts'] and ov['accuracy'] is not None and ov['accuracy'] >= STRONG_FROM and not weak:
        out.append('Accuracy is strong — raise the difficulty or try a timed set.')
    if not ov['attempts']:
        out.append('Start with a 10-question mixed set to see where you stand.')
    return out


# --------------------------------------------------------------------------- #
# e-mail
# --------------------------------------------------------------------------- #
def _esc(s):
    from markupsafe import escape
    return str(escape(s))


def _wrap(title, intro, rows_html, cta_label='Open EduPulse', note=''):
    body = (f'<h2 style="margin:0 0 8px;color:#0E3A8A;font-family:Georgia,serif">{_esc(title)}</h2>'
            f'<p style="font-size:15px;line-height:1.55">{intro}</p>{rows_html}'
            f'<p><a href="{SITE}/edupulse-uceed/" style="background:#FF6B0A;color:#fff;text-decoration:none;padding:10px 18px;border-radius:999px;font-weight:700">{cta_label}</a></p>'
            f'<p style="font-size:12px;color:#5A6278">{note} EduPulse practice scores are for guidance only and are not official UCEED marks. '
            'To change or stop these emails, open EduPulse → Settings, or write to info@eduaakashaa.com.</p>')
    return branded_shell(body)


def _table(pairs):
    return ('<table style="border-collapse:collapse;width:100%;font-size:14px;margin:10px 0">' + ''.join(
        f'<tr><td style="padding:7px 10px;border-bottom:1px solid #E8DFC8;color:#5A6278">{_esc(a)}</td>'
        f'<td style="padding:7px 10px;border-bottom:1px solid #E8DFC8;text-align:right"><strong>{_esc(b)}</strong></td></tr>' for a, b in pairs) + '</table>')


def send_result_email(att):
    """Result of one practice set → the student (if they opted in)."""
    prof = db.session.get(PulseProfile, att.user_id)
    user = db.session.get(User, att.user_id)
    if not (prof and prof.email_results and user and user.email) or not mailer.is_configured():
        return False
    ch = att.chapter.title if att.chapter else 'Mixed chapters'
    pairs = [('Set', ch), ('Correct', f'{att.correct} of {att.total}'), ('Wrong', str(att.wrong)), ('Skipped', str(att.skipped)),
             ('Accuracy (answered)', f'{att.accuracy}%' if att.accuracy is not None else '—'), ('Practice score', f'{practice_score(att)}')]
    html = _wrap(f'Your EduPulse result — {ch}', f'Hi {_esc((user.name or "").split(" ")[0])}, here is how your practice set went.', _table(pairs),
                 'Review the answers')
    text = f'EduPulse result — {ch}\nCorrect {att.correct}/{att.total}, wrong {att.wrong}, skipped {att.skipped}. Review: {SITE}/edupulse-uceed/attempt/{att.id}/result'
    mailer.send_async(user.email, f'EduPulse result: {att.correct}/{att.total} in {ch}', text, html, from_addr=mailer.INFO_FROM, reply_to=mailer.INFO_FROM)
    return True


def digest_data(user_id, days):
    end = utcnow()
    start = end - timedelta(days=days)
    prev_start = start - timedelta(days=days)
    return {'start': start, 'end': end, 'cur': overall(user_id, start), 'prev': overall(user_id, prev_start, start),
            'rows': chapter_stats(user_id, start), 'all_rows': chapter_stats(user_id), 'streak': streak(user_id)}


def _digest_html(name, role, d, days):
    cur, prev = d['cur'], d['prev']
    delta = ''
    if cur['accuracy'] is not None and prev['accuracy'] is not None:
        diff = cur['accuracy'] - prev['accuracy']
        delta = f' ({"+" if diff >= 0 else ""}{diff} points vs the previous {days} days)'
    pairs = [('Practice sets completed', str(cur['attempts'])), ('Questions answered', str(cur['answered'])),
             ('Accuracy', (f"{cur['accuracy']}%" if cur['accuracy'] is not None else '—') + delta), ('Practice streak', f"{d['streak']} day(s)")]
    weak = [r for r in d['all_rows'] if r['level'] == 'weak']
    strong = [r for r in d['all_rows'] if r['level'] == 'strong']
    lines = ''
    if strong:
        lines += '<p style="font-size:14px"><strong>Going well:</strong> ' + ', '.join(_esc(r['chapter'].title) for r in strong[:3]) + '</p>'
    if weak:
        lines += '<p style="font-size:14px"><strong>Needs attention:</strong> ' + ', '.join(f"{_esc(r['chapter'].title)} ({r['accuracy']}%)" for r in weak[:3]) + '</p>'
    tips = advice(d['all_rows'], overall_all(d))
    if tips:
        lines += '<ul style="font-size:14px;padding-left:18px">' + ''.join(f'<li>{_esc(t)}</li>' for t in tips[:3]) + '</ul>'
    if not cur['attempts']:
        lines = '<p style="font-size:14px">No practice sets were completed in this period. A short daily set keeps skills fresh.</p>' + lines
    who = {'student': f'Hi {_esc(name.split(" ")[0])}, here is your UCEED practice progress for the last {days} days.',
           'parent': f'Here is a summary of {_esc(name)}’s UCEED practice progress over the last {days} days. You are receiving this because the student shared it with you.',
           'mentor': f'Progress summary for your mentee {_esc(name)} over the last {days} days.'}[role]
    return _wrap(f'EduPulse-UCEED progress — {name}', who, _table(pairs) + lines, 'View progress' if role != 'parent' else 'About EduPulse')


def overall_all(d):
    return {'attempts': d['cur']['attempts'], 'accuracy': d['cur']['accuracy']}


def send_digest(prof, days=None, force=False):
    """E-mail the progress digest to the student, the parent (with consent) and the linked mentor. Returns recipients."""
    user = db.session.get(User, prof.user_id)
    if not user or not mailer.is_configured():
        return []
    days = days or (30 if prof.frequency == 'monthly' else 7)
    d = digest_data(prof.user_id, days)
    sent = []

    def go(to, role):
        if to:
            mailer.send_async(to, f'EduPulse-UCEED progress — {user.name}', f'EduPulse-UCEED progress for {user.name}. Open: {SITE}/edupulse-uceed/',
                              _digest_html(user.name or 'Student', role, d, days), from_addr=mailer.INFO_FROM, reply_to=mailer.INFO_FROM)
            sent.append(to)
    go(user.email, 'student')
    if prof.parent_consent and prof.parent_email:
        go(prof.parent_email, 'parent')
    if prof.mentor and prof.mentor.email:
        go(prof.mentor.email, 'mentor')
    db.session.add(PulseReport(user_id=prof.user_id, period_start=d['start'], period_end=d['end'], sent_to=', '.join(sent)[:500]))
    prof.last_report_at = d['end']
    db.session.commit()
    return sent


def due_profiles(now=None):
    now = now or utcnow()
    out = []
    for p in PulseProfile.query.filter(PulseProfile.frequency != 'off').all():
        gap = timedelta(days=30 if p.frequency == 'monthly' else 7)
        if (p.last_report_at is None and (now - (p.created_at or now)) >= gap) or (p.last_report_at and now - p.last_report_at >= gap):
            out.append(p)
    return out


def send_due_reports(now=None):
    """Send digests that are due. Safe to call repeatedly (a profile is only mailed once per period)."""
    n = 0
    for p in due_profiles(now):
        if send_digest(p):
            n += 1
    return n
