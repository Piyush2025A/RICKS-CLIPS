<!-- owner: a22-music-mixing-specialist | status: complete-phase3+3B | version: 0.2 | last_updated: 2026-11-28 -->
# A22 FINDINGS — music bed and mix (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A22.
Videos covered: 30/30 computational (native 44.1 kHz stereo, decoded in memory by ffmpeg pipe, nothing written but JSON/npy
numerics; no temporary WAVs). Visual ledger: 0 records (no images opened; no spectrograms rendered). The agent cannot hear:
every claim is computational. Scripts: `scripts/a22_an.py` (per video), `a22_duck.py`, `a22_struct.py`, `a22_agg.py`;
data: `data/music_per_video.csv`, `data/pv/*.json`, `data/eta_*.json`, `data/ltas_third_octave.csv`,
`data/music_change_vs_cuts.json`. Level unit "dBFS-ms" = mean-square dB re full scale of the (L−R)/2 or (L+R)/2 signal
(STFT-power converted, offset −58.96 dB). Quartiles = IQR across videos. Frozen rcpipe was not edited.
Shared limits: music is only separable in the stereo side channel (L−R)/2 (voice is mono → absent there; A20 F-002,
A21 F-002); a bed that is mono (centre) is invisible to the side view and hidden under the voice in mid. Source is
lossy AAC ~128 kb/s. Reference clips are never reproduced; all numbers describe craft for ORIGINAL music.

## F-A22-001 A stereo bed is present for the whole runtime in all 30 videos (MEASURED, medium-high, n = 30)
Side level per second (median of 20 ms frames): video median −48.6 dBFS-ms (IQR −49.8..−47.3; −54.0 RC30-21 .. −42.6
RC30-15); side minus mid −30.0 dB (−30.8..−28.5; −35.6..−24.4). No video has a section without side energy: the fraction
of 1-s windows more than 6 dB under the video's own median ("dropouts") is median 5 % (IQR 3–11 %); per-second SD 3.8 dB
(3.2–4.9; 1.7 RC30-22 .. 5.2 RC30-25). Not voice leakage: speech-active minus gap side level median +0.45 dB
(−0.3..+1.3; 3 outliers 1.6, 4.7, 10.1 caused by an end hit, RC30-03 10.1); per-second corr(side, mid) median 0.10
(−0.39..+0.34). So: continuous bed, no sections, no silent videos. Bed on/off/section structure is therefore NOT a style
element; the bed never stops. Limit: absence of a *mono* bed in some video cannot be excluded. Implementation: bed
runs from t = 0 to the last frame; no dead intro/outro.

## F-A22-002 Bed is tonal, sustained, harmonic-dominant, mid-range (MEASURED, medium, n = 30; instrument class HYPOTHESIS)
Side-channel spectral flatness ~0 (median < 1e-4; max 7e-4) = strongly peaked/tonal spectrum; spectral centroid median
1158 Hz (IQR 1028–1539; 789–3881; RC30-25 3881 outlier); harmonic/percussive energy ratio (HPSS, side) median +3.4 dB
(+1.6..+4.6; −5.8..+9.6): harmonic > percussive in 25/30, percussive-dominant in 5 (RC30-04, 05, 18, 21, 25 → −1.3, −1.6,
−0.8, −2.5, −5.8). Combined with A21 F-002 (OBSERVED: narrow tonal lines 250–700 Hz, partials to 4 kHz, notes
changing every 0.3–1 s) the class is "soft tonal pad / plucked-mallet-like arpeggio, no drum kit". HYPOTHESIS (low):
marimba/pluck vs synth cannot be separated by these features; the presence of a kick/snare backbeat is not supported
(percussive-dominant only in 5 videos, none shows beats, see F-A22-004). Implementation: low-density melodic pad/mallet
music, centroid ≈ 1.0–1.6 kHz, no drum loop.

## F-A22-003 Tonal centre mostly D (minor-leaning) (MEASURED, low-medium, n = 30)
Side chroma (22.05 kHz, 2048 FFT, frames > −21 dB offset scale), Krumhansl–Schmuckler best match: D minor 17/30, E minor
7, A minor 3, B major 1, C minor 1, A major 1 → D/E/A minor family 27/30. Median pitch-class profile (C…B): .075 .080
**.109** .077 **.116** .103 .058 .078 .060 .098 .072 .062; D, E, F, A strongest; G♯, F♯, B weakest → a D-minor/F-major or
E-Phrygian-ish diatonic set (D E F G A with A, no leading tone emphasis). Peak/mean of the profile only 1.35–2.0 and
winning correlation median 0.74 (0.44–0.90): key evidence is weak per video; 17/30 agreement on one tonic is the
stronger evidence. Limit: side-channel only; tuning assumed 440 Hz (tuning offset not estimated). Implementation: write
the original bed in D minor (or relative F major), 5–7 note diatonic palette, no chromatic leading tones.

## F-A22-004 No reliable tempo / no pulse; loops are 6–10 s (MEASURED, low for tempo, medium for loops, n = 30)
Tempo: librosa beat_track (start_bpm 100, side onset envelope) → median 103 BPM (IQR 98–110; 77–120): that is the prior
of the tracker, not evidence. Onset-autocorrelation peak strength (the confidence) median 0.09 (0.07–0.11; 0.05–0.19)
— weak; the autocorrelation BPM is scattered 44–200 (median 79 … 97), unsupported across videos. Beat-interval CV
only computed for the tracker output. Conclusion: no audible-grid pulse is measurable in the side channel
(CONSISTENT with sustained pad/slow notes). Loop length: chroma-frame autocorrelation, strongest lag 1–15 s per video:
median 9.0 s; values cluster at 9.0–10.0 s (13 videos), 6.0–7.2 s (9), 8.0–8.5 s (4), 10.5–11 s (2), 13.3–13.8 (2); in
17 videos another top-4 peak sits at 2× or ½× (e.g. 6.34/12.68, 6.88/13.76, 7.2/14.4) → real repetition. Peak strengths 0.13–0.68
(median 0.35). Validation: RC30-27 gives 4.24/8.5 s; A21 viewed ≈ 4.5 s on a spectrogram. Cross-check: 9.0–10 s = 4 bars of
4/4 at 96–107 BPM or 16 beats; 6–7.2 s = 3 bars at 100 BPM. HYPOTHESIS (low): music written on a ~100 BPM grid with
4-bar loops; the grid is not independently measured. Limits: chroma loop lag is also the harmonic-progression period,
not necessarily a sample loop; no shuffled control for the autocorrelation peak (could be run). Implementation: bed
loop 8–10 s (4 bars at 96–104 BPM or any slow tonal ostinato), looped/extended to 35–78 s; do not rely on beat-grid sync.

## F-A22-005 [CONFIRMED and scoped by F-A22-102] Bed is NOT ducked under speech (MEASURED, medium-high, n = 30)
Event-triggered averages (20 ms frames, ±1 s; baseline −1.0..−0.7 s) around 2,583 speech onsets and as many offsets (speech mask:
A20 Otsu on 300–3400 Hz of mid, closed 100 ms; n onsets per video 41–133, median 90 = word/phrase starts after ≥ 100 ms of low energy), minus the mean of 100 shuffled-event controls per
video, median across videos:
- side 300–3000 Hz: onset −0.18..+0.23 dB, offset −0.18..+0.25 dB; |z| > 3 in 3/30 (onset), 1/30 (offset) videos.
- mid 30–90 Hz (bass; voice-free): onset −0.47..+0.29 dB; offset −0.39..+0.26 dB; |z| > 3 in 1/30 and 0/30.
- side 30–150 Hz: −1.3 dB dip at −0.2 s before onsets (|z| > 3 in 0/30), ≈ noise.
Level during speech minus during gaps: side 300–3000 −0.14 dB (−0.44..+0.23); bass −0.08..+0.08 dB (−0.6..+1.6).
Duck depth < 0.5 dB in every view that is free of voice. This supersedes A20's "inconclusive": no sidechain ducking
exists; bed sits at a fixed offset under the voice. Limits: the bed's mono/mid speech-band component is masked by voice
and cannot be tested; per-video ETAs have 41–133 events (noisy, ±1 dB). Implementation: do NOT sidechain-duck; static
bed level, no pump. (Contradiction note: none; refines A20-F008.)

## F-A22-006 [PARTLY SUPERSEDED by F-A22-100/101: -14 is the mean-pause bound, -20 the single target] Bed-to-voice ratio: −14 dB upper bound (mid), ≈ −27 dB (side only) (MEASURED/INFERRED, medium, n = 30)
Mid, 400–2000 Hz: voice-active minus gap level 13.6 dB (13.2–14.6) — reproduces A20 (13.9) with a different STFT;
gap level = bed + voice tails + room, so this is an UPPER bound on bed level: bed ≤ −13.6 dB re voice. Side, same band:
voice (mid-active) minus side-gap 27.2 dB (25.9–28.8): the stereo part of the bed is ≈ −27 dB re voice. Other bands
(mid, active − gap): sub 30–100 Hz +0.9 dB (0.1–2.0), 100–400 Hz +5.8 (4.5–6.7), 2–8 kHz −1.5 dB (−2.1..−1.1). Reading:
in 30–100 Hz and 2–8 kHz the voice does not exceed the gap level → those bands are bed/noise-dominated; i.e. bed has
bass (≈ voice-level-independent rumble −22..−27 dB re total in the 40–100 Hz thirds) and a hi band as strong as in
speech. Total bed estimate: −14 to −27 dB re voice RMS; best single value INFERRED −20 dB (HYPOTHESIS, low); bed fully
wide ≈ −30 dB side re mid (F-A22-001). Implementation: music bus at −20 dB under VO (speech-band) as start, A/B −14..−24
in a listening-free check using LUFS gap-vs-speech difference of 12–14 dB on 400–2000 Hz.

## F-A22-007 Music changes do not align with shot boundaries (MEASURED, low-medium, n = 24 of 30 videos)
(6 videos lack shot_candidates: RC30-06, 09, 10, 11, 13, 21 — v0.2.0 batch incomplete.) Side-chroma+MFCC novelty
(25-frame windows) vs cut/gradual candidates (±0.25 s max novelty) against 300 uniform random time sets per video:
median z +0.45 (IQR −0.26..+1.44); p < 0.05 in 4/24 (chance ≈ 1.2); p > 0.95 in 0/24; median distance from a cut to
nearest music-change peak 1.01 s vs 1.15 s random (p ≤ 0.05 in 2/24). Music-change peaks 2.5 per 10 s (2.2–3.0) =
note-level changes, not section changes. Flash candidates (n = 4 videos) z −0.4. Story-beat (A19 act) alignment NOT
tested (act tables not used; time). Conclusion: bed is a loop running under the edit; cuts are not music-cut.
Implementation: lay one continuous bed under the picture; do not cut music at shots. Candidate lists have false
positives (calibration doc), which dilutes any real effect.

## F-A22-008 Endings: no tail, no outro; ~1 in 6 has a final hit (MEASURED, medium, n = 30)
Last voice frame is 0.1–0.8 s before the end (median 0.3 s; longest RC30-28 0.8 s) → no music tail/outro after
the voice in any video. Side level in the last second vs video median ≥ +14 dB in 5 videos (RC30-03 +21.9, 06 +17.5,
08 +21.9, 10 +25.3, 21 +14.1, the last also ramping +9..+14 over 5 s), +6.2 RC30-26, +5.6 RC30-11; RC30-29 drops −21.5 dB
(side cut to near-silence). 1-s resolution, so hit vs swell not separable; A21 saw the RC30-10 event as a ≈ 1 s decaying
broadband swell at 64.4 s. Implementation: cut the picture at the end of the last word + 0.1–0.4 s; optional 0.5–1 s
impact/swell in the last second for ≈ 15–20 % of videos; no fade-out tail.

## F-A22-009 Master: −14 LUFS, TP −2 dBTP, PLR 12, crest 14.8 dB, not clipped (MEASURED, high, n = 30)
Integrated −14.1 (A20 F-001 reproduced as input: not re-measured), TP −2.1 → PLR ≈ 12.0 LU. Mid sample-peak minus
RMS (crest) 14.8 dB (IQR 14.5–14.9; 13.9–15.7); share of samples within 0.5 dB of the peak ≈ 0 (< 0.01 %) → peaks are
not flat-topped: a true-peak limiter/soft normaliser with ceiling ≈ −2 dBFS, not clipped. Limit: crest/limiter reading
of the mid mix only. Implementation: see TECHNIQUES.

## F-A22-010 Long-term spectrum of the mix (MEASURED, high, n = 30; per-video IQR ≤ 4 dB per band)
`data/ltas_third_octave.csv` (Welch 8192, mid, 1/3-octave power re total). Median: 32 Hz −34.9, 63 Hz −25.5, 100 Hz −22.0,
126 Hz −11.9 (a +10 dB step in one third = steep high-pass at ≈ 110–120 Hz on the voice, bass bed below), peak 160 Hz
−7.7, 250 Hz −8.7, 500 Hz −11.9, 1 kHz −17.3, 2 kHz −20.9, 3.2 kHz −22.9 (trough), 4 kHz −20.8, 5 kHz −18.2, 6.4 kHz
−18.9, 8 kHz −18.1. Shape: ≈ −4.2 dB/octave from 250 Hz to 3 kHz, +4..+5 dB bump 4–8 kHz (presence/air, de-esser-free
bright top), steep low cut at ≈ 110 Hz. Narrow video-to-video IQR (≈ 1 dB at 100–1000 Hz) = one preset applied to every
video. Side spectrum: −40 dB re total, 300–700 Hz max (−37 at 635 Hz); falls to −49 dB at 4 kHz. Implementation:
EQ targets in TECHNIQUES.

## Contradictions / open
- A21 reads the bed as "20–30 dB under VO"; here: ≤ −14 dB (mid upper bound) and −27 dB (side). Both reported, not averaged.
- Tempo not established; loop is. Ducking absent (A20 inconclusive → resolved for voice-free views).
- Not done: A19 act alignment, shuffled null for loop peaks, mono-bed estimation by source separation (not attempted),
  spectrogram renders. RC30-27 stored `act` from an earlier pre-patch run was re-run; others consistent.

## Phase 3B additions (2026-11-28)
Visual ledger: 0 records (no frames/spectrograms opened by A22); computational: 30/30 native audio, decoded in memory at 48 kHz.
Script `scripts/a22_3b.py` (+ `a22_3b_agg.py`), data `data/pv3b/NN.json`, `data/bed_level_3B.csv`. Method: mid=(L+R)/2, side=(L-R)/2;
STFT 2048/480 (10 ms); speech = Otsu on 300-3400 Hz mid (5-frame smoothing, closing 90 ms); voiced = speech eroded 30 ms.
Pause definitions: **A** (old) inactive run >= 150 ms, untrimmed; **B** same, 50 ms trimmed each side (= A21-like); **C** strict: frames
>= 15 dB under the speech median, runs >= 150 ms, 30 ms trimmed (n 4-19 pauses, 0.5-2.9 s per video). Level = mean power in band. K-weighting = BS.1770 filters, 10 ms mean-square L+R, not gated.

## F-A22-100 Bed level re voice, independent re-derivation: the earlier and A21 numbers are the same quantity at different pause strictness (MEASURED, high for the numbers, medium for the interpretation, n = 30)
Voiced minus pause, mid 400-2000 Hz, median (IQR): **A 14.4 (13.9..15.1)**, **B 14.8 (14.2..16.0)**, **C 20.6 (19.9..21.8)**; B pause 10th-percentile floor
**24.8 (23.8..25.5)**; side 400-2000 (voiced mid minus side pause, B) **28.0 (26.3..29.2)**. A21: mean 15.6, floor 24.6, side 27.1 -> reproduced within 0.8-1.2 dB (speech-mask difference).
Explanation: my "<= -14 mid" = mean power in all inactive runs (includes voice tails/breaths/room, so an UPPER bound, stated as such in F-A22-006); my "-27 side" = stereo part only;
A21's "20-30 dB" = pause floor / side. No contradiction: mean pause -15, strict pause -21, floor -25, side-only -28. The mid bed is therefore between -15 and -25 dB re speech in the voice band;
the strict-pause value (-20.6, frames that are truly quiet) is the best single estimate (INFERRED, medium; the bed cannot be separated from room/codec noise).
**PRODUCTION TARGET (one value):** music bed stem, mean power in 400-2000 Hz over voiced frames = **-20 dB re the VO stem in the same band and frames, tolerance +-3 dB** (accept -17..-23).
End-to-end check on the final master (no stems needed): mean K-weighted level of pauses (>= 150 ms, 50 ms trimmed) = **-17.2 LUFS (IQR -17.7..-16.4; -21.0..-15.1)**, voiced frames **-13.2 LUFS (-13.5..-13.1)**,
ungated whole-file -14.1 (-14.3..-14.1); accept pause level -17.2 +-1.5 LUFS. Caveat (MEASURED): full-band K-weighted voiced-minus-pause is only 4.0 LU because the pause floor is full-spectrum (bass and 4-8 kHz): in pauses the 4-8 kHz power is 4.6 dB (IQR 4.1..5.5) ABOVE speech frames and 30-150 Hz is only 4.1 dB (3.0..4.6) below; this bed/room/codec hiss share cannot be split without stems (not attempted). Do not set the bed by full-band LUFS alone; set it in 400-2000 Hz.

## F-A22-101 Pause-based bed estimates depend on the pause definition by 6 dB (MEASURED, high, n = 30)
A -> C moves the 400-2000 Hz difference 14.4 -> 20.6 dB, the floor 24.8; side 400-2000 voiced-minus-pause stays +0.8 dB (B; IQR -0.1..1.6) = the stereo bed does not follow the voice. State the definition with every bed number.

## F-A22-102 Ducking re-test on voice-free views: none >= 2 dB (MEASURED, medium-high for 30-90 Hz and side, n = 30)
Voiced minus pause (B), negative = bed ducked under speech: bass 30-90 Hz (voice-free; voice is high-passed at ~115 Hz) **+1.2 dB (IQR -0.2..+2.5)**, videos <= -2 dB: 2/30 (RC30-08, 29), <= -1 dB: 5/30;
side 400-2000 Hz +0.8 (-0.1..+1.6), <= -2: 1/30 (RC30-12); side 30-150 Hz +2.2 (0.1..5.2), <= -2: 3/30 (22, 27, 08). Paired test (each pause vs the 300 ms voiced on both sides, n = 4-22 pauses, bootstrap CI): bass 30-90 median +2.1 dB (1.3..3.5), side 400-2000 +0.7 (-0.2..1.5); no video has a CI entirely < 0 on bass.
The bass is slightly HIGHER during speech (voice plosives/low-end spill or bed rise), the opposite of ducking. 30-150 Hz and 4-8 kHz are NOT clean: they contain voice (30-150 Hz +4.1 dB, 4-8 kHz: pause 4.6 dB louder than speech but sibilants make paired values +4 dB), so they are not diagnostic of ducking and are excluded from the claim.
Scope: no ducking of the bed in bass 30-90 Hz (mid) and in the stereo side signal; a mid speech-band duck of < 3 dB hidden under the voice cannot be excluded (the bed there is 15-25 dB below the voice). Combined with F-A22-005 ETAs: no sidechain ducking; implementation unchanged. Contradiction with A28 §3 concern: resolved as "valid only for voice-free bands", done.

## F-A22-103 End swell verified in 4 videos by both methods, 2 more disputed (MEASURED, medium, n = 30)
Side 60-1000 Hz, 100 ms frames, max of last 4 s minus body median, versus 300 random 4 s windows (p95): exceeds the control p95 in RC30-03 (29.6 dB), 06 (21.4), 08 (25.1), 10 (27.2) and 11 (7.8 dB rise vs its own low p95 6.1); A21 (different bands/frames) lists 01, 03, 06, 08, 10. Agreement 03, 06, 08, 10 (4/30); disputed 01 (8.0 dB rise, p95 11.5: not significant here) and 11 (A22 only). Others >= 10 dB but below their own p95 (04, 09, 12, 21, 23, 25, 26): bed note changes, not counted. Duration above body +6 dB: 03 1.6 s, 06 2.2, 08 1.1, 10 1.8, 21 2.2 (not significant) -> 1.1-2.2 s, matches A21's 1.5-2 s. Peak times 57.6, 64.6, 62.1, 64.4 s (0.4-2.9 s before the end). So: end swell exists in 4/30 (13 %) with high agreement, 2 more candidates unresolved. Implementation: optional 1.5-2 s swell in the last 3 s for roughly 1 in 8 videos.

## F-A22-104 Tempo: pulse measurable in 13/30 only, scattered; no common BPM (MEASURED, medium, n = 30)
Onset-envelope (side, 10 ms) autocorrelation peak in 60-140 BPM vs 100 block-shuffled nulls (1 s blocks): peak median 0.07 vs null 0.04 (sd 0.01); z > 3 in 13/30 (RC30-02 103 BPM, 03 61, 05 100, 07 68, 12 76, 14 107, 15 97, 17 65, 19 70, 21 65, 22 118, 27 75, 30 103); not significant 17/30. BPM of all 30: 61..136, median 92, no cluster -> the earlier ~100 BPM (F-A22-004) is NOT supported as a rule; where a pulse exists it is 61-118 BPM (note: 61-76 may be half-time of 122-152). Confidence low for any BPM value. The 6-10 s loop (F-A22-004) stands.
## F-A22-105 Track structure: one continuous bed per video (MEASURED, medium, n = 30)
Cosine of mean side chroma in adjacent 6 s windows: median 0.98 (IQR 0.96..0.98), minimum per video median 0.95 (0.83..0.99); lowest RC30-10 0.83, 08 0.86, 03 0.88, 28 0.89 (the end-swell videos, i.e. the swell, not a track change). No video shows a window pair < 0.8 -> no track change / key change in any of 30; with F-A22-001 (bed present throughout, 30/30) the bed is one track per video. Caveat: a change between two similar-key loops would not show in chroma.

## Phase 3B revisions
- F-A22-006: bed-vs-VO upper bound -14 and side -27 are KEPT but reinterpreted (F-A22-100); single target -20 dB (+-3) in 400-2000 Hz. "best value -20, HYPOTHESIS low" upgraded to INFERRED medium (strict-pause 20.6, floor 24.8 agree).
- F-A22-005: confirmed, now scoped (F-A22-102): bass 30-90 and side only.
- F-A22-004: "~100 BPM nominal" DOWNGRADED: tempo has no common value (F-A22-104). Loop result unchanged.
- F-A22-008: end hits: 4 videos confirmed as ~1.1-2.2 s swells (F-A22-103); the old list (21, 26, 11) was 1-s resolution and is partly noise (21 not significant here). RC30-29 near-silent side at the end not re-tested.
- Contradictions: none open. A21 reconciliation done; A21/A22 disagree on RC30-01 and RC30-11 as end-swell videos (reported, unresolved).
