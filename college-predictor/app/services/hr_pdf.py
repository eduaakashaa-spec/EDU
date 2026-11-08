"""A4 PDF of an HR letter on the EduAakashaA letterhead (reportlab), drawn from the same blocks as the on-screen letter."""
import os
import re
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

NAVY, INK, MUTED, HAIR, ORANGE = colors.HexColor('#0E3A8A'), colors.HexColor('#0E1B3D'), colors.HexColor('#5A6278'), colors.HexColor('#E8DFC8'), colors.HexColor('#FF6B0A')
W, H = A4
MX = 25 * mm                                                                                 # 2.5 cm margins, as in the Word templates
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'logo.png')
CONTACT = 'Coimbatore, Tamil Nadu  -  +91 80157 22706  |  info@eduaakashaa.com  |  www.eduaakashaa.com'

ST = {
    'p': ParagraphStyle('p', fontName='Helvetica', fontSize=10, leading=14.5, textColor=INK, spaceAfter=7, alignment=4),
    'item': ParagraphStyle('item', fontName='Helvetica', fontSize=10, leading=14.5, textColor=INK, spaceAfter=5, leftIndent=14, firstLineIndent=-14, alignment=4),
    'h': ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=5),
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=NAVY, alignment=1, spaceBefore=6, spaceAfter=8),
    'center': ParagraphStyle('center', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=INK, alignment=1, spaceAfter=10),
    'subject': ParagraphStyle('subject', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=INK, spaceBefore=4, spaceAfter=9),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=9.5, leading=12, textColor=INK),
    'cellb': ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=INK),
}


def _x(t):
    """Escape for reportlab Paragraph markup, keep **bold**, and drop characters Helvetica cannot draw."""
    t = str(t).replace('₹', 'INR ').replace('–', '-').replace('—', '-').replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    t = t.encode('latin-1', 'replace').decode('latin-1')
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


class _Numbered(rl_canvas.Canvas):
    """Canvas that knows the page count, for 'Page x of y' in the footer."""
    void = False

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self._decor(n)
            super().showPage()
        super().save()

    def _decor(self, n):
        c = self
        c.saveState()
        if os.path.exists(LOGO):
            c.drawImage(LOGO, MX, H - 27 * mm, width=14 * mm, height=14 * mm, preserveAspectRatio=True, mask='auto')
        c.setFont('Helvetica-Bold', 16)
        c.setFillColor(NAVY)
        c.drawString(MX + 17 * mm, H - 19 * mm, 'Edu')
        c.setFillColor(ORANGE)
        c.drawString(MX + 17 * mm + c.stringWidth('Edu', 'Helvetica-Bold', 16), H - 19 * mm, 'Aakashaa')
        c.setFont('Helvetica-Oblique', 8.5)
        c.setFillColor(MUTED)
        c.drawString(MX + 17 * mm, H - 24 * mm, 'Guiding students towards the right future')
        c.setFont('Helvetica', 8)
        c.drawRightString(W - MX, H - 16 * mm, 'Coimbatore, Tamil Nadu, India')
        c.drawRightString(W - MX, H - 20 * mm, '+91 80157 22706  |  info@eduaakashaa.com')
        c.drawRightString(W - MX, H - 24 * mm, 'www.eduaakashaa.com')
        c.setStrokeColor(ORANGE)
        c.setLineWidth(1.4)
        c.line(MX, H - 30 * mm, W - MX, H - 30 * mm)
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.6)
        c.line(MX, 20 * mm, W - MX, 20 * mm)
        c.setFont('Helvetica', 7.8)
        c.setFillColor(MUTED)
        c.drawString(MX, 15.5 * mm, CONTACT)
        c.drawRightString(W - MX, 15.5 * mm, '%d of %d' % (c._pageNumber, n))
        if self.void:
            c.setFont('Helvetica-Bold', 90)
            c.setFillColor(colors.Color(0.76, 0.23, 0.23, alpha=0.16))
            c.translate(W / 2, H / 2)
            c.rotate(35)
            c.drawCentredString(0, 0, 'VOID')
        c.restoreState()


def build(bl, title='HR letter', void=False):
    story = []
    for b in bl:
        k = b[0]
        if k == 'meta':
            t = Table([[Paragraph(_x(b[1]), ST['cellb']), Paragraph(_x(b[2]), ParagraphStyle('r', parent=ST['cellb'], alignment=2))]], colWidths=[(W - 2 * MX) / 2] * 2)
            t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
            story.append(t)
        elif k in ('subject', 'title', 'center', 'h'):
            story.append(Paragraph(_x(b[1]), ST[k]))
        elif k == 'p':
            story.append(Paragraph(_x(b[1]), ST['item'] if re.match(r'^\d+\. ', b[1]) else ST['p']))
        elif k == 'table':
            data = [[Paragraph('COMPONENT', ParagraphStyle('th', parent=ST['cellb'], textColor=colors.white, fontSize=8)), Paragraph('MONTHLY (INR)', ParagraphStyle('th', parent=ST['cellb'], textColor=colors.white, fontSize=8, alignment=2)),
                     Paragraph('ANNUAL (INR)', ParagraphStyle('th', parent=ST['cellb'], textColor=colors.white, fontSize=8, alignment=2))]]
            style = [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('LINEBELOW', (0, 0), (-1, -1), 0.4, HAIR), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
            for i, r in enumerate(b[1], start=1):
                s = ST['cellb'] if r[3] else ST['cell']
                data.append([Paragraph(_x(r[0]), s), Paragraph(_x(r[1]), ParagraphStyle('n', parent=s, alignment=2)), Paragraph(_x(r[2]), ParagraphStyle('n', parent=s, alignment=2))])
                if r[3]:
                    style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FFF4E8')))
            t = Table(data, colWidths=[(W - 2 * MX) * 0.54, (W - 2 * MX) * 0.23, (W - 2 * MX) * 0.23], repeatRows=1)
            t.setStyle(TableStyle(style))
            story += [t, Spacer(1, 8)]
        elif k == 'sign':
            seal = Table([[Paragraph('Signature &amp; company seal', ParagraphStyle('s', parent=ST['cell'], textColor=MUTED, alignment=1))]], colWidths=[62 * mm], rowHeights=[20 * mm])
            seal.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, HAIR), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
            seal.hAlign = 'LEFT'
            story.append(KeepTogether([Spacer(1, 6), Paragraph('For EduAakashaa,', ST['p']), seal, Spacer(1, 4),
                                       Paragraph('<b>%s</b><br/>%s' % (_x(b[1]), _x(b[2])), ST['p'])]))
        elif k == 'accept':
            story.append(KeepTogether([Spacer(1, 10), Paragraph('Candidate Acceptance', ST['h']),
                                       Paragraph('I, %s, have read and understood the terms of this offer letter including Annexure A and accept the same unconditionally.' % _x(b[1]), ST['p']),
                                       Spacer(1, 10), Paragraph('Signature: ______________________________ &nbsp;&nbsp;&nbsp;&nbsp; Date: ______________', ST['p'])]))
    buf = BytesIO()
    doc = BaseDocTemplate(buf, pagesize=A4, title=title, author='EduAakashaA', leftMargin=MX, rightMargin=MX, topMargin=36 * mm, bottomMargin=26 * mm)
    doc.addPageTemplates([PageTemplate(id='l', frames=[Frame(MX, 26 * mm, W - 2 * MX, H - 62 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)])])

    class Canvas(_Numbered):
        pass
    Canvas.void = bool(void)
    doc.build(story, canvasmaker=Canvas)
    return buf.getvalue()
