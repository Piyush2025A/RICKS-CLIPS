# Phase 3 local execution: dependencies, install, calibration, resumable plan (prepared 2026-11-27)

Status: **plan only. Nothing installed, no analysis run, manifest not frozen.** Inputs:
`research/rc30-dataset-verification.md` (D025), `research/phase3-plan.md`, `analysis/README.md`, `setup/`.
Runs in the user's **local** session (the footage exists only on this computer).

## 1. Exact dependencies of rcpipe v0.2.0 (MEASURED from code and lock files)
- **System (present, verified):** FFmpeg + FFprobe 6.1.1, CPython **3.13** (`~/miniconda3/bin/python3.13`, 3.13.13,
  `ensurepip` + `venv` + OpenSSL 3.5.6 available), glibc 2.39, x86_64. The system Python 3.12 and the existing
  `~/.venv` (3.12) are **not usable** (the script asserts 3.13) and are not touched.
- **Python packages imported by `analysis/`:** numpy, cv2 (opencv-python-headless), scipy, skimage (scikit-image),
  soundfile, PIL (pillow); **librosa** is imported by the audio stage (`rcpipe/audio.py`), so the **audio tier is
  required** for RC30 (sound analysis is mandatory under the RC30 rule).
- **Lock to install:** `setup/requirements-analysis-audio.lock`, 40 packages, hash-pinned, binary wheels only:
  numpy 2.5.5, opencv-python-headless 5.1.0.95, scipy 1.18.1, scikit-image 0.26.0, soundfile 0.14.0 (bundles
  libsndfile), pillow 13.0.0, matplotlib 3.11.2, librosa 1.0.1 + numba 0.68.1 / llvmlite 0.50.0 / scikit-learn 1.9.1 /
  soxr 1.1.0 and their pinned dependencies (full list in the lock). The 18 packages beyond the core lock are all
  librosa's dependency tree.
- No system packages (apt), no GPU libraries, no compilers needed. Download ≈ the 715 MB venv measured in the cloud
  (D016); disk free 105 GB.

## 2. Recommended isolated installation (awaiting approval)
```bash
cd ~/RICKS-CLIPS && PYTHON=~/miniconda3/bin/python3.13 bash setup/setup-analysis.sh --with-audio
.venv-analysis/bin/python analysis/tests/run_tests.py      # expect 318/318 (incl. 44 negative controls)
```
- Creates only `~/RICKS-CLIPS/.venv-analysis/` (git-ignored, `include-system-site-packages = false`); `--require-hashes
  --only-binary=:all: --no-deps`; `pip check` + import smoke test; idempotent (lock-hash stamp). Does not modify the
  miniconda base environment, system Python, `~/.venv`, PATH or shell profiles. Removal = delete that one folder.
- Why the explicit `PYTHON=`: `python3` resolves to miniconda today only because of PATH order; pinning the path
  makes the run independent of the shell.
- Known coupling (INFERRED): a venv links to its base interpreter; if miniconda's base Python is later upgraded past
  3.13, recreate the venv (re-run the script after deleting the folder). Alternative with stronger isolation: a
  dedicated conda env (`conda create -n rcpipe python=3.13.13`) as the base — rejected as default because it changes
  the conda installation and pulls packages outside the hash-pinned lock.
- The wheels' compatibility with this machine is INFERRED from tags (cp313, manylinux x86_64, glibc ≥ 2.17); the test
  suite run is the verification.

## 3. Real-footage calibration — one video (procedure, awaiting approval)
**Precondition:** `knowledge/dataset/MANIFEST.json` frozen. rcpipe refuses any `RC30-*` key without it (by design,
`pipeline.resolve_dataset`); the pilot is not run under a fake key.
**Pilot video:** the shortest file, `27.mp4` (928 frames, 30.93 s; its RC30 key follows from the freeze). Short means
the whole video can be inspected visually. Optional holdout (recommended): one long video, e.g. `15.mp4` (2,334 frames),
checked with the calibrated settings before the batch, to avoid tuning to a single video.

| Step | Action | Output (private unless stated) | Pass criterion |
|---|---|---|---|
| C0 | Re-hash `27.mp4` against the frozen manifest | — | SHA-256 equal |
| C1 | `run_pipeline.py <file> --key RC30-nn --dataset RC30 --manifest knowledge/dataset/MANIFEST.json --out ~/ricks-clips-private/analysis-data/rc30/v0.2.0 --sheets-every 1` (native decode; motion/shots on proxies as built) | per-frame tables, coverage, run manifest, sheets | exit 0; record wall time + peak RSS |
| C2 | Frame accounting cross-check: rcpipe frames vs the independent `framemd5` pass (D025) | — | 928 frames, identical pts list, ok + uncertain + failed + missing = 928 |
| C3 | Ground truth: director views **every** frame on the 1-frame contact sheets, then each shot-boundary candidate and each suspected boundary ±3 frames at native resolution; labels cut / dissolve (start-end) / flash / whip / none. Every view logged in `coverage/visual/director.jsonl` (frames, resolution, purpose) | label file (text; committed — numbers and frame IDs only) | visual coverage recorded honestly |
| C4 | Score detectors vs labels: shot-boundary precision/recall and frame offset; dissolve span error; flash detection | calibration table (text, committed) | target (proposed): hard-cut recall 100 %, ≤ 1 false positive/min, boundary offset 0 frames |
| C5 | Inspect specific known risks: same-palette hard cuts (synthetic miss at MAD 14.1–14.6 vs `cut_mad=15.0`); burned-in caption/UI band (set `--exclude-bottom/--exclude-top` from what is seen); static holds (0 bit-identical consecutive frames in all 30 files → holds need a tolerance); camera-vs-parallax blending flag | notes | each risk measured, not assumed |
| C6 | Audio: rcpipe extracts a **temporary 48 kHz mono** WAV from the 44.1 kHz stereo AAC. This is a derived analysis copy (the original is untouched), but it resamples and down-mixes. Decision for the user: accept as is (documented), or change rcpipe to analyse at native 44.1 kHz and keep stereo/side-channel measures | decision | recorded in DECISION_LOG |
| C7 | If any threshold or behaviour changes → rcpipe **0.3.0**: full suite re-run (318 + new real-footage regression using the committed labels), failures logged in A27's `FAILED.md`, decision entry; re-run C1–C4 | new version | suite all-pass; C4 targets met |
| C8 | Holdout (if approved) on one long video with frozen settings; spot-check boundaries | calibration table | same targets; otherwise back to C7 |
| C9 | Stop for review: report timing, accounting, scores, changes | report (committed) | user approves the batch |
Owner: A27 runs C1, C2, C4, C7 (`a27-frame-analysis-specialist`); the director does C3 labelling (A27 must not grade its
own detector on its own labels); A15 can be added as a second labeller (≤ 2 agents).

## 4. Resumable execution plan — 30 videos and specialists
**State and resume rule.** A video is *done for a stage* only if its computational coverage record exists with the
frozen `manifest_sha256`, the file's `input_sha256`, the batch `config_fingerprint`, and ok + uncertain + failed +
missing = `nb_frames` from the manifest. On restart, the batch script skips done videos and rcpipe's chunk checkpoints
resume inside a partly done video (decode-only replay). Progress is recorded in `PROGRESS.md` after each batch.
| Step | Who | Action | Gate |
|---|---|---|---|
| B0 | user | Identity + authorisation inputs (§5); approvals | user |
| B1 | director | Match files ↔ IDs ↔ dates, assign `RC30-01` newest … `RC30-30`, freeze and commit `MANIFEST.json`, record its SHA-256 | user approves freeze |
| B2 | director | Install venv (§2), suite 318/318 | user approves install |
| B3 | A27 + director | Calibration §3 | user approves batch |
| B4 | A27 | Batch the other videos one at a time, shortest first (early failures are cheap); default output root `~/ricks-clips-private/analysis-data/rc30/<version>/`; contact sheets every frame only if approved (disk/time), otherwise every 30 + all candidates | coverage = **50,898** frames, or every missing frame listed |
| B5 | A27 | Shared tables summary + SHA-256 of every per-frame table committed; tables stay private (plan §5) | committed ledger |
| B6+ | specialists | Waves 2–10 of `research/phase3-plan.md` §6, max 2 concurrent, briefs by path; agents that need pixels or tables run **in this local session** (cloud sessions cannot reach the footage) | per wave, user review at wave 1→2 and at the Phase 3 gate |
Time: unknown until C1 is measured. Reference point: decode + per-frame hashing of all 30 took 14 min here (D025);
rcpipe does more per frame, so expect hours, not minutes (INFERRED). Each batch run is bounded (e.g. 5 videos) so the
user can review between runs.
First-use agents: A20, A15, A13, A16, A14, A07, A09, A11, A10, A08, A01–A06, A12, A17–A19, A21, A22, A28 are discoverable
but unverified by invocation; each first brief starts with an identity/ownership check (as done for A27 in D012).

## 5. Inputs still needed from the user
1. Per file `1.mp4` … `30.mp4`: YouTube URL or video ID (titles are embedded, so a list of 30 URLs in any order is
   enough; the director matches by title and reports any mismatch).
2. Publication date/time: exact `publishedAt` needs the YouTube Data API (key via the secure form, plan §2) — or the
   user supplies dates from each video page (day precision) plus the Shorts-tab order to break ties.
3. Confirmation that these are the 30 newest Shorts on the channel's Shorts tab today (no newer Short missing, none
   older included).
4. Acquisition method and its authorisation (who obtained the files, how, and under which permission), to be written
   into `acquisition_method`. The files' metadata suggests merged YouTube streams (INFERRED, D025); plan §3 records
   that downloading without written permission conflicts with the YouTube ToS. This is the user's decision; the
   director records it and does not proceed with analysis until it is stated.
