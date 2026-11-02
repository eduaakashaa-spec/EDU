"""NIRF 2025 Architecture and Planning: the 15 sub-scores behind each institute's five parameter scores, as printed in NIRF's rating chart for the institute.
Entered by hand from the rating charts of 39 of the 40 ranked institutions (the charts supplied so far). Every row is checked in tests against the five NIRF scores:
TLR = SS + FSR + FQE + FRU, RPC = PU + QP + FPPP, GO = GPH + GUE + MS, OI = RD + WD + ESCS + PCS, PR = PR (to within rounding).
Order of each row: SS, FSR, FQE, FRU, PU, QP, FPPP, GPH, GUE, MS, RD, WD, ESCS, PCS, PR."""

# key, label, maximum marks on the architecture chart, parameter, what it measures (from the NIRF methodology paper)
SUB_PARAMS = [
    ('SS', 'Student strength', 20, 'TLR', 'Sanctioned intake and students on roll, with doctoral students.'),
    ('FSR', 'Faculty-student ratio', 30, 'TLR', 'Full-time regular faculty for the students enrolled. Full marks at about 1 faculty member to 15 students; none below 1 to 50.'),
    ('FQE', 'Faculty qualification and experience', 20, 'TLR', 'Share of faculty with a PhD, and a balance of faculty with up to 8, 8 to 15 and over 15 years of experience.'),
    ('FRU', 'Financial resources and their use', 30, 'TLR', 'Capital and running expenditure per student over three years, excluding new buildings and hostels.'),
    ('PU', 'Publications', 60, 'RPC', 'Publications per faculty member, from third-party databases, less retracted papers.'),
    ('QP', 'Quality of publications', 20, 'RPC', 'Citations per faculty member and the share of papers in the top 25 percent by citations.'),
    ('FPPP', 'Projects and professional practice', 20, 'RPC', 'Sponsored research and consultancy income per faculty member over three years.'),
    ('GPH', 'Placement and higher studies', 40, 'GO', 'Share of graduates placed plus share selected for higher studies, over three years.'),
    ('GUE', 'University examinations', 30, 'GO', 'Share of the approved intake passing within the stipulated time.'),
    ('MS', 'Median salary', 30, 'GO', 'Median salary of graduates over three years.'),
    ('RD', 'Region diversity', 30, 'OI', 'Students from other states (most of the marks) and from other countries.'),
    ('WD', 'Women diversity', 30, 'OI', 'Share of women among students (expected 50 percent) and faculty (expected 20 percent).'),
    ('ESCS', 'Economically and socially challenged students', 20, 'OI', 'Share of undergraduates whose full tuition is reimbursed by the institution.'),
    ('PCS', 'Facilities for physically challenged students', 20, 'OI', 'Lifts or ramps, walking aids and transport, and specially designed toilets.'),
    ('PR', 'Perception', 100, 'PR', 'A survey of employers and academic peers.'),
]
SUB_KEYS = [p[0] for p in SUB_PARAMS]

# NIRF institute id -> the 15 scores
SUB = {
    'IR-A-C-1331': (12.47, 30.00, 9.40, 8.00, 16.12, 11.38, 0.45, 33.83, 30.00, 12.56, 5.51, 30.00, 1.00, 20.00, 30.68),
    'IR-A-C-26794': (13.73, 27.86, 9.79, 3.99, 12.89, 17.14, 2.89, 26.00, 30.00, 15.08, 0.38, 30.00, 1.52, 20.00, 44.17),
    'IR-A-C-43708': (12.00, 30.00, 9.51, 11.13, 18.55, 15.63, 5.53, 36.67, 30.00, 22.03, 5.97, 30.00, 2.24, 20.00, 30.68),
    'IR-A-C-46330': (14.61, 24.11, 10.81, 14.17, 4.20, 16.11, 0.67, 27.47, 30.00, 15.64, 16.20, 29.89, 0.28, 20.00, 37.36),
    'IR-A-C-46873': (12.48, 25.50, 10.58, 9.26, 0.00, 0.00, 4.87, 35.47, 26.30, 15.86, 0.58, 26.30, 4.07, 20.00, 32.10),
    'IR-A-C-47256': (11.45, 27.42, 8.71, 7.92, 21.27, 2.72, 0.87, 29.11, 26.25, 10.52, 3.75, 27.52, 0.52, 20.00, 29.21),
    'IR-A-C-57952': (14.88, 29.53, 10.88, 11.29, 3.70, 9.40, 0.82, 35.00, 30.00, 15.83, 15.28, 30.00, 0.24, 20.00, 59.73),
    'IR-A-U-0072': (9.05, 28.40, 14.29, 6.80, 40.31, 18.94, 2.54, 29.92, 24.51, 18.90, 11.25, 25.86, 7.93, 20.00, 32.10),
    'IR-A-U-0092': (9.69, 25.00, 12.43, 7.09, 28.09, 17.45, 0.59, 13.95, 29.04, 17.99, 11.33, 29.56, 5.93, 16.00, 19.07),
    'IR-A-U-0099': (13.36, 18.75, 8.25, 7.04, 12.27, 18.39, 2.69, 38.33, 30.00, 14.86, 6.43, 30.00, 0.19, 20.00, 30.68),
    'IR-A-U-0108': (13.40, 30.00, 12.34, 13.27, 22.86, 19.71, 3.87, 40.00, 30.00, 21.42, 25.45, 30.00, 10.72, 20.00, 33.48),
    'IR-A-U-0116': (17.36, 22.53, 10.54, 15.46, 16.57, 7.70, 13.47, 19.63, 28.93, 21.91, 22.83, 28.08, 0.33, 20.00, 100.00),
    'IR-A-U-0127': (17.81, 30.00, 9.46, 14.95, 16.01, 13.15, 18.52, 27.67, 30.00, 20.39, 14.78, 30.00, 0.36, 20.00, 51.81),
    'IR-A-U-0146': (13.84, 30.00, 8.81, 10.33, 23.00, 14.37, 2.11, 18.27, 30.00, 16.04, 9.06, 30.00, 1.24, 20.00, 22.73),
    'IR-A-U-0189': (11.10, 20.21, 11.79, 7.63, 16.85, 15.82, 1.33, 32.27, 29.45, 20.51, 12.66, 29.28, 6.54, 20.00, 36.11),
    'IR-A-U-0201': (5.60, 30.00, 12.59, 24.61, 26.90, 14.55, 2.45, 17.82, 24.89, 13.76, 9.06, 22.35, 2.24, 20.00, 19.07),
    'IR-A-U-0202': (7.95, 30.00, 14.98, 12.89, 20.52, 16.37, 6.37, 17.00, 26.38, 15.93, 10.95, 28.39, 0.08, 20.00, 39.76),
    'IR-A-U-0217': (10.44, 30.00, 12.74, 14.21, 11.29, 11.93, 2.03, 11.33, 21.84, 17.49, 17.59, 29.70, 3.11, 20.00, 26.10),
    'IR-A-U-0263': (12.00, 30.00, 19.21, 28.25, 35.56, 17.81, 6.08, 34.56, 30.00, 20.09, 14.87, 30.00, 9.72, 20.00, 58.26),
    'IR-A-U-0284': (13.97, 24.75, 14.32, 13.01, 11.92, 18.24, 8.28, 30.88, 30.00, 19.13, 12.93, 27.66, 3.61, 20.00, 22.73),
    'IR-A-U-0334': (13.11, 18.41, 11.67, 12.92, 32.21, 15.56, 5.77, 37.24, 30.00, 20.80, 15.34, 30.00, 4.49, 20.00, 34.81),
    'IR-A-U-0357': (5.71, 30.00, 16.14, 12.00, 42.44, 20.00, 3.90, 25.40, 29.17, 20.21, 13.20, 25.78, 7.15, 20.00, 53.52),
    'IR-A-U-0373': (9.47, 21.00, 9.64, 11.75, 9.90, 18.15, 3.20, 22.56, 27.29, 22.46, 11.29, 24.55, 0.61, 20.00, 10.62),
    'IR-A-U-0379': (9.73, 30.00, 14.54, 10.13, 19.29, 17.67, 4.44, 16.89, 24.22, 24.19, 17.61, 23.90, 2.47, 20.00, 26.10),
    'IR-A-U-0410': (13.78, 19.52, 10.46, 8.06, 36.57, 18.81, 13.16, 33.03, 30.00, 18.98, 16.60, 29.59, 5.85, 20.00, 24.45),
    'IR-A-U-0439': (12.85, 22.50, 11.28, 6.56, 25.08, 18.66, 3.62, 6.38, 28.35, 16.52, 0.69, 29.30, 3.13, 20.00, 82.93),
    'IR-A-U-0461': (13.82, 30.00, 10.74, 11.58, 9.95, 11.69, 4.01, 16.67, 30.00, 21.36, 15.90, 30.00, 9.18, 20.00, 5.64),
    'IR-A-U-0467': (12.00, 19.74, 9.62, 14.58, 35.19, 15.66, 0.06, 30.07, 30.00, 20.39, 15.33, 30.00, 10.07, 20.00, 81.24),
    'IR-A-U-0473': (9.32, 30.00, 11.16, 11.80, 36.87, 18.55, 5.61, 23.33, 28.00, 18.51, 11.19, 24.55, 0.56, 20.00, 19.07),
    'IR-A-U-0560': (9.73, 30.00, 16.40, 23.93, 60.00, 15.86, 19.79, 33.04, 30.00, 26.24, 25.90, 22.73, 6.57, 20.00, 74.22),
    'IR-A-U-0573': (11.05, 19.80, 13.21, 25.44, 51.33, 16.11, 16.93, 29.51, 30.00, 30.00, 22.42, 18.23, 6.27, 20.00, 81.24),
    'IR-A-U-0575': (8.42, 30.00, 13.07, 8.61, 27.40, 15.13, 5.17, 29.00, 27.34, 19.62, 1.38, 26.84, 4.36, 20.00, 52.67),
    'IR-A-U-0584': (7.11, 30.00, 17.07, 18.65, 33.13, 17.13, 4.43, 30.56, 29.76, 18.83, 12.84, 29.26, 4.27, 20.00, 58.26),
    'IR-A-U-0626': (15.37, 27.50, 12.75, 13.13, 8.29, 4.91, 9.64, 28.90, 27.13, 19.65, 22.14, 29.61, 4.71, 20.00, 58.26),
    'IR-A-U-0627': (15.84, 19.31, 10.81, 11.86, 12.85, 14.61, 2.89, 34.55, 26.09, 19.78, 19.89, 28.06, 1.68, 20.00, 62.52),
    'IR-A-U-0747': (13.80, 30.00, 10.46, 14.05, 22.95, 18.04, 6.21, 20.00, 30.00, 19.26, 24.84, 30.00, 0.92, 20.00, 15.06),
    'IR-A-U-0749': (6.05, 30.00, 17.84, 11.67, 28.23, 11.57, 4.93, 24.80, 30.00, 18.20, 13.20, 26.10, 0.64, 20.00, 10.62),
    'IR-A-U-0779': (11.78, 30.00, 20.00, 10.28, 3.01, 0.00, 2.39, 31.58, 30.00, 18.07, 24.56, 30.00, 9.13, 20.00, 12.89),
    'IR-A-U-0830': (13.32, 28.26, 10.47, 11.71, 2.82, 0.00, 3.81, 29.13, 27.76, 15.64, 6.88, 30.00, 0.26, 20.00, 5.64),
}
