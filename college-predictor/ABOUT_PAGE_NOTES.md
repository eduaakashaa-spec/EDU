# About page — copy deliverables & implementation notes

Live copy: `app/templates/about.html` (route `/about`). This file holds the extras requested in the brief.

## 1. Mission and vision statements

**Mission:** To give every student personalised, honest mentorship — and to guide families through career choices and college admissions with clarity, care and consistent follow-through.

**Vision:** An educational guidance ecosystem where no student misses a suitable opportunity for want of information, clear procedures or guidance — and where families have a trusted, long-term partner for the decisions that matter.

## 2. Brand promise and tagline options

**Promise:** *We will listen carefully, explain honestly, guide responsibly and honour our commitments — throughout the journey we agree with you.*

Closing line (used on the page): *"Your child's future is not just another application to us. It is a responsibility we approach with care, commitment and purpose."*

Tagline options
1. **More than admission guidance — mentorship you can count on.** (primary, echoes the brand message)
2. Clarity. Confidence. Committed support.
3. We don't just tell you what to do. We help you navigate what comes next.
4. A trusted partner for every step of the journey.
5. Your future deserves commitment.

## 3. Recommended section order and calls to action

| # | Section | Anchor | Primary CTA |
|---|---|---|---|
| 1 | Hero — who we are | — | **Talk to a Mentor** (→ membership page) · Chat on WhatsApp |
| 2 | Why EduAakashaA exists | `#purpose` | — (let the story land) |
| 3 | Mission | `#mission` | — |
| 4 | Vision | `#vision` | — |
| 5 | Commitment to NRI families (dark band for prominence) | `#nri` | **Read the NRI admission guide** · Talk to a Mentor |
| 6 | Our approach — we take ownership (six steps) | `#approach` | — |
| 7 | Our values (eight) | `#values` | — |
| 8 | What makes our mentorship different | `#different` | — |
| 8b | Data you can use, freely — free insights, facts over social-media noise, open invitation | `#insights` | **Talk to a Mentor** · WhatsApp |
| 9 | A promise to students and parents | `#promise` | **Talk to a Mentor** · WhatsApp · email · phone |

CTAs are deliberately limited to the hero, the NRI band and the closing promise so the page reads as a story, not a sales page.

## 4. SEO

* **Title:** `About EduAakashaA | Educational Mentorship & College Admission Guidance` (69 chars)
* **Meta description:** `Student-first educational mentorship: personalised college admission guidance, career guidance and NRI admissions in India, with honest advice and committed support.` (165 chars; search results may trim the last few words)
* Open Graph title/description and `EducationalOrganization` JSON-LD (name, url, logo, email, telephone — nothing invented) are in the page `<head>`.
* Phrases used naturally in the copy: educational mentorship, college admission guidance, NRI admissions in India, career guidance for students, personalised admission counselling (via "personalised … mentorship"/"counselling steps"), Indian colleges / admission in Indian colleges for NRI families.
* One `<h1>`; each section is an `<h2>` with its own anchor; cards use `<h3>`.

## 5. Implementation notes for the developer

* **Brand consistency:** inherits `base.html` (header, footer, theme toggle) and `pages.css` hero/CTA components; page-specific styles are scoped under `.ab` / `ab-*` in the template, using the existing CSS variables (navy `--navy`, orange `--orange`, cream `--cream`, `Fraunces` / `Plus Jakarta Sans`). Dark mode is handled.
* **Responsive & accessible:** CSS grid with `auto-fit` (single column on phones); text line-length capped at 70ch; contrast is white-on-navy or navy-on-cream (WCAG AA); decorative icons are `aria-hidden` SVG via `ea_icon`; no content depends on JavaScript.
* **Removed from the old page:** the JOSAA "Check results" form, the generic FAQ, the "Hours: 24/7" and "Online portal only" lines. The old FAQ content is covered on the JoSAA and NRI pages. If you want the lead form back, add a new form posting to `api.capture_lead` with a new `source` (e.g. `about-conversation`).
* **Imagery:** no photographs are included — the brief asks for *authentic* student/mentor imagery and none was provided. Add real photos (with consent) in the hero or beside the Approach section; do not use stock images presented as students or testimonials. Recommended: 1200 × 800 px WebP, `alt` text describing the scene, `loading="lazy"` below the fold.
* **Do not add** testimonials, success rates, rankings, partnerships or credentials unless they can be substantiated; the page deliberately contains none. The disclaimer at the end (no guarantee of admission, college, branch or rank) should stay.
* **Contact details** (info@eduaakashaa.com, +91-80157 22706) match the rest of the site; business hours are intentionally omitted until confirmed.
* **Links:** "Talk to a Mentor" → `main.members_registration`; NRI CTA → `main.nri_guide`; WhatsApp → the global `WHATSAPP_URL`.
* **Tracking (optional):** add UTM/analytics events to the three CTA groups to learn which section converts.
