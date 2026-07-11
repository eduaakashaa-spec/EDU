"""Load JOSAA cutoff, NIRF ranking, DASA cutoff, and college directory data into memory at startup."""
import csv
import json
import os
import re
import pandas as pd

_josaa_df = None
_nirf_df = None
_dasa_df = None
_institutes = None
_programs = None
_quotas = None
_seat_types = None
_genders = None
_college_datasets = {}

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')


def _read_csv_dicts(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _read_json(filename):
    with open(os.path.join(DATA_DIR, filename), encoding='utf-8') as f:
        return json.load(f)


def _num(value, as_int=False):
    """'' -> None; otherwise int/float."""
    if value is None or value == '':
        return None
    f = float(value)
    return int(f) if as_int or f.is_integer() else f


def _num_or_str(value):
    """Numeric when possible, otherwise the raw string (e.g. NIRF band '101-150')."""
    try:
        return _num(value)
    except ValueError:
        return value


def _load_college_datasets():
    """Load the college directory CSVs (extracted from what used to be
    hard-coded JS arrays) and rebuild the exact structures the front-end
    scripts expect. Served to pages via /api/data/<name>.js."""
    global _college_datasets

    # Engineering colleges across India (enggcolleges_india page)
    engg = [{
        'n': r['name'], 's': r['state'], 'd': r['district'], 't': r['type'],
        'r': _num(r['nirf_rank'], as_int=True),
        'nb': r['nirf_band'] or None,
        'cp': [int(x) for x in r['cutoff_profile'].split('|')] if r['cutoff_profile'] else [],
        'b': r['branches'].split('|') if r['branches'] else [],
    } for r in _read_csv_dicts('engg_colleges_india.csv')]

    # TNEA notable colleges by district (tnea_colleges map page)
    tn_top = [{
        'n': r['name'], 'd': r['district'], 't': r['type'],
        'co': _num(r['cutoff']),
        'b': r['branches'].split('|') if r['branches'] else [],
    } for r in _read_csv_dicts('tnea_top_colleges.csv')]

    # TNEA expert guidance: 35-college benchmark table
    benchmark = [{
        'rank': _num_or_str(r['rank']), 'name': r['name'], 'short': r['short'],
        'city': r['city'], 'est': _num_or_str(r['est']), 'naac': r['naac'],
        'type': r['type'], 'typeLabel': r['typeLabel'], 'cutoff': r['cutoff'],
        'highest': r['highest'], 'median': r['median'], 'admission': r['admission'],
        'admitClass': r['admitClass'], 'typeFamily': r['typeFamily'],
    } for r in _read_csv_dicts('tnea_benchmark_colleges.csv')]

    # TNEA expert guidance: full college list + branches + cutoff records
    colleges = [{'n': r['name'], 'd': r['district'], 't': r['type']}
                for r in _read_csv_dicts('tnea_all_colleges.csv')]
    branches = [{'c': r['code'], 'n': r['name']}
                for r in _read_csv_dicts('tnea_branches.csv')]
    college_idx = {c['n']: i for i, c in enumerate(colleges)}
    branch_idx = {b['c']: i for i, b in enumerate(branches)}
    records = [[college_idx[r['college']], branch_idx[r['branch_code']],
                _num(r['oc']), _num(r['bc']), _num(r['bcm']), _num(r['mbc']),
                _num(r['sc']), _num(r['sca']), _num(r['st'])]
               for r in _read_csv_dicts('tnea_cutoff_records.csv')]
    tnea_data = {'colleges': colleges, 'branches': branches, 'records': records}

    # DASA institute-wise seat matrix
    seat_matrix = [{
        'inst_code': r['inst_code'], 'institute': r['institute'], 'program': r['program'],
        'ciwg': _num(r['ciwg'], as_int=True), 'nonciwg': _num(r['nonciwg'], as_int=True),
        'dasa_total': _num(r['dasa_total'], as_int=True), 'branch_cat': r['branch_cat'],
        'group': r['group'], 'nirf_rank': _num(r['nirf_rank'], as_int=True),
        'nirf_score': _num(r['nirf_score']), 'city': r['city'], 'state': r['state'],
    } for r in _read_csv_dicts('dasa_seat_matrix.csv')]

    # Datasets moved out of hard-coded page JS into files (served as globals).
    # TNEA cutoffs == the TNEA 2025 master; NIRF keeps the full 300-set; CBP
    # carries the real DASA CIWG ranks (incl. Manipal) from the CIWG xlsx.
    ciwg = _read_json('ciwg_choice_builder.json')

    _college_datasets = {
        'engg-colleges-india': {'EA_ENGG_COLLEGES': engg},
        'tnea-colleges': {'EA_TN_COLLEGES': tn_top},
        'tnea-expert-guidance': {'EA_TNEA_BENCHMARK': benchmark, 'EA_TNEA_DATA': tnea_data},
        'dasa-seat-matrix': {'EA_DASA_SEAT_MATRIX': seat_matrix},
        'tnea-cutoffs-full': {'EA_TNEA_FULL': _read_json('tnea_cutoffs_full.json')},
        'tnea2026-cutoffs': {'EA_TNEA2026': _read_json('tnea2026_cutoffs.json')},
        'nirf-full': {'EA_NIRF300': _read_json('nirf_full.json')},
        'ciwg-choice-builder': {'EA_CIWG': ciwg},
    }


def get_college_dataset(name):
    """Return {js_global_name: payload} for /api/data/<name>.js, or None."""
    return _college_datasets.get(name)


# Curated branch / course list for the survey + mentor-form dropdowns. Rendered
# as a <datalist>, so a value typed outside this list is still accepted.
BRANCH_OPTIONS = [
    'Computer Science & Engineering', 'Information Technology',
    'Artificial Intelligence & Data Science', 'AI & Machine Learning',
    'Computer Science & Business Systems', 'Cyber Security',
    'Electronics & Communication Engineering', 'Electrical & Electronics Engineering',
    'Electrical Engineering', 'Electronics & Instrumentation',
    'Instrumentation & Control Engineering', 'Mechanical Engineering', 'Mechatronics',
    'Robotics & Automation', 'Civil Engineering', 'Chemical Engineering',
    'Aeronautical Engineering', 'Aerospace Engineering', 'Automobile Engineering',
    'Biotechnology', 'Biomedical Engineering', 'Industrial / Production Engineering',
    'Metallurgical Engineering', 'Marine Engineering', 'Mining Engineering',
    'Agricultural Engineering', 'Food Technology', 'Textile Technology',
    'Architecture', 'Planning', 'Pharmacy',
    'Business Administration (MBA / BBA)', 'Computer Applications (MCA / BCA)',
    'Basic Sciences (B.Sc / M.Sc)', 'Commerce', 'Arts / Humanities', 'Other',
]


def get_branch_names():
    """Curated branch/course list for the survey + mentor-form dropdowns."""
    return BRANCH_OPTIONS


def get_college_names():
    """Sorted, de-duplicated India college/institute names for the dropdowns,
    drawn from the datasets already loaded at startup. Foreign / unlisted
    colleges are still fine — the field is a datalist, not a closed select."""
    names = set()
    engg = (_college_datasets or {}).get('engg-colleges-india', {}).get('EA_ENGG_COLLEGES', [])
    names.update(c['n'].strip() for c in engg if c.get('n'))
    tnea = ((_college_datasets or {}).get('tnea-expert-guidance', {})
            .get('EA_TNEA_DATA', {}).get('colleges', []))
    names.update(c['n'].strip() for c in tnea if c.get('n'))
    names.update(i.strip() for i in (_institutes or []) if i)
    return sorted(names, key=str.lower)


def _get_type(name):
    if re.search(r'Indian Institute of Technology', name, re.I) and not re.search(r'Information', name, re.I):
        return 'IIT'
    if re.search(r'National Institute of Technology', name, re.I):
        return 'NIT'
    if re.search(r'Indian Institute of Information Technology', name, re.I) or re.search(r'\bIIIT\b', name, re.I):
        return 'IIIT'
    return 'GFTI'


def load_data():
    """Read Excel/CSV files and cache as module-level DataFrames."""
    global _josaa_df, _nirf_df, _institutes, _programs, _quotas, _seat_types, _genders

    # --- JOSAA cutoffs ---
    josaa_path = os.path.join(DATA_DIR, 'josaa_cutoffs.xlsx')
    df = pd.read_excel(josaa_path)
    df.rename(columns={
        'Academic Program Name': 'Program',
        'Seat Type': 'SeatType',
        'Minimum Opening Rank': 'OpenRank',
        'Maximum Closing Rank': 'CloseRank',
    }, inplace=True)
    # Strip preparatory 'P' suffix from PwD ranks
    df['OpenRank'] = df['OpenRank'].astype(str).str.rstrip('P').astype(int)
    df['CloseRank'] = df['CloseRank'].astype(str).str.rstrip('P').astype(int)
    df['InstType'] = df['Institute'].apply(_get_type)
    df['CleanProgram'] = df['Program'].str.replace(r'\s*\(\d+ Years.*$', '', regex=True).str.strip()

    _josaa_df = df
    _institutes = sorted(df['Institute'].unique().tolist())
    _programs = sorted(df['Program'].unique().tolist())
    _quotas = sorted(df['Quota'].unique().tolist())
    _seat_types = sorted(df['SeatType'].unique().tolist())
    _genders = sorted(df['Gender'].unique().tolist())

    # --- NIRF rankings ---
    nirf_path = os.path.join(DATA_DIR, 'nirf_rankings.csv')
    ndf = pd.read_csv(nirf_path, usecols=['Institute', 'NIRF Rank'])
    ndf.rename(columns={'Institute': 'Name', 'NIRF Rank': 'Rank'}, inplace=True)
    ndf['Rank'] = ndf['Rank'].astype(str).str.split('-').str[0].astype(int)
    _nirf_df = ndf

    # --- DASA cutoffs ---
    global _dasa_df
    dasa_path = os.path.join(DATA_DIR, 'dasa_cutoffs.json')
    if os.path.exists(dasa_path):
        with open(dasa_path, encoding='utf-8') as f:
            dasa_records = json.load(f)
        _dasa_df = pd.DataFrame(dasa_records)
        # Coerce rank columns to nullable int
        for col in ['r1_open', 'r1_close', 'r2_open', 'r2_close', 'r3_open', 'r3_close',
                    'overall_open', 'overall_close']:
            _dasa_df[col] = pd.to_numeric(_dasa_df[col], errors='coerce')
        _dasa_df['nirf_rank'] = pd.to_numeric(_dasa_df['nirf_rank'], errors='coerce')

    # --- College directory CSVs (extracted from formerly hard-coded JS) ---
    _load_college_datasets()


def get_josaa_df():
    return _josaa_df


def get_nirf_df():
    return _nirf_df


def get_metadata():
    return {
        'institutes': _institutes,
        'programs': _programs,
        'quotas': _quotas,
        'seat_types': _seat_types,
        'genders': _genders,
    }


def get_nirf_lookup():
    """Return dict mapping institute name -> {Name, Rank}."""
    if _nirf_df is None:
        return {}
    return {row['Name']: {'Name': row['Name'], 'Rank': int(row['Rank'])}
            for _, row in _nirf_df.iterrows()}


def get_dasa_df():
    return _dasa_df
