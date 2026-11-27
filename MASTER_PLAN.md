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
| Visual asset generation | Google Flow (Nano Banana Pro / Imagen, via user's Google AI Pro) | Primary by mandate; integration path open (Phase 4) |
| 3D / 2.5D scene | Three.js inside Remotion (`@remotion/three`) | Pattern proven upstream; not yet built or rendered here |
| Compositing / timeline | Remotion (React) | Licence terms to confirm for commercial use (Phase 1 open item) |
| Encode / analysis | FFmpeg 6.1.1, FFprobe, OpenCV (to install), NumPy | FFmpeg verified; OpenCV missing |
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
- Write the 29 agent definitions in `.claude/agents/` (one file each) with: responsibilities, tool permissions,
  research methods, file ownership, measurable quality standards, knowledge-file paths.
- Define the knowledge base layout (`knowledge/<department>/<topic>.md`) and the file-ownership map.
- Define the orchestration protocol: max concurrent agents (default 2), hand-off format, verifier independence.
- Gate: user reviews every agent definition; one dry-run of a single agent on a read-only task.

### Phase 3 — Exhaustive reference video analysis
- Precondition: user confirms how reference footage is lawfully obtained and stored (private, never committed).
- Every frame at native fps (30 fps: no skipped frames), timestamps preserved; FFprobe metadata per file.
- Measurements: camera motion, frame change, character motion, lighting, colour, outlines, textures, DOF,
  transitions, pacing, audio sync (voice WPM, loudness, ducking).
- Separate coverage ledgers: `computational_coverage` (per-frame) vs `visual_inspection_coverage` (frames an agent
  actually viewed, with agent id). Every conclusion lists evidence, method, confidence, limitations.
- Re-verify the upstream repo's measured claims instead of trusting them (see audit §2.6).

### Phase 4 — Google Flow and ElevenLabs integration
- Google Flow: choose and verify an approved path (see `research/integration-feasibility.md` §1.4–1.5). End-to-end
  test = prompt → image in Flow → asset in our pipeline with provenance metadata, verified by checksum and viewing.
- ElevenLabs: network secret via environment settings; one approved low-cost TTS-with-timestamps test.
- Gate: both integrations verified end-to-end with recorded evidence and credit usage.

### Phase 5 — Character design and animation rig
Original cast; expression sheet; separated parts (head, eyes, mouth set, torso, limbs); rig and walk/act cycles.

### Phase 6 — Environment, layering, geometry, depth
2.5D layered plates vs true 3D geometry decision per shot type; perspective, parallax, sight-line safety.

### Phase 7 — Lighting, shaders, textures, grading, VFX
Two-tone/toon shading, world ink pass, card lighting, painted textures, grade, bloom, 2D effect sprites.

### Phase 8 — Camera, character movement, editing, audio sync
Camera grammar, transitions, pacing, word-timed acting, SFX, music, ducking, loudness target.

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
never evaluate work they produced.

## Standing technical constraints
- Dev tests 360p / 24 fps (e.g. 360×640 vertical). Reference analysis at native fps.
- No GPU in the cloud container: software WebGL2 only (audit §1.4).
- Container is ephemeral: commit and push anything worth keeping; media stays out of git.
