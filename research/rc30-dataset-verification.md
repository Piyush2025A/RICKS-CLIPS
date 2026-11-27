# RC30 dataset verification (Phase 3 preparation) — 2026-11-27

Status: **verification only, the dataset is NOT frozen and analysis has NOT started.** This ran in the user's
**local** Claude Code session on their computer (not the cloud container). Every probe was read-only: no file was
renamed, moved, re-encoded, resampled, uploaded or deleted. Media, frames and per-frame hashes stay outside the
repository (session scratchpad). Only this text and `knowledge/dataset/MANIFEST.draft.json` are committed.

## 1. Access and readability (MEASURED)
- Directory `~/ricks-clips-private/reference-videos/RC30/` (outside the repo): readable, 30 regular files
  `1.mp4` … `30.mp4`, nothing else. All 30 open and decode in full.
- Method: `ffprobe -show_format -show_streams` per file; `sha256sum`; full decode
  `ffmpeg -v error -i N.mp4 -map 0:v:0 -map 0:a:0 -f framemd5` (every video and audio frame decoded and hashed);
  video and audio packet tables via `ffprobe -show_entries packet=pts,dts,duration,flags`.
  Decode wall time 14 min 3 s for all 30 (CPU 29 min 47 s) on this computer.

## 2. Uniform technical properties (MEASURED, identical in all 30 files)
| Property | Value |
|---|---|
| Container | MP4 (`isom`, brands `isomiso6iso2avc1mp41`), written by `Lavf60.3.100` |
| Streams | exactly 1 video + 1 audio; no subtitle/data streams; no rotation side data |
| Video | H.264 High, level 4.0, 1080 × 1920 (vertical), yuv420p, progressive, limited (tv) range, BT.709 primaries/transfer |
| Frame rate | `r_frame_rate` = `avg_frame_rate` = 30/1; time base 1/15360; every packet step = 512 ticks = 1/30 s → **CFR 30 fps** |
| Audio | AAC-LC, 44,100 Hz, stereo, ~128 kb/s |
| Stream start | video first pts = 0.0333 s (1 frame), audio first pts = 0 s — offset to be honoured in A/V sync work |
| Embedded tags | `title` = video title, `artist` = "Ricks Clips"; stream handler "ISO Media file produced by Google Inc." No video ID, URL or date tags. |

## 3. Per-file results (MEASURED)
Frames = decoded video frames (= video packets = round(video duration × 30) in every file). Full SHA-256 in
`knowledge/dataset/MANIFEST.draft.json`.

| File | Embedded title | Frames | Video s | Container s | Bytes | Keyframes | SHA-256 (prefix) |
|---|---|---|---|---|---|---|---|
| 1.mp4 | Why Astronauts Can't Flush in Space | 1836 | 61.200 | 61.288 | 29,448,949 | 16 | `044548ca63faec6d…` |
| 2.mp4 | The Prisoner Who Tunneled Into a Bank | 1659 | 55.300 | 55.390 | 28,594,693 | 14 | `da755b91139eaee7…` |
| 3.mp4 | Why Samurai Feared The Flying Thunder | 1772 | 59.067 | 59.151 | 24,649,676 | 16 | `9c0c8f476a09c617…` |
| 4.mp4 | The Instinct That Makes You Crash | 1783 | 59.433 | 59.523 | 32,602,988 | 21 | `46128f6ebce54c38…` |
| 5.mp4 | How Mine Salting Worked | 1832 | 61.067 | 61.148 | 32,207,436 | 22 | `c579f05d47f9a51e…` |
| 6.mp4 | How One Cart Stopped an Entire Army | 2005 | 66.833 | 66.930 | 37,199,768 | 14 | `e783667da21ecd7d…` |
| 7.mp4 | Why Drivers Started Filming The Road | 1867 | 62.233 | 62.332 | 30,641,447 | 14 | `106b9a5feb64130b…` |
| 8.mp4 | This Shape Saved Roller Coasters | 1895 | 63.167 | 63.238 | 35,194,363 | 12 | `ecda566c555f50ed…` |
| 9.mp4 | The Pink Prison Cell Experiment | 1957 | 65.233 | 65.328 | 30,635,997 | 13 | `e7fcb2caa10e35be…` |
| 10.mp4 | Why Perfect Railroads Don't Work | 1955 | 65.167 | 65.258 | 36,004,258 | 14 | `00496dd4ecef5326…` |
| 11.mp4 | Why Sailors Carried Storm Oil | 1937 | 64.567 | 64.654 | 34,270,304 | 14 | `c5c83a1ee3f34c10…` |
| 12.mp4 | How a Mirror Rigged a Horse Race | 1922 | 64.067 | 64.167 | 35,274,885 | 16 | `464fc086bdaa74e3…` |
| 13.mp4 | The Town Built Around a Button | 1965 | 65.500 | 65.606 | 27,153,185 | 12 | `d466799da780116b…` |
| 14.mp4 | Why the Second Draw Always Wins | 1682 | 56.067 | 56.156 | 18,893,435 | 10 | `9b50b83493e38dbe…` |
| 15.mp4 | Every Memory Has a Price | 2334 | 77.800 | 77.890 | 28,973,900 | 17 | `99f601758bab9950…` |
| 16.mp4 | He Could Spot Winning Tickets Just by Looking | 1898 | 63.267 | 63.354 | 30,578,597 | 13 | `7c60204f8c5eca34…` |
| 17.mp4 | What the Grave Bell Really Meant | 1785 | 59.500 | 59.593 | 31,521,277 | 13 | `0b03186b0c851e54…` |
| 18.mp4 | Why Cashiers Keep Winning The Lottery | 1732 | 57.733 | 57.828 | 22,471,661 | 10 | `54c20b0747d8b07c…` |
| 19.mp4 | The Job Nobody Wants in Japan | 1815 | 60.500 | 60.591 | 21,142,906 | 17 | `09ef7fe7b3a14628…` |
| 20.mp4 | The Burglar Who Only Moved Furniture | 1751 | 58.367 | 58.455 | 24,101,832 | 13 | `3e0ea59cff6b291f…` |
| 21.mp4 | The Ancient Jar That Warned an Empire | 1945 | 64.833 | 64.933 | 36,187,888 | 15 | `5813b315f713d0d2…` |
| 22.mp4 | Levels of Pirate Cannonballs | 1905 | 63.500 | 63.586 | 30,193,303 | 15 | `bd873533cbb32941…` |
| 23.mp4 | This Knight Found the Ultimate Loophole | 1219 | 40.633 | 40.715 | 19,936,401 | 10 | `3e41fd80075efc67…` |
| 24.mp4 | An Unstoppable Spear vs an Unbreakable Shield | 1350 | 45.000 | 45.103 | 18,585,721 | 11 | `5af45ee1437dc755…` |
| 25.mp4 | How Painkillers Actually Work | 1033 | 34.433 | 34.538 | 15,938,771 | 8 | `6e8be44ff33b3a24…` |
| 26.mp4 | The Window That Breaks Japan's Gambling Law | 1351 | 45.033 | 45.126 | 16,748,402 | 11 | `20073b1bff120692…` |
| 27.mp4 | The Science Behind Slot Machines | 928 | 30.933 | 31.009 | 14,939,236 | 6 | `8d8c7621ff948b31…` |
| 28.mp4 | The Scientist's Insane Time Test | 1200 | 40.000 | 40.088 | 20,289,936 | 8 | `1abdaafacb53d7c2…` |
| 29.mp4 | Why Humans Can't Pick Random Numbers | 1413 | 47.100 | 47.193 | 20,347,400 | 11 | `cd4925a4119c9c8f…` |
| 30.mp4 | Your Brain's Secret Idea Zone | 1172 | 39.067 | 39.159 | 11,692,823 | 8 | `ccec3369b00d8a9b…` |

## 4. Duplicates, corruption, frame accounting (MEASURED)
- **Duplicates:** 30 distinct SHA-256; 30 distinct titles; **0** decoded video frames shared between any two files
  (exact frame-hash comparison over all 50,898 frames). No duplicate or re-uploaded video detected.
- **Corruption:** 0 decoder errors/warnings at `-v error`, ffmpeg exit 0 for all 30; audio packets = decoded audio
  frames in all 30.
- **Frame accounting:** in every file decoded frames = video packets = duration × 30; decoded pts are consecutive
  integers at 1/30 s (first 1, last = frame count): 0 gaps, 0 duplicated timestamps, 0 non-monotonic, 0 VFR steps.
  0 bit-identical consecutive frames (static holds are still re-encoded, so "held" frames differ by compression noise —
  hold detection must use a tolerance, not exact equality).
- Not checked: perceptual damage inside otherwise valid frames (requires viewing); none was viewed in this step.

## 5. Totals (MEASURED)
| Quantity | Value |
|---|---|
| Videos | 30 |
| Native video frames | **50,898** |
| Video stream duration | **1,696.600 s** (28 min 16.6 s) = 50,898 / 30 exactly |
| Container (longest stream) duration | 1,699.331 s |
| Storage | **796,421,438 bytes** (759.53 MiB) |

## 6. Identity, order and "latest 30" — NOT YET VERIFIED
- Filenames carry no ID or date; the files carry titles only. Video IDs, publication dates and source URLs are
  therefore **unknown** and the filename → `RC30-nn` mapping is not established. Whether `1.mp4` is newest is not
  assumed. (Observation only: files 23–30 are all 31–47 s, files 1–22 are 55–78 s.)
- Whether these are exactly the 30 most recently published Shorts cannot be verified from the files. It needs either
  (a) the 30 URLs/IDs + publication dates from the user, cross-checked against the channel's Shorts tab, or
  (b) the YouTube Data API key path of `research/phase3-plan.md` §2 (no key is present in this environment).
  Third-party channel tools and scraping youtube.com remain excluded (plan §2).

## 7. Acquisition provenance — USER CONFIRMATION REQUIRED
OBSERVED: the container was written by FFmpeg's libavformat 60.3.100 with YouTube's stream handler names and
embedded title/artist tags. INFERRED (not proven): the files are YouTube delivery streams merged into MP4 by an
FFmpeg-based tool, not creator masters. This matters because `research/phase3-plan.md` §3 rates download from YouTube
without written permission as conflicting with the YouTube ToS. The acquisition method and its authorisation must be
recorded by the user in `acquisition_method` before the manifest is frozen. Implication for analysis if they are
YouTube streams: ~2.3–4.3 Mb/s H.264 re-encodes; fine detail (outline width, grain, gradients) is compression-limited
and findings must say so.

## 8. Local compatibility with rcpipe v0.2.0 (MEASURED unless marked)
| Item | This computer | rcpipe/lock needs | Verdict |
|---|---|---|---|
| OS / arch | Linux Mint 22.1, x86_64, glibc 2.39 | manylinux x86_64 | compatible (INFERRED from wheel tags) |
| Python | 3.13.13 (miniconda, `python3`); system 3.12.3 (`~/.venv`) | CPython 3.13 | use the miniconda 3.13 interpreter (`PYTHON=python3`) |
| FFmpeg / FFprobe | 6.1.1 (Ubuntu build) | 6.1.1 | same version as the validated cloud setup |
| Python packages | numpy 2.4.6 only; cv2, scipy, skimage, soundfile, librosa absent | 40-package lock | **not installed**; `setup/setup-analysis.sh --with-audio` would create `.venv-analysis/` (~715 MB) — needs approval |
| CPU | Intel i7-7600U, 2 cores / 4 threads | — | slow but sufficient |
| RAM | 15 GiB (≈ 8 GiB available at test time) | ~105 MB RSS measured on synthetic runs | sufficient |
| GPU | Intel HD 620 (no CUDA) | none required | n/a |
| Disk | 105 GB free | per-frame tables: tens of MB (INFERRED) | sufficient |
Not done: lock resolution dry run on this machine, test-suite run (both need the venv).

## 9. Processing strategy (recommendation)
- **Run rcpipe locally in this session.** Footage is already here; moving 796 MB to the cloud would need ~90–100
  Drive parts of ≤ 9 MB uploaded by hand, re-ingested in every new ephemeral cloud session, and puts more copies of
  third-party footage in more places. Local runs keep the private master in one place.
- Pace: full decode + hashing ran at ≈ 60 fps here; rcpipe adds proxy motion/flow, shots, colour, edges, audio, so
  expect several hours for all 30 (INFERRED; measure on one video first). Run one video at a time (A27 alone, wave 1)
  with rcpipe chunk checkpoints so any interruption resumes; ≤ 2 agents total.
- Outputs: per-frame tables and contact sheets in `~/ricks-clips-private/analysis-data/` (never committed);
  coverage ledgers, aggregates, findings and table checksums committed (plan §5). Cloud sessions can work from the
  committed text; small private artefacts move via Drive only when needed.

## 10. Agents (MEASURED in this local session)
All 29 types `a01-character-designer` … `a29-final-qa-specialist` are listed in this session's registered agent
types; `python3 tools/validate_agents.py` → PASS. Discoverable ≠ invoked: only A23 and A27 have been verified by
invocation (D012, D017); none was invoked in this step.

## 11. Resumable execution plan (after approval only)
Each step is idempotent and ends with a recorded checkpoint in `PROGRESS.md`.
| Step | Action | Gate / evidence | Resume rule |
|---|---|---|---|
| V1 | User supplies 30 URLs (or IDs) + confirms Shorts-tab order; user records acquisition method/authorisation | user message | — |
| V2 | Director matches titles → IDs, assigns `RC30-01` (newest) … `RC30-30`, checks the newest 30 have no gaps; freezes `MANIFEST.json` (schema-validated), commits, records its SHA-256 | user approves freeze | re-run is a pure function of V1 inputs |
| V3 | Re-verify SHA-256 of all 30 files against the frozen manifest | 30/30 match | per file |
| V4 | Install venv (`PYTHON=python3 bash setup/setup-analysis.sh --with-audio`), run rcpipe suite (expect 318/318) | user approves install | script is idempotent |
| V5 | A27 pilot: rcpipe on the shortest video (`27.mp4`, 928 frames) at native fps; measure time/RSS; calibrate thresholds on real footage (new version + full suite if changed) | user reviews pilot | rcpipe chunk checkpoints |
| V6 | A27: remaining 29 videos one at a time; computational coverage must total 50,898 frames (or list every missing frame) | coverage ledger | skip videos with complete coverage + matching sha |
| V7+ | Specialist waves 2–10 per `research/phase3-plan.md` §6 | per wave | each agent's ledger |
