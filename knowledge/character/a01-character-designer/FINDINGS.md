# A01 FINDINGS — character design / identity (Phase 3, wave V1)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · author: A01
(`a01-character-designer`); written to disk by the director from A01's hand-off text (the agent's Write tool was
refused by the harness — content unchanged except formatting).
Visual ledger: 27 records (`knowledge/dataset/coverage/visual/a01-character-designer.jsonl`; 20 overview sheets at
180×320, 7 native frames at 1080×1920). Videos viewed: 01, 02, 03, 05, 06, 08, 09, 10, 12, 13, 15, 16, 17, 19, 20, 22,
24, 25, 28, 30 (20/30). Not viewed: 04, 07, 11, 14, 18, 21, 23, 26, 27, 29. Native frames: RC30-09-f000299,
RC30-12-f000269, RC30-01-f000509, RC30-05-f000209, RC30-20-f000569, RC30-03-f000389, RC30-22-f000089.
Overview tile time t s ↔ frame f(30t−1). Most claims OBSERVED; MEASURED values come from ≤ 7 native frames.

## F-a01-001 Construction
OBSERVED, high (20/20). Every character is a 2D hand-inked cut-out inside a lit 3D or painted set: oval head, pill
torso, single-stroke limbs, ball hands (no fingers), feet mostly absent. Sets are rendered 3D (01, 02, 03, 05, 06, 09,
10, 13) or painted with ink-outlined props (12, 15, 17, 19, 20, 22, 24, 28); character construction identical in both.

## F-a01-002 Proportions
Pattern medium, exact ratios low. MEASURED (rays.py, bright face region, hat/hair excluded): face w:h 1.10 (09),
1.15 (12), 1.10 (01), 1.26 (20, chunkier police head). OBSERVED (5 frames): head ≈ 1.25× (stout) to 1.8× (slim) torso
width; head height ≈ 0.85–1.05× torso height; legs ≈ 2–3× torso length. Silhouette "lollipop on stilts"; no corners
except hats/props. Exact numbers → A03.

## F-a01-003 Body archetypes
OBSERVED, medium. Slim pill (default, 20/20); stout pill (guards, cops, big prisoner — 09, 20, 13, 02 …, ≈ 6/20);
tall pin for wealth/authority (05 f000629 & f001079, 08, 12, 09, 10, ≈ 6/20); child scale 40–60 % (≈ 6/20); props or
organisms with the same face grammar (pill 25, powder sack 22 f000869, brain 28/25).

## F-a01-004 Outline
One dark ink line shared by head/torso/limbs (limbs are the line). Colour is tinted, not pure black (navy 12;
aubergine-black 09, 05). MEASURED at the head's widest point, scanlines normal to the edge: 09-f000299 median 17.5 px
(IQR 12–24, n = 60); 12-f000269 median 10 px (IQR 9–12, n = 54) at native 1080 width; head ≈ 500 px wide → ≈ 2–3.6 %
of head width. n = 2 frames → low–medium confidence. OBSERVED: painted-set props use a line about half as heavy;
rendered sets have no scenery outline, so the character line separates figure from ground.

## F-a01-005 Shading and lighting response
MEASURED + OBSERVED, medium. Faces near-white but take the scene tint; cheek-patch median RGB: 09 (220,190,209) pink
room; 12 (231,236,246) blue daylight; 05 (254,235,215) amber mine; 20 (253,247,245) and 01 (251,250,253) bright rooms.
Torsos flat colour with a soft gradient and light texture (pinstripes 03, line texture 01, pockets 20); hair/hats carry
most detail. Soft cast ground shadows in rendered sets (01 f000329–f000389, 02, 09, 03, 05). Dark scenes (01 f000509):
faint dark halo follows the outline.

## F-a01-006 Role colour coding
OBSERVED, medium. Torso hue is the primary identifier; each video fixes 3–6 saturated, mutually distinct hues.
Everyman/protagonist teal (03, 05, 10, 12, 20) or yellow-orange (01, 02, 16, 28); police/authority blue uniform +
peaked cap + gold star (09, 13, 20, 10); wealth white suit + top hat (05); crews/crowds one template in rotating hues or
stripes (22 pirates, 28 vests). Villains have no fixed colour — marked by hat/face/facial hair (03 goatee, 13
moustache, 15 f000059–f000149 hooded grin). ≈ 4–6 colours per character (torso, hair/hat, 1–2 accents, outline, white
face) — eyeballed; no k-means (see FAILED).

## F-a01-007 Headgear and hair = second identifier
OBSERVED, high (20/20). Beanie, bandana, top hat, bowler, police cap, boater, crown, nightcap, head-lamp; protagonist
default hair: short brown swoop with drawn hairline. Glasses and moustaches tertiary; a signature prop carries the
story role.

## F-a01-008 Face grammar
OBSERVED, high. Resting: solid black dot/oval eyes, heavy separate brows, minimal mouth; half-lid flat bar = smug.
Shock: white ring eyes with pupil dots (01 f000509, 28 f000209, 25 f000089). Rage/pain: gritted-teeth grid mouth;
sweat and tear drops as accessories. Faces sit low; hair/hat covers the top third. (Detailed expression system → A02.)

## F-a01-009 Characters per frame
OBSERVED, low. RC30-01 tally over 40 overview tiles: none 13, one 14, two 3, three-plus 10. Groups of ≥ 3 appear in
≥ 12/20 videos. Crowd members use the same construction at tiny scale with dot faces.

## F-a01-010 Scale in frame
MEASURED: face height 409–468 px of 1920 (21–24 %) in four close-ups. OBSERVED estimate: wides ≈ 4–8 %. Design
minimum: hat, torso hue and eyes must read at ≈ 8 % frame height.

## F-a01-011 Consistency across shots and lighting
OBSERVED, high. Constant: head shape, hair/hat silhouette, torso hue family, glasses, outline weight. Varies: face
tint/brightness, scale, head tilt, perspective skew, expression. Examples: 01 yellow-shirt f000029, f000569, f000869,
f001019; 05 teal buddy f000149–f000419; 20 teal dad f000179, f000299, f001109. (Hu-moment/palette metrics not computed.)

## F-a01-012 Exceptions
30 f000389–f000689 translucent blue x-ray body with brain, water-skinned head; 13 f000869–f000899 bronze statue
versions; 15 f000059–f000149 hooded shadow villain; 25 pill protagonist; 22 f000869 prop-as-character; 10
f000539–f000599 purple-faced anger gag; 06 f000239–f000359 heavily armoured commander; 19 f000569–f000599 huge face
close-up.

## Contradiction
Outline width: scanline method 10–17.5 px vs ray method 20–40 px (biased; FAILED F01). Scanline is preferred.

## Open questions
Unviewed videos (04, 07, 11, 14, 18, 21, 23, 26, 27, 29); rigid cards vs redrawn frames for heads/limbs (needs frame
sequences, A04); outline width needs > 2 frames (A10); exact ratios (A03); expression hand-over (A02).
