# PROGRESS

**Current phase:** Phase 2.5 — Operational Validation (approved 2026-11-27). Phase 2 accepted. Phase 3 not started.
**Last updated:** 2026-11-27

## Phase 1 — approved (conditionally, 2026-11-27); corrections completed
- [x] Permanent RC30 reference dataset rule added (CLAUDE.md, MASTER_PLAN.md Phase 3, `knowledge/dataset/README.md`,
      D007).
- [x] Google Flow research corrected: official daily image limits confirmed on Google's page (AI Pro: Nano Banana Pro
      100/day; Nano Banana 2.1 + 2 Lite 1,000/day shared; 2K upscale 200/day; image generation/upscaling not using
      monthly credits). Account-specific limits **unverified**. Flow Agent, custom Tools, Claude in Chrome and bridge
      options researched → `research/integration-feasibility.md` rev 2; D003 rev 2.
- [x] Dependencies: Python 3.13 compatibility verified by hash-pinned dry-run resolution; isolated venv script
      prepared (`setup/`, D010). Nothing installed; cloud environment unchanged.
- [x] Remotion licence checked: Free License for individuals / ≤ 3 people incl. commercial use (D008).

## Phase 2 — deliverables
- [x] 29 agent definitions: `.claude/agents/a01-…` to `a29-…` (generated from `tools/agentgen/agents_data.py`).
- [x] Responsibility + ownership matrix: `knowledge/_system/OWNERSHIP.md`.
- [x] Knowledge-base architecture: `knowledge/README.md`, `knowledge/_system/EVIDENCE.md`, `knowledge/dataset/README.md`,
      `knowledge/contracts/README.md`.
- [x] Orchestration protocol: `knowledge/_system/ORCHESTRATION.md`; evaluation rubric structure: `knowledge/_system/RUBRIC.md`.
- [x] Templates (research report, experiment, technique, failed approach, hand-off, brief, contract) and JSON Schemas
      (dataset manifest, measurement, computational coverage, visual coverage).
- [x] Validation: `python3 tools/validate_agents.py` → PASS (29 agents, 29 unique names/IDs, valid models/tools,
      16 required sections each, no ownership conflicts). Negative test with planted errors (duplicate, bad model,
      forbidden tool, overlapping ownership) → all detected. Schemas checked against the JSON Schema 2020-12 meta-schema.
- [x] Dry run: **blocker documented (D011).** Registered agents are not discoverable in this session
      (`Agent type 'a27-frame-analysis-specialist' not found`, retried twice). A substitute read-only dry run used a
      general-purpose subagent following the A27 definition verbatim. It produced a correct plan and found 5
      document inconsistencies, all fixed (ownership-column wording, schema IDs for our renders, required checksum,
      frame-count fields, shared-table storage path). This is **not** evidence that the registered agent can be invoked.

## Phase 2 — agent discovery verification (D012) ✅
- Fresh session, HEAD `492ee79`: all 29 agent types `a01-…`–`a29-…` appear in the session's registered agent list.
- `a27-frame-analysis-specialist` invoked explicitly by `subagent_type` (agent ID `afa524f2cc3a468c8`, 3 tool calls,
  ~6 s), read-only. It reported its A27 identity, its owned paths per `OWNERSHIP.md`, the RC30 frame-coverage rule,
  that `MANIFEST.json` does not exist, and `git log -1` = `492ee79` — all matching the repository. No files written.
- **Scope of evidence:** all 29 are *registered*; only A27 has been individually invoked and verified.

## Phase 2.5 — Operational Validation (in progress)
- [ ] A23 Google Flow integration feasibility investigation → `research/integration-feasibility.md`.

## Blockers
1. ~~Registered agents need confirmation in a fresh session (D011).~~ **Resolved (D012)**: all 29 registered; A27
   invoked and verified. Remaining agents to be verified on first use.
2. Phase 3 preconditions: an authorised footage acquisition/storage method for RC30; approval to run `setup/setup-analysis.sh`.
3. Google Flow: ToS on automation/commercial use unread; Agent/Tools credit discrepancy; bridge byte transfer unverified;
   Chrome integration not set up on the user's computer (D003 rev 2).
4. ElevenLabs API key not configured.
5. No GPU (software WebGL2 only).

## Next actions (pending approval)
1. Phase 2.5: A23 Google Flow feasibility investigation; user reviews the recommended architecture.
2. On Phase 3 approval: user confirms the acquisition method; run the setup script; director freezes `MANIFEST.json`;
   A27 runs first.
