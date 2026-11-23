"""Lay out the Four Muses manuscripts as practical A4 referee packets."""
from pathlib import Path
import re

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[1]
W, H = A4
M = 42
COL_GAP = 16
COL_W = (W - 2 * M - COL_GAP) / 2

MODULES = [
    ("N1", "Verte: The Green Hour", "n1-verte-the-green-hour.md", "n1-verte-the-green-hour.pdf", "nowheres-end-cover-inset.png", "cellar-referee-map.svg", "#1f624c", "#f1d35a"),
    ("N2", "Bleue: The Glass Road", "n2-bleue-the-glass-road.md", "n2-bleue-the-glass-road.pdf", "n2-bleue-cover-inset.png", "bleue-glass-road.svg", "#185c82", "#c7e7ee"),
    ("N3", "Crimson: The Thorn Feast", "n3-crimson-the-thorn-feast.md", "n3-crimson-the-thorn-feast.pdf", "n3-crimson-cover-inset.png", "crimson-thorn-hall.svg", "#7d1e2b", "#f0c1b4"),
    ("N4", "Detour: The Last Road", "n4-detour-the-last-road.md", "n4-detour-the-last-road.pdf", "n4-detour-cover-inset.png", "detour-last-road.svg", "#9b641d", "#f5d476"),
]

LEVELS = {"N1": "LEVELS 2-3", "N2": "LEVELS 3-4", "N3": "LEVELS 4-5", "N4": "LEVELS 5-6"}

PLAY_AIDS = {
    "N1": {
        "track": ["1 Hatch opens", "2 Nella doubles", "3 Lark demands key", "4 Roots close an exit", "5 Vesper offers compact", "6 Root's final offer"],
        "herb": "Moon-wormwood blooms when the party asks a feared question, frees a root-double, or gives a true secret and refuses the Root.",
        "ward": "INHALE a burned pinch: cancel one root, glamour, or doubling effect and reveal its source.",
        "dose": "VERTE: reveal concealed doors, glamours, and living roots for one exploration turn. Price: speak only in questions until rest.",
        "choices": "Harvest and leave; sever the feeding root; expose Vesper's secrecy; or take a stated bargain.",
        "blurb": "The road to Nowhere's End is gone, the inn clock strikes thirteen, and a root below the cellar is turning guests into doubles. Find moon-wormwood before the Green Hour closes. But the herb opens only to mercy or a question no one wants answered.",
        "handout": "The clock has struck thirteen. The road outside is now a hedge of silver moths. A woman at the bar says: No one needs to go below. No one needs to ask what is growing.",
        "rumors": ["The cellar door knows a name.", "A green drink makes people ask dangerous questions.", "The well remembers faces, not coins."]
        ,"muse": "VIRIDIENNE, the Green Sister: soft voice, silver moth veil, never answers an unasked question. Once per session she may reveal a concealed route after a character states a truth aloud."
        ,"pour": "GREEN HOUR POUR: When anyone drinks Verte, ask what they fear being noticed. They may answer, decline, or name a fictional equivalent. A truthful answer gives one clear sensory clue; declining still gives the dose's benefit."
        ,"route": ["START: common room; show Nella's moving shadow.", "LEADS: hatch, portraits, kitchen, or well - all reach below.", "CLIMAX: root-chamber; harvest, bargain, or sever."]
        ,"card": "Ask: What are you afraid will be noticed? Answer, pass, or name fiction. The dose always works."
    },
    "N2": {
        "track": ["1 Quiet", "2 Quiet", "3 Quiet", "4 Shadows speak", "5 Payment named", "6 Ferry leaves", "7 Reflections"],
        "herb": "Glass fennel blooms at the third crossing when a willing traveler leaves a true possession and walks on.",
        "ward": "STEEP AND SIP: protect one name, memory, or true possession from unseen reflective theft.",
        "dose": "BLEUE: cross still water, mirrors, or one impossible boundary. Price: your reflection acts one beat late until dawn.",
        "choices": "Free Bellwether; keep the road with Elian as ferryman; or rewrite the toll through public memory and confession.",
        "blurb": "Bellwether has vanished from every map except the reflection in its well. Guide its missing people across a river with no water, bargain with a courteous Ferryman, and harvest glass fennel where a traveler leaves something true behind.",
        "handout": "The dry River Sel reflects a night sky too deep to be real. In that water, the missing people of Bellwether walk east. No one leaves a mark.",
        "rumors": ["The road eats names.", "The ferry is always on time.", "The herb grows where the hand opens."]
        ,"muse": "AZURÉE, the Blue Sister: blue-glass eyes, wet boots, and a precise memory for every name. Once per session she names a fair crossing price before the party commits."
        ,"pour": "BLUE POUR: When anyone drinks Bleue, ask what true possession their reflection envies. The player defines it or passes. In either case, the late reflection points toward one honest crossing."
        ,"route": ["START: Bellwether; show the well and missing nameplates.", "CROSS: ford, reed gate, and ferry - state a price at each.", "CLIMAX: name-house; return names, keep road, or rewrite toll."]
        ,"card": "Ask: What true possession does your reflection envy? Answer, pass, or invent it. The dose always works."
    },
    "N3": {
        "track": ["1 Feast flatters", "2 Feast flatters", "3 Wishes begin", "4 Duke isolates", "5 Masks fuse", "6 Duke collects"],
        "herb": "Rose anise blooms in the heart-garden when a guest names a desire and refuses the Duke's easy version of it.",
        "ward": "CHEW ONE PETAL: cancel one rose-mark, thorn restraint, or social compulsion after naming a boundary.",
        "dose": "CRIMSON: restore 2d6 hp or hear a creature's strongest desire. Price: a red flower blooms where you next sleep.",
        "choices": "Public accounting; steal the heart-stone; or write a better bargain with an explicit future service.",
        "blurb": "The Briar Duke grants every guest the desire they dare not name - then calls in the price at midnight. Explore a thorned feast, expose the bargains made in private, and win rose anise by refusing the easy version of a wish.",
        "handout": "Your invitation bears a wax rose and a sentence in your own hand: Tonight, you may ask for what you truly want.",
        "rumors": ["The Duke never forces a signature.", "Every mask remembers its owner.", "A thorn cannot bind a wish named aloud."]
        ,"muse": "CARMINE, the Red Sister: red gloves, rose-thorn halo, and a laugh that never mocks a refusal. Once per session she lets a character state the price of a bargain before hearing its reward."
        ,"scene": "Choose room + guest + toast/dance/gift/refusal. Then resolve, show a consequence, and advance Midnight. Heat 1: rival; Heat 2: Duke learns a detail; Heat 3: mask fuses. Thorn token: refuse without Heat."
        ,"pour": "RED POUR: When anyone drinks Crimson, ask what desire they will name without demanding it be fulfilled. They may pass. Naming one gives a red witness; a pass still grants the potion effect."
        ,"route": ["START: gate; give each character an invitation token.", "SCENE: choose room, guest, and etiquette move; then advance Midnight.", "CLIMAX: high table; account, steal the heart, or make a better bargain."]
        ,"card": "Ask: What desire will you name without demanding it be fulfilled? Answer or pass. The dose always works."
    },
    "N4": {
        "track": ["1 Sign", "2 Sign", "3 Personal offer", "4 Detour choice", "5 Dream-copy", "6 Delay/fight", "7 Two actions", "8 Threshold reached"],
        "herb": "Wayfarer's balm grows at the unwanted mile after the party refuses a shortcut that would genuinely help them.",
        "ward": "BREW AND DRINK: cancel one Wyrm threshold, forced road move, or road-curse; leave a breadcrumb.",
        "dose": "DETOUR: turn a failed curse or road/Wyrm save into partial success. Price: a small valued thing is displaced behind you.",
        "choices": "Banish it; bind it into a non-mortal bearer; exile it down an impossible road; or replace the old bargain.",
        "blurb": "Every signpost offers a road to somewhere the party longs to reach. Every shortcut teaches the Dream-Wyrm a way home. Refuse the helpful road, find wayfarer's balm at the unwanted mile, and choose how the last road ends.",
        "handout": "At the crossroads, every sign bears your handwriting. One points home. One points to what you failed to save. The third points away from both.",
        "rumors": ["The road is not the promise; the choosing is.", "A reflection can carry more than a body.", "The herb grows where no one wants to go."]
        ,"muse": "DÉTOURNÉE, the Gold Sister: road-dust cloak, a signpost staff, and a smile for the inconvenient road. Once per session she identifies the safest costly detour."
        ,"pour": "GOLD POUR: When anyone drinks Detour, ask what small valued thing they are prepared to leave behind. They may pass. Whatever the answer, show where the displaced thing can later be recovered."
        ,"route": ["START: crossroads; write the desired destinations where all can see.", "ROAD: show shortcut, honest detour, and Wyrm cost before every choice.", "CLIMAX: last road; cross off protections, then strike, bind, exile, or bargain."]
        ,"card": "Ask: What small valued thing are you prepared to leave behind? Answer or pass. The dose always works."
        ,"protections": ["GLAMOUR: first attack misses", "BURROW: vanishes after damage", "DREAD: dream lash +2", "ESCAPE: moves after every hit"]
    },
}


def wrap(text, font, size, width):
    words, out, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, font, size) <= width:
            line = test
        else:
            out.append(line)
            line = word
    return out + ([line] if line else [])


def cover(c, code, title, art_name, field, accent):
    field, accent, cream, ink = HexColor(field), HexColor(accent), HexColor("#fbf4dc"), HexColor("#171d19")
    # Original period-module grammar: information-heavy cream header, code flag,
    # framed scene, descriptive copy, and a color-field publisher band.
    c.setFillColor(cream); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(field); c.rect(0, H-34, W, 34, fill=1, stroke=0)
    c.setFillColor(field); c.rect(0, H-150, 116, 116, fill=1, stroke=0)
    c.setStrokeColor(ink); c.setLineWidth(1.2); c.rect(12, H-138, 92, 92, fill=0, stroke=1)
    c.setFillColor(accent); c.setFont("Helvetica-Bold", 28); c.drawCentredString(58, H-83, code)
    c.setFont("Helvetica-Bold", 6.2); c.drawCentredString(58, H-104, "FANTASY ADVENTURE")
    c.setFillColor(cream); c.setFont("Helvetica-Bold", 8); c.drawString(132, H-59, "NOWHERE'S END ADVENTURE MODULE")
    c.setFillColor(ink); c.setFont("Times-Bold", 23); c.drawString(132, H-91, title.upper())
    c.setFont("Helvetica-Bold", 8); c.drawString(134, H-108, "FOR 4-6 CHARACTERS  |  " + LEVELS[code])
    c.setFillColor(HexColor("#0b1914")); c.rect(49, 328, W-98, 300, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ROOT / "assets" / "illustrations" / art_name)), 56, 335, width=W-112, height=286, preserveAspectRatio=False)
    c.setStrokeColor(field); c.setLineWidth(3); c.rect(49, 328, W-98, 300, fill=0, stroke=1)
    c.setFillColor(ink); c.setFont("Helvetica-Bold", 8.5); c.drawString(54, 303, "AN ORIGINAL FANTASY ADVENTURE")
    c.setFont("Helvetica", 8.2); y = 289
    for line in wrap(PLAY_AIDS[code]["blurb"], "Helvetica", 8.2, W-108):
        c.drawString(54, y, line); y -= 11
    c.setStrokeColor(HexColor("#92866a")); c.setLineWidth(.6); c.line(54, 228, W-54, 228)
    c.setFillColor(ink); c.setFont("Helvetica-Bold", 7.2); c.drawString(54, 211, "IN THIS MODULE:")
    c.setFont("Helvetica", 7.2)
    contents = {"N1": "A timed inn mystery, a root-bound cellar, Vermifuge, and moon-wormwood.", "N2": "A vanished village, three impossible crossings, a ferryman, and glass fennel.", "N3": "A thorned feast, masks of desire, an accounting, and rose anise.", "N4": "A road-crawl, the Dream-Wyrm, four protections, and wayfarer's balm."}[code]
    cy = 198
    for line in wrap(contents, "Helvetica", 7.2, W-108):
        c.drawString(54, cy, line); cy -= 9
    c.setFillColor(field); c.rect(0, 0, W, 78, fill=1, stroke=0)
    c.setStrokeColor(accent); c.setLineWidth(1); c.line(30, 64, W-30, 64)
    c.setFillColor(cream); c.setFont("Helvetica-Bold", 9); c.drawCentredString(W/2, 44, "THE FOUR MUSES OF NOWHERE'S END")
    c.setFont("Helvetica", 7); c.drawCentredString(W/2, 27, "FIND THE HERB  •  FACE THE PRICE  •  CHOOSE THE ROAD")
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(W/2, 11, code + "  |  " + LEVELS[code] + "  |  COMPLETE ADVENTURE")
    c.showPage()


def chrome(c, code, title, page, field):
    c.setFillColor(HexColor("#f5f0df")); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(HexColor(field)); c.setLineWidth(1); c.line(M, H-38, W-M, H-38); c.line(M, 33, W-M, 33)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 7.5); c.drawString(M, H-28, code + ": " + title.upper()); c.drawRightString(W-M, H-28, "REFEREE'S COPY")
    c.setFont("Helvetica", 8); c.drawCentredString(W/2, 21, str(page))


def map_page(c, code, title, map_name, field):
    chrome(c, code, title, 2, field)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 17); c.drawCentredString(W/2, H-78, "REFEREE ROUTE MAP")
    drawing = svg2rlg(str(ROOT / "assets" / "maps" / map_name))
    scale = min((W - 2*M) / drawing.width, 430 / drawing.height)
    drawing.scale(scale, scale); renderPDF.draw(drawing, c, (W - drawing.width * scale)/2, 175)
    aid = PLAY_AIDS[code]
    c.setFillColor(HexColor("#ffffff")); c.setStrokeColor(HexColor(field)); c.setLineWidth(1)
    c.roundRect(70, 615, W-140, 78, 6, fill=1, stroke=1)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 8); c.drawString(82, 677, "RUN THE MAP")
    c.setFillColor(HexColor("#202020")); c.setFont("Helvetica", 7.4)
    ry = 663
    for step in aid["route"]:
        for line in wrap("• " + step, "Helvetica", 7.4, W-164):
            c.drawString(82, ry, line); ry -= 9
        ry -= 1
    if code == "N1":
        img = ROOT / "assets" / "illustrations" / "vermifuge-sword-plate-v3-double-dragon.png"
        c.setFillColor(HexColor("#0b1914")); c.rect(W-112, 704, 52, 58, fill=1, stroke=0)
        c.drawImage(ImageReader(str(img)), W-110, 706, width=48, height=54, preserveAspectRatio=True, anchor='c')
        c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 5.6); c.drawRightString(W-61, 696, "VERMIFUGE")
    c.setFillColor(HexColor("#242424")); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W/2, 130, "Keep this map behind the screen. Read the visible route and price before every choice.")
    c.setFont("Helvetica", 7.4); c.drawCentredString(W/2, 112, "Rules key: AC, HD, and morale are optional d20-style shorthand; elsewhere, use comparable opposition and test only uncertain danger.")
    c.showPage()


def play_aids(c, code, title, field, accent):
    aid, cream = PLAY_AIDS[code], HexColor("#f5f0df")
    chrome(c, code, title, 3, field)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 17); c.drawCentredString(W/2, H-78, "REFEREE DASHBOARD")
    x, y, width = M, H-113, W-2*M
    def box(label, body, height):
        nonlocal y
        c.setFillColor(HexColor("#ffffff")); c.setStrokeColor(HexColor(accent)); c.setLineWidth(1); c.roundRect(x, y-height, width, height, 6, fill=1, stroke=1)
        c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 9); c.drawString(x+12, y-17, label)
        c.setFillColor(HexColor("#1b1b1b")); c.setFont("Helvetica", 8.4); ty = y-32
        for line in wrap(body, "Helvetica", 8.4, width-24): c.drawString(x+12, ty, line); ty -= 10
        y -= height + 10
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 10); c.drawString(x, y, "ESCALATION TRACK")
    y -= 15
    count = len(aid["track"])
    for index, item in enumerate(aid["track"], 1):
        slot = width/count; px = x + (index-1) * slot; c.setFillColor(HexColor(field)); c.circle(px+12, y-13, 10, fill=1, stroke=0)
        c.setFillColor(cream); c.setFont("Helvetica-Bold", 8); c.drawCentredString(px+18, y-16, str(index))
        c.setFillColor(HexColor("#202020")); c.setFont("Helvetica", 6.5)
        for li, line in enumerate(wrap(item, "Helvetica", 6.5, slot-5)[:3]): c.drawCentredString(px+slot/2, y-36-li*8, line)
    y -= 67
    if code == "N4":
        c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 8); c.drawString(x, y, "WYRM PROTECTIONS - CROSS OFF WHEN DISABLED / BOTTLE USED")
        y -= 13
        for index, item in enumerate(aid["protections"]):
            bx = x + index*(width/4)
            c.setStrokeColor(HexColor(field)); c.setLineWidth(1); c.rect(bx, y-20, 11, 11, fill=0, stroke=1)
            c.setFillColor(HexColor("#202020")); c.setFont("Helvetica", 6.5)
            for li, line in enumerate(wrap(item, "Helvetica", 6.5, width/4-18)[:2]): c.drawString(bx+16, y-10-li*7, line)
        y -= 30
    box("HERB HARVEST + PROTECTIVE DOSE", aid["herb"] + " Fresh dose: " + aid["ward"], 88)
    box("POTION REWARD", aid["dose"], 69)
    box("FEAST SCENE" if code == "N3" else "MUSE AT TABLE", aid.get("scene", aid["muse"]), 78)
    box("POURING MOMENT", aid["pour"], 78)
    box("FINALE MENU", aid["choices"], 58)
    c.setFillColor(HexColor("#353535")); c.setFont("Helvetica-Oblique", 7.5); c.drawCentredString(W/2, 70, "State a price before a bargain binds. Failed checks complicate; they never erase the next clue or route. D20 default: hard check = DC 15.")
    c.showPage()


def player_handout(c, code, title, field, accent):
    aid, cream = PLAY_AIDS[code], HexColor("#fbf4dc")
    c.setFillColor(cream); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(HexColor(field)); c.setLineWidth(4); c.rect(28, 28, W-56, H-56, fill=0, stroke=1)
    c.setStrokeColor(HexColor(accent)); c.setLineWidth(.8); c.rect(38, 38, W-76, H-76, fill=0, stroke=1)
    c.setFillColor(HexColor(field)); c.setFont("Times-Bold", 23); c.drawCentredString(W/2, H-115, "A NOTE FOR TRAVELERS")
    c.setFont("Helvetica-Bold", 9); c.drawCentredString(W/2, H-138, "NOWHERE'S END  •  " + code + "  •  PLAYER HANDOUT")
    c.setFillColor(HexColor("#242424")); c.setFont("Times-Italic", 14)
    y = H-205
    for line in wrap(aid["handout"], "Times-Italic", 14, W-150): c.drawCentredString(W/2, y, line); y -= 21
    c.setStrokeColor(HexColor(accent)); c.setLineWidth(1); c.line(100, y-15, W-100, y-15)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 12); c.drawCentredString(W/2, y-55, "THINGS PEOPLE SAY")
    y -= 95
    c.setFillColor(HexColor("#242424")); c.setFont("Helvetica", 11)
    for rumor in aid["rumors"]:
        for line in wrap("• " + rumor, "Helvetica", 11, W-170): c.drawCentredString(W/2, y, line); y -= 20
        y -= 13
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 11); c.drawCentredString(W/2, 244, "CUT-OUT BOTTLE CARD")
    cx, cy, cw, ch = 82, 105, W-164, 122
    c.setFillColor(HexColor("#ffffff")); c.setStrokeColor(HexColor(field)); c.setLineWidth(1.2); c.roundRect(cx, cy, cw, ch, 7, fill=1, stroke=1)
    c.setFillColor(HexColor(field)); c.setFont("Times-Bold", 15); c.drawCentredString(W/2, cy+98, code + " DRAUGHT")
    c.setFillColor(HexColor("#242424")); c.setFont("Helvetica", 8.7)
    py = cy+79
    for line in wrap(aid["dose"], "Helvetica", 8.7, cw-28): c.drawCentredString(W/2, py, line); py -= 11
    c.setFont("Helvetica-Oblique", 8.3)
    for line in wrap(aid["card"], "Helvetica-Oblique", 8.3, cw-28): c.drawCentredString(W/2, py-4, line); py -= 10
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", 7.5); c.drawString(cx+15, cy+16, "DOSES")
    for n in range(3):
        c.setStrokeColor(HexColor(field)); c.setLineWidth(1.2); c.circle(cx+67+n*31, cy+18, 9, fill=0, stroke=1)
    c.setFillColor(HexColor(field)); c.setFont("Helvetica-Oblique", 8); c.drawCentredString(W/2, 78, "Cut along the card edge if desired. All potion choices are fictional; the magical effect never depends on disclosure.")
    c.showPage()


def blocks(md):
    result, paragraph, table = [], [], []
    def flush():
        nonlocal paragraph, table
        if paragraph:
            result.append(("p", " ".join(paragraph))); paragraph = []
        if table:
            result.append(("t", table)); table = []
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            flush(); continue
        if line.startswith("#"):
            flush(); result.append(("h", re.sub(r"^#+\s*", "", line))); continue
        if line.startswith("|"):
            if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
                continue
            table.append(line.replace("|", " • ").strip(" •")); continue
        if line.startswith("-") or re.match(r"^\d+\.\s", line):
            flush(); result.append(("b", re.sub(r"^(-|\d+\.)\s*", "", line).replace("**", "").replace("*", ""))); continue
        paragraph.append(line.replace("**", "").replace("*", ""))
    flush()
    return result


def body(c, code, title, field, md):
    page, col, y = 5, 0, H-62
    chrome(c, code, title, page, field)
    def advance():
        nonlocal page, col, y
        if col == 0:
            col, y = 1, H-62
        else:
            c.showPage(); page += 1; chrome(c, code, title, page, field); col, y = 0, H-62
    def ensure(height):
        nonlocal y
        if y - height < 48:
            advance()
    for kind, value in blocks(md):
        if kind == "h":
            size = 15 if value.startswith("N") else 10
            ensure(size + 15); x = M + col * (COL_W + COL_GAP); c.setFillColor(HexColor(field)); c.setFont("Helvetica-Bold", size)
            c.drawString(x, y, value.upper()); y -= size + 7
        elif kind == "b":
            lines = wrap("• " + value, "Helvetica", 9.0, COL_W)
            ensure(len(lines)*10.8 + 7); x = M + col * (COL_W + COL_GAP); c.setFillColor(HexColor("#181818")); c.setFont("Helvetica", 9.0)
            for line in lines: c.drawString(x, y, line); y -= 10.8
            y -= 4
        elif kind == "t":
            for row in value:
                lines = wrap(row, "Helvetica", 8.2, COL_W)
                ensure(len(lines)*9.5 + 5); x = M + col * (COL_W + COL_GAP); c.setFillColor(HexColor("#303030")); c.setFont("Helvetica", 8.2)
                for line in lines: c.drawString(x, y, line); y -= 9.5
                y -= 2
            y -= 4
        else:
            lines = wrap(value, "Helvetica", 9.2, COL_W)
            ensure(len(lines)*11.2 + 8); x = M + col * (COL_W + COL_GAP); c.setFillColor(HexColor("#161616")); c.setFont("Helvetica", 9.2)
            for line in lines: c.drawString(x, y, line); y -= 11.2
            y -= 5
    c.showPage()


def main():
    outdir = ROOT / "output" / "pdf"; outdir.mkdir(parents=True, exist_ok=True)
    for code, title, source, output, art, map_name, field, accent in MODULES:
        c = Canvas(str(outdir / output), pagesize=A4, pageCompression=1)
        cover(c, code, title, art, field, accent)
        map_page(c, code, title, map_name, field)
        play_aids(c, code, title, field, accent)
        player_handout(c, code, title, field, accent)
        body(c, code, title, field, (ROOT / "modules" / source).read_text())
        c.save()


if __name__ == "__main__":
    main()
