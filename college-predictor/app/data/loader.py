"""Load JOSAA cutoff and NIRF ranking data from Excel/CSV into memory at startup."""
import os
import re
import pandas as pd

_josaa_df = None
_nirf_df = None
_institutes = None
_programs = None
_quotas = None
_seat_types = None
_genders = None

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')


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
