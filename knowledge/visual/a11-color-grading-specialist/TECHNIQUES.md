# A11 TECHNIQUES — measured grade recipes (RC30). Status: derived from measurements, NOT yet validated on our own renders (no EXP run).
All values are display-referred (sRGB-coded, full range after limited→full expansion), caption band excluded. Source of each number: FINDINGS F-a11-xxx and `data/`.

## T0 Range discipline
Encode our final video as BT.709 limited range (`-color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709`) like the reference; do all grade maths in full-range 0–1 and measure after expanding limited→full (never compare raw 16–235 with expanded values). QC uses `src/grade/qc_grade.py` (`--full-range` for PNG).

## T1 Baseline tone mapping (all moods)
Output black floor and white ceiling (video medians): p1 = 0.10 (IQR 0.075–0.117), p5 = 0.14, p99 = 0.94 (0.906–0.957), contrast p95−p5 = 0.64 (0.61–0.69).
Piecewise transfer `y = lift + (white−lift)·x` then shoulder above x0=0.80: `y = y0 + (white−y0)·(1−(1−t)^1.6)`, t=(x−x0)/(1−x0).
Params: day/neutral lift 0.10, white 0.95; low-key lift 0.03; shoulder starts 0.80. No S-curve (F-a11-004).
FFmpeg: `curves=all='0/0.10 0.5/0.52 0.8/0.84 1/0.95'` (neutral/day starting point; adjust per mood target table); Three.js: apply in the final full-screen pass after tone mapping, before sRGB encode (`out = mix(vec3(lift), vec3(white), shoulder(c))`).

## T2 Per-mood targets (frame medians; fit render percentile → target percentile)
| mood | p1 | p5 | p25 | p50 | p75 | p95 | p99 | C* p50 | C* p90 | black RGB | vignette c/c |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bright_neutral_interior | .146 | .253 | .523 | .673 | .801 | .926 | .966 | 19.8 | 50.2 | 41,30,37 | .89 |
| warm_day_sunset | .137 | .221 | .474 | .622 | .763 | .881 | .941 | 24.3 | 51.6 | 44,27,29 | .88 |
| day_cool_sky | .113 | .198 | .374 | .540 | .688 | .859 | .954 | 21.2 | 44.3 | 29,23,34 | .85 |
| neutral_mid | .097 | .139 | .313 | .486 | .652 | .859 | .964 | 18.2 | 39.0 | 25,20,26 | .80 |
| red_orange_glow | .098 | .128 | .248 | .399 | .554 | .857 | .948 | 33.2 | 60.8 | 40,15,17 | .62 |
| red_pink_saturated | .097 | .140 | .264 | .370 | .528 | .789 | .904 | 30.2 | 53.0 | 34,17,32 | .71 |
| warm_interior_lamp | .087 | .117 | .222 | .364 | .514 | .805 | .938 | 21.6 | 44.3 | 25,17,22 | .69 |
| night_blue | .075 | .099 | .186 | .289 | .428 | .731 | .920 | 23.5 | 43.9 | 13,15,30 | .67 |
| violet_dusk_neon | .070 | .102 | .181 | .270 | .394 | .668 | .807 | 43.2 | 70.8 | 10,13,42 | .61 |
| dark_low_key | .029 | .047 | .098 | .164 | .290 | .646 | .874 | 13.3 | 25.3 | 5,4,17 | .48 |
Fit: build an LUT by matching the CDF of the render's luma to these seven anchors (monotone PCHIP through (render_p_k → target_p_k), end points (0→p1·0.5?) kept ≥ target p1). Tolerance bands: IQR in `data/tone_chroma_hue_summary.json`. Do the fit **per scene mood, not per video** (p50 spans 0.15–0.65 across videos).
Lighting must supply the mood (A09 presets); the grade only trims: if a render needs > ±0.10 on p50 or a ΔC* p90 > 12, send hand-off to A09 (lights) / A08 (albedo) rather than grading harder.

## T3 Black tint (do not neutralise)
Add the mood black RGB (table) as the shadow floor: `rgb_out = max(rgb, blackRGB/255)` softened: `rgb + (1−rgb)^4 · (blackRGB/255 − lumaFloor)`. Dark pixels (L*<12) typical a* +8, b* −6 (magenta-blue); keep sky/ambient colour in shadow (A09).

## T4 Saturation
Scale chroma in OKLab/LCh (not RGB sat) to hit C* p90 per mood (table); global median targets: C* p50 24.9 (19.6–29.6), p90 47.2 (43.4–54.5); share of pixels C*>35: 27 % (12–46). Factor = target_p90 / render_p90, clamp 0.8–1.4. **No extra centre/hero saturation** (centre/periphery C* ratio 1.00, IQR 0.94–1.06). Suppress above C* 75 (violet neon ceiling ≈ 71).

## T5 Hue distribution targets (30° Lab-angle bins, chroma-weighted, whole frame)
Overall: 30–90° orange/yellow 37 %; 270–330° blue/violet 36 %; 0–30°/330–360° red-magenta 8 %; 90–180° yellow-green/green 11 %; 180–270° cyan-blue 8 %. Per mood: `hue_hist_12bin_30deg_Lab_angle` in `data/tone_chroma_hue_summary.json`. Scheme to reproduce: warm orange lit subject/ground against ultramarine-violet shadow/sky (≈ 210–225° apart); avoid teal (180–240° = 2 %). Implement as lighting colours (key ≈ h 60–75°, ambient/shadow ≈ h 280–290°), not hue rotations; a subtle LCh hue shift ≤ ±8° only for fine matching.

## T6 White cards/faces
Target face-white pixels L* ≈ 92 (88–96), a* ≈ +1, b* ≈ +1 (+6 warm lamp, −3 night) = sRGB ≈ (238,232,231). No pure 255 faces; keep white-card share ≈ 2.6 % of frame (0.4–6.8 %).

## T7 Vignette
Corner/centre luma ≥ 0.85 in day, 0.60–0.70 in night/lamp, 0.45–0.55 only in spotlit low-key. Produce with lighting falloff; any overlay must be ≤ 0.1 extra darkening (A10 upper bound).

## T8 Continuity rules
Same-location shots: ΔE76 of frame-mean Lab ≤ 8 (RC30 per-video median 3.4–11.5; single-location videos ≈ 3.5–5.5), |Δp50| ≤ 0.05. Declared mood change (cut or ~6-frame crossfade): allow ΔE up to 40 (RC30 p90 28–39); crossfade must be a monotone blend (luma overshoot < 5/255) — no flash unless it is a VFX event (flash overshoot 15–25 in RC30).

## T9 QC spec — `src/grade/qc_grade.py <video|png> [--mood M] [--fps 1] [--full-range]`
Decodes at 1 fps/270×480, masks caption band, computes median per-frame y_p1, y_p50, y_p99, contrast p95−p5, C* p50/p90. Checks: (a) video-level medians within RC30 IQR (video-level only; for a single scene use --mood); (b) with `--mood`, |Δ| ≤ 0.04 p1, 0.08 p50, 0.05 p99, 10 C* p90 vs table; (c) reports max |Δ p50| 1-s step (flag > 0.20 outside mood cuts) and % frames with p1 ≤ 2/255 (flag > 1 % outside low-key). Exit 1 on failure. Smoke-tested on a 3 s reference clip (private) — runs; thresholds untested on original renders.
