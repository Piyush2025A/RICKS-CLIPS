# A05 FAILED approaches and gaps (Phase 3 V1)

## FA-A05-001 — Frame-count-based dressing density not produced
Tried: estimate `props_per_establishing` by manual counting on 1-fps overview tiles (180x320). Result: counts are only order-of-magnitude (25-60) because tiles are too small to enumerate props and DOF hides objects. Lesson: needs native frames on a fixed grid with a written annotation protocol; not attempted within the ~60-view budget.

## FA-A05-002 — Vanishing-point / horizon extraction not run
Reason: no time/budget in this pass; the 360p overview tiles contain burned-in captions and DOF which would pollute line detection. Lesson: run LSD on native frames with the caption band (y 60-80 % of frame height) masked, and only on A27 shots flagged static.

## FA-A05-003 — Per-video motion numbers limited to 2 videos
`motion.csv` existed only for RC30-15 and RC30-27 when this was written; the other 28 were not processed yet. Camera-moving fractions therefore rest on n=2. Lesson: re-run the one-liner in F-A05-002 once A27 finishes the batch.

## FA-A05-004 — Dolly vs zoom cannot be separated
`motion.csv` has a 2-D similarity model only; `scale` change is both dolly and zoom, so we cannot say how far the virtual camera travels. Lesson: use visual strips (parallax between near and far objects) for the 3D claim, tables only for "camera moving".

## FA-A05-005 — Image strip file naming
First crop strips were saved per video at 240 px wide; text on small tiles (props signage) was not legible. Lesson: use 480 px tiles when reading signage.
