<!-- owner: a21-sound-effects-specialist | status: partial | version: 0.1 | last_updated: 2026-11-28 -->
# A21 FINDINGS (PARTIAL: stopped at turn limit)
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
