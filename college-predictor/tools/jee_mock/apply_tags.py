"""Add chapter tags to previous-year paper JSONs made by extract_pyq.py (after apply_key.py).

    python tools/jee_mock/apply_tags.py app/data/jee_mock/data/P0402S1.json tags.json

tags.json:  {"paper": "P0402S1", "tags": {"1": {"cat": "CNQ", "chapter": "Complex numbers", "diff": 2}, ...}}
  cat      a code of the JEE taxonomy in app/services/reinforce.py (JEE_TAXONOMY), from the question's own subject
  chapter  the chapter name as JEE Main names it (free text, shown in the report)
  diff     1 easy, 2 medium, 3 hard (a judgement, not an official figure)
Every question must be tagged and each code must belong to the question's subject, otherwise nothing is written.
Then set "tagged": true for the paper in tools/jee_mock/pyq_papers.json and run make_index.py.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}


def main(path, tagfile):
    from app.services.reinforce import JEE_TAXONOMY
    paper = json.load(open(path, encoding='utf-8'))
    tags = json.load(open(tagfile, encoding='utf-8'))['tags']
    codes = {s: {c for c, _n, _p in chs} for s, chs in JEE_TAXONOMY.items()}
    names = {c: n for chs in JEE_TAXONOMY.values() for c, n, _p in chs}
    problems = []
    for q in paper['qs']:
        t = tags.get(str(q['n']))
        if not t:
            problems.append('Q%s: no tag' % q['n'])
            continue
        subject = SUBJ.get(q.get('subj'))
        if t.get('cat') not in codes.get(subject, ()):
            problems.append('Q%s: code %r is not a %s chapter' % (q['n'], t.get('cat'), subject))
        if t.get('diff') not in (1, 2, 3):
            problems.append('Q%s: diff %r' % (q['n'], t.get('diff')))
    if problems:
        raise SystemExit('Not written:\n  ' + '\n  '.join(problems[:20]))
    for q in paper['qs']:
        t = tags[str(q['n'])]
        q['cat'] = t['cat']
        q['chapter'] = (t.get('chapter') or names[t['cat']]).strip()[:80]
        q['lvl'] = t['diff']
    paper['tagged'] = True
    json.dump(paper, open(path, 'w', encoding='utf-8'), separators=(',', ':'))
    print('tags applied to %d questions in %s' % (len(paper['qs']), path))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
