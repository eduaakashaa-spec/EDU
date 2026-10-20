# EduAakashaA Mentorship Portal

> One student. One connected mentorship journey. Three coordinated dashboards.
> Sessions, actions, KPIs, reviews, branch fit, college preferences and the final report — all read from one record.

This document is the product blueprint **and** the operating manual for the portal that is live in this repo.
Code: `app/models_mentorship.py` · `app/services/mentorship.py` · `app/routes/mentorship.py` ·
`app/templates/mentorship/*` · `app/templates/admin/mentorship_admin.html` · `app/static/css/mentorship.css` ·
tests: `tests/test_mentorship_portal.py`.

---

## 1. Deliverable A — Blueprint

### 1.1 Architecture (decision: extend the existing app, no new stack)

The existing site is a Flask app (app factory, blueprints, Jinja, SQLAlchemy, Flask-Login, Postgres on Neon, Render).
The portal is **one more blueprint** (`mentorship_bp`, prefix `/mentorship`) in the same app — same login, same
membership tiers, same design system — so there is nothing to embed or integrate separately.

| Concern | How it is done |
|---|---|
| Frontend | Server-rendered Jinja, `mentorship.css` (navy `#0E3A8A`, orange `#FF6B0A`, cream `#FBF7EE`, dark-mode aware, mobile-first). No JS framework. |
| Auth | The existing Flask-Login session. No second login. |
| Authorisation | Enforced **on the server** per request by `services.mentorship.role_for()`; templates only hide what the server would refuse anyway. |
| Database | New tables only (`ms_*`), created by `db.create_all()` — **no migration, no change to existing tables**. |
| Reports | ReportLab PDF (`reportlab` in `requirements.txt`); if it is missing the page falls back to a print-friendly view ("Print → Save as PDF"). |
| Notifications | In-portal messages and unread badges only. **Email/WhatsApp are not connected** and the UI says so (see §4). |
| Premium link | The student side requires live Premium status (`user.is_premium`); the portal is a tile in **Member Home → Mentorship Portal** and `premium_locked.html` is shown to non-Premium students. |

### 1.2 Roles and how they are decided

| Role | Who | Resolved by |
|---|---|---|
| **admin** | tier `admin` | `user.is_admin` — can open any record, owns configuration |
| **mentor** | tier `ea_mentor` | `enrolment.mentor_id == user.id` — only **assigned** students |
| **student** | the enrolled user | `enrolment.student_id == user.id` **and** Premium |
| **parent** | any account linked by an admin | row in `ms_parent_links` for that enrolment |
| (none) | everyone else | **404** (record ids cannot be probed) |

An account can hold different roles on different records (e.g. a parent of one student). Alumni "College Guides"
(tier `mentor`) are a different role and have no access.

### 1.3 Permission matrix

| Capability | Student | Parent | Mentor (assigned) | Admin |
|---|:-:|:-:|:-:|:-:|
| View own/linked student record | ✔ | ✔ (limited) | ✔ | ✔ any |
| Private mentor notes / internal messages | ✖ | ✖ | ✔ | ✔ |
| Student weekly reflections | ✔ own | ✖ (only a mentor-shared summary) | ✔ | ✔ |
| Schedule / edit / reorder sessions | ✖ | ✖ | ✔ | ✔ |
| Add **extra** session | ✖ | ✖ | ✔ within package allowance | ✔ always |
| Add / review actions | complete & comment on own | parent-owned only | ✔ | ✔ |
| Submit weekly check-in | ✔ | ✖ | ✖ (reviews) | ✖ (reviews) |
| Create / edit KPIs and record values | ✖ | ✖ | ✔ | ✔ |
| Branch-fit: interest/family ratings | ✔ interest + family | ✔ family view | ✔ readiness + feasibility | ✔ |
| Preference list: edit entries | ✔ | comment only | ✔ | ✔ |
| Approve list (family) | ✔ | ✔ | ✔ | ✔ |
| Mark "Ready for official portal entry" | ✖ | ✖ | ✔ | ✔ |
| Quarterly review: create / finalise / share | ✖ | ✖ | ✔ | ✔ |
| Review reflection / feedback | ✔ own (when requested) | ✔ (when requested) | read | read |
| Generate / approve / share report | ✖ | ✖ | ✔ | ✔ |
| View shared report | ✔ | ✔ | ✔ | ✔ |
| Activity history (audit) | ✖ | ✖ | ✔ | ✔ |
| Programmes, templates, enrolment, parent links, rules, branch catalogue, programme calendar | ✖ | ✖ | ✖ | ✔ |

### 1.4 Data model (all tables prefixed `ms_`, defined in `app/models_mentorship.py`)

```
ms_programmes ─┬─ ms_session_templates          (core sessions of a programme; count is data, not code)
               ├─ ms_events                     (programme calendar template: dates + source + verified_on)
               └─ ms_enrolments ─┬─ ms_parent_links → users
 (student_id, mentor_id → users) ├─ ms_sessions        (kind: core|extra|intervention|follow-up; planned_at ≠ actual_at)
                                 ├─ ms_actions         (owner, priority, due, status, evidence, feedback, parent_visible)
                                 ├─ ms_checkins        (one per week; draft → submitted → reviewed)
                                 ├─ ms_kpis ─ ms_kpi_obs
                                 ├─ ms_reviews         (Draft → Awaiting input → Ready for review → Finalised → Shared)
                                 ├─ ms_branchfit, ms_branch_ratings   (+ ms_branches = admin catalogue)
                                 ├─ ms_pref_lists ─ ms_pref_entries
                                 ├─ ms_events          (student-specific)
                                 ├─ ms_messages ─ ms_message_reads
                                 ├─ ms_reports         (frozen JSON snapshot: Draft → Approved → Shared)
                                 └─ ms_audit           (who changed what)
```

Stable integer ids, `created_at`/`updated_at` where it matters, foreign keys with cascade rules.

### 1.5 User journeys

* **Student:** Member Home → *My Mentorship* → Home (five answers: where am I / what's done / this week / biggest
  priority / what's next) → Sessions → Weekly Plan (complete actions, request help, submit the weekly check-in) →
  KPIs → Branch Fit → College Preferences → Calendar → Messages → Reports.
* **Mentor:** Mentor dashboard (10 clickable KPI cards that filter the student table) → student workspace (same tabs +
  staff forms) → record session → assign actions → review check-in → record KPI value → quarterly review → generate,
  approve and share the report.
* **Parent:** Overview → Sessions (recaps the mentor chose to share) → KPIs → Reviews (shared only) → Branch fit
  (add family view) → Preferences (comment, approve list) → Reports → Messages with the mentor.
* **Admin:** Admin → Mentorship → load/edit programme → enrol student (+ mentor, extra-session allowance) → link parent.

---

## 2. Deliverable B — What is built

| Spec area | Where | Notes |
|---|---|---|
| Student / mentor / parent dashboards | `tab_home.html`, `mentor_home.html` | Same data; role decides what is shown. |
| 10+ expandable sessions | `ms_session_templates` + `MsSession` | Default programme has the 10 specified sessions; admins add/edit/reorder/deactivate rows, mentors add extra/intervention/follow-up sessions. Status: Planned · Completed · Partially completed · Rescheduled · Cancelled · Missed. **Cancelled never counts as completed**; planned and actual dates are stored separately; session completion is independent of action completion. |
| Package control of extra sessions | `MsEnrolment.extra_quota` | Mentors can add extra sessions only within the allowance; admin can always add/raise it. |
| Weekly follow-up | `tab_weekly.html` | Review last week's actions → confidence (1–5) → reflection → next priority → urgent-help flag; save draft or submit; mentor reviews, comments, re-prioritises, schedules an intervention, shares a parent summary. |
| Action engine | `MsAction`, `services.action_state` | Labels: Due today · Due soon · Overdue · Completed on time · Completed late · Blocked · Requires mentor attention. Cancelled actions leave the completion denominator (rule shown in the UI). |
| KPI engine | `MsKpi`, `MsKpiObs`, `services.kpi_view` | Higher/lower is better, range, milestone, qualitative; baseline, target, unit, method, frequency, owner, trend; pause/archive. Marks/rank KPIs are flagged **exam outcome** and shown separately from effort KPIs. Values change only through an authorised entry. |
| Attention rules | `services.attention`, Admin → Attention rules | Overdue count, missed check-in gap, low confidence, help requests, missed session, exam soon with open actions. Thresholds editable (`Setting` keys `ms_rule_*`). Workflow prompts only. |
| Quarterly reviews | `tab_reviews.html` | Pre-populated snapshot (sessions, actions, KPIs, check-ins), compared with the previous review; student reflection and parent feedback; finalise then share. |
| Branch fit | `tab_branch.html`, `ms_branches` | Interest, readiness, feasibility and family fit are **four separate ratings**; the weighted view uses student-chosen weights and prints the formula. Mentor observations never overwrite the student's own. |
| College preferences / choice filling | `tab_prefs.html` | Multiple draft lists, reorder (↑ ↓, accessible), remove, per-choice interest/eligibility/data note **with year and source**, mentor recommendation, parent comment, nine-step workflow status, change history, "final family-approved list". A banner states EduAakashaA does **not** submit to official portals. |
| Exam catalogue, follow list & alerts | `tab_calendar.html`, `services/exam_calendar.py`, Admin → Mentorship → Exam catalogue | Admin-maintained list of exams (`ms_exams`, each with status Confirmed / Tentative / Expected, dates, source, last-verified). Students and mentors **follow** the exams they care about (`ms_exam_focus`, per student record); followed exams join the calendar. **Share:** download a `.ics` invitation (all followed or one exam), add to Google Calendar, or **email the invite** (with the .ics attached, from info@) to any personal address (max 5/hour/user). **Alerts:** adding an exam shows a *New exam added* alert with an **Add to my calendar** button; changing dates/status/name/source or removing an exam shows a *Schedule change / removed* alert with before → after — to every student, parent and mentor, plus an email from info@ when sending is configured. Re-saving with no real change alerts nobody. Each change bumps the exam `version` (ICS `SEQUENCE`), so re-importing the .ics updates calendar entries. |
| Calendar | `tab_calendar.html` | Merges programme events, student events, sessions, action due dates, review dates; filter by category; every event shows **source and last-verified date or "unverified"**. Agenda view. |
| Messaging | `tab_messages.html` | Audiences: student, parent, all (announcement), **internal** (mentor-only). Unread badges. |
| Final report | `tab_reports.html`, `report_view.html`, PDF | Draft → Approved → Shared snapshot; "Not recorded" for missing data (never zero); disclaimer; PDF download. |
| Admin controls | Admin → **Mentorship** | Programmes, session templates (count/order/topics/deliverables), enrol student, mentor assignment, extra-session allowance, parent links, programme calendar, attention rules, branch catalogue. |
| Audit | `ms_audit`, Activity History tab | Every write is logged with role and detail. |
| Member Home | `services/member_hub.py` | New **Mentorship Portal** category (premium), with a staff-only *Mentor dashboard* tile. |

---

## 3. Deliverable C — Data, security and setup

**Persistence:** everything is in the application database (Neon Postgres in production, SQLite in tests).
Refreshing the page never loses data.

**Security**
* Server-side role check on every route (`_ctx()` / `role_for()`); unauthorised access to a record returns 404, wrong role on a
  known record returns 403; anonymous users are redirected to login.
* A student cannot read another student; a parent only sees linked records; a mentor only sees assigned students; unrelated users get 404.
* Private mentor notes and internal messages are filtered **in the queries/render**, not only hidden in the page.
* Inputs are length-limited and validated on the server (ratings 1–5, statuses against allow-lists, dates parsed).
* No secrets, passwords or real student data are in the repository. Demo data exists only in tests and is labelled `DEMO`.
* Parent view never shows student reflections, private notes or internal attention flags; a mentor can share a written summary.
* Academic mentoring only: pages carry a note that this is not medical/psychological care and that outcomes are not guaranteed.

**Setup (production)**
1. `pip install -r requirements.txt` (adds `reportlab` for PDF).
2. Deploy — new tables are created on boot by `db.create_all()`. No migration is required.
3. Sign in as admin → **Admin → Mentorship → Load standard 10-session programme**.
4. Make sure the mentor has the **EA Mentor** role (Admin → Members) and that student and parent have accounts.
5. **Enrol a student** (student email, programme, mentor, extra-session allowance) → **Link parent** (parent account email).
6. Add the real exam / counselling dates under **Programme calendar**, each with its official source and last-verified date
   (nothing is pre-loaded because dates change every year).
7. The student must have **Premium** access (Premium Portal Access or a mentorship path) to open the portal.

**Notification integration points** (not connected): `routes/mentorship.message_post`, `checkin_review`, `report_step` are the places
to call `services.mailer.send_async(...)` once you want email alerts. Until then the UI states "Email / WhatsApp notification is not connected".

---

## 4. Deliverable D — Quality, limitations, deployment

**Automated checks:** `python tests/test_mentorship_portal.py` runs the 22 acceptance workflows on demo data — enrolment, mentor
assignment, journey display, scheduling, 11th session, check-in, review, task completion reflected on the dashboard, KPI baseline/target/update,
review pre-population, branch fit, preference review, parent visibility, student/parent/mentor isolation (including 404 on other records),
calendar sources, report with missing-data labels and PDF, cancelled ≠ completed, persistence across a DB reconnect, and external notifications stated as not connected.
Related suites (`test_member_home.py`, `test_ea_mentor_role.py`, …) still pass.

**Known limitations (honest list)**
* **Updates are page-load/refresh, not live push.** Dashboards read the same database, so a refresh always shows the latest; there is no websocket or auto-refresh.
* **Email / WhatsApp / push are not connected** (in-portal notifications only).
* **Exam alerts** are in-portal (shown until dismissed, 45-day window) plus email only when `RESEND_API_KEY`/SMTP is configured; there is no WhatsApp/push. Parents are alerted but cannot follow exams. The starter exam list mirrors the public exam-schedule page (October 2026): *Expected* rows carry only a likely window, so an admin must edit them when the official notice appears — that edit then alerts everyone.
* **Calendar is an agenda view** (grouped by month with category filter); month/week grid and drag-and-drop are not built. Reminder preferences are not built.
* **College dataset import** is not built: choices are entered per student with year + source. There is no bulk college/cutoff database and no live cutoffs, fees or eligibility rules — those must be entered and verified by a person.
* **Preference reordering uses ↑/↓ buttons** (accessible), not drag-and-drop.
* **Attachments/evidence** are links (URLs), not file uploads; message attachments are not supported.
* **Parent access** is per enrolment, linked by an admin; parents do not self-register against a student.
* **Time zones:** session times are stored in UTC and shown in the enrolment's time zone (default `Asia/Kolkata`); the zone is editable by an admin. On servers without a tz database it falls back to IST.
* **Reflections privacy** is enforced for the roles above; there is no separate consent record yet.
* **Mentor dashboard** computes rows per student (fine for tens/hundreds of students; add caching/aggregation before thousands).
* **Role permissions are fixed in code** (the matrix above); admins cannot yet edit them from the UI. Likewise report templates and KPI templates are code constants (`PRESET_KPIS`).
* A report states facts as recorded; it never predicts rank, seat or branch.

**Deploying into the existing membership area:** already done in code — Member Home → *Mentorship Portal* → *My Mentorship*, header "Mentorship Portal" link for admins and EA mentors,
Admin → Mentorship for configuration. Pushing to `main` deploys via Render auto-deploy; no extra service is needed.

**Extending:** a new grade or pathway is a new `MsProgramme` row plus its session templates (Admin → Mentorship). New KPI presets go in `services.mentorship.PRESET_KPIS`;
attention thresholds are editable in the admin page; new tabs are a function `_tab_<name>` in `routes/mentorship.py`, a template `tab_<name>.html` and an entry in `services.mentorship.TABS`.

## Parent onboarding assessment

When an admin links a parent (new or existing account), the parent is emailed from info@eduaakashaa.com with direct links to **that student's** dashboard and to `/mentorship/e/<id>/parent-assessment`. Only a parent linked to that enrolment (plus the assigned mentor and admin, read-only) can open it; the student gets 403 and other students' parents get 404. Answers are stored per parent in `ms_parent_assessments` (JSON), the parent's dashboard shows a "Next step" nudge until submitted, and Admin → Mentorship shows *assessment submitted / pending* with a **resend invite** button. If email is not configured nothing is sent and the admin is told.

## Ready-made add-on programmes and design/architecture branches

`app/data/mentorship_addons.py` defines nine ready-made add-ons: UCEED, NID DAT, NIFT, IIT Delhi–Abu Dhabi, TNEA, State-specific admission, SRM, Amrita and VIT (6–8 sessions each, a deliverable per session). **Admin → Mentorship → Load add-on programmes** creates any that are missing as normal programmes (tier `Add-on`; idempotent, admin edits kept), after which *Enrol student* works as usual. Members see the catalogue at `/mentorship/addons` (Member Home → Mentorship → "Add-on programmes") and can request one; requests are stored as `PageLead(source='mentorship-addon')` and emailed to info@ when email is configured. Sessions never state dates, fees or cut-offs — each points to the official notice. "CEAT" in the original request was read as the IIT Delhi–Abu Dhabi route; edit that programme if something else was meant.

The Branch catalogue (`DESIGN_BRANCHES` in `services/mentorship.py`) now also holds Architecture (B.Arch), Planning, Interior, seven NID B.Des discipline groups and four NIFT groups (B.Des streams, B.FTech Apparel Production). `ensure_branches()` adds missing defaults by name, so existing sites receive them without touching edited rows.

## Action tracker (meeting actions, owners, completion, sharing)

Every member's workspace has an **Action Tracker** tab (students, linked parents, mentors, admin). Actions carry an **owner** (student / parent / mentor), due date, priority and status, optionally linked to the session where they were agreed. Each owner updates their own: students mark student actions, a linked parent marks parent actions, the mentor/admin can update any. Progress is shown per owner (done ÷ total, overdue, needs help); cancelled actions are excluded; parents only see actions marked visible to them.

- **Add from meeting notes (staff):** paste one action per line — `owner | action | due date | priority` (also `parent: action`, dates as YYYY-MM-DD or DD/MM/YYYY). Invalid lines are reported and skipped.
- **All members:** `/mentorship/actions` (Mentor dashboard → Action tracker; Member Home tile for staff) lists every action across members, filterable by status, owner and member, with per-member progress and a **CSV export**. Admins see all members; mentors see their own.
- **Share:** *Email action list* sends a branded table from info@eduaakashaa.com to any of student / linked parents / mentor (parents receive only parent-visible actions; 20 sends per user per hour; audit logged). *WhatsApp* buttons open WhatsApp with the message pre-filled, using the phone saved in the student's profile (otherwise WhatsApp asks for the contact).
Test: `tests/test_action_tracker.py`.
