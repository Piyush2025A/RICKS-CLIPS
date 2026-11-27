# A09 FINDINGS — lighting & shadows (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A09.
(Written to disk verbatim by the director from A09's hand-off; the agent's Write tool refused the files.)
Visual ledger: 27 records (18 overview sheets at 180×320: 01–06, 09, 10, 12, 14, 15, 17, 19, 21, 22, 25, 26, 30; 9 native
frames at 1080×1920: 01 ×2, 03 ×2, 09 ×2, 04, 12, 17). Not viewed: 07, 08, 11, 13, 16, 18, 20, 23, 24, 27, 28, 29.
Computational: all 30 videos at 1 fps (1,697 frames, proxy 108×192, caption band excluded); private tooling `pair.py`,
`edge.py`, `mood_stats.py`, `classify.py` v0.1 (`~/ricks-clips-private/analysis-data/rc30/agents/a09-lighting-shadow-specialist/`);
`data/mood_classes.json` committed.
Method: lit/shade pairs = manual patch pairs (median of a 60–200 px box) on one material across one shadow boundary of
a native frame; linear sRGB; Y = Rec.709 luminance. n tiny → confidence capped at medium. H.264 re-encodes add 1–2 px
edge softening.

## F-A09-001 Cards cast hard dark shadows only under a strong directional key (resolves A01 vs A06)
OBSERVED + MEASURED, medium. Shadows: RC30-01-f000359 (each card casts floor + wall shadow with its own silhouette incl.
stick legs, dark neutral grey); RC30-09-f000629 (shadow on door and floor); RC30-09-f000929 (window-bar gobo light
crosses cards; legs cast on floor); RC30-14 f000779..f000929 (sheet; long blue shadows); RC30-12-f000059 (fence
shadows). Absence: RC30-03-f000089 and f000749 (firelit night, no ground shadow under any card); RC30-17-f000599 (faint
foot smudge only); RC30-30 (sheet, none); RC30-01-f000509 (faint dark halo only). Both A01 and A06 are right for their
own frames; the split by lighting condition is INFERRED; absence is hard to prove at sheet resolution. A01's "soft" is
not supported (edges are mostly hard, F-A09-004).
Implementation: `castShadow=true` on cards with an alpha-tested depth material in hard-key presets; off in night/fire/
illustrated presets (at most a weak blob, opacity 0.15–0.25).

## F-A09-002 Shadow density 1:7 to 1:13
MEASURED, medium, n = 9 pairs in 4 videos. Shade/lit Y: RC30-01-f000359 floor 0.075, tile 0.124; RC30-09-f000629 door
0.096, brick 0.096; RC30-09-f000929 floor (sky-fill heavy) 0.32; RC30-12-f000059 dirt 0.14, 0.19; RC30-04-f000209
field 0.27, grass 0.14. Median 0.14 (IQR 0.096–0.19, range 0.075–0.32) ≈ 7:1 key:fill. Card self-terminator shallower:
RC30-09-f000629 face (255,255,255) vs shaded (162,156,177) ≈ 0.36; RC30-09-f000929 (167,171,194) vs (252,246,247)
≈ 0.38. Implementation: world ambient ≈ 0.14 of key; card shader shade floor 0.36.

## F-A09-003 Shadows carry the ambient/sky colour
MEASURED, medium, n = 6 pairs in 4 videos. RC30-12-f000059 dirt (234,162,63) → (76,66,94), Δb* ≈ −57 to −75 (violet on
orange); RC30-04-f000209 field Δb* −20, grass −35; RC30-09-f000629 walls Δb* −8 with chroma rise (teal 124,184,196 →
22,60,86); RC30-01-f000359 grey interior Δb* ≈ 0 to −2 (neutral). Rule: shadow hue = dominant fill hue of the set; the
strong violet in 12 is stylisation (not corrected).

## F-A09-004 Shadow edges mostly hard
MEASURED, low–medium, n = 8 profiles in 4 videos. 10–90 % widths (px at 1080 wide): 01-f000359: 18, 5; 09-f000629: 2,
33, 10; 09-f000929: 13, 1; 12-f000059: 4, 42; 04-f000209: 67 (distant tree). Median ≈ 11.5 px (IQR ≈ 4–33) = 0.4–3 % of
width; edges widen with distance from the occluder. Implementation: PCFSoftShadowMap, radius 2–4, mapSize 2048.

## F-A09-005 Key direction
OBSERVED, low–medium (angles ±20°). Day/interior: key high (45–70°), 30–60° off camera axis (01-f000359 shadows down
and slightly right; 09-f000629 key from screen-right, shadow on door to the left; 04-f000209 sun from screen-left, tree
shadow falls right). Drama: low sun (10–30°) from behind, shadows toward camera (12-f000059, 14 f000779..f000929). True
azimuth from highlights not measured.

## F-A09-006 Mood presets
MEASURED + OBSERVED, medium. Rule-based classes on 1 fps proxy statistics (1,697 frames, 30 videos); median L*/a*/b*:
| Class | n | Videos | L* | a* | b* |
|---|---|---|---|---|---|
| neutral_mid | 450 | 30 | 53.5 | 2.9 | 2.2 |
| violet_dusk_neon | 222 | 21 | 37.0 | 20.4 | −30.8 |
| red_orange_glow | 179 | 21 | 46.2 | 18.6 | 21.4 |
| dark_low_key | 168 | 16 | 22.7 | 5.6 | −8.6 |
| night_blue | 165 | 24 | 36.6 | 6.9 | −12.9 |
| warm_day_sunset | 149 | 25 | 65.1 | 6.4 | 17.1 |
| day_cool_sky | 137 | 22 | 61.1 | 3.4 | −10.7 |
| warm_interior_lamp | 131 | 21 | 43.9 | 9.6 | 15.9 |
| red_pink_saturated | 82 | 17 | 44.6 | 19.9 | 0.5 |
| bright_neutral_interior | 14 | 9 | 68.6 | 3.1 | 3.2 |
Median 3 classes at ≥ 10 % share per video (range 1–5); 16/30 videos contain both a warm and a cool class at ≥ 10 %.
Overall L* median 47.7 (IQR 34–59), b* median 0.4 (IQR −12 to +13). Within-video SD b* 13.3, L* 12.7 → mood changes
inside a Short. Sheets confirm: day exterior 04, 06, 10, 12, 14; blue night 03, 15, 17, 21, 26; warm interior 05, 17, 02;
spotlight 30; red wash 25 and 09 from f000749; x-ray/cross-section 02, 17, 30; sunset 14, 21, 22. Limits: thresholds
unvalidated; whole-frame statistics include characters; class switches/min (14.6) mostly measure cut rate.

## F-A09-007 Re-lighting rides on story beats
OBSERVED, medium, 7 videos. A hub set is re-lit by cut or ≈ 6-frame crossfade between day/dusk/night states;
continuous sun moves inside one take not seen (not proven absent). 22: day ship → forge fire → dusk lantern ship
(f001019..f001109); 21: hall → dusk sun (f000899) → blue night; 06: day → dusk → rain night → sunrise (f001109); 17: pink
dusk → blue snow night with warm lamps; 26: warm hall alternating with blue-violet alley; 01: bright bathroom (f000029)
vs blue night bathroom (f000509); 25: cool domestic vs red bloodstream.

## F-A09-008 Cards take scene tint but stay readable
MEASURED + OBSERVED, medium, 6 native frames. RC30-01-f000509 (night): wall (172,184,229) and (0,0,61) but face
(251,250,254) and torso (242,193,48) stay bright — card almost exempt from scene darkness. RC30-03-f000749 (fire): face
left (233,210,204) vs right (252,235,217) — warm gradient toward fire. RC30-17-f000599 (lantern): face (251,195,137)
peach against blue ceiling (96,108,155). RC30-09-f000929: window-bar gobo crosses the cards (cards receive projected
light). Faces stay at L* ≥ 85 in every scene viewed (consistent with F-a01-005).

## F-A09-009 Practical lights
OBSERVED (+ MEASURED pools), medium. Fire pool RC30-03-f000089: ground (146,93,68) near → (62,51,57) far over ≈ 3 card
heights. Lantern pool RC30-17-f000599: boards (162,104,72) near vs (116,64,58) corner. Others: window shafts and floor
gobos (09, 02); RC30-19 flat yellow sun wedge on a wall (illustrated); screen glow (01 mission control); neon on wet
ground (26). Strong bloom on bright emissives (RC30-01-f000509 toilet, 05 gold); glows/rays → A12.

## F-A09-010 Two lighting treatments (mirrors A05's A/B split)
OBSERVED, medium. A — 3D PBR with real shadow maps, bloom, shafts: 01, 03, 04, 06, 09, 10, 12, 14, 21, 22, 26.
B — illustrated: 15, 17, 19, 25, 30 and cross-sections; light painted as flat gradients and hard-edged patches, no
shadow maps.

## F-A09-011 Rim / back light
OBSERVED, low–medium. Backlight appears as a sun/moon disc behind subjects, not a coloured rim on cards (03, 21
f000899, 14, 12); the ink outline does the separating. Card-edge fresnel is a HYPOTHESIS (not seen).

## F-A09-012 Ambient occlusion
OBSERVED, low–medium. Props show contact darkening (barrels, bench in RC30-09-f000929; bomb in RC30-03-f000749); cards
show none apart from a faint foot smudge in RC30-17-f000599. Night-scene halo is probably bloom or outline softness.

## Contradictions and limits
A01 "soft" vs A06 "none": resolved in F-A09-001. Not done: key azimuth from highlights; card fill ratio for most videos;
stylised-vs-physical shadow check on all 30; 12 videos unviewed. `color.csv` existed for 8 videos only (15, 23–28, 30)
→ own 1 fps pass for all 30; cross-check vs A27 tables open. Open: does shadow direction stay fixed within a take? Are
faces re-lit per frame or by a baked gradient?
