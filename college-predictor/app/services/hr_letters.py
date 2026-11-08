"""HR letters: the three EduAakashaA templates (offer, experience, relieving), their fields, reference numbers and the renderer.

Templates are plain text, one paragraph per line, with {{field}} placeholders and a few directives:
    @meta Left text | Right text      date and reference line          @title / @center / @h / @subject   headings
    @table comp                       the offer compensation table     @sign   signatory block     @accept   candidate acceptance block
    **bold**                          bold lead-in inside a line
Adapted from the EduAakashaa HR letter pack (offer, experience, relieving). Have labour counsel review the wording before first live use.
"""
import re
from datetime import date, datetime

from app.extensions import db
from app.models_hr import HrLetter, HrLetterTemplate

KINDS = {
    'offer': {'title': 'Offer letter', 'code': 'OFFER', 'name': 'candidate_full_name', 'blurb': 'At hiring, before the date of joining. Role, joining date, CTC with Annexure A and the terms; the candidate signs to accept.'},
    'experience': {'title': 'Experience certificate', 'code': 'EXP', 'name': 'employee_full_name', 'blurb': 'On or after the last working day, for future employers: tenure, designation, conduct and last drawn CTC.'},
    'relieving': {'title': 'Relieving letter', 'code': 'REL', 'name': 'employee_full_name', 'blurb': 'On the last working day: confirms notice served, handover, property returned and dues settled.'},
}
SIGNATORY = ('Dr. Muruganandam', 'Founder & Director')
WORKING_HOURS = 'Monday to Friday, 9:00 AM to 6:00 PM'

# ---- fields ----------------------------------------------------------------------------------------------------------------------------------
# kind: text | date | money | textarea ; money is entered as an annual INR amount
def _f(key, label, kind='text', required=True, default='', help=''):
    return dict(key=key, label=label, kind=kind, required=required, default=default, help=help)


_SIGN = [_f('authorized_signatory_name', 'Signatory name', default=SIGNATORY[0]), _f('authorized_signatory_designation', 'Signatory designation', default=SIGNATORY[1])]
FIELDS = {
    'offer': [
        _f('issue_date', 'Issue date', 'date'), _f('candidate_full_name', 'Candidate full name', help='Used in the acceptance block and the register.'),
        _f('candidate_first_name', 'First name', required=False, help='Used in the salutation. Left blank, the first word of the full name is used.'),
        _f('designation', 'Designation offered'), _f('office_location', 'Office location', default='Coimbatore'), _f('date_of_joining', 'Date of joining', 'date'),
        _f('working_hours', 'Working hours', default=WORKING_HOURS, help='Written into term 2 of the offer.'),
        _f('basic_annual', 'Basic salary, annual (INR)', 'money'), _f('hra_annual', 'HRA, annual (INR)', 'money'), _f('special_annual', 'Special allowance, annual (INR)', 'money'),
        _f('bonus_annual', 'Statutory bonus, annual (INR)', 'money'), _f('pf_annual', 'Employer PF contribution, annual (INR)', 'money'), _f('gratuity_annual', 'Gratuity provision, annual (INR)', 'money'),
        _f('reporting_manager_name', 'Reporting manager'), _f('reporting_manager_designation', 'Manager designation')] + _SIGN,
    'experience': [
        _f('issue_date', 'Issue date', 'date'), _f('employee_full_name', 'Employee full name'), _f('designation', 'Last designation held'),
        _f('office_location', 'Office location', default='Coimbatore'), _f('date_of_joining', 'Date of joining', 'date'), _f('date_of_leaving', 'Date of leaving (last working day)', 'date'),
        _f('key_responsibilities', 'Key responsibilities', 'textarea', help='One sentence, for example: student admissions counselling, parent engagement and follow-up.'),
        _f('reporting_manager', 'Reporting manager, with designation', help='For example: Arjun Krishnan, Head of Admissions.'),
        _f('conduct_adjective_1', 'Conduct word 1', default='dedicated'), _f('conduct_adjective_2', 'Conduct word 2', default='collaborative'), _f('conduct_adjective_3', 'Conduct word 3', default='highly professional'),
        _f('last_drawn_ctc', 'Last drawn annual CTC (INR)', 'money')] + _SIGN,
    'relieving': [
        _f('issue_date', 'Issue date', 'date', help='Normally the last working day.'), _f('employee_full_name', 'Employee full name'),
        _f('employee_first_name', 'First name', required=False, help='Used in the salutation. Left blank, the first word of the full name is used.'),
        _f('designation', 'Last designation held'), _f('date_of_joining', 'Date of joining', 'date'), _f('resignation_date', 'Resignation date', 'date'),
        _f('last_working_day', 'Last working day', 'date'), _f('notice_period_served', 'Notice period served', default='30 days'),
        _f('handover_recipient', 'Handover given to', help='For example: the HR team.')] + _SIGN,
}
ALL_KEYS = {k for fl in FIELDS.values() for k in (f['key'] for f in fl)}
COMPUTED = ['annual_ctc', 'basic_monthly', 'hra_monthly', 'special_monthly', 'bonus_monthly', 'gross_monthly', 'gross_annual', 'pf_monthly', 'gratuity_monthly', 'total_monthly', 'total_annual',
            'ref_no', 'year', 'serial']
ALLOWED = ALL_KEYS | set(COMPUTED) | {'basic_annual', 'hra_annual', 'special_annual', 'bonus_annual', 'pf_annual', 'gratuity_annual'}

# ---- default template text ---------------------------------------------------------------------------------------------------------------------
DEFAULTS = {
    'offer': '''@meta Date: {{issue_date}} | Ref No: {{ref_no}}
@subject Offer of Appointment - EduAakashaa
Dear {{candidate_first_name}},
We are delighted to extend this offer of appointment to you at EduAakashaa. Based on our interactions and your demonstrated potential, we are pleased to invite you to join our team in the role of {{designation}}, based at our {{office_location}} office.
Your date of joining shall be {{date_of_joining}}. Your Total Annual Cost to Company (CTC) shall be INR {{annual_ctc}}. A detailed break-up of your compensation is provided in Annexure A.
@h Annexure A - Compensation Break-up
@table comp
@h Terms & Conditions of Employment
1. **Probation.** You will be on probation for a period of six (6) months from the date of joining. Confirmation of employment is subject to satisfactory performance.
2. **Working Hours.** Standard working hours are {{working_hours}}. Additional hours may be required based on student counselling schedules, outreach events and academic cycles.
3. **Reporting Manager.** You will report to {{reporting_manager_name}}, {{reporting_manager_designation}}. Reporting lines may change in accordance with business requirements.
4. **Notice Period.** Either party may terminate this employment by providing one (1) month's written notice during probation and two (2) months' written notice after confirmation, or salary in lieu thereof.
5. **Confidentiality & Non-Disclosure.** You shall maintain strict confidentiality of all student personal data, parent contact information, mentorship intellectual property, counselling frameworks, pricing and proprietary methodologies, both during and after employment. This obligation survives termination.
6. **Leaves.** You will be entitled to twelve (12) Earned Leaves, ten (10) Casual Leaves and seven (7) Sick Leaves per calendar year, pro-rated for the first year of service. Leaves are subject to the Employee Handbook.
7. **Code of Conduct.** You shall abide by the EduAakashaa Employee Handbook, including policies on ethical counselling, student welfare, anti-harassment, data protection and social media conduct.
8. **Non-Solicitation.** For twelve (12) months following separation, you shall not solicit students, parents, employees, consultants or partner institutions of EduAakashaa for any competing purpose.
9. **Jurisdiction.** Jurisdiction: Coimbatore, Tamil Nadu courts.
10. **Offer Validity.** This offer is valid for seven (7) days from the date of issue. Kindly return a signed copy within this period, failing which the offer shall stand withdrawn.
We are excited to welcome you to the EduAakashaa family and look forward to a long and mutually rewarding association. Together, we will continue our mission of guiding students towards the right future.
@sign
@accept''',
    'experience': '''@meta Ref No: {{ref_no}} | Date: {{issue_date}}
@title EXPERIENCE CERTIFICATE
@center TO WHOMSOEVER IT MAY CONCERN
This is to certify that {{employee_full_name}} was employed with EduAakashaa in the position of {{designation}} at our {{office_location}} office from {{date_of_joining}} to {{date_of_leaving}}.
During the tenure, {{employee_full_name}} was primarily responsible for {{key_responsibilities}}, reporting to {{reporting_manager}}.
Throughout the association, we found {{employee_full_name}} to be {{conduct_adjective_1}}, {{conduct_adjective_2}} and {{conduct_adjective_3}} in approach. The last drawn annual CTC was INR {{last_drawn_ctc}}.
We confirm that the employee has been duly relieved of all responsibilities as of the date of leaving and has handed over all company property and confidential materials. There are no dues outstanding on either side.
We wish {{employee_full_name}} the very best in all future endeavours.
@sign''',
    'relieving': '''@meta Date: {{issue_date}} | Ref No: {{ref_no}}
@title RELIEVING LETTER
Dear {{employee_first_name}},
With reference to your resignation dated {{resignation_date}}, this is to confirm that you have been relieved from your duties as {{designation}} with EduAakashaa with effect from the close of business on {{last_working_day}}.
We acknowledge that you have:
1. Served the notice period of {{notice_period_served}} as per the terms of your employment.
2. Completed handover of all pending responsibilities to {{handover_recipient}}.
3. Returned all company property, documents, access credentials, and intellectual property.
4. Settled all financial dues; your full and final settlement has been processed.
Your period of employment with EduAakashaa was from {{date_of_joining}} to {{last_working_day}} in the role of {{designation}}.
We thank you for your contributions during your tenure and wish you the very best in your future endeavours.
@sign''',
}


# ---- formatting and numbers -------------------------------------------------------------------------------------------------------------------
def indian(n):
    """840000 -> '8,40,000'."""
    n = int(round(n))
    s, neg = str(abs(n)), n < 0
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ','.join(parts + [tail])
    return ('-' if neg else '') + s


def parse_money(text):
    t = re.sub(r'[,\s]|INR|Rs\.?|₹', '', str(text or ''), flags=re.I)
    if not re.fullmatch(r'\d+(\.\d+)?', t):
        raise ValueError('Enter an amount in rupees, digits only.')
    return int(round(float(t)))


def long_date(d):
    return d.strftime('%d %B %Y')


def fy_of(d):
    return d.year if d.month >= 4 else d.year - 1


def next_serial(kind, fy):
    last = db.session.query(db.func.max(HrLetter.serial)).filter_by(kind=kind, fy=fy).scalar()
    return (last or 0) + 1


def make_ref(kind, fy, serial):
    return 'EA/HR/%s/%d/%04d' % (KINDS[kind]['code'], fy, serial)


def comp_rows(v):
    """Compensation table rows (label, monthly, annual) from the annual components."""
    def m(a):
        return int(round(a / 12.0))
    basic, hra, special, bonus, pf, grat = (v['basic_annual'], v['hra_annual'], v['special_annual'], v['bonus_annual'], v['pf_annual'], v['gratuity_annual'])
    gross = basic + hra + special + bonus
    total = gross + pf + grat
    return [('Basic Salary', m(basic), basic), ('House Rent Allowance (HRA)', m(hra), hra), ('Special Allowance', m(special), special), ('Statutory Bonus', m(bonus), bonus),
            ('Gross Salary', m(gross), gross), ("Employer's PF Contribution", m(pf), pf), ('Gratuity', m(grat), grat), ('Total CTC', m(total), total)]


# ---- validation and the values a letter is issued with ------------------------------------------------------------------------------------------
def clean(kind, form):
    """Validate a submitted form. Returns (values, errors); values hold display strings plus the numbers needed to render."""
    vals, errors = {}, {}
    for f in FIELDS[kind]:
        raw = (form.get(f['key']) or '').strip()
        if not raw and f['key'] == 'candidate_first_name':
            raw = (form.get('candidate_full_name') or '').strip().split(' ')[0]
        if not raw and f['key'] == 'employee_first_name':
            raw = (form.get('employee_full_name') or '').strip().split(' ')[0]
        if not raw and f['required']:
            errors[f['key']] = 'Required.'
            continue
        if f['kind'] == 'date' and raw:
            try:
                vals[f['key'] + '__d'] = date.fromisoformat(raw)
                vals[f['key']] = long_date(vals[f['key'] + '__d'])
            except ValueError:
                errors[f['key']] = 'Enter a valid date.'
        elif f['kind'] == 'money' and raw:
            try:
                n = parse_money(raw)
                vals[f['key'] + '__n'] = n
                vals[f['key']] = indian(n)
            except ValueError as ex:
                errors[f['key']] = str(ex)
        else:
            vals[f['key']] = re.sub(r'\s*\n\s*', ' ', raw)[:400]
        if len(raw) > 400 and f['kind'] in ('text', 'textarea'):
            errors[f['key']] = 'Keep it under 400 characters.'
    d = lambda k: vals.get(k + '__d')                                                                       # noqa: E731
    if kind == 'experience' and d('date_of_joining') and d('date_of_leaving') and d('date_of_leaving') < d('date_of_joining'):
        errors['date_of_leaving'] = 'The date of leaving is before the date of joining.'
    if kind == 'relieving':
        if d('resignation_date') and d('date_of_joining') and d('resignation_date') < d('date_of_joining'):
            errors['resignation_date'] = 'The resignation date is before the date of joining.'
        if d('last_working_day') and d('resignation_date') and d('last_working_day') < d('resignation_date'):
            errors['last_working_day'] = 'The last working day is before the resignation date.'
    if kind == 'offer' and not errors:
        nums = {k: vals[k + '__n'] for k in ('basic_annual', 'hra_annual', 'special_annual', 'bonus_annual', 'pf_annual', 'gratuity_annual')}
        rows = comp_rows(nums)
        for (label, mo, an), key in zip(rows, ('basic', 'hra', 'special', 'bonus', 'gross', 'pf', 'gratuity', 'total')):
            vals[key + '_monthly'], vals[key + '_annual'] = indian(mo), indian(an)
        vals['annual_ctc'] = vals['total_annual']
    return vals, errors


def blocks(body, vals):
    """Template text -> list of blocks with every {{field}} filled."""
    def fill(t):
        return re.sub(r'\{\{\s*(\w+)\s*\}\}', lambda m: str(vals.get(m.group(1), '[' + m.group(1) + ']')), t)
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('@'):
            word, _, rest = line[1:].partition(' ')
            rest = fill(rest.strip())
            if word == 'meta':
                left, _, right = rest.partition('|')
                out.append(('meta', left.strip(), right.strip()))
            elif word in ('title', 'center', 'h', 'subject'):
                out.append((word, rest))
            elif word == 'table' and rest.strip() == 'comp':
                rows = []
                for key, label in (('basic', 'Basic Salary'), ('hra', 'House Rent Allowance (HRA)'), ('special', 'Special Allowance'), ('bonus', 'Statutory Bonus'), ('gross', 'Gross Salary'),
                                   ('pf', "Employer's PF Contribution"), ('gratuity', 'Gratuity'), ('total', 'Total CTC')):
                    rows.append((label, vals.get(key + '_monthly', ''), vals.get(key + '_annual', ''), key in ('gross', 'total')))
                out.append(('table', rows))
            elif word == 'sign':
                out.append(('sign', vals.get('authorized_signatory_name', SIGNATORY[0]), vals.get('authorized_signatory_designation', SIGNATORY[1])))
            elif word == 'accept':
                out.append(('accept', vals.get('candidate_full_name', '')))
            continue
        out.append(('p', fill(line)))
    return out


def _esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline_html(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', _esc(t))


def validate_body(body):
    """Template editor check: only known placeholders and directives."""
    errs = []
    for m in set(re.findall(r'\{\{\s*(\w+)\s*\}\}', body)):
        if m not in ALLOWED:
            errs.append('Unknown placeholder {{%s}}.' % m)
    for line in body.splitlines():
        if line.strip().startswith('@') and line.strip()[1:].split(' ')[0] not in ('meta', 'title', 'center', 'h', 'subject', 'table', 'sign', 'accept'):
            errs.append('Unknown directive %s.' % line.strip().split(' ')[0])
    if len(body) > 20000:
        errs.append('The template is too long.')
    return errs


def sample_values(kind):
    """Sample values for the template preview."""
    form = {f['key']: f['default'] for f in FIELDS[kind]}
    today = date.today().isoformat()
    form.update(issue_date=today, date_of_joining='2024-03-15', date_of_leaving=today, resignation_date='2026-10-15', last_working_day=today,
                candidate_full_name='Priya Ramesh', candidate_first_name='Priya', employee_full_name='Priya Ramesh', employee_first_name='Priya', designation='Senior Admissions Counsellor',
                reporting_manager_name='Arjun Krishnan', reporting_manager_designation='Head of Admissions', reporting_manager='Arjun Krishnan, Head of Admissions',
                key_responsibilities='student admissions counselling, parent engagement and follow-up', handover_recipient='the HR team', last_drawn_ctc='7,20,000',
                basic_annual='336000', hra_annual='168000', special_annual='252000', bonus_annual='28000', pf_annual='40320', gratuity_annual='15680')
    form['date_of_joining'] = '2026-12-01' if kind == 'offer' else '2024-03-15'
    vals, _ = clean(kind, form)
    vals['ref_no'] = make_ref(kind, fy_of(date.today()), 1)
    return vals


# ---- templates and issuing -----------------------------------------------------------------------------------------------------------------------
def template(kind):
    row = HrLetterTemplate.query.filter_by(kind=kind).first()
    if not row:
        row = HrLetterTemplate(kind=kind, body=DEFAULTS[kind], version=1)
        db.session.add(row)
        db.session.commit()
    return row


def issue(kind, vals, user):
    """Allocate the next reference number and store the letter. Caller has validated vals via clean()."""
    d = vals['issue_date__d']
    fy = fy_of(d)
    tpl = template(kind)
    for _attempt in range(3):                                   # two people issuing at once: retry on a clashing serial
        serial = next_serial(kind, fy)
        vals = dict(vals, ref_no=make_ref(kind, fy, serial), year=str(fy), serial='%04d' % serial)
        stored = {k: (v.isoformat() if isinstance(v, date) else v) for k, v in vals.items()}
        import json
        row = HrLetter(kind=kind, fy=fy, serial=serial, ref_no=vals['ref_no'], person_name=vals.get(KINDS[kind]['name'], ''), designation=vals.get('designation', ''), issue_date=d,
                       values_json=json.dumps(stored), body_snapshot=tpl.body, template_version=tpl.version, created_by=user.id)
        db.session.add(row)
        try:
            db.session.commit()
            return row
        except Exception:
            db.session.rollback()
    raise RuntimeError('Could not allocate a reference number; try again.')


def render(letter):
    return blocks(letter.body_snapshot, letter.values)


def to_html(bl):
    """Blocks -> HTML for the on-screen letter (the PDF draws the same blocks)."""
    h = []
    for b in bl:
        k = b[0]
        if k == 'meta':
            h.append('<div class="hl-meta"><span>%s</span><span>%s</span></div>' % (inline_html(b[1]), inline_html(b[2])))
        elif k == 'subject':
            h.append('<p class="hl-subject"><b>%s</b></p>' % inline_html(b[1]))
        elif k == 'title':
            h.append('<h2 class="hl-title">%s</h2>' % inline_html(b[1]))
        elif k == 'center':
            h.append('<p class="hl-center"><b>%s</b></p>' % inline_html(b[1]))
        elif k == 'h':
            h.append('<h3 class="hl-h">%s</h3>' % inline_html(b[1]))
        elif k == 'p':
            cls = ' class="hl-item"' if re.match(r'^\d+\. ', b[1]) else ''
            h.append('<p%s>%s</p>' % (cls, inline_html(b[1])))
        elif k == 'table':
            rows = ''.join('<tr class="%s"><td>%s</td><td>%s</td><td>%s</td></tr>' % ('tot' if r[3] else '', _esc(r[0]), _esc(r[1]), _esc(r[2])) for r in b[1])
            h.append('<table class="hl-tbl"><thead><tr><th>Component</th><th>Monthly (INR)</th><th>Annual (INR)</th></tr></thead><tbody>%s</tbody></table>' % rows)
        elif k == 'sign':
            h.append('<div class="hl-sign"><p>For EduAakashaa,</p><div class="hl-seal">Signature &amp; company seal</div><p><b>%s</b><br>%s</p></div>' % (_esc(b[1]), _esc(b[2])))
        elif k == 'accept':
            h.append('<div class="hl-accept"><h3 class="hl-h">Candidate Acceptance</h3><p>I, %s, have read and understood the terms of this offer letter including Annexure A and accept the same unconditionally.</p>'
                     '<p>Signature: ______________________________ &nbsp;&nbsp;&nbsp; Date: ______________</p></div>' % _esc(b[1]))
    return ''.join(h)
