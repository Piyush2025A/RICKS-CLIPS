# Production defaults (Phase 4 onward) — v2, 2026-11-28 (D033, D036)
The current production reference is **`knowledge/STYLE_BIBLE.md` v0.3** with the nine department bibles in
`knowledge/bibles/` (v0.3), each with its stated confidence and limitations. Measured reference statistics are
**initial production targets** for comparable craft — starting points to test against our own renders, not universally
mandatory rules. Where an older specialist TECHNIQUES file, engineering document or plan disagrees with this list,
this list and the v0.3 bibles win; historical research records and superseded findings stay in place for traceability.

| Topic | Production default | Evidence (bible / finding) |
|---|---|---|
| Captions | **Rendered captions are OPTIONAL and DISABLED by default (D036):** subtitles are added by the user after rendering with **Canva Auto Captions**. Keep the caption band (y ≈ 0.67–0.74 H) and the bottom 20 % free of key action so Canva captions stay readable. If burned-in captions are ever enabled (`pipeline/voice/captions.py`, kept for future use), the reference targets apply: caption ≈ 140 ms before the word onset (≈ 4 f @30, ≈ 3 f @24), one token at a time, centre 0.703 H, never blank (the old ~70 ms is superseded) | D036; AUDIO A4, F-A20-104 |
| Animation sync | **Sentence and story-beat timings** from the script + measured pauses (`pipeline/voice/beats.py` on `silence.py` output) — no transcription, no word timestamps by default. Word-level timing (ElevenLabs Scribe / API alignment) is optional and needs approval (credits) | D036 |
| Crossfade | default **7 frames at 30 fps ≈ 0.233 s** (typical 6–8 f); other rates convert **by time**: frames = round(0.2333 × fps) → **6 f at 24 fps**; 79 % of joins | EDITING T1–T2, F-a15-101, AUDIT_3B #3 |
| Facial expressions | swaps placed on **story beats / sentence timings** (hard swaps, ≈ 5 f holds, 11–30 f between bursts); **not** word-triggered; no lip-sync for narration | EXPRESSION E3–E5, F-A02-101..103 |
| Character shading | **smooth soft gradients** on cards, hard highlight streaks allowed; **no mandatory toon bands** (toon ramps only as an optional experiment) | CHARACTER C10, F-a01-102, A10 |
| Character cast shadows | **off by default**; enable per scene when the shot calls for it (hard card shadows in 4/30 reference videos) | LIGHTING L3, F-A09-101 |
| Background music | **static bed** as the initial default; **−20 dB (±3) relative to narration in the 400–2000 Hz speech band**; no sidechain ducking by default (≤ 1 dB if ever needed) | AUDIO A5–A6, F-a21-100, F-A22-100..102 |
| Character ink | **baked into the character artwork** (≈ 3.7 % of head width, very dark aubergine/brown-black), **scaling with character size**; no constant-width screen-space outline on cards | CHARACTER C9, F-a10-101..104 |
| Narration pace | ≈ 220 wpm initial target (sentences ≈ 11 words); first TTS test read at ≈ 197 wpm with default settings — raise `speed` (multilingual_v2) or tighten pauses when needed | STORY S10, F-A20-101, D036 |
| Narration loudness | VO stem −14 LUFS (±0.5), TP ≤ −2 dBTP **after** AAC encode: `pipeline/voice/normalize.py vo` (linear loudnorm, falls back to gain + 4× oversampled limiter at TP − 0.8 dB) | D036 TEST6S |
| Licences | ElevenLabs free tier = private development only (non-commercial, attribution); a paid plan is required before any publication. Flow outputs: commercial terms unresolved (A23 TERMS_REVIEW) | D034, D036 |
| Cut-outs | Background removal approved for OUR original generated character assets: originals stay unchanged (work on intaken copies), watermarks and content credentials respected and recorded in provenance; method/tool still to be chosen (local install or credits need approval) | D036 |
| Camera push | ≈ +24 % total scale over ≈ 33 f (30 fps), smoothstep easing | CAMERA K3–K4, F-a13-100..102 |
| Grade | black p1 ≈ 0.07, soft roll-off, vignette ≈ 0.70, no grain/CA | LIGHTING L10, L12 |
| Development renders | 360 × 640, 24 fps (convert every frame count by time) | CLAUDE.md rule 6 |
| Dataset identity | RC30 keys + SHA-256 are the identity for evidence; video IDs, publication dates and URLs are **deferred metadata** (`knowledge/dataset/IDENTITY.json`, D028); order by user attestation | D028 |

Frame-count conversion rule: every duration defined at 30 fps is converted by time (`round(seconds × fps)`), never by
copying the frame number.
