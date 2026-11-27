# Phase 3 overnight run — final report (2026-11-28, ≈ 01:20–05:40 IST, with one usage-limit pause)

## Coverage (actual)
- **Computational: 50,898 / 50,898 native frames (100 %)**, all 30 videos, rcpipe v0.2.0 unchanged. Per stage:
  decode/color/edges/sharpness native 100 % ok; shots proxy 100 % ok; motion proxy 45,288 ok + 5,610 uncertain (inside
  transitions, by design); 0 failed, 0 missing. Audio 30/30 analysed (each with the 0.033 s pre-video interval flagged).
  Ledgers: `knowledge/dataset/coverage/computational/` (60 files, schema-valid); table checksums
  `knowledge/dataset/index/RC30_tables.sha256`; run report `knowledge/quality/a27-frame-analysis-specialist/PHASE3_RUN.md`.
  Batch: 29,911 s summed wall time (2 workers), 1.70 frames/s per worker, peak RSS ≤ 451 MiB, 1.7 GB private output,
  1,076 every-frame contact sheets + 56 overview sheets (private).
- **Visual inspection (separate, honest): 537 ledger records across 22 agents + director** (`knowledge/dataset/coverage/visual/`).
  Only RC30-27 was viewed frame-by-frame in full (director, 928 frames on sheets). Every other video was viewed partially
  (1 fps overviews, candidate sheets, selected native frames). Visual coverage ≪ 100 % — by design and recorded as such.

## Specialist research (all saved, committed)
| Dept | Agents | Status |
|---|---|---|
| Character | A01, A02, A03, A04 | done (A03 partial: 7 videos measured) |
| Environment | A05, A06, A07, A08 | done (A07, A08 partial) |
| Visual | A09, A10, A11, A12 | done |
| Cinematography | A13, A14, A15 (2 parts, 24 videos, 303 confirmed transitions), A16 | done (A13 23 videos) |
| Story | A17, A18, A19 | done |
| Audio | A20, A22 done; A21 partial (SFX detectors below usable precision) | |
| Engineering | A25 feasibility review (50 techniques, 12 conflicts resolved, module plan) | done |
| Quality | A27 consolidation; A28 independent audit (20 claims: 10 verified, 5 partly, 0 not supported, 5 uncheckable) | done (A28 partial) |
| Not used | A23, A24, A26, A29 — not needed for reference analysis (Phase 4+/release) | — |
Consolidation: 9 bibles in `knowledge/bibles/` + `knowledge/STYLE_BIBLE.md` (draft v0.2, A28 corrections applied).

## Unresolved issues
1. Video IDs / publication dates deferred (`IDENTITY.json`); order rests on user attestation.
2. Conflicts kept unresolved: A15 vs A16 shot length (A15 = upper bound); A19 vs A16 openers; A21 vs A22 bed level;
   A18 vs A19 hook typing (needs blind two-axis re-code).
3. Weak areas: proportions (7 videos), walk (n = 1), expression timing (n = 9), SFX model, DOF blur magnitude, camera
   magnitudes (proxy 2-D), 6 videos without confirmed edit lists (06, 09, 10, 11, 13, 21), A10 ledger header overstates
   viewed videos (24 claimed vs 18 in ledger), A19 "frame 0 posed" not evidenced.
4. Harness: many specialist Write calls for FINDINGS/TECHNIQUES/FAILED were refused ("subagents should return findings as
   text"); the director wrote them verbatim from hand-offs (noted in each file).
5. A slow-dissolve post-pass (A27) did not improve recall usefully (FAILED X-A27-011).

## Exact next steps (need user decisions)
1. Review `knowledge/STYLE_BIBLE.md` and the 9 bibles; approve or correct.
2. Decide: treatment A (lit PBR) or B (outlined painterly) for the first production; own character signature; where
   final 1080p renders run (A25: software ≈ 5–20 s/frame).
3. Optional follow-up research (no approval issues): caption-OCR timeline for all 30 (would firm up A17/A18/A19/A20),
   confirm edit lists for the 6 missing videos, blind two-axis hook re-code, more A03/A04 measurements, A21 bed-subtracted
   SFX analysis.
4. Approve the Phase 3 gate → Phase 4 (Google Flow + ElevenLabs integration). No phase beyond 3 was started.
