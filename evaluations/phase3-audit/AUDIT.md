# Phase 3 RC30 — independent evidence-quality audit (A28)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · auditor A28
(`a28-independent-visual-evaluator`). A28 authored none of the audited findings.
Status: PARTIAL (see Final status).

Grades: VERIFIED / PARTLY / NOT SUPPORTED / UNCHECKABLE. Label check against `knowledge/_system/EVIDENCE.md`
(`high` requires consistency across >= 2/3 of videos (>= 20) and n >= 20 with a validated method).
Scripts: `~/ricks-clips-private/analysis-data/rc30/agents/a28-independent-visual-evaluator/` (private; run with
`.venv-analysis/bin/python -I`). Visual ledger: `knowledge/dataset/coverage/visual/a28-independent-visual-evaluator.jsonl`.

**Final status: PARTIAL — stopped at turn limit by director instruction.** 20 claims across 13 specialists graded;
ledger honesty checked for 7 agents; conflicts listed; task 4 (missed techniques on 6 random overview sheets) NOT done.
Visual coverage of this audit: 1 ledger record (4 native frames at 540x960). Everything else below is computational
re-derivation from other agents' committed tables and A27 private tables (not visual inspection).
Scripts (private, v0.1): `scripts/c1_tables.py` (A15 shots), `c2_loud.py` (loudness), `c3_moves.py` (A13 moves),
`c4_ledger.py` (ledger vs citations), `c5_black.py` (black level), `grab.sh` (ffmpeg select by decode index).
Inputs: A15 `data/transitions_confirmed.csv`, A13 `data/moves_table.csv`, A03 `data/landmarks.csv`, A27 v0.2.0
`audio.json`/`color.csv`/`frames.csv` (26 videos available: 09, 10 in progress, 06, 13 absent at audit time).

## 1. Claim grades
| # | Agent / claim | Grade | A28 evidence | Label check |
|---|---|---|---|---|
| 1 | A15 F-a15-009 shot median 3.06 s | VERIFIED (arithmetic) | Re-derived from CSV (non-FP, merge <= 15 f, centre boundaries): n = 322 shots, 24 videos, median 3.058 s, IQR 1.837–5.117. **Error in text:** "per-video median 2.0 s (RC30-01) to 9.1 s" — RC30-25 has median 1.28 s (7 shots, one 22.6 s hold) | medium OK; it is an upper bound (A16 F-002 not re-checked) |
| 2 | A15 F-a15-001 type counts (XF 228, HC 37, ZT 23, VB 9, FT 6, FP 126) | VERIFIED (arithmetic) | CSV counts identical | "high" on 24 videos OK for counts; visual typing not re-viewed |
| 3 | A15 F-a15-002 crossfade 6 f | UNCHECKABLE here (strips extracted, not viewed before stop); alpha-fit side reproduced: n = 222 (A15 says 220), median 10, IQR 7.25–12 | **Label overclaimed:** "high" rests on n = 162 visual reads in 17 videos (< 20/30 required by EVIDENCE.md) → should be medium |
| 4 | A13 F-a13-003 push +22 % over 35 f | VERIFIED as table arithmetic; magnitude NOT validated | moves_table: 133 non-fast pushes, 23 videos, Z median 22.26 % (IQR 13.1–40.3), dur 35 f (20–54). Z is a **sum** of per-frame % (compounded ≈ +25 %). Per-video median of medians 27.5 %. 16 native start/end frames of 8 clean pushes extracted but not compared (stopped) | medium-low appropriate (proxy, no ground truth) |
| 5 | A13 F-a13-004 smoothstep in 65 % of clean moves | VERIFIED (arithmetic) | clean non-fast rows = 78 (4 unfitted) → 48/74 = 65 % smoothstep, 21 videos | medium OK; depends on A13 thresholds |
| 6 | A20 F-A20-001 −14 LUFS, two clusters | VERIFIED | A27 `audio.json` 26 videos: median −14.1, range −15.6..−14.0, TP median −2.1; −15 cluster = 18, 23, 24, 27, 28, 29, 30 exactly as stated | high OK |
| 7 | A20 F-A20-002 effectively mono | VERIFIED | Independent ffmpeg mid/side (`pan` 0.5(L±R), astats RMS): side−mid RC30-06 −20.9 dB, 03 −20.5, 13 −31.4, 22 −32.0 (A20: 06 −20.9, 03 −20.5) | high OK |
| 8 | A22 F-A22-005 no ducking | UNCHECKABLE (not re-run) | Method note: test is valid only for the side channel and the voice-free bass band; the bed's mono/mid speech-band part is untestable (A22 says so). Rule "do not duck" therefore covers the stereo component only | medium-high is generous → medium |
| 9 | A22 F-A22-009 master −14 LUFS / TP −2 | VERIFIED (input = A20, confirmed in #6) | — | high OK |
| 10 | A14 F-a14-003 caption band y 0.689–0.717 | PARTLY (consistent, not re-measured) | OBSERVED on RC30-01-f000359, -f000509, RC30-03-f000089, -f000749: single-line caption centred at ≈ 0.70 H (≈ 675/960) | high OK (44/44, 22 videos). Note A11 masks 0.60–0.76 and states centre "≈ 0.67" — A11's figure is wrong, mask still covers it |
| 11 | A03 F-a03-001 head H/W 0.93 | VERIFIED (arithmetic) | landmarks.csv front, bare-headed rows: n = 12 → median 0.930 (0.837–1.08). Only 9 distinct characters in 5 videos (priest ×3, orange ×2) → effective n < 12 | low-medium correct |
| 12 | A03 F-a03-004 legs 1.4–1.5× torso vs A01 2–3× | VERIFIED direction (landmark-based, A01 by eye) | landmark arithmetic consistent; A03 side stronger | low OK |
| 13 | A09 F-A09-001 hard card shadows only under hard key | VERIFIED (observed) + nuance | RC30-01-f000359: every card casts a hard floor shadow with its own leg silhouette. RC30-03-f000089 / f000749: no card shadow **although a campfire sits beside the cards**, and props show none either; RC30-01-f000509: none. So shadows are a per-scene switch, not physically following the strongest light | medium OK; "strong key" condition stays INFERRED |
| 14 | A11 F-a11-001 blacks lifted, p1 0.099 | PARTLY (direction yes, magnitude overstated) | A27 native color.csv (26 videos): per-video median luma_p1 **18/255 = 0.071** (IQR 10–26 = 0.039–0.10), p5 0.124. A11's 270-px area proxy lifts p1 ≈ +7/255 (it noted "not quantified"). Text also self-contradicts: "≈ 9/255 above the limited-range floor" while values are stated full-range | high for direction; implementation floor 0.09–0.12 too high → use ≈ 0.04–0.10 |
| 15 | A10 F-a10-001 outline 10.3 px / 3.56 % HW | UNCHECKABLE (not re-measured) | Uses A03 landmarks (same 7 videos) + A01 segmentation; 26 heads, 13 videos | medium OK; see ledger note (§2) |
| 16 | A02 F-A02-001 swaps are single-frame, no tweens | PARTLY | Ledger confirms every-frame strips for cited swaps (25 f37→38, f44→45; 30 f79→80). But frame-level evidence exists for 4 shots / 4 videos; the other 16 videos are 1 fps tiles which cannot show a tween | **"high (20/20)" overclaimed** for the swap-timing part → medium-low (construction part may stay high) |
| 17 | A07 F-A07-001 DOF minority (22 % soft) | UNCHECKABLE visually (not re-viewed) | Arithmetic: Wilson CI given correctly; consistent with calibration ("blurred foreground in two-shot") and A05-010 macro DOF because A07 itself shows C 71 %, X 29 % soft | medium OK |
| 18 | A19 F-a19-003 hook archetypes | UNCHECKABLE (single coder, no re-code) | — | INFERRED low-medium correct. **F-a19-001 implementation "frame 0 is a posed scene" is not supported**: A19 states frame 0 and t < 1 s were never viewed |
| 19 | A19 F-a19-005 quick-cut opener 19/30 | PARTLY | List "01–12" includes 06, 09, 10, 11 for which no shot table existed; counts are 1 fps judgements; conflicts with A16 F-006 (0–1 confirmed transitions in first 3 s in 23/24) | medium too high; → low until a first-3-s every-frame strip exists |
| 20 | A13 F-a13-001 hold 10.5 % vs A16 static 17 % | VERIFIED as non-conflict | different thresholds (A13 hold < 0.10 %/f scale & < 0.2 %W; A16 < 0.5 px & < 0.002) | — |

## 2. Visual-ledger honesty (script `c4_ledger.py`: frame IDs cited in FINDINGS vs ledger coverage; overview records count only frames ≡ 29 mod 30)
- **A14** (42 records, 30 videos): 22 cited refs, all covered. PASS.
- **A09** (27 records, 18 videos): native frames claimed (01, 03, 09, 04, 12, 17) all in ledger; RC30-14 f779..929 cited as "sheet" = 6 overview tiles. PASS.
- **A10** (7 records, 18 videos): cited frames covered, but header "native frames from 24 videos" ≠ 18 videos viewed; 01, 03, 05, 09, 12, 22 were measured via A01 segmentation, never opened by A10. MINOR OVERCLAIM (wording).
- **A02** (29 records, 20 videos): frame-level timing claims covered by every-frame strips; 8 cited ranges (02 f449-509, 05 f1109-1139, 09 f809-839, 10 f539-599, 13 f89-119, 13 f989-1019, 28 f89-119, 27 f89-150) are 1 fps tile spans (2–3 tiles), so "range" means "seen at both ends", not every frame. ACCEPTABLE, should be worded as tiles.
- **A13** (6 records, 4 videos): every frame range labelled OBSERVED is covered at overview/sheet level; un-viewed big moves are explicitly labelled "MEASURED candidates, not viewed". PASS.
- **A12** (28 records): uncovered refs (15-f001443, 23-f000804..805, 28-f000223) are explicitly marked "not opened". PASS.
- **A07** (22 records, 30 videos): RC30-05 f869-929 cited for tele/macro look = 3 overview tiles; RC30-09 f689 not in ledger (context not checked).
- Ledger parse limitation: regex over free text; ranges > 400 f treated as single frames; 2 false IDs (RC30-79, RC30-89) are parse artefacts.

## 3. Conflicts and which side the evidence supports
| Conflict | Evidence-supported side |
|---|---|
| A01 soft card shadows vs A06 none | A09 split (both partly right) — confirmed on 4 natives (#13); add: switch is per scene, not per light |
| A01 legs 2–3× torso vs A03 1.4–1.5× | A03 (landmark measurement vs eye estimate) |
| A03 height 2.97 HW vs H-UP 3.5 HH | A03 (H-UP is not evidence), low n |
| A15 shot 3.06 s vs A16 "upper bound; RC30-22 ≥ 7 cuts/10 s" | Unresolved by A28; A16's point is structurally valid (A15 counts only rcpipe candidates). Production rule must not treat 3.06 s as typical for long-take 3D videos |
| A19 quick-cut opener 19/30 vs A16 0–1 transitions in 3 s | Unresolved; A16 rests on confirmed edits, A19 on 1 fps judgements incl. camera moves → A16 stronger for "cuts", A19 may be measuring "scene changes" |
| A20 ducking inconclusive vs A22 no ducking | A22 for the side channel only; mid-channel ducking untested by anyone |
| A21 bed 20–30 dB under VO vs A22 ≤ −14 (mid) / −27 (side) | Not resolvable from data; both bounds valid |
| A11 black p1 0.099 vs A27 native 0.071 | A27 native (measurement at native resolution beats proxy) |
| A11 caption centre 0.67 vs A14 0.70 | A14 (native measurement) + A28 observation |
| A13 push 22 %/move vs A14 12 %/s window vs A14 eye 5–10 %/1.6 s | Different units/definitions (A13 reconciliation accepted); no magnitude ground truth exists |

## 4. Missed techniques — NOT DONE (turn limit). Incidental observation from the 4 frames viewed (OBSERVED, low):
in-world monitor showing a live second scene with other characters (picture-in-picture, RC30-01-f000359) — check
whether A05 F-A05-008 / A06 F-A06-006 cover "screen showing another scene"; not verified.

## 5. Not checked (open for a follow-up audit)
A15 crossfade length visually (strips RC30-17 f295-310, 24 f1296-1308, 20 f1439-1452, 23 f620-631, 15 f681-696 were
being extracted to the private `view/` folder, not viewed); A13 push magnitude against native start/end frames (16 frames
extracted in `nat/`, not analysed); A10 outline re-measure; A16 F-002 RC30-22 cut count; A22 ducking re-run; A04, A05,
A06, A08, A12, A17, A21, A25 claims; repeat scoring (10 %) not done; task 4 (6 random overview sheets).
