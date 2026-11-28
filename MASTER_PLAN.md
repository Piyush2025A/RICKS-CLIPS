# MASTER PLAN — Ricks Clips AI Animation Studio

Status of each phase lives in `PROGRESS.md`. Every phase ends at a **gate**: its completion criteria are met with
recorded evidence, the user reviews, and the user explicitly approves the next phase. No phase starts early.

## Objective
A reusable, highly automated pipeline that produces original vertical animated shorts matching the benchmark
channel's visual sophistication, cinematic quality and storytelling effectiveness, using our own characters,
stories and narration. Priorities: quality → automation → scaling.

## Stack hypothesis (to be confirmed by experiments, not assumed)
| Layer | Candidate | Status |
|---|---|---|
| Visual asset generation | Google Flow (Nano Banana Pro / 2.1 / 2 Lite via user's Google AI Pro; published AI Pro limits 100 + 1,000 shared images/day, 200 2K upscales/day) | Primary by mandate; tiered integration D003 rev 2 (Phase 4) |
| 3D / 2.5D scene | Three.js inside Remotion (`@remotion/three`) | Pattern proven upstream; not yet built or rendered here |
| Compositing / timeline | Remotion (React) | Free licence applies to individuals / ≤ 3 people (D008); full terms before publishing |
| Encode / analysis | FFmpeg 6.1.1, FFprobe, `rcpipe` v0.2.0 (OpenCV, NumPy, SciPy, scikit-image, librosa) | Installed + verified (D016, D018); frozen until Phase 3 calibration |
| Private media transfer | Google Drive connector, private folders | Verified byte-exact (D023): cloud → Drive ≤ ~3.1 MB, Drive → cloud ≤ 10 MB per file; larger files split into parts |
| Narration | ElevenLabs API (TTS with timestamps) | Key not configured; untested |
| SFX / music | Synthesized (NumPy/SciPy) and/or licensed libraries | To evaluate (Phase 8) |

## Phases and gates

### Phase 0 — Workspace creation ✅ (repository, branch, cloud environment exist)

### Phase 1 — Environment validation, technical foundation, reference repository investigation
Completion criteria:
- Environment inspected and recorded (`research/technical-audit.md` §1) with commands as evidence.
- Reference repository inspected read-only at a recorded commit (§2), reusable techniques and weaknesses listed.
- Google Flow / ElevenLabs feasibility research recorded (`research/integration-feasibility.md`).
- Permanent docs created and consistent: `CLAUDE.md`, `MASTER_PLAN.md`, `PROGRESS.md`, `DECISION_LOG.md`, `.gitignore`.
- No dependencies installed, no renders, no generations, no API credits spent.

### Phase 2 — Specialized agent architecture and agent creation
- 29 agent definitions in `.claude/agents/` (generated from one data source; validated by `tools/validate_agents.py`).
- Knowledge base: `knowledge/` (layout in `knowledge/README.md`); ownership matrix `knowledge/_system/OWNERSHIP.md`.
- Orchestration protocol: `knowledge/_system/ORCHESTRATION.md` (max 2 concurrent, briefs by path, independence).
- Templates and schemas: `knowledge/_system/templates/`, `knowledge/_system/schemas/`.
- Proposed reproducible analysis setup: `setup/` (not applied).
- Gate: validator passes; one read-only dry run (or documented blocker); user reviews all definitions.

### Phase 3 — Exhaustive reference video analysis
- **Dataset rule (RC30, D007):** only the 30 most recently published Shorts of
  https://www.youtube.com/@RicksClips3000, by publication date (not popularity), frozen at phase start in
  `knowledge/dataset/MANIFEST.json` (core: keys, files, SHA-256, media facts; D028: video IDs, publication dates and URLs
  are deferred metadata in `knowledge/dataset/IDENTITY.json`, order by user attestation). No older
  Shorts; no substitution for unavailable videos; all specialists use the same frozen dataset.
- Precondition: user confirms the authorised acquisition and private storage method (never committed).
  Analysis environment: done (D016). Execution plan: `research/phase3-plan.md`.
- Every frame at native fps (30 fps: every frame accounted for), timestamps (pts) preserved; FFprobe metadata per file.
- Order and concurrency: `knowledge/_system/ORCHESTRATION.md` §4 (A27 shared tables first).
- Measurements: camera motion, frame change, character motion, lighting, colour, outlines, textures, DOF,
  transitions, pacing, narration, sound effects, music, editing and audio/picture synchronisation.
- Separate coverage ledgers: `computational_coverage` (per-frame) vs `visual_inspection_coverage` (frames an agent
  actually viewed, with agent id). Every conclusion lists evidence, method, confidence, limitations.
- Upstream repo reports are supplementary hypotheses (`H-UP`) only; re-verify them (see audit §2.6).

### Phase 4 — Google Flow and ElevenLabs integration
- Google Flow: tiered architecture D003 rev 2 (`research/integration-feasibility.md` §1.8, checklist §1.10). End-to-end
  test = prompt → image in Flow → asset in our pipeline with provenance metadata, verified by checksum and viewing.
- ElevenLabs: official connector (no API key in the repo); one approved low-cost narration-only test (D036: no transcription/timestamps; sync by sentence/story-beat timings; subtitles added post-render in Canva).
- Gate: both integrations verified end-to-end with recorded evidence and credit usage.

### Phase 5 — Character design and animation rig
Original cast; expression sheet; separated parts (head, eyes, mouth set, torso, limbs); rig and walk/act cycles.

### Phase 6 — Environment, layering, geometry, depth
2.5D layered plates vs true 3D geometry decision per shot type; perspective, parallax, sight-line safety.

### Phase 7 — Lighting, shaders, textures, grading, VFX
Smooth-gradient card shading (no mandatory toon bands), optional world ink pass (scenery-ink treatment only), baked
character ink that scales with the card, card lighting (cast shadows off by default, per scene), painted textures, grade,
bloom, 2D effect sprites. Targets: `knowledge/STYLE_BIBLE.md` v0.3 + `knowledge/PRODUCTION_DEFAULTS.md`.

### Phase 8 — Camera, character movement, editing, audio sync
Camera grammar, transitions (crossfade default 7 f @30 fps ≈ 0.233 s), pacing, story-beat-driven acting (not
mandatory word-triggered swaps), captions ≈ 140 ms ahead of the voice, SFX, static music bed (−20 dB re narration in the
speech band as the initial default), loudness target.

### Phase 9 — Six-second integrated benchmark
One 6 s shot through the full pipeline; side-by-side evaluation by independent evaluator agents; scored rubric.

### Phase 10 — Complete original animated pilot short (55–70 s)

### Phase 11 — Production automation, optimization and scaling

## Agent architecture (definitions created in Phase 2, not before)
| Dept | ID | Role |
|---|---|---|
| Character | A01 | Character designer |
| | A02 | Facial expression specialist |
| | A03 | Anatomy and proportion specialist |
| | A04 | Character rigging and movement specialist |
| Environment | A05 | 3D world designer |
| | A06 | 2.5D layering specialist |
| | A07 | Depth and perspective specialist |
| | A08 | Prop and texture designer |
| Visual | A09 | Lighting and shadow specialist |
| | A10 | Shader and outline specialist |
| | A11 | Colour grading specialist |
| | A12 | Visual effects specialist |
| Cinematography | A13 | Camera director |
| | A14 | Composition and framing specialist |
| | A15 | Transition specialist |
| | A16 | Editing and pacing specialist |
| Story | A17 | Story researcher and fact-checker |
| | A18 | Scriptwriter |
| | A19 | Hook and retention specialist |
| Audio | A20 | Voiceover specialist |
| | A21 | Sound effects specialist |
| | A22 | Music and audio mixing specialist |
| Engineering | A23 | Google Flow integration engineer |
| | A24 | Asset processing engineer |
| | A25 | Three.js and Remotion engineer |
| | A26 | Rendering and performance engineer |
| Quality | A27 | Exhaustive frame analysis specialist |
| | A28 | Independent visual evaluator |
| | A29 | Final quality assurance specialist |

The master director (main session) coordinates, owns phase gates, and records decisions. Quality agents (A27–A29)
never evaluate work they produced. Definitions: `.claude/agents/a<NN>-*.md`; matrix: `knowledge/_system/OWNERSHIP.md`.

## Standing technical constraints
- Dev tests 360p / 24 fps (e.g. 360×640 vertical). Reference analysis at native fps.
- No GPU in the cloud container: software WebGL2 only (audit §1.4).
- Container is ephemeral: commit and push anything worth keeping; media stays out of git.
