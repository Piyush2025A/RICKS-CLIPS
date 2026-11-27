# Expression & proportion bible (draft v0.1)
Sources: a02 (F-A02-*), a03 (F-a03-*), a04 (F-a04-005), a20 (F-A20-007).
## Expression system
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| E1 | Face = swappable layers | eyes × brows × mouth × accessories | F-A02-001 | H |
| E2 | Vocabulary size | 11 eye states, 6 brow states, 13 mouth states; accessories: sweat, pain ticks, blush, tint, steam | F-A02-002..005 | M |
| E3 | Hold-and-snap | changes are single-frame swaps, no tweening; bursts of 3–5 swaps in 10–20 frames then 20–100+ frame holds | F-A02-006, F-a04-005 | M |
| E4 | Timing vs words | swaps at −3…+2 frames of caption word change (median ≈ −1, n = 9) | F-A02-007 | L |
| E5 | No narrator lip-sync | in-scene talkers flap a 4-shape set held 1–5 frames, not phoneme-synced | F-A02-008 | M |
| E6 | Blink | half-lid → 1–2 closed frames → open (2–4 frames), every ≈ 2–4 s | F-A02-009, F-a04-005 | L |
| E7 | Same face grammar on objects | pills, sacks, brains get the same face parts | F-A02-002, F-a01-003 | M |
## Proportion spec (template for ORIGINAL characters)
Head H/W ≈ 0.93 reference (C3); height ≈ 3 HW (C4); torso width/HW slim 0.65 · tall 0.75 · stout 0.85; torso length
≈ 0.85 HW; scale kept rigid across shots (torso W/HW within ±1 % for one character in 3 shots). Evidence F-a03-001..006 (L).
Implementation: T-A02-01..09 face rig spec (part counts, state names); drive swaps from ElevenLabs word timestamps with
offset −1 frame; captions appear 2 frames before word onset (F-A20-007).
Open: timing n tiny (A02 n = 9; A03 7 videos); blink rate low confidence; two-axis re-measurement recommended.
