# A20 FINDINGS — narration / voiceover (Phase 3, RC30)
Phase 3B update 2026-11-28: see "Phase 3B additions" (F-A20-101..105) and "Phase 3B revisions".
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A20.
(Written to disk verbatim by the director from A20's hand-off; the agent's Write tool refused this file.)
All 30 videos computational (native 44.1 kHz stereo, pipe decode, read-only; no temporary WAVs). Visual ledger: 8
records — contact sheets RC30-02 f0–47, 15 f624–671, 24 f576–623, 25 f240–287, 26 f336–383, 27 f480–527, 28 f336–383,
30 f432–479 (120×213). The agent cannot hear; all claims computational. Tables: `data/audio_per_video.csv`,
`data/caption_tokens_per_video.csv`, `data/caption_audio_xcorr.json`; scripts in `scripts/`. Not done: second pitch
pass, ducking beyond one band, bimodality test, hand-checked word-timing error.

## F-A20-001 Loudness: two clusters (MEASURED, high, n = 30)
ffmpeg ebur128 on the native stream. Integrated median −14.1 LUFS (IQR −14.28..−14.02; range −15.6..−14.0); 23 videos
at −14.0..−14.3; 7 at −15.0..−15.6 (RC30-18, 23, 24, 27, 28, 29, 30). LRA median 2.2 LU (1.6–3.5); TP median −2.1 dBTP
(−3.6..−1.3); the −15 cluster peaks lower. Resolves −14 vs −15 (calibration RC30-27 −15.1): both real; not monotonic
in key order. Implementation: master −14 LUFS, TP ≤ −2, LRA 2–3 (A22).

## F-A20-002 Effectively mono (MEASURED, high, n = 30)
|L−R RMS| median 0.01 dB (max 0.07); L/R correlation median 0.996 (min 0.982); side vs mid median −27.5 dB
(−32.2..−20.5; widest RC30-03 −20.5, RC30-06 −20.9). Implementation: mono narration, near-mono bed; SFX panning untested.

## F-A20-003 Speech rate ≈ 2.85 caption tokens/s ≈ 3.3 words/s (~200 WPM) (MEASURED + OBSERVED, medium; n = 30 detected / 8 viewed)
Caption-pixel detector (luma ≥ 245, band y 1150–1550 × x 60–1020, 240×100) frame-difference spikes ≥ 200, local max,
3-frame refractory = token changes. Validated on 8 sheet windows (35 hand-read changes): recall ≈ 94 %, ≈ 10 % spurious
(bright backgrounds), detector +1 frame vs the hand read. Tokens/s median 2.85 (IQR 2.73–2.99; range 2.60–3.21, RC30-28
highest); token interval median 333 ms (p90 566, p99 800). Words/token 50/43 = 1.16 (mostly 1 word; 2–3 for short
phrases). Words/s 3.3 (3.16–3.46), plausible 3.0–3.7. Samples are mid-video; the other 22 videos rest on detector counts.
Implementation: ≈ 3.2–3.4 words/s, one token per ≈ 0.33 s, 8–9 tokens in the first 3 s (5–11).

## F-A20-004 Syllable-peak proxy (MEASURED, medium-low, n = 30)
300–3400 Hz Hilbert envelope, 10 Hz LP, peaks ≥ 3 dB prominence, ≥ 80 ms apart, active frames: 6.4 per active s
(6.26–6.67); 3.9 per total s; modulation peak 2.5 Hz; 1.38 peaks/token, ≈ 1.19/word → undercounts syllables (true
≈ 4.5/s, INFERRED). Cross-video r(tokens/s, peaks/s) = 0.11 (both near-constant) → only the level is validated.

## F-A20-005 Pauses short, little dead air (MEASURED, medium, n = 30, 1,527 gaps)
Gaps = runs below a per-video Otsu threshold of the 50 ms speech-band dB envelope, ≥ 150 ms, excluding head/tail.
0.86 gaps/s. Pooled p10 0.15, p25 0.17, median 0.21, p75 0.27, p90 0.34, p99 0.50 s; histogram 0.15–0.2: 620,
0.2–0.25: 403, 0.25–0.3: 234, 0.3–0.4: 192, 0.4–0.5: 60, 0.5–0.75: 18, > 0.75: 0. Gaps ≥ 0.3 s median 8.5/video
(3–17); ≥ 0.5 s 0–3; none ≥ 1 s. Sum of gaps > 0.25 s median 4.4 s (3.9–5.9; 2.0–9.6) = 9 % of runtime (5–20 %); highest
RC30-15 9.6 s, 21 8.4, 17 8.1, 13 7.8. Voice-active fraction 0.61. Phrase length (split at > 0.3 s) median 3.9 s
(3.0–6.1), 17 peaks. Limits: bed masking/smoothing shortens gaps; sub-150 ms breaths missed. Implementation: sentence
pause 0.3–0.5 s, breaths 0.15–0.25 s, none > 0.6 s.

## F-A20-006 Voice starts immediately (MEASURED, high, n = 30)
First active frame median 0.14 s (0.07–0.31); first caption token 0.20 s (0.10–0.53). Matches F-a19-001.
Implementation: voice onset ≤ 0.3 s.

## F-A20-007 Captions lead audio onsets by ≈ 70 ms (MEASURED, medium, n = 30)
Cross-correlation of caption-change impulses (t = (frame+1)/30) with speech-band onset strength, lags −400..+800 ms,
vs 20 circular-shift nulls: peak lag median +70 ms (IQR 60–90; 50–160), z median 4.5 (2.5–6.6), all 30 > 2.5 → the
caption appears ≈ 2 frames before syllable energy rises. Limits: energy onsets, bed smoothing, ±1-frame detector, no
hand-checked word-level ground truth — word-timing error in ms NOT established. Implementation: caption at
t_word − 2 frames; expression swaps at −3..+2 (A02). Contradiction with A02 ("alignment not established"): this is
statistical, not per-word.

## F-A20-008 VO-to-bed margin ≈ 14 dB; ducking inconclusive (MEASURED/INFERRED, low-medium, n = 30)
Speech-band active minus gap level median 13.9 dB (13.1–14.3; 10.5–15.6; RC30-15 lowest); gap level = bed + noise.
Low band 35–110 Hz active minus pause median −0.5 dB (−3.0..+0.5), but the bed has little energy there (−44 vs −21 dB)
→ weak test. Implementation: bed 12–14 dB under VO in the speech band; A22 tests sidechain ducking.

## F-A20-009 One narrator, tightly consistent (MEASURED; F0 low-medium; n = 30)
pyin on 16 kHz mono mid, 65–450 Hz, 64 ms frames, 20 ms hop, voiced flag AND active frames, 5-point median filter. F0
median 205 Hz (IQR 199–212; 186–219); p10 143 (129–152); p90 299 (272–322); std 4.9 semitones (4.3–5.4); spectral
centroid (active, 0–8 kHz) 1573 Hz (1535–1621; 1446–1671). Spread across videos ±5 % → consistent with one voice/setting
(INFERRED, no listening). Caveats: voiced_prob median ≈ 0.02 so the voiced flag was used; 35–53 % of pause frames
flagged voiced (bed bias); wide p10–p90 mixes intonation and octave errors; ≈ 200 Hz is high for an adult male →
open. Use only as a casting sanity check. (No voice cloning of the reference narrator.)

## F-A20-010 No in-scene character voices detected (INFERRED, low; 8 windows + F0 stats)
Caption styling identical in all viewed windows; narration over silent faces (A02); F0/centroid statistics uniform;
no bimodality test run.

## Open
Cause of the −14/−15 clusters; word-level timing error; words/token in 22 unviewed videos; ducking; sub-150 ms pauses;
cleaner F0 (private `f0full_*.npz` not analysed).

## Phase 3B additions (2026-11-28)
Source: private transcripts of all on-screen captions (30 videos, 4,999 caption segments read from the dense reading sheets
in 3B parts 1–3; text private, never committed) merged into `caption_timeline.csv` (private; consecutive identical texts
with abutting times merged). Numbers only: `data/narration_stats_3b.csv`; script `scripts/narr3b.py` (reproducible from the
private tables). 6,246 words in total. Exclusions: caption segments < 2 frames were dropped by the detector; RC30-28 seg 0
illegible (`?`, not counted). Audio proxy: A27 `audio_env.csv` (10 ms). No hand-checked word-level ground truth exists.

## F-A20-101 Speech rate is ≈ 3.7 words/s ≈ 220 wpm, higher than the earlier 200 wpm (MEASURED, high for the caption-rate, n = 30; 6,246 words)
Words ÷ (last caption end − first caption start): median 3.68 w/s (IQR 3.57–3.79; range 3.33–4.08) = 220.6 wpm (214–228;
200–245). Words per caption 1.27 (1.23–1.29; 1.18–1.35); caption interval median 332 ms (320–333; 299–367).
Caveat: this is the rate of captions, which are timed to the narration (F-A20-102/103), not a direct audio measurement; the
captions run from frame 1 to video end (first caption at frame 1 in 23/30, frames 2–5 in the other 7; tail 0–0.17 s), so the span equals
the runtime and includes pauses. Words/caption was 1.16 earlier (50 words/43 tokens, 8 windows) → corrected to 1.27.
Implementation: a script of ≈ 3.7 w/s (≈ 220 wpm), i.e. ≈ 230 words for a 60 s short (112–295 seen); 1 caption per
≈ 0.33 s.

## F-A20-102 Captions are continuous; sentence-final captions are held ≈ 5 frames longer (MEASURED, medium-high, n = 30; 4,961 captions)
Gaps between consecutive captions are 0 in 99.9 % of cases (> 100 ms: 0.4 % after sentence-final, 0.1 % otherwise; the largest
total gap in any video 0.53 s), so the caption track never goes blank mid-video — pauses are visible only as longer holds.
Median hold, 1-word captions: 9 frames (300 ms) not sentence-final (n 3,379) vs 14 frames (467 ms) sentence-final (n 393);
2-word 12 vs 17 (n 998/89); 3-word 17 vs 21 (n 79/21). Excess ≈ 4–5 frames ≈ 150–170 ms. Pooled caption hold 300 ms median
(p5 100, p95 633, p99 800); not quantised to a multiple of 3 frames (34 %, chance level). Implementation: sentence boundary =
caption held ≈ +0.15 s; do not insert > 0.3 s dead air. Limits: hold = pause + final-word lengthening, not separable.

## F-A20-103 Sentences: median 11 words, 18 per video (MEASURED, medium-high, n = 30; 503 sentences)
Sentence = text run ending with `.` `?` `!`. Pooled median 11 words (IQR 7–16; 1–37). Per video: 18 sentences (14–20; 10–22), per-video
median length 11 words (10–13; 9–21.5). Implementation: write 10–13-word sentences, ≈ 1 per 3.3 s, mix with a few 1–5-word
punch lines and up to ≈ 30 words.

## F-A20-104 Caption onset leads speech energy by ≈ 140 ms (4 frames) (MEASURED, medium-high, n = 30; 474 sentence starts)
Two independent estimates agree. (a) Sentence starts (caption after `.`/`?`/`!`): first time smoothed `rms_dbfs` rises through
the mid-level between the preceding pause floor and the speech level, minus caption start (t = (f_start+1)/30): per-video
median 141 ms (range 110–167; every video 110–167 ms, n per video 9–21; pooled 474). (b) Cross-correlation of caption starts
with A27 `onset_strength` (±300 ms, 40 circular-shift nulls): peak lag median +140 ms (IQR 130–160; −240..+210), z median
4.4 (3.9–5.1; all 30 ≥ 2.9). First active speech frame in the audio tables is 0.14 s (0.11–0.18; 0.07–0.31) vs caption 0.033 s.
**Supersedes F-A20-007 (≈ 70 ms, SUPERSEDED):** that figure used a pixel-spike detector and a different onset proxy; the new
one uses exact caption segment times. A 50 %-rise threshold lags the physical onset (consonant attack), so true word lead is
probably ≈ 100–140 ms; still not a hand-checked word-timing error. Implementation: caption appears ≈ 3–4 frames before the
vowel energy; expression/mouth swaps keyed on caption onset + 3 frames.

## F-A20-105 First/last word (MEASURED, high, n = 30)
First caption at t = 0.033 s (frame 1) in 23/30; frames 2–5 in RC30-12, 16, 17, 25, 26, 27, 28 (max 0.167 s) — the narration starts at once. The
last caption is held to the last frame (tail 0.02 s median), so last-word-to-end is not measurable from captions; the audio-side
tail was not re-measured. Implementation: voice in the first 5 frames, no pre-roll.

## Phase 3B revisions
- F-A20-003 CORRECTED: 3.3 w/s (200 wpm) → 3.7 w/s (221 wpm); words/caption 1.16 → 1.27 (now n = 6,246 words, 30 videos, not 8 viewed windows). Confidence upgraded medium → high for caption-rate.
- F-A20-007 SUPERSEDED by F-A20-104 (70 ms → 140 ms; method and n stated there).
- F-A20-005 (audio gaps 0.15–0.5 s, median 0.21) is consistent with F-A20-102 (sentence-final excess ≈ 0.15–0.17 s) and stays; the earlier implementation line "sentence pause 0.3–0.5 s" is DOWNGRADED to 0.15–0.3 s (only ≈ half of sentence ends reach 0.3 s in audio: 8.5 gaps ≥ 0.3 s vs 18 sentences per video). Unresolved: no word-level ground truth.
- Contradiction recorded (not averaged): earlier 70 ms vs now 140 ms caption lead; the newer, segment-time based figure is preferred.
- Open: hand-checked word timing error; audio-side last-word-to-end; pitch second pass.
