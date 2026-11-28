# A03 TECHNIQUES (provisional; derived from FINDINGS n<=18, low-medium confidence)
## Proportion spec sheet template (unit HW = head width; all values front view, hats excluded from head)
| Field | Slim (default) | Stout | Tall | Long-robe |
|---|---|---|---|---|
| head H/W | 0.94 +-0.05 | 0.93 | 0.90 | 0.92 |
| torso W / HW | 0.65 +-0.05 | 0.85 +-0.05 | 0.75 +-0.05 | 0.74 |
| torso L / HW (chin to pill bottom) | 0.85 +-0.10 | 0.85 | 0.85 | 1.65 |
| leg L / HW | 1.2 +-0.1 | 1.25 | 1.25 | 0.40 |
| total height / HW | 2.95 +-0.15 | ~3 | ~3 | 3.0 |
| leg fraction of height | 0.38 | n/a | 0.43 | 0.135 |
Stroke: one constant width for outline, limbs; hand disc 0.1 HW; foot = short stroke ~0.15 HW (eyeballed). Distinctness for our originals: change one of head H/W, torso W, leg length by >= 15% so silhouettes differ.
Turn rule: for a 3/4 or side turn keep head circle, narrow torso to ~0.5-0.55 HW, show stride in profile; do not squash the head.
## Rig pivots for A04 (INFERRED)
Root = pill bottom centre (hip). Pivots: neck = chin point at pill top; shoulders = pill top corners (x = +-torso_W/2, y = chin+0.1 HW); arms = single stroke from shoulder to ball hand; hips = pill bottom at x = +-0.2 HW; legs straight strokes (no knee), foot pivot at sole; head pivot at chin so tilts hinge there. Long-robe: legs begin below robe hem.
## Measure recipe
`python3 data/ratios.py data/landmarks.csv`; landmarks read from `data/grid.py` overlays of native frames (100 px grid). Add rows, rerun.

## Phase 3B revision (n = 66 characters, 26 videos; medium confidence; tolerances = IQR)
Head H/W 0.93 (0.89-0.98); torso W 0.66 adult / 0.89 large / 0.66 tall; torso L 0.89 HW; leg L 1.23 HW (1.12-1.32); leg/torso 1.38; height 3.0 HW = 3.27 HH; leg fraction 0.40; leg stroke 0.053 HW; child legs 0.6 HW (n=1). Annotation error median 3 px native (ratio 0.02-0.04). Rebuild: `python3 data/ratios_3b.py ...` (see FINDINGS 3B).
