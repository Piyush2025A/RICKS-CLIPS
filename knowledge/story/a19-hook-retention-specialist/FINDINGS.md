# A19 FINDINGS — hooks & retention (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A19.
(Written to disk verbatim by the director from A19's hand-off; the agent's Write tool refused this file.)
Visual ledger: 56 records (`knowledge/dataset/coverage/visual/a19-hook-retention-specialist.jsonl`): overview page 1 for
all 30 + page 2 for 26 (180×320 tiles, 1 fps). Videos RC30-01..30.
Coverage limits: overview resolution only (f000029, f000059, … every 30th frame + last tile); frame 0 and t < 1 s NOT
viewed; contact sheets (15, 23, 25, 27, 28, 30) not opened. Captions visible ≈ 1 word per sample → opening lines and
"But/So/Wait" pivots are partial (lower bounds). Hook typing single-coder (A18 blind re-code of 5 hooks owed).
Retention is never measured — every retention statement is HYPOTHESIS. Computational data: shot_candidates.json for
RC30-25, 27, 30 only; no audio tables. Captions paraphrased.

## Format (OBSERVED, high, n = 30)
All 30 are single-narrator animated explainers of one curious fact, dramatised with stick-body characters in 3D-ish
sets, with burned-in word-by-word captions in the lower third from t ≤ 1 s. Durations (last tile): 30.9 (27), 34.4 (25),
39.1 (30), ~40 (28), 40.6 (23), 45.0 (26), 45.1 (24), 47.1 (29), then 22 videos at 55.3–77.8 s (longest RC30-15).
Median ≈ 60 s.

## F-a19-001 Story already running at t = 1 s (OBSERVED, high, n = 30)
30/30: no title card, logo or static establishing hold at 1–3 s (f000029/f000059/f000089 of all 30). Implementation:
first spoken word at 0–0.5 s, caption from word 1, frame 0 is a posed scene.

## F-a19-002 Title subject on screen within 3 s (OBSERVED, medium-high)
28/30. Exceptions: RC30-12 (mirror not seen until ~16 s), RC30-30. Titles from embedded metadata, unconfirmed against
YouTube. Implementation: storyboard rule "title noun in shot 1 or 2", unless the noun is the answer to the gap.

## F-a19-003 Primary hook archetypes (INFERRED, low-medium, n = 30; title + first-3-s fragment)
claim/premise 7 (01, 08, 16, 22, 23, 27, 29); mystery object/odd act 7 (05, 06, 11, 13, 15, 20, 21); paradox 5 (04, 09,
19, 24, 26); stakes 5 (03, 10, 12, 17, 28); event already in progress 3 (02, 07, 18); direct address/"imagine" 2 (14,
30); explicit question 1 (25). Boundaries overlap — coarse tendency. Robust: no greeting/channel intro in any opening;
second-person openings are a minority.

## F-a19-004 Sound-off readable gap (OBSERVED, medium)
≈ 20/30 carry the open gap in readable in-world text or a counter: 01 "no flushing"/"off course" signs; 04 days-since
counter and arrow sign; 09 paint note and stopwatch; 13 stopwatch; 24 years-at-war counter; 28 wrist timer and
blueprint; 16 scratch grids; 05 headline; 29 floor panel (e.g. RC30-04-f000389..f000419, RC30-24-f000209..f000269,
RC30-13-f000749..f000779). Implementation: one readable prop per gap, built as a textured plane or Flow prop.

## F-a19-005 Two opening staging modes (OBSERVED, medium; MEASURED for 3)
Quick-cut opener 19/30 (2–3 shots in t = 1–3 s): 01–12, 17–22, 26. Stage opener 11/30 (one set, slow camera, acting):
13, 14, 15, 16, 23, 24, 25, 27, 28, 29, 30. MEASURED (shot_candidates, proxy 160 px, candidates only): first transition
RC30-25 f000118 (3.97 s), RC30-30 f000114 (3.83 s), RC30-27 f000248 (8.3 s). Stage openers skew to the short "idea"
videos. Which mode holds attention better is untested (HYPOTHESIS).

## F-a19-006 Face at t = 1 s (OBSERVED, medium)
A face-bearing character is visible at t = 1 s in 23/30; object-only/macro in 7/30 (03, 05, 14, 15, 19, 21, 11
borderline). Macro opener used when the object is the hook.

## F-a19-007 Pivot words (OBSERVED, low-medium; lower bounds)
Caught in 12/30 at 1 s sampling: 01 "So" 8 s, "But" 33 s (54 %); 02 "Even if" 8 s, "Still" 18 s, guards realise
42–52 s (76 %); 03 "But the" 11 s, thunder mechanism 44–55 s (75 %); 04 "So" 12 s, "Eventually" 22 s, "So… fixation"
44 s (74 %); 07 "because" 7 s, "but" 39 s, last word "invented" 61–62 s; 08 "So, of" 7 s, "But" 40 s (63 %); 09 "Wait"
35 s, "Well" 37 s; 12 "Wait" 10 s, wire reveal 49–50 s; 17 "Wait" 36 s, "Well" 37 s (60 %); 24 "So both" 12 s; 26 "Yet"
2 s, "but" 13 s. Pattern: first pivot ≈ 10–18 s; mechanism turn ≈ 55–75 % of runtime; payoff in the last 8–15 %. Pivot
often voiced by an in-world character ("Wait,"/"Well," in 09, 12, 17).

## F-a19-008 Late answer as a mechanism visual (OBSERVED, medium, n = 8 clear)
Answer to the title question arrives at ≈ 55–75 %: 01 vent spray freezing, 04 road POV, 08 loop shapes, 09 paint chart,
12 telegraph wire, 21 pendulum cross-section, 24 blueprint, 29 coin grid. Gap stays open ≈ 35–45 s of a 60–65 s video
(HYPOTHESIS that this holds the first 30 s).

## F-a19-009 Ending types (OBSERVED, medium; overlapping; 5 end tiles mid-gesture)
Mushroom-cloud/explosion gag on the last beat 4 (03, 06, 08, 10; 11 small blast) — HYPOTHESIS: laugh-out for physics
topics; reproduce only if originally motivated. Title concept named in the last 1–2 captions 7 (01 "stars", 04 "stump",
07 "dashcam invented", 19 "forever", 21, 25, 28 "in slow motion"). Ironic counter/sign flip 3 (24 years-at-war → days of
peace, 13, 26 "gambling: none"). Character-state reaction close 14 (02, 05, 09, 12, 14, 15, 16, 17, 18, 20, 22, 23, 27, 29).

## F-a19-010 Loop / bookend (OBSERVED, medium)
Strict visual loop 4/30 (same set + composition, one state changed): 13 button (f000089 vs f001964), 25 same man pain →
calm (f000029 vs f001032), 27 man at slot machine (f000029 vs f000927), 30 chair and steel balls with "holding… balls"
at both ends (f000029 vs f001171). Prop/set callback 7/30: 24 war counter, 29 magnifier, 18 clerk at counter, 28 tower,
04 tree → stump, 12 laughing room → nobody laughing, 21 jar. Linear, no callback 19/30. Implementation: end on a
match-cut to the frame-0 composition with one changed state variable; reuse an opening word in the last caption.

## F-a19-011 Three-act shape (INFERRED, medium)
Act 1 (0–~15 s): hook, situation, rule. Act 2 (~15–40 s): escalation through 2–3 complications/attempts (02, 05, 11, 13,
22). Act 3 (last 15–25 s): mechanism reveal, consequence, punch.

## F-a19-012 Exceptions (OBSERVED, medium)
22 ladder/levels structure, no single protagonist; 25, 27 shortest, mechanism-tour structure, close on the opening
character; 15 longest, nested second story; 12 delays the title noun (mirror) to the reveal; 14, 30 second-person /
hypothetical framing.

## Contradictions
None between evidence sets.

## Open requests
A27: first-3-s strip for all 30 (frame 0 and first visual change), audio first-voiced-onset table for all 30, OCR
caption timeline for true re-hook counts. A18: blind inter-rater re-code of 5 hooks. A28: independent hook review.
