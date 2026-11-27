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
- Synthetic test media: `SYN-<clip-id>-f<NNNNNN>` (`dataset: "SYN"`). Synthetic media only validates tools: it is never
  part of RC30, never listed in `MANIFEST.json` (whose schema accepts only `RC30-01..30`), and never cited as reference
  evidence. RC30 records must carry `manifest_sha256`; a `SYN-`/`OUR-` key with `dataset: "RC30"` is invalid.
- Resolution: every pixel measurement states `analysis_resolution.mode` = `native` (decoded source frames, unscaled) or
  `proxy` (downscaled for speed). Proxy values are never reported as native measurements; native frames stay
  retrievable by frame ID for specialist inspection.
- Experiment: `EXP-<agent-id>-<YYYYMMDD>-<nn>`; finding: `F-<agent-id>-<nnn>`.

## Coverage honesty
- **Computational coverage** (`coverage/computational/<analysis-id>.jsonl`): one record per video per analysis:
  frames expected/processed, and counts of `ok` / `uncertain` / `failed` / `missing` frames (sum = expected, overall and
  per stage), missing/failed frame IDs with reasons, pipeline version, config fingerprint, input SHA-256 (schema v2).
  30 fps footage must reach 100% processed or list every missing frame with the reason. "Uncertain" is still
  computational coverage; it is not visual inspection.
- **Audio computational coverage** (`coverage/computational/<analysis-id>.audio.jsonl`, `coverage-audio.schema.json`):
  stream identity, duration vs analysed seconds, missing intervals, per-stage status and processing errors.
- **Visual inspection coverage** (`coverage/visual/<agent-id>.jsonl`): one record per image actually opened (frame,
  sheet or strip) with the frame IDs it shows, the agent, the date and the purpose. A contact sheet covering 60
  frames counts those 60 frames as viewed *at sheet resolution* — record the resolution.
- Never write "inspected every frame" unless the visual ledger proves it.

## Contradictions
Record both sides with their evidence, label which is stronger and why, and escalate when a decision depends on it.
Never average contradictory findings into a single number.
