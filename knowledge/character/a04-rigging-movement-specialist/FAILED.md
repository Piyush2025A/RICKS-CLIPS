# A04 FAILED approaches (Phase 3)
1. Whole-frame / whole-ROI frame differencing to find duplicated (on-twos) frames: failed. The camera moves or drifts in essentially every frame (RC30-01 min diff 0.2/255 over 1,835 frames; only RC30-15 has three static runs of 14-22 frames), so no pair of frames is identical and diff series cannot show a hold. Replaced by ink-mask overlap after phase correlation (`data/iou.py`), valid only when the character ink is separable from dark scenery.
2. ECC alignment on loosely placed ROIs (`data/roi.py`, pill 25, head 28, head 07): residual stayed 5-30 because the ROI contained background and parallax; only the tight face ROI in RC30-15 gave a clean floor. Not used as evidence except for 15.
3. `motion.csv` residual columns (res_mean_mag, res_active_frac) as action locator: useless here, values 8-50 in almost every window because the global model cannot fit a 3D camera; windows chosen from sheets instead.
4. Ink-overlap on 22-f000213..f000240: debris/splinters are ink-coloured and swamp the character; result discarded.
5. Foot slip, bob amplitude, lean range: not measured. Needs a tracked foot/head point with camera compensation; tracking on 150 px strips was not accurate enough, and no second and third walker segment was located within the image budget. n for walk = 1.
6. Overview sheets (1 frame per second) cannot show motion timing; used only for the inventory of actions and poses.
7. Time: only 5 videos had every-frame sheets at run time (15, 25, 27, 28, 30 plus 23 without sheets); other videos needed my own native decode (strip.py) at about 20-60 s per video under shared CPU. A global computational sweep of all 30 videos was started and stopped because it could not answer the frame-rate question.

## Phase 3B additions
8. Ink-mask / leg-spread tracking on 06 march and 26 cop walk (`walk3.py`, `leg.py`): ROI contaminated by dark scenery or the camera changed scale, so the series were noise (06 ACF peaks < 0.25, 26 monotonic). Step for 06 taken from a visual count only; 26 unresolved.
9. Background subtraction for the static-looking 09 walker (`bgsub.py`): camera drifts slightly, the whole ROI differed from the median background (bbox height 460-480 px always); abandoned.
10. `iou2.py` on 26 f336-383: ROI full of static door frame gave 0.98 for all pairs (looks like a full hold); discarded as invalid. Lesson: check the ROI strip before trusting a "hold".
11. Walkers are rare: in about 20 sheets/strips viewed only 14, 06, 09, 26, 02 show walking, and none has a static camera plus visible planted feet, so foot slip and n >= 3 numeric walkers were not obtainable in this budget. 
