"""EduPulse-Explorer: question generators for maths and reasoning (Grades 7 to 10).

Every generator takes a seed and returns one question whose answer is computed, so a student never meets the same numbers twice and the key is always right.
A generated question has the id  g:<generator>:<seed>  and can be rebuilt from that id alone, so the server marks it without keeping the paper.
Question dict: sec, topic, grade ('7-8' | '9-10' | 'all'), diff (1-3), fam (exam families), q, opts (4 strings), ans, why, style.
"""
import random
from fractions import Fraction

FAM_APT = ['APT']
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _opts(rng, right, wrongs, fmt=str):
    """Four distinct options with the right one placed at random. `wrongs` are candidate distractors in order of preference."""
    seen = {fmt(right)}
    out = [fmt(right)]
    for w in wrongs:
        s = fmt(w)
        if s not in seen and len(out) < 4:
            seen.add(s)
            out.append(s)
    k = 1
    while len(out) < 4:                                          # pad with near values
        if not isinstance(right, (int, float, Fraction)) or k > 50:
            raise ValueError('not enough distinct options')
        s = fmt(right + k)
        k += 1
        if s not in seen:
            seen.add(s)
            out.append(s)
    order = list(range(4))
    rng.shuffle(order)
    return [out[i] for i in order], order.index(0)


def _mk(sec, topic, grade, diff, fam, q, opts, ans, why, style):
    return {'sec': sec, 'topic': topic, 'grade': grade, 'diff': diff, 'fam': fam, 'q': q, 'opts': opts, 'ans': ans, 'why': why, 'style': style}


def _g(x):
    return ('%g' % x)


# ---- MAT ---------------------------------------------------------------------------------------------------------------------------------
def percent_change(rng):
    base = rng.choice([40, 50, 60, 80, 120, 150, 200, 250, 400])
    up = rng.choice([10, 20, 25, 30, 40, 50])
    dn = rng.choice([10, 20, 25, 50])
    after_up = base * (100 + up) / 100
    final = after_up * (100 - dn) / 100
    net = round((final - base) / base * 100, 1)
    q = 'The price of a sketch pad is Rs %d. It rises by %d%% and then falls by %d%% of the new price. What is the final price (in Rs)?' % (base, up, dn)
    w = [base, base * (100 + up - dn) / 100, after_up, base * (100 - dn) / 100]
    o, a = _opts(rng, final, w, _g)
    return _mk('MAT', 'Maths: percentages', '7-8', 2, ['JEE', 'APT'], q, o, a,
               'After the rise the price is %g. A fall of %d%% is taken on this new price, giving %g. Taking the two changes as +%d-%d = %+d%% of the original is the common slip (net change is %g%%).' % (after_up, dn, final, up, dn, up - dn, net),
               'Exams chain two percentage changes and tempt you to add them.')


def ratio_share(rng):
    a, b, c = sorted(rng.sample(range(1, 8), 3))
    k = rng.choice([4, 5, 6, 8, 10, 12])
    total = (a + b + c) * k
    q = 'Three friends share Rs %d in the ratio %d : %d : %d. How many rupees does the one with the largest share get?' % (total, a, b, c)
    right = c * k
    w = [b * k, total * c // (a + b + c + 1), total // 3, (c + 1) * k]
    o, a_ = _opts(rng, right, w)
    return _mk('MAT', 'Maths: ratio and proportion', '7-8', 1, ['JEE', 'APT'], q, o, a_,
               'The ratio has %d+%d+%d = %d parts. One part is %d/%d = %d. The largest share has %d parts: %d x %d = %d.' % (a, b, c, a + b + c, total, a + b + c, k, c, c, k, right),
               'Share-in-a-ratio questions: find one part first.')


def speed_time(rng):
    v1 = rng.choice([30, 40, 45, 50, 60, 72])
    t = rng.choice([2, 3, 4, 5])
    v2 = rng.choice([x for x in [20, 24, 30, 36, 40, 45, 60] if x != v1])
    d = v1 * t
    right = Fraction(d, v2)
    q = 'A bus covers %d km at %d km/h. At %d km/h, how long would the same journey take (in hours)?' % (d, v1, v2)
    fmt = lambda x: _g(float(x)) if isinstance(x, Fraction) else _g(x)
    w = [Fraction(v2 * t, v1), Fraction(d, v1 + v2), Fraction(v1, v2) * 1, t]
    o, a = _opts(rng, right, w, lambda x: _g(round(float(x), 2)))
    return _mk('MAT', 'Maths: speed, distance and time', '7-8', 2, ['JEE', 'APT'], q, o, a,
               'Distance = %d x %d = %d km. Time at the new speed = %d / %d = %s hours. Distance stays the same; speed and time change in opposite directions.' % (v1, t, d, d, v2, _g(round(float(right), 2))),
               'The distance is hidden inside the first sentence: find it, then reuse it.')


def average_missing(rng):
    n = rng.choice([4, 5, 6])
    avg = rng.choice([12, 15, 18, 20, 24, 25])
    while True:
        vals = [rng.randint(avg - 7, avg + 7) for _ in range(n - 1)]
        last = avg * n - sum(vals)
        if avg - 9 <= last <= avg + 9 and last not in vals and last > 0:
            break
    q = 'The marks of %d students in a quiz are %s and one more that is not shown. The average of all %d is %d. What is the missing mark?' % (n, ', '.join(map(str, vals)), n, avg)
    w = [avg, last + n, last - n, sum(vals) // (n - 1)]
    o, a = _opts(rng, last, w)
    return _mk('MAT', 'Maths: averages', '7-8', 2, ['JEE', 'APT'], q, o, a,
               'Total = average x count = %d x %d = %d. The known marks add up to %d, so the missing one is %d - %d = %d.' % (avg, n, avg * n, sum(vals), avg * n, sum(vals), last),
               'Work with the total, not the average.')


def area_perimeter(rng):
    l, w_ = rng.randint(8, 24), rng.randint(4, 7)
    cut = rng.choice([2, 3, 4])
    area = l * w_ - cut * cut
    q = 'A rectangular sheet is %d cm long and %d cm wide. A square of side %d cm is cut from one corner. What is the area that is left (in square cm)?' % (l, w_, cut)
    wr = [l * w_, 2 * (l + w_) - cut, l * w_ - 4 * cut, l * w_ - cut]
    o, a = _opts(rng, area, wr)
    return _mk('MAT', 'Maths: area', '7-8', 1, ['JEE', 'UCD'], q, o, a,
               'Whole sheet = %d x %d = %d. The cut-out square is %d x %d = %d. Left: %d - %d = %d square cm.' % (l, w_, l * w_, cut, cut, cut * cut, l * w_, cut * cut, area),
               'Area of a shape with a piece removed: subtract areas, not sides.')


def linear_eq(rng):
    x = rng.randint(3, 15)
    a = rng.randint(2, 7)
    b = rng.randint(1, 12)
    c = rng.randint(2, 5)
    rhs = a * x + b
    q = 'I think of a number, multiply it by %d, add %d and get %d. What was the number?' % (a, b, rhs)
    wr = [x + 1, x - 1, (rhs - b) * a if a else 0, rhs // a]
    o, ans = _opts(rng, x, wr)
    return _mk('MAT', 'Maths: simple equations', '7-8', 1, ['JEE', 'APT'], q, o, ans,
               'Undo the steps in reverse: %d - %d = %d, then %d / %d = %d.' % (rhs, b, rhs - b, rhs - b, a, x), 'Think-of-a-number puzzles: reverse the operations.')


def two_step_eq(rng):
    x = rng.randint(4, 14)
    a = rng.randint(3, 8)
    b = rng.randint(2, a - 1)
    d = rng.randint(1, 9)
    e = (a - b) * x + d                                           # a x + d = b x + e
    q = 'Solve for x:  %dx + %d = %dx + %d' % (a, d, b, e)
    wr = [x + 1, x - 1, (e - d) // (a + b) if (a + b) else 1, x * 2]
    o, ans = _opts(rng, x, wr)
    return _mk('MAT', 'Maths: equations with x on both sides', '9-10', 2, ['JEE'], q, o, ans,
               'Collect x terms: (%d - %d)x = %d - %d, so %dx = %d and x = %d.' % (a, b, e, d, a - b, e - d, x), 'Move all x terms to one side first.')


def consecutive(rng):
    n = rng.randint(3, 6)
    s = rng.randint(4, 30)
    total = sum(range(s, s + n))
    q = 'The sum of %d consecutive whole numbers is %d. What is the largest of them?' % (n, total)
    right = s + n - 1
    wr = [s, s + n, total // n, total // n + 1 if n % 2 == 0 else s + 1]
    o, a = _opts(rng, right, wr)
    return _mk('MAT', 'Maths: number patterns', '9-10', 2, ['JEE', 'APT'], q, o, a,
               'For consecutive numbers the middle (average) is the sum divided by the count: %d / %d = %s. The largest is %d more than the smallest; the numbers are %d, ..., %d.' % (total, n, _g(total / n), n - 1, s, right),
               'Use the average as the middle value of a run of equal steps.')


def angle_polygon(rng):
    n = rng.choice([5, 6, 8, 9, 10, 12])
    right = (n - 2) * 180 // n
    q = 'What is the size of each interior angle of a regular polygon with %d sides (in degrees)?' % n
    wr = [360 // n, (n - 2) * 180, 180 - 360 // n + 10, right + 15]
    o, a = _opts(rng, right, wr)
    return _mk('MAT', 'Maths: polygon angles', '9-10', 2, ['JEE', 'NAT'], q, o, a,
               'Exterior angle = 360/%d = %d degrees, so the interior angle is 180 - %d = %d degrees.' % (n, 360 // n, 360 // n, right) if 360 % n == 0 else
               'Interior angles add up to (%d-2) x 180 = %d; each is %d / %d = %d degrees.' % (n, (n - 2) * 180, (n - 2) * 180, n, right),
               'Regular polygon: use the exterior angle or the (n-2) x 180 rule.')


def prob_balls(rng):
    r, b, g = rng.randint(2, 7), rng.randint(2, 7), rng.randint(1, 6)
    t = r + b + g
    q = 'A bag holds %d red, %d blue and %d green marbles. One marble is drawn at random. What is the probability that it is NOT blue?' % (r, b, g)
    right = Fraction(r + g, t)
    wr = [Fraction(b, t), Fraction(r, t), Fraction(r + g, t - 1) if t > 1 else Fraction(1, 2), Fraction(r + g, b)]
    o, a = _opts(rng, right, wr, lambda x: '%d/%d' % (Fraction(x).numerator, Fraction(x).denominator))
    return _mk('MAT', 'Maths: probability', '9-10', 2, ['JEE', 'APT'], q, o, a,
               'Total marbles = %d. Not blue = red + green = %d. Probability = %d/%d, which simplifies to %d/%d. (Also 1 - %d/%d.)' % (t, r + g, r + g, t, right.numerator, right.denominator, b, t),
               'Count the favourable outcomes directly, or use 1 minus the probability of the opposite.')


def compound_sim(rng):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000])
    r = rng.choice([5, 10, 20])
    si = p * r * 2 // 100
    ci = round(p * ((1 + r / 100) ** 2 - 1))
    q = 'Rs %d is kept for 2 years at %d%% per year. How much more interest (in Rs) does compound interest give than simple interest?' % (p, r)
    right = ci - si
    wr = [ci, si, right * 2, right + r]
    o, a = _opts(rng, right, wr)
    return _mk('MAT', 'Maths: simple and compound interest', '9-10', 3, ['JEE'], q, o, a,
               'Simple interest = %d x %d x 2 / 100 = %d. Compound interest = %d x (1.%02d^2 - 1) = %d. Difference = %d.' % (p, r, si, p, r, ci, right) if r >= 10 else
               'Simple interest = %d x %d x 2 / 100 = %d. Compound interest = %d x (1.%02d^2 - 1) = %d. Difference = %d.' % (p, r, si, p, r, ci, right),
               'The gap between compound and simple interest comes from interest on interest.')


def unit_conv(rng):
    a = rng.choice([(2.5, 'km', 'm', 1000), (450, 'cm', 'm', 0.01), (3.2, 'kg', 'g', 1000), (7500, 'ml', 'litres', 0.001), (90, 'km/h', 'm/s', 5 / 18), (15, 'm/s', 'km/h', 18 / 5)])
    v, u1, u2, f = a
    right = round(v * f, 3)
    q = 'Convert %s %s into %s.' % (_g(v), u1, u2)
    wr = [round(v / f, 3) if f else v, round(v * f * 10, 3), round(v * f / 10, 3), round(v + f, 3)]
    o, ans = _opts(rng, right, wr, _g)
    return _mk('MAT', 'Maths: units and measures', '7-8', 1, ['JEE', 'APT'], q, o, ans,
               'Use the factor: 1 %s = %s %s, so %s x %s = %s.' % (u1, _g(f), u2, _g(v), _g(f), _g(right)), 'Check that your answer is bigger or smaller in the direction you expect.')


# ---- LOG ---------------------------------------------------------------------------------------------------------------------------------
def number_series(rng):
    kind = rng.choice(['ap', 'gp', 'sq', 'alt', 'diff2'])
    s = rng.randint(2, 9)
    d = rng.randint(2, 7)
    if kind == 'ap':
        seq = [s + i * d for i in range(6)]
        why = 'Each term is %d more than the one before.' % d
    elif kind == 'gp':
        r = rng.choice([2, 3])
        seq = [s * r ** i for i in range(6)]
        why = 'Each term is %d times the one before.' % r
    elif kind == 'sq':
        seq = [(s + i) ** 2 for i in range(6)]
        why = 'The terms are the squares of %d, %d, %d, ...' % (s, s + 1, s + 2)
    elif kind == 'alt':
        e = rng.randint(2, 6)
        seq = []
        for i in range(6):
            seq.append(s + (i // 2) * d if i % 2 == 0 else 50 + (i // 2) * e)
        why = 'Two interleaved series: the odd positions rise by %d and the even positions by %d.' % (d, e)
    else:
        seq = [s]
        step = d
        for i in range(5):
            seq.append(seq[-1] + step)
            step += 2
        why = 'The gaps themselves grow by 2 each time (%d, %d, %d, ...).' % (d, d + 2, d + 4)
    right = seq[5]
    shown = ', '.join(map(str, seq[:5]))
    q = 'What comes next?   %s, ?' % shown
    wr = [right + 1, right - 1, right + d, seq[4] + (seq[4] - seq[3])]
    o, a = _opts(rng, right, wr)
    return _mk('LOG', 'Reasoning: number series', '7-8' if kind in ('ap', 'gp', 'sq') else '9-10', 1 if kind == 'ap' else 2 if kind in ('gp', 'sq') else 3, ['APT', 'IAT'], q, o, a,
               why + ' So the next term is %d.' % right, 'Find the rule from differences, ratios or two interleaved series.')


def letter_code(rng):
    word = rng.choice(['DESIGN', 'BRIDGE', 'ENGINE', 'CIRCUIT', 'SKETCH', 'MODEL', 'ROBOT', 'TOWER', 'PLAN', 'CLAY'])
    k = rng.randint(1, 4)
    sign = rng.choice([1, -1])

    def sh(w):
        return ''.join(chr((ord(c) - 65 + sign * k) % 26 + 65) for c in w)
    target = rng.choice([w for w in ['METRO', 'FRAME', 'LIGHT', 'PAINT', 'CRANE', 'GEARS'] if w != word])
    q = 'In a code, %s is written as %s. How is %s written in the same code?' % (word, sh(word), target)
    right = sh(target)
    wr = [''.join(chr((ord(c) - 65 - sign * k) % 26 + 65) for c in target), ''.join(chr((ord(c) - 65 + sign * (k + 1)) % 26 + 65) for c in target),
          ''.join(chr((ord(c) - 65 + sign * (k - 1)) % 26 + 65) for c in target) if k > 1 else target[::-1], target[::-1]]
    o, a = _opts(rng, right, wr)
    return _mk('LOG', 'Reasoning: letter coding', '7-8', 1, ['APT', 'UCD'], q, o, a,
               'Compare %s with %s: every letter moves %d place(s) %s in the alphabet. Apply the same move to %s to get %s.' % (word, sh(word), k, 'forward' if sign > 0 else 'back', target, right),
               'Coding questions: compare the first letters, then confirm on the second.')


def direction_walk(rng):
    steps = [(rng.choice(['north', 'south', 'east', 'west']), rng.choice([3, 4, 5, 6, 8, 10]))]
    dirs = {'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0)}
    names = list(dirs)
    for _ in range(2):
        prev = steps[-1][0]
        cand = [d for d in names if (dirs[d][0] * dirs[prev][0] + dirs[d][1] * dirs[prev][1]) == 0]
        steps.append((rng.choice(cand), rng.choice([3, 4, 5, 6, 8, 12])))
    x = sum(dirs[d][0] * n for d, n in steps)
    y = sum(dirs[d][1] * n for d, n in steps)
    dist = (x * x + y * y) ** 0.5
    if x == 0 or y == 0 or abs(dist - round(dist)) > 1e-9:
        return direction_walk(rng)
    right = int(round(dist))
    walk = ', then '.join('%d m %s' % (n, d) for d, n in steps)
    q = 'Asha walks %s. How far is she from where she started (in metres, in a straight line)?' % walk
    wr = [sum(n for _, n in steps), abs(x) + abs(y) - 1, abs(x) + abs(y), right + 2]
    o, a = _opts(rng, right, wr)
    return _mk('LOG', 'Reasoning: directions and distance', '9-10', 3, ['APT', 'JEE'], q, o, a,
               'Net movement: %d m east-west and %d m north-south (opposite moves cancel). The straight-line distance is sqrt(%d^2 + %d^2) = %d m.' % (abs(x), abs(y), abs(x), abs(y), right),
               'Combine opposite moves first, then use the right-angled triangle.')


def ranking(rng):
    names = rng.sample(['Asha', 'Bilal', 'Charu', 'Dev', 'Esha', 'Farid', 'Gita', 'Hari'], 5)
    n = len(names)
    order = names[:]                                              # tallest to shortest
    a, b, c, d, e = order
    q =('Five friends are compared by height. %s is taller than %s but shorter than %s. %s is shorter than %s and taller than %s. %s is taller than everyone else. Who is the second tallest?') % (c, d, b, d, c, e, a)
    right = b
    o, ans = _opts(rng, right, [a, c, d, e], str)
    return _mk('LOG', 'Reasoning: ordering', '7-8', 2, ['APT'], q, o, ans,
               'From the clues: %s tallest; %s is taller than %s; %s is taller than %s; %s taller than %s, which is above %s. Full order: %s. The second tallest is %s.' % (a, b, c, c, d, d, e, e, ' > '.join(order), right),
               'Chain the clues into one order before answering.')


def calendar_day(rng):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    i = rng.randint(0, 6)
    n = rng.choice([10, 17, 25, 30, 45, 52, 60, 100])
    right = days[(i + n) % 7]
    q = 'Today is %s. What day of the week will it be %d days from today?' % (days[i], n)
    wr = [days[(i + n + 1) % 7], days[(i + n - 1) % 7], days[(i + n // 7) % 7], days[(i - n) % 7]] + [d for d in days if d != right]
    o, a = _opts(rng, right, wr)
    return _mk('LOG', 'Reasoning: calendar', '7-8', 2, ['APT'], q, o, a,
               '%d = %d weeks and %d days (%d x 7 + %d). Whole weeks bring the same day, so move %d days on from %s: %s.' % (n, n // 7, n % 7, n // 7, n % 7, n % 7, days[i], right),
               'Divide by 7 and use only the remainder.')


def syllogism(rng):
    groups = rng.choice([('engineers', 'problem-solvers', 'curious people'), ('designers', 'sketchers', 'observers'), ('robots', 'machines', 'things with parts')])
    a, b, c = groups
    q = 'All %s are %s. All %s are %s. Which conclusion MUST be true?' % (a, b, b, c)
    right = 'All %s are %s.' % (a, c)
    wr = ['All %s are %s.' % (c, a), 'Some %s are not %s.' % (a, c), 'All %s are %s.' % (c, b)]
    o, ans = _opts(rng, right, wr)
    return _mk('LOG', 'Reasoning: logical deduction', '9-10', 2, ['APT', 'IAT'], q, o, ans,
               'If every %s is a %s, and every %s is a %s, then every %s is a %s. The reverse is not given: there can be %s who are not %s.' % (a[:-1], b[:-1], b[:-1], c[:-1] if c.endswith('s') else c, a[:-1], c, c, a),
               'Deduction: follow the chain forward only.')


def clock_angle(rng):
    h = rng.randint(1, 11)
    m = rng.choice([0, 10, 20, 30, 40, 50])
    ang = abs(30 * h - 5.5 * m)
    ang = min(ang, 360 - ang)
    q = 'What is the smaller angle between the hour hand and the minute hand of a clock at %d:%02d (in degrees)?' % (h, m)
    right = ang
    wr = [360 - ang if 360 - ang != ang else ang + 15, abs(30 * h - 6 * m), ang + 30, ang - 15 if ang >= 15 else ang + 45]
    o, a = _opts(rng, right, wr, _g)
    return _mk('LOG', 'Reasoning: clocks', '9-10', 3, ['APT', 'JEE'], q, o, a,
               'The hour hand is at 30 x %d + 0.5 x %d = %s degrees; the minute hand is at 6 x %d = %d degrees. The gap is %s degrees (smaller angle %s).' % (h, m, _g(30 * h + 0.5 * m), m, 6 * m, _g(abs(30 * h + 0.5 * m - 6 * m)), _g(ang)),
               'Remember the hour hand also moves as minutes pass.')


def odd_one_out_num(rng):
    k = rng.choice([2, 3, 4, 5])
    base = [k * i for i in rng.sample(range(2, 12), 4)]
    odd = rng.choice([x for x in range(7, 60) if x % k != 0])
    items = base + [odd]
    rng.shuffle(items)
    q = 'Which number does not belong with the others?   %s' % ',  '.join(map(str, items))
    opts = [str(odd)] + [str(x) for x in base[:3]]
    order = list(range(4))
    rng.shuffle(order)
    out = [opts[i] for i in order]
    return _mk('LOG', 'Reasoning: odd one out', '7-8', 1, ['APT', 'UCD'], q, out, order.index(0),
               'Every number except %d is a multiple of %d.' % (odd, k), 'Look for a shared property (multiples, squares, primes) shared by all but one.')


GENERATORS = {
    'pcchg': percent_change, 'ratio': ratio_share, 'speed': speed_time, 'avg': average_missing, 'area': area_perimeter, 'lin': linear_eq,
    'lin2': two_step_eq, 'consec': consecutive, 'poly': angle_polygon, 'prob': prob_balls, 'ci': compound_sim, 'unit': unit_conv,
    'series': number_series, 'code': letter_code, 'walk': direction_walk, 'rank': ranking, 'cal': calendar_day, 'syl': syllogism,
    'clock': clock_angle, 'odd': odd_one_out_num,
}


def build(gen, seed):
    """Rebuild a generated question from its generator name and seed (deterministic)."""
    rng = random.Random('%s-%d' % (gen, seed))
    q = GENERATORS[gen](rng)
    q['id'] = 'g:%s:%d' % (gen, seed)
    q['src'] = 'gen'
    return q


def from_id(qid):
    try:
        _, gen, seed = qid.split(':')
        if gen not in GENERATORS:
            return None
        return build(gen, int(seed))
    except (ValueError, KeyError):
        return None
