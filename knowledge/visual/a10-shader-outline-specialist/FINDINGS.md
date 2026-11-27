# A10 FINDINGS — shaders & ink outlines (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A10.
(Written to disk verbatim by the director from A10's hand-off; the agent's Write tool refused the files.)
Visual ledger: 7 records (~6 images opened); frames/crops private in
`~/ricks-clips-private/analysis-data/rc30/agents/a10-shader-outline-specialist/`. Native frames from 24 videos;
character outline: 26 head instances, 21 frames, 13 videos (target 25 frames: 4 short; 12-video target met); 21 new
natives fetched (10, 15, 16, 17, 19, 20, 30); video 08 failed (shell octal bug). `edges.csv` existed for only 8 videos
(15, 23–28, 30). Data/scripts in `data/` (~156 KB).

## F-a10-001 Character outline width
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

## F-a10-004 Scenery ink
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
