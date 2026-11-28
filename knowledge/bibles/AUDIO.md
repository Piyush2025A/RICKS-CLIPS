# Audio production bible (draft v0.3, Phase 3B)
Sources: a20 (F-A20-*, 3B F-A20-101..105), a22 (F-A22-*, 3B F-A22-100..105), a21 (F-a21-*, 3B F-a21-100..103),
calibration §1.6. Audits: AUDIT.md #6–#9, AUDIT_3B.md #8 + Tier 2.
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| A1 | Master loudness | −14 LUFS integrated (23/30 at −14.0..−14.3; 7 at −15), TP ≈ −2 dBTP, LRA 2–3 LU, not clipped | F-A20-001, F-A22-009 | H |
| A2 | Effectively mono | side −20…−32 dB under mid; L/R corr 0.996; side at AAC floor above ≈ 3.9 kHz | F-A20-002, F-a21-001/101 | H |
| A3 | Single narrator, continuous | ≈ 220 wpm (STORY S10); captions never go blank (gap 0 in 99.9 %); sentence-final caption held ≈ 5 f longer; sentence pauses ≈ 0.15–0.3 s (3A 0.3–0.5 s downgraded) | F-A20-101..103 | M–H |
| A4 | **Captions lead the voice by ≈ 4 frames** | ≈ **140 ms** (sentence-start RMS rise 110–167 ms per video on 30/30; onset x-corr +140 ms; A28 independent code 145 ms, IQR 130–160) — 3A "+70 ms" SUPERSEDED | F-A20-104, AUDIT_3B | M–H |
| A5 | Music bed throughout, static (no ducking found) | no ≥ 2 dB duck on voice-free views (bass 30–90 Hz +1.2 dB, side +0.8 dB; 30/30); a < 3 dB duck hidden in the mid speech band cannot be excluded; tonal, harmonic, mid-range, no drums; 6–10 s loops; no track changes in 30/30; a pulse is significant in only 13/30 (61–118 BPM; "≈ 100 BPM" downgraded) | F-A22-102/104/105, F-A22-001..004, AUDIT_3B #8 | M |
| A6 | **Bed level (A21 vs A22 resolved: same quantity, different pause definitions)** | mid 400–2000 Hz, voiced − pause: mean pause ≈ 15 dB (A21 15.6, A22 14.4–14.8); strict pause 20.6 dB; pause floor P10 ≈ 24.7 dB; side ≈ 27–28 dB. **Production target: bed stem −20 dB re VO stem (±3 dB) in 400–2000 Hz, static** (INFERRED choice; A28 PARTLY = definition-dependent). Master check: pauses ≈ −17.2 LUFS, voiced ≈ −13.2 LUFS | F-a21-100, F-A22-100/101, AUDIT_3B | M |
| A7 | Ending | 1.1–2.2 s end swell confirmed in 4/30 (03, 06, 08, 10); 01 and 11 disputed between A21/A22; no outro | F-A22-103, F-a21-103 | L–M |
| A8 | Mix spectrum | steep high-pass ≈ 115 Hz; +4 dB lift 4–8 kHz | F-A22-010 | H |
| A9 | SFX sparse and subordinate; no systematic whoosh on transitions | transition-locked side-channel hits 0.24 vs 0.20 shuffled control (excess mainly end fades); SFX density, level and sync **not measurable** — no detection method reached 0.7 precision (0.19–0.36) | F-a21-102/103 | L |
| A10 | No in-scene character voices; character lines narrator-read | — | F-A20-010, F-a18-006 | L |
Implementation: A20 TECHNIQUES (ElevenLabs direction: ≈ 220 wpm, short sentence pauses, loudness; word timestamps drive
captions **≈ 4 f ahead** of the voice; **no cloning of the reference narrator**); A22 TECHNIQUES T5 mix recipe (VO
−13.2 LUFS voiced, bed −20 dB re VO in 400–2000 Hz, static, master −14 LUFS / TP ≤ −2); A21 TECHNIQUES (SFX palette and
placement as design choices, not measured targets). Music/SFX: original, synthesised or licensed only; no generation or
paid assets without approval.
Open: SFX level/sync (needs stems or a better detector; template-loop bed subtraction untried); bed's mono share;
audio-side last-word-to-end.
