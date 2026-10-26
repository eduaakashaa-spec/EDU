"""Write app/data/jee_mock/data/index.json (the paper list the page reads).

Mocks M1-M5 are always ready. Previous-year NTA papers are listed from tools/jee_mock/pyq_papers.json and become `ready` only when their
data file exists with an official answer key applied (every question has `acc`)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
papers = [{'y': 'M%d' % i, 'kind': 'mock', 'title': 'EduAakashaa JEE Main Mock %d' % i, 'short': 'Mock %d' % i, 'n': 75, 'mins': 180, 'max': 300, 'ready': True} for i in range(1, 6)]
pyq_file = os.path.join(HERE, 'pyq_papers.json')
if os.path.exists(pyq_file):
    for p in json.load(open(pyq_file, encoding='utf-8')):
        f = os.path.join(DATA, p['y'] + '.json')
        ready = False
        if os.path.exists(f):
            d = json.load(open(f, encoding='utf-8'))
            ready = all(q.get('acc') for q in d['qs'])
        papers.append(dict({'n': 75, 'mins': 180, 'max': 300}, **p, kind='pyq', ready=ready))
json.dump({'papers': papers}, open(os.path.join(DATA, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(papers), 'papers;', sum(1 for p in papers if p['ready']), 'ready')
