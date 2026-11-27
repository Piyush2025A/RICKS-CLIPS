# Character design bible (draft v0.1)
Sources: knowledge/character/a01 (F-a01-*), a03 (F-a03-*), a10 (F-a10-001..003), a06 (F-A06-001/007), a09 (F-A09-008).
| # | Rule (craft) | Value / spec | Evidence | Conf |
|---|---|---|---|---|
| C1 | Characters are flat 2D ink-outlined cut-outs placed in a lit 3D world | billboard cards, depth-tested against 3D props | F-a01-001, F-A06-001, F-A05-001 | H |
| C2 | Simple geometric construction | oval/round head, pill torso, single-stroke limbs, ball hands, feet minimal | F-a01-001, F-a03-008 | H |
| C3 | Head proportions | head H/W ≈ 0.93 (IQR 0.89–0.98, n = 12); face w:h 1.10–1.26 (A01, face region) — measure on our own designs | F-a03-001, F-a01-002 | L–M |
| C4 | Overall height | ≈ 3 head widths (n = 8); legs ≈ 1.2 HW (A03) — A01's 2–3× torso estimate contradicted, A03 preferred (measured) | F-a03-002/004 | L |
| C5 | Archetypes by silhouette | slim (default), stout, tall-pin, child (40–60 %) + prop-as-character | F-a01-003, F-a03-005 | M |
| C6 | Identity hierarchy | torso hue (primary) → headgear/hair silhouette → one tertiary mark (glasses/facial hair/prop) | F-a01-006/007 | M–H |
| C7 | Palette per character | ≤ 6 colours; ≥ 60° hue spacing between co-present characters; near-white faces | F-a01-006, T-a01-01 | M |
| C8 | Ink line | baked into the card art, ≈ 3.6 % of head width (≈ 10 px at 1080 for a ~300 px head), near-black with small tint (L* < 10) | F-a10-001/002/003, F-a01-004 | M |
| C9 | Lighting response | faces take scene tint but stay readable (L* ≥ 85); card shade floor ≈ 0.36 | F-A09-008, F-A09-002, F-a01-005 | M |
| C10 | Consistency | constant: head shape, hat/hair silhouette, torso hue family, outline weight; variable: tint, scale, expression | F-a01-011, F-a03-006 | H |
| C11 | Crowds | same construction at tiny scale, dot faces, rotating palette | F-a01-009, T-a01-03 | M |
Originality (required): our cast must NOT reuse the reference's exact combination (white oval head + dot eyes + pill torso
+ uniform stick limbs). Candidate own signature (HYPOTHESIS, needs user approval): rounded-square heads, tapered limbs,
mitten hands, indigo ink (T-a01-02).
Implementation: Google Flow character sheets per T-a01-02 (front/¾/side/back, flat fills, ink baked, neutral grey bg);
Three.js card per T-a10-001 (alphaTest, hard premultiplied edge, A09 card-lighting uniforms).
Open: A03 child archetype and stroke thickness; exact silhouettes measured on 7 videos only.
