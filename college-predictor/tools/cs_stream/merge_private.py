"""Merge researched private-university branch lists into app/data/cs_stream_private.json for the member page /computer-science-stream.

Usage (from college-predictor/):  python tools/cs_stream/merge_private.py <research.json> [<research2.json> ...]
Each research file is {"universities": [{nirf_name, campus, verified, programmes, entrance, source_urls, checked_on, caveat}]} written from the universities' own pages.
Rules: only verified entries with at least one computer-stream programme are kept; nirf_name must be an exact name in app/data/eng_colleges.json (so a rank or band can be shown);
programmes that are not computer-stream are dropped; an entry already in the file is never overwritten.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from app.services.cs_family import family  # noqa: E402

OUT = os.path.join(ROOT, 'app', 'data', 'cs_stream_private.json')
NIRF = os.path.join(ROOT, 'app', 'data', 'eng_colleges.json')

# friendlier display names for NIRF spellings
DISPLAY = {
    'Jain university,Bangalore': 'Jain University',
    'Bansilal Ramnath Agarwal Charitable Trust`s Vishwakarama Institute of Technology': 'Vishwakarma Institute of Technology',
    'SVKM`s Narsee Monjee Institute of Management Studies': 'NMIMS (SVKM’s Narsee Monjee Institute of Management Studies)',
    'Shri Vile Parle Kelavani Mandal`s Dwarkadas J. Sanghvi College of Engineering': 'Dwarkadas J. Sanghvi College of Engineering',
    'Siksha `O` Anusandhan': 'Siksha ‘O’ Anusandhan (SOA)',
    'Kalinga Institute of Industrial Technology': 'KIIT (Kalinga Institute of Industrial Technology)',
    'Hindustan Institute of Technology and Science (HITS)': 'Hindustan Institute of Technology and Science (HITS)',
    'Dr. Vishwanath Karad MIT World Peace University': 'MIT World Peace University (MIT-WPU)',
    'Saveetha Institute of Medical and Technical Sciences': 'Saveetha Institute of Medical and Technical Sciences (SIMATS)',
    'Symbiosis International': 'Symbiosis International (Symbiosis Institute of Technology)',
    'M. S. Ramaiah Institute of Technology': 'M. S. Ramaiah Institute of Technology',
    'The Northcap University': 'The NorthCap University',
}
LEAD = re.compile(r'^\s*(B\.?\s?Tech\.?|B\.?\s?E\.?|Bachelor of (?:Technology|Engineering))\s*(?:in|[-:])?\s*(\(Hons\.?\))?\s*', re.I)


def clean(p):
    p = re.sub(r'\s+', ' ', str(p)).strip()
    return LEAD.sub('', p).strip(' -:') or p


def main(files):
    names = {c['name'] for c in json.load(open(NIRF, encoding='utf-8'))['colleges']}
    doc = json.load(open(OUT, encoding='utf-8'))
    have = {u['nirf_name'] for u in doc['universities']}
    added, skipped = [], []
    for f in files:
        for u in json.load(open(f, encoding='utf-8'))['universities']:
            nn = u.get('nirf_name')
            progs = [clean(p) for p in (u.get('programmes') or [])]
            progs = [p for p in dict.fromkeys(progs) if family(p)]
            if not u.get('verified') or not progs:
                skipped.append((nn, 'not verified or no computer programmes'))
                continue
            if nn not in names:
                skipped.append((nn, 'name not in the NIRF list'))
                continue
            if nn in have:
                skipped.append((nn, 'already in the file'))
                continue
            have.add(nn)
            doc['universities'].append({'name': DISPLAY.get(nn, nn), 'nirf_name': nn, 'campus': u.get('campus'), 'verified': True, 'programmes': progs, 'entrance': u.get('entrance'),
                                        'source_urls': (u.get('source_urls') or [])[:2], 'source_kind': u.get('source_kind') or 'own site', 'caveat': u.get('caveat')})
            added.append(nn)
    doc['checked_on'] = max([doc.get('checked_on') or ''] + [u.get('checked_on') or '' for f in files for u in json.load(open(f, encoding='utf-8'))['universities']])
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('added', len(added), '| total', len(doc['universities']))
    for a in added:
        print('  +', a)
    for n, why in skipped:
        print('  skipped:', n, '-', why)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
