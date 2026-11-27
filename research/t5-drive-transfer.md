# T5 — Google Drive binary transfer test (2026-11-27) — COMPLETE

Method: official Google Drive connector in a claude.ai/code cloud session. Synthetic files only, generated in the
session scratchpad (never committed). Private Drive folder `ricks-clips-t5` (My Drive, created by this test, no sharing
change; folder ID `1_DwW1oQX74ufdr1ishfDes8S06zQkQXq`). Upload = `create_file` with a file reference
(`sha256:<hex>:<path>`) and `disableConversionToGoogleType: true`. Download = `download_file_content`.

## Results (cloud → Drive → cloud)
| Size class | Files | Upload | Drive size/MIME | Download to cloud FS | SHA-256 |
|---|---|---|---|---|---|
| small (1.3–9.6 KB) | PNG, WAV, MP4, ZIP | 4/4 ok, ~4.8 s for 4 calls | exact bytes, MIME kept | 4/4 saved as files in the session's `tool-results/` dir | 4/4 MATCH |
| ~1 MB (1.00–1.05 MB) | PNG, WAV, MP4, ZIP | 4/4 ok, ~6.3 s for 4 calls | exact bytes, MIME kept | 4/4 saved as files, ~5 s for 4 calls | 4/4 MATCH |
| ~5 MB (5.0–5.8 MB) | PNG, WAV, MP4, ZIP | **0/4: refused before sending** | — | not tested | — |
| ~20 MB | — | not attempted (stopped after the 5 MB failure) | — | — | — |

Exact error for every 5 MB upload: "This request is over the 4.2 MB limit on each connector call from this session, so
nothing was sent ... That limit leaves room for about 3.1 MB of files carried in the request. Retrying won't help."
Timings are wall-clock between shell timestamps around batches of tool calls, so they include orchestration overhead.

## Findings
- **Byte-exact both ways up to ~1 MB, VERIFIED** for PNG, WAV, MP4 and ZIP (16/16 checksum matches).
- **No base64 in the conversation.** Uploads stream the referenced file; downloads are written to
  `~/.claude/projects/<project>/<session>/tool-results/mcp-Google_Drive-blob-*.<ext>` and the conversation only gets a
  one-line note. Exception: PNG/JPEG downloads are also shown as an inline image preview (context cost of one image).
- **Upload limit, VERIFIED:** 4.2 MB per connector call, about 3.1 MB of file content. Larger files cannot be
  uploaded from the cloud through this connector.
- **Download limit: UNVERIFIED.** Downloads of 1 MB worked; the 5 MB and 20 MB downloads could not be tested because
  the files could not be uploaded from the cloud. A user-uploaded 5 MB / 20 MB file would test this direction.
- Cost: no additional subscription or API charge was incurred (connector already attached; Drive storage only).
- Drive → user's computer: **VERIFIED by the user** (2026-11-27): all 8 files downloaded on Linux Mint, 8/8 SHA-256 match.

## Final verification: user's computer → Drive → cloud (2026-11-27)
User generated two random files locally, uploaded them in the browser to `ricks-clips-t5` and reported size + SHA-256.
| File | Bytes | Download to cloud | Time | SHA-256 |
|---|---|---|---|---|
| `t5-local-5MB.bin` | 5,000,000 | ok, saved as file (`tool-results/`) | ~1.6 s | `36cba767…46420` **MATCH** |
| `t5-local-20MB.bin` | 20,000,000 | **refused**: "over Google's 10 MB limit for downloads through this connector ... Trying again won't help." | — | not tested |
Note: Drive reports `canTrash: false` / `canMoveItemWithinDrive: false` for these two browser-uploaded files from the
connector; only the user can trash or move them (in Drive).

## Verified connector limits (cloud session)
| Direction | Limit per file | Evidence |
|---|---|---|
| cloud → Drive (upload) | ~3.1 MB of file content (4.2 MB per connector call) | 1 MB ok ×4; 5.0–5.8 MB refused ×4 |
| Drive → cloud (download) | 10 MB (Google's limit for this connector) | 5 MB ok; 20 MB refused |
| Drive ↔ user's computer (browser) | not limited by the connector | 8 files + 5 MB + 20 MB worked |
Integrity: every transfer that completed was byte-exact (16 cloud round trips + 8 local + 1 inbound = 25/25).

## Suitability as the permanent private media-transfer layer
- **Suitable for small assets, VERIFIED within limits:** Flow stills (the D015 PNG is 768 × 1376; typical PNGs at that
  size are well under 10 MB — INFERRED, check per asset), reference crops, audio stems, prompt/asset packs, and 360p/24 fps
  development previews of a few seconds into the cloud (≤ 10 MB) and out of it (≤ ~3.1 MB).
- **Not suitable alone for large files:** finished renders (e.g. a 60 s 1080p MP4 is typically tens of MB) exceed both
  limits. Private, no extra cost, no public links, byte-exact; manual browser step on the user's side.

## Recommendation for larger cloud-rendered videos (proposed, needs approval)
1. **Render finals on the user's computer (preferred).** The cloud session commits only source (scene code, EDL, audio
   cues, manifests: text) to git; the local session pulls and renders at full resolution next to the local assets.
   Pixels never need to leave the cloud. Needs the render toolchain (Node/Remotion, FFmpeg) installed locally later.
2. **Cloud renders stay small for review:** keep development renders at 360p/24 fps (CLAUDE.md rule 6) and short; send
   ≤ ~3 MB previews to Drive directly.
3. **Chunked transfer as fallback:** split a larger file into ≤ 3 MB parts plus a SHA-256 manifest, upload each part,
   reassemble locally (`cat` + `sha256sum -c`). Works within the verified limits but costs one connector call per 3 MB
   (a 60 MB file ≈ 20 calls); not tested yet.
4. Not recommended now: paid object storage (billing, secret management), GitHub (public repo), public tunnels.


## Expected checksums for local verification
| File | Bytes | SHA-256 |
|---|---|---|
| `t5-small.mp4` | 2219 | `1424c2630e8c1e3a3525e7f707e9353476d046b73167242d8c6f5da1c4ee7a26` |
| `t5-small.png` | 1276 | `43a4a98d0f6f08525ea40a214c31aeda015820527013be801e61f4d2d72b048f` |
| `t5-small.wav` | 9644 | `bab730c9c9e3d9702cdadc70effbb51063b8119df402b72efe89c34500f2d43f` |
| `t5-small.zip` | 1524 | `7217e02a8275ba9c7a32d96fc1974e14da770eb5f67a81122ed21e649767b22f` |
| `t5-1mb.mp4` | 1046500 | `d2d1803c9b0933b1f6325c567610900b48bd36053b7bf9611f794347ba924946` |
| `t5-1mb.png` | 1000781 | `c39ddadaa096d1cdb8c340bd9dc0c224c00053b4dd3ce6b9dbc00a4680f66f71` |
| `t5-1mb.wav` | 1000044 | `1f4d18e7b083af01480af207ab37fed50ffa5ad23c576a800d6784a87aa285b0` |
| `t5-1mb.zip` | 1000116 | `51a11e41594226df22a474a49c90c3992e47e49bdca6713fefcc51493e80952f` |

Files in the folder that were never uploaded: none (the 5 MB set was refused before sending).
