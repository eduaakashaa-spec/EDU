"""Add an extracted previous-year paper (extract_pyq.py output) to the mock centre: official key, chapter tags, section rules, paper list entry.

    python tools/jee_mock/add_pyq.py <extracted.json> <paper id, e.g. P250402S1> <key.csv> <tags.json> "JEE Main 2025 · 2 Apr · Shift 1" "2025 · 2 Apr · Shift 1"

Copies the extracted paper into app/data/jee_mock/data/, applies the key (apply_key.py: a DROP row in the NTA key becomes full marks to all), applies the tags (apply_tags.py), marks the
numerical sections of 90-question papers (10 numerical per subject, attempt any 5) with `choose`, and adds/updates the entry in pyq_papers.json. Run make_index.py afterwards.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')


def main(src, pid, keycsv, tagfile, title, short):
    import apply_key
    import apply_tags
    dest = os.path.join(DATA, pid + '.json')
    shutil.copyfile(src, dest)
    paper = json.load(open(dest, encoding='utf-8'))
    total = len(paper['qs'])
    assert total in (75, 90), total
    for s in paper['sections']:
        if s['type'] == 'NAT' and s['hi'] - s['lo'] + 1 == 10:
            s['choose'] = 5
    json.dump(paper, open(dest, 'w', encoding='utf-8'), separators=(',', ':'))
    apply_key.main(dest, keycsv)
    apply_tags.main(dest, tagfile)
    meta_path = os.path.join(HERE, 'pyq_papers.json')
    metas = [m for m in json.load(open(meta_path, encoding='utf-8')) if m['y'] != pid]
    meta = {'y': pid, 'title': title, 'short': short, 'tagged': True}
    if total == 90:
        meta.update(total=90, n=75, numnote='20 + any 5 of 10')
    metas.append(meta)
    json.dump(metas, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('added', pid, total, 'questions')


if __name__ == '__main__':
    main(*sys.argv[1:7])
