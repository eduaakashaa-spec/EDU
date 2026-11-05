"""Content for the public page /olympiad-exam-guide: the Indian Olympiads in mathematics and science (stages, dates, eligibility, formats, selection, syllabus, preparation).

Every fact was read from an official page (HBCSE, the Mathematical Association of India / IOQM site, IAPT, imo-official.org) on the date in CHECKED; SOURCES lists them. Where the pages did not settle
something (see NOT_CONFIRMED) the page says so. Past cut-offs are deliberately not shown: they are computed every year.
"""
import sys
from datetime import date

from app.services import olympiad

CHECKED = '5 November 2026'
UPDATED = CHECKED

# (label, start date, end date or None, note, source key)
TIMELINE = [
    ('IOQM 2026 (maths, stage 1)', date(2026, 9, 6), None, 'Held offline on an OMR sheet; no negative marking. Scores were released on 7 October 2026.', 'ioqm'),
    ('NSE student enrolment (science, stage 1)', date(2026, 8, 21), date(2026, 9, 16), 'Closed. Enrolment was through a registered school centre or directly on the IAPT website.', 'iapt'),
    ('RMO 2026 (maths, stage 2)', date(2026, 11, 15), None, '13:00 to 16:00; six problems, each needing a written proof. For IOQM 2026 qualifiers only.', 'hbcse_math'),
    ('NSEA, NSEP, NSEC, NSEB and NSEJS 2026', date(2026, 11, 21), date(2026, 11, 22), 'NSEA on 21 Nov (14:30 to 16:30); NSEP, NSEC, NSEB and NSEJS on 22 Nov; each paper is two hours. For students already enrolled.', 'iapt'),
    ('INMO 2027 (maths, stage 3)', date(2027, 1, 17), None, '12:00 to 16:30; six problems, each needing a written proof. For RMO 2026 qualifiers and INMO 2026 awardees.', 'hbcse_math'),
    ('INO lists published (science, stage 2)', date(2027, 1, 15), None, 'The list of students selected for the INOs is published on the IAPT website by this date; selected students must then register on the HBCSE website to get an admit card.', 'hbcse_sci'),
    ('INAO, INChO, INPhO and INBO 2027 (science, stage 2)', date(2027, 1, 30), date(2027, 1, 31), 'Tentative until confirmed on the HBCSE website: INAO and INChO on 30 Jan, INPhO and INBO on 31 Jan. About 17 centres.', 'hbcse_sci'),
]

STAGES_SCI = [
    ('Stage I', 'NSE', 'NSEA (astronomy), NSEB (biology), NSEC (chemistry), NSEP (physics) and NSEJS (junior science). Run by IAPT, held at nearly 2,000 schools.'),
    ('Stage II', 'INO', 'INAO, INBO, INChO, INPhO. Run by HBCSE at about 17 centres in early the next year. Questions are usually non-conventional and difficult.'),
    ('Stage III', 'OCSC', 'Orientation-cum-selection camps at HBCSE for the top students in each subject.'),
    ('Stage IV', 'Training', 'Training at HBCSE for the students selected for the Indian team.'),
    ('Stage V', 'International', 'IPhO, IChO, IBO and IOAA (and IJSO for junior science, organised through IAPT).'),
]
STAGES_MATH = [
    ('Stage 1', 'IOQM', 'Indian Olympiad Qualifier in Mathematics, run by the Mathematics Teachers\' Association (India). Integer answers, offline.'),
    ('Stage 2', 'RMO', 'Regional Mathematical Olympiad: six proof problems, 3 hours, for IOQM qualifiers.'),
    ('Stage 3', 'INMO', 'Indian National Mathematical Olympiad: six proof problems, 4.5 hours.'),
    ('Stage 4', 'IMOTC', 'International Mathematical Olympiad training camp (the 2026 camp was at CMI Chennai).'),
    ('Stage 5', 'IMO', 'International Mathematical Olympiad: up to six students per country; two papers of three problems, 4.5 hours each.'),
]

# (exam, who may enrol (2026-27 cycle), source)
ELIGIBILITY = [
    ('NSEA, NSEB, NSEC, NSEP 2026', 'Eligible to hold an Indian passport; born between 1 July 2007 and 30 June 2012 (both inclusive); in Class X, XI or XII; living and studying in India (or in the Indian school system) since 30 November 2024 or earlier; not completing Class XII before 30 November 2026; not starting university by 1 June 2027; not appearing in NSEJS 2026.'),
    ('NSEJS 2026', 'In Class 8, 9 or 10 on 30 November 2026; born between 1 January 2012 and 31 December 2013 (both inclusive); eligible to hold an Indian passport; living and studying in India since 30 November 2024; not appearing in NSEA, NSEB, NSEC or NSEP 2026.'),
    ('IOQM 2026', 'Born between 1 August 2007 and 31 July 2014 and studying in Class 8, 9, 10, 11 or 12; eligible to hold an Indian passport; living and studying in India (or the Indian school system) since 30 October 2024; not having qualified or being scheduled for the Class 12 boards before 30 October 2026; not starting university by 1 June 2027.'),
]

FORMATS = [
    ('NSE papers (science stage 1)', 'Two hours, 216 marks. Part A: 48 single-correct multiple-choice questions, +3 for a right answer and -1 for a wrong one. Part B: 12 questions of 6 marks with one or more correct options; credit only if every correct option and no wrong one is marked.'),
    ('IOQM (maths stage 1)', 'Offline on an OMR sheet, no negative marking. The 2024 paper\'s own instructions: 30 questions, 3 hours, 100 marks, each answer a one- or two-digit number; questions 1 to 8 carry 2 marks, 9 to 21 carry 3 marks, 22 to 30 carry 5 marks. The 2026 pages do not restate the format, so read the 2026 instructions.'),
    ('RMO and INMO (maths stages 2 and 3)', 'Six problems each needing a detailed written proof: 3 hours for RMO 2026 and 4.5 hours for INMO 2027.'),
    ('INAO, INBO, INChO, INPhO (science stage 2)', 'Papers in English and Hindi, circumscribed by the senior-secondary (Class XII, CBSE-equivalent) syllabus but usually non-conventional and difficult, comparable to the international Olympiads. Long-answer problems; INBO also has multiple-choice sections in recent years.'),
]

SELECTION = [
    ('NSE to INO', 'Students are split into Group A (Class XII) and Group B (Class X or XI). The minimum target for each group is 200 students for biology, chemistry and physics and 250 for astronomy. The minimum admissible score is 50% of the average of the top ten scores in the subject and the merit index is 80% of that average; everyone at or above the merit index is selected. A state and union-territory quota applies, and at least 20% of each INO are girls through a supernumerary quota. Cut-offs are computed each year.'),
    ('IOQM to RMO', 'At least 10% of the IOQM marks, but that alone is not enough. Per region, the top 200 students in Category A (Classes 8 to 11) and the top 40 in Category B (Class 12) qualify with ties, plus five additional girls in Category A.'),
    ('RMO to INMO', 'A non-zero RMO score is needed, but that alone is not enough. Per region the top 30 in Category A and the top 6 in Category B qualify (ties broken by the IOQM score), plus five additional girls in Category A. INMO 2026 awardees can write INMO 2027 directly.'),
    ('INO to OCSC', 'About 20 students per group (40 in all) for biology, chemistry and physics and 50 for astronomy, by INO merit. A student can attend only one subject camp (or the maths camp) a year, using a preference given at INO registration.'),
    ('Certificates and awards', 'HBCSE gives a Certificate of Merit to students at or above the last selected student in a subject, and merit awards in books and cash to the team selected at the OCSC. No official page we read lists scholarships or admission benefits.'),
]

FEES = [
    ('NSE (per student per subject)', 'Rs 300, not refundable (HBCSE and IAPT 2026 brochures).'),
    ('IOQM 2026', 'Rs 180 for Kendriya Vidyalaya and Jawahar Navodaya students and Rs 300 for all other schools (IOQM site). An older HBCSE FAQ shows lower figures, so use the IOQM site.'),
    ('Later stages (RMO, INMO, INO)', 'No fee for the later stages of the maths Olympiad; check the HBCSE brochure for the science INO.'),
]

INTERNATIONAL = [
    ('IMO 2027', 'Budapest, Hungary, 16 to 26 July 2027. Contestants must be born on or after 1 July of the year 20 years before; each country may send up to six.'),
    ('IPhO 2027', 'Saudi Arabia, July 2027; India\'s team of 5 students.'),
    ('IChO 2027', 'Chinese Taipei, July 2027; India\'s team of 4 students.'),
    ('IBO 2027', 'Poland, July 2027; India\'s team of 4 students.'),
    ('IOAA 2027', 'Venue to be announced, August or September 2027; India\'s team of 5 students.'),
    ('IJSO 2026', 'Sofia, Bulgaria, December 2026. Competitors must be 15 or younger on 31 December of the year of the competition; students normally come through NSEJS and INJSO.'),
]

WARNINGS = [
    'HBCSE cautions that many private examinations called "Olympiads" charge high fees, are not officially recognised by the Government of India and do not lead to the international Olympiads. The Olympiads on this page are the national programme run by HBCSE, the Mathematics Teachers\' Association (India) and IAPT.',
    'The first two stages of the science Olympiads do not necessarily need specialised coaching outside regular school, according to the HBCSE brochure; training starts from the third stage.',
    'The brochure also says Olympiads may not lead directly to career benefits: they are described as a stimulus to begin a career in science or mathematics.',
]

PREPARE = [
    ('Start with the official syllabus', 'The maths Olympiad syllabus is NCERT Class 8 to 10 mathematics plus algebra, plane geometry, combinatorics and number theory. The NSE papers are broadly at senior-secondary (Class XII) level for NSEA, NSEB, NSEC and NSEP, and at Class X level for NSEJS.'),
    ('Use HBCSE\'s past papers with solutions', 'HBCSE publishes past INAO, INBO, INChO, INPhO, INJSO, IOQM, RMO and INMO papers with solutions on its past-papers page. EduPulse-Olympiad turns the multiple-choice and integer-answer questions of those papers into timed practice.'),
    ('Practise the stage-1 style', 'Stage 1 rewards accuracy and speed: integer answers in IOQM, and +3 / -1 multiple choice in the NSE. Take timed mocks, rate your confidence, and keep an error log.'),
    ('Learn to write proofs for RMO and INMO', 'RMO and INMO are marked on complete written proofs, so practise writing each step and checking every case. These cannot be auto-marked, so work with a teacher or mentor.'),
    ('Review what you miss', 'EduPulse-Olympiad turns misses into review cards that return on a schedule, so ideas do not fade between stages.'),
]

FAQ = [
    ('Which Olympiads does the national programme cover?', 'Mathematics (IOQM, RMO, INMO), physics, chemistry, biology and astronomy (NSE, INO, OCSC), and junior science (NSEJS, INJSO). HBCSE is the nodal agency for the science and mathematics Olympiads in India.'),
    ('Is coaching needed?', 'HBCSE says the first two stages do not necessarily need specialised coaching outside regular school and that training starts from stage three. Strong problem practice and good school fundamentals matter most.'),
    ('Can I write both maths and science Olympiads?', 'Yes, they are separate. Within science, a student cannot write NSEJS and an NSE subject in the same year, and can attend only one subject camp (or the maths camp) a year.'),
    ('Can I still enrol for NSE 2026?', 'No. Student enrolment closed on 16 September 2026 and the papers are on 21 and 22 November 2026. Plan for the next cycle: enrolment normally runs in August and September (not confirmed for 2027).'),
    ('When is IOQM 2027?', 'The 2027 dates are not published yet. Watch the IOQM site and the HBCSE page.'),
    ('Do these EduAakashaA tests match the real paper?', 'They are practice tests. The multiple-choice marking (+3 / -1) follows NSE Part A and the integer-answer marking follows IOQM (no negative marks). Part B of the NSE (more than one correct option), RMO and INMO proofs and the stage-2 long-answer papers are not auto-marked here.'),
    ('Is IOQM only for Class 11 and 12?', 'No. For 2026, students in Classes 8 to 12 who meet the birth-date rule can enrol.'),
]

NOT_CONFIRMED = [
    'The 2026-27 maths brochure is a scanned image and could not be read, so IMOTC, EGMO and APMO details for 2026-27 and the IMO team size for 2027 are not shown.',
    'The IOQM 2026 pages do not state the number of questions, marks or duration; the figures above come from the 2024 paper.',
    'The INJSO 2027 date, NSEJS selection numbers and the exact IJSO 2026 dates were not found on official pages.',
    'IPhO, IChO, IBO and IOAA age limits and exam structures were not read: their official sites could not be fetched. The IMO rules are from imo-official.org.',
    'No official page we read lists medallist scholarships or admission benefits beyond the books-and-cash merit awards.',
    'IOQM registration dates differ slightly between the IOQM site and the MTA(I) page, so none are shown for the next cycle.',
]

SOURCES = [
    ('HBCSE science Olympiad page 2026-27', 'https://olympiads.hbcse.tifr.res.in/science-olympiad-2026-2027/'),
    ('HBCSE science Olympiad brochure 2026-27', 'https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2026/10/Brochure-2026-27-English-1.pdf'),
    ('HBCSE mathematical Olympiad page 2026-27', 'https://olympiads.hbcse.tifr.res.in/mathematical-olympiad-2026-2027/'),
    ('IOQM to RMO 2026 criteria', 'https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2026/10/IOQMtoRMO2026ec'),
    ('RMO to INMO criteria', 'https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2026/10/rmotoinmoec.pdf'),
    ('HBCSE syllabus page', 'https://olympiads.hbcse.tifr.res.in/syllabus/'),
    ('HBCSE past papers and sample questions', 'https://olympiads.hbcse.tifr.res.in/past-papers-sample-questions/'),
    ('HBCSE frequently asked questions', 'https://olympiads.hbcse.tifr.res.in/faqs/'),
    ('IAPT: NSE 2026 student brochure', 'https://iapt.org.in/wp-content/uploads/NSE-2026-Student-Brochure.pdf'),
    ('IAPT home page (NSE dates)', 'https://iapt.org.in/'),
    ('IOQM site (MTA India)', 'https://ioqm.mtai.org.in/'),
    ('IOQM 2026 eligibility', 'https://ioqm.mtai.org.in/documents/elcrIOQM.pdf'),
    ('Mathematics Olympiad syllabus', 'https://ioqm.mtai.org.in/documents/Syllabus for Mathematical Olympiad.pdf'),
    ('IMO regulations', 'https://www.imo-official.org/regulations/'),
    ('IJSO', 'https://ijsoweb.org/about-ijso'),
]


def _status(start, end, today):
    last = end or start
    if today > last:
        return 'Done', 'past'
    if today >= start:
        return 'Happening now', 'now'
    days = (start - today).days
    return ('In %d day%s' % (days, '' if days == 1 else 's')), 'soon' if days <= 30 else 'later'


def timeline(today=None):
    today = today or date.today()
    rows = []
    for label, start, end, note, _src in sorted(TIMELINE, key=lambda r: r[1]):
        s, k = _status(start, end, today)
        rows.append({'label': label, 'start': start, 'end': end, 'note': note, 'status': s, 'kind': k})
    return rows


def samples():
    """Six free questions from the bank: two maths (integer answer, shown on request), two physics and two chemistry."""
    out = []
    bank = olympiad.bank()
    for sec, n in (('MATH', 2), ('PHY', 2), ('CHEM', 2)):
        mine = [q for q in bank if q['sec'] == sec and (sec != 'MATH' or q['kind'] == 'int')][:40]
        step = max(1, len(mine) // n)
        for q in mine[::step][:n]:
            out.append({'sec': olympiad.SEC[sec], 'kind': q['kind'], 'q': q['q'], 'opts': q.get('opts') or [], 'ans': q['ans'], 'why': q['why'], 'src': olympiad.source_label(q)})
    return out


def context():
    return {'d': sys.modules[__name__], 'rows': timeline(), 'samples': samples(), 'n_bank': len(olympiad.bank())}
