"""Build a JEE mock-centre paper from an EduAakashaa "Solved Paper Guide" PDF (questions retyped from an NTA paper, with a one-page answer key and a worked solution for every question).

    python tools/jee_mock/build_guide.py "<guide.pdf>" J2401S1 "JEE Main 2024 (1 Feb, Shift 1)" [OUT_DIR]

Each question becomes one WebP image of the question body (stem and the four options, numbered 1-4 as printed in the guide) and each worked solution one WebP image
(steps, common mistake, tips). The answer key is read from the guide's key page. Section B (numerical) is 'attempt any 5 of 10' per subject, so those sections carry choose=5.
The paper JSON is written to app/data/jee_mock/data/<ID>.json; run make_index.py afterwards so the paper is listed.
"""
import base64
import io
import json
import os
import re
import sys

import pdfplumber
import pypdfium2 as pdfium

SCALE = 2.4
Q_W = 900
S_W = 820
CARD_X0, CARD_X1 = 43, 551

# the guide's own chapter grouping -> the mock centre's chapter codes
CHAP = {
    'Conic sections': 'COG', 'Complex numbers': 'CNQ', 'Definite integrals': 'INT', 'Differential equations': 'DEQ', 'Matrices and determinants': 'MAT', 'Permutations and combinations': 'PNC',
    'Sequences and series': 'SEQ', 'Three-dimensional geometry': 'VEC', 'Application of derivatives': 'LCD', 'Area under curves': 'INT', 'Binomial theorem': 'PNC', 'Circles': 'COG',
    'Continuity and differentiability': 'LCD', 'Exponential equations': 'CNQ', 'Functions': 'SRF', 'Limits': 'LCD', 'Probability': 'STP', 'Sets and relations': 'SRF', 'Statistics': 'STP',
    'Trigonometry': 'TRG', 'Vector algebra': 'VEC',
    'Current electricity': 'CUR', 'Moving charges and magnetism': 'MAG', 'Moving charges and': 'MAG', 'Alternating current': 'MAG', 'Capacitance': 'ELS', 'Electromagnetic induction': 'MAG', 'Electromagnetic waves': 'OPT',
    'Electrostatics': 'ELS', 'Kinetic theory': 'THM', 'Thermodynamics': 'THM', 'Centre of mass': 'ROT', 'Circular motion': 'LOM', 'Fluids': 'PMB', 'Gravitation': 'GRA', 'Kinematics': 'KIN',
    'Laws of motion': 'LOM', 'Motion in a plane': 'KIN', 'Properties of solids': 'PMB', 'Work, energy and momentum': 'WEP', 'Atoms': 'DUA', 'Dual nature of matter': 'DUA', 'Nuclei': 'DUA',
    'Semiconductors': 'DUA', 'Errors in measurement': 'UNM', 'Experimental physics': 'UNM', 'Units and dimensions': 'UNM', 'Ray optics': 'OPT', 'Wave optics': 'OPT', 'Waves': 'OSW',
    'Chemical bonding': 'BON', 'Coordination compounds': 'COO', 'Periodic table': 'PER', 'Salt analysis': 'PER', 'p-block elements': 'PER', 'Aromatic compounds': 'HYD', 'Aldehydes and ketones': 'ORG',
    'Amines': 'ORG', 'Biomolecules': 'BIO', 'Haloalkanes': 'HAL', 'Organic basics': 'ORG', 'Organic nomenclature': 'ORG', 'Organic reagents': 'ORG', 'Practical chemistry': 'ORG',
    'Practical organic chemistry': 'ORG', 'Stereochemistry': 'ORG', 'Redox reactions': 'RDX', 'Chemical kinetics': 'CKN', 'Electrochemistry': 'RDX', 'Ionic equilibrium': 'EQU', 'Mole concept': 'MOL',
    'Solutions': 'SOL', 'Structure of atom': 'ATS',
}
SUBJ_OF = lambda n: 'MATH' if n <= 30 else 'PHY' if n <= 60 else 'CHEM'


def parse_text(pdf):
    """Answer key and chapter map from the text pages."""
    txt = {}
    for i, p in enumerate(pdf.pages):
        txt[i + 1] = p.extract_text() or ''
    key = {}
    for m in re.finditer(r'Q(\d{1,2})\s+\((\d)\)', txt[31]):
        key[int(m.group(1))] = ('MCQ', int(m.group(2)))
    for m in re.finditer(r'Q(\d{1,2})\s+(\d+(?:\.\d+)?)\b(?!\))', txt[31]):
        n = int(m.group(1))
        if n not in key:
            key[n] = ('NAT', float(m.group(2)))
    for m in re.finditer(r'Q(\d{1,2})\s+none', txt[31]):
        key[int(m.group(1))] = ('BONUS', None)
    chap = {}
    pat = re.compile(r'^(?:(.*?)\s+)?((?:Q\d{1,2}(?:,\s*)?)+)\s+\d+$')
    for pg in (90, 91, 92):
        buf = ''
        for l in [x.strip() for x in txt[pg].splitlines()]:
            m = pat.match(l)
            if m:
                name = (m.group(1) or buf).strip()
                parts = re.split(r'\s[^\w\s,()\-]\s*', name)           # "Group <separator> Chapter" -> Chapter
                name = parts[-1].strip()
                name = 'Moving charges and magnetism' if name == 'Moving charges and' else name
                for n in re.findall(r'Q(\d{1,2})', m.group(2)):
                    chap[int(n)] = name
                buf = ''
            elif l.startswith(('CHAPTER', 'The grouping', 'P A G E', 'PAGE', 'W H A T', 'WHAT', 'Each ', 'revise', 'Mathematics:', 'Physics:', 'Chemistry:', 'after marking')):
                buf = ''
            elif l:
                buf = (buf + ' ' + l).strip()
    return key, chap


def webp(img, width):
    from PIL import Image
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    b = io.BytesIO()
    img.convert('RGB').save(b, 'WEBP', quality=82, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), img.width, img.height


def headers(page):
    h = [r for r in page.rects if 500 < r['width'] < 515 and 28 < r['height'] < 45]
    return sorted(h, key=lambda r: r['top'])


def card_bottom(page, top, limit):
    """Lowest drawn element of the card between `top` and `limit` (next card header or the page footer)."""
    ys = [w['bottom'] for w in page.extract_words() if top < w['top'] < limit]
    ys += [c['bottom'] for c in page.curves if top < c['top'] < limit and c['width'] < 520]
    ys += [r['bottom'] for r in page.rects if top < r['top'] < limit and 500 < r['width'] < 515]
    return max(ys) if ys else limit


def main(pdf_path, paper_id, title, out_dir):
    pdf = pdfplumber.open(pdf_path)
    doc = pdfium.PdfDocument(pdf_path)
    key, chap = parse_text(pdf)
    assert len(key) == 90, 'answer key incomplete: %d' % len(key)
    qimg, simg, qid = {}, {}, {}
    for pn in range(3, 30):                                       # question pages 4-30
        page = pdf.pages[pn]
        hs = headers(page)
        words = page.extract_words()
        render = doc[pn].render(scale=SCALE).to_pil()
        for i, h in enumerate(hs):
            lab = [w for w in words if abs(w['top'] - h['top']) < 14 and re.fullmatch(r'Q\d{1,2}', w['text']) and w['x0'] < 70]
            if not lab:
                continue
            n = int(lab[0]['text'][1:])
            top = h['bottom']
            limit = hs[i + 1]['top'] - 2 if i + 1 < len(hs) else 790
            bottom = card_bottom(page, top, limit) + 5
            crop = render.crop((int((CARD_X0 - 2) * SCALE), int((top + 2) * SCALE), int((CARD_X1 + 2) * SCALE), int(bottom * SCALE)))
            qimg[n] = webp(crop, Q_W)
    for pn in range(31, 89):                                      # solution pages 32-89
        page = pdf.pages[pn]
        hs = headers(page)
        words = page.extract_words()
        render = doc[pn].render(scale=SCALE).to_pil()
        for i, h in enumerate(hs):
            lab = [w for w in words if abs(w['top'] - h['top']) < 16 and re.fullmatch(r'Q\d{1,2}', w['text']) and w['x0'] < 70]
            if not lab:
                continue
            n = int(lab[0]['text'][1:])
            idw = [w for w in words if abs(w['top'] - h['top']) < 26 and w['text'].isdigit() and len(w['text']) >= 7]
            if idw:
                qid[n] = idw[0]['text']
            sol = [w for w in words if w['text'] == 'SOLUTION' and h['top'] < w['top'] < (hs[i + 1]['top'] if i + 1 < len(hs) else 800)]
            if not sol:
                continue
            limit = hs[i + 1]['top'] - 2 if i + 1 < len(hs) else 790
            bottom = card_bottom(page, sol[0]['top'], limit) + 4
            crop = render.crop((int((CARD_X0 - 2) * SCALE), int((sol[0]['top'] - 6) * SCALE), int((CARD_X1 + 2) * SCALE), int(bottom * SCALE)))
            simg[n] = webp(crop, S_W)
    missing = [n for n in range(1, 91) if n not in qimg or n not in simg]
    assert not missing, 'missing crops for %s' % missing
    qs = []
    for n in range(1, 91):
        kind, val = key[n]
        t = 'NAT' if (kind == 'NAT' or (kind == 'BONUS' and n > 0 and ((n - 1) % 30) >= 20)) else 'MCQ'
        subj = SUBJ_OF(n)
        name = chap.get(n)
        cat = CHAP.get(name) if name else None
        q = {'n': n, 't': t, 'subj': subj, 'cat': cat, 'chapter': name, 'qid': qid.get(n), 'img': qimg[n][0], 'w': qimg[n][1], 'h': qimg[n][2], 'sol': simg[n][0], 'sw': simg[n][1], 'sh': simg[n][2]}
        if kind == 'MCQ':
            q['acc'] = {'sets': ['ABCD'[val - 1]]}
            q['disp'] = str(val)
        elif kind == 'NAT':
            tol = 0.005 if val != int(val) else 0
            q['acc'] = {'ranges': [[val - tol, val + tol]]}
            q['disp'] = ('%g' % val)
        else:
            q['acc'] = {'bonus': True}
            q['disp'] = 'Full marks to all'
        qs.append(q)
    sections = []
    for subj, a in (('MATH', 1), ('PHY', 31), ('CHEM', 61)):
        sections.append({'type': 'MCQ', 'subj': subj, 'lo': a, 'hi': a + 19, 'right': 4, 'wrong': -1, 'partial': False})
        sections.append({'type': 'NAT', 'subj': subj, 'lo': a + 20, 'hi': a + 29, 'right': 4, 'wrong': -1, 'partial': False, 'choose': 5})
    paper = {'year': paper_id, 'title': title, 'mins': 180, 'max': 300, 'lab': '1234', 'key': 'solved', 'sections': sections, 'qs': qs,
             'notes': ['Answers were solved independently by EduAakashaa and Physics answers cross-checked with a published coaching key; the NTA final answer key for this shift has not been matched yet.',
                       'Q48: none of the printed options is correct, so full marks are given to everyone (as coaching keys do). Q38 assumes work done by the gas. Q85: the answer 0.9 is not a whole number.']}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, paper_id + '.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(paper, f, ensure_ascii=False, separators=(',', ':'))
    print('wrote', path, '%.1f MB' % (os.path.getsize(path) / 1e6), '| chapters mapped:', sum(1 for q in qs if q['cat']), '/ 90 | ids:', len(qid))
    unmapped = sorted({q['chapter'] for q in qs if not q['cat']})
    if unmapped:
        print('UNMAPPED chapter names:', unmapped)


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else os.path.join(root, 'app', 'data', 'jee_mock', 'data'))
