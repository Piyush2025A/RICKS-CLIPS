# Animation & movement bible (draft v0.3, Phase 3B)
Sources: a04 (F-a04-*, 3B F-a04-100..104), a02 (F-A02-101/102), a06 (F-A06-001/008), a12 (F-a12-*, 3B F-a12-100..104).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| M1 | Hybrid rig: redrawn per-pose bodies/limbs + rigid card transforms + face-part swaps; no fixed bone chain look | limbs are variable curves, knees bend | F-a04-001 | M |
| M2 | Pose updates on ones when bodies move; no on-twos look | moving bodies get a new drawing ≈ every frame (11 segments, 8 videos) | F-a04-101/102 | M |
| M3 | Dialogue bodies freeze | full body holds **24–48 f** while the face changes (09 guard 48, 10 anger pose 48) — supersedes "holds 6–12 f" for dialogue | F-a04-102 | M |
| M4 | Walk | step **≈ 11 f** at 30 fps (≈ 9 at 24), cycle ≈ 22 f — numeric n = 1 walker (RC30-14; intervals 11, 10, 11, 11); RC30-06 march ≈ 12 f visual; 3 other walkers unresolved; head bob ≈ 1.2 % of height (n = 1; H-UP "3–7 %" not supported); lean and foot slip not measured | F-a04-003, F-a04-100 | L |
| M5 | Gestures | anticipation 2–3 f for small gestures, ≈ 12 f for big hits (slap); action → hold (25 events, 15 videos; table in A04 TECHNIQUES) | F-a04-103 | M |
| M6 | Idle = held body + face changes; the camera supplies motion (no breathing bob) | — | F-a04-004 | M |
| M7 | Secondary motion via props/VFX, not hair physics (hair/hats rigid; hats fly off ballistic) | — | F-a04-006, F-a12-003/004 | L–M |
| M8 | Cards: x, y, z, uniform scale, roll; yaw locked to camera; depth sorting by geometry; limbs overlap props for gags | — | F-a04-007, F-A06-001/008 | M |
| M9 | Impact VFX | effects cut in at full density then decay; 1-frame muzzle bursts; smoke/debris covers (e.g. 22 f525–547); timing table for 18 events in 13 videos | F-a12-102/104, F-a12-003 | L–M |
| M10 | Character-to-character contact hidden by cuts or VFX | — | F-a04-004 | M |
Implementation: A04 TECHNIQUES (rig hierarchy, pivots/draw order, walk preset 11 f @30, gesture/hold table); A12
TECHNIQUES E01–E25; A25 module M-card-rig.
Open: walk n ≥ 3 with bob/lean/slip on a static-camera walker; pose frequency (presence only per video).
