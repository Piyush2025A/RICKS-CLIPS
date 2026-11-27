# Evidence, confidence and coverage rules

## Evidence labels (every claim carries one)
| Label | Meaning | Required with it |
|---|---|---|
| `MEASURED` | Computed by a script | command, script version/commit, input checksum, n, distribution |
| `OBSERVED` | The agent actually opened and viewed the image(s) | frame IDs, logged in the visual coverage ledger |
| `INFERRED` | Reasoned from measured/observed evidence | the chain of reasoning and its evidence IDs |
| `HYPOTHESIS` | Not yet tested | what would confirm or refute it |
| `H-UP` | Hypothesis taken from the upstream repo (`mromidev/claude-animated-shorts` @ `e3b817b`) | the upstream file/section |
| `SOURCE` | External documentation or research source | URL, access date, quote |

## Confidence
`high` (consistent across ≥ 2/3 of dataset videos, n ≥ 20, method validated), `medium` (consistent but small n or
method partly validated), `low` (few samples, method unvalidated, or contested). Always give the reason.

## Frame and evidence IDs
- Video key: `RC30-<nn>` where `nn` = 01..30 by publication date, newest = 01, fixed by `MANIFEST.json`.
- Frame ID: `RC30-<nn>-f<NNNNNN>` = zero-based decode index at native frame rate; every record also stores
  `pts_time` (seconds, from ffprobe) so timestamps are preserved.
- Range: `RC30-07-f000120..f000180` (inclusive).
- Audio time: `RC30-07-t12.340` (seconds from stream start).
- Our renders: `OUR-<production>-<render-id>-f<NNNNNN>`.
- Experiment: `EXP-<agent-id>-<YYYYMMDD>-<nn>`; finding: `F-<agent-id>-<nnn>`.

## Coverage honesty
- **Computational coverage** (`coverage/computational/<analysis-id>.jsonl`): one record per video per analysis:
  frames expected, frames processed, missing frame IDs, script version. 30 fps footage must reach 100% or list every
  missing frame with the reason.
- **Visual inspection coverage** (`coverage/visual/<agent-id>.jsonl`): one record per image actually opened (frame,
  sheet or strip) with the frame IDs it shows, the agent, the date and the purpose. A contact sheet covering 60
  frames counts those 60 frames as viewed *at sheet resolution* — record the resolution.
- Never write "inspected every frame" unless the visual ledger proves it.

## Contradictions
Record both sides with their evidence, label which is stronger and why, and escalate when a decision depends on it.
Never average contradictory findings into a single number.
