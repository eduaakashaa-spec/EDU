# EduAakashaA — Master Architecture Document

## Overview
A Flask-based college admission helper portal for Indian engineering aspirants. Covers NRI admissions (DASA/CIWG), JOSAA counselling, TNEA predictions, TANCET guidance, and career planning — powered by 12,000+ official data points from JOSAA 2025 and NIRF 2026 rankings.

> **Live reference site:** <https://eduaakashaa.in/>

---

## Current Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Flask app factory | ✅ Done | `app/__init__.py` — loads data at startup, registers 3 Blueprints |
| Data loader | ✅ Done | `app/data/loader.py` — reads JOSAA Excel + NIRF CSV + DASA JSON into Pandas DataFrames |
| Server-side API | ✅ Done | `app/routes/api.py` — 7 JSON endpoints (meta, predict, matrix, nirf, insights, analytics, DASA predict) |
| Page routes | ✅ Done | `app/routes/main.py` — 19 routes on `main_bp` Blueprint |
| JOSAA portal UI | ✅ Done | 7-tab SPA in `josaa.html` with `josaa.js` (fetch-based) + `josaa.css` |
| All content pages | ✅ Done | 22 templates — NRI guide, DASA, TNEA, TANCET, NIRF, Contact, etc. |
| Homepage | ✅ Done | Modern landing page using the global `style.css` design system |
| Chart.js analytics | ✅ Done | 8 charts + 2 insight charts, data fetched from API |
| Extensions (DB, auth) | ✅ Done | `extensions.py` — Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt |
| Database models | ✅ Done | `models.py` — User, DasaLead, Prediction, Payment, ContactInquiry |
| Auth system | ✅ Done | `routes/auth.py` — login, register, logout, dashboard, contact form |
| RBAC tier system | ✅ Done | Free (3 results) / Premium (unlimited) / Admin — enforced in API |
| DASA predict API | ✅ Done | Real 324-record dataset, Pandas filtering, NIRF-sorted, lead logging, RBAC-gated |
| Admin CLI | ✅ Done | `manage.py` — init_db, create_admin commands |
| PostgreSQL | ✅ Done | Migrated from SQLite; `DATABASE_URL` env-var driven via `.env` + python-dotenv |
| Services layer | 🔲 Planned | `services/predictor.py`, `services/rbac.py`, etc. |
| Payments (Razorpay) | 🔲 Planned | `routes/payment.py` — checkout flow |

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | Flask | 3.1.0 |
| Templating | Jinja2 (server-rendered) | — |
| Data layer | Pandas + openpyxl (in-memory DataFrames) | 2.2.3 |
| Database | PostgreSQL via Flask-SQLAlchemy + psycopg2-binary | 3.1.1 |
| Auth | Flask-Login (sessions) + Flask-Bcrypt (passwords) | 0.6.3 / 1.0.1 |
| RBAC | Custom tier-gated logic in API routes | — |
| Frontend | Vanilla HTML / CSS / JS | — |
| Charts | Chart.js (CDN) | 4.4.0 |
| Fonts | Google Fonts (Oswald) | — |
| Payments | Razorpay (planned) | — |
| Deployment | Gunicorn | 23.0.0 |

---

## Data Strategy

### Static Reference Data (Excel/CSV/JSON → Pandas, in-memory)
These are read-only datasets. Loaded once at app startup into global DataFrames. Updated by swapping files and restarting.

| Dataset | Source File | Contents |
|---|---|---|
| JOSAA Cutoffs | `app/data/files/josaa_cutoffs.xlsx` | 12,274 records — opening/closing ranks by institute, branch, category, round |
| NIRF Rankings | `app/data/files/nirf_rankings.csv` | ~300 engineering colleges with NIRF rank |
| DASA Cutoffs | `app/data/files/dasa_cutoffs.json` | 324 records — 215 CIWG + 109 Non-CIWG, 47 institutes, 11 branch categories, 3 rounds |

### Dynamic User Data (PostgreSQL via SQLAlchemy)
All user-generated data lives in PostgreSQL, managed via Flask-SQLAlchemy (`app/models.py`).
Connection configured via `DATABASE_URL` environment variable (`.env` file, loaded by python-dotenv).

| Model | Table | Key Fields |
|---|---|---|
| `User` | `users` | id, name, email, password_hash, tier (free/premium/admin), tier_expires_at, created_at. Properties: `is_premium`, `is_admin` |
| `DasaLead` | `dasa_leads` | id, name, email, rank, quota, branch, institute, timestamp, source |
| `Prediction` | `predictions` | id, user_id (FK), predictor (josaa/dasa/tnea), query_json, results_json, created_at |
| `Payment` | `payments` | id, user_id (FK), razorpay_order_id, razorpay_payment_id, amount, currency, status, plan, created_at |
| `ContactInquiry` | `contact_inquiries` | id, first_name, last_name, email, interested, message, created_at |

---

## Project Structure

```
college-predictor/
├── run.py                          # Flask entry point (port 5000)
├── config.py                       # App config (SECRET_KEY, DB URI, DEBUG)
├── manage.py                       # CLI — init_db, create_admin commands
├── requirements.txt                # flask, pandas, flask-sqlalchemy, flask-login, flask-bcrypt, etc.
├── ARCHITECTURE.md                 # ← You are here
├── README.md                       # Quick start, routes, dev log
│
├── app/
│   ├── __init__.py                 # App factory — create_app(), extensions init, 3 blueprints
│   ├── extensions.py               # db (SQLAlchemy), login_manager, bcrypt instances
│   ├── models.py                   # 5 SQLAlchemy models (User, DasaLead, Prediction, Payment, ContactInquiry)
│   │
│   ├── routes/
│   │   ├── __init__.py             # (package init)
│   │   ├── main.py                 # main_bp — 19 page routes
│   │   ├── api.py                  # api_bp — 7 JSON API endpoints (/api/...)
│   │   └── auth.py                 # auth_bp — login, register, logout, dashboard, contact_submit
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py               # Load JOSAA Excel + NIRF CSV + DASA JSON into Pandas DataFrames at startup
│   │   └── files/
│   │       ├── josaa_cutoffs.xlsx   # 12,274 JOSAA records
│   │       ├── nirf_rankings.csv   # ~300 NIRF-ranked engineering colleges
│   │       └── dasa_cutoffs.json   # 324 DASA 2025 cutoff records (all 3 rounds)
│   │
│   ├── templates/                  # 25 Jinja2 templates
│   │   ├── base.html               # Master layout — sticky bar, nav, footer, conditional Login/Dashboard
│   │   ├── home.html               # Landing page (hero, services, tools, pathways, CTA)
│   │   ├── nri_guide.html          # NRI Admission guide (10 chapters)
│   │   ├── josaa.html              # JOSAA Predictor portal (7-tab SPA)
│   │   ├── dasa_guide.html         # DASA & CIWG admissions guide
│   │   ├── dasa_seat_matrix.html   # DASA seat matrix
│   │   ├── tnea2026.html           # TNEA 2026 admissions
│   │   ├── tneamatrix.html         # TNEA seat matrix
│   │   ├── tneapc.html             # TNEA preference calculator
│   │   ├── tnea_cutoff.html        # TNEA cutoff analysis
│   │   ├── nirf_ranking.html       # NIRF engineering rankings
│   │   ├── iiits.html              # IIITs information
│   │   ├── annanri.html            # Anna University NRI admission
│   │   ├── professional_exam.html  # Professional exam guide (CA, CS, CMA)
│   │   ├── internship.html         # Internship programs
│   │   ├── mbamca.html             # MBA & MCA program guide
│   │   ├── tancet.html             # TANCET exam guide
│   │   ├── tancet_pulse.html       # TANCET PULSE
│   │   ├── ea_library.html         # EduAakashaa library / resources
│   │   ├── viteee_nri.html         # VITEEE for NRI students
│   │   ├── contact.html            # Contact page
│   │   ├── placeholder.html        # Generic "Coming Soon" template (no longer used)
│   │   └── auth/
│   │       ├── login.html          # Login form
│   │       ├── register.html       # Registration form
│   │       └── dashboard.html      # User dashboard
│   │
│   └── static/
│       ├── css/
│       │   ├── style.css           # Global site styles (dark/gold theme, Georgia serif, all components)
│       │   ├── josaa.css           # JOSAA portal styles (blue/orange, scoped under .josaa-portal)
│       │   ├── pages.css           # Page-specific overrides
│       │   └── homepage.css        # (orphaned — no longer used after homepage unification)
│       ├── js/
│       │   ├── main.js             # Hamburger menu, scroll spy, mobile nav
│       │   └── josaa.js            # Full predictor logic — 15+ functions, Chart.js charts
│       └── images/
│           └── .gitkeep
│
└── instance/
    └── (PostgreSQL replaces the old SQLite file here — no local db file)
```

---

## App Factory Pattern

```python
# app/__init__.py (simplified)
from flask import Flask
from app.extensions import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # User loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create DB tables
    with app.app_context():
        db.create_all()

    # Load static data into memory (JOSAA + NIRF DataFrames)
    from app.data.loader import load_all_data
    app.data = load_all_data()

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    return app
```

---

## Data Loader

```python
# app/data/loader.py
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')

def load_all_data():
    data = {}
    data['cutoffs'] = pd.read_excel(os.path.join(DATA_DIR, 'josaa_cutoffs.xlsx'))
    data['nirf'] = pd.read_excel(os.path.join(DATA_DIR, 'nirf_rankings.xlsx'))
    # Normalize column names
    for key in data:
        data[key].columns = data[key].columns.str.strip().str.lower().str.replace(' ', '_')
    return data
```

---

## Prediction Logic (Core Service)

```python
# app/services/predictor.py
from flask import current_app

def predict_colleges(rank, category, quota='AI', preferred_branches=None, round_no=6):
    """
    Given a user's rank, return colleges where their rank
    falls within the closing rank for that category.
    """
    df = current_app.data['cutoffs']

    # Filter by category and quota
    mask = (df['seat_type'] == category) & (df['quota'] == quota)
    if preferred_branches:
        mask &= df['branch'].isin(preferred_branches)

    results = df[mask & (df['closing_rank'] >= rank)]

    # Sort by closing rank (tighter = more competitive = better match)
    results = results.sort_values('closing_rank', ascending=True)

    # Merge NIRF data if available
    nirf = current_app.data['nirf']
    results = results.merge(nirf, on='institute', how='left')

    return results.to_dict(orient='records')
```

---

## Auth Setup

```python
# app/models.py (abbreviated — 5 models total)
from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tier          = db.Column(db.String(20), default='free')  # free / premium / admin
    tier_expires_at = db.Column(db.DateTime, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_premium(self):
        if self.tier == 'admin':
            return True
        if self.tier == 'premium' and self.tier_expires_at:
            return self.tier_expires_at > datetime.utcnow()
        return False

    @property
    def is_admin(self):
        return self.tier == 'admin'

class DasaLead(db.Model):     # Captures every DASA predict request
class Prediction(db.Model):   # Stores prediction query + results per user
class Payment(db.Model):      # Razorpay payment lifecycle
class ContactInquiry(db.Model): # Contact form submissions
```

### Auth Routes (`auth_bp`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/login` | GET/POST | Email + password login, Flask-Login session |
| `/register` | GET/POST | Name + email + password, bcrypt password hash |
| `/logout` | GET | Logs out, redirects to home |
| `/dashboard` | GET | @login_required — user profile + tier info |
| `/contact-submit` | POST | Contact form handler → saves ContactInquiry to DB |

---

## RBAC (Role-Based Access Control)

### Tier Definitions

| Tier | Access |
|---|---|
| `free` | Basic prediction (top 10 results), college search, NIRF rankings view |
| `premium` | Unlimited predictions, full result list, branch-wise analytics, trend charts, bookmark colleges, prediction history |
| `admin` | All premium features + user management, data upload, system controls |

### Tier Decorator

```python
# app/services/rbac.py
from functools import wraps
from flask import abort
from flask_login import current_user

def requires_tier(*allowed_tiers):
    """Gate routes by user tier. Admin always passes."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.tier == 'admin':
                return f(*args, **kwargs)
            if current_user.tier not in allowed_tiers:
                abort(403)
            # Check expiry for premium users
            if current_user.tier == 'premium' and not current_user.is_premium:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage in routes:
# @app.route('/advanced-analytics')
# @login_required
# @requires_tier('premium')
# def advanced_analytics():
#     ...
```

### Template-Level Gating

```html
<!-- In Jinja2 templates, show/hide UI elements by tier -->
{% if current_user.is_premium %}
    <a href="/analytics">Advanced Analytics</a>
    <a href="/trends">Branch Trends</a>
{% else %}
    <a href="/pricing">Upgrade to Premium</a>
{% endif %}
```

---

## Payment Flow (Razorpay)

### Flow Overview

```
User clicks "Upgrade" → Pricing page → Selects plan
    → Server creates Razorpay order (POST /payment/create-order)
    → Razorpay checkout opens in browser (JS SDK)
    → User completes payment (UPI/Card/Netbanking)
    → Razorpay sends callback to frontend
    → Frontend sends payment details to server (POST /payment/verify)
    → Server verifies signature with Razorpay SDK
    → On success: update user tier + tier_expires_at in SQLite
    → Redirect to success page
```

### Server-Side Payment Logic

```python
# app/services/payment.py
import razorpay
from flask import current_app
from app.extensions import db
from app.models.user import User, Payment
from datetime import datetime, timedelta

client = None

def get_razorpay_client():
    global client
    if not client:
        client = razorpay.Client(
            auth=(current_app.config['RAZORPAY_KEY_ID'],
                  current_app.config['RAZORPAY_KEY_SECRET'])
        )
    return client

PLANS = {
    'monthly': {'amount': 9900, 'days': 30},     # ₹99
    'yearly':  {'amount': 79900, 'days': 365},    # ₹799
}

def create_order(user_id, plan):
    """Create a Razorpay order and store it in DB."""
    rz = get_razorpay_client()
    plan_info = PLANS[plan]

    order = rz.order.create({
        'amount': plan_info['amount'],
        'currency': 'INR',
        'payment_capture': 1
    })

    payment = Payment(
        user_id=user_id,
        razorpay_order_id=order['id'],
        amount=plan_info['amount'],
        plan=plan,
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    return order

def verify_and_activate(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify Razorpay signature and upgrade user tier."""
    rz = get_razorpay_client()

    # Verify signature (raises SignatureVerificationError if invalid)
    rz.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    })

    # Update payment record
    payment = Payment.query.filter_by(razorpay_order_id=razorpay_order_id).first()
    payment.razorpay_payment_id = razorpay_payment_id
    payment.status = 'paid'

    # Upgrade user tier
    user = User.query.get(payment.user_id)
    plan_info = PLANS[payment.plan]
    user.tier = 'premium'
    user.tier_expires_at = datetime.utcnow() + timedelta(days=plan_info['days'])

    db.session.commit()
    return True
```

### Frontend Checkout (Jinja2 Template)

```html
<!-- templates/payment/pricing.html -->
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
function openCheckout(orderId, amount, plan) {
    var options = {
        "key": "{{ config.RAZORPAY_KEY_ID }}",
        "amount": amount,
        "currency": "INR",
        "name": "College Predictor",
        "description": plan + " Premium Plan",
        "order_id": orderId,
        "handler": function (response) {
            // Send to server for verification
            fetch('/payment/verify', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_signature: response.razorpay_signature
                })
            }).then(res => {
                if (res.ok) window.location.href = '/payment/success';
            });
        },
        "prefill": {
            "email": "{{ current_user.email }}"
        }
    };
    var rzp = new Razorpay(options);
    rzp.open();
}
</script>
```

### Config

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/eduaakashaa.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')       # planned
    # RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') # planned
```

---

## Security Principles

- All prediction logic, data processing, and business rules stay in Python (server-side). Never expose algorithms in JS or templates.
- API endpoints return only computed results, never raw DataFrames or file paths.
- Passwords hashed with bcrypt. Sessions managed by Flask-Login.
- SECRET_KEY and any sensitive config loaded from environment variables, never hardcoded.
- CSRF protection enabled via Flask-WTF on all forms.
- Razorpay KEY_SECRET never exposed to frontend. Only KEY_ID is used client-side.
- All payment verifications done server-side using Razorpay signature verification. Never trust client-side payment confirmation alone.
- Tier checks enforced server-side via decorators. Frontend tier gating is cosmetic only — always enforce on the backend.

---

## Key Design Decisions

1. **No separate backend service.** Flask handles everything — pages, API, auth. Simple monolith.
2. **Excel as source of truth for reference data.** No need to migrate cutoff/NIRF data into SQLite. Update by replacing files.
3. **SQLite for user data only.** No concurrency requirements. Single-file DB, zero config.
4. **Server-side rendering.** Jinja2 templates. No React/Vue. JS used only for interactivity (dropdowns, AJAX prediction calls).
5. **In-memory DataFrames.** Data loaded once at startup. Fast reads, no repeated disk I/O.

---

## Deployment Notes

- **Dev:** `flask run` with debug mode
- **Prod:** Gunicorn + Nginx on a VPS (DigitalOcean, AWS Lightsail, etc.) or Railway/Render for managed hosting
- SQLite file lives on disk alongside the app. Back it up periodically.
- For Excel file updates: replace file in `app/data/files/`, restart the app.

---

## Future Considerations (only if needed)

- **PostgreSQL:** Switch if you need multiple concurrent users or hosted DB.
- **Redis:** Add if you want caching for expensive prediction queries.
- **Celery:** Add if you need background jobs (email notifications, batch processing, auto-expiry checks for premium tiers).
- **REST API:** Formalize with Flask-RESTX if you build a mobile app later.
- **Razorpay Subscriptions API:** Switch from one-time orders to auto-recurring subscriptions if you want automatic monthly/yearly renewals.
- **Email Notifications:** Send payment receipts, tier expiry reminders, and welcome emails via Flask-Mail or a transactional service like Resend/SendGrid.