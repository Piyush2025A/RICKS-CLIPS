<!-- owner: A27 | format: knowledge/_system/templates/failed-approach.md | never delete entries -->
## X-A27-001: HS (hue-saturation) histogram distance for shot features  (2026-11-27)
- **Tried:** 12x6 hue-sat Bhattacharyya as `hist_hs` in shot detection (EXP-A27-20261127-01, synthetic `shots` clip).
- **Result:** baseline 0.08-0.10 on static scenes (vs 0.007 luma), 0.1-0.95 jitter during a crossfade; one false 39-frame gradual candidate f30-f69.
- **Why it failed:** sparse bins on smooth palettes flip across bin edges (medium confidence).
- **Lesson / do instead:** per-channel BGR 16-bin histograms (baseline 0.007, crossfade ~0.2/step, cut 0.78).
- **Revisit if:** real footage has flat-colour frames where hue is the only separator.

## X-A27-002: setpts on the default time base to build a VFR test clip  (2026-11-27)
- **Tried:** `setpts=<expr>/TB` with 24/30/60 Hz timing. **Result:** pts snapped to a 1/30 grid, 29 non-monotonic deltas; caught by the pts-vs-truth check.
- **Why:** TB = 1/30, fractional pts rounded. **Do instead:** `settb=1/90000,setpts=...` plus `-enc_time_base:v 1/90000`. High confidence.

## X-A27-003: ru_maxrss for peak RSS  (2026-11-27)
- **Result:** 354 MB for both 90- and 600-frame runs. **Why:** `ru_maxrss` is inherited through fork+exec from the parent (and librosa import for version stamps added ~250 MB at the end). **Do instead:** `/proc/self/status` VmHWM, importlib.metadata for versions. High confidence.

## X-A27-004: test expectations written before measuring (recorded, not hidden)  (2026-11-27)
- Ramp tolerance 2.5 gray levels vs real constant -2..-3 bias (x264/swscale) -> 3.5 plus a separate spread check (<= 1.5).
- Canny density 2*length/area fails for 2 px lines (edges merge, ~0.7x) -> informational for w <= 2.
- Determinism diff compared frame IDs containing the run key -> normalise the key.
- ebur128 frame log requires `-v verbose`; true-peak regex needed `(?s)`.

## X-A27-005: v0.2.0 first suite run 291/296 - four test-side faults and one gate that failed  (2026-11-27)
- **Test bugs (fixed, no pipeline change):** (1) `audio_env.csv` rows stop where the audio ends (nothing is fabricated), the test assumed rows up to the video end -> `max() of empty` crash; (2) validator self-test case expected `{"b":"y"}` valid although `b` has `const "x"` (my expectation was wrong, validator right); (3) two reproducibility checks read `run_manifest.json` after a later run had overwritten the shared output dir; (4) negative-control summary printed a wrong denominator.
- **Gate that failed (recorded, not tuned):** `sty_cut/q45` (CRF 45 ultrafast) was hard-gated and gave dissolve f59-67 plus an extra hard candidate f69. q45 had been declared a stress case (numbers reported, not gated) for tolerance checks, but the shot check was left as a bool gate; it was reclassified informational with a note. Thresholds were NOT changed. Confidence: high that CRF 45 degrades dissolve detection on this clip.
- **Lesson:** declare which variants are gated before writing the checks; read per-run files immediately after the run.

## X-A27-006: global-motion confidence labelled parallax as `high`  (2026-11-27)
- **Tried:** v0.1 RANSAC similarity + `inlier_frac` < 0.5 -> medium. **Result (sty_par, layers -1/-2/-4 px):** estimate -1.21..-1.29 px labelled `high` in 26-29 of 29 pairs, i.e. neither a layer speed nor an average, silently ambiguous. `inlier_frac` (0.57-0.60) does not separate it from rigid pans with a character (0.56-0.77).
- **Fix (v0.2.0):** second RANSAC on the outliers; a second coherent motion (>= 8 inliers, > 0.5 px from primary) -> columns `tx2,ty2,n_inliers2`, confidence `medium`, status `ok:second_motion` (found in 90-100% of parallax pairs). **Limit:** cannot tell parallax from an independent object (character) - every pan clip with a walking character is `medium` too. Phase correlation (+0.8 px on a static clip) and the residual fraction (0.17 static -> 0.49 panning) are not usable as parallax detectors on flat footage.

## X-A27-007: generator truth wrong for `cv2.rectangle` thickness  (2026-11-27)
- `cv2.rectangle(thickness=w)` draws 2w-1 px lines (1, 3, 5 px), so "2 px" outlines were 3 px. Found by comparing dark-pixel count with the intended width before the test run; replaced by exact block fills (width w, analytic ring area). Do not trust drawing-API thickness as ground truth.

## X-A27-008: corrupt-audio generator destroyed the container  (2026-11-27)
- Overwriting from ffprobe `pos` hit the Matroska block header (track vint, timecode, flags: payload starts at pos+4), corrupting the whole file (33 of 135 video frames decoded, "Invalid track number"). Fixed with +4; video then stayed 135/135. Also: ffmpeg banner lines containing the file name ("corrupt") matched the error regex; now only bracketed decoder/demuxer lines are taken as errors.

## X-A27-009: same-palette hard cut not detected  (2026-11-27)
- **Result:** hard cut at f30 between two scenes of identical palette: hist_dist 0.05 (< 0.3), MAD 14.1-14.6 (< 15), ssim_dist 0.26 -> no candidate in clean, q14, q35, q45. Thresholds tuned on noise-texture clips (EXP-01) do not transfer to flat-colour scenes with similar histograms.
- **Not fixed** (no hold-out; tuning on this one clip would be overfitting). **Revisit:** Phase 3 on RC30 with A-level inspection; candidate fix = add ssim_dist/edge_change outlier rule validated on a hold-out set.

## X-A27-010: director schema update broke two audio tests  (2026-11-27)
- Director added required `audio_present` (stream nullable) and made record-level `analysis_resolution` the FINEST stage resolution. My audio records lacked `audio_present` (-> t_audio/t_audio_coverage raised) and my record level used the most reduced stage. Fixed: every audio record carries `audio_present`; no-audio clips now emit an `audio_present:false` record (stream null, analyzed 0, whole duration missing "no audio stream"); record level = finest stage. Lesson: re-run the suite after any schema change.
