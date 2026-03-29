# College Predictor App — Master Architecture Prompt

## Overview
A Flask-based college admission predictor for JoSAA counselling. Users input their JEE rank, category, and preferences to get predicted college/branch allotments based on historical cutoff data.

---

## Current Implementation Status

The following components from the roadmap below are **already built and working**:

| Component | Status | Notes |
|-----------|--------|-------|
| Flask app factory | ✅ Done | `app/__init__.py` — loads data at startup, registers `main_bp` + `api_bp` |
| Data loader | ✅ Done | `app/data/loader.py` — reads JOSAA Excel + NIRF CSV into Pandas DataFrames |
| Server-side API | ✅ Done | `app/routes/api.py` — 6 JSON endpoints (meta, predict, matrix, nirf, insights, analytics) |
| Page routes | ✅ Done | `app/routes/__init__.py` — 19 routes on `main_bp` Blueprint |
| JOSAA portal UI | ✅ Done | 7-tab SPA in `josaa.html` with `josaa.js` (fetch-based) + `josaa.css` |
| Home page | ✅ Done | 10-chapter NRI Admission guide |
| Chart.js analytics | ✅ Done | 8 charts + 2 insight charts, data fetched from API |
| Extensions (DB, auth) | 🔲 Planned | `extensions.py`, Flask-SQLAlchemy, Flask-Login |
| User models | 🔲 Planned | `models/user.py`, `models/payment.py` |
| Services layer | 🔲 Planned | `services/predictor.py`, `services/rbac.py`, etc. |
| Payments (Razorpay) | 🔲 Planned | `routes/payment.py` |
| Remaining 17 pages | 🔲 Planned | Currently on `placeholder.html` |

---

## Tech Stack

- **Framework:** Flask (serves both frontend and backend)
- **Templating:** Jinja2 (server-side rendered HTML)
- **Static Data:** Pandas DataFrames loaded from Excel files at app startup
- **Database:** SQLite via Flask-SQLAlchemy (user data only)
- **Auth:** Flask-Login + Flask-Bcrypt (session-based authentication)
- **RBAC:** Custom decorator-based role/tier gating (free, premium, admin)
- **Payments:** Razorpay (Indian payment gateway, supports UPI/cards/netbanking)
- **Frontend:** HTML/CSS/JS (no frontend framework; Jinja2 templates + vanilla JS or minimal jQuery)

---

## Data Strategy

### Static Reference Data (Excel → Pandas, in-memory)
These are read-only datasets. Loaded once at app startup into global DataFrames. Updated by swapping Excel files and restarting the app.

| Dataset | Source File | Contents |
|---|---|---|
| JoSAA Cutoffs | `JOSAA_2025_Open_and_close_rank_for_Round1_6.xlsx` | Opening/closing ranks by institute, branch, category, round |
| NIRF Rankings | `NIRF_Engineering_Rank_2026.xlsx` | College NIRF rank, score, city, state |
| College Profiles | TBD | Institute name, branches offered, seat matrix, institute type (IIT/NIT/IIIT/GFTI) |

### Dynamic User Data (SQLite)
All user-generated data lives in SQLite.

| Table | Fields |
|---|---|
| `users` | id, username, email, password_hash, tier (free/premium/admin), tier_expires_at, created_at |
| `payments` | id, user_id, razorpay_order_id, razorpay_payment_id, amount, status (pending/paid/failed), plan (monthly/yearly), created_at |
| `predictions` | id, user_id, rank, category, quota, results_json, created_at |
| `bookmarks` | id, user_id, institute, branch, created_at |

---

## Project Structure

```
college-predictor/
├── app/
│   ├── __init__.py            # App factory, register blueprints, load DataFrames
│   ├── extensions.py          # db, login_manager, bcrypt instances
│   ├── models/
│   │   ├── user.py            # SQLAlchemy models (User, Payment, Prediction, Bookmark)
│   │   └── payment.py         # Payment model
│   ├── data/
│   │   ├── loader.py          # Load Excel files into DataFrames at startup
│   │   └── files/             # Excel files stored here
│   │       ├── josaa_cutoffs.xlsx
│   │       └── nirf_rankings.xlsx
│   ├── services/
│   │   ├── predictor.py       # Core prediction logic (pandas queries)
│   │   ├── college_search.py  # Search/filter colleges
│   │   ├── analytics.py       # Stats, trends, comparisons
│   │   ├── payment.py         # Razorpay order creation, verification, tier upgrade
│   │   └── rbac.py            # Role/tier decorators and permission checks
│   ├── routes/
│   │   ├── auth.py            # Login, register, logout
│   │   ├── main.py            # Home, dashboard
│   │   ├── predict.py         # Prediction form + results
│   │   ├── payment.py         # Pricing page, checkout, Razorpay webhook
│   │   └── api.py             # JSON API endpoints (if needed)
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── predict/
│   │   │   ├── form.html
│   │   │   └── results.html
│   │   └── college/
│   │       ├── search.html
│   │       └── profile.html
│   │   └── payment/
│   │       ├── pricing.html
│   │       └── success.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── config.py                  # App config (SECRET_KEY, DB URI, debug mode)
├── run.py                     # Entry point
├── seed_db.py                 # Script to create tables and seed initial data
└── requirements.txt           # flask, flask-sqlalchemy, flask-login, flask-bcrypt,
                               # flask-wtf, pandas, openpyxl, razorpay, gunicorn
```

---

## App Factory Pattern

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, login_manager, bcrypt
from app.data.loader import load_all_data

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Load static data into memory
    app.data = load_all_data()

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.predict import predict_bp
    from app.routes.payment import payment_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(payment_bp)

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
# app/models/user.py
from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tier = db.Column(db.String(20), default='free')  # free, premium, admin
    tier_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_premium(self):
        if self.tier == 'admin':
            return True
        if self.tier == 'premium' and self.tier_expires_at:
            return self.tier_expires_at > datetime.utcnow()
        return False

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    razorpay_order_id = db.Column(db.String(100), nullable=False)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Integer, nullable=False)  # in paise
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    plan = db.Column(db.String(20), nullable=False)  # monthly, yearly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

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
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
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