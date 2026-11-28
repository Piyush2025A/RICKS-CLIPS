# Phase 3B — research completion and quality improvement: plan and checkpoint log

Started 2026-11-28 (user request "PHASE 3 — RESEARCH COMPLETION AND QUALITY IMPROVEMENT"). Max 2 concurrent agents.
Brief: `knowledge/_system/briefs/PHASE3B-BRIEF.md`. Resume rule: a wave is done when its row says DONE with a commit.

## Pre-step
- Overnight background shells: re-checked — none alive (closed earlier; not repeated).
- Caption timeline (director, new computational evidence): `tools/caption_events.py` v0.1 — caption-band decode of every
  native frame (`-fps_mode passthrough`, frame counts reconciled against the manifest), outlined-white-stroke mask,
  IoU segmentation, one crop per caption segment on private tile sheets. Validated on RC30-27: 928/928 frames,
  95 segments, sheet 1 (60 crops) viewed: every tile one legible caption word/phrase, boundaries on word changes.
  No OCR engine is installed (none added — would need approval); text is read visually from the tile sheets.
  Private outputs only (third-party narration text is not committed).

## Waves (≤ 2 concurrent)
| Wave | Agents | Tasks | Status |
|---|---|---|---|
| 1 | A03, A15 | proportions on all applicable videos; edit lists 06/09/10/11/13/21 + crossfade-length visual check | pending |
| 2 | A01, A02 | character design across dataset; expression + transition timing (every-frame) | pending |
| 3 | A04, A07 | walks/gestures/poses/timing n ≥ 3; depth/parallax/DOF | pending |
| 4 | A08, A09 | props/textures completion; lighting/shadow verification | pending |
| 5 | A10, A11 | ledger reconciliation 24 vs 18 + missing inspections; grade uncertainties | pending |
| 6 | A12, A16 | VFX uncertainties; A15/A16 and A19/A16 disagreements (first-3-s every-frame sheets) | pending |
| 7 | A20 (×2 halves) | caption transcription + narration/timing verification | pending |
| 8 | A17 (blind coder), A21 | blind two-axis hook classification; bed-subtracted SFX | pending |
| 9 | A22, A13 | reconcile bed level with A21; camera magnitude check against native frames | pending |
| 10 | A28 | re-audit: 5 PARTLY + 5 UNCHECKABLE + new findings | pending |
| 11 | director | bibles, STYLE_BIBLE, records, completion report | pending |
A14: not re-run unless a later wave needs it (A28: ledger PASS; caption band verified).

## Checkpoint log
- Caption pass all 30 videos: 4,969 caption segments, 96 tile sheets (private), per-frame rows = manifest nb_frames for
  30/30 (no mismatch). Runtime ≈ 8–20 s per video. Wave 1 (A03, A15) launched.
- A15 DONE: 30/30 edit lists (569 rows), XF visual n=263 in 29 videos median 6 f (medium), shots n=414 median 3.17 s (upper bound).
- A03 DONE (turn-limit wrap-up): 26 videos / 66 characters measured; head H/W 0.933 (n=34), height 3.27 HH, leg/torso 1.38; eye spacing + arm length not measured.
- A01 DONE: census 30/30 (overview sheet 1), 22 native frames; shading = soft gradient (corrects 'flat'); outline near-black/warm brown; ball hands; legs SUPERSEDED → 1.2–1.5× (agrees A03 3B). Bible CHARACTER C8/C9 to update in consolidation.
- A04 DONE: walkers found 5, numeric step period still n=1 (RC30-14, 11 f); pose rate 11 segments/8 videos (ones, no twos; dialogue holds 24–48 f); 25 gestures/15 videos; bob 1.2 % (n=1) vs H-UP 3–7 % unresolved.
