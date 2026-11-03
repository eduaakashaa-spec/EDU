"""Aggregate the paper-by-paper analysis (agents' notes on structure, marks and topics of the NID papers in the supplied folder) into app/data/nid/analysis.json.
Only structure, marks and topic tags are used: no question text. One source is chosen per year and programme so nothing is counted twice:
official sample > scanned paper as printed > candidate-recalled (memory-based) paper.
Usage: python tools/nid/build_analysis.py <folder holding ana_A.json .. ana_D.json>"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'app', 'data', 'nid', 'analysis.json')
OBJ = ('MCQ', 'MSQ', 'NAT')
SUBJ = ('subjective', 'sketch', 'studio-3D', 'other')
SHORT = {'Visual reasoning (odd one out, patterns, series)': 'Visual reasoning', 'Spatial (cubes, nets, folding, rotation, mirror image)': 'Spatial reasoning',
         'Logical reasoning (coding, direction, syllogism, series)': 'Logical reasoning', 'Design awareness (logos, brands, symbols, signage)': 'Design awareness',
         'Indian crafts, textiles and culture': 'Indian crafts and culture', 'Materials, manufacturing and printing': 'Materials and printing', 'Sustainability and environment': 'Sustainability',
         'Design principles and elements': 'Design principles', 'Design history and designers': 'Design history', 'Ergonomics and human factors': 'Ergonomics',
         'General knowledge and current affairs': 'General knowledge', 'Science and everyday objects': 'Science and objects', 'Language and comprehension': 'Language',
         'Numerical and data': 'Numerical', 'Product and user problem-solving': 'Product and user problems', 'Storytelling and illustration': 'Storytelling', 'Sketching and drawing': 'Sketching',
         '3D and model making': '3D and model making'}


def short(t):
    return SHORT.get(t, t)


def main(src):
    ana = []
    for k in 'ABCD':
        for p in json.load(open(os.path.join(src, 'ana_%s.json' % k), encoding='utf-8')):
            p['grp'] = k
            ana.append(p)

    def find(grp, sub, year=None, prog=None):
        for p in ana:
            if p['grp'] == grp and sub in str(p.get('file')) and (year is None or p.get('year') == year) and (prog is None or p.get('programme') == prog):
                return p
        raise KeyError((grp, sub, year, prog))

    # B.Des: the paper used for each year, with how it was sourced
    picks = [
        (2015, find('A', 'nid-2015'), 'recalled by candidates'), (2016, find('A', 'nid-2016'), 'recalled by candidates'), (2017, find('A', 'nid-2017'), 'recalled by candidates'),
        (2018, find('D', 'nid-question-paper-for-bdes-2018'), 'paper as printed (scan)'), (2019, find('A', 'nid-2019'), 'recalled by candidates'), (2020, find('A', 'nid-2020'), 'recalled by candidates'),
        (2021, find('A', 'nid-2021'), 'recalled by candidates'), (2022, find('D', 'NID-DAT-B.Des-Paper'), 'paper as printed (scan)'), (2023, find('A', 'nid-2023'), 'recalled by candidates'),
        (2024, find('C', 'BDes', 2024), 'NID official sample'), (2025, find('C', 'BDes', 2025), 'NID official sample'),
    ]
    formats = []
    for year, p, srcname in picks:
        qs = p.get('questions') or []
        obj = [q for q in qs if q.get('type') in OBJ]
        sub = [q for q in qs if q.get('type') not in OBJ]
        om = sum(q.get('marks') or 0 for q in obj)
        sm = sum(q.get('marks') or 0 for q in sub)
        formats.append(dict(year=year, source=srcname, stage=p.get('stage'), total=p.get('total_marks'), mcq=len(obj), mcq_marks=round(om, 1) or None, subj=len(sub), subj_marks=round(sm, 1) or None,
                            minutes=p.get('duration_minutes'), obs=(p.get('observations') or '')[:260]))
    # counts that come from the marks printed on the papers (not from the tags)
    fix = {2015: dict(mcq=0, mcq_marks=None, subj=15, subj_marks=100), 2021: dict(mcq=19, mcq_marks=23, subj=0, subj_marks=None, total=None),
           2024: dict(mcq=19, mcq_marks=25, subj=7, subj_marks=75), 2025: dict(mcq=20, mcq_marks=25, subj=7, subj_marks=75)}
    for f in formats:
        f.update(fix.get(f['year'], {}))
    # M.Des
    mdes = [dict(year=2025, source='NID official sample', paper='CDAT Paper 1', mcq=18, mcq_marks=20), dict(year=2024, source='NID official sample', paper='CDAT Paper 1', mcq=15, mcq_marks=20)]

    # topic mix for the objective questions, by era
    def objtopics(papers):
        c = collections.Counter()
        for p in papers:
            for q in p.get('questions') or []:
                if q.get('type') in OBJ:
                    c[short(q['topic'])] += 1
        return c
    eras = [('2016 to 2018', [p for y, p, s in picks if y in (2016, 2017, 2018)]), ('2019 to 2023', [p for y, p, s in picks if y in (2019, 2020, 2021, 2022, 2023)]),
            ('2024 and 2025 (official samples)', [p for y, p, s in picks if y in (2024, 2025)])]
    topic_eras = []
    for name, ps in eras:
        c = objtopics(ps)
        n = sum(c.values())
        topic_eras.append(dict(era=name, n=n, rows=[dict(topic=t, n=v, pct=round(100.0 * v / n, 1)) for t, v in c.most_common()]))
    mdes_p = [find('C', 'MDes', 2025), find('C', 'MDes', 2024), find('D', 'NID-DAT-M.Des')]
    c = objtopics(mdes_p)
    n = sum(c.values())
    mdes_topics = dict(n=n, rows=[dict(topic=t, n=v, pct=round(100.0 * v / n, 1)) for t, v in c.most_common()])
    # open (drawing and design) tasks across all B.Des and M.Des papers
    sc = collections.Counter()
    nt = 0
    for p in ana:
        if p.get('kind') in ('memory-based past paper', 'official sample') and 'Anant' not in str(p.get('file')):
            for q in p.get('questions') or []:
                if q.get('type') not in OBJ:
                    sc[short(q['topic'])] += 1
                    nt += 1
    tasks = dict(n=nt, rows=[dict(topic=t, n=v, pct=round(100.0 * v / nt, 1)) for t, v in sc.most_common(8)])
    distinct = len([p for p in ana if p.get('kind') in ('memory-based past paper', 'official sample') and 'Anant' not in str(p.get('file'))])
    tagged = sum(len(p.get('questions') or []) for p in ana if p.get('kind') in ('memory-based past paper', 'official sample') and 'Anant' not in str(p.get('file')))
    out = dict(formats=formats, mdes=mdes, topic_eras=topic_eras, mdes_topics=mdes_topics, tasks=tasks, papers_read=len(ana), papers_analysed=distinct, questions_tagged=tagged)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for f in formats:
        print(f['year'], f['source'], f['total'], f['mcq'], f['mcq_marks'], f['subj'], f['subj_marks'])
    for e in topic_eras:
        print(e['era'], e['n'], [(r['topic'], r['pct']) for r in e['rows'][:5]])
    print('mdes', mdes_topics['n'], [(r['topic'], r['pct']) for r in mdes_topics['rows'][:6]])
    print('tasks', tasks)
    print(out['papers_read'], distinct, tagged)


if __name__ == '__main__':
    main(sys.argv[1])
