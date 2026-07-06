# EduAakashaa — Setup & Usage Guide

This guide covers three things:

1. **[First-time setup — local development](#1-first-time-setup--local-development)** (run the site on your own computer)
2. **[First-time setup — production](#2-first-time-setup--production-neon--render--github)** (put the site live on the internet)
3. **[How to use the site](#3-admin-guide)** — day-to-day workflows for **admins** and for **clients (students & parents)**

> Companion docs: [README.md](README.md) (project overview, routes, data sources) ·
> [ARCHITECTURE.md](ARCHITECTURE.md) (technical architecture) ·
> [../MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) (the old Google Sheets → Postgres migration)

---

## 1. First-time setup — local development

### 1.1 Prerequisites

| Tool | Version | Used for |
|------|---------|----------|
| Python | 3.12+ | the Flask app |
| Node.js + npm | 18+ | only for the browser test suite (optional) |
| Git | any recent | cloning / pushing |

### 1.2 Clone and install

```bash
git clone https://github.com/eduaakashaa-spec/EDU.git
cd EDU/college-predictor

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 1.3 Create your `.env` file

Create `college-predictor/.env` (never commit this file — it is git-ignored):

```bash
# --- minimum for local development ---
# Any of these work; SQLite needs zero setup:
DATABASE_URL=sqlite:///eduaakashaa-dev.db
# or a local/remote Postgres:
# DATABASE_URL=postgresql://user:pass@localhost:5432/eduaakashaa

SECRET_KEY=change-me-to-any-long-random-string
FLASK_DEBUG=1

# --- optional business settings (defaults shown) ---
# HOME_STATE=Tamil Nadu          # GST place of supply
# GST_RATE=0.18                  # 18%, prices are GST-inclusive
# COMPANY_LEGAL_NAME=...         # printed on invoices/exports
```

> ⚠️ **Never point your local `.env` at the production Neon database while
> developing** — every test form you submit would land in real customer data.
> Use SQLite or a local Postgres for development.

### 1.4 Initialise the database and create your admin account

```bash
python manage.py init_db            # creates all tables
python manage.py seed_sequences     # reference / invoice / receipt counters (needed for memberships)
python manage.py create_admin you@example.com YourPassword "Your Name"
python manage.py seed_demo          # optional — a few sample membership rows to play with
```

### 1.5 Run it

```bash
python run.py
# →  http://127.0.0.1:5000          (public site)
# →  http://127.0.0.1:5000/login    (log in with the admin account you created)
# →  http://127.0.0.1:5000/admin/membership   (admin portal)
```

The app loads all college/cutoff data (CSVs, Excel, JSON in `app/data/files/`)
into memory at startup — no extra data setup is needed.

### 1.6 Run the test suite (optional but recommended)

```bash
# From the repo root (one level above college-predictor), with the app running:
cd ..
npm install                          # first time only
npx playwright install chromium      # first time only
BASE_URL=http://127.0.0.1:5000 npx playwright test tests/smoke.spec.ts --project=chromium
```

This opens all 87 pages in a headless browser and fails if any page
errors, returns a bad status, or renders empty.

---

## 2. First-time setup — production (Neon + Render + GitHub)

The live stack is: **GitHub** (code) → **Render** (runs the Flask app, free tier)
→ **Neon** (managed Postgres, free tier). Total cost: ₹0.

### 2.1 Database — Neon

1. Create an account at <https://neon.tech> and create a project (any region;
   Singapore/AWS ap-southeast pairs well with Render Singapore).
2. Copy the **connection string** — it looks like
   `postgresql://user:pass@ep-xxxx-pooler.region.aws.neon.tech/neondb?sslmode=require`.
   Use the **pooled** connection string.

### 2.2 Hosting — Render

1. Create an account at <https://render.com> and connect your GitHub.
2. **New → Blueprint**, select the `EDU` repository. Render reads
   [`render.yaml`](../render.yaml) and creates the `eduaakashaa` web service
   automatically (root dir `college-predictor`, gunicorn, Singapore region,
   health check on `/`).
3. In the service's **Environment** tab set:
   - `DATABASE_URL` → the Neon connection string from step 2.1
   - (`SECRET_KEY` is auto-generated; `FLASK_DEBUG=0` and `PYTHON_VERSION` come from the blueprint)
4. Deploy. Tables are auto-created on first boot (`db.create_all()`).

### 2.3 One-time production bootstrap

Run these **once from your machine**, pointed at Neon (temporarily override the URL):

```bash
cd college-predictor
DATABASE_URL='postgresql://...neon connection string...' python manage.py seed_sequences
DATABASE_URL='postgresql://...neon connection string...' python manage.py create_admin admin@yourdomain.com StrongPassword "Admin Name"
```

Without `seed_sequences` the membership portal cannot allocate reference /
invoice / receipt numbers; without `create_admin` nobody can log into `/admin`.

### 2.4 Keep-alive (free tier sleeps)

Render's free tier spins the app down after ~15 minutes idle (first visit then
takes ~50 s). The repo's GitHub Action pings `/ping` every 10 minutes to keep
it awake — it works automatically once the repo is on GitHub with Actions enabled.

### 2.5 Deploying updates

`autoDeploy` is on: **every push to `main` deploys automatically.**

```bash
git add -A && git commit -m "your change" && git push origin main
# watch it go live (new code serves within ~2-4 minutes)
```

### 2.6 Custom domain (optional)

In Render → Settings → Custom Domains, add `eduaakashaa.in`, then create the
CNAME record Render shows you at your DNS provider. HTTPS is automatic.

---

## 3. Admin guide

### 3.1 Logging in

1. Go to `/login` and sign in with an **admin-tier** account
   (created via `manage.py create_admin`).
2. Once logged in, an **Admin** link appears in the site header, and you can
   open any of the admin pages directly.

### 3.2 The four admin sections

A shared tab bar links every section. The home of it all is the
**EA Admin Control Panel** at `/admin` (the Admin button in the site nav and
the legacy `/ea-admin-portal` URL both land there) — KPIs for members, leads,
applications and inquiries, plus recent-activity feeds.

| Page | URL | What's in it |
|------|-----|--------------|
| Overview | `/admin` | Control panel: KPIs, newest members, latest leads/applications, live announcements, upcoming schedule |
| Members | `/admin/users` | Every account: **change plan (free/premium/admin), set/clear validity, reset password, add or delete members** |
| Applications | `/admin/membership` | All membership applications (the old Google Sheet, replaced) |
| Leads & Assessments | `/admin/leads` | Every form/assessment submission from anywhere on the site |
| Inquiries | `/admin/inquiries` | Messages from the Contact page form |
| Announcements | `/admin/announcements` | Post notices to member dashboards (pin/hide/delete) |
| Schedule | `/admin/schedule` | Exams & events shown on member dashboards |
| Messages | `/admin/messages` | Template library — per-member WhatsApp / email drafts with placeholders filled |
| Alumni | `/admin/alumni` | Alumni mentor registrations — profiles, resume/photo, status & matching, referral tree (see §3.5) |

### 3.2b Members — changing a user's plan

Open **Members**, find the account (search or tier filter), click **Manage ▾**:
pick the plan (free / premium / admin), set a **Valid until** date (or tick
*no expiry*), and **Save plan**. The change takes effect on the member's next
page load. Guards: you cannot remove your own admin access, and admins must be
demoted before they can be deleted. **Reset password** and **Delete** live in
the same panel; **+ Add member** at the top creates a login directly (e.g.
after an offline payment).

### 3.3 Memberships — full workflow

This is the money workflow. An application moves through:
**New → Approved → Invoiced → Partially Paid → Paid**.

1. **A client applies** on `/members-registration` (tier options: Foundation
   Path, Aspirant Path, NRI / Global, NRI · AI Report, NRI · Expert Guidance,
   Elite Mentorship). They instantly get a reference number like `EA-PREM-0042`.
2. **You see it under `/admin/membership`** — KPI cards on top (Total / New /
   Invoiced / Paid), search by name/email/phone/reference, filter by status or tier.
3. **Click the reference** to open the detail page, where you can:
   - edit any field (name, contact, tier, state — GST recalculates automatically);
   - apply a **discount** with a reason;
   - add **ad-hoc line items** (extra services);
   - **issue an invoice** — allocates a transaction-safe invoice number and
     computes CGST/SGST (Tamil Nadu clients) or IGST (other states), 18% GST-inclusive;
   - **record payments** — full or partial; a receipt number is allocated and
     the status moves to Partially Paid / Paid automatically;
   - keep **internal notes** (never shown to the client).
4. **Export**: the "Export to Excel" button downloads everything (respecting
   your current search/filter) as an `.xlsx` for non-technical staff.

### 3.4 Leads & Assessments — where every form lands

Every tool on the site that captures visitor details posts to the same
intake and appears here, newest first, with a **source** tag telling you which
page it came from:

| Source tag | Page / tool |
|------------|-------------|
| `tnea-expert-guidance` | TNEA Expert Guidance — student gate form (marks + contact) |
| `free-report` | Free TNEA Report — report request with score/category |
| `tnea2026` | TNEA 2026 page — prediction request |
| `branch-fitness` | Branch-Fit Assessment — full results + contact |
| `josaa-assessment` / `student-assessment` | multi-step assessments |
| `stream-selection` | Stream Selection — student + parent details |
| `per-assessment` | PER Assessment submissions |
| `career-path-callback` | Career Path page — "Request a callback" form |
| `about-check-results` | About page — "Check Your Results" (email + JOSAA roll no) |
| `dasa-report-request` | DASA guide — "Email me my report" requests |

Workflow:
- **Search** by name/email/phone, or **filter by source**.
- Click **View →** on any lead to see the **full submitted payload** (every
  answer, score and field the visitor entered) pretty-printed.
- Follow up by phone/WhatsApp/email — contact details are extracted into
  their own columns even when they're buried inside assessment payloads.
- The same page also lists legacy **DASA predictor leads** at the bottom.

> Note: the assessments still *also* write to the old Google Sheets (via Apps
> Script) so any existing sheet-based workflow keeps working. Postgres is now
> the primary store; the sheets can be retired whenever you're ready.

### 3.5 Contact Inquiries

Messages from the Contact page form: name, email, what they're interested in,
and the message. Searchable. Reply by email — there's no in-app reply (yet).

### 3.6 Users

Everyone who registered an account, with their tier
(**free** — 3 DASA results max · **premium** — unlimited · **admin**).
To promote someone, currently use the CLI:
`python manage.py create_admin ...` for admins, or update the row in the DB
for premium (Razorpay self-serve payments are on the roadmap).

### 3.7 Admin FAQ

- **I forgot the admin password** → run `create_admin` again with the same
  email; it updates the password.
- **Invoice numbers look wrong / won't allocate** → run
  `python manage.py seed_sequences` against the production DB (see §2.3).
- **A page's college data needs updating** → edit the matching CSV in
  `app/data/files/` (see README → Data Sources), commit, push. No code
  changes needed; the site picks it up on deploy.

---

## 4. Client guide (students & parents)

What a visitor can do, in the order they usually do it:

### 4.1 Explore free tools (no account needed)

- **TNEA** (Tamil Nadu): cutoff **simulator** (`/tnea-simulator`), college maps
  (`/tnea-colleges`), the **Expert Guidance** hub (`/tnea-expert-guidance`) with a
  35-college benchmark table and a cutoff predictor, and a **Free TNEA Report**
  (`/free-report`).
- **JEE / JOSAA**: the JOSAA **predictor** (`/josaa`) — enter your rank,
  category and preferences to see realistic college options, plus analytics
  and NIRF rankings.
- **DASA / NRI** (students abroad): the DASA **predictor and guide**
  (`/dasa-admissions-guide`), seat matrix, closing ranks, and CIWG guidance.
- **Assessments**: stream selection (Class 10/12), branch-fitness, career
  path, student/JOSAA/PER assessments — answer the questions, get scored
  results immediately on screen.

### 4.2 What happens when you submit a form

Wherever you leave your details — an assessment, "Request a callback",
"Email me my report", the contact form — the EduAakashaa team receives it
instantly, and **a mentor follows up personally** (usually by WhatsApp or
phone). The floating **"Chat with a mentor"** WhatsApp button on every page is
the fastest way to reach the team directly.

### 4.3 Membership (paid mentorship)

1. Open **★ Membership** in the header (`/members-registration`).
2. Compare the six tiers (Foundation Path → Elite Mentorship) and submit the
   application form — **no payment is taken up front**.
3. You immediately get a **reference number** (e.g. `EA-PREM-0042`) — keep it.
4. A mentor reviews the application (target: within 2 working days), contacts
   you, and on approval you receive a **GST invoice**; payment confirms your seat.

### 4.4 Accounts (optional)

You can browse everything without an account. Registering (`/register`) gives
you a dashboard and — on the free tier — up to 3 DASA prediction results;
premium members get unlimited results and member-only reports.

Premium-only tool pages live under the **Premium Membership** nav dropdown
(marked with a 🔒 in the menu) and are gated with `@premium_required` —
anonymous visitors are asked to log in, and logged-in free-tier users see
`premium_locked.html`. The premium catalogue (all full ports of the legacy
live-site content, no placeholders):

| Page | Route | What it is |
|------|-------|------------|
| Why CSE? | `/why-cse` | CSE vs core branches — service/product salary data, AI-impact analysis, career roadmap |
| Best Location | `/best-location` | City-by-city study-destination analyzer (D3 + Chart.js) |
| Engineering Insights | `/engineering-insights` | Branch guide with scoring assessment + PDF report (jsPDF); submissions land in `/admin/leads` |
| Hostel & Culture Analytics | `/hostel-and-culture-analytics` | DASA hostel/campus-culture report with D3 visuals |
| TNEA Expert | `/tnea-expert` | Full TNEA 2026 guide — college table, cutoff predictor, Leaflet map, Student/Expert modes; expert-review requests land in `/admin/leads` |
| JOSAA EA Members | `/josaaea-members` | JOSAA 2025 college predictor with choice wizard + XLSX/PDF export; submissions land in `/admin/leads` |
| Expert Portal — DASA | `/expert-portaldasa` | DASA choice-filling matrix ("Beyond NIRF") |
| Engineering Branch Selection Guide | `/engineering-branch-selection-guide` | Interactive 12-branch comparison dashboard with fitness quiz + roadmap generator |
| DASA Prediction Report | `/dasa-prediction-report` | Member-edition prediction report (landing page) |
| Stream Selection / Members Report | `/stream-selection`, `/members-report` | Member pages (stream-selection psychometric port pending) |

`/dasa2026-schedule` (counselling calendar with a downloadable `.ics` of every
DASA 2026 deadline) is public. The **EA Team / Counsellor Portal** dropdown is
admin-only: `/counsellor-dashboard` (in-app triage of DASA 2026 Choice Builder
submissions, read live from the team Google Sheet), `/choice-builder-pro`
(in-app allotment analyzer), `/ea-admin-portal` (→ the `/admin` control panel) and
`/dasa2026-expert-report`.

---

## 5. Where the data lives (reference)

| What a visitor does | Stored in (Postgres table) | Admin sees it at |
|---------------------|---------------------------|------------------|
| Applies for membership | `membership_applications` (+ `membership_invoices`) | `/admin/membership` |
| Submits any assessment / report / callback form | `page_leads` | `/admin/leads` |
| Uses the legacy DASA predict API | `dasa_leads` | `/admin/leads` (bottom section) |
| Sends the Contact form | `contact_inquiries` | `/admin/inquiries` |
| Registers an account | `users` | `/admin/users` |
| Joins the alumni mentor network | `alumni_profiles` (incl. resume + photo) | `/admin/alumni` |

All admin pages require an **admin-tier login**; non-admins get a 403.

### 3.5 Alumni / Mentor Network

`/alumni-network` is a **public** recruitment page: alumni and current students
at top universities register to mentor parents in short paid sessions (the copy
advertises *up to $100 per meeting* and an *AED 100 referral bonus*). It's linked
from the **More** nav dropdown — share the URL directly with students you want to
recruit.

- The form collects contact + academic details (the matching keys: university,
  program, degree, admission route, stage), languages, availability, a short bio,
  and a **photo + resume** (validated by type and size — photo ≤3 MB, resume ≤5 MB —
  and stored in Postgres so they survive Render redeploys).
- Every registrant gets a **personal referral link** (`/alumni-network?ref=CODE`);
  anyone who signs up through it is recorded as `referred_by`, so you can track and
  pay referral bonuses.
- **Admins** manage everything at `/admin/alumni`: search/filter by university or
  status, open a profile to see all details, **download the resume / view the
  photo** (admin-only), set status (New → Verified → Active / Rejected), keep
  internal notes, and see the person's referral tree. Resume/photo files are served
  only to logged-in admins.
