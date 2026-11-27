# Knowledge base

Permanent, Git-tracked studio knowledge. It survives cloud sessions because it is committed and pushed. It holds
**text and numeric derived data only** — never reference video, frames, crops, contact sheets or third-party art.

## Layout
```
knowledge/
  README.md                 this file (director)
  _system/                  director-owned rules every agent reads
    ORCHESTRATION.md        how the director runs the 29 specialists
    EVIDENCE.md             evidence labels, confidence, frame IDs, coverage honesty
    OWNERSHIP.md            responsibility + file-ownership matrix (generated from agent definitions)
    RUBRIC.md               evaluation areas used by A28/A29
    templates/              research report, experiment, technique, failed approach, hand-off, brief, contract
    schemas/                JSON Schemas for manifests, measurements and coverage ledgers
  dataset/                  frozen RC30 reference dataset (metadata only)
    README.md               dataset rule and frame-ID format (director)
    MANIFEST.json           frozen list of 30 videos (director; created at the start of Phase 3)
    index/                  per-video frame index (A27)
    coverage/computational/ per-analysis frame coverage (A27 and analysts, via A27 scripts)
    coverage/visual/        <agent-id>.jsonl — frames each agent actually viewed (each agent its own file)
  contracts/                implementation contracts between agents (director-owned, co-signed)
  <department>/<agent-name>/  each specialist's own knowledge
    FINDINGS.md             evidence-backed findings (with evidence IDs)
    TECHNIQUES.md           approved techniques (promoted only after a passed experiment + A28 review)
    FAILED.md               failed approaches and lessons learned
    experiments/EXP-*.md    experiment records
    reports/<date>-<topic>.md  research reports
```
Folders and files are created when first needed from the templates. Empty placeholders are not committed, and no
file is pre-filled with conclusions.

## Lifecycle of knowledge
1. **Hypothesis** — a question or claim (incl. upstream-repo claims, `H-UP`) recorded in FINDINGS.md as `HYPOTHESIS`.
2. **Finding** — measured/observed with evidence IDs, method, confidence, limitations.
3. **Experiment** — a controlled test (one variable, 360p/24 fps) recorded in `experiments/`.
4. **Approved technique** — moved to TECHNIQUES.md after a passed experiment and an A28 review; the director logs
   the approval in `DECISION_LOG.md`.
5. **Failure** — anything that did not work goes to FAILED.md with the reason; never deleted.

## Versioning and revision history
- Git is the version history: one commit per completed milestone, message names agent ID and knowledge files.
- Every knowledge file starts with a header block: `owner`, `status` (draft/reviewed/approved/superseded),
  `version` (semver-like, bump minor for additions, major for reversals), `last_updated`, `evidence_basis`
  (dataset manifest hash).
- A reversal never deletes the old text: mark it `SUPERSEDED by <id>` and keep it.
- Findings reference the dataset manifest SHA-256 so results stay tied to the frozen dataset.

## Safe storage rules
- Numeric tables that contain image content (pixel arrays, thumbnails) are **not** committed.
- Large derived tables go to git-ignored `analysis/data/`; the knowledge base stores their schema, command,
  input checksums and summary statistics.
