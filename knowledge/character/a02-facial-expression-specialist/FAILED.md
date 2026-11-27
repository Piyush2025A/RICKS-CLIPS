# A02 FAILED approaches and lessons

## F-A02-X1 Audio onsets vs caption change (word onset proxy validation)
Tried: nearest audio onset (audio.json `onsets_s`, 5.6-7.8/s) to each caption change for RC30-15/25/27/30; also rms upward-crossing
(35th percentile threshold, >= 80 ms quiet before). Result: median lag ~0 but IQR +-5.5 frames, only 34-45 % within -3..+8; onset
density is so high that a random series would give the same IQR. Music/SFX bed hides VO onsets. Conclusion: caption timing not
validated against audio; lag claims in F-A02-007 are relative to caption only. Need a VO-isolated stem or ElevenLabs word
timestamps from our own productions.

## F-A02-X2 Caption-change detector false positives
cap.py flags changes from bright scenery/transition crossfades (RC30-09/25/28: interval median 3 frames, 5-7 changes/s). Only
used in shots where text and background were checked visually.

## F-A02-X3 Face crop positions guessed from overview-tile coordinates
Overview tiles are 180x320 (6x native); I first crop with wrong y offsets (25 f0-47, 27 f148-195, 30 f30-77/f560-607 showed
only forehead/hair). Lesson: crop from tile coords x6 with the 30 px header ignored, or view one native frame first. Cost ~5 image views.

## F-A02-X4 Whole-video blink/expression rate
Not attempted numerically: no face tracker valid for cartoons was run; ROI diff needs per-shot face boxes. Rates are strip-based, n tiny.

## F-A02-X5 Not done
48 px readability self-test, second halves of videos, 10 videos not in catalogue (04, 06, 08, 11, 14, 17, 20, 23, 24, 29), per-video
blink rate for >= 10 videos, swap-to-word lag n >= 30.
