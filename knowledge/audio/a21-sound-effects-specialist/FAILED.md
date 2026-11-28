<!-- owner: a21-sound-effects-specialist | version: 0.1 | last_updated: 2026-11-28 -->
# A21 FAILED
1. Mono-mix band rules (detect.py v0.1, detect2.py v0.2; sub boom, air/top clicks, tonal): 20-26 events/10 s in every video = speech (plosives, sibilants, low voices). Hand check of 8 "booms": 0 real SFX. Lesson: speech overlaps every SFX band; duration/harmonicity gates remove all noise events (0 sustained unvoiced noise >=300 ms in 30 videos) without isolating SFX.
2. The A12 splinter "burst" in RC30-22 is the /s/ of the word "smash" - never infer SFX from a broadband noise burst in a gap.
3. Side-channel residual detector (detect_side.py v0.3-0.5): the side channel still contains the music bed (note changes look like transients) and voice-consonant leakage (vertical HF columns). Precision about 50 % (v0.3 sample of 12), about 25 % (v0.5 strong tier sample of 12); event rates 3-30 per 10 s are unusable. Flux gate 450 separated 11 labelled cases but did not generalise. Sub-band rise detector (sub.py) fires 5-100 events per video, again music bass notes.
4. Duration estimate from residual within -12 dB of peak was inflated by the pad (many "riser_swell"). 
Lesson: needs a music-bed model (tonal-line subtraction with a looped template, cf. RC30-27 4.5 s loop) before event detection; or accept manual review of a short list.

## Phase 3B (2026-11-28)
5. First M1 run (side channel, 48 bands, floor clamp -20 dB) gave precision 0.56 at n=25 (12 videos) with lift 2.9. This was an artefact: bands above 3.9 kHz are codec floor in side and were clamped, so only the low bands could vary, and the surviving 25 events were mostly end-of-video swells (RC30-03/06/08/10), a real but tiny population. With the proper 36 active bands the same detector gives 3000+ events and lift 1.0. Lesson: check the codec floor of a channel before gating on a fraction of bands; clamp is not neutral.
6. Bed subtraction by rolling-median (past 1.0..0.2 s) does not remove the music: the bed changes notes every 0.3-1 s so most band rises of 6-18 dB are note changes. Grid of 12 settings: best lift 2.0 (precision 0.36) with only 9 % recall of +18 dB synthetic bursts. A looped-template subtraction (period 6-10 s, A22 F-A22-004) was not tried; it is the next candidate.
7. Using `caption_segments.csv` gaps as pauses fails: gaps >= 150 ms occur in 3 places in 30 videos. Pauses must be acoustic.
8. Mid-channel pause onset (M2) and sub+air joint rise (M3) are chance-level (lift 1.0/0.93): pause ends and plosives dominate.
