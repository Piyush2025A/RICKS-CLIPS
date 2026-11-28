<!-- owner: a21-sound-effects-specialist | version: 0.1 | last_updated: 2026-11-28 | status: provisional -->
# A21 TECHNIQUES (provisional; only items with some evidence, all low-medium confidence)
- Analysis: use side channel (L-R)/2 to view music+SFX without narration (F-a21-002/003); render mel images; never trust automatic counts yet.
- Bed: looped stereo tonal pad/loop, wide, side about -30 dB re mid, note changes every 0.3-1 s, loop about 4.5 s (RC30-27). Source: synthesize (original) or licensed with licence recorded per file.
- Impact palette (RC30-09/20): sub thump 30-100 Hz, 150-300 ms decay + 5-10 ms HF click; stereo-wide; repeat rhythm about 0.5 s (RC30-20: 9.35/9.9/10.45/11.15 s).
- Swell/ending hit (RC30-10 about 64.4 s): 0.5-1 s broadband noise swell with decay.
- Placement: bind impacts to the visual feature that is ~0.5 s after the story trigger (RC30-09: rings f820-838), not to caption onset; offsets in frames NOT yet measured, so test 0 vs +/-2 frames in A/B (EXP planned, not run).
- Level: side-level only measured; total level vs voice UNKNOWN. Default until measured: SFX peak -6 to -10 LU vs narration (HYPOTHESIS).
- Licence log per file in productions/<id>/sfx/ (rule, not from data).

## Phase 3B additions (2026-11-28)
- Bed level (approved, MEASURED medium-high, n = 30): mid bed about -20 dB re speech (400-2000 Hz; bounds -15.6 mean-pause / -24.6 pause floor), side (stereo) component about -27 dB re mid speech; static, no ducking (A22 F-A22-005). Check by speech-minus-pause level on your own mix: expect 15-16 dB mean and about 25 dB on the P10 floor.
- Codec limit: rendered mix has no side energy above about 3.9 kHz in the reference; do not take a missing wide HF as an absence of SFX.
- Ending swell (MEASURED, medium, 5-6/30 videos): 1.5-2 s low-weighted broadband swell with decay about 1-2 s before the end; optional, not universal.
- Transitions: reference shows no systematic whoosh in the stereo side channel (F-a21-103). Do not add a whoosh on every transition because of this study; test by listening-equivalent A/B in production.
- SFX placement/offset in frames: still no measured value (detector failed).
