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

## D018 · 2026-11-27 · Schemas v2 and rcpipe v0.2.0 (synthetic validation)
- User approved A27's four schema proposals. Director-owned changes: `SYN-` keys and a required `dataset` field with
  key rules (RC30 must carry `manifest_sha256`; `dataset-manifest` stays RC30-only); coverage status counts with the
  invariant ok + uncertain + failed + missing = expected (validator-enforced); new `coverage-audio` schema incl.
  `audio_present`; `pipeline_version`, `config_fingerprint`, 64-hex `input_sha256`; `analysis_resolution`
  native/proxy (record = finest stage, per-stage values in `stages`); `per_video` null instead of coercion to 0.
- A27 found 5 schema defects; 4 fixed by the director, 1 kept by design (new audio schema starts at version 1).
- A27 implemented v0.2.0; 318/318 checks incl. 44 negative controls, reproduced independently. Native frames are
  retrievable bit-exactly by frame ID; motion/shot measurements are proxy-resolution and labelled so.
- Known limitations recorded (PROGRESS, A27 FAILED.md/TECHNIQUES.md labelled synthetic-validated). Thresholds are
  not re-tuned on synthetic data; recalibration waits for authorised real footage.
- Status: accepted by user for implementation; results awaiting user review.

## D019 · 2026-11-27 · rcpipe frozen; T5 transfer via attached computer folder (preparation)
- User accepted rcpipe v0.2.0 with its documented limitations and froze the analysis implementation until Phase 3
  real-footage calibration. No further synthetic infrastructure work.
- T5 path chosen: the official computer-folder attach for cloud sessions (`list_computer_folders` /
  `request_computer_folder`), scoped to `~/ricks-clips-private/t5-transfer-test/` only. Rejected: third-party
  connectors, public tunnels, GitHub as media transport.
- Verified now: tools present; no folder served (empty listing). Not verified: whether the Linux desktop app offers
  folder serving, and whether binary bytes survive a round trip in either direction. Public docs read do not describe
  this feature; the in-session tool definitions are the only source (recorded as such).
- Status: accepted (user instruction); test pending user action on their computer.

## D020 · 2026-11-27 · T5 attempt 1 blocked: Linux computer does not offer folders to cloud sessions
- Evidence: `list_computer_folders` → `folders: []`; `cannot_be_used`: `t5-transfer-test` and `RICKS-CLIPS` on
  `Latitude-5289`, reason `not_available`, no cause given by the computer. No access was requested.
- Cause not certain. Excluded: hidden/~/Library paths. Remaining candidate per the tool: the Claude app version on
  that computer (Linux beta). Next: user checks for a Claude Desktop update; if none helps, T5 via attached folder is
  not available on Linux and the fallback is the local session (D014) with text-only hand-off.
- Attempt 2 after a Claude Desktop update and restart: identical result. The update did not help; cause still not
  given by the computer. Cloud-attached folder transfer is treated as unavailable from this Linux computer for now;
  Flow work continues in the local session with text-only hand-off (D014).
- Status: blocked (retry only if a later app release or the user reports a change).

## D021 · 2026-11-27 · Native folder sharing blocked; Google Drive connector chosen as T5 candidate
- D020 closed: native computer-folder sharing is blocked on the user's Linux Mint system (Claude Desktop 6.28899.6,
  no update available). Not pursued further.
- Candidate: the official Google Drive connector (already attached; no third-party connector, no public links). Upload
  of cloud files by byte reference and download as base64 are documented in its tool definitions; byte-exactness into
  the cloud filesystem and size limits are not, so they are the subject of the test.
- Local side: Linux has no official Google Drive desktop client (INFERRED, not checked); the user uploads/downloads
  through drive.google.com in the browser.
- Cost: no additional subscription or paid API needed for the connector (INFERRED from it being a claude.ai connector
  already attached); Drive storage comes with the user's Google account/AI Pro plan (storage size UNVERIFIED).
- Proposed test (awaiting approval): private folder `ricks-clips-t5` (not shared), synthetic files only
  (PNG, WAV, MP4, ZIP at ~10 KB, ~1 MB, ~5 MB, ~20 MB), SHA-256 compared in both directions, then trashed.
- Status: proposed.

## D022 · 2026-11-27 · T5 Drive transfer: byte-exact up to ~1 MB, upload capped at ~3.1 MB per file
- Verified: 16/16 byte-exact round trips (cloud → Drive → cloud) for PNG, WAV, MP4, ZIP at ~1–10 KB and ~1 MB; downloads
  land as files on the cloud filesystem, not as base64 in the conversation.
- Verified limit: each connector call from a cloud session is capped at 4.2 MB (~3.1 MB of file content), so cloud →
  Drive uploads of ~5 MB fail before sending. Stopped there per the test rules; no workaround attempted.
- Implication (INFERRED, to confirm): Drive works as a private channel for stills, short audio and small packs from the
  cloud; larger renders cannot leave the cloud this way. The Drive → cloud direction for larger files (e.g. Flow
  downloads uploaded by the user) is untested.
- Status: partial pass; awaiting the user's local verification and a decision on testing larger user-uploaded files.

## D023 · 2026-11-27 · T5 complete: Google Drive is the private small-asset transfer layer
- Verified end to end: cloud → Drive → cloud (16/16), Drive → user's computer (8/8, user-verified), user's computer →
  Drive → cloud (5 MB 1/1); 25/25 completed transfers byte-exact; no base64 in the conversation.
- Verified limits per file: upload from the cloud ~3.1 MB (4.2 MB per connector call); download into the cloud 10 MB
  (Google's connector limit; the 20 MB test file was refused). No extra cost; folder private; no sharing changes.
- Decision (proposed): use Drive for stills, audio, packs and small previews; render large final videos on the user's
  computer from git-committed source; chunked Drive transfer as an untested fallback. Paid storage, GitHub media and
  tunnels stay rejected.
- Status: T5 accepted as complete; transfer-layer recommendation awaiting user approval.

## D024 · 2026-11-27 · Phase 2.5 closed in scope; Phase 3 plan prepared
- User decisions: Google Drive is the private small-asset transfer layer (limits D023); cloud rendering remains the
  development workflow; large final-render transfer deferred until needed; no further general infrastructure work.
  rcpipe v0.2.0 preserved (318/318) and frozen until real-footage calibration.
- Phase 3 plan (`research/phase3-plan.md`): metadata via YouTube Data API v3 (official, key-only reads; no Shorts
  field exists, so ≤ 180 s candidates are confirmed by the user against the channel's Shorts tab); acquisition
  options ranked against the YouTube ToS (read 2026-11-27): creator-supplied files recommended; download tools without
  permission conflict with the ToS and are not recommended; screen recording rejected (not native frames). Ingestion
  of > 10 MB files by ≤ 9 MB parts via a private Drive folder with per-part and whole-file SHA-256. New rule proposed:
  per-frame tables stay private (Drive), their checksums and all aggregates/findings are committed.
- Status: proposed; awaiting user approval and acquisition decision. No footage acquired.

## D025 · 2026-11-27 · RC30 files verified locally; manifest drafted, not frozen
- User placed 30 files outside the repo (`~/ricks-clips-private/reference-videos/RC30/`). Verified read-only in the
  local session: all readable and fully decodable, uniform 1080×1920 H.264 CFR 30 fps + AAC 44.1 kHz, exact frame
  accounting (50,898 frames, 1,696.600 s), no duplicates, no corruption. Evidence: `research/rc30-dataset-verification.md`.
- Not verified: video IDs, publication dates, that these are the latest 30 Shorts (files hold titles only).
- Provenance: container metadata suggests FFmpeg-merged YouTube streams (INFERRED); acquisition method and
  authorisation must be confirmed by the user before freeze (plan §3).
- Recommended (proposed): run rcpipe locally on this computer (no 796 MB transfer); per-frame data stays private.
- Status: awaiting user inputs (IDs/dates, authorisation) and approvals (freeze, venv install, analysis start).

## D026 · 2026-11-28 · Local install, calibration and batch plan prepared (proposed)
- Audio-tier lock required (rcpipe's audio stage imports librosa). Install proposed as the existing script with an
  explicit interpreter: `PYTHON=~/miniconda3/bin/python3.13 bash setup/setup-analysis.sh --with-audio` → only
  `.venv-analysis/`; system Python, miniconda base and `~/.venv` untouched.
- Calibration on the shortest video (`27.mp4`, 928 frames) after the manifest freeze, with director ground-truth
  labels from full visual review; optional long holdout (`15.mp4`). Open user decision: rcpipe's temporary 48 kHz mono
  audio extraction vs native 44.1 kHz stereo analysis.
- Resume rule: a video/stage is done only if its coverage record matches manifest, input SHA-256, config fingerprint
  and the manifest frame count. Details: `research/phase3-local-execution.md`.
- Status: proposed; blocked on identity/date inputs and acquisition authorisation.

## D027 · 2026-11-28 · Local analysis environment verified; audio policy
- User approved and the director ran `PYTHON=~/miniconda3/bin/python3.13 bash setup/setup-analysis.sh --with-audio` on
  the user's computer: exit 0, 40/40 packages identical to the lock, `pip check` clean, synthetic suite 318/318
  (868.6 s; ≈ 4× the cloud's 216 s), peak RSS 408 MiB, venv 828 MB. System Python, miniconda base, reference videos
  (re-hashed) and rcpipe v0.2.0 unchanged.
- Audio decision (user): originals' 44.1 kHz stereo preserved; rcpipe's temporary 48 kHz mono path kept for
  envelope/spectral/onset measures with documented limitations; loudness already runs on the native stream; stereo
  measures will use native stereo via a separate versioned tool (A20–A22), not by changing rcpipe.
- Status: done. RC30 research still blocked on identities/dates, authorisation and manifest freeze.

## D028 · 2026-11-28 · RC30 core manifest frozen; identity metadata deferred
- User decisions: (1) acquisition — the user downloaded the 30 files from YouTube themselves and takes responsibility
  for private, non-redistributed style research under their own legal assessment (ToS conflict noted, plan §3);
  (2) frames, contact sheets and short audio excerpts may be sent to Claude (Anthropic) for inspection only — no other
  service, no Drive, no GitHub; (3) order: `1.mp4` newest … `30.mp4` oldest (user attestation, not independently
  verified); (4) schema change approved: video IDs/dates/URLs become deferred metadata in `IDENTITY.json`.
- Web search could not resolve IDs (titles and channel handle not indexed; 3 queries, then stopped). YouTube pages and
  third-party channel tools stay excluded; no API key available. Nothing fabricated: all IDs/dates are null/deferred.
- Frozen: `knowledge/dataset/MANIFEST.json` (schema `dataset-manifest` core v2), SHA-256 `fc6f147a…278e06`; 30 keys,
  30 SHA-256 equal to the files, 50,898 frames. The repo's lightweight validator cannot enforce minItems/maxItems
  (pre-existing limitation), so the 30-item count was asserted separately.
- Status: done.

## D029 · 2026-11-28 · Phase 3 calibration accepted; rcpipe v0.2.0 kept unchanged
- Pilot RC30-27 + holdout RC30-15: exact frame accounting, camera direction 7/7, shots = high-recall noisy candidates
  (miss class: slow same-palette dissolves). No material defect → no pipeline change; transitions confirmed visually (A15).
- Evidence: `research/phase3-calibration.md`. Status: done.

## D030 · 2026-11-28 · Phase 3 research run complete; bibles drafted
- 50,898/50,898 frames computationally processed; 25 agent runs; A28 audit applied; 9 bibles + STYLE_BIBLE v0.2.
- Operational decisions taken autonomously (user-authorised): per-agent wrap-up on turn limits; director wrote refused
  deliverables verbatim; moved A15 CSV into its owned folder; parallel visual-first waves during the batch.
- Status: awaiting user review of the Phase 3 gate. Report: `research/phase3-overnight-report.md`.

## D031 · 2026-11-28 · Phase 3B completion round (user-requested); caption timeline without OCR
- User request: strengthen incomplete/weak research before the Phase 3 gate; reuse the 50,898-frame computation;
  ≤ 2 concurrent agents; no Phase 4, no generation, no paid credits.
- Caption timeline: no OCR engine installed and none added (installing needs approval). Director tool
  `tools/caption_events.py` detects caption segments on every native frame (caption band only, `-fps_mode passthrough`,
  counts reconciled with the manifest) and builds private crop sheets; text was read visually by A20 (logged as overlay
  views). Third-party narration text stays private (`~/ricks-clips-private/.../captions/`); only counts, timings and
  ≤ 10-word quotes are committed.
- Hook disagreement: resolved by a blind two-axis coding by two independent coders (A17 + a fresh general-purpose
  agent), agreement measured (verbal κ 0.89, picture κ 0.57); A19's single-label scheme retired.
- Status: done. Evidence: `research/phase3b-completion-plan.md`, `research/phase3b-hook-codebook.md`.

## D032 · 2026-11-28 · Phase 3 (3A + 3B) complete; bibles v0.3; awaiting gate review
- Both independent audits applied (AUDIT.md, AUDIT_3B.md). Superseded values recorded in the bibles (e.g. 220 wpm,
  caption lead 140 ms, black p1 0.071, push +24 %, crossfade default 7 f, card shadows default off, DOF 9 % upper bound).
- Operational notes: several agents ended at turn limits (A03, A28) and were resumed to wrap up; A17 had no Bash, so the
  director logged its viewed sheets on its behalf (marked); A20 omitted 2 ledger records — director spot-checked both
  transcripts against the sheets (word-for-word match) and logged its own views; nothing added for unconfirmed views.
- Status: awaiting user review of the Phase 3 gate; report `research/phase3-completion-report.md`.

## D033 · 2026-11-28 · Phase 3 APPROVED (conditional, with documented limitations); Phase 4 authorised
- User: external review of commit `c0eb61c`; Phase 3 conditionally approved; Phase 4 (Google Flow + ElevenLabs
  integration) authorised after documentation corrections.
- Adopted as current production reference: `knowledge/STYLE_BIBLE.md` v0.3 + 9 bibles v0.3 (with stated confidence and
  limitations). New `knowledge/PRODUCTION_DEFAULTS.md` v1: caption lead ≈ 140 ms; crossfade 7 f @30 converted by time
  (6 f @24); story-beat expression swaps; smooth gradient card shading (no mandatory toon bands); card cast shadows off
  by default; static music bed −20 dB re narration in 400–2000 Hz; baked character ink scaling with size; measured values
  are initial targets, not mandatory rules; dataset identity per D028 (deferred metadata).
- Corrected active docs: CLAUDE.md (dataset identity), MASTER_PLAN.md (Phase 3 dataset, Phases 7–8), TECHNIQUES of A01,
  A08, A09, A13, A15, A16, A20, A25 (each correction tagged D033). Historical FINDINGS/research records unchanged.
- Git protections: `.gitignore` extended (all raster images, provenance sidecars, caption transcripts/timelines, hook
  packets, alignment JSON, more audio/video formats, private-data paths, API-key patterns; schemas and test fixtures
  excepted); pre-commit guard `tools/git-hooks/pre-commit` (media, private paths, > 1 MB, secret patterns) enabled via
  `git config core.hooksPath tools/git-hooks` (repo-local). Verified: blocks a PNG, a provenance file and a fake key;
  passes clean files. No tracked file removed (none matched the new rules).
- Status: done.

## D034 · 2026-11-28 · Phase 4 integration groundwork; stopped at credit/user gates
- Flow: supervised local workflow, skill, templates, intake tool and terms review adopted (no generation, 0 credits).
  Flow Agent/Tools not required for the initial workflow. Drive folder `ricks-clips-handoff` created (private) for
  local→cloud hand-off; lighthouse PNG uploaded (size verified); cloud-side hash check pending.
- ElevenLabs: connector verified read-only; timestamps = Scribe STT words (TTS returns none via the connector); free
  tier is non-commercial (paid plan needed before any commercial release — user decision). Recommended voice for the
  6-s test: workspace voice "David – Deep Audiobook & Documentary" (`cCYjmrGZaI86GUJ7F2Nn`, not a library voice, so
  usable on the free tier), alternative "James – Husky, Engaging and Bold" (`EkK5I93UQWFDigLMpZcX`); neither imitates
  the reference narrator. `eleven_v4` has no speed parameter (schema read); `eleven_multilingual_v2` has speed 0.7–1.2.
- Status: waiting for user approval of the 6-s test spend (~136 credits TTS + Scribe TBD) and for the cloud C2 check.
