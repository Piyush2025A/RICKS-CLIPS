# Analysis environment verification — 2026-11-27 (Phase 2.5, user-approved install)

Command: `bash setup/setup-analysis.sh --with-audio` in the claude.ai/code cloud container. Exit 0.

## Environment
- CPython 3.13.18 (system), venv `.venv-analysis/` (git-ignored, `include-system-site-packages = false`), pip 26.2.2.
- FFmpeg / FFprobe 6.1.1-3ubuntu5 (base image). libsndfile 1.2.2 (bundled with soundfile).
- Lock: `requirements-analysis-audio.lock`, 40 packages, 40 sha256 hashes, sha256 prefix `743318255c7521ff`.
  Core lock (22) is a strict subset of the audio lock.

## Results
| Check | Result |
|---|---|
| Install time (fresh venv, wheels from PyPI through the proxy) | **15 s** wall |
| Disk | venv 715 MB after install (752 MB after smoke tests' bytecode); pip cache 230 MB in `~/.cache/pip` (outside repo) |
| `pip check` | No broken requirements |
| Installed set vs lock | identical (40/40 names and versions; pip itself excluded) |
| Imports | 40/40 top-level modules import, incl. librosa 1.0.1, numba 0.68.1, llvmlite 0.50.0, scikit-learn 1.9.1 |
| Idempotency | re-run prints "analysis venv up to date", 0 s, no changes |
| `git status` | venv ignored; nothing new tracked |

## Smoke tests (synthetic data only, scratchpad, nothing kept)
| Test | Expected | Got |
|---|---|---|
| OpenCV phaseCorrelate, 7 px pan, 360×640 | 7, 0 | 7.00, −0.00 |
| skimage SSIM shifted vs original | < 1 | 0.972 |
| skimage CIEDE2000 self-difference | 0 | 0.0000 |
| Farneback optical flow, textured 7 px pan | ≈ 7 | 6.97 |
| PIL PNG write, matplotlib Agg savefig | ok | ok |
| FFmpeg encode 48 frames 24 fps (libx264, rawvideo pipe) → FFprobe `-count_frames` | 360×640, 24/1, 48 | 360×640, 24/1, 48 |
| OpenCV VideoCapture decode of same file | 48 frames | 48, luma ramp preserved |
| FFmpeg raw gray pipe decode (every-frame path) | 48 | 48 |
| soundfile WAV round trip 48 kHz | 96000 samples | 96000 |
| librosa yin f0, 440 Hz sine | 440 | 440.6 Hz |
| librosa onset_detect, clicks at 0.5/1.0/1.5 s | 0.5, 1.0, 1.5 | 0.51, 1.00, 1.50 |
| librosa resample 48k→16k (soxr) | 16000 | 16000 |
| scipy Welch peak, nperseg 8192 | 440 | 439.5 Hz |
| FFmpeg AAC encode → FFprobe → f32le decode | aac 48 kHz mono | aac 48000 1ch, 96256 samples (AAC priming/padding) |
| FFmpeg ebur128 integrated loudness | finite | −13.9 LUFS |

Test-design failures (not library faults), recorded per rule 2:
- First Farneback run on a flat, untextured rectangle returned dx 0.00 (aperture problem). Re-run on texture: 6.97.
- First Welch run used the default nperseg 256 (187.5 Hz bins) and peaked at 375 Hz. Re-run at nperseg 8192: 439.5 Hz.

## Installed versions (pip freeze)
`certifi==2026.11.20 cffi==2.1.1 charset-normalizer==3.5.3 cloudpickle==3.1.3 contourpy==1.4.0 cycler==0.12.1 decorator==5.3.2 fonttools==4.69.1 idna==3.20 ImageIO==2.38.2 joblib==1.6.0 kiwisolver==1.5.1 lazy-loader==0.6 librosa==1.0.1 llvmlite==0.50.0 matplotlib==3.11.2 msgpack==1.2.4 narwhals==2.29.0 networkx==3.7 numba==0.68.1 numpy==2.5.5 opencv-python-headless==5.1.0.95 packaging==26.4 pillow==13.0.0 platformdirs==4.14.8 pooch==1.9.0 pycparser==3.12 pyparsing==3.3.3 python-dateutil==4.0.0 requests==2.34.2 scikit-image==0.26.0 scikit-learn==1.9.1 scipy==1.18.1 soundfile==0.14.0 soxr==1.1.0 threadpoolctl==3.8.0 tifffile==2026.11.26 typing_extensions==4.16.0 tzdata==2026.6 urllib3==2.8.0 `

## Restoring in future cloud sessions
- The container is ephemeral; the venv does not survive. Re-run `bash setup/setup-analysis.sh --with-audio`
  (≈15 s; needs PyPI, which the environment allows by default). The hash stamp makes repeat runs no-ops.
- Optional (not applied; needs separate approval because it changes the stored cloud environment): save the guarded
  line `if [ -d RICKS-CLIPS ]; then bash RICKS-CLIPS/setup/setup-analysis.sh --with-audio; fi` as the environment
  setup script so every new session starts with the venv ready.
- Hashes are Linux x86_64 / CPython 3.13 only. A Python minor-version change in the base image fails the precondition
  check early, by design; re-resolve the lock then.
