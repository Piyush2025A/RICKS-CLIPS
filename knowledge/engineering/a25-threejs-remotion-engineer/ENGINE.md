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
- `src/contracts/`: `time.ts` (secondsToFrames = half-up on integer microseconds, BigInt, bit-for-bit with A20 common.seconds_to_frame), `narration.ts` (descriptor + validator, browser-safe), `narration-node.ts` (sha256 + verifyNarrationFile, Node only), `time.test.ts`, `narration.test.ts`, `assets.ts` (A24 facts + validator + LIGHTHOUSE_PLATE_V01), `beats.ts` (A20 beats parse/frames), `beats.test.ts`.
- `tsconfig.json` (strict, noUncheckedIndexedAccess, allowImportingTsExtensions; imports use explicit `.ts/.tsx`).

## npm scripts
`npm run typecheck` | `npm run studio` (untested here, no display) | `npm run still -- --frame 24 [--gl swangle] [--out out/x.png] [--audio]` | `npm test` (tsc + time + beats + narration tests) | `npm run synth-narration` | `npm run render-narration -- --descriptor <json> [--out out/x.mp4] [--frames a-b]`.
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

## Phase 5A corrections (2026-11-28)
Timing: `secondsToFrames` = A20 canonical rule (us = floor(t*1e6+0.5); frame = floor((us*fps+500000)/1e6), BigInt for the integer step;
rejects negative/non-finite t and non-integer or <=0 fps). Fixture `pipeline/voice/tests/fixtures/frame_conversion_vectors.json` 59/59 + 2.55@30=77, 0.0625@24=2, 0.1875@24=5.
`beats.test.ts` now exact (no tie tolerance): 14/14 spans equal to frames_24/frames_30 in productions/TEST6S/voice/beats.json.
Narration: composition `NarrationTest` (360x640, 24 fps, durationInFrames from `calculateMetadata` = secondsToFrames(duration_s, 24)), `<Audio>` + plate + BeatBox
placeholder (large/warm inside clause frames_24 spans). Node-only code lives in narration-node.ts because webpack cannot bundle `node:` imports (FAILED.md).
Synthetic end-to-end (`npm run synth-narration`, then `npm run render-narration -- --descriptor assets/private/audio/TEST6S/synthetic/narration.descriptor.json`):
169 frames, h264 360x640 24/1 (video 7.0417 s), AAC audio 48 kHz (Remotion encodes stereo), audio/format duration 7.061 s; render 6.1 s; plate SHA unchanged.
The stand-in is a 220 Hz tone, labelled `synthetic: true`, never a real voice.

## Accepting private narration (user steps)
Real files: original MP3 (44.1 kHz mono, 131,271 B, SHA-256 63768ec7be62105c34a6c2c43330e51c70fc8c85d9a946b7b9030afaad16927b; never modify) and the normalised VO WAV
(48 kHz mono 24-bit, -14.2 LUFS; <=10 MB). Both fit the private Drive layer.
1. On your computer compute the hashes (`sha256sum file` / `shasum -a 256 file` / PowerShell `Get-FileHash -Algorithm SHA256`); the MP3 must equal the value above.
2. Upload both to the Drive folder `ricks-clips-handoff` (unchanged names). Tell the director; a session downloads them.
3. Place them at `assets/private/audio/TEST6S/` (git-ignored; verify `git check-ignore -v assets/private/audio/TEST6S/<file>`). Never commit or move originals elsewhere.
4. Re-hash after transfer; compare to step 1. Measure the WAV duration with `ffprobe -v error -show_entries format=duration -of csv=p=0 <wav>`.
5. Create `assets/private/audio/TEST6S/narration.descriptor.json` (see synthetic example): `{"id":"TEST6S_vo","role":"vo","production":"TEST6S",
   "privatePath":"assets/private/audio/TEST6S/<wav name>","publicPath":"audio/TEST6S/<wav name>","sha256":"<WAV sha256>","duration_s":<ffprobe value>,
   "sample_rate":48000,"channels":1,"bytes":<size>,"loudness_lufs":-14.2,"true_peak_dbtp":<from A21 report if known>}`. Use the MP3 descriptor only if you want to render with the original.
6. `npm run render-narration -- --descriptor assets/private/audio/TEST6S/narration.descriptor.json`. The render throws NARRATION MISSING / SIZE MISMATCH / SHA-256 MISMATCH
   before bundling if anything differs. Audio is hard-linked into the ignored bundle (no copy into tracked paths).
Note: real duration (if not 7.06 s) changes the frame count automatically; beats.json times must come from the same audio.
