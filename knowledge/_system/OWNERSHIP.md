# Agent responsibility and file-ownership matrix

Generated with the agent definitions from `tools/agentgen/agents_data.py` (`python3 tools/agentgen/generate.py .`); never hand-edit either. Validated by `tools/validate_agents.py`.
Exclusive write access: only the listed owner edits a path. Everyone may read everything.

## Director-owned (main session)
`CLAUDE.md`, `MASTER_PLAN.md`, `PROGRESS.md`, `DECISION_LOG.md`, `README.md`, `.gitignore`, `.claude/`,
`knowledge/_system/`, `knowledge/README.md`, `knowledge/contracts/`, `knowledge/dataset/README.md`,
`knowledge/dataset/MANIFEST.json` (the frozen dataset), `research/` (except
`research/integration-feasibility.md`, owned by A23), `setup/`, `tools/`, `productions/*/BRIEF.md`.

## Specialists
| ID | Agent | Dept | Model | Tools | Owned paths | Owned knowledge folder |
|---|---|---|---|---|---|---|
| A01 | `a01-character-designer` | Character | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/characters/` | `knowledge/character/a01-character-designer/` |
| A02 | `a02-facial-expression-specialist` | Character | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/expressions/` | `knowledge/character/a02-facial-expression-specialist/` |
| A03 | `a03-anatomy-proportion-specialist` | Character | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/proportions/` | `knowledge/character/a03-anatomy-proportion-specialist/` |
| A04 | `a04-rigging-movement-specialist` | Character | sonnet | Read, Grep, Glob, Bash, Write, Edit | `src/rig/`<br>`design/rig/` | `knowledge/character/a04-rigging-movement-specialist/` |
| A05 | `a05-3d-world-designer` | Environment | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/sets/`<br>`src/world/` | `knowledge/environment/a05-3d-world-designer/` |
| A06 | `a06-layering-2-5d-specialist` | Environment | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/layers/`<br>`src/layers/` | `knowledge/environment/a06-layering-2-5d-specialist/` |
| A07 | `a07-depth-perspective-specialist` | Environment | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/depth/`<br>`src/depth/` | `knowledge/environment/a07-depth-perspective-specialist/` |
| A08 | `a08-prop-texture-designer` | Environment | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/props/`<br>`design/textures/`<br>`src/materials/` | `knowledge/environment/a08-prop-texture-designer/` |
| A09 | `a09-lighting-shadow-specialist` | Visual | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/lighting/`<br>`src/lighting/` | `knowledge/visual/a09-lighting-shadow-specialist/` |
| A10 | `a10-shader-outline-specialist` | Visual | sonnet | Read, Grep, Glob, Bash, Write, Edit, WebFetch | `src/shaders/`<br>`design/outlines/` | `knowledge/visual/a10-shader-outline-specialist/` |
| A11 | `a11-color-grading-specialist` | Visual | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/grade/`<br>`src/grade/` | `knowledge/visual/a11-color-grading-specialist/` |
| A12 | `a12-vfx-specialist` | Visual | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/vfx/`<br>`src/fx/` | `knowledge/visual/a12-vfx-specialist/` |
| A13 | `a13-camera-director` | Cinematography | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/camera/`<br>`src/camera/`<br>`productions/*/camera/` | `knowledge/cinematography/a13-camera-director/` |
| A14 | `a14-composition-framing-specialist` | Cinematography | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/composition/`<br>`productions/*/storyboard/` | `knowledge/cinematography/a14-composition-framing-specialist/` |
| A15 | `a15-transition-specialist` | Cinematography | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/transitions/`<br>`src/transitions/` | `knowledge/cinematography/a15-transition-specialist/` |
| A16 | `a16-editing-pacing-specialist` | Cinematography | sonnet | Read, Grep, Glob, Bash, Write, Edit | `design/editing/`<br>`productions/*/edit/` | `knowledge/cinematography/a16-editing-pacing-specialist/` |
| A17 | `a17-story-researcher-fact-checker` | Story | sonnet | Read, Grep, Glob, Write, Edit, WebSearch, WebFetch | `productions/*/research/` | `knowledge/story/a17-story-researcher-fact-checker/` |
| A18 | `a18-scriptwriter` | Story | opus | Read, Grep, Glob, Write, Edit | `productions/*/script/` | `knowledge/story/a18-scriptwriter/` |
| A19 | `a19-hook-retention-specialist` | Story | sonnet | Read, Grep, Glob, Write, Edit | `productions/*/hooks/` | `knowledge/story/a19-hook-retention-specialist/` |
| A20 | `a20-voiceover-specialist` | Audio | sonnet | Read, Grep, Glob, Bash, Write, Edit | `pipeline/voice/`<br>`productions/*/voice/` | `knowledge/audio/a20-voiceover-specialist/` |
| A21 | `a21-sound-effects-specialist` | Audio | sonnet | Read, Grep, Glob, Bash, Write, Edit | `pipeline/sfx/`<br>`productions/*/sfx/` | `knowledge/audio/a21-sound-effects-specialist/` |
| A22 | `a22-music-mixing-specialist` | Audio | sonnet | Read, Grep, Glob, Bash, Write, Edit | `pipeline/music/`<br>`pipeline/mix/` | `knowledge/audio/a22-music-mixing-specialist/` |
| A23 | `a23-google-flow-integration-engineer` | Engineering | sonnet | Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch | `pipeline/flow/`<br>`prompts/`<br>`research/integration-feasibility.md` | `knowledge/engineering/a23-google-flow-integration-engineer/` |
| A24 | `a24-asset-processing-engineer` | Engineering | sonnet | Read, Grep, Glob, Bash, Write, Edit, WebFetch | `pipeline/assets/` | `knowledge/engineering/a24-asset-processing-engineer/` |
| A25 | `a25-threejs-remotion-engineer` | Engineering | sonnet | Read, Grep, Glob, Bash, Write, Edit, WebFetch | `package.json`<br>`remotion/`<br>`src/engine/`<br>`src/contracts/` | `knowledge/engineering/a25-threejs-remotion-engineer/` |
| A26 | `a26-rendering-performance-engineer` | Engineering | sonnet | Read, Grep, Glob, Bash, Write, Edit, WebFetch | `pipeline/render/` | `knowledge/engineering/a26-rendering-performance-engineer/` |
| A27 | `a27-frame-analysis-specialist` | Quality | sonnet | Read, Grep, Glob, Bash, Write, Edit | `analysis/`<br>`knowledge/dataset/index/`<br>`knowledge/dataset/coverage/computational/` | `knowledge/quality/a27-frame-analysis-specialist/` |
| A28 | `a28-independent-visual-evaluator` | Quality | opus | Read, Grep, Glob, Bash, Write | `evaluations/` | `knowledge/quality/a28-independent-visual-evaluator/` |
| A29 | `a29-final-qa-specialist` | Quality | opus | Read, Grep, Glob, Bash, Write | `qa/` | `knowledge/quality/a29-final-qa-specialist/` |

## Shared append-only files
- `knowledge/dataset/coverage/visual/<agent-id>.jsonl` — each agent appends only to its own file.
- `knowledge/contracts/*.md` — director-owned; a change requires sign-off lines from every listed party.

`*` in a path means "any production id"; each production folder is split by sub-folder owner.
