# Camera & cinematography bible (draft v0.3, Phase 3B)
Sources: a13 (F-a13-*, 3B F-a13-100..103), a14 (F-a14-*), a07 (F-A07-004/005/007, F-a07-104), a05 (F-A05-002),
calibration, director caption tool. Audits: AUDIT.md #4/#5/#10/#20, AUDIT_3B.md #4/#10.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| K1 | Camera almost never locked off | hold **10.8 %** (IQR 8.4–14.4), creep 19.7 %, move 66.6 % of frames (30 videos, 767 moves) | F-a13-103 (extends F-a13-001) | M–H |
| K2 | Pushes dominate, usually combined with a small pan/tilt | push:pull ≈ 2:1; ≈ 66 % combined | F-a13-002 | M |
| K3 | Typical push | total scale change **+23.9 %** (IQR 10–46 %) over ≈ **33 f** (n = 181, 30 videos); pull-outs 14.3 % (n = 88). Validated on native frames (SIFT, 22 pushes/16 videos; A28 independent ORB check median ratio 0.99). 3A "+22 % (summed proxy)" SUPERSEDED. Per-move error ±20–70 % under parallax; 15–20 % of proxy "pushes" are not camera pushes (character scale, reveals) | F-a13-100/101, AUDIT_3B #4 | M |
| K4 | Easing | symmetric ease-in-out: smoothstep best fit **60 %** (n = 96, 30 videos; native curves 75 %, peak speed at 0.43 of the move); ease-out is a minority | F-a13-102 (revises 65 %) | M |
| K5 | No handheld or impact shake | HP RMS ≈ 0.8 px | F-a13-005 | M |
| K6 | Moves start with the shot, not on words | no evidence of word-locked move onsets (30 videos) | F-a13-006/103 | M |
| K7 | Signature moves | fly-throughs, dives into eyes/objects, long corridor dollies, orbits/pull-backs that change the scene without an edit (e.g. RC30-10 f48–95) | F-a13-008, F-a15-004, F-a16-101 | M |
| K8 | Shot-size mix (first 40 s) | MS 39 %, WS 21 %, insert 14 %, CU 13 %, EWS 12 % | F-a14-001 | M |
| K9 | Face placement | x ≈ 0.48, eyes y ≈ 0.38, head height ≈ 0.21 of frame; centre third | F-a14-002 | M |
| K10 | Caption band fixed | centre **0.703 H** (per-video IQR 0.7026–0.7030, every native frame of 30/30 videos), band 0.689–0.724, centred, one line, never moves | F-a14-003, director `caption_frames.csv`, AUDIT_3B #10 | H |
| K11 | Safe zones | nothing key in bottom 20 %; right strip crossed only by big close-ups (zone sizes are assumptions) | F-a14-004 | L–M |
| K12 | Hierarchy devices | frame-in-frame ≥ 16/30, leading lines 13, fg occluders 12, symmetry 10, dutch 8 | F-a14-006 | L |
| K13 | Lens/height | vertical FOV ≈ 73° (13 frames, 7 videos), eye-level dominant, horizon ≈ 0.38 | F-a07-104, F-A07-004/005/007 | L–M |
Implementation: A13 TECHNIQUES move library (push +24 % over 33 f @30 ≈ 26 f @24, smoothstep driven by Remotion frame);
A14 TECHNIQUES safe-zone overlay. Limits: dolly vs zoom not separable; orbits poorly captured by the 2-D model; per-move
magnitudes noisy (medians robust). A14 was not re-run in 3B (ledger PASS; caption band independently verified).
