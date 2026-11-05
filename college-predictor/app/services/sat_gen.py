"""SAT-style Math question generators for EduPulse-SAT.

Each generator builds a question FROM its answer (it picks the solution first and derives the numbers), so the key is correct by construction and every attempt gets new numbers.
A question id is 'g:<family>:<seed>'; the same id always rebuilds the same question, which is how a missed question comes back in the Daily Review with fresh numbers
only when the student asks for a new one (the card keeps the family, and a new seed is drawn).
Domains follow the Digital SAT Math content domains: Algebra, Advanced Math, Problem-Solving and Data Analysis, Geometry and Trigonometry.
Item: {id, sec 'MATH', domain, skill, kind 'mcq' | 'spr', stem, opts (4) for mcq, ans (index) for mcq or ans_text (canonical number as text) for spr, why, diff 1-3}.
A student-produced response is compared as a number (3/4, 0.75 and .75 are the same answer).
"""
import math
import random
from fractions import Fraction as F

DOMAINS = ['Algebra', 'Advanced Math', 'Problem-Solving and Data Analysis', 'Geometry and Trigonometry']


def fmt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else '%d/%d' % (v.numerator, v.denominator)


def dec(v, nd=2):
    x = round(float(v), nd)
    s = ('%.*f' % (nd, x)).rstrip('0').rstrip('.')
    return s or '0'


def sg(n):
    """' + 5' or ' - 5' for a term after the first."""
    return (' + %d' % n) if n >= 0 else (' - %d' % -n)


def _opts(rng, correct, wrongs, f=fmt):
    """Four distinct options with the correct one in a random place -> (opts, index). Wrongs that clash with the key or each other are replaced by nearby values."""
    seen, out = {f(correct)}, []
    for w in wrongs:
        t = f(w)
        if t not in seen:
            seen.add(t)
            out.append(w)
    k = 1
    while len(out) < 3:
        cand = correct + k * (1 if k % 2 else -1) * (1 if isinstance(correct, int) else F(1, 2))
        k += 1
        t = f(cand)
        if t not in seen:
            seen.add(t)
            out.append(cand)
    out = out[:3]
    allv = out + [correct]
    rng.shuffle(allv)
    return [f(v) for v in allv], [f(v) for v in allv].index(f(correct))


def _mcq(rng, dom, skill, stem, correct, wrongs, why, diff, f=fmt):
    opts, ans = _opts(rng, correct, wrongs, f)
    return {'sec': 'MATH', 'domain': dom, 'skill': skill, 'kind': 'mcq', 'stem': stem, 'opts': opts, 'ans': ans, 'why': why, 'diff': diff}


def _spr(dom, skill, stem, answer, why, diff):
    return {'sec': 'MATH', 'domain': dom, 'skill': skill, 'kind': 'spr', 'stem': stem, 'ans_text': fmt(answer), 'why': why, 'diff': diff}


def _either(rng, dom, skill, stem, correct, wrongs, why, diff, f=fmt, p_spr=0.35):
    """Multiple choice, or a student-produced response (about a third of the time) when the answer is a whole number or a simple fraction."""
    if rng.random() < p_spr and F(correct).denominator in (1, 2, 4, 5, 8, 10) and abs(F(correct)) < 10000:
        return _spr(dom, skill, stem, correct, why, diff)
    return _mcq(rng, dom, skill, stem, correct, wrongs, why, diff, f)


# ---------------------------------------------------------------------------------------- Algebra
def lin1(rng):
    a, x, b = rng.randint(2, 9), rng.randint(-8, 12), rng.randint(-15, 15)
    c = a * x + b
    return _either(rng, 'Algebra', 'Linear equations in one variable', 'If %dx%s = %d, what is the value of x?' % (a, sg(b), c), x, [F(c + b, a), F(c, a) - b, F(c - b, a) + 1],
                   '%s from both sides to get %dx = %d, then divide by %d: x = %d.' % (('Subtract %d' % b) if b >= 0 else ('Add %d' % -b), a, c - b, a, x), 1)


def lin_word(rng):
    fee, rate, hrs = rng.randint(20, 90), rng.randint(5, 25), rng.randint(3, 12)
    total = fee + rate * hrs
    return _either(rng, 'Algebra', 'Linear functions', 'A tutor charges a one-time fee of $%d plus $%d for each hour of tutoring. One student paid a total of $%d. For how many hours was the student tutored?' % (fee, rate, total),
                   hrs, [F(total, rate), (total - fee) // rate + 1, hrs - 1], 'The cost is %d + %dh. Set %d + %dh = %d, so %dh = %d and h = %d.' % (fee, rate, fee, rate, total, rate, total - fee, hrs), 1)


def system2(rng):
    x, y = rng.randint(-5, 9), rng.randint(-5, 9)
    a, b, c, d = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5), rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    if a * d - b * c == 0:
        d += 1
    e1, e2 = a * x + b * y, c * x + d * y
    which = rng.choice(['x', 'y', 'x + y'])
    ans = {'x': x, 'y': y, 'x + y': x + y}[which]
    wr = {'x': [y, x + y, -x], 'y': [x, x + y, -y], 'x + y': [x, y, x - y]}[which]
    return _either(rng, 'Algebra', 'Systems of two linear equations', 'The system of equations below has solution (x, y).\n%dx%s%dy = %d\n%dx%s%dy = %d\nWhat is the value of %s?' % (a, ' +' if b > 0 else ' -', abs(b), e1, c, ' +' if d > 0 else ' -', abs(d), e2, which),
                   ans, wr, 'Solving the pair gives x = %d and y = %d, so %s = %d.' % (x, y, which, ans), 2)


def ineq(rng):
    a, b = rng.randint(2, 7), rng.randint(1, 20)
    n = rng.randint(3, 14)
    c = a * n + b + rng.randint(0, a - 1)                       # 3x + b <= c  ->  greatest integer is n
    return _either(rng, 'Algebra', 'Linear inequalities in one variable', 'What is the greatest integer value of x for which %dx + %d ≤ %d?' % (a, b, c), n, [n + 1, n - 1, F(c - b, a)],
                   'Subtract %d: %dx ≤ %d, so x ≤ %s. The greatest integer is %d.' % (b, a, c - b, fmt(F(c - b, a)) if F(c - b, a).denominator > 1 else str(F(c - b, a)), n), 2)


def slope2(rng):
    m, b = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5]), rng.randint(-6, 8)
    x1, x2 = rng.randint(-3, 2), rng.randint(3, 8)
    y1, y2 = m * x1 + b, m * x2 + b
    return _either(rng, 'Algebra', 'Linear equations in two variables', 'A line in the xy-plane passes through the points (%d, %d) and (%d, %d). What is the y-intercept of the line?' % (x1, y1, x2, y2), b, [y1, -b, m],
                   'The slope is (%d - %d)/(%d - %d) = %d. Using y = %dx + b with the point (%d, %d) gives b = %d.' % (y2, y1, x2, x1, m, m, x1, y1, b), 2)


def _no_solution_item(rng, a, b):
    m = rng.randint(2, 4)                 # the second equation is m times the first, so k must be m times the constant of the first
    c = rng.randint(3, 15)
    stem = 'In the system below, k is a constant. For what value of k does the system have infinitely many solutions?\n%dx + %dy = %d\n%dx + %dy = k' % (a, b, c, m * a, m * b)
    return _either(rng, 'Algebra', 'Systems of two linear equations', stem, m * c, [c, m * a * b, c + m], 'The second equation is %d times the first, so for the equations to describe the same line k must be %d × %d = %d.' % (m, m, c, m * c), 3)


# ---------------------------------------------------------------------------------------- Advanced Math
def quad_sum(rng):
    r1, r2 = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]), rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8])
    if r1 == r2:
        r2 = -r2
    b, c = -(r1 + r2), r1 * r2
    ask = rng.choice(['sum', 'product', 'greater'])
    ans = {'sum': r1 + r2, 'product': r1 * r2, 'greater': max(r1, r2)}[ask]
    what = {'sum': 'the sum of the solutions', 'product': 'the product of the solutions', 'greater': 'the greater solution'}[ask]
    eq = 'x²%s%s = 0' % ((' + %dx' % b) if b > 0 else (' - %dx' % -b) if b < 0 else '', (' + %d' % c) if c > 0 else (' - %d' % -c) if c < 0 else '')
    return _either(rng, 'Advanced Math', 'Nonlinear equations in one variable', 'What is %s to the equation %s?' % (what, eq), ans, [-ans, r1 - r2 if ask != 'greater' else min(r1, r2), c if ask != 'product' else b],
                   'The equation factors as (x %s %d)(x %s %d) = 0, so the solutions are %d and %d; %s is %d.' % ('-' if r1 >= 0 else '+', abs(r1), '-' if r2 >= 0 else '+', abs(r2), r1, r2, what, ans), 2)


def quad_min(rng):
    h, k, a = rng.randint(-5, 7), rng.randint(-12, 15), rng.randint(1, 4)
    b, c = -2 * a * h, a * h * h + k
    form = 'f(x) = %dx²%s%s' % (a, (' + %dx' % b) if b > 0 else (' - %dx' % -b) if b < 0 else '', (' + %d' % c) if c > 0 else (' - %d' % -c) if c < 0 else '')
    return _either(rng, 'Advanced Math', 'Nonlinear functions', 'The function %s has a minimum value. What is the minimum value of f?' % form, k, [c, h, -k],
                   'Complete the square: f(x) = %d(x %s %d)² %s %d, so the minimum value is %d, reached at x = %d.' % (a, '-' if h >= 0 else '+', abs(h), '+' if k >= 0 else '-', abs(k), k, h), 3)


def expo(rng):
    p0, r, n = rng.choice([100, 200, 250, 400, 500, 800, 1000]), rng.choice([2, 3]), rng.randint(2, 5)
    per = rng.choice([2, 3, 4, 5])
    ans = p0 * r ** n
    return _either(rng, 'Advanced Math', 'Nonlinear functions', 'A colony starts with %d bacteria and its size multiplies by %d every hour. Which is the number of bacteria after %d hours?' % (p0, r, n), ans, [p0 * r * n, p0 * (r + n), p0 * r ** (n - 1)],
                   'The size is %d × %d^t. After %d hours it is %d × %d^%d = %d.' % (p0, r, n, p0, r, n, ans), 2)


def exponents(rng):
    a, m, n = rng.choice([2, 3, 5]), rng.randint(2, 6), rng.randint(2, 6)
    ans = a ** (m + n - 2)
    return _either(rng, 'Advanced Math', 'Equivalent expressions', 'What is the value of (%d^%d × %d^%d) / %d²?' % (a, m, a, n, a), ans, [a ** (m + n), a ** (m * n - 2), a ** (m + n - 1)],
                   'Add the exponents in the numerator: %d^%d. Dividing by %d² subtracts 2: %d^%d = %d.' % (a, m + n, a, a, m + n - 2, ans), 2)


def compose(rng):
    a, b, c, d = rng.randint(1, 4), rng.randint(-5, 6), rng.randint(1, 4), rng.randint(-5, 6)
    x = rng.randint(-3, 5)
    gx = c * x + d
    ans = a * gx + b
    return _either(rng, 'Advanced Math', 'Nonlinear functions', 'The functions f and g are defined by f(x) = %dx%s and g(x) = %dx%s. What is the value of f(g(%d))?' % (a, sg(b), c, sg(d), x), ans, [c * (a * x + b) + d, gx, a * x + b],
                   'First g(%d) = %d. Then f(%d) = %d(%d)%s = %d.' % (x, gx, gx, a, gx, sg(b), ans), 2)


def radical_eq(rng):
    x, k = rng.randint(3, 20), rng.randint(1, 6)
    s = rng.randint(2, 7)
    inner = s * s
    # sqrt(x + k) = s  with x chosen so x + k = s^2
    x = inner - k
    return _either(rng, 'Advanced Math', 'Nonlinear equations in one variable', 'What is the solution to the equation √(x%s) = %d?' % (sg(k), s), x, [inner, s - k, s + k], 'Square both sides: x%s = %d, so x = %d. Check: √%d = %d.' % (sg(k), inner, x, inner, s), 2)


def zero_k(rng):
    r, a = rng.randint(1, 5), rng.randint(1, 3)
    # p(x) = a x^2 + k x - c with p(r) = 0 -> choose k, c? choose k and solve c: instead ask k given c
    k = rng.randint(-6, 8)
    c = a * r * r + k * r
    return _either(rng, 'Advanced Math', 'Nonlinear equations in one variable', 'For the polynomial p(x) = %dx² + kx %s %d, where k is a constant, p(%d) = 0. What is the value of k?' % (a, '-' if c >= 0 else '+', abs(c), r), k, [-k, F(c, r), k + a],
                   'Substitute x = %d: %d·%d + %dk %s %d = 0, so %dk = %d and k = %d.' % (r, a, r * r, r, '-' if c >= 0 else '+', abs(c), r, c - a * r * r, k), 3)


# ---------------------------------------------------------------------------------------- Problem-Solving and Data Analysis
def pct_change(rng):
    p = rng.choice([40, 50, 60, 80, 120, 150, 200, 250, 400])
    up, down = rng.choice([10, 20, 25, 50]), rng.choice([10, 20, 25])
    new = F(p) * (100 + up) / 100 * (100 - down) / 100
    ans = new
    return _either(rng, 'Problem-Solving and Data Analysis', 'Percentages', 'The price of a jacket was $%d. The store raised the price by %d%%, and later reduced the new price by %d%%. What is the final price, in dollars?' % (p, up, down),
                   ans, [F(p) * (100 + up - down) / 100, F(p) * (100 - down) / 100, F(p) * (100 + up) / 100], 'After the increase: %d × %s = %s. After the decrease: %s × %s = %s.' % (p, dec(1 + F(up, 100)), fmt(F(p) * (100 + up) / 100), fmt(F(p) * (100 + up) / 100), dec(1 - F(down, 100)), fmt(ans)), 2)


def rate_conv(rng):
    kmh = rng.choice([36, 54, 72, 90, 108])
    secs = rng.choice([5, 10, 20])
    ans = F(kmh * 1000, 3600) * secs
    return _either(rng, 'Problem-Solving and Data Analysis', 'Ratios, rates and units', 'A train travels at a constant speed of %d kilometers per hour. How many meters does it travel in %d seconds?' % (kmh, secs), ans,
                   [F(kmh, 3600) * secs, F(kmh * 1000, 60) * secs, F(kmh * 3600, 1000) * secs], '%d km/h = %d × 1000 / 3600 = %s m/s. In %d seconds: %s × %d = %s meters.' % (kmh, kmh, fmt(F(kmh * 1000, 3600)), secs, fmt(F(kmh * 1000, 3600)), secs, fmt(ans)), 2)


def mean_missing(rng):
    n = rng.randint(4, 6)
    target = rng.randint(70, 92)
    scores = [rng.randint(60, 98) for _ in range(n - 1)]
    last = target * n - sum(scores)
    if not 0 <= last <= 100:
        scores = [target + rng.randint(-8, 8) for _ in range(n - 1)]
        last = target * n - sum(scores)
    return _either(rng, 'Problem-Solving and Data Analysis', 'One-variable data', 'A student\'s scores on %d tests were %s, and one more test score is not shown. The mean of all %d scores is %d. What is the score that is not shown?' % (n, ', '.join(map(str, scores)), n, target),
                   last, [target, F(sum(scores), n - 1), last + n], 'The total of all %d scores is %d × %d = %d. The shown scores add to %d, so the missing score is %d.' % (n, target, n, target * n, sum(scores), last), 2)


def prob_table(rng):
    a, b, c, d = [rng.randint(8, 40) for _ in range(4)]
    tot = a + b + c + d
    return _mcq(rng, 'Problem-Solving and Data Analysis', 'Probability and conditional probability',
                'A survey asked %d students whether they prefer online or in-person classes.\nOnline: %d juniors and %d seniors.\nIn-person: %d juniors and %d seniors.\nA student is chosen at random from the seniors. What is the probability that the student prefers online classes?' % (tot, a, b, c, d),
                F(b, b + d), [F(b, tot), F(a, a + c), F(b, a + b)], 'There are %d + %d = %d seniors, and %d of them prefer online classes, so the probability is %d/%d.' % (b, d, b + d, b, b, b + d), 2,
                f=lambda v: fmt(v))


def best_fit(rng):
    m, b = rng.choice([2, 3, 4, 5, 6]), rng.randint(5, 30)
    x = rng.randint(8, 20)
    return _either(rng, 'Problem-Solving and Data Analysis', 'Scatterplots and models', 'A scientist modelled the height of a plant, in centimeters, with the equation h = %dt + %d, where t is the number of days since planting. According to the model, what is the height of the plant after %d days?' % (m, b, x),
                   m * x + b, [m + x + b, (m + b) * x, m * (x + b)], 'Substitute t = %d: h = %d(%d) + %d = %d centimeters.' % (x, m, x, b, m * x + b), 1)


def two_way_pct(rng):
    n = rng.choice([40, 50, 80, 125, 200, 250])
    pct = rng.choice([12, 15, 20, 24, 30, 35, 40, 45])
    ans = F(n * pct, 100)
    return _either(rng, 'Problem-Solving and Data Analysis', 'Percentages', 'In a school of %d students, %d%% take an elective in music. How many students take music?' % (n, pct), ans, [F(n, pct), n - ans, F(pct * n, 10)],
                   '%d%% of %d is %d/100 × %d = %s.' % (pct, n, pct, n, fmt(ans)), 1)


# ---------------------------------------------------------------------------------------- Geometry and Trigonometry
def rect_comp(rng):
    w, h, cw, ch = rng.randint(8, 20), rng.randint(6, 14), rng.randint(2, 5), rng.randint(2, 5)
    ans = w * h - cw * ch
    return _either(rng, 'Geometry and Trigonometry', 'Area and volume', 'A rectangular garden is %d meters by %d meters. A rectangular pond that is %d meters by %d meters is built inside it. What is the area, in square meters, of the part of the garden that is not the pond?' % (w, h, cw, ch),
                   ans, [w * h + cw * ch, 2 * (w + h) - 2 * (cw + ch), w * h], 'The garden is %d × %d = %d. The pond is %d × %d = %d. The difference is %d square meters.' % (w, h, w * h, cw, ch, cw * ch, ans), 1)


def circle_sector(rng):
    r = rng.choice([3, 4, 5, 6, 8, 9, 10, 12])
    th = rng.choice([30, 45, 60, 90, 120, 180])
    arc = F(th, 360) * 2 * r
    return _mcq(rng, 'Geometry and Trigonometry', 'Circles', 'A circle has radius %d. What is the length of an arc of this circle that has a central angle of %d°? (Give the answer in terms of π.)' % (r, th), arc,
                [F(th, 360) * r, F(th, 360) * r * r, F(th, 180) * r * 4], 'The arc is %d/360 of the circumference 2πr = %dπ, so its length is %sπ.' % (th, 2 * r, fmt(arc)), 2,
                f=lambda v: ('%sπ' % fmt(v)) if v != 0 else '0')


def pyth(rng):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (20, 21, 29)])
    k = rng.randint(1, 3)
    a, b, c = a * k, b * k, c * k
    ask = rng.choice(['hyp', 'leg'])
    if ask == 'hyp':
        return _either(rng, 'Geometry and Trigonometry', 'Right triangles and trigonometry', 'A right triangle has legs of length %d and %d. What is the length of its hypotenuse?' % (a, b), c, [a + b, c - 1, a * b // 2],
                       'By the Pythagorean theorem the hypotenuse is √(%d² + %d²) = √%d = %d.' % (a, b, a * a + b * b, c), 1)
    return _either(rng, 'Geometry and Trigonometry', 'Right triangles and trigonometry', 'A right triangle has a hypotenuse of length %d and one leg of length %d. What is the length of the other leg?' % (c, a), b, [c - a, a + c, b + 1],
                   'The other leg is √(%d² - %d²) = √%d = %d.' % (c, a, c * c - a * a, b), 2)


def trig_ratio(rng):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    fn = rng.choice(['sin', 'cos', 'tan'])
    val = {'sin': F(a, c), 'cos': F(b, c), 'tan': F(a, b)}[fn]
    wrong = {'sin': [F(b, c), F(a, b), F(c, a)], 'cos': [F(a, c), F(b, a), F(c, b)], 'tan': [F(b, a), F(a, c), F(b, c)]}[fn]
    return _trig_item(rng, a, b, c, fn, val, wrong)


def _trig_item(rng, a, b, c, fn, val, wrong):
    # angle A is opposite BC (length a): opposite = a, adjacent = b, hypotenuse = c
    why = {'sin': 'sin A = opposite/hypotenuse = BC/AB = %d/%d.' % (a, c), 'cos': 'cos A = adjacent/hypotenuse = AC/AB = %d/%d.' % (b, c), 'tan': 'tan A = opposite/adjacent = BC/AC = %d/%d.' % (a, b)}[fn]
    return _mcq(rng, 'Geometry and Trigonometry', 'Right triangles and trigonometry', 'In right triangle ABC, the right angle is at C, AC = %d, BC = %d and AB = %d. What is the value of %s A?' % (b, a, c, fn), val, wrong, why, 2)


def similar(rng):
    k = rng.choice([F(3, 2), 2, 3, F(5, 2), F(4, 3)])
    a = rng.randint(3, 9)
    b = rng.randint(4, 12)
    side = F(a) * k
    return _either(rng, 'Geometry and Trigonometry', 'Lines, angles and triangles', 'Triangle ABC is similar to triangle DEF, where AB corresponds to DE and BC corresponds to EF. AB = %d, BC = %d and DE = %s. What is the length of EF?' % (a, b, fmt(side)),
                   F(b) * k, [F(b) + (side - a), F(b) * a / side, F(b) * k + 1], 'The scale factor is DE/AB = %s/%d = %s, so EF = %d × %s = %s.' % (fmt(side), a, fmt(k), b, fmt(k), fmt(F(b) * k)), 2)


def cylinder(rng):
    r, h = rng.choice([2, 3, 4, 5, 6]), rng.choice([5, 7, 8, 10, 12])
    return _mcq(rng, 'Geometry and Trigonometry', 'Area and volume', 'A cylinder has a radius of %d centimeters and a height of %d centimeters. What is its volume, in cubic centimeters? (Give the answer in terms of π.)' % (r, h), r * r * h, [2 * r * h, r * h, r * r * h * 2],
                'πr²h = π(%d)²(%d) = %dπ.' % (r, h, r * r * h), 1, f=lambda v: '%sπ' % fmt(v))


def angles(rng):
    a = rng.randint(25, 65)
    b = rng.randint(30, 70)
    ans = 180 - a - b
    return _either(rng, 'Geometry and Trigonometry', 'Lines, angles and triangles', 'In triangle PQR, the measure of angle P is %d° and the measure of angle Q is %d°. What is the measure, in degrees, of angle R?' % (a, b), ans, [a + b, 90 - a, 360 - a - b],
                   'The angles of a triangle add to 180°, so R = 180 - %d - %d = %d°.' % (a, b, ans), 1)


def circle_eq(rng):
    h, k, r = rng.randint(-6, 7), rng.randint(-6, 7), rng.randint(2, 9)
    ask = rng.choice(['radius', 'x'])
    eq = '(x %s %d)² + (y %s %d)² = %d' % ('-' if h >= 0 else '+', abs(h), '-' if k >= 0 else '+', abs(k), r * r)
    if ask == 'radius':
        return _either(rng, 'Geometry and Trigonometry', 'Circles', 'The equation %s represents a circle in the xy-plane. What is the radius of the circle?' % eq, r, [r * r, F(r, 2), r + h], 'The standard form is (x - h)² + (y - k)² = r², so r² = %d and r = %d.' % (r * r, r), 2)
    return _either(rng, 'Geometry and Trigonometry', 'Circles', 'The equation %s represents a circle in the xy-plane. What is the x-coordinate of the center of the circle?' % eq, h, [-h, k, r], 'The center is (h, k) = (%d, %d), so the x-coordinate is %d.' % (h, k, h), 2)


FAMILIES = {
    'lin1': lin1, 'linw': lin_word, 'sys2': system2, 'ineq': ineq, 'slope': slope2, 'dep': lambda rng: _no_solution_item(rng, rng.randint(2, 8), rng.randint(1, 9)),
    'quad': quad_sum, 'qmin': quad_min, 'expo': expo, 'exps': exponents, 'comp': compose, 'rad': radical_eq, 'zero': zero_k,
    'pct': pct_change, 'rate': rate_conv, 'mean': mean_missing, 'prob': prob_table, 'fit': best_fit, 'pcts': two_way_pct,
    'rect': rect_comp, 'sect': circle_sector, 'pyth': pyth, 'trig': trig_ratio, 'simi': similar, 'cyl': cylinder, 'ang': angles, 'ceq': circle_eq,
}
BY_DOMAIN = {d: [] for d in DOMAINS}


def build(family, seed):
    """The question for 'g:<family>:<seed>' (same id, same question)."""
    rng = random.Random('%s-%s' % (family, seed))
    q = FAMILIES[family](rng)
    q = dict(q)
    q['id'] = 'g:%s:%d' % (family, seed)
    q['family'] = family
    return q


def from_id(qid):
    try:
        _, fam, seed = qid.split(':')
        return build(fam, int(seed)) if fam in FAMILIES else None
    except (ValueError, KeyError):
        return None


def family_domain(family):
    return build(family, 1)['domain']


for _k in FAMILIES:
    BY_DOMAIN[family_domain(_k)].append(_k)


def pick(domain, rng):
    """A fresh 'g:' id from a domain."""
    fam = rng.choice(BY_DOMAIN[domain])
    return 'g:%s:%d' % (fam, rng.randint(1, 10 ** 6))


def parse_response(text):
    """A student-produced response as an exact number, or None when it is not a number. Accepts integers, decimals, '.5', '-3' and fractions such as '3/4'."""
    t = (text or '').strip().replace(' ', '').replace(',', '')
    if not t or len(t) > 12:
        return None
    try:
        if '/' in t:
            a, b = t.split('/')
            return F(int(a), int(b)) if int(b) != 0 else None
        return F(t)
    except (ValueError, ZeroDivisionError):
        return None


def is_correct(q, response):
    if q.get('kind') == 'spr':
        v = parse_response(response)
        return v is not None and v == F(q['ans_text'])
    return response == q['ans']
