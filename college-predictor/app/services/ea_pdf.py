"""EduAakashaA report look for server-generated PDFs (reportlab, so it works on the web server without a browser engine).

Follows the EduAakashaA report design system: dark navy cover with an orange glow and the logo, warm cream inner pages, navy as the workhorse colour with orange as
a sparing accent, serif headings, mono UPPERCASE labels, CSS-style bar charts, balanced callouts, a closing contact page and a standing disclaimer.
Usage: build_report(meta, pages) where `pages` is a list of lists of flowables made with the helpers below."""
import os
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

NAVY, NAVY_DEEP, NAVY_INK = colors.HexColor('#0E3A8A'), colors.HexColor('#0A2560'), colors.HexColor('#071A44')
ORANGE, ORANGE_SOFT = colors.HexColor('#FF6B0A'), colors.HexColor('#FF8A3D')
CREAM, CREAM2, PAPER = colors.HexColor('#FBF7EE'), colors.HexColor('#F5EFDF'), colors.HexColor('#FFFDF7')
INK, MUTED, HAIR = colors.HexColor('#0E1B3D'), colors.HexColor('#5A6278'), colors.HexColor('#E8DFC8')
GREEN, RED, AMBER = colors.HexColor('#1F8B5C'), colors.HexColor('#C23A3A'), colors.HexColor('#E89A1C')
W, H = A4
MX = 16 * mm
LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'logo.png')

SERIF, SERIF_I, SANS, SANS_B, MONO = 'Times-Bold', 'Times-BoldItalic', 'Helvetica', 'Helvetica-Bold', 'Courier-Bold'

ST = {
    'h1': ParagraphStyle('h1', fontName=SERIF, fontSize=22, leading=25, textColor=NAVY_INK, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName=SERIF, fontSize=14, leading=17, textColor=NAVY_INK, spaceBefore=12, spaceAfter=5),
    'eyebrow': ParagraphStyle('eyebrow', fontName=MONO, fontSize=7.6, leading=10, textColor=ORANGE, spaceAfter=3),
    'p': ParagraphStyle('p', fontName=SANS, fontSize=9.6, leading=14, textColor=INK, spaceAfter=4),
    'small': ParagraphStyle('small', fontName=SANS, fontSize=7.8, leading=11, textColor=MUTED),
    'cell': ParagraphStyle('cell', fontName=SANS, fontSize=8.6, leading=11, textColor=INK),
    'cellb': ParagraphStyle('cellb', fontName=SANS_B, fontSize=8.6, leading=11, textColor=INK),
    'th': ParagraphStyle('th', fontName=MONO, fontSize=7.2, leading=9, textColor=colors.white),
}


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def P(text, style='p'):
    return Paragraph(text, ST[style])


def eyebrow(text):
    return Paragraph(esc(text).upper(), ST['eyebrow'])


def heading(eyebrow_text, title):
    return [eyebrow(eyebrow_text), Paragraph(title, ST['h1']), Spacer(1, 3)]


# ---- components --------------------------------------------------------------------------------------------------------------------
def kpis(items, width=W - 2 * MX):
    """Row of stat tiles. items: [(label, value, tone)] with tone navy|orange|green|red."""
    tone = {'navy': NAVY, 'orange': ORANGE, 'green': GREEN, 'red': RED}
    n = len(items)
    cells = [[Paragraph('<font name="%s" size="19" color="%s">%s</font>' % (SERIF, tone.get(t, NAVY).hexval().replace('0x', '#'), esc(v)), ST['p']),
              Paragraph(esc(l).upper(), ParagraphStyle('kl', fontName=MONO, fontSize=6.6, leading=8.5, textColor=MUTED))] for l, v, t in items]
    tbl = Table([[c for c in cells]], colWidths=[width / n] * n)
    tbl.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), PAPER), ('BOX', (0, 0), (-1, -1), 0.6, HAIR), ('LINEAFTER', (0, 0), (-2, -1), 0.6, HAIR), ('LINEABOVE', (0, 0), (-1, 0), 2.4, ORANGE),
                             ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 9), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    return tbl


class Bars(Flowable):
    """Horizontal bar chart drawn natively (no JS). rows: [(label, pct 0-100 or None, value_text, colour)]."""

    def __init__(self, rows, width=W - 2 * MX, label_w=38 * mm, row_h=8.2 * mm):
        super().__init__()
        self.rows, self.width, self.label_w, self.row_h = rows, width, label_w, row_h
        self.height = row_h * len(rows) + 2

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        track_w = self.width - self.label_w - 2 * mm
        for i, (label, pct, text, col) in enumerate(self.rows):
            y = self.height - (i + 1) * self.row_h + 1.5 * mm
            c.setFillColor(INK)
            c.setFont(SANS_B, 8.4)
            c.drawString(0, y + 1.6 * mm, label[:30])
            c.setFillColor(CREAM2)
            c.roundRect(self.label_w, y, track_w, 5.2 * mm, 2.6 * mm, stroke=0, fill=1)
            if pct is not None and pct > 0:
                c.setFillColor(col)
                c.roundRect(self.label_w, y, max(5.2 * mm, track_w * min(pct, 100) / 100), 5.2 * mm, 2.6 * mm, stroke=0, fill=1)
            c.setFillColor(colors.white if pct and pct >= 22 else INK)
            c.setFont(MONO, 7.4)
            tx = self.label_w + (max(5.2 * mm, track_w * min(pct or 0, 100) / 100) - 2 * mm if pct and pct >= 22 else track_w * (pct or 0) / 100 + 2 * mm)
            (c.drawRightString if pct and pct >= 22 else c.drawString)(tx, y + 1.7 * mm, text)


def callout(text, tone='orange'):
    col = {'orange': ORANGE, 'navy': NAVY, 'green': GREEN, 'red': RED}.get(tone, ORANGE)
    t = Table([[Paragraph(text, ST['p'])]], colWidths=[W - 2 * MX])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF1E6') if tone == 'orange' else PAPER), ('LINEBEFORE', (0, 0), (0, -1), 3, col), ('BOX', (0, 0), (-1, -1), 0.5, HAIR),
                           ('LEFTPADDING', (0, 0), (-1, -1), 11), ('RIGHTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    return t


def data_table(head, rows, widths):
    body = [[Paragraph(esc(h).upper(), ST['th']) for h in head]] + [[Paragraph(esc(c), ST['cell']) if not isinstance(c, Flowable) else c for c in r] for r in rows]
    t = Table(body, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY_INK), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [PAPER, CREAM2]), ('GRID', (0, 0), (-1, -1), 0.3, HAIR), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 7)]))
    return t


def steps(items):
    """Numbered action list. items: [(title, text)]."""
    rows = []
    for i, (t, x) in enumerate(items, 1):
        rows.append([Paragraph('<font name="%s" size="15" color="#FF6B0A">%02d</font>' % (SERIF, i), ST['p']), Paragraph('<b>%s</b><br/>%s' % (esc(t), esc(x)), ST['p'])])
    tb = Table(rows, colWidths=[13 * mm, W - 2 * MX - 13 * mm])
    tb.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -2), 0.4, HAIR), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    return tb


# ---- page furniture ----------------------------------------------------------------------------------------------------------------
def _glow(c, cx, cy, r, col, steps_=22):
    c.saveState()
    for i in range(steps_):
        c.setFillColor(col)
        c.setFillAlpha(0.012 + 0.012 * i / steps_)
        c.circle(cx, cy, r * (1 - i / steps_), stroke=0, fill=1)
    c.restoreState()


def _navy_page(c):
    n = 70
    for i in range(n):
        f = i / (n - 1)
        a, b = (NAVY_INK, NAVY_DEEP) if f < .6 else (NAVY_DEEP, NAVY)
        g = f / .6 if f < .6 else (f - .6) / .4
        col = colors.Color(a.red + (b.red - a.red) * g, a.green + (b.green - a.green) * g, a.blue + (b.blue - a.blue) * g)
        c.setFillColor(col)
        c.rect(0, H - (i + 1) * H / n - 1, W, H / n + 2, stroke=0, fill=1)
    _glow(c, W * .86, H * .9, 120 * mm, ORANGE)
    _glow(c, W * .05, H * .08, 70 * mm, ORANGE_SOFT)


def _wordmark(c, x, y, size=15, on_dark=True):
    c.setFont(SERIF, size)
    c.setFillColor(colors.white if on_dark else NAVY_INK)
    c.drawString(x, y, 'Edu')
    wd = c.stringWidth('Edu', SERIF, size)
    c.setFillColor(ORANGE_SOFT if on_dark else ORANGE)
    c.drawString(x + wd, y, 'Aakashaa')


def _logo(c, x, y, s):
    try:
        c.drawImage(LOGO, x, y, s, s, mask='auto', preserveAspectRatio=True)
    except Exception:
        pass


def draw_cover(c, meta):
    _navy_page(c)
    _logo(c, MX, H - 32 * mm, 15 * mm)
    _wordmark(c, MX + 18 * mm, H - 24 * mm, 17)
    c.setFont(MONO, 7.4)
    c.setFillColor(colors.Color(1, 1, 1, .6))
    c.drawString(MX + 18 * mm, H - 29 * mm, 'GUIDING STUDENTS TOWARDS THE RIGHT FUTURE')
    c.setFillColor(ORANGE_SOFT)
    c.setFont(MONO, 8.4)
    c.drawString(MX, H * .56, meta['eyebrow'].upper())
    y = H * .56 - 14 * mm
    for ln, em in meta['title_lines']:
        c.setFont(SERIF_I if em else SERIF, 34)
        c.setFillColor(ORANGE_SOFT if em else colors.white)
        c.drawString(MX, y, ln)
        y -= 14 * mm
    c.setFont(SANS, 11)
    c.setFillColor(colors.Color(1, 1, 1, .8))
    for ln in meta['subtitle']:
        c.drawString(MX, y, ln)
        y -= 6 * mm
    # headline result card
    cw, ch, cy = W - 2 * MX, 30 * mm, 34 * mm
    c.setFillColor(colors.Color(1, 1, 1, .08))
    c.roundRect(MX, cy, cw, ch, 4 * mm, stroke=0, fill=1)
    c.setStrokeColor(colors.Color(1, 1, 1, .22))
    c.roundRect(MX, cy, cw, ch, 4 * mm, stroke=1, fill=0)
    cols = meta['cover_stats']
    for i, (lab, val) in enumerate(cols):
        x = MX + cw / len(cols) * i + 7 * mm
        c.setFont(SERIF, 21)
        c.setFillColor(colors.white if i else ORANGE_SOFT)
        c.drawString(x, cy + 15 * mm, str(val))
        c.setFont(MONO, 6.8)
        c.setFillColor(colors.Color(1, 1, 1, .62))
        c.drawString(x, cy + 8.5 * mm, lab.upper())
    c.setFont(MONO, 7)
    c.setFillColor(colors.Color(1, 1, 1, .5))
    c.drawString(MX, 20 * mm, meta['footer_left'].upper())
    c.drawRightString(W - MX, 20 * mm, 'PAGES %d' % meta['pages'])


def _inner(c, doc, meta):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(colors.Color(.055, .106, .239, .035))
    for gx in range(0, int(W), 9):                                  # faint grain, as on the cream template pages
        for gy in range(int(H * .0), int(H), 9):
            c.circle(gx, gy, .35, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(0, H - 3.2, W, 3.2, stroke=0, fill=1)
    _logo(c, MX, H - 14 * mm, 7 * mm)
    _wordmark(c, MX + 8.6 * mm, H - 11.2 * mm, 10.5, on_dark=False)
    c.setFont(MONO, 6.8)
    c.setFillColor(MUTED)
    c.drawRightString(W - MX, H - 11 * mm, meta['running_head'].upper())
    c.setStrokeColor(HAIR)
    c.setLineWidth(.6)
    c.line(MX, 14 * mm, W - MX, 14 * mm)
    c.setFont(MONO, 6.6)
    c.drawString(MX, 9.5 * mm, '%s  ·  PAGE %02d' % (meta['footer_left'].upper(), doc.page))
    c.drawRightString(W - MX, 9.5 * mm, 'WWW.EDUAAKASHAA.COM')


def draw_contact(c, meta):
    _navy_page(c)
    _logo(c, MX, H - 32 * mm, 15 * mm)
    _wordmark(c, MX + 18 * mm, H - 24 * mm, 17)
    c.setFillColor(ORANGE_SOFT)
    c.setFont(MONO, 8.4)
    c.drawString(MX, H * .70, 'LET US HELP YOU DECIDE')
    c.setFont(SERIF, 30)
    c.setFillColor(colors.white)
    c.drawString(MX, H * .70 - 13 * mm, 'Talk to a mentor.')
    c.setFont(SERIF_I, 30)
    c.setFillColor(ORANGE_SOFT)
    c.drawString(MX, H * .70 - 26 * mm, 'No upfront fee.')
    rows = [('INDIA', '+91 80157 22706'), ('UAE', '+971 50 516 8081'), ('EMAIL', 'info@eduaakashaa.com'), ('WEB', 'www.eduaakashaa.com'),
            ('OFFICES', 'Coimbatore, Tamil Nadu  ·  Dubai, UAE'), ('HOURS', 'Mon–Fri 9:00–22:00  ·  Sat & Sun 9:00–16:00')]
    y = H * .70 - 48 * mm
    for k, v in rows:
        c.setFont(MONO, 7.4)
        c.setFillColor(colors.Color(1, 1, 1, .55))
        c.drawString(MX, y, k)
        c.setFont(SANS_B, 11.5)
        c.setFillColor(colors.white)
        c.drawString(MX + 28 * mm, y, v)
        c.setStrokeColor(colors.Color(1, 1, 1, .14))
        c.line(MX, y - 3.2 * mm, W - MX, y - 3.2 * mm)
        y -= 10.5 * mm
    c.setFont(SERIF_I, 13)
    c.setFillColor(ORANGE_SOFT)
    c.drawString(MX, 28 * mm, 'Guiding students towards the right future')


def build_report(meta, content):
    """meta: eyebrow, title_lines [(text, italic_orange)], subtitle [lines], cover_stats [(label, value)], footer_left, running_head, title.
    content: flowables for the inner pages (use PageBreak between pages). A contact page is always appended."""
    n_inner = 1 + sum(1 for f in content if isinstance(f, PageBreak))
    meta = dict(meta, pages=1 + n_inner + 1)
    buf = BytesIO()
    doc = BaseDocTemplate(buf, pagesize=A4, title=meta.get('title', 'EduAakashaA report'), author='EduAakashaA', leftMargin=MX, rightMargin=MX, topMargin=22 * mm, bottomMargin=20 * mm)
    frame = Frame(MX, 20 * mm, W - 2 * MX, H - 42 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    state = {'contact': False}

    def cover(c, d):
        draw_cover(c, meta)

    def inner(c, d):
        if state['contact']:
            draw_contact(c, meta)
        else:
            _inner(c, d, meta)

    class _ContactMarker(Flowable):
        def wrap(self, aw, ah):
            return 0, 0

        def draw(self):
            state['contact'] = True

    doc.addPageTemplates([PageTemplate(id='cover', frames=[frame], onPage=cover, autoNextPageTemplate='inner'), PageTemplate(id='inner', frames=[frame], onPage=inner)])
    from reportlab.platypus import NextPageTemplate
    story = [NextPageTemplate('inner'), PageBreak()] + list(content) + [_ContactMarker(), PageBreak(), Spacer(1, 1)]
    doc.build(story)
    return buf.getvalue()
