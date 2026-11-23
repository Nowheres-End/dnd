"""Build a four-page, US Letter cover proof for The Four Muses of Nowhere's End."""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "four-muses-cover-proof.pdf"
W, H = letter

MODULES = [
    {
        "code": "N1", "title": "VERTE: THE GREEN HOUR", "level": "FOR 4-6 CHARACTERS OF LEVELS 2-3",
        "field": "#1f624c", "accent": "#f1d35a", "art": "nowheres-end-cover-inset.png",
        "copy": "An impossible inn, a sleeping Dream-Wyrm, and the first bottle of wormwood revelation.",
    },
    {
        "code": "N2", "title": "BLEUE: THE GLASS ROAD", "level": "FOR 4-6 CHARACTERS OF LEVELS 3-4",
        "field": "#185c82", "accent": "#c7e7ee", "art": "n2-bleue-cover-inset.png",
        "copy": "Guide the erased across a reflected river before their shadows arrive ahead of them.",
    },
    {
        "code": "N3", "title": "CRIMSON: THE THORN FEAST", "level": "FOR 4-6 CHARACTERS OF LEVELS 4-5",
        "field": "#7d1e2b", "accent": "#f0c1b4", "art": "n3-crimson-cover-inset.png",
        "copy": "At a fey feast every desire is granted - until the host names its price at midnight.",
    },
    {
        "code": "N4", "title": "DETOUR: THE LAST ROAD", "level": "FOR 4-6 CHARACTERS OF LEVELS 5-6",
        "field": "#9b641d", "accent": "#f5d476", "art": "n4-detour-cover-inset.png",
        "copy": "Choose the road no one wants, carry Vermifuge, and send the Dream-Wyrm away for a generation.",
    },
]


def wrap(canvas, text, font, size, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if stringWidth(trial, font, size) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + ([line] if line else [])


def cover(c, module):
    field, accent, cream = HexColor(module["field"]), HexColor(module["accent"]), HexColor("#fbf4dc")
    c.setFillColor(field); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(accent); c.rect(0, H-85, 96, 85, fill=1, stroke=0)
    c.setFillColor(HexColor("#143d31")); c.setFont("Helvetica-Bold", 15); c.drawCentredString(42, H-32, module["code"])
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(46, H-46, "A FANTASY"); c.drawCentredString(46, H-55, "ADVENTURE")
    c.setFillColor(cream); c.setFont("Helvetica-Bold", 9); c.drawCentredString(W / 2 + 26, H-27, "NOWHERE'S END  •  ADVENTURE MODULE " + module["code"])
    c.setFont("Times-Bold", 25); c.drawCentredString(W / 2 + 26, H-56, module["title"])
    c.setFont("Helvetica-Bold", 7.5); c.drawCentredString(W / 2 + 26, H-74, module["level"])
    c.setFillColor(HexColor("#0b1914")); c.rect(49, 276, W-98, 382, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ROOT / "assets" / "illustrations" / module["art"])), 56, 283, width=W-112, height=368, preserveAspectRatio=False)
    c.setStrokeColor(accent); c.setLineWidth(1.8); c.rect(49, 276, W-98, 382, fill=0, stroke=1)
    c.setFillColor(cream); c.setFont("Helvetica", 7.4)
    y = 252
    for line in wrap(c, module["copy"], "Helvetica", 7.4, W-84):
        c.drawCentredString(W / 2, y, line); y -= 9
    c.setFillColor(HexColor("#143d31")); c.rect(0, 0, W, 102, fill=1, stroke=0)
    c.setStrokeColor(accent); c.setLineWidth(.8); c.line(31, 91, W-31, 91)
    c.setFillColor(accent); c.setFont("Helvetica-Bold", 9); c.drawCentredString(W / 2, 69, "THE FOUR MUSES OF NOWHERE'S END")
    c.setFillColor(cream); c.setFont("Helvetica", 7.1); c.drawCentredString(W / 2, 50, "VERTE  •  BLEUE  •  CRIMSON  •  DETOUR")
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(W / 2, 25, module["code"] + "  |  A COMPLETE FANTASY ADVENTURE  |  FIND THE HERB, FACE THE PRICE")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUT), pagesize=letter, pageCompression=1)
    for module in MODULES:
        cover(c, module)
    c.save()


if __name__ == "__main__":
    main()
