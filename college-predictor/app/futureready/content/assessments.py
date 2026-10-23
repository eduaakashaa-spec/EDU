"""Core assessments 1-10 (assessment 11 is derived from 5 + the engineering interest map; 12 is a repeat/compare of selected ones)."""
from . import CH, LK, Q, TX

LIK = ['Not like me', 'A little like me', 'Sometimes like me', 'Mostly like me', 'Very much like me']

PASSAGE = ("Rainwater harvesting means collecting and storing rain from rooftops instead of letting it run into drains. The stored water "
           "can be used for gardens and cleaning and, after treatment, even for drinking. Cities that adopt it reduce pressure on groundwater "
           "and lower the chance of street flooding. However, tanks must be cleaned regularly; otherwise mosquitoes can breed in the standing water.")

# ---------------------------------------------------------------------------------------------------------------------------
A1 = dict(key='academic', number=1, group='core', title='Academic Foundations Diagnostic', kind='objective', minutes=25,
          purpose='A short check of foundational understanding in mathematics, science, reading, data and scientific reasoning, so mentors know which concepts to reinforce first.',
          instructions='Answer every question. Nobody is judging you: wrong answers show where to practise next. You can use rough paper; please do not use a calculator.',
          interpretation='This is a 20-question snapshot. It shows which ideas are secure and which need practice. It does not measure overall ability, school marks or potential, and one short test can be affected by mood, time and wording.',
          accessibility='Questions are text-based; the reading passage can be read aloud by a parent or mentor. No timer is enforced.',
          questions=[
    Q('AF-M-01', 'math', 'Solve for x: 3x − 7 = 11', ['4', '5', '6', '7'], 2, 'Add 7 to both sides: 3x = 18, then divide by 3: x = 6.', {'0': 'Subtracting 7 instead of adding it gives 3x = 4.'}),
    Q('AF-M-02', 'math', 'A bag costs ₹800. After a 25% discount, the price is:', ['₹550', '₹600', '₹625', '₹650'], 1, '25% of 800 is 200, so 800 − 200 = ₹600.', {'3': 'Taking 25% off 800 as ₹150 is a common slip.'}),
    Q('AF-M-03', 'math', 'Boys and girls in a club are in the ratio 3 : 2. There are 40 members. How many are boys?', ['16', '20', '24', '30'], 2, 'Ratio parts = 5. One part = 8, so boys = 3 × 8 = 24.', {'1': 'Splitting 40 equally ignores the ratio.'}),
    Q('AF-M-04', 'math', 'The area of a triangle with base 10 cm and height 6 cm is:', ['16 cm²', '30 cm²', '60 cm²', '36 cm²'], 1, 'Area = ½ × base × height = ½ × 10 × 6 = 30 cm².', {'2': 'Forgetting the ½ gives the area of a rectangle.'}),
    Q('AF-S-01', 'science', 'Which of these is a chemical change?', ['Ice melting', 'Iron rusting', 'Sugar dissolving in water', 'Glass breaking'], 1, 'Rusting makes a new substance (iron oxide). The others change form but not the substance.', {'0': 'Melting is a physical change: it can be reversed by freezing.'}),
    Q('AF-S-02', 'science', 'The SI unit of force is the:', ['joule', 'watt', 'newton', 'pascal'], 2, 'Force is measured in newtons (N). Joule is energy, watt is power and pascal is pressure.', {}),
    Q('AF-S-03', 'science', 'Plants make their own food using sunlight in a process called:', ['respiration', 'photosynthesis', 'digestion', 'evaporation'], 1, 'Photosynthesis uses light, carbon dioxide and water to make glucose and oxygen.', {'0': 'Respiration releases energy from food; it does not make it.'}),
    Q('AF-S-04', 'science', 'A car travels 120 km in 2 hours. Its average speed is:', ['40 km/h', '60 km/h', '120 km/h', '240 km/h'], 1, 'Average speed = distance ÷ time = 120 ÷ 2 = 60 km/h.', {'3': 'Multiplying instead of dividing is a common slip.'}),
    Q('AF-R-01', 'reading', 'What is the main idea of the passage?', ['Rain is always harmful to cities', 'Collecting rain for later use has benefits but needs upkeep', 'Mosquitoes are the biggest city problem', 'Drinking water should never be treated'], 1,
      'The passage lists benefits (reuse, less groundwater pressure, less flooding) and a caution about cleaning tanks.', {}, meta={'passage': PASSAGE}),
    Q('AF-R-02', 'reading', 'According to the passage, why must tanks be cleaned regularly?', ['To make the water colder', 'To stop mosquitoes breeding', 'To stop street flooding', 'To remove rooftops'], 1, 'The passage says standing water lets mosquitoes breed.', {}, meta={'passage': PASSAGE}),
    Q('AF-R-03', 'reading', 'In “cities that adopt it”, the word “adopt” most nearly means:', ['give away', 'start using', 'stop using', 'argue about'], 1, 'Here “adopt” means to take up and begin using a method.', {}, meta={'passage': PASSAGE}),
    Q('AF-R-04', 'reading', 'Which statement is NOT supported by the passage?', ['Stored rainwater can be used in gardens', 'Harvesting can reduce street flooding', 'Harvested rainwater is always safe to drink without treatment', 'Tanks need regular cleaning'], 2,
      'The passage says water can be used for drinking only “after treatment”.', {'2': 'Students often skim past the words “after treatment”.'}, meta={'passage': PASSAGE}),
    Q('AF-D-01', 'data', 'Books read in a month: Asha 6, Bilal 9, Chitra 4, Dev 9. Who read the most?', ['Asha', 'Bilal only', 'Bilal and Dev', 'Chitra'], 2, 'Bilal and Dev both read 9, which is the highest.', {'1': 'Check for ties before choosing a single name.'}),
    Q('AF-D-02', 'data', 'For the same data (6, 9, 4, 9), the total number of books read is:', ['26', '27', '28', '29'], 2, '6 + 9 + 4 + 9 = 28.', {}),
    Q('AF-D-03', 'data', 'Test scores out of 25: 12, 15, 18, 15, 20. The mean score is:', ['15', '16', '17', '18'], 1, 'Sum = 80; 80 ÷ 5 = 16.', {'0': '15 is the median/mode here, not the mean.'}),
    Q('AF-D-04', 'data', 'The temperature rose from 18 °C at 8 am to 30 °C at 2 pm. The average rise per hour was:', ['1 °C', '2 °C', '3 °C', '12 °C'], 1, 'Rise = 12 °C over 6 hours = 2 °C per hour.', {'3': '12 °C is the total rise, not the rate.'}),
    Q('AF-X-01', 'sci_reason', 'You test whether fertiliser helps plants grow. Which should you keep the same for all plants?', ['The fertiliser used', 'Amount of water and sunlight', 'Nothing, every plant is different', 'The height measured'], 1, 'In a fair test only one thing changes (the fertiliser). Water and sunlight stay the same.', {'0': 'The fertiliser is the thing you change on purpose.'}),
    Q('AF-X-02', 'sci_reason', 'Which question can be tested by an experiment?', ['Which plant is prettier?', 'Does more sunlight make bean plants grow taller?', 'Is science fun?', 'Why do people like gardens?'], 1, 'A testable question links something you can change to something you can measure.', {}),
    Q('AF-X-03', 'sci_reason', 'In your test, ice melted faster in warm water than in cold water. The fairest conclusion is:', ['Ice always melts faster everywhere', 'In this test, warmer water melted the ice faster', 'Cold water cannot melt ice', 'Ice melts only in warm water'], 1, 'Conclusions should stay inside what the test showed.', {'0': '“Always” and “everywhere” go beyond the evidence.'}),
    Q('AF-X-04', 'sci_reason', 'Why do scientists repeat experiments?', ['To use more equipment', 'To check that results are reliable', 'To make the experiment longer', 'Because the first result is always wrong'], 1, 'Repeating shows whether a result is consistent or just chance.', {}),
])

# ---------------------------------------------------------------------------------------------------------------------------
HAB = [('planning', 'I write down what I need to study each week.', 'I usually start studying without knowing what I will cover.'),
       ('concentration', 'I can focus on one task for 20 minutes without getting distracted.', 'Small distractions make me stop studying for a long time.'),
       ('time', 'I finish my homework before the deadline.', 'I often run out of time because I start late.'),
       ('revision', 'I look at my notes again a few days after a lesson.', 'I read things only once.'),
       ('notes', 'My notes help me when I revise.', 'I find it hard to understand my own notes later.'),
       ('questions', 'I ask a teacher or friend when I do not understand something.', 'I stay quiet even when I am confused.'),
       ('mistakes', 'When I get something wrong, I check why.', 'I do not look at corrected work.'),
       ('exam_prep', 'Before a test I make a plan for what to revise.', 'I leave test preparation to the night before.'),
       ('help', 'I ask for help early rather than waiting.', 'I try to hide that I am struggling.'),
       ('consistency', 'I study at roughly the same time on most school days.', 'My study routine changes a lot from week to week.')]
A2 = dict(key='habits', number=2, group='core', title='Learning Skills and Study Habits', kind='self', minutes=10,
          purpose='Finds practical habits to build on and one or two to improve, across ten learning skills.',
          instructions='Say how much each statement is like you right now (not how you would like to be). Honest answers give better suggestions.',
          interpretation='These are your own perceptions of your habits today. They are not marks, and habits can change quickly with practice. Mentors compare them with what you actually do in the action plan.',
          accessibility='Five-point scale with text labels; no time limit.',
          questions=[q for i, (d, a, b) in enumerate(HAB, 1) for q in (LK(f'LH-{i:02d}a', d, a), LK(f'LH-{i:02d}b', d, b, reverse=True))])

# ---------------------------------------------------------------------------------------------------------------------------
A3 = dict(key='reasoning', number=3, group='core', title='Reasoning and Problem-Solving', kind='objective', minutes=20,
          purpose='Samples eight kinds of everyday reasoning. Results are reported by task type, because each type is a separate skill that grows with practice.',
          instructions='Take your time. Rough paper is fine. If you are stuck, choose the answer you think is most reasonable.',
          interpretation='Two questions per task type is a small sample: use the result to decide what to practise, not to label ability. Reasoning improves with practice.',
          accessibility='All items are text-only; shape items are described in words.',
          questions=[
    Q('RP-N-01', 'numerical', '3 pens cost ₹24. At the same rate, 7 pens cost:', ['₹48', '₹54', '₹56', '₹63'], 2, 'One pen costs ₹8, so 7 pens cost ₹56.', {'3': '₹63 comes from 3 pens = ₹27 (adding rather than scaling).'}),
    Q('RP-N-02', 'numerical', '15% of 200 is:', ['15', '20', '30', '35'], 2, '10% of 200 is 20 and 5% is 10, so 15% is 30.', {}),
    Q('RP-L-01', 'logical', 'If it rains, the match is cancelled. The match was not cancelled. What must be true?', ['It rained', 'It did not rain', 'The match was short', 'It will rain later'], 1, 'If rain always causes cancellation, no cancellation means there was no rain.', {'0': 'This reverses the rule.'}),
    Q('RP-L-02', 'logical', 'Mia stands to the left of Noor, and Noor stands to the left of Om, in a line of three. Who is in the middle?', ['Mia', 'Noor', 'Om', 'Cannot tell'], 1, 'Order left to right: Mia, Noor, Om.', {}),
    Q('RP-P-01', 'patterns', 'What comes next? 2, 6, 12, 20, 30, ?', ['38', '40', '42', '44'], 2, 'Differences are 4, 6, 8, 10, so the next difference is 12: 30 + 12 = 42.', {'1': 'Adding a constant 10 ignores that the gaps grow.'}),
    Q('RP-P-02', 'patterns', 'What comes next? 1, 4, 9, 16, 25, ?', ['30', '34', '36', '49'], 2, 'These are square numbers: 1², 2², 3², 4², 5², so next is 6² = 36.', {}),
    Q('RP-V-01', 'verbal', 'Pen is to writer as brush is to:', ['paint', 'painter', 'canvas', 'colour'], 1, 'A writer uses a pen; a painter uses a brush.', {}),
    Q('RP-V-02', 'verbal', 'Which word is the odd one out?', ['apple', 'banana', 'carrot', 'mango'], 2, 'Carrot is a vegetable; the others are fruits.', {}),
    Q('RP-S-01', 'spatial', 'How many edges does a cube have?', ['6', '8', '12', '16'], 2, 'A cube has 12 edges, 8 corners and 6 faces.', {'0': '6 is the number of faces.'}),
    Q('RP-S-02', 'spatial', 'A flat cross-shaped net of six identical squares can be folded into a:', ['pyramid', 'cube', 'cylinder', 'cone'], 1, 'Six squares make the six faces of a cube.', {}),
    Q('RP-D-01', 'data', '12 students like cricket, 8 like football and 5 like both. Everyone likes at least one. How many students are there?', ['13', '15', '20', '25'], 1, 'Add and subtract the overlap: 12 + 8 − 5 = 15.', {'2': '20 counts the five who like both twice.'}),
    Q('RP-D-02', 'data', 'Savings start at ₹100 and grow by ₹50 every week. After 4 weeks you have:', ['₹250', '₹300', '₹350', '₹400'], 1, '100 + 4 × 50 = ₹300.', {}),
    Q('RP-C-01', 'decomposition', 'You must walk 6 km to a friend’s house and arrive by 5:00 pm, walking at 4 km/h. What is the best first question to answer?', ['What will we eat?', 'How long will the walk take?', 'What colour is the house?', 'Who else is going?'], 1, 'Time = distance ÷ speed lets you work out when to leave.', {}),
    Q('RP-C-02', 'decomposition', 'Your task is to build a model of the solar system. The best way to begin is to:', ['Buy the biggest ball you can find', 'Break the task into smaller steps: list planets, sizes, materials and a schedule', 'Start painting immediately', 'Wait until someone tells you what to do'], 1, 'Splitting a big task into steps makes it manageable.', {}),
    Q('RP-E-01', 'decision', 'You have ₹200. A notebook costs ₹60, a geometry box ₹90 and a pen set ₹70. How much more do you need to buy all three?', ['₹0', '₹10', '₹20', '₹30'], 2, 'Total = 60 + 90 + 70 = ₹220, which is ₹20 more than ₹200.', {}),
    Q('RP-E-02', 'decision', 'A trip by bus costs ₹300 per student, with a 10% discount for groups of 30 or more. A train costs ₹280 per student with no discount. For 40 students, the cheaper option per student is:', ['Bus (₹270)', 'Train (₹280)', 'They cost the same', 'Cannot be decided'], 0, '10% off ₹300 is ₹270, which is less than ₹280.', {'1': 'Compare the price after the discount, not before.'}),
])

# ---------------------------------------------------------------------------------------------------------------------------
PER = [('social', 'Personality: social energy', 'I enjoy working in groups more than working alone.', 'I need quiet time alone to recharge after a busy day.'),
       ('structure', 'Personality: structure', 'I like to know the plan before I start something.', 'I like to start and work out the plan as I go.'),
       ('curiosity', 'Personality: curiosity', 'I enjoy learning about things that are not in my syllabus.', 'I prefer to stick with what I already know.'),
       ('awareness', 'Emotion: awareness', 'I can usually tell what I am feeling and why.', 'My feelings often surprise me.'),
       ('regulation', 'Emotion: regulation', 'When I am upset, I can take a break and return calmer.', 'When something goes wrong, it spoils my whole day.'),
       ('empathy', 'Emotion: empathy', 'I notice when a friend is upset even if they do not say so.', 'I find it hard to understand why others react as they do.'),
       ('analytical', 'Reasoning: analytical', 'I like to break a problem into steps before solving it.', 'I find it hard to know where to start with a complex problem.'),
       ('intuitive', 'Reasoning: intuitive', 'I often get an idea of the answer before I can explain it.', 'I do not trust my first thoughts about a problem.'),
       ('evidence', 'Reasoning: evidence', 'Before I decide, I look for facts or examples.', 'I decide quickly and rarely check.')]
A4 = dict(key='per', number=4, group='core', title='PER Exploration: Personality, Emotion and Reasoning', kind='self', minutes=10,
          purpose='A reflective exploration of how you like to work, how you notice and manage feelings, and how you approach decisions.',
          instructions='There are no right answers. Choose what is most like you today. Preferences can change as you grow.',
          interpretation='PER describes preferences and tendencies at this moment. It is not a personality type, a diagnosis or a prediction. If a result worries you, talk to your mentor, parent or school counsellor.',
          accessibility='Five-point scale; no timer; short sentences.',
          questions=[q for i, (d, lbl, a, b) in enumerate(PER, 1) for q in (LK(f'PR-{i:02d}a', d, a), LK(f'PR-{i:02d}b', d, b, reverse=True))])

# ---------------------------------------------------------------------------------------------------------------------------
DOMAINS = [('build', 'Building and making', 'I enjoy building or fixing things with my hands.', 'I like turning an idea into a working model.'),
           ('design', 'Designing and drawing', 'I enjoy drawing, designing or decorating things.', 'I notice how things look and how they could be improved.'),
           ('puzzle', 'Solving puzzles', 'I like puzzles, riddles and logic games.', 'I enjoy working out a tricky problem even if it takes time.'),
           ('tech', 'Programming and technology', 'I like learning how apps, games or computers work.', 'I would enjoy telling a computer what to do step by step.'),
           ('science', 'Experimenting with science', 'I like experiments and finding out what happens.', 'I enjoy asking “why does this happen?” about the natural world.'),
           ('people', 'Helping people', 'I enjoy helping others learn or solve their problems.', 'I like working on things that make life better for people.'),
           ('organise', 'Organising projects', 'I like planning events, schedules or team tasks.', 'I enjoy making sure everyone knows what to do and by when.'),
           ('investigate', 'Investigating how things work', 'I like taking things apart to see how they work.', 'I read or watch videos about how machines or systems operate.'),
           ('communicate', 'Communicating ideas', 'I enjoy explaining ideas through speaking, writing or presenting.', 'I like debating or persuading with good reasons.'),
           ('nature', 'Understanding nature and sustainability', 'I care about the environment and enjoy learning about nature.', 'I like ideas that save water, energy or waste.')]
A5 = dict(key='interests', number=5, group='core', title='Interests and Strengths Explorer', kind='self', minutes=12,
          purpose='Helps you notice which kinds of activities you enjoy, as possibilities to explore with hands-on projects.',
          instructions='Choose how much each statement is like you. Then answer the two short questions in your own words.',
          interpretation='These show enjoyment, which is different from skill. An interest may be new and still growing. They are possibilities to try, not career assignments.',
          accessibility='Five-point scale; two optional open questions that can be answered by voice-to-text.',
          questions=[q for i, (d, lbl, a, b) in enumerate(DOMAINS, 1) for q in (LK(f'IX-{i:02d}a', d, a), LK(f'IX-{i:02d}b', d, b))] + [
              TX('IX-T1', 'open', 'When do you lose track of time? What exactly pulls you in?'),
              TX('IX-T2', 'open', 'Describe something you made, fixed, organised or solved that you are proud of.')])

# ---------------------------------------------------------------------------------------------------------------------------
RUB_CRITERIA = [('understand', 'Understanding the problem'), ('ideas', 'Generating ideas'), ('creativity', 'Creativity'),
                ('practical', 'Practicality'), ('reasoning', 'Explanation of reasoning'), ('reflection', 'Reflection and improvement')]
RUBRIC = {'levels': {1: 'Beginning', 2: 'Developing', 3: 'Secure', 4: 'Extending'},
          'descriptors': {
              'understand': {1: 'Restates the task only', 2: 'Names the problem and one affected person', 3: 'Explains who is affected, why it matters and one cause', 4: 'Also separates causes from symptoms'},
              'ideas': {1: 'One idea', 2: 'Two ideas', 3: 'Three or more different ideas', 4: 'Several different ideas, compared against each other'},
              'creativity': {1: 'Copies a common idea', 2: 'A familiar idea with a small twist', 3: 'An original combination or approach', 4: 'An original idea that surprises and still works'},
              'practical': {1: 'Not possible with easy-to-find things', 2: 'Possible but unclear how', 3: 'Clear, doable with everyday materials', 4: 'Clear, doable, low-cost and considers safety'},
              'reasoning': {1: 'No reasons given', 2: 'A reason for the choice', 3: 'Reasons linked to the problem', 4: 'Reasons, trade-offs and evidence'},
              'reflection': {1: 'No reflection', 2: 'Says what went well or badly', 3: 'Says what to change and why', 4: 'Plans a second test of the improvement'}}}
A6 = dict(key='creativity', number=6, group='core', title='Creativity and Practical Design Challenge', kind='rubric', minutes=40,
          purpose='A practical challenge: design a simple solution to a real problem. Your thinking process is assessed with a transparent rubric.',
          instructions='Pick one challenge and answer each step in your own words. Add a sketch on paper if you like (you can show your mentor). Many different solutions are valid. Cheap and simple ideas score just as well as expensive ones.',
          interpretation='The rubric looks at your process, not at how fancy the materials are. A mentor rates each criterion from 1 to 4 and writes feedback. Your own self-rating is shown next to it for reflection.',
          accessibility='Responses can be typed, dictated or described aloud to a mentor. No special equipment is needed.',
          meta={'rubric': RUBRIC, 'criteria': RUB_CRITERIA},
          questions=[
    Q('CD-01', 'challenge', 'Choose one challenge', ['Reduce waste in a classroom', 'Make a school bag easier and safer to carry', 'Design a simple way to save water at home or school'], None, '', qtype='choice',
      meta={'tags_hint': 'choice'}),
    TX('CD-02', 'understand', 'Step 1. In your own words: what is the problem, who is affected, and why does it matter?'),
    TX('CD-03', 'ideas', 'Step 2. List at least three different ideas (they can be rough or silly).'),
    TX('CD-04', 'creativity', 'Step 3. Choose one idea. Describe how it works, and what makes it different from what already exists.'),
    TX('CD-05', 'practical', 'Step 4. What would you need to build or try it? How could you test it using things you can easily find?'),
    TX('CD-06', 'reasoning', 'Step 5. Why did you choose this idea over the others? What are its limits?'),
    TX('CD-07', 'reflection', 'Step 6. If you tried it and it only half worked, what would you change?'),
    LK('CD-S1', 'self_rubric', 'I understood the problem well before choosing an idea.'),
    LK('CD-S2', 'self_rubric', 'I tried several ideas before choosing one.'),
    LK('CD-S3', 'self_rubric', 'My idea can really be tried with everyday materials.'),
])

# ---------------------------------------------------------------------------------------------------------------------------
AI_ANS = ('AI answer to “Tell me about the Great Wall of China”: “The Great Wall of China is easily visible from space with the naked eye and is over 50,000 km long. '
          'It was built entirely in the 20th century by a single emperor.”')
A7 = dict(key='ai_literacy', number=7, group='core', title='Digital and Responsible AI Literacy', kind='objective', minutes=15,
          purpose='Checks basic digital safety, how to judge information, and how to check an AI answer before trusting it.',
          instructions='Answer the questions, then do the short practical task at the end.',
          interpretation='Good digital habits are learnable. This shows which habits to practise. It does not judge how much technology you can access at home.',
          accessibility='Text-only; the practical task can be done aloud with a mentor.',
          questions=[
    Q('AI-01', 'ai_use', 'You use an AI chatbot for homework. Which is the best practice?', ['Copy its answer exactly', 'Use it to help understand, then check with your textbook and write in your own words', 'Ask it to take the test for you', 'Believe it because it sounds confident'], 1, 'AI can explain and suggest, but it can be wrong. You stay responsible for checking and for your own work.', {'3': 'Confident wording does not mean correct.'}),
    Q('AI-02', 'safety', 'Which of these should you NOT share with an online chatbot or stranger?', ['Your favourite colour', 'Your home address and phone number', 'The name of your favourite book', 'A school subject you like'], 1, 'Personal contact and location details can be misused.', {}),
    Q('AI-03', 'evaluate', 'An AI gives a surprising statistic with no source. What is the best next step?', ['Share it with friends', 'Look for the original source or another reliable source', 'Assume it is right', 'Assume it is wrong without checking'], 1, 'Trace claims to reliable sources before using them.', {}),
    Q('AI-04', 'evaluate', 'A web page has a shocking headline. What should you check first?', ['How many people liked it', 'Who published it and whether other reliable sources report it', 'Its colours', 'Whether it uses capital letters'], 1, 'Source and corroboration matter more than popularity or style.', {}),
    Q('AI-05', 'safety', 'Which password is strongest?', ['password123', 'your name and birth year', 'a long, unique phrase you use nowhere else', 'the same one as your email'], 2, 'Long, unique passwords resist guessing, and reuse spreads one leak to many accounts.', {}),
    Q('AI-06', 'safety', 'A message says “You won a free phone! Log in here to claim.” You should:', ['Log in quickly', 'Not click, and tell a trusted adult', 'Forward it to all friends', 'Reply with your password'], 1, 'Prize messages that ask for logins are usually scams.', {}),
    Q('AI-07', 'verify', AI_ANS + ' Which claims should you check before using this answer? (choose all that apply)', ['That it is visible from space with the naked eye', 'The stated length of 50,000 km', 'That it was built entirely in the 20th century by one emperor', 'That the answer has two sentences'], [0, 1, 2],
      'The visibility claim, the length figure and the construction history are all specific, checkable claims that need a reliable source. How many sentences there are does not matter.', {}, qtype='multi'),
    TX('AI-08', 'verify', 'Practical: how would you check one of those claims? Name the source you would use and what you would look for.'),
])

# ---------------------------------------------------------------------------------------------------------------------------
CC = [('listening', 'I listen to the end before I answer.', 'I often interrupt people when I think I know what they will say.'),
      ('explaining', 'I can explain an idea in a way my friends understand.', 'People often ask me to repeat my explanations.'),
      ('asking', 'I am comfortable asking questions in class or in a group.', 'I worry that my questions will sound silly.'),
      ('teamwork', 'In group work I do my part and help others do theirs.', 'In group work I prefer to leave the work to others.'),
      ('feedback', 'I can take feedback and use it to improve.', 'When someone corrects me, I get defensive.'),
      ('disagree', 'I can disagree politely and listen to the other side.', 'Disagreements make me want to give up or argue harder.')]
A8 = dict(key='communication', number=8, group='core', title='Communication and Collaboration', kind='mixed', minutes=12,
          purpose='Explores listening, explaining, asking questions, teamwork, feedback and handling disagreements.',
          instructions='First say how much each statement is like you. Then choose the best response in two short situations.',
          interpretation='The agreement items are self-perceptions. The two situations check judgement, not personality. Mentors also watch real group activities for evidence.',
          accessibility='Five-point scale plus two scenario questions; no timer.',
          questions=[q for i, (d, a, b) in enumerate(CC, 1) for q in (LK(f'CC-{i:02d}a', d, a), LK(f'CC-{i:02d}b', d, b, reverse=True))] + [
              Q('CC-S1', 'scenario', 'In a group project a teammate disagrees with your idea. The best response is to:', ['Insist your idea is best', 'Ask them to explain their reasoning and look for a combined solution', 'Stay silent and do it your way later', 'Tell the teacher immediately'], 1, 'Asking for reasons and looking for a combined answer solves the problem and keeps the team working.', {}),
              Q('CC-S2', 'scenario', 'A teacher says your presentation was hard to follow. A helpful reaction is to:', ['Decide you are bad at presenting', 'Ask which part was unclear and try again with a simpler structure', 'Say the teacher is unfair', 'Skip future presentations'], 1, 'Specific questions turn feedback into a plan.', {})])

# ---------------------------------------------------------------------------------------------------------------------------
SM = [('Goals are realistic', 'I set goals that I can really finish in the time I have.'),
      ('Steps', 'I break a big goal into smaller steps.'),
      ('Tracking', 'I keep track of what I have finished.'),
      ('Setbacks', 'When I miss a goal, I work out what to change and try again.'),
      ('Start', 'I start tasks on time without needing reminders.'),
      ('Priorities', 'I can decide what is most important to do first.'),
      ('Reflection', 'I think about what I learned at the end of each week.'),
      ('Help', 'I tell my mentor or parent when a goal is not going well.'),
      ('Balance', 'I make time for rest and hobbies as well as study.'),
      ('Ownership', 'I feel my goals are really mine.')]
A9 = dict(key='selfmgmt', number=9, group='core', title='Self-Management and Goal-Setting', kind='mixed', minutes=10,
          purpose='Helps you set realistic goals, break them into actions and learn from setbacks. Follow-through is measured from your real action plan over time, not only from these answers.',
          instructions='Say how true each statement is. Then write one goal for the next 30 days and three small steps. Your mentor will help turn it into an action plan.',
          interpretation='Your answers here are self-reports. The portal also shows how many agreed actions you actually completed, so you and your mentor can see the real pattern and adjust the plan together.',
          accessibility='Five-point scale; one open task.',
          questions=[LK(f'SM-{i:02d}', 'selfmgmt', t) for i, (_, t) in enumerate(SM, 1)] + [
              TX('SM-T1', 'goal', 'My goal for the next 30 days is…'),
              TX('SM-T2', 'goal', 'My three small steps are…')])

# ---------------------------------------------------------------------------------------------------------------------------
INTEREST_CHOICES = ['Building and making', 'Designing and drawing', 'Solving puzzles', 'Programming and technology', 'Experimenting with science',
                    'Helping people', 'Organising projects', 'Investigating how things work', 'Communicating ideas', 'Nature and sustainability']
A10 = dict(key='alignment', number=10, group='core', title='Parent–Student Alignment', kind='self', minutes=10,
           purpose='The student and a parent each answer the same questions separately, so the family can see where views match and where they differ, as topics for a friendly conversation.',
           instructions='Answer for yourself (students) or about your child (parents). Do not discuss answers until both are finished.',
           interpretation='Differences are not mistakes. They show something to talk about. Neither view is “wrong”, and nothing here is used to judge the student or the parent.',
           accessibility='Five-point scale, pick-three lists and open text; parents can use a phone.',
           questions=[
    Q('PS-01', 'interests', 'Pick the three activities the student enjoys most. (Students: pick yours. Parents: pick what you think your child enjoys most.)', INTEREST_CHOICES, None, qtype='multi', meta={'pick': 3}),
    Q('PS-02', 'strengths', 'Pick the three things the student is best at right now. (Students: pick yours. Parents: pick what you see.)', INTEREST_CHOICES, None, qtype='multi', meta={'pick': 3}),
    LK('PS-03', 'confidence', 'I feel confident about the student’s choices of subjects in the next two years.'),
    LK('PS-04', 'pressure', 'Talking about studies and the future at home feels comfortable.'),
    LK('PS-05', 'support', 'The student gets the support they need to study well.'),
    LK('PS-06', 'awareness', 'I understand how engineering admissions work in India.'),
    TX('PS-T1', 'expectations', 'What do you hope the student will achieve or learn in the next year?'),
    TX('PS-T2', 'concerns', 'What worries you most about the next year?'),
    TX('PS-T3', 'possibilities', 'What possibilities for the future are you excited about?'),
])

CORE = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10]
