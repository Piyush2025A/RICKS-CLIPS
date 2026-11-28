# Lighting & shader bible (draft v0.3, Phase 3B)
Sources: a09 (F-A09-*, 3B F-A09-101..105), a10 (F-a10-*, 3B F-a10-101..104), a11 (F-a11-*, 3B F-a11-101..108),
a12 (F-a12-*, 3B F-a12-100..104), a25 conflicts. Audits: AUDIT.md #13/#14, AUDIT_3B.md #14/#15.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| L1 | Key + hemisphere rig; deep shadows | shade/lit Y median **0.14** (IQR 0.11–0.255) ≈ 7:1 (n = 15 pairs, 7 videos; grade lifts blacks, true ratio probably deeper) | F-A09-102 (extends F-A09-002) | L–M |
| L2 | Shadows take the sky/fill hue; warm key + cool shadow is the common pairing (≈ 15 videos) | Δb* −8…−75 (violet on warm light down to −67) | F-A09-003/102/103, F-a11-005 | M |
| L3 | **Card cast shadows: per-scene switch, default OFF** | hard card floor shadows in **4/30** videos (01, 09, 14, 28), ambiguous 2, none 24; not predicted by sunlight (exteriors 04, 06, 07, 10, 13 have none) or by video index; can flip inside a video (14: none at f370, huge at f908); weak predictor: lit-3D treatment | F-A09-101 (30/30), A28 #13 | M |
| L4 | Shadow edges mostly hard | 10–90 % ≈ 11 px at 1080; PCFSoft radius 2–4, 2048 map | F-A09-004 | L–M |
| L5 | Mood presets; night/dark states common | 10 measured classes; night/dark in 17 videos, practical lights in ≈ 20; key elevation mostly 20–45° | F-A09-006/103 | L–M |
| L6 | Re-light by beat via cut/crossfade between hub states | day/dusk/night | F-A09-007 | M |
| L7 | Practicals with pools + bloom; no coloured rim light on cards (outline separates) | — | F-A09-009/011/104, F-a10-010 | M |
| L8 | Shading model: smooth lit gradients, no cel bands, no film grain, no chromatic aberration | grain ≤ codec noise; CA 0.00 px | F-a10-006/007/008/009 | M–H |
| L9 | Ink: character ink baked (**9.3 px / 3.68 % HW**, scales with the card); world/prop ink only in the scenery-ink treatment (B, 6/30 videos) via depth/normal Sobel | — | F-a10-101..104 (A28 VERIFIED) | M |
| L10 | Grade: **one grade for all treatments**; lifted blacks, soft roll-off, no S-curve | native per-video **p1 0.071** (18/255; IQR 0.04–0.10), p5 0.125, p99 0.96 (8-bit after limited→full expansion, v = code/255); black floor tracks exposure (≈ 0.03 dark, 0.075 mid, 0.10 bright shots); only 0.1 % of pixels at 255; no treatment difference (permutation p ≥ 0.13, low power). 3A "0.099 / 0.09–0.12" SUPERSEDED | F-a11-101..104 (A28 VERIFIED) | H (levels) / M (one grade) |
| L11 | Hue axis orange/yellow vs blue/violet; teal almost absent; no hero-vs-bg saturation boost | — | F-a11-006/008 | M |
| L12 | Vignette mild and constant | native corner/centre ≈ **0.70**, same in all treatments | F-a11-104 | M |
| L13 | Shot-to-shot colour steps | across 568 confirmed transitions median ΔE 15–21; black/white points move only ≈ 0.025/0.035 | F-a11-105 | M |
| L14 | VFX glows/flashes | no white-overlay flash found; luma "bumps" from effects: n = 80 in 27 videos, median +15.8 luma, rate **0.45 per 10 s** (supersedes 1.3/10 s), duration varies widely (IQR 3–22 f — no fixed length); lightning and 1-frame muzzle bursts exist (3A "no flashes" partly superseded) | F-a12-100..104 (A28 VERIFIED arithmetic) | M |
Post stack (A25 resolution): RenderPass → outline (treatment B only) → AO → DOF → Bloom (threshold ≈ 0.85–0.9, untested)
→ tonemap → grade → vignette (0.70) → output. Implementation: A09 TECHNIQUES preset table; A10 T-a10-001..003 + 3B
updates; A11 recipes T0–T10 + `src/grade/qc_grade.py`; A12 library E01–E25.
Open: key azimuth distribution; per-video fill ratio on ≥ 15 videos; whether card shading is baked or lit; per-mood grade
targets on per-frame labels; hero-object chroma; true tone curve.
