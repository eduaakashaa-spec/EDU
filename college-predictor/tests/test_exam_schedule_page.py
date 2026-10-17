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

print('exam-schedule page checks passed')
