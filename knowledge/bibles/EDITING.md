# Editing & transition bible (draft v0.3, Phase 3B)
Sources: a15 (F-a15-*, 3B F-a15-100..103), a16 (F-a16-*, 3B F-a16-100..104), a12 (3B F-a12-100), calibration,
director check RC30-10. Audits: AUDIT.md #1–#3/#19, AUDIT_3B.md #3/#19.
**Two units (resolves A15 vs A16):** *edit shot* = interval between confirmed edits (EDL, transition slots); *visual beat*
= interval between any major visual change incl. camera-driven scene changes without an edit (camera/scene budget).
| # | Rule | Value | Evidence | Conf |
|---|---|---|---|---|
| T1 | Crossfade is the default join | **79 %** of 391 confirmed transitions, **30/30 videos** (XF 308, HC 37, ZT 27, VB 11, FT 8) | F-a15-103 | H |
| T2 | Crossfade length | visible blend **6–8 f** at 30 fps; default **7 f** (A15 tile reads median 6 f, IQR 5–7, n = 263 in 29 videos; A28 every-frame reads run +2 f longer, median 7 f, n = 5; alpha-fit 10 f is an upper bound) → 5–6 f at 24 fps; camera keeps moving through | F-a15-101, AUDIT_3B #3 | M |
| T3 | Hard cuts rare and style-dependent | 9.5 % overall; **27 % of edits in RC30-01..08, 1.8 % in 09..30** (newest videos use more cuts) | F-a15-103 | M |
| T4 | Zoom-throughs / fly-throughs / VFX covers replace cuts at concept moments | ZT 27, VB 11, FT 8 | F-a15-004/005/103 | M |
| T5 | No white flash edits | no white-overlay flash found; luma bumps are in-shot effects | F-a15-005, F-a12-100/103 | M |
| T6 | Edit-shot length | median **3.18 s** (IQR 1.95–5.18, n = 409), per-video median 3.05 s (range 1.28 RC30-25 – 9.07 RC30-03), **2.15 edits/10 s**, ≈ 14 per video | F-a16-101, F-a15-103 (A28 VERIFIED) | M–H |
| T7 | Visual-beat length | median **2.85 s** with camera-driven scene changes (2.57 beats/10 s); ≈ 1.8 s / 4.2 per 10 s with a proxy detector (precision checked on RC30-22 only: 5.4 beats vs 1.3 edits per 10 s). 3A "RC30-22 ≥ 7 cuts/10 s" SUPERSEDED | F-a16-101/102 | M (tier B) / L (tier C) |
| T8 | Pacing flat across the runtime | act medians 2.93 / 2.95 / 3.43 s (24 videos; not re-run on 30) | F-a16-001 | M |
| T9 | Transitions land in narration pauses | blend overlaps a speech gap 65 % vs 44 % chance | F-a16-003 | M |
| T10 | Caption words are not a lock for transitions | — | F-a16-004 | M |
| T11 | **Opening 3 s (resolves A19 vs A16):** a visible change within 1–3 s in ≈ 80 % of videos (beats ≥ 1 in 25/30, median 1.5), but an **edit** in only 12/30 (median 0 edits); caption on screen from f0–f1 in 28/30; frame 0 mid-action 14, posed 16. A19's "quick-cut opener 19/30" counted beats, not cuts — wording retired | F-a16-103/104 (30/30 every-3rd-frame), AUDIT_3B #19 | M |
| T12 | Visible change at least every ≤ 3.5 s; never > 6 s of camera+cut dead time | — | F-a16-008 | L–M |
Implementation: A15 TECHNIQUES (Remotion overlap crossfade 7 f; zoom-through/iris; fly-through; VFX cover) +
`src/transitions/a15_stats.py`; A16 EDL template (edit shots) + beat budget (visual beats) + `pacing_qc.py`.
Tools: rcpipe candidates are high-recall, ≈ 61–70 % precision; misses slow same-palette dissolves (5 found in 3B) →
always confirm visually.
