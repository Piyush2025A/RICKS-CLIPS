# TEST_PLAN_6S — minimal 6-second ElevenLabs integration test (NOT RUN; needs user approval)
Owner A20. Purpose: prove, end to end, generate -> download -> private storage -> intake -> word timing -> captions ->
loudness, with the smallest possible spend. Nothing here runs until the director records the user's approval and the
credit figure. No cloning; no reference narrator imitation.

## Spend (estimates; confirm at approval time)
| Item | Basis | Credits |
|---|---|---|
| 1 take, eleven_multilingual_v2, 136 characters | director priced a 6 s line at 120 credits (~1 credit/char); 136 chars -> **~136** (INFERRED, +-10 %) | ~136 |
| Scribe (`eleven_scribe_v1`) on the ~7 s result | **TBD** - director to read the price from the connector before approving | TBD |
| Retakes | none; a failed check is reported, not re-rolled | 0 |
Account: free tier, 4,989 credits left (director, 2026-11-28). Free tier = non-commercial + attribution: this test is
internal; a commercial release needs a paid plan (user decision). Record licence tier in the manifest.

## Line (original, 22 words, 136 chars; ~6 s at 220 wpm)
"The lighthouse keeper counted seven storms, and none of them frightened her. The eighth one, though, knocked politely at the front door."
Two sentences (11 + 11 words) = the reference sentence length; has a comma pause, a sentence-final hold and a hyphen-free,
number-free text (pronunciation risk low). Save verbatim to `productions/TEST6S/voice/script.txt` before generating.

## Settings
Model `eleven_multilingual_v2` (supports `speed`, SSML `<break>`); stability 0.5, similarity 0.75, style 0.0, speaker boost on,
speed 1.0 (raise to 1.1 only in a *later* approved take if wps < 2.8). Output mp3_44100_128 (or the connector default; record it).
Voice: ONE library/designed voice chosen by the director via `creative_list_voices`: mature, warm, neutral-accent narrator,
brisk but not hurried, no celebrity/character likeness, not a clone. Offer 2 names in the approval request; generate only the
first (1 take). Voice id must come from the connector, never from memory.

## Steps and checks
Let `P=~/ricks-clips-private/audio`, `D=productions/TEST6S/voice`, PY=`.venv-analysis/bin/python -I`.
1. Director: `creative_create_flow`, `creative_generate_speech` (generations_count 1), poll the flow; note flow_id, credits.
2. Download the audio to `$P/raw/` (private; never committed).
3. Intake: `$PY pipeline/assets/intake.py <file> --kind audio --request-id TEST6S-take1 --provider elevenlabs --model eleven_multilingual_v2 --prompt-file $D/script.txt --settings-json <settings.json> --credits <actual> --store ~/ricks-clips-private`
   (check the store layout in intake.py first). PASS: sidecar with sha256, `--credits` recorded.
4. Silence: `$PY pipeline/voice/silence.py <audio> -o $D/silence.json`. PASS: first voiced <= 0.5 s; no internal pause > 0.6 s (warning otherwise).
5. Scribe on the raw audio (connector `creative_transcribe_audio`; cost approved above) -> save JSON as `$D/scribe.json`.
6. `$PY pipeline/voice/align.py scribe $D/scribe.json --script-file $D/script.txt --duration <ffprobe> --audio-sha256 <sha> -o $D/words.json`.
   PASS: 22/22 words matched (match_ratio >= 0.95), 0 validation issues, mean confidence >= 0.8.
7. Timing accuracy: hand-check 10 words (onsets read from the waveform/spectrogram plot with word markers; method in
   reports/); PASS: median |auto - manual| < 40 ms (target from the role spec). Scribe word edges are expected to be less
   exact than API alignment; if the median is 40-80 ms, report it and decide whether captions (140 ms lead) tolerate it.
8. `$PY pipeline/voice/captions.py $D/words.json --fps 30 24 --srt -o $D`. PASS: 0 warnings; lead 4 f @30 / 3 f @24; contiguous.
9. Trim (if the silence plan says so) and normalise: `pipeline/voice/normalize.sh vo <trimmed> $D/narration_norm.wav`.
   PASS: integrated -14.0 +-0.5 LUFS, TP <= -2 dBTP, 48 kHz mono. (Shift words.json by the trim offset before captions.)
10. Speech rate: words / (last_off - first_on) from words.json. PASS band 3.0-3.9 w/s (target 3.7); record, do not tune.
11. Write `$D/narration.manifest.json` (schema `schemas/narration.manifest.schema.json`): voice, model, settings, sha256, credits, approval ref, licence tier.
12. Optional (no extra spend): mix with a silent-licensed synthetic bed to exercise `normalize.sh mix`; PASS bed -20 +-0.5 dB in 400-2000 Hz.
Unit tests (`.venv-analysis/bin/python -I -m unittest discover -s pipeline/voice/tests`) must pass before step 1.

## Abort / report
If the audio is truncated, > 8 s, or the voice is unsuitable: stop, log in `knowledge/audio/a20-voiceover-specialist/FAILED.md`, ask before any retake.
Alternative cheaper path (director decision): if `/with-timestamps` becomes available via an API key later, step 5 is free
(`align.py chars`), and Scribe is only a cross-check.
