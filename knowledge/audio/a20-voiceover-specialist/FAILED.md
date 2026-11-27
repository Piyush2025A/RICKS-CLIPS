# A20 FAILED approaches and lessons (Phase 3)

## X1 pyin voiced probability threshold (2026-11-28)
`voiced_prob > 0.8` kept only 1.3 % of active frames on RC30-27 (median voiced_prob ~0.02 even with 65 % voiced flags). Lesson: with a music bed, use the
voiced flag plus active-speech gating; treat F0 as indicative only. 35-53 % of pause frames are also flagged voiced (bed pitch).

## X2 Caption-change detector, strict version
First rule required isolated sharp spikes (neighbour median < 25 % of threshold): it missed ~half of the tokens (RC30-02: 3 of 6). Relaxed to threshold
200 + local maximum + 3-frame refractory; recall ~94 %, ~10 % spurious (bright scene changes). Lesson: validate on contact sheets before counting.

## X3 Ducking test via low band
Low band 35-110 Hz has almost no bed energy (-44 dB vs -21 dB speech band), so active-vs-pause difference (median -0.5 dB) cannot show ducking. Inconclusive; needs
a bed-only reference or A22 stem analysis.

## X4 Visual-ledger error (corrected)
Two vlog records (RC30-14 f624-671, RC30-18 f720-767) were written before checking that sheets exist for those videos (they do not: sheets exist only for
02, 15, 23-30); the files were never opened and the two records were removed from the ledger. Lesson: log only after Read succeeds.

## X5 Not completed (turn limit)
Second pitch pass (fl 2048, loudest-half gating), hand-checked word timing error, per-video words/token for the 22 videos without sheets, bimodality test for
character voices, spectrogram images (none rendered, none logged).
