"""Mentorship programme — email and WhatsApp message templates.

Source material: the Elite Mentorship brochure (Grade 12 NRI, Class of 2027) and the
2027 Student Success / Mentorship guides (October 2026 editions). Every template
uses [Square Bracket] placeholders for the counsellor to fill. Facts quoted here
(fee, sessions, rules) come from those documents — re-check them each cycle.

Structure:  GROUPS -> list of {id, title, when, templates:[{label, channel, subject, body}]}
channel is "email" or "whatsapp".
"""

SIG_EMAIL = """Warm regards,
[Your Name]
[Designation], EduAakashaa
+91 80157 22706 (Phone / WhatsApp) · info@eduaakashaa.com · www.eduaakashaa.in
Guiding students towards the right future"""

SIG_WA = "— [Your Name], EduAakashaa"

UNSUB = "You are receiving this because you enquired with EduAakashaa. Reply STOP to be removed from our mailing list."

GROUPS = [
    # ------------------------------------------------------------------
    {
        "id": "marketing",
        "title": "1 · Marketing & promotion",
        "blurb": "Outbound campaigns to Grade 11–12 families in India and the Gulf. Always include the opt-out line.",
        "items": [
            {
                "id": "promo-launch",
                "title": "Promotional email — programme launch",
                "when": "Campaign to new leads / newsletter list. Send Tue–Thu, 6–8 pm Gulf time.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Grade 12 in the Gulf? One mentor, one plan, one seat decision — Class of 2027",
                        "body": """Dear [Parent Name],

A Grade 12 student in the Gulf is preparing for boards and JEE Main while five or more Indian admission systems run on separate calendars — DASA, CIWG, JoSAA, state and private NRI routes, and design/architecture tests. Most families do not lose seats to marks. They lose them to a missed rule or a late start.

EduAakashaa Elite Mentorship puts one senior mentor beside your family from enrolment to the seat decision:

• A dedicated 1:1 senior mentor, supported by a domain mentor and an admissions specialist
• Minimum 10 virtual 1:1 sessions per student
• Nine strategy deliverables — baseline assessment, live admissions roadmap, target college list (reach / match / safe), DASA-CIWG and JoSAA choice-filling strategy pack, final seat decision brief and more
• Premium portal, choice-filling simulator and DASA analytics for one year
• Time-zone-friendly mentoring for Gulf families

Did you know? DASA went from three rounds to two in 2026, and closing ranks moved in opposite directions by quota — CIWG got tougher, Non-CIWG eased. Families planning from last year's PDF are planning for a process that no longer exists.

Book a free 20-minute mentorship conversation — by video call, telephone or in person in Coimbatore:
[Booking link]  ·  WhatsApp +91 80157 22706

The best time to begin was Grade 11. The next best time is today.

""" + SIG_EMAIL + """

Note: EduAakashaa guides the process. No rank, score or seat is guaranteed; admission is decided by the authorities on rank and eligibility.
""" + UNSUB,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hello [Parent Name] 👋

Is your child in Grade 12 in the Gulf and aiming for an NIT / IIIT / IIT seat in 2027?

Most NRI families don't lose seats to marks — they lose them to a missed rule or a late start.

EduAakashaa *Elite Mentorship* gives you:
✅ One dedicated senior mentor, start to finish
✅ 10+ virtual 1:1 sessions
✅ A live admissions roadmap for DASA, CIWG, JoSAA & state routes
✅ Choice-filling strategy + final seat-decision brief

📅 Book a free 20-min conversation: [Booking link]

""" + SIG_WA + """
_(Guidance only — no seat or rank is guaranteed. Reply STOP to opt out.)_""",
                    },
                ],
            },
            {
                "id": "promo-data",
                "title": "Promotional email — data hook (DASA 2026 closing ranks)",
                "when": "Second touch to leads who opened the launch email. Pair with the premium DASA 2026 Analytics page.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "CIWG cut-offs tightened 8%. Non-CIWG eased 18%. What it means for 2027",
                        "body": """Dear [Parent Name],

We compared every DASA programme's final closing rank, 2026 against 2025, across 378 programmes:

• CIWG: the median closing rank fell about 8% — a tougher cut-off
• Non-CIWG: the median closing rank rose about 18% — an easier cut-off
• Computer / IT / AI eased, while Civil, Bio/Food and Chemical/Materials tightened the most — core branches are no longer a safe fallback

What this means for the Class of 2027: a CIWG-eligible student should plan for a better rank than last year's cut-off, not the same one — and the shortlist should be built on three to four years of trends, never on one closing rank.

Your mentor builds that shortlist with you. Book a free conversation: [Booking link]

""" + SIG_EMAIL + """

These are planning estimates from DASA 2025 (after Round 3) and DASA 2026 (after Round 2) OPEN gender-neutral seats — not guarantees of admission.
""" + UNSUB,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name],

📊 DASA 2026 vs 2025, across 378 programmes:
• CIWG closing ranks got *tougher* (~8%)
• Non-CIWG got *easier* (~18%)
• Core branches tightened the most

Planning for 2027? Don't use last year's cut-off — use 3–4 years of trends. We'll build your child's shortlist with you.

Free conversation: [Booking link]
""" + SIG_WA,
                    },
                ],
            },
            {
                "id": "promo-myth",
                "title": "Myth-buster message (parent groups)",
                "when": "Forwardable WhatsApp card for parent communities. Keep factual; cite the official brochure.",
                "templates": [
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """*3 DASA myths that cost NRI families a seat* 🚫

❌ "DASA admission is on SAT scores."
✅ Seats are allotted on the JEE Main CRL rank. SAT is not used.

❌ "Any child living in the Gulf gets CIWG."
✅ CIWG is for NRI students with a parent working in a listed Gulf country. OCI/PIO students apply under general DASA.

❌ "We'll move to India for Grade 12 and still apply."
✅ Classes 11 *and* 12 must both be completed abroad. The move ends DASA eligibility.

Rules above are from the DASA 2026 brochure; the 2027 brochure is awaited. Unsure about your child's eligibility? Ask us — [Booking link]

""" + SIG_WA,
                    }
                ],
            },
            {
                "id": "promo-webinar",
                "title": "Webinar / parent briefing invitation",
                "when": "Lead-generation event, 45 minutes + Q&A.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Free parent briefing: JEE 2027 → JoSAA → DASA, explained in 45 minutes",
                        "body": """Dear [Parent Name],

You are invited to a free live briefing for Grade 11–12 NRI families:

📅 [Date] · 🕗 [Time] IST / [Time] Gulf time · 🔗 [Link]

What we will cover:
1. The 2027 calendar — JEE Main sessions, JEE Advanced, JoSAA, DASA/CSAB
2. Who qualifies for DASA and CIWG (the residency and 75% rules)
3. What the 2026 closing-rank data says about 2027
4. The documents to prepare now
5. Open Q&A with a senior mentor

Seats are limited. Reserve yours: [Registration link]

""" + SIG_EMAIL + "\n" + UNSUB,
                    },
                    {
                        "label": "WhatsApp (invite)",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hello [Parent Name] 👋

You're invited to our *free parent briefing* — JEE 2027 → JoSAA → DASA/CIWG, in 45 minutes.

📅 [Date] · 🕗 [Time] IST / [Time] Gulf
🔗 Register: [Registration link]

Topics: 2027 calendar · eligibility rules · 2026 closing-rank data · documents to prepare now · live Q&A.

""" + SIG_WA,
                    },
                    {
                        "label": "WhatsApp (1-hour reminder)",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """⏰ Reminder: our parent briefing starts in 1 hour — [Time] IST / [Time] Gulf.
Join here: [Link]
See you there! """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "promo-reengage",
                "title": "Re-engagement — cold leads",
                "when": "Leads with no response for 30+ days; or after JEE Main Session 1 result.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Where does [Student Name]'s plan stand after JEE Main Session 1?",
                        "body": """Dear [Parent Name],

With JEE Main Session 1 [about to begin / now behind us], the next 90 days decide a lot: Session 2 strategy, the Class 12 board result against the 75% rule, and the document file for DASA/CIWG.

If you would like a second pair of eyes on where [Student Name] stands, a 20-minute conversation with a senior mentor is free and there is no obligation: [Booking link].

""" + SIG_EMAIL + "\n" + UNSUB,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], just checking in — the next 90 days decide a lot for the Class of 2027 (Session 2 strategy, board marks vs the 75% rule, document file).

Would a free 20-min conversation help? [Booking link]
""" + SIG_WA,
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    {
        "id": "enquiry",
        "title": "2 · Enquiry handling & enrolment",
        "blurb": "From first enquiry to signed engagement. Reply within 2 working hours where possible.",
        "items": [
            {
                "id": "enquiry-response",
                "title": "Response to enquiry",
                "when": "Immediately after a website / WhatsApp / call-back enquiry.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Thank you for your enquiry — EduAakashaa Mentorship",
                        "body": """Dear [Parent Name],

Thank you for reaching out to EduAakashaa about [Student Name]'s admission journey. I'm [Your Name], and I'll be your first point of contact.

From what you shared — [Grade / Board / Country of schooling / Routes of interest] — here is a quick orientation:

• Routes likely relevant for [Student Name]: [DASA / CIWG / JoSAA / TNEA / private NRI]
• Our one-to-one tier, Elite Mentorship, covers all eligible routes in parallel with a dedicated senior mentor
• The first step is a free initial discussion (about 20–30 minutes) where we record your inputs and expectations

Could you suggest a time that suits you this week? I can offer [Option 1], [Option 2] or [Option 3] — IST / Gulf time.

To make the conversation useful, it helps to have the following handy:
1. Student's current grade, board and latest marks
2. Country of schooling for Classes 11 and 12
3. Nationality / passport status (Indian, OCI/PIO, other) and parent's work country
4. Any colleges, branches or routes already on your mind

Looking forward to speaking with you.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hello [Parent Name], thank you for contacting EduAakashaa 🙏

I'm [Your Name]. I understand you're looking for guidance for [Student Name] (Grade [__], [Country]).

To help you best, could you share:
1️⃣ Latest marks / board
2️⃣ Country of schooling for Classes 11–12
3️⃣ Passport status & parent's work country
4️⃣ Routes you're considering

When is a good time for a quick 20-min call — [Option 1] or [Option 2]?
""" + SIG_WA,
                    },
                ],
            },
            {
                "id": "scope",
                "title": "Sharing the scope of the mentorship",
                "when": "After the discovery call, before the engagement agreement.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Scope of Elite Mentorship for [Student Name] — what's included (and what isn't)",
                        "body": """Dear [Parent Name],

It was a pleasure speaking with you and [Student Name]. As promised, here is what Elite Mentorship includes, so you can decide with the full picture.

THE PROGRAMME
Grade 12 track · 10–12 months · three phases — Foundation + Build, Target, Execute — delivered through our 5A method: Assess → Analyze → Advise → Apply → Achieve.

IN SCOPE
• Admissions strategy across all eligible routes (DASA, CIWG, JEE Main, JoSAA/CSAB, TNEA and state routes) with a live deadline and document calendar
• A living roadmap, revised each term
• Minimum 10 virtual 1:1 sessions with a lead counsellor, a domain mentor and an admissions specialist
• Form preparation, verification and deadline tracking (the family authorises and submits)
• Parent briefings with written summaries
• Premium portal access for one year, choice-filling simulator and analytics reports (all NITs/IIITs, DASA 2027)

NINE STRATEGY DELIVERABLES
1. Onboard Assessment · 2. Baseline Assessment and Eligibility Report · 3. Admissions Roadmap · 4. Document and Deadline Calendar · 5. Termly Progress and Course-Correction Notes · 6. Target College and Branch List (reach, match, safe) · 7. DASA/CIWG and JoSAA Choice-Filling Strategy Pack · 8. Final Seat Decision Brief · 9. Parent Guidance Report and briefing summaries

OUT OF SCOPE
• Subject tuition and JEE coaching — this is mentorship, not coaching
• Guaranteed ranks, scores or seats — no outcome is guaranteed
• Submitting forms without family sign-off
• Visa, passport and immigration processing
• Financial, loan or forex advice

Anything beyond this scope (for example, admission support for named institutions) is agreed per family and written into the engagement document with its price.

PROGRAMME FEE
₹74,999 including GST (Grade 12 track). Payment schedule: 50% on enrolment, 25% at Month 4, 25% at Month 8 or at counselling/admission. Any early-bird or sibling concession is written into your engagement document.

NEXT STEPS
1. Reply "Proceed" and I will send the engagement agreement
2. Sign (parent, student and counsellor) and make the front payment
3. Phase 1 begins with the onboard and baseline assessments

Happy to clarify anything on a call.

""" + SIG_EMAIL + """

EduAakashaa guides the process; admission and seat allotment are decided by the authorities on rank and eligibility.""",
                    },
                    {
                        "label": "WhatsApp (summary)",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], here's a quick summary of *Elite Mentorship* for [Student Name] 📋

*Included*
✔ Dedicated senior mentor (1:1)
✔ Minimum 10 virtual sessions
✔ 9 strategy deliverables (assessment, roadmap, target list, choice-filling pack, seat-decision brief…)
✔ Portal + simulator + analytics (1 year)
✔ Parent briefings

*Not included*
✘ Subject tuition / JEE coaching
✘ Guaranteed rank or seat
✘ Visa / immigration / loans

*Fee:* ₹74,999 incl. GST — 50% / 25% / 25%

Full details sent by email. Shall I send the agreement? """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "meeting-confirm",
                "title": "Initial discussion meeting — confirmation & reminder",
                "when": "On booking; reminder 24 h and 1 h before.",
                "templates": [
                    {
                        "label": "Email — confirmation",
                        "channel": "email",
                        "subject": "Confirmed: your EduAakashaa mentorship conversation on [Date], [Time]",
                        "body": """Dear [Parent Name],

Your initial discussion is confirmed:

📅 [Day, Date]
🕗 [Time] IST / [Time] Gulf time
📍 [Video link / Phone number / Coimbatore address]
👤 With: [Your Name], [Designation]

Please keep ready: [Student Name]'s latest mark sheet, passport details, parent's work-country details and any college/route ideas. Please also invite [Student Name] to join — their voice matters.

Need to reschedule? Reply to this email or WhatsApp +91 80157 22706.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp — reminder",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """⏰ Reminder, [Parent Name]: your EduAakashaa mentorship conversation is *[Today/Tomorrow] at [Time] IST / [Time] Gulf*.
🔗 [Link]
Please keep [Student Name]'s latest marks & passport details ready. See you soon! """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "enrol-confirm",
                "title": "Enrolment & payment confirmation",
                "when": "On receipt of the front payment and signed agreement.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Enrolment confirmed — [Student Name], Elite Mentorship (Class of 2027)",
                        "body": """Dear [Parent Name],

Welcome to EduAakashaa. We confirm the enrolment of [Student Name] in Elite Mentorship — Grade 12 Track, Class of 2027.

ENROLMENT SUMMARY
• Student: [Student Name] · Grade [__] · [Board]
• Programme: Elite Mentorship (10–12 months)
• Lead mentor: [Mentor Name]
• Payment received: ₹[Amount] on [Date] · Receipt no. [____]
• Next instalments: 25% at Month 4 (~[Month Year]); 25% at Month 8 or at counselling/admission (~[Month Year])
• Engagement document: attached

WHAT HAPPENS NEXT
1. Within 24 hours: your welcome message and portal login
2. Within 3 working days: onboarding assessment link for [Student Name] and parent
3. Within 7 days: first mentor session

Please keep this email — the engagement document sets out your scope, schedule and our exit, cancellation and confidentiality terms (early exit within 30 days is refundable pro rata; cancellations are made in writing from the registered parent email).

We're glad to be on this road with you.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Dear [Parent Name], we've received your payment of ₹[Amount] 🙏
✅ *[Student Name] is now enrolled in Elite Mentorship (Class of 2027).*

Mentor: [Mentor Name]
Next: onboarding assessment link in 3 working days · first session within 7 days.

Receipt & agreement have been emailed. Welcome to EduAakashaa! """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "payment-reminder",
                "title": "Instalment reminder",
                "when": "7 days before the Month 4 and Month 8 instalments.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Gentle reminder: instalment due [Date] — [Student Name]'s mentorship",
                        "body": """Dear [Parent Name],

A gentle reminder that the [second / final] instalment of ₹[Amount] for [Student Name]'s Elite Mentorship falls due on [Date], as per the schedule in your engagement document.

Payment details: [Bank / link]. Please share the reference once paid and we will send the receipt.

If a change is needed, please write to us in advance.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], a gentle reminder — instalment of ₹[Amount] for [Student Name]'s mentorship is due on [Date]. Payment link: [Link]. Thank you! """ + SIG_WA,
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    {
        "id": "onboarding",
        "title": "3 · Onboarding & assessment",
        "blurb": "First 7 days: welcome, onboarding assessment, report, first session.",
        "items": [
            {
                "id": "welcome-student",
                "title": "Welcome message for new students",
                "when": "Within 24 hours of enrolment. Address the student directly.",
                "templates": [
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Student Name] 👋 Welcome to EduAakashaa!

I'm [Mentor Name], your lead mentor. From today until your seat is confirmed, you'll never have to figure out admissions alone.

Here's how we'll work:
1️⃣ A short assessment (about 10 minutes) so I understand *you* — your goals, strengths and week
2️⃣ Your first 1:1 session on [Date/Time]
3️⃣ A roadmap that fits your real school week

One thing to remember: we are your guide, not your teacher. You do the studying; we help you decide *what to solve* and *which seat to choose*.

Small steps. Consistent progress. Better decisions. 🚀
""" + SIG_WA,
                    },
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Welcome to EduAakashaa, [Student Name] — here's how your journey begins",
                        "body": """Dear [Student Name],

Welcome! Your parents have trusted us with something important, and we take it seriously. I'm [Mentor Name], your lead mentor.

HOW THE NEXT 10–12 MONTHS WORK
Phase 1 · Foundation + Build — baseline assessment, eligibility locked, roadmap and document list drafted
Phase 2 · Target — JEE strategy, DASA/CIWG windows prepared, choice lists built and stress-tested
Phase 3 · Execute — forms, choice filling, seat decision and confirmation

YOUR FIRST WEEK
• Complete the onboarding questionnaire (about 10 minutes, nothing is graded): [Link]
• Join your portal: [Portal link] · Login: [Email]
• First session: [Date, Time]

WHAT I EXPECT FROM YOU
• Be honest, including about a bad week
• Keep your weekly planner and tracker — five minutes a day
• Bring your questions; no question is too small

WHAT YOU CAN EXPECT FROM ME
• I will listen first, then help you build a plan you can keep
• I will tell you plainly where the risks are
• I will never promise a result — I will help you make better decisions

See you in session one.

""" + SIG_EMAIL,
                    },
                ],
            },
            {
                "id": "assessment-invite-student",
                "title": "Invitation for onboarding assessment — student",
                "when": "Right after enrolment.",
                "templates": [
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Student Name], time for your onboarding assessment 📝

⏱ About 10 minutes · nothing is graded · answer honestly, there are no right answers
🔗 [Assessment link]
📅 Please complete it by [Date]

It helps me plan a roadmap that fits *your* week, not a generic one. Thank you! """ + SIG_WA,
                    },
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Your onboarding assessment — 10 minutes, nothing graded",
                        "body": """Dear [Student Name],

Before our first session I'd like to understand you — not just your marks.

The onboarding assessment covers your school day and study habits, subjects you feel most and least confident in, what usually stops you studying, the routes your family is considering, and what you want most from a mentor.

⏱ About 10 minutes · Nothing is graded · Your answers stay private to you, your parents and your mentor
🔗 [Assessment link] · Please complete by [Date]

""" + SIG_EMAIL,
                    },
                ],
            },
            {
                "id": "assessment-invite-parent",
                "title": "Invitation for onboarding assessment — parents",
                "when": "Same day as the student invite; parents complete a separate form.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Parent onboarding assessment for [Student Name] — 8 minutes",
                        "body": """Dear [Parent Name],

Parents see things we cannot — the household routine, finances, travel plans and the pressures around the student. A short parent assessment helps us build a plan the whole family can sustain.

It covers:
• Your goals and expectations for [Student Name]
• The routes and countries you are considering
• Budget comfort zones for tuition, hostel and travel
• Documents already available (passport, visa, employer certificate, mark sheets)
• Practical constraints — relocation, siblings, work schedules

⏱ About 8 minutes · 🔗 [Parent assessment link] · Please complete by [Date]

A small request: please let [Student Name] complete their own assessment independently. Their honest answers are the foundation of the plan.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hello [Parent Name] 🙏 As part of [Student Name]'s onboarding, please complete the *parent assessment* (8 min):
🔗 [Link] · by [Date]

It helps us plan around your goals, budget and constraints. Please let [Student Name] fill their own assessment separately. Thank you! """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "assessment-report",
                "title": "Assessment report sharing",
                "when": "Within 5–7 working days of both assessments. Share in a 30-minute walkthrough, not only as a PDF.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "[Student Name]'s Baseline Assessment & Eligibility Report is ready",
                        "body": """Dear [Parent Name] and [Student Name],

The Baseline Assessment and Eligibility Report is attached. It is the first stage (Assess) of our 5A method and the foundation for the Admissions Roadmap.

WHAT'S IN THE REPORT
1. Profile — interests, strengths, study habits and constraints
2. Eligibility check — residency (two years of Classes 11–12 abroad), CIWG status, the 75% / 7.5 CGPA rule and the subject combination, route by route
3. Document gaps — what is ready and what must be collected, with dates
4. Early observations — [one or two strengths, one or two areas to work on]
5. Proposed priorities for the next 30 days

HOW TO READ IT
The report is a starting point, not a verdict. Eligibility is stated against the 2026 rules and will be re-verified against the official 2027 brochure when published. Nothing in it is a guarantee of rank or admission.

LET'S WALK THROUGH IT
I've reserved [Date, Time] for a 30-minute walkthrough: [Link]. Please read the Eligibility and Document Gap sections beforehand and note your questions.

Please keep the report confidential — it is for the enrolled student and family only.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], [Student Name]'s *Baseline Assessment & Eligibility Report* is ready 📄 (sent by email).

Walkthrough: [Date, Time] — [Link].

Please look at the Eligibility and Document-gap sections beforehand. It's a starting point, not a verdict. """ + SIG_WA,
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    {
        "id": "ongoing",
        "title": "4 · Ongoing communication",
        "blurb": "Session reminders, exam schedule, newsletters, reports.",
        "items": [
            {
                "id": "session-reminder",
                "title": "Session reminder & follow-up",
                "when": "24 h before each session; follow-up the same day.",
                "templates": [
                    {
                        "label": "WhatsApp — reminder",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Student Name] 👋 Reminder: our session #[__] is *[Day] at [Time]* — [Link].
Please bring: ✔ this week's planner/tracker ✔ your last mock result ✔ one question you want answered.""" ,
                    },
                    {
                        "label": "WhatsApp — follow-up (after session)",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Thanks for today, [Student Name]! Your agreed commitments before next time:
1. [Commitment + measure]
2. [Commitment + measure]
3. [Commitment + measure]
Next session: [Date/Time]. You've got this 💪""",
                    },
                    {
                        "label": "WhatsApp — missed session",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Student Name], we missed you today — no worries, it happens. Which slot works for a quick catch-up: [Option 1] or [Option 2]? """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "exam-schedule",
                "title": "Exam schedule information",
                "when": "Send after each NTA/JoSAA/CSAB notification. Mark dates as Confirmed vs Expected, and always link the official source.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Class of 2027 calendar — key exam and counselling dates [as of [Date]]",
                        "body": """Dear [Parent Name] and [Student Name],

Here is the current admissions calendar for the Class of 2027. We have marked what is officially confirmed and what is expected from past cycles.

✅ CONFIRMED / LISTED
• JEE Main Session 1 — 22–24 and 28–30 January 2027 (buffer day 31 Jan), computer-based test; subject to the NTA notification

🟠 EXPECTED (based on past cycles — to be confirmed)
• JEE Main Session 1 registration — late October to late November 2026 (jeemain.nta.nic.in)
• Session 1 result — February 2027
• JEE Main Session 2 — registration February, exam early April 2027
• Final NTA score and All India Rank — late April 2027
• JEE Advanced (IIT route) — registration late April–early May, exam mid-May, result early June 2027
• JoSAA counselling — June–July 2027
• DASA / CSAB-Special — late July–August 2027 (the 2027 brochure is not yet published; 2026 ran 28 July–18 August in two rounds)
• Private NRI applications (Amrita, VIT etc.) — open from November 2026
• NATA — expected April–June 2027; NID DAT prelims — tentatively late December 2026

WHAT TO DO THIS MONTH
1. [Action 1 — e.g., confirm exam city choices and keep documents scanned to NTA size limits]
2. [Action 2]
3. [Action 3]

Please verify each date on the official site before acting: nta.ac.in, jeeadv.ac.in, josaa.nic.in, csab.nic.in. We re-check every date for you and will update you the day a notification is published.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """📅 *Class of 2027 key dates* (as of [Date])

✅ JEE Main Session 1: 22–30 Jan 2027 (subject to NTA notice)
🟠 Registration: late Oct–Nov 2026 (expected)
🟠 Session 2: April 2027 (expected)
🟠 JEE Advanced: mid-May 2027 (expected)
🟠 JoSAA: Jun–Jul 2027 (expected)
🟠 DASA/CSAB: late Jul–Aug 2027 (2027 brochure awaited)

⚠️ Always verify on official sites. We'll alert you the day anything is notified.
""" + SIG_WA,
                    },
                    {
                        "label": "WhatsApp — deadline alert",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """🚨 *Deadline alert* — [Event] closes on *[Date, Time] IST*.
Action needed: [what to do].
Documents ready? Reply YES or call me on [number] today. """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "newsletter",
                "title": "Motivational newsletter to students",
                "when": "Monthly or fortnightly. Praise a specific, true thing. Never promise a result.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Small steps, steady weeks — your [Month] note from EduAakashaa",
                        "body": """Dear [Student Name],

This month's thought:

"Nothing dramatic this week, and that is the point. Four steady weeks are worth more than one brilliant day."

A COMPARISON TRAP
It is easy to measure yourself against a friend's mock score or a coaching-class topper. You are not running their race. Look at your own line on your dashboard — is it going the right way?

THIS MONTH'S ONE HABIT
[Habit — e.g., Write down the reason for every mistake in your error log. Five minutes, every evening.]

A 2-MINUTE REFLECTION
• What was my hardest moment this month, and how did I handle it?
• What did I do that I'm proud of?
• What is one block I will protect next week?

QUICK REMINDERS
• Sleep is part of the plan — an extra hour of sleep beats an extra hour of panic
• A mock is a measurement, not a verdict
• Ask for help early; that is what we are here for

COMING UP
[Upcoming exam / registration / session]

Small steps. Consistent progress. Better decisions.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp — short boost",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Student Name] 🌟

"You are not running their race. Look at your own line on the dashboard. It is going the right way."

Four steady weeks beat one brilliant day. Proud of your effort on [specific thing]. Keep going 💪""",
                    },
                    {
                        "label": "WhatsApp — after a poor mock",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Thank you for sending this, [Student Name]. It took something to sit it and to share it. Let us find the marks that are closest to coming back. Let's talk at [time]? """ + SIG_WA,
                    },
                    {
                        "label": "WhatsApp — before an exam",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """You have a routine, a method for hard questions and a record of getting better. Take those in with you. All the best for tomorrow, [Student Name]! 🍀""",
                    },
                ],
            },
            {
                "id": "monthly-report",
                "title": "Monthly progress report (parents + student)",
                "when": "After the 30-minute monthly review. Private to student, parents and mentor — never shared in a group.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "[Student Name] — Progress review, [Month Year]",
                        "body": """Dear [Parent Name],

Thank you for joining [Student Name]'s review on [Date]. Here is the summary — one page, as agreed.

INDICATORS (this month vs last month)
• Study blocks completed: [x]/[y] ([%]) — last month [%]
• Revision topics completed vs plan: [x]/[y]
• Latest mock: attempted [__] · correct [__] · incorrect [__] · score [__] · accuracy [__]%
• Latest written paper: [marks] — marks lost to omissions: [__]
• Confidence (self-rated 1–5): [__] · Consistency (self-rated 1–5): [__]

WHAT HELPED  [One habit to keep]
WHAT DID NOT  [One habit to change]
OBSTACLES  [Obstacle(s) identified]

SUPPORT NEEDED FROM HOME
[Practical requests — e.g., a quiet hour after 9 pm, phone away during blocks, document collection]

AGREED PRIORITIES FOR NEXT MONTH (up to three)
1. [Priority + measure]
2. [Priority + measure]
3. [Priority + measure]

ADMISSIONS TRACK
• Documents: [ready / pending list]
• Upcoming deadlines: [dates]

Next review: [Date]

A note on reading this: we look at habits before results, and compare [Student Name] only with [Student Name]. Please avoid comparing with other children.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp (summary)",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """📊 *[Student Name] — [Month] review*
• Study blocks completed: [%] (last month [%])
• Latest mock: [score] · accuracy [%]
• Confidence [x]/5 · Consistency [x]/5

✅ Keep: [habit]
🔁 Change: [habit]
🎯 Next month: 1) [__] 2) [__] 3) [__]

Full report emailed. Next review: [Date]. """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "quarterly-review",
                "title": "Quarterly review report (course-correction notes)",
                "when": "End of each quarter / termly review. Written course-correction notes are a standard deliverable.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "[Student Name] — Quarterly review & course-correction notes, [Quarter / Year]",
                        "body": """Dear [Parent Name] and [Student Name],

Please find the quarterly review for [Quarter], measured against the Admissions Roadmap.

1. WHERE WE STARTED vs WHERE WE ARE
• Roadmap milestones planned: [x] · achieved: [y] · carried over: [z]
• Academic trend: [Boards / mocks — three-month trend]
• Admissions readiness: Eligibility [Confirmed / Pending] · Documents [x of y ready] · Target list [Draft / Final]

2. WHAT WENT WELL
[2–3 specific, true observations]

3. WHAT NEEDS ATTENTION
[2–3 items with evidence]

4. COURSE-CORRECTIONS
| Area | Change | Owner | By when |
| [Study plan] | [__] | [Student] | [Date] |
| [Documents] | [__] | [Parent] | [Date] |
| [Route/target list] | [__] | [Mentor] | [Date] |

5. NEXT QUARTER — KEY DATES
[Exam / registration / deadline list]

6. ROADMAP REVISIONS
[Any change to routes, targets or priorities — with the reason]

7. SESSIONS USED
[x] of 10+ minimum 1:1 sessions used · Next session: [Date]

This review is guidance based on current data; rules, fees and dates for the 2027 cycle are re-verified against official notifications as they are published. No rank or seat is guaranteed.

Your parent review call is on [Date, Time]: [Link].

""" + SIG_EMAIL,
                    },
                ],
            },
            {
                "id": "parent-briefing",
                "title": "Parent briefing invitation (at each gate)",
                "when": "Before JEE Main registration, before Session 2, before JoSAA, before DASA registration.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Parent briefing before [Gate: DASA/CIWG registration] — [Date]",
                        "body": """Dear [Parent Name],

As part of the programme we hold a parent briefing at each key gate. The next one is ahead of [Gate].

📅 [Date] · 🕗 [Time] IST / [Time] Gulf · 🔗 [Link]
Duration: 30–40 minutes

AGENDA
1. What changes now and what the official notification says
2. Your documents checklist — what to have in hand
3. Cost worksheet and decisions the family must make
4. Q&A

A written summary will follow in your inbox. Please bring any open questions.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hello [Parent Name], your parent briefing before *[Gate]* is on *[Date], [Time] IST / [Time] Gulf*.
🔗 [Link] · 30–40 min · written summary to follow.
Please keep the document checklist handy. """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "document-reminder",
                "title": "Document checklist reminder (DASA / CIWG)",
                "when": "Start 3 months before the window; weekly nudges until complete.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Document checklist for [Student Name] — [x] of [y] ready",
                        "body": """Dear [Parent Name],

In DASA a missing paper can cost the round, so we build the file early. Status as of [Date]:

READY ✅  [list]
PENDING ⏳  [list with owner and due date]

THE CHECKLIST (2026 rules — re-checked against the 2027 brochure when published)
• Student passport and proof of date of birth
• Mark sheets for Classes 10, 11 and 12
• School certificate confirming Classes 11 and 12 abroad
• Percentage / CGPA equivalence, where the board grades differently
• Medical certificate in the prescribed format
• OCI or PIO card, where applicable
• For CIWG: parent's passport, visa and work permit valid in the admission year
• For CIWG: employer certificate in the prescribed format

Please keep one folder (digital and paper) and one calendar. Reply with any item you need help obtaining.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], document file status for [Student Name]: *[x] of [y] ready* 📂
Pending: [item 1], [item 2].
Due by [Date]. Need help? Reply here. """ + SIG_WA,
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    {
        "id": "internal",
        "title": "5 · Mentors & internal",
        "blurb": "Emails to the mentoring team.",
        "items": [
            {
                "id": "mentor-assign",
                "title": "Email to mentors — new student assignment brief",
                "when": "When a student is assigned to a lead / domain mentor / admissions specialist.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "New assignment: [Student Name] · Grade [__] · [Country] · Class of 2027",
                        "body": """Hi [Mentor Name],

You have been assigned as [Lead / Domain / Admissions] mentor for the student below.

STUDENT SNAPSHOT
• Name: [Student Name] · Grade [__] · Board [__] · School/Country [__]
• Parent contact: [Name, phone, email] · Preferred time zone: [__]
• Routes of interest: [DASA / CIWG / JoSAA / TNEA / private]
• Eligibility flags: [e.g., OCI holder — no CIWG; residency rule check pending]
• Latest marks / mocks: [__]
• Programme: Elite Mentorship, [start date] · 10+ sessions minimum

FIRST 7 DAYS
1. Review the onboarding assessments (student + parent) in [link]
2. Hold session 1 by [Date] using the T7 session-notes format
3. Draft the Baseline Assessment & Eligibility Report within 5–7 working days
4. Set up the document and deadline calendar

WORKING PRINCIPLES (please re-read)
• We are a guide, not a teacher — no subject tuition, no guaranteed outcomes
• The family authorises and submits every application; we prepare and verify
• Student data and reports are confidential and never posted in groups or compared
• Praise only what is true; record concerns for parent/professional follow-up
• Re-verify every rule and date against the official notification before advising

Please acknowledge and flag any conflict or capacity issue today.

Thanks,
[Programme Head], EduAakashaa""",
                    },
                ],
            },
            {
                "id": "mentor-monthly",
                "title": "Email to mentors — monthly review & notes reminder",
                "when": "Last week of every month.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Monthly review & session-notes check — [Month Year]",
                        "body": """Hi team,

Monthly check-in:

DUE BY [Date]
1. Session notes (T7) uploaded for every session held this month
2. Monthly progress review (T8) held and one-page report (T6 dashboard) sent to each parent
3. Document & deadline calendars updated
4. Any student with a missed session or falling confidence flagged to me

THIS MONTH'S FOCUS
• [e.g., JEE Main registration — confirm every family has submitted and keeps the confirmation page]
• [e.g., watch for the DASA 2027 brochure — notify me the day it is published]

REMINDERS
• Minimum 10 virtual 1:1 sessions per student across the programme — check each student's usage
• Quarterly course-correction notes are due for [students list]

Please reply with a short status for your students by [Date].

Thanks,
[Programme Head]""",
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    {
        "id": "other",
        "title": "6 · Other important templates",
        "blurb": "Seat decision, thank-you, feedback, referral, closing.",
        "items": [
            {
                "id": "rule-alert",
                "title": "Official notification alert (e.g., DASA 2027 brochure released)",
                "when": "The day an official brochure / schedule is published.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Important: [DASA 2027 Information Brochure] has been published",
                        "body": """Dear [Parent Name],

The [DASA 2027 Information Brochure / schedule] was published on [Date] at [csab.nic.in].

WHAT CHANGED (vs 2026)
• [Change 1 — e.g., number of rounds]
• [Change 2 — e.g., fees]
• [Change 3 — e.g., eligibility or dates]

WHAT IT MEANS FOR [Student Name]
[Specific impact]

WHAT WE WILL DO
• Update your Admissions Roadmap and document calendar by [Date]
• Hold a short call on [Date, Time]: [Link]

Official source: [URL]. Please do not act on forwarded summaries without checking the official notice.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """🔔 *Official update:* [Document] published on [Date] ([source]).

Key changes: 1) [__] 2) [__] 3) [__]
Impact on [Student Name]: [__]

We're updating your roadmap by [Date]. Call at [Time]? """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "seat-decision",
                "title": "Final seat decision brief — delivery",
                "when": "At the allotment stage, before the family accepts, freezes or floats.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "[Student Name] — Final Seat Decision Brief (decision due [Date])",
                        "body": """Dear [Parent Name] and [Student Name],

The allotment result is out and your decision window closes on [Date, Time]. Attached is the Final Seat Decision Brief.

WHAT IS IN IT
• The allotted seat — institute, branch, category, fee tier
• Options if you Freeze / Slide / Float / Surrender / Withdraw / Exit — and what each costs you
• Comparison with the target list — branch, placements, fees, location, hostel
• Total cost worksheet and documents needed at physical reporting
• Our recommendation and the honest risks

Please remember: the decision is yours — we prepare the picture, you make the choice. Let's speak on [Date, Time]: [Link].

""" + SIG_EMAIL,
                    },
                ],
            },
            {
                "id": "congrats",
                "title": "Congratulations & thank-you",
                "when": "After seat confirmation / reporting.",
                "templates": [
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """🎉 Congratulations, [Student Name]! You've confirmed your seat at [Institute]. We're so proud of the effort and the choices you made along the way.

Next: pay fees at reporting, complete document verification, and plan your move. We're here for your questions till you settle in. """ + SIG_WA,
                    },
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Congratulations, [Student Name] — and thank you",
                        "body": """Dear [Parent Name] and [Student Name],

Congratulations on [Student Name]'s admission to [Institute / Programme]. It has been a privilege to walk this road with your family.

What made the difference was the steady work — the planner, the tracker, the conversations at home, and decisions made with good information.

A small request: would you share a few lines about your experience? [Feedback link]. If another family could benefit, we would be glad to be introduced — referred families receive [offer].

We wish [Student Name] a wonderful journey ahead.

""" + SIG_EMAIL,
                    },
                ],
            },
            {
                "id": "feedback",
                "title": "Feedback & testimonial request",
                "when": "30 days after seat confirmation, or at the programme midpoint (Month 4).",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Two minutes of your time: how are we doing, [Parent Name]?",
                        "body": """Dear [Parent Name],

We would value your honest feedback on the mentorship so far:
🔗 [Feedback form link] — 2 minutes

• What has helped most?
• What could be better?
• May we quote a line from you (first name only, with your permission)?

Thank you for helping us improve.

""" + SIG_EMAIL,
                    },
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], would you share 2 minutes of feedback on the mentorship? 🙏 [Link]. Your honest words help us improve — thank you! """ + SIG_WA,
                    },
                ],
            },
            {
                "id": "referral",
                "title": "Referral request",
                "when": "After positive feedback or a milestone achieved.",
                "templates": [
                    {
                        "label": "WhatsApp",
                        "channel": "whatsapp",
                        "subject": "",
                        "body": """Hi [Parent Name], glad we could help [Student Name]. If you know a family with a child in Grade 11–12 who could use clarity on DASA/CIWG/JoSAA, we'd be happy to give them a free 20-min conversation — just share their number or ask them to message us. [Referral offer, if any]. Thank you! """ + SIG_WA,
                    }
                ],
            },
            {
                "id": "exit",
                "title": "Cancellation / early-exit acknowledgement",
                "when": "On a written request from the registered parent email. Confirm within 3 working days; settle refunds within 14 working days.",
                "templates": [
                    {
                        "label": "Email",
                        "channel": "email",
                        "subject": "Acknowledgement of your request — [Student Name]'s mentorship",
                        "body": """Dear [Parent Name],

We acknowledge your written request dated [Date] to [cancel / pause] [Student Name]'s Elite Mentorship.

As per the engagement document:
• Requests within 30 days of enrolment: the fee paid is refundable pro rata for sessions and deliverables not yet used, less a one-time administration charge; portal access and materials already issued are revoked
• After 30 days the fee is non-refundable, because mentor and specialist time has been committed

Your case: [Applicable clause and calculation]. [Refund of ₹[Amount] will be settled within 14 working days / No refund applies].

We are sorry to see you go, and the door remains open. Please keep programme materials confidential, as set out in the engagement document.

""" + SIG_EMAIL,
                    },
                ],
            },
        ],
    },
]

GUIDELINES = [
    "Never promise a rank, score or seat. Use 'plan', 'estimate' and 'guidance'.",
    "Quote DASA/JoSAA rules as '2026 rules' until the 2027 brochure is published; mark dates Confirmed vs Expected.",
    "Marketing emails must carry the opt-out line; send WhatsApp promotions only to people who have opted in.",
    "Keep student dashboards and reports private to student, parents and mentor — never in groups, never compared.",
    "Keep fee and scope figures in step with the current engagement document (₹74,999 incl. GST, 50/25/25 in the 2027 Grade 12 track).",
    "Replace every [Square Bracket] before sending. Time zones: say both IST and Gulf time.",
]
