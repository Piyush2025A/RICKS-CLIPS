# A07 FAILED

- Automatic background-blur sigma from grid cells (Laplacian variance normalised by luma variance vs the frame's p90 cell, mapped by Gaussian calibration): AUC 0.57-0.72 against my visual soft/sharp labels (n=116); sigma_eq 0.5 vs 0.7 px. Cause: soft shading, flat colour fills and sky confound sharpness; metric saturates above ~2 px. Lesson: need edge-spread on straight edges or a subject mask; shares come from visual labels.
- Rack-focus search from global lap_var ramps: 3 viewed candidates gave 1 true focus pull, 1 fog dissolve, 1 unflagged hard cut. Global sharpness cannot separate cuts, fog and focus.
- Overall: shot-size, horizon and camera labels are manual; no vanishing-point FOV solve; run limited by CPU load (shared batch), sampling stepped from 10 to 30 frames for videos 05-30.

## Phase 3B
- Max-cell/min-cell edge-sigma ratio does not separate shallow DOF from content (flat fills, haze, low-contrast far scenery give 2-3 px): 5 visually deep frames scored 2.8 px vs shallow-bg 3.6. Labels still need viewing. Frames with large blur become edgeless (unmeasurable above about 8 px): macro blur under-counted.
- Automatic two-VP FOV solve: 187/581 frames pass loose filters but only 13 are well-conditioned (two finite horizontal VPs, same horizon); vertical-line VPs give ill-conditioned f. Failed to reach 15 frames / 10 videos; sample step 90 limits candidate count.
- A13 moves_table lateral windows with large displacement include cuts: parallax pairs there are noisy; only slow windows gave clean ratios.
- Atmospheric-depth re-measurement not done (time).
