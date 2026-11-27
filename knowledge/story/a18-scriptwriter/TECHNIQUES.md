# A18 TECHNIQUES — writing system for ORIGINAL scripts (from F-a18-001..009, F-a19, F-A20, F-a15/a16; medium-low)
Never reuse reference lines, stories or jokes. Every factual line needs an A17 claim ID before voice (A20).

## 1. Word budget (3.3 words/s incl. pauses; target 3.2–3.4 × D)
| Runtime | Words target | Hard range | Sentences (≈ 9 words) | Shots (≈ 3 s) |
|---|---|---|---|---|
| 45 s | 148 | 140–155 | 15–18 | 13–16 |
| 60 s | 198 | 190–205 | 20–24 | 17–21 |
| 75 s | 248 | 238–255 | 25–30 | 21–26 |
Duration estimate = words / 3.3 (report also / 3.0 and / 3.6). Must fall in D ± 2 s at 3.3.

## 2. Beat sheet (second marks; aligned with A19 T4 and A16 §1; words at 3.3 w/s)
| Beat | 45 s: t / words | 60 s: t / words | 75 s: t / words | Content rule |
|---|---|---|---|---|
| B1 Hook | 0–3 / 10 | 0–3 / 10 | 0–4 / 13 | ≤ 12 words; odd act on screen + verbal frame (two-axis, F-a18-001) |
| B2 Situation + rule | 3–9 / 20 | 3–12 / 30 | 4–14 / 33 | who, want, the rule; first irony by ≤ 15 s |
| B3 First pivot ("So …") | 9–13 / 13 | 12–18 / 20 | 14–21 / 23 | first fix/attempt |
| B4 Escalation | 13–24 / 36 | 18–33 / 50 | 21–42 / 69 | 2–3 attempts; ≥ 1 backfire; one quoted line ≤ 4 words |
| B5 Turn ("Wait"/"But") | 24–29 / 16 | 33–40 / 23 | 42–50 / 26 | reframe; new fact |
| B6 Mechanism | 29–38 / 30 | 40–52 / 40 | 50–63 / 43 | present tense; one prop/diagram with readable label |
| B7 Payoff | 38–42 / 13 | 52–57 / 16 | 63–70 / 23 | consequence in the character's world |
| B8 Button | 42–45 / 9 | 57–60 / 8 | 70–75 / 15 | callback word/prop; last word = punch noun; ≤ 0.6 s hold |
Sum 147 / 197 / 245. Mechanism must start at 50–70 % runtime.

## 3. Line-length and rhythm rules
- Median sentence 8–10 words; ≥ 25 % of sentences ≤ 5 words; ≤ 15 % > 15 words; max 20.
- Pick a mode per script: comedy (median ≈ 6) or narrative (median ≈ 12). Never 3 long sentences in a row.
- Clause ≤ 8 words (≈ one caption phrase run, ≈ one A20 pause-phrase).
- Beat heads: So / But / Then / Later / Wait. Never start a beat with "And".
- Voice: third person; past tense for the story, present for the mechanism. "You" only if the viewer can do it.
- Quoted character lines: ≤ 4 words, 1 per act, narrator-read, rendered as an on-screen reaction.

## 4. Joke rules (grounded in verified facts)
J1 fix backfires; J2 enforcer becomes victim; J3 literal reading of a rule; J4 deadpan understatement ("Problem
solved."); J5 time-skip gag (show passing time on a prop); J6 counter/sign flip at the end.
- ≈ 1 joke per 12 s (60 s → 4–5); first by 15 s; the last word carries the final irony.
- The irony must come from a verified claim. Invented visual exaggeration is allowed only if tagged `STAGING` in SCRIPT.md
  and not presented as fact. No jokes about real named people's bodies or ethnicities.
- Legend-grade facts use hedge words ("records say", "rumored", "claimed") — A17 §5.

## 5. Visual-writability checklist (gate: drawability = 100 %)
For each line: (1) the main noun or number is visible in the shot while its caption shows; (2) abstract terms get a
readable sign/label/stamp; (3) numbers are digits on a prop; (4) each fact = character action + visible result;
(5) no line depends on audio-only sarcasm; (6) props carrying a gap stay in the top two thirds (captions at ~70 %).

## 6. Caption-friendly phrasing
One word per token; 2–3 for article+noun, number+unit or short names. Avoid words > 12 letters at gap/punch moments
(put them on a sign instead). Write numbers as digits. Keep punch words at sentence end so they get their own token.

## 7. SCRIPT.md row format
`# | t_in–t_out | beat | line | words | visual (noun → shot/prop) | sign text | claim ID / status | joke type | STAGING?`
QC: total words, duration at 3.0/3.3/3.6, words per sentence (median, IQR), drawability %, joke times, mechanism %.

## 8. Example (fresh, neutral, non-RC30): "Why the fridge ruins bread" — 45 s, 148 words, ≈ 44.8 s at 3.3 w/s
All claims PENDING A17 (illustrative only; not for production until verified).
| # | t | beat | line | w | visual | claim |
|---|---|---|---|---|---|---|
| 1 | 0.0–3.3 | B1 | Tom keeps his bread in the fridge. That's why it's stale. | 11 | fridge opens on a rock-hard loaf; Tom taps it | C1 fridge speeds staling (pending) |
| 2 | 3.3–9.7 | B2 | Every Monday, Tom buys a soft loaf. Every Wednesday, he could build a wall with it. He thinks it dried out. | 21 | calendar MON → WED; loaf bricks in a toy wall (STAGING, J4) | — |
| 3 | 9.7–12.7 | B3 | So he seals it in a bag, airtight. Wednesday: brick. | 10 | bag zip; calendar WED; knock on loaf (J1) | C2 bagged bread still stales (pending) |
| 4 | 12.7–25.5 | B4 | He moves it to the fridge. Colder must be fresher. Now it's a brick by Tuesday. He weighs a slice: it hasn't lost much water. The loaf is hard but not dry. His neighbour keeps hers on the counter. Hers lasts longer. | 42 | fridge; calendar TUE; kitchen scale with digits; neighbour's soft loaf (J1) | C1, C3 staling ≠ water loss (pending) |
| 5 | 25.5–29.4 | B5 | Wait. Stale isn't dry. Stale is starch slowly turning back into crystals. | 13 | Tom freezes; sign "STALE ≠ DRY"; zoom into crumb | C4 retrogradation (pending) |
| 6 | 29.4–38.8 | B6 | Baking swells the starch into a soft gel. As the loaf cools, the starch lines back up, row by row, and squeezes the crumb hard. Cold makes it line up faster. | 31 | cutaway: gel blobs → rows of crystals; thermometer prop | C4, C1 |
| 7 | 38.8–41.8 | B7 | So the fridge was the fastest way to stale bread. | 10 | fridge wearing a ribbon "FASTEST STALER" (J6) | C1 |
| 8 | 41.8–44.8 | B8 | A few minutes in the oven: soft again. Until Wednesday. | 10 | oven glow, loaf soft; calendar flips to WED (callback, J5) | C5 reheating reverses it temporarily (pending) |
Checks: hook 11 words; first joke 5 s; jokes at 5, 11, 20, 39, 44 s; mechanism at 66 %; last word = callback noun;
sentences median 7 words (21 sentences); drawability 8/8.
