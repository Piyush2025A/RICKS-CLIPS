# Animation & movement bible (draft v0.1)
Sources: a04 (F-a04-*), a02 (F-A02-006), a06 (F-A06-001/008), a12 (F-a12-003..006).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| M1 | Hybrid rig: redrawn per-pose bodies/limbs + rigid card transforms + face-part swaps; no fixed bone chain look | limbs are variable curves, knees bend | F-a04-001 | M |
| M2 | Pose updates on ones (30 Hz) in action; bursts then holds; no on-twos look | holds 7–28 f | F-a04-002/005 | L–M |
| M3 | Walk | step ≈ 11 f at 30 fps (9 at 24), cycle ≈ 22 f; n = 1 walker | F-a04-003 | L |
| M4 | Idle = held body + face changes; the camera supplies motion (no breathing bob) | — | F-a04-004 | M |
| M5 | Secondary motion via props/VFX, not hair physics (hair/hats rigid; hats fly off ballistic) | — | F-a04-006, F-a12-003/004 | L–M |
| M6 | Cards: x, y, z, uniform scale, roll; yaw locked to camera; depth sorting by geometry; limbs overlap props for gags | — | F-a04-007, F-A06-001/008 | M |
| M7 | Impacts | anticipation ≈ 12 f lean; hit covered by VFX arcs/debris (spawn 1–3 f, spread 12 f, dwell 10–20 f) | F-a04-005, F-a12-003 | L |
| M8 | Character-to-character contact hidden by cuts or VFX | — | F-a04-004 | M |
Implementation: A04 TECHNIQUES (rig hierarchy, pivot/draw-order table, timing presets at 30/24 fps, cycle specs); A03
pivot guidance; A25 module M-card-rig. Open: n ≥ 3 walkers, bob/lean/slip, 10+ frame-rate segments.
