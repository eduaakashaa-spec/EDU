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
                            #   Announcement, ScheduleEvent, AlumniProfile, MentorMeeting, MentorMessage
    models_membership.py     # MembershipApplication, MembershipInvoice, DocSequence
    routes/
      __init__.py (main_bp) # all public content pages + premium pages (render_reference_page/_premium)
      api.py                # JSON endpoints incl. POST /api/leads (generic lead capture)
      auth.py               # login/register/logout/dashboard/contact
      membership.py         # /admin/membership + /admin/leads + /admin/inquiries + /admin/users (admin_required)
      admin_portal.py       # /admin control panel (overview, users, announcements, schedule, messages)
      alumni.py             # Alumni/Mentor network: public /alumni-network, /mentor portal, /admin/alumni
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

- **Alumni / Mentor Network** (`routes/alumni.py`, `templates/alumni_network.html`,
  `templates/mentor/dashboard.html`, `templates/admin/alumni_*.html`):
  - Public `/alumni-network` (linked from the **More** nav dropdown): recruits
    alumni/students at top unis to mentor parents in paid sessions. Copy is in
    **AED** ("up to AED 100 per meeting", "AED 100 per referral"). Collects
    academic details + **photo + resume** (validated by extension **and magic
    bytes**, size-capped 3MB/5MB, stored as `LargeBinary` in Postgres because
    Render's disk is ephemeral) + a **password**.
  - Registration **creates a `mentor`-tier login** (one per email, race-safe) and
    auto-logs them in. Per-registrant **referral link** `?ref=CODE` recorded as
    `referred_by` (validated against real codes; `javascript:`/non-http URLs
    stripped; per-IP rate limit 10/hr + 10-min email dedup on the endpoint).
  - **Mentor portal `/mentor`** (`mentor_required`): AED earnings (total/pending/
    paid) + calls attended, sessions table, referral link + who joined, two-way
    **messages with admins**, editable profile. Header shows "Mentor Portal";
    `/dashboard` redirects mentors here.
  - **Admin `/admin/alumni`** (admin tab): list/search, profile detail, admin-only
    resume download + photo view (`send_file`, attachment + `nosniff`), status
    workflow, **log sessions/bonuses with AED payout + mark paid**, reply to
    messages, referral tree.
  - **Auto referral bonus:** when a referred mentor completes their **first**
    meeting, the referrer is credited a one-time **AED 100** (a `kind='referral'`
    `MentorMeeting`, idempotent via `MentorMeeting.referred_alumni_id`; counts
    toward earnings, not "calls attended"). Logic: `_maybe_credit_referral()` in
    `alumni.py`, called after `admin_add_meeting`.
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
accounts→`/admin/users`, mentors→`/admin/alumni`.

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
- **Payouts are recorded, not settled** — admins log AED payouts + mark them paid,
  but money moves offline. A "payouts due" report/export could help.
- **Referral bonus** auto-credits earnings (done) but there's no payment
  integration — still manual settlement.
- **Stream Selection** (`/stream-selection`) is still the old placeholder — the
  psychometric assessment page was intentionally deferred; the user has the file
  to hand over when ready (migrate via the `.ported` pipeline).
- **Uploads at scale:** resumes/photos are in Postgres (fine for low volume; Neon
  free tier is ~0.5 GB). Move to object storage (S3/Cloudinary) if it grows.
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
