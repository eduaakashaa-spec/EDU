"""Read the answer keys of the BITSAT papers (PDFs in Documents/BITSAT_Extraction/AnswerKeys) into keys.json: {year: {n: 'A'..'D'}}.

Three layouts: 2015-2020 '12. (b) explanation'; 2021-2023 Prepp '... Answer: C' once per question, in question order; 2024 'N. question ... Ans. D'.
"""
import glob
import json
import os
import re
import sys

import fitz

SRC = 'C:/Users/KALIL/Documents/BITSAT_Extraction/AnswerKeys/'


def text(f):
    return '\n'.join(p.get_text() for p in fitz.open(f))


def old(t):
    out = {}
    for n, a in re.findall(r'(?m)^\s*(\d{1,3})\.\s*\(([a-dA-D])\)', t):
        out.setdefault(int(n), a.upper())
    return out


def prepp(t):
    ans = re.findall(r'Answer:\s*\(?([A-D])', t)
    return {i + 1: a for i, a in enumerate(ans)}


def ans_dot(t):
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'(?m)^\s*(\d{1,3})\.\s+\S', t)]
    out, cur = {}, 1
    chain = []
    for pos, n in marks:                      # the chain 1, 2, 3 ... of question starts
        if n == cur:
            chain.append((pos, n))
            cur += 1
    for k, (pos, n) in enumerate(chain):
        end = chain[k + 1][0] if k + 1 < len(chain) else len(t)
        m = re.search(r'Ans\.?\s*:?\s*\(?([A-D])\)?', t[pos:end])
        if m:
            out[n] = m.group(1)
    return out


if __name__ == '__main__':
    keys = {}
    for y in range(2015, 2025):
        f = glob.glob(SRC + 'BITSAT_AnswerKey_%d_*.pdf' % y)[0]
        t = text(f)
        keys[y] = (old if y <= 2020 else prepp if y <= 2023 else ans_dot)(t)
        print(y, len(keys[y]), 'answers; missing', [n for n in range(1, max(keys[y]) + 1) if n not in keys[y]][:12])
    json.dump(keys, open(sys.argv[1] if len(sys.argv) > 1 else 'keys.json', 'w'))
