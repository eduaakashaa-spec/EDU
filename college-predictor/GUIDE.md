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
| Overview | `/admin` | Full dashboard: grouped KPI bands (members, revenue, leads, guides, weekly growth), **4 charts**, and recent-activity feeds |
| Members | `/admin/users` | Every account: **change plan (free/premium/admin), set/clear validity, reset password, add or delete members** |
| Applications | `/admin/membership` | All membership applications (the old Google Sheet, replaced) |
| Leads & Assessments | `/admin/leads` | Every form/assessment submission from anywhere on the site |
| Inquiries | `/admin/inquiries` | Messages from the Contact page form |
| Announcements | `/admin/announcements` | Post notices to member dashboards (pin/hide/delete) |
| Schedule | `/admin/schedule` | Exams & events shown on member dashboards |
| Messages | `/admin/messages` | Template library — per-member WhatsApp / email drafts with placeholders filled |
| Email Templates | `/admin/templates` | Pick a ready email (welcome, thank-you, payment credited…), fill placeholders, open a draft from `eduaakashaa@gmail.com` (see §3.9) |
| Onboarding Assessments | `/admin/onboarding` | See completed member onboarding assessments (student + parent), paired by family, with a one-click **Copy for AI** to generate the Insight Dossier. Families fill it at `/onboarding-assessment` |
| College Guides | `/admin/alumni` | College Guide registrations — profiles, resume link/photo, status & matching, ₹ payouts, referral tree (see §3.5) |
| Surveys | `/admin/surveys` | College Experience Survey responses — grouped by college + "want to be a guide" leads (see §3.8) |

### 3.2b Members — changing a user's plan

Open **Members**, find the account (search or tier filter), click **Manage ▾**:
pick the plan (free / premium / admin / mentor), set a **Valid until** date (or tick
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

### 4.5 Give back — for students & alumni

Two things on the site are for people who've *been* to college, not those
choosing one (both under the **More** nav dropdown):

- **★ Rate Your College** (`/college-survey`) — a free, detailed survey to share
  an honest read of your college (academics, placements, hostel, safety,
  location and more). No login needed; it helps parents choose well.
- **★ Become a College Guide** (`/alumni-network`) — answer parents' questions
  about your college for **₹500–1000**, plus ₹1000 referral bonuses. No lock-in, no spam.

---

## 5. Where the data lives (reference)

| What a visitor does | Stored in (Postgres table) | Admin sees it at |
|---------------------|---------------------------|------------------|
| Applies for membership | `membership_applications` (+ `membership_invoices`) | `/admin/membership` |
| Submits any assessment / report / callback form | `page_leads` | `/admin/leads` |
| Uses the legacy DASA predict API | `dasa_leads` | `/admin/leads` (bottom section) |
| Sends the Contact form | `contact_inquiries` | `/admin/inquiries` |
| Registers an account | `users` | `/admin/users` |
| Registers as a College Guide | `alumni_profiles` (photo in DB, resume as a link) | `/admin/alumni` |
| Fills the College Experience Survey | `college_surveys` (answers in `responses_json`) | `/admin/surveys` |

All admin pages require an **admin-tier login**; non-admins get a 403.

### 3.5 College Guides (peer network)

`/alumni-network` is a **public** recruitment page for **College Guides**: alumni
and current students at top colleges register to answer parents' questions about
their college for pay (the copy advertises *get paid ₹500–1000, plus a ₹1000
referral bonus*). It's linked from the **More** nav dropdown ("★ Become a College
Guide") — share the URL directly with students you want to recruit. (The internal
user tier is still called `mentor` in the code.)

**Registration → mentor account.** The form collects contact + academic details
(the matching keys: university, program, degree, admission route, stage),
languages, availability, a short bio, a **photo** (validated by type + magic
bytes, capped ~200 KB, stored in Postgres so it survives Render redeploys) and a
**resume link** (a shared Google Drive / Dropbox / URL the mentor pastes — set to
"Anyone with the link"; only the URL is stored, keeping multi-MB files out of the
DB), plus a **password**. Submitting creates a login on the new **`mentor` tier**
(one account per email) and logs them straight into their portal. Every
registrant gets a **personal referral link** (`/alumni-network?ref=CODE`);
sign-ups through it are recorded as `referred_by`. **Referral bonuses are
automatic** — the moment a referred mentor completes their first meeting, the
referrer is credited a one-time **₹1000** on their earnings ledger (shown as a
"referral" session line and a "₹1000 ✓" tag beside that referral). Credited
exactly once per referred mentor.

**Guide portal — `/mentor`** (mentor-tier login; the header shows "Guide
Portal"). Guides see: their review status, **earnings** (total / pending / paid,
all in ₹) and calls attended, a table of their logged sessions + payouts, their
**referral link + who joined through it**, a **message thread with the team**,
and an editable profile (contact / languages / availability / bio; academic
fields are locked). Everything a guide sees is scoped to their own account.

**Admins manage it at `/admin/alumni`** (admin tab): search/filter by university
or status, open a profile to see all details, **open the resume link / view the
photo** (admin-only), set status (New → Verified → Active / Rejected), keep
internal notes, and see the referral tree. On each profile you can **log a
session** (a guide answering a parent's questions earns **₹500–1000**; the kind
dropdown keeps meeting/video/referral/bonus/adjustment for internal tracking)
with the ₹ payout and Completed/Scheduled/etc. status, **mark payouts as paid**,
and **reply to the guide's messages** — all of which flow through to that guide's
portal. "Calls attended" counts completed
`meeting`-type sessions; total earnings sum every completed session's payout.

### 3.8 College Experience Survey

`/college-survey` is a **free, public** survey (no payment to anyone) where a
student or alumnus of **any** college gives an honest, first-hand read of it —
the raw material the team uses to advise parents. It's linked from the **More**
nav dropdown; share the URL with anyone who's been to a college worth reviewing.

**It's deliberately detailed** — 10 sections (~96 questions): *about you &
admission, academics, placements & careers, infrastructure, hostel & food,
amenities, campus life & safety, administration & support, location &
surroundings, and a final verdict*. Most are one-tap ratings (Excellent → Poor);
the rest are quick MCQs and a few short/long text boxes. **Name, email, phone,
college and entrance exam/rank are required** (college & branch are typeable
dropdowns); everything else is optional. A checkbox lets them opt in to become a
**College Guide**, and the thank-you page points them there — so the free survey
doubles as a College-Guide recruitment funnel.

**Admins read responses at `/admin/surveys`** (Surveys tab): KPI cards
(responses, colleges covered, "open to mentoring" leads), and the responses are
**grouped by college** (each college is a collapsible section showing its
responses, most-reviewed colleges first). Search by name/college/branch/email,
and a per-response detail page that lays out every
answer grouped by section (colour-coded rating pills, the written notes, and the
respondent's contact details if they opted in to mentoring). The whole question
set lives in `routes/survey.py` (one `SECTIONS` list) — **to add or reorder
questions, edit that list; no database migration is needed** (answers live in a
single `responses_json` column).

### 3.9 Email Templates

`/admin/templates` (the **Email Templates** tab, under the Broadcast group) is a
one-click way to send a polished, on-brand email without writing it from scratch.
Nothing is sent automatically — you pick a template, fill in the blanks, and it
opens a **ready draft from `eduaakashaa@gmail.com`** that you review and send.

**How to use it:**
1. Pick a template card — they're grouped into **Members & Onboarding**,
   **Admissions & Payments**, **College Guides** and **Engagement & Season**.
   Some (like **Welcome** or **Deadline alert**) have variants — e.g. *new user*,
   *premium member who just paid*, *new College Guide*, or *JoSAA / TNEA / other*.
2. In the **To** field, start typing a name or email — it's a **searchable
   dropdown of everyone we know** (members, College Guides, leads, survey and
   contact-form emails). Picking a person fills their email and auto-fills the
   *first name* (and *college*, for guides). You can also just type any address.
3. Fill the remaining placeholders (amount, plan, dates, reference…). The subject
   line and a **logo-branded HTML preview** (exactly what the recipient sees —
   header logo + tagline, orange accent, contact footer) update live as you type.
4. Choose how to send:
   - **Open in Gmail** — opens Gmail's compose window already addressed and
     filled, from the `eduaakashaa@gmail.com` account (make sure you're signed in
     to it). Review and hit send.
   - **Open in mail app** — same, via your device's default mail client (`mailto`).
   - **Copy formatted email** — copies the designed HTML so you can paste it into
     Gmail with formatting intact; **Copy plain text** copies the text version.

**Templates included (19):** Welcome (new user / premium / College Guide) ·
Onboarding-assessment invite (student / parent) · Session confirmed · Session
recap & next steps · Report delivered · Documents (missing / all received) ·
Premium renewal reminder · Application received · Application approved ·
Payment reminder · Payment received (full / partial) · Guide matched ·
Thank-you for a guide session · Guide payout credited · Thank-you for the
survey · Counselling deadline alert (JoSAA / TNEA / other) · Win-back ·
Feedback request · Inquiry response. To add or edit one, edit `EMAIL_TEMPLATES`
in `app/services/email_templates.py`.
