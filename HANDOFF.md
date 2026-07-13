# EduAakashaA — Handoff for a New Chat

Paste this whole file into a fresh chat so the assistant can continue without
re-discovering everything. It captures the project layout, how to run/verify/
deploy, the accounts, the conventions used, and what's still open.

> Repo root: `/Users/asfaque/Desktop/EDU` · App lives in `college-predictor/`
> Git: branch `main`, auto-deploys to Render on every push.
> Live site: <https://eduaakashaa.onrender.com> (also the legacy reference site
> <https://www.eduaakashaa.in/>, a Hostinger build we are migrating away from).

---

## 1. What this is

A Flask college-admission-guidance portal for Indian / NRI engineering aspirants
(DASA/CIWG, JOSAA, TNEA, TANCET, NIRF, career planning). Being migrated from a
Hostinger/Google-Apps-Script site into a proper Flask + Postgres app.

**Stack:** Flask (app factory) · SQLAlchemy + Flask-Login + Flask-Bcrypt ·
PostgreSQL on **Neon** · hosted on **Render** (gunicorn, free tier, `render.yaml`,
autoDeploy from `main`) · GitHub Actions pings `/ping` every 10 min to beat the
free-tier sleep. Data (JOSAA/NIRF/DASA CSV+Excel+JSON in `app/data/files/`)
loads into memory at startup.

**Docs already in the repo (keep them updated):**
`college-predictor/README.md` (overview/routes/design system),
`college-predictor/ARCHITECTURE.md` (status table + technical detail),
`college-predictor/GUIDE.md` (setup + admin/day-to-day usage — §3 is the admin
guide, §3.5 is the Alumni/Mentor network).

---

## 2. Layout (where things live)

```
college-predictor/
  run.py                    # dev entry (loads .env, python run.py)
  manage.py                 # CLI: init_db, seed_sequences, create_admin, seed_demo
  config.py                 # Config: DATABASE_URL, SECRET_KEY, MAX_CONTENT_LENGTH(10MB),
                            #   SQLALCHEMY_ENGINE_OPTIONS(pool_pre_ping+pool_recycle), COMPANY/GST
  app/
    __init__.py             # create_app(): registers blueprints, 413 handler, context processor
    decorators.py           # admin_required, premium_required, mentor_required
    models.py               # User, DasaLead, Prediction, Payment, PageLead, ContactInquiry,
                            #   Announcement, ScheduleEvent, AlumniProfile, MentorMeeting, MentorMessage,
                            #   CollegeSurvey
    models_membership.py     # MembershipApplication, MembershipInvoice, DocSequence
    routes/
      __init__.py (main_bp) # all public content pages + premium pages (render_reference_page/_premium)
      api.py                # JSON endpoints incl. POST /api/leads (generic lead capture)
      auth.py               # login/register/logout/dashboard/contact
      membership.py         # /admin/membership + /admin/leads + /admin/inquiries + /admin/users (admin_required)
      admin_portal.py       # /admin control panel (overview w/ KPIs+charts, users, announcements,
                            #   schedule, messages, /admin/templates email templates)
      alumni.py             # Alumni/Mentor network: public /alumni-network, /mentor portal, /admin/alumni
      survey.py             # College Experience Survey: public /college-survey, /admin/surveys (SECTIONS-driven)
    templates/  static/(css|js|files)
  tests/  -> ../tests/smoke.spec.ts + all_pages.json   (Playwright, 87 pages)
```

---

## 3. Accounts, tiers & RBAC

`User.tier` ∈ **free | premium | admin | mentor**. Decorators in
`app/decorators.py`:
- `admin_required` → tier admin (else 403; anon → login).
- `premium_required` → `is_premium` (admin OR premium-not-expired). Non-premium
  logged-in users get `premium_locked.html` (403); anon → login.
- `mentor_required` → tier mentor (the alumni portal).
- `is_premium` treats a naive `tier_expires_at` as UTC (fixed a 500 — don't
  regress this).

**Real production accounts (Neon) — do NOT delete:**
- `eduaakashaa@gmail.com` — **admin** (password unknown to the assistant).
- `asfaque2004@gmail.com` — **premium**, password currently `123`
  (**weak — the user should change this**; it was set for testing on request).

**Testing accounts:** create throwaway `*@example.com` users as needed, then
**always delete them at the end** (they live in the *production* DB — see the
big warning in §4). Convention used all session: throwaway admin =
`admin-test@example.com` / `test123`.

---

## 4. Running & verifying locally

```bash
cd college-predictor
.venv/bin/python run.py        # or: PORT=5001 FLASK_DEBUG=0 .venv/bin/python run.py
# app takes a few seconds to boot (loads data); poll http://localhost:PORT/ for 200
```

⚠️ **CRITICAL GOTCHA:** `college-predictor/.env` currently points `DATABASE_URL`
at the **production Neon database**. So *running locally reads/writes live data*.
This is how prod DB migrations were applied this session (convenient) but it
means: any test rows you create locally are in prod — clean them up. If you want
true isolation, point `.env` at SQLite first.

**Preview/browser tooling:** this session used `mcp__Claude_Preview__*` and
`claude-in-chrome` MCP tools; they drop in and out. When unavailable, just run
the app with Bash + `curl` and drive flows that way (works fine).

**Smoke tests (from repo root, app running):**
```bash
BASE_URL=http://localhost:PORT ./node_modules/.bin/playwright test tests/smoke.spec.ts --reporter=line
# 87 pages: status <400, no JS console errors, non-empty. Add new PUBLIC pages to
# tests/all_pages.json (auth-gated pages like /mentor and /admin/* are NOT listed).
```

**Deploy:** `git push origin main` → Render autoDeploys (~3–7 min). Verify on
`https://eduaakashaa.onrender.com`. The DB schema is auto-created for *new*
tables via `db.create_all()` on boot, but **it does NOT ALTER existing tables** —
see §6.

---

## 5. What was built recently (newest first)

- **Homepage redesign v2** (`templates/home.html`, self-contained `hx-*` styles/JS):
  editorial hero ("The right college isn't luck. It's data.") with staggered word
  reveal + rotating exam word + drifting constellation canvas; a **live DASA-demo
  card** that types a rank and cascades real 2025 SAFE/REACH/DREAM rows; college
  marquee; count-up stats; scroll-drawn journey path (4 steps light up); dark navy
  "Try the engines" tool showcase with tilt cards; pathway cards; auto-rotating
  testimonial carousel; magnetic CTA. All vanilla JS, IntersectionObserver reveals
  with a scroll-sweep fallback (instant jumps can skip IO), honors
  prefers-reduced-motion. Verified via Playwright in real Chromium
  (animations settle, zero console errors).

- **Onboarding assessment — LIVE in-app** (design in `ONBOARDING_ASSESSMENT.md`; built out across
  `app/services/onboarding_assessment.py`, `app/routes/onboarding.py`, `OnboardingResponse` model,
  templates `onboarding_landing.html` / `onboarding_assessment.html` / `admin/onboarding_*.html`):
  the two-part instrument (student 60 items + parent 34 items — RIASEC / Big Five / SDT /
  self-efficacy / work values / light aptitude, dyadic ALIGN pairs) is now a real mobile form.
  `/onboarding-assessment` → pick student or parent → a **one-question-per-screen stepper**
  (progress bar, per-type widgets: likert, most/least forced-choice, rank, pick-2, choice-pair,
  num, SJT, open). Answers save to `onboarding_responses` keyed by item id (S1…/P1…). The two
  halves of a family pair on `family_key` (normalised student name + phone/email). Admin
  **People → Onboarding Assessments** (`/admin/onboarding`) lists families with student/parent
  status; the detail page renders both halves by module+tag and has a **Copy for AI** button that
  bundles the answers with a pointer to the Deliverable-2 rubric + Deliverable-3 dossier template.
  Confidential items (S50/P34) are shown counsellor-only and flagged. The questions live in ONE
  data module (`onboarding_assessment.py`) that drives the form, validation and admin display —
  edit that list to change questions; no migration (new table auto-creates on boot). The
  `assessment_invite` email template (student + parent) sends the link out.
- **Admin made faster** (`app/services/queries.py` `count_if`/`sum_if` + all admin routes):
  every KPI block now runs as ONE conditional-aggregate SELECT instead of N separate
  COUNTs — `/admin` overview went from **47 → 23 queries** per load; users/membership/
  alumni lists 7 → 4, surveys 5 → 3. On remote Neon Postgres, round trips dominate, so
  this is roughly a 2× server-time cut. Chart.js also moved out of `<head>` (no longer
  render-blocking). When adding new admin stats, extend the aggregate query — don't add
  another `.count()`.
- **Admin Email Templates v2** (`app/services/email_templates.py` registry;
  `templates/admin/templates.html` composer; `admin_portal.templates()` +
  `_recipient_directory()`): cards now grouped by category (Members & Onboarding /
  Admissions & Payments / College Guides / Engagement & Season) with 19 scenarios —
  added assessment invite (student/parent), session confirmed, session recap, report
  delivered, documents (missing/received), application approved, payment reminder,
  payment received (full/partial), deadline alerts (JoSAA/TNEA/other), win-back,
  feedback request, inquiry response. The **To** field is a searchable dropdown of every
  known contact (members, College Guides, leads, inquiries — deduped, capped, admin-only)
  and autofills the name/college placeholders. Emails render in a branded shell with the
  EduAakashaa logo (absolute prod URL so Gmail can load it), tagline, contact footer
  (India WhatsApp + UAE phone). Nothing is auto-sent. To add a template, edit
  `EMAIL_TEMPLATES` in `app/services/email_templates.py`.
- **Enhanced `/admin` overview** (`admin_portal.home`, `templates/admin/portal_home.html`):
  grouped KPI bands (members / membership & ₹ revenue / leads-inquiries-surveys /
  College-Guide activity & ₹ payouts / weekly growth) + **4 Chart.js charts** (8-week
  activity line, members-by-type doughnut, apps-by-status bar, top-lead-sources bar) +
  expanded recent-activity feeds (incl. newest guides & surveys). Revenue from
  `MembershipInvoice.amount_paid`, payouts from completed `MentorMeeting`s. Chart.js via CDN.
- **"Mentor network" → "College Guides" rebrand** (user-facing copy only; `tier='mentor'`,
  `/mentor` routes and models unchanged). Payout copy simplified to **"answer questions,
  ₹500–1000"** (no meeting/video split, no "per session"); referral bonus ₹1000.
- **Removed 4 unused pages** — Internship, Training, NRI Arabic (Foundation & Grammar):
  routes in `routes/__init__.py`, templates, nav links, home card, `tests/all_pages.json`.
- **College Experience Survey** (`routes/survey.py`, `templates/college_survey.html`,
  `templates/admin/surveys_list.html` + `survey_detail.html`):
  - Free, public `/college-survey` (linked from the **More** nav dropdown): a
    **deliberately exhaustive** "rate your college" survey — 10 sections / ~96
    questions (academics, placements, infra, hostel/food, amenities, campus life &
    safety, admin, location, verdict), mostly one-tap ratings + MCQs + short/long
    text. Required: name, email, phone, college, entrance-exam/rank; **college &
    branch are typeable `<datalist>` dropdowns** (colleges from
    `loader.get_college_names()`, branches from `get_branch_names()`; branch
    dropdown also on the mentor form). Doubles as a **mentor-recruitment funnel**
    (opt-in checkbox + thank-you CTA → `/alumni-network`).
  - **Definition-driven:** the whole question set is one `SECTIONS` list in
    `survey.py` — it renders the form, validates the POST (drops unknown keys /
    invalid choices / out-of-range scores) and drives the admin display. Answers
    live in a single `CollegeSurvey.responses_json` blob keyed by question id;
    only name/email/phone/institute/branch/batch/overall_rating/recommend_score/
    wants_to_mentor are first-class columns (for search/sort). **Add/reorder
    questions = edit `SECTIONS`, no DB migration.** Per-IP rate limit (20/hr).
  - **Admin `/admin/surveys`** (new **Surveys** tab): responses **grouped by
    college** (collapsible, most-reviewed first) + search + KPIs, and a
    per-response detail page grouping every answer by section (rating pills +
    written notes + "open to mentoring" contact).
- **Alumni / Mentor Network** (`routes/alumni.py`, `templates/alumni_network.html`,
  `templates/mentor/dashboard.html`, `templates/admin/alumni_*.html`):
  - Public `/alumni-network` (linked from the **More** nav dropdown): recruits
    alumni/students at top unis to mentor parents in paid sessions. Copy is in
    **₹** ("₹1000 per meeting", "₹500 per video Q&A", "₹1000 per referral"). Collects academic
    details + a **photo** (validated by extension **and magic bytes**, capped
    ~200 KB, stored in Postgres) + a **resume link** (pasted Drive/Dropbox/URL,
    http(s)-validated — only the URL is stored, no more `LargeBinary`) + a
    **password**.
  - Registration **creates a `mentor`-tier login** (one per email, race-safe) and
    auto-logs them in. Per-registrant **referral link** `?ref=CODE` recorded as
    `referred_by` (validated against real codes; `javascript:`/non-http URLs
    stripped; per-IP rate limit 10/hr + 10-min email dedup on the endpoint).
  - **Mentor portal `/mentor`** (`mentor_required`): ₹ earnings (total/pending/
    paid) + calls attended, sessions table, referral link + who joined, two-way
    **messages with admins**, editable profile. Header shows "Mentor Portal";
    `/dashboard` redirects mentors here.
  - **Admin `/admin/alumni`** (admin tab): list/search, profile detail, admin-only
    resume-link + photo view (`send_file`, attachment + `nosniff`), status
    workflow, **log sessions with ₹ payout + mark paid** (kinds: meeting ₹1000 /
    video Q&A ₹500 / referral / bonus / adjustment), reply to messages, referral
    tree.
  - **Auto referral bonus:** when a referred mentor completes their **first**
    meeting, the referrer is credited a one-time **₹1000** (a `kind='referral'`
    `MentorMeeting`, idempotent via `MentorMeeting.referred_alumni_id`; counts
    toward earnings, not "calls attended"). Logic: `_maybe_credit_referral()` in
    `alumni.py`, called after `admin_add_meeting`. Constant `REFERRAL_BONUS_INR`.
- **EA Admin Control Panel** (`routes/admin_portal.py`): `/admin` overview (KPIs +
  activity), member management at `/admin/users` (change tier free/premium/admin,
  set/clear validity, reset password, add/delete with lockout guards),
  announcements, schedule, message templates. `Announcement` + `ScheduleEvent`
  surface on member dashboards. The Admin nav button + legacy `/ea-admin-portal`
  both land on `/admin`.
- **Premium content pages** — 8 full ports from the live site, `@premium_required`:
  `/why-cse`, `/best-location`, `/engineering-insights`,
  `/hostel-and-culture-analytics`, `/tnea-expert`, `/josaaea-members`,
  `/expert-portaldasa`, `/engineering-branch-selection-guide`. Their in-page lead
  forms post to `/api/leads`.
- **Choice Builder PRO** `/choice-builder-pro` (admin) — the team's DASA analyzer
  tool migrated in-app (D3 + Chart.js). **Counsellor Dashboard**
  `/counsellor-dashboard` (admin) reads the team Google Sheet live via its Apps
  Script JSONP API.
- **DASA 2026 Schedule** `/dasa2026-schedule` (public) + a real `.ics` download.
- Fixes: Neon SSL drops (`pool_pre_ping`+`pool_recycle`), premium-expiry 500,
  duplicate WhatsApp floaters, broken `@import` on the TNEA page, DASA lead
  capture wired to `/api/leads`.

Data lands in Postgres and shows in admin: memberships→`/admin/membership`,
form/assessment leads→`/admin/leads`, contact→`/admin/inquiries`,
accounts→`/admin/users`, mentors→`/admin/alumni`, college surveys→`/admin/surveys`.

---

## 6. Conventions & gotchas (IMPORTANT — read before changing things)

- **DB migrations are manual.** No Alembic. `db.create_all()` creates *missing
  tables* on boot but never alters existing ones. To add a column to an existing
  table, run a one-off `ALTER TABLE …` against the DB (via a `.venv/bin/python`
  script that `load_dotenv()`s — which hits **prod Neon**). Example done this
  session: `ALTER TABLE mentor_meetings ADD COLUMN referred_alumni_id INTEGER`.
  For an *empty* table you can instead drop it and let `create_all` rebuild it.
- **`.ported` page pattern.** Big interactive pages ported 1:1 from the live site
  are wrapped in `<div class="ported ported-<slug>">{% raw %}…{% endraw %}</div>`;
  their CSS is scoped under `.ported` by a brace-walking prefixer so it can't leak
  onto the base nav/footer, and each has `static/css/<slug>.css` + `js/<slug>.js`.
  The migration build scripts live in the session scratchpad
  (`/private/tmp/claude-501/.../scratchpad/`, e.g. `build_choice_builder.py`,
  `migrate_ported_pages.py`) — reusable if you migrate more pages.
- **Design system:** navy `#0E3A8A`/`#071A44` + orange `#FF6B0A` on cream
  `#FBF7EE`; Fraunces (display) / Plus Jakarta Sans (body) / JetBrains Mono
  (labels). Reuse `style.css`, `components.css`, `pages.css`, `admin.css`. New
  pages should `{% extends "base.html" %}` and use these classes (hero, section,
  info-cards, btn-main/btn-out, adm-* for admin).
- **No CSRF protection site-wide** (pre-existing). Session cookie is SameSite=Lax
  by default and state-changing routes are POST-only, which mitigates cross-site
  forgery — but adopting Flask-WTF CSRF is a good future hardening. Reviews should
  not keep re-flagging this per-feature.
- **Jinja autoescape is on**; never render user input with `|safe`. User-supplied
  URLs must be http(s)-allowlisted (see `_safe_http_url` in alumni.py).
- **Security review pattern:** substantive features were reviewed with a Workflow
  (parallel dimensions → adversarial verify) or a single review sub-agent. The
  `Workflow` tool needs explicit opt-in ("ultracode" / "use a workflow") — the
  `Agent` tool does not. Real findings this session: stored-XSS via
  `javascript:` URLs, unauthenticated upload DoS (→ rate limit), referral-code
  fraud (→ validate codes) — all fixed.
- **Always clean up test data** you create in the prod DB (`%@example.com` rows +
  users), and re-verify at the end that only the two real accounts remain.
- **Commit style:** detailed messages; end with
  `Co-Authored-By: Claude <noreply@anthropic.com>`. Push to `main` only when the
  work is verified. Rebase on `origin/main` before pushing (other sessions push
  too).

---

## 7. Open / future items (nothing is broken — these are next steps)

- **Change the weak passwords** on prod: `asfaque2004@gmail.com` (currently `123`)
  and set/rotate the admin password.
- **Payouts are recorded, not settled** — admins log ₹ payouts + mark them paid,
  but money moves offline. A "payouts due" report/export could help.
- **Referral bonus** auto-credits earnings (done) but there's no payment
  integration — still manual settlement.
- **Stream Selection** (`/stream-selection`) is still the old placeholder — the
  psychometric assessment page was intentionally deferred; the user has the file
  to hand over when ready (migrate via the `.ported` pipeline).
- **Uploads at scale:** resumes are now **external links** (no DB bytes); mentor
  **photos** stay in Postgres but capped ~200 KB (fine for low volume; Neon free
  tier is ~0.5 GB). Move photos to object storage (S3/Cloudinary) if it grows.
- **Self-host CDN libs** (D3/Chart.js/Leaflet/jsPDF are from CDNs), and consider
  Flask-WTF CSRF + Flask-Limiter for production-grade hardening.
- **Razorpay / member payments** and membership invoice/receipt PDFs + emails are
  still Phase-B stubs in `membership.py`.

---

## 8. First moves for the new chat

1. `cd /Users/asfaque/Desktop/EDU && git pull && git log --oneline -5` (see §5).
2. Skim `college-predictor/GUIDE.md` §3 (admin guide) and `ARCHITECTURE.md`
   status table.
3. To test a flow: run the app (`.venv/bin/python run.py`), create a throwaway
   `*@example.com` account for the tier you need, exercise it, **delete it after**.
4. Push to `main` to deploy; verify on `https://eduaakashaa.onrender.com`; keep
   README/ARCHITECTURE/GUIDE updated and add public pages to
   `tests/all_pages.json`.
