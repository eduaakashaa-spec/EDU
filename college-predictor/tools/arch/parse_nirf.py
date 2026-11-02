"""Parse the NIRF 2025 Architecture 'Data Submitted by Institution' sheets (PDF) into app/data/arch_nirf.json.
Usage: python tools/arch/parse_nirf.py <folder with IR-A-*.pdf> [out json]
Every number is read from the sheet; nothing is estimated. Programme labels: UG5 (5-year UG), UG4 (4-year UG), PG2 and so on.
Placement years are the graduating year (2021-22, 2022-23, 2023-24). The median salary is the figure the institution reported, in rupees a year."""
import glob
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
import fitz  # noqa: E402


def text(path):
    d = fitz.open(path)
    t = ' '.join(p.get_text() for p in d)
    return re.sub(r'\s+', ' ', t)


def label(kind, yrs):
    return '%s%s' % (kind, yrs)


def parse(path):
    t = text(path)
    m = re.search(r'Institute Name: (.+?) \[(IR-A-[A-Z]-\d+)\]', t)
    out = dict(id=m.group(2), name=m.group(1).strip())
    # intake
    a, b = t.index('Sanctioned (Approved) Intake'), t.index('Total Actual Student Strength')
    blk = t[a:b]
    out['intake'] = {}
    for mm in re.finditer(r'(UG|PG)(?:-Integrated)? \[(\d+) Years? Program\(s\)\]((?: (?:\d+|-)){6})', blk):
        out['intake'][label(mm.group(1), mm.group(2))] = [None if x == '-' else int(x) for x in mm.group(3).split()]
    out['intake_years'] = ['2023-24', '2022-23', '2021-22', '2020-21', '2019-20', '2018-19']
    # strength
    a, b = t.index('Total Actual Student Strength'), t.index('Placement & Higher Studies')
    blk = t[a:b]
    keys = ['male', 'female', 'total', 'within_state', 'outside_state', 'outside_country', 'economically_backward', 'socially_challenged', 'reimb_govt', 'reimb_inst', 'reimb_private', 'no_reimb']
    out['strength'] = {}
    for mm in re.finditer(r'(UG|PG)(?:-Integrated)? \[(\d+) Years? Program\(s\)\]((?: \d+){12})', blk):
        out['strength'][label(mm.group(1), mm.group(2))] = dict(zip(keys, [int(x) for x in mm.group(3).split()]))
    # placement
    out['placement'] = {}
    for mm in re.finditer(r'(UG|PG)(?:-Integrated)? \[(\d+) Years? Program\(s\)\]: Placement & higher studies for previous 3 years(.*?)(?=(?:UG|PG)(?:-Integrated)? \[\d+ Years? Program\(s\)\]: Placement|Financial Resources:)', t):
        lab = label(mm.group(1), mm.group(2))
        body = mm.group(3)
        rows = []
        # UG: intake year, intake, admitted, lateral year, lateral, graduating year, graduating, placed, median, higher
        for r in re.finditer(r'(\d{4}-\d{2}) (\d+) (\d+) (\d{4}-\d{2}) (\d+) (\d{4}-\d{2}) (\d+) (\d+) (\d+)(?: ?\([^)]*\))? ?(\d+)', body):
            g = r.groups()
            rows.append(dict(entry=g[0], intake=int(g[1]), admitted=int(g[2]), graduating_year=g[5], graduating=int(g[6]), placed=int(g[7]), median=int(g[8]), higher_studies=int(g[9])))
        if not rows:
            for r in re.finditer(r'(\d{4}-\d{2}) (\d+) (\d+) (\d{4}-\d{2}) (\d+) (\d+) (\d+)(?: ?\([^)]*\))? ?(\d+)', body):
                g = r.groups()
                rows.append(dict(entry=g[0], intake=int(g[1]), admitted=int(g[2]), graduating_year=g[3], graduating=int(g[4]), placed=int(g[5]), median=int(g[6]), higher_studies=int(g[7])))
        out['placement'][lab] = rows
    # money (2023-24 is the first of each triple)
    def first_amount(name, scope):
        mm = re.search(name + r' (\d+) \(', scope)
        return int(mm.group(1)) if mm else None
    a = t.index('Utilised Amount for the Capital expenditure')
    b = t.index('Utilised Amount for the Operational expenditure')
    cap, op = t[a:b], t[b:t.index('Sponsored Research Details')]
    out['capex'] = dict(library=first_amount('Library', cap), laboratories=first_amount('New Equipment for Laboratories', cap), studios=first_amount('Studios', cap),
                        other=first_amount(r'Other expenditure on creation of Capital Assets \(excluding expenditure on Land and Building\)', cap))
    out['opex'] = dict(salaries=first_amount(r'Salaries \(Teaching and Non Teaching staff\)', op),
                       maintenance=first_amount(r'etc\)', op), seminars=first_amount('Seminars/Conferences/Workshops', op))
    sp = t[t.index('Sponsored Research Details'):t.index('Consultancy Project Details')]
    co = t[t.index('Consultancy Project Details'):t.index('PCS Facilities')]

    def triple(label_, scope):
        mm = re.search(re.escape(label_) + r' (\d+) (\d+) (\d+)', scope)
        return [int(x) for x in mm.groups()] if mm else None
    out['sponsored'] = dict(projects=triple('Total no. of Sponsored Projects', sp), amount=triple('Total Amount Received (Amount in Rupees)', sp))
    out['consultancy'] = dict(projects=triple('Total no. of Consultancy Projects', co), amount=triple('Total Amount Received (Amount in Rupees)', co))
    pc = t[t.index('PCS Facilities'):]
    ans = re.findall(r'\d\. Do your institution (?:buildings have Lifts/Ramps\?|have provision for walking aids, including wheelchairs and transportation from one building to another for handicapped students\?|buildings have specially designed toilets for handicapped students\?) (.*?)(?= \d\. Do your|Faculty Details)', pc)
    out['pcs'] = [x.strip() for x in ans]
    mm = re.search(r'Number of faculty members entered (\d+)', t)
    out['faculty'] = int(mm.group(1)) if mm else None
    return out


def main(folder, dest):
    res = {}
    for f in sorted(glob.glob(os.path.join(folder, 'IR-A-*.pdf'))):
        r = parse(f)
        res[r['id']] = r
    json.dump(res, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(res), 'sheets')
    bad = [(k, v['name']) for k, v in res.items() if not v['strength'] or not v['intake'] or v['faculty'] is None or not any(v['placement'].values()) or len(v['pcs']) != 3 or v['sponsored']['projects'] is None]
    print('incomplete:', bad)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'data', 'arch_nirf.json'))
