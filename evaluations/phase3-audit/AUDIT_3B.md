# Phase 3B independent re-audit (A28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · auditor A28
(`a28-independent-visual-evaluator`). A28 authored none of the audited findings and was not told expected outcomes.
Status: **COMPLETE for Tier 1 (10/10 re-graded), PARTIAL for Tier 2 (13 findings checked), short Tier 3.**

Grades: VERIFIED / PARTLY / NOT SUPPORTED / UNCHECKABLE. Label rules: `knowledge/_system/EVIDENCE.md`.
Scripts (private, v0.1, run with `.venv-analysis/bin/python -I`), in
`~/ricks-clips-private/analysis-data/rc30/agents/a28-independent-visual-evaluator/scripts/`:
`c6_push.py` (ORB similarity scale on push start/end natives), `c7_rederive.py` (A27 colour p1/p5, caption geometry,
A22 bed table), `c8_a20.py` (A20 rate, own caption-onset vs A27 `onset_strength` cross-correlation, 40 circular nulls),
plus inline one-off re-derivations (commands not saved as files: kappa, A03/A10/A12/A16/A02 table medians — each is a
median/IQR over the committed CSV/JSON named in the row).
Visual ledger (`knowledge/dataset/coverage/visual/a28-independent-visual-evaluator.jsonl`): **8 records, 3B added 7**:
5 every-frame crossfade strips (5 videos), 1 sheet of 4 native head crops, 1 sheet of 4 native frames at f300.
Videos with A28 visual evidence across 3A+3B: 01, 02, 03, 04, 05, 09, 18, 20, 22, 24, 30 (11). Everything else below is
computational re-derivation, not visual inspection. The 16 native push frames in `nat/` were processed by script only
(not viewed in 3B).

## Tier 1 — re-grades of the 10 non-verified 3A claims
| # | Claim (3B evidence) | 3A grade | 3B grade | A28 evidence | Label check |
|---|---|---|---|---|---|
| 3 | A15 crossfade 6 f (F-a15-101) | UNCHECKABLE | **PARTLY** | Table re-derived exactly: n = 263, 29 videos, median 6, IQR 5–7, 65.4 % in 5–7 f. OBSERVED, every frame, 5 random XFs (seed 28, 5 videos): my visible-blend length vs A15 — RC30-04 f360: 7 vs 5 (blend f361–367); 24 f712: 6 vs 6 (f714–719); 05 f564: 6 vs 4 (f566–571); 18 f972: 9 vs 8 (f973–981); 20 f693: 9–11 vs 7 (f695/696–704/705). A28 median 7 f, **A28 − A15 = +2 f median (range 0..+4), never shorter**. Supports A15's own caveat that subsampled-tile reading under-reads by 1–3 f | medium correct. Rule should read "typical 6–8 f visible (alpha-fit 10 f upper bound)", default 7 f rather than 6 f. n = 5, low power |
| 4 | A13 push magnitude (F-a13-100/101) | VERIFIED arithmetic / magnitude unvalidated | **VERIFIED (medium)** | Independent method (ORB 4000 + ratio 0.8 + RANSAC partial affine, caption band masked, 540x960, frames start and end) on my 8 extracted pairs: 15 failed (8 inliers); 03 f903–969 −3.9 % (A13 itself flags it as not a push, character shrinks — confirmed); 6 usable: direct/Zc ratios 1.77, 1.03, 1.15, 0.91, 0.29, 0.95 → **median 0.99**; direct/Z(sum) median **1.24** (A13: 0.99 and 1.21). Spread is large (RC30-29 f35–64: 6.9 % vs 23.9 %; RC30-02: 78 % vs 44 %), consistent with A13's ±20 % parallax caveat (I would say ±30–70 % per move). Sample overlaps A13's, method independent | medium OK; per-move values are noisy, medians robust |
| 8 | A22 no ducking (F-A22-102) | UNCHECKABLE | **VERIFIED within stated scope** | `bed_level_3B.csv` re-derived: bass 30–90 voiced−pause +1.23 dB (IQR −0.21..+2.54), ≤ −2 dB in 2/30; side 400–2000 +0.80 (−0.07..+1.60), ≤ −2 in 1/30; paired bass median +2.10. Matches text. Mid speech-band duck < 3 dB remains untestable — A22 now states this scope | medium-high only for bass/side; the rule "no sidechain duck" is INFERRED for the speech band |
| 10 | A14 caption band (A11 fix to 0.70) | PARTLY | **VERIFIED** | `caption_frames.csv` (director tool, every native frame, 30/30): per-video median caption centre **0.7026 H** (IQR 0.7026–0.7030, max 0.7057). A11 now states 0.70 | high OK |
| 14 | A11 black p1 (F-a11-101) | PARTLY | **VERIFIED** | A27 `color.csv` 30/30: per-video median p1 **18.5/255** (IQR 10–24.75, range 1–33), p5 32.5 (25.75–40.75). A11: 18 (10–25), p5 32. 0.099 correctly SUPERSEDED | high OK (30 videos, A27 validated table) |
| 15 | A10 outline width (F-a10-101) | UNCHECKABLE | **VERIFIED (arithmetic) + consistent by eye** | `ink_scan5_heads.json`: 80 heads, 26 videos, median 9.33 px (IQR 6.88–12.08), 3.68 % HW (2.72–4.93), per-video median 9.24 — exact. OBSERVED 4 random heads (seed 15) at native: my eye estimates ≈ 10–11 px (01-f839, A10 9.7), ≈ 5 (02-f959, A10 4.5), ≈ 8 (09-f269, A10 7.7), ≈ 7.5 (22-f659, A10 6.8): within ±1.5 px. Hats/caps outlined as part of the character in all 3 headgear heads (agrees F-a10-102) | medium-high acceptable; eye check n = 4 |
| 16 | A02 swap timing (F-A02-101) | PARTLY | **VERIFIED as table; label correct** | `expression_events_3b.csv`: 56 rows, 26 videos; inbetween 0 in 45, 1 in 1, blank in 10 (hold controls) → 45/46 as stated. Not re-viewed by A28 | medium correct (was "high" in 3A — now fixed) |
| 17 | A07 DOF share (F-a07-100..102) | UNCHECKABLE | **PARTLY** | 53/581 = 9.1 % (≥ 2.5 px) consistent with `frame_maxsigma.json` structure (re-count not completed). A07 itself shows the metric does not separate blur from flat/hazy content (control 2.8 px) → 7–9 % is an upper bound for metric-defined softness, and the 22 % visual count remains a recorded contradiction. Not re-viewed | "medium for order of magnitude, low for share" is correct |
| 18 | A19 hook archetypes (codebook) | UNCHECKABLE | **NOT SUPPORTED as a single-label scheme; two-axis replacement VERIFIED** | My own Cohen's κ from coder CSVs: V primary Po 0.933, **κ 0.891**; D (A 0–1.6 s vs B `D16_primary`) Po 0.70, **κ 0.566** — reproduces 0.89/0.57. A19 primary matches blind coders 12–14/30 | two coders, both LLM agents: V medium, D low-medium |
| 19 | A19 quick-cut opener 19/30 (A16 F-a16-103/104) | PARTLY | **PARTLY (re-defined)** | `openers_3b.csv`: eye edits ≥ 1 in 12/30 (A15 table 11/30), beats ≥ 1 in 25/30, beats median 1.5, caption at f0/f1 28/30 — all as stated. "Quick-cut" is false as *cuts* (12/30); true as *visual beats*. Director's RC30-10 check makes A15 30/30 | medium OK for the beat/edit split; A19 "quick-cut" wording must be retired |

## Tier 2 — new 3B findings checked (13)
| Finding | Grade | A28 evidence |
|---|---|---|
| A03 F-a03-101 head H/W 0.933 | VERIFIED | `ratios_3b_characters.csv`: n = 34, median 0.9335, 19 videos. "medium (19 < 20 videos)" correct |
| A03 F-a03-102 height 3.27 HH | PARTLY (minor) | table all-type height_HH n = 29, median 3.234; text says hatless non-robe n = 28 → 3.27. Filter not reproducible from the column set alone; difference 0.04 HH, immaterial |
| A03 F-a03-103 leg/torso 1.38 | VERIFIED | own ratio leg_HW/torsoL_HW: n = 56 (text 54), median 1.380 |
| A20 F-A20-101 220 wpm | VERIFIED (arithmetic) | `narration_stats_3b.csv` wpm 220.55 (214.4–227.5); recomputed words/span 220.5. It is caption-word rate over the full span (includes pauses); "high" acceptable for that definition only |
| A20 F-A20-104 caption leads speech ≈ 140 ms | VERIFIED (independent code) | `c8_a20.py`: all caption starts (pts (f+1)/30, confirmed frame 0 pts = 0.0333 in `frames.csv`) vs A27 `onset_strength`: per-video peak lag **median 145 ms (IQR 130–160)**, range −240..+210, z median 3.3, z ≥ 3 in 19/30. Same table input as A20's estimate (b), different code and event set (all captions, not sentence starts) |
| A21/A22 bed −20 dB re VO | PARTLY (definition choice) | `bed_level_3B.csv` mid 400–2000 voiced−pause: A 14.4, B 14.8, strict C **20.6** (19.9–21.8), pause P10 floor 24.8. −20 is the strict-pause value; −15 is the mean-pause value. Both reproduce; the single target is INFERRED medium, as A22 labels it |
| A16 F-a16-101 two-unit shot length | VERIFIED | `shots_two_units_3b.csv`: 379 edits; per-video edit median 3.05 s (2.74–4.07), 2.15 edits/10 s, beat B 2.85 s / 2.57, beat C 4.21/10 s — all exact. Tier C precision unknown (A16 says so) |
| A16 F-a16-103 openers | VERIFIED | see #19 |
| A12 luma bumps | VERIFIED (arithmetic) | `luma_bumps_3B.csv`: n = 80, 27 videos, Δ median 15.8 (12.7–20.8), duration median 6 f but **IQR 2.75–22 f** (bimodal-looking; "6 f" should not be used as a fixed bump length) |
| A02 F-A02-101 | VERIFIED (table) | see #16 |
| A10 F-a10-101 | VERIFIED | see #15 |
| A09 F-A09-105 vs A10 F-a10-102 treatment split | **CONFLICT — partly each** | see below |
| Hook κ (codebook) | VERIFIED | see #18 |

### A09 F-A09-105 vs A10 F-a10-102 (OBSERVED, low: 1 frame per video, 4 videos at f300, 405x720)
They classify different axes (A09 lighting rendering; A10 ink on scenery/props) but A09 also asserts "illustrated
videos use ink on props", which collides with A10's "A = no scenery ink" for 18, 24, 30.
- RC30-18 f300: painterly/flat soft light (A09 "illustrated" supported) with no visible scenery ink (A10 "A" supported).
- RC30-24 f300: stylised but lit 3D-looking terrain, bridge and water, no ink on scenery (A10 supported; A09 "illustrated" doubtful).
- RC30-30 f300: dark interior with spotlight pool and shaded floor/props, no scenery ink (A10 supported; A09 "illustrated" not supported at this frame).
- RC30-09 f300: flat pink set, character outlined, window bars drawn; consistent with A10 "mixed", A09 "lit-3D" doubtful.
- A09's own list is internally inconsistent: 02 and 11 are in both "lit-3D 01–14" and "mixed".
**Evidence-supported reading:** ink-on-scenery (A10) and painted-vs-lit light (A09) are independent per-video switches;
A09's coupling "illustrated ⇒ inked props" is NOT SUPPORTED for 18/24/30. A11 F-a11-102 (no grade difference) used
A09's groups; its conclusion does not depend on which split is used but should name the axis. Needs a joint
2-axis per-video label from more than 1 frame per video (owners A09 + A10).

## Tier 3 — ledger honesty (record counts and videos parsed from each `.jsonl`, regex `RC30-nn`)
| Agent | Header claim | Ledger | Verdict |
|---|---|---|---|
| A10 | 13 records, 30/30 videos; 3A "24" corrected to 18 | 13 records, 30 videos | PASS (correction honest) |
| A15 | 122 records, 29 videos (not 27) | 122, 29 | PASS |
| A02 | 58 records | 58, 30 | PASS |
| A07 | 27 records, 30 videos | 27, 30 | PASS |
| A08 | 38 records, 29/30 (30 unseen) | 38, 29 | PASS |
| A09 | 50 records, 30/30 | 50, 30 | PASS |
| A11 | 21 records, 21 videos | 21, 21 | PASS |
| A12 | 38 records | 38, 29 | PASS |
| A13 | 12 records; F-a13-100 "pair montages, 16 videos" | 12, 18 | PASS |
| A16 | 22 records, 30/30 | 22, 30 | PASS |
| A01 | 68 records, 30/30 | 68, 30 | PASS (native 29/30 subset not checked) |
| A03 | 97 records | 97, 30 | PASS |
| A21 | 10 records (spectrogram renders), "11 videos" | 10, 12 IDs parsed | PASS (parse counts mentions) |
| A22 | 0 records | no file | PASS |
| **A20** | header line 5: "Visual ledger: 8 records" | **58 records** (8 contact sheets 3A + 50 caption-overlay records 3B, 29 videos) | **FAIL (stale header, under-claim)**; and **RC30-22 has no overlay record** although transcription claims 30/30 → either add the missing record or mark RC30-22 text as not visually logged |

## Remaining conflicts and supported side
| Conflict | Supported side |
|---|---|
| A15 visual XF 6 f vs alpha-fit 10 f | Between: A28 every-frame reads median 7 f (n = 5), +2 f over A15 → use 7 f default, 6–8 typical |
| A09 treatment split vs A10 ink split | Independent axes; A10 supported on ink for 18/24/30; A09 coupling not supported (above) |
| A07 DOF 22 % visual vs 7–9 % edge metric | Unresolved; metric is calibrated but confounded by flat/hazy cells; both are upper/loose bounds |
| A21/A22 −15 vs −20 dB bed | Definition (mean pause vs strict pause); −20 target is a choice, not a measurement conflict |
| A19 vs A16 openers | Resolved: units (beats vs edits); A16 data reproduce |
| A08 no ink on props (14 natives) vs 3A thick ink | Resolved by per-video treatment (A10); my 4 frames agree |

## Not checked (honest list)
A01 shading/eye claims (only census columns opened); A08 F-A08-103 ink (only via A10/A09 frames above); A12 effect
event timings and census; A04, A05, A06, A14, A17, A18, A21 SFX-precision findings; A07 9.1 % re-count from
`frame_maxsigma.json` (structure read, count not finished); A02 strips not re-viewed; A13 easing (F-a13-102);
A22 end swell / tempo / track (F-A22-103..105); A20 F-A20-102/103/105 (sentence stats need private text);
repeat scoring for consistency (10 % rule) — not done; missed-techniques sweep (3A task 4) — still not done; A01
native-frame subset 29/30 in ledger not verified.
