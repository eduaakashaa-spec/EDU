"""Physics templates (g = 10 m s^-2 unless stated). Chapter codes: UNM units & errors, KIN kinematics, LOM laws of motion, WEP work-energy-power,
ROT rotation, GRA gravitation, PMB properties of matter, THM thermodynamics, OSW oscillations & waves, ELS electrostatics, CUR current electricity,
MAG magnetism & EMI, OPT optics, DUA modern physics."""
import math
from fractions import Fraction

from kit import Item, distinct, sgn, sub, sup, tpl
import kit as _kit


def n(x):
    """Physics answers read better as decimals when the fraction terminates (75/2 -> 37.5)."""
    if isinstance(x, Fraction) and x.denominator != 1:
        d = x.denominator
        for p in (2, 5):
            while d % p == 0:
                d //= p
        if d == 1:
            return _kit.n(float(x))
    return _kit.n(x)

P = 'PHY'


@tpl(P, 'UNM', nat=False)
def dimensions(r):
    base = {'force': (1, 1, -2), 'energy': (1, 2, -2), 'pressure': (1, -1, -2), 'velocity': (0, 1, -1), 'acceleration': (0, 1, -2), 'momentum': (1, 1, -1), 'power': (1, 2, -3),
            'density': (1, -3, 0), 'frequency': (0, 0, -1), 'area': (0, 2, 0), 'mass': (1, 0, 0), 'time': (0, 0, 1)}
    names = list(base)
    while True:
        a, b = r.sample(names, 2)
        op = r.choice(['/', '×'])
        d = tuple(x / y if False else (x - y if op == '/' else x + y) for x, y in zip(base[a], base[b]))
        if any(d) and all(abs(x) <= 4 for x in d):
            break

    def f(d):
        parts = []
        for sym, e in zip('MLT', d):
            if e:
                parts.append(sym if e == 1 else '%s<sup>%s</sup>' % (sym, sgn(e)))
        return '[' + ' '.join(parts) + ']'
    ans = f(d)
    wrongs = []
    for dd in [(d[0] + 1, d[1], d[2]), (d[0], d[1] - 1, d[2]), (d[0], d[1], d[2] + 1), (-d[0], d[1], d[2]), (d[0], d[1], -d[2])]:
        if dd != d and f(dd) != '[]':
            wrongs.append(f(dd))
    return Item('The dimensional formula of (%s %s %s) is' % (a, '÷' if op == '/' else '×', b), ans, wrongs, ['[%s] = %s and [%s] = %s.' % (a, f(base[a]), b, f(base[b])),
                'Dimensions %s: %s.' % ('subtract' if op == '/' else 'add', ans)], 'Adding exponents when dividing.')


@tpl(P, 'UNM')
def percent_error(r):
    dm, dv = r.randint(1, 4), r.randint(1, 4)
    ans = dm + 2 * dv
    return Item('In measuring kinetic energy K = ½mv<sup>2</sup>, the mass has a %d%% error and the speed a %d%% error. The maximum percentage error in K is' % (dm, dv), ans,
                distinct(ans, [dm + dv, 2 * dm + dv, dm * dv], 1), ['K &prop; m v<sup>2</sup>, so &Delta;K/K = &Delta;m/m + 2&Delta;v/v.', '= %d + 2×%d = %d%%.' % (dm, dv, ans)],
                'Not doubling the speed error for v<sup>2</sup>.', nat=ans)


@tpl(P, 'KIN')
def projectile_height(r):
    u, s = r.choice([(50, 0.6), (50, 0.8), (100, 0.6), (100, 0.8), (40, 0.6), (30, 0.8), (60, 0.8), (20, 0.5)])
    uy = u * s
    ans = n(uy * uy / 20)
    return Item('A body is projected with speed %d m/s at an angle whose sine is %s. Taking g = 10 m/s<sup>2</sup>, the maximum height reached is (in m)' % (u, n(s)), ans,
                [n(u * u / 20), n(uy / 10), n(uy * uy / 10)], ['Vertical component u<sub>y</sub> = %d × %s = %s m/s.' % (u, n(s), n(uy)), 'H = u<sub>y</sub><sup>2</sup>/2g = %s<sup>2</sup>/20 = %s m.' % (n(uy), ans)],
                'Using the full speed instead of the vertical component.', nat=int(uy * uy / 20) if (uy * uy / 20) == int(uy * uy / 20) else None)


@tpl(P, 'KIN')
def stopping_distance(r):
    v, a = r.choice([(20, 5), (30, 5), (40, 8), (10, 2), (60, 10), (36, 6), (50, 10)])
    ans = v * v / (2 * a)
    return Item('A car moving at %d m/s is brought to rest by a uniform retardation of %d m/s<sup>2</sup>. The distance travelled before stopping is (in m)' % (v, a), n(ans),
                [n(v * v / a), n(v / a), n(v * a)], ['v<sup>2</sup> = u<sup>2</sup> − 2as with v = 0.', 's = u<sup>2</sup>/2a = %d/%d = %s m.' % (v * v, 2 * a, n(ans))], 'Forgetting the factor 2 in 2as.',
                nat=int(ans) if ans == int(ans) else None)


@tpl(P, 'KIN')
def trains_crossing(r):
    l1, l2, v1, v2 = r.choice([(150, 100, 20, 30), (200, 100, 10, 20), (120, 80, 15, 25), (300, 100, 30, 50), (240, 160, 25, 15)])
    ans = (l1 + l2) / (v1 + v2)
    return Item('Two trains of lengths %d m and %d m move towards each other on parallel tracks at %d m/s and %d m/s. They take how many seconds to cross each other completely?' % (l1, l2, v1, v2), n(ans),
                [n((l1 + l2) / abs(v1 - v2)), n(l1 / (v1 + v2)), n((l1 + l2) / (v1 * v2) * 10)], ['Relative speed = %d + %d = %d m/s.' % (v1, v2, v1 + v2), 'Distance to clear = %d + %d = %d m.' % (l1, l2, l1 + l2), 't = %d/%d = %s s.' % (l1 + l2, v1 + v2, n(ans))],
                'Using the difference of speeds (that is for the same direction).', nat=int(ans) if ans == int(ans) else None)


@tpl(P, 'LOM')
def atwood(r):
    m1, m2 = r.choice([(3, 1), (5, 3), (4, 2), (6, 2), (9, 3), (7, 5), (2, 1)])
    a = Fraction((m1 - m2) * 10, m1 + m2)
    T = Fraction(2 * m1 * m2 * 10, m1 + m2)
    return Item('Two masses %d kg and %d kg hang from a light string over a smooth pulley (Atwood machine). Taking g = 10 m/s<sup>2</sup>, the tension in the string is (in N)' % (m1, m2), n(T),
                [n((m1 + m2) * 5), n(m1 * 10), n(m2 * 10)] if True else [], ['a = (m<sub>1</sub> − m<sub>2</sub>)g/(m<sub>1</sub> + m<sub>2</sub>) = %s m/s<sup>2</sup>.' % n(a), 'T = 2m<sub>1</sub>m<sub>2</sub>g/(m<sub>1</sub> + m<sub>2</sub>) = %s N.' % n(T)],
                'Taking the tension equal to the weight of the heavier mass.', nat=int(T) if T.denominator == 1 else None)


@tpl(P, 'LOM')
def incline_friction(r):
    mu = r.choice([Fraction(1, 4), Fraction(1, 8), Fraction(1, 2)])
    a = 6 - 8 * mu
    return Item('A block slides down a rough incline of angle 37&deg; (sin 37&deg; = 0.6, cos 37&deg; = 0.8) with coefficient of friction %s. Taking g = 10 m/s<sup>2</sup>, its acceleration is (in m/s<sup>2</sup>)' % n(mu), n(a),
                [n(6), n(6 + 8 * mu), n(8 - 6 * mu)], ['a = g(sin&theta; − &mu; cos&theta;) = 10(0.6 − %s × 0.8).' % n(mu), '= 6 − %s = %s m/s<sup>2</sup>.' % (n(8 * mu), n(a))], 'Swapping sin&theta; and cos&theta;.',
                nat=int(a) if a == int(a) else None)


@tpl(P, 'WEP')
def work_energy(r):
    m, F, mu, d = r.choice([(2, 30, 0.5, 10), (5, 40, 0.2, 20), (10, 60, 0.3, 5), (4, 50, 0.5, 8), (2, 24, 0.4, 25)])
    net = (F - mu * m * 10) * d
    return Item('A %d kg block is pulled on a rough horizontal floor (&mu; = %s) by a horizontal force of %d N through %d m. Taking g = 10 m/s<sup>2</sup>, the gain in kinetic energy is (in J)' % (m, n(mu), F, d), n(net),
                [n(F * d), n(mu * m * 10 * d), n((F + mu * m * 10) * d)], ['Friction = &mu;mg = %s N.' % n(mu * m * 10), 'Net work = (F − f)d = (%d − %s) × %d = %s J = gain in K.E.' % (F, n(mu * m * 10), d, n(net))],
                'Ignoring the work done against friction.', nat=int(net) if net == int(net) else None)


@tpl(P, 'WEP')
def spring_energy(r):
    k, x = r.choice([(200, 0.1), (400, 0.2), (100, 0.3), (500, 0.4), (800, 0.05), (1000, 0.1), (300, 0.2)])
    E = Fraction(1, 2) * k * Fraction(str(x)) ** 2
    return Item('A spring of force constant %d N/m is compressed by %s m. The energy stored in it is (in J)' % (k, n(x)), n(float(E)), [n(float(k * Fraction(str(x)) ** 2)), n(float(k * Fraction(str(x)))), n(float(E * 2 * 2))],
                ['U = ½kx<sup>2</sup> = ½ × %d × %s<sup>2</sup> = %s J.' % (k, n(x), n(float(E)))], 'Forgetting the ½, or not squaring x.', nat=int(E) if E.denominator == 1 else None)


@tpl(P, 'ROT')
def angular_momentum(r):
    i1, w1, i2 = r.choice([(4, 12, 6), (6, 20, 10), (3, 10, 5), (8, 15, 10), (10, 6, 4), (2, 30, 12)])
    w2 = Fraction(i1 * w1, i2)
    return Item('A rotating platform has moment of inertia %d kg m<sup>2</sup> and angular speed %d rad/s. A person on it changes the moment of inertia to %d kg m<sup>2</sup> without any external torque. The new angular speed is (in rad/s)' % (i1, w1, i2),
                n(w2), [n(Fraction(i2 * w1, i1)), n(w1 * (i1 + i2)), n(Fraction(w1, 2))], ['Angular momentum is conserved: I<sub>1</sub>&omega;<sub>1</sub> = I<sub>2</sub>&omega;<sub>2</sub>.', '&omega;<sub>2</sub> = %d × %d/%d = %s rad/s.' % (i1, w1, i2, n(w2))],
                'Inverting the ratio of the moments of inertia.', nat=int(w2) if w2.denominator == 1 else None)


@tpl(P, 'ROT', nat=False)
def disc_inertia(r):
    M, R = r.choice([(4, 1), (8, 0.5), (2, 2), (6, 1), (10, 0.2), (12, 0.5)])
    shape = r.choice([('uniform disc', Fraction(1, 2)), ('thin ring', Fraction(1)), ('solid sphere', Fraction(2, 5))])
    I = shape[1] * M * Fraction(str(R)) ** 2
    return Item('The moment of inertia of a %s of mass %d kg and radius %s m about an axis through its centre (perpendicular to the plane for the disc and ring) is (in kg m<sup>2</sup>)' % (shape[0], M, n(R)),
                n(float(I)), [n(float(M * Fraction(str(R)) ** 2)) if shape[1] != 1 else n(float(Fraction(1, 2) * M * Fraction(str(R)) ** 2)),
                              n(float(Fraction(2, 5) * M * Fraction(str(R)) ** 2)) if shape[1] != Fraction(2, 5) else n(float(Fraction(2, 3) * M * Fraction(str(R)) ** 2)), n(float(Fraction(1, 4) * M * Fraction(str(R)) ** 2))],
                ['I = %s MR<sup>2</sup> for a %s.' % (n(shape[1]), shape[0]), 'I = %s × %d × %s<sup>2</sup> = %s kg m<sup>2</sup>.' % (n(shape[1]), M, n(R), n(float(I)))], 'Using the wrong numerical factor for the shape.')


@tpl(P, 'GRA')
def gravity_height(r):
    W, k = r.choice([(200, 1), (360, 2), (90, 2), (160, 1), (450, 2)])
    ans = Fraction(W, (1 + k) ** 2)
    return Item('A body weighs %d N on the surface of the earth (radius R). Its weight at a height of %s above the surface is (in N)' % (W, 'R' if k == 1 else '%dR' % k), n(ans),
                [n(Fraction(W, 1 + k)), n(W * (1 + k) ** 2 // 1), n(Fraction(W, (1 + k) ** 3))], ['g&prime; = g R<sup>2</sup>/(R + h)<sup>2</sup> = g/(1 + h/R)<sup>2</sup> = g/%d.' % ((1 + k) ** 2), 'Weight = %d/%d = %s N.' % (W, (1 + k) ** 2, n(ans))],
                'Dividing by (R + h) instead of (R + h)<sup>2</sup>.', nat=int(ans) if ans.denominator == 1 else None)


@tpl(P, 'PMB')
def hydrostatic(r):
    h, rho = r.choice([(10, 1000), (20, 1000), (5, 1000), (2, 13600), (4, 800)])
    P0 = 100  # kPa
    ans = P0 + rho * 10 * h / 1000
    return Item('The absolute pressure at a depth of %d m in a liquid of density %d kg/m<sup>3</sup>, with atmospheric pressure 1.0 × 10<sup>5</sup> Pa and g = 10 m/s<sup>2</sup>, is (in kPa)' % (h, rho), n(ans),
                [n(rho * 10 * h / 1000), n(P0 - rho * 10 * h / 1000) if P0 - rho * 10 * h / 1000 > 0 else n(P0 * 2), n(P0 + rho * h / 1000)], ['Gauge pressure = &rho;gh = %d × 10 × %d = %s kPa.' % (rho, h, n(rho * 10 * h / 1000)), 'Absolute pressure = 100 + %s = %s kPa.' % (n(rho * 10 * h / 1000), n(ans))],
                'Leaving out atmospheric pressure.', nat=int(ans) if ans == int(ans) else None)


@tpl(P, 'THM')
def carnot_efficiency(r):
    t1, t2 = r.choice([(600, 300), (800, 400), (500, 400), (400, 300), (1000, 250), (900, 300)])
    eta = 100 * (1 - Fraction(t2, t1))
    return Item('A Carnot engine works between a source at %d K and a sink at %d K. Its efficiency (in %%) is' % (t1, t2), n(eta), [n(100 * Fraction(t2, t1)), n(100 * Fraction(t1 - t2, t2)), n(Fraction(t1 - t2, 10))],
                ['η = 1 − T<sub>2</sub>/T<sub>1</sub> = 1 − %d/%d.' % (t2, t1), 'Efficiency = %s%%.' % n(eta)], 'Using T<sub>2</sub>/T<sub>1</sub> as the efficiency.', nat=int(eta) if eta.denominator == 1 else None)


@tpl(P, 'THM')
def gas_law(r):
    p1, v1, t1, p2, v2 = r.choice([(1, 4, 300, 2, 3), (2, 6, 200, 3, 8), (1, 10, 300, 2, 20), (4, 2, 150, 2, 6), (3, 5, 100, 5, 6), (2, 3, 300, 4, 5)])
    t2 = Fraction(p2 * v2 * t1, p1 * v1)
    return Item('A fixed mass of ideal gas goes from (P = %d atm, V = %d L, T = %d K) to a state with P = %d atm and V = %d L. The final temperature is (in K)' % (p1, v1, t1, p2, v2), n(t2),
                [n(Fraction(p1 * v1 * t1, p2 * v2)), n(t1 + p2 * v2 - p1 * v1), n(t1 * 2)], ['P<sub>1</sub>V<sub>1</sub>/T<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>/T<sub>2</sub>.', 'T<sub>2</sub> = %d × %d × %d/(%d × %d) = %s K.' % (p2, v2, t1, p1, v1, n(t2))],
                'Inverting the ratio.', nat=int(t2) if t2.denominator == 1 else None)


@tpl(P, 'THM')
def first_law(r):
    q, w = r.randint(200, 900) // 10 * 10, r.randint(50, 600) // 10 * 10
    q = max(q, w + 40)
    ans = q - w
    return Item('A system absorbs %d J of heat and does %d J of work on its surroundings. The change in its internal energy is (in J)' % (q, w), ans, [q + w, w - q, q], ['&Delta;U = Q − W = %d − %d = %d J.' % (q, w, ans)],
                'Adding work done by the system to the heat absorbed.', nat=ans)


@tpl(P, 'OSW')
def shm_speed(r):
    k, m = r.choice([(100, 1), (400, 4), (900, 1), (200, 2), (1600, 4), (225, 1), (36, 1)])
    A = r.choice([2, 3, 5])
    w = int(math.sqrt(k / m))
    ans = A * w
    return Item('A %d kg mass attached to a spring of constant %d N/m oscillates with amplitude %d cm. Its maximum speed is (in cm/s)' % (m, k, A), ans, distinct(ans, [A * w * w, A * k // m if False else A * w // 2 if (A * w) % 2 == 0 else A * w + w, A * m * w], w),
                ['&omega; = √(k/m) = √(%d/%d) = %d rad/s.' % (k, m, w), 'v<sub>max</sub> = A&omega; = %d × %d = %d cm/s.' % (A, w, ans)], 'Using &omega;<sup>2</sup> instead of &omega;.', nat=ans)


@tpl(P, 'OSW')
def wave_speed(r):
    f, lam = r.choice([(100, 3), (250, 2), (500, 0.6), (50, 6), (400, 0.85), (680, 0.5)])
    v = f * lam
    kind = r.choice(['v', 'closed'])
    if kind == 'v':
        return Item('A wave of frequency %d Hz has wavelength %s m. Its speed is (in m/s)' % (f, n(lam)), n(v), [n(f / lam), n(f + lam), n(v / 2)], ['v = f&lambda; = %d × %s = %s m/s.' % (f, n(lam), n(v))],
                    'Dividing instead of multiplying.', nat=int(v) if v == int(v) else None)
    L = Fraction(str(lam)) / 4
    return Item('A closed organ pipe resonates at its fundamental in a wave of wavelength %s m. The length of the pipe is (in m)' % n(lam), n(float(L)), [n(lam / 2), n(lam), n(lam * 2 / 3)],
                ['A closed pipe holds a quarter wavelength in its fundamental.', 'L = &lambda;/4 = %s m.' % n(float(L))], 'Using &lambda;/2 (that is for an open pipe).')


@tpl(P, 'ELS')
def coulomb_force(r):
    while True:
        q1, q2, rc = r.randint(1, 6), r.randint(1, 6), r.choice([3, 5, 6, 9, 10, 15, 30])
        F = Fraction(90 * q1 * q2, rc * rc)
        if F.denominator == 1 and 1 <= F <= 3000:
            break
    return Item('Two point charges of %d &mu;C and %d &mu;C are placed %d cm apart in air (1/4&pi;&epsilon;<sub>0</sub> = 9 × 10<sup>9</sup> N m<sup>2</sup>/C<sup>2</sup>). The force between them is (in N)' % (q1, q2, rc), n(F),
                [n(F * 10), n(Fraction(F, 10)) if F % 10 == 0 else n(F + 9), n(Fraction(90 * (q1 + q2), rc * rc)) if True else ''], ['F = k q<sub>1</sub>q<sub>2</sub>/r<sup>2</sup> = 9×10<sup>9</sup> × %d×10<sup>−6</sup> × %d×10<sup>−6</sup>/(%d×10<sup>−2</sup>)<sup>2</sup>.' % (q1, q2, rc), '= %s N.' % n(F)],
                'Converting cm to m incorrectly.', nat=int(F))


@tpl(P, 'ELS')
def capacitors(r):
    c1, c2 = r.choice([(3, 6), (6, 12), (4, 12), (2, 3), (10, 15), (4, 4), (8, 24)])
    kind = r.choice(['series', 'parallel'])
    V = r.choice([10, 20, 50, 100])
    if kind == 'series':
        ce = Fraction(c1 * c2, c1 + c2)
    else:
        ce = Fraction(c1 + c2)
    E = Fraction(1, 2) * ce * V * V
    ask = r.choice(['C', 'E'])
    if ask == 'C':
        return Item('Two capacitors of %d &mu;F and %d &mu;F are connected in %s. The equivalent capacitance is (in &mu;F)' % (c1, c2, kind), n(ce),
                    [n(Fraction(c1 * c2, c1 + c2)) if kind == 'parallel' else n(c1 + c2), n(Fraction(c1 + c2, 2)), n(abs(c1 - c2) + 1)],
                    [('1/C = 1/%d + 1/%d' % (c1, c2)) if kind == 'series' else 'C = C<sub>1</sub> + C<sub>2</sub>', 'C = %s &mu;F.' % n(ce)], 'Mixing up the series and parallel formulas.', nat=int(ce) if ce.denominator == 1 else None)
    return Item('Two capacitors of %d &mu;F and %d &mu;F are connected in %s across a %d V battery. The total energy stored is (in &mu;J)' % (c1, c2, kind, V), n(E),
                [n(ce * V * V), n(Fraction(1, 2) * ce * V), n(Fraction(1, 2) * (c1 + c2) * V * V) if kind == 'series' else n(Fraction(1, 2) * Fraction(c1 * c2, c1 + c2) * V * V)],
                ['C<sub>eq</sub> = %s &mu;F.' % n(ce), 'U = ½CV<sup>2</sup> = ½ × %s × %d<sup>2</sup> = %s &mu;J.' % (n(ce), V, n(E))], 'Forgetting the ½ in the energy formula.', nat=int(E) if E.denominator == 1 else None)


@tpl(P, 'CUR')
def resistor_network(r):
    ra, rb, rc, V = r.choice([(6, 3, 4, 12), (12, 4, 5, 24), (6, 6, 3, 12), (10, 15, 4, 20), (4, 12, 2, 10), (20, 5, 6, 20)])
    par = Fraction(ra * rb, ra + rb)
    tot = par + rc
    I = Fraction(V) / tot
    return Item('Resistors of %d &Omega; and %d &Omega; in parallel are connected in series with a %d &Omega; resistor across a %d V battery of negligible resistance. The current drawn from the battery is (in A)' % (ra, rb, rc, V), n(I),
                [n(Fraction(V, ra + rb + rc)), n(Fraction(V) / par), n(Fraction(V, rc))], ['Parallel part = %d×%d/(%d+%d) = %s &Omega;.' % (ra, rb, ra, rb, n(par)), 'Total resistance = %s + %d = %s &Omega;.' % (n(par), rc, n(tot)), 'I = V/R = %d/%s = %s A.' % (V, n(tot), n(I))],
                'Adding all three resistances in series.', nat=int(I) if I.denominator == 1 else None)


@tpl(P, 'CUR')
def heating_power(r):
    V, R, t = r.choice([(220, 110, 10), (100, 50, 30), (12, 6, 60), (200, 40, 5), (120, 60, 20), (50, 25, 40)])
    P_ = Fraction(V * V, R)
    H = P_ * t
    return Item('A heater of resistance %d &Omega; is connected to a %d V supply for %d s. The heat produced is (in J)' % (R, V, t), n(H), [n(Fraction(V, R) * t), n(Fraction(V * V, R * R) * t), n(Fraction(V * V * R, 1) * t // 100)],
                ['Power = V<sup>2</sup>/R = %d/%d = %s W.' % (V * V, R, n(P_)), 'Heat = Pt = %s × %d = %s J.' % (n(P_), t, n(H))], 'Using I = V/R as the power.', nat=int(H) if H.denominator == 1 and H < 99999 else None)


@tpl(P, 'MAG')
def force_on_wire(r):
    B, I, L, th = r.choice([(0.5, 4, 0.5, 90), (0.2, 10, 0.5, 30), (0.4, 5, 2, 90), (1, 3, 0.2, 30), (0.5, 8, 0.25, 90), (0.1, 20, 1, 30)])
    s = Fraction(1, 2) if th == 30 else Fraction(1)
    F = Fraction(str(B)) * I * Fraction(str(L)) * s
    return Item('A straight wire of length %s m carrying %d A is placed in a uniform magnetic field of %s T at %d&deg; to the field. The force on the wire is (in N)' % (n(L), I, n(B), th), n(float(F)),
                [n(float(Fraction(str(B)) * I * Fraction(str(L)))) if th != 90 else n(float(Fraction(str(B)) * I * Fraction(str(L)) / 2)), n(float(F * 2)) if th == 90 else n(float(Fraction(str(B)) * I * Fraction(str(L)) * Fraction(866, 1000))), n(float(F / 2))],
                ['F = BIL sin&theta; = %s × %d × %s × %s.' % (n(B), I, n(L), n(float(s))), '= %s N.' % n(float(F))], 'Leaving out sin&theta; (or using cos&theta;).', nat=int(F) if F.denominator == 1 else None)


@tpl(P, 'MAG')
def transformer(r):
    np_, ns, Vp, Ip = r.choice([(100, 400, 220, 10), (500, 50, 220, 2), (200, 1000, 20, 5), (1000, 100, 2200, 3), (50, 150, 100, 6), (40, 10, 400, 5)])
    Vs = Fraction(Vp * ns, np_)
    Is = Fraction(Ip * np_, ns)
    ask = r.choice(['V', 'I'])
    if ask == 'V':
        return Item('An ideal transformer has %d turns in the primary and %d turns in the secondary. With a primary voltage of %d V the secondary voltage is (in V)' % (np_, ns, Vp), n(Vs),
                    [n(Fraction(Vp * np_, ns)), n(Vp + ns - np_), n(Fraction(Vp, 2))], ['V<sub>s</sub>/V<sub>p</sub> = N<sub>s</sub>/N<sub>p</sub>.', 'V<sub>s</sub> = %d × %d/%d = %s V.' % (Vp, ns, np_, n(Vs))], 'Inverting the turns ratio.', nat=int(Vs) if Vs.denominator == 1 else None)
    return Item('An ideal transformer has %d turns in the primary and %d in the secondary. The primary current is %d A. The secondary current is (in A)' % (np_, ns, Ip), n(Is),
                [n(Fraction(Ip * ns, np_)), n(Ip + ns - np_ if Ip + ns - np_ > 0 else Ip + 1), n(Fraction(Ip, 2))], ['Ideal transformer: V<sub>p</sub>I<sub>p</sub> = V<sub>s</sub>I<sub>s</sub>, so I<sub>s</sub>/I<sub>p</sub> = N<sub>p</sub>/N<sub>s</sub>.', 'I<sub>s</sub> = %d × %d/%d = %s A.' % (Ip, np_, ns, n(Is))],
                'Using the voltage ratio for currents.', nat=int(Is) if Is.denominator == 1 else None)


@tpl(P, 'OPT')
def lens_image(r):
    f, u = r.choice([(10, 30), (15, 30), (20, 60), (12, 36), (10, 15), (20, 30), (6, 9), (8, 24)])
    v = Fraction(f * u, u - f)
    m = v / u
    ask = r.choice(['v', 'm'])
    if ask == 'v':
        return Item('An object is placed %d cm in front of a convex lens of focal length %d cm. The image is formed at a distance (in cm) of' % (u, f), n(v), [n(Fraction(f * u, u + f)), n(u - f), n(Fraction(u * f, f))], ['1/v − 1/u = 1/f with u = −%d, f = +%d.' % (u, f), '1/v = 1/%d − 1/%d, so v = %s cm.' % (f, u, n(v))], 'Using u as a positive number in the lens formula.',
                    nat=int(v) if v.denominator == 1 else None)
    return Item('An object is placed %d cm in front of a convex lens of focal length %d cm. The magnitude of the linear magnification is' % (u, f), n(m), [n(Fraction(u, u - f)), n(Fraction(f, u)), n(Fraction(f, u - f)) if u - f != f else n(Fraction(1, 3))],
                ['v = uf/(u − f) = %s cm.' % n(v), 'm = v/u = %s/%d = %s.' % (n(v), u, n(m))], 'Using u/v for the magnification.')


@tpl(P, 'OPT')
def fringe_width(r):
    lam, D, d = r.choice([(600, 1.5, 0.3), (500, 2, 0.5), (400, 1, 0.2), (600, 2, 0.4), (500, 1, 0.25), (750, 2, 0.5), (480, 1.5, 0.24)])
    beta = lam * 1e-9 * D / (d * 1e-3) * 1e3
    return Item('In Young\'s double-slit experiment the slit separation is %s mm, the screen is %s m away and the wavelength is %d nm. The fringe width is (in mm)' % (n(d), n(D), lam), n(round(beta, 4)),
                [n(round(beta * 10, 4)), n(round(beta / 10, 4)), n(round(beta * 2, 4))], ['&beta; = &lambda;D/d = %d×10<sup>−9</sup> × %s/(%s×10<sup>−3</sup>).' % (lam, n(D), n(d)), '&beta; = %s mm.' % n(round(beta, 4))],
                'Unit slip between nm, mm and m.', nat=int(round(beta, 4)) if abs(beta - round(beta)) < 1e-9 else None)


@tpl(P, 'DUA')
def photoelectric(r):
    lam, phi = r.choice([(248, 2), (310, 1.5), (155, 3), (124, 6), (496, 1.5), (413, 2)])
    E = 1240 / lam
    K = round(E - phi, 3)
    if K <= 0:
        phi = round(E / 2, 1)
        K = round(E - phi, 3)
    return Item('Light of wavelength %d nm falls on a metal of work function %s eV (hc = 1240 eV nm). The maximum kinetic energy of the photoelectrons is (in eV)' % (lam, n(phi)), n(K),
                [n(round(E, 3)), n(round(E + phi, 3)), n(round(phi, 3))], ['Photon energy = 1240/%d = %s eV.' % (lam, n(round(E, 3))), 'K<sub>max</sub> = E − &phi; = %s − %s = %s eV.' % (n(round(E, 3)), n(phi), n(K))],
                'Giving the photon energy instead of the kinetic energy.', nat=int(K) if abs(K - round(K)) < 1e-6 and K == int(K) else None)


@tpl(P, 'DUA')
def half_life(r):
    T, k, N0 = r.choice([(5, 3, 800), (10, 2, 400), (2, 4, 1600), (3, 5, 640), (20, 3, 240), (6, 2, 100)])
    t = T * k
    ans = Fraction(N0, 2 ** k)
    return Item('A radioactive sample has half-life %d days and initially %d nuclei (in thousands). The number remaining after %d days is (in thousands)' % (T, N0, t), n(ans),
                [n(Fraction(N0, k)), n(Fraction(N0, 2 * k)), n(Fraction(N0, 2 ** (k - 1)))], ['Number of half-lives = %d/%d = %d.' % (t, T, k), 'N = N<sub>0</sub>/2<sup>%d</sup> = %d/%d = %s.' % (k, N0, 2 ** k, n(ans))],
                'Dividing by the number of half-lives rather than by 2 raised to it.', nat=int(ans) if ans.denominator == 1 else None)


@tpl(P, 'DUA', nat=False)
def bohr_energy(r):
    Z, nn = r.choice([(1, 2), (1, 3), (2, 2), (2, 3), (3, 3), (3, 2), (1, 4)])
    E = -13.6 * Z * Z / (nn * nn)
    sp = {1: 'hydrogen atom', 2: 'He<sup>+</sup> ion', 3: 'Li<sup>2+</sup> ion'}[Z]
    return Item('The energy of the electron in the n = %d orbit of a %s is (in eV)' % (nn, sp), n(round(E, 2)), [n(round(-13.6 * Z / nn, 2)), n(round(13.6 * Z * Z / (nn * nn), 2)) if False else n(round(-13.6 * nn * nn / (Z * Z), 2)), n(round(-13.6 / (nn * nn), 2)) if Z != 1 else n(round(-13.6 * Z * Z / nn, 2))],
                ['E<sub>n</sub> = −13.6 Z<sup>2</sup>/n<sup>2</sup> eV.', 'E = −13.6 × %d/%d = %s eV.' % (Z * Z, nn * nn, n(round(E, 2)))], 'Using Z instead of Z<sup>2</sup>.')
