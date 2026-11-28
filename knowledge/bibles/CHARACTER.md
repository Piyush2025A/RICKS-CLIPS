# Character design bible (draft v0.3, Phase 3B)
Sources: knowledge/character/a01 (F-a01-*, 3B F-a01-100..110), a03 (F-a03-*, 3B F-a03-101..106), a10 (F-a10-001..003,
3B F-a10-101..104), a06 (F-A06-001/007), a09 (F-A09-008, 3B F-A09-104). Audits: AUDIT.md, AUDIT_3B.md.
| # | Rule (craft) | Value / spec | Evidence | Conf |
|---|---|---|---|---|
| C1 | Characters are flat 2D ink-outlined cut-outs placed in a lit 3D world | billboard cards, depth-tested against 3D props | F-a01-001, F-A06-001, F-A05-001; outlined in 30/30 videos (F-a10-102) | H |
| C2 | Simple geometric construction | round head, pill torso, single-stroke limbs, **ball hands without fingers** (22/22 natives; exception RC30-23 gauntlet), minimal feet | F-a01-001, F-a01-106, F-a03-008 | H |
| C3 | Head proportions | head H/W **0.933** (IQR 0.889–0.980; n = 34 characters, 19 videos; A28 VERIFIED) | F-a03-101 (supersedes F-a03-001) | M |
| C4 | Overall height and limbs | height ≈ **3.27 head heights** (= 3.04 HW; IQR 3.09–3.47 HH, n = 28, 16 videos); leg ≈ 1.23 HW; **leg/torso 1.38** (IQR 1.26–1.51, n = 54, 23 videos); torso width 0.70 HW (n = 60); leg stroke 0.053 HW. A01's old "legs 2–3× torso" SUPERSEDED (A01 now 1.2–1.5×). H-UP "3.5 HH" sits above Q3 → not adopted | F-a03-102..104, F-a01-104 | M |
| C5 | Archetypes by silhouette | slim adult default (n = 48); large/stout, tall, robed; child rare (n = 1 measured, legs ≈ 0.6 HW); animals in 11/30 videos, object/organ characters in 5/30 (not measured) | F-a01-003/100/109, F-a03-105 | M (adults) / L (others) |
| C6 | Identity hierarchy | torso hue → headgear/hair silhouette (headgear in 27/30 videos, glasses 15/30) → one tertiary mark | F-a01-006/007/100 | M–H |
| C7 | Cast per video | median **7 distinct characters** (IQR 5–8); crowds in 17/30 | F-a01-100 (census from 1 overview sheet per video) | M |
| C8 | Palette per character | ≤ 6 colours; ≥ 60° hue spacing between co-present characters; near-white faces | F-a01-006, T-a01-01 | M |
| C9 | Ink line | baked into the card art; **9.3 px at 1080** (IQR 6.9–12.1) = **3.68 % of head width** (IQR 2.7–4.9 %; 80 heads, 26 videos; A28 VERIFIED, eye check ±1.5 px); colour very dark aubergine/brown-black, not pure black; one colour per character (some warm dark brown: 02, 27, 30); line **scales with the card** (log-log slope ≈ 0.55 in push-ins), not a constant screen width; thin-line exceptions 19, 28, 29 (0.7–1.4 % HW, cause open) | F-a10-101/103/104, F-a01-105 | M |
| C10 | Shading on cards | **soft gradient shading present** (22/22 natives) + hard highlight streaks on hair/hats (≥ 8/22) — the earlier "flat" wording is SUPERSEDED; no cel bands | F-a01-102 | M |
| C11 | Lighting response | cards take scene light: tinted/darkened in ≈ 12/16 shots, near-white in ≈ 4; no coloured rim | F-A09-104 (supersedes "almost exempt", F-A09-008) | L–M |
| C12 | Eyes | five eye types; resting face more often a **dash under a brow** (≈ 14/22) than a dot | F-a01-103 | M |
| C13 | Cast shadows | per-scene switch, default OFF (hard card shadows in 4/30 videos) — see LIGHTING L3 | F-A09-101, F-a01-107 | M |
| C14 | Consistency | constant: head shape, hat/hair silhouette, torso hue family, outline weight relative to head; variable: tint, scale, expression | F-a01-011, F-a03-006 | H |
| C15 | Crowds | same construction at tiny scale, dot faces, rotating palette | F-a01-009, T-a01-03 | M |
Originality (required): genre-level constants (round head, ball hands, ink baked into cards, ≈ 3 HW height) may be
shared; the reference's exact combination (white round head + dash/dot eyes under brows + pill torso + uniform stick limbs
+ its costume palette) must not be reproduced. Candidate own signature (HYPOTHESIS, needs user approval): rounded-square
heads, tapered limbs, mitten hands, indigo ink (T-a01-02, F-a01-110 safe-vs-copy-risk split).
Implementation: Google Flow character sheets per T-a01-02/04..07 (front/¾/side/back, soft gradient fills, ink baked at
3.7 % HW, neutral grey bg); Three.js card per T-a10-001 (alphaTest, premultiplied edge, A09 card-lighting uniforms; ink
scales with card).
Open: child/animal/object proportions; eye spacing and arm length (not measured); palette k-means; 64 px readability test.
