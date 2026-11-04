"""Read an official NEET answer key (text PDF) into {question number: set of accepted option numbers}.

The keys come in several layouts (a Q.No/Answer pair per line, four interleaved columns, "1.\n(3)", a pipe table in 2023); all reduce to a stream of
(number, answer) pairs, so one reader covers them. An answer such as "1,3" (two options accepted) is kept as a set; "Dropped" questions are left out.
"""
import re

import pymupdf


def read(pdf):
    t = '\n'.join(p.get_text() for p in pymupdf.open(pdf))
    if '|QNO' in t.replace(' ', ''):
        return {int(a): {int(b)} for a, b in re.findall(r'\|\s*(\d{1,3})\s*\|\s*([1-4])\s*', t)}
    t = re.sub(r'(?is)^.*?(?:answer|key)\s*\n', '', t, count=0) if False else t
    toks = [x.strip() for x in t.replace('*', '').split('\n') if x.strip()]
    out, i = {}, 0
    q_pat = re.compile(r'^(\d{1,3})\.?$')
    a_pat = re.compile(r'^\(?([1-4](?:\s*,\s*[1-4])*)\)?$')
    while i < len(toks) - 1:
        m, a = q_pat.match(toks[i]), a_pat.match(toks[i + 1])
        if m and a and int(m.group(1)) not in out:
            out[int(m.group(1))] = {int(x) for x in re.split(r'\s*,\s*', a.group(1))}
            i += 2
        else:
            i += 1
    return out


if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        k = read(f)
        miss = [n for n in range(1, max(k) + 1) if n not in k]
        print(f.split('/')[-1][:60], len(k), 'max', max(k), 'missing', miss[:10], 'multi', [n for n, v in k.items() if len(v) > 1])
