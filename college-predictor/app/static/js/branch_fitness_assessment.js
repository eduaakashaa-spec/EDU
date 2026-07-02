
const QUESTIONS = [{"id":1,"cat":"Interest","catClass":"cat-interest","text":"Which of these activities would you happily spend a free Saturday on?","ctx":"Choose what you would actually do \u2014 not what sounds impressive.","opts":[{"t":"Building an app, automating something, or playing with code/AI tools","s":{"cse":3,"ece":1}},{"t":"Opening up a gadget to see how the circuit works, fixing electronics","s":{"ece":3,"eee":2}},{"t":"Working on a bike/car engine, 3D printing, building physical things","s":{"mech":3,"civil":1}},{"t":"Watching videos on skyscrapers, bridges, city planning, architecture","s":{"civil":3,"mech":1}}]},{"id":2,"cat":"Interest","catClass":"cat-interest","text":"When you watch tech or science content online, what topics do you actually finish watching?","ctx":"Your watch history is more honest than your stated interests.","opts":[{"t":"AI, coding, startups, software product breakdowns","s":{"cse":3}},{"t":"Chip making, semiconductors, robotics, drones, space tech","s":{"ece":3,"eee":1,"mech":1}},{"t":"EVs, batteries, power grids, renewable energy","s":{"eee":3,"chem":1,"mech":1}},{"t":"Mega constructions, manufacturing processes, how things are made","s":{"civil":2,"mech":2,"chem":1}}]},{"id":3,"cat":"Interest","catClass":"cat-interest","text":"In school physics, which unit felt most natural to you?","ctx":"Branch curricula build directly on these foundations.","opts":[{"t":"Electricity, magnetism, and circuits","s":{"eee":3,"ece":2}},{"t":"Mechanics \u2014 forces, motion, rotation","s":{"mech":3,"civil":2}},{"t":"Honestly, I preferred maths/logic over physics","s":{"cse":3}},{"t":"Thermodynamics and heat","s":{"mech":2,"chem":2}}]},{"id":4,"cat":"Interest","catClass":"cat-interest","text":"Chemistry \u2014 be honest, how do you feel about it?","ctx":"Chemical engineering is heavily chemistry-based; other branches barely touch it after Year 1.","opts":[{"t":"I genuinely enjoy chemistry, especially physical/organic chemistry","s":{"chem":3}},{"t":"It is fine \u2014 I can do it but would not choose it","s":{"chem":1}},{"t":"I tolerate it for exams only","s":{}},{"t":"I actively dislike chemistry","s":{"cse":1}}]},{"id":5,"cat":"Interest","catClass":"cat-interest","text":"If you had to do a 2-month internship tomorrow, which would you pick?","ctx":"","opts":[{"t":"Software company \u2014 writing real code with a dev team","s":{"cse":3}},{"t":"Electronics lab \u2014 testing circuit boards, embedded systems","s":{"ece":3,"eee":1}},{"t":"Manufacturing plant \u2014 production lines, machines, quality control","s":{"mech":3,"chem":1}},{"t":"Construction site / infrastructure project office","s":{"civil":3}}]},{"id":6,"cat":"Interest","catClass":"cat-interest","text":"What kind of problems do you find satisfying to solve?","ctx":"","opts":[{"t":"Logic puzzles, algorithms, step-by-step debugging","s":{"cse":3}},{"t":"Physical/visual problems \u2014 why is this thing not working mechanically?","s":{"mech":2,"ece":1,"eee":1}},{"t":"Optimisation \u2014 making a process faster, cheaper, more efficient","s":{"chem":2,"mech":1,"cse":1}},{"t":"Design problems \u2014 planning something that has to work in the real world","s":{"civil":2,"mech":1,"ece":1}}]},{"id":7,"cat":"Interest","catClass":"cat-interest","text":"Do you enjoy coding \u2014 based on actual experience, not assumption?","ctx":"This is the single most decision-relevant interest question for CSE aspirants.","opts":[{"t":"Yes \u2014 I have written real code (projects, courses, competitive programming) and enjoy it","s":{"cse":4}},{"t":"I have tried basics (school Python/Scratch) and found it okay","s":{"cse":2,"ece":1}},{"t":"I have never really coded but assume I will like it","s":{"ece":1},"flag":"Considering CSE without coding experience \u2014 recommend trying a basic course before committing"},{"t":"I have tried coding and did not enjoy it","s":{"mech":1,"civil":1,"eee":1},"flag":"Has tried and disliked coding \u2014 CSE choice would be high-risk if being considered"}]},{"id":8,"cat":"Interest","catClass":"cat-interest","text":"Which future work environment appeals most?","ctx":"","opts":[{"t":"Tech office / remote \u2014 screens, code, product teams","s":{"cse":3,"ece":1}},{"t":"Lab + office mix \u2014 designing and testing hardware","s":{"ece":3,"eee":2}},{"t":"Plant / field + office \u2014 real machines, site visits, operations","s":{"mech":2,"chem":2,"civil":2}},{"t":"Large infrastructure projects \u2014 site offices, government/PSU settings","s":{"civil":3,"eee":1}}]},{"id":9,"cat":"Aptitude","catClass":"cat-aptitude","text":"How are your maths fundamentals \u2014 calculus, algebra, probability?","ctx":"All branches need maths, but CSE/ECE lean on discrete maths and signal processing; Civil/Mech on applied calculus.","opts":[{"t":"Strong \u2014 consistently among my best subjects, enjoy problem solving","s":{"cse":2,"ece":2,"eee":1}},{"t":"Good \u2014 solid scores with effort","s":{"cse":1,"ece":1,"mech":1,"civil":1,"eee":1,"chem":1}},{"t":"Average \u2014 I manage but it takes real work","s":{"civil":1,"mech":1}},{"t":"Weak \u2014 maths is my biggest struggle","s":{},"flag":"Weak maths foundation reported \u2014 all engineering branches will be challenging; foundational support needed in Year 1"}]},{"id":10,"cat":"Aptitude","catClass":"cat-aptitude","text":"When learning something new, what works best for you?","ctx":"","opts":[{"t":"Abstract first \u2014 give me the theory/logic, I can apply it later","s":{"cse":2,"ece":1}},{"t":"Hands-on first \u2014 let me touch/build it, then explain theory","s":{"mech":2,"civil":1,"eee":1}},{"t":"Visual \u2014 diagrams, simulations, seeing the system work","s":{"ece":1,"civil":1,"chem":1,"eee":1}},{"t":"Step-by-step procedures and worked examples","s":{"chem":1,"civil":1,"mech":1}}]},{"id":11,"cat":"Aptitude","catClass":"cat-aptitude","text":"How do you handle long, multi-step problems that take 30+ minutes to solve?","ctx":"","opts":[{"t":"I enjoy them \u2014 sustained problem-solving is my strength","s":{"cse":2,"ece":1,"chem":1}},{"t":"I can do them but prefer shorter, varied problems","s":{"mech":1,"eee":1,"civil":1}},{"t":"I lose focus \u2014 I prefer practical tasks over long abstract problems","s":{"mech":1,"civil":1}},{"t":"Depends entirely on whether the topic interests me","s":{}}]},{"id":12,"cat":"Aptitude","catClass":"cat-aptitude","text":"3D visualisation \u2014 rotating objects in your mind, reading engineering drawings. How natural is this for you?","ctx":"Critical for Mechanical, Civil, and parts of ECE (chip layout). Less critical for CSE.","opts":[{"t":"Very natural \u2014 I can mentally rotate and visualise structures easily","s":{"mech":3,"civil":3,"ece":1}},{"t":"Decent \u2014 I can do it with some effort","s":{"mech":1,"civil":1,"ece":1,"eee":1}},{"t":"Weak \u2014 I struggle with spatial visualisation","s":{"cse":2,"chem":1}},{"t":"I have never tested this","s":{}}]},{"id":13,"cat":"Aptitude","catClass":"cat-aptitude","text":"How patient are you with precision and detail \u2014 measurements, tolerances, careful procedures?","ctx":"","opts":[{"t":"Very \u2014 I naturally double-check and like precision","s":{"ece":2,"chem":2,"civil":1}},{"t":"Reasonably \u2014 I care about correctness but move fast","s":{"cse":2,"mech":1,"eee":1}},{"t":"I prefer big-picture thinking \u2014 details bore me","s":{"cse":1},"flag":"Self-reports low detail-orientation \u2014 relevant for hardware/chemical branches"},{"t":"Depends on the task","s":{}}]},{"id":14,"cat":"Aptitude","catClass":"cat-aptitude","text":"How comfortable are you with continuous learning \u2014 fields where what you learn today may be outdated in 5 years?","ctx":"CSE/AI evolves fastest; Civil/Mechanical fundamentals stay stable for decades.","opts":[{"t":"I love it \u2014 constantly learning new things energises me","s":{"cse":3,"ece":1}},{"t":"I am fine with it if the field interests me","s":{"cse":1,"ece":1,"eee":1}},{"t":"I prefer mastering stable fundamentals deeply over chasing new trends","s":{"civil":2,"mech":2,"chem":1}},{"t":"Have not thought about this","s":{}}]},{"id":15,"cat":"Knowledge","catClass":"cat-knowledge","text":"Can you name 3 specific job roles that a Mechanical engineer can hold \u2014 beyond just the title mechanical engineer?","ctx":"This tests real branch knowledge vs name familiarity.","opts":[{"t":"Yes easily \u2014 design engineer, thermal engineer, automotive R&D, robotics, HVAC, production","s":{"mech":1,"_know":3}},{"t":"I can name 1\u20132 with effort","s":{"_know":1}},{"t":"Not really \u2014 I know the branch name but not the actual roles","s":{"_know":0}},{"t":"I know roles for the branch I am interested in, just not Mechanical","s":{"_know":2}}]},{"id":16,"cat":"Knowledge","catClass":"cat-knowledge","text":"What do you think a CSE graduate actually studies in college?","ctx":"","opts":[{"t":"Data structures, algorithms, OS, databases, networks, theory of computation \u2014 plus programming","s":{"cse":1,"_know":3}},{"t":"Mostly programming languages and app development","s":{"_know":1},"flag":"Believes CSE is only programming languages \u2014 needs curriculum awareness before choosing"},{"t":"AI and machine learning mainly","s":{"_know":0},"flag":"Believes CSE is mainly AI/ML \u2014 actual curriculum is much broader and more theoretical"},{"t":"Honestly not sure of the specifics","s":{"_know":0}}]},{"id":17,"cat":"Knowledge","catClass":"cat-knowledge","text":"Do you know the difference between ECE and EEE as degrees?","ctx":"","opts":[{"t":"Yes \u2014 ECE focuses on electronics/communication/signal systems; EEE on power systems, machines, electrical infrastructure","s":{"ece":1,"eee":1,"_know":3}},{"t":"Roughly \u2014 one is more electronics, one is more electrical","s":{"_know":2}},{"t":"I thought they were basically the same","s":{"_know":0}},{"t":"Never looked into either","s":{"_know":0}}]},{"id":18,"cat":"Knowledge","catClass":"cat-knowledge","text":"Which statement about engineering careers is most accurate?","ctx":"Tests realistic understanding of the engineering job market.","opts":[{"t":"Any branch can lead to software jobs, but core branch jobs require that specific branch","s":{"_know":3}},{"t":"Only CSE students get software jobs","s":{"_know":0}},{"t":"Branch determines your career permanently \u2014 no switching later","s":{"_know":0}},{"t":"All branches have identical career options","s":{"_know":0}}]},{"id":25,"cat":"Skill Check","catClass":"cat-skill","text":"You need to find whether any name appears twice in a list of 500 names. What's your natural approach?","ctx":"Tests algorithmic thinking \u2014 a core skill for CSE and ECE.","opts":[{"t":"Sort the list or use a tracking set, then scan once \u2014 efficient and systematic","sk":{"logic":3}},{"t":"Compare every name against every other name, methodically","sk":{"logic":2}},{"t":"Eyeball it or use a spreadsheet's built-in duplicate finder","sk":{"logic":1}},{"t":"I honestly wouldn't know where to start","sk":{"logic":0}}]},{"id":26,"cat":"Skill Check","catClass":"cat-skill","text":"A problem asks you to translate a word description into an equation, then solve it using calculus. How do you feel?","ctx":"Tests mathematical ability \u2014 critical for CSE, ECE, and EEE.","opts":[{"t":"Confident \u2014 I can model it and solve, calculus included","sk":{"math":3}},{"t":"I can usually set it up, but solving takes real effort","sk":{"math":2}},{"t":"I struggle to translate words into equations","sk":{"math":1}},{"t":"Advanced maths is a genuine weakness for me","sk":{"math":0}}]},{"id":27,"cat":"Skill Check","catClass":"cat-skill","text":"Look at this code: for i in range(5): print(i). What does it do \u2014 and how comfortable are you with code like this?","ctx":"Tests programming aptitude \u2014 the #1 skill for CSE.","opts":[{"t":"Prints 0 to 4 \u2014 and I write code like this comfortably","sk":{"coding":3}},{"t":"It loops and prints something \u2014 I know basics but I'm not fluent","sk":{"coding":2}},{"t":"I'd have to guess \u2014 very little coding exposure","sk":{"coding":1}},{"t":"I have never seen code like this before","sk":{"coding":0}}]},{"id":28,"cat":"Skill Check","catClass":"cat-skill","text":"Imagine folding a flat cross-shaped sheet into a cube. Can you mentally 'see' which faces end up opposite each other?","ctx":"Tests spatial visualization \u2014 essential for Mechanical and Civil.","opts":[{"t":"Easily \u2014 I can mentally fold and rotate 3D shapes","sk":{"spatial":3}},{"t":"With some effort, or by sketching it out","sk":{"spatial":2}},{"t":"I find this kind of visualization quite hard","sk":{"spatial":1}},{"t":"I can't really picture this at all","sk":{"spatial":0}}]},{"id":29,"cat":"Skill Check","catClass":"cat-skill","text":"Two bulbs are wired in a series circuit. If one bulb burns out, what happens to the other?","ctx":"Tests circuit reasoning \u2014 core to ECE and EEE.","opts":[{"t":"The other goes off too \u2014 a series break stops the whole loop. I reason about circuits comfortably","sk":{"circuits":3}},{"t":"I think it goes off \u2014 I understand basic circuits","sk":{"circuits":2}},{"t":"I'm guessing \u2014 circuits aren't my strength","sk":{"circuits":1}},{"t":"I don't really understand how circuits work","sk":{"circuits":0}}]},{"id":30,"cat":"Skill Check","catClass":"cat-skill","text":"Problems involving forces, motion, energy, or heat transfer \u2014 how do you handle them?","ctx":"Tests applied physics \u2014 critical for Mechanical, Civil, and Chemical.","opts":[{"t":"Confidently \u2014 mechanics and thermodynamics are strengths of mine","sk":{"physics":3}},{"t":"Reasonably well, with some revision","sk":{"physics":2}},{"t":"I find applied physics challenging","sk":{"physics":1}},{"t":"Physics problem-solving is a real weakness for me","sk":{"physics":0}}]},{"id":19,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"Whose idea is your current branch preference \u2014 really?","ctx":"Confidential. Your counselor uses this to understand the full picture \u2014 there is no wrong answer.","opts":[{"t":"Fully mine \u2014 I researched and chose it","s":{},"h":"Branch preference is self-driven"},{"t":"Mine, but heavily shaped by what parents/family expect","s":{},"h":"Preference partially shaped by family expectations","flag":"Family influence on branch preference \u2014 verify genuine interest in counseling session"},{"t":"Mostly my parents choice \u2014 I went along with it","s":{},"h":"Branch is primarily parents choice","flag":"IMPORTANT: Branch is parent-driven, not student-driven \u2014 high disengagement risk; needs dedicated conversation"},{"t":"I do not have a real preference yet","s":{},"h":"No strong branch preference formed yet"}]},{"id":20,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"Is there a field outside engineering you secretly wish you could pursue?","ctx":"Confidential. This matters more than you think for branch selection.","opts":[{"t":"No \u2014 engineering is genuinely my path","s":{},"h":"Committed to engineering"},{"t":"Yes \u2014 design/arts/media, but engineering is the practical choice","s":{},"h":"Latent interest in design/arts/media","flag":"Hidden interest in creative fields \u2014 consider branches with design elements (Industrial Design, HCI within CSE, Architecture)"},{"t":"Yes \u2014 medicine/biology, but the path did not work out","s":{},"h":"Latent interest in medicine/biology","flag":"Hidden bio/medicine interest \u2014 Biotech, Biomedical, or Chemical Engineering may bridge this"},{"t":"Yes \u2014 business/finance/entrepreneurship","s":{},"h":"Latent interest in business/entrepreneurship","flag":"Business inclination \u2014 branch choice should preserve MBA/startup optionality"}]},{"id":21,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"What honestly worries you most about engineering college?","ctx":"","opts":[{"t":"Whether I can handle the academic pressure","s":{},"h":"Primary worry: academic pressure","flag":"Academic pressure anxiety \u2014 match college environment carefully"},{"t":"Choosing the wrong branch and regretting it","s":{},"h":"Primary worry: wrong branch regret"},{"t":"Being away from home/family for 4 years","s":{},"h":"Primary worry: homesickness/family separation","flag":"Separation anxiety signal \u2014 proximity to relatives or direct flights home worth factoring in college choice"},{"t":"Honestly, nothing major \u2014 I am ready","s":{},"h":"No major worries reported"}]},{"id":22,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"If your JEE rank only gets your preferred branch at a low-ranked college, what would YOU choose?","ctx":"Confidential \u2014 answer for yourself, not what your family would say.","opts":[{"t":"Take the branch at the lower college \u2014 branch matters more to me","s":{},"h":"Student prioritises branch over college brand"},{"t":"Take a better college with different branch \u2014 environment matters more","s":{},"h":"Student prioritises college brand over branch"},{"t":"Honestly torn \u2014 I do not know","s":{},"h":"Undecided on brand vs branch trade-off"},{"t":"My family would decide this, not me","s":{},"h":"Defers brand-vs-branch decision to family","flag":"Student defers major trade-off decisions entirely to family \u2014 agency conversation needed"}]},{"id":23,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"How much do you actually know about living in India for 4 years?","ctx":"","opts":[{"t":"A lot \u2014 I visit regularly, speak the language, and know what to expect","s":{},"h":"High India familiarity"},{"t":"Some \u2014 family trips, but college life will be different","s":{},"h":"Moderate India familiarity"},{"t":"Very little \u2014 I have grown up entirely abroad","s":{},"h":"Low India familiarity","flag":"Low India exposure \u2014 culture/safety readiness preparation strongly recommended before departure"},{"t":"I am actually nervous about this part","s":{},"h":"Anxious about India transition","flag":"Student expressed anxiety about India transition \u2014 needs transition support plan"}]},{"id":24,"cat":"Real Talk","catClass":"cat-hidden","hidden":true,"text":"Final honest question: on a gut level, how excited are you about becoming an engineer?","ctx":"","opts":[{"t":"Genuinely excited \u2014 I can see myself loving this","s":{},"h":"High intrinsic motivation for engineering"},{"t":"Positive but nervous \u2014 excited with normal doubts","s":{},"h":"Positive with normal apprehension"},{"t":"Neutral \u2014 it is a sensible path, not a passion","s":{},"h":"Pragmatic, not passionate about engineering","flag":"Neutral motivation \u2014 branch selection becomes MORE critical; pick highest-engagement branch"},{"t":"Honestly, low \u2014 I am doing this because it is expected","s":{},"h":"Low intrinsic motivation \u2014 externally driven","flag":"CRITICAL: Low motivation, externally-driven choice \u2014 full counseling conversation required before any decision"}]}];
const RANKS_JSON = {"ciwg":[{"i":"NIT Calicut","p":"Architecture","o":711,"c":1071,"b":"arch"},{"i":"SPA Delhi","p":"Architecture","o":798,"c":1132,"b":"arch"},{"i":"NIT, Tiruchirappalli","p":"Architecture","o":1384,"c":1384,"b":"arch"},{"i":"SPA: Vijayawada","p":"Architecture","o":1642,"c":3514,"b":"arch"},{"i":"SPA Delhi","p":"Planning","o":2466,"c":2466,"b":"arch"},{"i":"SPA, Bhopal","p":"Architecture","o":2752,"c":5223,"b":"arch"},{"i":"VNIT, Nagpur","p":"Architecture","o":5225,"c":6816,"b":"arch"},{"i":"NIT, Tiruchirappalli","p":"Computer Science and Engineering","o":5686,"c":16522,"b":"cse"},{"i":"SPA: Vijayawada","p":"Planning","o":7689,"c":7689,"b":"arch"},{"i":"NIT Hamirpur","p":"Architecture","o":8521,"c":10999,"b":"arch"},{"i":"Malaviya NIT Jaipur","p":"Architecture and Planning","o":11084,"c":11084,"b":"arch"},{"i":"MA NIT Bhopal","p":"Architecture","o":12004,"c":22175,"b":"arch"},{"i":"NIT, Warangal","p":"Computer Science and Engineering","o":13108,"c":38176,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Computer Science and Engineering","o":14980,"c":22657,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Electronics and Communication Engineering","o":16467,"c":33868,"b":"ece"},{"i":"NIT, Tiruchirappalli","p":"Mechanical Engineering","o":18126,"c":77267,"b":"mech"},{"i":"NIT Karnataka, Surathkal","p":"Information Technology","o":22657,"c":46502,"b":"cse"},{"i":"NIT Raipur","p":"Architecture","o":26086,"c":26086,"b":"arch"},{"i":"NIT, Tiruchirappalli","p":"Electrical and Electronics Engineering","o":26928,"c":78969,"b":"eee"},{"i":"NIT Karnataka, Surathkal","p":"Artificial Intelligence","o":28039,"c":43849,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Electronics and Communication Engineering","o":29028,"c":54969,"b":"ece"},{"i":"DTU, Delhi","p":"Computer Science and Engineering","o":30015,"c":103543,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Computational and Data Science","o":33610,"c":55280,"b":"cse"},{"i":"NIT, Warangal","p":"Computer Science and Engineering ( Artificial Intelligence & Data Science)","o":38327,"c":47457,"b":"cse"},{"i":"NIT Calicut","p":"Computer Science and Engineering","o":38493,"c":77929,"b":"cse"},{"i":"NIT, Warangal","p":"Civil Engineering","o":44759,"c":576584,"b":"civil"},{"i":"NIT, Rourkela","p":"Computer Science and Engineering","o":48810,"c":102778,"b":"cse"},{"i":"Malaviya NIT Jaipur","p":"Electronics and Communication Engineering","o":50164,"c":338394,"b":"ece"},{"i":"IIIT, Allahabad","p":"Information Technology","o":50167,"c":225013,"b":"cse"},{"i":"NIT, Warangal","p":"Mathematics and Computing","o":53982,"c":101392,"b":"cse"},{"i":"NIT, Warangal","p":"Electronics and Communication Engineering","o":55280,"c":90245,"b":"ece"},{"i":"NIT, Warangal","p":"Electronics and Communication Engineering (VLSI Design and Technology)","o":58297,"c":101537,"b":"ece"},{"i":"NIT Calicut","p":"Electronics and Communication Engineering","o":60443,"c":113231,"b":"ece"},{"i":"SV NIT, Surat","p":"Computer Science and Engineering","o":61924,"c":265144,"b":"cse"},{"i":"DTU, Delhi","p":"Electronics and Communication Engineering","o":65675,"c":191826,"b":"ece"},{"i":"Malaviya NIT Jaipur","p":"Computer Science and Engineering","o":69664,"c":233197,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Electrical and Electronics Engineering","o":75523,"c":110992,"b":"eee"},{"i":"MN NIT Allahabad","p":"Computer Science and Engineering","o":80333,"c":256738,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Chemical Engineering","o":84107,"c":141585,"b":"chem"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering (Artificial Intelligence)","o":88593,"c":202143,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Mechanical Engineering","o":89988,"c":128896,"b":"mech"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering with specialization in Artificial Intelligence and Data Science","o":91519,"c":202105,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Chemical Engineering","o":92001,"c":190350,"b":"chem"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering","o":93469,"c":319864,"b":"cse"},{"i":"IIIT, Allahabad","p":"Information Technology-Business Informatics","o":96740,"c":193900,"b":"cse"},{"i":"Malaviya NIT Jaipur","p":"Artificial Intelligence and Data Engineering","o":104275,"c":261513,"b":"cse"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering","o":105334,"c":250703,"b":"cse"},{"i":"NIT Calicut","p":"Chemical Engineering","o":109378,"c":195952,"b":"chem"},{"i":"NIT Calicut","p":"Electrical and Electronics Engineering","o":109772,"c":162162,"b":"eee"},{"i":"DTU, Delhi","p":"Information Technology","o":110693,"c":141512,"b":"cse"},{"i":"NIT, Warangal","p":"Electrical and Electronics Engineering","o":110992,"c":156706,"b":"eee"},{"i":"NIT Puducherry","p":"Computer Science and Engineering","o":113367,"c":214464,"b":"cse"},{"i":"NIT, Rourkela","p":"Artificial Intelligence","o":115049,"c":118955,"b":"cse"},{"i":"DTU, Delhi","p":"Mathematics and Computing","o":116009,"c":215669,"b":"cse"},{"i":"NIT, Rourkela","p":"Electronics and Communication Engineering","o":117029,"c":139686,"b":"ece"},{"i":"NIT, Jalandhar","p":"Computer Science and Engineering","o":117359,"c":497878,"b":"cse"},{"i":"DTU, Delhi","p":"Software Engineering","o":117535,"c":156029,"b":"other"},{"i":"NIT Durgapur","p":"Computer Science and Engineering","o":119143,"c":194796,"b":"cse"},{"i":"VNIT, Nagpur","p":"Computer Science and Engineering","o":121440,"c":147009,"b":"cse"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering with specialization in Cyber Security","o":123191,"c":313124,"b":"cse"},{"i":"NIT Delhi","p":"Computer Science and Engineering","o":124703,"c":245423,"b":"cse"},{"i":"IIIT, Allahabad","p":"Electronics and Communication Engineering","o":127370,"c":291546,"b":"ece"},{"i":"NIT Calicut","p":"Civil Engineering","o":130865,"c":363502,"b":"civil"},{"i":"NIT Delhi","p":"Electrical Engineering","o":131837,"c":289975,"b":"eee"},{"i":"NIT, Tiruchirappalli","p":"Civil Engineering","o":134053,"c":333855,"b":"civil"},{"i":"NIT, Tiruchirappalli","p":"Instrumentation and Control Engineering","o":142079,"c":178544,"b":"other"},{"i":"NIT, Warangal","p":"Mechanical Engineering","o":142600,"c":148054,"b":"mech"},{"i":"NIT Calicut","p":"Biotechnology","o":145015,"c":214118,"b":"chem"},{"i":"NIT Delhi","p":"Aerospace Engineering","o":146590,"c":153753,"b":"other"},{"i":"Malaviya NIT Jaipur","p":"Electrical Engineering","o":146766,"c":1060828,"b":"eee"},{"i":"VNIT, Nagpur","p":"Electronics and Communication Engineering","o":147532,"c":270474,"b":"ece"},{"i":"MIT Manipal","p":"Mathematics and Computing","o":150695,"c":627364,"b":"cse"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Computer Science and Engineering","o":153694,"c":246213,"b":"cse"},{"i":"NIT Calicut","p":"Engineering Physics","o":153753,"c":374066,"b":"other"},{"i":"Jawaharlal Nehru University, Delhi","p":"Computer Science and Engineering","o":156172,"c":584509,"b":"cse"},{"i":"NIT, Rourkela","p":"Electronics and Instrumentation Engineering","o":156706,"c":372745,"b":"other"},{"i":"NIT Calicut","p":"Mechanical Engineering","o":157178,"c":196041,"b":"mech"},{"i":"MIT Manipal","p":"Computer Science and Engineering","o":158725,"c":515477,"b":"cse"},{"i":"NIT, Rourkela","p":"Electrical Engineering","o":173994,"c":368435,"b":"eee"},{"i":"MN NIT Allahabad","p":"Electronics and Communication Engineering","o":175138,"c":390036,"b":"ece"},{"i":"NIT, Warangal","p":"Chemical Engineering","o":175621,"c":181015,"b":"chem"},{"i":"NIT Calicut","p":"Materials Science and Engineering","o":183002,"c":417977,"b":"meta"},{"i":"NIT, Tiruchirappalli","p":"Production Engineering","o":187126,"c":250166,"b":"mech"},{"i":"NIT, Rourkela","p":"Mechanical Engineering","o":188628,"c":219295,"b":"mech"},{"i":"MA NIT Bhopal","p":"Computer Science and Engineering","o":190496,"c":299739,"b":"cse"},{"i":"University of Hyderabad","p":"Computer Science and Engineering)","o":192322,"c":664049,"b":"cse"},{"i":"NIT, Warangal","p":"Bio Technology","o":195173,"c":355077,"b":"chem"},{"i":"MIT Manipal","p":"Biomedical Engineering","o":204241,"c":960930,"b":"other"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Electronics and Communication Engineering","o":204448,"c":275208,"b":"ece"},{"i":"NIT, Rourkela","p":"Chemical Engineering","o":205547,"c":357632,"b":"chem"},{"i":"Malaviya NIT Jaipur","p":"Mechanical Engineering","o":208250,"c":563932,"b":"mech"},{"i":"Indira Gandhi Delhi Technical University for Women Delhi","p":"Computer Science and Artificial Intelligence","o":209944,"c":339012,"b":"cse"},{"i":"IIIT (IIIT) Pune","p":"Computer Science and Engineering","o":218734,"c":1140984,"b":"cse"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Computer Science and Engineering","o":219432,"c":520518,"b":"cse"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Mathematics and Scientific Computing","o":225262,"c":509620,"b":"other"},{"i":"NIT Goa","p":"Computer Science and Engineering","o":226401,"c":274261,"b":"cse"},{"i":"NIT, Jamshedpur","p":"Computer Science and Engineering","o":229320,"c":386800,"b":"cse"},{"i":"Pt. Dwarka Prasad Mishra IIIT, Design & Manufacture Jabalpur","p":"Computer Science and Engineering","o":233653,"c":689088,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Civil Engineering","o":234186,"c":436089,"b":"civil"},{"i":"NIT Calicut","p":"Energy Engineering","o":235640,"c":268309,"b":"other"},{"i":"DTU, Delhi","p":"Mechanical Engineering","o":238520,"c":473418,"b":"mech"},{"i":"IIIT(IIIT) Kottayam","p":"Electronics and Communication Engineering","o":241063,"c":359106,"b":"ece"},{"i":"IIIT (IIIT), Sri City, Chittoor","p":"Computer Science and Engineering","o":241379,"c":408977,"b":"cse"},{"i":"NIT Delhi","p":"Electronics and Communication Engineering","o":247016,"c":333514,"b":"ece"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Computer Science and Engineering with Major in Artificial Intelligence","o":247243,"c":282946,"b":"cse"},{"i":"MIT Manipal","p":"Computer Science and Financial Technology","o":248452,"c":798758,"b":"cse"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering (Data Science)","o":251743,"c":257467,"b":"cse"},{"i":"VNIT, Nagpur","p":"Electrical and Electronics Engineering","o":254522,"c":403960,"b":"eee"},{"i":"SV NIT, Surat","p":"Mechanical Engineering","o":257972,"c":575947,"b":"mech"},{"i":"NIT Puducherry","p":"Electronics and Communication Engineering","o":258207,"c":417977,"b":"ece"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Information Technology","o":260223,"c":284722,"b":"cse"},{"i":"NIT, Kurukshetra","p":"Artificial Intelligence and Machine Learning","o":260778,"c":586946,"b":"cse"},{"i":"MN NIT Allahabad","p":"Mechanical Engineering","o":264569,"c":550551,"b":"mech"},{"i":"SV NIT, Surat","p":"Electronics and Communication Engineering","o":270474,"c":358608,"b":"ece"},{"i":"VNIT, Nagpur","p":"Mechanical Engineering","o":274707,"c":333505,"b":"mech"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Computer Science and Engineering)","o":274795,"c":293810,"b":"cse"},{"i":"NIT Delhi","p":"Artificial Intelligence and Data Science","o":280252,"c":280252,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Metallurgical and Materials Engineering","o":281114,"c":281114,"b":"meta"},{"i":"NIT Delhi","p":"Mechanical Engineering","o":288215,"c":316351,"b":"mech"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Computer Science and Engineering","o":289276,"c":396304,"b":"cse"},{"i":"NIT Delhi","p":"VLSI Design and Technology","o":289927,"c":289927,"b":"ece"},{"i":"SV NIT, Surat","p":"Artificial Intelligence","o":294350,"c":450137,"b":"cse"},{"i":"SV NIT, Surat","p":"Mathematics and Computing","o":295501,"c":376662,"b":"cse"},{"i":"NIT, Kurukshetra","p":"Artificial Intelligence and Data Science","o":299645,"c":763820,"b":"cse"},{"i":"NIT, Andhra Pradesh","p":"Computer Science and Engineering","o":301670,"c":306480,"b":"cse"},{"i":"SV NIT, Surat","p":"Artificial Intelligence","o":305470,"c":530134,"b":"cse"},{"i":"MN NIT Allahabad","p":"Biotechnology","o":308124,"c":308124,"b":"chem"},{"i":"MIT Manipal","p":"Aeronautical Engineering","o":310390,"c":909523,"b":"other"},{"i":"IIIT (IIIT), Sri City, Chittoor","p":"Artificial Intelligence and Data Science","o":311096,"c":934537,"b":"cse"},{"i":"MIT Manipal","p":"Mechanical Engineering","o":314793,"c":867558,"b":"mech"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Aerospace Engineering","o":317467,"c":317467,"b":"other"},{"i":"NIT, Kurukshetra","p":"Computer Science and Engineering","o":322335,"c":403752,"b":"cse"},{"i":"NIT Durgapur","p":"Electronics and Communication Engineering","o":325511,"c":390036,"b":"ece"},{"i":"NIT, Silchar","p":"Computer Science and Engineering","o":327195,"c":327195,"b":"cse"},{"i":"NIT, Kurukshetra","p":"Computer Science and Engineering)","o":328768,"c":328768,"b":"cse"},{"i":"NIT Calicut","p":"Production Engineering","o":333218,"c":498621,"b":"mech"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Mechanical Engineering","o":338240,"c":437322,"b":"mech"},{"i":"Pandit Deendayal Energy University, Gandhinagar","p":"Chemical Engineering","o":342862,"c":342862,"b":"chem"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Electrical and Electronics Engineering","o":347668,"c":347668,"b":"eee"},{"i":"IIIT(IIIT), Vadodara, Gujrat","p":"Computer Science and Engineering","o":347943,"c":347943,"b":"cse"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"B.Tech. in Electronics and Communication Engineering and M.Tech. in Microelectronics and VLSI Systems)","o":355077,"c":355077,"b":"ece"},{"i":"SV NIT, Surat","p":"Chemical Engineering","o":357023,"c":908293,"b":"chem"},{"i":"SV NIT, Surat","p":"Electronics and VLSI Engineering","o":358615,"c":431723,"b":"ece"},{"i":"MN NIT Allahabad","p":"Chemical Engineering","o":358809,"c":358809,"b":"chem"},{"i":"VNIT, Nagpur","p":"Chemical Engineering","o":360727,"c":574810,"b":"chem"},{"i":"NIT, Warangal","p":"Chemical Engineering)","o":367238,"c":367238,"b":"chem"},{"i":"NIT Puducherry","p":"Civil Engineering","o":372989,"c":372989,"b":"civil"},{"i":"NIT Goa","p":"Electronics and Communication Engineering","o":372992,"c":551924,"b":"ece"},{"i":"NIT, Rourkela","p":"Bio Medical Engineering","o":378306,"c":394021,"b":"other"},{"i":"NIT, Silchar","p":"Electronics and Communication Engineering","o":383910,"c":383910,"b":"ece"},{"i":"MA NIT Bhopal","p":"Electronics and Communication Engineering","o":395919,"c":610318,"b":"ece"},{"i":"NIT, Kurukshetra","p":"Electronics and Communication Engineering","o":396304,"c":655863,"b":"ece"},{"i":"NIT Durgapur","p":"Mathematics and Computing","o":396720,"c":396720,"b":"cse"},{"i":"Punjab Engineering College, Chandigarh","p":"Computer Science and Engineering","o":403752,"c":1139108,"b":"cse"},{"i":"MIT Manipal","p":"Electronics and Communication Engineering","o":411971,"c":721643,"b":"ece"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Integrated B. Tech.(IT) and M. Tech (IT)","o":417431,"c":421890,"b":"other"},{"i":"MA NIT Bhopal","p":"Electrical Engineering","o":419692,"c":585441,"b":"eee"},{"i":"DTU, Delhi","p":"Electrical Engineering","o":422072,"c":594412,"b":"eee"},{"i":"NIT, Srinagar","p":"Computer Science and Engineering","o":427477,"c":427477,"b":"cse"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Electronics and Telecommunication Engineering","o":437890,"c":437890,"b":"other"},{"i":"NIT Hamirpur","p":"Computer Science and Engineering","o":441386,"c":769321,"b":"cse"},{"i":"NIT Raipur","p":"Computer Science and Engineering","o":454797,"c":551081,"b":"cse"},{"i":"NIT Goa","p":"Mechanical Engineering","o":457872,"c":457872,"b":"mech"},{"i":"NIT Patna","p":"Computer Science and Engineering","o":459989,"c":875705,"b":"cse"},{"i":"NIT Puducherry","p":"Electrical and Electronics Engineering","o":462135,"c":462135,"b":"eee"},{"i":"Indira Gandhi Delhi Technical University for Women Delhi","p":"Computer Science and Engineering","o":463423,"c":672213,"b":"cse"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"B.Tech. in Electronics and Communication Engineering and M.Tech. in Communication Systems)","o":468854,"c":468854,"b":"ece"},{"i":"NIT, Jamshedpur","p":"Electronics and Communication Engineering","o":473691,"c":587044,"b":"ece"},{"i":"NIT, Kurukshetra","p":"Electronics and Communication Engineering)","o":474158,"c":474158,"b":"ece"},{"i":"MN NIT Allahabad","p":"Engineering and Computational Mechanics","o":475189,"c":475189,"b":"other"},{"i":"NIT, Kurukshetra","p":"Microelectronics & VLSI Engineering","o":485672,"c":968418,"b":"ece"},{"i":"NIT Karnataka, Surathkal","p":"Metallurgical and Materials Engineering","o":513425,"c":568773,"b":"meta"},{"i":"NIT, Warangal","p":"Mathematics","o":513655,"c":513655,"b":"other"},{"i":"NIT, Rourkela","p":"Bio Technology","o":513995,"c":584941,"b":"chem"},{"i":"MIT Manipal","p":"Biotechnology","o":515477,"c":515477,"b":"chem"},{"i":"MN NIT Allahabad","p":"Electrical Engineering","o":516450,"c":737665,"b":"eee"},{"i":"NIT Patna","p":"Artificial Intelligence and Data Science","o":521760,"c":521760,"b":"cse"},{"i":"DTU, Delhi","p":"Chemical Engineering","o":523204,"c":523204,"b":"chem"},{"i":"NIT, Kurukshetra","p":"Mechanical Engineering","o":550551,"c":675413,"b":"mech"},{"i":"IIIT (IIIT) Pune","p":"Electronics and Communication Engineering","o":559773,"c":559773,"b":"ece"},{"i":"Punjab Engineering College, Chandigarh","p":"Mechanical Engineering","o":560637,"c":560637,"b":"mech"},{"i":"SV NIT, Surat","p":"Electrical Engineering","o":572806,"c":914674,"b":"eee"},{"i":"NIT Patna","p":"Computer Science and Engineering with Specialization in Cyber Security)","o":576985,"c":576985,"b":"cse"},{"i":"NIT, Warangal","p":"Metallurgical and Materials Engineering","o":578455,"c":578455,"b":"meta"},{"i":"NIT Delhi","p":"Civil Engineering","o":580466,"c":580466,"b":"civil"},{"i":"Indian Maritime University - Visakhapatnam Campus","p":"Naval Architecture and Ocean Engineering","o":582932,"c":582932,"b":"arch"},{"i":"NIT Goa","p":"Electrical and Electronics Engineering","o":586914,"c":664049,"b":"eee"},{"i":"NIT Karnataka, Surathkal","p":"Mining Engineering","o":587729,"c":587729,"b":"meta"},{"i":"NIT, Rourkela","p":"Industrial Design","o":603766,"c":603766,"b":"mech"},{"i":"Puducherry Technological University, Puducherry","p":"Computer Science and Engineering","o":612144,"c":612144,"b":"cse"},{"i":"NIT, Andhra Pradesh","p":"Electronics and Communication Engineering","o":626036,"c":1029243,"b":"ece"},{"i":"MIT Manipal","p":"Cyber Physical Systems","o":636549,"c":636549,"b":"other"},{"i":"NIT, Kurukshetra","p":"Electrical Engineering)","o":656568,"c":656568,"b":"eee"},{"i":"DTU, Delhi","p":"Biotechnology","o":658181,"c":658181,"b":"chem"},{"i":"NIT Raipur","p":"Information Technology","o":658673,"c":658673,"b":"cse"},{"i":"NIT, Warangal","p":"Metallurgical and Materials Engineering)","o":662899,"c":662899,"b":"meta"},{"i":"VNIT, Nagpur","p":"Civil Engineering","o":667613,"c":667613,"b":"civil"},{"i":"Indira Gandhi Delhi Technical University for Women Delhi","p":"Information Technology","o":672213,"c":672213,"b":"cse"},{"i":"NIT, Jalandhar","p":"Information Technology","o":675536,"c":769321,"b":"cse"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Integrated B. Tech.(IT) and MBA","o":688993,"c":688993,"b":"other"},{"i":"NIT, Jalandhar","p":"Mechanical Engineering","o":707893,"c":707893,"b":"mech"},{"i":"Malaviya NIT Jaipur","p":"Chemical Engineering","o":707910,"c":707910,"b":"chem"},{"i":"NIT, Rourkela","p":"Physics","o":710572,"c":710572,"b":"other"},{"i":"NIT Agartala","p":"Computer Science and Engineering","o":717697,"c":931692,"b":"cse"},{"i":"NIT, Kurukshetra","p":"Mathematics and Computing","o":747088,"c":747088,"b":"cse"},{"i":"NIT, Kurukshetra","p":"Information Technology","o":763820,"c":763820,"b":"cse"},{"i":"Indira Gandhi Delhi Technical University for Women Delhi","p":"Artificial Intelligence and Machine Learning","o":769660,"c":769660,"b":"cse"},{"i":"DTU, Delhi","p":"Environmental Engineering","o":782356,"c":782356,"b":"other"},{"i":"Gautam Buddha University, Greater Noida","p":"Integrated B. Tech. - M. Tech in Computer Science & Engineering","o":792983,"c":792983,"b":"cse"},{"i":"NIT, Jalandhar","p":"Data Science and Engineering","o":809482,"c":809482,"b":"cse"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Design Engineering","o":832010,"c":832010,"b":"other"},{"i":"Punjab Engineering College, Chandigarh","p":"Computer Science and Engineering (Data Science)","o":962638,"c":1060828,"b":"cse"},{"i":"NIT Puducherry","p":"Mechanical Engineering","o":1149332,"c":1149332,"b":"mech"},{"i":"MA NIT Bhopal","p":"Mathematics and Data Science)","o":1221201,"c":1221201,"b":"cse"},{"i":"NIT Patna","p":"Electronics and Communication Engineering","o":1270913,"c":1270913,"b":"ece"}],"nonciwg":[{"i":"SPA Delhi","p":"Architecture","o":279,"c":6016,"b":"arch"},{"i":"NIT, Tiruchirappalli","p":"Architecture","o":1189,"c":21988,"b":"arch"},{"i":"NIT Calicut","p":"Architecture","o":1735,"c":19111,"b":"arch"},{"i":"NIT Karnataka, Surathkal","p":"Computer Science and Engineering","o":3706,"c":33736,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Computer Science and Engineering","o":4891,"c":17478,"b":"cse"},{"i":"NIT, Warangal","p":"Computer Science and Engineering","o":6401,"c":84741,"b":"cse"},{"i":"SPA: Vijayawada","p":"Architecture","o":9956,"c":9956,"b":"arch"},{"i":"NIT, Tiruchirappalli","p":"Electronics and Communication Engineering","o":11074,"c":46614,"b":"ece"},{"i":"NIT, Tiruchirappalli","p":"Chemical Engineering","o":29304,"c":364481,"b":"chem"},{"i":"NIT Karnataka, Surathkal","p":"Artificial Intelligence","o":33167,"c":76784,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Information Technology","o":34504,"c":87162,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Electronics and Communication Engineering","o":43365,"c":79607,"b":"ece"},{"i":"IIIT, Allahabad","p":"Information Technology","o":46247,"c":423129,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Computational and Data Science","o":49528,"c":76237,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Electrical and Electronics Engineering","o":54646,"c":116498,"b":"eee"},{"i":"NIT Calicut","p":"Computer Science and Engineering","o":56914,"c":126093,"b":"cse"},{"i":"NIT Calicut","p":"Electronics and Communication Engineering","o":59548,"c":257873,"b":"ece"},{"i":"NIT, Tiruchirappalli","p":"Mechanical Engineering","o":61085,"c":205379,"b":"mech"},{"i":"SV NIT, Surat","p":"Electronics and VLSI Engineering","o":62656,"c":62656,"b":"ece"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Electronics and Telecommunication Engineering","o":67281,"c":1089227,"b":"other"},{"i":"NIT, Rourkela","p":"Computer Science and Engineering","o":71444,"c":140041,"b":"cse"},{"i":"VNIT, Nagpur","p":"Computer Science and Engineering","o":73269,"c":280185,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Chemical Engineering","o":76661,"c":363190,"b":"chem"},{"i":"NIT, Warangal","p":"Computer Science and Engineering ( Artificial Intelligence & Data Science)","o":82449,"c":111529,"b":"cse"},{"i":"DTU, Delhi","p":"Computer Science and Engineering","o":82863,"c":241277,"b":"cse"},{"i":"NIT, Warangal","p":"Electronics and Communication Engineering","o":84813,"c":166004,"b":"ece"},{"i":"NIT Karnataka, Surathkal","p":"Electrical and Electronics Engineering","o":87536,"c":156135,"b":"eee"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering","o":88994,"c":853076,"b":"cse"},{"i":"NIT, Warangal","p":"Electronics and Communication Engineering (VLSI Design and Technology)","o":92174,"c":189638,"b":"ece"},{"i":"NIT, Warangal","p":"Mathematics and Computing","o":95748,"c":187769,"b":"cse"},{"i":"NIT Karnataka, Surathkal","p":"Mechanical Engineering","o":108837,"c":207370,"b":"mech"},{"i":"DTU, Delhi","p":"Mathematics and Computing","o":113807,"c":344926,"b":"cse"},{"i":"MIT Manipal","p":"Mechatronics Engineering","o":114474,"c":114474,"b":"other"},{"i":"SV NIT, Surat","p":"Computer Science and Engineering","o":114935,"c":709411,"b":"cse"},{"i":"IIIT, Allahabad","p":"Information Technology-Business Informatics","o":135036,"c":275947,"b":"cse"},{"i":"NIT, Rourkela","p":"Artificial Intelligence","o":147698,"c":187573,"b":"cse"},{"i":"MIT Manipal","p":"Computer Science and Engineering","o":148831,"c":214120,"b":"cse"},{"i":"Malaviya NIT Jaipur","p":"Computer Science and Engineering","o":150061,"c":494231,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Instrumentation and Control Engineering","o":151746,"c":230753,"b":"other"},{"i":"MN NIT Allahabad","p":"Computer Science and Engineering","o":156785,"c":931961,"b":"cse"},{"i":"NIT, Warangal","p":"Electrical and Electronics Engineering","o":160426,"c":314315,"b":"eee"},{"i":"NIT, Rourkela","p":"Electronics and Communication Engineering","o":165256,"c":196161,"b":"ece"},{"i":"NIT Calicut","p":"Electrical and Electronics Engineering","o":171618,"c":426990,"b":"eee"},{"i":"NIT, Rourkela","p":"Electrical Engineering","o":189927,"c":1173667,"b":"eee"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering (Artificial Intelligence)","o":196354,"c":1025758,"b":"cse"},{"i":"NIT, Warangal","p":"Mechanical Engineering","o":200250,"c":264569,"b":"mech"},{"i":"NIT Karnataka, Surathkal","p":"Metallurgical and Materials Engineering","o":204417,"c":688014,"b":"meta"},{"i":"NIT Delhi","p":"Computer Science and Engineering","o":205854,"c":926908,"b":"cse"},{"i":"VNIT, Nagpur","p":"Electronics and Communication Engineering","o":221245,"c":485153,"b":"ece"},{"i":"NIT Calicut","p":"Engineering Physics","o":229380,"c":424146,"b":"other"},{"i":"NIT, Rourkela","p":"Electronics and Instrumentation Engineering","o":237524,"c":747778,"b":"other"},{"i":"NIT Calicut","p":"Mechanical Engineering","o":246433,"c":521078,"b":"mech"},{"i":"Malaviya NIT Jaipur","p":"Electronics and Communication Engineering","o":250102,"c":587471,"b":"ece"},{"i":"DTU, Delhi","p":"Information Technology","o":257715,"c":484379,"b":"cse"},{"i":"NIT Durgapur","p":"Computer Science and Engineering","o":259359,"c":358272,"b":"cse"},{"i":"DTU, Delhi","p":"Software Engineering","o":259595,"c":450252,"b":"other"},{"i":"IIIT, Allahabad","p":"Electronics and Communication Engineering","o":277691,"c":1329568,"b":"ece"},{"i":"NIT, Kurukshetra","p":"Computer Science and Engineering","o":278291,"c":1020638,"b":"cse"},{"i":"NIT Calicut","p":"Energy Engineering","o":278297,"c":770804,"b":"other"},{"i":"Atal Bihari Vajpayee IIIT & Management Gwalior","p":"Computer Science and Engineering","o":281313,"c":530871,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Production Engineering","o":290606,"c":474054,"b":"mech"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Computer Science and Engineering","o":291413,"c":649670,"b":"cse"},{"i":"DTU, Delhi","p":"Electronics and Communication Engineering","o":298172,"c":1117096,"b":"ece"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Computer Science and Engineering","o":307337,"c":862161,"b":"cse"},{"i":"NIT, Rourkela","p":"Mechanical Engineering","o":307601,"c":701807,"b":"mech"},{"i":"MA NIT Bhopal","p":"Computer Science and Engineering","o":309532,"c":1017981,"b":"cse"},{"i":"IIIT (IIIT) Pune","p":"Electronics and Communication Engineering","o":311942,"c":311942,"b":"ece"},{"i":"NIT Goa","p":"Computer Science and Engineering","o":313267,"c":828008,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Civil Engineering","o":333855,"c":974217,"b":"civil"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering","o":340585,"c":775045,"b":"cse"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering with specialization in Cyber Security","o":343679,"c":765097,"b":"cse"},{"i":"Netaji Subhas University of Technology, Delhi","p":"Computer Science and Engineering (Data Science)","o":346398,"c":514758,"b":"cse"},{"i":"NIT, Warangal","p":"Chemical Engineering","o":355389,"c":603129,"b":"chem"},{"i":"NIT Calicut","p":"Chemical Engineering","o":357830,"c":843474,"b":"chem"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Computer Science and Engineering with Major in Artificial Intelligence","o":369594,"c":369594,"b":"cse"},{"i":"SV NIT, Surat","p":"Mathematics and Computing","o":399122,"c":399122,"b":"cse"},{"i":"NIT, Jamshedpur","p":"Computer Science and Engineering","o":412531,"c":1245851,"b":"cse"},{"i":"IIIT(IIIT) Kottayam","p":"Computer Science and Engineering with specialization in Artificial Intelligence and Data Science","o":452425,"c":878872,"b":"cse"},{"i":"Malaviya NIT Jaipur","p":"Artificial Intelligence and Data Engineering","o":463786,"c":907544,"b":"cse"},{"i":"IIIT, Design & Manufacturing, Kancheepuram","p":"Electronics and Communication Engineering","o":503149,"c":602270,"b":"ece"},{"i":"NIT Calicut","p":"Production Engineering","o":509668,"c":976425,"b":"mech"},{"i":"NIT, Kurukshetra","p":"Artificial Intelligence and Machine Learning","o":527060,"c":527060,"b":"cse"},{"i":"IIIT (IIIT), Sri City, Chittoor","p":"Artificial Intelligence and Data Science","o":530805,"c":530805,"b":"cse"},{"i":"SV NIT, Surat","p":"Electronics and Communication Engineering","o":533051,"c":624011,"b":"ece"},{"i":"MN NIT Allahabad","p":"Electronics and Communication Engineering","o":533851,"c":533851,"b":"ece"},{"i":"NIT Delhi","p":"Artificial Intelligence and Data Science","o":542924,"c":1025758,"b":"cse"},{"i":"NIT Goa","p":"Electronics and Communication Engineering","o":551924,"c":551924,"b":"ece"},{"i":"Indian Institute of Engineering Science and Technology, Shibpur","p":"Aerospace Engineering","o":555613,"c":555613,"b":"other"},{"i":"NIT, Warangal","p":"Bio Technology","o":603129,"c":779103,"b":"chem"},{"i":"NIT Karnataka, Surathkal","p":"Civil Engineering","o":607990,"c":607990,"b":"civil"},{"i":"DTU, Delhi","p":"Mechanical Engineering","o":617909,"c":1177629,"b":"mech"},{"i":"NIT Goa","p":"Electrical and Electronics Engineering","o":619516,"c":619516,"b":"eee"},{"i":"IIIT (IIIT) Pune","p":"Computer Science and Engineering","o":619976,"c":619976,"b":"cse"},{"i":"IIIT (IIIT), Sri City, Chittoor","p":"Computer Science and Engineering","o":639012,"c":639012,"b":"cse"},{"i":"NIT Calicut","p":"Civil Engineering","o":651222,"c":934725,"b":"civil"},{"i":"Punjab Engineering College, Chandigarh","p":"Computer Science and Engineering","o":664706,"c":819399,"b":"cse"},{"i":"NIT Puducherry","p":"Computer Science and Engineering","o":666619,"c":666619,"b":"cse"},{"i":"NIT Durgapur","p":"Mathematics and Computing","o":698829,"c":698829,"b":"cse"},{"i":"NIT, Tiruchirappalli","p":"Metallurgical and Materials Engineering","o":726464,"c":726464,"b":"meta"},{"i":"SV NIT, Surat","p":"Mechanical Engineering","o":737383,"c":737383,"b":"mech"},{"i":"NIT, Rourkela","p":"Bio Medical Engineering","o":805585,"c":805585,"b":"other"},{"i":"NIT Calicut","p":"Biotechnology","o":818619,"c":818619,"b":"chem"},{"i":"NIT, Kurukshetra","p":"Artificial Intelligence and Data Science","o":926908,"c":926908,"b":"cse"},{"i":"NIT, Rourkela","p":"Chemical Engineering","o":955829,"c":955829,"b":"chem"},{"i":"VNIT, Nagpur","p":"Electrical and Electronics Engineering","o":1074763,"c":1074763,"b":"eee"},{"i":"NIT, Warangal","p":"Chemical Engineering)","o":1224371,"c":1224371,"b":"chem"},{"i":"NIT Delhi","p":"Aerospace Engineering","o":1259326,"c":1259326,"b":"other"},{"i":"Malaviya NIT Jaipur","p":"Mechanical Engineering","o":1329417,"c":1329417,"b":"mech"},{"i":"NIT, Jalandhar","p":"Computer Science and Engineering","o":1347319,"c":1347319,"b":"cse"}]};

;


// ═══════ CONFIG ═══════
const GOOGLE_SHEET_URL = 'https://script.google.com/macros/s/AKfycby0S7vjygo2QSWxjEDUr5vQJ4zPWrTFHXIb4vXEpND3OopfSIilbkABlv8NnkOb9zzclw/exec';

const BRANCHES = {
  cse:  { name: 'Computer Science (CSE)',   color: '#0E3A8A' },
  ece:  { name: 'Electronics & Comm (ECE)', color: '#1A52C4' },
  eee:  { name: 'Electrical (EEE)',         color: '#7C3AED' },
  mech: { name: 'Mechanical Engineering',   color: '#D97706' },
  civil:{ name: 'Civil Engineering',        color: '#0D7377' },
  chem: { name: 'Chemical Engineering',     color: '#16A34A' },
};

const SKILLS = {
  logic:    { name: 'Logical & Algorithmic Reasoning', color: '#0E3A8A' },
  math:     { name: 'Mathematical Ability',            color: '#1A52C4' },
  coding:   { name: 'Programming / Coding',            color: '#FF6B0A' },
  spatial:  { name: 'Spatial / 3D Visualization',      color: '#D97706' },
  circuits: { name: 'Circuit & Electronics',           color: '#7C3AED' },
  physics:  { name: 'Physics (Mechanics/Thermo)',      color: '#0D7377' },
  chemistry:{ name: 'Chemistry',                       color: '#16A34A' },
  precision:{ name: 'Precision & Detail',              color: '#DC2626' },
};

// Top-3 critical skills per branch
const BRANCH_CRITICAL_SKILLS = {
  cse:  ['coding','logic','math'],
  ece:  ['circuits','math','logic'],
  eee:  ['circuits','physics','math'],
  mech: ['spatial','physics','precision'],
  civil:['spatial','math','precision'],
  chem: ['chemistry','precision','physics'],
};

const SKILL_BUILDING = {
  logic:    'Practice algorithmic problems on HackerRank/LeetCode (easy tier) and logic puzzles. A free intro-CS course (Harvard CS50) builds this fast.',
  math:     'Strengthen calculus, linear algebra & probability via Khan Academy. Solve 3-4 applied problems daily — engineering maths rewards consistency over cramming.',
  coding:   'Start Python on freeCodeCamp or CS50. Build 2-3 tiny projects (calculator, to-do app). Get comfortable with loops, functions & arrays before college.',
  spatial:  'Practice with free CAD tools (Tinkercad, Autodesk Fusion 360). Do mental-rotation and engineering-drawing exercises — spatial skill is highly trainable.',
  circuits: 'Learn electronics basics on All About Circuits / Khan Academy. Use the free Tinkercad Circuits simulator and try a starter Arduino kit.',
  physics:  'Revisit mechanics & thermodynamics fundamentals (HC Verma, Khan Academy). Focus on solving problems, not just reading theory.',
  chemistry:'Strengthen physical & organic chemistry. For chemical engineering specifically, prioritise thermodynamics and reaction kinetics.',
  precision:'Build through careful lab documentation, technical-drawing practice, and measurement exercises. Make double-checking detailed work a habit.',
};

// DASA 2026 schedule (official brochure v1.2)
const DASA_SCHEDULE = [
  { event: 'Registration, DEF payment, document upload & choice filling OPEN', date: 'Tue, 28 Jul 2026, 10:00 IST' },
  { event: 'Mock seat allocation display', date: 'Fri, 31 Jul 2026, 10:00 IST' },
  { event: 'Registration, DEF payment & document upload CLOSE', date: 'Mon, 03 Aug 2026, 10:00 IST' },
  { event: 'Last day: verifying officer queries + balance DEF', date: 'Tue, 04 Aug 2026, 21:00 IST' },
  { event: 'Choice filling & locking ENDS (auto-lock of saved choices)', date: 'Wed, 05 Aug 2026, 14:00 IST' },
  { event: 'Round I — Seat allotment result', date: 'Thu, 06 Aug 2026, 17:00 IST' },
  { event: 'Round I willingness window (Freeze/Slide/Float/Surrender/Withdraw/Exit)', date: '06-10 Aug 2026, by 17:00 IST' },
  { event: 'Round II — Seat allotment result (final)', date: 'Wed, 12 Aug 2026, 17:00 IST' },
  { event: 'Physical reporting at allotted institute (tentative)', date: '13-18 Aug 2026' },
];

const DOC_CHECKLIST = [
  'Valid passport (student) - 1+ year validity',
  'Valid passport (sponsoring parent) showing NRI status',
  'JEE Main 2026 scorecard with CRL rank (sole qualifying exam - no SAT)',
  'Class 12 mark sheet - min 75% aggregate (7.5 CGPA) in 5 subjects',
  'Class 10 certificate (date of birth proof)',
  'School certificate: 11th & 12th completion (Annexure 11 format)',
  'NRI proof: 2 years education (11th+12th) abroad in last 8 years',
  'Medical certificate (Annexure 10 format)',
  'CIWG only: parent Gulf passport + visa + work permit valid in 2026',
  'CIWG only: employer certificate (Annexure 12 format)',
  'Name consistency: identical across passport, JEE card, all certificates',
  'Bank details for refund: account, IFSC, SWIFT, IBAN (Gulf banks)',
];

let RANKS_DATA = null;
let student = {};
let current = 0;
let answers = {};
let branchScores = {};
let skillScores = {};
let knowledgeScore = 0;
let hiddenInsights = [];
let expertFlags = [];

const sections = [
  { at: 0,  icon: '🧲', title: 'Part 1 · Interest Mapping',   desc: 'What genuinely pulls your attention - answer honestly, not strategically.' },
  { at: 8,  icon: '🧠', title: 'Part 2 · Aptitude Signals',   desc: 'How your mind naturally works - there are no wrong answers.' },
  { at: 14, icon: '📚', title: 'Part 3 · Knowledge Check',    desc: 'What you actually know about engineering branches today.' },
  { at: 18, icon: '🎯', title: 'Part 4 · Skill Aptitude Check', desc: 'Quick competency checks for the skills each branch demands. Answer based on your real ability.' },
  { at: 24, icon: '🔍', title: 'Part 5 · The Real Questions', desc: 'Honest questions that help your counselor see what surveys miss. Your answers are confidential.' },
];

function startAssessment() {
  const name = document.getElementById('f-name').value.trim();
  const email = document.getElementById('f-email').value.trim();
  const phone = document.getElementById('f-phone').value.trim();
  const country = document.getElementById('f-country').value;

  let valid = true;
  [['f-name',name],['f-email',email],['f-phone',phone],['f-country',country]].forEach(function(pair) {
    const el = document.getElementById(pair[0]);
    if (!pair[1]) { el.classList.add('error'); valid = false; }
    else el.classList.remove('error');
  });
  if (!valid) { alert('Please fill all required fields marked *'); return; }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    document.getElementById('f-email').classList.add('error');
    alert('Please enter a valid email address'); return;
  }

  student = {
    name: name, email: email, phone: phone, country: country,
    board: document.getElementById('f-board').value,
    jeeStatus: document.getElementById('f-jee').value,
    jeeRank: document.getElementById('f-rank').value.trim(),
    pathway: document.getElementById('f-pathway').value,
    currentBranch: document.getElementById('f-current-branch').value.trim(),
    pref1: document.getElementById('f-pref1').value,
    pref2: document.getElementById('f-pref2').value,
    pref3: document.getElementById('f-pref3').value,
    timestamp: new Date().toISOString(),
  };

  document.getElementById('info-section').classList.add('hidden');
  document.getElementById('quiz-section').classList.remove('hidden');
  renderQ();
  window.scrollTo({ top:0, behavior:'smooth' });
}

function renderQ() {
  const q = QUESTIONS[current];
  const letters = ['A','B','C','D'];

  document.getElementById('progress-text').textContent = 'Question ' + (current+1) + ' of ' + QUESTIONS.length;
  document.getElementById('progress-fill').style.width = ((current/QUESTIONS.length)*100) + '%';

  const sec = sections.find(function(s) { return s.at === current; });
  const secContainer = document.getElementById('section-intro-container');
  if (sec) {
    secContainer.innerHTML = '<div class="section-intro"><div class="si-icon">' + sec.icon + '</div><h3>' + sec.title + '</h3><p>' + sec.desc + '</p></div>';
  } else {
    secContainer.innerHTML = '';
  }

  const revSections = sections.slice().reverse();
  const currentSec = revSections.find(function(s) { return current >= s.at; });
  document.getElementById('section-text').textContent = currentSec ? currentSec.title.split('·')[1].trim() : '';

  document.getElementById('btn-back').style.display = current > 0 ? 'block' : 'none';
  const btnNext = document.getElementById('btn-next');
  btnNext.disabled = answers[q.id] === undefined;
  btnNext.textContent = current === QUESTIONS.length-1 ? 'Finish & Generate Report →' : 'Next →';

  let optsHtml = '';
  q.opts.forEach(function(o, i) {
    const sel = answers[q.id] === i ? 'selected' : '';
    optsHtml += '<button class="opt-btn ' + sel + '" data-i="' + i + '" onclick="pick(this)">' +
      '<span class="opt-letter">' + letters[i] + '</span><span>' + o.t + '</span></button>';
  });

  document.getElementById('q-container').innerHTML =
    '<div class="q-card">' +
    '<div class="q-number">QUESTION ' + (current+1) + ' / ' + QUESTIONS.length + '</div>' +
    '<span class="q-category ' + q.catClass + '">' + q.cat + '</span>' +
    '<p class="q-text">' + q.text + '</p>' +
    (q.ctx ? '<p class="q-context">' + q.ctx + '</p>' : '') +
    '<div class="options">' + optsHtml + '</div></div>';
}

function pick(el) {
  answers[QUESTIONS[current].id] = parseInt(el.dataset.i);
  document.querySelectorAll('.opt-btn').forEach(function(b) { b.classList.remove('selected'); });
  el.classList.add('selected');
  document.getElementById('btn-next').disabled = false;
}

function nextQ() {
  if (current < QUESTIONS.length-1) { current++; renderQ(); window.scrollTo({top:0,behavior:'smooth'}); }
  else computeResults();
}

function prevQ() { if (current > 0) { current--; renderQ(); } }

function computeResults() {
  branchScores = { cse:0, ece:0, eee:0, mech:0, civil:0, chem:0 };
  skillScores = { logic:0, math:0, coding:0, spatial:0, circuits:0, physics:0, chemistry:0, precision:0 };
  knowledgeScore = 0;
  hiddenInsights = [];
  expertFlags = [];

  QUESTIONS.forEach(function(q) {
    const idx = answers[q.id];
    if (idx === undefined) return;
    const opt = q.opts[idx];
    if (opt.s) {
      Object.keys(opt.s).forEach(function(k) {
        if (k === '_know') knowledgeScore += opt.s[k];
        else branchScores[k] = (branchScores[k]||0) + opt.s[k];
      });
    }
    if (opt.sk) {
      Object.keys(opt.sk).forEach(function(k) { skillScores[k] = opt.sk[k]; });
    }
    if (opt.h) hiddenInsights.push({ q: q.text, a: opt.t, note: opt.h });
    if (opt.flag) expertFlags.push(opt.flag);
  });

  // Derive chemistry (Q4) and precision (Q13) from existing answers
  if (answers[4] !== undefined)  skillScores.chemistry = [3,2,1,0][answers[4]];
  if (answers[13] !== undefined) skillScores.precision = [3,2,0,1][answers[13]];

  showResults();
}

function getRankedBranches() {
  const maxPossible = { cse:23, ece:17, eee:12, mech:18, civil:15, chem:11 };
  return Object.keys(branchScores).map(function(key) {
    return { key: key, score: branchScores[key], name: BRANCHES[key].name, color: BRANCHES[key].color,
             pct: Math.min(100, Math.round((branchScores[key] / maxPossible[key]) * 100)) };
  }).sort(function(a,b) { return b.pct - a.pct; });
}

function getSkillProfile() {
  return Object.keys(SKILLS).map(function(key) {
    const pct = Math.round((skillScores[key] / 3) * 100);
    return { key: key, name: SKILLS[key].name, color: SKILLS[key].color, pct: pct,
             level: pct>=67?'Strong':pct>=34?'Developing':'Gap' };
  });
}

function skillGapFor(branchKey) {
  const crit = BRANCH_CRITICAL_SKILLS[branchKey] || [];
  return crit.map(function(sk) {
    const pct = Math.round((skillScores[sk] / 3) * 100);
    return { skill: sk, name: SKILLS[sk].name, color: SKILLS[sk].color, pct: pct,
             gap: pct < 50, level: pct>=67?'Strong':pct>=34?'Developing':'Gap' };
  });
}

function getPrefOrder() {
  const prefs = [student.pref1, student.pref2, student.pref3].filter(function(p) { return p; });
  // Dedupe preserving order
  const seen = {}; const out = [];
  prefs.forEach(function(p) { if (!seen[p]) { seen[p] = 1; out.push(p); } });
  return out;
}

// ═══════ COLLEGE RECOMMENDATION ═══════
function recommendColleges(rank, topBranchKeys, pathway) {
  if (!rank || isNaN(rank)) return null;
  rank = parseInt(rank);
  let pool = [];
  const p = (pathway || '').toLowerCase();
  if (p.indexOf('ciwg') !== -1 && p.indexOf('dasa') !== -1 && p.indexOf('+') !== -1) {
    pool = RANKS_DATA.ciwg.map(function(d) { return Object.assign({src:'CIWG'}, d); })
      .concat(RANKS_DATA.nonciwg.map(function(d) { return Object.assign({src:'Non-CIWG'}, d); }));
  } else if (p.indexOf('ciwg') !== -1) {
    pool = RANKS_DATA.ciwg.map(function(d) { return Object.assign({src:'CIWG'}, d); });
  } else {
    pool = RANKS_DATA.nonciwg.map(function(d) { return Object.assign({src:'Non-CIWG'}, d); });
  }
  const results = [];
  pool.forEach(function(prog) {
    if (topBranchKeys.indexOf(prog.b) === -1) return;
    const closing = prog.c;
    let chance, chanceColor, sortBucket;
    if (rank <= closing * 0.7)      { chance = 'High';     chanceColor = '#16A34A'; sortBucket = 0; }
    else if (rank <= closing)       { chance = 'Good';     chanceColor = '#65A30D'; sortBucket = 1; }
    else if (rank <= closing * 1.3) { chance = 'Moderate'; chanceColor = '#D97706'; sortBucket = 2; }
    else if (rank <= closing * 1.8) { chance = 'Stretch';  chanceColor = '#EA580C'; sortBucket = 3; }
    else return;
    const fitIdx = topBranchKeys.indexOf(prog.b);
    results.push({ inst: prog.i, prog: prog.p, closing: closing, src: prog.src,
      chance: chance, chanceColor: chanceColor, sortKey: sortBucket*1000000 + fitIdx*500000 + closing });
  });
  results.sort(function(a,b) { return a.sortKey - b.sortKey; });
  return results.slice(0, 10);
}

function showResults() {
  document.getElementById('quiz-section').classList.add('hidden');
  const section = document.getElementById('result-section');
  section.classList.remove('hidden');

  const ranked = getRankedBranches();
  const top = ranked[0], second = ranked[1];
  const skillProfile = getSkillProfile();
  const prefOrder = getPrefOrder();
  const knowledgePct = Math.round((knowledgeScore / 12) * 100);
  const knowledgeLabel = knowledgePct >= 67 ? 'Strong' : knowledgePct >= 34 ? 'Moderate' : 'Limited';

  const gap = top.pct - second.pct;
  let clarityText = '';
  if (gap >= 20) clarityText = 'Your profile shows a <strong>clear fit</strong> toward ' + top.name + '.';
  else if (gap >= 10) clarityText = 'Your profile leans toward ' + top.name + ', with ' + second.name + ' as a strong second.';
  else clarityText = 'Your profile shows <strong>mixed signals</strong> - normal, and exactly where expert guidance helps most.';

  // ── Branch fit bars ──
  let fitRowsHtml = '';
  ranked.forEach(function(b, i) {
    fitRowsHtml += '<div class="bf-row"><span class="bf-rank">' + (i+1) + '</span>' +
      '<span class="bf-name">' + b.name + '</span>' +
      '<div class="bf-bar-wrap"><div class="bf-bar" style="width:0%;background:' + b.color + '" data-w="' + b.pct + '"></div></div>' +
      '<span class="bf-pct" style="color:' + b.color + '">' + b.pct + '%</span></div>';
  });

  // ── Preference vs Fit comparison ──
  let prefHtml = '';
  if (prefOrder.length > 0) {
    const fitOrder = ranked.map(function(b){ return b.key; });
    let rows = '';
    for (let i = 0; i < Math.max(prefOrder.length, 3); i++) {
      const prefKey = prefOrder[i];
      const fitKey = fitOrder[i];
      const prefName = prefKey ? BRANCHES[prefKey].name : '—';
      const fitName = fitKey ? BRANCHES[fitKey].name : '—';
      let matchIcon = '';
      if (prefKey && fitKey) {
        if (prefKey === fitKey) matchIcon = '<span style="color:#16A34A;font-weight:700;">✓ aligned</span>';
        else if (fitOrder.indexOf(prefKey) !== -1 && fitOrder.indexOf(prefKey) <= 2) matchIcon = '<span style="color:#D97706;font-weight:700;">~ close</span>';
        else matchIcon = '<span style="color:#DC2626;font-weight:700;">✗ differs</span>';
      }
      rows += '<div class="cmp-row"><span class="cmp-rank">' + (i+1) + '</span>' +
        '<span class="cmp-cell cmp-pref">' + prefName + '</span>' +
        '<span class="cmp-cell cmp-fit">' + fitName + '</span>' +
        '<span class="cmp-match">' + matchIcon + '</span></div>';
    }
    const pref1Key = prefOrder[0];
    const alignTop = pref1Key === top.key;
    prefHtml =
      '<div class="section-label">Your Preference vs Assessment Fit</div>' +
      '<div class="cmp-table">' +
      '<div class="cmp-row cmp-head"><span class="cmp-rank">#</span><span class="cmp-cell">You Prefer</span><span class="cmp-cell">Assessment Fit</span><span class="cmp-match">Match</span></div>' +
      rows + '</div>' +
      '<div class="insight-card ' + (alignTop ? '' : 'flag') + '"><span class="insight-icon">' + (alignTop ? '✅' : '⚠️') + '</span><span>' +
      (alignTop
        ? 'Your top preference (' + BRANCHES[pref1Key].name + ') matches your strongest assessment fit. That alignment is a good sign - your interest and aptitude point the same way.'
        : 'Your top preference (' + BRANCHES[pref1Key].name + ') differs from your strongest assessment fit (' + top.name + '). This gap is worth a careful conversation - sometimes preference reflects passion worth pursuing, sometimes it reflects external influence. The skill analysis below will help clarify.') +
      '</span></div>';
  }

  // ── Skill profile bars ──
  let skillRowsHtml = '';
  skillProfile.forEach(function(s) {
    const col = s.pct>=67?'#16A34A':s.pct>=34?'#D97706':'#DC2626';
    skillRowsHtml += '<div class="bf-row"><span class="dim-emoji">' + (s.pct>=67?'✅':s.pct>=34?'🔶':'❌') + '</span>' +
      '<span class="bf-name" style="min-width:175px;">' + s.name + '</span>' +
      '<div class="bf-bar-wrap"><div class="bf-bar" style="width:0%;background:' + s.color + '" data-w="' + s.pct + '"></div></div>' +
      '<span class="bf-pct" style="color:' + col + '">' + s.pct + '%</span></div>';
  });

  // ── Skill gap analysis for preferred branch (or top fit) ──
  const gapBranchKey = prefOrder.length > 0 ? prefOrder[0] : top.key;
  const gapBranchName = BRANCHES[gapBranchKey].name;
  const gaps = skillGapFor(gapBranchKey);
  let gapRowsHtml = '';
  const gapSkillsFound = [];
  gaps.forEach(function(g) {
    const col = g.pct>=67?'#16A34A':g.pct>=34?'#D97706':'#DC2626';
    if (g.gap) gapSkillsFound.push(g);
    gapRowsHtml += '<div class="gap-row">' +
      '<div class="gap-skill"><div class="gap-skill-name">' + g.name + '</div>' +
      '<div class="gap-skill-tag" style="color:' + col + ';background:' + col + '18;border:1px solid ' + col + '44">' + g.level + '</div></div>' +
      '<div class="bf-bar-wrap"><div class="bf-bar" style="width:0%;background:' + g.color + '" data-w="' + g.pct + '"></div></div>' +
      '<span class="bf-pct" style="color:' + col + '">' + g.pct + '%</span></div>';
  });

  let gapHtml =
    '<div class="section-label">Skill Gap Analysis — ' + (prefOrder.length > 0 ? 'Your Preferred Branch: ' : 'Your Best-Fit Branch: ') + gapBranchName + '</div>' +
    '<div class="gap-card">' +
    '<div class="gap-header">The 3 most critical skills for ' + gapBranchName + ' — and where you stand today</div>' +
    gapRowsHtml + '</div>';

  // ── Skill-building recommendations for gaps ──
  let buildHtml = '';
  if (gapSkillsFound.length > 0) {
    let items = '';
    gapSkillsFound.forEach(function(g) {
      items += '<div class="insight-card flag"><span class="insight-icon">🛠️</span><span><strong>' + g.name + ' (' + g.pct + '%):</strong> ' + SKILL_BUILDING[g.skill] + '</span></div>';
    });
    buildHtml = '<div class="section-label">Skill-Building Plan — Close These Gaps Before College</div>' + items;
  } else {
    buildHtml = '<div class="insight-card"><span class="insight-icon">💪</span><span><strong>No critical skill gaps</strong> for ' + gapBranchName + '. You already have a solid foundation in its core skills — focus on deepening them and building projects.</span></div>';
  }

  // ── College recommendations ──
  const recos = recommendColleges(student.jeeRank, [top.key, second.key], student.pathway);
  let collegeHtml = '';
  if (recos && recos.length > 0) {
    let rowsHtml = '';
    recos.forEach(function(r, i) {
      rowsHtml += '<div class="college-row"><span class="cr-rank">' + (i+1) + '</span>' +
        '<div class="cr-info"><div class="cr-inst">' + r.inst + '</div>' +
        '<div class="cr-prog">' + r.prog + ' · ' + r.src + '</div></div>' +
        '<div class="cr-meta"><span class="cr-chance" style="background:' + r.chanceColor + '22;color:' + r.chanceColor + ';border:1px solid ' + r.chanceColor + '44">' + r.chance + '</span>' +
        '<span class="cr-closing">2025 cutoff: ' + r.closing.toLocaleString('en-IN') + '</span></div></div>';
    });
    collegeHtml = '<div class="section-label">Top 10 Recommended Colleges — Rank ' + parseInt(student.jeeRank).toLocaleString('en-IN') + ' & Branch Fit</div>' +
      '<div class="college-list">' + rowsHtml + '</div>' +
      '<p style="font-size:0.72rem;color:var(--muted);margin:-0.5rem 0 1.25rem;line-height:1.5;">Based on DASA 2025 final-round closing ranks. 2026 cutoffs vary. High = well inside cutoff · Good = within · Moderate = within 30% beyond · Stretch = possible in later rounds.</p>';
  } else if (student.jeeRank) {
    collegeHtml = '<div class="insight-card flag"><span class="insight-icon">📊</span><span>Your rank is beyond the 2025 cutoff range for your top-fit branches in this dataset. Later rounds and Other-GFTI institutes often go deeper — discuss alternatives with your counselor.</span></div>';
  } else {
    collegeHtml = '<div class="insight-card"><span class="insight-icon">ℹ️</span><span>Enter your JEE rank at the start to get college recommendations from real DASA 2025 closing ranks.</span></div>';
  }

  // ── Expert flags ──
  let flagsHtml = '';
  if (expertFlags.length > 0) {
    let items = '';
    expertFlags.forEach(function(f) { items += '<div class="insight-card flag"><span class="insight-icon">💡</span><span>' + f + '</span></div>'; });
    flagsHtml = '<div class="section-label">Insights for Your Counseling Session</div>' + items;
  }

  section.innerHTML =
    '<div class="verdict-banner"><h2>📊 Your Branch Fit Profile</h2><p>' + clarityText + '</p></div>' +
    '<div class="branch-fit"><div class="bf-header">Branch Fit Ranking — Interest + Aptitude</div>' + fitRowsHtml + '</div>' +
    prefHtml +
    '<div class="section-label">Your Skill Profile — 8 Core Engineering Skills</div>' +
    '<div class="branch-fit"><div class="bf-header">Measured from the Skill Aptitude section</div>' + skillRowsHtml + '</div>' +
    gapHtml + buildHtml +
    '<div class="insight-card"><span class="insight-icon">📚</span><span><strong>Branch Knowledge Level: ' + knowledgeLabel + ' (' + knowledgePct + '%)</strong> — ' +
    (knowledgePct >= 67 ? 'You have a realistic understanding of what branches actually involve.' :
     knowledgePct >= 34 ? 'Partial branch knowledge - worth deepening before finalising.' :
     'Limited branch knowledge with misconceptions detected - counseling will clarify your options.') + '</span></div>' +
    collegeHtml + flagsHtml +
    '<div class="section-label">Get Your Full Report</div>' +
    '<div id="submit-status-container"></div>' +
    '<div style="display:flex;gap:0.75rem;flex-wrap:wrap;">' +
    '<button class="btn btn-primary" style="flex:1;min-width:200px;" onclick="emailReport()">📧 Send Report to My Email</button>' +
    '<button class="btn btn-orange" style="flex:1;min-width:200px;" onclick="whatsappReport()">💬 Get Report on WhatsApp</button>' +
    '</div>' +
    '<p style="font-size:0.75rem;color:var(--muted);margin-top:0.75rem;text-align:center;line-height:1.5;">Your full report — branch fit, skill-gap analysis, top 10 colleges and the DASA 2026 schedule — is emailed to you and saved for our counselors to review.</p>';

  setTimeout(function() {
    document.querySelectorAll('.bf-bar').forEach(function(bar) { bar.style.width = bar.dataset.w + '%'; });
  }, 200);

  window.scrollTo({ top:0, behavior:'smooth' });
}

// ═══════ GOOGLE SHEETS ═══════
async function emailReport() {
  const container = document.getElementById('submit-status-container');
  if (GOOGLE_SHEET_URL === 'PASTE_YOUR_APPS_SCRIPT_URL_HERE') {
    container.innerHTML = '<div class="submit-status submit-err"><span>⚠️</span><span>Report service not configured yet. Please WhatsApp us instead.</span></div>';
    return;
  }
  container.innerHTML = '<div class="submit-status submit-wait"><span>⏳</span><span>Sending your report to ' + student.email + ' ...</span></div>';

  const payload = buildPayload();
  try{fetch('/api/leads?source=branch-fitness',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).catch(function(){});}catch(e){}
  try {
    await fetch(GOOGLE_SHEET_URL, { method: 'POST', mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(payload) });
    container.innerHTML = '<div class="submit-status submit-ok"><span>✅</span><span>Your report is on its way to <strong>' + student.email + '</strong> (check spam too). An EduAakashaa counselor will also review it and reach out within 24-48 hours.</span></div>';
  } catch (e) {
    container.innerHTML = '<div class="submit-status submit-err"><span>❌</span><span>Could not send right now - check your connection and try again, or use the WhatsApp button.</span></div>';
  }
}

function whatsappReport() {
  const ranked = getRankedBranches();
  const top = ranked[0], second = ranked[1];
  const prefOrder = getPrefOrder();
  const gapBranchKey = prefOrder.length > 0 ? prefOrder[0] : top.key;
  const gaps = skillGapFor(gapBranchKey).filter(function(g){ return g.gap; });

  // Fire the email/sheet submission in the background too, so WhatsApp users are also captured
  if (GOOGLE_SHEET_URL !== 'PASTE_YOUR_APPS_SCRIPT_URL_HERE') {
    try { fetch(GOOGLE_SHEET_URL, { method:'POST', mode:'no-cors', headers:{'Content-Type':'text/plain'}, body: JSON.stringify(buildPayload()) }); } catch(e) {}
    try{fetch('/api/leads?source=branch-fitness',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(buildPayload())}).catch(function(){});}catch(e){}
  }

  let msg = 'Hi EduAakashaa! I just completed the Engineering Branch Fit Assessment.\n\n';
  msg += 'Name: ' + student.name + '\n';
  msg += 'JEE Rank: ' + (student.jeeRank || 'Not yet') + '\n';
  msg += 'Pathway: ' + (student.pathway || 'Not sure') + '\n\n';
  msg += 'My top branch fit: ' + top.name + ' (' + top.pct + '%)\n';
  msg += '2nd fit: ' + second.name + ' (' + second.pct + '%)\n';
  if (prefOrder.length) msg += 'My preferred branch: ' + BRANCHES[prefOrder[0]].name + '\n';
  if (gaps.length) msg += 'Skill gaps to close: ' + gaps.map(function(g){ return g.name; }).join(', ') + '\n';
  msg += '\nPlease send me my full report and admission guidance. I would also like to know about your Expert Guidance packages.';

  var status = document.getElementById('submit-status-container');
  if (status) status.innerHTML = '<div class="submit-status submit-ok"><span>✅</span><span>Opening WhatsApp... your summary is pre-filled. Your full report is also being sent to your email.</span></div>';

  window.open('https://wa.me/918015722706?text=' + encodeURIComponent(msg), '_blank');
}

// Builds the full payload: flat fields for the Sheet + structured arrays for the email report
function buildPayload() {
  const ranked = getRankedBranches();
  const skillProfile = getSkillProfile();
  const prefOrder = getPrefOrder();
  const recos = recommendColleges(student.jeeRank, [ranked[0].key, ranked[1].key], student.pathway);
  const gapBranchKey = prefOrder.length > 0 ? prefOrder[0] : ranked[0].key;
  const gapsAll = skillGapFor(gapBranchKey);
  const gaps = gapsAll.filter(function(g){ return g.gap; });
  const knowledgePct = Math.round((knowledgeScore/12)*100);

  return {
    // ── Flat fields for the Google Sheet ──
    timestamp: student.timestamp, name: student.name, email: student.email, phone: student.phone,
    country: student.country, board: student.board, jeeStatus: student.jeeStatus,
    jeeRank: student.jeeRank, pathway: student.pathway, statedBranch: student.currentBranch,
    prefOrder: prefOrder.map(function(k){ return BRANCHES[k].name; }).join(' > ') || 'Not ranked',
    topBranch: ranked[0].name + ' (' + ranked[0].pct + '%)',
    secondBranch: ranked[1].name + ' (' + ranked[1].pct + '%)',
    thirdBranch: ranked[2].name + ' (' + ranked[2].pct + '%)',
    allScores: ranked.map(function(b) { return b.name + ': ' + b.pct + '%'; }).join(' | '),
    skillProfile: skillProfile.map(function(s){ return s.name.split(' ')[0] + ': ' + s.pct + '%'; }).join(' | '),
    skillGaps: gaps.length ? gaps.map(function(g){ return g.name + ' (' + g.pct + '%)'; }).join(' | ') : 'None for ' + BRANCHES[gapBranchKey].name,
    knowledgeScore: knowledgePct + '%',
    topColleges: recos ? recos.slice(0,5).map(function(r) { return r.inst + ' - ' + r.prog + ' (' + r.chance + ')'; }).join(' | ') : 'No rank provided',
    expertFlags: expertFlags.join(' || ') || 'None',
    hiddenInsights: hiddenInsights.map(function(h) { return h.note; }).join(' || ') || 'None',
    // ── Structured data for the student email report ──
    sendStudentEmail: true,
    gapBranchName: BRANCHES[gapBranchKey].name,
    reportKnowledge: knowledgePct,
    reportBranchFit: ranked.map(function(b){ return { name: b.name, pct: b.pct }; }),
    reportSkills: skillProfile.map(function(s){ return { name: s.name, pct: s.pct, level: s.level }; }),
    reportGaps: gapsAll.map(function(g){ return { name: g.name, pct: g.pct, level: g.level, gap: g.gap, rec: g.gap ? SKILL_BUILDING[g.skill] : '' }; }),
    reportColleges: recos ? recos.map(function(r){ return { inst: r.inst, prog: r.prog, closing: r.closing, chance: r.chance, src: r.src }; }) : [],
  };
}


RANKS_DATA = RANKS_JSON;

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zkQIAt' }, '*');
	});

	heightObserver.observe(document.documentElement);
