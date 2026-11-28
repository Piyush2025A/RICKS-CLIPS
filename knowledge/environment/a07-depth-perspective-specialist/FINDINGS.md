# A07 FINDINGS: depth and perspective (Phase 3, partial)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual-ledger records: 27 after 3B (22 before; `knowledge/dataset/coverage/visual/a07-depth-perspective-specialist.jsonl`).
Computational: native 4x3 grid stats (rows 0-20/20-40/40-58/82-100 % of height; caption band excluded) every 10th frame (RC30-01..04) / every 30th (05..30): 26,226 cell rows, 30/30 videos. Scripts + small JSON in `data/` (v0.1). Visual: 15 videos on 1-fps overview sheets (03,04,05,06,08,10,12,13,14,17,19,21,22,25,30), 3 random-sample montages (120 frames, seed 7, all 30 videos, 116 labelled), 3 rack-focus strips, 1 horizon check strip.
Limits common to all: labels are mine from 180x320 tiles; per-video n is 3-4 frames; sheets only (no 4x native zoom).

## F-A07-001 [SUPERSEDED numbers: see F-a07-100/101; 22 % soft share is an over-call from 180x320 tiles]: Most frames are deep focus; visible defocus is a minority, concentrated in close-ups
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

## F-A07-003 [SUPERSEDED by F-a07-100: edge-spread now gives px values]: Background blur magnitude, only coarse
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
- Tele/compressed look appears only in macro (RC30-05 f000869-929 [3 overview tiles only, 1 fps, not native], RC30-06 f000569) via DOF, not by FOV.

## F-A07-008: Depth ordering: foreground framing and occlusion are used constantly
- OBSERVED. Confidence: medium-high (all 15 sheet videos).
- Patterns: (a) foreground silhouette at frame edge (grass RC30-04/06, tree trunk RC30-04, rail sleepers RC30-10, bars RC30-21 f001139, desk edge RC30-19/12); (b) props occlude lower body of cards (counters, desks); (c) over-the-shoulder close heads in the edge of frame in two-shots (RC30-12 f000209, 15, 29); (d) circular lens vignettes (binoculars RC30-12 f000389, f000569).
- A06 already covers card sorting; here: always keep 2-3 depth planes (near framing at 0.5-2 m, subject, far backdrop).

## Open questions
Edge-spread sigma on native crops of soft frames; remaining 18 ramps; FOV from vanishing points; DOF vs camera-motion (motion blur) separation; per-shot-type horizon.
## Contradictions
Weak numeric proxy vs strong visual labels for defocus (F-A07-003): not averaged; visual labels used for shares, numbers withheld.


## Phase 3B additions (2026-11-28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`. Ledger 27 records, 30 videos with some visual evidence (mostly 1-fps/overview or 200x356 tiles; native-resolution frames are NOT individually viewed in 3B, only 540x960 downsampled JPG tiles). Computational (not visual): native 1080x1920 edge-spread on 581 frames (every 90th frame, all 30 videos, 12 cells/frame, caption band 58-82 % excluded); scripts `scripts/` (edgesigma.py in `scripts/`), tables in `data/`.

### F-a07-100: Edge-spread blur metric works; in-focus floor is about 1.0-1.7 px, and 91 % of sampled frames have no cell above 2.5 px
- MEASURED. Confidence: medium (30 videos, n=581 frames, 5,269 cells; validated by synthetic Gaussian blur of native frames, RC30-04 f300/f900).
- Method: Canny edge points per 3x4 cell, sigma = contrast / (2.507 x peak gradient) along the gradient (contrast = profile max-min within +-10 px). Calibration (added Gaussian s -> measured, px@1080): 0 -> 1.65, 1 -> 1.77, 2 -> 2.3, 3 -> 3.0, 4 -> 3.95, 6 -> 5.4; above about 8 px too few edges survive (cell becomes "unmeasurable", so large blur is under-counted). Cell sigma distribution: median 1.43, IQR 1.24-1.68, p95 2.09, p99 3.57.
- Frames with max cell sigma >= 2.5 px: 53/581 = 9.1 % (23 videos); >= 3: 38/581 = 6.5 % (18 videos); >= 4: 13 = 2.2 % (10 videos). Viewed on 2 stratified montages (80 frames) and a top-39 montage: the max-sigma ratio alone does NOT separate blur from content (flat or hazy cells give 2-3 px), so thresholds 2.5-3 are upper bounds on shallow-DOF share.
- Implementation: treat 1.0-1.7 px as "sharp" (ink outline after YouTube encode); simulate DOF only when you want > 3 px.

### F-a07-101: DOF classes and blur magnitude (px@1080, added sigma beyond in-focus, 31 hand-labelled frames of the top-39 montage)
- OBSERVED labels + MEASURED sigma. Confidence: low-medium (n=6/6/14 per class; labelling at 200x356 tiles; cell sigma only measurable up to about 8 px, so macro values are lower bounds).
- deep (default, about 90 %): added sigma 0; look = render with ink outlines, background to horizon sharp.
- shallow-bg (character sharp, town/stadium/room soft; RC30-13 f810,1170,1260,900,360; 14-990, 14-1440; 17-900,1170; 29-1260; 20-1620; 02-0; 18-90; 16-0): added sigma median 3.6 px (IQR 3.3-4.0, range 2.7-5.0).
- shallow-fg (blurred near object at frame edge, subject sharp; 14-90, 14-450, 14-270, 18-270, 18-1710, 28-1080): median 3.9 (3.2-4.2, 2.9-4.8).
- macro (object or eyes fill frame, bg black or blurred; 30-360, 21-630, 11-1530, 15-1440, 27-360, 28-180): median 4.0 (3.0-4.8, 1.3-5.3); 30-360 raw cell sigma 5.1-5.2 with most other cells edgeless, so true blur there is larger (HYPOTHESIS about 8-12 px).
- Control: 5 frames flagged by the metric but visually deep (14-1350, 14-180, 08-630, 04-1440, 14-0; haze or low-contrast far scenery) gave 2.8 (2.7-2.9): not separable from shallow-bg numerically; the label is visual.
- Typical DOF look is therefore mild: about 3-5 px@1080 (0.3-0.45 % of width), far below the 6-12 px earlier guessed in TECHNIQUES. Scale by output height/1920.
- Implementation: bokehScale/Gaussian sigma 3-4 px@1080 on the far plane for shallow-bg; 4-5 px on the near plane for shallow-fg; macro up to 8+ px.

### F-a07-102: Soft-frame share revised from 22 % to about 7-9 % (upper bound), 18-23 of 30 videos
- MEASURED (computational) + OBSERVED cross-check. Confidence: medium for the order of magnitude, low for the exact share.
- Edge metric over all 30 videos (n=581, uniform 1 per 3 s): 6.5 % (sigma >= 3) to 9.1 % (>= 2.5). Concentrated: RC30-13 (6 of its frames), 14 (13 of its frames), 18 (6), 28 (4); videos with none >= 3: 12 of 30. The old visual 22 % (n=116, 180x320 tiles) counted mild bokeh, painterly and atmospheric softness: CONTRADICTION recorded, both retained (visual 22 % vs edge 6.5-9 %); the edge value is preferred because it has a calibrated method. Overview-tile re-check (3B): no additional shallow-DOF frames identified beyond those in the 3 montages.
- Limit: every 90th frame (n=581, 1.1 % of frames); cells with flat fill are unmeasurable so macro shares are under-counted.

### F-a07-103: Camera-move parallax comes in two regimes: rigid drift (ratio about 1) and layered dolly/orbit (ratio far from 1)
- MEASURED (proxy flow on 540x960 pairs 5-26 frames apart, Farneback; far = textured pixels in top 35 % of frame, near = bottom 18 %; windows from rcpipe motion.csv lateral detector and A13 moves_table). Confidence: low-medium (32 pair measurements, 10 videos: RC30-02, 05, 11, 13, 16, 20, 23, 24, 26, 29; 12 pairs viewed as flow heatmaps).
- Rigid drift (22 pairs, 8 videos, median shift 4.5 px@1080 per 5 frames): top/bottom displacement ratio median 0.85 (IQR -0.53..0.99; clean windows 11, 13, 16, 20, 29 give 0.9-1.35), p90-p10 flow spread 5.6 px (proxy), i.e. the picture moves as one plate: cards, UI plates, lock-off slow pans. No depth-dependent shift.
- Layered motion (10 pairs, 5 videos: 02, 05, 20, 23, 24; median shift 54 px@1080 per window half): top/bottom ratio median 0.48 (IQR 0.05-0.82), values -8 to +6; p90-p10 spread 61 px (proxy) versus shift 27: near floor, props and far backdrop move at clearly different rates, and in 2 of 10 the signs are opposite (orbit around the subject). Heatmaps (RC30-02 f1485-1576, RC30-05 f576-611, f1198-1238) show 3 bands: far wall/mountain, subject plane, foreground floor.
- Implication for a Three.js scene: lock-off drift needs no depth; for dolly/orbit moves keep a clear near/subject/far depth stack so that near:far shift ratio is at least 2:1 (near layer at 0.5-2 m, subject 3-6 m, backdrop >= 20 m; shift ratio = Z_far / Z_near for pure truck). INFERRED.
- Limit: top/bottom regions are a proxy for far/near; moving characters and cuts inside windows add noise (A13 windows with shift > 50 px are partly cuts). Not a measured per-object ratio.

### F-a07-104: FOV, automatic two-vanishing-point solve gives median 73 degrees vertical (13 frames, 7 videos): TARGET (15 frames, 10 videos) NOT MET
- MEASURED (LSD + RANSAC on 540x960, principal point = centre, both VPs near the same horizon, f^2 = -(v1-c).(v2-c)); of 581 frames only 13 pass strict filters (RC30-06 x4, 10 x3, 11 x2, 07, 12, 13, 22). Confidence: low (7 videos, n=13; horizon lines drawn and viewed on all 13, plausible in about 8, doubtful in 3).
- vFOV median 73 (IQR 62-83, 10-90 % 38-90, range 31-121); the median supports the "wide" label of F-A07-007 (about 24 mm equivalent on a 9:16 sensor). Spread reflects solver instability and genuine per-shot lens changes (RC30-11 f630 121 degrees ship deck, RC30-13 f1260 31 degrees centred plinth).
- Unresolved: FOV per shot class; needs manual or more robust solve.

### F-a07-105: Atmospheric depth, no new measurement in 3B
- Not re-measured (time); F-A07-006 stands (n=9, 6 videos, low-medium). The 13 frames of the FOV montage and the 39 DOF frames show distant town/mountain bands bleaching toward sky colour (RC30-04 f1440, 06 f1890, 14 f1350) consistent with it, OBSERVED only. The brief target of 10 frames in 10 videos is not met.

## Phase 3B revisions
- F-A07-001: numbers SUPERSEDED (22 % to 7-9 %; per-class shares C 71 %, X 29 %, M 15 %, W 8 % no longer supported as shares of DOF, only as relative ordering, visual and low). Confidence stays medium for "mostly deep focus", now backed by an edge metric.
- F-A07-003: SUPERSEDED by F-a07-100/101 (measured 3-5 px added sigma, not 6-12 px guess).
- F-A07-007: FOV hypothesis 55-80 degrees upgraded to measured median 73 (low confidence, n=13); the RC30-05 f869-929 tele/macro claim rests on 3 overview tiles (1 fps), not native frames (A28 ledger note).
- Ledger: RC30-09 f689 was a parse artefact: the cited f000509-f000689 range in F-A07-006 belongs to RC30-25 (overview tiles f509...f689, all = 29 mod 30, in the ledger). A28 #17 "UNCHECKABLE": now re-checked computationally (contradiction above).
- Ledger coverage statement: 30 videos with visual evidence of any kind; native-resolution full-frame views by A07: none (min view 200x356, max 270x480); all 3B views are downsampled tiles and overlays.
