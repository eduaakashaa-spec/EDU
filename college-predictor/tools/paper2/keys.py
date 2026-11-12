"""Read NTA Paper 2 final answer keys ('QUESTION ID / CORRECT OPTION ID' pairs, as PDF text) and attach them to extracted papers.

    python tools/paper2/keys.py <scratch dir with out/<id>/meta.json> <id>=<key.pdf>[,<key2.pdf>] ...

The key PDF is read as one stream of tokens; for every question id of the paper the token that follows it is its answer: an option id (MCQ: becomes the index 0-3 of the option as the
picture labels it A-D), a number (numerical question), or 'Dropped' (full marks to everyone). Prints what could not be matched and writes <scratch>/out/<id>/key.json {n: answer}.
Answers: MCQ -> 0..3, NAT -> a number, dropped -> 'bonus'. With two key PDFs the second must agree with the first wherever both carry the question.
"""
import json
import os
import re
import sys

import fitz

DROP = {'dropped', 'drop', 'bonus'}


def stream(pdf):
    toks = []
    for p in fitz.open(pdf):
        for line in p.get_text().split('\n'):
            for tk in line.replace('|', ' ').split():
                toks.append(tk)
    return toks


def answers(toks, qids):
    """Walk the stream; a token that is a still-unassigned question id of this paper starts a pair (id, answer): the answer token is then skipped, so an option id that equals another
    question's id (the ids of some papers overlap) is never read as a question. 'a,' followed by more tokens means several accepted options: kept as 'multi'."""
    out, i = {}, 0
    while i < len(toks) - 1:
        tk = toks[i]
        if tk in qids and tk not in out:
            a = toks[i + 1]
            i += 2
            if a.endswith(','):
                while i < len(toks) and toks[i - 1].endswith(',') and re.fullmatch(r'[\d.]+,?', toks[i]):
                    i += 1
                a = 'multi'
            out[tk] = a
        else:
            i += 1
    return out


def clean(a):
    if a is None:
        return None
    a = re.sub(r'\(\d\)$', '', a).strip()
    return a


def main(scratch, pid, pdfs):
    meta = json.load(open(os.path.join(scratch, 'out', pid, 'meta.json')))
    qids = {q['qid'] for q in meta['qs'] if q['t'] != 'DRAW'}
    merged, notes = {}, []
    for pdf in pdfs:
        ans = answers(stream(pdf), qids)
        for q, a in ans.items():
            a = clean(a)
            if q in merged and merged[q] != a:
                notes.append('key files disagree on %s: %s vs %s' % (q, merged[q], a))
            merged.setdefault(q, a)
    key, missing = {}, []
    for q in meta['qs']:
        if q['t'] == 'DRAW':
            continue
        a = merged.get(q['qid'])
        if a is None:
            missing.append(q['n'])
        elif a == 'multi':
            missing.append(q['n'])
            notes.append('Q%d accepts several options: left out' % q['n'])
        elif a.lower() in DROP:
            key[q['n']] = 'bonus'
        elif q['t'] == 'MCQ':
            if a in q['oids']:
                key[q['n']] = q['oids'].index(a)
            else:
                missing.append(q['n'])
                notes.append('Q%d answer %s is not among its option ids' % (q['n'], a))
        else:
            try:
                key[q['n']] = float(a)
            except ValueError:
                missing.append(q['n'])
                notes.append('Q%d numerical answer %r unreadable' % (q['n'], a))
    json.dump({str(k): v for k, v in key.items()}, open(os.path.join(scratch, 'out', pid, 'key.json'), 'w'))
    bonus = sorted(k for k, v in key.items() if v == 'bonus')
    print(pid, '| keyed', len(key), 'of', sum(1 for q in meta['qs'] if q['t'] != 'DRAW'), '| missing', missing, '| dropped', bonus, '|', notes[:4])
    return key


if __name__ == '__main__':
    for a in sys.argv[2:]:
        pid, files = a.split('=')
        main(sys.argv[1], pid, files.split(','))
