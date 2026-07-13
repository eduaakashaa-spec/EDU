# EduAakashaa — Pre-Production Go-Live Checklist

Run through this before every production deploy (push to `main` → Render autodeploy →
https://eduaakashaa.onrender.com). Tick each box. Anything that fails blocks the release.

> Tip: Render free tier cold-starts (~50 s) after idle — the **first** request after a
> sleep is slow, not broken. Warm it, then test.

---

## 1. Build & boot
- [ ] `git status` clean; on `main`; latest pulled.
- [ ] App imports & boots locally: `.venv/bin/python -c "from app import create_app; create_app()"` (no traceback).
- [ ] `requirements.txt` covers every import (pandas, openpyxl, flask-login, bcrypt, etc.).
- [ ] No stray debug prints / `FLASK_DEBUG=1` left on for prod.
- [ ] Smoke test all public pages: from repo root `BASE_URL=http://127.0.0.1:<port> npx playwright test tests/smoke.spec.ts --project=chromium` → every route <400, no console errors. Regenerate `tests/all_pages.json` from `app.url_map` if routes changed.

## 2. Datasets load (served from files, not JS)
- [ ] Each dataset endpoint returns 200 + its global:
  `/api/data/tnea-cutoffs-full.js` (EA_TNEA_FULL), `/api/data/tnea2026-cutoffs.js` (EA_TNEA2026),
  `/api/data/nirf-full.js` (EA_NIRF300), `/api/data/ciwg-choice-builder.js` (EA_CIWG),
  `/api/data/engg-colleges-india.js`, `/api/data/tnea-colleges.js`,
  `/api/data/tnea-expert-guidance.js`, `/api/data/dasa-seat-matrix.js`.
- [ ] The 4 master xlsx exist in `app/data/files/` (JOSAA / NIRF / TNEA 2025 / DASA CIWG).
- [ ] `nirf_full.json` has 300 rows; `tnea_cutoffs_full.json` 3,448; `ciwg_choice_builder.json` has MIT Manipal.

## 3. Predictors & tools return results (the core value)
- [ ] **JOSAA predictor** (`/josaa`): enter a rank → college list renders; `/api/josaa/predict`, `/josaa/matrix`, `/josaa/nirf` respond.
- [ ] **DASA predictor** (`/api/dasa/predict`): POST a rank → results.
- [ ] **Choice Builder PRO** (`/choice-builder-pro`, admin): enter a DASA rank + CIWG → tiered list renders; **MIT Manipal appears** with real ranks (not the synthetic estimate).
- [ ] **TNEA** (`/tnea-expert`, `/tnea-colleges`, `/free-report`): cutoffs/colleges render; TNEA 2026 simulator loads.
- [ ] **NIRF** (`/nirf-ranking`, `/nirf-analytic`): 300 institutes render; scores match expectation (e.g. IIT Madras 88.72).
- [ ] **DASA seat matrix / ranks** pages render.
- [ ] Spot-check 2–3 known values against the source data (no NaN / blank / "undefined").
- [ ] Browser console shows **no JS errors** on each tool page.

## 4. Forms save to the DB
- [ ] Contact form (`/contact-us`) → row in ContactInquiry (`/admin/inquiries`).
- [ ] Any page lead form → PageLead (`/admin/leads`); DASA lead capture works.
- [ ] College Survey (`/college-survey`) → CollegeSurvey (`/admin/surveys`).
- [ ] Alumni / College Guide signup (`/alumni-network`) → AlumniProfile (`/admin/alumni`); resume upload (PDF/DOC/DOCX → R2) + photo validated; admin can open the resume.
- [ ] Membership apply (`/membership/apply`) → MembershipApplication (`/admin/membership`) with a reference no.
- [ ] **Onboarding assessment** (`/onboarding-assessment/student` & `/parent`) → OnboardingResponse; student+parent **pair** by family in `/admin/onboarding`.
- [ ] Rate limits still allow normal use (not too aggressive).

## 5. Onboarding assessment extras
- [ ] Admin detail (`/admin/onboarding/<id>`): **Copy for AI** works; **Download .md (with rubric)** downloads a self-contained file (responses + Deliverable 2 & 3).
- [ ] Confidential items (S50/P34) shown counsellor-only, not in family-facing copy.
- [ ] Auto-confirmation email: **requires SMTP env** (`SMTP_HOST/USER/PASS`) — see §7. Without it, submit still works (email is a no-op). With it, submitting sends the student/parent a confirmation.

## 6. Admin & auth
- [ ] `/admin` overview loads fast (KPI bands + 4 charts + recent activity).
- [ ] Every `/admin/*` route requires admin tier; a logged-out user is redirected to `/login`.
- [ ] Member management (add / tier+validity / password / delete) works with lockout guards (can't remove own admin).
- [ ] Email Templates (`/admin/templates`): recipient dropdown loads, a draft opens in Gmail, logo renders in preview.
- [ ] Premium pages gated by `@premium_required`; DASA Review / Counsellor dashboard load.

## 7. Config & secrets (Render env)
- [ ] `DATABASE_URL` → **production Neon Postgres** (NOT a local sqlite; NOT a test DB).
- [ ] `SECRET_KEY` set to a real secret (not `dev-key-change-in-production`).
- [ ] `pool_pre_ping` + `pool_recycle` on (Neon SSL-drop fix) — already in config.
- [ ] GST/company/bank env vars set for invoices (`GSTIN`, `COMPANY_*`, `BANK_*`).
- [ ] **SMTP** vars set if auto-emails are wanted: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` (Gmail → App Password).
- [ ] `MAX_CONTENT_LENGTH` (10 MB) fine for resume+photo uploads.
- [ ] **R2 resume storage** vars set: `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET` (Object Read & Write token scoped to `eduaakashaa`). Without them, guide signup fails at the resume step.

## 8. Layout, mobile & UX
- [ ] Sticky top nav stays **above page content** on scroll on the ported pages (dasa-guide, free-report, best-location, career-path, tnea pages) — no overlay.
- [ ] Mobile navbar opens/closes; dropdowns reachable; onboarding stepper works one-question-per-screen on a phone.
- [ ] WhatsApp floater doesn't cover key controls; no duplicate floaters.
- [ ] Dark-mode / responsive spot check on 1–2 key pages.

## 9. Data integrity & migrations
- [ ] New tables auto-create on boot (`db.create_all()`) — but it does **NOT** alter existing tables. If a model column changed, run the ALTER manually on Neon first.
- [ ] `OnboardingResponse` table exists in prod after deploy (first load creates it).
- [ ] No destructive migration run against prod without a backup.

## 10. Post-deploy verification (on the live URL)
- [ ] Warm the site (first request), then re-run §3 spot-checks on https://eduaakashaa.onrender.com.
- [ ] Submit one real onboarding assessment (student) end-to-end; confirm it appears in `/admin/onboarding` and the confirmation email arrives (if SMTP on).
- [ ] Check GH Actions `/ping` keep-alive is green.
- [ ] Watch Render deploy logs for exceptions in the first few minutes.

---
_Owner: ___________  Date: ___________  Commit: ___________  Result: ☐ Go  ☐ No-go_
