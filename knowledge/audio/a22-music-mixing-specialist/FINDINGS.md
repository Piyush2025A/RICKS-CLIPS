<!-- owner: a22-music-mixing-specialist | status: complete-phase3 | version: 0.1 | last_updated: 2026-11-28 -->
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

## F-A22-005 Bed is NOT ducked under speech (MEASURED, medium-high, n = 30)
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

## F-A22-006 Bed-to-voice ratio: −14 dB upper bound (mid), ≈ −27 dB (side only) (MEASURED/INFERRED, medium, n = 30)
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
