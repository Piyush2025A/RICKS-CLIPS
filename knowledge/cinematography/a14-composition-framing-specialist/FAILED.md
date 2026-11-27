# A14 FAILED approaches and limits
1. Caption x-extent from a white-with-black-neighbour pixel mask: merged with white scene objects (e.g. RC30-01-f000029 width 0.41-0.73, RC30-18-f000989 left 0.14), so horizontal extent/centring is unreliable. Only y values are reported as MEASURED; x is OBSERVED.
2. Global-motion scale from motion.csv as in-shot zoom: proxy resolution, parallax and crossfade frames inflate it (median 12 %/s versus ~5-10 % per 1.6 s seen on sheets). Reported as upper bound.
3. Saliency: cv2.saliency availability was not checked; a numpy spectral-residual substitute was used. Aid only.
4. Overview sheet page 2 (t > 40 s) not viewed because of the image budget and turn limit; shot-size tally covers about 60-65 % of runtime for videos 1-22.
5. Native frame extraction was slow (about 1.5 min per video under shared CPU); only 44 frames/22 videos, chosen where a face is visible (selection bias toward close shots). v0.2.0 every-frame sheets existed for only 8 videos (15, 23-28, 30).
6. vlog frame ranges were first written as "A..RC30-nn-B"; corrected with sed to the EVIDENCE.md format.
7. Not done: controlled head-top experiment (0.25 vs 0.35), no EXP record created; no saliency/safe-zone script committed (described in TECHNIQUES.md only).
