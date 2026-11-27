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
