# EduAakashaa College Predictor

A Flask-based college admission helper portal for Indian engineering aspirants, powered by official JOSAA 2025 counselling data and NIRF 2026 rankings.

> **Live reference site:** <https://eduaakashaa.in/>  
> **Origin:** Migrated from a Hostinger/Zyro website builder into a proper Flask codebase.

---

## Quick Start

```bash
cd college-predictor
pip install -r requirements.txt
python run.py

# → http://127.0.0.1:5000
```

---

## Project Structure

```
college-predictor/
├── run.py                          # Flask entry point (port 5000)
├── config.py                       # App configuration (SECRET_KEY, DEBUG)
├── requirements.txt                # Python dependencies
├── ARCHITECTURE.md                 # Full architecture spec (future roadmap)
├── README.md                       # ← You are here
│
└── app/
    ├── __init__.py                 # App factory — create_app(), registers Blueprint
    │
    ├── routes/
    │   ├── __init__.py             # main_bp Blueprint — all 19 routes defined here
    │   └── main.py                 # Imports main_bp (entry point for the blueprint)
    │
    ├── templates/
    │   ├── base.html               # Master layout — sticky bar, nav (19 links), footer
    │   ├── home.html               # NRI Admission guide (10 chapters, full content)
    │   ├── josaa.html              # JOSAA Predictor portal (7-tab SPA)
    │   └── placeholder.html        # "Coming Soon" template for unbuilt pages
    │
    ├── static/
    │   ├── css/
    │   │   ├── style.css           # Main site styles (dark/gold theme, Georgia serif)
    │   │   └── josaa.css           # JOSAA portal styles (blue/orange, Arial sans-serif)
    │   ├── js/
    │   │   ├── main.js             # Hamburger menu, scroll spy, mobile nav
    │   │   └── josaa.js            # Full predictor logic — 15+ functions, Chart.js charts
    │   ├── data/
    │   │   └── josaa_data.js       # 367 KB — JOSAA cutoff dataset + NIRF rankings
    │   └── images/                 # (reserved for future assets)
    │
    └── data/
        └── files/                  # (reserved for Excel source files)
```

---

## Pages & Routes

| Route | Template | Status | Description |
|-------|----------|--------|-------------|
| `/` | home.html | ✅ Built | NRI Admission guide — 10 chapters covering DASA, CIWG, country guides, fee comparison |
| `/josaa` | josaa.html | ✅ Built | JOSAA College Predictor — 7 interactive tabs (see below) |
| `/iiits` | placeholder.html | 🔲 Planned | IIITs information |
| `/annanri` | placeholder.html | 🔲 Planned | Anna University NRI admission |
| `/dasa-seat-matrix` | placeholder.html | 🔲 Planned | DASA seat matrix |
| `/dasa-admissions-guide` | placeholder.html | 🔲 Planned | DASA & CIWG admissions guide |
| `/nirf-ranking` | placeholder.html | 🔲 Planned | NIRF engineering rankings |
| `/tnea2026` | placeholder.html | 🔲 Planned | TNEA 2026 admissions |
| `/tneamatrix` | placeholder.html | 🔲 Planned | TNEA seat matrix |
| `/tneapc` | placeholder.html | 🔲 Planned | TNEA preference calculator |
| `/tnea-cutoff` | placeholder.html | 🔲 Planned | TNEA cutoff analysis |
| `/professional-exam` | placeholder.html | 🔲 Planned | Professional exam guide |
| `/internship-programs` | placeholder.html | 🔲 Planned | Internship programs |
| `/contact` | placeholder.html | 🔲 Planned | Contact page |
| `/mbamca-program` | placeholder.html | 🔲 Planned | MBA & MCA program guide |
| `/tancet` | placeholder.html | 🔲 Planned | TANCET exam guide |
| `/ea-library` | placeholder.html | 🔲 Planned | EduAakashaa library |
| `/tancet-pulse` | placeholder.html | 🔲 Planned | TANCET PULSE |
| `/viteee-for-nri` | placeholder.html | 🔲 Planned | VITEEE for NRI students |

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

Data is loaded server-side at startup using Pandas. The client never sees the full dataset — all data access goes through 6 JSON API endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /api/josaa/meta` | Dropdown options (institutes, programs, quotas, seat types, genders) |
| `GET /api/josaa/predict` | Filtered prediction results for a given rank/category/gender |
| `GET /api/josaa/matrix` | Institute×branch matrix data |
| `GET /api/josaa/nirf` | Filtered NIRF rankings |
| `GET /api/josaa/insights` | Pre-computed IIT/NIT branch analysis |
| `GET /api/josaa/analytics` | Pre-computed chart datasets (8 Chart.js charts) |

---

## Design System

The app uses two distinct visual themes:

| Property | Main site (`style.css`) | JOSAA portal (`josaa.css`) |
|----------|------------------------|---------------------------|
| Primary | `#1A1A2E` (dark) | `#1E4DB7` (blue) |
| Accent | `#C9A84C` (gold) | `#F97316` (orange) |
| Background | `#F9F5EE` (cream) | `#F0F4FF` (light blue) |
| Font | Georgia, serif | Arial, sans-serif |
| Scoping | Global | `.josaa-portal` wrapper |

The JOSAA CSS is scoped under `.josaa-portal` to avoid conflicting with the base layout styles.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.1.0 (Python) |
| Data Layer | Pandas + openpyxl (in-memory DataFrames) |
| API | Flask Blueprint (`api_bp`) — 6 JSON endpoints |
| Templating | Jinja2 (server-rendered) |
| Routing | Flask Blueprints (`main_bp` + `api_bp`) |
| Frontend | Vanilla HTML/CSS/JS |
| Charts | Chart.js 4.4.0 (CDN) |
| Fonts | Google Fonts (Oswald) |
| Deployment | Gunicorn (production) |

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

---

## Future Roadmap (from ARCHITECTURE.md)

- [x] **Server-side prediction** — Pandas-based prediction engine via Flask API endpoints
- [x] **Excel data loading** — JOSAA/NIRF data loaded from Excel/CSV via `app/data/loader.py`
- [ ] **User authentication** — Flask-Login + Flask-Bcrypt (session-based)
- [ ] **Premium tier** — RBAC with free/premium/admin roles
- [ ] **Razorpay payments** — Subscription checkout for premium features
- [ ] **SQLite database** — User data, predictions, bookmarks
- [ ] **Build remaining 17 pages** — TNEA, DASA, TANCET, Contact, etc.
- [ ] **Playwright tests** — Replace boilerplate test with actual page tests
