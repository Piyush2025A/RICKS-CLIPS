# A11 colour & tone grading — Phase 3 FINDINGS (RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual ledger: 15 records
(`knowledge/dataset/coverage/visual/a11-color-grading-specialist.jsonl`, 1 fps overview sheets, videos 01 02 03 06 09 10 12 14 17 19 21 23 25 28 30) ·
videos covered computationally: 30/30 (1 fps native pass, 1,697 frames) + 10/30 native per-frame (`color.csv`, v0.2.0: 02 15 23 24 25 26 27 28 29 30).

## Method and range handling (read first)
- Source is BT.709 limited range (16–235). My pass decodes with `ffmpeg scale=270:480:flags=area:in_range=limited:out_range=full:in_color_matrix=bt709`
  (explicit expansion), then Y' = 0.2126R'+0.7152G'+0.0722B' on gamma-coded values 0–1 (display-referred), CIELAB via OpenCV (D65, sRGB).
  All luma values below are **full-range-expanded 0–1**; 16/255 = 0.063 is the limited-range floor.
- A27 `color.csv` luma is also expanded (p1 min 1, p99 max 255 would be impossible unexpanded). Its per-video medians agree with mine within ±7/255
  (02: p50 115 vs 110; 23: 132 vs 137; 28: 146 vs 140) — differences = caption pixels (white text) included in A27 and masked in mine, plus 270 px proxy. A27 p99/clip numbers are therefore caption-contaminated; I use my masked pass for clipping.
- Caption band masked: y 0.60–0.76 of frame height (OBSERVED on sheets 02/03/14/25: caption centre ≈ 0.67).
- 1 fps sampling (frame ≈ 30k) → n = 1,697 frames, 30 videos. "Mood" labels = nearest A09 F-A09-006 centroid in (L*,a*,b*) of the whole frame — **my approximation, not A09's rule-based labels** (n per class 125–200, 17–26 videos each).
- Scripts + inputs: `scripts/pass1fps.py pass2.py analyze.py analyze2.py trans.py`; outputs in `data/`. Reproduce: `.venv-analysis/bin/python scripts/pass1fps.py 1..30; analyze.py`.

## F-a11-001 Blacks are lifted: the typical Short has no true black
MEASURED, high (n=30 videos, 1,697 frames). Per-video median of frame luma p1: **0.099** (IQR 0.075–0.117; = 25/255, ≈ 9/255 above the limited-range floor); p5 0.140 (0.099–0.165).
Pooled frame p1 0.094 (IQR 0.057–0.131). Frames with > 1 % pixels ≤ 2/255: 7.2 %, concentrated in 01 (98 % of frames), 07 (42 %), 27 (29 %), 30 (21 %), 08 (14 %), 26, 05 — all low-key/space/night videos. Videos 09, 11 clip the top instead (see 002).
Per mood p1 (frame median): bright interior 0.146, warm day/sunset 0.137, day cool 0.113, neutral 0.097, red/orange 0.098, warm lamp 0.087, night blue 0.075, violet 0.070, dark low-key 0.029. Evidence `data/per_video_tone_chroma.csv`, `tone_chroma_hue_summary.json`.
Limits: p1 includes the dark ink outline and dark scenery (outline pixels are dark in every frame, yet p1 stays ≥ 0.07 in 23/30 videos, so the outline colour itself is lifted/tinted, not 0,0,0 — consistent with A10). 270 px area-downscale softens thin outlines, raising p1 slightly (not quantified).
Implementation: floor the output black at ≈ 0.09–0.12 for day/neutral moods (≈ 23–30/255); allow 0.03–0.05 only for declared low-key scenes.

## F-a11-002 Highlights are soft: p99 ≈ 0.94, clipping is rare and mood/scene-specific
MEASURED, high (n=30). Per-video p99 median 0.938 (IQR 0.906–0.957); p95 0.798 (0.771–0.859); pooled frame p99 0.933 (0.857–0.970). Frames with > 1 % pixels ≥ 253/255: 5.8 % (caption masked). Video-level: 09 (51 % of frames), 11 (52 %), 01 (20 %), 19 (12 %), 24 (9 %) — specular/white-wall/bloom scenes; 23/30 videos have < 2 % such frames.
Near-white (Y ≥ 235/255) pixel share: median 1.4 % of frame (IQR 0.1–4.0 %).
Implementation: white point ≈ 0.94 (240/255) for p99; tone-map/roll-off the top instead of hard clip (consistent with A10 bloom finding). Do not normalise to 1.0.

## F-a11-003 Compressed contrast, midtone brightness is strongly mood-driven (not one global grade)
MEASURED, high. Contrast (p95−p5) per video 0.643 (IQR 0.613–0.694; range 0.51 (03) – 0.85 (11)). Per-video p50 median 0.430 (IQR 0.347–0.516); **continuous spread 0.146 (01) to 0.655 (29)**, no gap → no single target; fit per mood (F-a09-006 classes). Frame-level p50 (IQR) by mood: bright interior 0.673 (0.637–0.723), warm day 0.622, day cool 0.540, neutral 0.486, red/orange 0.399, red/pink 0.370, warm lamp 0.364, night blue 0.289, violet 0.270, low-key 0.164. Full percentile ladders p1/5/25/50/75/95/99 per mood: `data/tone_chroma_hue_summary.json → per_mood`.
Within-video L* SD median 12.6 (IQR 10.8–13.5): every Short moves across moods (agrees with F-A09-006).

## F-a11-004 Tone-curve shape: no evidence of a strong S-curve; shape = lifted black + long linear-ish shoulder with soft roll-off
INFERRED from distributions, **low-medium**: a transfer curve cannot be identified from output histograms alone (no scene-referred input). Evidence: pooled 16-bin luma histogram (mean share, bin width 16/255): 0.033, 0.077, 0.094, 0.093, 0.090, 0.081, 0.074, 0.072, 0.069, 0.067, 0.060, 0.055, 0.046, 0.038, 0.030, 0.022 (`data/white_card_black_tint_hist.json`): mode at 32–64, almost flat 32–176, linear decay to the top, only 3 % in bin 0 and 2 % in top bin. Day-class quartiles are symmetric about p50 (day cool: 0.374 / 0.540 / 0.688 → gaps 0.166 / 0.148); a strong S would compress p25/p75 away from the median and pile mass at both ends — not seen. Night classes are skewed (p25–p50 gap 0.10 vs p50–p75 0.14) = exposure, not curve.
Implementation: neutral baseline = identity with black floor + highlight shoulder (TECHNIQUES T1); add contrast only through lighting, not an S-curve. Verify later by A/B on our own render (EXP not yet run).

## F-a11-005 Black point is tinted by mood (blue/violet in dark scenes, warm red in red washes) — shadows are not neutral
MEASURED, medium-high (n=30, per-frame median RGB of pixels ≤ frame p1). Per mood sRGB: dark low-key (5,4,17); night blue (13,15,30); violet neon (10,13,42); day cool (29,23,34); neutral (25,20,26); bright interior (41,30,37); warm day (44,27,29); warm lamp (25,17,22); red/orange glow (40,15,17); red/pink (34,17,32). Dark pixels (L*<12) median a*/b* pooled: a* +8 (IQR 5–11), b* −6 (−11…0): shadows lean **magenta-blue (cool-violet), even in warm scenes**. Confirms F-A09 "shadow hue carries sky colour" — do not grade it away. Per video: `data/black_point_rgb_per_video.json`.
Limit: black pixel set includes scenery/outline colours; 270 px.

## F-a11-006 Chroma: moderate and mood-scaled; no hero-vs-background saturation boost
MEASURED, high (n=30). C* p50 per video 24.9 (IQR 19.6–29.6); C* p90 47.2 (43.4–54.5). 27 % of pixels (median; IQR 12–46 %) have C* > 35. Frame-level C* p90 by mood: violet neon 70.8, red/orange 60.8, red/pink 53.0, warm day 51.6, bright interior 50.2, day cool 44.3, night 43.9, warm lamp 44.3, neutral 39.0, low-key 25.3.
Centre (25–75 %) vs periphery (outside 15–85 %) mean C*: ratio median 0.997 (IQR 0.94–1.06): **no systematic subject-centre saturation lift**; per video 0.76 (19) – 1.34 (30, spot-lit centre). Hero/background separation in RC30 is by value/outline/light (A09/A14), not by a saturation grade. Limit: centre includes mid-ground, not a hero mask (would need A27 segmentation).

## F-a11-007 Characters' white faces/cards are off-white and nearly neutral, light-tinted by the scene
MEASURED, medium. Near-neutral bright pixels (L* > 82, C* < 12): share 2.6 % of frame (IQR 0.4–6.8 %). Their median colour: L* 92.5 (IQR 88.6–95.7), a* +1, b* +1 (IQR −1…+5), sRGB ≈ (238, 232, 231); per-video median L* 87–100. i.e. white-card pixels sit at ≈ 0.91–0.93 luma, not 1.0, warm-neutral by +1 b*, shifted warmer in warm scenes (b* up to +6) and cooler in night scenes (min −3.5). Confirmed on sheets: faces warm-white under lamps in 17 and 30, blue-tinged at night in 03, 21 and 17 (OBSERVED, sheets only, low-medium).
Implementation: keep face albedo ≈ 0.93–0.95 linear-display white and let lights tint; do not clamp to 255.

## F-a11-008 Hue: orange/yellow vs blue/violet axis dominates; teal/cyan is almost absent
MEASURED, high (n=30, 12 bins × 30° of CIELAB hue angle h_ab, chroma>8, chroma-weighted; 0° ≈ red-magenta, 60° orange, 90° yellow, 180° green-cyan, 270° blue, 300° violet). Pooled shares: 30–60° 18.1 %, 60–90° 19.4 %, 270–300° **28.3 %**, 300–330° 7.2 %, 0–30° 5.0 %, 90–120° 5.4 %, 330–360° 3.1 %; 180–240° (cyan/teal) only 2.3 % and 240–270° (pure blue) 5.8 %. Warm orange (30–90°) ≈ 37.5 % vs blue-violet (270–330°) 35.5 %: a near-complementary orange/blue-violet pairing (≈ 210–225° apart), but **not teal/orange** (teal/cyan 180–240° = 2.3 %) — the cool side is ultramarine/violet-leaning blue, not cyan. Green (120–180°) ≈ 5 % (grass scenes: 06, 23, 10 partly) — green appears as local scenery.
Per mood: night blue 59 % in 270–300° (+11 % 300–330°); violet neon 63 % + 27 %; dark low-key 48 % + dark orange 27 %; day cool: blue 41 % + 180–270° 25 % (sky) vs orange 13 %; warm day: 60–90° 43 %, 90–120° 17 %, 30–60° 18 %; warm lamp 30–60° 34 %, 60–90° 41 %; red/orange 30–60° 53 %, 60–90° 27 %; red/pink spread 0–30°/330–360° 32 % + blue-violet 32 % (25: pink-red body vs blue pill). Table: `data/tone_chroma_hue_summary.json → per_mood[*].hue_hist_12bin_30deg_Lab_angle`. 16/30 videos contain warm and cool moods ≥ 10 % (F-A09-006); scenes pair warm lit subject on warm-ground against cool sky/shadow (OBSERVED 12, 14, 21, 10, 17).
Limit: histograms include scenery; label "hero warm / background cool" is OBSERVED on sheets only, not measured per object.

## F-a11-009 Whole-frame vignette ratio is mild in day and strong in low-key (scene + lighting, not a separate overlay)
MEASURED (upper bound, combined with scene falloff; A10 already bounds the overlay). corner/centre luma ratio median 0.75 (per-video IQR 0.59–0.80): bright interior 0.89, warm day 0.88, day cool 0.85, neutral 0.80, warm lamp 0.69, night 0.67, red/orange 0.62, violet 0.61, low-key 0.48. Extremes per video: 28 (0.96), 20 (0.89) vs 30 (0.42), 15 (0.46), 26 (0.49). Implementation: do not add a stronger vignette than 0.85 in day; let spot/lamp lighting create the rest.

## F-a11-010 Shot-to-shot colour steps are large and follow lighting changes; crossfades are monotone blends
MEASURED (1 fps, 30 videos) + OBSERVED. Mean-frame Lab ΔE76 between consecutive seconds: median 7.5 (IQR 2.9–16.5), p90 28.6, p95 39.5; |Δ luma p50| per second median 0.033, p90 0.20. Per-video median ΔE from 3.4 (27) to 11.5 (10): low in single-location videos (26, 27, 30, 03, 29), high in multi-set stories (10, 19, 22, 25, 17).
Native, 10 processed videos, 166 transition candidates (A27 cut/gradual/flash, includes false positives): pre→post ΔE76 median 17 (IQR 7–29, p90 39). Gradual (crossfade, ~6 frames) candidates have **overshoot ≈ 0** (median 0–7 luma units; luma stays between the two shots → plain dissolve, no grade flash). Flash candidates have 15–25 unit overshoot (video-level exceptions 23, 28, 30 = VFX/light flashes, F-a12).
Interpretation (INFERRED, medium-low): jumps are authored mood changes (day→dusk→night, hall→bloodstream), same-set shots keep a constant grade — not evidence for per-shot colour correction; can't prove absence of per-shot trims. Visual confirmation on 15 sheets: jumps at 02 f000659 (violet cell), 06 f000899 (night), 09 f000749 (pink), 17 f000329 (blue night), 21 f001019 (night), 25 f000149 (red), 28 f000869/f000989 (amber/red), 30 f000749 (underwater).
Implementation: tolerance for same-location shots ΔE76 ≲ 8 and |Δp50| ≲ 0.05; allow up to ΔE 40 only at a declared mood change.

## Contradictions / open
- Per-video p50 is a continuum, not bimodal-by-video, but moods inside videos are bimodal-ish; never pool (we report per mood).
- A27 native `p99 ≥ 254` frame shares (0–35 %) vs my masked 5.8 %: difference = white captions; use masked.
- Mood labels are approximate; A09 per-frame labels were not available as a table. Re-run with A09 labels if published.
- Not measured: hero-object masks, per-shot (cut-resolved) ΔE for the 20 videos not yet in v0.2.0, true tone-curve transfer (needs matched renders → A09/A10 A/B).
