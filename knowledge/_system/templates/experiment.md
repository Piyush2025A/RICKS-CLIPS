<!-- owner: <agent-id> | status: planned|running|passed|failed|inconclusive | version: 0.1 | last_updated: YYYY-MM-DD -->
# EXP-<agent-id>-<YYYYMMDD>-<nn>: <title>

- **Hypothesis:** <what should change and why> (links to findings / H-UP)
- **Single variable:** <name> — values tested: <A> vs <B>
- **Held constant:** scene, assets (checksums), seed, camera, lighting, code commit
- **Spec:** 360x640, 24 fps, <frames> frames (or single still); output in git-ignored `out/exp/<id>/`
- **Success criteria (set before running):** <measurable threshold and/or A28 judgement question>
- **Commands:** <exact commands>
- **Cost:** compute time estimate; credits: none / approved by user on <date>

## Results
Measured values, observations (with visual coverage entries), artefact paths (not committed).

## Verdict
passed / failed / inconclusive — reason. If failed, copy the lesson into `FAILED.md`.
