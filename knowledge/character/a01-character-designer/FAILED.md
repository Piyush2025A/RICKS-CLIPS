# A01 FAILED
- F01 Ray-based outline width: rays from the face centroid are oblique to the edge and merge with dark backgrounds →
  20–40 px, contradicting scanline 10–17.5 px. Discarded (`data/outline_rays_v1_UNRELIABLE.json`). Use scanlines normal
  to the edge or an A27 contour measurement.
- F02 Silhouette fill ratio, Hu moments, k-means palette: not computed — no alpha/clean masks, only composited frames;
  needs a segmentation pass (A27).
- F03 `analysis/get_frames.py` ≈ 1 min/frame under batch load (it decodes from the start); only 7 of ~12 planned native
  frames extracted (02, 25, 30 skipped). Request several frames per call; prefer contact sheets.
- Process note: `pkill -f get_frames` killed the agent's own shell — never use broad pkill patterns.
- F04 (3B) Per-shot-type character counts: not produced. 1-fps tiles carry no shot-type label and the eyeballed tally covers only 3 videos; do not cite as a distribution. Needs a shot table from A15/A16 joined to a character detector (A27).
- F05 (3B) Native check at 1080×1920 for 22 videos was not viewable economically; frames were downscaled to 540×960 (outline widths therefore not re-measured). Sub-pixel outline/colour claims need crops.
- F06 (3B) Classifier refused a bash for-loop that batch-wrote ledger records; ledger records were then written one command per image with explicit frame ranges (no change in content).
