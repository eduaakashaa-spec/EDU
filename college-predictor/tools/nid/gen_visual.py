"""Procedural visual and spatial questions for the NID mock centre. Every question is built by code, so the answer is computed, not typed:
odd one out, mirror image, rotation, paper fold and punch, 3 x 3 matrix, shape analogy, chiral odd one out, cube opposite faces, squares in a grid,
lines of symmetry, clock angle, colour-wheel relations.  Output: app/data/nid/visual.json
Run: python tools/nid/gen_visual.py"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'app', 'data', 'nid', 'visual.json')
INK, FILL, SOFT, ACC = '#0E3A8A', '#FF6B0A', '#DCE6FA', '#1F8B5C'
LETTERS = 'ABCD'


def svg(w, h, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">%s</svg>' % (w, h, w, h, body)


# ---- polyomino figures -------------------------------------------------------------------------------------------------------------------
def norm(cells):
    mx, my = min(x for x, y in cells), min(y for x, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def rot90(cells):                       # clockwise on screen (y down): (x, y) -> (-y, x)
    return norm({(-y, x) for x, y in cells})


def rot180(cells):
    return rot90(rot90(cells))


def mirror(cells):                      # left-right
    return norm({(-x, y) for x, y in cells})


def flipv(cells):                       # top-bottom
    return norm({(x, -y) for x, y in cells})


def variants(cells):
    out, c = [], norm(cells)
    for _ in range(4):
        out.append(c)
        c = rot90(c)
    return out


def chiral(cells):
    return norm(mirror(cells)) not in variants(cells)


def asym(cells):
    c = norm(cells)
    return len({v for v in variants(c)}) == 4 and norm(mirror(c)) not in variants(c) is False or len(set(variants(c))) >= 2


def fig(cells, size=100, col=INK, fill=SOFT, grid=None):
    cells = norm(cells)
    w = max(x for x, y in cells) + 1
    h = max(y for x, y in cells) + 1
    n = max(w, h, 3)
    u = (size - 16) / float(n)
    ox, oy = (size - u * w) / 2.0, (size - u * h) / 2.0
    body = ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/>' % (ox + x * u, oy + y * u, u, u, fill, col) for x, y in sorted(cells))
    return svg(size, size, body)


def random_poly(rng, size, box=4, need_chiral=True):
    while True:
        cells = {(rng.randrange(box), rng.randrange(box))}
        while len(cells) < size:
            x, y = rng.choice(sorted(cells))
            dx, dy = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nx, ny = x + dx, y + dy
            if 0 <= nx < box and 0 <= ny < box:
                cells.add((nx, ny))
        c = norm(cells)
        if max(x for x, y in c) >= 1 and max(y for x, y in c) >= 1 and len(set(variants(c))) == 4 and (not need_chiral or chiral(c)):
            return c


def place(rng, correct, wrong):
    opts = [correct] + list(wrong)
    order = list(range(len(opts)))
    rng.shuffle(order)
    return [opts[i] for i in order], order.index(0)


# ---- the generators ----------------------------------------------------------------------------------------------------------------------
def g_mirror(rng):
    c = random_poly(rng, rng.choice([5, 6]))
    cands = [mirror(c), flipv(c), rot90(c), rot180(c)]
    cands = [x for x in cands if x != mirror(c)] if False else cands
    right = mirror(c)
    wrong = [x for x in (flipv(c), rot180(c), c) if x != right]
    # flipv and rot180 are different figures from the mirror for a chiral shape; the original is shown 'moved' as a distractor
    wrong = [x for x in dict.fromkeys(wrong) if x != right][:3]
    if len(wrong) < 3:
        return None
    opts, a = place(rng, right, wrong)
    stem = svg(200, 110, '<g transform="translate(10,5)">%s</g><line x1="120" y1="8" x2="120" y2="102" stroke="#C23A3A" stroke-width="2" stroke-dasharray="5 4"/><text x="124" y="60" font-size="11" fill="#C23A3A">mirror</text>' % fig(c, 100).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100" role="img">', '<g>').replace('</svg>', '</g>'))
    return dict(sec='SPA', topic='Mirror image', level='B', marks=1, q='A vertical mirror stands on the right-hand side of the figure. Which option shows the figure as it appears in the mirror?', svg=stem, opts=[dict(svg=fig(o)) for o in opts], ans=a,
                why='A mirror on the right reverses left and right: the cell furthest to the left in the figure appears furthest to the right in the reflection, while heights stay the same. Options that turn the figure upside down or half a turn are not reflections in a vertical mirror.')


def g_rotation(rng):
    c = random_poly(rng, rng.choice([5, 6]))
    turn = rng.choice([('90 degrees clockwise', rot90), ('180 degrees', rot180), ('90 degrees anticlockwise', lambda z: rot90(rot180(z)))])
    right = turn[1](c)
    pool = [mirror(c), flipv(c), rot90(c), rot180(c), rot90(rot180(c)), mirror(right)]
    wrong = [x for x in dict.fromkeys(pool) if x != right and x != c][:3]
    if len(wrong) < 3:
        return None
    opts, a = place(rng, right, wrong)
    return dict(sec='SPA', topic='Rotation of a figure', level='B', marks=1, q='The figure is turned %s. Which option shows the result?' % turn[0], svg=fig(c, 110), opts=[dict(svg=fig(o)) for o in opts], ans=a,
                why='Turn the figure in your mind one quarter at a time and follow its longest arm: after %s it points the way shown in the correct option. The wrong options are reflections (which a turn can never produce) or turns through another angle.' % turn[0])


def g_chiral_odd(rng):
    c = random_poly(rng, rng.choice([5, 6]))
    rots = variants(c)
    rng.shuffle(rots)
    same = rots[:3]
    odd = mirror(c)
    if odd in variants(c):
        return None
    opts, a = place(rng, odd, same)
    return dict(sec='SPA', topic='Odd one out by reflection', level='BM', marks=2, q='Three of the figures are the same shape turned to different positions. One is its mirror image. Which is the odd one out?', opts=[dict(svg=fig(o)) for o in opts], ans=a,
                why='Turning a figure never changes which way it curls. Three options can be turned onto each other; the odd one curls the other way, so it is the mirror image.')


def g_analogy(rng):
    c = random_poly(rng, 5)
    c2 = random_poly(rng, 6)
    t = rng.choice([('turned a quarter clockwise', rot90), ('turned half a turn', rot180), ('reflected left to right', mirror), ('flipped upside down', flipv)])
    a1 = t[1](c)
    right = t[1](c2)
    pool = [rot90(c2), rot180(c2), mirror(c2), flipv(c2), c2]
    wrong = [x for x in dict.fromkeys(pool) if x != right][:3]
    if len(wrong) < 3 or a1 == c or right == c2:
        return None
    opts, a = place(rng, right, wrong)
    stem = svg(330, 100, '<g transform="translate(0,0)">%s</g><text x="104" y="56" font-size="22" fill="#445">&#8594;</text><g transform="translate(120,0)">%s</g><text x="224" y="56" font-size="16" fill="#445">::</text><g transform="translate(240,0)">%s</g><text x="300" y="56" font-size="22" fill="#445">?</text>' % tuple(
        fig(x, 90).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90" role="img">', '<g>').replace('</svg>', '</g>') for x in (c, a1, c2))[:3])
    return dict(sec='VIS', topic='Figure analogy', level='B', marks=2, q='The second figure is the first figure %s. Apply the same change to the third figure. Which option results?' % t[0], svg=stem, opts=[dict(svg=fig(o)) for o in opts], ans=a,
                why='Work out the change from figure 1 to figure 2 (%s) and apply exactly that change to figure 3. The other options apply a different change.' % t[0])


def g_fold(rng):
    axis = rng.choice(['v', 'h'])
    px, py = rng.choice([1, 2]) / 6.0 * 2, rng.choice([1, 2, 3]) / 8.0 * 2          # position inside the folded half, in unit square coordinates (0..1)
    # folded sheet: half square; unit coordinates inside the full sheet, hole in the near half
    if axis == 'v':        # fold left half over right: the folded sheet occupies x in [0.5, 1]
        hx, hy = 0.5 + px * 0.5 * 0.9 + 0.05, py * 0.9 + 0.05
        pts = [(hx, hy), (1 - hx, hy)]
        other = [(hx, hy), (hx, 1 - hy)]
    else:                  # fold top over bottom: folded sheet occupies y in [0.5, 1]
        hx, hy = px * 0.9 + 0.05, 0.5 + py * 0.5 * 0.9 + 0.05
        pts = [(hx, hy), (hx, 1 - hy)]
        other = [(hx, hy), (1 - hx, hy)]
    four = [(hx, hy), (1 - hx, hy), (hx, 1 - hy), (1 - hx, 1 - hy)]
    one = [(hx, hy)]
    diag = [(hx, hy), (1 - hx, 1 - hy)]
    def sheet(holes, size=100):
        b = '<rect x="8" y="8" width="84" height="84" fill="#FFFDF7" stroke="%s" stroke-width="1.8"/>' % INK
        b += ''.join('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="1.4"/>' % (8 + 84 * x, 8 + 84 * y, '#fff', '#C23A3A') for x, y in holes)
        return svg(size, size, b)
    cands = [other, four, diag, one]
    if sorted(map(lambda p: (round(p[0], 3), round(p[1], 3)), pts)) in [sorted(map(lambda p: (round(p[0], 3), round(p[1], 3)), o)) for o in cands]:
        return None
    opts, a = place(rng, pts, cands[:3])
    # stem: the folded sheet with the punch, and a fold line
    if axis == 'v':
        stem = svg(220, 100, '<rect x="8" y="8" width="84" height="84" fill="#FFFDF7" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3"/><rect x="50" y="8" width="42" height="84" fill="%s" stroke="%s" stroke-width="1.8"/><circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#C23A3A" stroke-width="1.4"/><text x="104" y="54" font-size="11" fill="#445">folded in half, then one hole punched</text>' % (INK, SOFT, INK, 8 + 84 * hx, 8 + 84 * hy))
        txt = 'A square sheet is folded in half from left to right (the left half goes over the right half), and one hole is punched through the folded layers as shown. Which option shows the sheet when it is opened out?'
    else:
        stem = svg(220, 100, '<rect x="8" y="8" width="84" height="84" fill="#FFFDF7" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3"/><rect x="8" y="50" width="84" height="42" fill="%s" stroke="%s" stroke-width="1.8"/><circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#C23A3A" stroke-width="1.4"/><text x="104" y="54" font-size="11" fill="#445">folded in half, then one hole punched</text>' % (INK, SOFT, INK, 8 + 84 * hx, 8 + 84 * hy))
        txt = 'A square sheet is folded in half from top to bottom (the top half goes over the bottom half), and one hole is punched through the folded layers as shown. Which option shows the sheet when it is opened out?'
    return dict(sec='SPA', topic='Paper folding and punching', level='B', marks=1, q=txt, svg=stem, opts=[dict(svg=sheet(o)) for o in opts], ans=a,
                why='Opening the fold mirrors the hole across the fold line, so there are two holes, level with each other across the line of the fold. Four holes would need two folds; a single hole or a hole mirrored across the other line is wrong.')


SHAPES = ['circle', 'square', 'triangle']
FILLS = ['none', 'half', 'full']


def cell_svg(shape, fill, size=60, col=INK):
    c = size / 2.0
    r = size * 0.33
    f = {'none': '#FFFDF7', 'half': '#9DB4E4', 'full': col}[fill]
    if shape == 'circle':
        return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (c, c, r, f, col)
    if shape == 'square':
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (c - r, c - r, 2 * r, 2 * r, f, col)
    return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (c, c - r - 2, c + r + 2, c + r, c - r - 2, c + r, f, col)


def g_matrix(rng):
    s = SHAPES[:]
    f = FILLS[:]
    rng.shuffle(s)
    rng.shuffle(f)
    k = rng.choice([1, 2])
    cell = lambda r, c: (s[(r + c) % 3], f[(r * k + c * (3 - k)) % 3])
    cells = {(r, c): cell(r, c) for r in range(3) for c in range(3)}
    ans_shape, ans_fill = cells[(2, 2)]
    body = ''
    for r in range(3):
        for c in range(3):
            body += '<rect x="%d" y="%d" width="60" height="60" fill="none" stroke="#B9C4DA"/>' % (c * 60 + 4, r * 60 + 4)
            if (r, c) != (2, 2):
                body += '<g transform="translate(%d,%d)">%s</g>' % (c * 60 + 4, r * 60 + 4, cell_svg(*cells[(r, c)]))
            else:
                body += '<text x="%d" y="%d" font-size="30" fill="#C23A3A" text-anchor="middle">?</text>' % (c * 60 + 34, r * 60 + 46)
    pool = []
    for sh in SHAPES:
        for fl in FILLS:
            if (sh, fl) != (ans_shape, ans_fill):
                pool.append((sh, fl))
    # distractors: one with the wrong shape, one with the wrong fill, one with both wrong
    wrong = [(rng.choice([x for x in SHAPES if x != ans_shape]), ans_fill), (ans_shape, rng.choice([x for x in FILLS if x != ans_fill])), (rng.choice([x for x in SHAPES if x != ans_shape]), rng.choice([x for x in FILLS if x != ans_fill]))]
    wrong = list(dict.fromkeys(wrong))
    if len(wrong) < 3:
        return None
    opts, a = place(rng, (ans_shape, ans_fill), wrong)
    return dict(sec='VIS', topic='Pattern in a grid', level='B', marks=2, q='Each row and each column of the grid follows the same two rules, one for the shapes and one for the shading. Which option replaces the question mark?', svg=svg(190, 190, body),
                opts=[dict(svg=svg(70, 70, '<g transform="translate(5,5)">%s</g>' % cell_svg(sh, fl))) for sh, fl in opts], ans=a,
                why='Look at shapes first: each shape appears once in every row and every column, so the missing cell takes the shape that is absent from its row and column (%s). Then do the same for the shading (%s). Only one option has both.' % (ans_shape, 'plain' if ans_fill == 'none' else 'half-shaded' if ans_fill == 'half' else 'solid'))


def arrow(angle, size=80, col=INK):
    c = size / 2.0
    pts = [(c, 8), (c + 14, 30), (c + 5, 30), (c + 5, size - 10), (c - 5, size - 10), (c - 5, 30), (c - 14, 30)]
    return '<g transform="rotate(%d %.1f %.1f)"><polygon points="%s" fill="%s" stroke="%s" stroke-width="1.6"/><circle cx="%.1f" cy="%.1f" r="4" fill="%s"/></g>' % (
        angle, c, c, ' '.join('%.1f,%.1f' % p for p in pts), SOFT, col, c + 16, size - 16, FILL)


def g_series(rng):
    step = rng.choice([45, 90, 135, -45, -90])
    start = rng.choice([0, 45, 90])
    seq = [(start + i * step) % 360 for i in range(4)]
    right = seq[3]
    pool = [(right + 45) % 360, (right - 45) % 360, (right + 180) % 360, (right + 90) % 360, (right - 90) % 360]
    wrong = [p for p in dict.fromkeys(pool) if p != right][:3]
    opts, a = place(rng, right, wrong)
    body = ''
    for i in range(3):
        body += '<g transform="translate(%d,0)">%s</g>' % (i * 86, svg(80, 80, arrow(seq[i])).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80" role="img">', '<g>').replace('</svg>', '</g>'))
        body += '<text x="%d" y="46" font-size="16" fill="#445">,</text>' % (i * 86 + 80)
    body += '<text x="268" y="52" font-size="30" fill="#C23A3A">?</text>'
    return dict(sec='VIS', topic='Series of rotating figures', level='B', marks=1, q='The figures turn by the same amount each time. Which option comes next in the series?', svg=svg(300, 86, body),
                opts=[dict(svg=svg(80, 80, arrow(o))) for o in opts], ans=a,
                why='Each figure is the one before it turned by %d degrees %s. Apply that turn once more to the third figure to get the answer.' % (abs(step), 'clockwise' if step > 0 else 'anticlockwise'))


def poly_pts(n, cx, cy, r, rot=0):
    return ' '.join('%.1f,%.1f' % (cx + r * math.sin(rot + 2 * math.pi * i / n), cy - r * math.cos(rot + 2 * math.pi * i / n)) for i in range(n))


def g_odd_sides(rng):
    n = rng.choice([3, 4, 5, 6, 7])
    m = rng.choice([x for x in (3, 4, 5, 6, 7, 8) if x != n])
    cols = ['#9DB4E4', '#F5B98A', '#9ED7B8', '#E0C3F0']

    def one(sides, rot, col):
        return svg(90, 90, '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (poly_pts(sides, 45, 47, 34, rot), col, INK))
    figs = [(n, rng.random() * 3, rng.choice(cols)) for _ in range(3)]
    opts, a = place(rng, (m, rng.random() * 3, rng.choice(cols)), figs)
    return dict(sec='VIS', topic='Odd one out by number of sides', level='B', marks=1, q='Three of these figures share a feature. Which one is the odd one out?', opts=[dict(svg=one(*o)) for o in opts], ans=a,
                why='Count the sides: three figures have %d sides and one has %d. Size, colour and the way a figure is turned do not matter.' % (n, m))


def quad(shaded):
    b = ''
    for i in range(4):
        x, y = (i % 2) * 40 + 5, (i // 2) * 40 + 5
        b += '<rect x="%d" y="%d" width="40" height="40" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, INK if i in shaded else '#FFFDF7', INK)
    return svg(90, 90, b)


def g_odd_shade(rng):
    k = rng.choice([1, 2, 3])
    m = rng.choice([x for x in (1, 2, 3) if x != k])
    import itertools
    same = rng.sample(list(itertools.combinations(range(4), k)), 3)
    odd = rng.choice(list(itertools.combinations(range(4), m)))
    opts, a = place(rng, odd, same)
    return dict(sec='VIS', topic='Odd one out by shading', level='B', marks=1, q='Which figure is the odd one out?', opts=[dict(svg=quad(o)) for o in opts], ans=a,
                why='Count the shaded squares in each figure: three have %d shaded and one has %d. Their positions do not matter.' % (k, m))


# ---- cube with letters (isometric) -------------------------------------------------------------------------------------------------------
def cube(top, left, right, size=110):
    cx, cy, s = size / 2.0, size / 2.0 + 4, 34
    dx, dy = s * math.cos(math.pi / 6), s * 0.5
    T = [(cx, cy - 2 * dy - s * 0.0 - dy * 0), (cx + dx, cy - dy), (cx, cy), (cx - dx, cy - dy)]
    T = [(cx, cy - s), (cx + dx, cy - s + dy), (cx, cy - s + 2 * dy), (cx - dx, cy - s + dy)]
    L = [(cx - dx, cy - s + dy), (cx, cy - s + 2 * dy), (cx, cy + dy * 0 + s * 0 + (cy - (cy - s + 2 * dy)) + 0 + s), (cx - dx, cy - s + dy + s)]
    L = [(cx - dx, cy - s + dy), (cx, cy - s + 2 * dy), (cx, cy - s + 2 * dy + s), (cx - dx, cy - s + dy + s)]
    R = [(cx + dx, cy - s + dy), (cx, cy - s + 2 * dy), (cx, cy - s + 2 * dy + s), (cx + dx, cy - s + dy + s)]
    P = lambda pts: ' '.join('%.1f,%.1f' % p for p in pts)
    mid = lambda pts: (sum(p[0] for p in pts) / 4.0, sum(p[1] for p in pts) / 4.0)
    b = ''
    for pts, col, lab in ((T, '#EAF0FB', top), (L, '#C9D7F2', left), (R, '#A9BFE8', right)):
        mx, my = mid(pts)
        b += '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.8" stroke-linejoin="round"/><text x="%.1f" y="%.1f" font-size="17" font-weight="700" text-anchor="middle" fill="%s">%s</text>' % (P(pts), col, INK, mx, my + 6, INK, lab)
    return svg(size, size, b)


def g_cube(rng):
    letters = list('ABCDEF')
    rng.shuffle(letters)
    a, b, c, d, e, f = letters      # a-f? choose: views share two adjacent faces a,b; the two faces next to both are c and d, so c is opposite d
    view1 = (a, b, c)
    view2 = (a, d, b)          # the other end of the edge shared by a and b: seen from there the order of left and right changes
    ask, right = (c, d) if rng.random() < .5 else (d, c)
    others = [x for x in letters if x not in (ask, right)]
    wrong = rng.sample(others, 3)
    opts, an = place(rng, right, wrong)
    return dict(sec='SPA', topic='Cube: opposite faces', level='BM', marks=2, q='Two views of the same cube are shown (top, left and right faces visible). Which letter is on the face opposite to the face marked %s?' % ask,
                svg=svg(250, 110, '<g>%s</g><g transform="translate(130,0)">%s</g>' % tuple(x.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" width="110" height="110" role="img">', '').replace('</svg>', '') for x in (cube(*view1), cube(*view2)))),
                opts=[dict(t=o) for o in opts], ans=an,
                why='Faces %s and %s appear in both views. The only faces that touch both of them are %s and %s, which sit at the two ends of the edge they share, so %s and %s are opposite faces.' % (a, b, c, d, c, d))


# ---- counting, clock, symmetry, colour wheel ---------------------------------------------------------------------------------------------
def g_squares(rng):
    n = rng.choice([3, 4, 5])
    tot = sum(k * k for k in range(1, n + 1))
    u = 120 / n
    body = ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#FFFDF7" stroke="%s" stroke-width="1.6"/>' % (5 + i * u, 5 + j * u, u, u, INK) for i in range(n) for j in range(n))
    wrong = list(dict.fromkeys([n * n, tot - n, tot + n, tot - 1, n * n + n]))
    wrong = [w for w in wrong if w != tot][:3]
    opts, a = place(rng, tot, wrong)
    return dict(sec='VIS', topic='Counting squares', level='B', marks=1, q='How many squares of all sizes are there in this %d by %d grid?' % (n, n), svg=svg(130, 130, body), opts=[dict(t=str(o)) for o in opts], ans=a,
                why='Count by size: ' + ' + '.join('%d (of side %d)' % ((n - k + 1) ** 2, k) for k in range(1, n + 1)) + ' = %d.' % tot)


def clock(h, m, size=110):
    c = size / 2.0
    hang = math.radians(30 * (h % 12) + m * 0.5)
    mang = math.radians(6 * m)
    ticks = ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d"/>' % (c + 44 * math.sin(math.radians(30 * i)), c - 44 * math.cos(math.radians(30 * i)), c + 50 * math.sin(math.radians(30 * i)), c - 50 * math.cos(math.radians(30 * i)), INK, 2 if i % 3 else 3) for i in range(12))
    return svg(size, size, '<circle cx="%.1f" cy="%.1f" r="52" fill="#FFFDF7" stroke="%s" stroke-width="2.4"/>%s<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4" stroke-linecap="round"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#C23A3A" stroke-width="2.4" stroke-linecap="round"/><circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (
        c, c, INK, ticks, c, c, c + 26 * math.sin(hang), c - 26 * math.cos(hang), INK, c, c, c + 40 * math.sin(mang), c - 40 * math.cos(mang), c, c, INK))


def g_clock(rng):
    h, m = rng.randrange(1, 13), rng.choice(range(5, 60, 5))
    ang = abs(30 * (h % 12) - 5.5 * m)
    ang = min(ang, 360 - ang)
    txt = ('%g' % ang)
    wrong = list(dict.fromkeys(['%g' % x for x in (max(0, ang - 15), ang + 15, abs(30 * h - 6 * m) % 180, ang + 30, 180 - ang) if '%g' % x != txt and x > 0 and x <= 180]))[:3]
    while len(wrong) < 3:
        wrong.append('%g' % (ang + 10 * (len(wrong) + 1)))
    opts, a = place(rng, txt, wrong)
    return dict(sec='VIS', topic='Angle between clock hands', level='B', marks=2, q='What is the smaller angle between the hour hand and the minute hand when the time is %d:%02d?' % (h, m), svg=clock(h, m), opts=[dict(t=o + ' degrees') for o in opts], ans=a,
                why='The minute hand moves 6 degrees a minute and the hour hand 0.5 degrees a minute. At %d:%02d the minute hand is at %g degrees and the hour hand at %g degrees from 12, so the angle is %g degrees.' % (h, m, 6 * m, 30 * (h % 12) + 0.5 * m, ang))


def g_symmetry(rng):
    spec = {'a rectangle that is not a square': (2, lambda: svg(90, 90, '<rect x="10" y="26" width="70" height="38" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % INK)),
            'an equilateral triangle': (3, lambda: svg(90, 90, '<polygon points="%s" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % (poly_pts(3, 45, 52, 38), INK))),
            'a square': (4, lambda: svg(90, 90, '<rect x="16" y="16" width="58" height="58" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % INK)),
            'a regular pentagon': (5, lambda: svg(90, 90, '<polygon points="%s" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % (poly_pts(5, 45, 49, 38), INK))),
            'a regular hexagon': (6, lambda: svg(90, 90, '<polygon points="%s" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % (poly_pts(6, 45, 46, 38), INK))),
            'a parallelogram that is not a rhombus': (0, lambda: svg(90, 90, '<polygon points="22,62 12,28 62,28 72,62" fill="#9DB4E4" stroke="%s" stroke-width="2"/>' % INK))}
    keys = list(spec)
    target = rng.choice([k for k in keys if spec[k][0] > 0])
    others = rng.sample([k for k in keys if k != target], 3)
    k = spec[target][0]
    opts, a = place(rng, target, others)
    names = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
    return dict(sec='VIS', topic='Lines of symmetry', level='B', marks=1, q='Which of the figures has exactly %s lines of symmetry?' % names[k], opts=[dict(svg=spec[o][1](), t=None) for o in opts], ans=a,
                why='%s has %d line%s of symmetry. A regular polygon with n sides has n; a rectangle that is not a square has 2; a parallelogram that is not a rhombus or rectangle has none.' % (target.capitalize(), k, 's' if k != 1 else ''))


WHEEL = ['Yellow', 'Yellow-Orange', 'Orange', 'Red-Orange', 'Red', 'Red-Violet', 'Violet', 'Blue-Violet', 'Blue', 'Blue-Green', 'Green', 'Yellow-Green']
HEX = ['#F7D417', '#F4B71C', '#F28C1A', '#EC5B1F', '#D8262B', '#B2236D', '#7A2A8C', '#4B3A9A', '#2457B5', '#1A8C94', '#2A9A47', '#9DBF2C']


def wheel_svg():
    b = ''
    for i, col in enumerate(HEX):
        a1, a2 = math.radians(30 * i - 15), math.radians(30 * i + 15)
        x1, y1, x2, y2 = 80 + 70 * math.sin(a1), 80 - 70 * math.cos(a1), 80 + 70 * math.sin(a2), 80 - 70 * math.cos(a2)
        b += '<path d="M80 80 L%.1f %.1f A70 70 0 0 1 %.1f %.1f Z" fill="%s" stroke="#fff" stroke-width="1.5"/>' % (x1, y1, x2, y2, col)
    b += '<circle cx="80" cy="80" r="22" fill="#fff"/>'
    return svg(160, 160, b)


def g_wheel(rng):
    i = rng.randrange(12)
    kind = rng.choice(['comp', 'tri', 'ana', 'split'])
    name = WHEEL[i]
    ctx = 'On the standard 12-hue colour wheel (in order: ' + ', '.join(WHEEL) + ')'
    if kind == 'comp':
        right = WHEEL[(i + 6) % 12]
        q = '%s, which hue is the complement of %s?' % (ctx, name)
        wrong = [WHEEL[(i + 5) % 12], WHEEL[(i + 4) % 12], WHEEL[(i + 3) % 12]]
        why = 'A complement lies directly opposite on the wheel, six steps away. Six steps from %s is %s.' % (name, right)
        opts, a = place(rng, right, wrong)
        opts = [dict(t=o) for o in opts]
    elif kind == 'tri':
        right = (WHEEL[(i + 4) % 12], WHEEL[(i + 8) % 12])
        q = '%s, which pair of hues forms a triadic scheme with %s?' % (ctx, name)
        wrong = [(WHEEL[(i + 3) % 12], WHEEL[(i + 9) % 12]), (WHEEL[(i + 6) % 12], WHEEL[(i + 2) % 12]), (WHEEL[(i + 5) % 12], WHEEL[(i + 7) % 12])]
        why = 'A triad uses three hues equally spaced, four steps apart. From %s that gives %s and %s.' % (name, right[0], right[1])
        opts, a = place(rng, right, wrong)
        opts = [dict(t=' and '.join(o)) for o in opts]
    elif kind == 'ana':
        right = (WHEEL[(i - 1) % 12], WHEEL[(i + 1) % 12])
        q = '%s, which pair of hues forms an analogous scheme with %s as the middle colour?' % (ctx, name)
        wrong = [(WHEEL[(i + 1) % 12], WHEEL[(i + 2) % 12]), (WHEEL[(i - 2) % 12], WHEEL[(i + 2) % 12]), (WHEEL[(i + 3) % 12], WHEEL[(i - 3) % 12])]
        why = 'An analogous scheme uses neighbours: the hue just before and just after %s, namely %s and %s.' % (name, right[0], right[1])
        opts, a = place(rng, right, wrong)
        opts = [dict(t=' and '.join(o)) for o in opts]
    else:
        right = (WHEEL[(i + 5) % 12], WHEEL[(i + 7) % 12])
        q = '%s, which pair forms a split-complementary scheme with %s?' % (ctx, name)
        wrong = [(WHEEL[(i + 6) % 12], WHEEL[(i + 7) % 12]), (WHEEL[(i + 4) % 12], WHEEL[(i + 8) % 12]), (WHEEL[(i + 4) % 12], WHEEL[(i + 6) % 12])]
        why = 'Split-complementary takes the two hues on either side of the complement. The complement of %s is %s, so the pair is %s and %s.' % (name, WHEEL[(i + 6) % 12], right[0], right[1])
        opts, a = place(rng, right, wrong)
        opts = [dict(t=' and '.join(o)) for o in opts]
    return dict(sec='CLR', topic='Colour wheel relationships', level='B', marks=1, q=q, svg=wheel_svg(), opts=opts, ans=a, why=why)


GENS = [('mirror', g_mirror, 10), ('rotation', g_rotation, 10), ('chiral', g_chiral_odd, 10), ('analogy', g_analogy, 8), ('fold', g_fold, 10), ('matrix', g_matrix, 10), ('series', g_series, 8),
        ('oddsides', g_odd_sides, 8), ('oddshade', g_odd_shade, 8), ('cube', g_cube, 10), ('squares', g_squares, 6), ('clock', g_clock, 8), ('symmetry', g_symmetry, 8), ('wheel', g_wheel, 12)]


def main():
    out, seen = [], set()
    for name, fn, count in GENS:
        got, seed = 0, 0
        while got < count and seed < 400:
            seed += 1
            rng = random.Random('%s-%d' % (name, seed))
            q = fn(rng)
            if not q:
                continue
            key = (name, json.dumps(q['opts'], sort_keys=True) + q.get('svg', '') + q['q'])
            if key in seen:
                continue
            seen.add(key)
            q['id'] = 'V-%s-%02d' % (name[:5].upper(), got + 1)
            q['gen'] = name
            out.append(q)
            got += 1
        print(name, got)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'questions', os.path.getsize(OUT) // 1024, 'KB')


if __name__ == '__main__':
    main()
