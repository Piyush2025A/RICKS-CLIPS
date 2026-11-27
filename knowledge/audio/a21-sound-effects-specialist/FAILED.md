<!-- owner: a21-sound-effects-specialist | version: 0.1 | last_updated: 2026-11-28 -->
# A21 FAILED
1. Mono-mix band rules (detect.py v0.1, detect2.py v0.2; sub boom, air/top clicks, tonal): 20-26 events/10 s in every video = speech (plosives, sibilants, low voices). Hand check of 8 "booms": 0 real SFX. Lesson: speech overlaps every SFX band; duration/harmonicity gates remove all noise events (0 sustained unvoiced noise >=300 ms in 30 videos) without isolating SFX.
2. The A12 splinter "burst" in RC30-22 is the /s/ of the word "smash" - never infer SFX from a broadband noise burst in a gap.
3. Side-channel residual detector (detect_side.py v0.3-0.5): the side channel still contains the music bed (note changes look like transients) and voice-consonant leakage (vertical HF columns). Precision about 50 % (v0.3 sample of 12), about 25 % (v0.5 strong tier sample of 12); event rates 3-30 per 10 s are unusable. Flux gate 450 separated 11 labelled cases but did not generalise. Sub-band rise detector (sub.py) fires 5-100 events per video, again music bass notes.
4. Duration estimate from residual within -12 dB of peak was inflated by the pad (many "riser_swell"). 
Lesson: needs a music-bed model (tonal-line subtraction with a looped template, cf. RC30-27 4.5 s loop) before event detection; or accept manual review of a short list.
