# A15 FAILED / LESSONS
- Least-squares alpha fit (frame = a*A+(1-a)*B on 120x213 tiles) over-estimates crossfade length (median 10 vs visual 5-7) when the camera moves during the blend; needs motion-compensated or native-frame fitting.
- Turn limit reached after 6 full videos: viewing ~75 composite strips (6 candidates each) is too expensive for 24 videos in one session. Next time pre-filter gradual candidates with motion.csv (continuous camera) and view only ambiguous ones; split videos across sessions.
- Overview-sheet miss detection and easing-curve measurement not started.
