# EduAakashaA College Predictor

A Flask-based college admission helper portal for Indian engineering aspirants, powered by official JOSAA 2025 counselling data and NIRF 2026 rankings. Covers NRI admissions (DASA/CIWG), JOSAA counselling, TNEA predictions, TANCET guidance, professional exams, and career planning.

> **Live reference site:** <https://eduaakashaa.in/>  
> **Origin:** Migrated from a Hostinger/Zyro website builder into a proper Flask codebase.

---

## Quick Start

```bash
cd college-predictor
pip install -r requirements.txt

# Initialise database & seed admin user
python manage.py init_db
python manage.py seed_sequences            # reference / invoice / receipt counters
python manage.py create_admin admin@eduaakashaa.com Admin123
python manage.py seed_demo                 # optional — sample membership rows

# Run the app
python run.py
# → http://127.0.0.1:5000
# Admin membership portal → http://127.0.0.1:5000/admin/membership
```

> **Migration note:** the membership/invoicing system is being migrated off
> Google Apps Script + Google Sheets into this app (PostgreSQL).
> See `../MIGRATION_GUIDE.md` and `ARCHITECTURE.md` → "Apps Script → Flask Migration".

---

## Project Structure

```
college-predictor/
├── run.py                          # Flask entry point (port 5000)
├── config.py                       # App config (SECRET_KEY, DB URI, DEBUG)
├── manage.py                       # CLI — init_db, create_admin commands
├── requirements.txt                # Python dependencies
├── ARCHITECTURE.md                 # Full architecture spec
├── README.md                       # ← You are here
│
└── app/
    ├── __init__.py                 # App factory — create_app(), 3 blueprints
    ├── extensions.py               # db, login_manager, bcrypt instances
    ├── models.py                   # 5 SQLAlchemy models
    │
    ├── routes/
    │   ├── main.py                 # main_bp — 19 page routes
    │   ├── api.py                  # api_bp — 7 JSON API endpoints
    │   └── auth.py                 # auth_bp — login, register, logout, dashboard, contact
    │
    ├── data/
    │   ├── loader.py               # Load JOSAA Excel + NIRF CSV into Pandas DataFrames
    │   └── files/                  # josaa_cutoffs.xlsx, nirf_rankings.csv
    │
    ├── templates/                  # 25 Jinja2 templates
    │   ├── base.html               # Master layout — sticky bar, nav, footer
    │   ├── home.html               # Landing page (hero, services, tools, pathways, CTA)
    │   ├── nri_guide.html          # NRI Admission guide (10 chapters)
    │   ├── josaa.html              # JOSAA Predictor portal (7-tab SPA)
    │   ├── (17 more content pages) # DASA, TNEA, TANCET, NIRF, MBA/MCA, Contact, etc.
    │   └── auth/                   # login.html, register.html, dashboard.html
    │
    └── static/
        ├── css/
        │   ├── style.css           # Global styles (dark/gold theme, all components)
        │   ├── josaa.css           # JOSAA portal (blue/orange, .josaa-portal scope)
        │   └── pages.css           # Page-specific overrides
        ├── js/
        │   ├── main.js             # Hamburger menu, scroll spy
        │   └── josaa.js            # Predictor logic, Chart.js charts
        └── images/
```

---

## Pages & Routes

### Content Pages (`main_bp`)

| Route | Template | Description |
|-------|----------|-------------|
| `/` | home.html | Landing page — hero, services, tools, pathways, testimonials, CTA |
| `/nri-admissions-guide` | nri_guide.html | NRI Admission guide — 10 chapters (DASA, CIWG, country guides, fees) |
| `/josaa` | josaa.html | JOSAA College Predictor — 7 interactive tabs (see below) |
| `/dasa-admissions-guide` | dasa_guide.html | DASA & CIWG admissions guide |
| `/dasa-seat-matrix` | dasa_seat_matrix.html | DASA seat matrix analysis |
| `/nirf-ranking` | nirf_ranking.html | NIRF 2026 engineering rankings |
| `/tnea2026` | tnea2026.html | TNEA 2026 admissions overview |
| `/tneamatrix` | tneamatrix.html | TNEA seat matrix |
| `/tneapc` | tneapc.html | TNEA preference calculator |
| `/tnea-cutoff` | tnea_cutoff.html | TNEA cutoff analysis |
| `/iiits` | iiits.html | IIITs information |
| `/annanri` | annanri.html | Anna University NRI admission |
| `/professional-exam` | professional_exam.html | Professional exam guide (CA, CS, CMA) |
| `/internship-programs` | internship.html | Internship programs |
| `/mbamca-program` | mbamca.html | MBA & MCA program guide |
| `/tancet` | tancet.html | TANCET exam guide |
| `/tancet-pulse` | tancet_pulse.html | TANCET PULSE |
| `/ea-library` | ea_library.html | EduAakashaa library / resources |
| `/viteee-for-nri` | viteee_nri.html | VITEEE for NRI students |
| `/contact` | contact.html | Contact page |

### Auth Routes (`auth_bp`)

| Route | Method | Description |
|-------|--------|-------------|
| `/login` | GET/POST | Email + password login |
| `/register` | GET/POST | User registration |
| `/logout` | GET | Logout + redirect |
| `/dashboard` | GET | User profile & tier info (login required) |
| `/contact-submit` | POST | Contact form submission |

### Membership & Admin Routes (`membership_bp`)

| Route | Method | Description |
|-------|--------|-------------|
| `/membership/apply` | POST | Public membership application intake (replaces Apps Script `doPost`) |
| `/admin/membership` | GET | Admin: all requests — search, filter, paginate, KPI cards |
| `/admin/membership/<id>` | GET | Admin: single request detail + actions |
| `/admin/membership/<id>/update` | POST | Edit fields / status / notes (recomputes GST) |
| `/admin/membership/<id>/discount` | POST | Apply discount + reason |
| `/admin/membership/<id>/adhoc` | POST | Set ad-hoc line items (JSON) |
| `/admin/membership/<id>/invoice` | POST | Issue invoice (transaction-safe number) |
| `/admin/membership/<id>/payment` | POST | Record payment / issue receipt |
| `/admin/membership/export.xlsx` | GET | Download all (filtered) rows as Excel |

### API Endpoints (`api_bp` — prefix `/api`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/josaa/meta` | GET | Dropdown options (institutes, programs, quotas, seat types, genders) |
| `/api/josaa/predict` | GET | Filtered prediction results for rank/category/gender |
| `/api/josaa/matrix` | GET | Institute × branch matrix data |
| `/api/josaa/nirf` | GET | Filtered NIRF rankings |
| `/api/josaa/insights` | GET | Pre-computed IIT/NIT branch analysis |
| `/api/josaa/analytics` | GET | Pre-computed chart datasets (8 Chart.js charts) |
| `/api/dasa/predict` | POST | DASA prediction with lead logging + RBAC-gated results |

---

## JOSAA Predictor — Feature Breakdown

The `/josaa` page is a single-page app within the Flask template, with 7 tabs:

### 1. Predictor (`🔮`)
- Input: JEE rank (CRL), category (10 options), gender, quota, institute type, branch
- Server-side filtering of 12,274 JOSAA records via `/api/josaa/predict`
- Calculates admission chance as **Safe / Moderate / Reach** based on rank position within the opening-closing rank span
- Optional: ±10% buffer, NIRF-weighted sorting
- Results table with pagination (25 per page)

### 2. Matrix (`📊`)
- College-branch comparison grid showing closing ranks
- Color-coded by rank range: 🟢 ≤5K, 🔵 ≤20K, 🟡 ≤50K, 🩷 ≤1.5L, ⚪ >1.5L
- Filterable by institute type, category, branch, quota

### 3. Analytics (`📈`)
- 6 KPI cards (institutes, programs, data entries, NIRF ranked, rounds, categories)
- 8 Chart.js visualizations:
  - Institute type distribution (doughnut)
  - Category-wise seat share (pie)
  - Top 10 branches (horizontal bar)
  - IIT vs NIT vs IIIT avg closing rank (bar)
  - Cutoff by branch & type (scatter with trend)
  - Top 25 institutes by opening rank (bar)
  - Hidden gem trade-off analysis (scatter)
  - Category advantage for CSE (bar)

### 4. NIRF 2026 (`🏆`)
- Searchable, filterable NIRF Engineering rankings (~300 colleges)
- Filter by state, rank range (Top 10/25/50/100/200)

### 5. Insights (`💡`)
- Data-driven recommendations (dynamically generated insight cards)
- College vs Branch trade-off analysis charts
- IIT admission clarity section with JEE Advanced context

### 6. Process (`📋`)
- 4 sub-tabs:
  - **JOSAA Process** — 7-step admission flow with timeline
  - **2026 Deadlines** — expected schedule table (20 events)
  - **FAQ** — dynamically rendered from josaa.js
  - **Announcements** — latest news alerts

### 7. Presentations (`🎬`)
- 3 video presentation scripts for students/parents/educators
- Slide outlines + full script excerpts

---

## Data Sources

| Dataset | Size | Format | Contents |
|---------|------|--------|----------|
| JOSAA cutoffs | 487 KB | Excel (`app/data/files/josaa_cutoffs.xlsx`) | 128 institutes, 253 programs, 6 quotas, 10 seat types, 2 genders, 12,274 records |
| NIRF 2026 | 16 KB | CSV (`app/data/files/nirf_rankings.csv`) | ~300 engineering colleges with Name + NIRF Rank |
| DASA cutoffs | 30 KB | JSON (`app/data/files/dasa_cutoffs.json`) | 324 records — 215 CIWG + 109 Non-CIWG, 47 institutes, 11 branch categories, 3 rounds |

Data is loaded server-side at startup using Pandas. The client never sees the full dataset — all data access goes through 6 JSON API endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /api/josaa/meta` | Dropdown options (institutes, programs, quotas, seat types, genders) |
| `GET /api/josaa/predict` | Filtered prediction results for a given rank/category/gender |
| `GET /api/josaa/matrix` | Institute×branch matrix data |
| `GET /api/josaa/nirf` | Filtered NIRF rankings |
| `GET /api/josaa/insights` | Pre-computed IIT/NIT branch analysis |
| `GET /api/josaa/analytics` | Pre-computed chart datasets (8 Chart.js charts) |
| `POST /api/dasa/predict` | Real DASA cutoff filtering (324 records, NIRF-sorted, RBAC-gated) |

---

## Design System

All pages (including the homepage) share a single `style.css` design system:

| Property | Main site (`style.css`) | JOSAA portal (`josaa.css`) |
|----------|------------------------|---------------------------|
| Primary | `#1A1A2E` (dark) | `#1E4DB7` (blue) |
| Accent | `#C9A84C` (gold) | `#F97316` (orange) |
| Background | `#F9F5EE` (cream) | `#F0F4FF` (light blue) |
| Font | Georgia, serif | Arial, sans-serif |
| Scoping | Global | `.josaa-portal` wrapper |

**Key `style.css` components:** `.hero`, `.main-content` (900px max-width), `.section`, `.eyebrow`, `.section__title`, `.info-cards`, `.service-cards`, `.toc-grid`, `.chapter-divider`, `.steps`, `.check-list`, `.fee-compare`, `.final-cta`, `.btn-main`, `.btn-out`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.1.0 (Python) |
| Database | PostgreSQL via Flask-SQLAlchemy 3.1.1 + psycopg2-binary |
| Auth | Flask-Login 0.6.3 + Flask-Bcrypt 1.0.1 |
| Data Layer | Pandas 2.2.3 + openpyxl 3.1.5 (in-memory DataFrames) |
| API | Flask Blueprints (`api_bp`) — 7 JSON endpoints |
| Templating | Jinja2 (server-rendered) |
| Routing | 3 Flask Blueprints (`main_bp`, `api_bp`, `auth_bp`) |
| Frontend | Vanilla HTML/CSS/JS |
| Charts | Chart.js 4.4.0 (CDN) |
| Fonts | Google Fonts (Oswald) |
| Deployment | Gunicorn 23.0.0 |

---

## Development Log

### Phase 1 — Site Exploration
- Navigated all 19 pages of the Hostinger site using Playwright
- Extracted HTML structure, CSS, and design tokens
- Catalogued navigation links and page hierarchy

### Phase 2 — Frontend Replica
- Created static HTML/CSS/JS replica of the NRI Admission home page
- Verified rendering at localhost:8080

### Phase 3 — Flask Migration
- Scaffolded Flask project with app factory pattern
- Created `base.html` master template with full navigation (19 links) and footer
- Created `home.html` with 10-chapter NRI Admission content
- Created `placeholder.html` for 17 unbuilt pages
- Defined all 19 routes in Blueprint

### Phase 4 — JOSAA Predictor Deep Extraction
- Navigated to the JOSAA page (iframe-embedded SPA on the live site)
- Extracted complete data: 12,123 JOSAA records, 128 institutes, 253 programs
- Extracted NIRF data: ~300 ranked engineering colleges
- Fixed HTML entity encoding issues in the extracted data
- Saved as `josaa_data.js` (367 KB)

### Phase 5 — JOSAA Predictor Build
- Created `josaa.css` — full JOSAA portal stylesheet (14 KB)
- Created `josaa.js` — complete predictor logic with 15+ functions (31 KB)
- Created `josaa.html` — full 7-tab template extending base.html
- Scoped JOSAA CSS under `.josaa-portal` to prevent style conflicts

### Phase 6 — Consolidation & Cleanup
- Removed `frontend/` folder (redundant — CSS/JS/HTML fully superseded by Flask templates)
- Removed `extract_data.py` and `fix_data.py` (one-time data extraction utilities)
- Removed `__pycache__/` directories
- Updated `.gitignore` for Python/Flask/IDE/OS artifacts
- Added `.gitkeep` to empty directories (`data/files/`, `static/images/`)
- Created this README

### Phase 7 — Server-Side API Migration
- Created `app/data/loader.py` — Pandas module that reads JOSAA Excel + NIRF CSV at startup
- Created `app/routes/api.py` — `api_bp` Blueprint with 6 JSON API endpoints
- Updated `app/__init__.py` — loads data at startup, registers `api_bp`
- Rewrote `app/static/js/josaa.js` — replaced all global constant access with `fetch()` API calls
- Removed `josaa_data.js` script tag from `josaa.html`
- Deleted `app/static/data/josaa_data.js` (354 KB static data file)
- Added `pandas` and `openpyxl` to `requirements.txt`
- Fixed NIT quota filtering bug (NITs use 'OS' quota, not 'AI')

### Phase 8 — Header & Navigation Fix
- Split JOSAA header into two rows: brand bar (logo + badge) and navigation bar
- Removed `position: sticky` and high `z-index` that caused header to overlay dropdowns
- Navigation is now horizontally scrollable on mobile instead of hidden
- Added brand text label next to logo

### Phase 9 — Content Pages
- Built all 17 placeholder pages with full content templates
- Each page follows `style.css` design system: `.hero`, `.main-content`, `.section`, `.eyebrow`, `.info-cards`, `.check-list`, etc.
- Total: 22 content templates (+ `base.html`, `placeholder.html`, `josaa.html`)

### Phase 10 — Homepage Redesign
- Created a modern landing page with 10 sections: hero, services, tools, pillars, pathways, two-pathway comparison, steps, testimonials, CTA
- Initially used a separate `homepage.css` with `hp-` prefixed classes

### Phase 11 — Database, Auth & RBAC
- Added Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt to the stack
- Created `extensions.py`, `models.py` (5 models: User, DasaLead, Prediction, Payment, ContactInquiry)
- Created `auth_bp` blueprint: login, register, logout, dashboard, contact form
- Implemented tier system: free (3 DASA results), premium (unlimited), admin
- RBAC enforced in `api.py` — DASA predict logs leads and gates results by tier
- Created `manage.py` CLI: `init_db`, `create_admin`
- Seeded admin user: admin@eduaakashaa.com
- Updated `base.html` with conditional Login/Dashboard nav link
- Created auth templates: `auth/login.html`, `auth/register.html`, `auth/dashboard.html`

### Phase 12 — Homepage Unification
- Rewrote `home.html` to use the same `style.css` design system as all other content pages
- Removed dependency on `homepage.css` — all `hp-` prefixed classes replaced with standard components
- Mapped sections: `hp-hero` → `.hero`, `hp-services` → `.info-cards`, `hp-tools` → `.service-cards`, `hp-pathways` → `.toc-grid`, `hp-dual-paths` → `.fee-compare`, `hp-steps` → `.steps`, etc.
- Site now has a fully consistent visual identity across every page

### Phase 13 — DASA Real Data + PostgreSQL
- Scraped live DASA predictor iframe on eduaakashaa.in using Playwright — extracted `RAW_DATA` (175 KB JS variable)
- Saved 324 real DASA 2025 cutoff records to `app/data/files/dasa_cutoffs.json` (215 CIWG + 109 Non-CIWG, 47 institutes, 11 branch categories, 3 rounds)
- Updated `loader.py` — added `get_dasa_df()` to load DASA JSON at startup
- Replaced 8-row placeholder in `/api/dasa/predict` with real Pandas filtering (quota, branch category, institute, rank-based chance, NIRF-sorted)
- Updated `dasa_guide.html` form dropdowns to match actual data branch categories and all 36 real institute names
- Migrated database from SQLite → PostgreSQL; `config.py` already reads `DATABASE_URL` env var so zero Flask code changes needed
- Added `psycopg2-binary` to `requirements.txt`; created `.env` template with `DATABASE_URL` and `SECRET_KEY`

---

### Phase 14 — Apps Script → Flask Membership Migration (in progress)
- Assessed Google Sheets/Drive as a production DB (security, GST integrity, speed) — see `../MIGRATION_GUIDE.md`
- Extracted the legacy Apps Script backend structure (50 functions, 35-column sheet schema) → `../migration/LEGACY_APPS_SCRIPT_REFERENCE.md`
- Added `models_membership.py` — `MembershipApplication`, `MembershipInvoice`, `DocSequence` (paise-based money)
- Added `services/pricing.py` — GST engine (CGST/SGST/IGST, GST-inclusive); math unit-verified
- Added `routes/membership.py` — public `/membership/apply` intake + full admin portal + Excel export
- Added admin templates (`templates/admin/`) in the EduAakashaa design system
- Transaction-safe reference/invoice/receipt numbering via `doc_sequences`
- Wired into `app/__init__.py`; added `seed_sequences` / `seed_demo` to `manage.py`
- **Pending (Phase B):** invoice/receipt PDF generation, transactional email, one-time Sheet→Postgres backfill

## Future Roadmap

- [x] **Server-side prediction** — Pandas-based prediction engine via Flask API endpoints
- [x] **Excel data loading** — JOSAA/NIRF data loaded from Excel/CSV via `app/data/loader.py`
- [x] **Build all content pages** — 22 templates with full content (TNEA, DASA, TANCET, Contact, etc.)
- [x] **User authentication** — Flask-Login + Flask-Bcrypt (session-based)
- [x] **SQLite database** — 5 models: User, DasaLead, Prediction, Payment, ContactInquiry
- [x] **RBAC tier system** — Free (3 results) / Premium (unlimited) / Admin
- [x] **DASA predict API** — Real DASA 2025 cutoff data (324 records), lead logging, RBAC-gated
- [x] **Homepage unification** — All pages share the same `style.css` design system
- [x] **PostgreSQL migration** — Switched from SQLite to PostgreSQL; `DATABASE_URL` env-var driven
- [x] **Membership data model** — MembershipApplication, MembershipInvoice, DocSequence
- [x] **GST pricing engine** — CGST/SGST/IGST, GST-inclusive, paise-based
- [x] **Admin membership portal + Excel export** — non-tech staff data view
- [ ] **Membership PDFs** — invoice/receipt generation (WeasyPrint/ReportLab)
- [ ] **Membership emails** — application/invoice/receipt notifications
- [ ] **Sheet → Postgres backfill** — one-time import of legacy data
- [ ] **Razorpay payments** — Subscription checkout for premium tier upgrades
- [ ] **Services layer** — Extract prediction/RBAC logic into dedicated service modules
- [ ] **Playwright tests** — Replace boilerplate test with actual page tests
- [ ] **Email notifications** — Payment receipts, tier expiry reminders
- [ ] **Production deployment** — Gunicorn + Nginx, environment variable config
