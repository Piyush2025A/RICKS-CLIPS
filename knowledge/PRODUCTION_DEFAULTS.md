# Production defaults (Phase 4 onward) — v1, 2026-11-28 (D033)
The current production reference is **`knowledge/STYLE_BIBLE.md` v0.3** with the nine department bibles in
`knowledge/bibles/` (v0.3), each with its stated confidence and limitations. Measured reference statistics are
**initial production targets** for comparable craft — starting points to test against our own renders, not universally
mandatory rules. Where an older specialist TECHNIQUES file, engineering document or plan disagrees with this list,
this list and the v0.3 bibles win; historical research records and superseded findings stay in place for traceability.

| Topic | Production default | Evidence (bible / finding) |
|---|---|---|
| Caption lead | caption appears **≈ 140 ms before** the word's voice onset (≈ 4 f at 30 fps, ≈ 3 f at 24); one token at a time, centre 0.703 H, never blank between words; the old ~70 ms / "2 frames" is superseded | AUDIO A4, F-A20-104, AUDIT_3B |
| Crossfade | default **7 frames at 30 fps ≈ 0.233 s** (typical 6–8 f); other rates convert **by time**: frames = round(0.2333 × fps) → **6 f at 24 fps**; 79 % of joins | EDITING T1–T2, F-a15-101, AUDIT_3B #3 |
| Facial expressions | swaps placed on **story beats** (hard swaps, ≈ 5 f holds, 11–30 f between bursts); **not** mandatory word-triggered swaps; no lip-sync for narration | EXPRESSION E3–E5, F-A02-101..103 |
| Character shading | **smooth soft gradients** on cards, hard highlight streaks allowed; **no mandatory toon bands** (toon ramps only as an optional experiment) | CHARACTER C10, F-a01-102, A10 |
| Character cast shadows | **off by default**; enable per scene when the shot calls for it (hard card shadows in 4/30 reference videos) | LIGHTING L3, F-A09-101 |
| Background music | **static bed** as the initial default; **−20 dB (±3) relative to narration in the 400–2000 Hz speech band**; no sidechain ducking by default (≤ 1 dB if ever needed) | AUDIO A5–A6, F-a21-100, F-A22-100..102 |
| Character ink | **baked into the character artwork** (≈ 3.7 % of head width, very dark aubergine/brown-black), **scaling with character size**; no constant-width screen-space outline on cards | CHARACTER C9, F-a10-101..104 |
| Narration pace | ≈ 220 wpm initial target (sentences ≈ 11 words) | STORY S10, F-A20-101 |
| Camera push | ≈ +24 % total scale over ≈ 33 f (30 fps), smoothstep easing | CAMERA K3–K4, F-a13-100..102 |
| Grade | black p1 ≈ 0.07, soft roll-off, vignette ≈ 0.70, no grain/CA | LIGHTING L10, L12 |
| Development renders | 360 × 640, 24 fps (convert every frame count by time) | CLAUDE.md rule 6 |
| Dataset identity | RC30 keys + SHA-256 are the identity for evidence; video IDs, publication dates and URLs are **deferred metadata** (`knowledge/dataset/IDENTITY.json`, D028); order by user attestation | D028 |

Frame-count conversion rule: every duration defined at 30 fps is converted by time (`round(seconds × fps)`), never by
copying the frame number.
