"""Build app/data/neet/bank.json and analysis.json from the transcribed and solved question chunks.

Usage: python tools/neet/build_bank.py <work folder with out/<year>_<chunk>.json> <folder with the answer-key PDFs>
Each chunk file holds questions read from the page images of one paper (booklet code per year below), with an independent solve. A question is kept only when
  * it is not a figure question (a picture would be needed),
  * the solve gave an option and it equals the option in the National Testing Agency's published key for that booklet code (a key with two accepted options, or no entry because the question was
    dropped, excludes the question),
  * it has four non-empty options and does not point at a figure the reader cannot see.
The same question asked in more than one year is kept once, with every source listed.
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keys  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'neet')
KEYFILE = {2018: 'neet-2018-answer-key-pdf-may-06-2018-aa-1761561302.pdf', 2019: 'neet-2019-paper-1-answer-key-pdf-may-05-2019-p5-1761558147.pdf',
           2020: 'neet-2020-answer-key-pdf-sep13-2020-e1-1760964574.pdf', 2021: 'neet-2021-answer-key-pdf-sep-12-2021-m1-1760962139.pdf',
           2022: 'neet-2022-answer-key-pdf-jul-17-2022-q1-1760959199.pdf', 2023: 'neet-2023-answer-key-pdf-may-07-2023-e1-1760947924.pdf',
           2024: 'neet-2024-paper-1-answer-key-pdf-may-5-2024-q5-1760946220.pdf',
           2025: 'NEET_2025_1_Question_Paper_and_Answer_Key_PDF_May_04_2025_48__9d74466e8441911833a7d7138bc5df65.pdf'}
CODE = {2018: 'AA', 2019: 'P5', 2020: 'E1', 2021: 'M1', 2022: 'Q1', 2023: 'E1', 2024: 'Q5', 2025: '48'}
SECS = ['PHY', 'CHEM', 'BOT', 'ZOO']
FIGURE_WORDS = re.compile(r'\b(figure|diagram|as shown|shown below|shown in|shown above|in the picture|given graph|following graph|graph given)\b', re.I)


def subject(n, per):
    return SECS[min(3, (n - 1) // per)]


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def topic_of(t):
    t = (t or 'Other').split(':')[0].split(' - ')[0].strip()
    return t[:60] if t else 'Other'


def main(work, kdir):
    tot_read = Counter()
    yearstat = {}
    items = []
    for y in sorted(KEYFILE):
        k = keys.read(os.path.join(kdir, KEYFILE[y]))
        size = max(k)
        per = size // 4
        files = sorted(glob.glob(os.path.join(work, 'out', '%d_*.json' % y)))
        seen, kept, fig, nokey, mismatch, unsure, bad = set(), 0, 0, 0, 0, 0, 0
        for f in files:
            for q in json.load(open(f, encoding='utf-8')):
                n = q.get('n')
                if not isinstance(n, int) or n in seen or not 1 <= n <= size:
                    continue
                seen.add(n)
                tot_read[y] += 1
                if q.get('fig'):
                    fig += 1
                    continue
                opts = [str(o).strip() for o in (q.get('opts') or [])]
                text = str(q.get('q') or '').strip()
                if len(opts) != 4 or len(set(opts)) != 4 or not all(opts) or len(text) < 12 or FIGURE_WORDS.search(text + ' ' + ' '.join(opts)):
                    bad += 1
                    continue
                a = q.get('ans')
                if not a:
                    unsure += 1
                    continue
                ks = k.get(n)
                if not ks or len(ks) != 1:
                    nokey += 1
                    continue
                if a not in ks:
                    mismatch += 1
                    continue
                kept += 1
                items.append({'sec': subject(n, per), 'topic': topic_of(q.get('topic')), 'q': text, 'opts': opts, 'ans': a - 1, 'why': str(q.get('why') or '').strip(), 'src': [[y, n]]})
        yearstat[y] = {'code': CODE[y], 'paper_questions': size, 'read': len(seen), 'figure': fig, 'unreadable': bad, 'unsure': unsure, 'no_single_key': nokey, 'key_differs': mismatch, 'kept': kept}
        print(y, yearstat[y])
    merged, by_text = [], {}
    for it in sorted(items, key=lambda r: (r['src'][0][0], r['src'][0][1])):
        key = (norm(it['q']), tuple(sorted(norm(o) for o in it['opts'])))
        if key in by_text:
            by_text[key]['src'] += it['src']
            continue
        by_text[key] = it
        merged.append(it)
    for i, it in enumerate(merged):
        it['id'] = 'N%04d' % i
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'bank.json'), 'w', encoding='utf-8') as f:
        json.dump([{k: it[k] for k in ('id', 'sec', 'topic', 'q', 'opts', 'ans', 'why', 'src')} for it in merged], f, ensure_ascii=False, separators=(',', ':'))
    secs = Counter(it['sec'] for it in merged)
    topics = defaultdict(Counter)
    for it in merged:
        topics[it['sec']][it['topic']] += len(it['src'])
    peryear = defaultdict(Counter)
    for it in merged:
        for y, _ in it['src']:
            peryear[y][it['sec']] += 1
    an = {'years': {str(y): {**v, 'by_sec': dict(peryear[y])} for y, v in yearstat.items()}, 'secs': dict(secs), 'questions': len(merged), 'read': sum(tot_read.values()),
          'repeated': sum(1 for it in merged if len(it['src']) > 1),
          'topics': {s: [[t, c] for t, c in topics[s].most_common(24)] for s in SECS}}
    with open(os.path.join(OUT, 'analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(an, f, ensure_ascii=False, indent=1)
    print('bank', len(merged), dict(secs), 'repeated across years', an['repeated'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
