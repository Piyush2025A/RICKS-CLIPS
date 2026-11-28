# A16 FAILED — approaches that did not work (Phase 3)
- 2026-11-28 Frame-difference "dead time" on raw MAD/residual motion: median MAD of a narrator close-up with nothing happening (RC30-27 f100-195) was 17 (proxy units) because the camera drifts continuously; a plain threshold marks nearly every frame as change. Replaced by spike-above-local-median detection + A13 moves + cuts (F-a16-008). Proxy detector remains threshold-dependent.
- Speech-rate vs cut-density cross-correlation: tokens/s is 2.6-3.2 across videos (A20) and per-second variation is word-level noise; nothing to correlate. Not run.
- Using caption changes as the "nearest speech event" for the shuffled control: caption events every ~9 f make the control uninformative (observed 2.5 f vs null 2.8 f). Speech gaps are the informative target (F-a16-003/004).
- Using A19 act boundaries per video: A19 reports only typical ranges (no per-video table). Used normalised-time proxies 25/65 % instead.
- Trusting A15 boundaries for pacing in long-take 3D videos (03, 22): undercount hard cuts (F-a16-002).
- Expression-swap and VFX contributions to change rate: no per-frame tables from A02/A12 (only hand tallies of 4 shots), so not combined quantitatively.

## Phase 3B
- 1 fps overview counting for cut rate (F-a16-002): counted whips/pans and acting as cuts, gave >= 7/10 s for RC30-22; every-5th-frame check gives ~5.4 beats/10 s. Do not count scene changes from 1 fps tiles.
- First-3 s eye reads of RC30-06, 12, 19 labelled camera pans/wipes as cuts; A15 FP rows corrected this. Always separate "edit" from "camera-driven beat".
- Own beat detector (window feature distance) is threshold-bound: 0.35 -> 6.1, 1.4 -> 3.0 beats/10 s; only RC30-22 hand-calibrated; tier C is a proxy, not a measurement of true beats.
