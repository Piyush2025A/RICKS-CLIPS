# A15 FINDINGS — transitions (Phase 3 parts 1 + 2, Phase 3B 2026-11-28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A15.
(Part-2 text written to disk verbatim by the director from A15's hand-off; the agent's Write tool refused it. It
supersedes the part-1 file.) Visual ledger: `knowledge/dataset/coverage/visual/a15-transition-specialist.jsonl`
(**122 records as of 3B**, 29 videos with visual evidence (all but RC30-27, director ground truth only); was 83 part-2 + 23 part-1; 120×213 tiles cropped from rcpipe every-frame sheets, plus 180×320 overview sheets for
recall). Scripts: `src/transitions/a15_tiles.py` (+ private mk.py, gap.py, alpha2.py). Data:
`data/transitions_confirmed.csv` (**569 rows, 30 videos after 3B**; was 429 rows, 24 videos).

## Coverage (honest)
Every rcpipe candidate confirmed on every-frame tiles in 23 videos: RC30-01, 02, 03, 04, 05, 07, 08, 12, 14, 15, 16, 17,
18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30 (RC30-15 also holds the director-supplied missed dissolve). RC30-27 rows are
the director's ground truth (not re-inspected). Not processed by rcpipe at the time: RC30-06, 09, 10, 11, 13, 21 (SUPERSEDED: added in 3B, CSV now 30/30).
24/30 videos in the CSV at that time. Columns: video, cand_start, cand_end, type, notes, xf_start_alpha10, xf_len_alpha10_90. Frames
= rcpipe candidate range, not exact edit frames; notes hold visually read frames (fNNN–NNN) for most crossfades. Types:
XF crossfade, HC hard cut, ZT zoom-through/iris/scale reveal, FT fly-through, VB VFX/object cover or wipe, FP false
positive; "MISSED" rows are real transitions rcpipe did not flag.

## Counts (OBSERVED, 24 videos, 429 rows)
Real 303 = XF 228, HC 37, ZT 23, VB 9, FT 6; FP 126. Per video (XF/HC/ZT/FT/VB; FP): 01 9/5/2/1/0;3 · 02 18/1/1/0/0;1 ·
03 3/2/0/0/1;6 · 04 4/11/1/0/0;7 · 05 2/8/1/0/2;12 · 07 10/5/0/1/0;3 · 08 13/0/0/0/0;2 · 12 11/0/6/1/0;6 · 14 8/0/3/0/0;6 ·
15 18/0/1/0/1;9 · 16 13/0/1/0/0;2 · 17 16/0/0/0/0;2 · 18 10/0/2/0/1;9 · 19 18/0/0/0/0;6 · 20 11/0/0/1/0;8 ·
22 4/1/0/1/2;14 · 23 11/1/0/1/2;4 · 24 6/1/0/0/0;8 · 25 6/0/0/0/0;1 · 26 12/0/0/0/0;2 · 27 6/0/0/0/0;2 (director) ·
28 4/2/3/0/0;6 · 29 8/0/0/0/0;2 · 30 7/0/2/0/0;5.

## F-a15-001 Crossfade is the dominant joiner (OBSERVED, high; 24 videos, 303 real)
228/303 = 75 %. Hard cuts rare overall (37 = 12 %) and concentrated in a group of videos (F-a15-008). Contradicts the
RC30-27 calibration remark "0 hard cuts" only for RC30-01..07 (style varies per video). Implementation: default scene
join = crossfade.

## F-a15-002 Crossfade length (OBSERVED + MEASURED) — CONFIDENCE `high` SUPERSEDED (see F-a15-101: medium)
Visual read from every-frame tiles (n = 162 crossfades, 17 videos): median 6 frames (0.2 s), IQR 5–7, p10–p90 4–8, mode
5, range 3–23 (one outlier: a slow glow bloom). Per-video medians 4–8: slowest RC30-15 (8), fastest RC30-23 and 26 (4).
Least-squares alpha fit on 120×213 tiles (n = 220): median 10, IQR 7–12, max 30 — over-estimates because of simultaneous
camera motion and tile resolution (FAILED) → upper bound only. Endpoints by eye (±1 frame). Easing curve NOT measured.

## F-a15-003 rcpipe hard-cut candidates unreliable in videos 12–30 (OBSERVED, medium)
In 01–08 every start = end hard-cut candidate was a true cut (32/32). In 12–30 the hard_cut_candidate label (15
instances) was a real cut only 3 times (RC30-24 f840, RC30-28 f711 and f1077); the rest were 1–3-frame dissolves
(RC30-23 f940, RC30-26 f135–151, RC30-30 f368–375), scope/iris snaps (RC30-12 f549, 570, 593, 608), VFX covers (RC30-22
f541, f1793) or in-shot changes. View them. (Contradiction with part 1's "all hard-cut candidates real": both kept —
part 1 covered only 01–08.)

## F-a15-004 Camera moves and scale reveals replace cuts (OBSERVED, medium)
ZT (23) and FT (6) cluster by video. Device iris/eye/scope zoom-throughs: RC30-12 scope in/out four times; RC30-14
eye→scope and scope iris; RC30-28 eye→brain and visor door; RC30-30 eye iris→corkboard; RC30-18 scene shrinking into a
fishbowl; RC30-04 pupil POV; RC30-05 ore texture. FT: RC30-01 vent pipe, RC30-07 windshield, RC30-12 doorway, RC30-20
fast floor-to-room pan, RC30-22 cannon barrel, RC30-23 foliage push. In many dissolves the camera keeps moving through
the blend (RC30-01, 02, 16, 25).

## F-a15-005 VFX/object covers (VB 9) (OBSERVED, medium)
Muzzle flash (RC30-05 f59), dust cloud (RC30-05 f1669–1678), explosion whiteout then dissolve (RC30-03 f1728–1739),
smoke puff then reveal or circular wipe (RC30-22 f541–546, f1792–1799), foreground tree/market pillar sweeping the
frame (RC30-23 f146–155, f173–187), hat filling frame (RC30-18 f1629–1634), light-bloom whiteout then dissolve (RC30-15
f1953–1987). No pure flash edit among ~20 flash candidates (agrees with F-a12-008).

## F-a15-006 rcpipe candidate precision and recall (MEASURED, medium)
Precision 293 real / 417 candidate rows = 70 % (excludes 8 director-only RC30-27 rows and 4 missed rows); FP sources:
in-shot VFX/lighting shifts, continuous camera moves, character animation, text/overlay fades. Recall: overview 1 fps
scan + every-3rd-frame gap tiles for RC30-12, 16, 19, 23, 26 (12, 16, 19, 26 only to t = 40 s; 23 whole): 77 real,
3 missed (all RC30-23: f173–187 object wipe, f1156–1163 slow crossfade, f1099–1101 match cut) = 74/77 = 96 %. With
director ground truth (RC30-27 6/6; RC30-15 25/26 + missed f1074–1087) combined 105/109 = 96 %. Limits: 1 fps cannot
see two events in one second; all RC30-23 misses were in the tail where rcpipe gave no candidate for the last 212
frames (f1007–1219). Miss class = slow same-palette dissolves and match cuts (agrees with the calibration).

## F-a15-007 Triggers (INFERRED, low)
Crossfades at location/time/beat changes (day→night RC30-08, 17, 24); zoom-throughs at concept metaphors (eye =
memory/brain RC30-14, 28, 30; scope/lens = watching RC30-12); hard cuts within a location on dialogue beats (RC30-04,
05). Not tested against narration timing.

## F-a15-008 Style clusters (OBSERVED, medium)
(A) dissolve-only (HC ≤ 1, XF ≥ 80 % of real): 02, 08, 12, 14, 15, 16, 17, 19, 20, 25, 26, 27, 29, 30; (B) cut-mixed:
01, 04, 05, 07 (HC 25–69 %); (C) long-take continuous-camera/VFX 3D scenes with few real joins and many FPs: 03, 22 (and
05); (D) device zoom-through motifs (≥ 2 ZT): 12, 14, 18, 28, 30. HC share 32 % (32/101) in RC30-01..08 vs 2.5 % (5/202)
in RC30-12..30 incl. 27 — split along dataset order (01 newest); cause unknown (format change over time is a
HYPOTHESIS). Exceptions: RC30-02 and 08 are dissolve-only in the early group.

## F-a15-009 Shots per video and shot length (MEASURED, medium) — 24-video numbers and the per-video range SUPERSEDED (see F-a15-103; RC30-25 median is 1.28 s, not 9.1 s as range upper end)
From confirmed real boundaries (multi-part transitions merged within 15 frames; FP excluded; 24 videos, n = 322 shots):
median shot 3.06 s (92 frames), IQR 1.84–5.12 s, range 0.47–22.6 s; median 14 shots/video (IQR 9–17; 6 in RC30-03 to 21
in RC30-02 and 15); per-video median shot 2.0 s (RC30-01) to 9.1 s (RC30-03), 6.3 s (RC30-22). Limits: hard cuts missed
by rcpipe and scene changes by continuous camera moves are not counted (RC30-03, 22 look long).

## F-a15-010 Crossfades combine with moves or colour washes (OBSERVED, medium)
RC30-14 f1318–1342, RC30-29 f295–302, RC30-19 f69–76, RC30-15 f706–718 (vertical-streak shimmer); blend length stays
≈ 6 frames, the move carries the join.

## Ambiguities
RC30-12 f1102–1106 (XF, low); RC30-17 f1171–1182 (XF, low); RC30-18 f1307–1311 (ZT, low); RC30-20 f808–817 and
f855–864 (light-sweep overlay, FP); RC30-24 f567–608 (in-shot grade, FP); RC30-23 f1099–1101 cut frame not isolated.

## Open items
~~RC30-06, 09, 10, 11, 13, 21~~ (done in 3B); overview scan beyond 40 s for 12, 16, 19, 26 and the other 17 videos; native-resolution
crossfade endpoints; easing curve; narration alignment (A16/A20); hard-cut recall in 03 and 22.

## Phase 3B additions (2026-11-28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`. Scripts: `src/transitions/a15_stats.py`
(counts + shot length, reproducible: `python3 src/transitions/a15_stats.py`), `src/transitions/a15_tiles.py` (tiles),
private `agents/a15-transition-specialist/gap3b.py` (gap check). Data: `data/transitions_confirmed.csv` (569 rows),
`data/xf_visual_lengths.csv` (263 visual crossfade reads), `data/per_video_counts_3b.csv`. Ledger: 39 new images (25
candidate composites, 6 gap composites, 6 crossfade-check composites, 2 overview sheets of RC30-06), all tiles 120x213
(overview 180x320). Not viewed: overview sheets of RC30-09, 10, 11, 13, 21 (recall there rests on a computational
windowed-histogram gap scan plus gap tiles at its peaks, see F-a15-102).

### F-a15-100 Edit lists for the six missing videos (OBSERVED, medium; 6 videos, 135 rcpipe candidate rows + 5 misses)
Every rcpipe candidate of RC30-06, 09, 10, 11, 13, 21 was classified on every-frame tiles (frames subsampled every
2nd frame for candidates longer than ~9 f; endpoints +-1-2 f). Rows: XF 80, ZT 4 (RC30-09 f1391-1397 push into monitor;
RC30-11 f795-799 captain face fills frame then ocean; RC30-13 f562-572 pull-back out of a sky disc through a window;
RC30-21 f63-69 dragon head pull-back), FT 2 (RC30-09 f1161-1175 fall through room to aerial; RC30-10 f802-809 push
through train window), VB 2 (RC30-06 f1906-1912 firework streak cover; RC30-10 f1928-1943 explosion cover), HC 0, FP 52.
Per video XF/ZT/FT/VB/HC;FP: 06 16/0/0/1/0;6 - 09 10/1/1/0/0;9 - 10 11/0/1/1/0;10 - 11 14/1/0/0/0;7 - 13 10/1/0/0/0;12 -
21 19/1/0/0/0;8 (ZT in 21 and RC30-13 as stated). All six are cluster-A style (dissolve-only, zero hard cuts); RC30-09,
10, 13 are long-take continuous-camera 3D videos with many FPs (camera moves, in-shot VFX). The five hard_cut
candidates (RC30-10 f1928; RC30-11 f800, f803, f1219, f1259) and the flash candidates were in-shot events or VFX covers.
Limitations: slow dissolves with a camera move are cut at the visible ghost frames; long-candidate rows (RC30-13 f1150-1157,
RC30-21 f1452-1472) are +-2 f; classification of RC30-10 f311-317 (object cover vs camera blur) and RC30-06 f1957-1968 low.

### F-a15-101 Crossfade length distribution, 29 videos (OBSERVED + MEASURED, medium - replaces F-a15-002 confidence)
Visual reads n = 263 crossfades in 29 videos (all except RC30-27; n per video 2-19; videos with n <= 4: 01, 02, 03, 04, 05,
07, 08, 22, 28). Median 6 f (0.20 s), IQR 5-7, p10-p90 4-8, mode 5, range 3-23. Share 5-7 f = 65 %; <= 4 f = 19 %; 8-11 f =
15 %; >= 12 f = 2 reads (13 f, 23 f) = 0.8 %. By source: older 17 videos n = 163 median 6 (IQR 5-7); six new videos n = 80
median 5 (IQR 4-6; RC30-21 median 4 across 19 dissolves, RC30-11 median 5); strip check of 01-05, 08 n = 20 (every 2nd frame,
+-2 f) median 5.5 (IQR 4-8). Per-video medians 3.5-8 (slowest RC30-15 8, 01 8; fastest 05 3.5, 03/04/21/23/26 4). Slow
dissolves exist (RC30-01 f406-424 day to night read as ~9 f visible but alpha fit says 15; RC30-15 f1074-1087 14 f) but
visually-readable 12+ f dissolves are rare. Confidence medium, not high: coverage and n now meet the EVIDENCE.md
thresholds, but the method (eye reading of subsampled 120x213 tiles, +-1-2 f) is unvalidated against any ground truth and
faint alpha tails (< ~10 %) are invisible, so visual length probably under-reads slow fades by 1-3 f; the alpha fit
(median 10) remains an upper bound. Easing curve still unmeasured. A28 #3 accepted: the "6 f" label is now backed by
29 videos, but as "typical 5-7 f", not as an exact constant. Implementation: default dissolve 6 f (0.2 s) at 30 fps, linear
or smoothstep alpha, +-2 f jitter allowed; 4 f for fast beats, 8 f for scene/time changes; keep camera motion running
through the blend.

### F-a15-102 rcpipe candidate precision/recall in the six new videos (MEASURED, medium-low)
Precision 83 real / 135 candidate rows = 61 % (FP: continuous camera moves, in-shot VFX, lightning flashes, prop/character
motion). Misses (5) found by a windowed-histogram gap scan (12-frame sum of hist_bgr outside candidate +-8 f; 5-6 peaks per
video viewed as every-2nd-frame tiles, 31 peaks): RC30-06 f141-146, RC30-11 f384-388 and f681-686, RC30-21 f1850-1855 and
f1858-1864; all XF. Recall 83/88 = 94 %, an upper-bound estimate (only the top peaks were viewed; 1 fps overview viewed
for RC30-06 only). Same miss class as before (slow, same-palette or camera-moving dissolves).

### F-a15-103 Dataset-wide counts and shot length, 30/30 videos (MEASURED, medium; UPPER BOUND for shot length)
`python3 src/transitions/a15_stats.py`, 569 rows. Real 391 = XF 308 (79 %), HC 37 (9.5 %), ZT 27, VB 11, FT 8; FP 178.
Hard cuts: 37 only in RC30-01..08 + 22, 23, 24, 28 (32/118 = 27 % of real in RC30-01..08 incl. new 06, 5/273 = 1.8 % in 09..30 incl. the five other new videos). Shots (non-FP
boundaries merged within 15 f; n = 414 shots): median 3.17 s (95 f), IQR 1.92-5.17 s, range 0.47-22.6 s; shots/video median
14 (IQR 9.5-17, range 6-21); per-video median shot: median 3.05 s, IQR 2.74-4.00, range 1.28 s (RC30-25: 7 shots, one
22.6 s hold; correcting the earlier "to 9.1 s" slip - the longest per-video median is RC30-03 9.07 s) to 9.07 s. Per-video
medians (s): 01 1.99 02 2.27 03 9.07 04 2.87 05 2.71 06 2.33 07 2.80 08 3.07 09 4.42 10 4.03 11 3.78 12 3.17 13 4.68
14 5.47 15 3.75 16 2.73 17 3.03 18 3.02 19 2.70 20 3.75 21 2.86 22 6.27 23 2.19 24 3.87 25 1.28 26 2.77 27 3.00 28 4.07
29 4.13 30 3.93. **Caveat for A16:** boundaries are only edits/dissolves/scope-snaps that were confirmed visually. Continuous-
camera scene changes without an edit (RC30-03, 09, 10, 13, 22, e.g. RC30-13 f110-263 pull-back to aerial, RC30-10 f251-302 cliff
to desert to rail yard) are counted as FP, so the catalogue shot length is an upper bound for "scene" length and is NOT a
cut rate; RC30-03, 09, 10, 13, 22 are the long-take videos where it overstates most. Not resolved here; A16 owns the
conflict.

## Phase 3B revisions
- F-a15-002: confidence high -> medium (A28 #3 accepted); n 162/17 videos -> 263/29 videos (F-a15-101); median 6 and IQR 5-7
  unchanged. Text marked SUPERSEDED in heading.
- F-a15-009: numbers superseded by F-a15-103 (30 videos, n = 414, median 3.17 s); per-video range corrected (A28 #1:
  RC30-25 is 1.28 s, the longest per-video median is RC30-03 9.07 s). Both remain upper bounds.
- F-a15-001/008: still hold; with six new cluster-A videos XF share 75 % -> 79 %, HC 12 % -> 9.5 % of real. F-a15-008's
  split between RC30-01..08 (27 % HC) and 09..30 (1.8 %) holds; the six new videos have 0 HC.
- F-a15-003 (rcpipe hard-cut candidates unreliable): confirmed again, 0 of 5 hard_cut candidates in the six new videos were edits.
- F-a15-006: precision 70 % (24 videos) -> 70 % (30 videos pooled 376 real/552 cand rows ~ 68 %); new six = 61 %.
- Open: RC30-27 has no visual reads (director ground truth only); easing curve; native-resolution endpoints; hard cuts in
  long-take videos; overview scans of RC30-09, 10, 11, 13, 21 not viewed.
