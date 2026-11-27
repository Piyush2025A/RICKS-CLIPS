# A07 FINDINGS: depth and perspective (Phase 3, partial)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual-ledger records: 22 (`knowledge/dataset/coverage/visual/a07-depth-perspective-specialist.jsonl`).
Computational: native 4x3 grid stats (rows 0-20/20-40/40-58/82-100 % of height; caption band excluded) every 10th frame (RC30-01..04) / every 30th (05..30): 26,226 cell rows, 30/30 videos. Scripts + small JSON in `data/` (v0.1). Visual: 15 videos on 1-fps overview sheets (03,04,05,06,08,10,12,13,14,17,19,21,22,25,30), 3 random-sample montages (120 frames, seed 7, all 30 videos, 116 labelled), 3 rack-focus strips, 1 horizon check strip.
Limits common to all: labels are mine from 180x320 tiles; per-video n is 3-4 frames; sheets only (no 4x native zoom).

## F-A07-001: Most frames are deep focus; visible defocus is a minority, concentrated in close-ups
- MEASURED-by-count of OBSERVED labels. Confidence: medium (n=116, 30 videos; labels subjective).
- Frames with clearly soft background or foreground (label >=1): 26/116 = 22 % (Wilson 95 % 16-31 %); strong (>=2): 4/116 = 3 % (1-9 %). Videos with >=1 soft sample: 14/30 (03,04,05,06,14,15,18,20,22,23,26,28,29,30); strongest 15 and 29 (4/4).
- By shot type (C close-up = head >40 % width, M medium, W wide, X macro/object): C 12/17 soft (71 %, 47-87 %); X 4/14 (29 %); M 7/46 (15 %); W 3/39 (8 %). Shot mix of sample: C 15 %, M 40 %, W 34 %, X 12 %.
- Wide and medium scenes (RC30-04, 06, 10, 21, 22 sheets) have crisp backgrounds to the horizon; look is engine-render "deep focus" plus ink-outlined cards.
- Implementation: default DOF off for W/M; enable for C and macro (see TECHNIQUES). Aperture is a per-shot-type switch, not a global setting.

## F-A07-002: Real focus pull / blur-resolve exists but is rare
- OBSERVED. Confidence: low (1 clear case).
- RC30-15 f001075..f001125: background characters and bed blurred while the foreground frog is sharp (f001085), background sharpens by f001105 (about 1 s). Probably combined with a crossfade. RC30-21 f000419 sheet tile: blurred foreground banner at frame edge. RC30-10 f000299/f000329: fast streak/blur on cuts (motion blur, not DOF).
- Search method: smoothed log lap_var ramps (>2.5x in 20 frames, no cut candidate) in the 6 videos having sharpness.csv (15,23,25,27,28,30): 21 ramps; 3 viewed: RC30-23 f158-198 = unflagged hard cuts, RC30-25 f445-465 = fog-veil dissolve then dolly-in (haze clearing), RC30-15 f1085-1105 = genuine focus pull. 18 ramps unviewed (open).
- Implementation: animate bokeh scale 0 -> 6 px@1080 / focus distance over 24-30 frames at cut-in; use sparingly.

## F-A07-003: Background blur magnitude, only coarse
- MEASURED (proxy, weak). Confidence: low.
- Gaussian blur calibration on native cells (n=92, calib_curve.json): normalised Laplacian energy falls to 0.47 at sigma 0.5 px, 0.08 at 1 px, 0.01 at 2 px, so the proxy saturates above about 2 px@1080. Sampled frames: median bg/ref ratio 0.42 (IQR 0.23-0.65) for deep-focus frames vs 0.21 (0.06-0.39) for soft frames, i.e. sigma_eq about 0.5 vs 0.7 px: overlap too large (AUC 0.63-0.72, see FAILED). I cannot give a measured px sigma for defocus.
- INFERRED from tiles: soft backgrounds look like roughly 6-12 px@1080 blur (details unreadable, shapes and lights remain). HYPOTHESIS, to be tested with edge-spread on native crops.

## F-A07-004: Camera height is mostly eye-level to character; high angles ~1/5, low ~1/6
- OBSERVED. Confidence: medium (n=116, 30 videos).
- E (camera near character-body height) 74 (64 %), H (looking down, desk/plinth/aerial) 23 (20 %), L (low, ground plane and rails dominate) 19 (16 %). Low is typical of exteriors (RC30-04, 10, 14, 24, 07); high of rooms and gags (19 office tilt-down, 13 plaza, 18 top-down card table, 20 room).
- Dutch/roll tilts: RC30-19 f000479, f000629 and 28 (from A06).

## F-A07-005: Horizon sits above centre, median 38 % from top
- MEASURED on frames with a visible horizon. Confidence: low-medium (n=17 labelled, 9 videos; plus 9 detected-line checks).
- Labelled horizon y (fraction from top): median 0.38, IQR 0.25-0.43, range 0.20-0.65 (RC30-04 0.40-0.42, 24 0.43-0.50, 10 0.37, 12 0.20-0.28, 06 0.27-0.33, 08 0.47, 29 0.55, 07 0.25). Low-angle shots put the horizon at 0.25-0.45; character feet then sit in the lower 40 %.
- Implementation: camera pitch ~0 with a shift (principal point ~ 0.55-0.6 H) or pitch down 3-8 degrees at height ~ character mid-height.

## F-A07-006: Atmospheric haze is a colour shift of far ground toward sky, not a contrast loss
- MEASURED. Confidence: low-medium (9 frames from 6 videos: 04, 06, 08, 10, 12, 24, 29; haze lines viewed in strip).
- dE76(Lab) to sky-at-horizon colour: far ground band (just under horizon) median 28.8 (IQR 24.9-58.3) vs near ground 86.3 (54.4-101.0); haze_delta (near minus far) median 29.5 (16.4-53.4); far/near ratio median 0.55 (0.40-0.66). Strongest RC30-08 f001830 (far 16 vs near 101, ratio 0.16: distant tower and hills nearly sky-coloured) and RC30-04 f000209 (road and fields bleach toward pale sky).
- Chroma and local contrast: no consistent far<near drop (far chroma lower in 5/9, contrast lower in 4/9): hence haze here is mostly lightness/hue blend with the sky, with texture kept.
- Whole-dataset grid: top row vs bottom row median saturation 119 vs 126, L 116 vs 98, chroma 27.8 vs 23.9 (n=30 video medians): no strong global falloff; frames are not systematically hazy.
- Stylised fog: RC30-25 uses a dense red/pink haze veil as a theme (corridor, f000509-f000689), RC30-11 underwater blue, RC30-14 backlit dust f000779-f000869.
- Implementation: THREE.Fog (linear) with colour = horizon sky colour; near 8-15 m, far 150-400 m for open landscapes; none in interiors.

## F-A07-007: Perspective and lens feel: strong perspective, wide field of view
- OBSERVED. Confidence: medium for "wide", low for any degree value.
- Road/rail/corridor convergence, big near-object scale (RC30-10 f000449 head vs rails, RC30-04 f000779 cab, RC30-25 corridor f000509) and stretched box corners (RC30-19 f000479, f000629) indicate a wide lens. HYPOTHESIS: vertical FOV 55-80 degrees (about 24 mm-equivalent or wider); no vanishing-point FOV solve was done (open).
- Tele/compressed look appears only in macro (RC30-05 f000869-929, RC30-06 f000569) via DOF, not by FOV.

## F-A07-008: Depth ordering: foreground framing and occlusion are used constantly
- OBSERVED. Confidence: medium-high (all 15 sheet videos).
- Patterns: (a) foreground silhouette at frame edge (grass RC30-04/06, tree trunk RC30-04, rail sleepers RC30-10, bars RC30-21 f001139, desk edge RC30-19/12); (b) props occlude lower body of cards (counters, desks); (c) over-the-shoulder close heads in the edge of frame in two-shots (RC30-12 f000209, 15, 29); (d) circular lens vignettes (binoculars RC30-12 f000389, f000569).
- A06 already covers card sorting; here: always keep 2-3 depth planes (near framing at 0.5-2 m, subject, far backdrop).

## Open questions
Edge-spread sigma on native crops of soft frames; remaining 18 ramps; FOV from vanishing points; DOF vs camera-motion (motion blur) separation; per-shot-type horizon.
## Contradictions
Weak numeric proxy vs strong visual labels for defocus (F-A07-003): not averaged; visual labels used for shares, numbers withheld.
