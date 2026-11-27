# Audio production bible (draft v0.1)
Sources: a20 (F-A20-*), a22 (F-A22-*), a21 (F-a21-*), calibration §1.6.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| A1 | Master loudness | −14 LUFS integrated (23/30 at −14.0..−14.3; 7 at −15), TP ≈ −2 dBTP, LRA 2–3 LU, not clipped | F-A20-001, F-A22-009 | H |
| A2 | Effectively mono | side −27.5 dB under mid; L/R corr 0.996 | F-A20-002, F-a21-001 | H |
| A3 | Single narrator, continuous | voice from ≈ 0.14 s; ≈ 3.3 words/s; pauses median 0.21 s, none > 0.75 s; dead air ≈ 9 % | F-A20-003/005/006/009 | M |
| A4 | Captions lead voice by ≈ 2 frames | +70 ms (n = 30, statistical) | F-A20-007 | M |
| A5 | Music bed throughout, never ducked | tonal, harmonic, mid-range (centroid ≈ 1.2 kHz), no drums; 6–10 s loops; D-minor family common | F-A22-001..005 | M |
| A6 | Bed level | ≤ −14 dB re voice (mid upper bound), ≈ −27 dB side-only; start at −20 dB | F-A22-006, F-A20-008 | M |
| A7 | Music does not follow cuts; no outro; ≈ 1 in 6 ends on a final hit | — | F-A22-007/008 | L–M |
| A8 | Mix spectrum | steep high-pass ≈ 115 Hz; +4 dB lift 4–8 kHz | F-A22-010 | H |
| A9 | SFX sparse and subordinate; no whooshes on transitions found | clear SFX in 4 videos | F-a21-003/005 | L |
| A10 | No in-scene character voices; character lines narrator-read | — | F-A20-010, F-a18-006 | L |
Implementation: A20 TECHNIQUES (ElevenLabs direction sheet: ≈ 200 WPM, pause lengths, loudness; word timestamps drive
captions and expression swaps; **no cloning of the reference narrator**); A22 TECHNIQUES (music brief, mix chain, FFmpeg
loudnorm I=−14 TP=−2 LRA≈3); A21 TECHNIQUES (SFX palette, placement rules). Music/SFX: original, synthesised or licensed
only; no generation or paid assets without approval. Open: SFX density/sync unmeasured (A21 detectors < usable precision).
