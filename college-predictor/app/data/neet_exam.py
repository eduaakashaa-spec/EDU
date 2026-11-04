"""Content for the public page /neet-papers-analysis: what the NEET (UG) papers 2018 to 2026 asked, how many questions each year printed, and how to practise.

Question counts come from the National Testing Agency's published answer key for one booklet code per year (180 answers in 2018, 2019, 2020 and 2025; 200 in 2021 to 2024, where each
subject had a Section B with a choice of 10 from 15). The subject and topic mix is our reading of the questions that can be shown as text (app/data/neet/analysis.json, built by
tools/neet/build_bank.py). Confirm dates, eligibility, fees and the current pattern in the NEET (UG) information bulletin.
"""
import sys

from app.services import neet

UPDATED = '4 November 2026'

ERAS = [
    ('2018 to 2020', '180 questions, 45 a subject', 'Physics, Chemistry, Botany and Zoology with 45 compulsory questions each; +4 for a right answer, −1 for a wrong one.'),
    ('2021 to 2024', '200 questions, 180 to attempt', 'Each subject has Section A (35 compulsory) and Section B (15, attempt any 10). Marks are for the 180 questions attempted, 720 in all.'),
    ('2025', 'Back to 180 questions', 'The 2025 paper printed 180 questions, 45 a subject, with no choice. The marking stayed +4 and −1.'),
]

THEMES = [
    ('Biology is half the paper', 'Botany and Zoology together are 90 of the 180 marks-bearing questions in every year. Most are direct NCERT questions: facts, definitions, match-the-list and statement questions.'),
    ('Physics rewards formulas and speed', 'Mechanics, electricity and magnetism, optics, modern physics and electronics supply most questions. Many are one-step numerical problems: know the formula and the units.'),
    ('Chemistry splits three ways', 'Physical (mole concept, equilibrium, thermodynamics, kinetics, electrochemistry), inorganic (periodic table, bonding, coordination compounds, p- and d-block) and organic (named reactions, reaction mechanisms, biomolecules).'),
    ('Match, statement and assertion-reason', 'Many questions give two lists to match, two statements to judge, or an assertion and a reason. Read each statement separately before choosing.'),
    ('Wrong answers cost marks', 'A wrong answer takes away 1 mark and a right one earns 4. Answer when you can remove at least two options; leave the rest blank.'),
]

PRACTICE = [
    ('Biology every day', 'Read one NCERT chapter and do 30 questions from the same chapter the same day. Biology repays daily repetition more than any other subject.'),
    ('Full mock once a week', 'A 180-question mock in 180 minutes, no phone. The report splits marks and time by subject and shows the topics that cost you marks.'),
    ('Use the negative marking', 'Each wrong answer costs 1. The report shows how many marks you lost to wrong answers you were sure of: those are the gaps to close first.'),
    ('Let the review do the remembering', 'Every missed or guessed question becomes a review card that returns after 1, 3, 7, 14 and 30 days. Do your Daily Review before new questions.'),
    ('Earlier papers, topic by topic', 'Questions repeat in idea if not in words. After each chapter, solve that chapter’s questions from the 2018 to 2026 papers.'),
]

FAQ = [
    ('Are these the real NEET questions?', 'The mock centre uses questions from the NEET (UG) papers 2018 to 2026 that can be shown as text, with the answer from the National Testing Agency’s answer key for the booklet code we transcribed. We kept a question only when an independent solve agreed with the key.'),
    ('Why are some questions missing from a year’s paper?', 'Questions that need a figure, graph or drawn structure, and questions the key does not settle (dropped, or two options accepted), are left out. The count is shown on each paper.'),
    ('Why is only one booklet code used for each year?', 'NEET prints each paper in several booklet codes with the same questions in a different order. One code per year covers the whole paper.'),
    ('How is marking done?', '+4 for a right answer, −1 for a wrong one and 0 for a blank. Confirm the marking in the current NEET (UG) information bulletin.'),
    ('Is the 2026 answer key final?', 'No. For the 3 May 2026 paper (booklet code 13) we only had the National Testing Agency’s provisional answer key. A 2026 question is kept only when an independent solve agrees with that key, but the final key can differ where candidates challenged a question. Tell your mentor if you doubt one.'),
    ('Who can use the mock centre?', 'Premium members. The analysis page and the six sample questions are open to everyone, and the free sample mock tests need only a phone number and email.'),
]

TAGS = 'NEET past papers, NEET previous year questions, NEET mock test, NEET 2025 paper, NEET physics chemistry biology questions'


def analysis():
    return neet.analysis()


def samples():
    """Six free questions: two physics, two chemistry, one botany, one zoology (answers show on tap)."""
    pick = []
    for sec, k in (('PHY', 2), ('CHEM', 2), ('BOT', 1), ('ZOO', 1)):
        pool = [q for q in neet.bank() if q['sec'] == sec and len(q['q']) < 230 and all(len(o) < 60 for o in q['opts'])]
        pool.sort(key=lambda q: (-q['src'][0][0], q['id']))
        years = set()
        for q in pool:
            if len(years) < k and q['src'][0][0] not in years:
                years.add(q['src'][0][0])
                pick.append(q)
    return [dict(sec=neet.SEC[q['sec']], q=q['q'], opts=q['opts'], ans=q['ans'], why=q['why'], src=neet.source_label(q)) for q in pick]


def context():
    ana = analysis()
    years = sorted(ana['years'].items(), reverse=True)
    return dict(d=sys.modules[__name__], ana=ana, years=years, samples=samples(), n_bank=len(neet.bank()), n_years=len(neet.year_papers()), SEC=neet.SEC, topics=ana['topics'])
