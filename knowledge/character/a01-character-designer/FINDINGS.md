# A01 FINDINGS — character design / identity (Phase 3, wave V1)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · author: A01
(`a01-character-designer`); written to disk by the director from A01's hand-off text (the agent's Write tool was
refused by the harness — content unchanged except formatting).
Visual ledger (updated 3B): 68 records (`knowledge/dataset/coverage/visual/a01-character-designer.jsonl`: 50 overview sheets viewed at 180×320 tiles [20 in V1, 30 in 3B, first sheet of each video = t 1–40 s only], 7 native frames at 1080×1920 [V1], 11 two-frame images of 22 native frames downscaled to 540×960 [3B]). Videos with visual evidence: 30/30 (sheet 1 of every video); videos with a native-decoded frame in the ledger: 29/30 (all except 25). Second overview sheets (t > 40 s) were NOT opened. V1 text below: 'Videos viewed 20/30' is SUPERSEDED by this line. Native frames: RC30-09-f000299,
RC30-12-f000269, RC30-01-f000509, RC30-05-f000209, RC30-20-f000569, RC30-03-f000389, RC30-22-f000089.
Overview tile time t s ↔ frame f(30t−1). Most claims OBSERVED; MEASURED values come from ≤ 7 native frames.

## F-a01-001 Construction
OBSERVED, high (20/20). Every character is a 2D hand-inked cut-out inside a lit 3D or painted set: oval head, pill
torso, single-stroke limbs, ball hands (no fingers), feet mostly absent. Sets are rendered 3D (01, 02, 03, 05, 06, 09,
10, 13) or painted with ink-outlined props (12, 15, 17, 19, 20, 22, 24, 28); character construction identical in both.

## F-a01-002 Proportions
Pattern medium, exact ratios low. MEASURED (rays.py, bright face region, hat/hair excluded): face w:h 1.10 (09),
1.15 (12), 1.10 (01), 1.26 (20, chunkier police head). OBSERVED (5 frames): head ≈ 1.25× (stout) to 1.8× (slim) torso
width; head height ≈ 0.85–1.05× torso height; legs ≈ 2–3× torso length [SUPERSEDED 3B: see F-a01-104]. Silhouette "lollipop on stilts"; no corners
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
[EXTENDED 3B, see F-a01-102.] MEASURED + OBSERVED, medium. Faces near-white but take the scene tint; cheek-patch median RGB: 09 (220,190,209) pink
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
[REFINED 3B, see F-a01-103: dot eyes are one of five eye types.] OBSERVED, high. Resting: solid black dot/oval eyes, heavy separate brows, minimal mouth; half-lid flat bar = smug.
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

---
## Phase 3B additions (2026-11-28)
Evidence base: sheet 1 (t = 1–40 s, 40 tiles of 180×320) of all 30 videos, each opened (ledger: 30 `contact_sheet` records);
22 native frames (02, 04, 06, 07, 08, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 26, 27, 28, 29, 30), decoded at native
resolution by ffmpeg, **downscaled to 540×960 before viewing** (ledger: 11 `frame` records, two frames per image). Not covered: t > 40 s
in every video longer than 40 s (second overview sheets unopened), RC30-25 native. Per-video table: `data/census_3b.csv`
(my judgement per video from tiles; counts approximate ±1; no per-frame detector). All claims OBSERVED unless stated.

### F-a01-100 Character census (30 videos)
OBSERVED, medium (n = 30 videos, counts eyeballed). Distinct human-type characters per video: median 7 (IQR 5–8, range 2–9; mean 6.5).
Types and videos: (a) human adult/teen, 30/30; (b) human child/small scale, 7/30 (04, 07, 08, 13, 15, 20, 27); (c) crowd of ≥ 6
simultaneous figures on one tile, 17/30 (03, 06, 08, 09, 10, 12, 14, 16, 17, 19, 21, 22, 23, 24, 25, 26, 28); (d) animal, 11/30
(11, 12, 14, 15, 19, 20, 21, 23, 24, 26, 28); (e) object/organ with a face or character role, 5/30 (13 statues, 22 powder sack, 25
pills, 28 brain with face, 30 brain without face). Headgear on at least one character 27/30 (not 19, 25, 30); glasses on at least
one 15/30; moustache/beard on at least one ≥ 11/30 (not tallied exactly). Characters on screen per 1-fps tile (n = 3 fully tallied
videos, 120 tiles): RC30-01 none 13 / one 14 / two 3 / three+ 10; RC30-04 15 / 16 / 9 / 0; RC30-14 3 / 19 / 12 / 6. So 8–38 % of
tiles contain no character (environment/prop inserts), one or two characters dominate (≈ 70–75 % of tiles), 3+ only when a crew/crowd
beat exists. Per shot type (insert / close-up / medium / wide) was **not** tallied: no shot-type labels exist for 1-fps tiles. Limit:
tiles at 1 fps; first 40 s only; characters inside cars (07) counted when a face is visible.
Implementation: cast budget ≈ 5–8 named designs per 40 s episode; always plan one prop/organ/animal variant per episode.

### F-a01-101 Design constants hold ≥ 20 videos (see table in 'Design constants' below)
OBSERVED, high for items marked H (≥ 20/30 sheet videos AND consistent on the native frames). Exceptions with keys recorded per row.

### F-a01-102 Shading is present: soft tint gradient plus hard highlight streaks (corrects "flat" reading)
OBSERVED on 22/22 native frames, medium. (1) Faces and torsos are not flat: every checked frame shows a soft gradient or scene tint
on the head and torso (cool lower-face band 14 f299; gradient on torso 29 f509, 30 f299, 02 f749; scene-tinted face 30 f299 cream,
15 f209 blue). (2) Hair, hats and helmets carry hard-edged specular streaks (08 f179 both caps, 14 f299 hat band, 23 f089 armour,
27 f089 hair, 28 f209 hair, 29 f509 hair) in ≥ 8/22. (3) No fully self-shadowed cel terminator on the face was seen. Outline
sits on top of all shading. So the card is "soft gradient + highlight streaks", not "none" and not "cel shadow". Contradicts nothing
in V1 (F-a01-005 said gradient), but A06/A09 wording "flat" should be read as "no hard cel shadow".
Implementation: bake 2-stop gradient (≈ 10–15 % L* range) + 1–2 white highlight streaks on hair/hat in the card art; no runtime shading except the A09 tint.

### F-a01-103 Eye construction: five types, none exclusive
OBSERVED, medium–high (22 native + 30 sheets). Types: (1) solid black dot/oval (08 f179, 18/19 calm); (2) ring + pupil dot for shock (11 f329,
13 f089, 28 f209 big white rings with heavy outline; 18 f089 thin grey rings); (3) thin dash/bar under a heavy brow = deadpan (02, 04,
29, 30 f299 "half-lid" with a line); (4) ^ arcs closed = happy (16, 17, 12 sheets); (5) round glasses = two rings + dots (05, 13,
20, 21, 23, 26, 29). Brows: separate heavy strokes, 22/22. Cheek blush ovals appear on some (11 f329, 23 f089, 21 f179 pink) = 3/22 native.
Resting default: type 3 in ≈ 14/22, type 1 in ≈ 6/22. Eyes sit in the lower half of the head; hair/hat covers the top third. Expression sets → A02.

### F-a01-104 Legs vs torso: correction (SUPERSEDES F-a01-002 "legs 2–3× torso")
OBSERVED by eye on two clean full-leg frames (07 f839: torso ≈ 93 px, legs ≈ 110 px at 540 width → 1.2×; 29 f509: torso ≈ 235 px,
legs ≈ 280 px → 1.2×; reading error ±10 %). Together with A03 F-a03-004 (landmarks: legs 1.22 HW ≈ 1.4–1.5× torso, n = 6 slim, 7 videos)
the defensible range is 1.2–1.5× torso length; the V1 "2–3×" was an optical effect of thin lines and low placement. **Dependency:** A03's
further videos were not available in `knowledge/character/a03-anatomy-proportion-specialist/` at 3B time (file unchanged: 7/30 videos); numbers
here defer to A03. Confidence low (n = 2 mine); direction (not 2–3×) is high-confidence because both independent methods agree.

### F-a01-105 Outline colour: ink is near-black to dark brown, per character, never pure black on every shot
OBSERVED on 22/22, medium (visual only; no sampled hex). Near-black with blue/aubergine tint in the cool-lit scenes (06, 07, 10, 13,
21, 23, 24, 28); warm dark brown in warm-lit or hair-brown characters (02 f749 body and limbs brown; 27 f089 limbs brown; 30 f299 warm
brown, thinner than elsewhere). Limb strokes are the same colour as the head contour; limbs are usually 60–100 % of head-contour
weight (thinner in 30, 02). Painted props carry a thinner line than the character (06 gong?, 08 wallet, 24 anvil). One-colour contour;
no inner line colour. Numeric value remains the V1 measurement (scanline 10–17.5 px at 1080 w, n = 2); not re-measured.

### F-a01-106 Hands and feet
OBSERVED 22/22 native: hands are a round ball or mitten at the stroke end, no fingers (02 cup, 08 wallet, 11 and 13 clasped balls, 29
button panel with a dot hand, 30 steel balls held in ball hands). Exception: armour gauntlet drawn as segmented plates (23 f089).
Props are held by overlap, not gripped. Feet: legs end in a rounded stroke tip (default); a small flat foot nub appears in 29 f509;
footwear only as costume/prop when needed (slippers 02 sheet f809, 20 sheet f1079; boot prop 22). Seated figures bend legs at the
knee as two strokes (02, 30).

### F-a01-107 Card shadows: native check of the A28 conflict
OBSERVED, medium, per-scene not per-light. Native frames with **no** cast shadow under the figure: 04 f569 (sunny roadside), 06 f299
(sunny grass), 08 f179, 14 f299 (noon street), 30 f299 (spotlight on the chair, only the chair is shadowed), 02 f749. Sheet tiles
with a clear cast shadow: 01 f329–f389, 09 f629–f899, 14 f779–f959 (sunset, long shadows), 24 f029, 03 f1049. Shadow follows
strong low or window light in these but A28's counter-example (03 campfire) stays. Not resolvable by me; the shadow is a
per-shot switch that correlates with directional low sun/window light in 5 of 6 present cases.

### F-a01-108 Silhouette/shape language
OBSERVED, high (30/30 sheets). Round head (circle/ovoid, H/W ≈ 0.93 per A03) on a pill torso: roundness signals approachable
everyman. Square/trapezoid appears only in costumes and props (peaked caps 02/09/13/20, armour 06/23, boxy hats). Tall pin torso =
wealth/authority (05, 10, 12); stout wide pill = guard/boss (02, 09, 11, 13, 20); small = child/novice. Triangular cues: hat brims,
pointed cowboy/pirate hats (11, 14), nightcap tip (17), hair curl (18). Role is read by head-top silhouette first (hat shapes distinct
in ≥ 25 videos), then torso hue. 64 px height test: not run on references (no masks).

### F-a01-109 Animals and object characters use a second construction
OBSERVED, medium. Cats (19 f659 sheet+native, 20, 26) are 2D ink-outlined cut-outs with simple dot faces and whisker lines, same line
rules as humans. Horses (12, 14), frogs (21), donkey (23), large mascot animal (11) look 3D-rendered or painted, not stick-style.
Pills (25) and the powder sack (22) reuse the human face grammar on a non-human body. Therefore animals ≈ 2 routes: reuse the
outline-card pipeline (small animals) or render (large animals). Limit: only one animal checked on a native frame (19).

### Design constants (original-character spec input)
Videos = of 30 (sheet evidence); "native" = of 22 native frames this round. Conf per EVIDENCE.md (high needs ≥ 20 videos + validated method).
| Property | Value | n videos | Conf | Exceptions (keys) |
|---|---|---|---|---|
| Head | circle/ovoid, white-cream fill, closed ink contour; H/W 0.93 (A03, n = 12, 5 videos) | 30 (sheets) | H shape, L ratio | 25 pill head; 30 water-skin head; 13 bronze statues |
| Torso | pill/bean, single closed contour; width 0.65 HW slim, 0.85 stout (A03) | 30 | H shape, L ratio | long robe 21, 23; armour 06, 23 |
| Limbs | single constant-width stroke, two legs, two arms, no joints drawn | 30 | H | knight armour 23 (segmented) |
| Legs / torso length | 1.2–1.5× (my eye 1.2 n = 2; A03 1.4–1.5, n = 6) | 7 (A03) + 2 mine | L | robes 0.4 HW legs (21, 23) |
| Hands | ball/mitten, no fingers | 22 native / 30 sheets | H | 23 gauntlet |
| Feet | none (rounded stroke end); footwear only as costume | 22 native | M | 29 nub; slippers 02, 20 |
| Eyes | 5 types (dot, ring+pupil, dash under brow, ^ arc, glasses); eyes in lower half | ≥ 24 | H | none found |
| Brows | separate heavy strokes, high expressiveness | 22 native | H | — |
| Mouth | minimal line/dot at rest; open arc/teeth grid for emotion | 30 | H | — |
| Outline | one dark colour (near-black to brown), ≈ 2.5–3.6 % of head width (V1 n = 2, A10 n = 26/13 videos) | 30 | M | brown 02, 27, 30 |
| Shading | soft gradient + scene tint; hair/hat hard streaks; no cel terminator | 22 native | M–H | none fully flat |
| Cast shadow | per-scene switch, ≈ 40 % of sampled shots | 6 native + tiles | L–M | see F-a01-107 |
| Palette per character | 4–6 colours (torso, hair/hat, 1–2 accents, outline, white face); not k-means measured | 30 sheets | M | — |
| Co-present characters | distinct torso hues; 3–6 hues per scene | 30 | M | — |
| Headgear | on ≥ 1 character | 27 | H | 19, 25, 30 |
| Protagonist headgear | present in ≈ 10/30 | ≈ 10 | L | bare-headed protagonists 07, 09, 18, 25, 29, 30 |
| Glasses | on ≥ 1 character | 15 | M | — |
| Facial hair | on ≥ 1 character | ≥ 11 | L–M | — |
| Characters in a 40 s episode | median 7 distinct (IQR 5–8) | 30 | M | 25 (2), 30 (3) |
| Characters per tile | 0 in 8–38 %, 1–2 in ≈ 70 %, 3+ in 0–25 % | 3 videos | L | — |
| Crowds | same template, tiny, rotating hues | 17 | M | — |
| Animals | present | 11 | M | cats 2D, large animals rendered |
| Object/organ characters | face grammar on non-human body | 5 | L–M | — |
| Set rendering | lit 3D or painted, ink only on characters and key props | 30 | H | — |

### F-a01-110 Original-signature guidance (genre vs copy risk)
INFERRED from the table, label HYPOTHESIS for the "safe" split until user approval.
**Genre constants (shared by ≥ 20 videos; safe to use):** characters ink-outlined and clearly separate from a lit set; round-ish head with eyes
in the lower half and heavy brows; bean/pill torso; thin constant-width limbs; hat or hair as the identity top-shape; torso hue as the
role code; 4–6 colours per character; per-episode small cast with one prop/organ/animal variant; crowds as tiny same-template figures.
**Would look copied (avoid the combination, not each item):** (1) pure white circle head + dot/ring eyes + heavy separate brows +
half-lid bar + pill torso + two long parallel stick legs + ball hands in the same ratios (head 0.93, torso 0.65 HW, legs 1.2–1.5×); (2)
the identity set of recurring role costumes (teal everyman, yellow-shirt protagonist, police blue cap with gold star, white-suit top-hat
rich man, name-tag uniforms, striped pirates); (3) the single-lock hair curl, swoop fringe and shading streak pattern; (4) the same
caption-and-card staging. **Differentiators for our cast (from T-a01-02, still HYPOTHESIS):** rounded-square or egg-tilted head, tapered
limbs, mitten or three-lump hands, coloured (indigo/burgundy) ink, non-white warm face fill, shoes drawn on every character, a distinct
eye grammar (e.g. vertical ovals or crescent), a fixed per-character silhouette notch (ear, tuft or hat) not borrowed from reference
costumes, and animals/props drawn in the same line system so the world reads as one author. No reference design is traced or
re-skinned; rules only.

## Phase 3B revisions
- F-a01-002 legs "2–3× torso": **SUPERSEDED** by F-a01-104 (1.2–1.5×; A03 preferred; dependency on A03 remaining videos).
- F-a01-004 outline: **EXTENDED** (F-a01-105): colour is per-character near-black to brown; weight still n = 2 measured.
- F-a01-005 shading: **EXTENDED/CORRECTED** (F-a01-102): soft gradient present on 22/22; hard streaks on hair/hats; "flat" wording must not be used.
- F-a01-008 face grammar: **REFINED** (F-a01-103): five eye types; "resting = dot eyes" downgraded (resting is more often a dash under a brow, ≈ 14/22).
- F-a01-009 characters per frame: **UPGRADED** from n = 1 to n = 3 videos; still low; and census F-a01-100 supersedes the "≥ 12/20 groups" count with 17/30 crowd videos.
- F-a01-012 exceptions: ADD 25 pills as crowd, 22 powder-sack, 28 brain character, 30 brain without face, 11 large rendered mascot animal, 12/14 rendered horses, 21 rendered frogs.
- F-a01-003 child archetype: now 7/30 (04, 07, 08, 13, 15, 20, 27), up from ≈ 6/20; still not measured numerically (A03).
- F-a01-011 consistency: unchanged; native frames of 29 videos show same construction in all.
- Bible `knowledge/bibles/CHARACTER.md` C4: leg figure compatible; C8/C9: add colour variance (brown) and "gradient present".
- Open: second overview sheets (t > 40 s) unopened; no palette k-means; no 64 px readability on references; A03 re-measure pending; scene-shadow rule unresolved.
