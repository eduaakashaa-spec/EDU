"""Extract the NIFT 2016-2022 GAT papers (numbered questions, separate answer-key page) into raw JSON.

Usage: python tools/nift/extract_old.py <folder of txt dumps> <out.json>
Papers before 2022 mark options a) b) c) d) or (1) (2) (3) (4); the 2022 papers print four bare option lines
and end each question with "(1 mark, negative marking)". Keys list "Qn  letter" pairs.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

PROG = {'bdes': 'B.Des', 'bftech': 'B.F.Tech', 'mdes': 'M.Des', 'mfm': 'M.F.M', 'mftech': 'M.F.Tech'}
OPT = re.compile(r'^\s*\(?([a-dA-D1-4])[\)\.]\s+(\S.*)$')
NOISE = re.compile(r'^(Page \d+|www\.prepp\.in|\(1 mark.*|<<<PAGE.*)$')


def clean(s):
    s = s.replace(' ', ' ').replace('�', "'")
    return re.sub(r'\s+', ' ', s).strip()


def read_lines(path):
    out = []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        ln = ln.rstrip()
        if ln.strip() and not NOISE.match(ln.strip()):
            out.append(ln)
    return out


def parse_marked(path):
    """Papers with a) b) c) d) / (1)..(4) options."""
    out, cur, nxt, ctx, trail = [], None, 1, '', []
    for ln in read_lines(path):
        m = re.match(r'^\s*(\d+)\.\s*(.*)$', ln)
        if m and int(m.group(1)) == nxt:
            if trail and len(' '.join(trail)) > 250:
                ctx = clean(' '.join(trail))
            trail = []
            cur = {'n': nxt, 'stem': [m.group(2)], 'opts': [], 'ctx': ctx}
            out.append(cur)
            nxt += 1
            continue
        if cur is None:
            continue
        o = OPT.match(ln)
        if o and len(cur['opts']) < 4:
            cur['opts'].append(clean(o.group(2)))
        elif len(cur['opts']) == 0:
            cur['stem'].append(ln)
        elif len(cur['opts']) < 4:
            cur['opts'][-1] += ' ' + clean(ln)
        else:
            trail.append(clean(ln))
    return out


def parse_bare(path):
    """2022 style: stem, then exactly four option lines, then the marks note (already stripped)."""
    out, cur, nxt = [], None, 1
    for ln in read_lines(path):
        m = re.match(r'^\s*(\d+)\.\s*(.*)$', ln)
        if m and int(m.group(1)) == nxt:
            cur = {'n': nxt, 'lines': [m.group(2)] if m.group(2).strip() else [], 'ctx': ''}
            out.append(cur)
            nxt += 1
        elif cur is not None:
            cur['lines'].append(ln)
    res = []
    for q in out:
        ls = [clean(l) for l in q['lines'] if clean(l)]
        res.append({'n': q['n'], 'stem': ls[:-4], 'opts': ls[-4:] if len(ls) >= 4 else ls, 'ctx': ''})
    return res


def read_key(path):
    t = open(path, encoding='utf-8').read()
    pairs = re.findall(r'Q(\d+)\s+([a-dA-D1-4])\b', t)
    return {int(n): ('ABCD'[int(l) - 1] if l.isdigit() else l.upper()) for n, l in pairs}


def main(src, dst):
    res = []
    keys = {}
    for f in glob.glob(os.path.join(src, 'nift-*answer-key*.txt')):
        b = os.path.basename(f)
        y = int(re.search(r'nift-(\d{4})', b).group(1))
        p = re.search(r'nift-\d{4}-([a-z]+)-', b).group(1)
        keys[(y, p)] = read_key(f)
    for f in sorted(glob.glob(os.path.join(src, 'nift-*-gat-question-paper*.txt'))):
        b = os.path.basename(f)
        y = int(re.search(r'nift-(\d{4})', b).group(1))
        if y not in (2016, 2017, 2018, 2020, 2021, 2022):
            continue
        p = re.search(r'nift-\d{4}-([a-z]+)-gat', b).group(1)
        key = keys.get((y, p), {})
        qs = parse_bare(f) if y == 2022 else parse_marked(f)
        for q in qs:
            stem = clean(' '.join(q['stem']) if isinstance(q['stem'], list) else q['stem'])
            res.append({'year': y, 'prog': PROG[p], 'n': q['n'], 'stem': stem, 'ctx': q.get('ctx', ''), 'opts': q['opts'], 'key': key.get(q['n'])})
    json.dump(res, open(dst, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    full = [r for r in res if len(r['opts']) == 4 and r['key']]
    print(len(res), 'questions;', len(full), 'with 4 options and a key;', dict(Counter((r['year'], r['prog']) for r in res)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
