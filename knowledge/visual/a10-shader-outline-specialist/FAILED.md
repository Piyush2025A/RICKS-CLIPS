# A10 FAILED
- F-1 `edges.csv` `edge_width_px` as ink width: quantised to {1.5, 3.5, 5.1}, median 1.5 px in 5/8 videos — not a line width; own scans used.
- F-2 Global dark-line histograms (`lines_all.py`): the hair class is 2–3 px in every frame incl. treatment A (grass,
  bark, text) — cannot tell ink from texture.
- F-3 Gradient-share and black-hat coverage (`scene_stats.py`, `thin.py`) to separate A from B: black-hat picks up
  shading/dark masses (median "thickness" 4 px, coverage 16 %) — dropped; flat/hard shares track content, not treatment.
- F-4 First horizontal scans over-stated width on slanted edges (median 10.75 px, IQR 4.75–18.7 in `ink_scan2`) until the
  normal correction in `ink_scan3`.
- F-5 Vignette from composition-confounded luma: not separable; low confidence.
- F-6 Native fetch for video 08 failed (`printf %02d` with `08` read as octal); not retried.
- The Write tool refused the deliverables; texts returned in the hand-off.
