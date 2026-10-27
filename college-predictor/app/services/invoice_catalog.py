"""Items an admin can pick from when writing an invoice: the EduAakashaA membership paths (prices from models_membership.TIER_PRICES) plus any items the admin adds.
Saved in the settings table (key 'invoice_catalog') once the admin edits it; until then the membership paths are offered at their listed prices. A price chosen
here is only a starting point: the invoice row's rate is always editable."""
import json

from app.extensions import db
from app.models_membership import TIER_PRICES, TIERS, Setting

KEY = 'invoice_catalog'


def default_items():
    return [{'name': '%s membership' % t, 'price': round(TIER_PRICES.get(t, 0) / 100, 2), 'group': 'Membership'} for t in TIERS if t in TIER_PRICES]


def _clean(items):
    out = []
    for it in items or []:
        name = str(it.get('name') or '').strip()[:200]
        if not name:
            continue
        try:
            price = max(round(float(it.get('price') or 0), 2), 0)
        except (TypeError, ValueError):
            price = 0
        out.append({'name': name, 'price': price, 'group': 'Membership' if it.get('group') == 'Membership' else 'Other'})
    return out


def load():
    row = db.session.get(Setting, KEY)
    if row and row.value:
        try:
            items = _clean(json.loads(row.value))
            if items:
                return items
        except (ValueError, TypeError):
            pass
    return default_items()


def save(items):
    row = db.session.get(Setting, KEY) or Setting(key=KEY)
    row.value = json.dumps(_clean(items))
    db.session.add(row)
    db.session.commit()


def reset():
    row = db.session.get(Setting, KEY)
    if row:
        db.session.delete(row)
        db.session.commit()
