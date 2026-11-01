"""Build the IAT question bank from the rendered pages and the written solutions.

Reads  <scratch>/r/<year>.json and the images in <scratch>/r/<year>/, and <scratch>/sol_<year>.json (worked solutions).
Writes app/data/iat/q<year>.json and copies the images to app/static/img/iat/<year>/.
Usage: python tools/iat/build_bank.py <scratch_dir> [year ...]
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SJ = {'Biology': 'BIO', 'Chemistry': 'CHE', 'Mathematics': 'MAT', 'Physics': 'PHY'}


def main(scratch, years):
    out_data = os.path.join(ROOT, 'app', 'data', 'iat')
    os.makedirs(out_data, exist_ok=True)
    for y in years:
        render = json.load(open(os.path.join(scratch, 'r', '%s.json' % y), encoding='utf-8'))
        try:
            sol = json.load(open(os.path.join(scratch, 'sol_%s.json' % y), encoding='utf-8'))
        except OSError:
            sol = []
        sol = {(s['subject'], (int(s['n']) - 1) % 15 + 1): s for s in sol}
        dst = os.path.join(ROOT, 'app', 'static', 'img', 'iat', str(y))
        os.makedirs(dst, exist_ok=True)
        rows = []
        for q in render:
            s = sol.get((q['subj'], q['n']), {})
            agree = s.get('agree', True) is not False
            files = (q['stem'] + q['opts']) if q['ok'] else q['full']
            for f in files:
                shutil.copy(os.path.join(scratch, 'r', str(y), f), os.path.join(dst, f))
            rows.append(dict(year=int(y), sj=SJ[q['subj']], n=q['n'], ok=bool(q['ok']), stem=q['stem'], opts=q['opts'], full=q['full'], topic=s.get('topic', ''), diff=s.get('diff', ''),
                             why=s.get('why', ''), agree=agree, note=s.get('note', '')))
        json.dump(rows, open(os.path.join(out_data, 'q%s.json' % y), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(y, len(rows), 'questions;', sum(1 for r in rows if r['ok'] and r['agree']), 'usable;', sum(1 for r in rows if r['why']), 'with solutions;', sum(1 for r in rows if not r['agree']), 'disagreements')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:] or ['2021', '2022', '2023', '2024', '2025', '2026'])
