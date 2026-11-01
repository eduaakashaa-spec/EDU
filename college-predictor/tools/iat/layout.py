"""Shared layout helper for the IAT renderers: split a question segment into the stem and the four option rectangles.

Every content box (word, picture or drawing such as a fraction bar) in the segment is assigned to the option marker whose line is nearest to the
box centre; boxes well above the first marker form the stem (only on the first page of the question). A layout check then refuses any split in which
an option does not contain its own marker line, options overlap, or the stem runs into the first option: such questions are left unshuffled.
"""
import fitz


def boxes(page, top, bottom, x_min, skip):
    out = []
    for w in page.get_text('words'):
        if w[3] < top or w[1] > bottom or w[0] < x_min - 4:
            continue
        if any(abs(w[0] - s[0]) < 0.5 and abs(w[1] - s[1]) < 0.5 for s in skip):
            continue
        out.append(fitz.Rect(w[:4]))
    try:
        for im in page.get_image_info():
            r = fitz.Rect(im['bbox'])
            if r.y1 >= top and r.y0 <= bottom and r.width > 2:
                out.append(r)
    except Exception:
        pass
    try:
        for dr in page.get_drawings():
            r = fitz.Rect(dr['rect'])
            if r.y1 >= top and r.y0 <= bottom and r.width < page.rect.width * 0.95 and r.x0 >= x_min - 4:
                out.append(r)
    except Exception:
        pass
    return [b for b in out if b.y1 > top and b.y0 < bottom]


def split(page, top, bottom, x_min, marks, right, first_page=True):
    """marks: list of fitz.Rect (marker word boxes) in order.
    Returns (stem_rect or None, [option rects], layout_ok)."""
    ys = [m.y0 + m.height / 2 for m in marks]
    skip = [(m.x0, m.y0) for m in marks]
    bs = boxes(page, top, bottom, x_min, skip)
    stem, opts = [], [[] for _ in marks]
    thr = ys[0] - 11 if first_page else -1e9
    for b in bs:
        c = b.y0 + b.height / 2
        if c < thr:
            stem.append(b)
            continue
        k = min(range(len(ys)), key=lambda i: abs(ys[i] - c))
        opts[k].append(b)

    def rect(lst, pad=2):
        if not lst:
            return None
        r = fitz.Rect(lst[0])
        for b in lst[1:]:
            r |= b
        return fitz.Rect(max(0, r.x0 - pad), max(top, r.y0 - pad), min(right, r.x1 + pad), min(bottom, r.y1 + pad))

    s_rect = rect(stem)
    o_rects = [rect(o) for o in opts]
    ok = all(o is not None for o in o_rects)
    if ok:
        for y, r in zip(ys, o_rects):
            if not (r.y0 - 1.5 <= y <= r.y1 + 1.5):
                ok = False
        for a, b in zip(o_rects, o_rects[1:]):
            if a.y1 > b.y0 + 3:
                ok = False
        if s_rect is not None and s_rect.y1 > ys[0] + 1:
            ok = False
    return s_rect, o_rects, ok
