# A02 TECHNIQUES — expression library spec for a Remotion / Three.js face rig (original characters)

Derived from FINDINGS F-A02-001..010. Parameters are from RC30 observation (low-medium confidence where noted).
Frame rate 30 fps native; our dev render is 24 fps -> convert frames x0.8 (hold 4 f @30 = ~3 f @24).

## T-A02-01 Rig = 4 swappable layers + wobble
Layers: EYES (state set below), BROWS, MOUTH, ACCESSORY (sweat, ticks, blush, tint). Each layer is a sprite/SVG/texture
swap on ONE frame; no tween on shape. Head transform wobble (rotate +-1-3 deg, translate 2-4 px at 2-4 frame cadence) runs under all states
(visible in 03 f830-877, 25 f45-64) so held faces never freeze.

## T-A02-02 Eye set (11) - build in this order
E1 dot pair (default) | E2 dot + half-lid bar (smug) | E3 flat bars / double lines (closed/sleep/pain) | E4 closed arcs `^ ^` (happy/laugh)
| E5 ring + pupil (shock; pupil offset +-2 px = look) | E6 `> <` | E7 big round eyes small pupil (terror) | E8 glasses overlay |
E9 visor/sunglasses overlay | E10 glow (colour param) | E11 half-lid mid-blink. Min state count for launch = E1-E6 + E11.
Readable-at-small rule (OBSERVED): use solid ink strokes, >= 2 px per 1080 width at 8 % head scale, avoid thin detail
inside rings.

## T-A02-03 Brow set (6): flat, raised-one, raised-both, angry-inward-down, worried-inner-up, none(merged). Brow layer swaps independently of eyes
(brow change is the cheapest beat: allow 2-3 brow swaps per reaction burst).

## T-A02-04 Mouth set
Core 8: M1 line/tick (neutral & narrator hold), M2 smirk, M3 grin+teeth grid, M4 grit teeth grid, M5 open oval, M6 wide open + tongue,
M7 wavy unease, M8 frown. Extra: M9 closed smile, M10 laugh-open, M11 lopsided toothy. Interior colour: dark with red tongue.
"Acting flap" set (4 shapes: M1, M3-half-open, M6, M3 narrow) cycle for in-scene talking: hold each 1-5 f (random 2-3 median), burst length = line length.
No phoneme visemes needed: VO is narration, mouths are not synced (F-A02-008). If a character is meant to speak in-scene, drive flap on/off from the ElevenLabs
word timestamps for THAT line (flap while within [word_start, word_end]) - HYPOTHESIS, untested.

## T-A02-05 Accessories
sweat drop (1-2, temple, persists during state), pain/anger ticks (3-5 radiating red lines), blush patch, steam puffs (anger), Z marks (sleep),
head tint (green sick, purple fury, blue sleep). Accessory ON on the same frame as the state swap; OFF with the state.

## T-A02-06 Timing rules (frames @30 fps; relative to ElevenLabs word_start t_w)
- Reaction swap frame = round(t_w*30) + k, k in [-3, +2] (median -1) (F-A02-007, n=9, low). Start: k=-2.
- Burst (reaction): 3-5 swaps within 10-20 frames of the beat (eyes+brows+mouth cascade, e.g. sleepy -> ring+wavy (f0) -> smirk (f+10) -> dots (f+13) -> neutral hold).
- Hold after burst: 20-30 frames (strong pain/anger), >= 28 frames neutral; narrator neutral holds >= 96 frames with only blinks.
- Do NOT retrigger a state faster than 1 frame (swaps are legal on consecutive frames); 3-4 shape changes/s sustained is the ceiling.
- Expression changes per scene: target 1 burst per sentence/beat (~every 2-4 s), narrator shots 0.

## T-A02-07 Blink rule
Eyes layer -> E11 half-lid (1 f) -> E3 bars (1-2 f) -> E1 (total 2-4 f). Interval random 2-4 s (jitter), suppress in the 10 frames around a state swap; blink may double as a swap bridge (E1->E3->E5).
Closed-eye states (E3/E4) do not blink.

## T-A02-08 Validation checklist for our library (A28)
Each state: written trigger line, readable at 48 px face crop (our own render, test not done here), timing rule above. Quick regression: render each
state grid at 360p 24 fps, check tile legibility.

## T-A02-09 Reproduction scripts (private data, no media in repo)
`scripts/strip.py video key start n x y w h out cols tile` -> every-frame crop strip with frame numbers (cv2).
`scripts/cap.py video key` -> caption-change detection (white text >= 245 luma in y 1150-1550) -> per-frame (i, white_px, diff).
Caption change = diff > 100; merge within 2 frames. Output summary `data/caption_change_frames.json` (noisy in bright/scenic frames:
RC30-09, 25, 27, 28 show false positives, intervals of 3 frames - use only with visual confirmation, as in F-A02-007).
`scripts/mouth.py` = dark-pixel fraction in a mouth ROI (camera motion pollutes; not usable standalone).
