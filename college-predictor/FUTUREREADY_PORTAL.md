# EduAakashaA FutureReady Mentorship Portal (Grades 8–9)

A module of the existing Flask app (`app/futureready/`, blueprint `/futureready`). It reuses the site's login, roles, database, PDF stack and brand theme. It adds **new tables only** (`fr_*`); nothing existing is altered.

## 1. Information architecture

| Area | Route | Who |
|---|---|---|
| Entry / workspace picker | `/futureready/` | everyone (public intro when signed out) |
| Student home (dashboard) | `/futureready/s/<id>` | student, parent, assigned mentor, admin |
| Onboarding (10 steps, save and resume) | `/s/<id>/onboarding/<1-10>` | student, parent (consent, goals), staff (programme) |
| Assessments 1–12 | `/s/<id>/assessments`, `/a/<key>`, `/attempt/<id>` | student (parent: alignment only) |
| Aptitude Sampler | `/s/<id>/sampler` | student |
| Engineering Branch Explorer, compare, shortlist, interest map | `/branches`, `/branches/<key>`, `/branches/compare`, `/s/<id>/interest-map` | signed-in users |
| Entrance System Awareness Centre | `/admissions` | public |
| Subject Foundations Explorer | `/foundations` | signed-in |
| Suggestions (recommendations) | `/s/<id>/recommendations` | mentor approves; family sees approved |
| Goals, actions, projects | `/s/<id>/plan` | student, parent, mentor |
| Mentor workspace: sessions + notes | `/s/<id>/mentor` | mentor/admin (private notes); family sees shared |
| Reports A–F (+PDF) | `/s/<id>/reports` | staff create; family sees Shared |
| Administration | `/futureready/admin` | admin |
| Privacy and child safety | `/privacy` | public |

## 2. User journeys

* **Student**: sign in → onboarding (consent is recorded by a parent) → baseline assessments over several days → results with explanations → interest map and branch exploration → accepts mentor-approved suggestions into the action plan → projects, reflections → sees shared reports and growth.
* **Parent**: links to a child → records consent and goals → completes the parent view of Assessment 10 → reads shared results and reports → sees only shared notes; sends private notes to the mentor.
* **Mentor** (`ea_mentor`): sees assigned students only → rates the practical task with the rubric → generates and reviews suggestions → sets goals and actions → schedules sessions, writes private/shared notes → creates, reviews and shares reports.
* **Administrator**: enrols students, links parents, assigns mentors → edits content (versioned) → verifies admission information → manages windows → audit log, CSV export, deletion on request → creates a labelled demo workspace.

## 3. Data model (`app/futureready/models.py`)

`FrProfile` (one per student) · `FrParentLink` · content: `FrAssessment`, `FrQuestion` (versioned), `FrBranch`, `FrAdmission`, `FrResource` · records: `FrAttempt`, `FrSkillScore`, `FrShortlist`, `FrGoal`, `FrAction`, `FrNote`, `FrSession`, `FrRecommendation`, `FrProject`, `FrBadge`, `FrReport` (frozen JSON), `FrNotice` · governance: `FrWindow`, `FrAudit`.

## 4. Assessment framework

| # | Assessment | Type | Reported as |
|---|---|---|---|
| 1 | Academic Foundations Diagnostic | objective | per-skill bands |
| 2 | Learning Skills and Study Habits | self-report | per-habit mean (1–5) |
| 3 | Reasoning and Problem-Solving | objective | per-task-type bands |
| 4 | PER: Personality, Emotion, Reasoning | self-report | tendencies (never a type) |
| 5 | Interests and Strengths Explorer | self-report + 2 open questions | per-domain interest |
| 6 | Creativity and Practical Design Challenge | rubric (mentor) | 6 criteria × 4 levels, visible descriptors |
| 7 | Digital and Responsible AI Literacy | objective + task | bands + practical |
| 8 | Communication and Collaboration | self-report + scenarios | tendencies |
| 9 | Self-Management and Goal-Setting | self-report + task | tendencies, with follow-through from the real action plan |
| 10 | Parent–Student Alignment | self-report, two audiences | matches and gaps for conversation |
| 11 | Engineering Branch Interest Map | scenarios | interest tags (no right answer) |
| 12 | Entrance-System Awareness Check | objective | awareness |

Plus the Aptitude Sampler (10 skills × 3 levels × 3 items) and a Quarterly Reflection used in quarterly reports.

**Scoring standards** (`engine.py`): objective skills use **Secure ≥ 80%, Developing 50–79%, Needs reinforcement < 50%**; a skill with fewer than 2 answered items is shown as “Too few items” and never labelled. Self-report items (reverse-scored where marked) are averaged on 1–5 and are always described as “how you see yourself”. Open text and the practical task are assessed by a mentor against the visible rubric. Results state what they do not mean. **No rank, cut-off or admission prediction anywhere.**

Every question carries a stable `code` + `version`; an edit creates version n+1 and retires the old row, so old attempts keep their wording. Every objective question has an explanation and, where useful, a note about the common slip.

## 5. Entrance-system content and governance

Routes are stored as `FrAdmission` rows. TNEA is described as a **merit-based admission and counselling process, not an entrance examination**. All routes ship as **“Requires verification”**: a route shows as *Verified* only when the admin has filled **year, official URL, reviewer and last-verified date**. Eligibility text is displayed only for verified routes. Seed rows contain stable, general descriptions and official links, not year-specific dates, fees or cut-offs.

**Action for the team:** before families rely on the Entrance System page, verify each route from its official notice (Admin → Admission routes).

## 6. Recommendations and reports

`reco.py` is rule-based: objective gaps, low habits (self-report), top interests → projects, digital-literacy gaps, parent-student gaps. Each suggestion stores its evidence (assessment, skill, value, number of items). Suggestions are **hidden from the family until a mentor approves**. Accepting one creates an action in the plan.

Reports (`reports.py`): Starting-Point, Skill-Gap, Engineering Pathway, Monthly, Quarterly, Growth. A report is a frozen JSON snapshot; staff create a draft, review it, then **Share**. HTML and PDF (reportlab) come from the same data. Growth compares a student with their own earlier results and flags changes based on few items. Reports never include private mentor notes or parent notes.

## 7. Privacy, safety, access

* Access is decided in `access.py` (`role_for`, `profile_or_403`) on every route: admin, assigned `ea_mentor`, the student, linked parents.
* Assessments are locked until a **parent or guardian** records consent (staff may record it after speaking with the parent).
* Private mentor notes and parent notes are invisible to students; parents never see a student's open-text answers or the student's alignment answers.
* `FrAudit` records consent, report sharing/PDF, exports, deletions, content edits. Admin can delete a student's FutureReady data (type DELETE).
* CSV export contains scores only (no text), real students only.

## 8. Demo mode

Admin → “Create a labelled demo workspace” makes a sample student and parent (`*@futureready.test`, random passwords shown once) with completed assessments, a rubric, plan, notes, session and a shared report. Every page shows a DEMONSTRATION banner; demo data is excluded from exports.

## 9. Deployment

1. Deploy as usual (Render). Tables are created automatically at start-up (`db.create_all`); no migration is needed.
2. Sign in as admin → `/futureready/admin` → **Load / refresh standard content** (idempotent; never overwrites edits).
3. Make staff mentors `ea_mentor` (existing member admin). Students and parents register normally; enrol them from the admin page by e-mail, assign the mentor and link parents.
4. Verify admission routes (section 5) and set review dates.
5. Optional: create the demo workspace to rehearse with the team.

No new environment variables or packages (uses Flask, SQLAlchemy and reportlab already in `requirements.txt`).

## 10. Testing checklist

`python tests/test_futureready.py` covers: content integrity (unique codes, valid answers, 30 sampler sets × 3 items), idempotent seeding, enrolment, access control (other student / parent / mentor, anonymous), onboarding and consent gate, autosave, scoring rules and bands, reverse-scored items, interest tags, rubric permissions, sampler sets, parent vs student alignment, recommendation approval and de-duplication, action ownership, private-note privacy, report draft/share/PDF and growth, content versioning, admission verification gate, demo mode, export exclusion, deletion guard.

Manual checks: mobile layout (≤ 640 px) of the assessment page; keyboard-only completion of an assessment; screen-reader labels on Likert groups; print view of a report.

## 11. Known limitations

* Notifications are **in-app notices** only; e-mail/WhatsApp hooks are not wired for FutureReady.
* Content is original and reviewed once; it needs educator review (a second reviewer and pilot with real students) before wide use. Item statistics (difficulty/discrimination) cannot exist until real attempts accumulate.
* Parent account linking is by e-mail of an already-registered account.
* Charts are lightweight (bars/tables); the growth view is a table, not a chart.
* The sampler has three items per set: a practice tool, not an ability measure.
* The pre-existing tests `test_mailer.py` and `test_mentorship_portal.py` fail on earlier changes (sender address, member-hub image check) unrelated to FutureReady.
