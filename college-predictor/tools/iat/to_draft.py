"""Turn the parse_key.py output into a draft with stem, four options and image roles.
Usage: python tools/iat/to_draft.py <parsed.json> <draft.json>
Options are written as {t: text or '', img: file or ''}. In the official 2025 and 2026 key documents the first option (a) is the correct answer.
"""
import json
import re
import sys


def clean(t):
    t = t.replace('→', '-')  # a mis-encoded minus in some PDFs shows as an arrow
    t = re.sub(r'\s*\n\s*', ' ', t).strip()
    return re.sub(r'\s{2,}', ' ', t)


def main(src, dst):
    qs = json.load(open(src, encoding='utf-8'))
    out = []
    for q in qs:
        txt = q['text']
        txt = re.sub(r'^\s*\d+\.\s*Question\s+\d+\s*\n', '', txt)
        txt = re.sub(r'\n\d+\s*$', '', txt.strip())          # trailing page number
        txt = re.sub(r'\n?=====PAGE=====\n?', '\n', txt)
        # split at option markers at line starts
        parts = re.split(r'(?m)^\(([a-d])\)\s*', txt)
        stem = clean(parts[0])
        opts = {}
        for k in range(1, len(parts) - 1, 2):
            opts[parts[k]] = clean(parts[k + 1])
        # a later page may only hold '(c)' '(d)' markers
        imgs = [i['file'] for i in q['images']]
        o = [{'t': opts.get(c, ''), 'img': ''} for c in 'abcd']
        empty = [k for k in range(4) if not o[k]['t']]
        stem_imgs = []
        if imgs:
            if len(empty) == 4 and len(imgs) >= 4:
                stem_imgs = imgs[:len(imgs) - 4]
                for k, f in enumerate(imgs[len(imgs) - 4:]):
                    o[k]['img'] = f
            elif len(empty) == 2 and len(imgs) >= 2 and False:
                pass
            else:
                stem_imgs = imgs
        out.append(dict(subj=q['subj'], n=q['n'], stem=stem, opts=o, stem_imgs=stem_imgs, empty=len(empty), nimgs=len(imgs)))
    json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), 'drafts')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
