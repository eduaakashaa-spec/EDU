"""Exam-date watcher: snippet extraction, change detection, internal due-checks, report. Run: python tests/test_exam_watch.py"""
import json
import os
import sys
import tempfile
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
os.environ.update(DATABASE_URL='sqlite:///' + os.path.join(tempfile.mkdtemp(), 'w.db'), SECRET_KEY='t')
import exam_watch as ew

page1 = '<html><script>var x="15 Jan 2027"</script><p>Registration opens on 25 October 2026. Welcome to our site.</p><p>The examination will be held on 22 Jan 2027.</p></html>'
page2 = page1.replace('22 Jan 2027', '24 Jan 2027')
text = ew.clean_text(page1)
assert 'var x' not in text
sn = ew.snippets(text, ['registration', 'examination'])
assert len(sn) == 2 and any('25 October 2026' in s for s in sn) and not any('Welcome' in s for s in sn)
assert ew.snippets(text, ['bulletin']) == []

src = [{'id': 'a', 'name': 'A', 'url': 'http://x', 'exams': ['e1'], 'keywords': ['registration', 'examination']}]
cur = {'html': page1}
ew.fetch = lambda url: cur['html']
ch, er, st = ew.check_sources(src, {})
assert ch == [] and er == [] and 'a' in st                       # baseline: no alert
ch, er, st2 = ew.check_sources(src, st)
assert ch == []                                                   # unchanged
cur['html'] = page2
ch, er, st3 = ew.check_sources(src, st2)
assert len(ch) == 1 and any('24 Jan 2027' in s for s in ch[0][1]) and any('22 Jan 2027' in s for s in ch[0][2])


def boom(url):
    raise RuntimeError('403')


ew.fetch = boom
ch, er, st4 = ew.check_sources(src, st3)
assert ch == [] and len(er) == 1 and st4['a'] == st3['a']        # unreachable: reported, old snapshot kept

# internal checks against the real data
notes, ok = ew.internal_checks(date(2027, 1, 20))
assert ok and any('verified' in n for n in notes) and any('jee-main' in n for n in notes)
quiet, ok = ew.internal_checks(date(2026, 10, 17))
assert ok and not any('verified' in n for n in quiet)

# end to end (offline) writes a report and sets the workflow output
d = tempfile.mkdtemp()
out = os.path.join(d, 'out.txt')
os.environ['GITHUB_OUTPUT'] = out
sys.argv = ['x', '--offline', '--today', '2027-01-20', '--state', os.path.join(d, 's.json'), '--report', os.path.join(d, 'r.md')]
ew.main()
assert 'has_findings=true' in open(out).read() and 'Nothing was changed on the site' in open(os.path.join(d, 'r.md'), encoding='utf-8').read()
# every source in the config is well-formed and points at known exam ids
cfg = json.load(open(os.path.join(ROOT, 'app/data/exam_sources.json'), encoding='utf-8'))['sources']
from app.services import exam_page as ep
ids = {e[0] for c in ep.CATEGORIES for e in c['exams']}
assert all(s['url'].startswith('https://') and s['keywords'] for s in cfg) and all(set(s['exams']) <= ids for s in cfg), [s['id'] for s in cfg if not set(s['exams']) <= ids]
print('exam watch checks passed')
