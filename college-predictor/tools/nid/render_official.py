"""Cut the objective questions (picture, stem and options) out of NID's own sample papers into WebP images.
Papers (page ranges are 1-based, inclusive): B.Des DAT Prelims sample 2025 (pages 2-8) and 2024 (21-26); M.Des CDAT Paper 1 sample 2025 (2-5) and 2024 (7-10).
Writes app/static/img/nid/<code>/q<NN>.webp and app/data/nid/official.json (no answers: those are added by official_keys.json).
Usage: python tools/nid/render_official.py <folder with SamplePaper_DATPrelims_BDes.pdf and ..._MDes.pdf>"""
import io
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
import fitz  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
ZOOM = 2.0
PAPERS = [  # code, title, programme, file, first page, last page, stop-after question, marks rule: question number -> marks
    ('BDES25', 'B.Des DAT Prelims sample paper 2025', 'B.Des', 'SamplePaper_DATPrelims_BDes.pdf', 2, 8, 20, lambda n: 1 if n <= 15 else 2),
    ('BDES24', 'B.Des DAT Prelims sample paper 2024', 'B.Des', 'SamplePaper_DATPrelims_BDes.pdf', 21, 26, 19, lambda n: 1 if n <= 13 else 2),
    ('MDES25', 'M.Des CDAT Paper 1 sample 2025', 'M.Des', 'SamplePaper_DATPrelims_MDes.pdf', 2, 5, 18, lambda n: 1 if n <= 16 else 2),
    ('MDES24', 'M.Des CDAT Paper 1 sample 2024', 'M.Des', 'SamplePaper_DATPrelims_MDes.pdf', 7, 10, 15, lambda n: 1 if n <= 10 else 2),
]


def trim(img, pad=8):
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    box = ImageChops.difference(img, bg).getbbox()
    if not box:
        return img
    x0, y0, x1, y1 = box
    return img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))


def main(src):
    out = []
    for code, title, prog, fname, p0, p1, last, mk in PAPERS:
        doc = fitz.open(os.path.join(src, fname))
        d = os.path.join(APP, 'static', 'img', 'nid', code.lower())
        os.makedirs(d, exist_ok=True)
        marks = []
        for pi in range(p0 - 1, p1):
            for w in doc[pi].get_text('words'):
                m = re.fullmatch(r'Q(\d+)\)', w[4])
                if m:
                    marks.append((int(m.group(1)), pi, w[1]))
        marks.sort(key=lambda x: (x[1], x[2]))
        marks = [m for m in marks if m[0] <= last]
        for k, (n, pi, y) in enumerate(marks):
            parts = []
            page = doc[pi]
            bottom = page.rect.height - 28
            nxt = marks[k + 1] if k + 1 < len(marks) else None
            y1 = nxt[2] - 3 if nxt and nxt[1] == pi else bottom
            rects = [(pi, y - 4, y1)]
            if nxt and nxt[1] > pi:                     # question runs on to the following page(s) before the next one starts
                for pj in range(pi + 1, nxt[1]):
                    rects.append((pj, 30, doc[pj].rect.height - 28))
                top_of_next = [w[1] for w in doc[nxt[1]].get_text('words') if w[1] < nxt[2] - 3 and w[1] > 30]
                if nxt[2] > 60 and (top_of_next or True) and nxt[2] - 30 > 25:
                    rects.append((nxt[1], 30, nxt[2] - 3))
            for pj, a, b in rects:
                pix = doc[pj].get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=fitz.Rect(0, a, doc[pj].rect.width, b), alpha=False)
                parts.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'))
            w_ = max(p.width for p in parts)
            im = Image.new('RGB', (w_, sum(p.height for p in parts)), (255, 255, 255))
            yy = 0
            for p in parts:
                im.paste(p, (0, yy))
                yy += p.height
            im = trim(im)
            fn = 'q%02d.webp' % n
            im.save(os.path.join(d, fn), 'WEBP', quality=78, method=6)
            out.append(dict(paper=code, n=n, marks=mk(n), img='img/nid/%s/%s' % (code.lower(), fn), page=pi + 1))
        print(code, len(marks), 'questions')
    meta = [dict(code=c, title=t, programme=pr, questions=sum(1 for o in out if o['paper'] == c), marks=sum(o['marks'] for o in out if o['paper'] == c)) for c, t, pr, f, a, b, l, m in PAPERS]
    json.dump(dict(papers=meta, questions=out), open(os.path.join(APP, 'data', 'nid', 'official.json'), 'w', encoding='utf-8'), indent=1)
    print(meta)


if __name__ == '__main__':
    main(sys.argv[1])
