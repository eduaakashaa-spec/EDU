"""Content for the public page /class12-pcb: Class 12 PCB (Physics, Chemistry, Biology) Analytics.

* chapters_pcb.json: the 14 Physics and 10 Chemistry chapters of the PCM hub plus 13 Biology chapters, each with indicative marks (only the unit-group marks are official), the Core / Build / Later class for
  the four levels and a rule, hook and trap. Facts in the Biology cards were checked by an independent reviewer; students are told to check each rule against NCERT.
* playbook_pcb.json: the level plans (what to do first at each level) and six illustrative answer sheets, written by EduAakashaA in CBSE style: not CBSE papers and not real students' scripts.
* facts_pcb.json: official facts read on CHECKED from the NTA, NMC, CBSE and other official pages, with the source URL for each, the routes (entrance rules) and what could not be confirmed.
"""
import json
import os
import sys

from app.services import pcm12

CHECKED = '5 November 2026'
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pcm12')


def _read(name, default):
    try:
        with open(os.path.join(DIR, name), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def context():
    chapters = pcm12.chapters('pcb')
    pb = _read('playbook_pcb.json', {'levels': [], 'sheets': []})
    facts = _read('facts_pcb.json', {'facts': [], 'routes': [], 'biology_units': [], 'notes': []})
    states = ['Maharashtra', 'Delhi', 'Kerala', 'Andhra Pradesh']
    groups = [('National rules and CBSE', [f for f in facts['facts'] if ': ' not in f['topic'] or f['topic'].split(': ')[0] not in states], True)]
    for st in states:
        mine = [dict(f, topic=f['topic'].split(': ', 1)[1]) for f in facts['facts'] if f['topic'].startswith(st + ': ')]
        if mine:
            groups.append((st, mine, False))
    sources = []
    for f in facts['facts']:
        if f['source'] and f['source'] not in sources:
            sources.append(f['source'])
    for r in facts['routes']:
        if r.get('source') and r['source'] not in sources:
            sources.append(r['source'])
    data = {'chapters': [{k: c[k] for k in ('id', 'subj', 'name', 'unit', 'marks', 'levels', 'why', 'rules', 'hook', 'trap')} for c in chapters], 'levels': pb['levels'], 'sheets': pb['sheets'],
            'cats': pcm12.cfg('pcb')['cats'], 'marks': pcm12.cfg('pcb')['marks'], 'labels': pcm12.cfg('pcb')['labels'], 'marks_order': list(pcm12.cfg('pcb')['marks'])}
    return {'d': sys.modules[__name__], 'data': data, 'facts': facts, 'groups': groups, 'sources': sources, 'n_chapters': len(chapters), 'n_routes': len(facts['routes']), 'checked': CHECKED}
