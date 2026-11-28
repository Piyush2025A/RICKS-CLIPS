# Phase 3 completion round (3B) — shared brief (director, 2026-11-28). Read fully, together with PHASE3-BRIEF.md.

Goal: strengthen the weak, partial and disputed parts of the overnight Phase 3 research. **Do not redo successful work.**
All rules of `PHASE3-BRIEF.md` still apply (dataset, private paths, ledger logging, ownership, no media in git).

## Read first
- Your own `FINDINGS.md` / `TECHNIQUES.md` / `FAILED.md` (you are extending them, not rewriting from scratch).
- `evaluations/phase3-audit/AUDIT.md` (A28 grades; fix what it says about your claims).
- `research/phase3-overnight-report.md` §Unresolved; the relevant bible in `knowledge/bibles/`.
- Your private scratch folder `~/ricks-clips-private/analysis-data/rc30/agents/<agent-id>/` (reuse earlier crops/scripts).

## Evidence that exists already (reuse; do not regenerate)
- rcpipe v0.2.0 tables for all 30 videos (all 50,898 frames): `~/ricks-clips-private/analysis-data/rc30/v0.2.0/RC30-nn/`.
- Every-frame contact sheets (48 frames each, 120×213) for all 30 videos: `.../RC30-nn/sheets/`.
- 1-fps overview sheets: `~/ricks-clips-private/analysis-data/rc30/overview/`.
- **NEW caption timeline (3B):** `~/ricks-clips-private/analysis-data/rc30/captions/RC30-nn/`
  `caption_segments.csv` (seg, f_start, f_end, t_start, t_end, crop bbox) — one row per on-screen caption (one word or
  short phrase), detected computationally on every native frame by `tools/caption_events.py`;
  `sheets/RC30-nn_cap_NNN.png` (60 caption crops per image, segment id + frame range printed).
  Text transcripts (when produced by A20) go to `.../captions/RC30-nn/caption_text.csv` (private; third-party text is
  **never** committed in full — commit only counts, timings and ≤ 10-word quotes).
- Other agents' committed `data/` tables (A03 landmarks, A15 transitions_confirmed.csv, A13 moves_table.csv, …).
- Native frames: `analysis/get_frames.py` (decodes from the start: one call per video with all frame IDs), or faster
  for a single range: `ffmpeg -nostdin -i <video> -vf "select='between(n\,A\,B)'" -fps_mode passthrough out_%04d.png`
  (`n` = zero-based decode index = our frame index).

## Rules added for 3B
1. **Time budget:** aim to finish within ≈ 60–90 minutes of work. Prefer depth on the listed tasks over new topics.
2. **No unbounded waiting.** Prefer running commands in the foreground. If you must wait for a background process,
   wait on its PID with a bound, e.g. `timeout 1800 tail --pid=<PID> -f /dev/null`. **Never** use
   `pgrep -f "<pattern>"` loops (they match their own shell and never end). Never leave a background job running when
   you return your hand-off.
3. **Coverage claims must equal the ledger.** State "videos with visual evidence" from your `.jsonl`; computational
   evidence is listed separately. Do not round up.
4. **Deliverable format:** append new findings to your files with new numbers (`F-<agent>-1NN`, a heading
   `## Phase 3B additions (2026-11-28)`), and add a `## Phase 3B revisions` section listing which earlier findings are
   corrected/downgraded/upgraded and why (old text may be left in place but must be marked SUPERSEDED where wrong).
   Update the header lines (visual-ledger record count, videos covered). If Write/Edit to your files is refused, return
   the complete new sections as text in your hand-off; the director will insert them verbatim.
5. Confidence follows `knowledge/_system/EVIDENCE.md` (`high` needs ≥ 20 videos and n ≥ 20 with a validated method).
   Unresolved remains unresolved: say so.
6. Hand-off ≤ 300 words: files changed, new/changed finding IDs, coverage numbers (from the ledger), open items.
