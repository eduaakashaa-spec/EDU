"""Build app/data/nid/bank.json (the question bank of the NID mock centre) and app/data/nid/tasks.json (studio tasks).
Inputs: app/data/nid/visual.json (procedural visual and spatial questions, answers computed by code), the four authored text sets bank_K1..K4.json and tasks.json
(all original EduAakashaA questions; each text answer was checked by an independent blind solve, see the build notes), from a scratch folder.
Usage: python tools/nid/build_bank.py <scratch folder>"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'app', 'data', 'nid')
BAD = re.compile(r'collegedekho|careers360|collegedunia|shiksha|getmyuni|toprankers|creative ?edge|whatsapp', re.I)
SEC = {'VIS': 'Visual reasoning', 'SPA': 'Spatial reasoning', 'LOG': 'Logical reasoning', 'CLR': 'Colour theory', 'PRI': 'Design principles', 'AWR': 'Design awareness', 'HIS': 'Design history',
       'CRF': 'Indian crafts and culture', 'MAT': 'Materials and printing', 'ERG': 'Ergonomics', 'SUS': 'Sustainability', 'SCI': 'Science and objects', 'GKN': 'General knowledge',
       'LAN': 'Language', 'CRT': 'Critical thinking'}


def main(scratch):
    bank, seen = [], set()
    vis = json.load(open(os.path.join(DATA, 'visual.json'), encoding='utf-8'))
    for q in vis:
        q['src'] = 'visual'
        bank.append(q)
    for k in ('K1', 'K2', 'K3', 'K4'):
        for i, q in enumerate(json.load(open(os.path.join(scratch, 'bank_%s.json' % k), encoding='utf-8'))):
            assert len(q['opts']) == 4 and len(set(q['opts'])) == 4 and 0 <= q['ans'] <= 3 and q['sec'] in SEC, (k, i)
            d = dict(sec=q['sec'], topic=q['topic'], level=q['level'], marks=q['marks'], q=q['q'], opts=[dict(t=o) for o in q['opts']], ans=q['ans'], why=q['why'], src='text')
            if q.get('passage'):
                d['passage'] = q['passage']
                d['group'] = q.get('group')
            d['id'] = 'N-%s-%03d' % (q['sec'], i)
            bank.append(d)
    out = []
    for q in bank:
        assert q['sec'] in SEC and 0 <= q['ans'] < len(q['opts']) and q['level'] in ('B', 'M', 'BM') and q['marks'] in (1, 2), q['id']
        txt = json.dumps(q, ensure_ascii=False)
        assert not BAD.search(txt), q['id']
        key = (q['q'], json.dumps(q['opts'], ensure_ascii=False), q.get('svg', ''))
        assert key not in seen, q['id']
        seen.add(key)
        if q.get('id') is None:
            q['id'] = 'N-%s-%03d' % (q['sec'], len(out))
        out.append(q)
    ids = [q['id'] for q in out]
    assert len(ids) == len(set(ids))
    json.dump(out, open(os.path.join(DATA, 'bank.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tasks = json.load(open(os.path.join(scratch, 'tasks.json'), encoding='utf-8'))
    for t in tasks:
        assert sum(r['marks'] for r in t['rubric']) == t['marks'], t['id']
        assert not BAD.search(json.dumps(t, ensure_ascii=False)), t['id']
    json.dump(tasks, open(os.path.join(DATA, 'tasks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(out), 'questions', dict(Counter(q['sec'] for q in out)))
    print('levels', dict(Counter(q['level'] for q in out)), 'marks', dict(Counter(q['marks'] for q in out)), len(tasks), 'tasks')


if __name__ == '__main__':
    main(sys.argv[1])
