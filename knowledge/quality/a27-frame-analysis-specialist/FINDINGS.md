<!-- owner: A27 | format: knowledge/_system/templates (finding) | evidence-backed only -->
## F-a27-001: slow-dissolve post-pass does not close the recall gap (MEASURED, medium-low)
Windowed cumulative difference over shot_features.csv recovers at most 1 of the 4 A15-listed rcpipe misses without
flooding (the other settings that reach a second miss add >= 22 new flags per 12 videos at <= 9 % precision).
n = 4 known misses, 228 XF rows (226 already candidates); reference list is not independent of rcpipe candidates.
Details and parameters: FAILED.md X-A27-011. Script: private, slow_dissolve_postpass@1.0. Decision: keep rcpipe
candidates as-is; slow same-palette dissolves need visual search (A15 gap checks), not a table post-pass.

## F-a27-002: all 30 RC30 videos fully accounted (MEASURED, high)
50,898 / 50,898 native frames; per-stage coverage and caveats in PHASE3_RUN.md; ledgers in
knowledge/dataset/coverage/computational/ validated against the repo schemas (60 records, 0 errors).
