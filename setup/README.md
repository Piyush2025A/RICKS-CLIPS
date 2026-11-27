# Environment setup (proposed — awaiting user approval)

Nothing here has been run or saved as the cloud environment's setup script. Applying it is a separate decision.

## Tiers
| Tier | File | For | Status |
|---|---|---|---|
| Analysis core | `requirements-analysis.lock` (22 pkgs) | Phase 3 frame/colour/motion analysis | hash-pinned, resolution verified (pip `--dry-run --require-hashes`) |
| Analysis + audio | `requirements-analysis-audio.lock` (40 pkgs) | adds librosa (onsets, beat tracking, pitch) | same; heavier (numba, llvmlite, scikit-learn) |
| Rendering | — | Phase 5+ Node: remotion, @remotion/three, three, R3F, postprocessing | not prepared; A25 pins in `package.json` after approval |

Top-level choices (Python 3.13 cp313/abi3 wheels exist for all, checked 2026-11-27):
numpy 2.5.5 · opencv-python-headless 5.1.0.95 (no GUI/libGL needed) · scipy 1.18.1 · scikit-image 0.26.0 (SSIM,
CIEDE2000, skeletonize) · soundfile 0.14.0 (bundles libsndfile) · matplotlib 3.11.2 (plots for reports) ·
pillow 13.0.0 · optional librosa 1.0.1.

Deliberately excluded: Blender, yt-dlp, faster-whisper/PyTorch, any downloaded binaries. Each needs a separate
justification and authorisation. FFmpeg/FFprobe 6.1.1 come from the base image.

## Run (after approval)
```bash
bash setup/setup-analysis.sh
```
```bash
bash setup/setup-analysis.sh --with-audio
```
- Creates `.venv-analysis/` (git-ignored); idempotent via a lock-file hash stamp; binary wheels only; hashes
  enforced; `pip check` and an import smoke test run at the end.
- Hashes are for Linux x86_64 / CPython 3.13 wheels. Another platform needs a re-resolved lock.

## As a cloud setup script (proposal, not applied)
If approved, the environment setup script would be one guarded line run from the repo checkout's parent:
```bash
if [ -d RICKS-CLIPS ]; then bash RICKS-CLIPS/setup/setup-analysis.sh; fi
```
