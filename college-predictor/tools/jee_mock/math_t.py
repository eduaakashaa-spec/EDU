"""Mathematics templates. Chapter codes: CNQ complex & quadratics, SEQ sequences, PNC permutations/combinations/binomial, MAT matrices,
LCD limits & derivatives, INT integrals, DEQ differential equations, COG coordinate geometry, VEC vectors & 3D, STP statistics & probability,
TRG trigonometry, SRF sets-relations-functions."""
import itertools
import math
from fractions import Fraction

from kit import Item, distinct, n, sgn, sub, sup, tpl

M = 'MATH'


@tpl(M, 'CNQ')
def sum_sq_roots(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    while a == b:
        b = r.randint(1, 9)
    p, q = a + b, a * b
    ans = a * a + b * b
    return Item('If &alpha; and &beta; are the roots of x<sup>2</sup> − %dx + %d = 0, then &alpha;<sup>2</sup> + &beta;<sup>2</sup> is equal to' % (p, q), ans,
                distinct(ans, [p * p + 2 * q, p * p - q, p * p - 4 * q, p * p], 1),
                ['Sum of roots = %d and product = %d.' % (p, q), '&alpha;<sup>2</sup> + &beta;<sup>2</sup> = (&alpha; + &beta;)<sup>2</sup> − 2&alpha;&beta; = %d − %d = %d.' % (p * p, 2 * q, ans)],
                'Using +2&alpha;&beta; instead of −2&alpha;&beta;.', nat=ans)


@tpl(M, 'CNQ')
def modulus_product(r):
    a, b, c, d = [r.randint(1, 6) for _ in range(4)]
    ans = (a * a + b * b) * (c * c + d * d)
    return Item('For z<sub>1</sub> = %d + %di and z<sub>2</sub> = %d + %di, the value of |z<sub>1</sub>z<sub>2</sub>|<sup>2</sup> is' % (a, b, c, d), ans,
                distinct(ans, [(a * a + b * b) + (c * c + d * d), (a * c + b * d) ** 2, (a * c - b * d) ** 2 + 1], 3),
                ['|z<sub>1</sub>z<sub>2</sub>| = |z<sub>1</sub>||z<sub>2</sub>|, so |z<sub>1</sub>z<sub>2</sub>|<sup>2</sup> = |z<sub>1</sub>|<sup>2</sup>|z<sub>2</sub>|<sup>2</sup>.',
                 '= (%d + %d)(%d + %d) = %d.' % (a * a, b * b, c * c, d * d, ans)], 'Adding the squared moduli instead of multiplying.', nat=ans)


@tpl(M, 'CNQ', nat=False)
def sum_powers_i(r):
    k = r.randint(5, 60)
    rem = k % 4
    ans = {0: '0', 1: 'i', 2: 'i − 1', 3: '−1'}[rem]
    opts = {'0', 'i', 'i − 1', '−1', '1', '−i'}
    wrong = [o for o in ['0', 'i', 'i − 1', '−1', '1', '−i'] if o != ans]
    return Item('The value of i + i<sup>2</sup> + i<sup>3</sup> + &hellip; + i<sup>%d</sup> is' % k, ans, wrong[:3] if rem not in (1, 2) else [w for w in wrong if w not in ('1',)][:3],
                ['Every block of four consecutive powers of i adds up to 0.', '%d = 4 × %d + %d, so only the last %d term(s) remain.' % (k, k // 4, rem, rem),
                 'Remaining sum = %s.' % ans], 'Forgetting that i + i<sup>2</sup> + i<sup>3</sup> + i<sup>4</sup> = 0.')


@tpl(M, 'SEQ')
def ap_sum(r):
    a, d, m = r.randint(2, 9), r.randint(2, 6), r.choice([10, 12, 15, 20])
    ans = m * (2 * a + (m - 1) * d) // 2
    return Item('The sum of the first %d terms of the arithmetic progression %d, %d, %d, &hellip; is' % (m, a, a + d, a + 2 * d), ans,
                distinct(ans, [m * (2 * a + m * d) // 2, m * (a + (m - 1) * d), m * (2 * a + (m - 2) * d) // 2], 2),
                ['a = %d, d = %d, n = %d.' % (a, d, m), 'S<sub>n</sub> = n/2 [2a + (n − 1)d] = %d/2 × [%d + %d] = %d.' % (m, 2 * a, (m - 1) * d, ans)],
                'Using nd instead of (n − 1)d.', nat=ans)


@tpl(M, 'SEQ')
def gp_sum(r):
    a, q, m = r.randint(1, 5), r.choice([2, 3]), r.randint(4, 6)
    ans = a * (q ** m - 1) // (q - 1)
    return Item('The sum of the first %d terms of the geometric progression %d, %d, %d, &hellip; is' % (m, a, a * q, a * q * q), ans,
                distinct(ans, [a * (q ** (m + 1) - 1) // (q - 1), a * (q ** m), a * (q ** m - 1)], 3),
                ['a = %d, r = %d, n = %d.' % (a, q, m), 'S<sub>n</sub> = a(r<sup>n</sup> − 1)/(r − 1) = %d(%d − 1)/%d = %d.' % (a, q ** m, q - 1, ans)],
                'Using r<sup>n+1</sup> instead of r<sup>n</sup>.', nat=ans)


@tpl(M, 'SEQ')
def sn_to_term(r):
    A, B, k = r.randint(1, 5), r.randint(1, 6), r.randint(5, 12)
    ans = A * (2 * k - 1) + B
    return Item('If the sum of the first n terms of a sequence is S<sub>n</sub> = %sn<sup>2</sup> + %dn, the %s term is' % (n(A), B, '%d<sup>th</sup>' % k), ans,
                distinct(ans, [A * k * k + B * k, A * (2 * k + 1) + B, A * (2 * k - 1)], 2),
                ['T<sub>k</sub> = S<sub>k</sub> − S<sub>k−1</sub>.', 'S<sub>k</sub> − S<sub>k−1</sub> = %d[k<sup>2</sup> − (k − 1)<sup>2</sup>] + %d = %d(2k − 1) + %d.' % (A, B, A, B),
                 'For k = %d this is %d.' % (k, ans)], 'Taking T<sub>k</sub> = S<sub>k</sub>.', nat=ans)


@tpl(M, 'PNC')
def word_arrangements(r):
    words = ['LEVEL', 'BANANA', 'ALLAHABAD', 'MISSISSIPPI', 'COMMITTEE', 'SUCCESS', 'PEPPER', 'INDIA', 'APPLE', 'BALLOON', 'ARRANGE', 'STATISTICS']
    w = r.choice(words)
    from collections import Counter
    c = Counter(w)
    ans = math.factorial(len(w))
    for v in c.values():
        ans //= math.factorial(v)
    rep = ' '.join('%s×%d' % (k, v) for k, v in c.items() if v > 1)
    return Item('The number of distinct arrangements of all the letters of the word %s is' % w, ans,
                distinct(ans, [math.factorial(len(w)), ans * 2, ans // 2 if ans % 2 == 0 else ans + 7], max(1, ans // 10)),
                ['The word has %d letters. Repeated letters: %s.' % (len(w), rep), 'Arrangements = %d!/(product of factorials of repeats) = %d.' % (len(w), ans)],
                'Not dividing by the factorial of each repeated letter.', nat=ans if ans < 99999 else None)


@tpl(M, 'PNC')
def committee(r):
    m, w, k = r.randint(4, 7), r.randint(3, 6), r.randint(3, 4)
    tot = math.comb(m + w, k)
    ans = tot - math.comb(m, k)
    return Item('A committee of %d is chosen from %d men and %d women. The number of committees containing at least one woman is' % (k, m, w), ans,
                distinct(ans, [tot, math.comb(m, k) * w, math.comb(w, 1) * math.comb(m + w - 1, k - 1)], 5),
                ['Total committees = C(%d, %d) = %d.' % (m + w, k, tot), 'Committees with no woman = C(%d, %d) = %d.' % (m, k, math.comb(m, k)), 'Required = %d − %d = %d.' % (tot, math.comb(m, k), ans)],
                'Counting a committee with two women twice (choose one woman, then anyone).', nat=ans)


@tpl(M, 'PNC')
def binomial_term(r):
    N = r.choice([6, 9, 12])
    j = r.randint(1, N - 1)
    a, b = r.randint(1, 3), r.randint(1, 3)
    k = 2 * N - 3 * j
    ans = math.comb(N, j) * a ** (N - j) * b ** j
    return Item('In the expansion of (%sx<sup>2</sup> + %s/x)<sup>%d</sup>, the coefficient of x<sup>%d</sup> is' % ('' if a == 1 else a, b, N, k), ans,
                distinct(ans, [math.comb(N, j), math.comb(N, j + 1) * a ** (N - j - 1) * b ** (j + 1), math.comb(N, j) * a ** j * b ** (N - j)], max(1, ans // 8)),
                ['General term: T<sub>j+1</sub> = C(%d, j)(%sx<sup>2</sup>)<sup>%d−j</sup>(%s/x)<sup>j</sup>.' % (N, a, N, b), 'Power of x: 2(%d − j) − j = %d, so j = %d.' % (N, k, j),
                 'Coefficient = C(%d, %d) × %d<sup>%d</sup> × %d<sup>%d</sup> = %d.' % (N, j, a, N - j, b, j, ans)], 'Swapping the powers of the two constants.', nat=ans if ans < 99999 else None)


@tpl(M, 'PNC')
def stars_bars(r):
    balls, boxes = r.randint(5, 9), r.randint(3, 5)
    ans = math.comb(balls + boxes - 1, boxes - 1)
    return Item('The number of ways of distributing %d identical balls into %d different boxes (a box may stay empty) is' % (balls, boxes), ans,
                distinct(ans, [boxes ** balls, math.comb(balls - 1, boxes - 1), math.comb(balls + boxes, boxes)], 3),
                ['Number of non-negative solutions of x<sub>1</sub> + &hellip; + x<sub>%d</sub> = %d is C(%d + %d − 1, %d − 1).' % (boxes, balls, balls, boxes, boxes), '= C(%d, %d) = %d.' % (balls + boxes - 1, boxes - 1, ans)],
                'Using %d<sup>%d</sup> (that is for different balls).' % (boxes, balls), nat=ans)


def _det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


@tpl(M, 'MAT')
def det3(r):
    while True:
        m = [[r.randint(-3, 4) for _ in range(3)] for _ in range(3)]
        d = _det3(m)
        if 2 <= d <= 60:
            break
    rows = ' &nbsp; '.join('[%s]' % ' '.join(sgn(x) for x in row) for row in m)
    return Item('The determinant of the matrix with rows %s is' % rows, d,
                distinct(d, [-d, d + 4, d - 6], 3), ['Expand along the first row: a(ei − fh) − b(di − fg) + c(dh − eg).', 'Evaluating gives %d.' % d],
                'Sign slip on the middle term of the expansion.', nat=d)


@tpl(M, 'MAT')
def det_scaling(r):
    nn, dA, kk = r.choice([2, 3]), r.randint(2, 5), r.randint(2, 4)
    kind = r.choice(['scale', 'adj'])
    if kind == 'scale':
        ans = kk ** nn * dA
        return Item('If A is a %d × %d matrix with det A = %d, then det(%dA) equals' % (nn, nn, dA, kk), ans, distinct(ans, [kk * dA, kk ** (nn - 1) * dA, dA ** nn], 2),
                    ['det(kA) = k<sup>n</sup> det A for an n × n matrix.', '= %d<sup>%d</sup> × %d = %d.' % (kk, nn, dA, ans)], 'Multiplying det A by k only once.', nat=ans)
    ans = dA ** (nn - 1)
    return Item('If A is a %d × %d matrix with det A = %d, then det(adj A) equals' % (nn, nn, dA), ans, distinct(ans, [dA, dA ** nn, dA ** (nn + 1)], 1),
                ['det(adj A) = (det A)<sup>n−1</sup>.', '= %d<sup>%d</sup> = %d.' % (dA, nn - 1, ans)], 'Using (det A)<sup>n</sup>.', nat=ans)


@tpl(M, 'MAT')
def matrix_power(r):
    a, p = r.randint(1, 4), r.randint(3, 9)
    ans = 2 + a * p
    return Item('If A = [[1, %d], [0, 1]], the sum of all the entries of A<sup>%d</sup> is' % (a, p), ans, distinct(ans, [2 + a, 2 + a * p + a, a ** p + 2], 1),
                ['A<sup>k</sup> = [[1, ka], [0, 1]] (prove by induction).', 'A<sup>%d</sup> = [[1, %d], [0, 1]], whose entries add up to 2 + %d = %d.' % (p, a * p, a * p, ans)],
                'Computing A<sup>p</sup> as entrywise powers.', nat=ans)


@tpl(M, 'LCD')
def limit_power(r):
    m, a = r.randint(2, 5), r.randint(1, 3)
    ans = m * a ** (m - 1)
    return Item('lim<sub>x&rarr;%d</sub> (x<sup>%d</sup> − %d)/(x − %d) equals' % (a, m, a ** m, a), ans, distinct(ans, [a ** (m - 1), m * a ** m, m * a ** (m - 2) if a > 0 else 0], 2),
                ['The limit is the derivative of x<sup>%d</sup> at x = %d.' % (m, a), 'm a<sup>m−1</sup> = %d × %d<sup>%d</sup> = %d.' % (m, a, m - 1, ans)], 'Writing a<sup>m</sup> instead of a<sup>m−1</sup>.', nat=ans)


@tpl(M, 'LCD', nat=False)
def limit_sin(r):
    p, q = r.randint(1, 7), r.randint(2, 9)
    while math.gcd(p, q) != 1 or p == q:
        p, q = r.randint(1, 7), r.randint(2, 9)
    ans = Fraction(p, q)
    return Item('lim<sub>x&rarr;0</sub> sin(%dx)/(%dx) equals' % (p, q), n(ans), [n(Fraction(q, p)), '1', '0'],
                ['sin(kx)/x &rarr; k as x &rarr; 0.', 'Hence the limit is %d/%d.' % (p, q)], 'Inverting the ratio.')


@tpl(M, 'LCD')
def derivative_value(r):
    a, b, c, x0 = r.randint(1, 4), r.randint(-4, 5), r.randint(-5, 6), r.randint(1, 4)
    ans = 3 * a * x0 * x0 + 2 * b * x0 + c
    if ans < 1:
        c += abs(ans) + 3
        ans = 3 * a * x0 * x0 + 2 * b * x0 + c
    return Item('If f(x) = %sx<sup>3</sup> %s %sx<sup>2</sup> %s %sx, then f&prime;(%d) equals' % ('' if a == 1 else a, '+' if b >= 0 else '−', n(abs(b)), '+' if c >= 0 else '−', n(abs(c)), x0), ans,
                distinct(ans, [a * x0 ** 3 + b * x0 ** 2 + c * x0, ans + a, ans - b], 2),
                ['f&prime;(x) = %dx<sup>2</sup> + %dx + %d.' % (3 * a, 2 * b, c), 'At x = %d: %d + %d + %d = %d.' % (x0, 3 * a * x0 * x0, 2 * b * x0, c, ans)], 'Evaluating f instead of f&prime;.', nat=ans)


def _maxq(a, h, k):
    # f(x) = -a x^2 + 2ah x + (k - a h^2) wrong sign fix: -a(x-h)^2 + k = -a x^2 + 2ah x + (k - a h^2)
    b, c = 2 * a * h, k - a * h * h
    ans = k
    cs = ('+ %d' % c) if c >= 0 else ('− %d' % -c)
    return Item('The maximum value of f(x) = −%sx<sup>2</sup> + %dx %s is' % ('' if a == 1 else a, b, cs), ans, distinct(ans, [c, b, k + a * h * h], 2),
                ['f(x) = −%s(x − %d)<sup>2</sup> + %d after completing the square.' % ('' if a == 1 else a, h, k), 'The maximum occurs at x = %d and equals %d.' % (h, k)],
                'Reading the constant term %d as the maximum.' % c, nat=ans)


@tpl(M, 'LCD')
def maxq(r):
    return _maxq(r.randint(1, 3), r.randint(1, 6), r.randint(2, 20))


@tpl(M, 'INT')
def definite_integral(r):
    while True:
        a, b, k = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
        v = Fraction(a * k ** 3, 3) + Fraction(b * k ** 2, 2)
        if v.denominator == 1:
            break
    ans = int(v)
    return Item('The value of the integral &int;<sub>0</sub><sup>%d</sup> (%sx<sup>2</sup> + %dx) dx is' % (k, '' if a == 1 else a, b), ans,
                distinct(ans, [a * k ** 2 + b * k, a * k ** 3 + b * k ** 2, ans + k], 2),
                ['Antiderivative: %sx<sup>3</sup>/3 + %dx<sup>2</sup>/2.' % ('' if a == 1 else a, b), 'At x = %d: %s + %s = %d.' % (k, n(Fraction(a * k ** 3, 3)), n(Fraction(b * k ** 2, 2)), ans)],
                'Dropping the 1/3 or 1/2 factor.', nat=ans)


@tpl(M, 'INT')
def area_parabola_line(r):
    k = r.choice([6, 12, 18])
    ans = k ** 3 // 6
    return Item('The area (in square units) of the region bounded by y = x<sup>2</sup> and y = %dx is' % k, ans, distinct(ans, [k ** 3 // 3, k ** 2 // 2, k ** 3 // 4], 6),
                ['The curves meet at x = 0 and x = %d.' % k, 'Area = &int;<sub>0</sub><sup>%d</sup> (%dx − x<sup>2</sup>) dx = %d·%d<sup>2</sup>/2 − %d<sup>3</sup>/3 = %d.' % (k, k, k, k, k, ans)],
                'Forgetting to subtract the area under the parabola.', nat=ans)


@tpl(M, 'DEQ')
def order_degree(r):
    p, q = r.randint(2, 4), r.randint(2, 4)
    kind = r.choice([0, 1])
    if kind == 0:
        stem = 'The sum of the order and the degree of the differential equation (d<sup>2</sup>y/dx<sup>2</sup>)<sup>%d</sup> + (dy/dx)<sup>%d</sup> = x is' % (p, q)
        order, degree = 2, p
    else:
        stem = 'The sum of the order and the degree of the differential equation d<sup>3</sup>y/dx<sup>3</sup> + (dy/dx)<sup>%d</sup> + y<sup>%d</sup> = 0 is' % (q, p)
        order, degree = 3, 1
    ans = order + degree
    return Item(stem, ans, distinct(ans, [order * degree, ans + 1, ans - 1, q + order], 1), ['Order = highest derivative present = %d.' % order,
                'Degree = power of that highest derivative once the equation is a polynomial in derivatives = %d.' % degree, 'Sum = %d.' % ans], 'Taking the largest power anywhere as the degree.', nat=ans)


@tpl(M, 'DEQ')
def exp_growth(r):
    k, y0, m = r.randint(2, 5), r.randint(2, 7), r.choice([2, 3, 4, 5])
    ans = y0 * m
    return Item('If dy/dx = %dy with y(0) = %d, then y(ln %d / %d) equals' % (k, y0, m, k), ans, distinct(ans, [y0 * k, y0 + m, y0 * m * k], y0),
                ['Solution: y = %d e<sup>%dx</sup>.' % (y0, k), 'At x = ln %d/%d: e<sup>ln %d</sup> = %d, so y = %d × %d = %d.' % (m, k, m, m, y0, m, ans)], 'Evaluating e<sup>kx</sup> as x instead of e<sup>ln m</sup> = m.', nat=ans)


@tpl(M, 'COG')
def point_line_distance(r):
    a, b = r.choice([(3, 4), (5, 12), (8, 15), (6, 8)])
    h = int(math.hypot(a, b))
    x1, y1 = r.randint(-5, 8), r.randint(-5, 8)
    t = r.randint(1, 5)
    c = t * h - a * x1 - b * y1
    ans = t
    cs = ('+ %d' % c) if c >= 0 else ('− %d' % -c)
    return Item('The distance of the point (%d, %d) from the line %dx + %dy %s = 0 is' % (x1, y1, a, b, cs), ans, distinct(ans, [t * h, t * h // 2 if t % 2 == 0 else t + 1, t + 2], 1),
                ['Distance = |ax<sub>1</sub> + by<sub>1</sub> + c|/√(a<sup>2</sup> + b<sup>2</sup>).', 'Numerator = %d, denominator = √(%d + %d) = %d.' % (t * h, a * a, b * b, h), 'Distance = %d/%d = %d.' % (t * h, h, t)],
                'Forgetting to divide by √(a<sup>2</sup> + b<sup>2</sup>).', nat=ans)


@tpl(M, 'COG')
def circle_radius(r):
    g, f, rad = r.randint(1, 6), r.randint(1, 6), r.randint(2, 9)
    c = g * g + f * f - rad * rad
    cs = ('+ %d' % c) if c >= 0 else ('− %d' % -c)
    ans = rad
    return Item('The radius of the circle x<sup>2</sup> + y<sup>2</sup> − %dx − %dy %s = 0 is' % (2 * g, 2 * f, cs), ans, distinct(ans, [rad * rad, g + f, abs(c)], 1),
                ['Compare with x<sup>2</sup> + y<sup>2</sup> + 2gx + 2fy + c = 0: g = −%d, f = −%d, c = %d.' % (g, f, c), 'r = √(g<sup>2</sup> + f<sup>2</sup> − c) = √(%d) = %d.' % (rad * rad, rad)],
                'Reporting r<sup>2</sup> instead of r.', nat=ans)


@tpl(M, 'COG')
def foci_distance(r):
    a, b, c = r.choice([(5, 3, 4), (13, 5, 12), (10, 6, 8), (17, 8, 15), (25, 7, 24), (15, 9, 12)])
    ans = 2 * c
    return Item('The distance between the foci of the ellipse x<sup>2</sup>/%d + y<sup>2</sup>/%d = 1 is' % (a * a, b * b), ans, distinct(ans, [c, 2 * b, 2 * a], 2),
                ['a<sup>2</sup> = %d, b<sup>2</sup> = %d so c<sup>2</sup> = a<sup>2</sup> − b<sup>2</sup> = %d, c = %d.' % (a * a, b * b, c * c, c), 'Distance between foci = 2c = %d.' % ans], 'Giving c instead of 2c.', nat=ans)


@tpl(M, 'VEC')
def cross_magnitude_sq(r):
    while True:
        u = [r.randint(-3, 4) for _ in range(3)]
        v = [r.randint(-3, 4) for _ in range(3)]
        dot = sum(x * y for x, y in zip(u, v))
        uu, vv = sum(x * x for x in u), sum(x * x for x in v)
        ans = uu * vv - dot * dot
        if 1 <= ans <= 200:
            break
    f = lambda w: '%si %sj %sk' % (sgn(w[0]), ('+' if w[1] >= 0 else '−') + n(abs(w[1])), ('+' if w[2] >= 0 else '−') + n(abs(w[2])))
    return Item('For the vectors a = %s and b = %s, |a × b|<sup>2</sup> equals' % (f(u), f(v)), ans, distinct(ans, [uu * vv, uu * vv + dot * dot, ans + 2 * abs(dot) + 1], 3),
                ['|a × b|<sup>2</sup> = |a|<sup>2</sup>|b|<sup>2</sup> − (a·b)<sup>2</sup>.', '|a|<sup>2</sup> = %d, |b|<sup>2</sup> = %d, a·b = %d.' % (uu, vv, dot), '%d × %d − %d = %d.' % (uu, vv, dot * dot, ans)],
                'Using + (a·b)<sup>2</sup>.', nat=ans)


@tpl(M, 'VEC')
def point_plane_distance(r):
    a, b, c, h = r.choice([(2, 3, 6, 7), (1, 2, 2, 3), (4, 4, 7, 9), (2, 6, 9, 11), (2, 1, 2, 3), (3, 4, 12, 13)])
    x1, y1, z1 = r.randint(-3, 5), r.randint(-3, 5), r.randint(-3, 5)
    t = r.randint(1, 4)
    d = t * h - (a * x1 + b * y1 + c * z1)
    ds = ('+ %d' % d) if d >= 0 else ('− %d' % -d)
    return Item('The distance of the point (%d, %d, %d) from the plane %dx + %dy + %dz %s = 0 is' % (x1, y1, z1, a, b, c, ds), t, distinct(t, [t * h, t + 1, t * h // 2 if (t * h) % 2 == 0 else t + 3], 1),
                ['Distance = |ax<sub>1</sub> + by<sub>1</sub> + cz<sub>1</sub> + d|/√(a<sup>2</sup> + b<sup>2</sup> + c<sup>2</sup>).', 'Numerator = %d, denominator = √%d = %d.' % (t * h, a * a + b * b + c * c, h), 'Distance = %d.' % t],
                'Forgetting the square-root denominator.', nat=t)


@tpl(M, 'STP', nat=False)
def prob_union(r):
    den = r.choice([12, 20, 24])
    pa, pb = r.randint(3, den // 2), r.randint(3, den // 2)
    pab = r.randint(1, min(pa, pb) - 1)
    ans = Fraction(pa + pb - pab, den)
    return Item('If P(A) = %s, P(B) = %s and P(A &cap; B) = %s, then P(A &cup; B) is' % (n(Fraction(pa, den)), n(Fraction(pb, den)), n(Fraction(pab, den))), n(ans),
                [n(Fraction(pa + pb, den)), n(Fraction(pa + pb + pab, den)), n(Fraction(pa + pb - 2 * pab, den))], ['P(A &cup; B) = P(A) + P(B) − P(A &cap; B).', '= (%d + %d − %d)/%d = %s.' % (pa, pb, pab, den, n(ans))],
                'Forgetting to subtract the overlap.')


@tpl(M, 'STP')
def binomial_params(r):
    nn = r.choice([9, 12, 16, 18, 20, 24])
    p = r.choice([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4)])
    if (nn * p).denominator != 1:
        nn = nn * p.denominator
    mean, var = nn * p, nn * p * (1 - p)
    return Item('For a binomial distribution the mean is %s and the variance is %s. The number of trials n is' % (n(mean), n(var)), nn, distinct(nn, [int(mean), int(mean + var), int(mean * 2)], 2),
                ['Mean = np and variance = npq, so q = variance/mean = %s and p = %s.' % (n(var / mean), n(1 - var / mean)), 'n = mean/p = %s/%s = %d.' % (n(mean), n(1 - var / mean), nn)],
                'Taking n = mean or n = mean + variance.', nat=nn)


@tpl(M, 'STP', nat=False)
def cond_prob_dice(r):
    s = r.choice([7, 8, 9, 10])
    k = r.choice([2, 3, 4, 5])
    space = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    given = [(i, j) for i, j in space if i == k or j == k]
    both = [(i, j) for i, j in given if i + j == s]
    ans = Fraction(len(both), len(given))
    wrong = [Fraction(len(both), 36), Fraction(len([1 for i, j in space if i + j == s]), 36), Fraction(len(both) + 1, len(given))]
    return Item('Two fair dice are thrown. The probability that the sum is %d given that at least one die shows %d is' % (s, k), n(ans), [n(w) for w in wrong],
                ['Outcomes with at least one %d: %d (out of 36).' % (k, len(given)), 'Of these, the sum is %d in %d cases.' % (s, len(both)), 'P = %d/%d = %s.' % (len(both), len(given), n(ans))],
                'Dividing by 36 instead of by the reduced sample space.')


@tpl(M, 'TRG')
def num_solutions(r):
    kind = r.choice([('sin 2x = 0', 5), ('sin 2x = 1', 2), ('cos 2x = 0', 4), ('sin x = 1/2', 2), ('cos 3x = 1', 4), ('sin 3x = 0', 7), ('tan x = 1', 2)])
    eq, ans = kind
    return Item('The number of solutions of %s in the interval [0, 2&pi;] is' % eq, ans, distinct(ans, [ans + 1, ans - 1, ans * 2], 1),
                ['Write the general solution and count the values of x that fall in [0, 2&pi;], including both end points.', 'Counting gives %d solutions.' % ans], 'Missing an end point of the closed interval.', nat=ans)


@tpl(M, 'TRG', nat=False)
def tan_sum(r):
    a, b = Fraction(1, r.randint(2, 5)), Fraction(1, r.randint(2, 6))
    ans = (a + b) / (1 - a * b)
    return Item('If tan A = %s and tan B = %s, then tan(A + B) is' % (n(a), n(b)), n(ans), [n(a + b), n((a - b) / (1 + a * b)), n(a * b)],
                ['tan(A + B) = (tan A + tan B)/(1 − tan A tan B).', '= (%s + %s)/(1 − %s) = %s.' % (n(a), n(b), n(a * b), n(ans))], 'Using + in the denominator.')


@tpl(M, 'SRF')
def count_functions(r):
    mm, nn = r.randint(2, 4), r.randint(4, 7)
    kind = r.choice(['onetoone', 'refl', 'sym'])
    if kind == 'onetoone':
        ans = math.perm(nn, mm)
        return Item('The number of one-one functions from a set with %d elements to a set with %d elements is' % (mm, nn), ans, distinct(ans, [nn ** mm, mm ** nn, math.comb(nn, mm)], 5),
                    ['The first element has %d images, the next %d, and so on.' % (nn, nn - 1), 'Total = P(%d, %d) = %d.' % (nn, mm, ans)], 'Using n<sup>m</sup> (all functions, not only one-one).', nat=ans)
    k = r.randint(2, 4)
    if kind == 'refl':
        ans = 2 ** (k * (k - 1))
        return Item('The number of reflexive relations on a set with %d elements is' % k, ans, distinct(ans, [2 ** (k * k), 2 ** (k * (k + 1) // 2), 2 ** k], 7), ['Each of the %d diagonal pairs must be present.' % k,
                    'The other %d pairs are free: 2<sup>%d</sup> = %d relations.' % (k * (k - 1), k * (k - 1), ans)], 'Counting all 2<sup>k<sup>2</sup></sup> relations.', nat=ans)
    ans = 2 ** (k * (k + 1) // 2)
    return Item('The number of symmetric relations on a set with %d elements is' % k, ans, distinct(ans, [2 ** (k * k), 2 ** (k * (k - 1)), 2 ** (k * (k - 1) // 2)], 7),
                ['A symmetric relation is fixed by choosing among the %d diagonal pairs and the %d unordered off-diagonal pairs.' % (k, k * (k - 1) // 2), 'Total = 2<sup>%d</sup> = %d.' % (k * (k + 1) // 2, ans)], 'Ignoring the diagonal pairs.', nat=ans)
