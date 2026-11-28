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
- F-7 (3B) Automated head tracking along push-in moves (`push_width.py`, bright-component nearest a manual seed): seeds wrong in 7 of 11
  frames (head_w 13-1079 px), result `data/push_width.json` is invalid and unused; replaced by pooled/same-character statistics plus viewing.
- F-8 (3B) The system python has no cv2/scipy; use `.venv-analysis/bin/python -I`. Frame extraction for 30 videos took ~3 min in the foreground (timed out at
  120 s and moved to background); wait with bounded loops on file counts.
