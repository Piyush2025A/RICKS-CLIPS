# COLOUR_5A — BT.709 correction of the MP4 encode (Phase 5A, user-approved)
Script version a26-render-v1 (+colour patch). Remotion 4.0.547, ffmpeg 6.1.1 (system, zscale present), same container (software WebGL2).

## Finding (MEASURED, high)
Legacy encode (Remotion v4 `colorSpace` unset = `default`) tagged range tv / primaries bt709 / transfer iec61966-2-1, matrix unknown, and did NO matrix filter: swscale used its default **BT.601** RGB->YCbCr. Decoding it as BT.709 (what players assume for 360x640 only if tagged/HD) gives errors up to 40 levels (pure green); the file is only self-consistent if read as BT.601.

## Setting used (default in render.ts mp4 mode; flag `--colorspace default` reproduces legacy for contrast only)
`renderMedia({ colorSpace: 'bt709', pixelFormat: 'yuv420p', codec: 'h264', crf: 18 })`. Source (node_modules/@remotion/renderer/dist/ffmpeg-args.js): adds `-colorspace:v bt709 -color_primaries:v bt709 -color_trc:v bt709 -color_range tv` AND `-vf zscale=matrix=709:range=limited:primariesin=709:primaries=709:transferin=709:transfer=709`, i.e. tags and the actual RGB->YCbCr conversion both BT.709 limited. No separate FFmpeg remux needed. transfer tag is bt709 (not sRGB): pixel values are NOT transfer-converted (transferin=transfer), so sRGB-encoded pixels are stored as-is; bt709 is the conventional tag players expect (sRGB-vs-709 gamma difference is a known, accepted display nuance; INFERRED).

## ffprobe tags (MEASURED)
Patches and EngineTest MP4: h264, yuv420p, color_range=tv, color_space=bt709, color_primaries=bt709, color_transfer=bt709. Legacy: tv / unknown / bt709 / iec61966-2-1.

## Colour-patch test
Composition `Patches` (`pipeline/render/colour/index.tsx`): 14 flat CSS cells (2x7, 180x91 px), 360x640, 24 fps, 6 frames; cell 13 is a raw WebGL2 canvas (clear colour) of the same skin tone as cells 6 and 12. Measure: `.venv-analysis/bin/python pipeline/render/colour/measure.py <mp4> 3` (frame 3, central 40% of each cell, ffmpeg `scale=in_color_matrix=<m>:in_range=tv:out_range=pc,format=rgb24`; 709 vs smpte170m(601)). Source sRGB values listed in the script. n=14 patches, 1 frame (patches are static; single frame sufficient).

| MP4 | read as | max abs err R / G / B (levels) | worst patch |
|---|---|---|---|
| corrected (bt709) | BT.709 | 1 / 2 / 1 | 2 (skin-dark 141,85,36 G) |
| corrected (bt709) | BT.601 (wrong) | 23 / 5 / 12 | 23 (pure red) |
| legacy (default) | BT.709 | 7 / 40 / 4 | 40 (pure green) |
| legacy (default) | BT.601 | 2 / 2 / 2 | 2 |

Neutrals (0, 32, 128, 200, 255) exact under either matrix (matrix only affects chroma). Y' plane (raw, no conversion): black 16, white 235, grey128 126 (limited-range OK). WebGL patch (cell 13) = CSS patches (cells 6, 12): identical centre (223,171,137), so the canvas output path matches DOM colour (tested raw WebGL2 clear, not a Three.js lit material; Three.js colour management/tone mapping is A25's scope).
Expected 4:2:0 + quantisation error ≤2-3 levels: met (max 2).

## EngineTest re-render (MEASURED)
`render.ts mp4 --concurrency 4 [--audio]`: 360x640, 24/1, nb_read_frames 48, tags as above; with `--audio` AAC stream present. Determinism: two renders each of audio (sha f01d9898…2033), no-audio and Patches (4b0a2dd1…cc2cd) gave identical hashes. Plate SHA-256 unchanged (bd4fac1d…) after every run.
No-audio EngineTest sha256 (2 runs identical): 11b4de32147e907e5cf575259bafe95f135aed36008f82e881b59c6c55f1a38c.

## Limitations
Matrix/range verified with ffmpeg decode (swscale), not with browser/phone players (not tested). Chroma subsampling errors only measured at patch centres; edges and fine saturated detail will bleed (inherent 4:2:0). Transfer tag choice bt709 vs sRGB not display-tested. Determinism holds for this browser/ffmpeg build and concurrency 4 only. Timing n=1 per run (not a benchmark; zscale cost not isolated). Frame 3 only used for patch values.
