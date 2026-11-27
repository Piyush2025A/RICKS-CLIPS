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
- [x] A23 (`a23-google-flow-integration-engineer`, invoked as a registered agent) Google Flow feasibility
      investigation → `research/integration-feasibility.md` §1A (rev 3): ranked options, recommended architecture,
      test plan T0–T7, open questions. Research only: nothing executed, installed, authenticated or generated. Three
      external Flow MCP repos read as source only (FlowPilot `e0dce06`, google-flow-mcp `e6a7137`, flow-studio
      `ed709b0`), cloned outside the repo; none recommended for installation. A23 is now the second agent verified by invocation.
- [ ] **Director review flag (D013):** A23's correction C1 ("a cloud session cannot attach a Remote Control folder")
      conflicts with this cloud session's own tools (`list_computer_folders` / `request_computer_folder`, which attach a
      folder that the user's computer serves via Remote Control). Listing returned 0 folders (none served). To be
      tested in T5; not yet verified either way.
- [x] **Cloud browser connectivity test — FAILED (D014), 2026-11-27.** From this cloud session (claude.ai/code), the
      `chrome-browser` skill loaded, but no `mcp__claude-in-chrome__*` tools (nor `enable__mcp__claude-in-chrome`)
      were available; ToolSearch for the exact names and for "chrome" returned no match. No tab was listed, read or
      operated; no navigation, generation or settings change. Evidence that cloud sessions cannot reach the user's
      Chrome (closes the cloud part of C3 against cloud support).
      **Not tested:** local Chrome integration (local Claude Code + extension, `claude --chrome`). Still pending as T0/T1.
- [x] Separate **local** Claude Code session on the user's computer established (same repo) for Google Flow.
- [x] **Local Flow generation — REPORTED BY THE LOCAL SESSION (D015), 2026-11-27; not independently verified by
      the cloud session.** One image generated with Nano Banana 2 Lite and downloaded through the official Claude in
      Chrome integration:
      PNG, 768 × 1376 px; generation ~15–27 s; Flow balance 1,050 credits before and after; monthly credits consumed
      0; private local storage and provenance records established; visible watermark and embedded content credentials
      preserved; download required manual confirmation.
      Still **unverified:** cloud-to-local (and local-to-cloud) binary asset transfer (T5).
- [x] **Analysis environment installed and verified (D016), 2026-11-27** — `bash setup/setup-analysis.sh --with-audio`
      (user-approved): exit 0, 15 s, venv 715 MB; `pip check` clean; installed set identical to the 40-package lock;
      40/40 imports incl. librosa 1.0.1; idempotent re-run (0 s); synthetic image/video/audio smoke tests and
      FFmpeg/FFprobe 6.1.1 round trips pass. Two first-attempt test-design failures (flat-texture optical flow, coarse
      Welch bins) re-run correctly. Evidence: `setup/VERIFICATION.md`. Environment is ephemeral: re-run the script each
      session (cloud setup script not changed).
- [x] **A27 computational analysis pipeline `rcpipe` v0.1.0 — synthetic validation only (D017), 2026-11-27.**
      Built by the registered `a27-frame-analysis-specialist`: `analysis/rcpipe/` (probe, native decode, reconcile,
      motion, shots, stats, audio, sheets, pipeline/checkpoints, schema), CLI `analysis/run_pipeline.py`, tests
      `analysis/tests/`, docs `analysis/README.md`. Suite **159/159 pass** (A27 run, 128 s; director's independent
      rerun, 126 s; first A27 run was 152/158, failures logged in
      `knowledge/quality/a27-frame-analysis-specialist/FAILED.md`). Highlights: CFR 30 fps and VFR 24/30/60 frame
      counts reconcile exactly with a burned-in per-frame barcode (no drop/dup/reorder); camera tx/ty error ≤ 0.016 px;
      camera vs object separation on a panning background; cut/dissolve/flash candidates with 0 false positives;
      loudness exact to −23/−16 LUFS; resume and rerun byte-identical; peak RSS flat (~105 MB) from 90 to 600 frames.
      **Limits:** thresholds tuned on synthetic noise textures only, untested on real flat-colour animation or YouTube
      compression; no audio coverage ledger record; rotation-tagged/HDR/10-bit untested. Computational measurements
      only, no semantic understanding. No real RC30 media used.
- [ ] Schema changes proposed by A27 (not applied, director/user decision): SYN key pattern, `frames_uncertain`,
      audio coverage variant, `input_sha256` + script version fields.
- [ ] User decisions on §1A.9 (Chrome automation risk, pixel storage, Gemini API, approvals for T3/T4/T6/T7).

## Blockers (corrected 2026-11-27)
1. ~~Agent discovery (D011).~~ **Resolved (D012).** All 29 registered; A27 and A23 verified by invocation; others on first use.
2. ~~Analysis environment not installed.~~ **Resolved (D016).** Re-run `setup/setup-analysis.sh --with-audio` each new
   cloud session (~15 s) unless the user approves saving it as the environment setup script.
3. **Phase 3 not authorised.** Preconditions: user approval and an authorised RC30 footage acquisition/storage method.
4. Google Flow (D013–D015):
   - ~~Chrome integration not set up~~ — local Claude in Chrome generation works (D015, reported by local session).
   - Cloud session has no browser access (D014); Flow work runs only in the local session.
   - Cloud ↔ local binary transfer unverified (T5); pixels stay local until it passes.
   - Labs.google / Flow ToS on automation and commercial use not read.
   - Agent/Tools credit discrepancy (C2) untested (T4); direct-generation path used 0 monthly credits (D015).
   - User decisions in `research/integration-feasibility.md` §1A.9 pending. (Its §4 blocker table predates D014–D015;
     A23 to refresh on next task.)
5. ElevenLabs: no API key in the environment; an ElevenLabs connector is attached to sessions but untested. No
   generation without approval.
6. No GPU (software WebGL2 only).

## Next actions (pending approval)
1. Phase 2.5: review A27 pipeline (D017) and proposed schema changes.
2. User decisions on Flow §1A.9; T5 bridge test.
3. On Phase 3 approval: user confirms the acquisition method; director freezes `MANIFEST.json`; A27 runs the
   validated pipeline first.
