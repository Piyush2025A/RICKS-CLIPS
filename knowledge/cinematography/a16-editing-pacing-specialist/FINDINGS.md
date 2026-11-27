# A16 FINDINGS — edit rhythm model (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A16.
Visual ledger: `knowledge/dataset/coverage/visual/a16-editing-pacing-specialist.jsonl` (3 records: overview sheets 180x320, 1 fps,
RC30-18, RC30-22, RC30-03, t = 1-40 s). Everything else is computational (not visual coverage).
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

## F-a16-002 A15's edit list undercounts cuts in long-take 3D videos: shot length 3.06 s is an UPPER bound (OBSERVED, medium-low; RC30-22, 03)
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

## F-a16-006 First 3 s: usually zero or one transition; the opening shot is 2-6 s (MEASURED, medium; 24 videos)
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
