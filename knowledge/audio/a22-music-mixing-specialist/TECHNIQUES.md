<!-- owner: a22-music-mixing-specialist | status: draft-from-measurements | version: 0.1 | last_updated: 2026-11-28 -->
# A22 TECHNIQUES — music brief and mix chain (derived from RC30 measurements; nothing auditioned)
All values are targets inferred from measurements (see FINDINGS IDs). No music asset exists yet: therefore no licence
entry is required; when one is produced/sourced, add a row to `knowledge/audio/a22-music-mixing-specialist/LICENCES.md`
(source, licence, URL/author, date, checksum) BEFORE use. Only original or free-licensed (CC0/CC-BY with attribution
recorded) music; no paid libraries or AI-music subscriptions without user approval. Never reuse reference audio.

## T1 Music brief template (ORIGINAL or licensed bed)
| Field | Target | Source |
|---|---|---|
| Role | continuous under-bed, 0 s to end; never stops; no intro, no outro tail | F-A22-001, 008 |
| Length | cover 31–78 s (median ≈ 62 s): deliver a 8–10 s seamless loop + 60–80 s extended render | F-A22-004 |
| Loop | 4 bars at ≈ 96–104 BPM (9.2–10 s) or 3 bars at 100 BPM (7.2 s); loop point on a chord boundary, tail-free, equal start/end level; test with sample-exact loop at 3 repetitions | F-A22-004 (HYPOTHESIS: grid) |
| Tempo | ≈ 100 BPM nominal but no perceptible beat grid needed; no drum kit, no backbeat | F-A22-004, 002 |
| Key / mode | D minor (alt. E minor, relative F major); diatonic D E F G A (+Bb/C ok), avoid chromatic leading tones | F-A22-003 |
| Instrumentation | soft sustained pad + sparse plucked/mallet-like notes (one note per 0.3–1 s); centroid 1.0–1.6 kHz; harmonic ≫ percussive; no sub-bass solo lines | F-A22-002 |
| Dynamics | static: per-second level SD ≈ 3–4 dB, no builds, no drops, no sections | F-A22-001 |
| Stereo | bed side (L−R)/2 ≈ −30 dB re its own mid at the master (pad wide, bass/mallets centred); pad-reverb stereo | F-A22-001 |
| Spectrum | energy 100–700 Hz centre of mass; roll-off above 4 kHz in the side; a low bass layer 40–100 Hz about −25 dB re total | F-A22-006, 010 |
| Ending | no fade/outro; picture ends 0.1–0.8 s after last word; optional 0.5–1 s impact or riser in the last second (≈ 15–20 % of videos: +14..+25 dB side burst) | F-A22-008 |
| Deliverables | stereo 44.1/48 kHz 24-bit WAV loop; stems: pad, mallet, bass (if any); BPM/key metadata; licence row | — |
Acceptance by measurement (replaces listening for the automated check): side-channel level median −48.6 ± 3 dBFS-ms at
master; side−mid −30 ± 3 dB; chroma-autocorr loop lag 6–10 s peak ≥ 0.3; no flat-top peaks.

## T2 Mix chain targets (voice-first, bed static)
1. Voice bus (mono, from A20 ElevenLabs render): high-pass ≈ 110–120 Hz (steep, ≥ 18 dB/oct; reference spectrum steps
   +10 dB across 100→126 Hz), gentle body 160–250 Hz (reference peak), −4 dB/oct tilt 250 Hz→3 kHz, +4 dB shelf/bell
   4–8 kHz presence; compression to LRA ≈ 2–3 LU (ratio ≈ 3:1, fast attack, 8–10 dB reduction on peaks; VO is heavily
   levelled: LRA median 2.2). FFmpeg: `highpass=f=115:poles=2,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6000:t=q:w=0.7:g=3,
   acompressor=threshold=-24dB:ratio=3:attack=5:release=120:makeup=6`. [values are starting points, HYPOTHESIS, to be
   verified against the T4 spectrum check]
2. Bed bus: bed at −20 dB re voice RMS (start; allowed −14..−24); side width as brief; no sidechain ducking (F-A22-005):
   `[bed]volume=-20dB[b];[vo][b]amix=inputs=2:normalize=0:duration=first`. If a duck is wanted for clarity, keep ≤ 1 dB —
   the reference has none (< 0.5 dB).
3. Master: two-pass `loudnorm` to I = −14 LUFS, TP = −2 dBTP, LRA = 3 (reference LRA 1.6–3.5):
   pass 1 `ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-2:LRA=3:print_format=json -f null -`, pass 2 same filter with
   `measured_I/LRA/TP/thresh/offset` and `linear=true`; then `alimiter=limit=0.794:level=disabled` (−2 dBFS ceiling) if
   the measured TP exceeds −2. Final upsample/encode: AAC ≥ 128 kb/s 44.1/48 kHz; re-measure with `ebur128=peak=true`
   after encoding (codec can add ≈ 0.3–1 dB TP). Accept: −14.0 ± 0.3 LUFS (or −14..−15 as in the 7 quieter reference
   videos), TP ≤ −2.0 dBTP (project rule ≤ −1), PLR 11–13 LU, mid crest 14–15.5 dB, peak-flat-top share < 0.01 %.
4. Mono-compatibility: master is near-mono (L/R corr 0.98–1.0, side −27.5 dB re mid, A20 F-002): keep SFX centred,
   bed wide only in pads.

## T3 Measurement recipe (reproducible, `scripts/`)
`a22_an.py NN` per video (ffmpeg pipe decode → M=(L+R)/2, S=(L−R)/2 → STFT 2048/441 hop at 22.05 kHz; Otsu speech mask on
300–3400 Hz; band levels; side chroma/key/loop; novelty), `a22_duck.py NN` (event-triggered averages vs 100 shuffled
controls), `a22_struct.py`, `a22_agg.py` (tables). Run for a produced mix: expect the T1/T2 acceptance numbers; deviations
> 3 dB flag a problem. Run from repo root with `.venv-analysis/bin/python`.

## T4 Mix check before delivery
side-level median, side−mid, voice-active minus gap (400–2000 Hz) = 12–14 dB (bed upper bound −14), bass band act-gap ≈ 0,
LTAS 1/3-octave curve within ±3 dB of `data/ltas_third_octave.csv`, no ducking ETA (> 1 dB dip = remove).

## T5 Mix recipe, Phase 3B update (supersedes the numbers in T2.2 and T2.3 where different; v0.2)
| Stem | Target | Measure | Source |
|---|---|---|---|
| VO | speech-frame K-weighted level -13.2 LUFS on the master (IQR -13.5..-13.1); stem LRA 2-3 LU | 10 ms mean-square, voiced frames | F-A22-100 |
| Bed | **-20 dB re VO in 400-2000 Hz (+-3), static, from t=0 to end, no sidechain duck** (allowed duck <= 1 dB; reference < 2 dB on bass/side) | stem vs stem, voiced frames, mean power | F-A22-100, 102 |
| Bed check on master | pause frames (>= 150 ms, 50 ms trimmed) -17.2 +-1.5 LUFS; side 400-2000 voiced-minus-pause 0.8 +-2 dB | master only | F-A22-100 |
| Bed spectrum | full-spectrum floor: 4-8 kHz in pauses >= speech frames; 30-150 Hz about 4 dB under speech | master | F-A22-100 |
| SFX | no level measured (A21 detection failed); keep SFX peak below VO peak, no sub-bass solo | - | F-a21-102 |
| End | optional 1.5-2 s low-weighted swell in the last 3 s for ~1 in 8 videos | - | F-A22-103 |
| Master | -14 LUFS integrated (accept -14.0 +-0.3; reference whole-file -14.1), TP <= -2 dBTP (project rule <= -1), LRA <= 3 LU, PLR 12 | ebur128 peak=true after encode | F-A22-009 |
Tempo: no BPM requirement (F-A22-104); write at any 60-120 BPM, loop 6-10 s. Pause-based checks always state definition B above.
