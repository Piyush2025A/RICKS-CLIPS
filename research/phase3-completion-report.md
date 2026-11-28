# Phase 3 completion report (3A overnight run + 3B completion round) — 2026-11-28
Manifest `knowledge/dataset/MANIFEST.json` SHA-256 `fc6f147a…278e06` (30 videos, 50,898 frames). Supersedes the status
tables of `research/phase3-overnight-report.md` (3A). Checkpoint log: `research/phase3b-completion-plan.md`.

## 1. Coverage (actual)
- **Computational:** 50,898 / 50,898 native frames (rcpipe v0.2.0, 3A; reused, not repeated). **New in 3B:** caption
  band of every native frame of 30/30 videos (`tools/caption_events.py`; per-frame rows = manifest frame counts, no
  mismatch) → 4,969 caption segments, all transcribed (private). Further 3B computation on native data by specialists:
  A07 blur metric on 581 native frames (30 videos), A11 black/white points on all frames (A27 tables), A13 native SIFT on
  22 pushes, A21/A22 bed levels on 30/30 native audio, A20 narration statistics on 30/30 caption timelines, A10 outline
  scans (80 heads, 26 videos), A03 landmarks (66 characters, 26 videos).
- **Visual inspection (ledger, separate):** 3A 537 records → **943 records** after 3B (24 ledgers incl. director and the
  blind coder B). Every video has visual evidence from 18–22 agents. Full every-frame viewing of a whole video exists only
  for RC30-27 (director, 3A); 3B every-frame viewing covers windows: first 3 s of 30/30 videos (A16 every 3rd frame;
  coder B every frame), expression events in 26 videos (A02), crossfades in 29 videos (A15) + 5 (A28), whole RC30-22 at
  every 5th frame (A16), push moves in 16 videos (A13). Caption crops were viewed for 30/30 videos (A20 + director
  spot-checks of 22 and 30). Records per specialist and video (matrix from `python3 tools/ledger_matrix.py --md`; a
  record = one opened image naming that video; tiles/sheets/crops included):

| Agent | records | videos | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a01-character-designer | 68 | 30 | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 2 | 3 | 2 | 2 | 2 | 3 | 2 | 3 |
| a02-facial-expression-specialist | 58 | 30 | 2 | 2 | 3 | 1 | 2 | 1 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 3 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 1 | 4 | 2 | 4 | 2 | 1 | 4 |
| a03-anatomy-proportion-specialist | 97 | 30 | 4 | 3 | 4 | 3 | 4 | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 5 | 3 | 3 | 3 | 2 | 3 | 4 | 2 | 3 | 4 | 2 | 2 | 4 | 3 | 3 | 4 | 1 |
| a04-rigging-movement-specialist | 42 | 21 | 1 | 4 | · | 3 | · | 5 | 3 | · | 3 | 3 | 1 | 1 | 2 | 3 | 2 | · | · | · | 2 | 2 | · | 2 | · | 1 | 1 | 3 | · | 1 | 1 | 1 |
| a05-3d-world-designer | 39 | 30 | 3 | 3 | 2 | 4 | 2 | 3 | 3 | 2 | 2 | 3 | 2 | 2 | 3 | 2 | 1 | 2 | 3 | 2 | 2 | 2 | 3 | 2 | 1 | 1 | 4 | 1 | 1 | 1 | 4 | 2 |
| a06-layering-2-5d-specialist | 14 | 30 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| a07-depth-perspective-specialist | 27 | 30 | 4 | 4 | 7 | 7 | 6 | 7 | 5 | 8 | 3 | 6 | 7 | 7 | 8 | 7 | 6 | 7 | 7 | 6 | 5 | 6 | 6 | 7 | 5 | 4 | 5 | 4 | 5 | 5 | 6 | 6 |
| a08-prop-texture-designer | 38 | 29 | 3 | 1 | 3 | 4 | 5 | 1 | 3 | 3 | 3 | 3 | 1 | 5 | 1 | 3 | 3 | 4 | 4 | 2 | 2 | 5 | 5 | 1 | 4 | 1 | 4 | 3 | 4 | 1 | 1 | · |
| a09-lighting-shadow-specialist | 50 | 30 | 6 | 3 | 5 | 5 | 3 | 3 | 3 | 2 | 7 | 3 | 2 | 5 | 2 | 5 | 4 | 2 | 4 | 2 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 3 |
| a10-shader-outline-specialist | 13 | 30 | 2 | 1 | 2 | 4 | 2 | 1 | 3 | 1 | 2 | 2 | 3 | 2 | 1 | 4 | 2 | 3 | 3 | 3 | 2 | 2 | 4 | 3 | 4 | 1 | 2 | 5 | 2 | 2 | 4 | 3 |
| a11-color-grading-specialist | 21 | 21 | 1 | 1 | 1 | · | 1 | 1 | 1 | · | 1 | 1 | 1 | 1 | · | 1 | 1 | · | 1 | · | 1 | · | 1 | · | 1 | · | 1 | 1 | · | 1 | 1 | 1 |
| a12-vfx-specialist | 38 | 29 | 2 | 1 | 2 | 3 | 3 | 2 | 1 | 3 | 4 | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 1 | 1 | 2 | 3 | 1 | 5 | 2 | 1 | 1 | · | 2 | 3 | 2 | 2 |
| a13-camera-director | 12 | 18 | 4 | 1 | 2 | 1 | 1 | · | 1 | 1 | · | · | · | · | · | 1 | 2 | 1 | 1 | · | · | 2 | · | · | 1 | 1 | 1 | 2 | 1 | · | 1 | · |
| a14-composition-framing-specialist | 42 | 30 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 3 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 3 |
| a15-transition-specialist | 122 | 29 | 4 | 5 | 3 | 5 | 5 | 7 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 5 | 4 | 3 | 4 | 6 | 4 | 6 | 4 | 5 | 3 | 2 | 4 | · | 3 | 2 | 3 |
| a16-editing-pacing-specialist | 22 | 30 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| a17-story-researcher-fact-checker | 32 | 30 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| a18-scriptwriter | 14 | 8 | 2 | · | · | 2 | · | · | · | · | 2 | · | · | · | · | · | · | 2 | · | · | · | · | · | · | 2 | 2 | · | · | 1 | · | · | 1 |
| a19-hook-retention-specialist | 56 | 30 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 1 | 2 | 1 |
| a20-voiceover-specialist | 58 | 29 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 3 | 1 | · | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 |
| a21-sound-effects-specialist | 10 | 12 | · | · | 1 | 2 | 2 | · | 1 | · | 3 | 3 | · | · | · | 1 | · | · | · | · | · | 1 | 2 | 4 | · | · | · | · | 4 | · | · | 1 |
| a28-independent-visual-evaluator | 8 | 11 | 2 | 1 | 1 | 1 | 1 | · | · | · | 2 | · | · | · | · | · | · | · | · | 2 | · | 1 | · | 1 | · | 2 | · | · | · | · | · | 1 |
| coder-b-blind | 30 | 30 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| director | 32 | 5 | · | · | · | · | · | · | · | · | · | 1 | · | · | · | · | 6 | · | · | · | · | · | · | 1 | · | · | · | · | 23 | · | · | 1 |
| **all** | 943 | 30 | 22 | 21 | 21 | 22 | 21 | 19 | 21 | 18 | 22 | 21 | 19 | 19 | 18 | 21 | 21 | 19 | 19 | 18 | 19 | 21 | 19 | 20 | 20 | 21 | 20 | 19 | 20 | 19 | 20 | 22 |

Ledger honesty (A28 AUDIT_3B Tier 3): 14 agents PASS; A10's 3A header ("24 videos") corrected to 18; A20's stale header
corrected by the director; A17's views (no Bash) logged by the director on its behalf, marked as such.

## 2. Newly completed research (3B) — key results
| Area | Result (finding IDs) | Conf |
|---|---|---|
| Edit lists | 30/30 videos now confirmed (A15 +140 rows for 06/09/10/11/13/21; 391 real transitions: XF 79 %, HC 9.5 %); 5 slow dissolves rcpipe missed (F-a15-100/103) | H (counts) |
| Crossfade length | 6 f by tile reads (n = 263, 29 videos); A28 every-frame reads +2 f → default 7 f (F-a15-101, AUDIT_3B #3) | M |
| Proportions | 26 videos, 66 characters: head H/W 0.933, height 3.27 HH, leg/torso 1.38 (F-a03-101..106) | M |
| Character design | census 30/30 (median 7 characters/video); soft gradient shading (not flat); ball hands; eyes = dash under brow most often; outline near-black/aubergine (F-a01-100..110) | M |
| Expressions | 46 events, 26 videos: 45 hard swaps, no in-betweens; holds ≈ 5 f; no lip/word lock in 12 shots (F-A02-101..105) | M |
| Body motion | moving bodies on ones; dialogue bodies frozen 24–48 f; 25 gestures timed; walk still n = 1 numeric (F-a04-100..104) | M / L |
| Depth | DOF metric on 581 natives: soft ≥ 2.5 px 9.1 % (upper bound), blur σ ≈ 3.6–4 px; parallax regimes; FOV ≈ 73° (F-a07-100..104) | L–M |
| Props/textures | props real 3D; ≈ 3 hero props/video; grain only on grass/gravel/lattice; material table (F-A08-101..107) | M |
| Lighting | card shadows 4/30 (per-scene switch, default off); key/fill ≈ 7:1 (n = 15 pairs); cards receive light (F-A09-101..104) | M / L–M |
| Ink / outline | 9.3 px = 3.68 % HW (80 heads, 26 videos; A28 VERIFIED); scenery ink A 20 / B 6 / mixed 4; line scales with card (F-a10-101..104) | M |
| Grade | native p1 0.071 on 30/30; one grade across treatments; vignette 0.70 (F-a11-101..108; A28 VERIFIED) | H / M |
| VFX | luma bumps n = 80 (0.45 per 10 s); 18 effect events timed; no white-overlay flashes (F-a12-100..104) | M |
| Camera | push +23.9 % over 33 f validated on native frames (A28 independent check 0.99); smoothstep 60 %; hold 10.8 % (F-a13-100..103) | M |
| Editing | edit shot 3.18 s vs visual beat 2.85 s; openers: change in 25/30, edit in 12/30 (F-a16-100..104) | M |
| Captions / narration | 220 wpm; captions lead voice ≈ 140 ms (A28 145 ms); never blank; sentences 11 words (F-A20-101..105) | H / M |
| Hooks | two blind coders × 30: verbal κ 0.89, picture κ 0.57 (`research/phase3b-hook-codebook.md`) | M / L–M |
| Bed level | A21/A22 reproduce each other (mean pause ≈ 15 dB, strict 20.6, floor 24.7, side ≈ 27–28) → target −20 dB ±3 (F-a21-100, F-A22-100/101) | M |
| Ducking | none ≥ 2 dB on voice-free views (F-A22-102; A28 VERIFIED in scope) | M |
| SFX | bed-subtracted detection: no method ≥ 0.7 precision (0.19–0.36) → SFX density/sync not reported (F-a21-102/103) | — (failure recorded) |

## 3. Independent verification (A28)
3A audit's 10 non-verified claims re-graded in 3B: **VERIFIED 6** (#4 push magnitude, #8 no-ducking in scope, #10 caption
band, #14 black level, #15 outline width, #16 swap timing as table), **PARTLY 3** (#3 crossfade length → 7 f default,
#17 DOF share = upper bound, #19 openers true for beats not cuts), **NOT SUPPORTED 1** (#18 A19 single-label hook
archetypes; two-axis replacement reproduced). 13 new 3B findings checked: 10 VERIFIED, 2 PARTLY (A03 height filter,
bed target definition-dependent), 1 conflict analysed (A09 vs A10 treatment split). Not checked: listed in AUDIT_3B
"Not checked" (A01 shading/eyes, A04, A05, A06, A14, A17, A18, A12 event timings, A22 end swell/tempo, A13 easing,
10 % repeat scoring, missed-techniques sweep).

## 4. Disagreements
| Disagreement | Status | Basis |
|---|---|---|
| A15 vs A16 shot length | **Resolved** — two units (edit shot 3.18 s; visual beat 2.85 s) | F-a16-101, AUDIT_3B Tier 2 |
| A19 vs A16 openers | **Resolved** — A19 counted beats, A16 counted edits | F-a16-103, AUDIT_3B #19 |
| A18 vs A19 hook typing | **Resolved** — single list mixed two axes; blind two-axis coding reproducible | hook codebook, AUDIT_3B #18 |
| A21 vs A22 bed level | **Resolved** — same quantity, different pause definitions; target −20 dB is a choice | F-a21-100, F-A22-100 |
| A01 vs A03 leg length | **Resolved** — A01 now agrees (1.2–1.5×) | F-a01-104, F-a03-103 |
| A08 no prop ink vs 3A thick ink | **Resolved** — per-video scenery-ink treatment | F-a10-102, AUDIT_3B |
| A11 vs A27 black level; A11 vs A14 caption centre | **Resolved** — A11 corrected (0.071; 0.70) | F-a11-101, AUDIT_3B #10/#14 |
| A09 "cards almost exempt" vs light on cards | **Resolved** — newer, larger sample (12/16 lit) | F-A09-104 |
| A09 light-treatment split vs A10 ink split | **Partly** — independent axes; A10 supported for ink; A09 split low and inconsistent | AUDIT_3B |
| A07 DOF 22 % visual vs 9.1 % metric | **Unresolved** — both loose bounds | F-a07-100, AUDIT_3B #17 |
| A04 head bob 1.2 % vs H-UP 3–7 % | **Unresolved** (n = 1) | F-a04-100 |
| A03 height 3.27 HH vs H-UP 3.5 HH | **Unresolved** (H-UP is not evidence; measured value used) | F-a03-102 |
| A21 vs A22 end swell on 01/11 | **Unresolved** | F-A22-103 |
| A02 swap-before-word (3A) vs no word lock (3B) | **Resolved toward 3B** (larger test); 3A kept as low, non-general | F-A02-103 |
| A20 caption lead 70 ms (3A) vs 140 ms (3B) | **Resolved toward 3B** (exact caption times; A28 145 ms) | F-A20-104 |

## 5. Remaining limitations
- Walk cycle numeric n = 1; bob/lean/foot slip unmeasured (no static-camera walker found).
- SFX density, level and sync not measurable with current methods (no stems; picture events too dense for validation).
- Light-rendering treatment per video (A09) low confidence; scenery-ink label from 1–2 frames per video.
- DOF share contradictory; FOV from 13 frames; haze not re-measured; key azimuth and per-video fill ratio not measured.
- Child/animal/object proportions, eye spacing, arm length; blink rate; 3A expression vocabulary (overview-based).
- Picture-axis hook coding moderate (κ 0.57), both coders are LLM agents; no audience-retention data for any hook rule.
- A16 visual-beat tier C precision checked on one video; A13 per-move magnitudes noisy (±20–70 %).
- Video IDs/dates deferred; order rests on user attestation.
- Visual coverage is broad but partial: whole-video every-frame viewing only for RC30-27.

## 6. Implementation-ready production recommendations
See `knowledge/STYLE_BIBLE.md` §2–3 (hard QC targets) and the 9 bibles. Highest-value, best-evidenced defaults:
1. Narration ≈ 220 wpm, sentences ≈ 11 words; captions one token at 0.70 H, never blank, ≈ 4 f ahead of word timestamps.
2. Master −14 LUFS / TP −2, mono-compatible; static bed −20 dB re VO (400–2000 Hz); no ducking; one loop per video.
3. Crossfade 7 f default (79 % of joins); hard cuts ≤ 10 %; edit every ≈ 3.2 s; a visible change every ≈ 2.9 s.
4. Camera moving ≈ 2/3 of frames; push +24 % over ≈ 33 f with smoothstep; no shake.
5. Characters: head H/W 0.93, ≈ 3.3 HH tall, leg/torso ≈ 1.4, ball hands, soft gradient shading, ink 3.7 % HW
   scaling with the card; expressions as hard swaps with ≈ 5 f holds; no lip-sync.
6. Grade: p1 ≈ 0.07, soft roll-off, vignette 0.70, no grain/CA; card cast shadows off unless a scene calls for them.
7. Hooks: plain claim or paradox whose twist word lands at 3–5 s, over an act already happening or a posed character
   the words make strange; caption from frame 0–1.
Tooling for QC of our own renders: rcpipe, `tools/caption_events.py`, `src/grade/qc_grade.py`, A16 `pacing_qc.py`,
`src/transitions/a15_stats.py`.

## 7. Readiness assessment for Phase 4 (Google Flow + ElevenLabs integration)
**Ready, with caveats.** The research gives measured, audited targets for voice, captions, mix, editing, camera, grade
and character construction — enough to brief ElevenLabs (rate, pauses, loudness) and Google Flow (character sheets,
props, environments) and to QC outputs numerically. Not blocking Phase 4 but needing decisions or follow-up:
(a) user decisions — scenery-ink treatment (A majority vs B), our own character signature, where 1080p renders run;
(b) SFX rules are design choices, not measurements; (c) walk/body-motion presets rest on one walker;
(d) Phase 2.5 integration items (Flow ToS reading, ElevenLabs connector test) remain as recorded in PROGRESS blockers.

## 8. Decisions requested from the user
1. Review `knowledge/STYLE_BIBLE.md` v0.3 and the bibles; approve or correct.
2. Choose the scenery-ink treatment and the own character signature (HYPOTHESIS in CHARACTER).
3. Decide where final renders run.
4. Approve (or not) the Phase 3 gate and the start of Phase 4. **No Phase 4 work has been started.**
