# Phase 3B — blind two-axis hook classification: codebook (director, 2026-11-28)

Purpose: resolve the A18 vs A19 hook-typing disagreement (A18 F-a18-001: 1/5 primary agreement; diagnosis = the
single category list mixes an on-screen dimension and a verbal dimension; A19 coded title + first 3 s, A18 coded 1–5 s).
Method: an independent coder who has **not** read A18/A19 hook labels codes all 30 videos on two separate axes from
the same fixed window. The director then computes agreement with A19 (30 videos) and A18 (5 videos).

## Window (fixed for every video)
- **Picture:** frames f000000–f000089 (t = 0–3 s) on the every-frame contact sheets
  (`~/ricks-clips-private/analysis-data/rc30/v0.2.0/RC30-nn/sheets/RC30-nn_sheet_f000000-f000047.png`, `..._f000048-f000095.png`).
- **Words:** the burned-in captions whose onset is < 3.0 s (private packet
  `~/ricks-clips-private/analysis-data/rc30/captions/hook_packet_3s.txt`); a second packet `hook_packet_5s.txt` gives
  the words up to 5 s for an optional "frame completed by 5 s" note.
- Titles are **not** used (A19 used titles; that is one source of the disagreement — coded separately below).

## Axis D — on-screen device (what the picture shows in 0–3 s; one primary, optional secondary)
| Code | Definition |
|---|---|
| D1 odd act | a character is doing something strange/unexpected (the oddness is visible) |
| D2 key object | the frame is built around a single object/prop/display (sign, counter, machine, document) |
| D3 event in progress | an ongoing event/disaster/process already under way (not a single odd act by one person) |
| D4 person/setting intro | a character or place is introduced in a neutral state (posed, nothing odd yet) |
| D5 other | none of the above (state what) |

## Axis V — verbal frame (what the words in 0–3 s do; one primary, optional secondary)
| Code | Definition |
|---|---|
| V1 claim/premise | states a fact or premise ("X did Y", "In 1920 …") |
| V2 paradox | states a contradiction or something that sounds impossible/backwards |
| V3 stakes | states a threat, cost, danger or consequence |
| V4 question | asks an explicit question |
| V5 direct address | speaks to the viewer ("you", "imagine") as the main move |
| V6 other | none of the above (state what) |

## Coding rules
- Code D from picture only, V from words only. Then a 1–5 confidence for each axis.
- Note whether the verbal frame is complete by 3 s or only by 5 s (from the 5 s packet).
- Coders must not read: A18/A19 FINDINGS, `knowledge/bibles/STORY.md`, `knowledge/STYLE_BIBLE.md`,
  `evaluations/phase3-audit/AUDIT.md`, `research/phase3*-report*.md`, this file's analysis section.

## Mapping for agreement (director)
A19's 7 categories map onto one axis each: claim/premise → V1; paradox → V2; stakes → V3; explicit question → V4;
direct address → V5; mystery object/odd act → D1 or D2; event in progress → D3. Agreement with A19 is counted on the
axis that A19's label belongs to (primary or secondary match reported separately).

## Analysis (filled in by the director after coding)
(pending)
