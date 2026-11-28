# A25 FAILED.md
No experiments run in this review (desk study; no installs, renders or code per director brief). Entries so far are documentation gaps, not failed approaches.

| Date | Attempt | Result | Lesson |
|---|---|---|---|
| 2026-11-28 | WebFetch https://www.remotion.dev/docs/three for determinism rules, version requirements, delayRender for textures | Page does not cover them (returned only ThreeCanvas, Sequence layout="none", SSR `gl: angle`) | Determinism and delayRender claims stay INFERRED; check `remotion.dev/docs/delay-render` and a `npm view` version-compat step during the approved setup phase |
| 2026-11-28 | WebFetch https://www.remotion.dev/docs/license for terms | Overview only; thresholds are on /license/pricing | Licence eligibility rests on `research/integration-feasibility.md` until re-verified |

## 2026-11-28 Phase 5A
- F-A25-F01 symlinked plate in publicDir: bundler dropped it; symlink in bundle: server 404. Use hard link.
- F-A25-F02 continueRender in texture onLoad: plate black (canvas not redrawn). Use advance() after commit.
- F-A25-F03 chromiumOptions.gl = angle / swiftshader / angle-egl: WebGL context creation failed (BindToCurrentSequence failed). Use swangle.
