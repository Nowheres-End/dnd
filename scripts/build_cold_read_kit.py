"""Build the human cold-read kit for the Four Muses referee packets."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
W, H = A4
M = 48
INK = HexColor("#183f34")
PAPER = HexColor("#f8f1dd")
GOLD = HexColor("#bd9b38")


def wrap(text, font, size, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if stringWidth(trial, font, size) <= width:
            line = trial
        else:
            lines.append(line); line = word
    return lines + ([line] if line else [])


def chrome(c, page, title):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(1); c.line(M, H-40, W-M, H-40); c.line(M, 38, W-M, 38)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8); c.drawString(M, H-29, "THE FOUR MUSES OF NOWHERE'S END  |  COLD-READ KIT")
    c.drawRightString(W-M, H-29, title.upper()); c.setFont("Helvetica", 8); c.drawCentredString(W/2, 24, str(page))


def text(c, x, y, value, size=10, width=W-2*M, leading=13, font="Helvetica"):
    c.setFont(font, size)
    for line in wrap(value, font, size, width): c.drawString(x, y, line); y -= leading
    return y


def box(c, x, y, w, h, title, prompts):
    c.setFillColor(HexColor("#ffffff")); c.setStrokeColor(GOLD); c.setLineWidth(1); c.roundRect(x, y-h, w, h, 7, fill=1, stroke=1)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawString(x+12, y-18, title)
    yy = y-34
    c.setFillColor(HexColor("#202020")); c.setFont("Helvetica", 8.8)
    for prompt in prompts:
        for line in wrap("• " + prompt, "Helvetica", 8.8, w-24): c.drawString(x+12, yy, line); yy -= 11
        yy -= 3


def cover(c):
    c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H-110, W, 110, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Times-Bold", 29); c.drawCentredString(W/2, H-62, "THE FOUR MUSES")
    c.setFont("Helvetica-Bold", 11); c.drawCentredString(W/2, H-82, "HUMAN COLD-READ JUDGE KIT")
    c.setFillColor(PAPER); c.setFont("Times-Bold", 25); c.drawCentredString(W/2, H-205, "READ COLD. RUN HONESTLY.")
    c.setFont("Helvetica", 11); y = H-250
    intro = "This kit supports three independent referee reads: one newer DM, one experienced old-school DM, and one production/accessibility reviewer. Do not give judges the design notes or prior reviews. Give each judge the four A4 module PDFs and their matching scorecard."
    for line in wrap(intro, "Helvetica", 11, W-135): c.drawCentredString(W/2, y, line); y -= 16
    c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(100, H-360, W-100, H-360)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 12); c.drawCentredString(W/2, H-400, "SHARED PROTOCOL")
    steps = [
        "Open the assigned PDF with no briefing beyond its cover and player handout.",
        "Time the interval from opening the PDF to announcing the first player decision.",
        "Mark every moment you must invent an essential rule or search more than one page.",
        "Run or mentally simulate at least one escalation and one finale resolution.",
        "Return the completed scorecard with page references and a one-sentence verdict.",
    ]
    y = H-435; c.setFillColor(PAPER); c.setFont("Helvetica", 10.5)
    for i, step in enumerate(steps, 1):
        y = text(c, 94, y, f"{i}. {step}", 10.5, W-188, 15); y -= 5
    c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W/2, 90, "This is a fictional-game usability test. Do not use real alcohol or solicit personal disclosures.")
    c.showPage()


def scorecard(c, page, role, focus, checks):
    chrome(c, page, role)
    c.setFillColor(INK); c.setFont("Times-Bold", 23); c.drawString(M, H-84, role)
    c.setFont("Helvetica", 10); c.drawString(M, H-105, focus)
    c.setStrokeColor(GOLD); c.line(M, H-118, W-M, H-118)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawString(M, H-143, "JUDGE DETAILS")
    c.setFont("Helvetica", 9); c.drawString(M, H-160, "Name/alias: ______________________  Date: __________  Module(s): ______________________")
    c.drawString(M, H-177, "Rules system used: __________________  Actual run / read-through: __________________")
    top = H-207
    box(c, M, top, W-2*M, 168, "CORE MEASURES", [
        "Time to first player decision: ______ minutes (pass: 10 or fewer).",
        "Essential-rule page hunts: ______ (pass: 1 or fewer per scene).",
        "Potion effect, price, and dose count understood without referee pages: Yes / No.",
        "Finale resolved without inventing an unstated success rule: Yes / No.",
        "Would you run this unchanged? Yes / No / With revisions.",
    ])
    box(c, M, top-185, W-2*M, 170, "ROLE-SPECIFIC CHECKS", checks)
    box(c, M, top-370, W-2*M, 150, "EVIDENCE LOG", [
        "Page/section where you paused: ________________________________________________",
        "What was missing or misleading: _________________________________________________",
        "What made a decision easier: ____________________________________________________",
        "One change with the highest value: _______________________________________________",
    ])
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawString(M, 135, "ONE-SENTENCE VERDICT")
    c.setStrokeColor(HexColor("#777777")); c.line(M, 118, W-M, 118); c.line(M, 100, W-M, 100); c.line(M, 82, W-M, 82)
    c.showPage()


def main():
    out = ROOT / "output" / "pdf" / "four-muses-human-cold-read-kit.pdf"
    c = Canvas(str(out), pagesize=A4, pageCompression=1)
    cover(c)
    scorecard(c, 2, "JUDGE 1: NEWER DM", "You may know RPG basics, but do not rely on old-school habits or hidden conventions.", [
        "Could you identify the first scene, visible pressure, and next decision from pages 1-3?",
        "Were tracks, checks, saves, and monster actions explained enough to make a call?",
        "Which page made you feel uncertain, and what exact sentence would have helped?",
        "Could you run the final conflict after reading only the front aids and one body page?",
    ])
    scorecard(c, 3, "JUDGE 2: VETERAN DM", "Use your old-school experience, but flag every place a new referee would have to invent procedure.", [
        "Do clocks, factions, clues, and escalation make a complete operating loop?",
        "Do maps express routes, secrets, encounter positions, and alternatives at usable scale?",
        "Are dangers, saves, failure states, noncombat outcomes, and finales adjudicable as written?",
        "Flag loopholes, dead ends, and player choices that collapse the adventure's pressure.",
    ])
    scorecard(c, 4, "JUDGE 3: PRODUCTION & ACCESSIBILITY", "Review as a print-product reader who also understands actual game-table use.", [
        "At 100% print size, can you read maps, tracks, cards, footers, and two-column body pages under ordinary light?",
        "Does hierarchy make the next action findable in under ten seconds?",
        "Do labels and shapes preserve meaning without color? Are player and referee secrets cleanly separated?",
        "Does the package feel like an original classic fantasy module rather than an imitation?",
    ])
    c.save()


if __name__ == "__main__":
    main()
