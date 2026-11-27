<!-- owner: <agent-id> | status: draft | version: 0.1 | last_updated: YYYY-MM-DD | evidence_basis: MANIFEST sha256 <...> -->
# <Topic> — research report (<agent-id>, YYYY-MM-DD)

## Question
What exactly is being measured or decided, and why (link to brief).

## Data
- Dataset: RC30, manifest sha256 `<...>`; videos used: `RC30-..` (all 30, or list exclusions with reasons).
- Shared tables used (A27): `<table>` v`<script version>`.
- Computational coverage record: `coverage/computational/<analysis-id>.jsonl`.
- Visual inspection record: `coverage/visual/<agent-id>.jsonl` (entries `<range>`).

## Method
Commands/scripts (path + commit), parameters, thresholds, exclusions (captions, blur, transitions).

## Results
| Metric | n | median | IQR / distribution | per-video spread | label | confidence |
|---|---|---|---|---|---|---|

Evidence IDs for every row.

## Contradictions and uncertainty
Including comparison with `H-UP` upstream claims (confirmed / refuted / inconclusive).

## Limitations

## Implications for production
Proposed rules (still `HYPOTHESIS` until an experiment passes).

## Hand-offs
