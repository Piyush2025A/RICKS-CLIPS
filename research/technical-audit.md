# Technical audit — Phase 1 (2026-11-27)

Evidence levels: **Verified** = observed by a command in this session · **Inferred** = reasoned from evidence ·
**Untested** = not exercised.

## 1. Environment

### 1.1 Repository and Git — Verified
| Item | Value | Evidence |
|---|---|---|
| Remote | `https://github.com/Piyush2025A/RICKS-CLIPS` (public per user) | `git remote -v` |
| Branch | `claude/beautiful-fermat-fs0iqn` (from `main` @ `3c2f5a4` "Initial commit") | `git status`, `git log` |
| Initial content | `README.md` only (26 bytes) | `ls -la` |
| Working tree at start | clean | `git status` |

### 1.2 GitHub permissions
| Capability | Status | Evidence |
|---|---|---|
| Read our repo over git | Verified | `git ls-remote origin` returned `main` |
| Push to our dev branch | **Verified** — commit `3c4c6f9` pushed to `origin/claude/beautiful-fermat-fs0iqn` | `git push -u origin ...` |
| Clone public third-party repo | Verified | clone of `mromidev/claude-animated-shorts` |
| GitHub MCP tools (issues/PRs) | Untested | scope: `piyush2025a/ricks-clips` only |
| Push to `main` / merge | Not attempted (forbidden without approval) | — |

### 1.3 Hardware and OS — Verified
| Item | Value | Command |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS, kernel 6.18.44, x86_64 (VM) | `/etc/os-release`, `uname -a` |
| CPU | 4 vCPU, Intel Xeon @ 2.10 GHz | `nproc`, `lscpu` |
| RAM | 15 GiB, no swap | `free -h` |
| Disk | `/` 60 GB available (per-session allowance; `df` can mislead) | `df -h` |
| GPU | **None** (`nvidia-smi` absent, no `/dev/dri`) | — |

### 1.4 Browser and graphics — Verified
- Playwright 1.63.0 (global), Chromium build 1243 at `/opt/pw-browsers`, `google-chrome` = Chrome for Testing 158.0.8127.36.
- Headless Chromium WebGL probe (Playwright, default flags and ANGLE/SwiftShader flags): **WebGL2 available,
  renderer `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))`, MAX_TEXTURE_SIZE 8192.** This is CPU
  software rasterisation. WebGL1 was not probed separately (the probe reused the canvas).
- Implication (Inferred): Three.js/Remotion renders will be CPU-bound. Upstream reports ~4 fps at 2K on a GPU PC;
  expect far slower here. 360p dev tests are the right scale; final 1080p/2K renders may need a GPU machine.

### 1.5 Runtimes and tools — Verified
| Tool | Version / status |
|---|---|
| Python | 3.13.18 (`/usr/local/bin/python3`), pip present |
| Node.js / npm / npx | v22.23.5 / 10.9.9 / 10.9.9; pnpm 10.28, yarn 1.22, TypeScript 6.0.2 global |
| FFmpeg / FFprobe | 6.1.1-3ubuntu5; encoders include libx264, libvpx-vp9, aac, libmp3lame (hardware encoders listed but no device) |
| git-lfs | present |
| yt-dlp | **missing** |
| Remotion, three, @remotion/three | **not installed** (no project yet) |
| Blender | **missing** |

### 1.6 Python libraries — Verified (`pip list`, 98 packages)
Present: numpy 2.5.3, pandas 3.0.5, pillow 13.0, requests, onnxruntime, PyYAML, pytest, mcp, claude-agent-sdk.
**Missing for this project:** opencv (cv2 import fails), scipy, scikit-image, matplotlib, librosa, soundfile,
faster-whisper, elevenlabs SDK, google-genai.

### 1.7 Network — Verified (`curl` status codes)
api.github.com 200 · youtube.com 200 · labs.google 200 · registry.npmjs.org 200 · pypi.org 200 ·
generativelanguage.googleapis.com 404 (reachable; root path) · api.elevenlabs.io 404 (reachable; root path) ·
github.com 400 at root (git over HTTPS works). Environment network policy: **unrestricted** (`get_environment`).
All HTTPS goes through an agent proxy with TLS re-termination.

### 1.8 Credentials present — Verified (names only, values not read)
GitHub tokens are injected by the platform. **No ElevenLabs, Google/Gemini or OpenAI API key** in the environment;
no network secrets saved on the environment. The session has claude.ai connectors for ElevenLabs, Google Drive and
Gmail (not exercised).

### 1.9 Claude Code subagents — Verified (tool availability only)
The Agent tool is available (general-purpose, Explore, Plan, web-fetch, etc.). No project `.claude/agents/` directory
exists yet. No subagent was launched in Phase 1.

### 1.10 Persistence — Verified / Inferred
- Container is ephemeral; reclaimed after inactivity. Only committed **and pushed** work survives (Verified by platform docs).
- Scratchpad and `/tmp` are cleared on reboot/cleanup. The reference clone lives there and will disappear.
- Environment has **no setup script**, so every fresh container starts without our dependencies.
- Another cloud environment named `animated-shorts-engine` exists on the account (not inspected).

## 2. Reference repository: `mromidev/claude-animated-shorts`

- Commit inspected: **`e3b817b6afc6cd413466d43f11ba31209e034bbf`** (2026-11-01, "Add 20 reference contact sheets"),
  2 commits total, 36 MB. Location: session scratchpad (outside the project). Nothing executed.
- Contents: `SKILL.md` (166 lines), `STYLE_BIBLE.md`, 8 reports (~4.3k lines), `templates/bridge/` (13 TS/TSX
  files, ~4.7k lines), `templates/audio/` (6 Python files + cues), `templates/scripts/` (5 helpers),
  `references/frames/` (38 JPGs, 540×960), `references/sheets/` (20 JPGs, 1800×1920).

### 2.1 Licence and restrictions
- Code and docs: MIT (© 2026 Mr omi). Reuse permitted with notice.
- **Reference frames and contact sheets are third-party video stills** ("included for style study only"); the MIT
  licence cannot grant rights to them. They must **not** enter our public repo (D001). The upstream text also says
  never to copy the channel's scripts, characters or shots — consistent with our rules.

### 2.2 Architecture
One Remotion composition (1080×1920, 30 fps) wrapping a `ThreeCanvas`; a single three.js world posed per frame from
a story timeline. Pinned stack in CONTEXT.md: Remotion 4.0.290, three 0.175, @react-three/fiber 9.1.2,
@react-three/postprocessing 3.0.4, postprocessing 6.37.2.

| Area | Files | Technique |
|---|---|---|
| Characters | `toon.ts`, `cast.ts`, `cardshade.ts` | Canvas2D `Pen` drawing API (600×1000 design canvas), bean heads, stick limbs, variable-width plum outline, 14-expression face library; camera-facing billboard cards lit by scene light; blinks, walk cycles |
| World | `build.ts`, `world.ts`, `paint.ts` | Procedural boxy houses + Kenney CC0 GLB props recoloured; HD procedural Canvas2D textures; sky gradient shader, fog = horizon colour; sight-line culler removes geometry blocking cameras |
| Lighting / shading | `lights.ts`, `shade.ts` | Day/golden presets; sun camera-relative, frozen per shot; two-tone stylised shadow colour (`twoTone`/`untone`) |
| Ink | `ink.ts` | Own screen-space pass from depth + normals before DOF; 5.1→3.3 px with distance; character cards on a NOINK layer |
| DOF | `lensblur.ts` | Custom thin-lens single-gather blur, per-beat `dofAt` table |
| Post | `Bridge.tsx`, `grade.ts` | ink → lens → bloom (emissive only) → NEUTRAL tonemap → fitted grade; MSAA 4; pixel params scale with height/1920 |
| Camera / timeline | `story.ts` | SHOTS, CAMS keyframes with smootherstep glides, push-in on holds, flip-sign impact kicks, crossfades, white flash; actions 0–3 f before the word |
| Audio | `templates/audio/*.py` | Event table mirrored from the picture timeline → synthesized SFX + original march score (NumPy/SciPy), ducking keyed from words.json, loudness to −15 LUFS |
| QA | `short_qa.py`, `sbs_sheet.py`, `bridge-stills.mjs` | Per-frame black/white/frozen/pop detection, EBU R128 loudness, silence, per-shot stats, contact sheets; still rendering; side-by-side sheets |

### 2.3 Reusable techniques (worth re-implementing in our own code)
1. Post-chain ordering (ink as its own pass before DOF; bloom after DOF; grade after tonemap) and resolution-scaled
   pixel parameters.
2. Depth+normal world ink pass with distance-tapered width; characters excluded via a layer.
3. Lit billboard character cards (no emissive) with contact blob shadows.
4. Word-timed shot plan: every reaction 0–3 f before its word; story timeline as the single source of truth for
   picture **and** sound.
5. Camera grammar: glides of 18–40 f, creeping push-in on every hold, sign-flipping decaying impact kicks.
6. Per-frame QA script (frozen spans, pops, loudness) — good pattern; port to OpenCV and our 24/30 fps rules.
7. Sandbox-per-owner experiment loop with merge script — maps well to our department ownership (Phase 2).
8. Readability-trap checklist (props near lens, ambiguous silhouettes, flag/sign errors).

### 2.4 Missing dependencies / non-portable parts
- No `package.json`, `Root.tsx`, `index.ts` or lockfile — it is a template set, not a runnable project.
- 26 Kenney GLB models expected at `public/bridge/kenney/*.glb` are **not included** (CC0, must be fetched separately
  and licence-checked).
- `voice.wav`, `words.json` and the `~/bridge-short/` project folder are not included.
- Analysis scripts cited by the reports (`references/<topic>/scripts/*.py`, `cam2.py`, `track.py`, …) are **not
  included**, so its measurements cannot be reproduced.
- Windows-specific paths (`C:/Program Files/Google/Chrome/...`, `D:` temp drive) and `gl: "angle"` GPU assumption.
- No ElevenLabs code: voice is "record or generate"; word timings from an unspecified STT.
- Python audio needs scipy (missing here).

### 2.5 Weaknesses and components to improve
- **Single-story coupling:** world, cast and timeline are hard-wired to "the bridge" short; needs a data-driven
  scene/shot schema to be reusable.
- **Characters are procedural Canvas2D drawings,** not AI-generated assets — no path for Google Flow art, separated
  body parts or a rig. This is our biggest architectural divergence (Phase 5).
- **No true 2.5D layering system** for generated plates; world is procedural geometry only.
- **Self-graded quality:** final scores (e.g. colour 5–7/10) come from its own Opus verifier, not independent review;
  scores remain mid-range by its own account.
- **Measurement gaps:** captions masked heuristically; DOF/blur measured on 720p re-encodes; reference walks from few
  samples; several values are explicitly "judgment calls".
- **Disk/temp hygiene problems** with Remotion bundles (110 GB reported) — relevant to our 60 GB allowance.
- Final export at 2K with `--scale 1.3333` assumes a GPU; impractical on our CPU container.

### 2.6 Internal inconsistencies found (do not adopt without re-measurement)
| Topic | Claim A | Claim B |
|---|---|---|
| Camera move shape | STYLE_BIBLE: "ease-out bursts, peak at first frame" | motion.md: that finding "is wrong"; moves are symmetric ease-in-out ~23 f |
| Hard cuts | STYLE_BIBLE: "almost never (0–1 per video)" | SKILL.md: "hard cuts on big jumps" |
| Loudness | STYLE_BIBLE: reference −14 LUFS | mix.py targets −15 LUFS |
| Day fog | SKILL look targets: 25→420 m | final values: 25→300 m |

### 2.7 Security review of upstream code
Grep for `child_process`, `exec(`, `eval(`, `curl`, `http` in templates: no network calls or shell execution in the
TS sources; Python uses `subprocess` only for ffmpeg/ffprobe. No install scripts exist. Low risk, but still not run.

## 3. Gaps between our vision and the upstream approach
| Our vision | Upstream | Gap |
|---|---|---|
| AI-generated original 2D characters (Flow) | Procedural Canvas2D | New asset pipeline + segmentation into parts |
| Separated parts + rig | Whole-card drawings swapped per pose | Rig system needed |
| AI environments / textures, 2.5D layers | Procedural geometry + Canvas2D textures | Plate/layer pipeline, depth estimation |
| ElevenLabs narration | External, unspecified | API integration + timestamps |
| 360p/24 fps dev tests | 540p stills, 30 fps | Our test harness |

## 4. Recommended setup script (proposed — not applied)
To run once Phase 2/3 are approved (versions to pin at that time):
```bash
apt-get install -y --no-install-recommends libgl1 sox
```
```bash
pip install opencv-python-headless scipy scikit-image matplotlib soundfile librosa
```
Project-local (in `package.json`, not global): `remotion`, `@remotion/cli`, `@remotion/three`, `@remotion/renderer`,
`three`, `@react-three/fiber`, `@react-three/postprocessing`, `postprocessing`, `typescript`.
Optional, decision-dependent: `faster-whisper` (word timings fallback), `elevenlabs` SDK, `yt-dlp` **only** if the
user confirms authorised acquisition of reference footage.
Note: saving a setup script changes the stored environment and requires user approval.

## 5. Open items
- Remotion licence: free for individuals/small companies; a company licence may be required depending on team size —
  confirm before commercial use (not verified in this phase).
- Reference footage authorisation and storage method for Phase 3.
- GPU availability for final-resolution renders.
