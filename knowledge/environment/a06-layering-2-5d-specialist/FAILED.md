# A06 FAILED approaches

## FA-001 Per-feature LK tracking over 10–20 frames (2026-11-28)
Goodfeatures + pyramid LK (win 21, 3 levels) over 10–20 frames at 540x960 on RC30-06/10/25/04/21/01/29/13/22 gave displacements up to 320 px with p90/p10 ratios 2.5–14.8 and non-monotone y-band medians. Cause: large camera motion + flat-shaded regions lose/jump tracks; results not trusted and not used. Lesson: use 2-frame dense flow (done in F-A06-003/004) or per-frame chained tracking with forward-backward check.

## FA-002 k-means flow clusters as "plate count"
k over-counts for continuous depth gradients (dolly) and mixes character animation with camera flow. Only usable as a "flow diversity" proxy. A real discrete-plate test needs occlusion/A07 evidence or a depth-estimation model (not available).

## FA-003 Contact sheets as source
Per-frame sheets existed for only 4/30 videos at run time; decoded native video with OpenCV instead (strips in private folder).

## FA-004 Not achieved
Overscan percentage (no plates in reference), halo pixel-statistics test, orbit >30 deg around a card. 
