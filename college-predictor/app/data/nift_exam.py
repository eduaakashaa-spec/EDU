"""Content for the public page /nift-papers-analysis: what the NIFT GAT and CAT papers asked, how the format changed, and how to practise.

Format facts come from the paper files themselves: the 2024 and 2025 computer-based papers print their section structure, marks, duration and marking; the 2016 and 2017 papers print
section headings; for 2018 to 2023 the number of questions comes from the answer keys. Section and topic mixes are our tagging of the questions that can be read as text
(app/data/nift/analysis.json, built by tools/nift/build_bank.py). Confirm dates, eligibility, fees and the current pattern in the NIFT information bulletin.
"""
import json
import os
import sys

from app.services import nift

UPDATED = '3 November 2026'
_HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nift')

# (year, mode, programme, questions, sections, duration, marking)
FORMAT = [
    ('2025', 'B.Des', '100 marks', 'Communication and English comprehension 32 q (40 marks) · Quantitative 20 · Analytical and logical 15 · GK and current affairs 25', '120 min', '+1, −0.25'),
    ('2025', 'B.F.Tech', '150 marks', 'Part A as B.Des (100) · Part B: quantitative 15, analytical 12 q (15 marks), case study 4 q (20 marks)', '180 min', '+1, −0.25'),
    ('2025', 'M.Des', '120 marks', 'Communication and comprehension 32 q (50 marks) · Quantitative 20 · Analytical 23 q (25 marks) · GK 25', '120 min', '+1, −0.25'),
    ('2025', 'M.F.M', '150 marks', 'Communication and comprehension 34 q (50) · Quantitative 20 · GK 25 · Case study 6 q (30) · Analytical (balance of the marks)', '180 min', '+1, −0.25'),
    ('2025', 'M.F.Tech', '150 marks', 'Communication and comprehension 35 q (45) · Case study 5 q (25) · Quantitative 27 q (30) · Analytical 22 q (25) · GK 25', '180 min', '+1, −0.25'),
    ('2024', 'B.Des', '100 marks', 'Communication and English comprehension 31 q (40 marks) · Quantitative 20 · Analytical and logical 15 · GK and current affairs 25', '120 min', '+1, −0.25'),
    ('2024', 'B.F.Tech', '150 marks', 'Part A as B.Des (100) · Part B: quantitative 15, analytical 15, case study 4 q (20 marks)', '180 min', '+1, −0.25'),
    ('2024', 'M.Des', '120 marks', 'Communication 30 q · English comprehension 5 q (30 marks) · Quantitative 20 · GK 15 · Analytical (balance of the marks)', '120 min', '+1, −0.25'),
    ('2024', 'M.F.M', '150 marks', 'Communication and comprehension 33 q (50) · Case study 8 q (40) · Quantitative 10 · Analytical 25 · GK 25', '180 min', '+1, −0.25'),
    ('2024', 'M.F.Tech', '150 marks', 'Communication and comprehension 35 q (45) · Case study 5 q (25) · Quantitative 30 · Analytical 25 · GK 25', '180 min', '+1, −0.25'),
    ('2023', 'All GAT', '100 / 150 / 120 / 150 / 150 questions', 'B.Des 100 · B.F.Tech 150 · M.Des 120 · M.F.M 150 · M.F.Tech 150 (from the answer keys)', 'not printed', 'negative marking printed'),
    ('2022', 'All GAT', 'same counts as 2023', 'B.Des 100 · B.F.Tech 150 · M.Des 120 · M.F.M 150 · M.F.Tech 150', 'not printed', '1 mark, negative marking'),
    ('2020 and 2021', 'B.Des, B.F.Tech', '100 / 150 questions', 'B.Des 100 questions (2020, 2021) · B.F.Tech 150 (2020)', 'not printed', 'not printed'),
    ('2018', 'B.Des', '100 questions', 'Five sections as in 2016 and 2017', 'not printed', 'not printed'),
    ('2016 and 2017', 'B.Des', '100 questions', 'Quantitative 20 · English communication 25 · English comprehension 25 · Analytical 15 · GK and current affairs 15', 'not printed', 'not printed'),
]

ERAS = [
    ('2016 to 2021', 'Paper-based B.Des GAT of 100 questions', 'Five sections in a fixed pattern: quantitative 20, English communication 25, comprehension 25, analytical 15, GK and current affairs 15. B.F.Tech had 150 questions in 2020.'),
    ('2022 and 2023', 'Five programmes, longer papers', 'GATs for B.Des (100 questions), B.F.Tech (150), M.Des (120), M.F.M (150) and M.F.Tech (150).'),
    ('2024 and 2025', 'Computer-based, with a written case study', 'The papers show 2 or 3 hours, +1 for a right answer and −0.25 for a wrong one. Communication and comprehension carry the largest block of marks (40 to 60). The master’s fashion papers and B.F.Tech Part B add a case study of 4 to 8 questions that carry 20 to 40 marks.'),
]

THEMES = [
    ('English is the biggest block', 'Synonyms and antonyms, idioms, spelling, one-word substitution, fill in the blank and passage questions together carry 40 to 60 marks in every 2024 and 2025 paper. Vocabulary and idioms repay daily practice most.'),
    ('Quantitative questions are school maths', 'Simple interest, percentages, profit and loss, time and work, ratio, averages and speed come back every year. Speed matters more than difficulty: the whole paper allows only about 1.2 minutes a question.'),
    ('Analytical questions repeat patterns', 'Number series, blood relations, seating arrangements, coding and direction questions recur. A pattern learned once is worth marks every year.'),
    ('GK follows the news and the subject', 'Current affairs, awards, sports, books, geography, and fashion, textile and art awareness. Revise the last 12 months of news before the exam.'),
    ('The creative paper rewards ideas and finish', 'Three tasks for 100 marks in 3 hours (as in the 2024 B.Des CAT): design with given shapes, show a transformation in boxes, draw a scene from memory, express a feeling in colour, write about an experience.'),
]

PRACTICE = [
    ('Two sections every day', 'English (15 minutes of vocabulary and idioms) and one of quantitative or analytical (15 questions). Short and daily beats long and weekly.'),
    ('Mock under exam conditions', 'A full GAT mock once a week: 1.2 minutes a question, and no phone. Mark yourself with the report, which splits your time and marks by section.'),
    ('Use the negative marking', 'A wrong answer costs 0.25. Answer when you can rule out two options; leave the rest. The report shows how many marks you lost to wrong answers you were sure of.'),
    ('Let the review do the remembering', 'Every missed or guessed question becomes a review card that returns after 1, 3, 7, 14 and 30 days. Do your Daily Review before new questions.'),
    ('CAT: practise on paper', 'Do one studio task a week in the time given, and show it to your mentor. Look at the four-line rubric: idea, use of the brief, form, finish.'),
]

FAQ = [
    ('Are these the real NIFT questions?', 'The mock centre uses questions from NIFT’s earlier GAT papers (2016 to 2023) that can be shown as text, with the answer from the paper’s key. We kept a question only when an independent solve agreed with the key. The 2024 and 2025 papers were used for format only. The generated maths and reasoning questions are original EduAakashaA practice items.'),
    ('Why are some questions missing from a year’s paper?', 'Questions that need a figure, or whose key we could not confirm, are left out, so a paper shows fewer than 100 questions. The count is shown on each paper.'),
    ('How is marking done?', '+1 for a right answer, −0.25 for a wrong one and 0 for a blank, as the 2024 and 2025 papers print. Confirm the marking in the current NIFT information bulletin.'),
    ('Does the mock test the CAT?', 'No computer can mark a drawing. The studio section restates the tasks of earlier B.Des and M.Des CATs, gives a four-line rubric and lets you mark yourself and show your mentor.'),
    ('What about the situation test?', 'The B.Des selection process also has a hands-on test. This portal does not mark it; read the current NIFT information bulletin for its form and weight.'),
    ('Who can use the mock centre?', 'Premium members. The analysis page and the six sample questions are open to everyone.'),
]

TAGS = 'NIFT GAT past papers, NIFT previous year questions, NIFT mock test, NIFT B.Des, NIFT B.F.Tech, NIFT M.Des, NIFT M.F.M, NIFT CAT'


def analysis():
    return nift.analysis()


def samples():
    """Six free questions: two quantitative, two English, one analytical, one GK (answers show on tap)."""
    pick = []
    for sec, k in (('QA', 2), ('ENG', 2), ('ANA', 1), ('GK', 1)):
        pool = [q for q in nift.bank() if q['sec'] == sec and not q.get('ctx') and len(q['q']) < 220 and all(len(o) < 60 for o in q['opts'])]
        pool.sort(key=lambda q: (-q['src'][0][0], q['id']))
        years = set()
        for q in pool:
            if len(years) < k and q['src'][0][0] not in years and (sec != 'GK' or q['src'][0][0] <= 2022):
                years.add(q['src'][0][0])
                pick.append(q)
    return [dict(sec=nift.SEC[q['sec']], q=q['q'], opts=q['opts'], ans=q['ans'], why=q['why'], src=nift.source_label(q)) for q in pick]


def cat_counts():
    st = nift.studio()
    kinds = {'draw': 'Draw, colour or depict', 'design': 'Design a product or print', 'story': 'Show a sequence or transformation', 'write': 'Write about an experience'}
    out = []
    for k, label in kinds.items():
        out.append((label, sum(1 for t in st if t['kind'] == k)))
    return out, len(st)


def context():
    kinds, n_tasks = cat_counts()
    ana = analysis()
    mix = [m for m in ana['mix'] if m['prog'] == 'B.Des']
    return dict(d=sys.modules[__name__], ana=ana, mix=mix, samples=samples(), kinds=kinds, n_tasks=n_tasks, n_bank=len(nift.bank()), n_years=len(nift.year_papers()), SEC=nift.SEC,
                topics=ana['topics'])
