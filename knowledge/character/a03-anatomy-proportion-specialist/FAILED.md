# A03 FAILED / lessons
- F-a03-F01: Overview-sheet candidate hunt: most characters are cropped (legs off-frame, seated, robed), so only ~8 of ~35 selected frames gave sole-to-head height. Next time pre-screen with a script (dark-outline bbox) or ask for full-figure shots.
- F-a03-F02: Manual landmarks off a 100 px overlay at ~0.78 downscale: +-8-10 px (3-6% of HW at small scale); gives ratio noise ~10-15% (11-f000719 vs f000749). Use crops at 1:1 or edge-snapping next time. No re-annotation done: rules with error >10% are LOW confidence.
- F-a03-F03: Hats/hair hide skull top (~half of figures), so head H/W only for bareheaded (n=12).
- F-a03-F04: get_frames.py under load took minutes per video; extraction of 04/11/18/21/27/29 batches was not fully consumed before turn limit. Turn limit reached with ~12 frames unmeasured.
- F-a03-F05 (3B): leg-stroke scan by dark-run width failed on cluttered backgrounds (runs up to 74 per figure); 32 of 54 rejected; use segmentation of the figure outline instead.
- F-a03-F06 (3B): eye spacing and arm length not attempted (time/turn limit); overview sheet 1 only used for candidate search; 18/25/27/30 judged unmeasurable from it.
- F-a03-F07 (3B): chin landmark ambiguous at head/collar overlap (27 px max re-annotation diff); child/animal/object characters not measurable (n=1 / none).
