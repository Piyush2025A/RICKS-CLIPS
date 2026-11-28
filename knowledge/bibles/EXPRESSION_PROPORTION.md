# Expression & proportion bible (draft v0.3, Phase 3B)
Sources: a02 (F-A02-*, 3B F-A02-101..105), a03 (F-a03-*, 3B F-a03-101..106), a04 (F-a04-005, 3B F-a04-101..103),
a20 (3B F-A20-104). Audits: AUDIT.md #16, AUDIT_3B.md #16.
## Expression system
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| E1 | Face = swappable layers | eyes × brows × mouth × accessories | F-A02-001 (construction) | H |
| E2 | Vocabulary size | 11 eye states, 6 brow states, 13 mouth states; accessories: sweat, pain ticks, blush, tint, steam | F-A02-002..005 (overview-based, not re-checked in 3B) | M |
| E3 | Hold-and-snap | **45 of 46 expression changes are hard swaps of discrete drawings, no in-betweens** (every-frame strips, 26 videos; A28 VERIFIED as table); bursts of swaps then holds: hold next to an event median **5 f** (IQR 4–8, n = 26); swap-free holds 11–31 f | F-A02-101/102 (supersedes 3A "high 20/20") | M |
| E4 | Timing vs words | mouths/faces are **not locked to caption word onsets** (12 talking shots, 10 videos; permutation p 0.13–0.96; faces hold across 2–3 caption changes). 3A "swap −1 f before word" (n = 9) downgraded to low, non-general | F-A02-103, F-A02-007 | M (no lock) |
| E5 | No narrator lip-sync | in-scene talkers flap a small shape set; do **not** build a phoneme viseme engine | F-A02-008, F-A02-103 | M |
| E6 | Blink | 1–3 closed frames (7 events, 6 videos); blink interval unresolved | F-A02-104 | L |
| E7 | Same face grammar on objects | pills, sacks, brains get the same face parts | F-A02-002, F-a01-003 | M |
## Proportion spec (template for ORIGINAL characters — see CHARACTER C3–C5)
Head H/W 0.93; height ≈ 3.3 HH (≈ 3.0 HW); torso width ≈ 0.70 HW; leg ≈ 1.23 HW; leg/torso ≈ 1.38; leg stroke ≈ 0.05 HW;
outline ≈ 3.7 % HW. Measurement error: median 3 px at native, ratio error 0.02–0.04. Evidence F-a03-101..106 (66
characters, 26 videos; adults dominate) — M for adults, L for other types.
Implementation: T-A02-01..09 face rig spec; drive expression swaps from **story beats**, not from word timestamps; hold
5 f around a change and 11–30 f between bursts; captions ≈ 4 frames ahead of the voice (AUDIO A4).
Open: blink rate; readability at 48 px; eye spacing / arm length; child, animal and object-character proportions.
