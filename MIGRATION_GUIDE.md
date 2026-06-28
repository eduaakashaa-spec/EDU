# EduAakashaa — Membership/Invoice Migration Guide

**Goal:** decide whether the membership "database" should stay in Google
Drive (Google Sheets), and migrate the Apps Script membership + invoicing
system into the existing Flask codebase — securely and fast.

**Date:** 2026-06-28
**Repos involved:** this Flask app (`college-predictor/`) + two Apps Script
projects (see `migration/LEGACY_APPS_SCRIPT_REFERENCE.md`).

---

## 1. TL;DR recommendation

**Do not keep the production database in Google Sheets/Drive. Migrate it into
the PostgreSQL database the Flask app already runs.**

Google's infrastructure is secure and reliable, but using a *Sheet* as your
application database for **customer PII + GST tax invoices** carries real
security, integrity and speed problems (below). You already have PostgreSQL,
Flask-Login auth, bcrypt and an RBAC tier system — the membership system
belongs there. Accessing the Sheet from Flask via the Google API is *possible*
but would be the worst of both worlds, so it is **not** recommended.

Keep Google only where it genuinely helps: optionally a **one-way read-only
export** to a Sheet for staff who like spreadsheets, and (optionally) Drive for
PDF archival in a **non-public** folder via a service account.

---

## 1b. Build status (this session)

Decision confirmed with you: the **admin page becomes the place non-tech staff
see all data** (no spreadsheet, no DB access), with a one-click **Export to
Excel** for when they want a sheet. Built so far, in the Flask app:

| Piece | File | Status |
|---|---|---|
| Membership/invoice tables (PostgreSQL) | `app/models_membership.py` | ✅ wired into `app/__init__.py` |
| GST pricing engine (CGST/SGST/IGST, GST-inclusive) | `app/services/pricing.py` | ✅ math unit-verified |
| Public application intake (replaces `doPost`) | `POST /membership/apply` | ✅ |
| Admin data view — search / filter / paginate | `GET /admin/membership` | ✅ EduAakashaa-styled |
| Admin detail + actions (edit, discount, ad-hoc, issue invoice, record payment) | `GET/POST /admin/membership/<id>/…` | ✅ transaction-safe invoice/receipt numbering |
| **Export to Excel** (respects filters) | `GET /admin/membership/export.xlsx` | ✅ |
| CLI: `seed_sequences`, `seed_demo` | `manage.py` | ✅ |

**Still to do (Phase B):** invoice/receipt **PDF generation**, **email**
sending, and a **one-time backfill** of the existing Google Sheet rows. Hooks
are already marked in the code where these plug in. Code is written but not yet
run end-to-end here (the build sandbox can't mount your Desktop folder) — see
"How to run locally" below.

### How to run locally
```bash
cd college-predictor
pip install -r requirements.txt
python manage.py init_db          # creates the new tables
python manage.py seed_sequences   # reference / invoice / receipt counters
python manage.py seed_demo        # optional: 3 sample rows to see the admin page
python manage.py create_admin you@eduaakashaa.com YourPassword   # if not already
python run.py
# log in, then open  /admin/membership
```

---

## 2. Is keeping the DB in Google Drive safe? — Assessment

### What "the database" actually is today
A single Google Sheet ("Requests" tab, ~35 columns) holding every membership
application: customer PII (name, email, phone, city, state) **and** financial /
tax data (tier price, discounts, CGST/SGST/IGST, totals, invoice numbers,
payment records). Invoice and receipt **PDFs are stored in Google Drive**.
Sequence counters and the admin password live in Apps Script PropertiesService.

### Security
| Concern | Verdict |
|---|---|
| Google data-centre security (encryption at rest/in transit, uptime) | ✅ Strong — not the problem |
| Access control | ⚠️ Coarse & human-managed. One wrong "Anyone with the link" toggle exposes all PII + financials. The logo already uses public link-sharing, and invoice/receipt PDFs in Drive are typically link-shared to be emailable — meaning **tax documents with PII may be world-readable by URL**. |
| Admin authentication | ⚠️ Single shared password (`guard`/`adminLogin`). No per-user accounts, no bcrypt, no lockout/rate-limit, no audit of who changed what. The Flask app already has stronger auth. |
| Data-protection compliance (India DPDP Act 2023) | ⚠️ Harder to govern access, deletion and minimisation in a shared spreadsheet than in an app-gated DB. |

### Data integrity
| Concern | Verdict |
|---|---|
| Transactions / ACID | ❌ Sheets is not transactional. Invoice numbers come from Properties`lastInv`, written separately from the row — under concurrency you can get **duplicate or skipped invoice numbers**, which is a GST compliance problem (invoice numbering must be unique & sequential). |
| Concurrent edits | ⚠️ Admin editing while `doPost` appends a new application can race. |
| Backups | ⚠️ Version history ≠ real backups; an accidental delete or bad paste can corrupt data. |

### Speed & scale
| Concern | Verdict |
|---|---|
| Per-operation latency | ❌ Every SpreadsheetApp/Drive call is a network round-trip (100s of ms–seconds). Admin actions feel slow. |
| Growth | ❌ Sheets degrades as rows grow into the thousands. |
| Apps Script quotas | ❌ 6-min execution limit, daily execution caps, and **email limits (~100/day consumer Gmail, 1,500/day Workspace)** — a hard ceiling for a growing membership business. |

### Conclusion
Safe enough as a *prototype* for low volume; **not** a sound long-term
production database for PII + tax invoices, especially when a proper DB is
already in place.

---

## 3. Can we use it from our own code instead of Apps Script?

**Yes, technically.** Flask can talk to Sheets/Drive directly:
- Create a Google Cloud **service account**, download its JSON key.
- Enable Sheets API + Drive API; share the Sheet/folders with the service
  account email.
- Use `gspread` (Sheets) and `google-api-python-client` (Drive) from Flask.

**But it's not recommended here**, because it keeps every downside above
(API latency, quotas, no transactions, link-sharing risk) while adding a Google
dependency to your own server — and you already run PostgreSQL, which is faster,
transactional and fully under your control. Use the Sheets API route **only**
if non-technical staff must edit records directly in a spreadsheet UI; even
then, prefer a one-way Postgres → Sheet export.

---

## 4. Target architecture (recommended)

```
Browser (premium-membership.html, admin UI)
        │  HTTPS
        ▼
Flask app (college-predictor)  ── single codebase, in git, Gunicorn+Nginx
        ├── PostgreSQL          ← membership applications, invoices, payments (source of truth)
        ├── PDF service         ← WeasyPrint/ReportLab generates invoice & receipt PDFs
        ├── File storage        ← invoice/receipt PDFs on server disk or S3-compatible bucket (private)
        └── Email service       ← transactional email (SMTP / Resend / SendGrid / SES)
```

Why this is more secure **and** faster:
- Auth: reuse Flask-Login + bcrypt + the `admin` tier (replace the shared password).
- Integrity: DB transaction wraps "allocate invoice number + write row" → no gaps/dupes.
- Speed: local SQL queries in milliseconds; no Apps Script quotas or Sheets latency.
- Governance: PII/financial data behind app auth; PDFs private, links signed/expiring.
- One deploy, one backup strategy, full version control.

---

## 5. What's already done (existing Flask app)

| Capability | Status | Where |
|---|---|---|
| Flask app factory, blueprints | ✅ | `app/__init__.py` |
| **PostgreSQL** via SQLAlchemy | ✅ | `extensions.py`, `DATABASE_URL` in `.env` |
| Auth: login/register/logout + sessions | ✅ | `routes/auth.py`, Flask-Login |
| Password hashing | ✅ | Flask-Bcrypt |
| RBAC tiers (free/premium/admin) | ✅ | `models.User`, enforced in `api.py` |
| Data models: User, DasaLead, Prediction, **Payment**, ContactInquiry | ✅ | `models.py` |
| JOSAA/DASA predictors + content pages | ✅ | `routes/api.py`, `routes/main.py`, templates |
| Admin CLI (`init_db`, `create_admin`) | ✅ | `manage.py` |

The foundation we need (DB + auth + RBAC + a Payment model) is **already in
place** — the membership/invoice layer just needs to be added on top.

---

## 6. What's to be done (migration plan)

### Phase 0 — Prereqs (½ day)
- [ ] Free disk space / confirm a working Python env (current sandbox is out of disk).
- [ ] Create `.env` entries (see §8). Copy secrets **by hand** from the Apps
      Script CONFIG/PropertiesService — never commit them.
- [ ] Add deps to `requirements.txt`: `weasyprint` (or `reportlab`),
      an email lib (`flask-mail` or provider SDK), and if doing a Sheets export
      later, `gspread` + `google-api-python-client`.

### Phase 1 — Data model (½ day)  ← **scaffolded for you**
- [ ] Add `MembershipApplication`, `Invoice`, `InvoiceReceipt` models that mirror
      the Sheet schema (clean column names). Starter file:
      `app/models_membership.py` (created in this migration — review then merge
      into `models.py` / import it in `app/__init__.py`).
- [ ] `python manage.py init_db` to create the new tables.

### Phase 2 — Application intake (½ day)
- [ ] New blueprint `routes/membership.py` with `POST /membership/apply`
      replacing Apps Script `doPost`/`handleApplicationSubmit`.
- [ ] Point `premium-membership.html` form at the new endpoint.
- [ ] Validation + CSRF + spam/honeypot.

### Phase 3 — Pricing / GST engine (1 day)
- [ ] Port `computeTotals`/`recalcRow`: tier price + add-ons + ad-hoc − discount,
      GST 18% inclusive, CGST+SGST vs IGST by place of supply.
- [ ] Unit tests covering each tax case (intra-state vs inter-state, discounts, ad-hoc).

### Phase 4 — Admin portal (1–2 days)
- [ ] Admin routes (login_required + `admin` tier) replacing the Apps Script
      admin APIs: list, update, set discount, set ad-hoc, issue invoice,
      record payment, resend email.
- [ ] Reuse the existing EduAakashaa-styled `Admin.html` as a Jinja template.
- [ ] **Transactional** invoice/receipt number allocation (DB sequence/row lock)
      to guarantee unique, gap-free numbering.

### Phase 5 — PDF invoices & receipts (1 day)
- [ ] Port `documentHtml`/`buildDocumentPdf` to a Jinja HTML template rendered to
      PDF via WeasyPrint. Keep the existing invoice/receipt layout.
- [ ] Store PDFs in a **private** location (server disk or S3 bucket); serve via
      an authenticated route or signed, expiring URL — not public links.

### Phase 6 — Email (½ day)
- [ ] Port `emailApplicationReceived`/`emailInvoice`/`emailReceipt` to the chosen
      transactional provider (better deliverability + no Gmail 100/day cap).
- [ ] Always CC `info@eduaakashaa.com` (matches current behaviour).

### Phase 7 — Data backfill (½ day)
- [ ] One-time script: read the existing "Requests" Sheet (via `gspread` or an
      exported CSV) → insert rows into PostgreSQL. Verify counts & totals.
- [ ] Re-link or re-archive existing invoice/receipt PDFs.

### Phase 8 — Cutover & decommission (½ day)
- [ ] Switch the live form to the Flask endpoint; monitor.
- [ ] Optional: one-way Postgres → Sheet export for staff visibility.
- [ ] Lock down / unpublish the Apps Script web app; tighten Drive sharing.

### Phase 9 — Security & deploy hardening (ongoing)
- [ ] Force HTTPS, set `SESSION_COOKIE_SECURE`, `HTTPONLY`, `SAMESITE`.
- [ ] Enable CSRF (Flask-WTF) on all forms (noted as planned in ARCHITECTURE.md).
- [ ] Rotate the admin credential; remove the shared password concept.
- [ ] Automated PostgreSQL backups; restrict DB network access.
- [ ] Razorpay payments (already on the roadmap) wired to the `Payment` model.

---

## 7. Security checklist (carry into every phase)
- Secrets only in `.env` / environment — never in code or git. Add `.env` to `.gitignore` (verify).
- Invoice/receipt PDFs **private**; no "anyone with link" sharing of PII.
- Per-admin accounts (bcrypt), audit who issued/edited invoices.
- Server-side validation + CSRF on all forms; never trust client totals.
- Transactional invoice numbering (unique, sequential — GST requirement).
- HTTPS everywhere; secure session cookies.

---

## 8. `.env` keys to add (fill from Apps Script CONFIG — do not commit)
```
# already present
DATABASE_URL=postgresql://...
SECRET_KEY=...

# membership / invoicing
ADMIN_EMAIL=info@eduaakashaa.com
COMPANY_LEGAL_NAME=...
COMPANY_PAN=...
GSTIN=
BANK_AC_NAME=...
BANK_AC_NO=...
BANK_IFSC=...
BANK_NAME=...
BANK_BRANCH=...
HOME_STATE=Tamil Nadu
GST_RATE=0.18
LOGO_URL=...

# email provider
MAIL_SERVER=...
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_DEFAULT_SENDER=info@eduaakashaa.com

# only if you keep a Sheets export/backfill
GOOGLE_SERVICE_ACCOUNT_JSON=path/to/service-account.json
REQUESTS_SHEET_ID=...
```

---

## 9. Effort estimate
Roughly **6–9 working days** end-to-end for one developer, phaseable and
shippable incrementally (intake first, admin/PDF/email next, backfill last).

---

## 10. Open questions for you
1. **PDF storage:** server disk, or an S3-compatible bucket (recommended if you deploy on multiple instances)?
2. **Email provider:** keep Gmail SMTP short-term, or move to Resend/SendGrid/SES?
3. **Staff spreadsheet:** do non-technical staff need a live Sheet view (one-way export), or is the Flask admin UI enough?
4. **Backfill source:** can you share the existing "Requests" Sheet (or a CSV export) so I can write the one-time import?
