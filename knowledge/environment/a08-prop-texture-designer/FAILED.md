# A08 FAILED — approaches that did not work (Phase 3)

## X-A08-001 Per-frame sharpness/edge tables as a treatment A vs B texture-energy measure
`sharpness.csv` (lap_var, grad_energy) and `edges.csv` (canny_density) medians per video, groups A (02, 26, 27), B (15, 25, 29, 30),
hybrid (23, 24, 28): lap_var 351-850 (A), 341-850 (B), 495-956 (H); no separation. Frame-wide metrics are dominated by character
ink, captions and lighting, not flat-material texture. `edge_width_px` medians are quantised (1.5/3.5/5.1) and not usable as seam width.
Lesson: material texture needs manual patch boxes; only 10 of 30 videos had tables at the time. Data kept in `data/frame_level_hf_by_video.json`.

## X-A08-002 Blind intensity profiles for seam FWHM
Profiles placed without seeing the exact pixel location returned 2-48 px widths, i.e. hit fills or wide shapes, not lines (`scripts/prof.py`).
Replaced by skeleton/distance-transform width (`scripts/lw.py`), which is quantised and includes text and stripes. A true FWHM needs boxes chosen on a zoomed crop.

## X-A08-003 Patch boxes contaminated by edges or text
Discarded (flagged in `data/patch_stats.json`): crate planks and steel pan (05 f869), blue table top (09 f359), navy ticket gap and digit zone (16 f1049), 7-seg display (27 f419). Lesson: view a 4x crop of each box before measuring.

## X-A08-004 Native frame extraction
First background batch of `get_frames.py` produced nothing (silently); re-run via a script file worked at ~1-2 min per video. Frames 22 f689/f419, 13 f749, 29 f509, 02 f149 were requested but never viewed (turn limit).

## X-A08-005 Process note
A command that tried to create and delete a dummy ledger record was blocked and had no effect; the ledger (24 records) was verified intact. Visual ledger counts only images actually opened.

## Phase 3B additions
### X-A08-006 Grid-cell patch picking from 360x640 composites
Of 36 cells chosen from 4-frame grids, 15 were wrong or contaminated (caption text, ink, adjacent objects; 'orange earth' turned out to be a blue shadow, 'fabric', 'plastic crate', 'enamel fridge' caught text). A second round of 9 explicit boxes gave 4 usable (bell, glass, enamel, siding) and 5 failed (bedspread, planks under caption, forehead, red paint on a wheel). Lesson: the caption sits at y 1340-1530 (A27/captions table), never box there; pick boxes on a 4x crop, not a thumbnail. Fabric, plastic and steel remain unmeasured.
### X-A08-007 Plank seam FWHM
The strip (12 f209, y 1330-1420) lies inside the caption band, so 6-10 px widths are text edges. Discarded. Use captions/caption_segments.csv to mask.
### X-A08-008 Treatment A/B by 1-fps tile
At 180 px tiles the thick-ink-on-props question cannot be answered; needs native crops per video.
