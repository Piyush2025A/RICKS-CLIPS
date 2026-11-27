<!-- owner: a22-music-mixing-specialist | status: draft | version: 0.1 | last_updated: 2026-11-28 -->
# A22 FAILED — approaches that did not work
- **Tempo from beat tracking (side channel):** librosa beat_track with start_bpm 100 returns 77–120 BPM (median 103)
  = the prior; onset-autocorrelation confidence 0.05–0.19 and BPM scatter 44–200 → tempo not established. Pause segments
  (A20 gaps ≥ 150 ms, median 0.21 s) are far too short for tempo. Do not report a tempo as measured.
- **Absolute presence threshold:** first threshold (side > −80 dBFS) was meaningless because STFT power was not
  scaled to dBFS (all frames passed); fixed by offset −58.96 dB; "presence" then trivially 100 %, so dropout fraction
  (1-s windows 6 dB under the video median) was used instead. First run of RC30-27 used the unpatched thresholds
  and was rerun.
- **Mid low-band ducking test (35–150 Hz) was confounded by voice** (F0 ≈ 205 Hz, harmonics/voice onset leakage; onset +1.1,
  offset +2.9 dB artefact at t = 0). Replaced by 30–90 Hz and side-channel bands (F-A22-005).
- **Mixing bed level from mid gaps** over-estimates bed (gaps contain voice tails/room): only an upper bound.
- **Shot alignment:** 6 videos (06, 09, 10, 11, 13, 21) had no shot_candidates.json (rcpipe batch incomplete) → n = 24.
- **Source separation / mono-bed estimation:** not attempted (no separator allowed/installed).
- Process note: parallel background launches wrote duplicate runs on the same outputs (first launch with wrong filename
  `01.mp4` vs `1.mp4`); results are idempotent but wasted CPU.
