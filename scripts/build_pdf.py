from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "nowheres-end-print-edition.pdf"
W, H = letter
M, BODY = 45, 8.65
INK, GREEN, GOLD, PARCHMENT = HexColor("#151515"), HexColor("#151515"), HexColor("#4d4d4d"), HexColor("#f4eddb")

def wrap(c, text, font, size, width):
    words, result, line = text.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if stringWidth(candidate, font, size) <= width: line = candidate
        else: result.append(line); line = word
    return result + ([line] if line else [])

def para(c, text, x, y, width, size=BODY, leading=10.6):
    c.setFont("Helvetica", size); c.setFillColor(INK)
    for line in wrap(c, text, "Helvetica", size, width): c.drawString(x, y, line); y -= leading
    return y

def chrome(c, title, page):
    c.setFillColor(PARCHMENT); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GREEN); c.setLineWidth(1); c.line(M, H-42, W-M, H-42); c.line(M, 34, W-M, 34)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 8); c.drawString(M, H-32, "N1: NOWHERE'S END"); c.drawRightString(W-M, H-32, title.upper())
    c.setFont("Helvetica", 8); c.drawCentredString(W/2, 22, str(page))

def section(c, title, page, blocks):
    chrome(c, title, page)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 16); c.drawCentredString(W/2, H-78, title.upper())
    c.setStrokeColor(INK); c.setLineWidth(.7); c.line(M, H-87, W-M, H-87)
    gutter, colw = 18, (W - 2*M - 18) / 2
    ys = [H-108, H-108]
    for idx, (label, text) in enumerate(blocks):
        col = idx % 2; x, y = M + col * (colw + gutter), ys[col]
        if label:
            c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 9); c.drawString(x, y, label.upper()); y -= 14
        y = para(c, text, x, y, colw) - 11
        ys[col] = y
    c.showPage()

def cover(c, art):
    # Original layout in the visual language of a compact, 1980s adventure
    # module: green field, yellow code flag, title block, inset action art,
    # and referee-facing product copy. No third-party trade dress or marks.
    green, yellow, cream = HexColor("#1f624c"), HexColor("#f1d35a"), HexColor("#fbf4dc")
    c.setFillColor(green); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(yellow); c.rect(0, H-85, 96, 85, fill=1, stroke=0)
    c.setFillColor(HexColor("#143d31")); c.setFont("Helvetica-Bold", 15); c.drawCentredString(42, H-32, "N1")
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(46, H-46, "A FANTASY")
    c.drawCentredString(46, H-55, "ADVENTURE")
    c.setFillColor(cream); c.setFont("Helvetica-Bold", 9); c.drawCentredString(W/2+26, H-27, "NOWHERE'S END  •  ADVENTURE MODULE N1")
    c.setFont("Times-Bold", 25); c.drawCentredString(W/2+26, H-56, "VERTE: THE GREEN HOUR")
    c.setFont("Helvetica-Bold", 7.5); c.drawCentredString(W/2+26, H-74, "FOR 4-6 CHARACTERS OF LEVELS 2-3")
    c.setFillColor(HexColor("#0b1914")); c.rect(49, 276, W-98, 382, fill=1, stroke=0)
    c.drawImage(art, 56, 283, width=W-112, height=368, preserveAspectRatio=False)
    c.setStrokeColor(yellow); c.setLineWidth(1.8); c.rect(49, 276, W-98, 382, fill=0, stroke=1)
    c.setFillColor(cream); c.setFont("Helvetica", 7.2)
    copy = (
        "When the Green Hour spills across the moor, four strangers follow an impossible road to an inn that has no name. "
        "Within waits Vermifuge, a sword made to drive a Dream-Wyrm from the world - and four bottled paths offered by the Muses of Nowhere's End."
    )
    y = 252
    for line in wrap(c, copy, "Helvetica", 7.2, W-88):
        c.drawCentredString(W/2, y, line); y -= 9
    c.setFillColor(HexColor("#143d31")); c.rect(0, 0, W, 102, fill=1, stroke=0)
    c.setStrokeColor(yellow); c.setLineWidth(.8); c.line(31, 91, W-31, 91)
    c.setFillColor(yellow); c.setFont("Helvetica-Bold", 9); c.drawCentredString(W/2, 69, "THE FOUR MUSES OF NOWHERE'S END")
    c.setFillColor(cream); c.setFont("Helvetica", 7.1); c.drawCentredString(W/2, 50, "VERTE  •  BLEUE  •  CRIMSON  •  DETOUR")
    c.setFont("Helvetica-Bold", 6.5); c.drawCentredString(W/2, 25, "N1  |  A COMPLETE FANTASY ADVENTURE  |  THE GREEN HOUR BEGINS HERE")
    c.showPage()

def map_page(c, title, page, svg, caption):
    chrome(c, title, page); c.setFillColor(INK); c.setFont("Helvetica-Bold", 16); c.drawCentredString(W/2, H-78, title.upper())
    drawing = svg2rlg(str(svg)); scale = min((W-2*M)/drawing.width, 520/drawing.height)
    drawing.scale(scale, scale); renderPDF.draw(drawing, c, M, 160)
    c.setFillColor(GOLD); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W/2, 125, caption)
    c.showPage()

def art_page(c, title, page, art, caption, text):
    chrome(c, title, page); c.setFillColor(INK); c.setFont("Helvetica-Bold", 16); c.drawCentredString(W/2, H-78, title.upper())
    c.drawImage(art, M, 285, width=W-2*M, height=345, preserveAspectRatio=True, anchor="c")
    c.setFillColor(GOLD); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W/2, 265, caption)
    para(c, text, M, 230, W-2*M); c.showPage()

def sister_page(c, art):
    chrome(c, "The sisters: Verde & Blue", 14); c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 22); c.drawString(M, H-78, "The sisters: Verde & Blue")
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 10); c.drawString(M, H-118, "VIRIDIENNE - VERTE")
    y = para(c, "Fern-clad, wormwood-scented, and devoted to revelation. She wants the Root exposed before it dies. Offer: reveal every glamour, secret door, and root-double for one turn. Price: ask the question you most avoid. Opposes Carmine's mercy when it conceals Vesper's guilt. Clue: the promise says bearing, not bleeding.", M, H-140, W-2*M)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 10); c.drawString(M, y-8, "AZURÉE - BLEUE")
    para(c, "River-voiced and crowned with frosted glass, she represents passage. She wants the road opened even if the inn fails. Offer: carry the party across one impossible boundary. Price: leave one safe place behind forever. Opposes Verte's demand to expose every truth before anyone leaves. Clue: the well reflects a champion carrying a sword but no body.", M, y-30, W-2*M)
    c.drawImage(art, 150, 150, width=312, height=250, preserveAspectRatio=True, anchor="c")
    c.setFillColor(GOLD); c.setFont("Helvetica-Oblique", 8.5); c.drawCentredString(W/2, 132, "The four sisters gather at the last pour.")
    c.showPage()

def back(c):
    c.setFillColor(HexColor("#18251e")); c.rect(0,0,W,H,fill=1,stroke=0); c.setFillColor(HexColor("#eadfbd"))
    c.setFont("Helvetica-Bold", 25); c.drawCentredString(W/2,H-135,"THE GREEN HOUR IS WAITING")
    c.setFont("Helvetica",11); c.drawCentredString(W/2,H-161,"A complete old-school fantasy adventure for 4-6 characters of 2nd-3rd level")
    c.setFont("Helvetica-Oblique",10); c.drawCentredString(W/2,90,"Nowhere's End  •  N1")
    c.save()

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True); c = Canvas(str(OUT), pagesize=letter, pageCompression=1)
    cover_art = ImageReader(str(ROOT/"assets/illustrations/nowheres-end-cover-inset.png")); cellar_art = ImageReader(str(ROOT/"assets/illustrations/cellar-emissary.png"))
    cover(c, cover_art)
    section(c,"Contents & use",2,[
        ("Contents","Player introduction 3; using this module 4; rules 5; the Green Hour 6; guest map 7; referee cellar 8; keys 9-11; cellar illustration 12; Vesper and Lark 13; the four sisters 14-15; creatures 16; Vermifuge and draughts 17; Wyrm protections 18; finale 19; handouts 20-21; referee reference 22; notes 23."),
        ("At the table","This is a complete old-school adventure for four to six 2nd- or 3rd-level characters. It uses ascending Armor Class, Hit Dice, morale, and saves, but can be adapted easily. The module is presented in reader order; print the player map and handouts separately if desired."),
        ("Credits","All adventure text, maps, and game mechanics are original. The four draught names are product-inspired references; confirm trademark and licensing permissions before commercial release.")])
    section(c,"The road opens",3,[
        ("Read aloud","The road sheds its ruts behind you. Ahead, a warm lamp burns above a door set in open moorland. The windows show a crowded common room, though no smoke rises from the chimney. Above the door is no name - only a small green moth circling a clock stopped one minute before midnight."),
        ("At the threshold","A woman in mourning silk smiles without surprise. Travelers, she says, you are precisely in time for the Green Hour. Do try not to promise anything. The party can see the common room, bar, gallery, kitchen door, and a padlocked cellar hatch. No road remains behind them."),
        ("First questions","Ask each character what brought them onto the moor, which guest they notice first, and whether they accept a drink. Put Nella near the fire, Lark near the bottles, and Vesper at the missing eighth place."),
        ("Things guests say","The clock has been wrong since the last traveler left. • A green drink makes a person ask dangerous questions. • The cellar door knows a name. • No one remembers arriving by the same road. A bard at the fire says every road has an end; this one misplaced its beginning.")])
    section(c,"Using this module",4,[
        ("Premise","Long ago the Court of Moths bound a Dream-Wyrm beneath this impossible inn. Vesper's compact renews that prison through one willing champion each century. Vermifuge can drive the Wyrm from its host; the four faerie sisters arrive to argue four paths through the bargain."),
        ("Play loop","Let the party question guests, name a draught, and choose allies before the thirteenth stroke. Then advance the Green Hour each exploration turn. Every major truth has three clues. At the Root-chamber, fighting, bargaining, sister concord, surrendering the blade, and escaping through Detour are all viable conclusions."),
        ("Immediate pressures","Nella is beginning to change; Lark demands Vermifuge; the road has disappeared. Do not wait for a passive party: the clock strikes thirteen after ten minutes in the inn."),
        ("Referee priorities","Offer a choice, clue, or cost every turn. State prices before a bargain binds. Let the party create plans the text did not predict; the Court respects literal cleverness, not a preferred solution.")])
    section(c,"Table rules",5,[
        ("Checks","Roll d20 and succeed on 12+; use 10+ for a sensible plan and 15+ for a difficult or dangerous one. A relevant class ability may succeed outright. One exploration turn is about ten minutes; searching, treating an injury, or navigating the casks consumes a turn."),
        ("Reaction & morale","For an undecided creature, roll 2d6: 2 hostile, 3-5 unfriendly, 6-8 uncertain, 9-11 favorable, 12 helpful. Check morale at half strength or when a leader falls; a result over morale means flee, bargain, or surrender."),
        ("Save conversion","Save vs. spells means magic, will, or mental effect; save vs. paralysis means restraint, body, or fortitude. Save as a level means that level's normal progression. Without saves, use a difficult check."),
        ("Clue discipline","Never gate progress behind a single roll. The portraits, well, sisters, Vesper's ledger, and Lark all reveal overlapping facts about the compact and Root."),
        ("Light & noise","Green lamps make hidden things visible but attract mothlings. Loud, unmetered music drives a swarm away for 1d6 turns. Fire harms roots but advances collapse; tell players this before they commit to it.")])
    section(c,"The Green Hour",6,[
        ("Thirteenth stroke","The clock chimes thirteen times. Every lamp burns green. Begin at Green Hour 1 and advance one step after each exploration turn."),
        ("1-3","At 1, glamours thin and the hatch opens. At 2, Nella becomes a root-double unless protected. At 3, the Court arrives; Lark presses for a decision and mothlings patrol."),
        ("4-6","At 4, the Root makes offers to isolated characters. At 5, the inn begins to fail; violence, fire, or broken casks collapse an exit. At 6, dawn presses at the windows: the Dream-Wyrm rises and takes two actions. Push the finale now."),
        ("Event check","Each turn, choose or roll: hidden route visible; mothlings arrive; a guest repeats a clue; the Root makes an offer; an impossible clock chimes; or an exit shifts."),
        ("Keep it fair","Reveal the next consequence before advancing the hour: a green lamp, a distant moth-cloud, or a groan below the floor. Escalation should narrow choices, never erase them.")])
    map_page(c,"Guest map of the inn",7,ROOT/"assets/maps/inn-player-map.svg","Player-facing: print or show this map without the referee map.")
    map_page(c,"Referee cellar",8,ROOT/"assets/maps/cellar-referee-map.svg","Tactical referee map: one square equals 5 feet; print at full page size.")
    section(c,"Keys 1-2",9,[
        ("1. Common room","Vesper serves ordinary food and refuses cellar talk until someone asks for a drink by color. deTour, a road-worn bard, tunes a three-string lute by the fire. Give his rumors in order after Green Hour advances: sword drives worm from heart; well remembers faces; no oath says champion must bleed. Nella dreams of a pearl-black eye beneath the floor."),
        ("2. Bar & hatch","Four bottles stand in a locked glass case, each holding three doses. A character may drink one dose whenever they can act; resolve its effect and price immediately. The Last Pour is optional and uses one dose from each chosen bottle. Vesper has the key; Lark has a silver duplicate. Behind it, d'Aniel's recipe card identifies every draught and reveals one non-potion Wyrm counter after a turn's study.")])
    section(c,"Keys 3-4",10,[
        ("3. Portrait gallery","Former keepers fade from their paintings. Behind the third portrait is the service stair. Touching a portrait yields one true answer but costs a minor memory until sunrise. The third keeper says: What is borne may be borne in a frame."),
        ("4. Kitchen","A copper automaton feeds arrivals and none who leave. It trades the brass cellar key for a recipe it has never tasted: sweetness with bitterness beneath, served cold and named for a road. The answer is Detour. Violence rings the dinner bell and attracts 1d4 mothlings each turn.")])
    section(c,"Keys 5-7",11,[
        ("5. Cask vault","Black casks make a maze. Only upside-down chalk arrows are honest. On a failed navigation check or every second turn here, 1d4 mothlings descend. The DETOUR cask contains the dry hidden passage."),
        ("6. Whispering well","The well holds silver moths, not water. It answers three questions: Dreams, first; the Wyrm, last. A bearer at the last stroke. Carry what is true in what is not flesh. A sincere gift produces the silver key if needed."),
        ("7. Root-chamber","White roots surround an iron chair holding Vermifuge. The root-heart is AC 14, 30 hp, immune to ordinary edged weapons; fire deals double damage but advances collapse. Removing the sword or destroying the heart breaks the ward and raises the Dream-Wyrm. At Green Hour 6 it gains a second action; use page 18.")])
    art_page(c,"Cellar of silver moths",12,cellar_art,"Lark-of-Ash carries the silver key through the cask vault.","The cask vault is a maze only while the party treats it as one. The upside-down arrows, Detour cask, and service stair all supply routes through it. Keep exploration moving: offer a choice, a clue, or a cost each turn.")
    section(c,"Vesper, Lark & companions",13,[
        ("Madame Vesper","AC 13; HD 4; hp 18; shadow lash +4 (1d6; target cannot cross a threshold next round); save as 4th-level magic-user; morale 8. She bargains before violence, protects the inn over individuals, and dissolves into shadow at 0 hp. She intended the bearer of Vermifuge as the Court's champion."),
        ("Lark-of-Ash","AC 14; HD 3; hp 13; Move 40/fly 60 as moth; thorn knife +3 (1d4) or glamour (save vs. spells or lose next action); save as 3rd-level thief; morale 10. Lark cannot knowingly speak a direct lie and wants the Root ended quietly."),
        ("deTour, bard","AC 12; HD 2; hp 8; dagger +1 (1d4); save as 2nd-level thief; morale 7. His surname distinguishes him from *Detour* the amber draught and Détournée the sister. Once each Green Hour, one loud round of lute music drives mothlings away for 1d6 turns."),
        ("d'Aniel, hedge-wizard","Absent, but present in stained notes and late reflections. He distilled the sisters' ancient gifts into the four draughts; he did not create them. Choose before play: dry-passage escapee with fifth formula; prisoner in well-reflection and substitute champion; or first root-double among guests.")])
    sister_page(c, ImageReader(str(ROOT/"assets/illustrations/four-sisters.png")))
    section(c,"The sisters: Red & Gold",15,[
        ("Carmine - Crimson","Rosehip-red, thorned, and devoted to desire. She wants Vesper to admit who the compact was meant to save. Offer: restore 2d6 hp to every willing creature in the room and reveal each one's strongest desire. Price: speak one true desire aloud. Opposes Detour's clever substitute if it lets Vesper evade remorse. If rejected, she names a desire aloud."),
        ("Detournée - Detour","Travel-stained gold and never in the same place twice. She represents the liberating wrong turn. Offer: open a route from the Root-chamber to a sincerely wished-for place. Price: something small but beloved travels the other way. Opposes Bleue's escape if it merely moves the prison onto a new road. If rejected, she misplaces a beloved small object. Clue: a painting, dreamer, or reflection can bear a burden without flesh."),
        ("Concord","If all four hear the compact, they can vote to interpret it. Earn a sister's vote by accepting her offer or acting on her value: reveal, free, desire, or deviate.")])
    section(c,"Creatures",16,[
        ("Mothling swarm","AC 12; HD 2; hp 9; Fly 30; cloud attack in a 10-foot space (1d4 and save vs. spells or lose fine sight for one turn); morale 7. Normal weapons deal half damage; fire deals double but risks collapse. Loud unmetered music drives them away for 1d6 turns."),
        ("Root-double","AC 12; HD 2; hp 10; root-hand +2 (1d6); morale 9. It knows memories through the prior dawn and speaks in its victim's voice. Showing it a cherished object makes it hesitate one round. Vermifuge kills it in one strike."),
        ("Pale Root","The Wyrm's exposed feeding tendril. At round end, restrain a creature within 20 feet (save vs. paralysis or 1d6 and held) or make an offer. At Green Hour 6 it acts twice. It is an environment with a heart, not a stationary punching bag.")])
    section(c,"Vermifuge & draughts",17,[
        ("Vermifuge","A black sword with a pale bone grip. It is potent against fey, plants, parasites, and bindings. Once each Green Hour, it cuts a magical bond, locked route, or root. Removing it breaks the ward. Against the Dream-Wyrm it deals 2d6; once its protections are stripped, a failed save vs. spells drives it below the moor for a generation."),
        ("Four draughts","Each bottle holds three doses and can be drunk whenever a character can act; resolve the effect and price immediately. d'Aniel distilled the sisters' gifts into Verte, Bleue, Crimson, and *Detour* as remedies against the Wyrm. Verte reveals concealed doors and glamours; Bleue crosses still water, mirrors, and reflections; Crimson restores vigor and reveals desire; *Detour* opens a wished-for route, then sends something valued to the old destination."),
        ("The Last Pour","An optional tavern ritual: two or more willing characters spend different doses. Missing cups may go to an NPC, portrait ghost, or a character taking two prices. In character, name a question, road, desire, or wrong turn; a player may veil or pass. The sisters call this ritual a vermifuge: it drives the Wyrm from the mind before it reaches the heart."),
        ("Saving boons","Each sincere drinker receives one use before dawn. Verte turns a failed glamour, charm, illusion, or Root-offer save into success. Bleue succeeds against restraint, traps, drowning, or being rooted. Crimson rerolls fear, poison, death, or parasitic vitality loss. Detour halves a curse or Root effect and places the drinker in the nearest plausible safe space."),
        ("No potion required","Once each: spend an action in green lamplight to speak a verifiable truth (Glamour ends for scene); press the silver key into an iron ring (Burrow ends until its next turn); name a cherished in-world memory and take 1 hp (Dread ends for you); shatter a mirror, shield, or still water surface (Escape ends for scene). The cups make these wins permanent.")])
    section(c,"The Wyrm's protections",18,[
        ("At its rising","The Dream-Wyrm rises when the sword leaves the chair or the Root-heart dies. AC 15; HD 6; hp 27; Move 20/burrow 20; bite +5 (2d6 and save vs. spells or dream one round); morale 11. It has two actions at Green Hour 6 or after three Root offers."),
        ("Four protections","Glamour creates false exits and a root-double each round; Verte removes it. Burrow lets it vanish below after a hit; Bleue removes it. Dread forces all witnesses to save or lose a round; Crimson removes it. Escape lets it flee through dream or mirror at 0 hp; Detour removes it."),
        ("Permanent victory","Spend the matching boon as a free declaration after its effect. With any protection left, reducing the Wyrm to 0 hp drives it down only until the next Green Hour. With all four removed, Vermifuge deals 2d6 and a failed save vs. spells sends it below the moor for a generation."),
        ("Root offers","Never compulsory: 1 show the route to Vermifuge; forget a loved face. 2 heal 2d6; grow a white flower. 3 reveal betrayal; lose a name. 4 restore a spell; the Root borrows its sound. 5 open a lock; next door leads wrong. 6 ask a portrait; it names you to the Court.")])
    section(c,"Finale",19,[
        ("1. Name the ward","When the sword leaves the chair or the Root-heart dies, reveal the Dream-Wyrm. Read the compact aloud. Before combat, the party may offer a portrait, reflection, dream, or non-mortal bearer through sister concord."),
        ("2. Run protections","Apply Glamour, Burrow, Dread, and Escape. A matching Last Pour boon removes its protection permanently. The non-potion counters on page 17 each take one action and suppress their matching protection only as stated."),
        ("3. Resolve Vermifuge","With any protection remaining, reducing the Wyrm to 0 hp drives it down only until the next Green Hour. With all four gone, Vermifuge deals 2d6 and a failed save vs. spells banishes it for a generation."),
        ("The hard-won cut","Banish the Wyrm for a generation. Vesper ages a century overnight and is finally free; the inn remains, altered but honest."),
        ("The renewed ward","Sister concord accepts a substitute bearer. The Court renews the prison and leaves a future favor owing; no living character is sacrificed."),
        ("The open road","Carry Vermifuge away. The inn vanishes at dawn and the Wyrm remains unresolved; roads later lead somewhere they should not.")])
    section(c,"Handout: the compact",20,[
        ("Give this to players","A mortal champion bearing the blade shall come freely to the Court of Moths at the last stroke of the Green Hour. In exchange, the road shall remain open, the inn shall endure, and no root shall drink the dreams of those beneath its roof."),
        ("Lark's riddle","A picture bears a face. A dream bears a sleeper. A mirror bears a traveler. Tell me, oath-breaker: which of these must bleed?")])
    section(c,"Handout: four paths",21,[
        ("Give this to players","Green reveals. Blue carries. Red desires. Gold strays. Four sisters, four cups, four ways to reach the end of the road."),
        ("Bottle labels","Verte: For seeing what green things hide. Bleue: For taking the road held in glass. Crimson: For hearing what the heart would have. Detour: For reaching the place you should not reach.")])
    section(c,"Referee reference",22,[
        ("Major truths","Breaking ward raises Wyrm: chair, Root-heart, sword. Dream-Wyrm feeds on dreams: Nella, well, offer. Bearing loophole: portrait, crown, sisters. Cellar route: portrait, automaton, arrows. Vermifuge drives Wyrm from host: sword, well, ledger."),
        ("Before play","Print the guest map and pages 20-21. Put the four draught names on cards. Keep the Green Hour track and accepted Root offers visible. Decide Nella's strongest mundane desire before the session begins."),
        ("After play","If the Root dies, decide what becomes of the road. If the Court is satisfied, choose a favor it will call in later. If the road opens, make its next impossible destination the next adventure.")])
    section(c,"Notes",23,[("At the table","Use this page for the exact wording of bargains, the sisters' votes, accepted Root offers, and the names stolen by mothlings.")] + [("","________________________________________________________________________________")] * 16)
    back(c)

if __name__ == "__main__": main()
