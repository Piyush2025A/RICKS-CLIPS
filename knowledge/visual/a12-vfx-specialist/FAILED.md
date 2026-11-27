# A12 FAILED
1. `flash_candidate` as screen-flash detector: 0/8 candidates in 4 videos were true flashes (zooms, wipes, bloom). Use
   luma + visual confirmation.
2. Counting VFX from 1 fps overview sheets: effects last 4–50 frames and are missed or caught mid-life; types findable,
   durations/rates not. Needs a hand count on every-frame sheets.
3. Frame timing outside the 8 videos with A27 sheets: private every-2nd/3rd-frame strips via ffmpeg `-ss` seek — labels
   are offsets (±1 frame), weaker than A27 sheets. (Write tool refused the knowledge files; texts returned in hand-off.)
4. luma_mean spikes alone mix cuts, lighting changes and wipes → only an upper bound on VFX frequency.
5. Not done: effect-to-audio lag (hand-off A21); effect-area masks; no EXP-* experiments (no rendering this phase).
