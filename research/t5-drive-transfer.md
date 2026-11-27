# T5 — Google Drive binary transfer test (2026-11-27)

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
- Not yet verified: Drive → user's computer and user's computer → Drive → cloud (needs the user, see below).

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
