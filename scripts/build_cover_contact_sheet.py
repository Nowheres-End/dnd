"""Create a one-page comparison sheet from the four rendered A4 covers."""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "four-muses-a4-cover-sheet.pdf"
W, H = landscape(A4)
ITEMS = [
    ("N1", "VERTE: THE GREEN HOUR", "tmp/pdfs/cover-sheet/n1-1.png", "#1f624c"),
    ("N2", "BLEUE: THE GLASS ROAD", "tmp/pdfs/cover-sheet/n2-1.png", "#185c82"),
    ("N3", "CRIMSON: THE THORN FEAST", "tmp/pdfs/cover-sheet/n3-1.png", "#7d1e2b"),
    ("N4", "DETOUR: THE LAST ROAD", "tmp/pdfs/cover-sheet/n4-1.png", "#9b641d"),
]

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setFillColor(HexColor("#f5f0df")); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#153f35")); c.setFont("Times-Bold", 22); c.drawCentredString(W/2, H-30, "THE FOUR MUSES OF NOWHERE'S END")
    c.setFont("Helvetica-Bold", 8); c.drawCentredString(W/2, H-45, "A4 MODULE COVER COMPARISON")
    card_w, card_h = 172, 244
    positions = [(37, 278), (212, 278), (387, 278), (562, 278)]
    for (code, title, img, color), (x, y) in zip(ITEMS, positions):
        c.setFillColor(HexColor(color)); c.roundRect(x-4, y-4, card_w+8, card_h+29, 5, fill=1, stroke=0)
        c.drawImage(ImageReader(str(ROOT / img)), x, y, width=card_w, height=card_h, preserveAspectRatio=True, anchor="c")
        c.setFillColor(HexColor("#153f35")); c.setFont("Helvetica-Bold", 8); c.drawCentredString(x+card_w/2, y-20, code + "  " + title)
    c.setFillColor(HexColor("#153f35")); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W/2, 184, "Four colors. Four herbs. Four paths through the Green Hour.")
    c.setFillColor(HexColor("#333333")); c.setFont("Helvetica", 8); c.drawCentredString(W/2, 160, "Each A4 module includes a cover blurb, referee route map, dashboard, player handout, herb expedition, and multiple endings.")
    c.save()

if __name__ == "__main__":
    main()
