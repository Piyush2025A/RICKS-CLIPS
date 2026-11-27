# DECISION LOG

Format: ID · date · decision · reasoning · status (proposed = awaiting user approval; accepted = user approved).

## D001 · 2026-11-27 · Reference repository is research material only
- Cloned `mromidev/claude-animated-shorts` at `e3b817b6afc6cd413466d43f11ba31209e034bbf` into the session scratchpad,
  outside the tracked project. No code, frames or contact sheets copied into this repo; nothing executed.
- Why: its code is MIT, but its `references/frames` and `references/sheets` are stills from a third-party channel
  ("for style study only"); no licence covers them, and our repository is public.
- Status: accepted (follows the user's Phase 1 instructions).

## D002 · 2026-11-27 · Upstream measured numbers are hypotheses, not facts
- The upstream reports contradict each other (e.g. STYLE_BIBLE "ease-out burst" camera grammar vs motion.md, which
  calls that finding wrong; LUFS −14 measured vs −15 mix target). Scores are self-assessed by its own verifier.
- Why: rule 2 (no unverified findings). Phase 3 re-measures from footage we are authorised to analyse.
- Status: accepted.

## D003 · 2026-11-27 · Google Flow integration architecture (rev 2, proposed)
- Rev 1 (superseded): "user-operated Flow → Drive → Drive connector" as the primary path. The user corrected this:
  manual Flow-to-Drive transfer is approved **only as a fallback and initial hand-off test**, not the final
  architecture. Rev 1 also wrongly used monthly video-credit figures instead of the daily image allowance.
- Rev 2: tiered architecture (`research/integration-feasibility.md` §1.8):
  Tier 0 manual hand-off test (approved fallback) → Tier 1 Flow-native custom Tools + Agent batch generation →
  Tier 2 preferred target: local Claude Code + official Claude in Chrome operating Flow in the user's visible,
  logged-in browser, with a local-to-cloud bridge (Remote Control folder or local intake).
- Basis: no official Flow API; official image limits (AI Pro: Nano Banana Pro 100/day, Nano Banana 2.1 + 2 Lite
  1,000/day shared, 2K upscale 200/day, no monthly credits for image generation/upscaling) confirmed on Google's
  page; account-specific limits unverified. Chrome integration is documented for local CLI/VS Code, not for cloud
  sessions. Drive connector binary transfer to the cloud filesystem is unverified.
- Rejected: third-party session-cookie wrappers, unreviewed CDP MCP servers, token extraction.
- Status: proposed. Tier 0 approved by the user; Tier 2 needs a ToS review and user approval in Phase 4.

## D004 · 2026-11-27 · Google AI Pro does not pay for Gemini API calls
- Google's AI-plans doc and support replies state subscription benefits apply in the apps / AI Studio UI; API keys
  use separate Cloud billing. Any Nano Banana / Imagen API use is a separate paid decision.
- Status: accepted as a finding; any API use requires user approval (rule 10).

## D005 · 2026-11-27 · No dependencies installed in Phase 1; setup script proposed, not applied
- Proposed contents were in `research/technical-audit.md` §4. Status: superseded by D010.

## D006 · 2026-11-27 · Development render spec
- 360p vertical (360×640), 24 fps for all development tests; reference analysis at native fps.
- Status: accepted (user rule 6 and 7).

## D007 · 2026-11-27 · RC30 frozen reference dataset (permanent rule)
- Phase 3 analyses **only** the 30 most recently published Shorts of https://www.youtube.com/@RicksClips3000, by
  publication date (not popularity), frozen at the start of Phase 3 in `knowledge/dataset/MANIFEST.json` with IDs,
  publication dates, durations and source metadata. No older Shorts; no substitution for unavailable videos.
- Every native frame processed computationally; 30 fps footage fully accounted for; separate computational and
  visual coverage ledgers; narration, SFX, music, editing and sync analysed; upstream reports are hypotheses only;
  footage acquired and stored only through authorised methods, never committed.
- Why: one shared, reproducible evidence base for all 29 specialists. Status: accepted (user, Phase 1 review).

## D008 · 2026-11-27 · Remotion licence
- The official pricing page offers a Free License for "individuals and companies of up to 3 people … unlimited
  commercial use. Terms apply." An individual commercial workflow qualifies (INFERRED). Full terms to be read before
  publication; re-check if the team exceeds 3 people. Status: accepted as a finding.

## D009 · 2026-11-27 · Agent architecture: 29 ordinary subagents with exclusive file ownership
- Format: Markdown + YAML frontmatter in `.claude/agents/` (official docs). Explicit `tools` allowlists (never
  inherited); no `Agent`/`SendMessage` tools, so specialists cannot spawn agents; web tools only for A10, A17,
  A23–A26; A18/A19 have no shell; A28/A29 have no Edit and write only to `evaluations/` / `qa/`.
- Models: `sonnet` for 26 specialists; `opus` for A18 (script), A28 (independent evaluation), A29 (release QA) to
  conserve Claude Pro usage. `maxTurns` caps per agent.
- Definitions and `knowledge/_system/OWNERSHIP.md` are generated from one data source so they cannot drift;
  `tools/validate_agents.py` checks format, uniqueness, tools, models, sections and ownership conflicts.
- Limitation: `tools` cannot restrict Bash to specific commands (whole tools only), so Bash limits rely on
  instructions; `permissions.deny` rules are a possible later hardening step (not applied).
- Status: proposed for user review (Phase 2 deliverable).

## D010 · 2026-11-27 · Reproducible analysis environment (proposed)
- Isolated venv `.venv-analysis/`, hash-pinned lock files for CPython 3.13 (core: 22 packages; +audio/librosa: 40),
  binary wheels only, idempotent script `setup/setup-analysis.sh`. Rendering dependencies kept separate (Node, later).
- Lock resolution was verified with `pip install --dry-run --require-hashes`; nothing installed; cloud environment
  configuration unchanged. Status: proposed — awaiting approval to run and/or save as the setup script.

## D011 · 2026-11-27 · Agent discovery limitation recorded
- New agents in `.claude/agents/` were **not** discoverable in the session that created the directory
  (`Agent type 'a27-frame-analysis-specialist' not found`), despite the docs saying changes are detected without
  restart. The dry run therefore used a general-purpose subagent instructed to follow the A27 definition verbatim.
  It is evidence that the definition and protocols are usable, **not** that the registered agent was invoked.
  A real invocation must be confirmed in a fresh session. Status: accepted (documented limitation).

## D012 · 2026-11-27 · Agent discovery blocker resolved; Phase 2.5 introduced
- In a fresh session at `492ee79`, all 29 custom agents are listed as registered agent types. `a27-frame-analysis-specialist`
  was invoked explicitly (not via a general-purpose substitute; agent ID `afa524f2cc3a468c8`) for a read-only test and
  returned answers consistent with the repository (identity, ownership, RC30 rule, MANIFEST absent, HEAD commit).
- Probable cause of D011 (INFERRED, not re-verified against docs): agents are loaded at session start, and the
  directory was created mid-session.
- Limitation: only A27 has been individually invoked; the other 28 are registered but unverified by invocation.
- User approved Phase 2 and introduced Phase 2.5 — Operational Validation, prioritising Google Flow integration
  before Phase 3 reference analysis.
- Status: accepted (user approved).

## D013 · 2026-11-27 · Google Flow integration architecture rev 3 (proposed)
- A23 recommends (`research/integration-feasibility.md` §1A.7): Flow runs only in the user's own visible browser on
  their computer, via Tier 1 (Flow Agent/Tools + project Download) and Tier 2 (local Claude Code + official Claude in
  Chrome, user present, paced, stop on any CAPTCHA/login/safety prompt). Downloads go to a private inbox outside the
  repo; an intake script writes text manifests (SHA-256, dimensions, model, quota count). Only text crosses to the
  cloud. Supersedes D003 rev 2 where different.
- Rejected for installation: FlowPilot (automation-masking flag, off-screen window), Flow Studio (watermark removal,
  credit-exhaustion account switching, plaintext keys), google-flow-mcp (closest to our rules, but still unreviewed
  third-party code driving a logged-in session); custom tunnelled remote connector and hosted Flow services (high risk).
- Director note: A23's C1 (withdrawing the cloud-attached Remote Control folder bridge) conflicts with tools present
  in this cloud session (`request_computer_folder`). Unresolved; to be tested in T5. If it works, cloud-side commands
  and file tools could reach the local inbox directly, without moving pixels into the cloud.
- Status: proposed — awaiting user decisions (§1A.9).

## D014 · 2026-11-27 · Cloud browser connectivity failed; Flow browser work moves to a local session
- Test: the user opened Google Flow in their Chrome and asked this cloud session to read it. The `chrome-browser` skill
  loaded, but no Claude in Chrome tools were exposed (ToolSearch: no match for `mcp__claude-in-chrome__*` or "chrome").
  Nothing was read or operated in the browser; no retries.
- Distinction: this is evidence about **cloud-session browser connectivity** only (result: not available). It says
  nothing about **local Chrome integration** (local Claude Code + extension via `claude --chrome` /
  `claude remote-control --chrome`), which remains untested (T0/T1 in `research/integration-feasibility.md` §1A.8).
- Decision: the user will run a separate local Claude Code session on their computer, on the same repository, for
  Google Flow work. The cloud session keeps planning, documentation and text-only hand-off via git.
- Status: accepted (user instruction).

## D015 · 2026-11-27 · Local Claude in Chrome → Flow generation works (reported by local session)
- Reported by the user's local Claude Code session (not re-verified from the cloud): one Nano Banana 2 Lite image
  generated and downloaded via official Claude in Chrome; PNG 768 × 1376; ~15–27 s; Flow balance 1,050 → 1,050;
  zero monthly credits; private local storage + provenance records; visible watermark and content credentials
  preserved; the download needed a manual confirmation.
- Implications: local Chrome integration (Option 2, §1A.6) is functional for a single generation; the image path
  did not move the credit balance (consistent with §1.2, informs C2 for the direct path only). The download
  confirmation is a fixed manual step. Cloud ↔ local binary transfer (T5) remains unverified, so pixels stay local.
- Status: accepted as a reported result; "working" status for the full integration still requires T5 and a batch test.

## D016 · 2026-11-27 · Analysis environment (D010) installed and verified
- User approved installing the full analysis tier with audio. Lock files checked first (40 + 22 packages, every package
  sha256-pinned, core ⊂ audio, script runs no network/system commands beyond pip). Install: 15 s, 715 MB, clean
  `pip check`, installed set equals the lock, 40/40 imports, idempotent re-run. Smoke tests on synthetic data only,
  including FFmpeg/FFprobe encode/probe/decode for video and audio (results: `setup/VERIFICATION.md`).
- Restoration: ephemeral container → re-run the script in each new session (~15 s). Saving it as the stored cloud
  environment setup script is recommended but **not applied** (needs separate approval).
- Status: D010 accepted (verified).

## D017 · 2026-11-27 · Reference-analysis pipeline built and validated on synthetic data
- A27 built `rcpipe` v0.1.0 in `analysis/` (owned path). Native-frame decode uses an ffmpeg rawvideo pipe with
  passthrough timing; frame IDs are zero-based decode indices with ffprobe pts; a negative control confirmed that
  `-fps_mode cfr` would alter VFR frame counts, so passthrough is mandatory.
- Validation used synthetic media only (scratchpad / git-ignored `out/`); nothing generated was committed. 159/159
  checks pass, reproduced independently by the director. Failures found and fixed are logged (A27 `FAILED.md`); four test
  expectations were amended with stated reasons (codec ramp bias, Canny on ≤ 2 px lines, run-key in frame IDs,
  ebur128 verbosity).
- Limitations: thresholds not yet calibrated on real animation/compression; camera vs character separation is an
  estimate with uncertainty flags; outputs are computational only.
- Proposed schema changes deferred (see PROGRESS). Status: accepted as Phase 2.5 infrastructure; recalibration on
  real footage happens only after Phase 3 authorisation.
