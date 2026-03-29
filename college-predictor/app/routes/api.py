"""API Blueprint — server-side JOSAA/NIRF endpoints."""
import re
from flask import Blueprint, jsonify, request
from app.data.loader import get_josaa_df, get_nirf_df, get_metadata, get_nirf_lookup

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Branch category keyword mapping for grouped filtering
BRANCH_CAT_KEYWORDS = {
    'cs': ['Computer Science', 'Information Technology', 'Artificial Intelligence', 'Data Science', 'Software', 'Computing'],
    'ec': ['Electronics', 'Communication', 'Electrical', 'Instrumentation', 'Telecommunication', 'VLSI'],
    'me': ['Mechanical', 'Production', 'Manufacturing', 'Aerospace', 'Automobile', 'Industrial'],
    'ce': ['Civil', 'Environmental', 'Structural', 'Construction', 'Transportation'],
    'ch': ['Chemical', 'Materials', 'Metallurgy', 'Biotechnology', 'Biochemical', 'Polymer'],
    'mc': ['Mathematics', 'Physics', 'Statistics', 'Engineering Science'],
}


def _branch_cat_mask(df, branch_cat):
    """Return a boolean mask filtering CleanProgram by category keywords."""
    keywords = BRANCH_CAT_KEYWORDS.get(branch_cat, [])
    if not keywords:
        return df['CleanProgram'].notna()  # match all
    pattern = '|'.join(re.escape(k) for k in keywords)
    return df['CleanProgram'].str.contains(pattern, case=False, na=False)


def _get_type(name):
    if re.search(r'Indian Institute of Technology', name, re.I) and not re.search(r'Information', name, re.I):
        return 'IIT'
    if re.search(r'National Institute of Technology', name, re.I):
        return 'NIT'
    if re.search(r'Indian Institute of Information Technology', name, re.I) or re.search(r'\bIIIT\b', name, re.I):
        return 'IIIT'
    return 'GFTI'


# ---------- metadata (dropdown options) ----------
@api_bp.route('/josaa/meta')
def josaa_meta():
    return jsonify(get_metadata())


# ---------- predictor ----------
@api_bp.route('/josaa/predict')
def josaa_predict():
    rank = request.args.get('rank', type=int)
    if not rank or rank < 1:
        return jsonify({'error': 'Invalid rank'}), 400

    cat = request.args.get('cat', 'OPEN')
    gender = request.args.get('gender', 'Gender-Neutral')
    quota = request.args.get('quota', '')
    inst_type = request.args.get('instType', '')
    branch = request.args.get('branch', '')
    branch_cat = request.args.get('branchCat', '')
    use_buffer = request.args.get('buffer') == '1'

    df = get_josaa_df()
    nirf_lookup = get_nirf_lookup()

    mask = (df['SeatType'] == cat) & (df['Gender'] == gender)
    if quota:
        mask &= df['Quota'] == quota
    if inst_type:
        mask &= df['InstType'] == inst_type
    if branch:
        mask &= df['CleanProgram'] == branch
    elif branch_cat:
        mask &= _branch_cat_mask(df, branch_cat)
    multiplier = 3 if use_buffer else 1.5
    mask &= df['CloseRank'] * multiplier >= rank

    filtered = df[mask]
    results = []
    for _, r in filtered.iterrows():
        inst = r['Institute']
        open_r, close_r = int(r['OpenRank']), int(r['CloseRank'])
        if rank <= close_r:
            span = close_r - open_r
            pos = rank - open_r
            if span <= 0 or pos <= span * 0.33:
                chance = 'safe'
            elif pos <= span * 0.7:
                chance = 'moderate'
            else:
                chance = 'reach'
        else:
            ratio = rank / close_r if close_r > 0 else 999
            if ratio <= 1.5:
                chance = 'reach'
            else:
                chance = 'longshot'
        nirf = nirf_lookup.get(inst)
        nirf_rank = nirf['Rank'] if nirf and nirf['Rank'] < 9999 else 9999
        results.append({
            'inst': inst,
            'prog': r['Program'],
            'q': r['Quota'],
            'st': r['SeatType'],
            'g': r['Gender'],
            'open': open_r,
            'close': close_r,
            'chance': chance,
            'nirfRank': nirf_rank,
            'instType': _get_type(inst),
        })
    return jsonify(results)


# ---------- matrix ----------
@api_bp.route('/josaa/matrix')
def josaa_matrix():
    cat = request.args.get('cat', 'OPEN')
    quota = request.args.get('quota', '')
    inst_type = request.args.get('type', '')
    branch = request.args.get('branch', '')
    branch_cat = request.args.get('branchCat', '')
    search = request.args.get('search', '').lower()

    df = get_josaa_df()
    nirf_lookup = get_nirf_lookup()

    mask = (df['SeatType'] == cat) & (df['Gender'] == 'Gender-Neutral')
    if quota:
        mask &= df['Quota'] == quota
    if inst_type:
        mask &= df['InstType'] == inst_type
    if branch:
        mask &= df['CleanProgram'] == branch
    elif branch_cat:
        mask &= _branch_cat_mask(df, branch_cat)
    if search:
        mask &= df['Institute'].str.lower().str.contains(search, regex=False) | \
                df['Program'].str.lower().str.contains(search, regex=False)

    filtered = df[mask]

    inst_data = {}
    for _, r in filtered.iterrows():
        inst = r['Institute']
        prog = r['Program']
        close = int(r['CloseRank'])
        open_r = int(r['OpenRank'])
        if inst not in inst_data:
            inst_data[inst] = {}
        if prog not in inst_data[inst] or close < inst_data[inst][prog]['c']:
            inst_data[inst][prog] = {'o': open_r, 'c': close}

    # Sort by NIRF, limit 50
    sorted_insts = sorted(inst_data.keys(),
                          key=lambda i: nirf_lookup.get(i, {}).get('Rank', 9999))[:50]

    KEY_BRANCHES = [
        'Computer Science and Engineering (4 Years, Bachelor of Technology)',
        'Electronics and Communication Engineering (4 Years, Bachelor of Technology)',
        'Electrical Engineering (4 Years, Bachelor of Technology)',
        'Mechanical Engineering (4 Years, Bachelor of Technology)',
        'Civil Engineering (4 Years, Bachelor of Technology)',
        'Chemical Engineering (4 Years, Bachelor of Technology)',
        'Mathematics and Computing (4 Years, Bachelor of Technology)',
        'Information Technology (4 Years, Bachelor of Technology)',
        'Artificial Intelligence (4 Years, Bachelor of Technology)',
        'Data Science and Artificial Intelligence (4 Years, Bachelor of Technology)',
    ]

    all_branches = set()
    for inst in sorted_insts:
        all_branches.update(inst_data[inst].keys())

    branches = [b for b in (KEY_BRANCHES if not branch else [branch]) if b in all_branches]
    if not branches:
        branches = sorted(all_branches)[:8]

    rows = []
    for inst in sorted_insts:
        nirf = nirf_lookup.get(inst)
        rows.append({
            'inst': inst,
            'instType': _get_type(inst),
            'nirfRank': nirf['Rank'] if nirf and nirf['Rank'] < 9999 else None,
            'branches': {b: inst_data[inst].get(b) for b in branches},
        })

    return jsonify({'branches': branches, 'rows': rows})


# ---------- NIRF ----------
@api_bp.route('/josaa/nirf')
def josaa_nirf():
    q = request.args.get('q', '').lower()
    max_r = request.args.get('maxRank', 9999, type=int)

    ndf = get_nirf_df()
    results = []
    for _, n in ndf.iterrows():
        if int(n['Rank']) > max_r:
            continue
        if q and q not in n['Name'].lower():
            continue
        results.append({'Name': n['Name'], 'Rank': int(n['Rank'])})
    return jsonify(results)


# ---------- insights ----------
@api_bp.route('/josaa/insights')
def josaa_insights():
    df = get_josaa_df()

    # IIT branch analysis
    iit_mask = df['InstType'].eq('IIT') & df['SeatType'].eq('OPEN') & df['Gender'].eq('Gender-Neutral')
    iit = df[iit_mask].groupby('Program')['CloseRank'].agg(['mean', 'count'])
    iit_list = [(p.split('(')[0].strip(), int(round(row['mean'])))
                for p, row in iit.iterrows() if row['count'] >= 2]
    iit_list.sort(key=lambda x: x[1])
    iit_list = iit_list[:8]

    # NIT branch analysis (NITs use OS quota, not AI)
    nit_mask = df['InstType'].eq('NIT') & df['SeatType'].eq('OPEN') & \
               df['Gender'].eq('Gender-Neutral') & df['Quota'].eq('OS')
    nit = df[nit_mask].groupby('Program')['CloseRank'].agg(['mean', 'count'])
    nit_list = [(p.split('(')[0].strip(), int(round(row['mean'])))
                for p, row in nit.iterrows() if row['count'] >= 2]
    nit_list.sort(key=lambda x: x[1])
    nit_list = nit_list[:8]

    return jsonify({'iitBranches': iit_list, 'nitBranches': nit_list})


# ---------- analytics (pre-computed chart data) ----------
@api_bp.route('/josaa/analytics')
def josaa_analytics():
    df = get_josaa_df()
    nirf_lookup = get_nirf_lookup()
    institutes = sorted(df['Institute'].unique().tolist())
    programs = sorted(df['Program'].unique().tolist())

    # 1. Institute type counts
    type_cnt = {'IIT': 0, 'NIT': 0, 'IIIT': 0, 'GFTI': 0}
    for inst in institutes:
        type_cnt[_get_type(inst)] += 1

    # 2. Seat type distribution
    seat_cnt = df['SeatType'].value_counts().to_dict()

    # 3. Top branches
    prog_cnt = df['Program'].value_counts().head(10)
    top_branches = [[p.split('(')[0].strip()[:22], int(c)] for p, c in prog_cnt.items()]

    # 4. Avg closing by type (OPEN, Gender-Neutral; AI for IIT/IIIT, OS for NIT)
    open_gn = df[(df['SeatType'] == 'OPEN') & (df['Gender'] == 'Gender-Neutral')]
    open_gn_ai = open_gn[open_gn['Quota'].isin(['AI', 'OS'])]
    type_avg = {}
    for t in ['IIT', 'NIT', 'IIIT', 'GFTI']:
        vals = open_gn_ai[open_gn_ai['InstType'] == t]['CloseRank']
        type_avg[t] = int(round(vals.mean())) if len(vals) > 0 else 0

    # 5. Cutoff scatter data (6 branches)
    scatter_branches = [
        'Computer Science and Engineering (4 Years, Bachelor of Technology)',
        'Electronics and Communication Engineering (4 Years, Bachelor of Technology)',
        'Mechanical Engineering (4 Years, Bachelor of Technology)',
        'Civil Engineering (4 Years, Bachelor of Technology)',
        'Chemical Engineering (4 Years, Bachelor of Technology)',
        'Mathematics and Computing (4 Years, Bachelor of Technology)',
    ]
    scatter_data = {}
    for bi, b in enumerate(scatter_branches):
        points = []
        branch_df = open_gn[open_gn['Program'] == b]
        for _, r in branch_df.iterrows():
            inst = r['Institute']
            nirf = nirf_lookup.get(inst)
            x = nirf['Rank'] if nirf and nirf['Rank'] < 9999 else None
            y = int(r['CloseRank'])
            if y < 200000 and x is not None:
                points.append({'x': x, 'y': y, 'label': inst})
        scatter_data[b.split('(')[0].strip()[:20]] = points[:30]

    # 6. Top 25 institutes (min opening rank, OPEN, GN)
    inst_best = open_gn.groupby('Institute')['OpenRank'].min()
    top25 = inst_best.nsmallest(25)
    top25_data = [{'inst': i.replace('Indian Institute of Technology', 'IIT')
                   .replace('National Institute of Technology', 'NIT')[:32],
                   'val': int(v), 'type': _get_type(i)} for i, v in top25.items()]

    # 7. Hidden gem NIT comparison (CSE vs Mech vs ECE) — NITs use OS quota
    nit_open_gn_os = open_gn[open_gn['InstType'].eq('NIT') & open_gn['Quota'].eq('OS')]
    nit_cse = {}
    nit_mech = {}
    nit_ece = {}
    for _, r in nit_open_gn_os.iterrows():
        inst = r['Institute']
        prog = r['Program']
        nirf = nirf_lookup.get(inst)
        if not nirf or nirf['Rank'] >= 9999:
            continue
        if re.search(r'Computer Science and Engineering.*4 Years.*Bachelor of Technology', prog):
            nit_cse[inst] = int(r['CloseRank'])
        if re.search(r'Mechanical Engineering.*4 Years.*Bachelor of Technology', prog):
            nit_mech[inst] = int(r['CloseRank'])
        if re.search(r'Electronics and Communication Engineering.*4 Years.*Bachelor of Technology', prog):
            nit_ece[inst] = int(r['CloseRank'])
    gem_insts = [i for i in nit_cse if i in nit_mech][:12]
    gem_data = [{'inst': i.replace('National Institute of Technology', 'NIT')[:22],
                 'cse': nit_cse.get(i, 0), 'mech': nit_mech.get(i, 0), 'ece': nit_ece.get(i, 0)}
                for i in gem_insts]

    # 8. Category advantage CSE
    cats = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST']
    cse_mask = df['Program'].str.contains(r'Computer Science and Engineering.*4 Years.*Bachelor of Technology', regex=True) & \
               df['Gender'].eq('Gender-Neutral') & df['Quota'].isin(['AI', 'OS'])
    cat_vals = []
    for c in cats:
        vals = df[cse_mask & (df['SeatType'] == c)]['CloseRank']
        cat_vals.append(int(round(vals.mean())) if len(vals) > 0 else 0)

    return jsonify({
        'typeCnt': type_cnt,
        'seatCnt': seat_cnt,
        'topBranches': top_branches,
        'typeAvg': type_avg,
        'scatterData': scatter_data,
        'top25': top25_data,
        'gemData': gem_data,
        'catAdvantage': {'cats': cats, 'vals': cat_vals},
    })


# ================================================================
# DASA PREDICTOR API
# ================================================================

# ------ DB logging for marketing leads ------
def _log_dasa_lead(name, email, rank, quota, branch, institute):
    """Log user details for marketing into the database."""
    from app.extensions import db
    from app.models import DasaLead
    lead = DasaLead(
        name=name, email=email, rank=int(rank),
        quota=quota, branch=branch, institute=institute,
        source='dasa_predictor',
    )
    db.session.add(lead)
    db.session.commit()
    return lead


# ------ RBAC: Premium user check ------
def _is_premium_user():
    """Check if current session belongs to a premium/admin user."""
    from flask_login import current_user
    if current_user.is_authenticated:
        return current_user.is_premium
    return False


@api_bp.route('/dasa/predict', methods=['POST'])
def dasa_predict():
    """DASA college predictor endpoint.

    Accepts user details, logs lead, returns predictions.
    Full results are gated behind premium access (RBAC).
    """
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    rank = data.get('rank')
    quota = (data.get('quota') or 'non-ciwg').strip().lower()
    branch = (data.get('branch') or '').strip()
    institute = (data.get('institute') or '').strip()

    if not rank or not isinstance(rank, (int, float)) or int(rank) < 1:
        return jsonify({'error': 'Invalid DASA rank'}), 400

    rank = int(rank)

    # Log lead for marketing (always, regardless of premium status)
    if name and email:
        _log_dasa_lead(name, email, rank, quota, branch, institute)

    # TODO: Load actual DASA cutoff data from Excel/CSV once available.
    # For now, use a placeholder dataset structure matching DASA format.
    # Expected columns: Institute, Programme, Quota (CIWG/Non-CIWG),
    #                   OpenRank, CloseRank, Round
    #
    # When data file is ready:
    # 1. Add dasa_cutoffs.xlsx to app/data/files/
    # 2. Add load function in loader.py (similar to JOSAA loader)
    # 3. Replace placeholder below with real filtering logic

    # --- Placeholder sample results ---
    sample_results = [
        {'inst': 'NIT Tiruchirappalli', 'prog': 'Computer Science and Engineering', 'quota': 'Non-CIWG', 'open': 1, 'close': 85, 'chance': 'safe', 'nirfRank': 9},
        {'inst': 'NIT Warangal', 'prog': 'Computer Science and Engineering', 'quota': 'Non-CIWG', 'open': 5, 'close': 120, 'chance': 'safe', 'nirfRank': 21},
        {'inst': 'NIT Karnataka Surathkal', 'prog': 'Computer Science and Engineering', 'quota': 'Non-CIWG', 'open': 3, 'close': 105, 'chance': 'moderate', 'nirfRank': 17},
        {'inst': 'NIT Calicut', 'prog': 'Electronics and Communication Engineering', 'quota': 'Non-CIWG', 'open': 10, 'close': 200, 'chance': 'moderate', 'nirfRank': 25},
        {'inst': 'NIT Rourkela', 'prog': 'Mechanical Engineering', 'quota': 'Non-CIWG', 'open': 8, 'close': 180, 'chance': 'reach', 'nirfRank': 19},
        {'inst': 'IIIT Hyderabad', 'prog': 'Computer Science and Engineering', 'quota': 'Non-CIWG', 'open': 2, 'close': 60, 'chance': 'safe', 'nirfRank': 50},
        {'inst': 'NIT Durgapur', 'prog': 'Information Technology', 'quota': 'Non-CIWG', 'open': 15, 'close': 250, 'chance': 'reach', 'nirfRank': 64},
        {'inst': 'NIT Jaipur', 'prog': 'Computer Science and Engineering', 'quota': 'Non-CIWG', 'open': 12, 'close': 220, 'chance': 'moderate', 'nirfRank': 55},
    ]

    # Filter by quota
    q_label = 'CIWG' if quota == 'ciwg' else 'Non-CIWG'
    results = [r for r in sample_results if r['quota'] == q_label or True]  # placeholder: show all

    # Filter by branch category
    if branch:
        branch_kw = BRANCH_CAT_KEYWORDS.get(branch, [])
        if branch_kw:
            results = [r for r in results
                       if any(kw.lower() in r['prog'].lower() for kw in branch_kw)]

    # Chance classification (placeholder logic)
    for r in results:
        if rank <= r['close']:
            r['chance'] = 'safe' if rank <= r['close'] * 0.7 else 'moderate'
        elif rank <= r['close'] * 1.3:
            r['chance'] = 'reach'
        else:
            r['chance'] = 'longshot'

    # RBAC: Premium users get full results; free users get preview
    is_premium = _is_premium_user()
    total = len(results)

    if is_premium:
        return jsonify({
            'premium': True,
            'total': total,
            'results': results,
        })
    else:
        # Free users: Show first 3 results only + blur/lock the rest
        preview = results[:3]
        return jsonify({
            'premium': False,
            'total': total,
            'results': preview,
            'message': f'Showing 3 of {total} results. Upgrade to Premium for full access.',
        })
