# A19 FAILED — approaches that did not work or were not possible (Phase 3)

| Date | Attempt | Result | Lesson |
|---|---|---|---|
| 2026-11-28 | Read frame 0 and f000029/f000059/f000089 from every-frame contact sheets for all 30 videos | Sheets exist only for 6 videos (RC30-15, 23, 25, 27, 28, 30) at run time; I did not open them (budget spent on the 1 fps overviews that cover all 30). | Frame 0 and sub-second first-visual-change are NOT observed for any video. Request A27 for a first-3-s strip (frames 0..89) for all 30, or the sheets once rcpipe finishes. |
| 2026-11-28 | Time-to-first-word from audio | Not attempted: audio.json exists for 6 videos only and I cannot run tools (no Bash). | Ask A27 for an audio onset table (first voiced onset per video) for all 30. |
| 2026-11-28 | Count re-hook words ("But", "So") per video from overview captions | Overview tiles are 1 fps; the caption changes every ~0.3-0.5 s, so only ~1 in 3 words is seen. Re-hook counts are a lower bound only. | Use the every-frame sheets (or an OCR caption track from A27/A20) for a true re-hook timeline before quoting rates. |
| 2026-11-28 | Hook coding with inter-rater check | Single coder only; A18 blind re-code of 5 hooks not yet done. | Treat F-a19-003 as a coarse tendency; schedule the A18 check. |
| 2026-11-28 | Infer "what works" from the dataset | Not valid: no view/retention data supplied; dataset chosen by recency, not popularity. | Every retention claim stays HYPOTHESIS. |
