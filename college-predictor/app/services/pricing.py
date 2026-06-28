"""
GST pricing engine — ports the Apps Script `computeTotals`/`recalcRow` logic.

All money is handled in **paise** (integers) to avoid floating-point rounding
errors. Prices are GST-INCLUSIVE (the customer-facing price already contains the
18% tax), so we back-calculate the taxable value and tax components.

Place of supply rule:
  - customer state == company home state  → intra-state → CGST + SGST
  - otherwise                              → inter-state → IGST
"""
from dataclasses import dataclass, asdict


@dataclass
class Totals:
    final_total: int      # paise, GST inclusive (what the customer pays)
    taxable_value: int    # paise, before GST
    total_gst: int        # paise
    cgst: int             # paise
    sgst: int             # paise
    igst: int             # paise
    intra_state: bool

    def as_dict(self):
        return asdict(self)


def compute_totals(tier_price=0, addon_amount=0, adhoc_amount=0, discount=0,
                   customer_state='', home_state='Tamil Nadu', gst_rate=0.18):
    """
    Compute the GST-inclusive total and its tax breakdown.

    All amount args are in paise. Returns a Totals dataclass.
    """
    tier_price = int(tier_price or 0)
    addon_amount = int(addon_amount or 0)
    adhoc_amount = int(adhoc_amount or 0)
    discount = int(discount or 0)

    gross = tier_price + addon_amount + adhoc_amount - discount
    if gross < 0:
        gross = 0

    final_total = gross
    # Back out the taxable value from a GST-inclusive amount.
    taxable_value = round(final_total / (1 + gst_rate))
    total_gst = final_total - taxable_value

    intra = bool(customer_state) and bool(home_state) and \
        customer_state.strip().lower() == home_state.strip().lower()

    if intra:
        cgst = total_gst // 2
        sgst = total_gst - cgst   # keep the rupee exact; remainder goes to SGST
        igst = 0
    else:
        igst = total_gst
        cgst = 0
        sgst = 0

    return Totals(
        final_total=final_total,
        taxable_value=taxable_value,
        total_gst=total_gst,
        cgst=cgst,
        sgst=sgst,
        igst=igst,
        intra_state=intra,
    )


# ---- small helpers for display ----------------------------------------------
def rupees(paise):
    """Format paise as a ₹ string, e.g. 99900 -> '₹999.00'."""
    paise = int(paise or 0)
    return f'₹{paise / 100:,.2f}'


def to_paise(rupee_value):
    """Convert a rupee value (str/float/int) to integer paise."""
    if rupee_value in (None, ''):
        return 0
    return int(round(float(rupee_value) * 100))
