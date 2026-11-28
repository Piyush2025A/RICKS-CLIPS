# A03 FINDINGS: proportions (Phase 3, wave V1, TRUNCATED at turn limit)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A03.
Visual ledger: `knowledge/dataset/coverage/visual/a03-anatomy-proportion-specialist.jsonl` = 97 records (64 overlays of native frames, 33 overview/contact sheets). Phase 3B: 27 videos have native-frame overlays (26 with measured figures); 18, 27, 30 sheet only (overview sheet 1, t=1-40 s). Videos measured (landmark rows): 26/30.
Videos measured: 04, 07, 11, 14, 21, 23, 26 (7/30). Viewed on sheets only: 18, 27, 29. This is below the 15-video / n 25-40 target: all numbers are LOW-MEDIUM confidence.
Method: manual landmarks (native px, read off a 100 px grid overlay, +-8-10 px) in `data/landmarks.csv` (22 figure rows, 15 frames); ratios by `data/ratios.py` -> `data/ratios.txt`. Unit = head width (HW) because hats hide the skull top. Repeat-annotation check NOT done (error estimate below is from f719 vs f749 consistency only).

## F-a03-001 Head shape (MEASURED, low-medium) [SUPERSEDED by F-a03-101: n=12 rows was 9 characters]
Head H/W (hair counted, hats excluded, front view): median 0.93, IQR 0.89-0.98, n=12 (07, 14, 21, 23, 26). Slim n=7 median 0.94. Head is a slightly wide oval/circle; H-UP 0.93 is consistent (the hypothesis is supported, not proven). Outlier 23-f000029 1.08 (small figure, likely reading error).

## F-a03-002 Total height ~3 head widths (MEASURED, low) [SUPERSEDED by F-a03-102]
Height (head top to sole) / HW: median 2.97, IQR 2.93-3.04, n=8 (slim 07-839 2.88, 26-749 3.01/3.32; tall 14-959 2.95; priest 23 2.95/3.00/3.13). In head heights (HH = HW/0.93) about 3.2. This refutes H-UP 3.5 HH for this sample (n small, pose/perspective noise).

## F-a03-003 Torso (MEASURED, low-medium; front, stand/dynamic)
Torso width / HW: slim 0.65 (IQR 0.65-0.66, n=9); stout 0.85 (n=3, 0.81-0.89); tall 0.75 (n=3); robe-pill 0.74 (n=3). Torso length (chin to pill bottom) / HW: slim 0.85 (0.82-1.00, n=9); stout 0.84 (n=3); tall 0.84 (n=3); robe 1.65 (n=3, 1.62-1.69). The torso is a pill about 0.65-0.85 of head width and ~0.85 of it long.

## F-a03-004 Legs (MEASURED, low) [SUPERSEDED by F-a03-103]
Leg length (pill bottom to sole) / HW: slim 1.22 (1.16-1.29, n=6); stout 1.27 (n=3); tall 1.26 (n=2); robe 0.40 (n=3). Leg fraction of height: slim 0.38 (0.37-0.40, n=4); tall 0.43 (n=1); robe 0.135 (n=3). Legs are 1.4-1.5x torso length for slim/tall; the A01 "2-3x" estimate is not reproduced.

## F-a03-005 Archetype classes
Slim (default), stout (cop 04, captain 11: torso 0.85 HW, wider), tall (14 cowboys: torso 0.75, legs longest, 0.43 of height), long-robe (23 priest, 21 officials: robe pill 1.65 HW long, legs 0.4 HW, hides legs). Child scale not measured (no clean frame found in my 7 videos). Class differences are mostly torso width and leg length; head H/W is shared.

## F-a03-006 Scale consistency (MEASURED, low)
Same priest in 3 shots (23-f001019, f000449, f000029): torso W/HW 0.731/0.747/0.738, torso L/HW 1.69/1.62/1.65, height/HW 3.00/2.95/3.13: rigid design scales uniformly (spread < 5%, except head H/W reading). Counter-example, possible close-up enlargement: 11 captain torso L/HW 0.84 (close f749) vs 1.14 (wide f719); 26 orange torso L/HW 0.83 (f749) vs 1.00 (f659 close). Direction is inconsistent, so treat as annotation noise (+-15%), not evidence of shot-dependent redraw.

## F-a03-007 Foreshortening / turned views (OBSERVED, low; one frame)
14-f000179: head and body turned right: torso width / HW fell to 0.51 (front 0.75 for the same character, f000959) while the head stayed a full circle (face features shifted to the edge); legs show as side stride, foot as a short horizontal line. 14-f000659 walking: head frontal, torso leans in-plane, no squash. 26-f000989: back view uses the same construction (hair-covered head, pill, hanging arms with ball hands). Bodies narrow, they are not squashed; heads keep silhouette.

## F-a03-008 Limbs and hands (OBSERVED, medium for construction; thickness NOT measured)
Limbs are single constant-width dark strokes, no taper, no knees drawn, ends with ball hands (21-f000119: hand disc ~36 px = 0.09 HW; 26-f000989 ~31 px = 0.14 HW, eyeballed, +-30%) and a short horizontal foot line or flat blob. Legs lines in 14-f000959 look ~15 px at HW 314 (~0.05 HW, eyeballed). Pill torso outline equal to limb stroke.

## F-a03-009 Hat/hair
Headgear hides the skull top in ~half of figures; wide hats (14 cowboy brim ~2x HW, 11 plume) add silhouette width without changing head size. Rig head bounding box = circle only.

## Contradictions
H-UP 3.5 HH vs measured ~3.2 HH (n=8); A01 legs 2-3x torso vs measured 1.4-1.5x (n=6-8; A01 estimated by eye). Both reported, not averaged.

## Open questions (unfinished)
Frames extracted but not measured: 04-f000149, 11-f000599, 18-f000989/f001019, 21-f000659/f000779, 27-f000059, 29 (3 frames, extraction pending). No child archetype data; no stroke-thickness script (distance transform); no 10% re-annotation; videos 01-03, 05-06, 08-10, 12-13, 15-17, 19-20, 22, 24-25, 28, 30 not measured; limb stroke/hand circles need script; 3/4 turn n=1.

## Phase 3B additions (2026-11-28)
Manifest SHA-256 `fc6f147a...8278e06`. Data: `data/landmarks_3b.csv` (60 rows, sha256 3d6e3a77...c24f6; native px; 46 frames, 19 new videos), `ratios_3b_stats.txt`, `ratios_3b_characters.csv`, `limbw_3b.csv`. Scripts `build_3b.py`, `ratios_3b.py`, `limbw.py` v1.0. Command: `python3 data/ratios_3b.py data/landmarks.csv data/landmarks_3b.csv data/limbw_3b.csv data/reannot_3b.csv data/ratios_3b`. Combined 3A+3B: 82 rows, 66 distinct characters (identity = video + person; cross-video identity not verified, generic uniforms may share a rig), 26 videos. Stats use n = characters, front view, non-seated, per-character median of rows. Landmarks read by eye on 100 px grid overlays (display 844x1500, x1.28 to native).
**Annotation repeatability (6 frames re-annotated at 2x crop):** all landmarks median 3.0 px, p90 11, max 27 px (native; chin and torso_r worst when outline is ambiguous). Derived: head H/W median 0.037, torso W 0.033, leg/HW 0.020, torso L 0.021 ratio units (max 0.09-0.17).

### F-a03-101 Head H/W (MEASURED, medium)
Bareheaded, hair counted: median 0.933, IQR 0.889-0.980, range 0.81-1.11, n=34 characters in 19 videos. H-UP 0.93 supported. Per-character repeat spread across shots 4-29 %. Medium (19 < 20 videos; error 0.037).
### F-a03-102 Height (MEASURED, medium)
Head top to sole, hatless, non-robe: 3.04 HW (IQR 2.90-3.25) = 3.27 HH (IQR 3.09-3.47), n=28 characters, 16 videos. H-UP 3.5 HH lies above Q3; 6/28 >= 3.5 (close/low-angle shots reach 4.2-5.0: 16 clerk, 19 grey suit, 03 samurai). Adults ~3.2 HH, not 3.5; wide distribution.
### F-a03-103 Torso and legs (MEASURED, medium)
Torso W/HW 0.70 (IQR 0.62-0.82) n=60, 25 videos; torso L/HW 0.89 (0.85-1.00) n=60; leg L/HW 1.23 (1.12-1.32) n=56, 24 videos; leg fraction 0.40 (0.37-0.42) n=29, 16 videos. Leg/torso-length 1.38 (IQR 1.26-1.51, n=54, 23 videos): A01 "2-3x" refuted again; 3A "1.4-1.5" confirmed. Medium: counts meet thresholds but shot-to-shot spread (e.g. 05 bowler leg 54 %, 20 dad torso L 45 %) is large.
### F-a03-104 Types (MEASURED/OBSERVED, low for small groups)
Adult n=48: torso W 0.66, leg 1.22, height 3.04 HW. Large/stout n=5: torso W 0.89 (0.77-1.21), legs 1.23. Tall n=4: torso W 0.66 (0.52-0.76), leg 1.26-2.64 (samurai 03, tophat 05 long legs). Robe n=2-3 (priest, official, bonnet woman): torso L 1.2-1.65, legs hidden. Child n=1 (08 girl in dress, red check): head 0.95, legs 0.60 HW (adult 1.22), height 2.8 HW: children are short-legged with the same head, one sample only (low). Animal/object characters (cats 15/19/20, capsule pills 25, sack 22): OBSERVED only, not measured (blurred/too small).
### F-a03-105 Limb stroke (MEASURED, low-medium)
Leg stroke width 0.053 HW (IQR 0.047-0.056), n=22 characters, 13 videos (clean scans only: 4-8 dark runs, max run <= 2.5x median; 32 of 54 rejected for clutter). About 10 px at HW 200. Consistent with the 3A eyeballed 0.05. Not visually validated.
### F-a03-106 Three-quarter (OBSERVED/MEASURED, low)
Torso W/HW at 3/4: 0.51-0.75 (n=5 rows) vs 0.70 front; head stays round (06 soldier 0.99, 29 auditor 1.15, hair mass).
### Not measured
Eye spacing and arm length (no landmarks annotated; no validated method). Videos with no measurable standing figure: 18 (counter bust/seated), 25 (bust human, blurred pills), 27 (seated on stool/cropped), 30 (seated on chair throughout) - judged from overview sheet 1 only (t=1-40 s, 1 fps); overview_2 sheets not opened.

## Phase 3B revisions
- F-a03-001: SUPERSEDED by F-a03-101 (9 -> 34 characters; median unchanged 0.93; low-medium -> medium).
- F-a03-002: SUPERSEDED by F-a03-102 (2.97 HW stays ~3.0 but IQR widened; low -> medium).
- F-a03-004 / A28 claim #12: SUPERSEDED by F-a03-103 (leg/torso 1.38 vs 1.4-1.5; medium).
- F-a03-003, -005: torso widths confirmed (0.65 slim, 0.85 stout); child now n=1.
- F-a03-006 unchanged; F-a03-008 thickness now measured (F-a03-105).
- Contradiction kept open: H-UP 3.5 HH vs measured 3.27 (IQR 3.09-3.47); not averaged.
