# The Four Muses of Nowhere's End

An original four-module fantasy adventure line set at the edge of the Green
Hour. It uses concise old-school procedures with d20-compatible AC, HD, morale,
and save shorthand; translate those terms to a table's own rules where needed.
The current playable booklet is
**N1: Verte - The Green Hour**.

## Premise

At twilight, a road that should not exist opens beyond the last tavern. It
leads to **Nowhere's End**, a waystation held in place by bargains with the
fair folk. Its cellar protects four impossible draughts and a sleeping sword:
**Vermifuge**. When the Green Hour begins lasting until dawn, the characters
must decide who gets the sword, who drinks the last potion, and whether the
road will ever close.

## Start here

- [Adventure overview](adventure/00-overview.md)
- [Player introduction](adventure/01-player-introduction.md)
- [Keyed locations](adventure/02-keyed-locations.md)
- [Creatures and NPCs](adventure/03-creatures-and-npcs.md)
- [Treasures and potions](adventure/04-treasure-and-potions.md)
- [Referee procedures](adventure/05-referee-procedures.md)
- [Four-Muse series bible](series/00-four-muses-series.md)
- [N1: Verte - The Green Hour](modules/n1-verte-the-green-hour.md)
- [N2: Bleue - The Glass Road](modules/n2-bleue-the-glass-road.md)
- [N3: Crimson - The Thorn Feast](modules/n3-crimson-the-thorn-feast.md)
- [N4: Detour - The Last Road](modules/n4-detour-the-last-road.md)

## Editorial approach

The tone is inspired by early tabletop fantasy modules: evocative locations,
dangerous exploration, terse referee-facing keys, faction choices, and
consequences that outlast the dungeon. It does not reproduce any particular
game text or ruleset.

## Product-inspired potion names

The potion collection is inspired by the public presentation of Nowhere's End
Absinthe (Verte, Bleue, Crimson, and Detour), including its botanical and
Green Hour themes. The in-game effects are original and are not beverage or
health advice. Confirm any product, trademark, or licensing permissions before
commercial publication.

## Repository layout

```text
adventure/       Playable manuscript, organized in running order
assets/          Maps, art, and layout assets (add originals here)
references/      Research notes and source-attribution ledger
LICENSE           CC BY-NC-SA 4.0 draft license
```

## Development

This repository deliberately uses Markdown so the adventure can be revised in
plain text and later laid out in the tool of your choice. Keep player-facing
material separate from referee secrets, and record externally sourced facts in
`references/`.

## Print edition

The intended physical edition is an **8.5 × 11 in US Letter, saddle-stitched
booklet**. The production brief, pagination plan, and preflight list live in
[`publishing/`](publishing/). The current manuscript plan targets a 20-page
booklet (including covers): one folded-and-stapled signature, printed
double-sided and imposed as spreads.

## PDF and page-turning proof

The current print edition is [nowheres-end-print-edition.pdf](output/pdf/nowheres-end-print-edition.pdf).
It contains 24 US Letter pages in reader order; give this PDF to the printer
unless it asks for imposed spreads.

The companion **A4 portrait** referee PDFs are available as [N1 Verte](output/pdf/n1-verte-the-green-hour.pdf), [N2 Bleue](output/pdf/n2-bleue-the-glass-road.pdf),
[N3 Crimson](output/pdf/n3-crimson-the-thorn-feast.pdf), and
[N4 Detour](output/pdf/n4-detour-the-last-road.pdf). Each includes a full-color
cover, referee route map, escalation dashboard, player handout, and compact
two-column running text with a scenario-specific action roster.

## Playability gate

The editorial release bar is documented in [the A+ playability gate](series/a-plus-playability-gate.md).
Run `uv run --python 3.12 --with pypdf python scripts/check_four_muses.py` to
verify each module's structural table requirements and its print packet.

For a browser proof, open [`viewer/index.html`](viewer/index.html) in a local
web server. The arrow buttons and left/right keys turn its rendered pages. From
the repository root, a Python-capable environment can serve it with:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/viewer/`. Rebuild the PDF and viewer images
after manuscript changes with `uv run --python 3.12 --with reportlab --with svglib python
scripts/build_pdf.py`, followed by `pdftoppm -r 150 -png` for the viewer pages.
