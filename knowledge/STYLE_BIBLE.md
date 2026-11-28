# STYLE_BIBLE — consolidated production style (draft v0.3, 2026-11-28, Phase 3B)
Derived from the RC30 Phase 3 + 3B research (manifest `fc6f147a…278e06`); department detail and evidence in
`knowledge/bibles/*.md` → specialist FINDINGS. **Goal: comparable craft with ORIGINAL, independently publishable
characters, worlds, stories and assets.** Status: draft v0.3 with both independent audits applied (AUDIT.md, AUDIT_3B.md);
pending user review. Confidence H/M/L per rule.

## 1. The look in one paragraph
Flat 2D cut-out characters with soft gradient shading and a baked very dark ink line (≈ 3.7 % of head width, scaling with
the card) live inside real perspective 3D worlds that the camera almost never stops moving through. Most videos (20/30)
have no ink on scenery; a minority (6/30) ink the scenery too. Lighting is a key + sky-coloured fill (≈ 7:1); characters
receive scene light; card cast shadows are a per-scene switch that is usually off. One grade everywhere: lifted blacks
(p1 ≈ 0.07), soft roll-off, mild constant vignette, orange/yellow vs blue/violet. Scenes join with ≈ 7-frame crossfades
(79 %), with zoom-throughs and fly-throughs at concept moments; the camera also changes the scene without an edit. One
narrator talks continuously at ≈ 220 words/min over a static tonal bed ≈ 20 dB down (speech band), −14 LUFS mono, with
one-word captions fixed at 0.70 frame height running ≈ 4 frames ahead of the voice. Stories: odd situation → failed
attempt → hidden mechanism at 50–75 % → ironic punch word; the opening's verbal twist lands at 3–5 s.

## 2. Hard targets (for QC of our renders)
| Area | Target | Conf | Bible |
|---|---|---|---|
| Format | 1080×1920, 30 fps final (360×640, 24 fps dev) | — | project rule |
| Runtime | 45–65 s (reference median ≈ 60 s; range 31–78) | H | STORY |
| Words | ≈ 220 wpm (3.7 words/s) → ≈ 165 / 220 / 275 words at 45 / 60 / 75 s; sentences ≈ 11 words | H/M | STORY S10 |
| Voice onset | first word ≤ 0.2 s (frame 1 in 23/30); sentence pauses ≈ 0.15–0.3 s; no title card | H/M | AUDIO A3, STORY S1 |
| Loudness | −14 LUFS, TP ≤ −2 dBTP, LRA 2–3, mono-compatible | H | AUDIO A1–A2 |
| Bed | −20 dB (±3) re VO in 400–2000 Hz, static (no duck), looped 6–10 s, one track per video | M | AUDIO A5–A6 |
| Captions | Production (D036): rendered captions off by default — added post-render in Canva Auto Captions; keep the 0.67–0.74 H band clear of key action. Reference (if enabled): 1 token, centre 0.703 H, never blank, ≈ 140 ms before the word | H/M | CAMERA K10, AUDIO A3–A4 |
| Edit shots | median ≈ 3.2 s, ≈ 2.2 edits per 10 s, ≈ 14 per video, flat pacing | M–H | EDITING T6, T8 |
| Visual beats | a visible change every ≈ 2.9 s (incl. camera-driven scene changes); ≤ 3.5 s without change | M / L–M | EDITING T7, T12 |
| Transitions | crossfade default 7 f @30 (6–8; 5–6 @24), 79 %; hard cuts ≤ 10 %; in narration pauses | M | EDITING T1–T3, T9 |
| Opening | caption from frame 0–1; a visible change within 1–3 s; an edit in 0–3 s is optional (12/30) | M | EDITING T11, STORY S3 |
| Camera | moving ≈ 67 % of frames, hold ≈ 11 %; push +24 % over ≈ 33 f, smoothstep (60 %); no shake | M | CAMERA K1–K5 |
| Character | head H/W 0.93; height ≈ 3.3 HH; leg/torso ≈ 1.4; ball hands; ink 3.7 % HW (9.3 px for a 250 px head) | M | CHARACTER C2–C4, C9 |
| Expressions | hard swaps, no in-betweens; ≈ 5 f holds around changes, 11–30 f between bursts; no lip-sync | M | EXPRESSION E3–E5 |
| Body animation | moving bodies on ones; dialogue bodies frozen 24–48 f; walk step ≈ 11 f (n = 1) | M / L | ANIMATION M2–M4 |
| Lighting | shade/lit ≈ 0.14; shadow hue = sky; card cast shadows OFF by default | L–M / M | LIGHTING L1–L3 |
| Grade | p1 ≈ 0.07 (0.04–0.10), p99 ≈ 0.96, soft roll-off, vignette 0.70, no grain, no CA | H/M | LIGHTING L8, L10, L12 |
| DOF | minority; added blur ≈ 3.6–4 px at 1080 on soft layers | L–M | ENVIRONMENT W8 |
| Story | mechanism visual at 50–75 %; irony ≈ every 12 s; last word = punch | M/L | STORY S5–S8 |

## 3. Implementation map (our tools)
- **Google Flow**: ORIGINAL character sheets (front/¾/side/back, baked ink, soft gradient fills), expression part sheets,
  props and painterly textures, environment art per the chosen scenery-ink treatment (CHARACTER, ENVIRONMENT, A01/A05/A08
  TECHNIQUES).
- **Three.js (@remotion/three)**: perspective sets (near/subject/far 0.5–2 / 3–6 / ≥ 20 m for orbit and dolly shots),
  billboard cards with the A09/A10 card shader (ink scales with the card), material presets (A08 table), treatment-B
  outline pass only when chosen, DOF/bloom/AO post stack in the A25 order; camera rig with smoothstep moves; VFX E01–E25.
- **Remotion**: timeline, 7-frame crossfades, zoom-through/iris masks, captions in the fixed band ≈ 4 f ahead of word
  timestamps, expression swaps driven by story beats, safe-zone overlay in dev.
- **ElevenLabs**: ORIGINAL voice directed to ≈ 220 wpm with short sentence pauses; word timestamps → captions; never clone
  the reference narrator.
- **FFmpeg**: loudnorm (I = −14, TP = −2, LRA ≈ 3), static bed −20 dB re VO in the speech band, mono-compatible mix,
  high-pass ≈ 100–115 Hz; rcpipe + `tools/caption_events.py` + `qc_grade.py` + `pacing_qc.py` on our renders to compare
  against these targets.
- Module architecture and order: `knowledge/engineering/a25-threejs-remotion-engineer/TECHNIQUES.md` (M1–M15).

## 4. Originality rules
No reference characters, faces, designs, sets, signage, stories, topics already in RC30, scripts, jokes, music or voice.
Reference caption transcripts are private research material, never committed or reused. Use the reference only for
measured craft parameters. Genre-level constants may be shared; the reference's exact character combination must not be
reproduced (CHARACTER, originality note). Proposed own character signature (needs approval): rounded-square heads,
tapered limbs, mitten hands, indigo ink. Story sourcing via A17 rubric + originality gate.

## 5. Known weak spots (do not over-trust)
Walk cycle (numeric n = 1; bob/lean/slip unmeasured); SFX density/level/sync (no detector reached usable precision);
light-rendering treatment split (A09, low, inconsistent; scenery-ink split by A10 is the usable axis, 1–2 frames per
video); DOF share (metric upper bound vs visual over-call, contradiction kept); per-move camera magnitudes (noisy;
medians robust); key azimuth, fill ratio on ≥ 15 videos; blink rate; child/animal/object proportions; picture-axis hook
coding (κ 0.57; two LLM coders); 3A overview-based expression vocabulary not re-checked. Decisions pending the user:
scenery-ink treatment (A majority / B), where final renders run, own character signature.
