<!-- owner: A26 | status: final | version: 1.0 | last_updated: 2026-11-28 -->
# BENCHMARK_5A: Phase 5A render verification (EngineTest, 360x640 @ 24 fps, 48 frames)

Evidence tags: all MEASURED unless stated. Script version `a26-render-v1` (`pipeline/render/render.ts`, `common.ts`, `diag/index.tsx`).
Experiment record: `experiments/EXP-a26-20261128-01.md`. Outputs in git-ignored `out/a26/` (206 MB total, incl. 9 PNG sequences' last copies, 3 bundles, MP4s).

## Environment
4 vCPU Intel Xeon @ 2.30 GHz, 15 GiB RAM, no GPU. Node 22.23.5, Remotion 4.0.547, three 0.187.0, R3F 9.8.2, commit 196f572.
Browser: Remotion chrome-headless-shell 158.0.8127.2 (UA string). ffmpeg/ffprobe 6.1.1. gl = swangle (ANGLE over SwiftShader Vulkan). scale 1, PNG for tests.
Plate SHA-256 `bd4fac1d...a3a`: verified before and after every run (all `plateUnchanged: true`; final sha256sum identical; inode shared by hard links only).

## 1. Determinism (MEASURED, confidence high for this machine/flags/version; not cross-machine)
| Test | n pairs | Result |
|---|---|---|
| Frame 24, two fresh processes | 1 | identical (`aee435c5...`) |
| Frames 0, 17, 47, each twice in fresh processes | 3 | 3/3 identical (`9ae42f70`, `dd91a719`, `e9369f40`) |
| Same process, 10 stills: 24,24,0,0,17,17,47,47,24,24 | 5 | 5/5 pairs identical; also equal to the fresh-process hashes |
| 48-frame PNG sequence x3 at each of concurrency 1, 2, 4 (9 runs) | 9 runs x 48 | 48/48 frames identical in every run vs run c1_1 (432/432); max distinct hashes per frame = 1 |
| Sequence frame vs still of the same frame (0, 17, 24, 47) | 4 | identical |
| All 48 frames distinct from each other | 48 | 48 unique hashes (animation moves) |
| MP4 (c4, no audio) rendered twice | 1 | file SHA-256 identical (`4aafd276...`) |
No mismatch, so no pixel-diff quantification was needed. Concurrency does not change pixels.

## 2. Performance (MEASURED; software WebGL, NOT predictive of GPU)
| Item | n | median | p90 / range | Notes |
|---|---|---|---|---|
| Bundle, cold webpack cache | 1 | 16.1 s | - | cache dir `node_modules/.cache/webpack` removed first; diag bundle cold 15.8 s |
| Bundle, warm | 3 | 2.6 s | 2.3-2.8 | (+1 earlier 2.0 s) |
| selectComposition (fresh browser) | 9 | 0.32 s | 0.29-0.35 | |
| Still, fresh process (browser launch included) | 7 | 0.608 s | p90 0.632, 0.574-0.634 | process-level time incl. node start about +0.5 s (not in table) |
| Still, same process, 10 stills (browser launched per still) | 10 | 0.671 s | p90 0.715, 0.635-0.739 | |
| Sequence 48 f PNG, concurrency 1 | 3 | 4.58 s = 10.5 fps = 0.095 s/frame | 4.52-4.66 | |
| Sequence 48 f PNG, concurrency 2 | 3 | 2.97 s = 16.2 fps = 0.062 s/frame | 2.81-3.00 | 1.54x |
| Sequence 48 f PNG, concurrency 4 | 3 | 2.68 s = 17.9 fps = 0.056 s/frame | 2.66-2.69 | 1.71x; c4 on 4 vCPU gains little over c2 |
| MP4 H.264 crf 18, jpeg frames q100, concurrency 4 | 1 timed (+1 audio run 2.44 s) | 2.19 s (21.9 fps) | - | includes encode |
Cold vs warm: first still after container idle was 0.594 s (no distinct cold penalty seen); only the webpack bundle shows a cold penalty (16 s vs 2.6 s).
Scene is a single textured card + placeholder box: this is a floor, not representative of lit multi-card scenes. Extrapolate nothing to 1080p or GPU.

## 3. Memory and disk (MEASURED, /proc sampling every 150 ms)
| Case | node VmHWM | Chromium sum RSS peak (processes) | max single Chromium VmHWM | total peak |
|---|---|---|---|---|
| still | 169 MB | 482 MB (5) | 164 MB | 647 MB |
| seq c1 (n=3) | 203-212 MB | 495-500 MB (5) | 164 MB | 690-700 MB |
| seq c2 (n=3) | 211-214 MB | 673-679 MB (6) | 165 MB | 871-882 MB |
| seq c4 (n=3) | 204-207 MB | 1038-1043 MB (8) | 186-191 MB | 1240-1246 MB |
| mp4 c4 | 190 MB | 1096-1110 MB (9) | 186-191 MB | 1283-1298 MB |
Roughly +180 MB per extra browser tab. 16 GiB is ample at 360p. Peak disk for everything in `out/a26` = 0.2 GB.

## 4. Software WebGL (MEASURED in page via `pipeline/render/diag/index.tsx`)
gl=swangle: WebGL 2.0 (OpenGL ES 3.0 Chromium); unmasked renderer `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`; MAX_TEXTURE_SIZE 8192, MAX_RENDERBUFFER 8192, MAX_VIEWPORT 8192x8192, max anisotropy 16, MSAA samples 4, 31 WebGL2 extensions, EXT_color_buffer_float yes. WebGL1 also available.
Chromium logs the deprecation "Automatic fallback to software WebGL ... use --enable-unsafe-swiftshader" (future Chromium may stop allowing this; watch on browser upgrade, INFERRED).
gl=angle, swiftshader, angle-egl: each re-tested once (diag composition): `getContext('webgl2')` and `('webgl')` both null. Claim from A25 CONFIRMED for this browser/container.
8192 px texture cap suffices for 1080x1920 plates and 4K stills (not tested at that size).

## 5. Encode check (MEASURED, ffprobe 6.1.1, `out/a26/mp4/noaudio.mp4`)
codec h264 High, pix_fmt yuv420p, 360x640, r_frame_rate = avg_frame_rate = 24/1, nb_frames 48 (counted 48), duration 2.000000 s; bit rate 445 kbps (112 KB). color_range tv, color_primaries bt709, color_transfer iec61966-2-1 (sRGB tag), **color_space (matrix) unknown/untagged**. `frame_count_ok` = true.
Risk (INFERRED, medium): untagged matrix with sRGB transfer may be decoded as BT.601 by some players at SD sizes, shifting colours. Recommend explicit `colorSpace` option / ffmpeg tags (bt709 matrix) in the final profile, verified by a colour-patch test. Not changed here (dev only).

## 6. Audio (MEASURED)
A25 `EngineTest` supports `audio` prop (public-relative path, `<Audio src=staticFile>`); harness `mp4 --audio` generates the 0.25 s 440 Hz synthetic WAV into the git-ignored public dir (`test/tone.wav`) and passes it. Result `out/a26/mp4/audio.mp4`: video unchanged (h264, 48 frames), plus AAC LC 48 kHz stereo, 2.005 s (audio is 5 ms longer than video), 317 kbps. ffmpeg volumedetect: mean -27.3 dB, max -15.2 dB (non-silent). The 0.25 s tone is mounted without `<Sequence>`, so only the first 0.25 s carry sound. Real narration and loudness validation (-14 LUFS) untested here.

## 7. Repo hygiene (MEASURED)
`git status --short`: only untracked `pipeline/render/` and `knowledge/engineering/a26-rendering-performance-engineer/` (text/scripts). `git ls-files` contains 0 png/mp4/wav. `out/` and `assets/private/` are ignored (`git check-ignore` incl. the linked plate path).

## Commands
`R="node --experimental-strip-types --no-warnings pipeline/render/render.ts"`
`$R prepare` | `$R still --frame 24 --out out/a26/d/s1.png` | `$R stills --frames 24,24,0,0,17,17,47,47,24,24 --outdir out/a26/inproc` | `$R seq --concurrency 4 --outdir out/a26/seq_c4` | `$R mp4 --concurrency 4 [--audio] --out out/a26/mp4/x.mp4` | `$R prepare --entry pipeline/render/diag/index.tsx --name diag --noplate; $R diag --bundle out/a26/diag --id Diag --gl <mode>`.

## Limitations
Single machine, single scene; determinism proven only for this browser build and flags. Timings dominated by Chromium start and PNG encode for a trivial scene. MP4 timing n=1-2. Memory sampler is polled (150 ms) so true peaks may be slightly higher. No GPU measurement exists (docs: GPU options remain a user decision; software timings must not be extrapolated). The sampler's own overhead may explain in-process stills being slightly slower than fresh ones.
