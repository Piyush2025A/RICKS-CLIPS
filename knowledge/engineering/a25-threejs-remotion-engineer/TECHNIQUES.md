# A25 TECHNIQUES — module architecture and implementation order
Status: PROPOSAL (INFERRED, nothing built, no code files). Promote an item to "approved" only after an EXP record with a 360p still.
Global rules (INFERRED from DOC-1/DOC-2): (1) every animated value is a pure function of `frame`, `fps`, and static props; no `useFrame`, `Date.now`, `performance.now`, `Math.random` (use seeded PRNG `mulberry32(hash(id))`); (2) author in seconds or 30-fps frames, convert once; (3) screen-space sizes in "px at 1080 wide", scaled by `renderWidth/1080`; (4) renders via `chromiumOptions.gl: 'angle'` (software fallback = SwiftShader; `swangle` recommended by docs for no-GPU), long renders split into segments (angle leak, DOC-2).

## Module list and contracts
Notation: In -> Out. Owners per OWNERSHIP.md; A25 owns `src/contracts/` and `src/engine/`.
| # | Module | Owner of internals | Inputs (contract) | Outputs |
|---|---|---|---|---|
| M1 | Timeline / EDL | A16 data, A25 runtime | `EDL.json` (shots in seconds, transitions seconds, camera key, lighting preset id, card cues), `fps`, `words.json` | `ShotPlan[]` with integer `[startFrame, endFrame)`; transition overlaps; `frameToShotLocal(frame)` |
| M2 | Scene graph / world builder | A05, A08 | `SetSpec` (type, footprint, props, instance lists, materials by class id, time-of-day variants) | `THREE.Group` set + named anchors (card marks, camera corridors, light rigs) |
| M3 | Card rig | A06, A04, A01 | `CardSpec` (layer atlas, pivots in HW units, pose library id), `CardState(frame)`: root xyz, pose, limb control points, face state ids, tint | billboard group (yaw-only), card meshes with alpha-test; depth material for shadows; contact blob |
| M4 | Face/expression scheduler | A02 | `ExpressionTrack` (state id + start in 30-f frames or word index+k), `words.json`, seed | `FaceState(frame)` (eyes, brows, mouth, accessories, wobble offset); blink schedule |
| M5 | Card shader | A10 | `CardShadeParams` from lighting (uShade, uMinExp, uSkyTint, uPractical, uFaceFloor), albedo atlas | ShaderMaterial |
| M6 | Camera rig | A13, A14, A07 | `CameraKey[]` per shot (start/end framing x,y,scale or position, move type, easing id, duration s, fov, principal-point shift) | `PerspectiveCamera` state for frame; optional `zoom2d` scale about target; safe-zone check data |
| M7 | Lighting presets | A09 | `LightingPreset` id + blend (a, b, t) | light rig values (key, hemi, practicals, fog, shadow flags, cardShadow mode), interpolated per frame |
| M8 | Post stack | A10, A11, A07 | `PostSpec` (outline on/off + widthPx, AO on/off, DOF bokehScale and focus target, bloom params, grade LUT id/params, vignette), `uiScale` | composited framebuffer via ordered passes: outline -> AO -> DOF -> bloom -> tonemap -> grade -> vignette -> output |
| M9 | Grade LUT toolchain | A11 | offline stills + mood id | `lut-<mood>.png` (neutral 16^3 strip) + params JSON (offline Python; not runtime) |
| M10 | VFX library | A12 | `EffectCue` {id E01-E18, tStart s, params, seed, anchor} | meshes/sprites/overlays with analytic positions in t; DOM overlay layers for 2D-only effects |
| M11 | Transitions | A15 | `Transition` {type crossfade/cut/zoom/iris/cover/fly, seconds, from, to, params} | overlap Sequences + opacity ramp (default), or shader mask for iris/zoom; sources: two scenes in overlap |
| M12 | Captions | A14/A20 | `words.json` (word, t_on, t_off), style | DOM layer in safe band (y 1290-1420 @1920), lead 70 ms; outside WebGL |
| M13 | Asset registry | A24/A25 | Flow outputs in `assets/` (git-ignored), manifest with hash | preloaded textures with `delayRender`, sRGB flags, mipmap policy |
| M14 | QC / dev overlays | A28/A29 | frame, render | safe-zone overlay, determinism hash test, tsc, 24-fps frame-accuracy test, per-frame timing log |
| M15 | Render orchestrator | A25 | composition id, range, quality flag (dev/final) | segmented renders + ffmpeg concat + BT.709 limited tagging (A11 T0); logs seconds per still |

## Remotion composition layout (INFERRED)
`Root` -> `Composition(id, fps, width, height, durationInFrames from EDL)`. `Shot` = `<Sequence layout="none">` inside a single `<ThreeCanvas>` for 3D scenes (DOC-1); captions and 2D overlays sit in sibling DOM layers above the canvas. Crossfades: overlap two `Shot` Sequences; opacity applied via material/render-target blend (M11) rather than DOM so the grade stack applies once (or two canvases if post stack is identical per scene; cheaper to build, grade applied per scene).

## Contract rules (src/contracts/ vocabulary)
Types to define (names only): `Seconds`, `Frame30`, `FrameLocal`, `PxAt1080`, `ShotPlan`, `CameraKey`, `LightingPreset`, `CardSpec`, `CardState`, `FaceState`, `PostSpec`, `EffectCue`, `Transition`, `WordTiming`, `RenderQuality {dev|final}`. All are plain serialisable JSON so Python tools (A11, A16 QC) share them. `PxAt1080` -> pixels via `uiScale`. Quality flag only changes resolution-dependent cost knobs (shadow map size, AO/DOF on/off, bloom resolution); never changes timing or composition.

## Implementation order for Phases 5-8 (each step = one EXP with one 360p still, plus a two-render hash test)
1. Phase 5a scaffold (after approval): pinned versions check, `tsc --noEmit`, Remotion + ThreeCanvas hello still, measure `still_time`, determinism hash twice. Gate: tsc 0 errors, hash equal.
2. 5b contracts + M1 timeline + M15 renderer segmenting; frame-accuracy test at 24 fps (frame N maps to same sec as 30-fps timeline).
3. 5c M2 minimal set (floor, wall, 3 props) + M7 lighting presets DAY/NIGHT + M3 card with a placeholder alpha PNG + M5 shader. Check edge fringe on bright/dark at 360p.
4. 5d M6 camera moves (T-01..T-03b, expDecay entry) with easing functions from A13; test frame positions numerically.
5. 6a M8 minimal post: bloom + grade (A11 T1) + output; then M9 LUT fit on a still against A11 mood table.
6. 6b M4/M3 face + blink + word-timed swaps (needs ElevenLabs word timestamps from A20, approved spend only).
7. 6c M11 crossfade (5/6 f), hard cut; then zoom/iris/cover.
8. 7a M10 starter VFX E01, E02, E07, E08, E09, E12, E15 (cheap, high reuse); defer E13, E17, E14.
9. 7b Outline pass (treatment B) + DOF; evaluate cost at 360p; decide A vs B via A28 stills; SSAO last, probably baked.
10. 8 Final-quality path: 1080x1920 30 fps on laptop or GPU box; A26 budgets; cross-machine PSNR tolerance instead of hash equality.

## Dev/final parity checklist
Same code path; knobs: `uiScale`, shadow map size (1024 dev / 2048 final), outline min-width clamp 1 px at dev, AO off at dev, DOF off at dev unless shot tests it. Record each knob in the render manifest so stills are comparable.

## Open questions for director
1. Pick treatment A (lit PBR, no ink) or B (ink pass) before Phase 6; outline pass is the biggest single cost and conflict source.
2. Approve one `npm view` compat check and Remotion Free licence re-verification at setup.
3. Where will final 1080p renders run (laptop HD 620 or rented GPU)? Container software GL is only for dev.
4. Hand-offs: A10/A05 on toon vs standard (C2); A06/A07 on pitched cards (C10); A11 on face floor vs grade (C11); A26 for first benchmarks.
