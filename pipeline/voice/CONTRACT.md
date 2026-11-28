# Voice pipeline contract (A20) - v1.0, Phase 4
Tools in this directory turn a generated narration into: a manifest, a canonical word timeline, caption schedules at
30 and 24 fps, a silence/trim report and loudness-normalised stems. Run everything with `.venv-analysis/bin/python -I`.
No tool spends credits or calls a network; the paid steps (TTS, Scribe) happen outside, with recorded approval.

## Data flow
```
script.txt --(director: connector TTS, approved)--> narration_raw.mp3 --intake.py--> private store (sha256 sidecar)
narration_raw --silence.py--> silence.json (trim plan)         narration_raw --(Scribe, approved)--> scribe.json
scribe.json + script.txt --align.py scribe--> words.json  (or API alignment --align.py chars--> words.json)
words.json --captions.py--> captions_30.json, captions_24.json (+ .srt)
trimmed audio --normalize.sh vo--> narration_norm.wav (48 kHz mono, -14 LUFS)  [+ bed --normalize.sh mix--> master]
everything --> narration.manifest.json
```
Outputs live in `productions/<id>/voice/`. Raw media stays in `~/ricks-clips-private/` (never committed).

## Files and schemas (`schemas/`, JSON Schema 2020-12 subset; checked by `tests/schemacheck.py`)
| File | Schema | Notes |
|---|---|---|
| `narration.manifest.json` | narration.manifest.schema.json | voice id/name/origin (never "cloned"), model, settings, exact submitted text, audio sha256 / rate / channels / duration / loudness, credits (estimated, actual, scribe), take, approval ref, licence tier + commercial_use |
| `words.json` | words.schema.json | `words[]`: index, word (with attached punctuation), t_on, t_off (s), char_start/char_end (offsets into the submitted text, tags included; -1 when unknown), source (`api_alignment` / `scribe` / `forced`), confidence, optional flags |
| `captions_<fps>.json` | captions.schema.json | per fps: token, word_indices, show_at, hide_at (s), frame_in (inclusive), frame_out (exclusive), sentence_final |

## Units and frame conversion
Seconds are the master unit. Frames are derived by time: `frame = floor(t * fps + 0.5)` for any fps (30 final, 24 dev). Durations
specified in frames at 30 fps convert by time (5 f hold = 0.1667 s = 4 f @24; 0.14 s lead = 4 f @30, 3 f @24). The rate is
always stored with the captions. Trim shifts all word times by `-trim_start_s`.

## Alignment rules (`align.py`)
* Char alignment -> words: whitespace tokenisation; punctuation stays attached; punctuation-only tokens merge into the previous
  word; `-`, `'`, `.`/`,` inside numbers stay inside a word; em/en dash ends a word (`rate-` / `really`); SSML `<...>` and v3
  `[audio tags]` are masked (offsets preserved) and never become words; empty/multi-char entries, zero-length characters and
  missing timestamps (filled from neighbours) are handled; word onset = earliest char start, offset = latest char end.
* Scribe: only `type: word` items are used (`spacing`, `audio_event` dropped). With a script, normalised tokens (lowercase,
  edge punctuation removed) are matched with `difflib.SequenceMatcher`; script wording and char spans win. Mismatch kinds in
  `alignment_report.mismatches`: `substituted` (timed from the transcript word, confidence <= 0.5), `missing` (script word absent
  from audio: interpolated, confidence 0), `extra` (transcript word absent from script: reported, not emitted).
  Scribe confidence = exp(logprob) when given, else 0.8.
* Validation: onsets monotonic, no overlap (>1 ms), t_off >= t_on, all inside [0, duration]. `repair_words` clamps and flags `repaired`.
  A words.json with non-empty `validation_issues` must not be handed to A25/A22 unreviewed.

## Caption rules (`captions.py`; PRODUCTION_DEFAULTS, F-A20-102..104)
One token on screen; default token = 1 word (production default). `--merge-function-words` (off) joins up to 3 words when
leading ones are short function words - an optional experiment matching the reference 1-3 word median, not a default.
show = onset - 0.140 s (>= 0); hide = next show (never blank); a sentence-final token (`. ! ? ...`) stays >= 5 f @30 after its
word end unless the next onset is earlier; last token hides at t_off + hold clamped to duration; >= 0.10 s between successive
show times (warning when that pushes a caption past its onset); frame_out > frame_in always; everything clamped to the clip.

## Silence and loudness
`silence.py`: -45 dBFS, 10 ms frames; trim plan keeps <= 0.20 s head / <= 0.30 s tail; pauses >= 0.25 s listed, > 0.6 s warned.
`normalize.py vo`: high-pass 100 Hz, two-pass `loudnorm` I=-14 TP=-2 LRA=3 (linear), 48 kHz **mono** 24-bit WAV (narration stem;
reference side channel ~27 dB below mid). `mix`: bed gain set so bed band power (400-2000 Hz, VO-voiced frames) is -20 dB re VO,
static, from t=0, looped/trimmed to the VO length, no sidechain; then two-pass loudnorm to -14 LUFS / TP -2; deliverable is
48 kHz stereo (mono duplicated). Outputs are new files; existing outputs are never overwritten. A22 owns the real mix; this is the reference recipe.
Limit: with LRA/TP not reachable in linear mode ffmpeg falls back to dynamic normalisation - always read the `result` measurement.

## Tests
`.venv-analysis/bin/python -I -m unittest discover -s pipeline/voice/tests` (30 tests; synthetic audio generated at test time;
fixtures regenerate with `tests/make_fixtures.py`). Not covered: real TTS output, real Scribe responses (formats follow the
director's description of the connector, unverified until the 6 s test).

## D036 update (2026-11-28) — narration-only default
- Default production path: narration audio + `silence.json` + `beats.json` (sentence/clause timings from the script and
  measured pauses; `beats.py`). No Scribe transcription, no word timestamps, no rendered captions by default (the user
  adds subtitles post-render with Canva Auto Captions). `align.py` and `captions.py` stay for optional future use.
- `normalize.py vo` falls back to gain + 4× oversampled limiter (ceiling TP − 0.8 dB) when linear loudnorm is TP-limited;
  verified on TEST6S: −14.2 LUFS / −2.8 dBTP (WAV), −14.3 / −2.2 after AAC.
