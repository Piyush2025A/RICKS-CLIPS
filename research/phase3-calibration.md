# Phase 3 real-footage calibration — rcpipe v0.2.0 (2026-11-28)

Manifest: `knowledge/dataset/MANIFEST.json` SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`.
Pipeline: rcpipe v0.2.0 unchanged (commit `edfef36`), config fingerprint `2c484ea9…1b03`, native decode, contact sheet
every frame. Machine: user's laptop (i7-7600U 2c/4t, 15 GiB). Outputs private in
`~/ricks-clips-private/analysis-data/rc30/v0.2.0/` (never committed).

## 1. Pilot RC30-27 (`27.mp4`, 928 frames, 30.93 s)
### 1.1 Run (MEASURED)
exit 0; wall 340.4 s (5 min 41 s) = **2.73 frames/s** (0.367 s/frame); CPU user 423.9 s + sys 113.0 s (≈ 1.6 cores);
peak RSS 334 MiB; output 37 MB incl. 20 contact sheets (48 frames each, 120 × 213 px tiles).

### 1.2 Frame accounting and timestamps (MEASURED)
- reconcile: nb_read_packets = nb_read_frames = pts list = decoded = **928** (container nb_frames absent).
- Independent cross-check against the D025 `framemd5` pass: 928 = 928 frames; max |pts difference| 3.3 × 10⁻⁷ s.
- Coverage record: frames_processed 928, missing 0; per stage ok/uncertain/failed/missing:
  decode 928/0/0/0 native · color 928/0/0/0 native · edges 928/0/0/0 native · sharpness 928/0/0/0 native ·
  shots 928/0/0/0 proxy (160 px features) · motion 870/58/0/0 proxy (≤ 320 px estimator); the 58 uncertain motion
  frames are exactly the frames inside gradual-transition candidates (by design).
- First video pts 0.0333 s, audio starts at 0: `av_start_offset_s` = −0.0333 recorded.

### 1.3 Shot boundaries vs ground truth
Ground truth (OBSERVED): the director viewed **all 928 frames** on the 20 contact sheets (120 × 213 per frame;
20 records in `knowledge/dataset/coverage/visual/director.jsonl`).
| True transition (OBSERVED) | Type | rcpipe candidate | Result |
|---|---|---|---|
| f000248–f000253 | crossfade, 6 fr | gradual 248–254 | TP |
| f000338–f000343 | crossfade, 6 fr | gradual 338–344 | TP |
| f000421–f000426 | crossfade, ~6 fr | gradual 420–427 | TP |
| f000494–f000499 | crossfade, 6 fr | gradual 493–499 | TP |
| f000540–f000546 | crossfade, ~6 fr | gradual 539–547 | TP |
| f000778–f000783 | crossfade, 6 fr | gradual 777–783 | TP |
| — | (tail of the f540 crossfade) | gradual 550–555 | FP (duplicate fragment) |
| — | strip curls into a wheel inside one shot (object morph) | gradual 768–774 | FP (content change, not an edit) |
Recall **6/6 = 100 %**, precision 6/8 = 75 %, start offset ≤ 1 frame. **No hard cuts exist in this video**, so hard-cut
detection (incl. the known same-palette miss at `cut_mad = 15`) is not exercised here. Rate of FPs 3.9/min exceeds the
proposed ≤ 1/min target; both FPs are of a recognisable kind (adjacent duplicate; fast in-shot animation) and are
resolved by visual confirmation in the transition catalogue (A15). Not a material pipeline defect → no code change.

### 1.4 Camera motion vs observation (MEASURED proxy values; OBSERVED direction)
Per true shot, product of frame-to-frame similarity scale and sum of translation (proxy px):
| Shot (frames) | Observed camera behaviour | scale product | Σtx, Σty | Agreement |
|---|---|---|---|---|
| 0–247 | continuous pull-back from reel macro to wide shot of character | 0.243 | −95, +62 | yes (zoom-out ≈ 4×) |
| 254–337 | near-static two-shot, slight push | 1.067 | +39, +1 | yes |
| 344–420 | tilted macro, tracking the bill into the slot | 1.439 | −600, +1005 | yes (move + push) |
| 427–493 | near-static tilted close-up | 1.088 | −3, +2 | yes |
| 500–539 | fast fly-in towards the machine | 3.116 | +393, +135 | yes |
| 547–777 | long downward tilt along the reel strip | 1.719 | +25, −3111 | yes (tilt) |
| 784–927 | pull-out revealing the character | 0.573 | −276, +631 | yes |
Direction agrees for 7/7 shots. Magnitudes are proxy-space 2-D similarity estimates of a 3-D camera (dolly vs zoom
cannot be distinguished; parallax layers blend — known limitation D018). Confidence labels: mostly `medium`.

### 1.5 Colour / edges / sharpness
Native-resolution per-frame statistics (luma percentiles, CIELAB means/std, saturation, 12-bin hue histogram, dark-ink
fraction, edge density, Laplacian sharpness) computed for 928/928 frames. No ground truth exists for these; they are
descriptive measurements, reliable as statistics of the decoded (BT.709 limited-range, AAC/H.264-compressed) frames,
not of the original masters. The `dark_thr = 60` "ink" fraction also counts dark scene areas (casino shadows) — it is
an upper bound for outline coverage, not an outline measurement.

### 1.6 Audio (MEASURED)
- Native stream (ffmpeg ebur128, both channels): integrated **−15.1 LUFS**, LRA 2.5 LU, true peak −2.7 dBTP,
  short-term median −14.9 LUFS, max −13.8; momentary max −11.9.
- Native stereo check (ffmpeg `astats`, 44.1 kHz, original stream): L RMS −18.00 dB, R RMS −17.99 dB; side signal
  0.5·(L−R) RMS −47.0 dB → side is **29 dB below** the channels: effectively mono. For this video the D027 48 kHz mono
  path loses no meaningful stereo information.
- 48 kHz mono path: envelope/spectral rows at 10 ms; 240 onsets in 31.0 s (7.7/s; speech-syllable density).

### 1.7 Observations made during ground-truthing (OBSERVED, RC30-27 only; for specialists to verify dataset-wide)
- Edit grammar: 7 shots joined by 6 short (≈ 0.2 s) crossfades; the camera is moving in almost every shot.
- Burned-in captions: one word or short phrase at a time, white bold text with dark outline, horizontally centred at
  ≈ 70 % of frame height; captions change per word → usable as a word-timing proxy.
- Characters: flat 2D cut-out bean-head figures with ink outline inside a lit, rendered 3D casino set; expressions
  change frequently (blinks, brows, mouth shapes) within shots.
- Depth of field: strongly blurred foreground band in the two-shot (f000254–f000337); shallow DOF on macros.
- VFX: specular shine sweep on the jackpot row (f000643–f000650); stamping/counter animation (f000689–f000767);
  holographic blue wireframe "x-ray" cutaway (f000778 onward).

## 2. Holdout RC30-15 (`15.mp4`, 2,334 frames, 77.8 s)
HOLDOUT_PENDING

## 3. Calibration decision
DECISION_PENDING
