# A18 FINDINGS — script structure (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A18 (scriptwriter).
(Write tool refused this file; written to disk verbatim by the director from A18's hand-off.)
Visual ledger: 14 records (`knowledge/dataset/coverage/visual/a18-scriptwriter.jsonl`) — overview sheets only (180×320
tiles, 1 frame per second = f000029, f000059, … + last frame). Videos viewed: 8 — RC30-01, 04, 09, 16, 23, 24, 27, 30
(full runtime each). No contact sheets, native frames or audio opened.
Sampling limit: speech ≈ 2.85 caption tokens/s (F-A20-003) → 1-fps tiles show ≈ 35 % of tokens. Word-level numbers are
estimates from that sample, never transcriptions. Captions paraphrased; quoted fragments ≤ 3 words. 8/30 videos → no
finding reaches `high`. Hand counts: `data/caption_sample_counts.csv` (no Bash available → no script; recount from the
ledgered sheets).

## F-a18-001 Hook re-code for A19 — low agreement; re-code NOT blind (OBSERVED + MEASURED, low)
Method: tiles t = 1–5 s of RC30-04, 09, 16, 23, 30 (caption fragment + image), A19's 7 categories, one primary +
optional secondary. Contamination: A19 FINDINGS (containing these labels) were on the mandatory reading list and were
read before coding (FAILED FA-a18-001). Bias would favour agreement; agreement was still low.
| Key | A18 primary (secondary) | A19 | Primary agrees |
|---|---|---|---|
| RC30-04 | odd act: drivers steer into a lone roadside tree (paradox voiced 6–9 s) | paradox | no (A19 = my secondary) |
| RC30-09 | odd act: jail painted one exact pink, recipe note at 3 s (claim) | paradox | no |
| RC30-16 | claim: a man tells winners without scratching | claim | yes |
| RC30-23 | odd act: buying a pardon for a crime not yet committed (claim) | claim | no (A19 = my secondary) |
| RC30-30 | odd act: person holding steel balls over plates (direct address from 5 s) | direct address | no (A19 = my secondary) |
Primary agreement 1/5 (20 %); Cohen's κ ≈ 0.13 (Po 0.20, Pe 0.08; n = 5 too small to be meaningful); any-label overlap
4/5. Diagnosis (INFERRED, medium): boundary effect, not misreading. A19 coded title + first 3 s; A18 coded what is shown
and said at 1–5 s. The on-screen device is usually an odd act; the verbal frame (claim/paradox/address) comes from title
or sentence 2. Recommendation: two-axis scheme — on-screen device (odd act / key object / event in progress / person)
× verbal frame (claim / paradox / stakes / question / address) — re-coded on all 30 by two coders blind to each other.
Implementation: HOOKS.md records both axes per variant.

## F-a18-002 One spine: odd situation → attempt → backfire/escalation → mechanism → ironic close (OBSERVED, medium, n = 8)
Skeletons (own words, seconds from 1-fps tiles):
- 01 (61 s): space toilet + strict flush schedule (0–13) → rule broken at night (14–17) → ship ringed by false "stars",
  navigation lost (18–32) → "But" + mechanism: vented waste freezes to crystals (33–49) → stars vs crystals, star
  sighting is the only way home (50–61).
- 04 (59 s): lone tree, cars hit it (0–9) → "So" warning sign, crashes double (12–17) → opportunist profits (18–21) →
  "Eventually" the sheriff hits it, chops it (22–35) → stump still hit (36–43) → named effect on a road sign (44–49) →
  explanation, last word the stump (50–59).
- 09 (65 s): cell painted one shade (0–11) → stopwatch test, biggest inmate calms (12–30) → in-world "Wait,"/"Well,"
  (35–37) → spread nationwide (39–42) → overstay reverses effect (43–57) → "But" only minutes; last word the reversal (58–65).
- 16 (63 s): claim of the skill (0–5) → backstory: fired, buys cards (6–17) → investigates printing (18–22) → spends
  severance on cards (23–30) → mechanism: number grids, single-occurrence pattern (31–42) → temptation map (45–48) →
  reports it instead; official dismissive then convinced (49–60) → game pulled (61–63).
- 23 (41 s): pardon for a future crime (0–3) → pardon trade via price board (4–16) → knight buys (17–24) → later robs the
  seller (25–33) → seller protests, pardon shown (34–38) → seller sold it to his own robber (39–41).
- 24 (45 s): spear + shield claims (0–6) → 100-years-war counter (7–9) → "So both" kings buy (10–12) → week-long standoff
  (13–23) → secret question to the smith (24–33) → blueprint stamped impossible (34–37) → "So" nobody dares test (38–43)
  → counter flips to peace (44–45).
- 27 (31 s): near-miss on reels (0–4) → "So" same next door (5–8) → friend, money in (9–16) → "let's" look inside (17) →
  reel-strip mechanism (18–25) → "So" one-short is likelier than the jackpot (26–31).
- 30 (39 s): odd act in 2nd person (0–9) → "Then" the jolt mechanism (10–20) → famous user hedged "rumored" (21–23) →
  named brain state with on-screen label (24–28) → idea board, keep the idea (29–37) → loop to opening act (38–39).
7/8 have an attempt/rule that backfires or escalates before the mechanism; mechanism named/shown at ≈ 50–85 % runtime
(01 54 %, 04 75 %, 09 66 %, 16 49 %, 24 76 %, 27 58 %, 30 62 %); 23 is the exception (loophole twist, 78–100 %, no
mechanism). Agrees with F-a19-007/008, F-a17-004. Implementation: TECHNIQUES §2 beat sheet.

## F-a18-003 Sentence length ≈ 9 words median; two rhythm modes (MEASURED from sample, low-medium, n = 8, 404 tokens)
Method: per tile, does the visible token carry sentence-final punctuation (. ? !)? Share of final tokens ≈ 1 / mean
sentence length (tokens). Words = tokens × 1.16 (F-A20-003). Seconds = tokens / 2.85.
| Key | tokens | ends | tok/sentence | ≈ words | ≈ s |
|---|---|---|---|---|---|
| 09 | 65 | 14 | 4.6 | 5.4 | 1.6 |
| 16 | 63 | 13 | 4.8 | 5.6 | 1.7 |
| 27 | 31 | 5 | 6.2 | 7.2 | 2.2 |
| 01 | 61 | 8 | 7.6 | 8.8 | 2.7 |
| 30 | 39 | 5 | 7.8 | 9.1 | 2.7 |
| 23 | 41 | 5 | 8.2 | 9.5 | 2.9 |
| 24 | 45 | 4 | 11.3 | 13.1 | 4.0 |
| 04 | 59 | 5 | 11.8 | 13.7 | 4.1 |
Pooled 59/404 → 6.8 tokens ≈ 7.9 words; per-video median 7.7 tokens ≈ 8.9 words ≈ 2.7 s (IQR ≈ 5.5–9.8 tokens; range
5.4–13.7 words). Clause ends incl. commas pooled 92/404 → ≈ 4.4 tokens ≈ 5 words per clause. Modes (INFERRED):
dialogue-comedy (09, 16) ≈ 5-word sentences with short quoted lines; narrative/legend (04, 24) ≈ 13 words. Limits:
small periods at 180×320 may be missed (inflates length); 31–65 tokens/video → ±40 % per-video error. Consistent with
A16 "shot ≈ one clause ≈ 9 tokens / 3 s" and A20 pause-phrase 3.9 s (a phrase holds 1–2 sentences).
Implementation: TECHNIQUES §3 line-length rules; QC counts words/sentence in SCRIPT.md.

## F-a18-004 Connective pivots every ≈ 10–15 s; "So" dominates (OBSERVED, low-medium, n = 8, lower bounds)
"So" ≥ 8× (01 8 s; 04 12, 42 s; 16 53 s; 24 12, 38 s; 27 5, 26 s), "But" 3× (01 33 s; 09 60 s; 27 13 s), "Then" 2×
(24 17 s; 30 10 s), time jumps "Eventually"/"later" (04 22 s; 09 30 s; 23 25 s), in-world "Wait,"/"Well," (09 35–37 s).
"So" = consequence/new attempt; "But" = complication or late caveat; time-jump words open act 2/3.
Implementation: one connective at the head of each act-level beat.

## F-a18-005 Second person rare; sustained in 1/8 (OBSERVED, low-medium, n = 8)
Sustained: 30 only. Incidental: 24 "You see" (in-character), 27 "let's" (narrator invites a look inside). None seen in
01, 04, 09, 16, 23 — including 04, whose title uses "You". Agrees with F-a19-003. Implementation: default third person,
past tense for the story, present tense for the mechanism; "you" only when the viewer can do the act.

## F-a18-006 Facts are dramatised by ordinary characters acting out consequences and speaking short lines (OBSERVED, medium, n = 8)
Quoted character lines (≤ 4 words) in 6/8 (01 commander at 28 s; 09 guards; 16 official; 24 king to smith; 27 friend;
23 seller), read by the single narrator (F-A20-010). Each fact becomes an action with a visible result: recipe note +
stopwatch (09), "days since" counter + giant sign (04), crystal cloud mistaken for stars (01), number grid lighting up
(16), blueprint stamped impossible (24), reel strip with one jackpot stop (27). Protagonists are ordinary roles with one
want. Implementation: every fact line pairs with a character action and a result prop.

## F-a18-007 Irony beat ≈ every 12 s; last caption word is the punch (OBSERVED + INFERRED, low-medium, n = 8)
≈ 32 comic/ironic beats in 404 s (judgement) → ≈ 1 per 12–13 s; first by 8–17 s in 7/8. Type: situational irony grown
from the fact (fix makes it worse; enforcer becomes victim; skill used honestly; deadpan official; time-passing gag), not
wordplay. Last caption = concrete noun or reversal word in 7/8 (01 "stars", 04 "stump", 09 "opposite", 16 "store", 23
"to him", 27 "jackpot", 30 "balls"; 24 ends over a counter flip). Agrees with F-a19-009/010.

## F-a18-008 Captions are drawable; abstract terms become signs (OBSERVED, medium, n = 8)
≈ 58 sampled tokens were concrete nouns/numbers; none lacked its referent in the same tile. Abstract terms became
readable props: road sign for the named effect (04), label for the brain state (30), "impossible" stamp (24), sin price
board (23), status screens (01), closed-game sign (16). Numbers shown as digits on counters/props (04, 09, 16, 24, 27).
Limits: 1-fps sample, 180×320. Implementation: drawability = 100 % gate in SCRIPT.md (TECHNIQUES §5).

## F-a18-009 Word budget ≈ 3.3 words/s; ≈ one sentence per shot (INFERRED, medium)
From F-A20-003: 31 s ≈ 100 words, 45 s ≈ 150, 60 s ≈ 200, 75 s ≈ 250. With A15 median shot 3.06 s and median sentence
≈ 2.7 s, a shot holds ≈ 1 sentence (≈ 10 words). Pauses ≤ 0.5 s (F-A20-005) → no silent holds > 0.6 s except the
button. Implementation: budgets in TECHNIQUES §1.

## Contradictions
1. Hook typing A18 vs A19 (F-a18-001): 1/5 primary agreement; both kept. Category list mixes two dimensions; treat
   F-a19-003 counts as low until a two-axis blind re-code. Escalated.
2. Unit gap (not contradiction): sentence ≈ 2.7 s vs A20 pause-phrase ≈ 3.9 s.

## Open requests
A27/A20: full caption OCR timeline for 30 videos (replaces sampled F-a18-003/004). A19/A28: two-axis blind hook re-code.
