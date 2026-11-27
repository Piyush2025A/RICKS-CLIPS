# Lighting & shader bible (draft v0.1)
Sources: a09 (F-A09-*), a10 (F-a10-*), a11 (F-a11-*), a12 (F-a12-*), a25 conflicts.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| L1 | Key + hemisphere rig; ambient ≈ 0.14 of key (shadow density 1:7) | shade/lit Y median 0.14 (n = 9) | F-A09-002 | M |
| L2 | Shadows take the sky/fill hue | Δb* −8…−75 depending on set; never neutralise in grade | F-A09-003, F-a11-005 | M |
| L3 | Card cast shadows only under a hard directional key; none in night/fire/illustrated | per-preset flag map / blob / none | F-A09-001 (resolves A01 vs A06), A25 C-resolution | M |
| L4 | Shadow edges mostly hard | 10–90 % ≈ 11 px at 1080; PCFSoft radius 2–4, 2048 map | F-A09-004 | L–M |
| L5 | Mood presets | 10 measured classes (L*a*b*), 3 per video median; warm+cool in 16/30 | F-A09-006, data/mood_classes.json | M |
| L6 | Re-light by beat via cut/6-frame crossfade between hub states | day/dusk/night | F-A09-007 | M |
| L7 | Practicals with pools + bloom; no rim light on cards (outline separates) | — | F-A09-009/011, F-a10-010 | M |
| L8 | Shading model: smooth lit gradients, no cel bands, no film grain, no chromatic aberration | grain ≤ codec noise; CA 0.00 px | F-a10-006/007/008/009 | M–H |
| L9 | Ink: character ink baked (≈ 3.6 % HW); world ink only in treatment B (≈ 2–3 px, no taper), via depth/normal Sobel | — | F-a10-001..005 | M |
| L10 | Grade: lifted blacks (no true black), soft highlights (p99 ≈ 0.94), compressed contrast, no S-curve | — | F-a11-001..004 | M |
| L11 | Hue axis orange/yellow vs blue/violet; teal almost absent; no hero-vs-bg saturation boost | — | F-a11-006/008 | M |
| L12 | Vignette mild in day, strong in low-key (comes from lighting) | corner/centre ≈ 0.73 (upper bound) | F-a11-009, F-a10-010 | L |
| L13 | VFX: hit effects cut in at full density then ease out; glows/rays additive; no screen flashes | E01–E18 library | F-a12-001..012 | L–M |
Post stack (A25 resolution): RenderPass → outline (B only) → AO → DOF → Bloom (threshold ≈ 0.85–0.9, untested) →
tonemap → grade → vignette → output. Implementation: A09 TECHNIQUES preset table; A10 T-a10-001..003; A11 grade recipes +
`src/grade/qc_grade.py`; A12 starter library.
