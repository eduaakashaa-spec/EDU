"""Which section (PHY, CHE, ENG, LR, MAT) each question of a BITSAT paper PDF belongs to, read from the section headings printed in the paper.

    python tools/bitsat/sections.py <pdf> <style num|q>      prints the question ranges per section
"""
import re
import sys

import fitz

sys.path.insert(0, __file__.rsplit('tools', 1)[0] + 'tools/bitsat') if False else None
import crop  # noqa: E402

LABELS = [('PHY', re.compile(r'PHYSICS', re.I)), ('CHE', re.compile(r'CHEMISTRY', re.I)), ('ENG', re.compile(r'ENGLISH', re.I)),
          ('LR', re.compile(r'LOGICAL', re.I)), ('MAT', re.compile(r'MATH', re.I))]


def of_paper(pdf, style):
    """-> {n: section code}; None when the paper carries no usable headings."""
    doc = fitz.open(pdf)
    ch = crop.markers(doc, style)
    heads = []
    for pi, page in enumerate(doc):
        w = page.rect.width
        for b in page.get_text('blocks'):
            first = b[4].strip().split('\n')[0] if b[4].strip() else ''
            if crop.HEAD.match(first) and len(first) < 60 and not first.upper().startswith('DIRECTION'):
                code = next((c for c, rx in LABELS if rx.search(first)), None)
                if code:
                    heads.append(((pi, 0 if b[0] < w * 0.45 else 1, b[1]), code))
    heads.sort()
    out, cur = {}, None
    for n, pi, col, x, y in ch:
        for key, code in heads:
            if key <= (pi, col, y):
                cur = code
        out[n] = cur
    return out


def ranges(sec):
    out, last = [], None
    for n in sorted(sec):
        if sec[n] != last:
            out.append([sec[n], n, n])
            last = sec[n]
        else:
            out[-1][2] = n
    return out


if __name__ == '__main__':
    print(ranges(of_paper(sys.argv[1], sys.argv[2])))
