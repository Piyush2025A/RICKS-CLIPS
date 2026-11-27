# Phase 3 shared specialist brief (director, 2026-11-28) — read fully before working

## Dataset (frozen)
- `knowledge/dataset/MANIFEST.json`, SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06`
  (quote it in every finding). Keys `RC30-01` (newest, `1.mp4`) … `RC30-30` (`30.mp4`), order by user attestation;
  video IDs/dates deferred (`IDENTITY.json`). 30 videos, 50,898 frames, all 1080×1920, CFR 30 fps, AAC 44.1 kHz stereo.
- Titles per key: `MANIFEST.json` → `videos[].title`. Frame ID = `RC30-nn-fNNNNNN` (zero-based decode index);
  t = (index + 1) / 30 s (first video pts is 0.0333 s; audio starts at 0).
- Footage (private, read-only, never copy into the repo): `~/ricks-clips-private/reference-videos/RC30/<n>.mp4`.

## Computational tables (A27 / rcpipe v0.2.0, private) — read these before viewing images
`~/ricks-clips-private/analysis-data/rc30/v0.2.0/RC30-nn/`:
| File | Content (per frame unless noted) | Resolution |
|---|---|---|
| `frames.csv` | frame_id, frame_index, pts_time | — |
| `color.csv` | luma mean/std/p1…p99, CIELAB L/a/b mean+std, sat/val, hue circular mean, chroma_frac, 12-bin hue histogram | native |
| `edges.csv`, `sharpness.csv` | edge density, dark-pixel ("ink", gray < 60 — includes dark scenery) fraction, Laplacian sharpness | native |
| `motion.csv` | global camera model tx, ty, scale, rot_deg, inliers, confidence; residual (object) motion mean/p95/active fraction/centroid | **proxy** ≤ 320 px |
| `shot_features.csv`, `shot_candidates.json` | histogram/MAD/SSIM differences; boundary CANDIDATES (cut / gradual / flash) | **proxy** 160 px |
| `audio.json`, `audio_env.csv` | EBU R128 loudness on native stream; 10 ms RMS, centroid, 3 band levels, dominant freq, onset strength; onset times | loudness native; rest 48 kHz mono (limits: `research/phase3-local-execution.md` §7) |
| `coverage.jsonl`, `measurements.json` | coverage counts; per-video aggregate measurements | — |
| `sheets/RC30-nn_sheet_fAAAAAA-fBBBBBB.png` | contact sheets: **every frame**, 48 per sheet (8×6), 120×213 per tile, frame ID + time printed | 120×213 |
Calibration facts (`research/phase3-calibration.md`): transitions seen so far are ~6-frame crossfades; candidate lists
contain false positives (in-shot fast animation, duplicate fragments) → confirm visually before counting.
Overview sheets (one per video, 1 frame per second, larger tiles): `~/ricks-clips-private/analysis-data/rc30/overview/RC30-nn_overview.png`.

## Viewing images (authorised: Claude only)
- You may open contact sheets, overview sheets and native frames with Read. Native frames:
  `.venv-analysis/bin/python analysis/get_frames.py ~/ricks-clips-private/reference-videos/RC30/<n>.mp4 --key RC30-nn
  --frames RC30-nn-f000123 ... --out ~/ricks-clips-private/analysis-data/rc30/agents/<agent-id>/`
  Crops/strips you make also go under that private folder. **Never** write images into the repo, never upload them.
- **Log every image you open**: `python3 tools/vlog.py <agent-id> <kind> <WxH as seen> "<purpose>" <frame IDs/ranges>`.
  Computational processing is not inspection. Never claim more visual coverage than your ledger shows.
- You cannot hear audio. Audio work is computational (tables, ffmpeg/librosa on the native stream, spectrogram images
  you render privately); spoken words are available from the burned-in captions (one word/phrase at a time, ≈ 70 %
  frame height), which you can read from sheets/frames.
- Tools: `.venv-analysis/bin/python` (numpy, opencv, scipy, scikit-image, librosa, matplotlib, soundfile), ffmpeg 6.1.1.
  Do not install anything; do not modify `analysis/` (A27-owned, frozen v0.2.0); write scripts under your private
  agent folder or your owned repo paths.

## Coverage expectation
Cover the dataset broadly: use evidence from **≥ 20 of the 30 videos** for any pattern you call recurring (EVIDENCE.md:
`high` = consistent across ≥ 2/3 of videos, n ≥ 20). Use tables to find candidates across all 30, then view sheets/frames
to confirm. Note variations and exceptions with their video keys.

## Deliverables (inside your owned knowledge folder, see `knowledge/_system/OWNERSHIP.md`)
1. `FINDINGS.md` — numbered `F-<agent>-NNN`, each with: claim; label (MEASURED/OBSERVED/INFERRED/HYPOTHESIS);
   evidence (keys, frame IDs/ranges or audio times, table + column used, n videos); method; confidence + reason;
   limitations; **implementation** (how to reproduce with Three.js/Remotion/FFmpeg/Google Flow/our tools).
   Header: manifest SHA-256, date, visual-ledger record count, videos covered.
2. `TECHNIQUES.md` — reusable production recipes derived from the findings (parameters, not prose).
3. `FAILED.md` — methods that did not work and why (may be short).
4. Optional `data/*.json|csv` — small numeric summaries you computed (text only; no per-frame dumps > 1 MB).
Return a ≤ 250-word hand-off: files written, top findings, coverage numbers, open questions.

## Hard rules
Original-work goal: describe techniques to reproduce the *craft*, never to copy characters, designs, stories or
artwork. No credentials, no media in git, no paid services, no generations, no web uploads. Stay inside your owned
paths (plus your visual ledger). If something fails, record it in `FAILED.md` and continue with what you can do.
