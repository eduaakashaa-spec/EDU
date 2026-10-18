"""Daily exam-date watcher for /exam-schedule.

What it does (it never edits the site by itself):
  1. Fetches each official page listed in app/data/exam_sources.json and pulls out the sentences that
     mention a keyword (e.g. "registration", "exam date") together with a date.
  2. Compares them with the previous run (state file) and reports anything added / removed / changed.
  3. Checks our own data (app/services/exam_page.py) for rows that are due for confirmation: Expected /
     Tentative dates that are close or already past, and a "verified on" stamp that has gone stale.
  4. Writes a Markdown report and sets the step output `has_findings` for the GitHub workflow, which opens or
     updates one review issue. A person (or Claude) then edits exam_page.py — dates are only marked
     Confirmed when the conducting body has announced them.

Usage:  python scripts/exam_watch.py --state .watch/state.json --report .watch/report.md
First run with no state only records a baseline (no change alerts).
"""
import argparse
import html
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

MONTH = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
DATE_RE = re.compile(r'(?:\b\d{1,2}(?:st|nd|rd|th)?\s*(?:[-–to]+\s*\d{1,2}(?:st|nd|rd|th)?\s*)?' + MONTH + r'\.?,?\s*20\d\d\b|\b' + MONTH + r'\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s*20\d\d\b|\b\d{1,2}[/.-]\d{1,2}[/.-]20\d\d\b)', re.I)
UA = 'Mozilla/5.0 (compatible; EduAakashaA-ExamWatch/1.0; +https://www.eduaakashaa.com)'
MAX_SNIPPETS = 25


def clean_text(raw):
    raw = re.sub(r'(?is)<(script|style|noscript).*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(raw)).strip()


def snippets(text, keywords):
    """Sentences that contain a keyword AND a date, shortened and de-duplicated."""
    out, seen = [], set()
    for sent in re.split(r'(?<=[.!?])\s+|\s{2,}|\s[|•·]\s', text):
        s = sent.strip()
        if len(s) < 12 or not DATE_RE.search(s):
            continue
        low = s.lower()
        if keywords and not any(k.lower() in low for k in keywords):
            continue
        s = s[:220]
        key = re.sub(r'\W+', '', s.lower())
        if key not in seen:
            seen.add(key)
            out.append(s)
        if len(out) >= MAX_SNIPPETS:
            break
    return out


def fetch(url):
    import requests
    r = requests.get(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*'}, timeout=25)
    r.raise_for_status()
    return r.text


def check_sources(sources, state):
    changes, errors, new_state = [], [], {}
    for src in sources:
        sid = src['id']
        try:
            text = clean_text(fetch(src['url']))
            snips = snippets(text, src.get('keywords', []))
        except Exception as exc:  # network / TLS / 403 — report, keep the old snapshot
            errors.append((src, f'{type(exc).__name__}: {str(exc)[:120]}'))
            if sid in state:
                new_state[sid] = state[sid]
            continue
        new_state[sid] = {'snippets': snips, 'seen': datetime.now(timezone.utc).strftime('%Y-%m-%d')}
        if sid not in state:
            continue                                    # baseline for this source
        old = set(state[sid].get('snippets', []))
        added = [s for s in snips if s not in old]
        removed = [s for s in old if s not in set(snips)]
        if added or removed:
            changes.append((src, added, removed))
    return changes, errors, new_state


def internal_checks(today):
    """Rows in exam_page.py that are due for a human look. Skipped (with a note) if the app cannot be imported."""
    try:
        from app.services import exam_page as ep
    except Exception as exc:
        return [f'Internal checks skipped — could not import exam_page ({type(exc).__name__}).'], None
    notes = []
    age = (today - ep.VERIFIED).days
    if age > 7:
        notes.append(f'The page says “verified {ep.VERIFIED:%d %b %Y}” — that is {age} days ago. Re-verify and bump `VERIFIED` once checked.')
    soon = today + timedelta(days=21)
    for cat in ep.CATEGORIES:
        for ex in cat['exams']:
            eid, name, status, start = ex[0], ex[1], ex[4], ex[6]
            if status == 'Confirmed' or not start:
                continue
            try:
                d0 = date.fromisoformat(start)
            except ValueError:
                continue
            if d0 < today:
                notes.append(f'**{name}** (`{eid}`) is still {status} but its start date {d0:%d %b %Y} has passed — confirm or move it.')
            elif d0 <= soon:
                notes.append(f'**{name}** (`{eid}`) is {status} and starts {d0:%d %b %Y} — look for an official announcement.')
    for eid, rows in ep.DEADLINES.items():
        for kind, dt, status, _note in rows:
            if status == 'Confirmed' or not dt or kind not in ('open', 'close', 'late', 'result'):
                continue
            try:
                d0 = date.fromisoformat(dt)
            except ValueError:
                continue
            if d0 < today:
                notes.append(f'Deadline `{eid}` · {kind} · {d0:%d %b %Y} ({status}) has passed — confirm what actually happened.')
            elif d0 <= today + timedelta(days=14):
                notes.append(f'Deadline `{eid}` · {kind} · {d0:%d %b %Y} is within 14 days and still {status}.')
    return notes, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--state', default='.watch/state.json')
    ap.add_argument('--report', default='.watch/report.md')
    ap.add_argument('--sources', default=os.path.join(ROOT, 'app', 'data', 'exam_sources.json'))
    ap.add_argument('--today', default=None, help='override today (YYYY-MM-DD) for testing')
    ap.add_argument('--offline', action='store_true', help='skip fetching (internal checks only)')
    a = ap.parse_args()
    today = date.fromisoformat(a.today) if a.today else date.today()

    with open(a.sources, encoding='utf-8') as fh:
        sources = json.load(fh)['sources']
    state = {}
    first_run = not os.path.exists(a.state)
    if not first_run:
        try:
            with open(a.state, encoding='utf-8') as fh:
                state = json.load(fh)
        except (OSError, ValueError):
            first_run = True

    changes, errors, new_state = ([], [], state) if a.offline else check_sources(sources, state)
    notes, _ = internal_checks(today)

    lines = [f'# Exam schedule review — {today:%d %b %Y}', '',
             'Automated daily check of official pages against `/exam-schedule`. **Nothing was changed on the site.** '
             'Review each item, update `college-predictor/app/services/exam_page.py` only from an official announcement, '
             'and keep the status honest (Confirmed / Tentative / Expected).', '']
    if changes:
        lines += ['## Official pages that changed', '']
        for src, added, removed in changes:
            lines += [f"### {src['name']} — [{src['url']}]({src['url']})", f"Affects: {', '.join('`'+i+'`' for i in src.get('exams', []))}", '']
            lines += [f'- ➕ {s}' for s in added[:10]] + [f'- ➖ ~~{s}~~' for s in removed[:10]] + ['']
    if notes:
        lines += ['## Our data that needs a look', ''] + [f'- {n}' for n in notes] + ['']
    if errors:
        lines += ['## Sources that could not be read', '',
                  'Not a failure of the site — many official portals block automated requests. Check these by hand.', ''] + \
                 [f"- {s['name']} ([link]({s['url']})): {e}" for s, e in errors] + ['']
    has = bool(changes or notes)
    if first_run and not a.offline:
        lines += ['_First run: baseline recorded for the official pages; change alerts start from the next run._', '']
    if not has:
        lines += ['No changes detected today.', '']

    os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
    with open(a.report, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    if not a.offline:
        os.makedirs(os.path.dirname(os.path.abspath(a.state)), exist_ok=True)
        with open(a.state, 'w', encoding='utf-8') as fh:
            json.dump(new_state, fh, ensure_ascii=False, indent=1)
    out = os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out, 'a', encoding='utf-8') as fh:
            fh.write(f'has_findings={"true" if has else "false"}\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
