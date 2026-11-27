# Camera & cinematography bible (draft v0.1)
Sources: a13 (F-a13-*), a14 (F-a14-*), a07 (F-A07-004/005/007), a05 (F-A05-002), calibration.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| K1 | Camera almost never locked off | hold 10.5 %, creep 18.6 %, move 64 % of frames (23 videos) | F-a13-001, F-A05-002 | M–H |
| K2 | Pushes dominate, usually combined with a small pan/tilt | push:pull 66:34; 66 % combined | F-a13-002 | M |
| K3 | Typical push | +22 % scale over ≈ 35 frames (1.2 s); in-shot creep +10–35 % over 1–2 s | F-a13-003, F-a14-007 | M |
| K4 | Easing | symmetric ease-in-out (smoothstep best fit 65 %, n = 74), attack ≈ 10 f; fast shot-entry moves settle with ease-out | F-a13-004/007 | M |
| K5 | No handheld or impact shake | HP RMS ≈ 0.8 px | F-a13-005 | M |
| K6 | Moves start with the shot (35–44 % within 6 f of a cut vs 15 % chance), not on words | — | F-a13-006 | M |
| K7 | Signature moves | fly-throughs, dives into eyes/objects, long corridor dollies, screen-zoom reveals | F-a13-008, F-a15-004 | M |
| K8 | Shot-size mix (first 40 s) | MS 39 %, WS 21 %, insert 14 %, CU 13 %, EWS 12 % | F-a14-001 | M |
| K9 | Face placement | x ≈ 0.48, eyes y ≈ 0.38, head height ≈ 0.21 of frame; centre third | F-a14-002 | M |
| K10 | Caption band fixed | y 0.689–0.724, centred, one line, never moves; key content avoids it | F-a14-003/004 | H |
| K11 | Safe zones | nothing key in bottom 20 %; right strip crossed only by big close-ups (zone sizes are assumptions) | F-a14-004 | L–M |
| K12 | Hierarchy devices | frame-in-frame ≥ 16/30, leading lines 13, fg occluders 12, symmetry 10, dutch 8 | F-a14-006 | L |
| K13 | Lens/height | wide feel (FOV 55–80° HYPOTHESIS), eye-level dominant, horizon ≈ 0.38 | F-A07-004/005/007, F-a13-009 | L–M |
Implementation: A13 TECHNIQUES move library (durations at 30/24 fps, smoothstep easing driven by Remotion frame); A14
TECHNIQUES safe-zone overlay spec for Remotion compositions. Limits: motion magnitudes are proxy 2-D estimates; dolly vs
zoom not separable; orbits not detectable from the 2-D model.
