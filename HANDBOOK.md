# EduAakashaa — The Team Handbook

**Who this is for:** someone who has been handed this project and does not write code.
No programming knowledge is assumed. If you can use Gmail and a web browser, you can
follow this document.

**What this is:** the complete operating manual for the EduAakashaa website — what it is,
what it's made of, who owns which account, how to change it, how to run it, and what to do
when it breaks.

**How to read it:** don't read it top to bottom. Read **Part 1** (10 minutes) so the rest
makes sense, then jump to whatever you need. Use the contents below.

> **The single most important sentence in this document:** you are not expected to write
> code. You are expected to describe what you want to an AI assistant called Claude Code,
> check that it worked, and know which buttons are dangerous. **Part 3** teaches you that.

---

## Contents

| Part | What's in it | Read it when |
|---|---|---|
| [Part 1 — What this thing is](#part-1--what-this-thing-is) | The project in plain English, and how a website actually works | First. Always. |
| [Part 2 — The account map](#part-2--the-account-map) | Every service, who owns it, what it costs, what breaks | Before you touch anything |
| [Part 3 — Claude Code](#part-3--claude-code-your-main-tool) | Your main tool, and how to talk to it | Before your first change |
| [Part 4 — Setting up your computer](#part-4--setting-up-your-computer-from-zero) | From a brand-new laptop to a working setup | Day one |
| [Part 5 — The tech stack](#part-5--the-tech-stack-in-plain-english) | What each piece of software does | When curious |
| [Part 6 — Making a change](#part-6--making-a-change-and-getting-it-live) | How an edit reaches the live website | Every time you change something |
| [Part 7 — Running the site day to day](#part-7--running-the-site-day-to-day) | The admin area, every page explained | Daily |
| [Part 8 — Updating college data](#part-8--updating-college-data) | Cutoffs, colleges, rankings | Each admission season |
| [Part 9 — Email](#part-9--email-how-it-works-and-why-its-fragile) | How email works and why it's fragile | When email misbehaves |
| [Part 10 — The danger zone](#part-10--the-danger-zone) | Irreversible actions and known traps | **Before clicking anything in admin** |
| [Part 11 — When it breaks](#part-11--when-something-breaks) | Troubleshooting playbook | In a panic |
| [Part 12 — Known problems](#part-12--known-problems-that-need-fixing) | Real issues someone must fix | This week |
| [Part 13 — Glossary](#part-13--glossary) | Every piece of jargon, defined | Whenever a word confuses you |

---

# Part 1 — What this thing is

## 1.1 The business, in one paragraph

EduAakashaa helps Indian students and their parents choose an engineering college. Students
arrive from Google or WhatsApp, use free tools (predict which college a rank can get, browse
colleges, take an assessment), and leave their contact details. Those become **leads**. Some
leads buy a paid mentorship **membership**. Paid members get extra pages, one-on-one
counselling sessions, and document verification. Money is collected **manually** (bank
transfer / UPI), and an invoice is raised by hand in the admin area.

## 1.2 What "the website" is actually made of

Most non-technical people picture a website as one thing. It's four:

| Piece | What it is | Where it lives |
|---|---|---|
| **The code** | The instructions that build every page | GitHub (an online folder with history) |
| **The server** | A computer that runs the code and answers visitors | Render (rented, currently free) |
| **The database** | A permanent notebook: members, leads, invoices | Neon (rented, currently free) |
| **The file storage** | Uploaded PDFs and documents | Cloudflare R2 (rented) |

They are four **separate rented services**, each with its own login. They only work together
because someone configured them to. This is the single most important idea in this handbook:
**there is no "the website" you can point at.** There are four services and a chain that
connects them.

## 1.3 How a visitor actually gets a page

When someone types your web address:

1. Their browser asks **Render's** computer for the page.
2. Render runs the **code** (which came from GitHub).
3. The code asks the **database** (Neon) for anything it needs — "is this person logged in?"
4. The code fills in an HTML template and sends the finished page back.
5. The browser draws it.

All four must be alive. If Neon is down, pages that need the database break, but pages that
don't will still work — which is why "the site is half-broken" is a normal, meaningful thing
to observe.

## 1.4 The three addresses, and why there are three

This confuses everyone. There are three different addresses and they do different jobs:

| Address | What it is | Used for |
|---|---|---|
| `eduaakashaa.onrender.com` | Where the app **actually runs** | The real, live site. Every link in every automated email points here. |
| `eduaakashaa.in` | The **brand** address | Printed on PDFs and reports. This is the **old Hostinger site**, being migrated away from. |
| `eduaakashaa.com` | The **email** address | Verified with Resend so automated email can be sent. Nothing is hosted here. |

Plain English: **`.in` is what people read, `.com` is what sends mail, `.onrender.com` is what
actually works.**

## 1.5 Where the code lives on your computer

```
EDU/                          ← the repository ("repo") — the whole project
├── HANDBOOK.md               ← this file
├── HANDOFF.md                ← a technical briefing written for AI assistants, not humans
├── render.yaml               ← tells Render how to run the site
├── tests/                    ← automated browser checks
└── college-predictor/        ← THE ACTUAL WEBSITE. Almost everything is in here.
    ├── run.py                ← the "on switch"
    ├── manage.py             ← one-off admin commands (create an admin, etc.)
    ├── requirements.txt      ← the list of software the site needs
    ├── config.py             ← settings
    ├── .env                  ← YOUR SECRETS. Never share. Never commit. (see 2.6)
    ├── GUIDE.md              ← older setup + admin guide (still useful)
    ├── README.md             ← project overview + development history
    ├── tests/                ← automated checks
    └── app/
        ├── __init__.py       ← starts everything up
        ├── models.py         ← the shape of the database
        ├── routes/           ← one file per section of the site (the "pages")
        ├── templates/        ← the HTML — what pages look like
        ├── static/           ← images, styling, browser code. ⚠️ PUBLIC TO EVERYONE.
        ├── services/         ← email, file storage, invoice maths
        └── data/files/       ← the college spreadsheets (CSV/Excel/JSON)
```

**Remember `app/static/`.** Everything in it is downloadable by any visitor. It is not
protected by a login, ever. A password put in there is a public password. This has already
caused one real problem on this project (see Part 12).

---

# Part 2 — The account map

This is the section you were most worried about, and rightly so.

## 2.1 The chain, in one picture

```
              eduaakashaa@gmail.com   ← the master key. Everything hangs off this.
                        │
   ┌──────────┬─────────┼──────────┬────────────┬─────────────┐
   │          │         │          │            │             │
 GitHub     Render    Neon    Cloudflare     Resend     Microsoft 365
 (code)    (server)  (database)   R2         (email)      (DNS for
                                (files)                 eduaakashaa.com)
                                                              │
                                                     Resend can only send
                                                    because DNS records
                                                    here say it may.
```

Read that top down. **If the Gmail account is lost, the recovery path to every one of those
services is lost with it.** Not the services themselves — they'd keep running — but your
ability to log in, fix, pay, or rescue them.

## 2.2 The services, one by one

| Service | What it does for you | Plan | If you lose access |
|---|---|---|---|
| **Gmail** (`eduaakashaa@gmail.com`) | The master account. Password resets for everything else land here. Also the admin login for the site. Also the team inbox for alerts. | Free | Catastrophic — it's the recovery path for all of the below |
| **GitHub** (`eduaakashaa-spec/EDU`) | Stores the code and its full history. Pushing here triggers a deploy. Also runs the keep-alive alarm clock. | Free, **PUBLIC** | Can't deploy changes. Site keeps running. |
| **Render** | Runs the website. Rebuilds and redeploys automatically when code reaches GitHub's `main`. | **Free**, Singapore | **Site goes down.** |
| **Neon** | The PostgreSQL database. Every member, lead, invoice, application. | Free | **Total data loss. There is no backup.** See 2.5. |
| **Cloudflare R2** | Private storage for uploaded resumes and verification documents. Bucket: `eduaakashaa`. | Paid-as-you-go (pennies) | Uploaded documents become unreachable. |
| **Resend** | Sends all automated email over the web. | Free tier | **All automated email silently stops.** Nothing errors. |
| **Microsoft 365** | Hosts the DNS records for `eduaakashaa.com`. Resend's proof-of-ownership records live here. | Paid | Resend fails verification → email stops. |
| **Google Apps Script + Sheets** | Six old webhooks that copy assessment answers into Google Sheets. | Free | **Nothing breaks** — see 2.4. |

**Not used, despite what you may assume:** there is **no payment gateway** (no Razorpay, no
Stripe — money moves offline and invoices are typed by hand), and there is **no analytics of
any kind** (no Google Analytics, no Meta pixel). Nobody is tracking your visitors. If you
want visitor numbers, that has to be added.

## 2.3 What `eduaakashaa@gmail.com` is actually wired into, in the code

Not folklore — these are the real places the address appears:

- **The site's admin login.** It is an `admin` tier account in the database.
- **The team alert inbox.** Whenever someone registers as a College Guide, submits a survey,
  or uploads documents, the heads-up email goes here. (Set by `ADMIN_NOTIFY_EMAIL` and
  `DOC_NOTIFY_EMAIL`; this address is the built-in default if they're not set.)
- **The Gmail compose button in the admin area.** The email-templates page opens Gmail with
  this account pre-selected. **It only works if you're signed into that exact Gmail account
  in the same browser.** If a teammate uses it while signed into their own Gmail, it opens
  the wrong account.
- **Almost certainly the owner of the Google Apps Script webhooks** — but nobody wrote that
  down anywhere, so it is an assumption. **Verify it and record it below.**

### ✍️ Fill this in — the repo cannot tell you these

The code proves what's connected. It cannot prove **who owns the login**. Somebody with the
passwords must complete this table and keep it in a password manager (**not** in this file,
which is public):

| Service | Login email | 2-factor on? | Who has access | Recovery codes stored where |
|---|---|---|---|---|
| Gmail | eduaakashaa@gmail.com | ? | ? | ? |
| GitHub | ? | ? | ? | ? |
| Render | ? | ? | ? | ? |
| Neon | ? | ? | ? | ? |
| Cloudflare | ? | ? | ? | ? |
| Resend | ? | ? | ? | ? |
| Microsoft 365 | ? | ? | ? | ? |
| Google Apps Script | ? | ? | ? | ? |

## 2.4 The Google Sheets webhooks (safe to ignore, safe to delete)

Seven assessment pages still quietly copy their answers into Google Sheets, left over from
the old Hostinger site. **Every one of those pages also saves the same answer to the real
database**, which you read at `/admin/leads`. So the Sheets are a duplicate.

Two things to know:

1. **You can ignore them.** Nothing breaks if the Sheets stop working. Your data is in Neon.
2. **They are open to the public internet.** The webhook addresses sit in public browser code,
   with no password. Anyone who reads your page source can post junk into those Sheets. They
   can't reach your database or your members — the damage is limited to the Sheets.

The team already deleted a page for this exact reason once (`/counsellor-dashboard`, July
2026). These six were never revisited. **Recommendation: delete the Apps Script deployments
once you've confirmed nobody reads those Sheets.**

## 2.5 The backup situation — read this twice

> **There is no backup of the database.**

Every member, every lead, every invoice, every assessment lives in one free-tier Neon
database and nowhere else. If it is deleted, misconfigured, or the free plan lapses, it is
gone. There is no export running anywhere. Nothing in this repo backs it up.

There is a partial escape hatch: **Admin → People → Membership → Export to Excel** downloads
the membership applications. That is one table, not the database.

**This is the biggest single risk in the project.** Ask Claude Code to set up a scheduled
backup, or at minimum download that Excel export on a schedule.

## 2.6 Secrets: what they are and the one rule

A **secret** is a password-like string that proves the site is allowed to use a service —
the database address, the email API key, the file-storage keys.

They live in a file called `.env` inside `college-predictor/`, and in Render's dashboard
under **Environment**. Two copies of the same list: one for your laptop, one for the live
site.

**The one rule: `.env` never leaves your computer.** It is deliberately excluded from GitHub
(that's what `.gitignore` does). Never paste its contents into a chat, an email, a support
ticket, or this handbook. If you think a secret leaked, **rotate it** — go to that service,
generate a new key, and update it in both places. A leaked key that's been replaced is
harmless. A leaked key that's still live is somebody else's key.

Here is what the app looks for, and what happens if it's missing:

| Setting | What it's for | If missing |
|---|---|---|
| `SECRET_KEY` | Signs the login cookie so people can't forge an admin session | **The site refuses to start.** Deliberate. |
| `DATABASE_URL` | Where the database is | ⚠️ **Site starts anyway** and quietly uses a temporary file that Render wipes on every deploy → **silent data loss**. The one dangerous default. |
| `RESEND_API_KEY` | Lets the site send email | Email silently stops. No error. |
| `MAIL_FROM` | The "from" address on automated mail | Defaults to `noreply@eduaakashaa.com`. Must match the domain verified in Resend or Resend rejects it. |
| `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET` | File uploads | Uploads fail with a clear message. |
| `FLASK_DEBUG` | Developer mode | ⚠️ Must be `0` in production. `1` on a live site lets strangers run commands on your server. |

⚠️ **Known gap:** Render's config file (`render.yaml`) only declares four settings. The
**email and file-storage keys are not in it** — they were added by hand in the dashboard. If
anyone ever rebuilds the Render service from that file, email and uploads will silently stop
working with no error anywhere. Write them down (in your password manager) before that
happens.

---

# Part 3 — Claude Code, your main tool

## 3.1 What it is

Claude Code is an AI assistant that runs on your computer, reads this project, and makes
changes for you. **You describe the outcome you want in plain English. It writes the code.**

That is genuinely how this project is maintained. You do not need to learn Python.

## 3.2 What it can and can't do

**It can:** read every file, explain anything, make changes, run the site, test it in a
browser, take screenshots, run the automated checks, commit and push (deploying your change),
and tell you what it did.

**It can't:** log into Gmail/Render/Neon as you, know a password you never told it, see your
screen unless you say so, or know something that isn't written down somewhere. It also
**cannot undo a deploy that already went out** — only push another change on top.

**It will sometimes be wrong.** It is very good and not infallible. This is why every rule
below exists.

## 3.3 How to talk to it

The difference between a useless answer and a great one is almost entirely the prompt.

### The formula

> **What you want** + **where** + **why** + **how you'll know it worked**

### Bad vs good

| ❌ Don't say | ✅ Say instead |
|---|---|
| "fix the form" | "On the onboarding assessment, the phone field accepts letters. It should only accept digits and a leading +. Show me it working." |
| "make it look better" | "The Contact page buttons are much bigger than the ones on the Membership page. Make them match Membership. Show me a before/after screenshot." |
| "add analytics" | "We have no analytics. What are my options, what does each cost, and what's the privacy impact? Don't write any code yet — just recommend one." |
| "the site is broken" | "Since about 3pm today `/josaa` shows a 500 error. Nothing was deployed. Find the cause, tell me what it is, and don't change anything until I say so." |
| "update the colleges" | "Add these 5 colleges to the TNEA list. Here's the data: [paste]. Update the right CSV and confirm they show on /tnea-colleges." |

### Five habits that will save you

1. **Ask before you order.** Start with *"explain how X works"* or *"what would it take to
   do Y?"* before *"do Y"*. Understanding costs you 30 seconds and saves you a bad deploy.
2. **Ask for proof, always.** End with **"show me it working"** or **"run the tests"**. It
   can open a browser and screenshot the result. If it says "done" with no evidence, ask for
   evidence.
3. **One thing at a time.** Five requests in one message gets you five half-changes. Ship
   one, check it, then the next.
4. **Say when you don't understand.** *"Explain that like I've never coded"* is a completely
   normal thing to type, as often as you need.
5. **Make it say what it's unsure about.** *"What could this break?"* and *"what did you
   assume?"* surface the risks it wouldn't otherwise mention.

### The safety rules

- 🚫 **Never paste a password, API key, or the contents of `.env` into the chat.** It doesn't
  need them. It reads the file itself when it must.
- 🛑 **Anything involving money, deleting data, or emailing members — ask it to explain the
  plan first, and approve it yourself.** Never let it send a bulk email without you reading
  the exact text.
- ✅ **Ask "is this tested?" before "push it".**
- ⚠️ **Watch for the database warning.** Your laptop's `.env` currently points at the **live
  production database**. Testing a form on your laptop can write real rows into real data.
  Whenever you're testing something that saves data, say: *"use a local test database, not
  production."*

### Copy-paste prompts for common jobs

```
Explain what this project is and how it's put together. I'm not technical.

Run the site on my computer and give me the address to open.

I want to change [X] on the [Y] page. Explain what you'd change before doing it.

Add these colleges to the TNEA data: [paste rows]. Update the CSV, show me it on the page.

Something is broken on [page]. Find out why. Don't change anything yet.

Run all the tests and tell me in plain English if anything is failing.

I've checked it and I'm happy. Commit this and push it live.

Is our email working right now? Check and tell me how you know.

Set up an automatic backup of the database. Explain the options and cost first.
```

## 3.4 What "push it live" actually does

When you say **"push it"**, this happens with no further confirmation:

1. Your change is saved to the project history (a **commit**).
2. It's uploaded to GitHub (a **push**).
3. **Render notices within seconds and starts deploying.**
4. About 2–5 minutes later, **the public website has changed.**

There is no staging site. There is no review step. **Pushing is publishing.** Only say "push
it" when you've seen it working.

---

# Part 4 — Setting up your computer from zero

You only do this once. Budget an hour. If a step fails, paste the exact error into Claude
Code and ask what it means.

**Step 1 — Install the tools.**
You need three: **Git** (the history tool), **Python 3.12** (the language the site is
written in), and **Claude Code**. On a Mac, opening the Terminal app and typing `git` will
offer to install Git for you. Ask Claude Code (via its website/desktop app) for the current
install steps for your operating system — they change, and it will know.

**Step 2 — Get an invite.** Someone with access must add your GitHub account to the
`eduaakashaa-spec` organisation.

**Step 3 — Download the project.** In a terminal:

```bash
git clone https://github.com/eduaakashaa-spec/EDU.git
cd EDU/college-predictor
```

**Step 4 — Build the project's private toolbox.**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The first line makes a **virtual environment** — a private box holding exactly the software
versions this project needs, so it can't clash with anything else on your laptop. The second
fills it.

**Step 5 — Create your `.env` file.** Ask whoever holds the secrets. It goes at
`college-predictor/.env`. There is **no example file in the repo** — this is a known gap.
Ask Claude Code: *"list every environment variable this app reads and what each is for"* and
it will produce the list from the code.

> ⚠️ **The `.env` you'll be handed points at the live production database.** Ask for a
> separate test database before you experiment with forms.

**Step 6 — Start it.**

```bash
.venv/bin/python run.py
```

Open `http://127.0.0.1:5000`. That's the whole site, running on your laptop, invisible to
everyone else. Press `Ctrl+C` to stop it.

> **If it refuses to start** with a message about `SECRET_KEY` — that's correct behaviour, not
> a bug. Your `.env` is missing or in the wrong place.

**Step 7 — Give yourself an admin login** (only on a fresh/test database):

```bash
.venv/bin/python manage.py create_admin you@example.com yourpassword "Your Name"
.venv/bin/python manage.py seed_sequences
```

The second line sets up invoice numbering. Skip it and the invoice page can't issue numbers.

**Step 8 — Prove it all works.**

```bash
.venv/bin/python tests/test_onboarding_assessment.py
```

Or just ask Claude Code: *"run all the tests and tell me if anything's broken."*

---

# Part 5 — The tech stack in plain English

Everything the site depends on. It's a deliberately short list — that's a good thing.

| Thing | What it honestly does |
|---|---|
| **Python 3.12** | The language the site is written in. |
| **Flask** | The framework that turns web addresses into pages. The skeleton. |
| **Gunicorn** | The engine that runs the site in production. `run.py` is for your laptop only. |
| **SQLAlchemy** | Lets the code talk to the database in Python instead of raw database language. |
| **Flask-Login** | Remembers who is logged in. |
| **Flask-Bcrypt** | Scrambles passwords so even you can't read them. This is why a forgotten password must be **reset**, never "looked up". |
| **psycopg2** | The cable between Python and PostgreSQL. |
| **pandas** + **openpyxl** | Read and filter the college spreadsheets. |
| **boto3** | Uploads files to Cloudflare R2. |
| **python-dotenv** | Reads your `.env`. |

**That's the entire list — 10 items.** Email uses no library at all; it's built from Python's
own toolkit. Fewer dependencies means fewer things that break unattended.

**Two structural facts worth knowing:**

- **The college data is loaded once when the site starts** and held in memory. Editing a CSV
  therefore does nothing until the site restarts (which a deploy does automatically).
- **There is no database migration system.** The site creates *missing tables* on startup but
  will **never change an existing one**. Adding a column to a live table is a manual job.
  Tell Claude Code *"we have no migrations"* before asking for any database change.

---

# Part 6 — Making a change and getting it live

## 6.1 The pipeline

```
  You edit          Save to history      Upload            Render sees it
  a file      →      (a "commit")   →   ("push")     →     and rebuilds
                                                                 │
                                                    2–5 min later, live.
```

In practice you say *"commit and push this"* and Claude Code does all of it.

## 6.2 The words

| Word | Plain English |
|---|---|
| **repository / repo** | The project folder, with its complete history |
| **commit** | A save point with a note explaining why |
| **push** | Upload your save points to GitHub → **triggers the live deploy** |
| **pull** | Download other people's changes |
| **branch** | A parallel copy for work in progress |
| **`main`** | The branch that **is** the live site |
| **deploy** | Render rebuilding and publishing the site |

## 6.3 The rule that matters

**`main` is live.** There is no test site between you and the public. Pushing to `main`
changes the real website within minutes.

## 6.4 A safe change, start to finish

1. *"Explain how the contact form works."* — understand it
2. *"Change X to Y."* — make it
3. *"Show me it working."* — verify it
4. *"Run the tests."* — check nothing else broke
5. *"Commit and push."* — publish it
6. Open the live site 5 minutes later — confirm it

## 6.5 Undoing

Nothing is ever truly lost — Git remembers everything. Say:

> *"The last change broke the site. Undo it and push the fix."*

The site is fixed a few minutes later. **Note:** this undoes *code*. It does **not** undo
deleted database rows and it does **not** recall a sent email.

---

# Part 7 — Running the site day to day

Log in at `/login` with an admin account, then go to `/admin`.

## 7.1 The admin menu

**Overview** — `/admin` — counters and recent activity. Look-only, safe.

**People ▾**

| Page | What you do there |
|---|---|
| `/admin/users` | Everyone with a login. Change someone's plan, reset a password, delete them. ⚠️ **See Part 10 before using "Manage".** |
| `/admin/documents` | Ask a member for documents; approve or reject what they upload. |
| `/admin/membership` | Paid mentorship applications: New → Approved → Invoiced → Partially Paid → Paid. The money workflow. |
| `/admin/onboarding` | The student/parent questionnaires, paired up by family. |

**Inbox ▾**

| Page | What you do there |
|---|---|
| `/admin/leads` | **Every form anyone filled in anywhere**, newest first, tagged by page. Your pipeline. |
| `/admin/inquiries` | Contact-page messages. Read-only — you reply from your own email. |

**Broadcast ▾**

| Page | What you do there |
|---|---|
| `/admin/announcements` | Post a notice to member dashboards. ⚠️ Can **email every member at once**. |
| `/admin/schedule` | Exam and counselling dates shown to members. |
| `/admin/messages` | Copy a ready-written WhatsApp/email message. Sends nothing. Safe. |
| `/admin/templates` | Polished email templates. ⚠️ Has a **"Send now"** button that really sends. |
| `/admin/email-test` | **Send yourself a test email.** The first thing to try when email seems broken — it shows the real error. Labelled **"Email Test (SMTP)"** in the menu, which is misleading: it tests whichever transport is live, and in production that's Resend, not SMTP. |

**Network ▾**

| Page | What you do there |
|---|---|
| `/admin/alumni` | College Guide registrations: approve, log sessions, record payouts. |
| `/admin/surveys` | College Experience Survey answers, grouped by college. |

**Finance ▾**

| Page | What you do there |
|---|---|
| `/admin/invoices` | Every GST invoice raised. |
| `/admin/invoices/new` | Raise one by hand. |
| `/admin/invoice-settings` | **Your company details as printed on invoices** — GSTIN, bank details, address. Edit them here, not in code. |

## 7.2 The four kinds of account

| Tier | Can see |
|---|---|
| **free** | All public pages. Predictions capped at 3 results. |
| **premium** | Everything, uncapped, plus ~11 members-only pages. **Can expire** on a date. |
| **admin** | All of the above plus the entire admin area. |
| **mentor** | **Only** the College Guide portal at `/mentor`. Not premium. |

## 7.3 Where leads come from

Every form and assessment on the site posts to one place and lands in `/admin/leads`, tagged
with the page it came from. Contact-form messages are the exception — they go to
`/admin/inquiries`.

---

# Part 8 — Updating college data

The colleges, cutoffs and rankings are **spreadsheets in the project**, not database rows.
They live in `college-predictor/app/data/files/`.

## 8.1 The easy ones (plain CSV — open in Excel)

| File | Feeds |
|---|---|
| `engg_colleges_india.csv` | `/enggcolleges-india` |
| `tnea_top_colleges.csv` | the `/tnea-colleges` map |
| `tnea_benchmark_colleges.csv`, `tnea_all_colleges.csv`, `tnea_branches.csv`, `tnea_cutoff_records.csv` | `/tnea-expert-guidance` |
| `dasa_seat_matrix.csv` | `/dasa-seat-matrix` |
| `nirf_rankings.csv` | NIRF rankings |

To update: edit the CSV, then ask Claude Code to push it. **No code changes needed.** The
site picks it up on the next deploy.

**One quirk:** a `|` (pipe) inside a cell means "this is a list" — e.g. several branches in
one cell. Keep that pattern.

## 8.2 The harder ones

`josaa_cutoffs.xlsx` (Excel) and several `.json` files aren't as friendly. Ask Claude Code to
handle those.

## 8.3 Why this is safe

The data is **read-only while the site runs**. There's no admin button that can corrupt it,
and a broken CSV fails loudly at startup rather than quietly serving wrong answers. This is
the safest thing in the project to change.

---

# Part 9 — Email: how it works, and why it's fragile

## 9.1 The story

Email should be simple. It isn't, for one specific reason worth understanding:

> **Render's free plan blocks the normal way of sending email (SMTP), entirely.**

Identical code and credentials that send fine from a laptop fail on Render with a network
error. So this site sends through **Resend**, over the ordinary web instead. That's why
there's an extra service in your account list.

## 9.2 The chain

```
Site → Resend → checks eduaakashaa.com is really yours
                    ↓
        by reading DNS records in Microsoft 365
                    ↓
              → delivers the email
```

**Every link must hold.** If the DNS records in Microsoft 365 are changed or removed, Resend
stops trusting the domain and **all email stops**. If `MAIL_FROM` is changed to an address at
a domain Resend hasn't verified, Resend rejects it outright.

## 9.3 The failure that matters most

**Email fails silently.** The site is built to never crash a page because email broke — so
when email stops, **nothing turns red.** No error, no alert. Members simply stop receiving
things and nobody finds out for weeks.

**So check it deliberately:** go to **Admin → Broadcast → "Email Test (SMTP)"** and send
yourself one. (Ignore the "SMTP" in the label — it tests whatever is actually being used,
which in production is Resend.) That page sends immediately and shows the real error if it
fails. Do it monthly, and after any change to email settings or DNS.

## 9.4 What sends email automatically

Adding a member (optionally with their password in plain text), announcements, document
requests/confirmations/results, guide payout confirmations, new guide registrations, survey
submissions, onboarding assessment confirmations, and invoices.

---

# Part 10 — The danger zone

Read this before clicking things in admin.

## 10.1 ☢️ The trap: never click "Manage" on a College Guide

**This is a real, confirmed bug, not a theoretical one.**

The `/admin/users` list shows everyone — including `mentor`-tier College Guides. But the
"Plan" dropdown only offers **free / premium / admin**. It has no "mentor" option, so for a
guide's row the browser silently pre-selects **free**.

Open "Manage ▾" on a College Guide to change *anything*, click Save, and **you have just
demoted them to a free user.** They instantly lose the `/mentor` portal.

**You cannot undo it from the admin area** — "mentor" isn't an accepted value, so you can't
set it back. It needs direct database access to repair.

**Until this is fixed: do not open "Manage" on any College Guide.** (An older doc,
`GUIDE.md`, wrongly says the dropdown offers mentor. It doesn't. Trust this page.)

## 10.2 Things that delete permanently

No undo, no bin, no confirmation email:

- **Delete a member** — also erases their predictions and payments. (Guarded: can't delete
  yourself or another admin.)
- **Delete an invoice** — ⚠️ **no guard and no confirmation.** A paid, numbered, already-emailed
  invoice can vanish, leaving a hole in your invoice sequence. Your accountant will care.
- Delete an announcement, a schedule event, a meeting, or a payout record.

## 10.3 Things that leave the building

Once these go, they cannot be recalled:

- **The announcement email blast** — ticking "email all" mails every member, on a background
  thread. It does show you the recipient count first. **Read the count.**
- **"Send now"** on the templates page.
- **Adding a member with "Email login details" ticked** — this is **on by default** and emails
  their password in plain text.

## 10.4 Quiet surprises

- **Editing a membership application recalculates GST automatically.** Changing a state or
  tier changes the money.
- **Resetting a password does not tell the user.** They'll just be locked out until you say so.

## 10.5 The golden rules

1. Never open "Manage" on a College Guide (10.1).
2. Read the recipient count before any blast.
3. Assume every "Delete" is forever. It is.
4. Never test forms against the production database.
5. `FLASK_DEBUG` is `0` in production. Always.

---

# Part 11 — When something breaks

## 11.1 First: is it actually broken?

**The site is on Render's free plan, so it falls asleep when nobody visits.** The first visit
then takes **up to ~50 seconds** while it wakes up. That is normal and not a fault.

A GitHub Action pings the site every 10 minutes to keep it awake, which mostly hides this.
If that Action is disabled or GitHub is having a bad day, the sleepiness comes back.

**So: wait a full minute and reload before declaring an emergency.**

## 11.2 The playbook

| Symptom | Most likely cause | What to do |
|---|---|---|
| Site slow on first load, fine after | Free-tier sleep | Nothing. Normal. |
| Site down completely | Render | Check the Render dashboard for a failed deploy |
| Broke right after a push | Your change | *"Undo the last change and push the fix"* |
| **Email stopped** | Resend key or DNS | **Admin → Broadcast → Email Test** — it shows the real error |
| Uploads fail | R2 keys | Check the R2 settings in Render's Environment tab |
| Data vanished | ☢️ `DATABASE_URL` missing → it silently used a temporary file | Check Render's Environment tab **immediately** |
| A page 500s | A code bug | *"[page] is showing a 500 error. Find out why. Don't change anything yet."* |

## 11.3 The universal move

Copy the exact error and paste it to Claude Code with:

> *"This is happening: [paste]. I don't know what it means. Explain it simply, tell me how
> serious it is, and what my options are. Don't change anything yet."*

## 11.4 Two things you cannot fix from a laptop

- **Render's free plan has no shell access.** You can't log into the server. That's why the
  in-browser `/admin/email-test` page exists.
- **The database has no backup.** If Neon is empty, there is nothing to restore. See 2.5.

---

# Part 12 — Known problems that need fixing

These are real, verified, and outstanding. **Give this list to whoever does the next piece of
technical work.** They're ordered by how much they'd hurt.

### 1. 🔴 A real password is published on the public internet

`HANDOFF.md` (in this repo, which is **public on GitHub**) contains a live production account
and its password in plain text — a **premium** account. Anyone who finds the repo can log in
as that user today.

**Do now:** change that password; remove the line; and understand that **Git remembers
history**, so deleting the line does not remove it from the public record — the password must
actually be changed.

### 2. 🔴 There is no database backup

The whole business — members, leads, invoices — sits in one free-tier database with no backup
of any kind. See 2.5. **This is the biggest risk in the project.**

### 3. 🟠 A password is hardcoded in public browser code

`EXPERT_PIN = 'edu2026'` sits in two files under `app/static/`, which any visitor can read by
viewing the page source. The gate it protects is therefore decorative. (It currently guards
nothing live, which limits the damage.) This is the **same class of mistake** that got
`/counsellor-dashboard` deleted in July 2026 — the lesson didn't reach these two files.

### 4. 🟠 The College Guide demotion trap

See 10.1. A one-line fix for a developer; a silent disaster for an operator.

### 5. 🟡 Render's config doesn't declare the email or storage keys

`render.yaml` lists four settings. The Resend and R2 keys were added by hand in the dashboard.
Rebuild the service from that file and email plus uploads die silently. See 2.6.

### 6. 🟡 Six public, unauthenticated Google Sheets webhooks

See 2.4. Redundant — safe to delete once you've confirmed nobody reads the Sheets.

### 7. 🟢 Older docs have drifted out of date

`GUIDE.md` says the dropdown offers "mentor" (it doesn't — see 10.1), that plans must be
changed in the database (they're changeable at `/admin/users`), and that the templates page
only opens drafts (there's now a real Send button). `README.md` says there are 3 blueprints;
there are 10. **Where they disagree with this handbook, trust this handbook** — it was
written by reading the actual code.

---

# Part 13 — Glossary

| Word | Plain English |
|---|---|
| **API** | A door for programs (rather than people) to fetch data |
| **Backend** | The part on the server that thinks. Invisible to visitors. |
| **Blueprint** | A section of the site grouped in one file (auth, admin, invoices…) |
| **Branch** | A parallel copy of the code for work in progress |
| **Cold start** | The ~50s delay when a sleeping free-tier site wakes up |
| **Commit** | A save point in the project's history, with a note |
| **CSV** | A spreadsheet saved as plain text. Opens in Excel. |
| **Database** | The permanent notebook: members, leads, invoices |
| **Deploy** | Publishing a change to the live site |
| **DNS** | The internet's phone book. Turns a name into an address. |
| **`.env`** | The file holding your secrets. Never share it. |
| **Environment variable** | A setting passed to the app from outside the code |
| **Flask** | The framework this site is built with |
| **Frontend** | What the visitor sees |
| **Git** | The tool that remembers every version of everything |
| **GitHub** | The website where Git history is stored and shared |
| **Lead** | Someone who filled in a form. A potential customer. |
| **Migration** | A controlled database change. **This project has none.** |
| **`main`** | The branch that is the live site |
| **Push** | Upload commits to GitHub → **triggers a live deploy** |
| **Repository / repo** | The project folder plus its full history |
| **Route** | A web address and the code behind it |
| **Secret** | A password-like string that proves the site may use a service |
| **SMTP** | The traditional way of sending email. **Blocked on Render's free plan.** |
| **Template** | The HTML skeleton of a page, with blanks the code fills in |
| **Tier** | An account's level: free / premium / admin / mentor |
| **Virtual environment (`.venv`)** | A private box of the exact software versions this project needs |
| **Webhook** | A URL that another service posts data to |

---

## Where to go next

| You want to | Go to |
|---|---|
| Set up your laptop | Part 4 |
| Understand the accounts | Part 2 |
| Make your first change | Part 3, then Part 6 |
| Do the daily admin | Part 7 |
| Fix something urgently | Part 11 |
| Brief a developer | Part 12 |
| More technical depth | `college-predictor/GUIDE.md`, `README.md`, `ARCHITECTURE.md` — but where they contradict this file, trust this file |

---

*This handbook was written by reading the actual code, not from memory or older documents.
Where it contradicts `GUIDE.md` or `README.md`, it is because those drifted — see Part 12.7.*

*When you change how something works, change this file in the same breath. A handbook nobody
trusts is worse than no handbook.*
