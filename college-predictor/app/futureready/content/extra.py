"""Assessments 11-12 and the Aptitude Sampler (10 skills x 3 levels). The sampler is practice, not selection: no cut-offs, no rank or admission predictions."""
from . import CH, LK, Q, TX

# ---- 11: Engineering Branch Interest Map -------------------------------------------------------------------------------------
A11 = dict(key='eng_interest', number=11, group='engineering', title='Engineering Branch Interest Map', kind='self', minutes=12,
           purpose='Ten everyday scenarios show which kinds of engineering work you are drawn to. Combined with your Interests Explorer, it suggests branches to explore, never one to choose.',
           instructions='In each scenario, pick the option you would most enjoy, even if you are not sure you would be good at it yet.',
           interpretation='This shows what you are curious about right now. It does not predict your future or decide your branch: interests grow with experience, and several branches usually overlap.',
           accessibility='Ten short scenarios; no timer; can be read aloud.',
           questions=[
    CH('EM-01', 'map', 'Your school wants to cut its electricity bill. What do you most want to do?',
       [('Measure the power used by classroom devices and chart it', {'investigate': 2, 'science': 1, 'nature': 1}), ('Design and build a small solar charger', {'build': 2, 'science': 1, 'nature': 1}),
        ('Write a program that reminds students to switch off lights', {'tech': 2, 'puzzle': 1}), ('Plan a campaign and a schedule to change habits', {'organise': 2, 'communicate': 1, 'people': 1})]),
    CH('EM-02', 'map', 'A city’s main bridge is old. What interests you most?',
       [('Working out how much weight it can carry', {'investigate': 2, 'science': 1, 'build': 1}), ('Designing a better-looking, safer bridge', {'design': 2, 'build': 1}),
        ('Using sensors and data to detect cracks early', {'tech': 2, 'investigate': 1}), ('Coordinating the repair so traffic keeps moving', {'organise': 2, 'people': 1})]),
    CH('EM-03', 'map', 'You are given an old broken radio. You would…',
       [('Open it and trace how the parts connect', {'investigate': 2, 'build': 1}), ('Redesign it into a modern shape', {'design': 2}), ('Write code to make it a smart speaker', {'tech': 2, 'puzzle': 1}), ('Make a guide so others can repair radios too', {'communicate': 2, 'people': 1})]),
    CH('EM-04', 'map', 'A hospital needs a low-cost way to monitor patients. You would…',
       [('Work out how to measure heart rate with a small sensor', {'science': 2, 'build': 1, 'people': 1}), ('Design a comfortable wearable device', {'design': 2, 'people': 1}),
        ('Analyse patient data to predict problems early', {'tech': 2, 'investigate': 1, 'puzzle': 1}), ('Plan how the device will reach rural clinics', {'organise': 2, 'people': 2})]),
    CH('EM-05', 'map', 'Your town has a water shortage. You would…',
       [('Study how to clean and reuse waste water', {'science': 2, 'nature': 2}), ('Build a model rain-water harvesting system', {'build': 2, 'nature': 1}), ('Map leaks and usage with data', {'tech': 1, 'investigate': 2}), ('Organise neighbourhood groups to share water', {'organise': 2, 'people': 2})]),
    CH('EM-06', 'map', 'You watch a drone fly. What makes you most curious?',
       [('How the wings and motors produce lift', {'science': 2, 'investigate': 2}), ('How it senses obstacles and decides what to do', {'tech': 2, 'puzzle': 2}), ('How to build a stronger, lighter frame', {'build': 2, 'design': 1}), ('How drones could help farmers or rescuers', {'people': 2, 'organise': 1})]),
    CH('EM-07', 'map', 'A factory wastes materials. You would…',
       [('Time each step and find the slowest one', {'organise': 2, 'investigate': 1}), ('Redesign the machine to waste less', {'build': 2, 'design': 1}), ('Use cameras and data to spot defects', {'tech': 2, 'puzzle': 1}), ('Test a new material in a lab', {'science': 2, 'investigate': 1})]),
    CH('EM-08', 'map', 'You are asked to improve the school playground. You would…',
       [('Draw and model a safer, attractive layout', {'design': 2, 'build': 1}), ('Check the strength of the equipment', {'investigate': 2, 'science': 1}), ('Survey students to learn what they want', {'people': 2, 'communicate': 1}), ('Plan a budget and timetable', {'organise': 2})]),
    CH('EM-09', 'map', 'Which project would you volunteer for?',
       [('A robot that sorts recycling', {'build': 2, 'tech': 2, 'nature': 1}), ('A game that teaches maths', {'tech': 2, 'people': 1, 'design': 1}), ('A model of a green home', {'design': 2, 'nature': 2}), ('A study of how bicycles work', {'investigate': 2, 'build': 1})]),
    CH('EM-10', 'map', 'Which sentence sounds most like you?',
       [('I like to take things apart to see how they work.', {'investigate': 2, 'build': 1}), ('I like making things look and feel right.', {'design': 2}), ('I like to find the rule behind a puzzle.', {'puzzle': 2, 'tech': 1}), ('I like to bring people together to get things done.', {'organise': 2, 'people': 1, 'communicate': 1})]),
])

# ---- 12: Entrance-system awareness check -------------------------------------------------------------------------------------
A12 = dict(key='entrance_check', number=12, group='entrance', title='Entrance-System Awareness Check', kind='objective', minutes=10,
           purpose='Checks basic awareness of how engineering admission works in India, so families can ask better questions. It is not a preparation test for any exam.',
           instructions='Answer what you know. “I am not sure” is a good start; the Entrance System Awareness Centre explains each item.',
           interpretation='This measures awareness of the system, not ability. Year-specific facts (dates, eligibility, fees) can change and must always be checked on the official website.',
           accessibility='Plain-language questions; no timer.',
           questions=[
    Q('EA-01', 'awareness', 'Which examination is used for admission to the Indian Institutes of Technology (IITs)?', ['JEE Advanced (after qualifying JEE Main)', 'NEET', 'CLAT', 'None, there is no exam'], 0, 'IIT admission uses JEE Advanced, for which JEE Main is the qualifying step.', {'1': 'NEET is for medical programmes.'}),
    Q('EA-02', 'awareness', 'JoSAA is best described as…', ['An entrance examination', 'A counselling process that allots seats using JEE ranks', 'A coaching centre', 'A scholarship'], 1, 'JoSAA allots seats in participating institutions; it is not an exam.', {'0': 'The exam produces the rank; JoSAA uses the rank.'}),
    Q('EA-03', 'awareness', 'TNEA (Tamil Nadu Engineering Admissions) is best described as…', ['A merit-based admission and counselling process, not an entrance examination', 'A national entrance examination', 'An exam conducted by NTA', 'A coaching programme'], 0, 'TNEA is a merit-based admission and counselling process; rules for ranking are published each year.', {'1': 'It is a state process, not a national exam.'}),
    Q('EA-04', 'awareness', 'Why should families always check the official website for dates and eligibility?', ['Rules, dates and fees change from year to year', 'Because the rules never change', 'Because social media always has the latest rule', 'It is not needed'], 0, 'Admission rules are updated regularly, and official notices are the only reliable source.', {}),
    Q('EA-05', 'awareness', 'Which statement is correct?', ['One exam decides a student’s whole career', 'There are many routes into engineering, and several branches lead to similar careers', 'Only one branch is “the best”', 'Marks never matter'], 1, 'Students have many routes and many branches to explore.', {}),
    Q('EA-06', 'awareness', 'Some private universities admit students through…', ['Their own entrance examination or accepted national scores', 'Only a national exam', 'Only an interview', 'Random selection'], 0, 'Institutions may run their own tests; check each notice.', {}),
    Q('EA-07', 'awareness', 'A counselling process mainly decides…', ['Which seat a candidate is allotted', 'Which questions appear on an exam', 'The syllabus', 'The exam date'], 0, 'Counselling is where seats are allotted according to published rules.', {}),
    Q('EA-08', 'awareness', 'What is the best use of Class 8–9 for future engineering interest?', ['Build strong basics in maths, science and reading, and explore interests through projects', 'Memorise past papers', 'Choose a branch immediately', 'Stop other activities'], 0, 'Strong foundations and curiosity matter most at this stage; branch choice is years away.', {}),
])

# ---- 13: Parent questionnaire is the same as assessment 10 with audience 'parent' ---------------------------------------------

# ---- Reflection / growth review (used in quarterly reports) --------------------------------------------------------------------
A_REFLECT = dict(key='reflection', number=None, group='core', title='Quarterly Reflection', kind='self', minutes=8,
                 purpose='A short reflection each quarter on confidence, progress and support, so the growth report includes your voice.',
                 instructions='Answer honestly. This is for you and your mentor.',
                 interpretation='Self-reports show how you feel about your progress. They sit beside, and do not replace, the work you have actually completed.',
                 accessibility='Five-point scale and two short text boxes.',
                 questions=[LK('QR-01', 'confidence', 'I feel more confident about my studies than three months ago.'),
                            LK('QR-02', 'clarity', 'I understand myself and my interests better than three months ago.'),
                            LK('QR-03', 'support', 'I get the help I need from my mentor and family.'),
                            LK('QR-04', 'pressure', 'I feel under a lot of pressure about the future.', reverse=True),
                            TX('QR-T1', 'proud', 'What are you most proud of this quarter?'),
                            TX('QR-T2', 'next', 'What do you want to try next?')])

# ---- Aptitude sampler ------------------------------------------------------------------------------------------------------
SAMPLER_SKILLS = [('numerical', 'Numerical reasoning'), ('logical', 'Logical reasoning'), ('patterns', 'Pattern recognition'), ('verbal', 'Verbal reasoning'),
                  ('spatial', 'Spatial reasoning'), ('data', 'Data interpretation'), ('mechanical', 'Mechanical reasoning'), ('scientific', 'Scientific reasoning'),
                  ('decomposition', 'Problem decomposition'), ('digital', 'Digital logic')]


def _s(skill, level, n, prompt, opts, ans, expl, dist=None):
    return Q(f'AS-{skill[:3].upper()}-{level}{n}', skill, prompt, opts, ans, expl, dist or {}, level=level)


S = []
_add = S.append
# numerical
_add(_s('numerical', 1, 1, '45 + 38 =', ['73', '83', '93', '82'], 1, '45 + 38 = 83.'))
_add(_s('numerical', 1, 2, '6 × 7 =', ['36', '42', '48', '49'], 1, '6 × 7 = 42.'))
_add(_s('numerical', 1, 3, 'Half of 18 is…', ['6', '8', '9', '12'], 2, '18 ÷ 2 = 9.'))
_add(_s('numerical', 2, 1, '20% of 150 is…', ['20', '25', '30', '35'], 2, '10% = 15, so 20% = 30.'))
_add(_s('numerical', 2, 2, '3/4 of 24 is…', ['16', '18', '20', '21'], 1, '24 ÷ 4 = 6; 6 × 3 = 18.'))
_add(_s('numerical', 2, 3, 'Two numbers are in the ratio 2 : 3 and add up to 50. The larger is…', ['20', '25', '30', '35'], 2, 'Parts = 5, one part = 10, so 3 parts = 30.'))
_add(_s('numerical', 3, 1, 'A price rises by 20%, then falls by 20%. Compared with the start, the final price is…', ['the same', '4% lower', '4% higher', '2% lower'], 1, '100 → 120 → 96. That is 4% lower.', {'0': 'The second 20% is taken from a bigger number.'}))
_add(_s('numerical', 3, 2, 'The mean of five numbers is 12. Four of them are 10, 11, 13 and 14. The fifth is…', ['10', '11', '12', '13'], 2, 'Total = 60; the four add to 48; the fifth is 12.'))
_add(_s('numerical', 3, 3, 'Pipe A fills a tank in 6 hours, pipe B in 3 hours. Together they fill it in…', ['1 hour', '2 hours', '3 hours', '4.5 hours'], 1, 'In one hour they fill 1/6 + 1/3 = 1/2 of the tank, so 2 hours.'))
# logical
_add(_s('logical', 1, 1, 'All cats are animals. Tom is a cat. So Tom is…', ['an animal', 'a dog', 'a bird', 'not an animal'], 0, 'If all cats are animals and Tom is a cat, Tom is an animal.'))
_add(_s('logical', 1, 2, 'If today is Monday, tomorrow is Tuesday. Today is Monday. So tomorrow is…', ['Monday', 'Tuesday', 'Wednesday', 'Cannot tell'], 1, 'The rule gives Tuesday.'))
_add(_s('logical', 1, 3, 'Ria is taller than Sam, and Sam is taller than Tej. The tallest is…', ['Sam', 'Tej', 'Ria', 'Cannot tell'], 2, 'Ria > Sam > Tej.'))
_add(_s('logical', 2, 1, 'All birds have feathers. A penguin is a bird. So a penguin…', ['has feathers', 'cannot swim', 'cannot be a bird', 'may have no feathers'], 0, 'It follows directly from the rule.'))
_add(_s('logical', 2, 2, 'No fish can walk. Some pets are fish. So…', ['some pets cannot walk', 'all pets can walk', 'no pets are fish', 'fish are never pets'], 0, 'Those pets that are fish cannot walk.'))
_add(_s('logical', 2, 3, 'A is left of B, B is left of C, C is left of D in a row. Who is second from the right?', ['A', 'B', 'C', 'D'], 2, 'Order from left: A, B, C, D, so C is second from the right.'))
_add(_s('logical', 3, 1, 'If the alarm rings, Ravi wakes up. Ravi woke up. Did the alarm necessarily ring?', ['Yes', 'No, he may have woken for another reason', 'Yes, always', 'Cannot be a rule'], 1, 'The rule says alarm → wakes, not wakes → alarm.', {'0': 'This reverses the rule.'}))
_add(_s('logical', 3, 2, '“All my friends like football.” Raj does not like football. Which must be true?', ['Raj is my friend', 'Raj is not my friend', 'Raj dislikes sport', 'I do not like football'], 1, 'If Raj were a friend, he would like football.'))
_add(_s('logical', 3, 3, 'In a class, 18 like maths, 15 like science, 8 like both and 5 like neither. How many students are in the class?', ['26', '30', '35', '46'], 1, '18 + 15 − 8 = 25 like at least one; plus 5 = 30.'))
# patterns
_add(_s('patterns', 1, 1, '5, 10, 15, 20, ?', ['22', '25', '30', '35'], 1, 'Add 5 each time.'))
_add(_s('patterns', 1, 2, '2, 4, 8, 16, ?', ['18', '24', '32', '64'], 2, 'Each term doubles.'))
_add(_s('patterns', 1, 3, 'A, C, E, G, ?', ['H', 'I', 'J', 'K'], 1, 'Skip one letter each time.'))
_add(_s('patterns', 2, 1, '3, 5, 9, 17, ?', ['25', '31', '33', '35'], 2, 'Differences double: 2, 4, 8, 16, so 17 + 16 = 33.'))
_add(_s('patterns', 2, 2, '1, 1, 2, 3, 5, 8, ?', ['11', '12', '13', '14'], 2, 'Each term is the sum of the previous two.'))
_add(_s('patterns', 2, 3, '100, 90, 81, 73, 66, ?', ['58', '60', '62', '64'], 1, 'Differences are 10, 9, 8, 7, 6, so the next is 66 − 6 = 60.'))
_add(_s('patterns', 3, 1, '2, 3, 5, 8, 13, ?', ['18', '19', '20', '21'], 3, 'Differences 1, 2, 3, 5 → 8, so 13 + 8 = 21.'))
_add(_s('patterns', 3, 2, '1, 2, 6, 24, 120, ?', ['240', '480', '600', '720'], 3, 'Multiply by 2, 3, 4, 5, 6.'))
_add(_s('patterns', 3, 3, '2, 6, 18, 54, ?', ['108', '126', '162', '216'], 2, 'Multiply by 3 each time.'))
# verbal
_add(_s('verbal', 1, 1, 'Cold is to hot as day is to…', ['sun', 'night', 'light', 'morning'], 1, 'Opposites.'))
_add(_s('verbal', 1, 2, 'Which is the odd one out?', ['Rose', 'Lily', 'Tulip', 'Mango'], 3, 'The others are flowers.'))
_add(_s('verbal', 1, 3, 'A word that means almost the same as “big” is…', ['tiny', 'large', 'thin', 'slow'], 1, '“Large” is a synonym.'))
_add(_s('verbal', 2, 1, 'Doctor is to hospital as teacher is to…', ['book', 'school', 'student', 'class'], 1, 'The place where each works.'))
_add(_s('verbal', 2, 2, 'Which is the odd one out?', ['square', 'circle', 'triangle', 'cube'], 3, 'A cube is three-dimensional; the others are flat shapes.'))
_add(_s('verbal', 2, 3, 'The word closest in meaning to “reluctant” is…', ['eager', 'unwilling', 'angry', 'tired'], 1, '“Reluctant” means unwilling.'))
_add(_s('verbal', 3, 1, '“Brevity” means…', ['length', 'shortness', 'bravery', 'noise'], 1, 'Brevity is shortness, especially of speech or writing.'))
_add(_s('verbal', 3, 2, 'Library is to books as orchestra is to…', ['music', 'conductor', 'musicians', 'stage'], 2, 'A library holds books; an orchestra consists of musicians.'))
_add(_s('verbal', 3, 3, '“Although it was expensive, the phone was popular.” The word “although” signals…', ['addition', 'contrast', 'time', 'cause'], 1, '“Although” introduces a contrast.'))
# spatial
_add(_s('spatial', 1, 1, 'How many sides does a triangle have?', ['2', '3', '4', '5'], 1, 'Three.'))
_add(_s('spatial', 1, 2, 'How many sides does a hexagon have?', ['5', '6', '7', '8'], 1, 'Six.'))
_add(_s('spatial', 1, 3, 'How many faces does a rectangular box have?', ['4', '6', '8', '12'], 1, 'Six.'))
_add(_s('spatial', 2, 1, 'How many faces does a triangular prism have?', ['3', '4', '5', '6'], 2, 'Two triangles and three rectangles.'))
_add(_s('spatial', 2, 2, 'You face north, turn right, then turn right again. You are now facing…', ['north', 'east', 'south', 'west'], 2, 'North → east → south.'))
_add(_s('spatial', 2, 3, 'The letter “b” is flipped left-to-right in a mirror. It looks like…', ['p', 'd', 'q', 'b'], 1, 'The left–right mirror image of b is d.'))
_add(_s('spatial', 3, 1, 'A cube painted red on all faces is cut into 27 equal small cubes. How many small cubes have exactly 3 red faces?', ['4', '6', '8', '12'], 2, 'Only the 8 corner cubes.'))
_add(_s('spatial', 3, 2, 'In the same 27-cube, how many have exactly 2 red faces?', ['6', '8', '12', '24'], 2, 'The 12 edge cubes, one from each edge.'))
_add(_s('spatial', 3, 3, 'In the same 27-cube, how many have no red face?', ['0', '1', '3', '6'], 1, 'Only the one at the centre.'))
# data
_add(_s('data', 1, 1, 'Books read: Mon 4, Tue 6, Wed 3. Which day had the most?', ['Mon', 'Tue', 'Wed', 'All same'], 1, 'Tuesday has 6.'))
_add(_s('data', 1, 2, 'Using the same data, the total is…', ['11', '12', '13', '14'], 2, '4 + 6 + 3 = 13.'))
_add(_s('data', 1, 3, 'The difference between the highest and lowest day is…', ['2', '3', '4', '6'], 1, '6 − 3 = 3.'))
_add(_s('data', 2, 1, 'The mean of 4, 6, 8, 10 is…', ['6', '7', '8', '9'], 1, '28 ÷ 4 = 7.'))
_add(_s('data', 2, 2, 'The median of 3, 9, 5, 7, 1 is…', ['3', '5', '7', '9'], 1, 'Sorted: 1, 3, 5, 7, 9; the middle is 5.'))
_add(_s('data', 2, 3, 'The mode of 2, 3, 3, 5, 3, 6 is…', ['2', '3', '5', '6'], 1, '3 appears most often.'))
_add(_s('data', 3, 1, 'Sales rose from 40 to 50. The percentage increase is…', ['10%', '20%', '25%', '50%'], 2, '10 ÷ 40 = 25%.', {'0': 'Divide the change by the starting value.'}))
_add(_s('data', 3, 2, 'A bar chart’s vertical axis starts at 90 instead of 0. This makes small differences look…', ['smaller', 'larger', 'exactly the same', 'impossible to see'], 1, 'A truncated axis exaggerates differences.'))
_add(_s('data', 3, 3, 'Class A: 20 students, mean 60. Class B: 30 students, mean 70. The combined mean is…', ['65', '66', '67', '68'], 1, '(1200 + 2100) ÷ 50 = 66.', {'0': 'The classes are different sizes, so a plain average of 60 and 70 is wrong.'}))
# mechanical
_add(_s('mechanical', 1, 1, 'Which of these is a simple machine?', ['Lever', 'Television', 'Battery', 'Mirror'], 0, 'A lever is a simple machine.'))
_add(_s('mechanical', 1, 2, 'A seesaw is an example of a…', ['pulley', 'lever', 'wedge', 'screw'], 1, 'It pivots on a fulcrum.'))
_add(_s('mechanical', 1, 3, 'A ramp makes lifting a load…', ['need less force over a longer distance', 'impossible', 'need more force', 'need no force'], 0, 'A ramp trades distance for force.'))
_add(_s('mechanical', 2, 1, 'A longer spanner makes it easier to loosen a nut because it gives…', ['more friction', 'a greater turning effect', 'more weight', 'less force'], 1, 'Turning effect (torque) = force × distance.'))
_add(_s('mechanical', 2, 2, 'A small gear drives a larger gear. The larger gear turns…', ['faster', 'slower', 'at the same speed', 'not at all'], 1, 'The larger gear has more teeth, so turns more slowly.'))
_add(_s('mechanical', 2, 3, 'A movable pulley lets you lift a load with about…', ['twice the force', 'half the force but more rope pulled', 'no force', 'the same rope'], 1, 'Force is halved, but you pull twice the rope.'))
_add(_s('mechanical', 3, 1, 'A 10-tooth gear drives a 30-tooth gear. When the driver turns 3 times, the driven gear turns…', ['1 time', '3 times', '9 times', '30 times'], 0, 'Ratio 1 : 3, so 3 turns of the driver give 1 turn.'))
_add(_s('mechanical', 3, 2, 'A 2 m lever has its fulcrum 0.5 m from a 60 N load. What effort at the far end (1.5 m away) balances it?', ['10 N', '20 N', '30 N', '60 N'], 1, '60 × 0.5 = F × 1.5, so F = 20 N.'))
_add(_s('mechanical', 3, 3, 'The same force on a smaller area produces…', ['less pressure', 'greater pressure', 'the same pressure', 'no pressure'], 1, 'Pressure = force ÷ area.'))
# scientific
_add(_s('scientific', 1, 1, 'In a fair test, you change…', ['one thing', 'everything', 'nothing', 'two things at once'], 0, 'Change one variable and keep the others the same.'))
_add(_s('scientific', 1, 2, 'Which of these is a living thing?', ['Rock', 'Tree', 'River', 'Cloud'], 1, 'A tree is a living thing.'))
_add(_s('scientific', 1, 3, 'Water boils at about 100 °C at…', ['sea level', 'the top of Everest', 'inside a freezer', 'any height at the same temperature'], 0, 'At sea-level pressure, water boils near 100 °C; this changes with altitude.'))
_add(_s('scientific', 2, 1, 'A control group is used to…', ['compare with the group that was changed', 'make the experiment longer', 'hide the result', 'avoid measuring'], 0, 'It provides a baseline.'))
_add(_s('scientific', 2, 2, 'Which material conducts electricity well?', ['Copper', 'Plastic', 'Wood', 'Rubber'], 0, 'Metals such as copper are good conductors.'))
_add(_s('scientific', 2, 3, 'In a torch, the energy changes mostly from…', ['chemical → electrical → light', 'light → heat', 'sound → light', 'heat → chemical'], 0, 'The battery stores chemical energy.'))
_add(_s('scientific', 3, 1, 'Three trial results are 10, 11 and 25 cm. The best next step is to…', ['ignore the odd result', 'repeat the trial and check the 25 cm result', 'average and stop', 'say the experiment failed'], 1, 'An outlier should be investigated, not just thrown away.'))
_add(_s('scientific', 3, 2, 'A student tests one plant per fertiliser and concludes fertiliser X is best. The main weakness is…', ['too few plants', 'wrong colour', 'wrong season', 'none'], 0, 'One plant per condition cannot show a reliable difference.'))
_add(_s('scientific', 3, 3, 'Ice-cream sales and drownings rise together in summer. The best explanation is…', ['ice cream causes drowning', 'a third factor, hot weather, affects both', 'drowning causes ice-cream sales', 'it is only luck'], 1, 'A correlation can come from a shared cause.'))
# decomposition
_add(_s('decomposition', 1, 1, 'To find the area of a classroom floor you need…', ['length and width', 'height only', 'colour', 'number of windows'], 0, 'Area = length × width.'))
_add(_s('decomposition', 1, 2, 'When planning a birthday party, a sensible first step is to decide…', ['the guest list and budget', 'the cake flavour', 'the cleaning plan', 'the photographs'], 0, 'Number of guests and budget shape every other choice.'))
_add(_s('decomposition', 1, 3, 'Which is a sub-task of “make a sandwich”?', ['Spread butter on bread', 'Eat dinner', 'Wash the car', 'Buy shoes'], 0, 'It is one step of making a sandwich.'))
_add(_s('decomposition', 2, 1, 'To find the cheaper pack, compare…', ['the price per unit', 'the colour', 'the weight of the box', 'the brand name'], 0, 'Unit price makes different sizes comparable.'))
_add(_s('decomposition', 2, 2, 'A program prints the wrong total. The best first check is…', ['the inputs and each calculation step', 'restart the computer', 'change the colours', 'delete everything'], 0, 'Trace the data step by step.'))
_add(_s('decomposition', 2, 3, 'A job takes 12 steps of 5 minutes each. Three helpers share the steps equally and work together. How long does it take?', ['10 min', '15 min', '20 min', '60 min'], 2, '60 minutes ÷ 3 = 20 minutes.'))
_add(_s('decomposition', 3, 1, 'Tasks: A (2 days), B (3 days, only after A), C (4 days, independent). One person does them one at a time. Minimum total days?', ['4', '5', '7', '9'], 3, '2 + 3 + 4 = 9 days.'))
_add(_s('decomposition', 3, 2, 'Same tasks, two people working in parallel. Minimum total days?', ['4', '5', '7', '9'], 1, 'Person 1: A then B = 5 days; person 2: C = 4 days; the project ends at day 5.'))
_add(_s('decomposition', 3, 3, 'You keep halving 64 until you reach 1. How many halvings?', ['4', '5', '6', '8'], 2, '64 → 32 → 16 → 8 → 4 → 2 → 1 is six steps.'))
# digital
_add(_s('digital', 1, 1, 'You should share your one-time password (OTP) with…', ['your friend', 'no one', 'a caller from “the bank”', 'anyone who asks'], 1, 'Real organisations never ask for your OTP.'))
_add(_s('digital', 1, 2, 'Which is a common file type for a photograph?', ['.jpg', '.exe', '.mp3', '.zip'], 0, '.jpg is an image format.'))
_add(_s('digital', 1, 3, 'Which is an input device?', ['Keyboard', 'Monitor', 'Speaker', 'Printer'], 0, 'A keyboard sends data to the computer.'))
_add(_s('digital', 2, 1, 'The binary number 101 equals…', ['3', '4', '5', '6'], 2, '4 + 0 + 1 = 5.'))
_add(_s('digital', 2, 2, 'Phishing means…', ['tricking people into revealing information', 'fishing online', 'cleaning a computer', 'copying a file'], 0, 'It is a scam that imitates a trusted source.'))
_add(_s('digital', 2, 3, 'A loop repeats an instruction. Which describes it?', ['Do something several times', 'Do something once', 'Never stop and never start', 'Delete the program'], 0, 'Loops repeat steps.'))
_add(_s('digital', 3, 1, 'The binary number 1101 equals…', ['11', '12', '13', '14'], 2, '8 + 4 + 0 + 1 = 13.'))
_add(_s('digital', 3, 2, 'A loop starts with 5 and adds 3, four times. The final value is…', ['14', '17', '20', '23'], 1, '5 + 3 × 4 = 17.'))
_add(_s('digital', 3, 3, 'An image looks extremely realistic. The best caution is…', ['Images can be generated or edited, so check the source', 'It must be real', 'Pictures cannot be edited', 'Only videos can be faked'], 0, 'Realistic does not mean authentic.'))

SAMPLER = dict(key='sampler', number=None, group='sampler', title='Aptitude Sampler', kind='objective', minutes=15,
               purpose='Short practice sets in ten skills at three levels. It is for practice and awareness; it has no pass mark, no cut-off and no rank or admission prediction.',
               instructions='Choose a skill and a level. Start at Level 1 and move up when you feel ready. Each set takes about five minutes.',
               interpretation='A set shows how a handful of questions went today. It is not a measure of ability, and it must not be used to decide a branch or college. The aim is to practise and notice what to strengthen.',
               accessibility='Short multiple-choice sets; no timer is enforced.',
               questions=S)
