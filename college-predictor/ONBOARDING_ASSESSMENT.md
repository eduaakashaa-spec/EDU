# EduAakashaa Membership Onboarding Assessment
### Class 12 · Engineering (India) · Student + Parent instruments · AI-ready

**Purpose.** Completed by every new member family *before* the first 1-on-1. The student and parent(s)
answer separately (each on their own phone, without comparing answers). A completed pair is pasted into
an AI together with the **AI Analysis Rubric** (Deliverable 2), which produces the **Insight Dossier**
(Deliverable 3) — an identical structure for every family, so consultants can compare clients at a glance.

**Delivery notes (in-app form).**
- Single sitting: student ≈ 28–33 min (70 items shown), parent ≈ 10–15 min (34 items).
- **One account per family.** Both halves are filled behind a login and paired on the account id —
  the student and the parent sign in with the *same* EduAakashaa account. Nothing is matched on
  names or phone numbers any more.
- **Class-gated items.** S61 asks the student's class; the nine NCERT questions then shown are the
  ones for that class (N11* for class 11, N12* for class 12). The other nine are never displayed and
  never stored — treat them as absent, not as blanks.
- One question per screen on mobile; module intros are one line each; no uploads, no manual scoring.
- Items marked **(optional)** may be skipped; everything else is required.
- Ask the family to fill it independently: *"There are no right answers. Please don't compare answers —
  the differences are exactly what makes your first session useful."*

---

## Tag dictionary

Every item carries one primary tag. `ALIGN-*` tags mark dyadic pairs — the same underlying question asked
to both sides; the AI computes the gap.

| Tag | Dimension | Meaning |
|---|---|---|
| `ACAD-CLASS` | Academic reality | Class 11 or 12 — gates which NCERT question set is served |
| `ACAD-MARKS` / `ACAD-TREND` / `ACAD-ENTR` | Academic reality | Reported marks · direction of movement · entrance-mock standing |
| `ACAD-GAP` | Academic reality | Board-exam vs entrance-exam confidence gap |
| `SELFEFF-PHY / -CHE / -MAT` | Academic self-efficacy | Subject-wise belief in own capability (kept separate from marks) |
| `NCERT-PHY / -CHE / -MAT` | Demonstrated knowledge | Board-level NCERT questions actually answered — the objective counterweight to `SELFEFF-*` and self-reported marks |
| `CAL-*` | Calibration | "How sure are you?" follow-ups; scales the certainty of nearby self-ratings |
| `RIASEC-R / -I / -A / -S / -E / -C` | Interests (Holland) | Realistic · Investigative · Artistic · Social · Enterprising · Conventional |
| `RIASEC-ALL` / `RIASEC-OPEN` | Interests | Full ranking item · open-text interest evidence |
| `BIG5-O / -C / -E / -A / -N` | Personality (Big Five) | Openness · Conscientiousness · Extraversion · Agreeableness · Neuroticism |
| `MOTIV-RANK` | Motivation (SDT) | Ranked reasons for engineering (intrinsic → external) |
| `MOTIV-AUTONOMY` | Motivation (SDT) | Own choice vs default/parental expectation |
| `MOTIV-OPEN` | Motivation | Counterfactual narrative ("if not engineering…") |
| `VALUE-RANK` / `VALUE-FC` | Work values | Ranked values · forced-choice dilemmas (security, achievement, autonomy, helping, creativity, prestige) |
| `BRANCH-PREF` | Branch fit | Ranked branch preference |
| `BRANCH-AWARE-*` | Branch awareness | What the student believes a branch actually involves |
| `BRANCH-MYTH` | Branch awareness | True/False misconception check |
| `BRANCH-HERD` | Branch awareness | Herd-bias signal (reasons behind the #1 branch) |
| `ASPIRE-*` / `FEAR` | Aspirations & fears | Ideal future · definition of success · worries |
| `CONSTR-LOC / -BUDGET-AWARE / -BUDGET-EST` | Constraints | Relocation · budget awareness · budget estimate (student side) |
| `PREP-MODE / -CONSIST / -TEMPER / -PLAN` | Prep approach | Coaching vs self-study · consistency · exam temperament · planning |
| `APT-VERBAL / -NUM / -LOGIC / -SPATIAL` | Light aptitude | One brief reasoning sampler each (signal, never a verdict) |
| `SJT-*` | Situational judgement | Realistic dilemma + open rationale |
| `PRESSURE / PRESSURE-EXT / PRESSURE-COMP` | Pressure points | Home tension · relatives' influence · sibling comparison |
| `HIDDEN` / `HIDDEN-P` | Unspoken issues | Optional "what haven't you said out loud" probes |
| `PARENT-KNOW-ADM / -ECO / -QUIZ / -OPEN` | Knowledge audit | Admissions-process familiarity · economics/quality familiarity · truth-check quiz · confusion narrative |
| `PARENT-BUDGET / -LOAN / -BUDGET-TYPE` | Budget | 4-year budget band · loan stance · government-only vs private |
| `PARENT-RISK-*` | Risk appetite | Safe vs ambitious · branch-first vs college-first |
| `PARENT-EXPECT / -RANK / -INVOLVE` | Expectations | What makes membership worth it · service priorities · involvement style |
| `PARENT-CSE` / `PARENT-FLEX-BRANCH` | Branch fixedness | How negotiable CSE / the preferred branch is |
| `ALIGN-BRANCH / -CAREER / -FREEDOM / -BUDGET / -BUDGET-AWARE / -STRENGTH / -INTEREST / -MOTIV / -LOC / -PRESSURE` | Dyadic gaps | Student item ↔ parent item pairs; the gap is the output |

**Response-type shorthand:** `L5` Likert-5 (1 = Strongly disagree … 5 = Strongly agree, unless anchors shown) ·
`FC` forced-choice · `RANK` drag-to-rank · `MCQ` multiple choice (one correct) · `OPEN` free text ·
`SJT` scenario (FC + open "why") · `NUM` number entry.

---

# DELIVERABLE 1 — QUESTION BANK

## STUDENT INSTRUMENT (S1–S61 + NCERT set N11*/N12*)

> *Intro shown in app:* "This helps your counsellor understand the real you — not just your marks.
> There are no right answers, and nothing here is shared without your OK. Answer for yourself, not for
> who you think you should be."

### Module A · Where you stand academically (S61, S1–S8)
*One line intro: "Quick reality check — marks and confidence are different things, and we ask about both."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S61 | Which class are you in right now? **Class 11 · Class 12** (asked first — gates Module A2) | FC | `ACAD-CLASS` | — | — |
| S1 | In your most recent major exam (school/term test), roughly what did you score? — **Physics %** · **Chemistry %** · **Maths %** (three quick entries; estimates are fine) | NUM ×3 | `ACAD-MARKS` | — | P1 |
| S2 | Over the last year, each subject has been… **Physics / Chemistry / Maths:** Improving · Steady · Slipping | FC ×3 | `ACAD-TREND` | — | — |
| S3 | "If I meet a completely new type of **Physics** problem, I can usually crack it if I put in the effort." | L5 | `SELFEFF-PHY` | — | P4 |
| S4 | "If I meet a completely new type of **Chemistry** problem, I can usually crack it if I put in the effort." | L5 | `SELFEFF-CHE` | — | — |
| S5 | "If I meet a completely new type of **Maths** problem, I can usually crack it if I put in the effort." | L5 | `SELFEFF-MAT` | — | P4 |
| S6 | How sure are you about the three ratings you just gave? — Very sure · Fairly sure · Honestly, guessing | FC | `CAL-SELFEFF` | — | — |
| S7 | Right now, which feels more under control? — Board exams · Entrance exams (JEE/state) · Both about equal · Honestly, neither | FC | `ACAD-GAP` | — | — |
| S8 | In recent JEE Main / entrance mocks, your typical score band: 90+ percentile · 80–90 · 70–80 · 50–70 · Below 50 · Haven't taken proper mocks yet | FC | `ACAD-ENTR` | — | — |

### Module A2 · Nine questions from your NCERT syllabus (N11* / N12*)
*Intro: "Three each from Physics, Chemistry and Maths — straight from your NCERT textbook, at board
level. No negative marking, no timer, and your counsellor sees this as a diagnostic, never a verdict.
Please don't look anything up: a wrong answer here is more useful to us than a googled right one."*

Nine of the eighteen below are shown, chosen by **S61**. All are single-correct MCQs pitched at NCERT
board level (not JEE Advanced) — the point is to measure what the student can actually do, instead of
trusting the self-ratings in S3–S5. Correct answers are held server-side and never rendered in the form;
they are injected into the AI bundle at export time.

**Class 11 (shown when S61 = Class 11)**

| # | Item | NCERT chapter | Tag | Answer |
|---|---|---|---|---|
| N11P1 | A ball is thrown at 20 m/s at 30° above the horizontal. Taking g = 10 m/s², its total time of flight is: 1 s · **2 s** · 2.5 s · 4 s | Motion in a Plane | `NCERT-PHY` | 2 s |
| N11P2 | A 5 kg block rests on a rough floor (μ = 0.2) and is pushed by a horizontal 20 N force. Taking g = 10 m/s², its acceleration is: 0 · **2 m/s²** · 4 m/s² · 6 m/s² | Laws of Motion | `NCERT-PHY` | 2 m/s² |
| N11P3 | Escape velocity at Earth's surface is about 11.2 km/s. For a planet of the same density but twice Earth's radius, escape velocity would be about: 5.6 · 11.2 · **22.4** · 44.8 km/s | Gravitation | `NCERT-PHY` | 22.4 km/s |
| N11C1 | How many moles of oxygen atoms are present in 88 g of CO₂? (C = 12, O = 16): 2 · 3 · **4** · 6 | Some Basic Concepts of Chemistry | `NCERT-CHE` | 4 |
| N11C2 | Which of these has the largest atomic radius? **Na** · Mg · Al · Si | Classification of Elements & Periodicity | `NCERT-CHE` | Na |
| N11C3 | The hybridisation of the central atom in BF₃ is: sp · **sp²** · sp³ · sp³d | Chemical Bonding & Molecular Structure | `NCERT-CHE` | sp² |
| N11M1 | The sum of the first 20 terms of the AP 3, 7, 11, … is: 800 · **820** · 840 · 860 | Sequences & Series | `NCERT-MAT` | 820 |
| N11M2 | How many 3-digit numbers can be formed from the digits 1–9 if no digit is repeated? 84 · **504** · 648 · 729 | Permutations & Combinations | `NCERT-MAT` | 504 |
| N11M3 | The value of lim(x→0) sin(3x)/x is: 0 · 1/3 · 1 · **3** | Limits & Derivatives | `NCERT-MAT` | 3 |

**Class 12 (shown when S61 = Class 12)**

| # | Item | NCERT chapter | Tag | Answer |
|---|---|---|---|---|
| N12P1 | Three 6 Ω resistors are connected in parallel. The equivalent resistance is: **2 Ω** · 3 Ω · 9 Ω · 18 Ω | Current Electricity | `NCERT-PHY` | 2 Ω |
| N12P2 | A converging lens of focal length 20 cm forms an image of an object placed 30 cm in front of it. The image distance is: 12 cm · 20 cm · **60 cm** · −60 cm | Ray Optics | `NCERT-PHY` | 60 cm |
| N12P3 | A parallel-plate capacitor has capacitance C. The plate separation is halved and a dielectric of constant 2 fills the gap. The new capacitance is: C · 2C · **4C** · 8C | Electrostatic Potential & Capacitance | `NCERT-PHY` | 4C |
| N12C1 | Which 0.1 m aqueous solution has the highest boiling point? Glucose · Urea · NaCl · **CaCl₂** | Solutions (colligative properties) | `NCERT-CHE` | CaCl₂ |
| N12C2 | The oxidation state of cobalt in [Co(NH₃)₆]Cl₃ is: +1 · +2 · **+3** · +6 | Coordination Compounds | `NCERT-CHE` | +3 |
| N12C3 | For a first-order reaction, the half-life is: directly proportional to the initial concentration · inversely proportional to it · **independent of it** · proportional to its square | Chemical Kinetics | `NCERT-CHE` | Independent of the initial concentration |
| N12M1 | If A is a 3×3 matrix with \|A\| = 2, then \|2A\| is: 4 · 8 · **16** · 32 | Determinants | `NCERT-MAT` | 16 |
| N12M2 | The value of ∫₀^(π/2) cos x dx is: 0 · **1** · −1 · π/2 | Integrals | `NCERT-MAT` | 1 |
| N12M3 | The function f(x) = x³ − 3x has a local maximum at: **x = −1** · x = 0 · x = 1 · x = 3 | Application of Derivatives | `NCERT-MAT` | x = −1 |

### Module B · What actually interests you (S9–S14)
*Intro: "Forget marks for a minute. These are about what you'd enjoy — pick honestly, not strategically."*

Each of S9–S12 shows three activities; pick the one you'd **most** enjoy and the one you'd **least** enjoy.

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S9 | (a) Assemble and fine-tune a drone till it flies right `R` · (b) Figure out *why* a circuit fails when heated `I` · (c) Design how an app looks and feels `A` | FC most/least | `RIASEC-R/I/A` | — | P3 |
| S10 | (a) Teach a junior a topic until it finally clicks `S` · (b) Convince a panel to fund your team's idea `E` · (c) Organise a fest's schedule, budgets and lists so nothing slips `C` | FC most/least | `RIASEC-S/E/C` | — | P3 |
| S11 | (a) Strip and rebuild a two-wheeler engine `R` · (b) Run a stall and beat a sales target `E` · (c) Spend a free afternoon on a maths/physics puzzle nobody assigned `I` | FC most/least | `RIASEC-R/E/I` | — | — |
| S12 | (a) Write/design the college magazine `A` · (b) Keep a lab's records so precise anyone can rely on them `C` · (c) Be the person friends come to with problems `S` | FC most/least | `RIASEC-A/C/S` | — | — |
| S13 | Rank these six from "most like me" (1) to "least like me" (6): Making and fixing real things `R` · Understanding how and why things work `I` · Creating something original `A` · Helping people learn or grow `S` · Leading, pitching, building a venture `E` · Bringing order — systems, data, checklists `C` | RANK | `RIASEC-ALL` | — | P3 |
| S14 | What's something you do where you lose track of time? What exactly pulls you in? (2–3 lines) | OPEN | `RIASEC-OPEN` | — | P2 |

### Module C · How you work (S15–S24)
*Intro: "Ten quick statements. First instinct is best."* (All L5.)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S15 | I enjoy exploring ideas even when they're outside the syllabus. | L5 | `BIG5-O` | — | — |
| S16 | I prefer sticking to methods I already know rather than trying new ways. | L5 | `BIG5-O` | ✔ | S15 |
| S17 | I finish my study plan even when nobody is checking on me. | L5 | `BIG5-C` | — | — |
| S18 | I tend to leave things to the last minute. | L5 | `BIG5-C` | ✔ | S17 |
| S19 | Group work energises me more than working alone. | L5 | `BIG5-E` | — | — |
| S20 | After a day with lots of people, I need quiet time to recharge. | L5 | `BIG5-E` | ✔ | S19 |
| S21 | I adjust easily when a friend wants to do things differently. | L5 | `BIG5-A` | — | — |
| S22 | People say I keep arguing my point even when it upsets others. | L5 | `BIG5-A` | ✔ | S21 |
| S23 | Small setbacks (a bad mock, one poor mark) can spoil my whole day. | L5 | `BIG5-N` | — | — |
| S24 | I stay steady even when an exam goes badly. | L5 | `BIG5-N` | ✔ | S23 |

### Module D · Why engineering — and what matters to you (S25–S32)
*Intro: "The honest version, please — this is the one section where 'because everyone said so' is a perfectly useful answer."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S25 | Rank these reasons for doing engineering, from most true for you (1) to least (6): I genuinely enjoy this kind of problem-solving · It fits what I want to do with my life · I'd feel ashamed/guilty backing out now · The status and respect it brings · My parents/family expect it · The salary and settled life it promises | RANK | `MOTIV-RANK` | — | P5 |
| S26 | "Choosing engineering was mainly **my own** decision." | L5 | `MOTIV-AUTONOMY` | — | P5 |
| S27 | "If it were completely up to me, I might have chosen a different path." | L5 | `MOTIV-AUTONOMY` | ✔ | S26 |
| S28 | Imagine every stream guaranteed you a good college seat. You would: Still pick engineering, no doubt · Probably still engineering · Seriously consider something else · Pick something else | FC | `MOTIV-AUTONOMY` | — | — |
| S29 | If engineering didn't exist, what would you study or become instead? (1–2 lines — "no idea" is a fine answer) | OPEN | `MOTIV-OPEN` | — | — |
| S30 | Rank what matters most in your future work life (1 = most): Stability and security · Being clearly excellent at something · Freedom to decide how I work · Making a difference to people · Building/creating new things · Recognition and prestige | RANK | `VALUE-RANK` | — | — |
| S31 | Pick one: (a) A stable, respected job that rarely changes · (b) An exciting, changing role where some years are uncertain | FC | `VALUE-FC` | — | — |
| S32 | Pick one: (a) ₹25 LPA doing work that bores you · (b) ₹12 LPA doing work you genuinely enjoy | FC | `VALUE-FC` | — | — |

### Module E · Branches — what you know and want (S33–S40)
*Intro: "No trick questions. 'Not sure' is genuinely useful information for your counsellor."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S33 | Rank these branch groups by your current preference (1 = top): CSE/IT/AI-DS · ECE/EEE · Mechanical/Aerospace/Auto · Civil/Environmental · Chemical/Biotech · Something else (name it) | RANK | `BRANCH-PREF` | — | P8 |
| S34 | How settled is your #1 choice? — Fully settled · Fairly settled · Could easily change · I ranked almost at random | FC | `CAL-BRANCH` | — | — |
| S35 | In your own words: what does a **software (CSE) engineer** actually do on a normal working day? (2–3 lines) | OPEN | `BRANCH-AWARE-CSE` | — | — |
| S36 | Same question for **your #1 branch** (skip if it's CSE): what does that engineer do all day? | OPEN | `BRANCH-AWARE-TOP` | — | — |
| S37 | What makes your #1 branch right for *you specifically*? (2–3 lines) | OPEN | `BRANCH-HERD` | — | — |
| S38 | True, False or Not sure: (a) Only CSE/IT students can get software jobs · (b) The "highest package" in college ads is what a typical student gets · (c) Mechanical/Civil careers often peak through GATE, PSUs and higher studies rather than campus mass-hiring · (d) A top NAAC grade guarantees strong placements | FC ×4 | `BRANCH-MYTH` | — | P15 |
| S39 | **SJT.** You get your dream branch at a lower-ranked college, *and* a branch you dislike at a famous college. Which do you take? (a) Dream branch, lower college · (b) Famous college, disliked branch · (c) Genuinely can't say — **and why?** (2–3 lines) | SJT | `SJT-BRANCH` | — | P23 |
| S40 | **SJT.** Suppose your closest friends all lock CSE, but you keep thinking about Mechanical. What do you actually do? (a) Follow CSE — safer together · (b) Pick Mechanical anyway · (c) Try to talk myself out of Mechanical · (d) Something else — **and why?** | SJT | `SJT-HERD` | — | — |

### Module F · Where you hope this goes (S41–S44)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S41 | Describe your **ideal working day ten years from now** — where you wake up, the work you do, the people around you. (3–4 lines; dream freely) | OPEN | `ASPIRE-DAY` | — | P7 |
| S42 | Which feels most like "I've made it" at 30? (pick one): A senior, stable role in a strong company · My own startup/venture · Research or higher studies (IISc/IIT/abroad) · A high-paying job even if the work is routine · Being the respected expert people call first | FC | `ASPIRE-DEF` | — | P7 |
| S43 | What worries you most about the next 12 months? (1–2 lines) | OPEN | `FEAR` | — | — |
| S44 | What do you think your **parents** want for you? Is it the same as what *you* want? (2–3 lines) | OPEN | `ALIGN-CAREER` | — | P10 |

### Module G · Real-life constraints (S45–S50)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S45 | For college, you would honestly prefer: Stay in/near my home town · Anywhere in my state · Anywhere in India — distance no bar · I'd rather not move, but I will if needed | FC | `CONSTR-LOC` | — | P22 |
| S46 | Do you know roughly what your family can spend on your engineering? — Yes, clearly · Roughly · No idea — we've never discussed it | FC | `CONSTR-BUDGET-AWARE` | — | P19 |
| S47 | Your best guess of the total 4-year budget (fees + hostel + everything): Under ₹4 L · ₹4–8 L · ₹8–12 L · ₹12–20 L · ₹20–30 L · Above ₹30 L · Truly no idea | FC | `CONSTR-BUDGET-EST` | — | P17 |
| S48 | In the **final college decision**, how much say do you expect to have? — It'll be fully my call · Mostly mine, parents advise · Truly joint · Mostly my parents' call · Fully my parents' call | FC | `ALIGN-FREEDOM` | — | P11 |
| S49 | "College/exam discussions at home often end in tension." | L5 | `PRESSURE` | — | P29 |
| S50 | **(optional)** Is there anything about your preferences you haven't told your parents yet? It stays between you and your counsellor. | OPEN | `HIDDEN` | — | P34 |

### Module H · How you're preparing (S51–S56)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S51 | Your main prep mode right now: Classroom coaching + school · Online coaching · Mostly self-study · School alone, no extra prep | FC | `PREP-MODE` | — | — |
| S52 | "I follow a fixed weekly study routine." | L5 | `PREP-CONSIST` | — | — |
| S53 | "Honestly, I study seriously only when an exam is close." | L5 | `PREP-CONSIST` | ✔ | S52 |
| S54 | In the actual exam hall, compared to mocks/practice, you usually perform: Better · About the same · Worse · Totally unpredictable | FC | `PREP-TEMPER` | — | — |
| S55 | **SJT.** Two weeks before boards, your JEE mock scores suddenly drop. What do you actually do first — and why? (2–3 lines) | SJT | `SJT-PRESSURE` | — | — |
| S56 | Do you have a written week-by-week plan up to your exams? — Yes, and I mostly follow it · A rough plan in my head · No plan yet | FC | `PREP-PLAN` | — | — |

### Module I · Four quick brain-teasers (S57–S60)
*Intro: "Last four — tiny puzzles, 30–60 seconds each. They're a signal for your counsellor, not a test score."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| S57 | **Blueprint** is to **Building** as **Recipe** is to: Kitchen · Chef · Dish · Menu | MCQ (✓ Dish) | `APT-VERBAL` | — | — |
| S58 | Pump A fills a tank in 6 hours; pump B in 3. Together they take: 2 h · 2.5 h · 3 h · 4.5 h | MCQ (✓ 2 h) | `APT-NUM` | — | — |
| S59 | 5, 9, 17, 33, … what comes next? 49 · 57 · 65 · 66 | MCQ (✓ 65) | `APT-LOGIC` | — | — |
| S60 | A cube is painted on all sides, then cut into 27 identical small cubes. How many small cubes have paint on **exactly two** faces? 6 · 8 · 12 · 24 | MCQ (✓ 12) | `APT-SPATIAL` | — | — |

**Student consistency pairs (for reliability scoring):** S15/S16 · S17/S18 · S19/S20 · S21/S22 · S23/S24 · **S26/S27** · **S52/S53**. Reverse-coded items: S16, S18, S20, S22, S24, S27, S53.

---

## PARENT INSTRUMENT (P1–P34)

> *Intro shown in app:* "You know your child in ways no test can capture. This helps your counsellor
> combine your knowledge with your child's own answers. Please fill it independently — don't compare
> answers; the differences are exactly what we'll work on together. Answer honestly, not ideally."

### Module 1 · Your child, as you see them (P1–P6)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P1 | Rank your child's school subjects by real strength (1 = strongest): Physics · Chemistry · Maths | RANK | `ALIGN-STRENGTH` | — | S1, S3–S5 |
| P2 | Outside studies, what does your child most enjoy doing — and what do they do when nobody is directing them? (2–3 lines) | OPEN | `ALIGN-INTEREST` | — | S14 |
| P3 | Which **two** of these would your child most enjoy? Making/fixing real things · Figuring out why things work · Creating/designing something original · Helping and teaching people · Leading and persuading · Organising things perfectly | FC pick-2 | `ALIGN-INTEREST` | — | S9–S13 |
| P4 | "My child is genuinely confident in Maths and Physics." | L5 | `ALIGN-STRENGTH` | — | S3, S5 |
| P5 | "Engineering was mainly my **child's own** idea." | L5 | `ALIGN-MOTIV` | — | S25–S27 |
| P6 | How sure are you about your answers so far? — Very sure · Fairly sure · Honestly, guessing a bit | FC | `CAL-P` | — | — |

### Module 2 · Your hopes — and your child's (P7–P11)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P7 | Describe the life you hope your child has at 30 — work, place, lifestyle. (2–3 lines) | OPEN | `ALIGN-CAREER` | — | S41, S42 |
| P8 | Which branch do you prefer for your child (CSE/IT · ECE/EEE · Mechanical · Civil · Chemical/Biotech · No preference), **and** how fixed is that? — Must be this branch · Strong preference, open to discussion · Mild preference · Fully my child's choice | FC ×2 | `ALIGN-BRANCH`, `PARENT-FLEX-BRANCH` | — | S33 |
| P9 | About **CSE specifically**: Only CSE makes sense to me · CSE preferred, others acceptable · Whatever fits my child · I actually prefer a non-CSE branch | FC | `PARENT-CSE` | — | S33 |
| P10 | Independently of your hopes — what do you believe your **child** wants? (2–3 lines) | OPEN | `ALIGN-CAREER` | — | S44 |
| P11 | The final college decision should be: My/our call as parents · Parents decide after hearing the child · Truly joint · Child decides after hearing us · Fully my child's call | FC | `ALIGN-FREEDOM` | — | S48 |

### Module 3 · The admissions landscape — honest self-check (P12–P16)
*Intro: "Nobody knows all of this — that's what we're for. Your honest ratings become your session agenda."*
(Scale: 1 = never heard of it · 3 = broadly aware · 5 = could explain it to another parent.)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P12 | Rate your familiarity: (a) JEE Main vs JEE Advanced — what each is for · (b) JoSAA counselling — rounds, choice filling, NIT/IIIT/GFTI routes · (c) Your home-state counselling (e.g. TNEA) — how seats are allotted · (d) Private-university exams (BITSAT, VITEEE, SRMJEEE, COMEDK…) · (e) Management / NRI quota — how it works and what it costs | L5 ×5 | `PARENT-KNOW-ADM` | — | — |
| P13 | Rate your familiarity: (a) Deemed vs autonomous vs affiliated colleges · (b) NAAC / NBA accreditation — what it does and doesn't tell you · (c) Branch-vs-college trade-offs · (d) Placement realities — median vs "highest package" · (e) Education loans and scholarships | L5 ×5 | `PARENT-KNOW-ECO` | — | — |
| P14 | Quick check — in JoSAA counselling, NIT seats are allotted mainly on: JEE Advanced rank · **JEE Main rank** · Class 12 marks alone · College interviews | MCQ (✓ JEE Main rank) | `PARENT-KNOW-QUIZ` | — | — |
| P15 | True or False: "The 'highest package' a college advertises is a good estimate of what a typical student there earns." | MCQ (✓ False) | `PARENT-KNOW-QUIZ` | — | S38 |
| P16 | Which part of the whole admissions process feels most confusing or worrying right now? (2–3 lines) | OPEN | `PARENT-KNOW-OPEN` | — | — |

### Module 4 · Budget — the practical picture (P17–P21)
*Intro: "A realistic budget shapes the entire strategy. This stays confidential."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P17 | Total 4-year budget you can realistically commit (fees + hostel + everything): Under ₹4 L · ₹4–8 L · ₹8–12 L · ₹12–20 L · ₹20–30 L · Above ₹30 L · Not yet decided | FC | `PARENT-BUDGET`, `ALIGN-BUDGET` | — | S47 |
| P18 | An education loan is: Something we'd take comfortably · Acceptable if genuinely needed · A last resort · Not an option for us | FC | `PARENT-LOAN` | — | — |
| P19 | Does your child know this budget? — Yes, exactly · Roughly · No — we haven't discussed money with them | FC | `ALIGN-BUDGET-AWARE` | — | S46 |
| P20 | Your honest starting position: Government/aided colleges only · Prefer government, private if clearly better · Open to any college that fits · Prefer reputed private colleges | FC | `PARENT-BUDGET-TYPE` | — | — |
| P21 | **SJT.** The college that fits your child best costs ~30% more than your budget. What would you actually do — and why? (2–3 lines) | SJT | `SJT-P-BUDGET` | — | — |

### Module 5 · Risk appetite (P22–P25)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P22 | How far are you comfortable sending your child? — Day-scholar distance only · Within our state · Anywhere in India · Depends entirely on the college | FC | `ALIGN-LOC` | — | S45 |
| P23 | If forced to choose: (a) The **right branch** at a less famous college · (b) The **famous college**, whatever branch it offers — **and why?** (1–2 lines) | SJT | `PARENT-RISK-BC` | — | S39 |
| P24 | **SJT.** Results day: your child's rank is well below hope. Your instinct? (a) Take the best seat available this year · (b) A repeat year for a better rank · (c) Depends — on what? — **why?** (1–2 lines) | SJT | `PARENT-RISK-REPEAT` | — | — |
| P25 | "A well-known college near home is always the safer choice than a better-fit college far away." | L5 | `PARENT-RISK-SAFE` | ✔ | P22, P23 |

### Module 6 · Working with us (P26–P28)

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P26 | Twelve months from now, what would make you say this membership was **completely worth it**? (2–3 lines) | OPEN | `PARENT-EXPECT` | — | — |
| P27 | Rank what you need most from us (1 = highest): Building the right college list · Branch guidance for my child · Forms, deadlines and counselling-round execution · Helping my child and me get on the same page | RANK | `PARENT-EXPECT-RANK` | — | — |
| P28 | Your preferred involvement: Involve me in every step · Key decisions only · Work mainly with my child, keep me posted · Guide us, but we decide everything ourselves | FC | `PARENT-EXPECT-INVOLVE` | — | — |

### Module 7 · The home front (P29–P34)
*Intro: "Last section — the household reality. Honest answers help us help you; nothing is judged."*

| # | Item | Type | Tag | Rev | Pair |
|---|---|---|---|---|---|
| P29 | "College/exam discussions at home often end in tension." | L5 | `ALIGN-PRESSURE` | — | S49 |
| P30 | "Opinions of relatives and family friends carry real weight in this decision." | L5 | `PRESSURE-EXT` | — | — |
| P31 | "My child ends up being compared with siblings/cousins on academics." | L5 | `PRESSURE-COMP` | — | — |
| P32 | "Whichever branch my child finally chooses, I will back it." | L5 | `PARENT-FLEX-BRANCH` | ✔ | P8, P9 |
| P33 | "Honestly, without my push, my child would not take this decision seriously." | L5 | `ALIGN-MOTIV` | ✔ | P5 |
| P34 | **(optional)** Is there anything about this decision you haven't been able to discuss openly with your child? It stays with your counsellor. | OPEN | `HIDDEN-P` | — | S50 |

**Parent consistency pairs (for reliability scoring):** **P5/P33** · **P8+P9/P32** · **P22+P23/P25**. Reverse-coded items: P25, P32, P33.

---

# DELIVERABLE 2 — AI ANALYSIS RUBRIC

*Consultant instructions: paste the block below into the AI, followed by the completed student and parent
responses (item numbers + answers). The block is self-contained.*

```text
YOU ARE the analysis engine for EduAakashaa (evidence-based college counselling, India).
You receive one family's completed onboarding assessment: STUDENT items S1–S61 plus a nine-
question NCERT set (N11* for a class-11 student, N12* for a class-12 student — only one set is
ever present, per S61), and PARENT items P1–P34. Each scored item arrives with its correct
answer and whether the student got it RIGHT or wrong appended in square brackets; use that
marking, never re-derive it yourself. Produce ONE Insight Dossier in EXACTLY the template at
the end.

NON-NEGOTIABLE RULES
1. Never invent data. If an item is blank, write "Not answered". Do not guess missing marks,
   budgets or feelings.
2. Quote each respondent verbatim at least once per dossier section where open text exists;
   put quotes in quotation marks and mark the item number, e.g. (S41).
   CONFIDENTIALITY EXCEPTION: items S50 and P34 are promised confidential to the person who
   answered them. NEVER quote OR paraphrase S50 or P34 anywhere in the dossier; they feed
   only the single counsellor-only flag line in §7. Rule 2 does not apply to them.
3. This is not a clinical instrument. Never diagnose, never use psychiatric language. Describe
   tendencies ("tends to", "reports"), not fixed traits.
4. Neutral, warm, parent-readable language. No hype, no jargon without a plain-language gloss.
5. Where a calibration item (S6, S34, P6) says "guessing", soften every claim built on the
   related answers ("student's own confidence in this rating is low").

TAG DICTIONARY (what each dimension means)
ACAD-*: reported marks/trend/mock band; SELFEFF-*: subject self-efficacy (belief, not marks);
CAL-*: how sure the respondent is; RIASEC-R/I/A/S/E/C: Holland interest themes; BIG5-O/C/E/A/N:
Big Five; MOTIV-*: Self-Determination-Theory motivation (autonomous vs controlled);
VALUE-*: work values; BRANCH-*: branch preference/awareness/misconceptions/herd bias;
ASPIRE/FEAR: aspirations and worries; CONSTR-*: constraints; PREP-*: study habits;
APT-*: light reasoning sampler; SJT-*: situational judgement; PRESSURE*: home pressure;
HIDDEN*: unspoken issues; PARENT-KNOW-*: admissions knowledge audit; PARENT-BUDGET/LOAN/
BUDGET-TYPE: money; PARENT-RISK-*: risk appetite; PARENT-EXPECT*: expectations of consultant;
ALIGN-*: student↔parent paired items — compute the gap.

SCORING PROCEDURES

A. RIASEC code (S9–S13)
   Triads S9–S12: "most" = +2 to that letter, "least" = −1. Letters per option are marked in
   the item bank (S9: a=R b=I c=A; S10: a=S b=E c=C; S11: a=R b=E c=I; S12: a=A b=C c=S).
   Ranking S13: rank1=+5, rank2=+4, rank3=+3, rank4=+2, rank5=+1, rank6=0 to each letter.
   Sum per letter → 3-letter code from the top three. Tie-break: more triad "most" picks wins;
   if still tied, show both letters ("RI(E/C)"). If max−min ≤ 3 across all six letters, add
   flag "flat interest profile — treat code as weak signal". Use S14's open text as evidence
   for or against the code and say so explicitly.

B. Big Five (S15–S24)
   Reverse-score S16, S18, S20, S22, S24 as (6 − x). Trait score = mean of its two items:
   O=(S15,S16r) C=(S17,S18r) E=(S19,S20r) A=(S21,S22r) N=(S23,S24r).
   Bands: ≤2.4 Low · 2.5–3.5 Moderate · ≥3.6 High. Report each trait as one line:
   band + what it means for counselling this student (e.g. high N + entrance pressure →
   plan mock-exam routine early). Never present as a fixed personality verdict.

C. Academic standing (S1–S8)
   For each PCM subject build a marks×self-efficacy quadrant:
   marks ≥75% & SE ≥4 → "solid"; marks ≥75% & SE ≤3 → "under-confident (hidden strength)";
   marks <60% & SE ≥4 → "over-confident — verify with mocks/aptitude"; marks <60% & SE ≤3 →
   "development zone"; else "steady middle". Add trend (S2) as an arrow ↑→↓.
   Note the board-vs-entrance gap (S7) and mock band (S8). If S8 = "no proper mocks yet"
   AND JEE ambitions appear anywhere, raise a red flag.

C2. NCERT diagnostic (N11*/N12*, gated by S61)
   Only one class's set is present. Score 1 point per item marked RIGHT; unanswered = 0 but
   say so. Report per subject out of 3 — Physics (…P1–P3), Chemistry (…C1–C3), Maths (…M1–M3)
   — and a total out of 9. Bands per subject: 3/3 "secure" · 2/3 "workable" · ≤1/3 "gap".
   These are NINE board-level questions, not an exam. Never call a band a verdict, never
   convert it to a percentage or a predicted rank, and never let it override S1 marks: it is
   one signal to triangulate with, and say that in the dossier.

C3. Calibration: claimed vs demonstrated (the point of C2)
   For each subject compare the self-efficacy rating (S3 Physics / S4 Chemistry / S5 Maths)
   against that subject's NCERT band, and name the gap:
   - SE ≥4 and band "gap"          → OVER-CLAIMING. The most action-worthy finding in the
     dossier: the student believes a subject is handled and the evidence disagrees. Phrase it
     for a 17-year-old to read without shame ("rates Maths a 4 but the three NCERT questions
     didn't land — worth an early diagnostic, not a worry").
   - SE ≤2 and band "secure"       → UNDER-CLAIMING / hidden strength. Say so plainly; this
     student is likely talking themselves out of a branch they can do.
   - SE and band agree             → CALIBRATED. One line, no drama; this is good news and it
     makes every other self-report in the instrument more trustworthy — say that.
   Weight the whole comparison down if S6 = "Honestly, guessing" (the student told you the
   ratings were noise) and mention that you did.
   If S1 marks and the NCERT band disagree sharply (e.g. 85% reported, 0/3 demonstrated),
   flag "self-reported marks unverified" for the counsellor — state the discrepancy, do NOT
   accuse the student of inflating anything.

D. Motivation type (S25–S29 + parent P5/P33)
   From S25 ranks give points rank1=5 … rank6=0.
   Autonomous = points(enjoy problem-solving) + points(fits my life).
   Controlled = points(shame/guilt) + points(status) + points(family expectation) + points(salary).
   Then classify:
   - "Self-driven": Autonomous > Controlled AND S26 ≥ 4 AND S28 ∈ {still engineering, probably}.
   - "Aligned but guided": Autonomous ≥ Controlled AND external signals present (S26 ≤ 3 OR
     family expectation ranked ≤ 3rd).
   - "Complying": Controlled > Autonomous OR S27 ≥ 4 OR S28 ∈ {seriously consider else, pick else}.
   - "Conflicted / default": signals contradict each other (e.g. S26 ≥4 AND S27 ≥4) — say so.
   Use S29 ("if not engineering…") as narrative evidence. Cross-check with parent P5/P33 —
   disagreement on whose idea engineering was is an ALIGN-MOTIV gap (see F).

E. Values (S30–S32)
   Top-2 from S30 = headline values. S31/S32 confirm or contradict: e.g. top value "Stability"
   but S32 picks the ₹12 LPA passion job → note the tension verbatim. Report top-2 + any tension.

F. ALIGNMENT MAP — compute every row (the highest-value output)
   For each pair output status 🟢 aligned / 🟡 partly / 🔴 conflict + one line of evidence per side.
   - ALIGN-BRANCH: S33 rank-1 vs P8 preference (+ P9 CSE stance + P32). Same branch family → 🟢.
     Adjacent openness ("mild preference") → 🟡. "Must be this branch" vs different S33 top → 🔴.
   - ALIGN-CAREER: S41/S42/S44 vs P7/P10. Judge semantic match of life pictures. Also score
     the EMPATHY GAP: does P10 (parent's guess of child's want) actually match what the child
     wrote in S41/S44? Mismatch → 🔴 empathy gap, quote both.
   - ALIGN-FREEDOM: map S48 and P11 onto 1–5 (1 = fully parents … 5 = fully child).
     |diff| 0–1 → 🟢, 2 → 🟡, ≥3 → 🔴.
   - ALIGN-BUDGET: S47 band vs P17 band. Same/adjacent band → 🟢/🟡, ≥2 bands apart or student
     "truly no idea" while parent has decided → 🔴. ALIGN-BUDGET-AWARE: S46 vs P19 must agree;
     "child knows exactly" (P19) + "no idea" (S46) → 🔴 and name it plainly.
   - ALIGN-STRENGTH: P1 ranking + P4 vs S1 marks and S3–S5 self-efficacy. Parent's #1 subject
     = child's weakest marks/SE → 🔴.
   - ALIGN-INTEREST: P2/P3 vs student RIASEC code + S14. Overlap of themes → 🟢.
   - ALIGN-MOTIV: P5 vs S26/S27 (and P33). Both say child's own idea → 🟢; parent says child's
     idea but student says "might have chosen differently" → 🔴 (hidden compliance).
   - ALIGN-LOC: S45 vs P22. Student "anywhere in India" vs parent "day-scholar only" → 🔴.
   - ALIGN-PRESSURE: S49 vs P29. Student ≥4 while parent ≤2 → 🔴 "tension invisible at home".

G. Branch awareness & herd bias (S35–S38 + S33/S34)
   Score S35 and S36 descriptions 0–2: 0 = wrong/empty/filmi ("hacking all day"), 1 = partial
   ("coding" with no texture), 2 = specific & realistic (mentions teamwork, debugging, projects,
   sites, design work etc.). Herd index from S37 + S40: reasons ONLY about placements, salary,
   friends, family or prestige → HIGH herd; concrete pull toward the work itself → LOW.
   Myth check S38 key: (a) False (b) False (c) True (d) False — each wrong/unsure answer is a
   misconception to correct in session 1. Parent quiz P14 (✓ JEE Main rank) and P15 (✓ False)
   feed the parent knowledge section.

H. Aptitude sampler (S57–S60)
   Key: S57 Dish · S58 2 h · S59 65 · S60 12. Report per-domain right/wrong in one line and
   the count (e.g. 3/4). This is a 4-item signal: describe as "directional only". NEVER call
   it IQ, never let one wrong answer override strong marks; DO flag a pattern (e.g. numerical+
   logical wrong AND weak maths SE AND falling maths trend).

I. Parent knowledge audit (P12–P16)
   List every sub-item rated ≤ 2 — that IS the session agenda, in the parent's own priority
   order (lowest first). Overconfidence check: quiz item wrong while related familiarity
   rated ≥ 4 → flag "confident but incorrect on X — handle gently". Quote P16 verbatim.

J. RELIABILITY / QUALITY FLAGS (compute before writing anything)
   Consistency pairs (expect opposite directions): S15/S16, S17/S18, S19/S20, S21/S22,
   S23/S24, S26/S27, S52/S53; P5/P33, (P8+P9)/P32, (P22+P23)/P25.
   A pair is CONTRADICTED when both sides ≥4 or both ≤2 (after noting the second item is
   reverse-worded). Also flag: straight-lining (≥90% of an instrument's Likert answers
   identical), all-maximum self-presentation (every self-rating at ceiling with no admitted
   weakness anywhere), and blank-heavy sections (>25% skipped).
   Instrument confidence: High = 0 contradictions, Medium = 1, Low = ≥2 or straight-lining.
   State the confidence level at the top of the dossier and soften wording accordingly.

OUTPUT
Fill the INSIGHT DOSSIER template EXACTLY as given: same section numbers, same headings, same
order, no extra sections, no renaming. Every section ≤ 180 words except §6 (talking points),
which is 3–4 bullets of ≤ 40 words each. Use the emoji status marks only where the template
shows them. If either instrument is missing entirely, produce the dossier from the available
side and mark every dyadic row "single-sided — gap unknown".
```

---

# DELIVERABLE 3 — INSIGHT DOSSIER TEMPLATE

```markdown
# INSIGHT DOSSIER — {Student name} · Class 12 · {City}
Prepared {date} · Student instrument: {complete/partial} · Parent instrument: {complete/partial}
Data confidence: {High/Medium/Low} — {one-line reason if not High}

## 1. Snapshot
- Holland code: {XYZ} {(+ "flat profile" flag if applicable)} — one-line meaning
- Big Five: O {band} · C {band} · E {band} · A {band} · N {band} — one line on the two most
  counselling-relevant traits
- Top values: {value 1}, {value 2} {± tension note}
- Motivation type: {Self-driven / Aligned but guided / Complying / Conflicted-default} —
  one-line evidence with quote
- One sentence: who this student is, in plain words.

## 2. Academic standing
*Class {11/12} (S61) — NCERT set {N11*/N12*}*

| Subject | Marks | Trend | Self-efficacy | NCERT | Calibration | Read |
|---|---|---|---|---|---|---|
| Physics | {…} | {↑→↓} | {…}/5 | {n}/3 {secure/workable/gap} | {calibrated / over-claiming / under-claiming} | {solid / hidden strength / over-confident / development zone / steady} |
| Chemistry | … | … | … | … | … | … |
| Maths | … | … | … | … | … | … |
- NCERT diagnostic total: {n}/9 — nine board-level questions, a signal to triangulate, not a verdict
- Calibration headline: {the single most action-worthy claimed-vs-demonstrated gap, or "well calibrated
  across all three — treat this student's self-reports as reliable"}
- Board vs entrance: {S7 + S8 summary}
- Aptitude sampler: {n}/4 ({domains wrong}) — directional signal only
- Red flags: {none / list}

## 3. Alignment map (student ↔ parent)
| Dimension | Status | Student says | Parent says |
|---|---|---|---|
| Branch | 🟢/🟡/🔴 | {evidence} | {evidence} |
| Career picture | 🟢/🟡/🔴 | … | … |
| Empathy gap (does parent know what child wants?) | 🟢/🟡/🔴 | … | … |
| Decision freedom | 🟢/🟡/🔴 | … | … |
| Budget estimate | 🟢/🟡/🔴 | … | … |
| Budget awareness | 🟢/🟡/🔴 | … | … |
| Strengths & interests | 🟢/🟡/🔴 | … | … |
| Whose idea was engineering | 🟢/🟡/🔴 | … | … |
| Location/relocation | 🟢/🟡/🔴 | … | … |
| Pressure perception | 🟢/🟡/🔴 | … | … |
Biggest single gap to address first: {one line}.

## 4. What the parents know / don't know → session agenda
- Comfortable with: {list of ≥4-rated areas}
- Gaps to teach (session agenda, in order): {every area rated ≤2, lowest first}
- Overconfidence alerts: {quiz-vs-rating mismatches, or "none"}
- In their words: "{P16 quote}"

## 5. Budget & constraints
- 4-year budget: {P17} · Loan stance: {P18} · College type: {P20}
- Student's picture of the money: {S46/S47 vs P17/P19 in one line}
- Location: {S45 vs P22 in one line}
- Other constraints: {anything from S43 that constrains choices — do NOT pull in S50/P34,
  which are confidential and handled only in §7}

## 6. Recommended 1-on-1 talking points (3–4 bullets)
- {The specific conversation this family needs first, with the item evidence in brackets}
- …
- …

## 7. Risk flags
- Misconceptions to correct: {from S38 wrong answers, S35/S36 scores, P14/P15}
- Herd-bias risk: {high/moderate/low + one-line evidence}
- Reliability cautions: {contradicted pairs / straight-lining / "none"}
- Hidden pressure (from pressure items S49/P29–P31 only): {summarise sensitively}
- Confidential item present: {student / parent / both / none} — where present, "raise
  privately with that respondent first". Do NOT quote, paraphrase, or reveal the content
  of S50/P34 anywhere in this dossier; this line only signals that a private note exists.
```

> **Audience note.** Treat the whole dossier as potentially family-visible. Nothing
> counsellor-only may appear in it except the single "Confidential item present" signal
> above (which names *that* a note exists, never *what* it says).

---

### Design rationale (for the EduAakashaa team — not shown to families)

- **Forced-choice everywhere signal matters.** RIASEC (most/least triads + one ranking), motivation
  reasons, values and branch preference are all ranked or forced — Likert is reserved for traits,
  efficacy and pressure, where intensity genuinely matters.
- **Marks ≠ confidence, by construction.** S1 (marks) and S3–S5 (self-efficacy) are scored into
  quadrants; "hidden strength" and "over-confident" cells change the counselling conversation more
  than either number alone.
- **The dyad is the product.** Ten ALIGN rows, each traceable to a numbered pair. The empathy-gap row
  (P10 vs S41/S44) catches the most common failure: parents who know their hopes but not their child's.
- **Herd bias is measured, not assumed.** S37's "why this branch for YOU", S40's friends-lock-CSE
  dilemma and the S35/S36 realism scores triangulate whether CSE preference is informed or inherited.
- **Reliability is built in.** Seven student and three parent consistency pairs, straight-lining and
  ceiling checks, and calibration items that downgrade certainty instead of discarding data.
- **Sensitive items are protected.** S50/P34 are optional, flagged confidential, and the rubric
  forbids quoting them into parent-facing copy.
