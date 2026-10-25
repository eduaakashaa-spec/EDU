"""Chemistry templates. Chapter codes: MOL mole concept & stoichiometry, ATS atomic structure, BON bonding & shapes, THE thermodynamics,
EQU equilibrium (incl. ionic), RDX redox & electrochemistry, KIN kinetics, SOL solutions, PER periodic table, COO coordination compounds,
ORG general organic & isomerism, HYD hydrocarbons, HAL/OXY/CAR/NIT carbon compounds, BIO biomolecules.
Facts used are standard textbook values; every numerical answer is computed in the template."""
import math
from fractions import Fraction

from kit import Item, distinct, sgn, sub, sup, tpl
import kit as _kit

C = 'CHEM'


def n(x):
    if isinstance(x, Fraction) and x.denominator != 1:
        d = x.denominator
        for p in (2, 5):
            while d % p == 0:
                d //= p
        if d == 1:
            return _kit.n(float(x))
    return _kit.n(x)


MM = {'NaOH': 40, 'KOH': 56, 'H<sub>2</sub>SO<sub>4</sub>': 98, 'CaCO<sub>3</sub>': 100, 'NaCl': Fraction(117, 2), 'glucose (C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>)': 180,
      'Na<sub>2</sub>CO<sub>3</sub>': 106, 'HCl': Fraction(73, 2), 'urea (CH<sub>4</sub>N<sub>2</sub>O)': 60}


@tpl(C, 'MOL')
def mass_for_solution(r):
    while True:
        sp = r.choice(list(MM))
        M = r.choice([0.1, 0.2, 0.5, 1, 2])
        V = r.choice([100, 200, 250, 500, 1000])
        m = Fraction(str(M)) * Fraction(V, 1000) * MM[sp]
        if m == int(m) and 1 <= m <= 400:
            break
    return Item('The mass of %s required to prepare %d mL of a %s M solution is (in g)' % (sp, V, n(M)), n(m), [n(m * 10), n(m / 10) if m % 10 == 0 else n(m + 2), n(m * 2)],
                ['Moles = M × V(L) = %s × %s = %s mol.' % (n(M), n(Fraction(V, 1000)), n(Fraction(str(M)) * Fraction(V, 1000))), 'Mass = moles × molar mass = %s × %s = %s g.' % (n(Fraction(str(M)) * Fraction(V, 1000)), n(MM[sp]), n(m))],
                'Using the volume in mL without converting to litres.', nat=int(m))


def _stoich(eq, A, B, ma, mb, mass, k):
    # ratios by moles of A : moles of B from the balanced equations used above
    ratio = {'carbon': 1, 'hydrogen': 1, 'magnesium': 1, 'CaCO<sub>3</sub>': 1, 'nitrogen': 2}[A]
    ans = k * ratio * mb
    return Item('From the reaction %s, the mass of %s formed from %s g of %s (completely reacted) is (in g)' % (eq, B, n(mass), A), n(ans),
                [n(mass), n(k * mb), n(ans + mb) if ratio == 1 else n(k * mb // 2)],
                ['Moles of %s = %s/%s = %d.' % (A, n(mass), n(ma), k), '1 mol of %s gives %d mol of %s, so moles of %s = %d.' % (A, ratio, B, B, k * ratio), 'Mass of %s = %d × %d = %s g.' % (B, k * ratio, mb, n(ans))],
                'Ignoring the mole ratio in the balanced equation.', nat=int(ans))


@tpl(C, 'MOL')
def stoich_wrapper(r):
    rx = r.choice([('C + O<sub>2</sub> → CO<sub>2</sub>', 'carbon', 12, 'CO<sub>2</sub>', 44), ('2H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O', 'hydrogen', 2, 'water', 18),
                   ('2Mg + O<sub>2</sub> → 2MgO', 'magnesium', 24, 'MgO', 40), ('CaCO<sub>3</sub> → CaO + CO<sub>2</sub>', 'CaCO<sub>3</sub>', 100, 'CO<sub>2</sub>', 44),
                   ('N<sub>2</sub> + 3H<sub>2</sub> → 2NH<sub>3</sub>', 'nitrogen', 28, 'NH<sub>3</sub>', 17)])
    eq, A, ma, B, mb = rx
    k = r.choice([2, 3, 4, 5, 10])
    return _stoich(eq, A, B, ma, mb, ma * k, k)


@tpl(C, 'MOL')
def dilution(r):
    M1, V1, M2 = r.choice([(2, 50, 0.5), (1, 100, 0.25), (6, 25, 1), (4, 50, 0.5), (12, 10, 1.2), (3, 100, 0.5)])
    V2 = Fraction(M1 * V1, 1) / Fraction(str(M2))
    return Item('%d mL of a %s M solution is diluted until its molarity is %s M. The final volume of the solution is (in mL)' % (V1, n(M1), n(M2)), n(V2), [n(V2 - V1), n(Fraction(M2).limit_denominator(100) * V1 / M1 if False else Fraction(str(M2)) * V1 / M1), n(V1 * (M1 + Fraction(str(M2))))],
                ['M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>.', 'V<sub>2</sub> = %s × %d/%s = %s mL.' % (n(M1), V1, n(M2), n(V2))], 'Giving the volume of water added instead of the final volume.', nat=int(V2) if V2.denominator == 1 else None)


@tpl(C, 'ATS')
def quantum_counts(r):
    nn = r.randint(2, 5)
    kind = r.choice(['orb', 'elec', 'rn', 'an'])
    if kind == 'orb':
        ans = nn * nn
        return Item('The maximum number of orbitals in the shell with principal quantum number n = %d is' % nn, ans, distinct(ans, [2 * ans, nn, 2 * nn - 1], 1), ['Each subshell l has 2l + 1 orbitals and l runs from 0 to n − 1.', 'Total = n<sup>2</sup> = %d.' % ans], 'Giving the number of electrons (2n<sup>2</sup>) instead.', nat=ans)
    if kind == 'elec':
        ans = 2 * nn * nn
        return Item('The maximum number of electrons that the shell with n = %d can hold is' % nn, ans, distinct(ans, [nn * nn, 2 * nn, ans - 2], 2), ['Number of orbitals = n<sup>2</sup> = %d, each holding 2 electrons.' % (nn * nn), 'Total = 2n<sup>2</sup> = %d.' % ans], 'Giving n<sup>2</sup>, the number of orbitals.', nat=ans)
    l = r.randint(0, nn - 1)
    nm = 'spdf'[l] if l < 4 else 'g'
    if kind == 'rn':
        ans = nn - l - 1
        return Item('The number of radial nodes in a %d%s orbital is' % (nn, nm), ans, distinct(ans, [l, nn - 1, nn - l + 1], 1), ['Radial nodes = n − l − 1 = %d − %d − 1 = %d.' % (nn, l, ans)], 'Counting n − l (forgetting to subtract 1).', nat=ans)
    ans = l
    return Item('The number of angular nodes in a %d%s orbital is' % (nn, nm), ans, distinct(ans, [nn - l - 1, nn - 1, l + 1], 1), ['Angular nodes = l, and for a %s orbital l = %d.' % (nm, l)], 'Using the number of radial nodes instead.', nat=ans)


@tpl(C, 'ATS')
def bohr_radius_ratio(r):
    n1, n2 = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (2, 4)])
    Z = r.choice([1, 2, 3])
    ans = Fraction(n2 * n2, n1 * n1)
    return Item('For hydrogen-like species, the ratio of the radius of the n = %d orbit to that of the n = %d orbit (same species) is' % (n2, n1), n(ans), [n(Fraction(n2, n1)), n(Fraction(n1 * n1, n2 * n2)), n(Fraction(n2 ** 3, n1 ** 3))],
                ['r<sub>n</sub> &prop; n<sup>2</sup>/Z.', 'r<sub>%d</sub>/r<sub>%d</sub> = %d<sup>2</sup>/%d<sup>2</sup> = %s.' % (n2, n1, n2, n1, n(ans))], 'Using r &prop; n instead of n<sup>2</sup>.', nat=int(ans) if ans.denominator == 1 else None)


SPECIES = [  # (formula html, central atom, bonded atoms, lone pairs on central, steric number, shape)
    ('NH<sub>3</sub>', 'N', 3, 1, 4, 'pyramidal'), ('H<sub>2</sub>O', 'O', 2, 2, 4, 'bent'), ('SF<sub>4</sub>', 'S', 4, 1, 5, 'see-saw'), ('ClF<sub>3</sub>', 'Cl', 3, 2, 5, 'T-shaped'),
    ('XeF<sub>2</sub>', 'Xe', 2, 3, 5, 'linear'), ('XeF<sub>4</sub>', 'Xe', 4, 2, 6, 'square planar'), ('BrF<sub>5</sub>', 'Br', 5, 1, 6, 'square pyramidal'), ('SO<sub>2</sub>', 'S', 2, 1, 3, 'bent'),
    ('PCl<sub>5</sub>', 'P', 5, 0, 5, 'trigonal bipyramidal'), ('SF<sub>6</sub>', 'S', 6, 0, 6, 'octahedral'), ('CH<sub>4</sub>', 'C', 4, 0, 4, 'tetrahedral'), ('BF<sub>3</sub>', 'B', 3, 0, 3, 'trigonal planar'),
    ('XeF<sub>6</sub>', 'Xe', 6, 1, 7, 'distorted octahedral'), ('ICl<sub>2</sub><sup>−</sup>', 'I', 2, 3, 5, 'linear')]


@tpl(C, 'BON')
def lone_pairs(r):
    f, c, bp, lp, sn, shape = r.choice(SPECIES)
    kind = r.choice(['lp', 'sn'])
    if kind == 'lp':
        ans = lp
        return Item('The number of lone pairs of electrons on the central atom of %s is' % f, ans, distinct(ans, [bp, sn, lp + 1, max(lp - 1, 0)], 1),
                    ['Steric number of %s = %d (%d bond pairs + %d lone pairs).' % (c, sn, bp, lp), 'Lone pairs = %d.' % lp], 'Counting the bonded atoms instead.', nat=ans)
    ans = sn
    return Item('The steric number (bond pairs + lone pairs) of the central atom in %s, which has a %s shape, is' % (f, shape), ans, distinct(ans, [bp, lp, sn + 1], 1), ['%d bond pairs and %d lone pairs on %s.' % (bp, lp, c), 'Steric number = %d.' % sn],
                'Ignoring the lone pairs.', nat=ans)


BONDS = [('ethene (C<sub>2</sub>H<sub>4</sub>)', 5, 1), ('ethyne (C<sub>2</sub>H<sub>2</sub>)', 3, 2), ('benzene (C<sub>6</sub>H<sub>6</sub>)', 12, 3), ('ethanal (CH<sub>3</sub>CHO)', 6, 1),
         ('hydrogen cyanide (HCN)', 2, 2), ('propyne (CH<sub>3</sub>C≡CH)', 6, 2), ('buta-1,3-diene (CH<sub>2</sub>=CH–CH=CH<sub>2</sub>)', 9, 2), ('ethanoic acid (CH<sub>3</sub>COOH)', 7, 1),
         ('propene (CH<sub>3</sub>CH=CH<sub>2</sub>)', 8, 1), ('carbon dioxide (CO<sub>2</sub>)', 2, 2)]


@tpl(C, 'BON')
def sigma_pi(r):
    name, s, p = r.choice(BONDS)
    kind = r.choice(['s', 'p', 'sum'])
    ans = {'s': s, 'p': p, 'sum': s + p}[kind]
    word = {'s': 'sigma (σ) bonds', 'p': 'pi (π) bonds', 'sum': 'bonds in all (σ and π together)'}[kind]
    return Item('The number of %s in %s is' % (word, name), ans, distinct(ans, [s + p, s, p, s - 1, ans + 1], 1), ['Every bond has one σ bond; each double bond adds one π bond and each triple bond adds two.', 'Counting for %s: σ = %d, π = %d.' % (name, s, p)],
                'Counting a triple bond as one π bond.', nat=ans)


MO = [('N<sub>2</sub>', 3, 0), ('O<sub>2</sub>', 2, 2), ('O<sub>2</sub><sup>+</sup>', 2.5, 1), ('O<sub>2</sub><sup>−</sup>', 1.5, 1), ('B<sub>2</sub>', 1, 2), ('C<sub>2</sub>', 2, 0), ('N<sub>2</sub><sup>+</sup>', 2.5, 1),
      ('H<sub>2</sub><sup>+</sup>', 0.5, 1), ('F<sub>2</sub>', 1, 0), ('He<sub>2</sub>', 0, 0), ('Li<sub>2</sub>', 1, 0), ('NO', 2.5, 1)]


@tpl(C, 'BON', nat=False)
def bond_order_mo(r):
    sp, bo, unp = r.choice(MO)
    return Item('According to molecular orbital theory, the bond order of %s is' % sp, n(bo), [n(x) for x in (bo + 0.5, abs(bo - 0.5), bo + 1) if x != bo] + ['0'], ['Fill the molecular orbitals in order and use bond order = (N<sub>b</sub> − N<sub>a</sub>)/2.', 'For %s the bond order is %s.' % (sp, n(bo))],
                'Using the electron count of the neutral molecule for an ion.')


@tpl(C, 'THE', nat=False)
def gibbs(r):
    dH, dS, T = r.choice([(-40, -100, 300), (-60, -150, 300), (-100, -200, 400), (50, 100, 600), (-20, -50, 200), (30, 100, 400)])
    dG = Fraction(dH * 1000 - T * dS, 1000)
    return Item('For a reaction &Delta;H = %d kJ and &Delta;S = %d J/K. The value of &Delta;G at %d K is (in kJ)' % (dH, dS, T), n(dG), [n(dH - T * dS), n(Fraction(dH * 1000 + T * dS, 1000)), n(dH + dS)],
                ['&Delta;G = &Delta;H − T&Delta;S, with &Delta;S converted to kJ/K.', '= %d − %d × (%s) = %s kJ.' % (dH, T, n(Fraction(dS, 1000)), n(dG))], 'Not converting J to kJ.', nat=int(dG) if dG >= 0 and dG.denominator == 1 else None)


@tpl(C, 'THE', nat=False)
def hess(r):
    a, b = r.randint(20, 120), r.randint(20, 120)
    k = r.choice([2, 3])
    ans = -k * (a + b)
    ask = r.choice(['sum', 'rev'])
    if ask == 'sum':
        return Item('Given A → B, &Delta;H = −%d kJ and B → C, &Delta;H = −%d kJ, the enthalpy change for %sA → %sC is (in kJ)' % (a, b, k, k), n(ans), [n(-(a + b)), n(k * (a - b)), n(k * (a + b))],
                    ['A → C: &Delta;H = −%d + (−%d) = −%d kJ.' % (a, b, a + b), 'Multiplying the equation by %d multiplies &Delta;H: %d kJ.' % (k, ans)], 'Not scaling &Delta;H by the stoichiometric factor.')
    return Item('For A → B, &Delta;H = −%d kJ and for C → B, &Delta;H = −%d kJ. The enthalpy change for A → C is (in kJ)' % (a, b), n(-a + b), [n(-a - b), n(a - b), n(a + b)],
                ['Reverse C → B to get B → C with &Delta;H = +%d kJ.' % b, 'A → B → C: −%d + %d = %d kJ.' % (a, b, -a + b)], 'Forgetting to change the sign when reversing a reaction.')


@tpl(C, 'EQU')
def equilibrium_k(r):
    while True:
        a, b, c = r.randint(1, 3), r.randint(1, 3), r.randint(2, 12)
        K = Fraction(c * c, a * b ** 3)
        if K.denominator == 1 and K <= 400:
            break
    return Item('For N<sub>2</sub> + 3H<sub>2</sub> ⇌ 2NH<sub>3</sub> the equilibrium concentrations are [N<sub>2</sub>] = %d M, [H<sub>2</sub>] = %d M and [NH<sub>3</sub>] = %d M. The value of K<sub>c</sub> is' % (a, b, c), n(K),
                [n(Fraction(a * b ** 3, c * c)), n(Fraction(c, a * b)), n(Fraction(c * c, a * b * 3))], ['K<sub>c</sub> = [NH<sub>3</sub>]<sup>2</sup>/([N<sub>2</sub>][H<sub>2</sub>]<sup>3</sup>).', '= %d<sup>2</sup>/(%d × %d<sup>3</sup>) = %d/%d = %s.' % (c, a, b, c * c, a * b ** 3, n(K))],
                'Writing the ratio upside-down or ignoring the stoichiometric powers.', nat=int(K))


@tpl(C, 'EQU')
def ph_calc(r):
    kind = r.choice(['hcl', 'ba', 'naoh', 'buf'])
    if kind == 'hcl':
        k = r.randint(1, 5)
        ans = k
        return Item('The pH of a 10<sup>−%d</sup> M aqueous HCl solution at 25&deg;C is' % k if k < 7 else '', ans, distinct(ans, [14 - k, k + 1, k - 1 if k > 1 else 7], 1), ['HCl is a strong acid: [H<sup>+</sup>] = 10<sup>−%d</sup> M.' % k, 'pH = −log[H<sup>+</sup>] = %d.' % k], 'Confusing pH with pOH.', nat=ans)
    if kind == 'ba':
        k = r.randint(2, 5)
        ans = 14 - k
        return Item('The pH of a 5 × 10<sup>−%d</sup> M Ba(OH)<sub>2</sub> solution at 25&deg;C is (log 2 = 0.3; take [OH<sup>−</sup>] = 10<sup>−%d</sup> M)' % (k + 1, k), ans, distinct(ans, [k, 14 - k - 1, 14 - k + 1], 1),
                    ['Each Ba(OH)<sub>2</sub> gives 2 OH<sup>−</sup>: [OH<sup>−</sup>] = 2 × 5 × 10<sup>−%d</sup> = 10<sup>−%d</sup> M.' % (k + 1, k), 'pOH = %d, so pH = 14 − %d = %d.' % (k, k, ans)], 'Forgetting that Ba(OH)<sub>2</sub> supplies two OH<sup>−</sup>.', nat=ans)
    if kind == 'naoh':
        k = r.randint(2, 5)
        ans = 14 - k
        return Item('The pH of a 10<sup>−%d</sup> M NaOH solution at 25&deg;C is' % k, ans, distinct(ans, [k, 14 - k + 1, 7 + k], 1), ['pOH = %d.' % k, 'pH = 14 − pOH = %d.' % ans], 'Reporting pOH as the pH.', nat=ans)
    pka, ratio = r.choice([(4, 10), (5, 100), (4, 1), (6, 10), (5, 1)])
    ans = pka + int(math.log10(ratio))
    return Item('A buffer contains an acid HA (pK<sub>a</sub> = %d) and its salt with [A<sup>−</sup>]/[HA] = %d. Its pH is' % (pka, ratio), ans, distinct(ans, [pka - int(math.log10(ratio)), pka + 1 if ratio != 10 else pka + 2, pka * 2], 1),
                ['Henderson–Hasselbalch: pH = pK<sub>a</sub> + log([A<sup>−</sup>]/[HA]).', '= %d + log %d = %d.' % (pka, ratio, ans)], 'Inverting the salt/acid ratio.', nat=ans)


OXN = [('Mn in KMnO<sub>4</sub>', 7), ('Cr in K<sub>2</sub>Cr<sub>2</sub>O<sub>7</sub>', 6), ('S in H<sub>2</sub>SO<sub>4</sub>', 6), ('N in HNO<sub>3</sub>', 5), ('P in H<sub>3</sub>PO<sub>4</sub>', 5), ('Cl in HClO<sub>4</sub>', 7),
       ('Cr in CrO<sub>4</sub><sup>2−</sup>', 6), ('Mn in MnO<sub>4</sub><sup>2−</sup>', 6), ('S in SO<sub>3</sub><sup>2−</sup>', 4), ('N in NO<sub>2</sub>', 4), ('C in HCOOH', 2), ('Fe in K<sub>4</sub>[Fe(CN)<sub>6</sub>]', 2),
       ('Fe in K<sub>3</sub>[Fe(CN)<sub>6</sub>]', 3), ('S in S<sub>2</sub>O<sub>8</sub><sup>2−</sup> (peroxodisulphate, including the peroxide bond)', 6), ('N in NH<sub>4</sub><sup>+</sup>', -3), ('Cl in KClO<sub>3</sub>', 5)]


@tpl(C, 'RDX')
def oxidation_number(r):
    name, v = r.choice(OXN)
    return Item('The oxidation number of %s is' % name, sgn(v) if v < 0 else '+%d' % v, [('+%d' % x if x > 0 else sgn(x)) for x in (v + 1, v - 1, v + 2, -v if v != 0 else 1) if x != v][:4],
                ['Assign O = −2 (or the usual values) and balance the total charge.', 'Solving gives %s = %s.' % (name.split(' in ')[0], ('+%d' % v) if v > 0 else sgn(v))], 'Forgetting the overall charge on the ion.',
                nat=v if v > 0 else None, nat_stem='Find the oxidation number of %s.' % name)


@tpl(C, 'RDX')
def faraday(r):
    metal, M_, z = r.choice([('silver', 108, 1), ('copper', 64, 2), ('aluminium', 27, 3), ('zinc', 65, 2), ('nickel', 58.5, 2)])
    mol_e = r.choice([0.5, 1, 2, 3, 6])
    Q = int(mol_e * 96500)
    m = Fraction(str(mol_e)) / z * Fraction(str(M_))
    return Item('The mass of %s (molar mass %s g/mol, ion charge %d+) deposited by passing %d C of charge is (in g; F = 96500 C/mol)' % (metal, n(M_), z, Q), n(m),
                [n(Fraction(str(mol_e)) * Fraction(str(M_))), n(Fraction(str(mol_e)) * Fraction(str(M_)) / z / 2), n(Fraction(str(mol_e)) / z)], ['Moles of electrons = %d/96500 = %s.' % (Q, n(mol_e)), 'Moles of metal = %s/%d.' % (n(mol_e), z), 'Mass = %s × %s = %s g.' % (n(Fraction(str(mol_e)) / z), n(M_), n(m))],
                'Ignoring the charge on the ion.', nat=int(m) if m == int(m) else None)


@tpl(C, 'CKN')
def half_lives(r):
    N0, k = r.choice([(800, 3), (640, 4), (100, 2), (1000, 3), (512, 5), (96, 3)])
    ans = Fraction(N0, 2 ** k)
    return Item('A first-order reaction has %s g of reactant initially. After %d half-lives the amount left is (in g)' % (n(N0), k), n(ans), [n(Fraction(N0, k)), n(Fraction(N0, 2 * k)), n(Fraction(N0, 2 ** (k - 1)))],
                ['After each half-life the amount halves.', 'Left = %d/2<sup>%d</sup> = %d/%d = %s g.' % (N0, k, N0, 2 ** k, n(ans))], 'Dividing by the number of half-lives instead of 2 raised to it.', nat=int(ans) if ans.denominator == 1 else None)


@tpl(C, 'CKN')
def rate_order(r):
    a, b = r.randint(0, 2), r.randint(0, 2)
    if a + b == 0:
        a = 1
    fa, fb = 2 ** a, 2 ** b
    return Item('For a reaction A + B → products, doubling [A] alone raises the rate %s times, and doubling [B] alone raises it %s times. The overall order of the reaction is' % (n(fa), n(fb)), a + b, distinct(a + b, [fa + fb, fa * fb, a * b + 1], 1),
                ['Rate &prop; [A]<sup>x</sup>[B]<sup>y</sup>: 2<sup>x</sup> = %d gives x = %d and 2<sup>y</sup> = %d gives y = %d.' % (fa, a, fb, b), 'Overall order = x + y = %d.' % (a + b)], 'Adding the rate factors instead of the exponents.', nat=a + b)


@tpl(C, 'SOL')
def raoult(r):
    while True:
        na, nb = r.randint(1, 5), r.randint(1, 5)
        pa, pb = r.choice([100, 200, 300, 400, 500]), r.choice([100, 200, 300, 400, 500])
        if pa != pb:
            tot = Fraction(na * pa + nb * pb, na + nb)
            if tot.denominator == 1:
                break
    return Item('Liquids A and B form an ideal solution of %d mol A and %d mol B. Their vapour pressures when pure are %d mm Hg and %d mm Hg. The total vapour pressure of the solution is (in mm Hg)' % (na, nb, pa, pb), n(tot),
                [n(Fraction(pa + pb, 2)), n(pa + pb), n(Fraction(na * pa, na + nb))], ['x<sub>A</sub> = %d/%d, x<sub>B</sub> = %d/%d.' % (na, na + nb, nb, na + nb), 'P = x<sub>A</sub>P<sub>A</sub>&deg; + x<sub>B</sub>P<sub>B</sub>&deg; = %s mm Hg.' % n(tot)],
                'Averaging the two pure vapour pressures without weighting by mole fraction.', nat=int(tot))


@tpl(C, 'SOL', nat=False)
def freezing_point(r):
    nonlocal_i = r.choice([1, 2, 3])
    sol = {1: 'glucose', 2: 'NaCl (assume complete dissociation)', 3: 'CaCl<sub>2</sub> (assume complete dissociation)'}[nonlocal_i]
    m = r.choice([0.1, 0.2, 0.5, 1])
    Kf = 1.86
    dT = round(Kf * m * nonlocal_i, 3)
    return Item('The depression in freezing point of a %s m aqueous solution of %s is (K<sub>f</sub> = 1.86 K kg/mol; in K)' % (n(m), sol), n(dT), [n(round(Kf * m, 3)), n(round(Kf * m * (nonlocal_i + 1), 3)), n(round(Kf / m, 3))],
                ['&Delta;T<sub>f</sub> = i K<sub>f</sub> m with van\'t Hoff factor i = %d.' % nonlocal_i, '= %d × 1.86 × %s = %s K.' % (nonlocal_i, n(m), n(dT))], 'Using i = 1 for an electrolyte.')


@tpl(C, 'PER', nat=False)
def periodic_trend(r):
    ie = {'Li': 520, 'Be': 899, 'B': 801, 'C': 1086, 'N': 1402, 'O': 1314, 'F': 1681, 'Ne': 2081}
    en = {'F': 4.0, 'O': 3.5, 'N': 3.0, 'Cl': 3.0, 'C': 2.5, 'S': 2.5, 'H': 2.1, 'Si': 1.8, 'Al': 1.5, 'Mg': 1.2, 'Na': 0.9, 'K': 0.8}
    kind = r.choice(['ie_hi', 'ie_lo', 'en_hi', 'en_lo'])
    if kind.startswith('ie'):
        els = r.sample(list(ie), 4)
        pick = max(els, key=lambda e: ie[e]) if kind == 'ie_hi' else min(els, key=lambda e: ie[e])
        return Item('Among %s, the element with the %s first ionisation enthalpy is' % (', '.join(els), 'highest' if kind == 'ie_hi' else 'lowest'), pick, [e for e in els if e != pick],
                    ['First ionisation enthalpies (kJ/mol): ' + ', '.join('%s %d' % (e, ie[e]) for e in els) + '.', 'The %s value belongs to %s.' % ('highest' if kind == 'ie_hi' else 'lowest', pick)], 'Forgetting the dips at Be/B and N/O.')
    while True:
        els = r.sample(list(en), 4)
        vals = sorted(en[e] for e in els)
        if len(set(vals)) == 4:
            break
    pick = max(els, key=lambda e: en[e]) if kind == 'en_hi' else min(els, key=lambda e: en[e])
    return Item('Among %s, the element with the %s electronegativity (Pauling scale) is' % (', '.join(els), 'highest' if kind == 'en_hi' else 'lowest'), pick, [e for e in els if e != pick],
                ['Pauling values: ' + ', '.join('%s %s' % (e, en[e]) for e in els) + '.', '%s has the %s value.' % (pick, 'highest' if kind == 'en_hi' else 'lowest')], 'Reading the trend down a group the wrong way.')


COMPLEX = [('[Fe(CN)<sub>6</sub>]<sup>4−</sup>', 'Fe<sup>2+</sup>', 6, 0), ('[Fe(H<sub>2</sub>O)<sub>6</sub>]<sup>2+</sup>', 'Fe<sup>2+</sup>', 6, 4), ('[Co(NH<sub>3</sub>)<sub>6</sub>]<sup>3+</sup>', 'Co<sup>3+</sup>', 6, 0),
           ('[CoF<sub>6</sub>]<sup>3−</sup>', 'Co<sup>3+</sup>', 6, 4), ('[Cr(H<sub>2</sub>O)<sub>6</sub>]<sup>3+</sup>', 'Cr<sup>3+</sup>', 6, 3), ('[Ni(CO)<sub>4</sub>]', 'Ni (0)', 4, 0), ('[Mn(CN)<sub>6</sub>]<sup>3−</sup>', 'Mn<sup>3+</sup>', 6, 2),
           ('[NiCl<sub>4</sub>]<sup>2−</sup>', 'Ni<sup>2+</sup>', 4, 2), ('[Ti(H<sub>2</sub>O)<sub>6</sub>]<sup>3+</sup>', 'Ti<sup>3+</sup>', 6, 1), ('[Cu(NH<sub>3</sub>)<sub>4</sub>]<sup>2+</sup>', 'Cu<sup>2+</sup>', 4, 1)]


@tpl(C, 'COO')
def unpaired_complex(r):
    f, ion, cn, un = r.choice(COMPLEX)
    kind = r.choice(['un', 'mu', 'cn'])
    if kind == 'un':
        return Item('The number of unpaired electrons in the complex %s is' % f, un, distinct(un, [un + 1, un + 2, max(un - 1, 0), 5], 1), ['The metal ion is %s; use the ligand field strength to decide high-spin or low-spin filling.' % ion, 'Unpaired electrons = %d.' % un],
                    'Assuming high-spin for every complex.', nat=un)
    if kind == 'mu':
        mu = round(math.sqrt(un * (un + 2)), 2)
        opts = [n(round(math.sqrt(k * (k + 2)), 2)) for k in range(0, 6) if k != un]
        return Item('The spin-only magnetic moment of %s is (in BM)' % f, n(mu), opts[:5], ['Unpaired electrons = %d (metal ion %s).' % (un, ion), '&mu; = √[n(n + 2)] = √[%d × %d] = %s BM.' % (un, un + 2, n(mu))], 'Using n instead of √[n(n + 2)].')
    return Item('The coordination number of the metal in %s is' % f, cn, [x for x in (cn + 2, cn - 2, 8, 2, 3) if x != cn][:4], ['Coordination number = number of donor atoms attached to the metal = %d.' % cn], 'Counting ligands where some are bidentate.', nat=cn)


DBE = [('C<sub>6</sub>H<sub>6</sub>', 6, 6, 0, 0), ('C<sub>7</sub>H<sub>8</sub>', 7, 8, 0, 0), ('C<sub>8</sub>H<sub>10</sub>', 8, 10, 0, 0), ('C<sub>3</sub>H<sub>6</sub>O', 3, 6, 0, 0), ('C<sub>5</sub>H<sub>5</sub>N', 5, 5, 1, 0),
       ('C<sub>2</sub>H<sub>5</sub>Cl', 2, 5, 0, 1), ('C<sub>4</sub>H<sub>6</sub>', 4, 6, 0, 0), ('C<sub>10</sub>H<sub>8</sub>', 10, 8, 0, 0), ('C<sub>3</sub>H<sub>4</sub>O<sub>2</sub>', 3, 4, 0, 0), ('C<sub>6</sub>H<sub>5</sub>NO<sub>2</sub>', 6, 5, 1, 0), ('C<sub>6</sub>H<sub>12</sub>', 6, 12, 0, 0)]


@tpl(C, 'ORG')
def dbe(r):
    f, c, h, nn, x = r.choice(DBE)
    ans = (2 * c + 2 + nn - h - x) // 2
    return Item('The degree of unsaturation (double-bond equivalents) of %s is' % f, ans, distinct(ans, [ans + 1, ans - 1, ans + 2, max(ans - 2, 0)], 1), ['DBE = (2C + 2 + N − H − X)/2 (oxygen does not count).', '= (%d + 2 + %d − %d − %d)/2 = %d.' % (2 * c, nn, h, x, ans)], 'Counting oxygen or forgetting that N adds 1.', nat=ans)


@tpl(C, 'ORG')
def isomer_counts(r):
    tbl = [('alkane C<sub>4</sub>H<sub>10</sub>', 2), ('alkane C<sub>5</sub>H<sub>12</sub>', 3), ('alkane C<sub>6</sub>H<sub>14</sub>', 5), ('alkane C<sub>7</sub>H<sub>16</sub>', 9),
           ('compound C<sub>3</sub>H<sub>8</sub>O (alcohols and ethers)', 3), ('compound C<sub>4</sub>H<sub>10</sub>O (alcohols and ethers)', 7), ('compound C<sub>2</sub>H<sub>6</sub>O (alcohols and ethers)', 2),
           ('amine C<sub>3</sub>H<sub>9</sub>N (all amines)', 4), ('amine C<sub>4</sub>H<sub>11</sub>N (all amines)', 8), ('carbonyl compounds C<sub>4</sub>H<sub>8</sub>O (aldehydes and ketones)', 3),
           ('carbonyl compounds C<sub>5</sub>H<sub>10</sub>O (aldehydes and ketones)', 7)]
    name, ans = r.choice(tbl)
    return Item('The number of structural isomers (ignoring stereoisomers) of the %s is' % name, ans, distinct(ans, [ans + 1, ans - 1, ans + 2, ans * 2], 1), ['Enumerate carbon skeletons, then place the functional group.', 'The count is %d.' % ans],
                'Missing a branched skeleton or counting stereoisomers.', nat=ans)


@tpl(C, 'HYD')
def hydrogenation(r):
    tbl = [('buta-1,3-diene', 2), ('but-1-yne', 2), ('benzene', 3), ('propene', 1), ('hex-1-en-5-yne', 3), ('cyclohexene', 1), ('naphthalene (C<sub>10</sub>H<sub>8</sub>, complete hydrogenation)', 5),
           ('penta-1,4-diene', 2), ('ethyne', 2), ('toluene (complete ring hydrogenation)', 3)]
    name, ans = r.choice(tbl)
    return Item('The number of moles of H<sub>2</sub> needed to hydrogenate 1 mole of %s completely is' % name, ans, distinct(ans, [ans + 1, ans - 1, ans + 2, 2 * ans], 1), ['Add 1 mol H<sub>2</sub> per C=C (or per ring in a saturated ring), 2 mol per C≡C, and 3 mol per benzene ring.', 'Total = %d mol.' % ans],
                'Counting a triple bond as taking one mole.', nat=ans)


@tpl(C, 'HYD')
def combustion_o2(r):
    while True:
        c, h = r.randint(2, 8), r.randint(4, 18)
        if h % 4 == 0 and h <= 2 * c + 2:
            break
    ans = c + h // 4
    f = 'C<sub>%d</sub>H<sub>%d</sub>' % (c, h)
    return Item('The number of moles of O<sub>2</sub> required for complete combustion of 1 mole of the hydrocarbon %s is' % f, ans, distinct(ans, [c + h // 2, c, c + h], 1),
                ['C<sub>x</sub>H<sub>y</sub> + (x + y/4)O<sub>2</sub> → xCO<sub>2</sub> + (y/2)H<sub>2</sub>O.', 'x + y/4 = %d + %d = %d.' % (c, h // 4, ans)], 'Using y/2 instead of y/4.', nat=ans)


@tpl(C, 'HAL')
def monochlorination(r):
    tbl = [('propane', 2), ('n-butane', 2), ('isobutane (2-methylpropane)', 2), ('n-pentane', 3), ('neopentane (2,2-dimethylpropane)', 1), ('cyclohexane', 1), ('2,2-dimethylbutane', 3),
           ('2,3-dimethylbutane', 2), ('toluene (ring and side chain)', 4), ('benzene', 1)]
    name, ans = r.choice(tbl)
    return Item('The number of different monochloro structural isomers obtainable from %s by free-radical chlorination (ignore stereoisomers) is' % name, ans, distinct(ans, [ans + 1, ans + 2, max(ans - 1, 1)], 1),
                ['Count the sets of equivalent hydrogens: each set gives one monochloro product.', 'Number of sets = %d.' % ans], 'Counting every hydrogen as different.', nat=ans)


@tpl(C, 'HAL')
def sn_rates(r):
    k = r.choice([2, 3])
    mech = r.choice(['SN1', 'SN2'])
    ans = k if mech == 'SN1' else k * k
    rate = 'k[RX]' if mech == 'SN1' else 'k[RX][Nu<sup>−</sup>]'
    return Item('The rate law of a substitution reaction is rate = %s. If the concentrations of both RX and Nu<sup>−</sup> are multiplied by %d, the rate changes by a factor of' % (rate, k), ans, distinct(ans, [k, k * k, 2 * k, 1], 1),
                ['The rate depends only on the species present in the rate law, each to its own power.', 'Factor = %s.' % ('%d' % ans)], 'Counting a species that is not in the rate law.', nat=ans)


@tpl(C, 'BIO')
def peptides(r):
    kind = r.choice(['bonds', 'dip', 'tri'])
    if kind == 'bonds':
        k = r.randint(4, 20)
        return Item('The number of peptide bonds in a linear polypeptide made from %d amino acid residues is' % k, k - 1, distinct(k - 1, [k, k + 1, k - 2], 1), ['n residues joined in a chain have n − 1 peptide bonds.'], 'Counting one bond per residue.', nat=k - 1)
    if kind == 'dip':
        k = r.randint(2, 5)
        return Item('The number of different dipeptides that can be formed from %d different amino acids (each may be used more than once) is' % k, k * k, distinct(k * k, [k * (k - 1), 2 * k, math.comb(k, 2)], 1), ['Two positions, each with %d choices: %d<sup>2</sup> = %d.' % (k, k, k * k)], 'Using k(k − 1), which does not allow repeats.', nat=k * k)
    k = r.randint(2, 4)
    return Item('The number of different tripeptides that can be formed from %d different amino acids if each amino acid may be used any number of times is' % k, k ** 3, distinct(k ** 3, [k * (k - 1) * (k - 2) if k > 2 else 6, 3 * k, k ** 2], 1),
                ['Three positions, each with %d choices.' % k, 'Total = %d<sup>3</sup> = %d.' % (k, k ** 3)], 'Not allowing a repeated amino acid.', nat=k ** 3)
