# A11 FAILED / LESSONS
- **F1 caption mask too wide (0.50–0.85)**: first pass masked 35 % of the frame; caption actually ≈ 0.64–0.70 (viewed sheets 02/03/14/25). Restarted with 0.60–0.76. Lesson: view a sheet before fixing a mask.
- **F2 killing my own run**: `pgrep -f` + `kill` hit my shell (exit 144) and the first pass; no batch process was touched (rcpipe ffmpeg PIDs survived) — never use pgrep -f patterns again, use a PID recorded at launch.
- **F3 tone-curve identification**: a transfer curve can't be recovered from output histograms alone; only distribution shape descriptors (lift, shoulder, symmetry) are reported (F-a11-004, low-medium). Needs matched-scene A/B on our renders.
- **F4 A27 color.csv for clipping**: includes white burned-in captions → p99 ≥ 254 inflated (0–35 % of frames vs 5.8 % masked). Use masked 1 fps pass for clipping; color.csv only for transitions (caption-insensitive in mean Lab, but not exact).
- **F5 mood labels**: A09's per-frame rule labels are not available as a table; used nearest centroid in L*a*b* of the frame mean — mixed-light frames may be misassigned. Not validated.
- **F6 transitions**: only 10/30 videos had both shot_candidates and color.csv when I ran; candidates include false positives. Cut-resolved ΔE for the remaining 20 not done.
- **F7 hero vs background**: no segmentation available; centre/periphery is a weak proxy (centre includes mid-ground).
