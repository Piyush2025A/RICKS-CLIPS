# ENGINE.md — Phase 5A engine foundation (A25, 2026-11-28)

## Pinned versions (npm view, 2026-11-28; exact pins in package.json)
remotion / @remotion/cli / @remotion/three / @remotion/renderer / @remotion/bundler 4.0.547 (all must be identical);
react + react-dom 19.3.1 (R3F 9.8.2 peer: react >=19 <19.4); three 0.187.0 + @types/three 0.187.0; @react-three/fiber 9.8.2;
@types/react 19.3.3, @types/react-dom 19.3.0, @types/node 22.20.7 (Node 22.23.5); typescript 5.9.3 (npm `latest` is 7.0.2; not
used: untested with Remotion/R3F types, deliberate conservative pin). No zod (hand validators). No postprocessing libs.
@remotion/three peer: three >=0.137, @react-three/fiber >=8.
Licence: https://www.remotion.dev/docs/license/pricing re-checked 2026-11-28 (WebFetch): free for individuals and companies of up to 3 people,
all features, unlimited commercial use, subject to Terms (D008 holds).

## Structure
- `remotion/index.ts` registerRoot; `remotion/Root.tsx` composition `EngineTest` 360x640 @24 fps, 48 frames; `remotion/EngineTest.tsx` ThreeCanvas scene.
- `remotion/scripts/still.ts` still renderer (bundle + renderStill).
- `src/engine/`: `useTexture.ts` (delayRender-aware texture hook, sRGB), `PlateCard.tsx` (cover-scaled unlit background card), `PlaceholderCard.tsx` (box animated from useCurrentFrame).
- `src/contracts/`: `time.ts` (secondsToFrames = floor(t*fps+0.5)), `assets.ts` (A24 facts + validator + LIGHTHOUSE_PLATE_V01), `beats.ts` (A20 beats parse/frames), `beats.test.ts`.
- `tsconfig.json` (strict, noUncheckedIndexedAccess, allowImportingTsExtensions; imports use explicit `.ts/.tsx`).

## npm scripts
`npm run typecheck` | `npm run studio` (untested here, no display) | `npm run still -- --frame 24 [--gl swangle] [--out out/x.png] [--audio]` | `npm run test:beats`.
Env `RC_BROWSER` overrides the browser executable (default: Remotion's own downloaded chrome-headless-shell 158.0.8127.2, in git-ignored node_modules/.remotion).

## Private asset serving
Remotion's bundler copies publicDir and drops symlinks; its server (serve-handler) has symlinks disabled (404 seen). Working method: bundle into
git-ignored `out/remotion-bundle`, then HARD-LINK the plate into `out/remotion-bundle/public/flow/` (same inode, no byte copy; falls back to a copy
inside out/ only). `git check-ignore -v` confirms `assets/private/` and `out/` ignored; plate SHA-256 verified before and after every render (unchanged).
Caveat: the hard link lives in out/; delete out/ safely (original keeps its inode). Never `chmod`/write through the link.

## Determinism rules
No `useFrame`, `Math.random`, `Date`, `performance.now()` for animation; all motion = f(useCurrentFrame()/fps). Time authored in seconds.
During rendering ThreeCanvas runs `frameloop="never"` and advances only on frame change: any async content (textures) must call `advance()` after commit
before releasing its delayRender (implemented in useTexture.ts). Colour: `flat` (NoToneMapping), outputColorSpace sRGB, texture sRGB, plate material toneMapped=false.
Captions: none (prop `captions` default false, no component).

## Limitations
gl modes: only `swangle` created a WebGL context here; `angle`, `swiftshader`, `angle-egl` all failed ("Could not create a WebGL context", FAILED.md).
Hash determinism verified per machine/flags only. Audio component only compile-checked plus mounted in a still with a synthetic WAV (no audible/video render test).
Cover scaling trims ~0.4% of plate height (aspect 0.5581 vs 0.5625) top/bottom in total. Remotion prints a memory-detect warning (CGroup) harmlessly; three 0.187 warns THREE.Clock deprecated (from R3F).
