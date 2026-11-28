# A15 FAILED / LESSONS
- Least-squares alpha fit (frame = a·A + (1−a)·B on 120×213 tiles) over-estimates crossfade length (median 10 vs visual
  6) when the camera moves during the blend and at low resolution; needs motion-compensated or native-frame fitting.
  Use visual endpoints instead.
- Part 1 hit the turn limit after 6 videos (75 strips of 6 candidates). Part-2 fix: auto-composite 13-tile candidate
  strips (six candidates per image) cut cost to ≈ 3–6 images per video; 17 videos done in one session.
- 1 fps overview scans help recall only with every-3rd-frame gap tiles to disambiguate continuous camera moves; 1 fps
  cannot resolve events within the same second.
- rcpipe candidates for RC30-23 ended at f1007 of 1219 frames — check tail coverage (no candidate in the last N seconds)
  as a miss warning sign.
- Part-1 CSV was first written to repo-root `data/` (outside ownership); moved by the director into this folder.
- Not done: easing curve; overview scan beyond t = 40 s for 12, 16, 19, 26; the 6 videos not processed by rcpipe.

## Phase 3B
- Crossfade endpoints from 120x213 every-2nd-frame composites carry +-1-2 f error; composites of long candidates were subsampled
  (13 tiles per row) so exact start/end frames of slow dissolves in RC30-13/21 are not exact. Needs native frames or
  motion-compensated fitting if exact easing is required.
- The overview-sheet scan for the six new videos was replaced (except RC30-06) by a windowed-histogram gap scan; it found 5
  misses but its recall is unvalidated.
- Windowed gap scan thresholds were chosen by inspection of candidate windows (median 0.9-1.3, p10 0.5-0.7); peaks below ~0.35
  were not examined.
