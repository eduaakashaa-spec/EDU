"""Group the NIRF Engineering list (app/data/files/nirf_full.json, 300 institutions: ranks 1-100 and bands 101-150, 151-200, 201-300) into city regions and states.
Writes app/data/eng_cities.json: {colleges: [...], cities: [{key,label,state,capital,ids}], states: [{key,label,ids}]}.
A city region holds the named city plus the towns next to it (for example Chennai also takes Kattankulathur, Sriperumbudur and Thiruvallur).
Top 10 means the ten best NIRF positions in the region; where fewer than ten institutions are in the list, all of them are shown."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
BAND = {'Rank 101-150': 125, 'Rank 151 to 200': 175, 'Rank 201 to 300': 250}

# key, label, state, state capital?, cities (lower case) that belong to the region
REGIONS = [
    ('mumbai', 'Mumbai', 'Maharashtra', True, ['mumbai', 'navi mumbai', 'thane', 'kalyan', 'panvel', 'vasai', 'mumbai suburban']),
    ('pune', 'Pune', 'Maharashtra', False, ['pune', 'pimpri-chinchwad', 'pimpri chinchwad', 'lavale', 'lonavala', 'talegaon']),
    ('nagpur', 'Nagpur', 'Maharashtra', False, ['nagpur']),
    ('chennai', 'Chennai', 'Tamil Nadu', True, ['chennai', 'thiruvallur', 'kancheepuram', 'kanchipuram', 'sriperumbudur', 'kattankulathur', 'chengalpattu', 'chengalpet', 'tiruvallur', 'kalavakkam']),
    ('coimbatore', 'Coimbatore', 'Tamil Nadu', False, ['coimbatore', 'tiruppur', 'erode']),
    ('tiruchirappalli', 'Tiruchirappalli (Trichy)', 'Tamil Nadu', False, ['tiruchirappalli', 'trichy', 'thanjavur', 'samayapuram']),
    ('kozhikode', 'Kozhikode (Calicut) and Palakkad', 'Kerala', False, ['kozhikode', 'calicut', 'palakkad']),
    ('thiruvananthapuram', 'Thiruvananthapuram', 'Kerala', True, ['thiruvananthapuram', 'trivandrum']),
    ('delhi', 'Delhi NCR', 'Delhi', True, ['delhi', 'new delhi', 'south delhi', 'gautam budh nagar', 'greater noida', 'noida', 'faridabad', 'gurugram', 'gurgaon', 'sonipat', 'ghaziabad', 'sahibabad', 'gurugram, haryana']),
    ('ahmedabad', 'Ahmedabad and Gandhinagar', 'Gujarat', True, ['ahmedabad', 'gandhinagar']),
    ('bengaluru', 'Bengaluru', 'Karnataka', True, ['bengaluru', 'bangalore']),
    ('hyderabad', 'Hyderabad', 'Telangana', True, ['hyderabad', 'sangareddy', 'medchal', 'rangareddy', 'ranga reddy', 'secunderabad', 'shamshabad', 'ibrahimpatnam', 'ibrahimpatan', 'rangareddy', 'yadadri-bhuvangiri']),
    ('kolkata', 'Kolkata', 'West Bengal', True, ['kolkata', 'howrah', 'salt lake', 'north 24 parganas', 'north twenty four parganas']),
    ('lucknow', 'Lucknow', 'Uttar Pradesh', True, ['lucknow']),
    ('jaipur', 'Jaipur', 'Rajasthan', True, ['jaipur']),
    ('bhopal', 'Bhopal', 'Madhya Pradesh', True, ['bhopal']),
    ('patna', 'Patna', 'Bihar', True, ['patna']),
    ('bhubaneswar', 'Bhubaneswar', 'Odisha', True, ['bhubaneswar']),
    ('guwahati', 'Guwahati', 'Assam', True, ['guwahati']),
    ('chandigarh', 'Chandigarh and Mohali', 'Chandigarh', True, ['chandigarh', 'mohali', 'sahibzada ajit singh nagar', 'panchkula', 'kharar', 'rupnagar']),
    ('dehradun', 'Dehradun', 'Uttarakhand', True, ['dehradun']),
    ('raipur', 'Raipur', 'Chhattisgarh', True, ['raipur', 'naya raipur']),
    ('ranchi', 'Ranchi', 'Jharkhand', True, ['ranchi']),
    ('vijayawada', 'Vijayawada and Amaravati', 'Andhra Pradesh', True, ['vijayawada', 'amaravati', 'guntur', 'vaddeswaram']),
    ('visakhapatnam', 'Visakhapatnam', 'Andhra Pradesh', False, ['visakhapatnam']),
    ('puducherry', 'Puducherry', 'Puducherry', True, ['puducherry', 'pondicherry']),
    ('shimla', 'Shimla and Solan', 'Himachal Pradesh', True, ['shimla', 'solan']),
    ('itanagar', 'Itanagar', 'Arunachal Pradesh', True, ['itanagar']),
]


def pos(c):
    return c['rank'] if c['rank'] else BAND.get(c['band'], 999)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def main(out):
    data = json.load(open(os.path.join(APP, 'data', 'files', 'nirf_full.json'), encoding='utf-8'))
    for i, c in enumerate(data):
        c['key'] = slug(c['name'])[:60]
        c['pos'] = pos(c)
    seen, cols = {}, []
    for c in data:
        if c['key'] in seen:
            c['key'] += '-' + str(len(seen))
        seen[c['key']] = 1
    cities = []
    for key, label, state, cap, names in REGIONS:
        ids = [c for c in data if c['city'].strip().lower() in names and (c['state'] == state or key in ('delhi', 'chandigarh', 'vijayawada', 'puducherry'))]
        ids.sort(key=lambda c: (c['pos'], -(c['score'] or 0), c['name']))
        if ids:
            cities.append(dict(key=key, label=label, state=state, capital=cap, n=len(ids), ids=[c['key'] for c in ids[:10]]))
    states = {}
    for c in data:
        states.setdefault(c['state'], []).append(c)
    sts = []
    for s, lst in sorted(states.items()):
        lst.sort(key=lambda c: (c['pos'], -(c['score'] or 0), c['name']))
        sts.append(dict(key=slug(s), label=s, n=len(lst), ids=[c['key'] for c in lst[:10]]))
    used = {k for g in cities + sts for k in g['ids']}
    cols = [dict(key=c['key'], name=c['name'], city=c['city'], state=c['state'], rank=c['rank'], band=c['band'], score=c['score'], type=c['type'], nirf_id=c['id']) for c in data if c['key'] in used]
    json.dump(dict(colleges=cols, cities=cities, states=sts), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(cols), 'colleges;', len(cities), 'cities;', len(sts), 'states')
    for g in cities:
        print(g['label'].ljust(30), g['n'], len(g['ids']))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(APP, 'data', 'eng_cities.json'))
