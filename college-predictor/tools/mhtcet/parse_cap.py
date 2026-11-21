"""Parse an official MHT CET CAP Round I cut-off PDF (State CET Cell) into JSON.

usage: python -I parse_cap.py <in.pdf> <out.json>
Output: {inst_code: {"name", "status", "hu", "branches": {branch_code: {"name", "levels": {level: {category: [rank, percentile]}}}}}}
level is one of S (State Level), HH (Home Univ seats to Home Univ candidates), HO (Home Univ seats to Other candidates), OH (Other than Home Univ seats to Other... as printed), O.
"""
import json
import re
import sys

import pymupdf

INST = re.compile(r'^(\d{4,5}) - (.+)$')
BR = re.compile(r'^(\d{9,10})([A-Z]{0,3}) - (.+)$')
STATUS = re.compile(r'^Status:\s*(.+?)(?:\s+Home University\s*:\s*(.+))?$')
PCT = re.compile(r'^\((\d{1,3}\.\d+)\)$')
RANK = re.compile(r'^\d{1,7}$')
CODE = re.compile(r'^[A-Z][A-Z0-9]{1,}$')


def level_of(text):
    t = text.lower()
    if t.startswith('state level'):
        return 'S'
    if 'home university seats allotted to home university' in t:
        return 'HH'
    if 'home university seats allotted to other than home university' in t:
        return 'HO'
    if 'other than home university seats allotted to other than home university' in t:
        return 'OO'
    if 'other than home university seats allotted to home university' in t:
        return 'OH'
    return None


def lines_of(page):
    """Visual lines: words grouped by rounded baseline, sorted top to bottom, each line a list of (x0, x1, text)."""
    words = page.get_text('words')
    rows = {}
    for x0, y0, x1, y1, w, *_ in words:
        key = round((y0 + y1) / 2 / 2.0)  # 2pt buckets
        rows.setdefault(key, []).append((x0, x1, w))
    out = []
    for k in sorted(rows):
        ws = sorted(rows[k])
        out.append((k, ws, ' '.join(w for _a, _b, w in ws)))
    return out


def parse(path):
    doc = pymupdf.open(path)
    data = {}
    inst = br = None
    level = None
    cols = None          # [(xcenter, code)]
    stage_seen = False
    pending_status = False
    for page in doc:
        for _k, ws, text in lines_of(page):
            t = text.strip()
            m = INST.match(t)
            if m and not BR.match(t):
                inst = data.setdefault(m.group(1).zfill(5), {'name': m.group(2).strip(), 'status': None, 'hu': None, 'branches': {}})
                br = None; cols = None; level = None
                continue
            m = BR.match(t)
            if m and inst is not None:
                br = inst['branches'].setdefault(m.group(1).zfill(10) + m.group(2), {'name': m.group(3).strip(), 'levels': {}})
                cols = None; level = None
                continue
            if t == 'Status:':
                pending_status = True
                continue
            if pending_status:
                pending_status = False
                t2 = 'Status: ' + t
                m = STATUS.match(t2)
                if m and inst is not None:
                    inst['status'], inst['hu'] = m.group(1).strip(), (m.group(2) or '').strip()
                    continue
            m = STATUS.match(t)
            if m and inst is not None:
                inst['status'], inst['hu'] = m.group(1).strip(), (m.group(2) or '').strip()
                continue
            lv = level_of(t)
            if lv:
                level = lv; cols = None
                continue
            if t == 'Stage':
                continue
            codes = [w for _a, _b, w in ws if w != 'Stage' and CODE.match(w)]
            if br is not None and len(codes) >= 1 and len(codes) == len([w for _a, _b, w in ws if w != 'Stage']) \
                    and any(k in c for c in codes for k in ('OPEN', 'TFWS', 'EWS', 'ORPHAN', 'MI')):
                cols = [((a + b) / 2, w) for a, b, w in ws if w != 'Stage' and CODE.match(w)]
                continue
            if cols is None or br is None or level is None:
                continue
            # value rows: ranks and (percentiles); a row beginning with a stage label I / II / III ...
            toks = ws
            if toks and toks[0][2] in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII'):
                stage_label = toks[0][2]
                stage_seen = stage_label == 'I'
                toks = toks[1:]
            for a, b, w in toks:
                xc = (a + b) / 2
                col = min(cols, key=lambda c: abs(c[0] - xc))
                if abs(col[0] - xc) > 40:
                    continue
                cell = br['levels'].setdefault(level, {}).setdefault(col[1], [None, None])
                pm = PCT.match(w)
                if pm:
                    if cell[1] is None:
                        cell[1] = float(pm.group(1))
                elif RANK.match(w):
                    if cell[0] is None:
                        cell[0] = int(w)
    return data


if __name__ == '__main__':
    d = parse(sys.argv[1])
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False)
    nb = sum(len(v['branches']) for v in d.values())
    print(sys.argv[1], 'institutes', len(d), 'branches', nb)
