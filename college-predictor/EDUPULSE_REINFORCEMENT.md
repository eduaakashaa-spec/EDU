# EduPulse – Reinforcement

Daily practice, confidence-aware knowledge tracking and mentor intelligence for JEE Main and UCEED members.
Live module of the existing EduAakashaA portal: `/edupulse-reinforce/` (Flask blueprint `reinforce_bp`).

**What was delivered.** The working application *is* the interactive prototype: it ships with a clearly labelled demonstration workspace
(Admin → Create demo) that shows the popup, the one-question-at-a-time flow, the mentor dashboard, chapter drill-down, recommendations and the parent report
with sample data. Demo students are flagged, use `*.test` e-mail addresses and are excluded from exports.

## 1. Scope of the MVP

| Area | In the MVP | Left for later (not built) |
|---|---|---|
| Student | Login popup for pending practice; one-question flow; mandatory Guess / Low / Medium / High; autosave and resume; completion summary; explanations once released; dashboard (streak, pending, recent, suggested next steps) | Streak rewards, spaced-repetition calendar, offline mode |
| Mentor | Student overview with search/filters; chapter-wise matrix with evidence counts; drill-down to topic and question; four-pattern view; observations and follow-up dates; assignment builder (5 to 10 questions, schedule, due, popup rules, release rules, per-student distinct questions, duplicate); recommendations to approve / modify / reject | Bulk reassign by rule, mentor-to-mentor handover |
| Question bank | Taxonomy; metadata (difficulty, type, marks, estimated time, concept, misconception, source); draft → in review → approved → retired; versioning; CSV import (all-or-nothing validation) and export; starter bank of the original JEE and UCEED mock questions | Rich editor with images and formulas, duplicate detection |
| Parent | Weekly and monthly report in plain language, only for linked parents and only when the mentor switches it on | E-mail delivery of the report |
| Notifications | In-portal notices, de-duplicated by key | E-mail / WhatsApp reminders (the Member Home WhatsApp buttons already exist) |
| Admin | Thresholds, starter bank, demo, attempts export, audit log | |

## 2. Roles and permissions (enforced on the server)

| Capability | Student (premium) | Parent | Mentor (`ea_mentor`) | Admin |
|---|---|---|---|---|
| Open own assignments, answer, resume | ✔ own only | – | – | – |
| See answer key / explanation | only after the release rule allows it | – | ✔ | ✔ |
| See a student's chapter matrix | own summary | report only | only students on their roster | all |
| Weekly / monthly report | own | only linked child **and** report switched on | own students | all |
| Assign practice | – | – | own roster, approved questions only | all |
| Approve a recommendation | – | – | own students | all |
| Create / edit questions | – | – | ✔ (edit makes a new version) | ✔ |
| Approve a question | – | – | not their own question | ✔ |
| Retire a question, thresholds, exports, demo | – | – | – | ✔ |

Unlinked parents, other students and other mentors receive 404. Free-tier members cannot open the module.

## 3. User journeys

1. **Mentor assigns.** Assign practice → choose exam track and students (or a group) → filter or pick questions (5 to 10) → set start/due (IST), popup rule, release rule → Assign. Each student gets an assignment with their own question set (distinct per student when asked).
2. **Student practises.** Member Home shows the popup for pending work (mandatory popups cannot be snoozed; dismissible ones offer "Remind me later") → Start → one question at a time → the confidence buttons unlock only after an answer, and *Next* only after a confidence level → answers autosave → submit → summary. Explanations arrive when the release rule allows.
3. **Mentor reviews.** Dashboard shows overdue/pending, accuracy and attention chapters → student page → chapter matrix → drill-down → suggestions → approve (creates a real assignment), modify (opens the builder pre-filled) or reject.
4. **Parent reads.** Report page with effort, accuracy vs the previous period, strengths, areas being worked on, mentor notes marked "for parent".

## 4. Learning patterns and formulas

Confidence is stored beside correctness and never changes it.

| Pattern | Rule | Meaning |
|---|---|---|
| P1 Knows and is confident | correct and High | secure understanding for that question |
| P2 Knows but lacks confidence | correct and Guess/Low | possible lucky guess or fragile confidence |
| P3 Gap the student is aware of | wrong and Guess/Low | aware gap |
| P4 Overconfident error | wrong and High | possible misconception |
| (Medium) | either | kept as an intermediate band, counted separately |

* Accuracy = correct ÷ answered in the period, always shown with *n*.
* High-confidence error rate = wrong High ÷ all High answers (used only when High answers ≥ `min_high_n`).
* Share of correct answers rated Guess/Low = P2 ÷ all correct.

**Chapter status** (first rule that matches; thresholds are admin-editable, defaults in brackets):

1. fewer than `min_distinct` (8) distinct questions → **Insufficient data** ("Building understanding" for the student)
2. High answers ≥ `min_high_n` (3) and high-confidence error rate ≥ `high_err_rate` (25%) → **Priority review**
3. accuracy < `revise_accuracy` (50%) → **Needs revision**
4. recent accuracy ≥ earlier accuracy + `improving_delta` (10 points) with at least `min_recent` (4) answers in each window and accuracy still below the strong bar → **Improving**
5. accuracy ≥ `strong_accuracy` (80%), at least `min_sessions` (2) sessions and a correct re-check of a question after at least `retention_days` (5) days → **Strong evidence of understanding**
6. otherwise → **Developing**

There is no hidden model: every status can be traced to the numbers shown beside it. These are signals for planning, not predictions of exam results, and the wording avoids absolute claims.

**Recommendations** (suggestions only; nothing is assigned until a mentor approves):

* Misconception check: P4 count in a chapter ≥ `alert_high_errors` (2)
* Targeted review: chapter "Needs revision" (mentions the prerequisite chapter from the taxonomy)
* Confidence builder: at least 40% of correct answers rated Guess/Low with ≥ 6 answers
* Retention check: chapter developing/improving/strong with enough questions but no delayed re-check yet

## 5. Data model (new tables only; no migration needed, created by `db.create_all()`)

`rf_taxonomy`, `rf_questions` (qid + version, `active` flag, status, answer/explanation/misconception), `rf_students` (roster, mentor, exam, group, parent_report, demo),
`rf_assignments`, `rf_assignment_students` (unique per assignment + student), `rf_items` (the questions a student was given), `rf_drafts` (autosave),
`rf_attempts` (**immutable** attempt history: answer, confidence, correctness, marks, seconds, question version), `rf_observations`, `rf_recommendations`,
`rf_notices` (unique per user + dedupe key), `rf_settings`, `rf_audit`.

Existing tables reused: `User` and tiers, mentor links (`MsEnrolment`, `PulseProfile`) for roster import, parent links (`MsParentLink`, `FrParentLink`),
and the JEE / UCEED mock results (shown beside, never mixed into, the reinforcement figures).

## 6. Integration assumptions

* Students must already have an account; the mentor adds them by e-mail or imports their existing mentees.
* Parent access reuses the existing parent links and adds a per-student on/off switch controlled by the mentor.
* Question content: the starter bank is the original EduAakashaA mock questions (computed answers, worked solutions). Previous-year NTA papers are **not** in the bank because their answer keys are not yet applied.
* Times are stored in UTC and shown in IST.
* The mock test centres, EduPulse-UCEED and the Mentorship Portal are untouched; their tests still pass.

## 7. Security and privacy

Server-side role checks on every route; answer keys never leave the server until `released()` allows it (checked in `/api/asg/<id>/review`; the question payload carries no key);
saves after completion are refused (409); question HTML is sanitised with an allow-list; CSV import is validated in full before anything is written; admin exports exclude demo data;
a token-protected `/cron/events` endpoint (env `REINFORCE_CRON_TOKEN`) can send deadline notices if a scheduler is configured, otherwise events are processed when staff and students open their pages.

## 8. Example report (parent, weekly, sample data)

> **Aarav · last 7 days** · 24 questions practised (previous week: 16) · 4 days practised · accuracy 61% (previous: 55%)
> *Strengths building:* Laws of motion (strong evidence of understanding), Kinematics (developing).
> *Being worked on:* Work, energy & power: some answers are still incorrect despite high confidence. The mentor is reviewing the underlying concept and will reassess next week.

## 9. Testing and deployment

* `python tests/test_reinforce.py` covers access control (anonymous, free, student, parent, other mentor), popup rules, remind-later, the full answer flow with mandatory confidence, resume, idempotent submit, immutability, grading with negative marks (mcq, msq, numerical), release rules, notice de-duplication, pattern and chapter-status formulas, recommendations needing mentor approval, question workflow and versioning, CSV import validation, parent access, demo isolation and threshold validation.
* Related suites re-run: member home, EduPulse-UCEED, UCEED mock centre, EduPulse-JEE, FutureReady. (`test_mentorship_portal` has one earlier, unrelated failure on a hub image name.)
* Deployment: no manual step. On the next deploy the tables are created automatically. Then, as admin: **Admin → Load starter bank**, add students on **Roster**, assign practice. Optional: set `REINFORCE_CRON_TOKEN` and call `/edupulse-reinforce/cron/events?token=…` from a scheduler.
* Local preview with sample data: `python tools/rf_dev_server.py` (temporary database, port 5077).

## 10. Acceptance criteria status

| Criterion | Status |
|---|---|
| Popup only for pending work; none for completed | ✔ tested |
| Cannot proceed without a confidence rating | ✔ tested (client and server) |
| No answer keys before release | ✔ tested |
| Attempt history immutable; question edits create versions | ✔ tested |
| Chapter judgements need minimum evidence | ✔ tested |
| Mentor approval before any adaptive assignment | ✔ tested |
| Parents see only linked children with report enabled | ✔ tested |
| Existing mock tests unaffected | ✔ suites re-run |
| Large question bank | starter bank only (660 original questions: 375 JEE and 285 UCEED, 5 to 15 per JEE chapter); a larger bank needs authored content or CSV import |
