# A14 Composition and framing: FINDINGS (Phase 3, RC30)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` | date 2026-11-28 | agent a14-composition-framing-specialist
Visual ledger: 42 records in `knowledge/dataset/coverage/visual/a14-composition-framing-specialist.jsonl` (30 overview sheets page 1 = t 1..40 s; 6 every-frame sheets; 6 montages of 44 native frames with grid/safe-zone overlay).
Videos covered: shot-size tally 30/30 (first 40 s each; videos 25 and 27 complete, 23, 24, 26, 28-30 ~85-100 %, 1-22 ~60-65 % of runtime); native placement 22 videos (01,02,03,05,06,07,08,09,10,12,14,15,16,18,19,20,21,23,25,27,29,30); caption band 44 natives/22 videos; camera framing sheets 6 (15,23,24,26,28,30) + motion tables 8 (15,23-28,30).
Data: `data/shot_size_tally.csv`, `data/subject_placement.csv`, `data/caption_bbox_native.json`, `data/camera_motion_framing.csv`.
Method note for all "viewed" numbers: eye annotation on a 10 % grid, estimated error about +/-0.03 (x, y). Labels are visual judgements; the saliency result is an aid only.

## Shot-size definition used (consistent across the 30 videos)
Character-based, using the main character's head height (hh, fraction of frame height; heads are large round white discs, so hh is a stable scale):
- EWS: environment dominates, any figure < ~5 % of frame height or none (landscape, space, cross-section, aerial).
- WS: whole figure(s) visible and small, hh < 0.10.
- MS: hh 0.10-0.20 (figure from knees/full body to waist; group shots of 2-4 characters).
- CU: hh > 0.20 (head and shoulders, face-dominated). ECU (hh > 0.45, face fragment) is merged into CU in the tally (2/44 natives were ECU).
- INSERT: prop / screen / document / object detail with no character face as subject (macro detail is merged here).
Tally unit = one 1 fps overview tile (time-weighted, not shot-count). Boundary hh 0.20-0.22 is fuzzy (e.g. RC30-14-f000299 labelled MS at hh 0.22).

## F-a14-001 Shot-size mix: medium shots dominate, no video is single-size
Claim: Time-weighted over 1,188 one-second tiles (30 videos): MS 39.2 %, WS 21.3 %, INSERT 14.3 %, CU(+ECU) 13.2 %, EWS 12.0 %. Per-video median (IQR): MS 37.5 % (32-45), WS 21 % (12.5-27.5), CU 13.6 % (7.5-17.5), INSERT 12.5 % (5-22.5), EWS 10 % (2.5-15). MS present in 30/30 videos, WS 29/30, CU 28/30, INSERT 28/30, EWS 24/30.
Label: OBSERVED (tiles viewed, hand-tallied). Confidence: medium-high (n=30 videos, n=1,188 tiles; tally by one rater; seconds 41-77 not viewed).
Evidence: overview sheet 1 of every video, `data/shot_size_tally.csv`; ledger 30 records.
Exceptions: EWS-heavy RC30-25 (46 %, corridor/bloodstream), RC30-08 (35 %), RC30-04 (25 %), RC30-24 (25 %); INSERT-heavy RC30-27 (39 %), RC30-16 (35 %), RC30-05 (25 %); CU-heavy RC30-19 (25 %), RC30-16 (25 %), RC30-27 (29 %); no CU at all in RC30-03 and RC30-26.
Limitations: first ~40 s only for videos 1-22; counts are 1 fps samples; MS/CU boundary subjective.
Implementation: use the mix as a target band per 60 s short (TECHNIQUES.md section 2); define size by head height in the storyboard so the camera/Remotion framing can be verified numerically.

## F-a14-002 Faces sit in the centre third, above centre; headroom is moderate
Claim (44 native frames, 22 videos): main-face centre x median 0.48 (IQR 0.36-0.51; range 0.19-0.78); 34/44 inside 0.33-0.67; 26/44 inside 0.40-0.60; 8/44 left of 0.33, 2/44 right of 0.67 (no strong right bias). Eye line y median 0.38 (IQR 0.32-0.47; range 0.20-0.65); 26/44 in the upper-third band 0.20-0.40. Head top y median 0.30 (IQR 0.20-0.37). Head height median 0.21 (IQR 0.16-0.26). Headroom is therefore ~0.2-0.37 of frame height in typical frames; head cropped by top edge in 1/44 (RC30-29-f000059 head top 0.09, magnifier close-up; RC30-09-f000599 giant head intentionally cropped).
Label: OBSERVED (annotated on gridded natives), estimated error +/-0.03. Confidence: medium (n=44 frames chosen where a face is visible, so close shots over-represented: labels CU 23, MS 18, WS 2, ECU 1; not a random sample of all frames).
Evidence: `data/subject_placement.csv` (frame IDs there), ledger montage records.
Exceptions: strong left-third placement 8 frames (e.g. RC30-01-f000029 x 0.28, RC30-23-f000479 x 0.19, RC30-27-f000089 x 0.28, RC30-08-f000689 x 0.29), used when a prop or second character takes the other side; right-edge faces RC30-27-f000479 (0.78, clipped) and RC30-29-f000509 (0.77).
Contradiction check: none.
Limitations: face centre is a visual estimate; multi-character frames use the primary (largest or speaking) character.
Implementation: eye line target y 0.30-0.47 (storyboard "eye row"), head top 0.20-0.37; centre-third default, off-centre only with a counter-weight (prop, second character, sign).

## F-a14-003 Burned-in caption band: fixed at y 0.689-0.724, centred, single line, never moves
Claim: In 44/44 native frames (22 videos) the caption text bbox top is at y median 0.689 (IQR 0.6885-0.690; range 0.674-0.696) and bottom at median 0.717 (IQR 0.717-0.724; range 0.717-0.738), i.e. pixel rows about 1323-1380 of 1920 for a single line (about 57 px tall incl. outline, white fill with thick black outline). Same position regardless of shot size or camera motion (confirmed on 6 every-frame sheets: caption static while the scene moves). Caption sits 0.26-0.31 above the bottom edge, so it clears the bottom 20 % UI zone by about 0.08.
Label: MEASURED (white-pixel-with-black-neighbour mask in the 0.50-0.85 height band, `analysis` script in scratchpad, input natives from get_frames; y values only) + OBSERVED on 42 tiles of overview sheets (caption at ~0.67-0.70 of tile in every video). Confidence: high for y (consistent 44/44, 22 videos). 
Limitations: x extent from the mask is unreliable (merges with white scene pixels; see FAILED.md) so width and centring are OBSERVED only: one to three words, centred. Two-line captions not seen in the tiles reviewed.
Implementation: reserve rows y 0.672-0.74 (1290-1420 px) in all Remotion compositions; see TECHNIQUES.md overlay.

## F-a14-004 Key content avoids the bottom and top UI zones; the right strip is crossed by big close-ups only
Claim (44 natives, 22 videos): bottom 20 % (y > 0.80): 0/44 heads reach into it (head bottom median 0.51); caption band overlapped by a head 2/44 (head bottom in 0.685-0.725: RC30-02-f000149 face under a lifted vault lid, RC30-25-f000029) and eye line inside the caption band 0/44, face centre y > 0.65 in 0/44. Top 8 %: head top < 0.08 in 1/44. Right 15 % (x > 0.85): the head box crosses it in 5/44 frames (11 %: RC30-09-f000329, -16-f000509, -20-f000539, -27-f000479, -29-f000509), all CU or edge-placed; face centre never beyond 0.78. Torsos, legs, floor and props routinely occupy the bottom 20 % and the caption band (legs/floor visible in most MS and WS tiles).
Label: OBSERVED + INFERRED (zone thresholds are the director's assumptions, not measured from the platform; no platform documentation consulted). Confidence: medium (n=44, selected frames).
Interpretation: the author keeps faces and eyes clear of the caption and bottom zone; the caption is placed at 0.70 so the lower 30 % can hold feet, props, floor decoration.
Implementation: safe rectangle for faces/eyes/hands, TECHNIQUES.md section 1.

## F-a14-005 Saliency check: the face wins over the caption in most frames
Claim: Spectral-residual saliency (own numpy implementation, 128x228) on the 44 natives: the head box holds median 36 % of the top-10 %-salient pixels (median 4.4x its area share; > area share in 44/44); the caption band (0.685-0.725 full width, 4 % of area) holds median 13 % (3.1x area); caption out-weighs the head in 4/44 frames.
Label: MEASURED (aid only; head boxes are hand-annotated). Confidence: low-medium (single method, black/white outlined text inflates saliency, head box approximate). Not a substitute for visual judgement.
Implementation: run the same test on our storyboard frames (script described in TECHNIQUES.md); reject frames where caption share > head share.

## F-a14-006 Visual hierarchy devices (frequency across the 30 overview sheets)
All OBSERVED (sheet 1 of all 30 videos; count = videos with at least one clear example, not frame share). Confidence: medium (counts by one viewer at 180x320).
1. Frame-within-frame (window, porthole, door, arch, jail bars, circular vignette/peephole/binocular): >= 16/30 videos. Examples RC30-01 (porthole t29), -12 (telescope circles t13, t19-20), -18 (round vignette t13-14), -20 (peephole t22-23), -21 (cell bars t38-40), -28 (portholes t9-11), -26 (doorways), -19, -06 (gate arch), -09 (cell door).
2. Foreground occluder / large blurred or cropped foreground object on a frame edge (cannon, pot, couch, car, rails, grass, hatch lid, benches): >= 12/30. Examples RC30-03 t36-40, -11 (pot/cannon), -20 (couch), -02-f000149 (vault lid overhead the face), -07, -09 t33-38 (guards in front). Cross-reference F-A07-008 (A07: foreground framing and occlusion used constantly).
3. Leading lines / one-point perspective: >= 13/30 (road RC30-04 t6-9, highway -07, rails -10 and -24, corridor -25, aisle -26 t5-8, carpet -21 t14-16, racetrack -12 t14-15).
4. Symmetry / centred axis: >= 10/30 (corridor RC30-25 t17-33, pachinko aisle -26, concentric town -13 t5-8, throne -21, rings floor -30, vault door -02).
5. Tilted (dutch) framing: static dutch >= 8/30 (RC30-28 t1-6, -10-f000719, -14 t5-20, -11 t31-34, -19 t24-29, -08 t19-25, -13 t13-16). Camera roll measured in 8 videos: median |roll| 0.54 deg/s, > 2 deg/s in 19 % of 1 s windows, > 5 deg/s in 6 % (MEASURED, proxy 320 px, `data/camera_motion_framing.csv`); the strongest roll is RC30-28 (44 % of windows > 2 deg/s).
6. Subject contrast: the near-white head disc with thick dark outline is the highest-value shape in the frame in most shots; dark or saturated, low-key scenes (night, RC30-03, -13, -20, -25, -26, -30) raise this further; warm-body vs cool-background complementary pairs appear (orange/blue RC30-26-f000779, yellow/blue RC30-29-f000509). Not measured numerically.
Limitations: tile size hides small devices; counts are lower bounds.
Implementation: storyboard template field `devices` (frame / occluder / lead-lines / symmetry / dutch / contrast) with at least one per shot; dutch only in action beats, roll <= 5 deg/s.

## F-a14-007 Framing changes inside a shot: slow push-in with the subject held in the centre third
Claim: On six every-frame sheets (RC30-24 f384-431, -26 f384-431, -30 f192-239, -28 f240-287, -23 f384-431, -15 f528-575, 1.6 s each) the camera is almost never still but the change over 1.6 s is small: (a) RC30-30: head top 0.13 to ~0.15, head height up ~10 %, subject stays x 0.50; (b) RC30-24: scene pushes forward along the rails, king stays on the left third line (x ~0.30) and grows ~+30 %; (c) RC30-26: doorway shot pushes in with fixed subject x, then a 6-frame crossfade to the next shot whose subject starts at x 0.5, head top 0.33 and settles lower (0.42) as it pushes; (d) RC30-23: strongest push, stall and characters scale up ~+35 % while the caption stays fixed at y 0.70; (e) RC30-15: almost static with 6-frame dissolve to a new composition; (f) RC30-28: rolling + panning, subject (brain) moves from centre to the lower right edge and is partly cropped at the end of the window. Start and end framing therefore differ by scale (typically +10-35 % over 1-2 s), small pan (|dx| < ~0.1 of width) and, only in action shots, roll.
Computed (MEASURED, proxy <= 320 px, 8 videos, 303 one-second windows): cumulative zoom median 12.4 %/s (IQR 5.5-35.3 %/s, p90 65 %/s); zoom-in 71 %, zoom-out 26 %, near-static 4 % of windows. Caveat: windows include crossfade frames, parallax and subject motion; the visual check (RC30-15, -30: ~5-10 % in 1.6 s) is lower than the table value, so the table is an upper bound (see Contradictions).
Label: OBSERVED (6 sheets) + MEASURED. Confidence: medium (6 sheets, 8 tables, 1.6 s windows).
Implementation: author both a start frame and an end frame in the storyboard (see template); the end frame must still pass the safe-zone check; default push 10-35 % over the shot, subject x held +/-0.05; hand motion parameters to A13.

## F-a14-008 (withdrawn)
A first-tile (t = 1 s) opening-size count was not done carefully; withdrawn. Opening staging stays with A19.

## Contradictions
- Zoom: motion tables (median +12 %/s, 8 videos) versus eye reading of sheets (about +5-10 % over 1.6 s in RC30-15 and -30). Both kept; table is an upper bound because of proxy resolution and parallax. Does not change a rule (we recommend 10-35 % per shot as a design target, flagged low-medium).
- Right-side placement: reference faces do not avoid the right 15 % strongly (5/44 cross it), which is not consistent with a strict "keep everything out of the right strip" rule; our rule keeps faces/eyes out of it but allows decorative parts of big heads.

## Open questions
1. Shot-size time series (seconds 41-77) and per-beat rhythm need the page-2 sheets (not viewed) or A27 shot boundaries.
2. Platform UI zone sizes (right 15 %, bottom 20 %, top 8 %) are the director's assumptions; verify against current platform documentation before locking.
3. Whether the head-top median 0.30 is a deliberate rule or a side effect of the fixed caption at 0.70 (INFERRED link, untested; a controlled A/B head top 0.25 vs 0.35 would test it).
