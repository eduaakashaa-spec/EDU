"""Build app/data/nift/bank.json and analysis.json from the extracted NIFT questions and the independent-solve annotations.

Usage: python tools/nift/build_bank.py <work folder>
The work folder holds cand.json (extracted questions with the paper's key) and blind/out_c*.json (one annotation per question made by an independent solve
without sight of the key: status, answer, sec, topic, why, fix). A question enters the bank only when the independent answer equals the paper's key.
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'app', 'data', 'nift')
SENT = re.compile(r'(?<=[.!?”"\'])\s+(?=[A-Z“"])')
PASSAGE_WORDS = re.compile(r'passage|paragraph|author|according to the|the writer', re.I)


def read(path):
    b = open(path, 'rb').read()
    try:
        return json.loads(b.decode('utf-8'))
    except UnicodeDecodeError:
        return json.loads(b.decode('cp1252', errors='replace'))


def main(work):
    cand = {q['id']: q for q in json.load(open(os.path.join(work, 'cand.json'), encoding='utf-8'))}
    ann = {}
    for f in sorted(glob.glob(os.path.join(work, 'blind', 'out_c*.json'))):
        for r in read(f):
            ann[r['id']] = r
    bank, tally = [], Counter()
    for i, r in ann.items():
        c = cand[i]
        if r['status'] != 'ok':
            tally['unsure'] += 1
            continue
        if r['answer'] != c['key']:
            tally['key differs'] += 1
            continue
        stem, opts = c['stem'], c['opts']
        fx = r.get('fix')
        if isinstance(fx, dict) and fx.get('stem') and len(fx.get('opts', [])) == 4:
            stem, opts = fx['stem'], fx['opts']
        if len({o.lower() for o in opts}) < 4:
            tally['duplicate options'] += 1
            continue
        ctx = c['ctx']
        if r['sec'] == 'CMP' and not ctx and len(stem) <= 350:
            tally['passage missing'] += 1
            continue
        if r['sec'] == 'CMP' and not ctx and len(stem) > 350:
            m = re.search(r'\s*Directions?\s*:\s*(?:Read|Study|Go through)[^:]{0,100}?(?:below|following)[.:]?\s*', stem, re.I)
            if m and m.start() > 8 and len(stem[m.end():]) > 150:
                stem, ctx = stem[:m.start()].strip(), stem[m.end():].strip()
            else:
                parts = SENT.split(stem)
                if len(parts) >= 3 and len(' '.join(parts[:-1])) > 200:
                    stem, ctx = parts[-1], ' '.join(parts[:-1])
        src = [[c['year'], c['prog'], c['n']]]
        for a in c['also']:
            m = re.match(r'(\d{4}) (\S+) Q(\d+)', a)
            src.append([int(m.group(1)), m.group(2), int(m.group(3))])
        bank.append({'id': 'T' + i[1:], 'sec': r['sec'], 'topic': r['topic'].strip(), 'q': stem, 'ctx': ctx, 'opts': opts, 'ans': 'ABCD'.index(c['key']), 'why': r['why'].strip(), 'src': src})
    txt = json.dumps(bank, ensure_ascii=False)
    assert not re.search(r'prepp|collegedunia|careers360|shiksha', txt, re.I)
    os.makedirs(OUT, exist_ok=True)
    json.dump(bank, open(os.path.join(OUT, 'bank.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(bank), 'in bank;', dict(tally), dict(Counter(b['sec'] for b in bank)))

    # topic and section mix over every question read from the papers (tagged by the independent solve), by year for B.Des
    by_year, topics = defaultdict(Counter), defaultdict(Counter)
    for i, r in ann.items():
        c = cand[i]
        if r.get('sec') not in ('QA', 'ENG', 'CMP', 'ANA', 'GK'):
            continue
        by_year[(c['year'], c['prog'])][r['sec']] += 1
        topics[r['sec']][r['topic'].strip().title()] += 1
    mix = [{'year': y, 'prog': p, **dict(cn), 'n': sum(cn.values())} for (y, p), cn in sorted(by_year.items())]
    top = {s: [{'topic': t, 'n': n} for t, n in cn.most_common(8)] for s, cn in topics.items()}
    json.dump({'mix': mix, 'topics': top, 'read': sum(sum(v.values()) for v in by_year.values())}, open(os.path.join(OUT, 'analysis.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('analysis written;', len(mix), 'paper rows')


if __name__ == '__main__':
    main(sys.argv[1])
