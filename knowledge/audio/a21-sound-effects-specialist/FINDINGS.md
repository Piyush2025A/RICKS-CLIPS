<!-- owner: a21-sound-effects-specialist | status: partial | version: 0.1 | last_updated: 2026-11-28 -->
# A21 FINDINGS (PARTIAL: detection failed twice; bed level measured in 3B)
Manifest SHA-256 fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06. Visual ledger: 8 records (spectrogram renders, not video frames; no contact sheets opened). Audio decoded from all 30 native streams (44.1 kHz stereo, in memory, no WAV left). Scripts: pipeline/sfx/ (a21-sfx-0.1..0.5).
NO per-video SFX density, level or sync number is reported: the detectors did not reach acceptable precision (see FAILED.md). Everything below is what was actually verified.

## F-a21-001 Narration dominates; the mix is spectrally uniform (MEASURED, medium-high, n=16 videos tabulated)
Full-band median 40-41 dB (arbitrary STFT scale) in all 16 tabulated videos; side(L-R)/2 is 20-32 dB below mid (data/audio_chain_stats.csv). Mix is near-mono, voice-centred. Limitation: videos 17-30 not tabulated (side probe ran on all 30; values not summarised).
Implementation: keep SFX stereo-narrow or low-level; do not rely on width for separation.

## F-a21-002 A stereo music/tonal bed exists in the side channel (OBSERVED, medium; spectrograms of 22, 27, 09, 04, 05, 07, 10, 14, 21, 23, 30)
Side-channel mel images show sustained narrow tonal lines (about 250-700 Hz fundamentals with partials to 4 kHz) that change notes every 0.3-1 s; in RC30-27 the pattern loops about every 4.5 s across 31 s. Narration is absent there. This is a quiet music/pad bed under the voice. Confidence medium: viewed in ~11 videos, not all 30; the bed is not proven to be "music" vs synth pad.
Implementation: bed = looped tonal pad/loop 20-30 dB under VO, wide stereo (side ~ -30 dB re mid).

## F-a21-003 Clear non-speech SFX events do exist but are sparse (OBSERVED, low-medium; n = 4 videos with clear cases)
Seen in side-channel spectrograms: RC30-09 two broadband impact hits with strong sub tail at about 27.2 s and 27.9 s (frames ~f815 and ~f835; A12 expanding rings at f820, f829, f838); RC30-20 four periodic thumps (sub decay + HF click) at about 9.35, 9.9, 10.45, 11.15 s; RC30-21 wideband noise bursts about 27.1-27.2 s and 27.7 s; RC30-10 broadband swell/hit starting about 64.4 s (final seconds, ~1 s decaying). Brief HF ticks at RC30-07 52.33 s, RC30-22 42.06 s, RC30-30 16.2-16.4 s are plausible but could be voice leakage.
Implementation: impacts = 30-100 Hz thump with 150-300 ms decay plus short HF click; swells = 0.5-1 s broadband noise.

## F-a21-004 A12 open requests (OBSERVED, low)
- RC30-22 splinter burst (f000203, t=6.8 s): the 6.50-6.68 s broadband noise burst is the /s/ of "smash" (mono-mix harmonicity 0.1, hi-band only; no side-channel event in 0-12 s image). NO SFX evidence at f203. Not sync-able.
- RC30-27 shine (f000643, t=21.47 s): no SFX visible in mono mel (19.5-23.5 s) and none in the side channel at 21.5 s. No SFX evidence.
- RC30-09 vein start (f000799, t=26.67 s): no event at 26.67 s; the bed becomes denser/broadband from 25.35 s (mono: low band and sub +25 dB, sustained) and impacts occur at 27.2/27.9 s, i.e. about +0.5 s (+16 f) and +1.2 s (+37 f) after vein start. Sync offset therefore lag, but matched to the A12 rings (f820-838) rather than to the start.

## F-a21-005 Transitions: no whoosh evidence (INFERRED, low)
RC30-27 crossfade f248-253 (8.27-8.43 s) shows nothing but speech in mono and no side event in the 31 s side image (viewed only at coarse scale). Crossfades were not systematically tested (event-triggered average vs control not run). Open question.

## Contradictions / open questions
- Mono-mix rules (F-0.1/0.2) flagged ~160 "booms"; hand check 0/8 non-speech. Side-channel threshold sample: precision about 6/12 (v0.3), about 3/12 (v0.5 strong tier). Counts from those runs are NOT findings.
- Open: SFX density per 10 s, rel. level vs voice, sync on >= 6 videos, ambience per location, centre-panned SFX (invisible in side channel). Next step: event-triggered averages of side-channel flux around shot_candidates cuts and A12 events with shuffled controls.

## Phase 3B additions (2026-11-28)
Header update: visual ledger now 10 records (8 old + 2 new spectrogram renders, `image_kind: render`; videos with visual evidence: 11 incl. RC30-03 and RC30-10 already seen). Computational evidence (not visual): 30/30 videos decoded natively, side/mid band features, pause levels, grid evaluation. Scripts a21-sfx-0.6/0.7 in `pipeline/sfx/p3b_*.py`; data in `data/*_3B.*`. Environment had only numpy (no librosa/scipy); all code is numpy-only. Note: a pause-in-captions definition is unusable: `caption_segments.csv` has gaps >= 150 ms in only 2 of 30 videos (3 gaps in total; captions are back-to-back), so pauses were defined acoustically (mid 300-3400 Hz, Otsu, closed 100 ms, runs >= 150 ms, 50 ms margins trimmed); 77 % (IQR 73-82) of pause starts fall within 100 ms of a caption boundary, which is consistent with, not proof of, true word gaps.

## F-a21-100 Bed level in voice-free pauses, mid and side (MEASURED, medium-high, n = 30 videos, 54 pauses/video median (24-81), 6.6 s of pause/video)
Mean-power level of voiced frames minus mean-power level of pauses (`data/bed_pause_levels_3B.csv`, `bed_cross_channel_3B.csv`):
- mid 400-2000 Hz: speech - pause = 15.6 dB (IQR 14.9-16.5; 11.3-19.0). Same with only the 300 ms of speech adjacent to each pause: 15.5 dB. Full band: 6.0 dB (5.3-6.7); 60-150 Hz 2.5 dB; 2-8 kHz -2.5 dB (pause louder than speech in the top band).
- side: speech(mid-channel)-referenced levels are channel-crossed: mid speech 400-2000 minus side pause = 27.1 dB (25.7-28.5; 19.4-32.6); mid pause minus side pause = 11.5 dB (10.2-12.6).
- side speech-active minus side pause (same channel): +0.4 dB (-0.1..+1.2) in 400-2000 Hz, +0.1 dB full band = the side bed does not move with the voice (confirms A22 F-A22-005/001).
- The mean pause level is not a floor: the 10th percentile of pause frames is 9.1 dB (8.1-10.3) below the mean (mid 400-2000). Speech minus mid pause P10 = 24.6 dB (23.4-25.8; 19.5-29.2); speech minus side pause P10 = 35.9 dB.
**Reconciliation (A28 s3 row):** A21's "20-30 dB under VO" and A22's "<= -14 (mid) / -27 (side)" are both reproduced and measure different things: -15.6 dB is the mean pause level (bed + voice tails + room; upper bound), -24.6 dB is the quiet floor of pauses (lower bound on how loud the true bed can be if it is mono; the bed cannot be quieter than the floor frames are, so the mid bed lies between -15.6 and -24.6 dB re speech 400-2000 Hz). Side-only bed -27 dB. Best single value for the mid-channel bed: about -20 dB re speech (INFERRED, medium). Limits: the pause floor still contains room noise, voice tails and codec noise; head-minus-tail of pauses is +1.0 dB (-0.1..+1.9) i.e. tails are present in part of the pause.

## F-a21-101 The side channel carries information only below about 3.9 kHz (MEASURED, high, n = 30)
Side band medians above the 36th log band (about 3.9 kHz) sit at -90..-130 dB (codec floor) while mid stays at about -20 dB: AAC discards stereo HF. Any SFX/whoosh with HF-only stereo energy cannot be seen in side; a side-channel whoosh detector can only use <= 3.9 kHz. This corrects my first 3B run, which clamped the floor at -20 dB across all 48 bands and produced misleading precision (0.56 at n=25): see FAILED 5.

## F-a21-102 Bed-subtracted SFX detection: NO method passes (MEASURED, high that it fails, n = 30 videos)
Labels: picture-sync to A12/A15 events (window +-4 f). Picture events are dense (about 0.4/s) so chance coincidence is about 20 % (shuffled controls). Results:
- M1 side broadband rise over rolling-median bed (grid in `data/m1_grid_3B.txt`, 12 settings, 99-3008 candidates in 17-30 videos): precision 0.20-0.36 against chance 0.18-0.20 (lift 1.0-2.0); best setting (rise > 24 dB in >= 70 % of bands) n = 99, 17 videos, precision 0.36, but recall of synthetic +18 dB bursts only 9 %. Looser settings recall 0.6-0.9 of +12 dB synthetic bursts yet 19-106 events/min and lift ~1.0 (music note changes).
- M2 (mid, inside pauses, rise >= 12 dB over pause P10): n = 511 in 30 videos, precision 0.21 vs 0.20 (lift 1.00); >= 20 dB: n = 55, 0.15 (lift 0.73).
- M3 (mid sub+air joint rise with voice band flat): n = 1532, precision 0.19 vs 0.20 (lift 0.93); strongest tier (>= 18 dB) n = 233, 0.20 (lift 1.03).
Criterion (precision >= 0.7, n >= 60, >= 8 videos) is met by none. Therefore SFX density per minute, level vs VO and offset in frames are NOT reported as video-wide values. Caveat: labels by picture sync are a lower bound on precision (an SFX not tied to a picture event is counted wrong), but chance-level lift of M2/M3 and 1.0-2.0 for M1 show there is no hidden signal either.

## F-a21-103 No whoosh on transitions in the side channel; a swell at the ending exists in some videos (MEASURED, medium, n = 569 A15 transitions + 123 A12 events, 30 videos)
Picture-triggered test (`data/picture_triggered_side_3B.txt`): fraction of events with a strict side broadband rise (> 18 dB in >= 50 % of bands < 3.9 kHz) within 3 f before to 10 f after the event: all A15 transitions 0.24 vs shuffled 0.20 (p 0.010); excluding VB (video-end fade) the kinds are at chance: XF (n=308) 0.22 vs 0.19 (p 0.075), FP (n=178) 0.28 vs 0.22 (p 0.035), ZT (27) 0.26 vs 0.23, HC (37) 0.19 vs 0.16; A12 bumps (80) 0.23 vs 0.19, flashes (43) 0.14 vs 0.15. At the stricter >= 70 % setting: A15 0.07 vs 0.05 (p 0.000, driven by VB: 4/11 = 0.36 vs 0.03), XF 0.06 vs 0.05, bumps 0.04 vs 0.05. Detector sensitivity for such events is partial (synthetic +18 dB burst recall 29-63 % at these settings), so a whoosh rate up to about 10-20 % of transitions cannot be excluded; a whoosh on every transition (e.g. 569 events) would be detected. Transitions with side-channel whooshes are not the norm: HYPOTHESIS that transition sound is absent or centre-panned/mid-only (the mid test in pauses found nothing either, F-a21-102 M2).
End swell: side 60-1000 Hz maximum over the last 4 s minus body median is median 5.2 dB (IQR 4.0-8.4); exceeds the random-window control p95 in 5/30 videos (RC30-01 5.9, RC30-03 27.3, RC30-06 20.4, RC30-08 22.9, RC30-10 25.5 dB; peak times 60.4, 57.5, 64.5, 62.0, 64.3 s) and >= 10 dB in 6/30 (`data/end_swell_3B.csv`). OBSERVED: spectrograms of RC30-10 (60-66 s) and RC30-03 (54-60 s) show a broadband low-weighted swell with decay starting about 64.9 s and 58.1 s, about 2 s long, side much stronger than the preceding bed (OBSERVED, 2 videos, confirms F-a21-003 for RC30-10). Implementation: a 1.5-2 s low-weighted broadband swell/hit near the end in about 1 of 5 videos; not a rule for all.

## Phase 3B revisions
- F-a21-001 unchanged. F-a21-002 and F-a21-003 confirmed (end swell now quantified, F-a21-103), but their implementation lines on "bed 20-30 dB under VO" are refined by F-a21-100: bed (mid) about -15.6 to -24.6 dB re speech, side -27 dB.
- F-a21-005 (transitions: no whoosh evidence, INFERRED low) is UPGRADED to MEASURED medium by F-a21-103 (n = 569 transitions), with the sensitivity caveat.
- TECHNIQUES 'Level: ... peak -6 to -10 LU vs narration (HYPOTHESIS)' is NOT supported or refuted; no SFX level measured (detection failed).
- Contradiction with A22 resolved: not a contradiction (F-a21-100). No contradiction left open for the director.
