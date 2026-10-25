# EduPulse-UCEED — question bank, practice and progress reports

A members-only tool (Member Home → **EduPulse-UCEED**, Premium) where students practise UCEED-style **multiple-choice questions chapter by chapter**, see their progress on a dashboard, and have results and progress emailed to themselves, their parent and their mentor.

Code: `app/models_pulse.py` · `app/services/pulse.py` · `app/routes/pulse.py` · `app/templates/pulse/*` · `app/templates/admin/pulse_*.html` · `app/static/css/pulse.css` · tests `tests/test_pulse.py`.

---

## 1. What is in the question bank — read this first

| | |
|---|---|
| **Starter bank** | 40 **original EduAakashaA practice questions** (5 in each of 8 chapters), text-only, with explanations. Their answers are machine-checked in `tests/test_pulse.py`. |
| **Not included** | **UCEED previous-year papers.** They are copyrighted, so they were not copied. The tool says on the dashboard that the bank is original practice material and EduPulse scores are guidance, not official marks. |
| **Adding real content** | Admin → EduPulse → *Import (CSV)* or *Add a question*. Add genuine previous-year items **only if you hold the rights**; fill `source` and `year`. Imports arrive as **drafts** and only **published** questions reach students. |
| **Figures** | UCEED Part A is visual. Each question can carry one JPG/PNG/WebP figure (< 500 KB). The starter questions are text-only; add figure-based questions yourself. |
| **MCQ only** | The tool covers the MCQ type. NAT / MSQ question types and Part B drawing are not part of it. |

Chapters mirror Phase 2 of the UCEED roadmap: Visual perception & observation · Spatial reasoning & visualisation · Patterns, shapes & transformations · Logical & analytical reasoning · Everyday design awareness · Problem-solving & lateral thinking · Materials, objects & functionality · Interpreting visual information & creativity.

## 2. How it works

**Student** (Premium member)
1. Open EduPulse-UCEED → fill the one-step registration (class, optional parent email **with a consent tick**, report frequency, "email me each result").
2. Pick a chapter (or a mixed set), 5/10/15/20 questions, untimed or timed (90 s per question; auto-submits).
3. Submit → result page with the correct answers, explanations, per-chapter breakdown and a practice score. Re-submitting is ignored.
4. The dashboard shows sets, questions answered, accuracy, streak, accuracy trend, per-chapter status (*Not enough data / Needs work (<60%) / On track / Strong (≥80%)*), coverage, next-step advice and recent sets.
5. Question choice prefers **unseen questions**, then ones previously answered wrongly, then the rest. Correct answers and explanations are never sent to the browser before submission.

**Mentor** (EA Mentor): *EduPulse mentor view* lists students who linked them (admin: all) with accuracy, streak, last activity and weak chapters; each student has a read-only detail page. A mentor is linked automatically from the student's Mentorship record, or an admin sets it (Admin → EduPulse → Registered students).

**Parent**: receives email only — no login, so there is no parent account to secure. Parent emails are sent **only if the student ticked the consent box**; the admin list shows "no consent — not mailed" otherwise.

**Admin**: Admin → EduPulse — chapters with published/total counts, add/edit/publish/unpublish/delete questions, CSV import and export, registered students, mentor assignment, report sending.

## 3. Email

All emails go from **info@eduaakashaa.com** (reply-to info@).

| Email | To | When |
|---|---|---|
| Practice result | the student (if "email me each result" is on) | right after each submitted set |
| Progress digest | student · parent (consent) · linked mentor | weekly or monthly (student's choice); also "Send report" / "Send all due reports" in admin |

A digest shows sets, questions, accuracy (with the change versus the previous period), streak, chapters going well / needing attention and next steps. Each student is mailed **at most once per period** (`pulse_reports` log).

**Email only works when a transport is configured** (`RESEND_API_KEY` with `eduaakashaa.com` verified, or SMTP). If it is not, the dashboard says so, the admin buttons say nothing was sent, and nothing is faked.

### Scheduling the periodic reports
The app has no built-in clock, so call it weekly (it only mails profiles whose period has elapsed):

* **Render Cron Job / any scheduler:** `python manage.py send_pulse_reports`
* **GitHub Actions:** `.github/workflows/pulse-reports.yml` calls `GET /edupulse-uceed/cron/reports?token=…` every Monday. Add repository secrets `PULSE_CRON_TOKEN` and (optional) `SITE_URL`, and set the same `PULSE_CRON_TOKEN` in Render. Without the token the endpoint returns 404.

## 4. Data model (`pulse_*` tables — created automatically)

`pulse_chapters` · `pulse_questions` (stem, 4 options, correct, explanation, difficulty, source, year, optional image, draft/published) · `pulse_profiles` (registration, parent email + consent, mentor, frequency) · `pulse_attempts` · `pulse_answers` (one row per question per attempt) · `pulse_reports` (digest log). Answered questions are never hard-deleted — they are unpublished so past results still render.

## 5. Privacy & safety

Student progress is visible to the student, their linked mentor and admins only. Parents get summaries by email with the student's consent. The consent text is on the registration form; students can switch reports off or remove the parent email in Settings, or write to info@eduaakashaa.com. Practice scoring (+1 / −⅓) is for guidance and is **not** the official UCEED marking scheme.

## 6. Limitations

* The starter bank is small (40) and text-only — it is a working foundation, not a full question bank; plan to add figure-based questions.
* No NAT/MSQ types, no drawing evaluation, no adaptive difficulty beyond "unseen first, then wrong".
* Reports need email sending to be configured and the weekly trigger set up (above).
* Mentor linking relies on the Mentorship record or an admin assignment.

## UCEED Mock Test Centre (previous-year papers + EduAakashaa mocks)

`/edupulse-uceed/mock` (Premium members; Member Home tile "UCEED Mock Test Centre"). The page is the supplied single-file portal (`app/data/uceed_mock/app.html`) inside a site page, so it keeps the EduAakashaa theme and navigation.

* **Papers:** official UCEED Part A papers 2018–2026 (613 questions, with official answers and EduAakashaa step-by-step explanations) and five original EduAakashaa practice papers (M1–M5). Timed mock (the year's real marking scheme, partial marks for MSQ) or untimed practice.
* **Confidence check:** each answer is rated Guess / Low / Medium / High. Reports show right/wrong by confidence, **sure but wrong** (High and wrong: a belief or method to fix), **unsure but right** (knowledge not yet trusted), topic tables and written pointers. With fewer than 8 rated answers the report says calibration cannot be judged.
* **Members-only files:** the papers live in `app/data/uceed_mock/data/` (not under `static/`) and are served through a login-checked route, so they are never public.
* **Saved results:** every finished test posts to `/edupulse-uceed/mock/results` (table `pulse_mock_results`, created automatically). Students see history, averages and a report/PDF per attempt on the mock page; the mentor view (`/edupulse-uceed/mentor`) shows mocks, average and sure-but-wrong rate per student, and each report. Taking a mock creates the student's EduPulse profile with e-mail digests **off** and links their mentor from the Mentorship record.
* **Adding or changing papers:** replace the JSON in `app/data/uceed_mock/data/` and the `YEARS`/`MOCKS` lists in `app.html` (see `app/data/uceed_mock/README.md`). Check every answer against the IIT Bombay answer key before publishing.
* **Change from the supplied file:** answers typed with the on-screen NAT keypad now enable the confidence buttons (they stayed disabled before, so keypad users could not rate).
* **Rights:** the official papers are IIT Bombay material; make sure your use is covered before opening the centre to members.
* Scores are practice guidance only and do not predict a UCEED score, rank or admission.

## EduPulse-JEE Mock Test Centre (JEE Main)

`/edupulse-jee/` (Premium members; Member Home tile "EduPulse-JEE Mock Test Centre"; button on the EduPulse page). Same engine and theme as the UCEED centre, built for JEE Main Paper 1 (B.E./B.Tech.) in the 2027 pattern.

* **Pattern:** 75 questions, 180 minutes, Mathematics / Physics / Chemistry, each 20 MCQ + 5 numerical; **+4 correct, −1 wrong, 0 blank in both sections** (NTA Information Bulletin 2027). Timed mock (3 h, free movement between subjects) and untimed practice.
* **Confidence + negative-marking tracker:** every answer is rated Guess / Low / Medium / High. The report shows marks gained and lost by subject and by MCQ vs numerical, the *avoidable loss* (wrong answers rated Guess or Low), *sure but wrong* answers, and for each confidence level the accuracy and the average marks per answer (4p − (1 − p); break-even accuracy is 20%) with the net marks of your Guess/Low answers, so students can see whether guessing helped. Reports are rule-based and explain themselves; fewer than 10 rated answers is called out rather than judged.
* **Papers:**
  * **EduAakashaa Mocks 1–5** (original, 375 questions, 40 chapters). Every answer is computed by the template that wrote the question (`tools/jee_mock/`); `python tools/jee_mock/build.py` regenerates a set (change `SEED_BASE` for new questions), `make_app.py` rebuilds the page and `make_index.py` the paper list.
  * **NTA previous-year papers (2026 B.Tech, 9 shifts):** the PDFs supplied are exam-engine exports with the questions as images and **no answer key** (the "possible answers" values are placeholders). `tools/jee_mock/extract_pyq.py` turns a PDF into a paper (75 questions as images with options labelled A–D) and `apply_key.py` applies the official key (CSV: `n` or `qid`, `answer` as A–D, an NTA option id, or the numeric value; `|` for two accepted answers; `BONUS`). A paper stays "not yet available" and is never served until every question has a key.
* **Saved results:** table `pulse_jee_results` (created automatically); posts to `/edupulse-jee/results`. Students see history and a report/PDF per attempt; mentors see JEE mocks, average and marks lost to negatives in `/edupulse-uceed/mentor` and per student. Taking a mock creates the student's EduPulse profile with e-mail digests off and links their mentor from the Mentorship record.
* Scores are practice guidance only and do not predict a JEE Main score, percentile or rank.
