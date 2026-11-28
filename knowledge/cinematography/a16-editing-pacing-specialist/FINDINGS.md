# A16 FINDINGS — edit rhythm model (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A16.
Visual ledger: `knowledge/dataset/coverage/visual/a16-editing-pacing-specialist.jsonl` (22 records after 3B; videos with visual evidence 30/30: 3 overview sheets of RC30-18/22/03 at 1 fps; 3B: 4 composites of RC30-22 every 5th frame f0-f1905, and 15 composites of every 3rd frame f0-f87 of all 30 videos, 120x213 tiles cropped from the every-frame sheets). Everything else is computational. NOTE: 3B opener views are every 3rd frame, not every frame; RC30-22 views every 5th frame.
Videos: 24 with A15 confirmed edit lists (01-05, 07, 08, 12, 14-20, 22-30 minus none; 06, 09, 10, 11, 13, 21 have none). Input:
A15 `transitions_confirmed.csv` (sha256 prefix a103bde67848d3da; non-FP rows, parts within 15 f merged, boundary = span centre →
294 boundaries, 318 shots), A20 caption series (`capser_*.npy`, A20 detector re-run) and speech gaps (re-run of A20 Otsu envelope, `scripts/gaps.py`,
gap counts match A20), A13 `moves_table.csv`, A27 `shot_features.csv`/`motion.csv`.
Reproduce: `.venv-analysis/bin/python scripts/gaps.py; scripts/pacing.py; scripts/beats.py; scripts/deadtime.py` (outputs in `data/`).
Controls: boundary-vs-speech tests use 500 circular shifts of each video's whole transition list (preserves shot structure).

## F-a16-001 Pacing is flat across the runtime: no acceleration, no deceleration (MEASURED, medium; n = 24 videos, 318 shots)
Acts by normalised time (A19 gives only approximate seconds: Act 1 ~0-15 s, Act 2 ~15-40 s, Act 3 last 15-25 s; at the ~60 s median this
equals 0-25 %, 25-65 %, 65-100 %). Shot length (median, IQR): Act 1 2.93 s (1.97-5.20, n 85); Act 2 2.95 s (1.83-4.80, n 122);
Act 3 3.43 s (1.91-5.23, n 111). Cut rate per 10 s (per-video median, IQR): 2.05 (1.24-2.87) / 2.56 (2.14-2.88) / 2.01 (1.71-2.80);
Wilcoxon Act 1 vs 3 p = 0.84 (11 videos faster in Act 3, 13 slower); Friedman p = 0.19. Pooled boundaries per decile of runtime:
23, 29, 39, 31, 28, 38, 22, 31, 25, 28 (no trend). Per-video Spearman(shot length, position): median -0.05 (IQR -0.24..+0.17; 11 pos / 13 neg).
Faint pattern only: escalation 25-55 % has the highest cut rate (median 2.77 /10 s, 22 videos without 03/22) and the last 15 % the lowest (1.82).
Limits: boundaries are A15's, which undercount hard cuts (F-a16-002); a flat result could hide a real trend in the missing cuts.
Implementation: do not ramp cut rate; vary it by beat (F-a16-007). Default ~2-2.5 transitions/10 s, shot 1.8-5.1 s (IQR), median ~3 s.

## F-a16-002 A15's edit list undercounts cuts in long-take 3D videos: shot length 3.06 s is an UPPER bound (OBSERVED, medium-low; RC30-22, 03) - NUMBER '>= 7 cuts/10 s' SUPERSEDED by F-a16-101 (every-frame check: about 5.4 visual beats/10 s, of which 1.3 are edits); the upper-bound logic stands
RC30-22: A15 lists 8 joins in 63.5 s (median shot 6.27 s). The 1 fps overview (t = 1-40 s) shows a different shot at ≈ 29 of 39 consecutive-second steps
(ship deck → water → barrels → shore → furnace → powder bag → ship …), i.e. ≥ 0.7 cuts/s (≈ 7 per 10 s, lower bound; 1 fps cannot separate a cut from a
fast move) vs A15's 1.3 per 10 s. RC30-03 (A15: 5 joins, median 9.07 s): scene changes at t ≈ 1-2, 2-4, 5-6, 7-9, 19-20 match; a few angle changes inside the tent
(t ≈ 13 close-up) may be uncounted. RC30-18 and 03 also change character/expression every 1-2 s inside one set (F-a16-004).
Consequence: pooled shot-length statistics here are biased long; cluster C (03, 22) is not "long-take" in rhythm terms — RC30-22 is the fastest-cut video.
Beat-window tables (F-a16-007) exclude 03 and 22 for that reason. Open: A15/A27 should re-run hard-cut detection on 22 (and 12-30 generally; F-a15-003).
Implementation: judge pacing by "scene content changes/s", not by crossfades alone.

## F-a16-003 Transitions are placed at narration pauses more often than chance, but the effect is moderate (MEASURED, medium; 294 boundaries, 24 videos)
vs a circular-shift control (500 draws/video): (a) span of the transition (≈ 6 f) overlaps a speech gap ≥ 150 ms: 64.6 % observed vs 43.9 % null
(median over videos; 19 of 24 videos above null, Wilcoxon p = 1.3e-4); (b) transition centre inside a gap: 28.6 % vs 19.3 % (17/24 above, p = 0.053);
(c) centre within ±0.25 s of a gap ≥ 0.3 s: 23.8 % vs 12.7 % (null p95 15.3 %, pooled); (d) median distance centre → nearest gap centre 6.35 f vs 10.2 f null
(19/24 lower, p = 2.6e-4); pooled distance to nearest gap (0 if inside): median 2.8 f, IQR 0-6.8 f; signed offset centre - nearest gap edge: median +1.2 f (IQR -1.8..+4.6).
So roughly 1.5-2x the chance rate, not a rule: ~74 % of transitions are NOT in a ≥ 0.3 s pause. Gaps are short (A20: median 0.21 s) so "inside a gap" is a ±3-frame target.
Limits: gap = envelope detector (bed masks short gaps); A15 boundary uncertain ±1-3 f; A15 misses cuts (F-a16-002).
Implementation: when free to choose, centre the ~6 f crossfade on a pause/clause boundary (±5 f); do not wait for ≥ 0.3 s pauses (they occur ~0.4/s).

## F-a16-004 Caption/word change is NOT a usable lock for transitions (MEASURED, medium; same 294 boundaries)
Caption changes arrive every ≈ 9-10 f, so any frame is within a few frames of one. Median |centre - nearest caption change| 2.5 f observed vs 2.8 f null
(per-video: 17/24 below null, p = 0.007 — a 0.3 f effect, no practical value); 64 % within 3 f of a change (chance level ≈ 60 %). Same conclusion as A13 for camera moves.
Implementation: derive transition frames from pauses/clauses (F-a16-003), not from word onsets; word-level sync is only needed for captions and expression snaps (A02: swap at word onset -3..+2 f).

## F-a16-005 Shot ≈ one clause: 1 pause-phrase, 9 caption tokens (MEASURED, medium; 318 shots)
Caption tokens per shot median 9 (IQR 5-15; mean 11.7 ≈ 3.5 s at 0.33 s/token — consistent with shot median ≈ 3 s). Pauses ≥ 0.3 s inside a shot: median 0, 62.6 % of shots contain none →
a shot normally spans 1 pause-split phrase (IQR 1-2); phrase length (A20) median 3.9 s ≈ shot length. Implementation: plan 1 shot per clause, ~9 words (3 s); sentence of 2 clauses = 2 shots.

## F-a16-006 First 3 s: usually zero or one transition; the opening shot is 2-6 s (MEASURED, medium; 24 videos) - extended to 30 videos and split into edits vs beats by F-a16-103/104; the 'hook is not rapid cutting' conclusion is KEPT for edits but incomplete for beats
Transitions with centre < 3 s: 0 in 14 videos, 1 in 9, 2 in 1 (RC30-20) — total 11. First shot length median 3.67 s (IQR 2.13-6.30); first transition at t 0.75 s (14) to 11.9 s (24). Final shot median 2.90 s (1.81-5.06).
The visual hook is character/camera action inside a shot (A13 moves start at the cut; A02 expression bursts), plus 9 caption tokens (A20: 8-9 in 3 s), not rapid cutting.
Contrast with A19 F-a19-005 "quick-cut opener 19/30 (2-3 shots in 1-3 s)": that count uses 1 fps tiles and includes hard cuts A15 may miss; not resolved (see contradictions).
Implementation: 1 transition max in the first 3 s unless the story needs a hard cut; ensure an on-screen change (move start, expression snap, prop entry) within 0.5-1.0 s.

## F-a16-007 Beat-window template (MEASURED on normalised-time proxies, low-medium; 22 videos, 03 and 22 excluded)
Beat types are not labelled per video (A19 gives only typical timing), so beats = windows: hook 0-3 s; setup 3 s-25 %; escalation 25-55 %; reveal 55-85 %; punch 85-100 %.
Shot length median (IQR): hook 2.52 s (1.84-3.67, n 19); setup 2.90 (1.93-5.12, n 81); escalation 2.90 (1.82-4.76, n 87); reveal 3.08 (1.86-5.09, n 86); punch 3.12 (1.88-4.13, n 49).
Transitions per video: setup 2 (median), escalation 4.5, reveal 3, punch 1. Cut rate /10 s medians: 2.06 / 2.77 / 2.20 / 1.82. Per act (0-25/25-65/65-100 %): 3 / 5 / 4 transitions per video (≈ 12 total, 13 shots).
Differences between windows are small compared with IQRs; do not over-fit. Limits: windows ≠ true beats (HYPOTHESIS that they map to A19's structure); A15 undercount applies.
Implementation: see TECHNIQUES beat budget table.

## F-a16-008 Dead time: every window has a change if character/expression and caption events count; camera-and-cut-only dead time is 2-6 s (MEASURED, low-medium; OBSERVED check on 3 videos)
Three definitions (per video max gap with no event; `data/change_rate_deadtime.csv`, thresholds in script):
(D1) no cut/transition: median of max gap 10.5 s (IQR 9.0-13.2; max 22.6 s RC30-25 — but RC30-25 first-shot hold; 24 videos).
(D2) no cut AND no A13 camera move (moves cover 23 videos, not RC30-12): median 3.4 s (2.4-4.7), max 10.6 s (RC30-18), then 6.3 (22), 6.0 (16), 5.5 (29).
Camera is static (|tx|,|ty| < 0.5 px, |scale-1| < 0.002 at proxy resolution) only 17 % of frames (12-24 %), longest static run median 1.5 s (max 6.0 s RC30-16).
(D3) D2 + frame-difference spikes (|MAD(t) - 15-frame median| > 4 robust sigma, 6 f refractory; proxy for expression swaps/object motion; events 18.6 /10 s [17.0-19.9]): median max gap 3.3 s (2.6-3.8), max 6.2 s (RC30-16, f996); at 3 or 6 sigma: 2.6 s / 3.8 s medians, maxima 4.1 / 9.0 s.
OBSERVED check: the longest D2 gap (RC30-18 f987-1306, 10.6 s = t 33-43.5 s) is one waiting-room set with a held camera, but the character changes pose/expression every 1-2 s and a second character enters at t ≈ 39 s (overview tiles t = 33-40). So "dead" for camera and cuts, not for acting.
Expression swaps (A02: bursts 3-5 swaps then 20-100 f hold) were not available as a table → not in D1-D3 except via the MAD proxy; VFX (A12: ~1.3 luma events /10 s) is too sparse to matter.
Implementation: rule "something visibly changes at least every 3.5 s (p75 of max-gap D3) and never > 6 s" — change = cut, camera move start/reversal, expression burst, prop/character entry, VFX. Camera should not be still > 2.3 s (p75 of longest static run).
Limits: proxy 160-320 px; MAD spikes also fire on camera shake; "change" threshold arbitrary — sensitivity above. 3 videos viewed, 1 fps.

## F-a16-009 Visual event rate vs speech: ~1 scene transition per 12 caption tokens (INFERRED, low)
Transitions 2.0-2.6 per 10 s ↔ tokens 28.5 per 10 s (A20: 2.85 /s) → ≈ 12 tokens per transition (mean 11.7 per shot, F-a16-005). A13 moves (555 rows in 23 videos, ≈ 24 per video ≈ 4 per 10 s) start at the cut, so the cut is the master clock and the move/expression events hang from it.
Not cross-correlated with speech rate (rates are nearly constant across videos: A20 tokens/s 2.6-3.2) — the planned cross-correlation had no variance to work with (FAILED.md).

## Contradictions / open
- A19 F-a19-005 (quick-cut opener 19/30) vs F-a16-006 (0-1 A15 boundaries in first 3 s for 23/24): different measuring bases (1 fps tiles incl. camera-driven scene shifts vs confirmed crossfade/cut list). Both kept.
- A15 shot length 3.06 s vs F-a16-002 (≥ 7 cuts/10 s in RC30-22 at 1 fps): both kept; A15's is an upper bound.
- Not done: A19 per-video act boundaries (only typical ranges exist); per-beat-type labels; expression-swap table; unprocessed videos 06, 09, 10, 11, 13, 21; no per-video every-frame sheets inspected (1 fps overviews only).

## Phase 3B additions (2026-11-28)
Inputs: A15 `transitions_confirmed.csv` (569 rows, 30 videos: real = XF/HC/ZT/FT/VB, merged within 15 f, boundary = span centre; FP rows whose note matches camera|pull|push|zoom|fly|descent|pan|tilt|follow|whip|continuous = "camera-driven candidates"), rcpipe `color.csv` (own detector), `captions/RC30-nn/caption_segments.csv`, every-frame sheets. Scripts: `scripts/units3b.py [thr]`, `scripts/openers3b.py`, `scripts/comp3b.py` (composites, private output). Tables: `data/shots_two_units_3b.csv`, `data/openers_3b.csv`, `data/beats_events_3b.json`.

### F-a16-100 Two shot units, defined (METHOD)
(a) **edit shot** = interval between confirmed edits (A15 real rows, incl. crossfade, hard cut, zoom/fall/veil transitions). (b) **visual beat** = interval between any major visual change = edits + continuous-camera scene changes (fly-through, whip pan, fast push/pull that replaces what is in frame). Beats are measured on three tiers: B = edits + A15 camera-driven FP rows not within 15 f of an edit (56 rows); C = B + own detector peaks. Own detector: window distance d(t) = L1 between mean features of frames [t+4,t+12] and [t-12,t-4] (12 hue bins, L, a, b, saturation; color.csv), peaks >= 0.7, 12 f apart, not within 15 f of an edit/camera row. Calibration: recovers 88 % of A15 edits within +-10 f at 0.7 (97 % at 0.35, 78 % at 1.0, 54 % at 1.4).

### F-a16-101 Shot length and rate by unit, 30 videos (MEASURED edits and tier B; tier C proxy; medium)
| Unit | Pooled shot length median (IQR), s | n shots | Per-video median of medians (IQR), s | Rate /10 s, per-video median (IQR) |
|---|---|---|---|---|
| edit shot (409 shots, 379 edits) | 3.18 (1.95-5.18) | 409 | 3.05 (2.74-4.07) | 2.15 (1.84-2.64) |
| beat B (edits + 56 camera-driven rows) | 2.85 (1.73-4.53) | 465 | 2.85 (2.33-3.62) | 2.57 (2.15-2.92) |
| beat C (+ 269 detector extras) | 1.77 (1.03-3.06) | 734 | 1.86 (1.50-2.11) | 4.21 (3.86-4.46) |
Sensitivity of tier C rate (per-video median /10 s): threshold 0.35 -> 6.09; 0.7 -> 4.21; 1.0 -> 3.40; 1.4 -> 3.01 (at 1.4 only 54 % of real edits are even detected, so < 3 is not a valid reading). Per-video values incl. 03, 22: edits/10 s 0.85, 1.26; B 1.19, 1.89; C 3.05, 4.41 (`data/shots_two_units_3b.csv`).
Limits: tier C extras are not individually verified (precision unknown; includes fast character motion and colour shifts); only RC30-22 was hand-counted (F-a16-102), so the C level is calibrated on one video.

### F-a16-102 RC30-22 every-frame check: about 34 visual beats in 62.4 s = 5.4 /10 s, not >= 7 (OBSERVED, medium-low; one video, every 5th frame)
Viewed f0-f1905 in four 12-column composites (every 5th frame, ledger). Hand tally of whole-frame content/viewpoint replacements (whips, cuts, crossfades, fast reframes; slow sunset drift and character acting not counted): about 8 in f0-475, 12 in f480-955, 7 in f960-1435, 7 in f1440-1870; total 34 (plausible range 28-40; ±6 from judging fast pans). Of these, A15 real edits are 8 (1.3 /10 s): the rest are camera-driven (e.g. f53 whip to sea, f73 tilt to sails, f600/f630 zoom into furnace, f730 pull out to beach, f805 into powder bag, f1525 hull to iron wall). Detector C at 0.7 gives 27 (4.4 /10 s), 18 % below the hand count. So the earlier ">= 7 cuts/10 s" (F-a16-002, 1 fps overview) overstated: 1 fps steps counted pans and character acting; and A15's 1.3/10 s is an edit count, not an error. Both are right for different units.
Implementation: RC30-22-type 3D long-take videos run ~1.3 edits and ~5 beats per 10 s.

### F-a16-103 First 3 s, all 30 videos: edits 0 (median), visual beats 1.5 (median) (OBSERVED, medium; 30/30 videos, every 3rd frame f0-f87)
Per video in `data/openers_3b.csv`. Eye-counted edits in 0-3 s: 0 in 18 videos, 1 in 11, 2 in 1; A15 real rows < f90 agree in 29/30 (RC30-10: apparent hard cut f63-66, A15 lists none, unconfirmed). Eye-counted beats: 0 in 5 (13, 23, 24, 28, 30), 1 in 10, 2 in 10, 3 in 4, 4 in 1 (RC30-22): median 1.5 (IQR 1-2); >= 1 beat in 25/30, >= 2 in 15/30. Frame 0: mid-action in 14, posed/idle in 16; none is a title card or black frame. First caption starts at f0 or f1 in 28/30 (RC30-16 f2, RC30-25 f2; median onset f0), so the caption is already on screen at frame 0 in 28/30; 9-10 caption segments start inside 3 s (IQR 9-10). Four of my first reads were camera pans that I took for cuts (RC30-06, 12, 19 and 10 partly) -> A15's FP rows are right; this is why edits and beats must be kept apart.

### F-a16-104 A19 vs A16 openers reconciled: both measured, on different units (OBSERVED + MEASURED, medium)
A19 "quick-cut opener" (19/30: 01-12, 17-22, 26) = at least one visible scene change in t = 1-3 s. My beat counts: all 19 have >= 1 beat (13 have >= 2, median 2.0), but only 10 have an A15 edit < 3 s (median edits 1). A19 "stage opener" (11/30: 13-16, 23-25, 27-30) = one set, slow camera: median beats 1.0, median edits 0; 5 have 0 beats, 6 have 1 beat (14, 15, 16, 25, 27, 29 each contain one fast camera event, 14 and 15 up to 3). So A19 measured visual beats (roughly), A16 measured edits; A19's split is supported as a beat-based split (19/19 quick videos have a beat; 6/11 stage videos also have one, so the boundary is soft). Reconciled rule: **open with a visible change in the first 3 s in ~80 % of videos (25/30 have >= 1 beat), but implement it as an edit in only ~40 % (12/30 have an edit); the typical opener is one camera-driven or edit beat inside 1-3 s with captions running from frame 0.** Stage openers are the 5-6 videos with 0-1 beats; they rely on character acting and a slow push/pull.

### Which number to use in production
- Pacing the **EDL / transition slots / crossfade count**: edit shots (3.2 s median, IQR 2.0-5.2; 2.2 edits/10 s).
- Pacing **visual change / retention / camera and scene budget**: visual beats (~1.9 s median on the proxy, ~4 beats/10 s, range 3-5; hand count RC30-22 5.4/10 s). Cameras in Three.js should therefore be scripted to create about two camera-driven scene changes per edit.
- 3.06/3.18 s must not be quoted as "the shot length" of long-take 3D videos (03, 22, 24, 25, 12): there the edit shot length is 5-9 s but beats stay at ~2-2.5 s.

## Phase 3B revisions
- F-a16-002: ">= 7 cuts/10 s in RC30-22" SUPERSEDED by F-a16-102 (5.4 beats/10 s, 1.3 edits/10 s); "A15 shot length is an upper bound for rhythm" KEPT, now quantified (F-a16-101): edit 3.18 s vs beat 1.8-2.9 s.
- F-a16-006: extended from 24 to 30 videos (F-a16-103); "0-1 transitions" confirmed (A15 agrees with eye in 29/30), but the claim "hook is not rapid cutting" is narrowed to "not rapid edits"; beats are present in 25/30. Confidence unchanged (medium).
- F-a16-001/003/005/007: unchanged (still on 24 videos and A15 edit boundaries; not re-run with the six new videos).
- Coverage: visual evidence for 30/30 videos is limited to f0-f87 (every 3rd frame) except RC30-22 (whole video, every 5th frame) and 3 overview sheets; the rest of each video is computational only.
- Contradictions resolved: A15 3.06 s vs A16 "7 cuts/10 s": different units, A16's number was wrong. A19 19/30 vs A16 0-1 edits: different units, reconciled in F-a16-104. Not resolved: tier-C precision (only one video hand-counted); true frame-by-frame beat counts for the other 29 videos.
