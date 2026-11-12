"""Assemble the BITSAT mock-centre data from cropped papers: copy the question pictures into static/img/bitsat/<year>/ and write app/data/bitsat/papers.json + keys.json.

    python tools/bitsat/build_data.py <scratch dir holding keys.json and one folder per paper>  2016:c2016 2017:c2017 ...   (year:folder)

Each folder is the output of crop.py (qNNN.webp, pNNN_MMM.webp, meta.json). The section of every question is read from the printed headings (sections.py); questions whose
picture shows no options at all, whose picture is a stray line, or that have no key are listed under `skip` and never used in a test.
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import sections  # noqa: E402

PAPERS = 'C:/Users/KALIL/Documents/BITSAT_Extraction/QuestionPapers/'
PDF = {y: PAPERS + 'BITSAT_QuestionPaper_%d_aHR0cHM6Ly9jZG.pdf' % y for y in range(2015, 2025)}
IMG = os.path.join(ROOT, 'app', 'static', 'img', 'bitsat')
DATA = os.path.join(ROOT, 'app', 'data', 'bitsat')


OVERRIDE = {2015: [['PHY', 1, 40], ['CHE', 41, 80], ['ENG', 81, 95], ['LR', 96, 105], ['MAT', 106, 150]]}


def main(scratch, jobs):
    keys_all = json.load(open(os.path.join(scratch, 'keys.json'), encoding='utf-8'))
    os.makedirs(DATA, exist_ok=True)
    meta_path = os.path.join(DATA, 'papers.json')
    key_path = os.path.join(DATA, 'keys.json')
    papers = json.load(open(meta_path, encoding='utf-8')) if os.path.exists(meta_path) else {}
    keys = json.load(open(key_path, encoding='utf-8')) if os.path.exists(key_path) else {}
    for job in jobs:
        y, folder = job.split(':')
        y = int(y)
        src = os.path.join(scratch, folder)
        m = json.load(open(os.path.join(src, 'meta.json')))
        sec = sections.of_paper(PDF[y], 'num')
        n = m['n']
        rng = sections.ranges(sec)
        if y in OVERRIDE:                                  # the 2015 paper prints no English heading: English is Q81-95 (checked on the pictures)
            rng = OVERRIDE[y]
            sec = {n_: c for c, lo, hi in rng for n_ in range(lo, hi + 1)}
        key = {str(k): v for k, v in keys_all[str(y)].items() if int(k) <= n}
        skip, why = [], {}
        covered = {n_ for p_ in m['passages'] for n_ in range(p_['lo'], p_['hi'] + 1)}      # a question without printed options may take them from its instruction picture
        for q in m['q']:
            k = q['n']
            if not q['ok']:
                skip.append(k)
                why[k] = 'no picture'
            elif q['h'] < 45:
                skip.append(k)
                why[k] = 'picture too short'
            elif q['opts'] == 0 and k not in covered:
                skip.append(k)
                why[k] = 'no options in the picture'
            elif str(k) not in key:
                skip.append(k)
                why[k] = 'no key'
        dest = os.path.join(IMG, str(y))
        shutil.rmtree(dest, ignore_errors=True)
        os.makedirs(dest)
        for f in glob.glob(os.path.join(src, '*.webp')):
            shutil.copy(f, dest)
        papers[str(y)] = {'n': n, 'sections': [[c, lo, hi] for c, lo, hi in rng], 'passages': [[p['lo'], p['hi']] for p in m['passages']], 'skip': sorted(skip),
                          'note': 'memory-based paper with the published key'}
        keys[str(y)] = key
        print(y, n, 'questions; sections', rng, '; skipped', {k: why[k] for k in sorted(why)})
    json.dump(papers, open(meta_path, 'w', encoding='utf-8'), indent=0)
    json.dump(keys, open(key_path, 'w', encoding='utf-8'), separators=(',', ':'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
