# A13 FAILED approaches

## FAIL-001 — Counting all "moves" at a low threshold overstates camera craft
First pass (hold-vs-move at 0.5x thresholds) classified 56-92 % of frames as move and 555 moves, 55 % of which are fast, transition-like events (crossfade tails, screen-zoom reveals, object motion leaking). Lesson: split tiers (fast/non-fast, near-candidate) before fitting easing; the pooled fit (linear/ease-out mixed) hides the symmetric smoothstep majority in the clean subset.

## FAIL-002 — Shake detector on global motion
Sign-alternation burst detector (>=3 alternations/12 f, >= 1 %W) fired 136 times; visual check showed object (droplet) motion and fast action leaking into the global model, no camera shake. Not a valid shake detector at 320 px; "no shake" is concluded from quiet-frame RMS and two viewed sequences only. A proper detector needs a static-background mask (A27 residual mask / region of rim pixels).

## FAIL-003 — Word-lock test with caption events
Caption changes every ~9 f (3 events/s), so the baseline chance of an onset within +-3 f is 63 %; the test has no power. Also capev.json exists only for videos 1-10 (7 overlap). Needs word-level onset times (A20 forced alignment) and the full batch.

## FAIL-004 — Orbit / dive-into-eye detection
Not separable in a 2-D similarity model (pan+roll+scale ambiguity); not inventoried as such. Needs 3-D camera pose (not available) or manual viewing of all 30 overview sheets.

## FAIL-005 — Move window definition near masked crossfades
Windows truncated by the +-2-frame candidate mask give flat (linear/ease-out) profiles; boundary-adjacent group (n=159) is therefore less trustworthy than the clean subset (n=74).
