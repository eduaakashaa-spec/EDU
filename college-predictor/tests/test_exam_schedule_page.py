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
        assert b.count('BEGIN:VEVENT') == 1 and 'www.eduaakashaa.com' in b and 'eduaakashaa.in' not in b
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

print('exam-schedule page checks passed')
