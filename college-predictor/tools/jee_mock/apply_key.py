"""Apply an official answer key to a previous-year paper JSON made by extract_pyq.py.

    python tools/jee_mock/apply_key.py app/data/jee_mock/data/P0402S1.json key.csv

key.csv has a header row and these columns (extra columns are ignored):
    n  or  qid        question number (1-75) or the NTA question id
    answer            MCQ: A-D, or the correct option id printed by NTA; NAT: the number.
                      Two accepted answers: separate with | (e.g. A|C or 4|5). Use BONUS for a question dropped with full marks to all.
After applying, run tools/jee_mock/make_index.py so the paper switches to 'ready'. The script refuses to finish if any question is left without a key.
"""
import csv
import json
import sys


def main(path, keyfile):
    paper = json.load(open(path, encoding='utf-8'))
    rows = list(csv.DictReader(open(keyfile, encoding='utf-8-sig')))
    by_n = {q['n']: q for q in paper['qs']}
    by_qid = {str(q.get('qid')): q for q in paper['qs']}
    done = set()
    for row in rows:
        row = {(k or '').strip().lower(): (v or '').strip() for k, v in row.items()}
        q = by_n.get(int(row['n'])) if row.get('n') else by_qid.get(row.get('qid', ''))
        ans = row.get('answer') or row.get('correct') or row.get('key') or ''
        if q is None or not ans:
            print('skipped row', row)
            continue
        if ans.upper() in ('BONUS', 'DROPPED', 'DROP'):
            q['acc'] = {'bonus': True}
            q['disp'] = 'Full marks to all'
            done.add(q['n'])
            continue
        parts = [p.strip() for p in ans.replace(',', '|').split('|') if p.strip()]
        if q['t'] == 'MCQ':
            letters = []
            for p in parts:
                if p.upper() in ('A', 'B', 'C', 'D'):
                    letters.append(p.upper())
                elif p in q['oids']:
                    letters.append('ABCD'[q['oids'].index(p)])
                else:
                    raise SystemExit('Q%d: cannot read answer %r' % (q['n'], p))
            q['acc'] = {'sets': sorted(set(letters))}
            q['disp'] = ' or '.join(sorted(set(letters)))
        else:
            vals = [float(p) for p in parts]
            q['acc'] = {'ranges': [[v, v] for v in vals]}
            q['disp'] = ' or '.join(('%g' % v) for v in vals)
        done.add(q['n'])
    missing = [q['n'] for q in paper['qs'] if q['n'] not in done]
    if missing:
        raise SystemExit('No key for questions: %s (nothing written)' % missing)
    paper['key'] = 'applied'
    json.dump(paper, open(path, 'w', encoding='utf-8'), separators=(',', ':'))
    print('key applied to %d questions in %s' % (len(done), path))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
