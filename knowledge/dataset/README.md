# RC30 — frozen reference dataset (permanent rule)

Owner: director. Approved by the user on 2026-11-27 (Phase 1 review).

## Rule
- Primary reference channel: https://www.youtube.com/@RicksClips3000
- The dataset is **exactly the 30 most recently published Shorts** on that channel, ordered by **publication date**
  (not popularity), determined once at the start of Phase 3 and then **frozen**.
- No older Shorts outside the dataset are ever analysed. Unavailable references are **not substituted**; they are
  recorded as `unavailable` and the analysis reports n < 30.
- `MANIFEST.json` (schema: `../_system/schemas/dataset-manifest.schema.json`) records for all 30: video ID, title,
  publication date, duration, source URL, metadata source, and — after authorised acquisition — media checksums and
  ffprobe stream metadata. Its SHA-256 is quoted by every finding.
- Footage is acquired **only through a method the user has authorised** and stored privately outside the repository
  (or in git-ignored `private/`). Video, frames, crops and sheets are never committed.
- Every native frame is processed computationally without skipping; for 30 fps footage every frame is accounted for.
  Computational and visual-inspection coverage are recorded separately (`coverage/computational/`, `coverage/visual/`).
- Analysis covers picture and sound: narration, sound effects, music, editing and synchronisation.
- Upstream repository reports are supplementary hypotheses (`H-UP`), never evidence.

## Frame IDs
`RC30-<nn>-f<NNNNNN>`: `nn` = 01 (newest) … 30 (oldest) at freeze time; `NNNNNN` = zero-based decode index at the
native frame rate; every record also stores ffprobe `pts_time`. See `../_system/EVIDENCE.md`.

## Status
Not yet frozen. `MANIFEST.json` is created at the start of Phase 3, after user approval.
