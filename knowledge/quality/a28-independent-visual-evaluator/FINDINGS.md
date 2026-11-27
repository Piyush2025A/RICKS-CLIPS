# A28 FINDINGS — Phase 3 evidence-quality audit (summary)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · visual ledger 1 record
(4 native frames, 540x960). Full detail: `evaluations/phase3-audit/AUDIT.md` (PARTIAL, turn limit).

## F-a28-001 Headline numbers reproduce from committed tables (MEASURED, high for arithmetic)
A15 shot 3.058 s (n 322, 24 videos), A15 type counts, A13 push 22.3 %/35 f (n 133) and smoothstep 48/74, A03 H/W 0.930
(n 12), A20 −14.1 LUFS (26 videos via A27) and mono (side −20.5..−32 dB, 4 videos, independent ffmpeg). Reproduction
validates arithmetic, not the underlying detectors (A13 magnitudes have no ground truth).
## F-a28-002 A09 shadow rule confirmed with nuance (OBSERVED, medium; 4 frames, 2 videos)
Hard card shadows in RC30-01-f000359; none in RC30-03-f000089/f000749 despite an adjacent campfire → per-scene switch.
## F-a28-003 A11 black level overstated by proxy (MEASURED, medium; 26 videos)
Native per-video median luma p1 18/255 (0.071) vs A11 0.099 at 270 px. Use ≈ 0.04–0.10.
## F-a28-004 Confidence labels too high (INFERRED from EVIDENCE.md rules)
A15 F-002 "high" (17 videos); A02 F-001 swap timing "high" (4 videos frame-level); A19 F-005 medium (1 fps, 4 listed
videos lacked tables); A22 F-005 medium-high (side channel only).
## F-a28-005 Unsupported implementation detail
A19 F-a19-001 "frame 0 is a posed scene" — frame 0 never viewed. A15 per-video shot range omits RC30-25 (1.28 s).
## F-a28-006 Ledger honesty (MEASURED, 7 agents)
A14, A09, A13, A12 pass; A02 acceptable (tile spans); A10 header overclaims 24 vs 18 viewed videos.
