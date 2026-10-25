"""Framework for the EduAakashaa JEE Main practice mocks.

A template is a function f(r) -> Item(...), where `r` is a random.Random. The answer is *computed* in the template, so the key can never disagree
with the working. Each template can produce an MCQ (4 options) and, when `nat_ok`, a numerical (integer) question.
"""
import math
import random
from fractions import Fraction

REG = {'MATH': [], 'PHY': [], 'CHEM': []}


class Item:
    """stem: html. ans: displayed correct option (MCQ). wrong: list of plausible wrong options (same style). nat: integer answer or None."""

    def __init__(self, stem, ans, wrong, steps, trap='', nat=None, nat_stem=None):
        self.stem, self.ans, self.wrong, self.steps, self.trap, self.nat, self.nat_stem = stem, ans, list(wrong), steps, trap, nat, nat_stem


def tpl(subj, cat, nat=True, weight=1):
    def deco(fn):
        REG[subj].append({'fn': fn, 'cat': cat, 'nat': nat, 'weight': weight, 'name': fn.__name__})
        return fn
    return deco


# ---- number formatting helpers -------------------------------------------------------------------------------------------------
def n(x):
    """Plain number: integers without a decimal point, floats trimmed."""
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = ('%.4f' % x).rstrip('0').rstrip('.')
        return s
    return str(x)


def sgn(x):
    s = n(abs(x))
    return ('−' if x < 0 else '') + s


def sup(base, e):
    return '%s<sup>%s</sup>' % (base, e)


def sub(base, e):
    return '%s<sub>%s</sub>' % (base, e)


def distinct(ans, wrong, spread=None, fmt=str):
    """Return exactly 3 distinct wrong options that differ from ans (padding with nearby values if needed)."""
    out, seen = [], {str(ans)}
    for w in wrong:
        s = str(w)
        if s not in seen:
            seen.add(s)
            out.append(w)
    k = 1
    while len(out) < 3 and spread is not None:
        for cand in (ans + k * spread, ans - k * spread):
            s = fmt(cand)
            if s not in seen and len(out) < 3:
                seen.add(s)
                out.append(cand)
        k += 1
    return out[:3]


def build_question(entry, r, want_nat):
    """Run a template until it yields a valid item of the wanted kind. Returns a dict (without n/section fields)."""
    for _ in range(40):
        it = entry['fn'](r)
        if want_nat:
            if it.nat is None or int(it.nat) != it.nat or it.nat < 0 or it.nat > 99999:
                continue
            return dict(t='NAT', cat=entry['cat'], stem=it.nat_stem or it.stem, ans=int(it.nat), steps=it.steps, trap=it.trap, name=entry['name'])
        wrong = [str(w) for w in it.wrong]
        opts = []
        seen = {str(it.ans)}
        for w in wrong:
            if w not in seen:
                seen.add(w)
                opts.append(w)
        if len(opts) < 3:
            continue
        opts = opts[:3] + [str(it.ans)]
        r.shuffle(opts)
        return dict(t='MCQ', cat=entry['cat'], stem=it.stem, opts=opts, ans=opts.index(str(it.ans)), steps=it.steps, trap=it.trap, name=entry['name'])
    raise RuntimeError('template %s could not produce a %s question' % (entry['name'], 'NAT' if want_nat else 'MCQ'))


def pick_templates(subj, count, nat_count, r, used_names):
    """Choose `count` MCQ templates and `nat_count` NAT templates for a paper, spreading chapters and limiting repeats."""
    pool = REG[subj]
    nat_pool = [e for e in pool if e['nat']]

    def draw(src, k, taken):
        out = []
        by_cat_used = {}
        cands = src[:]
        r.shuffle(cands)
        # first pass: one per template, preferring chapters not yet used; second pass allows repeats
        while len(out) < k:
            cands.sort(key=lambda e: (taken.get(e['name'], 0), by_cat_used.get(e['cat'], 0), r.random()))
            e = cands[0]
            out.append(e)
            taken[e['name']] = taken.get(e['name'], 0) + 1
            by_cat_used[e['cat']] = by_cat_used.get(e['cat'], 0) + 1
        return out
    taken = {}
    mcq = draw(pool, count, taken)
    nat = draw(nat_pool, nat_count, taken)
    return mcq, nat
