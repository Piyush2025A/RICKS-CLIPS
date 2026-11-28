# A10 FINDINGS — shaders & ink outlines (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A10.
(Written to disk verbatim by the director from A10's hand-off; the agent's Write tool refused the files.)
Visual ledger (corrected 2026-11-28): 13 records; ledger videos with at least one frame I opened: 30 of 30 (18 in Phase 3A; 3B added a
620x620 crop survey of all 30 at f300 plus head-edge crops of 01, 03, 05, 09, 12, 22). Phase 3A header claim "native frames from 24 videos" was
WRONG: 18 videos were viewed; 01, 03, 05, 09, 12, 22 were only measured from A01 segmentation (computational) until 3B. Computational: F-a10-001
used A03/A01 tables; 3B rescan (F-a10-101) is computational on 26 videos. Frames/crops private in
`~/ricks-clips-private/analysis-data/rc30/agents/a10-shader-outline-specialist/` and the session scratchpad. 3A notes: video 08 fetch failed
(shell octal bug); `edges.csv` existed for only 8 videos. Data/scripts in `data/`.

## F-a10-001 Character outline width  (SUPERSEDED in numbers by F-a10-101; kept for history)
MEASURED, medium. Median 10.3 px at 1080 width (IQR 7.6–13.7, range 2.8–29.3) = 3.56 % of head width (IQR 2.9–4.4 %).
n = 26 head instances, 21 frames, 13 videos: 04, 07, 11, 14, 21, 23, 26 (A03 landmarks) and 01, 03, 05, 09, 12, 20, 22
(A01 face segmentation). Method (`scripts/ink_scan4.py`): sub-pixel horizontal scans across the head side edge; width
= FWHM of the dark line × Sobel edge-normal x-component; scans with normal < 0.6 rejected. Limits: landmarks
approximate; extremes 2.8 and 29 px kept (probably landmark errors or hair merging). Consistent with F-a01-004.

## F-a10-002 Width scales with character size → baked into the card
MEASURED, medium-low. Spearman ρ = 0.56 (p = 0.003, n = 26); log-log slope 0.54 (between constant screen space 0 and
object space 1). Same-character pairs: captain in 11 (head 179→313 px, line 5.2→10.8), orange in 26 (416→217 px, line
15.2→9.3), red cowboy in 14 (237→314 px, line 10.5→29.3, suspicious). Reading: the line is painted into a billboarded
texture (as F-A06-007), not a screen-space post pass.

## F-a10-003 Line colour
MEASURED, medium. Core L* median 2.7 (IQR 0.2–11.3), a* +6, b* 0; 17/26 below L* 5 → near-black with a small tint. Warm
sets (26, 21, 23) show lighter cores ≈ L* 15–25; whether the line tracks scene colour rests on 3 videos (low). Face fill
gray median 232.

## F-a10-004 Scenery ink  (PARTLY SUPERSEDED by F-a10-102: treatment is per video, with mixed cases)
OBSERVED + MEASURED on 2 crops. Treatment A: no world ink (04, 07, 10, 11, 14, 18, 26 checked; 2× crops show tonal,
DOF-soft edges only: 04-f000149 trunk, 14-f000299 building, 23-f000449 tower). A05's "hybrid" 11, 14, 18 show no scenery
outline in these frames. Treatment B: thin dark lines on silhouettes and interior creases (door panels, arch ribs, trim,
shelves, ceiling tiles) — 25-f000519, 29-f000359, 19, 16, 20, 15, 17; gold trim in 21 is painted texture, not ink.
Hairline FWHM: 25-f000519 median 2.4 px (n = 2109, IQR 1.7–4.1); 29-f000359 median 2.1 px (n = 1487). No taper with depth
(far arches 2.7–3.0 px, near doors 2.0 px). Line colour = darkened, desaturated surface colour: RGB (122,81,65) in the
pink corridor, (65,55,41) on the tower. Limits: 2 frames in 2 videos; pass-drawn vs texture-painted not distinguishable.

## F-a10-005 Character ink is 3–5× heavier than scenery ink
MEASURED, medium (≈ 10 px vs 2–3 px).

## F-a10-006 Face fills are smooth gradients, not cel bands
MEASURED, medium. n = 21 heads, 7 videos: hard-gradient share (≥ 6 gray levels/px) median 0.0002, max 0.003; flat share
median 0.46, smooth share 0.49; p95–p5 luma range 32 levels. Limit: pixels < gray 150 excluded, so A09's hard terminator
is not tested here.

## F-a10-007 Scenery shading
OBSERVED, medium. Both treatments use smooth real-time lighting; B adds painted textures and an ink line, no cel bands.
Speculars are white blooms on glossy props plus water caustics; no star glints. Gradient-share stats did not separate A
from B (FAILED F-3).

## F-a10-008 No film grain
MEASURED, medium. Residual std in flat zones 0.19–0.53 gray levels (49 frames, 22 videos) = codec-noise level.

## F-a10-009 No chromatic aberration
MEASURED, high. Radial R–B shift median 0.00 px (IQR −0.06 to +0.06); positive in 47 % of patches; 5 % > 0.5 px; n = 221
patches in 49 frames.

## F-a10-010 Bloom and vignette
Bloom: OBSERVED, low-medium — glow around lamps/highlights in ≈ 15–18 of 24 videos viewed (e.g. 11, 14, 19, 20, 26, 27,
29, 16, 17, 30), strongest in dim sets with lamps; threshold ≈ luma 0.9 (INFERRED). Vignette: INFERRED, low — temporal
median image per video (`scripts/vig.py`), corner/centre luma ratio median 0.73 (IQR 0.56–0.81), < 1 in 29/30 (exception
14); a centred white character confounds this → upper bound only.

## F-a10-011 `edges.csv` is a weak ink indicator
LOW. `edge_width_px` quantised to {1.5, 3.5, 5.1}; `dark_line_ratio` 0.15 (video 30) to 0.77 (video 24).

## Contradictions
1. F-a10-002 slope 0.54 (between screen and object space); same-character pairs lean object space, large scatter.
2. A05 labels 11, 14, 18 hybrid with light/no outlines; these frames show none.
3. Painted vs pass-drawn scenery lines not separable without a tracked camera-move sequence.

## Open questions
Baked vs pass-drawn scenery line in B (needs tracked move); character ink colour vs scene tone (more warm-set samples);
vignette strength (character-free sample); retry video 08.


## Phase 3B additions (2026-11-28)

## F-a10-101 Character outline width, re-measured on 26 videos
MEASURED, medium-high (n and videos meet the high threshold; method not independently validated, landmark error unquantified, so medium-high).
Method (`data/scripts/ink_scan5.py`): native 1080x1920 frames, A03 head landmarks (3A + `landmarks_3b.csv`), 7 rows per head between 12 % and 55 %
of head height above the chin, both sides; perpendicular profile = horizontal profile sampled every 0.25 px, FWHM of the dark stroke at the half-depth
between core and the inside/outside reference, multiplied by the edge-normal x-component (scans with normal < 0.6 rejected; contrast filters).
Result: 80 heads, 58 frames, 26 videos, 694 scans. Per head: median 9.3 px at 1080 width (IQR 6.9-12.1, range 2.3-29.3) = 3.68 % of head width
(IQR 2.72-4.93 %, range 0.7-9.8). Per-video medians (n = 26): 9.2 px (IQR 7.1-11.8). Scan level: 9.0 px (IQR 5.0-14.5). Core gray median 8 (IQR 1-23).
Agrees with F-a10-001 (10.3 px / 3.56 %); the IQR is wider because 3B adds videos with thin lines (19, 28, 29: 2.3-3 px, 0.7-1.4 % of head width).
Excluded: back views, heads < 60 px, hats/hair rows (rows kept in the lower face). Videos 19, 28, 29 give thin lines on some characters (see Contradictions).

## F-a10-102 Ink treatment per video (all 30 viewed) resolves the A08 contradiction
OBSERVED (crop survey, 1 frame per video at f300, 620x620 native crop downscaled 0.5, plus 3A natives and 3B push-in frames), medium-low
(1-2 frames per video; thin lines can vanish at 0.5x, so A may be under-counted by a few).
Characters: thick dark outline in 30/30 videos. Worn headgear (hats, helmets, chef hat) is outlined as part of the character in 05, 06, 11, 12, 14, 22.
Scenery/props: A (lit, no ink on scenery or props) 20 videos: 01, 02, 03, 04, 05, 06, 07, 08, 10, 11, 12, 13, 14, 18, 21, 22, 24, 26, 27, 30.
B (visible dark ink on props and/or scenery) 6 videos: 16, 19, 20, 23, 25, 29. Mixed (ink on some props, lit elsewhere in the video) 4 videos:
09 (flat pink painterly set), 15, 17 (underground shot inked, attic lit), 28 (porthole ring inked; outdoor lab scene lit).
So A08 3B (no ink in 14 natives) and A08 F-010 / A10 "thick ink" are both true: they sampled different videos. Treatment is per video, with
a few mixed videos; it is not one global style. 3A had 7 videos in B; the survey keeps 25, 29, 19, 16, 20 in B and moves 15, 17 to mixed.
Props can carry thick ink: clock rim in 19 = 8.0 px FWHM (n = 15 rows, IQR 7.5-16.5, core gray 18); porthole ring in 28 = 12.5 px (n = 20, IQR
10.8-102, the upper quartile is contaminated by the ring's flat dark band; core 20). Scenery hairlines in B stay 2.0-2.4 px (F-a10-004). Two frames only.
Scripts: `data/scripts/prop_ink.py`.

## F-a10-103 Outline colour: dark aubergine/brown-black, not pure black
OBSERVED, medium-low (6 head-edge crops in 3B: 09, 12, 22, 05 show a dark purple-brown stroke, roughly RGB 40-50, 25-35, 35-45 by eye; 03 near-black;
01 blends into a dark navy set). With F-a10-003 (core L* median 2.7, a* +6) and A01's note, the line is a very dark warm/purple black. Per-character
colour tracking was not measured in 3B beyond these crops; the A01 observation of a warm brown line on some characters is neither confirmed nor
refuted (the tint is small and the codec lifts line cores).

## F-a10-104 Line width vs scale on push-ins
OBSERVED (6 push-in moves from A13 `moves_table.csv`, 4 native frames each, viewed: 28 f448-611, 22 f580-629, 26 f154-236, 30 f725-820, 17 f443-512,
16 f500-527) + MEASURED (pooled heads), medium-low. Visual: in 30 and 16 the character outline is thin when the head is small and thick when it fills the
frame, i.e. the line grows with the card (30: hairline at f725, heavy rim at f820; 16: thin at f500 to heavy at f509). Not constant screen width. Measured
across the 80 heads: pooled log-log slope of line width on head width = 0.55; same-character pairs (head ratio >= 1.3, n = 7): median per-pair slope 0.53
(IQR 0.19-1.17; one pair has a negative slope: sailor in 11); width by head-width band: < 200 px 7.7 px (4.1 %, n = 26), 200-300 px 9.2 px (3.7 %, n = 31),
300-400 px 10.8 px (3.0 %, n = 16), >= 400 px 11.9 px (2.5 %, n = 7). Reading: the line is baked into the card art and scales with it, but sub-linearly
(the art is not drawn with a size-proportional stroke); no sign of a screen-space constant-width pass. Automated per-frame head tracking along the moves
failed (FAILED F-7), so there is no per-frame curve.

## Phase 3B revisions
- F-a10-001: numbers superseded by F-a10-101 (26 videos, 80 heads); old value stays within the new IQR. Confidence up.
- F-a10-002: upgraded to n = 80 heads (rho 0.39, p = 0.0004 pooled; slope 0.55); the old rho 0.56 on 26 heads is superseded; conclusion unchanged.
- F-a10-004 / F-a10-005: treatment is per video (F-a10-102); "thick scenery ink absent" and "present" are both true by video. Props can be as heavy as
  characters (19, 28), so "character ink is 3-5x heavier than scenery" holds for scenery hairlines only.
- Header: coverage corrected to the ledger (above).

## Phase 3B contradictions / open
1. Thin character outlines in 19, 28, 29 (0.7-1.4 % of head width) vs 3-5 % elsewhere: could be a different character style or measurement on
   thin/dark hair edges; unresolved, not averaged away.
2. A01's "warm brown per character" colour vs near-black: not resolved.
3. Baked vs pass-drawn scenery line in B: still needs a tracked camera-move sequence.
