"""Content for the public page /nid-papers-analysis: what the NID admission-test papers asked, year by year and topic by topic, and how to practise.
Source of the numbers: app/data/nid/analysis.json, built by tools/nid/build_analysis.py from the structure, marks and topic tags of the NID papers in the supplied folder.
Official format facts come only from NID's own sample papers (2024 and 2025). The papers recalled by candidates are used for structure and themes only; none of their questions are reproduced.
Dates, fees, eligibility and the stages of the current cycle are in the portal's NID admission guide, which follows NID's handbook."""
import json
import os

UPDATED = '3 November 2026'
_HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nid')

OFFICIAL = [
    ('B.Des DAT Prelims sample (2024 and 2025)', '100 marks. An objective part of 25 marks: the 2025 sample has 15 questions of 1 mark and 5 of 2 marks, mostly picture-based (odd one out, puzzles, cubes, logos and signs, colour wheel, general knowledge and science). Then 75 marks of drawing and writing answered in boxes on the paper: ideas with sketches, a poster, user groups for a product, drawing from image fragments, a board-game design.'),
    ('M.Des CDAT Paper 1 sample (2024 and 2025)', 'Multiple choice only in the sample: 20 marks, 16 questions of 1 mark and 2 of 2 marks in 2025 (10 and 5 in 2024). Reasoning-heavy: coding, direction, critical thinking and assumptions, with design literacy on materials, printing, ergonomics, circular design, universal design, colour schemes and design principles. Few questions depend on a picture.'),
    ('What the samples do not print', 'No duration, no negative marking and no answer key appear in the sample files. Check the stages, the weight of Prelims and the marking in the current NID handbook, summarised in our NID admission guide.'),
]

ERAS = [
    ('2015', 'Drawing and writing only', 'All the marks were for subjective tasks: ten drawing and written tasks of 6 to 12 marks and a five-part reasoning set.'),
    ('2016 to 2018', 'A long general-aptitude paper', 'About 60 to 90 multiple-choice questions for 70 marks (marks from 0.5 to 3 a question) and a short creative part of about 30 marks. General knowledge, language passages, science and puzzles dominated.'),
    ('2019 to 2023', 'Shorter objective part, more studio thinking', 'About 20 to 28 multiple-choice questions for 30 to 40 marks, and in some years 70 marks of creative tasks. Spatial and visual reasoning became the biggest block.'),
    ('2024 and 2025 (official samples)', 'A 25-mark objective part and 75 marks of drawing', 'Official samples: 19 or 20 multiple-choice questions for 25 marks, and seven subjective questions for 75 marks.'),
]

THEMES = [
    ('Spatial reasoning is the biggest objective block', 'Cubes and nets, fold-and-punch, mirror images, rotations and top views appear in every era and are the largest single topic in the recent papers.'),
    ('Visual puzzles repeat', 'Odd one out, pattern completion and counting figures (triangles, squares) come back almost every year.'),
    ('Design awareness is steady', 'Logos, road signs and symbols, packaging, colour relationships and the principles of design.'),
    ('General knowledge follows the news and the environment', 'Early papers lean on current affairs and science; the recent ones lean on environment, policy and everyday science.'),
    ('The open tasks reward ideas, not polish', 'Storytelling in frames, drawing from an unusual viewpoint, redesign for a particular user, reuse of an object, and a poster with a line of text recur.'),
]

PRACTICE = [
    ('Spatial and visual reasoning', 'Do a few puzzles daily in sets of 10, and draw the answer before you look. Mirror images, nets and fold-and-punch repay practice quickly.'),
    ('Design literacy', 'Colour wheel relationships, design principles, ergonomics, materials and printing, signs and symbols: a short revision note for each, then sets by section.'),
    ('General knowledge with a design eye', 'Read about crafts, sustainability, famous designers and everyday science; ask how things are made and why they look the way they do.'),
    ('Drawing and ideas', 'Ten minutes of observation sketching daily; one timed idea task a week (three different ideas, labelled); one four-frame story a week.'),
    ('Critical thinking (M.Des)', 'Assumptions, evidence versus opinion, cause versus correlation, and framing a problem: practise with short real-life scenarios.'),
]

FAQ = [
    ('Are these the real NID questions?', 'No. We read the papers to learn their structure and topics. The practice questions in the mock centre are original EduAakashaA questions. The only NID questions in the centre are NID’s own published sample papers, shown as published.'),
    ('How reliable are the papers recalled by candidates?', 'Treat them as a guide to themes, not as exact papers. They are written from memory, and some formats differ between sources. The official sample papers are the best guide to the format.'),
    ('Is there negative marking?', 'The official sample papers print none. Confirm in the current NID handbook before the exam.'),
    ('What is Prelims used for?', 'See the NID admission guide on this site, which follows the handbook: it describes the stages and what the Prelims score is used for.'),
    ('Do the mock tests mark the drawing questions?', 'No. A computer cannot mark a sketch. The Studio section gives original drawing and studio tasks with a rubric to mark yourself and a way to show your mentor.'),
]

TAGS = 'NID DAT past papers analysis, NID B.Des Prelims sample paper, NID M.Des CDAT, NID mock test, NID preparation, spatial reasoning, design aptitude test'


def analysis():
    with open(os.path.join(_HERE, 'analysis.json'), encoding='utf-8') as f:
        return json.load(f)


def samples():
    """Six sample questions for the public page: three visual ones and three text ones (answers appear in the page: they are practice samples)."""
    with open(os.path.join(_HERE, 'bank.json'), encoding='utf-8') as f:
        bank = json.load(f)
    pick = []
    for pre in ('V-MIRRO-02', 'V-FOLD-02', 'V-MATRI-02'):
        pick += [q for q in bank if q['id'] == pre]
    for sec in ('CLR', 'ERG', 'CRT'):
        pick += [q for q in bank if q['sec'] == sec and q['src'] == 'text' and q['marks'] == 1][:1]
    out = []
    for q in pick:
        out.append(dict(id=q['id'], q=q['q'], svg=q.get('svg'), opts=q['opts'], ans=q['ans'], why=q['why']))
    return out


def context():
    ana = analysis()
    return dict(ana=ana, samples=samples())
