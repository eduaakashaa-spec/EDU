"""Public /exam-schedule page: statuses, filters, calendar downloads, no stale domain.
Run from college-predictor/:  python tests/test_exam_schedule_page.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.update(DATABASE_URL='sqlite:///:memory:', SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.services import exam_page

app = create_app()
c = app.test_client()

r = c.get('/exam-schedule')
assert r.status_code == 200
t = r.get_data(as_text=True)
assert 'India Entrance Exam Schedule' in t and '{%' not in t and 'eduaakashaa.in' not in t
for label in ('Confirmed', 'Tentative', 'Expected'):
    assert f'xs-st {label}' in t
st = exam_page.counts()
assert st['total'] == sum(len(x['exams']) for x in exam_page.CATEGORIES) and f'<b>{st["total"]}</b>' in t
for key, _ in exam_page.FILTERS:
    assert f'data-f="{key}"' in t
    if key != 'all':
        assert f'data-cat="{key}"' in t                                   # every filter has a section to show

# facts that were corrected against official sources must be on the page
assert 'Sunday 29 Nov 2026' in t and '23–24 Nov' not in t                  # CAT: IIM Indore, not 23–24 Nov
assert 'Sunday 17 Jan 2027' in t and '18 Jan 2027' not in t                # UCEED / CEED
assert 'Sunday 6 Dec 2026' in t                                            # CLAT
assert '20 Dec 2026' in t and 'KVPY' not in t and 'DSAT' not in t and 'ISAT' not in t
assert 'UPSEE' in t and 'no separate UPSEE' in t

# every exam row: unique id, valid status, valid ISO dates, and a working calendar link when dated
ids = set()
for _cat, row in exam_page.all_exams():
    id_, name, badge, when, status, desc, start, end, note = row
    assert id_ not in ids
    ids.add(id_)
    assert status in ('Confirmed', 'Tentative', 'Expected')
    if start:
        assert end and start <= end
        ics = c.get(f'/exam-schedule/{id_}.ics')
        assert ics.status_code == 200 and ics.mimetype == 'text/calendar', id_
        b = ics.data.decode().replace(chr(13) + chr(10) + ' ', '')     # RFC 5545 line unfolding
        n_ms = len([m for m in exam_page.deadlines_for(id_) if m['d']])
        assert b.count('BEGIN:VEVENT') == 1 + n_ms and 'www.eduaakashaa.com' in b and 'eduaakashaa.in' not in b      # exam + its dated deadlines
        if status == 'Expected':
            assert 'EXPECTED WINDOW ONLY' in b and 'TENTATIVE' in b       # never presented as a fixed exam day
        if status == 'Confirmed':
            assert 'STATUS:CONFIRMED' in b
    else:
        assert f'/exam-schedule/{id_}.ics' not in t                        # undated rows have no calendar button
assert c.get('/exam-schedule/does-not-exist.ics').status_code == 404

allics = c.get('/exam-schedule.ics')
body = allics.data.decode()
assert allics.status_code == 200 and body.startswith('BEGIN:VCALENDAR') and body.count('BEGIN:VEVENT') == len(exam_page.all_events())
assert 'DTSTART;VALUE=DATE:20270117' in body and 'DTSTART;VALUE=DATE:20261129' in body and 'DTSTART;VALUE=DATE:20270206' in body
assert 'attachment' in allics.headers['Content-Disposition']

# internal links on the page resolve
import re
for href in sorted(set(re.findall(r'href="(/[^"#]*)"', t))):
    if href.startswith('/static') or href.endswith('.ics'):
        continue
    assert c.get(href).status_code in (200, 301, 302, 403), href

# views: one JSON dataset drives Gantt / by-month / calendar; every id the script needs exists
import json
blob = re.search(r'<script type="application/json" id="xs-data">(.*?)</script>', t, re.S).group(1)
rows = json.loads(blob.replace('\u003c', '<').replace('\u003e', '>').replace('\u0026', '&').replace('\u0027', "'"))
assert len(rows) == st['total'] and all(r['status'] in ('Confirmed', 'Tentative', 'Expected') for r in rows)
assert any(r['id'] == 'uceed' and r['start'] == '2027-01-17' for r in rows)
for v in ('cards', 'gantt', 'months', 'calendar'):
    assert f'data-view="{v}"' in t and f'id="v-{v}"' in t
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static/js/exam_schedule.js'), encoding='utf-8').read()
missing = [i for i in sorted(set(re.findall(r"\$\('#([A-Za-z0-9_-]+)'\)", js))) if f'id="{i}"' not in t and i not in ('card-' + 'x',)]
assert not [m for m in missing if not m.startswith('card-')], missing
assert c.get('/static/js/exam_schedule.js').status_code == 200 and c.get('/static/css/exam_schedule.css').status_code == 200

# deadlines: milestones are well-formed, ordered, and carried by the page, the JSON, the cards and the .ics downloads
from datetime import date as _d
ids_all = {r[0] for _c, r in exam_page.all_exams()}
assert set(exam_page.DEADLINES) <= ids_all
for eid, ms in exam_page.DEADLINES.items():
    for kind, d, status, _n in ms:
        assert kind in exam_page.KIND_LABEL and status in ('Confirmed', 'Tentative', 'Expected')
        assert d is None or _d.fromisoformat(d)
    by = {k: d for k, d, _s2, _n in ms if d}
    if 'open' in by and 'close' in by:
        assert by['open'] <= by['close'], eid
    if 'close' in by and 'late' in by:
        assert by['close'] < by['late'], eid
    if 'result' in by and 'exam' not in by:
        row = exam_page.find(eid)
        assert row and (row[7] is None or by['result'] >= row[7] or eid == 'cat'), eid          # a result never precedes its exam
# the facts the user asked for
u = {k: d for k, d, _s2, _n in exam_page.DEADLINES['uceed'] if d}
assert u['open'] == '2026-10-01' and u['close'] == '2026-10-31' and u['late'] == '2026-11-06' and u['result'] == '2027-03-06'
assert {k: d for k, d, _s2, _n in exam_page.DEADLINES['nid-prelims']}['close'] == '2026-11-30'
assert {k: d for k, d, _s2, _n in exam_page.DEADLINES['slat']}['close'] == '2026-12-04'
assert 'data-a="open"' in t and 'Late-fee window' in t and 'Applications:' in t and 'xs-next' in t and 'xs-deadlines' in t
assert all('ms' in r for r in rows) and any(r['ms'] for r in rows)
assert 'Last date with late fee' in t and 'Applications close' in t
dics = c.get('/exam-schedule/deadlines.ics')
db_ = dics.data.decode().replace(chr(13) + chr(10) + ' ', '')
assert dics.status_code == 200 and db_.count('BEGIN:VEVENT') == len(exam_page.milestone_events()) > 30
assert 'Late-fee' in db_ or 'late fee' in db_.lower()
assert 'DTSTART;VALUE=DATE:20261106' in db_ and 'DTSTART;VALUE=DATE:20270306' in db_      # UCEED late-fee date and result
assert any('EXPECTED' in ev for ev in db_.split('BEGIN:VEVENT'))                          # expected dates are flagged in the event text
js2 = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static/js/exam_schedule.js'), encoding='utf-8').read()
assert 'Expected' in js2 and 'never' in js2.lower()                                      # the script documents that expected dates don't open applications

print('exam-schedule page checks passed')
