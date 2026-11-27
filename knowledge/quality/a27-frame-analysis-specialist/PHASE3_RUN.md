<!-- owner: A27 | Phase 3 wave C1 run record | script analysis/consolidate_c1.py@1.0 (rcpipe v0.2.0 unchanged) -->
# Phase 3 RC30 run record (rcpipe v0.2.0)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`. Private root
`~/ricks-clips-private/analysis-data/rc30/v0.2.0/RC30-nn/` (1.7 GB, never committed). Command (per video):
`nice -n 10 .venv-analysis/bin/python analysis/run_pipeline.py <n>.mp4 --key RC30-nn --dataset RC30 --manifest knowledge/dataset/MANIFEST.json --out .../v0.2.0 --sheets-every 1`.
Consolidation: `python3 analysis/consolidate_c1.py` (copies ledgers, validates, writes checksums and index summary).

## 1. Frame accounting (MEASURED, high)
30 videos, **50,898 decoded = 50,898 container frames**; frames.csv, color, edges, sharpness, motion and shot_features
all have exactly nb_frames rows in every video; sheets = ceil(nb_frames/48) in every video (every frame on a sheet,
1,076 sheets total; per-video counts in `knowledge/dataset/index/RC30_frame_index_summary.csv`).
pts: first pts = 0.033333 s (frame 0) in all 30 videos (pts axis starts at 1/30). audio_env.csv has 10 ms hops.
Checksums of all 9 per-frame tables per video: `knowledge/dataset/index/RC30_tables.sha256` (270 lines).

## 2. Ledger validation (MEASURED)
`schema.validate_coverage` on 30 `RC30-nn.jsonl` and `schema.validate_audio_coverage` on 30 `RC30-nn.audio.jsonl`
(schema v2 / audio v1, repo validator): **60 records, 0 errors**. All carry manifest_sha256 and the input_sha256 of their video.

## 3. Coverage per stage (frames; ok / uncertain / failed / missing)
| stage | mode, resolution | ok | uncertain | failed | missing |
|---|---|---|---|---|---|
| decode | native 1080x1920 | 50,898 | 0 | 0 | 0 |
| color | native 1080x1920 | 50,898 | 0 | 0 | 0 |
| edges | native 1080x1920 | 50,898 | 0 | 0 | 0 |
| sharpness | native 1080x1920 | 50,898 | 0 | 0 | 0 |
| shots | **proxy** 160x284 (INTER_AREA) | 50,898 | 0 | 0 | 0 |
| motion | **proxy** 320x569 (INTER_AREA) | 45,288 | **5,610 (11.0 %)** | 0 | 0 |
Record-level class = worst stage, so 5,610 frames are "uncertain" overall; the first frame of each video (no previous
pair) is counted ok with status `ok:reference_frame_no_previous_pair`.
Mode split: 4 stages x 50,898 native frames; 2 stages proxy. Colour, edge and sharpness numbers are native; every
motion and shot-boundary number is a proxy-resolution measurement (do not quote them as native).

## 4. Audio coverage (MEASURED)
30/30 videos have audio: AAC, 44.1 kHz stereo, analysed at 48 kHz mono + stereo side measure. Duration 1,699.33 s,
analysed 1,698.33 s; each video has exactly **one** missing interval of 0.033 s at the start (~t = 0.023-0.057 s,
"timestamp gap or undecodable packets between decoded audio frames", zero-filled, rows flagged valid=0). All four audio
stages (decode, loudness, onsets, spectral) are therefore `uncertain` in 30/30 records (120 of 120) - a formal
status from that start gap, not a quality finding; no audio errors. Loudness is measured on the original stream.

## 5. Run cost (MEASURED from batch logs / calibration; /usr/bin/time)
Per-video wall time is elapsed time with **two workers sharing the CPU** (and, for some videos, other jobs), so
frames/s is not a clean throughput figure. RC30-27 and RC30-15 from `research/phase3-calibration.md`.
Sum of per-video wall time 29911 s (8.31 worker-hours); **aggregate 50,898 / 29,911 = 1.70 frames/s per worker**
(median per-video 2.0; range 0.86 RC30-14 to 2.73 RC30-27). Slowest runs (RC30-02, 14, 18 at 0.86-0.99 frames/s,
~29 min each) ran ~2x slower than neighbours of the same size; cause not logged (INFERRED: CPU contention).
Peak RSS 334-451 MiB (max RC30-15, 2,334 frames); grows with frame count. batch.log window of the resumed batch:
2026-11-28 01:20-05:19 (+05:30), 28 videos by two workers.

| key | frames | wall s | frames/s | peak RSS MiB | motion uncertain | candidates |
|---|---|---|---|---|---|---|
| RC30-01 | 1836 | 816.7 | 2.25 | 407 | 197 | 21 |
| RC30-02 | 1659 | 1691.3 | 0.98 | 393 | 213 | 22 |
| RC30-03 | 1772 | 811.1 | 2.18 | 402 | 136 | 14 |
| RC30-04 | 1783 | 786.5 | 2.27 | 404 | 138 | 26 |
| RC30-05 | 1832 | 808.9 | 2.26 | 409 | 210 | 34 |
| RC30-06 | 2005 | 843.5 | 2.38 | 423 | 215 | 26 |
| RC30-07 | 1867 | 818.1 | 2.28 | 412 | 151 | 21 |
| RC30-08 | 1895 | 880.2 | 2.15 | 407 | 153 | 16 |
| RC30-09 | 1957 | 974.7 | 2.01 | 413 | 281 | 24 |
| RC30-10 | 1955 | 967.0 | 2.02 | 419 | 212 | 24 |
| RC30-11 | 1937 | 1010.5 | 1.92 | 412 | 198 | 30 |
| RC30-12 | 1922 | 1100.1 | 1.75 | 417 | 230 | 26 |
| RC30-13 | 1965 | 886.0 | 2.22 | 414 | 292 | 26 |
| RC30-14 | 1682 | 1952.5 | 0.86 | 397 | 155 | 20 |
| RC30-15 | 2334 | 931.9 | 2.50 | 451 | 403 | 35 |
| RC30-16 | 1898 | 857.5 | 2.21 | 413 | 204 | 18 |
| RC30-17 | 1785 | 820.1 | 2.18 | 404 | 193 | 19 |
| RC30-18 | 1732 | 1745.3 | 0.99 | 399 | 261 | 24 |
| RC30-19 | 1815 | 840.2 | 2.16 | 403 | 204 | 26 |
| RC30-20 | 1751 | 789.2 | 2.22 | 400 | 253 | 21 |
| RC30-21 | 1945 | 958.5 | 2.03 | 413 | 235 | 26 |
| RC30-22 | 1905 | 1076.1 | 1.77 | 410 | 222 | 28 |
| RC30-23 | 1219 | 1126.8 | 1.08 | 358 | 100 | 16 |
| RC30-24 | 1350 | 932.8 | 1.45 | 367 | 141 | 17 |
| RC30-25 | 1033 | 806.0 | 1.28 | 344 | 62 | 8 |
| RC30-26 | 1351 | 916.9 | 1.47 | 365 | 119 | 15 |
| RC30-27 | 928 | 340.4 | 2.73 | 334 | 58 | 8 |
| RC30-28 | 1200 | 1145.7 | 1.05 | 356 | 163 | 19 |
| RC30-29 | 1413 | 1376.8 | 1.03 | 372 | 107 | 11 |
| RC30-30 | 1172 | 899.8 | 1.30 | 352 | 104 | 15 |

## 6. Limitations (honest)
- **Proxy stages:** shots (160x284) and motion (320x569) are not native. Motion is a similarity fit on a proxy; 5,610
  frames (11 %) are marked uncertain (fit confidence). Motion magnitudes are proxy-scale values with no ground truth
  (A28 audit #4: A13 push +22 % verified as table arithmetic only, magnitude not validated).
- **Shot candidates are candidates, not shots.** 636 candidates over 30 videos. A15 (every-frame review): precision
  about 70 % (293 real / 417 reviewed rows; false positives from in-shot VFX/lighting, continuous camera moves, character
  animation, text/overlay fades), recall about 96 % (105/109 against overview + director ground truth). Known misses:
  slow same-palette dissolves (RC30-15 f1074-1087, RC30-23 f1156-1163), an object wipe (RC30-23 f173-187) and a match cut
  (RC30-23 f1099-1101); RC30-23 gave no candidate for its last 212 frames. The `hard_cut_candidate` label is unreliable in
  videos 12-30 (A15 F-a15-003: 32/32 correct in 01-08, many false in 12-30). Recall estimate is from 1 fps overview
  review and is a lower-quality bound on misses (cannot see two events within one second).
- **Slow-dissolve post-pass failed** (FAILED.md X-A27-011): no usable recall gain.
- No native-resolution motion or shot stage exists; a native re-run would be a new pipeline version (not done).
- Audio: first 33 ms zero-filled in all videos; onsets/loudness near t = 0 uncertain.
- Computational processing only; no visual inspection is claimed here (the sheets are for others to view).

## 7. A28 audit notes relevant to these tables (evaluations/phase3-audit/AUDIT.md)
- #6 loudness (audio.json): VERIFIED on 26 videos (median -14.1 LUFS; the -15 cluster = 18, 23, 24, 27-30); high.
- #14 native color.csv luma_p1 median 18/255 = 0.071 (IQR 10-26): the native table beats the 270 px proxy used by A11;
  A28 ruled for the A27 native numbers (contradiction table, p1 0.099 vs 0.071).
- #4 motion table: proxy, magnitude not validated; use as relative/ordinal evidence.
- #19 and ledger-honesty section: claims at 1 fps tiles vs every-frame strips; shot tables for 06, 09, 10, 11 were missing at
  audit time and now exist in the v0.2.0 tables.
- A28 re-derived from A27 v0.2.0 private tables without finding table inconsistencies (no A27 numeric correction requested).
