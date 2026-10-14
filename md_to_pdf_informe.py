#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_pdf_informe.py
Converteix un Markdown gran (informe tecnic en catala) a un PDF amb portada,
index i estil propi. Fet amb reportlab + markdown (Platypus), que en Windows
no necessita cap DLL externa (a diferencia de weasyprint).

Motiu de triar reportlab: el document te 277 files de taula i 16 blocs de codi
amb estil; fpdf2 es torna fragil en aquesta combinacio.

Fonts: Segoe UI (text i negreta) i Consolas (codi, monoespaiada).
"""

import os
import re

import markdown
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

BASE = os.environ.get(
    "INFORME_BASE",
    os.path.dirname(os.path.abspath(__file__)),
)
SRC = os.path.join(BASE, "Informe-Sistema-BernatLab-RPi.md")
OUT = os.path.join(BASE, "Informe-Sistema-BernatLab-RPi.pdf")

# ---------------------------------------------------------------- tipografia
# El script ha de poder tornar a generar el PDF tant a Windows com a la RPi
# (es va descobrir que l'informe s'ha de poder refer a la propia maquina, no
# nomes des del portatil). Es proven candidats en ordre i s'usa el primer que
# existeixi; si no n'hi ha cap de les families preferides, es cau a
# DejaVu/liberation i, en ultim terme, a les fonts base de PDF.
FONT_DIRS = [
    r"C:\Windows\Fonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/msttcorefonts",
    "/usr/local/share/fonts",
]

FAMILIES = [
    # (nom logic, [noms de fitxer possibles])
    ("Body", ["segoeui.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "arial.ttf"]),
    ("Body-Bold", ["segoeuib.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "arialbd.ttf"]),
    ("Body-Italic", ["segoeuii.ttf", "DejaVuSans-Oblique.ttf", "LiberationSans-Italic.ttf", "ariali.ttf"]),
    ("Body-BoldItalic", ["segoeuiz.ttf", "DejaVuSans-BoldOblique.ttf",
                         "LiberationSans-BoldItalic.ttf", "arialbi.ttf"]),
    ("Mono", ["consola.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf", "cour.ttf"]),
    ("Mono-Bold", ["consolab.ttf", "DejaVuSansMono-Bold.ttf", "LiberationMono-Bold.ttf",
                   "courbd.ttf"]),
]


def find_font(candidates):
    for d in FONT_DIRS:
        for c in candidates:
            p = os.path.join(d, c)
            if os.path.exists(p):
                return p
    return None


# Fallback final: les fonts base del format PDF (Helvetica/Courier). Sempre hi
# son, no cal instal·lar res. A la RPi no hi ha CAP font TrueType (ni DejaVu):
# si no es contempla aquest cas, el script peta amb "Cannot open resource None".
BASE14 = {
    "Body": "Helvetica",
    "Body-Bold": "Helvetica-Bold",
    "Body-Italic": "Helvetica-Oblique",
    "Body-BoldItalic": "Helvetica-BoldOblique",
    "Mono": "Courier",
    "Mono-Bold": "Courier-Bold",
}

FONTS_USED = {}
for logical, cands in FAMILIES:
    p = find_font(cands)
    if p:
        pdfmetrics.registerFont(TTFont(logical, p))
        FONTS_USED[logical] = os.path.basename(p)
    else:
        # Les 14 fonts base del PDF (Helvetica, Courier...) ja venen
        # registrades de serie a reportlab: no s'han de registrar, nomes usar
        # el seu nom. Intentar-ho peta amb "'str' object has no attribute
        # 'fontName'".
        FONTS_USED[logical] = BASE14[logical] + " (base PDF)"

# Amb les fonts base no es pot registrar un TTF amb alias; es fa servir un
# diccionari d'alies que s'aplica als estils (vegeu _ff()).
FONT_ALIAS = {lg: (lg if lg in FONTS_USED and not FONTS_USED[lg].endswith("(base PDF)")
                   else BASE14[lg])
              for lg, _ in FAMILIES}


def _ff(logical):
    """Nom real de font a usar en un estil (pot ser una font base PDF)."""
    return FONT_ALIAS.get(logical, logical)

# ---------------------------------------------------------------- colors
NAVY = colors.HexColor("#12294a")
ACCENT = colors.HexColor("#1d6fb8")
ACCENT2 = colors.HexColor("#0f9d8a")
GREY = colors.HexColor("#5a6472")
LIGHT = colors.HexColor("#f2f5f9")
CODEBG = colors.HexColor("#f6f8fa")
CODEBORDER = colors.HexColor("#d8dee6")
ROWBG = colors.HexColor("#eef3f8")

# ---------------------------------------------------------------- styles
ss = getSampleStyleSheet()
S = {}
S["body"] = ParagraphStyle(
    "body", parent=ss["BodyText"], fontName=_ff("Body"), fontSize=9.4, leading=13.4,
    alignment=TA_JUSTIFY, textColor=colors.HexColor("#1c2430"), spaceAfter=4.2,
)
S["h1"] = ParagraphStyle(
    "h1", parent=ss["Heading1"], fontName=_ff("Body-Bold"), fontSize=17, leading=21,
    textColor=NAVY, spaceBefore=6, spaceAfter=8,
)
S["h2"] = ParagraphStyle(
    "h2", parent=ss["Heading2"], fontName=_ff("Body-Bold"), fontSize=13, leading=16.5,
    textColor=ACCENT, spaceBefore=13, spaceAfter=5,
)
S["h3"] = ParagraphStyle(
    "h3", parent=ss["Heading3"], fontName=_ff("Body-Bold"), fontSize=11, leading=14,
    textColor=NAVY, spaceBefore=9, spaceAfter=4,
)
S["h4"] = ParagraphStyle(
    "h4", parent=ss["Heading4"], fontName=_ff("Body-Bold"), fontSize=9.8, leading=12.5,
    textColor=ACCENT2, spaceBefore=7, spaceAfter=3,
)
S["bullet"] = ParagraphStyle(
    "bullet", parent=S["body"], leftIndent=11, bulletIndent=3, spaceAfter=2.6,
    alignment=TA_LEFT,
)
S["code"] = ParagraphStyle(
    "code", parent=ss["Code"], fontName=_ff("Mono"), fontSize=7.4, leading=9.6,
    textColor=colors.HexColor("#141b26"),
)
S["cell"] = ParagraphStyle(
    "cell", parent=S["body"], fontSize=7.9, leading=10.2, alignment=TA_LEFT, spaceAfter=0,
)
S["cellh"] = ParagraphStyle(
    "cellh", parent=S["cell"], fontName=_ff("Body-Bold"), textColor=colors.white,
)
S["quote"] = ParagraphStyle(
    "quote", parent=S["body"], leftIndent=12, rightIndent=8,
    textColor=colors.HexColor("#3d4654"), fontName=_ff("Body-Italic"), spaceAfter=5,
)
S["toc"] = ParagraphStyle(
    "toc", parent=S["body"], fontSize=9.2, leading=14.5, alignment=TA_LEFT, spaceAfter=0,
)

# ---------------------------------------------------------------- header/footer
PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 18 * mm, 18 * mm, 20 * mm, 17 * mm


def decorate(canv, doc):
    canv.saveState()
    # linea superior
    canv.setStrokeColor(ACCENT)
    canv.setLineWidth(1.1)
    canv.line(LM, PAGE_H - 12 * mm, PAGE_W - RM, PAGE_H - 12 * mm)
    canv.setFont(_ff("Body"), 7.4)
    canv.setFillColor(GREY)
    canv.drawString(LM, PAGE_H - 10.4 * mm, "Informe tecnic del sistema · BernatLab + Raspberry Pi hortosona")
    canv.drawRightString(PAGE_W - RM, PAGE_H - 10.4 * mm, "21 de setembre de 2026")
    # peu
    canv.setStrokeColor(colors.HexColor("#c9d3de"))
    canv.setLineWidth(0.5)
    canv.line(LM, 12.5 * mm, PAGE_W - RM, 12.5 * mm)
    canv.setFont(_ff("Body"), 7.6)
    canv.setFillColor(GREY)
    canv.drawString(LM, 9 * mm, "Document de lliurament per a desenvolupador")
    canv.drawRightString(PAGE_W - RM, 9 * mm, "pagina %d" % doc.page)
    canv.restoreState()


def first_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 86 * mm, PAGE_W, 86 * mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT2)
    canv.rect(0, PAGE_H - 89 * mm, PAGE_W, 3 * mm, stroke=0, fill=1)

    canv.setFillColor(colors.white)
    canv.setFont(_ff("Body"), 11)
    canv.drawString(LM, PAGE_H - 26 * mm, "DOCUMENTACIO TECNICA")

    canv.setFont(_ff("Body-Bold"), 30)
    canv.drawString(LM, PAGE_H - 44 * mm, "Informe del sistema")
    canv.setFont(_ff("Body"), 15)
    canv.setFillColor(colors.HexColor("#b8d4f0"))
    canv.drawString(LM, PAGE_H - 56 * mm, "BernatLab  ·  Raspberry Pi 4  ·  hortosona")
    canv.setFont(_ff("Body"), 9.4)
    canv.drawString(LM, PAGE_H - 68 * mm, "Estat real verificat sobre la maquina")
    canv.drawString(LM, PAGE_H - 75 * mm, "Adrecat a: desenvolupador/a que hagi de mantenir o continuar el sistema")
    canv.restoreState()


# ---------------------------------------------------------------- cover body
def cover_body():
    fl = []
    fl.append(Spacer(1, 92 * mm))
    fl.append(Paragraph("Que conte aquest informe", S["h2"]))
    fl.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceAfter=7))
    items = [
        ("1-3", "Resum executiu, maquinari, sistema operatiu i xarxa (Tailscale, SSH, Funnel)."),
        ("4-5", "Arquitectura: els quatre mecanismes d'execucio i el mapa complet de ports i serveis."),
        ("6", "Els projectes web propis, un per un, amb les seves APIs i particularitats."),
        ("7-8", "El repositori bernatlab (curs, llibre, CI, regles) i el RUNBOOK."),
        ("9", "IoT: la cadena meteorologica que funciona i el projecte LoRa que no."),
        ("10-11", "Backups (sistema v2) i notificacions per ntfy."),
        ("12", "Automatitzacions: les 23 tasques de cron."),
        ("13", "Seguretat: que esta be i quins deutes hi ha."),
        ("14-15", "Hort Osona, CyberLab i Maker Lab."),
        ("16", "Treball en curs, coses no acabades i feines obertes per ordre de rendibilitat."),
        ("17", "Guia practica per a qui arriba nou: comandes, regles i com validar que tot va be."),
        ("18-20", "Glossari, index de fitxers i nota final."),
    ]
    data = [
        [Paragraph("<b>%s</b>" % a, S["cell"]), Paragraph(b, S["cell"])] for a, b in items
    ]
    t = Table(data, colWidths=[16 * mm, None], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#dfe6ee")),
    ]))
    fl.append(t)
    fl.append(Spacer(1, 8 * mm))
    fl.append(Paragraph(
        "Avis important: aquest informe descriu l'ESTAT REAL de la maquina, comprovat executant-hi "
        "comandes. En dos punts contradiu la documentacio oficial del projecte (la memoria RAM i la "
        "IP de xarxa local, a la seccio 2), i aquestes contradiccions s'assenyalen expressament.",
        S["quote"]))
    fl.append(PageBreak())
    return fl


# ---------------------------------------------------------------- md -> html
def md_to_html(text):
    md = markdown.Markdown(extensions=["extra", "tables", "fenced_code", "sane_lists", "nl2br"])
    return md.convert(text)


def inline(txt):
    """Converteix el markdown enlinia (ja passat per markdown -> HTML) a marques
    que enten reportlab.

    Dos paranys que ha calgut resoldre:
      1. markdown ja ha convertit els accents greus a <code>...</code> i els
         asteriscs a <strong>/<em>. Si es deixen, l'escapament d'angles els
         imprimeix literals ("<code>") al PDF.
      2. El contingut d'un <code> pot portar asteriscs propis de la comanda
         (per exemple `*_state.json`), que markdown ha convertit a <em>. Si es
         processen despres, els asteriscs queden dins del bloc monoespaiat.
         Solucio: extreure els trossos de codi ABANS de tocar cap asterisc i
         tornar-los al final.
    """
    spans = []

    def keep(m):
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        inner = inner.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        spans.append(inner)
        return "\x00%d\x00" % (len(spans) - 1)

    txt = re.sub(r"<code>(.*?)</code>", keep, txt, flags=re.S)
    txt = re.sub(r"<strong>(.*?)</strong>", r"**\1**", txt, flags=re.S)
    txt = re.sub(r"<em>(.*?)</em>", r"*\1*", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

    txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt, flags=re.S)
    txt = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", txt)
    txt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", txt)

    def restore(m):
        s = spans[int(m.group(1))]
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return '<font face="%s" size="8.4">%s</font>' % (_ff("Mono"), s)

    return re.sub(r"\x00(\d+)\x00", restore, txt)


def split_table(rows):
    header = [inline(c) for c in rows[0]]
    body = [[inline(c) for c in r] for r in rows[2:]]
    return header, body


def make_table(header, body, avail):
    """header/body: llistes de tuples (text, atributs_de_la_cell).

    Es fan servir els atributs de `<td>` (per exemple `style="text-align: right"`)
    per detectar columnes numeriques i alinear-les a la dreta. I es reserven
    les columnes alineades a la dreta ABANS de repartir l'amplada, perque una
    columna numerica ampla no es mengi l'espai de les descripcions.
    """
    ncols = len(header)
    if ncols == 0:
        return None
    rows_txt = [[c[0] for c in header]] + [[c[0] for c in r] for r in body]
    rows_txt = [r + [""] * (ncols - len(r)) if len(r) < ncols else r[:ncols]
                for r in rows_txt]

    right = [False] * ncols
    for row in [header] + body:
        for j, (_t, attrs) in enumerate(row[:ncols]):
            if "text-align: right" in (attrs or ""):
                right[j] = True

    widths = None
    if ncols >= 2:
        plain = [[re.sub(r"<[^>]+>", "", c) for c in r] for r in rows_txt]
        widest = [max(len(r[j]) for r in plain) for j in range(ncols)]
        if any(right):
            # ample minim garantit per a les columnes numeriques (port, etc.)
            fixed = {j: 0.085 for j in range(ncols) if right[j]}
            left = 1.0 - sum(fixed.values())
            others = [j for j in range(ncols) if not right[j]]
            weights = [max(len(r[j]) for r in plain) ** 0.5 for j in others]
            tot = sum(weights) or 1.0
            widths = [0.0] * ncols
            for k, j in enumerate(others):
                widths[j] = left * weights[k] / tot
            for j in fixed:
                widths[j] = fixed[j]
            widths = [avail * w for w in widths]
        else:
            avg = sum(len(r[0]) for r in plain) / float(len(plain))
            last_avg = sum(len(r[-1]) for r in plain) / float(len(plain))
            if ncols >= 3 and avg <= 12 and last_avg > 45:
                w0 = 0.09
                wmid = (1.0 - w0) / 2.4 / (ncols - 2)
                wlast = 1.0 - w0 - wmid * (ncols - 2)
                widths = [avail * w0] + [avail * wmid] * (ncols - 2) + [avail * wlast]
            else:
                w0 = 0.17 if avg < 10 else (0.23 if avg < 18 else 0.29)
                rest = (1.0 - w0) / (ncols - 1)
                widths = [avail * w0] + [avail * rest] * (ncols - 1)

    cell_r = ParagraphStyle("cellr", parent=S["cell"], alignment=2)
    cellhr = ParagraphStyle("cellhr", parent=S["cellh"], alignment=2)
    data = []
    for i, row in enumerate(rows_txt):
        line = []
        for j, c in enumerate(row):
            if right[j]:
                st = cellhr if i == 0 else cell_r
            else:
                st = S["cellh"] if i == 0 else S["cell"]
            line.append(Paragraph(c, st))
        data.append(line)

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, CODEBORDER),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, NAVY),
    ]
    for i in range(1, len(rows_txt)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBG))
    t.setStyle(TableStyle(style))
    return t


def code_block(lines):
    txt = "\n".join(lines)
    # markdown ha escapat les entitats HTML; dins d'un bloc de codi s'han de
    # veure tal com son (si no, al PDF hi surt "&amp;" en lloc de "&").
    txt = (txt.replace("&lt;", "<").replace("&gt;", ">")
              .replace("&quot;", '"').replace("&#39;", "'").replace("&amp;", "&"))
    pre = Preformatted(txt, S["code"])
    t = Table([[pre]], colWidths=[PAGE_W - LM - RM], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("BOX", (0, 0), (-1, -1), 0.5, CODEBORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def build_flow(html):
    """Recorre l'HTML amb un escaner de blocs.

    S'havia fet abans línia a línia, però el tancament del bloc de codi pot
    venir com a '</code></pre>' a la mateixa línia, i el bloc no es tancava mai:
    la resta del document s'empassava dins d'un Preformatted de 17.501 punts
    d'alçada. Amb un escaner de blocs això no pot passar.
    """
    avail = PAGE_W - LM - RM
    flow = []
    pos = 0
    n = len(html)
    pat = re.compile(
        r"<pre>.*?</pre>" r"|<table>.*?</table>" r"|<h[1-4]>.*?</h[1-4]>"
        r"|<ul>.*?</ul>" r"|<ol>.*?</ol>" r"|<blockquote>.*?</blockquote>"
        r"|<hr\s*/?>",
        re.S,
    )
    buf = []

    def flush_par():
        if not buf:
            return
        for chunk in "".join(buf).split("<p>"):
            txt = re.sub(r"</?p>", "", chunk).strip()
            if txt and txt != "<p>":
                flow.append(Paragraph(inline(txt), S["body"]))
        buf.clear()

    for m in pat.finditer(html):
        between = html[pos:m.start()]
        if between.strip():
            buf.append(between)
        flush_par()
        blk = m.group(0)
        pos = m.end()

        if blk.startswith("<pre>"):
            inner = re.sub(r"^<pre><code[^>]*>", "", blk)
            inner = re.sub(r"</code></pre>$", "", inner)
            inner = re.sub(r"</pre>$", "", inner)
            lines = inner.split("\n")
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            flow.append(Spacer(1, 3))
            flow.append(code_block(lines))
            flow.append(Spacer(1, 5))
            continue

        if blk.startswith("<table>"):
            rows = []
            for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", blk, re.S):
                cells = re.findall(r"<t[dh]([^>]*)>(.*?)</t[dh]>", rm.group(1), re.S)
                if cells:
                    rows.append([(re.sub(r"\s+", " ", c[1]).strip(), c[0]) for c in cells])
            if rows:
                flow.append(Spacer(1, 3))
                head, body = rows[0], rows[1:]
                tb = make_table(head, body, avail)
                if tb is not None:
                    flow.append(tb)
                flow.append(Spacer(1, 6))
            continue

        mh = re.match(r"<h([1-4])>(.*?)</h\1>", blk, re.S)
        if mh:
            lvl = int(mh.group(1))
            txt = inline(re.sub(r"\s+", " ", mh.group(2)).strip())
            if lvl == 1:
                flow.append(CondPageBreak(40 * mm))
                flow.append(Spacer(1, 3))
                flow.append(Paragraph(txt, S["h1"]))
                flow.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT,
                                       spaceBefore=1, spaceAfter=8))
            elif lvl == 2:
                flow.append(CondPageBreak(28 * mm))
                flow.append(Paragraph(txt, S["h2"]))
                flow.append(HRFlowable(width="100%", thickness=0.6,
                                       color=colors.HexColor("#cfe0f0"), spaceAfter=4))
            elif lvl == 3:
                flow.append(CondPageBreak(20 * mm))
                flow.append(Paragraph(txt, S["h3"]))
            else:
                flow.append(Paragraph(txt, S["h4"]))
            continue

        if blk.startswith("<blockquote>"):
            inner = re.sub(r"^<blockquote>|</blockquote>$", "", blk)
            inner = re.sub(r"</p>\s*<p>", " ", inner)
            inner = re.sub(r"</?p>", " ", inner)
            inner = re.sub(r"\s+", " ", inner).strip()
            if inner:
                flow.append(Spacer(1, 2))
                flow.append(Paragraph(inline(inner), S["quote"]))
            continue

        if blk.startswith("<ul>") or blk.startswith("<ol>"):
            ordered = blk.startswith("<ol>")
            items = re.findall(r"<li>(.*?)</li>", blk, re.S)
            for k, it in enumerate(items, 1):
                t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", it)).strip()
                if not t:
                    continue
                flow.append(Paragraph(inline(t), S["bullet"],
                                      bulletText=("%d." % k) if ordered else "&bull;"))
            flow.append(Spacer(1, 4))
            continue

        # <hr>
        flow.append(Spacer(1, 4))
        flow.append(HRFlowable(width="100%", thickness=0.5,
                               color=colors.HexColor("#d5dee8"), spaceAfter=6))

    tail = html[pos:]
    if tail.strip():
        buf.append(tail)
    flush_par()
    return flow


# ---------------------------------------------------------------- TOC
def build_toc(html):
    heads = re.findall(r"<h2>(.*?)</h2>", html)
    fl = [Paragraph("Index", ParagraphStyle(
        "toct", parent=S["h1"], fontSize=22, leading=26, textColor=NAVY, spaceAfter=2))]
    fl.append(HRFlowable(width="100%", thickness=1.6, color=ACCENT, spaceAfter=10))
    intro = ("L'informe te 20 seccions. Les quatre primeres son les que cal llegir abans de tocar "
             "res; la 16 llista el que esta a mitges i la 17 es la guia practica.")
    fl.append(Paragraph(intro, S["body"]))
    fl.append(Spacer(1, 6))
    data = []
    for h in heads:
        m = re.match(r"^(\d+)\.\s*(.*)$", h)
        num, title = (m.group(1), m.group(2)) if m else ("", h)
        data.append([Paragraph("<b>%s</b>" % num, S["toc"]),
                     Paragraph(inline(title), S["toc"])])
    t = Table(data, colWidths=[12 * mm, None], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#e2e8f0")),
    ]))
    fl.append(t)
    fl.append(PageBreak())
    return fl


def main():
    text = open(SRC, encoding="utf-8").read()
    html = md_to_html(text)
    body = build_flow(html)

    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
        title="Informe tecnic del sistema BernatLab + Raspberry Pi hortosona",
        author="Bernat Mora Sanglas",
        subject="Documentacio tecnica de lliurament",
    )
    frame_cover = Frame(LM, BM, PAGE_W - LM - RM, PAGE_H - TM - BM, id="cover")
    frame_body = Frame(LM, BM, PAGE_W - LM - RM, PAGE_H - TM - BM, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover], onPage=first_page),
        PageTemplate(id="body", frames=[frame_body], onPage=decorate),
    ])

    story = []
    story.append(NextPageTemplate("body"))
    story.extend(cover_body())
    story.extend(build_toc(html))
    story.extend(body)
    doc.build(story)
    print("PDF:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
