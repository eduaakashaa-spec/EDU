# Legacy Apps Script — Reference Snapshot

Captured from the two live Google Apps Script projects so the migration has a
record of the existing behaviour. **No secrets are reproduced here** (bank
details, PAN, admin password and IDs live in the script's CONFIG block /
PropertiesService and must be copied by hand into the new `.env`).

## Projects

| Project | Script ID | Role |
|---|---|---|
| EA ADMIN PORTAL | `1xN2M02oNRQlJfLHJBcJrIgsIVw76G1wpn7VZ9Ejk9xY0CxZhT3Lp4UjN` | Backend `Code.gs` (doGet/doPost) + `Admin.html` |
| EA MEMBERSHIP NRI PORTAL | `1r2EYG_V9812jyXN5BswmJlPcRLuLlKIf29SekHb6D3z7Ts7YCbv3rrc1` | `Admin.html` front-end (EduAakashaa-styled) |

## What the backend does

- `doPost(...)` — receives free membership applications from
  `premium-membership.html`, appends a row to the Google Sheet.
- `doGet(?page=admin)` — serves the admin portal HTML.
- `google.script.run` APIs — admin actions (login, edit, discount, ad-hoc
  items, issue invoice, record payment, resend email).
- Google Sheet — single source of truth ("Requests" tab).
- Google Drive — stores every invoice + receipt PDF (folders: Requests /
  Invoices / Receipts).
- Gmail (MailApp/GmailApp) — notifies the requestor and info@eduaakashaa.com.

## Google services used (counts)

SpreadsheetApp (DB), DriveApp (PDF storage), MailApp + GmailApp (email),
PropertiesService (config + sequence counters), ContentService (JSON API),
HtmlService (admin portal + HTML→PDF), Utilities (blob/PDF conversion).

## Function inventory (Code.gs, ~835 lines)

Entry / routing: `doGet`, `doPost`, `readParams`, `jsonOut`
Application intake: `handleApplicationSubmit`
Admin auth: `adminLogin`, `guard`  *(single shared password)*
Admin actions: `adminListRequests`, `adminUpdateRequest`, `adminSetDiscount`,
  `adminSetAdhoc`, `adminIssueInvoice`, `adminRecordPayment`, `adminResend`
Pricing/GST: `computeTotals`, `recalcRow`, `tierDescriptor`, `round2`, `money`
Sheet-as-DB: `getSheet`, `migrateHeaders`, `rowToObj`, `COL`, `g`, `getOne`, `setIf`
Sequences: `nextReference`, `nextInvoiceNo`, `nextReceiptNo`, `nextSeq`
Drive: `rootFolder`, `subFolder`, `saveToDrive`, `fileFromUrl`, `logoDataUri`
PDF build: `buildDocumentPdf`, `documentHtml`, `lineRow`, `row2`
Email: `emailApplicationReceived`, `emailInvoice`, `emailReceipt`, `mailShell`, `kvTable`
Utils: `clean`, `pad`, `esc`, `safeParse`, `fmtDate`, `fy`, `setup`

## Sheet schema — "Requests" tab (the database to migrate)

```
Reference, Timestamp, Status, Name, Email, Phone, City, State,
Tier, Tier Price, Add-ons, Add-on Amount,
Discount, Discount Reason, Ad-hoc Items (JSON), Ad-hoc Amount,
Final Total (incl GST), Taxable Value, CGST, SGST, IGST, Total GST,
Invoice No, Invoice URL, Invoice Date,
Payment Status, Amount Paid, Balance Due, Payment Mode, Payment Ref, Payment Date,
Receipt No, Receipt URL, Internal Notes, Last Updated
```

### Enumerations observed
- **Tiers:** Foundation Path · Aspirant Path · NRI / Global · Elite Mentorship
- **Status:** New · Approved · Invoiced · Partially Paid · Paid
- **Payment Status:** Unpaid · Partially Paid · Paid
- **Reference prefix:** `EA-PREM-` ; sequence keys in PropertiesService:
  `lastSeq` (ref `EA/...`), `lastInv` (`EA/...` invoice no), `lastRcpt` (`RCPT/...`)
- **Tax:** CGST+SGST when place of supply = home state (Tamil Nadu), else IGST; GST 18%, prices GST-inclusive.

## Secrets to copy by hand into the new `.env` (do NOT commit)
- Admin password (currently the shared `admin` guard)
- Spreadsheet ID, Drive root folder ID
- Bank account name / number / IFSC / branch, company PAN
- Logo Drive file URL/ID
- Any Gmail/notification address overrides
