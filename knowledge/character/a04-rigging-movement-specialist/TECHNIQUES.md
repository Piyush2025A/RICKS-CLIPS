# A04 TECHNIQUES (provisional; derived from FINDINGS F-a04-001..007, n small, confidence low-medium)
Frame values at 30 fps (reference) and 24 fps (dev, x0.8, rounded). Items marked [H] are design choices not measured in the reference.

## 1. Hybrid rig (Three.js card / Remotion 2D layer)
Root = `Group` at hip, yaw locked to camera (A06). Draw order back to front (z offsets 0.001 apart, `alphaTest` cutouts, depth-tested):
| Order | Part | Pivot (local, unit HW = head width; from A03) | Allowed rotation (deg) | Swap set |
|---|---|---|---|---|
| 1 | back arm | shoulder (x = +/-0.33, y = +0.1 below chin) | -170..+170 | hand/prop attach |
| 2 | back leg | hip (x = -0.2, y = pill bottom) | -45..+45 | stride poses |
| 3 | torso pill | root (hip centre) | -15..+15 lean [H] | outfit/state tint (e.g. anger colour, A01) |
| 4 | front leg | hip (x = +0.2) | -45..+45 | stride poses |
| 5 | front arm | shoulder (x = -0.33) | -170..+170 | hand/prop attach |
| 6 | head circle | neck = chin point at pill top | -20..+20 | none (circle never squashed) |
| 7 | face layer | head centre | 0 | eyes, brows, mouth, sweat (A02 swap sets) |
| 8 | headgear/hair | head centre | follows head | hat can detach to prop mesh |
Limbs: quadratic Bezier stroke, constant width (A03 0.05 HW), 3 control points (root, bend, tip), hand ball 0.1 HW, foot short stroke 0.15 HW. Keyframes set control points per frame, so curved/bent poses are free.
Large pose changes (lying, seated, back view, crouched) = whole-card pose swap from a library (A24 supplies separated layers per pose); do not rotate the standing rig 90 deg.
Prop detach: hat/held items are separate meshes; on a hit, remove from head and give ballistic motion: v0 6-10 u/s, spin 360-720 deg/s, gravity 9.8 [H], flight 25-30 frames (06-f000778..f000810).

## 2. Frame-rate policy
- Evaluate everything at 30 fps (24 fps dev). Drawings/poses on ones during action; hold keys 6-12 frames in dialogue; do not apply twos/threes unless a style test is approved.
- Face swaps: bursts of 2-4 consecutive new drawings (1 frame each), then hold >= 7 frames (15-f001393..f001408).

## 3. Presets (frames at 30 / 24 fps)
| Preset | 30 fps | 24 fps | Notes (source) |
|---|---|---|---|
| walk step | 11 (range 10-12) | 9 | 14-f000656..f000703 numeric n=4 intervals (10-11); 06 march visual 12; cycle 22 / 18 (3B) |
| walk bob | 1-2 % of height (MEASURED 1.2 %, n=1, 14) | same | H-UP 3-7 % not supported; test 1 % vs 3 % in the controlled experiment |
| walk lean | [H] forward 3-5 deg | same | observed slight forward tilt only |
| blink | close 2, open 2-3 | 2 / 2 | 15-f000000..f000005 |
| expression pop | 2-4 swaps then hold 7+ | 2-3 / 6+ | 15-f001397..f001408 |
| anticipation | 8-12 | 6-10 | 06-f000764..f000776 lean before hit (approx) |
| strike/hit pose hold | 3-6 | 2-5 | [H] |
| scream/blast hold | up to 28 | 22 | 22-f000213..f000240 |
| fall/tumble | 14-18 rot 540-720 deg, scale +/-20 % | 11-14 | 25-f000224..f000239 (approx 15 f) |
| settle after landing | 6-10, damped sine 2 cycles, amp 6 % | 5-8 | [H] not measured |
| camera push on held card | 24-45 f ease in-out, scale 1.0 -> 2.5-3 | 19-36 | 15-f000000..f000031 (3x in 31 f) |
| entrance pop-up | 8-12 (scale 0.6 -> 1) | 6-10 | 19-f001139..f001169 (approx) |
| anger tint | swap to tint + steam puffs, hold | n/a | 10-f000539 |
Easing: ease-out-cubic (0.215, 0.61, 0.355, 1) for settles; push-ins ease-in-out sine; overshoot on cards not seen: default 0-5 %.

## 4. Cycles
- Walk: 22-frame cycle at 30 fps (two steps of 11); key poses: contact L (0), passing (5-6), contact R (11), passing (16-17); legs redrawn every frame via Bezier control-point interpolation; head vertical offset peaks at passing; camera follows body (character in place), ground texture slides at 1 step length per 11 frames to avoid skating (foot slip target < 5 % of step length, our test, to be measured).
- Idle: hold body; blink every 90-150 frames [H]; head micro-drift <= 1 % per second [H]. Life comes from camera push-in and ambient particles (30-f000768..f000815).
- Slow push-in on a held card: scale ramp with ease-in-out, 24-45 f, 2.5-3x.

## 5. Production notes
- Request from A27: tracked head/foot tables (F-a04 open question 1) before locking walk bob/slip numbers.
- Run `data/iou.py` on any new walk or gesture segment to count held vs changed frames; report n.

## 6. Phase 3B additions (measured, F-a04-100..104)
Gesture/hold timing (30 fps -> 24 fps x0.8), n = events in F-a04-103:
| Preset | 30 fps | 24 fps | Source |
|---|---|---|---|
| dialogue body hold (face swaps only) | 24-48 | 19-38 | 09 f480-527 (48), 10 f528-575 (48), 14 f384-407 (24), 06 f312-335 (24+) |
| small gesture (kick, holster, raise object, head turn) | anticipation 2-3, action 5-10, hold 4-20 | 2 / 4-8 / 3-16 | 07, 14, 26 |
| arm raise + wave | anticipation 2-3, action 12 | 2 / 10 | 09 f410-423 |
| big hit anticipation | 12 | 10 | 06 f764-776 |
| hold then sudden move | hold 29, action 11 on ones | 23 / 9 | 29 f1064-1103 |
| entrance walk-in | 32 (one character crosses frame) | 26 | 09 f496-527 |
| moving body drawing rate | new drawing each frame (ink overlap median 0.5-0.9) | each frame | 14, 09, 29, 10, 07 |
| march step | 12 | 10 | 06 f104-139 (visual) |
Rule: no twos/threes; during dialogue freeze the body completely (not a breathing loop) and put life into face swaps, steam/VFX and camera. Run `data/iou2.py` on new segments.
