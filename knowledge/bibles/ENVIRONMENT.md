# Environment design bible (draft v0.1)
Sources: a05 (F-A05-*), a06 (F-A06-*), a07 (F-A07-*), a08 (F-A08-*).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| W1 | Worlds are real perspective 3D (parallax, occlusion, VP rotation) — never fake moves on flat plates | — | F-A05-001, F-A06-003/005 | H |
| W2 | Two art treatments share one construction | A: lit PBR, no scenery ink (01–07, 09, 26, 27…); B: outlined painterly scenery (15–21, 25, 29, 30); hybrids exist | F-A05-004, F-A09-010, F-a10-004, F-A08-010 | M |
| W3 | Location taxonomy | interiors, wide exteriors, cutaway slabs, macro hero objects, inner-body/abstract, flat diagram planes in world | F-A05-003, F-A05-009/010 | H |
| W4 | Locations per video | ≈ 5–6 per 40 s, hub sets revisited with new angle/time of day | F-A05-003, F-A09-007 | M |
| W5 | Depth structure | continuous gradient, 3 visual bands (fg/mid/far); near/far speed ratio median 3.8 | F-A06-003/004 | M |
| W6 | Foreground framing and occlusion constantly used | frame-in-frame ≥ 16/30 videos | F-A07-008, F-a14-006 | M |
| W7 | Depth of field is a minority look | ≈ 22 % of frames soft; close-ups 71 %, wides 8 % | F-A07-001 | M |
| W8 | Haze = colour shift toward sky (not contrast loss) | far ground ≈ 0.55 of near-ground ΔE from sky | F-A07-006 | L |
| W9 | Camera height / horizon | eye-level 64 %, high 20 %, low 16 %; horizon ≈ 38 % from top; wide lens feel | F-A07-004/005/007 | M |
| W10 | Props: chunky, bevelled, oversized toys; detail only on the story face | hero ×1.5–3; 1 macro hero prop per beat; 3–6 dressing props per set | F-A08-001/002, F-A05-005 | M–H |
| W11 | Textures painted, not photographic; energy only on organic materials | speckle 3–6 L* on rock/earth; flat fills for man-made | F-A08-003/004 | M |
| W12 | In-world text carries the story gap | signs, counters, documents as world planes; beat text ≥ 35 px cap height | F-A05-008, F-A06-006, F-A08-007/008, F-a19-004 | M |
| W13 | Dense fg+mid, calm back plane; instanced repetition + DOF falloff for density | — | F-A05-006 | M |
Implementation: A05 TECHNIQUES (shot-type geometry vs plate table, set budget, scale table, asset list, Flow prompt template);
A08 TECHNIQUES (material presets, typography); A25 module M-world. Production default (proposal): ≤ 6 reusable sets per
Short (F-a17-009). User decision pending: treatment A or B for our first production (A25 open question).
