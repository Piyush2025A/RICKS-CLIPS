# Editing & transition bible (draft v0.1)
Sources: a15 (F-a15-*), a16 (F-a16-*), calibration, a12 (F-a12-008).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| T1 | Crossfade is the default join | 75 % of 303 confirmed transitions (24 videos) | F-a15-001 | H |
| T2 | Crossfade length | 6 frames at 30 fps (0.2 s; IQR 5–7) → 5 frames at 24 fps; linear; camera keeps moving through | F-a15-002/010 | M (A28: 17 videos visual, 'high' too strong) |
| T3 | Hard cuts rare and style-dependent | 12 % overall; 32 % in RC30-01..08, 2.5 % in 12..30 (format change over time — HYPOTHESIS) | F-a15-001/008 | M |
| T4 | Zoom-throughs / fly-throughs / VFX covers replace cuts at concept moments | ZT 23, FT 6, VB 9 | F-a15-004/005 | M |
| T5 | No flash edits | 0 of ~28 flash candidates were flashes | F-a15-005, F-a12-008 | M |
| T6 | Shot length | median 3.06 s (A28 re-computed VERIFIED from the edit list; upper bound per A16; IQR 1.84–5.12), ≈ 14 shots per video; RC30-25 median 1.28 s is outside A15's stated per-video range | F-a15-009, F-a16-002, AUDIT | M |
| T7 | Pacing flat across the runtime | act medians 2.93 / 2.95 / 3.43 s | F-a16-001 | M |
| T8 | Transitions land in narration pauses | blend overlaps a speech gap 65 % vs 44 % chance; median 2.8 f to nearest gap | F-a16-003 | M |
| T9 | Caption words are not a lock for transitions | — | F-a16-004 | M |
| T10 | Shot ≈ one clause (≈ 9 caption tokens ≈ 1 pause-phrase) | — | F-a16-005 | M |
| T11 | Opening 3 s: 0–1 transitions; opening shot 2–6 s | (contradiction with A19 "quick-cut opener 19/30" — A16 measured on edit lists; A19 judged 1 fps tiles) | F-a16-006, F-a19-005 | M |
| T12 | Visible change at least every ≤ 3.5 s; never > 6 s of camera+cut dead time | — | F-a16-008 | L–M |
Implementation: A15 TECHNIQUES (Remotion overlap crossfade; zoom-through/iris; fly-through; VFX cover); A16 EDL template +
`pacing_qc.py` (R1–R3, R5, R6 coded). Tools: rcpipe candidates ≈ 70 % precision, ≈ 96 % recall → always confirm visually.
