"""Structural release check for the Four Muses module line."""
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "N1 Verte": ("modules/n1-verte-the-green-hour.md", "output/pdf/n1-verte-the-green-hour.pdf", "moon-wormwood"),
    "N2 Bleue": ("modules/n2-bleue-the-glass-road.md", "output/pdf/n2-bleue-the-glass-road.pdf", "glass fennel"),
    "N3 Crimson": ("modules/n3-crimson-the-thorn-feast.md", "output/pdf/n3-crimson-the-thorn-feast.pdf", "rose anise"),
    "N4 Detour": ("modules/n4-detour-the-last-road.md", "output/pdf/n4-detour-the-last-road.pdf", "wayfarer's balm"),
}
REQUIRED = ("run this first", "referee facts", "harvest", "factions", "finale", "playability checks", "price", "sister at the table", "bottle play")
TABLE_AIDS = {
    "N1 Verte": "fast room roster",
    "N2 Bleue": "crossing roster",
    "N3 Crimson": "guest roster",
    "N4 Detour": "endgame dashboard",
}

failed = []
for title, (source, pdf, herb) in MODULES.items():
    text = (ROOT / source).read_text().lower()
    missing = [term for term in REQUIRED if term not in text]
    if herb not in text:
        missing.append("named herb: " + herb)
    if text.count("clue") < 3:
        missing.append("at least three clue references")
    if TABLE_AIDS[title] not in text:
        missing.append("module-specific at-table roster")
    pages = len(PdfReader(str(ROOT / pdf)).pages)
    if pages < 6:
        missing.append("6-page print packet")
    if missing:
        failed.append(f"{title}: " + ", ".join(missing))
    else:
        print(f"PASS {title}: herb, procedures, clues, factions, finale, and {pages}-page packet")

if failed:
    raise SystemExit("\n".join(failed))
