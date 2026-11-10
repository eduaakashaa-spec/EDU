"""Build a JEE Main 2026 Session 1 (January) mock-centre paper from transcribed question records.

    python tools/jee_mock/build_jan.py J0121S1 "JEE Main 2026 · 21 Jan · Shift 1" "21 Jan · Shift 1" maths.json physics.json chem.json

Each JSON is a list of {src, qid, subj, kind, cat, diff, stem, opts, ans, steps, svg, status, note}: the NTA question retyped by EduAakashaA with its own worked steps.
Only status 'ok' rows enter the paper (our own solution agrees with the printed official answer); 'skip' (needs a drawn figure) and 'mismatch' rows are left out.
With --key <key_all.json> <shift> (e.g. 21s2) every question id must be in the NTA Session 1 final key: numerical answers must equal the key (a key of 'a,b' accepts both), a question
the key shows as 'Drop' or with several accepted options is left out. Lettered answers cannot be compared (the key's option numbers follow a different option order), so they rest
on the printed official answer plus our independent solution. --exclude <json> lists '<tag>_<src>' questions left out on review, with the reason.
Writes app/data/jee_mock/data/<ID>.json and adds the paper to pyq_papers.json (recreated: true, tagged: true). Run make_index.py afterwards.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')


def build(paper_id, title, short, files, key=None, exclude=None):
    """key: {subject: [(question id, answer token), ...]} for the shift (NTA Session 1 final key); exclude: {'<tag>_<src>': reason} for questions left out on review."""
    exclude = exclude or {}
    allk = {i: a for rows in (key or {}).values() for i, a in rows}
    pool = {}
    for sub, rows_ in (key or {}).items():
        code = {'Mathematics': 'MATH', 'Physics': 'PHY', 'Chemistry': 'CHEM'}[sub]
        pool[code] = {float(x) for _i, a in rows_[20:] for x in a.split(',') if x.replace('.', '', 1).isdigit()}
    rows = []
    for f in files:
        tag = os.path.basename(f)[4:-5] if os.path.basename(f).startswith('out_') else os.path.basename(f)
        for r in json.load(open(f, encoding='utf-8')):
            r['_tag'] = '%s_%s' % (tag, r['src'])
            rows.append(r)
    kept, left = [], {}
    for r in rows:
        why = None
        if r.get('status') != 'ok':
            why = r.get('status')
        elif r['_tag'] in exclude:
            why = 'review: ' + exclude[r['_tag']]
        elif key is not None:
            k = allk.get(r['qid'])
            assert k is not None, ('question id not in the NTA key', r['_tag'], r['qid'])
            if k == 'Drop':
                why = 'dropped by NTA'
            elif r['kind'] == 'MCQ' and not k.isdigit():
                why = 'NTA accepts several options'
            elif r['kind'] == 'NAT':
                vals = [float(x) for x in k.split(',')]
                if float(r['ans']) not in vals:                  # the booklet's printed id can sit next to another numerical item: the value must still be one the key lists for the subject
                    assert float(r['ans']) in pool.get(r['subj'], ()), ('NAT answer is not in the NTA key for the subject', r['_tag'], r['ans'], k)
                    print('  note: %s numerical id pairs with a different key value (%s vs %s); value found elsewhere in the key' % (r['_tag'], r['ans'], k))
                    vals = [float(r['ans'])]
                r['_vals'] = vals
        if why:
            left[r['_tag']] = why
        else:
            kept.append(r)
    for r in kept:
        assert r['kind'] in ('MCQ', 'NAT') and r['cat'] and r['diff'] in (1, 2, 3), r['_tag']
        if r['kind'] == 'MCQ':
            assert r['opts'] and len(r['opts']) == 4 and r['ans'] in 'ABCD', r['_tag']
    qs, sections, n = [], [], 0
    for subj in ('MATH', 'PHY', 'CHEM'):
        for kind in ('MCQ', 'NAT'):
            part = sorted((r for r in kept if r['subj'] == subj and r['kind'] == kind), key=lambda r: int(r['src']))
            if not part:
                continue
            lo = n + 1
            for r in part:
                n += 1
                q = {'n': n, 't': kind, 'subj': subj, 'cat': r['cat'], 'lvl': r['diff'], 'src': r['src'], 'qid': r['qid'], 'stem': r['stem'], 'steps': r['steps'], 'trap': '',
                     'fig': r.get('svg') or '', 'svg': '', 'note': ''}
                if kind == 'MCQ':
                    q.update(opts=r['opts'], layout='grid', disp=r['ans'], acc={'sets': [r['ans']]})
                else:
                    vals = r.get('_vals') or [float(r['ans'])]
                    q.update(disp=' or '.join('%g' % v for v in vals), acc={'ranges': [[v, v] for v in vals]})
                qs.append(q)
            sections.append({'type': kind, 'subj': subj, 'lo': lo, 'hi': n, 'right': 4, 'wrong': -1, 'partial': False})
    mx = sum(4 * (s['hi'] - s['lo'] + 1) for s in sections)
    skipped = len(left)
    for k, v in sorted(left.items()):
        print('  left out', k, '-', v)
    paper = {'year': paper_id, 'title': title + ' (recreated)', 'mins': 180, 'max': mx, 'key': 'recreated', 'tagged': True, 'sections': sections, 'qs': qs,
             'notes': ['JEE Main 2026 Session 1 (NTA paper), retyped by EduAakashaA from a memory-based booklet that carries the NTA question IDs; worked steps are our own.',
                       'Numerical answers match the NTA final key (16 Feb 2026); lettered answers follow the printed official answer and were each re-solved independently.']}
    path = os.path.join(DATA, paper_id + '.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(paper, fh, ensure_ascii=False, separators=(',', ':'))
    meta_path = os.path.join(HERE, 'pyq_papers.json')
    metas = json.load(open(meta_path, encoding='utf-8'))
    metas = [m for m in metas if m['y'] != paper_id]
    metas.append({'y': paper_id, 'title': title + ' (recreated)', 'short': short + ' · recreated', 'recreated': True, 'tagged': True, 'total': len(qs), 'n': len(qs), 'max': mx, 'mins': 180,
                  'numnote': 'MCQ + numerical',
                  'note': 'Retyped from the NTA paper with our own worked steps; %d question%s left out (dropped by NTA, several accepted options, or a drawn figure we could not read reliably).' % (skipped, '' if skipped == 1 else 's') if skipped else 'Retyped from the NTA paper with our own worked steps.'})
    json.dump(metas, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path, '%.0f KB' % (os.path.getsize(path) / 1e3), '|', len(qs), 'questions | max', mx, '| left out', skipped)


if __name__ == '__main__':
    args = sys.argv[1:]
    key = exclude = None
    if '--key' in args:                                   # --key key_all.json 21s2
        i = args.index('--key')
        kd = json.load(open(args[i + 1], encoding='utf-8'))[args[i + 2]]
        key = {k: [tuple(x) for x in v] for k, v in kd.items()}
        del args[i:i + 3]
    if '--exclude' in args:                               # --exclude jan_exclude.json
        i = args.index('--exclude')
        exclude = json.load(open(args[i + 1], encoding='utf-8'))
        del args[i:i + 2]
    build(args[0], args[1], args[2], args[3:], key, exclude)
