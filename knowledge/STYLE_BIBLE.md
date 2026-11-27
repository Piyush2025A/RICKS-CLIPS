# STYLE_BIBLE — consolidated production style (draft v0.2, 2026-11-28)
Derived from the RC30 Phase 3 research (manifest `fc6f147a…278e06`); department detail and evidence in
`knowledge/bibles/*.md` → specialist FINDINGS. **Goal: comparable craft with ORIGINAL, independently publishable
characters, worlds, stories and assets.** Status: draft v0.2 with A28 audit corrections; pending user review. Confidence H/M/L per rule.

## 1. The look in one paragraph
Flat 2D cut-out characters with baked near-black ink (≈ 3.6 % of head width) live inside real perspective 3D worlds that
the camera almost never stops moving through. Lighting is a key + sky-coloured fill (≈ 7:1), shadows carry the sky hue,
cards cast hard shadows only under a hard key, faces stay near-white and readable. Grade: lifted blacks, soft highlights,
no S-curve, orange/yellow vs blue/violet. Scenes join with 6-frame crossfades, punctuated by zoom-throughs and
fly-throughs. One narrator talks continuously at ≈ 200 WPM over an un-ducked tonal bed at −14 LUFS mono, with one-word
captions fixed at ≈ 70 % frame height. Stories: odd situation → failed attempt → hidden mechanism at 50–75 % → ironic
punch word.

## 2. Hard targets (for QC of our renders)
| Area | Target | Conf | Bible |
|---|---|---|---|
| Format | 1080×1920, 30 fps final (360×640, 24 fps dev) | — | project rule |
| Runtime | 45–65 s (reference median ≈ 60 s; range 31–78) | H | STORY |
| Words | ≈ 3.3 words/s → 148 / 198 / 248 words at 45 / 60 / 75 s | M | STORY S10 |
| Voice onset | ≤ 0.3 s; pauses ≤ 0.6 s; no title card | H/M | AUDIO A3, STORY S1 |
| Loudness | −14 LUFS, TP ≤ −2 dBTP, LRA 2–3, mono-compatible | H | AUDIO A1–A2 |
| Bed | under voice by ≈ 14–20 dB in the speech band, not ducked, looped 6–10 s | M | AUDIO A5–A6 |
| Captions | 1 token (≈ 1.16 words) at a time, band y 0.689–0.724, 2 frames before the word | H/M | CAMERA K10, AUDIO A4 |
| Shots | median ≈ 3 s, ≈ 14 per 60 s, flat pacing | M | EDITING T6–T7 |
| Transitions | crossfade 6 f @30 / 5 f @24 default (75 %); hard cuts ≤ 10 %; placed in narration pauses | M | EDITING T1–T3, T8 |
| Camera | moving ≥ 60 % of frames; push +22 % over ≈ 35 f, smoothstep; no shake | M | CAMERA K1–K5 |
| Change rate | visible change every ≤ 3.5 s | L–M | EDITING T12 |
| Character ink | baked, ≈ 3.6 % head width, L* < 10 | M | CHARACTER C8 |
| Expressions | hold-and-snap swaps, bursts of 3–5 then holds; no lip-sync for narration | M | EXPRESSION E3–E5 |
| Lighting | ambient ≈ 0.14 of key; shadow hue = sky; faces L* ≥ 85 | M | LIGHTING L1–L3 |
| Grade | black floor ≈ 0.04–0.10 (no true black), p99 ≈ 0.94, no grain, no CA | M | LIGHTING L8, L10 |
| Story | mechanism visual at 50–75 %; irony ≈ every 12 s; last word = punch | M/L | STORY S5–S8 |

## 3. Implementation map (our tools)
- **Google Flow**: ORIGINAL character sheets (front/¾/side/back, baked ink, flat fills), expression part sheets, props and
  painterly textures, environment art per treatment (CHARACTER, ENVIRONMENT, A01/A05/A08 TECHNIQUES).
- **Three.js (@remotion/three)**: perspective sets, billboard cards with the A09/A10 card shader, presets per mood,
  treatment-B outline pass, DOF/bloom/AO post stack in the A25 order; camera rig with smoothstep moves; VFX library E01–E18.
- **Remotion**: timeline, 6-frame crossfades, zoom-through/iris masks, captions in the fixed band, expression swaps from
  word timestamps, safe-zone overlay in dev.
- **ElevenLabs**: ORIGINAL voice directed to ≈ 200 WPM, short pauses; word timestamps → captions (−2 f) and swaps (−1 f);
  never clone the reference narrator.
- **FFmpeg**: loudnorm (I = −14, TP = −2, LRA ≈ 3), mono-compatible mix, high-pass ≈ 100–115 Hz; rcpipe + `qc_grade.py` +
  `pacing_qc.py` run on our renders for comparison against these targets.
- Module architecture and order: `knowledge/engineering/a25-threejs-remotion-engineer/TECHNIQUES.md` (M1–M15).

## 4. Originality rules
No reference characters, faces, designs, sets, signage, stories, topics already in RC30, scripts, jokes, music or voice.
Use the reference only for measured craft parameters. Proposed own character signature (needs approval): rounded-square
heads, tapered limbs, mitten hands, indigo ink. Story sourcing via A17 rubric + originality gate.

## 5. Known weak spots (do not over-trust)
Proportions (7 videos measured), walk (n = 1), expression timing (n = 9), SFX model (detectors failed), hook typing
(single-axis labels disagree), DOF blur magnitude (no px value), camera magnitudes (proxy 2-D), vignette (confounded),
6 videos without confirmed edit lists. Decisions pending the user: treatment A vs B, where final renders run, own
character signature.
