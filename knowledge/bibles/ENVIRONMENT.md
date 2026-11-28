# Environment design bible (draft v0.3, Phase 3B)
Sources: a05 (F-A05-*), a06 (F-A06-*), a07 (F-A07-*, 3B F-a07-100..105), a08 (F-A08-*, 3B F-A08-101..107),
a10 (3B F-a10-102), a09 (3B F-A09-105). Audits: AUDIT.md, AUDIT_3B.md (#17, A09/A10 split).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| W1 | Worlds are real perspective 3D (parallax, occlusion, VP rotation); props are real 3D assets — flat cards only for panels, UI, photos mounted on meshes | — | F-A05-001, F-A06-003/005, F-A08-101 | H |
| W2 | **Scenery ink is a per-video switch (axis 1)** | no scenery/prop ink in **20/30** (A); scenery ink in **6** (B: 16, 19, 20, 23, 25, 29); mixed 4 (09, 15, 17, 28); props in 19/28 can carry thick ink (8–12 px). A08's "no ink on props" (14 natives) and the 3A "thick ink" claim sampled different videos — both right | F-a10-102 (A28: supported on 18/24/30), F-A08-103 | M (1–2 frames/video) |
| W3 | **Light rendering is a separate axis (axis 2)** | lit-3D vs painted/illustrated light; A09's split (lit-3D 01–14, 22, 27; illustrated 15–20, 23–25, 29, 30; mixed 02, 11, 21, 26, 28) is low confidence: internally inconsistent (02, 11 in two groups) and its "illustrated ⇒ inked props" coupling is NOT SUPPORTED (A28) | F-A09-105, AUDIT_3B | L |
| W4 | Location taxonomy | interiors, wide exteriors, cutaway slabs, macro hero objects, inner-body/abstract, flat diagram planes in world | F-A05-003, F-A05-009/010 | H |
| W5 | Locations per video | ≈ 5–6 per 40 s, hub sets revisited with new angle/time of day | F-A05-003, F-A09-007 | M |
| W6 | Depth structure / parallax | two regimes: lock-off drifts move as one plate (top/bottom displacement ratio ≈ 0.85); dolly/orbit moves are layered (ratio ≈ 0.48). Three.js stack for orbit/dolly: near 0.5–2 m / subject 3–6 m / far ≥ 20 m | F-a07-103 (32 pairs, 10 videos), F-A06-003/004 | M |
| W7 | Foreground framing and occlusion constantly used | frame-in-frame ≥ 16/30 videos | F-A07-008, F-a14-006 | M |
| W8 | Depth of field is a minority look, modest blur | in-focus edges 1.0–1.7 px; frames with a cell ≥ 2.5 px blur **9.1 %** (581 natives, 30 videos; metric upper bound, confounded by flat/hazy areas); added blur sigma ≈ **3.6 px** (shallow bg), 3.9 (shallow fg), ≥ 4.0 (macro) at 1080 — 3A "6–12 px" too high. 3A visual "22 % soft" kept as a recorded contradiction (tile over-call) | F-a07-100..102, F-A07-001, AUDIT_3B #17 | L–M |
| W9 | Haze = colour shift toward sky (not contrast loss) | far ground ≈ 0.55 of near-ground ΔE from sky (9 frames, 6 videos; not re-measured) | F-A07-006 | L |
| W10 | Camera height / horizon / lens | eye-level 64 %, high 20 %, low 16 %; horizon ≈ 38 % from top; vertical FOV ≈ **73°** (13 frames, 7 videos) | F-A07-004/005/007, F-a07-104 | L–M |
| W11 | Props: chunky, bevelled, oversized; detail only on the story face | median **3 hero props per video**; signs/boards/documents in 20/20 viewed videos, counters ≈ 11 | F-A08-001/002/102, F-A05-005 | M |
| W12 | Textures painted, mostly flat | grain only on grass (local std 3–12 L*), gravel (4–10), lattice; wood, paint, sand, dirt, floors, sky flat (std ≤ 0.8); clapboard seams 5–6 px | F-A08-104..106 (31 patches, 14 videos) | M |
| W13 | In-world text and screens carry the story gap | signs/counters/documents as world planes; screens/UI/lens inserts in ≥ 11/29 videos (three builds; the RC30-01 monitor is a flat 2D inset scene, INFERRED) | F-A05-008, F-A08-107, F-a19-004 | M |
| W14 | Dense fg+mid, calm back plane; instanced repetition + DOF falloff for density | — | F-A05-006 | M |
Implementation: A05 TECHNIQUES (shot-type geometry, set budget, scale table, Flow prompt template); A08 TECHNIQUES
(numeric Three.js material table: roughness/metalness/L*C*, texture sizes; T-A08-06 prop budget; T-A08-07 screen builds);
A07 TECHNIQUES (DOF/parallax/FOV parameters); A25 module M-world. **User decision pending:** scenery-ink treatment (A, the
majority, or B) for our first production; a joint 2-axis per-video label (A09 + A10) is still open.
Open: fabric/plastic/steel/glass albedo; texel density (not measurable from video); haze re-measure; manual vanishing points.
