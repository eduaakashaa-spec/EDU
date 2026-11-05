"""No UAE phone number, Dubai office or UAE address appears in the contact details of any page (EduAakashaA operates in India only).
Run from college-predictor/:  python tests/test_no_uae_contact.py"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD = [re.compile(r'\+971[ \d-]{6,}'), re.compile(r'UAE\s*:?\s*(<span>)?\+971'), re.compile(r'Dubai,\s*UAE'), re.compile(r'Coimbatore\s+and\s+Dubai'), re.compile(r'Coimbatore[^<]{0,20}[·&]\w*;?\s*Dubai')]
files = glob.glob(os.path.join(ROOT, 'app', 'templates', '**', '*.html'), recursive=True) + glob.glob(os.path.join(ROOT, 'app', 'data', 'pcm12', 'pages', '*.html')) + glob.glob(os.path.join(ROOT, 'app', 'data', 'gulf', '*.html'))
hits = []
for f in files:
    s = open(f, encoding='utf-8', errors='ignore').read()
    s = re.sub(r'data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+', '', s)                # embedded images are not text
    s = re.sub(r'"data":"[A-Za-z0-9+/=]{200,}"', '', s)
    for b in BAD:
        for m in b.finditer(s):
            ctx = s[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
            if 'testimonial' in f or 'Parent' in ctx:                               # a parent's location in a testimonial is not a contact detail
                continue
            hits.append((os.path.relpath(f, ROOT), ctx))
assert not hits, hits[:5]
# the four PCM pages keep the India contact details
for n in ('answer-lab', 'board-playbook', 'eligibility', 'thumb-rules'):
    s = open(os.path.join(ROOT, 'app', 'data', 'pcm12', 'pages', n + '.html'), encoding='utf-8').read()
    assert '+91-80157 22706' in s and 'Coimbatore, Tamil Nadu' in s, n
print('no UAE contact checks passed')
