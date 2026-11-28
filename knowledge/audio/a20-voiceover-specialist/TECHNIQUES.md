# A20 TECHNIQUES — ElevenLabs direction sheet (derived from RC30 measurements; approved for planning only)
No generation or spend is authorised by this file. No cloning or imitation of the reference narrator: choose/design an ORIGINAL voice and
use the numbers below only for pace, pause and level.

## T1 Delivery targets (source: F-A20-003/004/005/006)
| Parameter | Target | Tolerance |
|---|---|---|
| Speech rate | 3.3 words/s (~200 WPM) in spoken time — 3B caption-timeline rate over the voiced span ≈ 3.7 words/s (220 wpm, IQR 214-228), F-A20-101; use 220 wpm as the initial target | 3.0-3.9 |
| Caption/word token cadence | one token per 0.33 s (median), 1-3 words each | p90 0.57 s |
| Voice onset | <= 0.3 s after frame 0 | 0.07-0.5 s |
| Intra-sentence breath gap | 0.15-0.25 s | median 0.21 |
| Phrase/sentence-end gap | 0.3-0.5 s | none > 0.6 s |
| Voice-active fraction | ~0.6 of runtime | 0.55-0.68 |
| Pause total (> 0.25 s) | ~9 % of runtime | 5-20 % |
| Median phrase length | ~4 s | 3-6 s |
Brisk, continuous, low-dead-air read. Check the draft: if TTS speech rate at default is < 2.8 w/s, raise speed (ElevenLabs speed setting) or trim
script; verify with `words.json` (T3), not by ear.

## T2 Level and format (F-A20-001/002/008)
Narration mono; mix master -14 LUFS integrated (acceptable -15), TP <= -2 dBTP, LRA 2-3 LU; speech-band VO-to-bed margin ~12-14 dB, bed low in 300-3400 Hz.
Stereo width not needed (side 27 dB below mid). Mix belongs to A22.

## T3 Word timestamps for captions and expressions
1. Production: request TTS with timestamps (ElevenLabs character/word alignment endpoint) after director approval and credit estimate; log characters and credits.
2. Write `productions/<id>/voice/words.json`: [{word, start_s, end_s}] plus frame = round(start_s*30).
3. Caption token = 1 word (2-3 for short function-word runs like "dug a"); show caption ≈ 140 ms (≈ 4 frames at 30 fps, ≈ 3 at 24) before start_s (3B F-A20-104 supersedes the ~70 ms of F-A20-007). [Phase 4 correction 2026-11-28, D033: see knowledge/PRODUCTION_DEFAULTS.md]
4. Expression swaps/beats: frame(start_s) - 3 .. +2 (A02).
5. Verify on one hand-checked 30 s sample (error target median < 40 ms) before trusting; if no TTS timestamps, use forced alignment with an approved local tool.
6. Reference-side proxy (no audio words available): caption-pixel spike detector `scripts/cap20.py` + `capev.py` (recall ~94 %, ~10 % spurious).

## T4 Casting sanity checks (F-A20-009, low confidence)
Single narrator voice for the whole video, constant settings across all videos (reference F0/centroid spread across videos +-5 %). Measure a candidate's
pyin F0 median/p10/p90 and centroid with `scripts/audio_an.py` for comparison, but do not chase 205 Hz: the reference F0 estimate is bed-biased.
No separate character voices needed (F-A20-010).

## T5 Reproduce
`.venv-analysis/bin/python -I scripts/audio_an.py <n>` (run with cwd = output dir) -> aud_<n>.json; `cap20.py <n>` -> capser_<n>.npy; `capev.py`;
`xcorr.py`; `capstat.py`; `agg.py` (writes data CSVs). Inputs: `~/ricks-clips-private/reference-videos/RC30/<n>.mp4`.

## T6 ElevenLabs direction sheet for an ORIGINAL narrator (Phase 4, 2026-11-28; planning only, no spend authorised)
Evidence for numbers: F-A20-101..105 (MEASURED, reference). The ElevenLabs facts below are from the director's connector report
and general product knowledge: INFERRED / HYPOTHESIS until the 6 s test (`pipeline/voice/TEST_PLAN_6S.md`) verifies them.
| Item | Direction |
|---|---|
| Identity | One original library/designed voice, constant across all videos. Never clone, never imitate the reference narrator or any real person; do not chase the reference F0 (bed-biased, F-A20-009). |
| Pace | ~220 wpm (3.7 w/s over the voiced span; accept 3.0-3.9), sentences ~11 words, breath gap 0.15-0.3 s, no pause > 0.6 s. Measure with `words.json`, not by ear. |
| Model A: `eleven_multilingual_v2` | Has a `speed` voice setting (HYPOTHESIS: 0.7-1.2) and SSML `<break time="0.3s"/>` for pauses; stable, predictable; ~1 credit/char (120 credits for the 6 s test line). First choice for the test: pace is tunable by parameter, and `align.py` strips the break tags. |
| Model B: `eleven_v3` / v4 | Expressive, inline audio tags (`[whispers]`, `[excited]`); tags are text, so they cost characters and appear in alignment text (`align.py` masks them). HYPOTHESIS: no `speed` knob, so pace is steered by punctuation/wording and stability presets; less predictable duration. Try only after Model A passes; one variable at a time. |
| Flash/turbo | Cheaper (HYPOTHESIS ~0.5 credit/char), lower expressiveness; use for non-final timing drafts only if the director approves the spend. |
| Settings start | stability 0.5, similarity 0.75, style 0, speaker boost on, speed 1.0 (raise toward 1.1 only if wps < 2.8). Keep identical across videos; change one setting per experiment. |
| Text prep | Short sentences (~11 words), commas for breath, spell out numbers/acronyms, no stage directions in the narration text, pronunciation fixes via respelling or an approved pronunciation dictionary, log every substitution. |
| Timing source | Preferred: API `/with-timestamps` (free with the TTS call; needs an API key - not available). Fallback: Scribe `words` (extra credits, ~tens of ms edge error unverified) -> `align.py scribe`. Local forced alignment only with an approved tool. |
| Cost control | 1 take per test; log characters, credits, settings, flow id in the manifest; estimate before every call; keep scripts short; free tier is non-commercial + attribution (user decision on a paid plan before any release). |
| Post | trim to <= 0.2 s head / <= 0.3 s tail (`silence.py`), `normalize.sh vo` (-14 LUFS, TP -2, mono 48 kHz); A22 does the real mix (bed -20 dB re VO, static). |
Caption token rule: default one word per token (PRODUCTION_DEFAULTS); function-word merging (T3.3 "dug a") is an optional experiment (`captions.py --merge-function-words`).
Tools: `pipeline/voice/` (CONTRACT.md).
