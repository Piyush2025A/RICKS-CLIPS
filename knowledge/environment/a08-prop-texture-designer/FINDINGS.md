# A08 FINDINGS — props, surfaces, signage, material response (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual-ledger records: 24.
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
