# A08 FINDINGS — props, surfaces, signage, material response (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual-ledger records: 38 (3B: +14) · videos with visual evidence (ledger): 29 of 30 (3B round: 20 videos; RC30-30 still unseen).
(Written to disk verbatim by the director from A08's hand-off; the agent's Write tool refused this file.)
Viewed: 9 full overview sheets (05, 16, 27, 09, 13, 22, 02, 18, 29), 2 montages of t = 10/20/30 s tiles from 20 other
videos (01, 03, 04, 06, 07, 08, 10, 11, 12, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 28) = 29/30 videos at ~180×320;
13 native 1080×1920 frames. Computational: per-frame tables existed for only 10 videos (02, 15, 23–30); native patch
stats on 5 videos (05, 09, 16, 18, 27), 29 manually boxed patches (6 contaminated, discarded). All L*/C* are SCREEN
values (albedo × light × grade), not albedo. Technique only; do not reproduce their props/text.

## F-A08-001 Props are chunky, simplified, slightly oversized toy versions of real objects
OBSERVED, high (all 29 videos seen; strongest 05, 09, 13, 16, 18, 22, 27, 29). Evidence: RC30-16-f000599 printing press
(fat rounded boxes, big gauge), RC30-18-f000449 wallet/licence ~2× hand scale, RC30-13 stopwatch counter larger than
the button, RC30-27-f000209 slot cabinet taller than the character. Low-poly bevelled boxes/cylinders; rivets as dots,
vents as 3 lines; detail spent on the ONE readable element. Implementation: boxes/cylinders with 1–3 cm bevel, hero
props ×1.5–3, detail only on the story face.

## F-A08-002 Inventory: documents/labels/counters/money dominate; machines/tools are set pieces
OBSERVED, medium (eyeballed, no counts). Documents/signs (05 newspaper f449, 09 paint note, 16 scratch card/grids, 18
licence, 28 blueprint); counters/gauges/timers (04, 09, 13 stopwatch, 27 credits LED + jackpot ticker, 16 WINNERS board,
24); money (05, 18, 27); machines (16 press, 27 slot internals, 01); food (09, 02); tools (05, 06, 22); vehicles (05, 07,
10, 18, 29). The same prop is shown in macro to carry the fact (05 pan f869, 27 payout strip f599, 16 grid f1049),
consistent with F-a19-004. Budget: 1 macro hero prop per beat with readable text/number; 3–6 dressing props per set.

## F-A08-003 Texture energy lives in organic materials (treatment A); man-made and treatment-B surfaces are near-flat
MEASURED (small n) + OBSERVED; medium for direction, low for numbers. Median local std of L* (7×7) per patch:
A (05, 27): cave rock 2.9 and 4.0; sand 1.7 (L* std 10.9 from large emboss); gravel 5.6; gold dust 9.3; packed dirt 3.7;
wood table macro only 0.34 (L* std 2.4, soft streaks). B (18, 16): laminate counter 0.18 (painted flecks 8–30 px);
leather 0.05; ceiling tile 0.15; polo 0.23. Hybrid (09): concrete 0.14; brick wall 0.2–3.4; cutting mat 0.34; planks
0.29. Enamel panel 0.11; lit paper 0.12. Per-frame Laplacian tables did NOT separate A from B (FAILED X-A08-001).
Implementation: fine speckle only on rock/earth/gravel (3–6 L*); flat fills for man-made; variation via soft
low-frequency streaks or sparse painted marks.

## F-A08-004 Textures are painted/stylised, not photographic
OBSERVED, medium-high. Rock = terrazzo-like speckle (05 f089); ground = painterly emboss blobs (05 f869); wood = soft
orange streaks + thin dark plank seams 2–4 px, boards 200–500 px wide (05 f539); paper = cream gradient + print; brick
= rectangles with hairline joints (09, 22 f689). Tiling repeats not tested at native scale. Author textures at
1024–2048 px, painterly.

## F-A08-005 Ink/seam lines on props ≈ 2–6 px at 1080 wide
MEASURED (skeleton width, quantised), low–medium. Median (p25–p75): B props near/mid 4.0 (2.8–6.0) 16 f599; B cabinet
2.8 (2.0–4.0); B wallet 4.0 (2.8–8.0) 18 f449; hybrid prison far 2.8 (2.0–4.0) 09 f359; A cliff cracks 2.0 (2.0–2.8)
05 f449; A slot marquee 4.5 (4.0–6.0) 27 f209. Includes text strokes/stripes/character ink; not true FWHM. Stitch
dash ~3 px; lines thin with distance (OBSERVED). Use 3–4 px near / 2 px far; seams 2–4 px (A10 owns the shader).

## F-A08-006 Screen colour per material — L* median [p10–p90] / C* / hue° (n = 1 patch each, MEASURED, low–medium; data/patch_stats.json)
wood dark amber 25 [23–28]/32/53 (05 f539); wood planks 43 [41–47]/26/70 (09 f209); cave rock 61–67 [51–75]/51–53/66
(05 f089 ×2); sandstone cliff 68 [58–74]/26/67; sand 51 [43–71]/30/65; dirt 37 [31–46]/22/60; gravel 47 [20–61]/15/53;
gold dust 69 [53–88]/67/87; newspaper 95 [73–98]/21/96; banknote print 60 [45–72]/44/107; warm-lit paper strip
89 [86–91]/53/91 (27 f599); leather 27 [25–29]/43/54 (18); red enamel 55 [53–56]/94/39 (27 f419); red polo 44/77/37;
laminate counter 63 [50–75]/3/−10; ceiling tile 76 [74–78]/3.5/−30 (16 f329); concrete floor 89 [84–94]/3.5/−150
(09 f359); grey brick 70 [57–72]/18/−102; cyan brick dado 82 [64–86]/21/−120; cutting mat 73 [42–73]/42/168.
Hero props C* 55–95 vs set surfaces C* 3–30; neutral surfaces take the light tint. Character head white computed (p6)
but its box not viewed: unverified. Metal albedo not measured.

## F-A08-007 Prop text: bold condensed/slab caps for headlines, mono/sans for data; cap height 12–65 px at 1080×1920
OBSERVED from native pixel positions (±4 px), medium. Newspaper headline ~65 px, masthead ~28, body 5–7 px (greeked);
slot strip labels ~30–35, headers ~22; LED ticker digits ~110–150 px with unlit ghost segments at ~15–20 % intensity,
CREDITS label ~60; lottery dotted-matrix digits ~38, small print ~15; WINNERS board digits ~95 with split-flap seam;
licence text 14–20, badge ~40. In-world names are fictional parody names (not reproduced here). Beat-carrying text
≥ ~35 px cap; ≤ 15 px is decoration. English throughout; 26 also shows Japanese signage (montage tile).

## F-A08-008 Counters are in-world objects (odometer, 7-segment, split-flap) that roll digits
OBSERVED, medium: 27 f209 ticker with a digit mid-roll ghosting; 13 f719–f749 counter 004→047; 27 f689–f749 multiplier
x00→x14; 16 f989–f1139 grid cells light per match. Bezel + emissive glow so the camera can move around them. Timing
not measured (A12).

## F-A08-009 Material response: few big highlights, simplified glass/liquid
OBSERVED, medium. Gold/metal: bright streaks + sparkle + bloom (05 f539); dark steel pan with rim specular (f869).
Glass = translucent white wedge with edge highlight, no refraction (05 f869 dome, 13 button dome). Liquid = flat
saturated fill + swirl + 2 specular dots (09 f209). Emissive = dark panel, bloom halo ~12 px (16 f1049); 7-segment
ghosts (27 f419). Holographic iridescent foil border on scratch cards (16 f1049). Roughness 0.2–0.4 on hero metal
(INFERRED).

## F-A08-010 Treatment split visible in props (agrees with F-A05-004, F-A09-010)
OBSERVED. A (05, 27, 02): lit PBR-like, highlights, speckled rock, no scenery ink. B (16, 18, 29): thick ink on every
prop, flat fills with a 2–3-tone cel step, saturated primaries, hazard stripes. Hybrid 09/22: toon + thin dark lines.

## Open questions
No true FWHM seam profile; no 360p shimmer test; texel density not measurable from video; B measured on only 2 videos;
4 requested frames (22 f689, 13 f749, 29 f509, 02 f149) extracted privately but never viewed; albedo vs light separation
needs A09/A11; RC30-30 unseen; counter timing for A12. No contradictions with A05/A09/A19.

## Phase 3B additions (2026-11-28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`. Ledger after 3B: 38 records (14 new). 3B visual: 5 four-video composites of 1-fps overview sheets (20 videos: 01 03 04 06 07 08 10 11 12 14 15 17 19 20 21 23 24 25 26 28); 4 grids of 15 native frames (14 videos) with a 6x10 cell overlay; 2 native-patch montages; 1 four-frame screen check (01 19 12 20); 2 every-frame sheets (21, 23). Computational: patch statistics on 14 native frames (14 videos). Scripts: `scripts/patch3b.py`, `scripts/patch3b_xy.py`; data: `data/patches_3b_cells.json`, `data/patches_3b_xy.json`. All L*/C* are SCREEN values (albedo x light x grade). Composites are ~180x320 per tile: prop identity is readable, texture is not (texture claims use native patches only).

### F-A08-101 Props and sets are real 3D assets in a game-engine-like renderer; flat painted cards are the exception
OBSERVED, medium-high (20 videos at 1 fps, plus 2 every-frame sheets). RC30-21 f240-287 (every frame): the giant bell shows continuous perspective change, its floor carpet foreshortens and the gold dragon claws rotate relative to the body during the camera move, so it is a modelled volume, not a card. RC30-23 f240-287: the vertical board with three panels moves as one object with parallax against the village; the panel faces are flat painted illustrations (cards mounted on a 3D frame). Other 3D evidence in the overview sheets: 01 spaceship exterior rotating (f959-1019), 04 road/tree/truck dolly, 07 dashboard from inside the car, 25 corridor fly-through, 26 aisles with perspective. Flat 2D inserts (painted, no perspective): 12 scope scene, 15 polaroid/photo, 19 inbox UI, 28 blueprint, 23 panel art. Limitation: perspective was judged by eye on 120 px tiles; no geometric fit. Implementation: build hero props as meshes; put illustrations on flat quads mounted on meshes.

### F-A08-102 Prop census (20 videos): median 3 hero props per video (range 2-3); categories
OBSERVED, medium (eyeballed from 1-fps sheets, counts are "props shown large/macro with readable content"; a different viewer could differ by +-1). Per video: 01 toilet, star-map card, OFF COURSE display (3); 03 bomb, gold bowl (2); 04 tow sign, lit arrow sign, days-counter sign (3); 06 wooden contraptions, paper/bamboo (2); 07 car dashboard, cash pile, hospital bed (3); 08 coaster, OPENING sign, telescope (3); 10 train, rails, poster (2); 11 ship, giant lens/monocle (2); 12 racetrack, mirror stand, betting board (3); 14 revolver/holster, PHOTOGRAPHS sign (2); 15 gauge/scale, photos, jar (3); 17 coffin, bell, mailbox (2-3); 19 clock, calendar, inbox screen (3); 20 fridge note, scope (2); 21 giant bell-vessel, throne (2); 23 Price board, chest, pardon scroll (3); 24 years-at-war counter, tables, sword (3); 25 body-map UI, pill (2); 26 prize counter, arcade cabinets, vending machine (3); 28 tower, blueprint, red LED board (3). Categories by count of videos with at least one: signs/boards/documents 20/20; counters/gauges/clocks/LED 11 (01 04 08 12 15 19 23 24 25 28 plus 21 gong none); vehicles 6 (04 07 10 11 01 28); containers (chests, jars, bowls, crates) 8; weapons/tools 6; furniture/bed/couch 6. With the earlier 9 videos this confirms F-A08-002 (documents/signs/counters dominate). Props are never cut-out dressing: every video has at least one hero prop whose text or number is the joke carrier.
Implementation: author 2-3 hero props per short (T-A08-06); every short also needs one sign or counter.

### F-A08-103 Outline: props and scenery carry NO ink in the lit videos; only characters are outlined
OBSERVED, medium (14 native frames, 20 overview videos). In 04, 07, 08, 10, 12, 14, 21, 25, 26 (native or overview) cars, bell, house siding, cabinets, rails have no dark outline; separation comes from shading and colour. In 15, 17, 20, 23 (more painterly or stylised) props likewise have no outline, but painted shadow shapes and rim light carry the edge; a thick dark line is on characters only (consistent with F-A10/F-A05 on character ink). This CONTRADICTS the 3A wording (F-A08-010, thick ink on "every prop" in treatment B 16/18/29): those videos were seen in 3A at 180 px and the earlier native crops (16 f599, 18 f449) showed dark prop lines; both observations stand and are not averaged. Not resolved: which videos are "treatment B" is A05/A09-owned; my 3B sample contains 0 clear thick-ink-prop videos besides 3A's. Confidence low-medium on the split by video.

### F-A08-104 Clean-patch texture statistics, 14 videos, 31 patches: only grass, gravel and mesh patterns have visible grain; everything else is flat
MEASURED (patches viewed at 2.4x and filtered; contaminated ones dropped) + OBSERVED, medium (n=31 patches, 14 videos: 03 04 07 08 10 12 14 15 17 20 21 23 25 26; `data/patches_3b_cells.json`, `patches_3b_xy.json`). Median local std (7x7, L*) of valid patches: flat classes 0.0-0.8 (wood 0.59, red paint 0.23-0.47, enamel 0.16, painted metal 0.15, sand 0.20, dirt 0.19, floors/walls 0.0-0.43, sky 0-0.12, stone 0.8); grained classes: grass 3.3 / 12.4 (crisp blades) / 7.7 (stylised night grass with dark strokes), gravel/ballast 4.3 / 10.2, lattice mesh pattern 13.3 (geometry, period about 14 px at 1080 wide). High-frequency FFT power ratio (>1/8 cycle/px): grass 0.09-0.61, ballast 0.52, mesh 0.46, versus 0.02-0.26 elsewhere. Texture is scale-specific: grain is visible only at the pixel size of blades/stones (3-12 px). Wood planks carry no grain at 1080 (L* std 2.4 with knots and nail holes only). Limitations: single patch per class per video; caption band and ink avoided by choosing cells; fabric, plastic, steel and glass lack a clean native patch (two attempts failed, FAILED X-A08-006). Implementation: noise-free albedo for everything except grass/gravel/pattern geometry; for those use 3-12 px detail painted at texture resolution 1024.

### F-A08-105 Screen-colour ranges per material (3B, n per row, MEASURED, low-medium; not albedo)
Patch L* median [p10-p90] / C* / hue: wood planks 45 [..]/27/48 (12 f209); sand 71/28/72 (14 f209); dirt 27/32/52 (23 f299) and 43/43/59 (03 f839); grass 69/64/112 (04 f539), 39/46/130 (07 f419), night 54/21/135 (08 f629); gravel 56/9/48 (04) and 46/17/32 (10 f629); red car paint 64/61/31 (04) and 45/90/38 (07); pale-blue fridge enamel 81/21/233 (20 f299); dark painted metal 29/14/293 (21 f329); gold 65/46/78 (21 f329, with specular blotches std 1.8); glass capsule cap 93/3/205 (25 f419, soft gradient, near clipping); stone pillar 23/8/338 (21); skin/white head 93/6/280 (12 f209, outline pixels 8 %); skin-pink flesh wall 32/40/13 and floor 39/54/29 (25 f419); skies 47/66/285 (07), 81/16/281 (10), 56/66/282 (14), night 14/38/294 (08); floors/walls 17-38 L* dark rooms (15, 21, 26) and 72-83 bright rooms (20: tile 72/24/184, ceiling 83/12/288). Reading: hue follows the light grade (blue/violet in night scenes: hue 280-300 for neutrals), so absolute albedo is NOT recoverable here (A09/A11 owns the separation). Hero paint C* 60-90 vs neutrals C* 3-30 repeats F-A08-006 in 14 more videos.

### F-A08-106 Seam/line width measured: clapboard siding 5-6 px FWHM
MEASURED, low (n=3 seams, one frame, RC30-17 f749 x 300-350, column-median L* profile, depth 16 L*, FWHM 5/6/5 px at 1080 wide). Consistent with 2-6 px in F-A08-005. The wood plank seam profile on 12 f209 failed (caption overlaps; widths 6-10 px but invalid). Use 5 px at 1080 wide (2 px at 360p) for painted board seams close to camera.

### F-A08-107 In-world screens and inserts: three builds, in about half the videos
OBSERVED, medium-low on build method (INFERRED), medium on frequency. Of 29 videos viewed, at least 11 show a screen, UI or lens insert: 01 (wall monitor on a crew room wall showing the same cast as a smaller 2D scene, f149-239 world-map screens, f359 'NO FLUSHING' monitor, bezel and reflection, the A28 incident), 19 (full-frame phone UI 'Inbox (0)', f749: flat, white glow border, spinner, 2D overlay not on a mesh), 12 (circular lens/scope mask with gold ring around a flat painted racetrack scene, f569-599, no perspective inside), 20 (scope mask), 15 (polaroid/photo cards), 25 (holographic body-map UI with labelled rings), 28 (red LED board, blueprint), 24, 16, 27, 13 (counters from 3A). Builds: (a) in-world monitor = textured quad (render-to-texture or pre-rendered 2D clip) with dark bezel and an emissive overlay; (b) screen-space UI card composited by Remotion with outer glow; (c) circular mask with metallic ring over a 2D scene. Frequency about 1 per video; A28's f359 'live second scene' is build (a): a small flat 2D scene, not a second 3D render (the characters inside are 2D with no perspective change, as far as 360 px allowed). Implementation: T-A08-07.

## Phase 3B revisions
- F-A08-010 (treatment split in props): PARTLY SUPERSEDED by F-A08-103; the thick ink on props is not seen in 3B's 14 native frames; 3A claim retained with its two native crops (16, 18) but low-medium confidence for generalising.
- F-A08-002 (inventory, medium): UPGRADED by F-A08-102 (counts from 20 more videos; still eyeballed, medium).
- F-A08-003 (texture energy only in organic): CONFIRMED and widened by F-A08-104 (14 videos); numbers for A/B split downgraded: grain depends on object scale, not treatment.
- F-A08-005 (line widths): one true FWHM added (F-A08-106); earlier skeleton widths stay as upper bounds.
- F-A08-006: extended by F-A08-105; contradiction recorded in F-A08-103.
- Open: texel density (not measurable from video; keep HYPOTHESIS), 360p shimmer test (not run, needs our renders), RC30-30 unseen, fabric/plastic/steel/glass native albedo, counter timing (A12), true prop outline presence per treatment.
