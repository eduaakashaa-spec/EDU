"""Parse an IAT paper PDF (one question per page, layout used from 2023) into a JSON draft: text, options, and the embedded images by page.

Usage: python tools/iat/parse_key.py <pdf> <out.json> [img_dir]
The 2025 and 2026 "Key" PDFs state that option (a) is the correct answer in every question; the parser records that as answer 0.
"""
import json
import os
import re
import sys

import pypdf

SUBJ = ['Biology', 'Chemistry', 'Mathematics', 'Physics']


def main(pdf, out, img_dir=None):
    r = pypdf.PdfReader(pdf)
    pages = []
    for i, p in enumerate(r.pages):
        t = p.extract_text() or ''
        imgs = []
        try:
            for k, im in enumerate(p.images):
                imgs.append((k, im.name, im))
        except Exception:
            pass
        pages.append((i + 1, t, imgs))
    qs, subj, cur = [], None, None
    for pg, t, imgs in pages:
        lines = [x for x in t.split('\n')]
        head = lines[0].strip() if lines else ''
        if head in SUBJ:
            subj = head
            lines = lines[1:]
            t = '\n'.join(lines)
        m = re.match(r'\s*(\d+)\.\s*Question\s+(\d+)', t)
        if m:
            cur = dict(subj=subj, n=int(m.group(1)), pages=[pg], text=t, images=[])
            qs.append(cur)
        elif cur is not None and pg > 1 and t.strip() and not t.startswith('English Answer Key'):
            cur['pages'].append(pg)
            cur['text'] += '\n' + t
        if cur is not None and imgs and (m or cur['pages'][-1] == pg):
            for k, name, im in imgs:
                if img_dir:
                    os.makedirs(img_dir, exist_ok=True)
                    fn = 'p%02d_%s_%d%s' % (pg, subj[:3].lower(), cur['n'], '_%d' % k)
                    ext = os.path.splitext(name)[1] or '.png'
                    open(os.path.join(img_dir, fn + ext), 'wb').write(im.data)
                    cur['images'].append(dict(page=pg, file=fn + ext, w=getattr(im.image, 'width', 0) if hasattr(im, 'image') else 0))
                else:
                    cur['images'].append(dict(page=pg, name=name))
    json.dump(qs, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(qs), 'questions;', sum(1 for q in qs if q['images']), 'with images')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
