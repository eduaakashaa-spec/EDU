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


@dataclass
class InvoiceTotals:
    subtotal: int         # paise, sum of line items (before discount/fee/GST)
    discount: int         # paise
    additional_fee: int   # paise
    taxable_value: int    # paise, GST-exclusive base (subtotal - discount + fee)
    total_gst: int        # paise
    cgst: int
    sgst: int
    igst: int
    total: int            # paise, taxable + GST (what the customer pays)
    intra_state: bool

    def as_dict(self):
        return asdict(self)


def compute_invoice_totals(items, discount=0, additional_fee=0, customer_state='',
                           home_state='Tamil Nadu', gst_rate=0.18):
    """GST-EXCLUSIVE invoice maths: line items are pre-tax, GST is added on top
    of (subtotal - discount + additional_fee). All amounts in paise.

    `items` is a list of dicts each with integer `qty` and `rate` (paise)."""
    subtotal = sum(int(i.get('qty', 1) or 0) * int(i.get('rate', 0) or 0) for i in items)
    discount = int(discount or 0)
    additional_fee = int(additional_fee or 0)

    taxable = subtotal - discount + additional_fee
    if taxable < 0:
        taxable = 0
    total_gst = round(taxable * gst_rate)

    intra = bool(customer_state) and bool(home_state) and \
        customer_state.strip().lower() == home_state.strip().lower()
    if intra:
        cgst = total_gst // 2
        sgst = total_gst - cgst
        igst = 0
    else:
        igst = total_gst
        cgst = sgst = 0

    return InvoiceTotals(
        subtotal=subtotal, discount=discount, additional_fee=additional_fee,
        taxable_value=taxable, total_gst=total_gst, cgst=cgst, sgst=sgst, igst=igst,
        total=taxable + total_gst, intra_state=intra)


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
