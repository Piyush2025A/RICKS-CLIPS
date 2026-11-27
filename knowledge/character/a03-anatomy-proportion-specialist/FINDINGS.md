# A03 FINDINGS: proportions (Phase 3, wave V1, TRUNCATED at turn limit)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A03.
Visual ledger: `knowledge/dataset/coverage/visual/a03-anatomy-proportion-specialist.jsonl` (10 overview sheets 180x320; 20 native frames viewed as grid overlays, ~844x1500 or crop 1500x972; RC30-27-f000059 viewed, not measured).
Videos measured: 04, 07, 11, 14, 21, 23, 26 (7/30). Viewed on sheets only: 18, 27, 29. This is below the 15-video / n 25-40 target: all numbers are LOW-MEDIUM confidence.
Method: manual landmarks (native px, read off a 100 px grid overlay, +-8-10 px) in `data/landmarks.csv` (22 figure rows, 15 frames); ratios by `data/ratios.py` -> `data/ratios.txt`. Unit = head width (HW) because hats hide the skull top. Repeat-annotation check NOT done (error estimate below is from f719 vs f749 consistency only).

## F-a03-001 Head shape (MEASURED, low-medium)
Head H/W (hair counted, hats excluded, front view): median 0.93, IQR 0.89-0.98, n=12 (07, 14, 21, 23, 26). Slim n=7 median 0.94. Head is a slightly wide oval/circle; H-UP 0.93 is consistent (the hypothesis is supported, not proven). Outlier 23-f000029 1.08 (small figure, likely reading error).

## F-a03-002 Total height ~3 head widths (MEASURED, low)
Height (head top to sole) / HW: median 2.97, IQR 2.93-3.04, n=8 (slim 07-839 2.88, 26-749 3.01/3.32; tall 14-959 2.95; priest 23 2.95/3.00/3.13). In head heights (HH = HW/0.93) about 3.2. This refutes H-UP 3.5 HH for this sample (n small, pose/perspective noise).

## F-a03-003 Torso (MEASURED, low-medium; front, stand/dynamic)
Torso width / HW: slim 0.65 (IQR 0.65-0.66, n=9); stout 0.85 (n=3, 0.81-0.89); tall 0.75 (n=3); robe-pill 0.74 (n=3). Torso length (chin to pill bottom) / HW: slim 0.85 (0.82-1.00, n=9); stout 0.84 (n=3); tall 0.84 (n=3); robe 1.65 (n=3, 1.62-1.69). The torso is a pill about 0.65-0.85 of head width and ~0.85 of it long.

## F-a03-004 Legs (MEASURED, low)
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
