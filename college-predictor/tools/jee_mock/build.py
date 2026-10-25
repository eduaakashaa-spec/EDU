"""Build the five EduAakashaa JEE Main practice mocks (M1-M5): 75 questions each in the 2027 pattern (per subject 20 MCQ + 5 numerical, +4 / -1).

    python tools/jee_mock/build.py            # writes app/data/jee_mock/data/M1.json ... M5.json
Every answer is computed by the template that wrote the question. Run with a different SEED_BASE for a fresh set.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
import chem_t, math_t, phys_t  # noqa: F401  (registers the templates)

OUT = os.environ.get('JEE_DATA_DIR') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'jee_mock', 'data')
SEED_BASE = int(os.environ.get('SEED_BASE', '2027'))
SUBJ = [('MATH', 'Mathematics'), ('PHY', 'Physics'), ('CHEM', 'Chemistry')]


def make_paper(idx, seen_stems):
    r = random.Random(SEED_BASE * 100 + idx)
    qs, sections, n = [], [], 0
    for subj, _ in SUBJ:
        mcq_t, nat_t = kit.pick_templates(subj, 20, 5, r, set())
        for kind, entries, count in (('MCQ', mcq_t, 20), ('NAT', nat_t, 5)):
            lo = n + 1
            local = set()
            for e in entries:
                pool = [x for x in kit.REG[subj] if x['nat'] or kind == 'MCQ']
                alts = [e] + r.sample(pool, len(pool))             # a template with few parameter combinations falls back to another one
                q = None
                for cand in alts:
                    for attempt in range(25):
                        q = kit.build_question(cand, r, kind == 'NAT')
                        if q['stem'] not in local and q['stem'] not in seen_stems:
                            break
                    else:
                        continue
                    break
                else:
                    raise RuntimeError('no unused question left for %s %s' % (subj, kind))
                local.add(q['stem'])
                seen_stems.add(q['stem'])
                n += 1
                d = {'n': n, 't': q['t'], 'subj': subj, 'cat': q['cat'], 'stem': q['stem'], 'steps': q['steps'], 'trap': q['trap'], 'fig': '', 'svg': '', 'note': ''}
                if q['t'] == 'MCQ':
                    d['opts'] = q['opts']
                    d['layout'] = 'grid' if max(len(o) for o in q['opts']) < 22 else 'list'
                    d['disp'] = 'ABCD'[q['ans']]
                    d['acc'] = {'sets': ['ABCD'[q['ans']]]}
                else:
                    d['disp'] = str(q['ans'])
                    d['acc'] = {'ranges': [[float(q['ans']), float(q['ans'])]]}
                qs.append(d)
            sections.append({'type': kind, 'subj': subj, 'lo': lo, 'hi': n, 'right': 4, 'wrong': -1, 'partial': False})
    return {'year': 'M%d' % idx, 'mins': 180, 'max': 300, 'sections': sections, 'qs': qs}


def main():
    os.makedirs(OUT, exist_ok=True)
    seen = set()
    for i in range(1, 6):
        p = make_paper(i, seen)
        assert len(p['qs']) == 75
        with open(os.path.join(OUT, 'M%d.json' % i), 'w', encoding='utf-8') as f:
            json.dump(p, f, ensure_ascii=False, separators=(',', ':'))
        from collections import Counter
        c = Counter(q['cat'] for q in p['qs'])
        print('M%d' % i, len(p['qs']), 'questions;', len(c), 'chapters; most repeated:', c.most_common(3))


if __name__ == '__main__':
    main()
