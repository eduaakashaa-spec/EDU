"""Extract the NIFT 2023 GAT papers (text with the key printed under each question) into raw JSON.

Usage: python tools/nift/extract_2023.py <folder of txt dumps> <out.json>
The txt dumps are one file per PDF, pages joined with <<<PAGE n>>> markers.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

PROG = {'bdes': 'B.Des', 'bftech': 'B.F.Tech', 'mdes': 'M.Des', 'mfm': 'M.F.M', 'mftech': 'M.F.Tech'}


def clean(s):
    s = s.replace(' ', ' ').replace('�', "'")
    return re.sub(r'\s+', ' ', s).strip()


def parse(path):
    txt = open(path, encoding='utf-8').read()
    txt = re.sub(r'<<<PAGE \d+>>>\n', '', txt)
    txt = re.sub(r'^www\.prepp\.in\s*$', '', txt, flags=re.M)
    parts = re.split(r'^Q(\d+)\.\s?', txt, flags=re.M)
    out = []
    for i in range(1, len(parts) - 1, 2):
        n, body = int(parts[i]), parts[i + 1]
        pre, _, post = body.partition('Answer of above question:')
        lines = [l for l in pre.split('\n') if l.strip()]
        spaced = [l for l in lines if l.startswith(' ')]
        if len(spaced) >= 4 and all(l.startswith(' ') for l in lines[-len(spaced):]):
            opts, stem = [clean(l) for l in spaced], lines[:len(lines) - len(spaced)]
        else:
            opts, stem = [clean(l) for l in lines[-4:]], lines[:-4]
        ans = clean(' '.join(l for l in post.split('\n') if l.strip()))
        out.append({'n': n, 'stem': stem, 'opts': opts, 'ans': ans})
    return out


def main(src, dst):
    res = []
    for f in sorted(glob.glob(os.path.join(src, 'nift-2023-*-gat-question-paper*.txt'))):
        prog = PROG[re.search(r'nift-2023-([a-z]+)-gat', os.path.basename(f)).group(1)]
        for q in parse(f):
            res.append({'year': 2023, 'prog': prog, 'n': q['n'], 'stem': clean(' '.join(q['stem'])), 'opts': q['opts'], 'ans_text': q['ans']})
    json.dump(res, open(dst, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    ok = [q for q in res if any(o.lower() == q['ans_text'].lower() for o in q['opts'])]
    print(len(res), 'questions;', len(ok), 'answer matches an option;', dict(Counter(q['prog'] for q in res)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
