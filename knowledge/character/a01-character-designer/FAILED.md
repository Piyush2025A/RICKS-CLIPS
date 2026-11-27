# A01 FAILED
- F01 Ray-based outline width: rays from the face centroid are oblique to the edge and merge with dark backgrounds →
  20–40 px, contradicting scanline 10–17.5 px. Discarded (`data/outline_rays_v1_UNRELIABLE.json`). Use scanlines normal
  to the edge or an A27 contour measurement.
- F02 Silhouette fill ratio, Hu moments, k-means palette: not computed — no alpha/clean masks, only composited frames;
  needs a segmentation pass (A27).
- F03 `analysis/get_frames.py` ≈ 1 min/frame under batch load (it decodes from the start); only 7 of ~12 planned native
  frames extracted (02, 25, 30 skipped). Request several frames per call; prefer contact sheets.
- Process note: `pkill -f get_frames` killed the agent's own shell — never use broad pkill patterns.
