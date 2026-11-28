<!-- owner: A26 | version: 1.0 | last_updated: 2026-11-28 -->
# A26 FAILED.md
| Date | Attempt | Result | Lesson |
|---|---|---|---|
| 2026-11-28 | `chromiumOptions.gl` = angle / swiftshader / angle-egl (diag composition, one run each) | WebGL2 and WebGL1 contexts both null in-page; confirms A25 F-A25-F03 | Use `swangle` only on this container/browser (158.0.8127.2) |
| 2026-11-28 | First draft of render.ts mixed `??` and `\|\|` unparenthesised | Syntax error before any run | Parenthesise mixed nullish/or expressions |
No determinism mismatches occurred (432/432 sequence frames identical), so there is no failed determinism result to record.

## 2026-11-28 Legacy MP4 colour (Phase 5A)
Initial encode (`pixelFormat yuv420p`, no `colorSpace`) was BT.601-encoded with an untagged matrix; reading it as BT.709 gives up to 40-level error. Lesson: always set `colorSpace: 'bt709'` and verify with a colour-patch test (COLOUR_5A.md). No other failures in this task.
