# A12 FINDINGS — visual effects (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A12.
(Written to disk by the director from A12's hand-off; the agent's Write tool refused the files. Content unchanged.)
Visual ledger: 28 records (`knowledge/dataset/coverage/visual/a12-vfx-specialist.jsonl`): 18 overview sheets (180×320,
1 fps); 8 A27 every-frame sheets (120×213: RC30-15 ×2, 23, 27 ×2, 28, 30); 2–3 private strips from native decode
(180×320; RC30-04 f000863.., RC30-09 f000775.., RC30-22 f000199..; labels are ffmpeg-seek offsets, ±1 frame — the
exact kind split in the ledger is approximate). Videos with visual evidence: 23/30 (01–09, 11–13, 15, 16, 18, 19, 21–23,
27–30). Private strip script: `~/ricks-clips-private/analysis-data/rc30/agents/a12-vfx-specialist/mkstrip.sh`.
Limits: every-frame timing is n = 1 per effect type; 1 fps tiles miss short effects (per-video counts not measured);
word sync uses caption changes (±1–2 frames); no audio used; luma statistics only for 15, 23, 25, 27, 28, 30.
Confidence low–medium throughout.

## F-a12-001 Effect vocabulary (OBSERVED, medium, 23 videos; 1 fps tiles)
- Debris / splinters: 22-f000209..f000269, 02-f000899, 04-f000929..f001019, 07-f000479 & f000869 (money bills),
  09-f000809..f000839, 05-f000029 (muzzle burst).
- Red branching crack/vein lines: 09-f000779..f000839, 04-f000869..f000929.
- Smoke, steam, dust puffs: 22-f000539, 03-f000089 & f000119, 07-f000959, 12-f000059, 04-f000029.
- Sparks, embers, glints, sparkles: 03-f001199, 22-f000929, 05-f000239 & f001019, 16-f000059, 01-f000659, 29-f000239,
  08-f000689, 12-f001079 (sun flare).
- Glow / colour wash: 16-f000089..f000149 (golden), 15 end (white bloom), 28-f000978..f001001 (red),
  22-f001019..f001109 (sunset), 13-f000509..f000599 (glowing ring).
- Light rays: 02-f000029, 04-f000989..f001019 (radial burst), 19-f000299..f000479, 21-f000899, 05-f000059.
- Speed lines / streaks: 22-f000059 (cannonball), 21-f000149 & f000569, 11-f001049.
- Particles: splash 11-f000059; rain 06-f000989.. & 11-f000869; confetti 08-f000929 & 12-f000119; bubbles + caustic
  overlay 30-f000816..f000863.
- Emotion marks: sweat drops (13, 29, 22, 21, 18), "Z" sleep marks (04-f000659, 21-f001019), red anger eyes (04).
- UI / holograms: 01-f000209/f000239 countdown "2"/"GO"; 13-f000749 stopwatch counter; 16-f001079..f001169 coloured
  number highlights; 27 wireframe; 29 magnifier; 04 counter boards.
- Ghost overlays (06-f000179, 09-f000659, 02-f000869) are crossfade transitions (A15), not VFX.

## F-a12-002 Rendering style (OBSERVED, low–medium)
Environment effects (debris, smoke, rain, sparks, fire) look 3D and scene-lit. Line effects are flat 2D strokes without
thick ink outline; red veins have a soft pink additive halo; the RC30-27 wireframe is thin cyan lines. Glows and rays
are additive overlays. Bubbles are thin ring outlines; caustics a tiled bright-line texture. INFERRED: character marks
are 2D flat shapes; environment effects come from the 3D engine; no thick-ink particle systems.

## F-a12-003 Splinter burst (OBSERVED, low, n = 1: 22-f000199..f000246, every 2nd frame)
Caption word "smash". Star-shaped splinter hub appears ≈ f000203 for 1–2 frames; wall hole opens at f000201 and stays.
Shards fill the width by f000215; dense until ≈ f000231; still present at f000245 (+46 f). Model: spawn 1–3 f, hub
1–2 f, spread 12 f, dwell 10–20 f, fade 30+ f. Victim reaches full pose ≈ 5 frames in.

## F-a12-004 Red vein / crack growth (OBSERVED, low–medium; 09-f000775..f000846 every 3rd frame; 04-f000863..f000910 every 2nd)
- 09: floor cracks pre-exist; veins sprout from the body at f000799, ≈ 9 frames after caption "tattoos" (f000790), and
  extend in ≈ 6 steps over 18 frames; a faint expanding ring at f000820, f000829, f000838, each with longer branches;
  pink glow strengthens from f000820; debris specks at f000841.
- 04: red glowing eyes switch on in one step at f000886; road cracks spread over ≈ 8 frames from f000888; debris/dust
  rise f000892–f000896; red squiggles flicker 2 frames each f000889–f000899; camera pulls back simultaneously.

## F-a12-005 Hologram wireframe (OBSERVED + MEASURED, medium for this instance; RC30-27 f000768–f000815)
Object morphs into a wheel f000768–f000773. First overlay frame f000779: white veil + cyan cage; cage brightens
f000780–f000783 while the camera changes; from f000784 a persistent cyan perspective box with grid lines stays through
f000815 (36+ f). Lines thin, additive, constant width, ≈ #3EC8F0–#4FD3FF. The A15 gradual candidate 777–783 is this VFX
build — count it once.

## F-a12-006 Bloom-to-white build (MEASURED luma_mean + OBSERVED, medium; RC30-15 f001948–f001982)
luma_mean 46 (f001948) → 65 (f001952) → 103 (f001957) → 138 (f001959) → 175 (f001963) → peak 193 (f001968). Rise
≈ 20 frames (S-curve); decay 13 frames to 144; ≈ 155 in the next scene. A small glowing chip grows a warm halo until the
frame is white-gold; luma_p99 saturates.

## F-a12-007 Red mood wash (MEASURED a_mean + OBSERVED, low–medium; RC30-28 f000978–f000998)
a_mean 9.8 (f000980) → 26 (f000982) → 34 (f000984) → 38–41 (f000994): ramp 12–14 frames; holds 25+ frames (past
f001007); with soft vignette; caption "frightened".

## F-a12-008 flash_candidate ≠ screen flash (OBSERVED + MEASURED, medium; 4 videos, n = 8 candidates)
Opened: 15-f000027..29 fast push-in blur; 15-f001930..32 camera move; 15-f001966 inside the bloom; 23-f000148..153
foreground tree-trunk wipe (A15); 28-f000970 zoom through a mouth; 30-f000856 & f000861 iris zoom with radial streaks.
Luma only (not opened): 15-f001443 (100→93, no spike); 23-f000804..805 (dip 128→99→back, probably a wipe); 28-f000223.
No viewed candidate is a white/colour overlay flash → true screen flashes rare or absent. Classification → A15.

## F-a12-009 Shine sweep (OBSERVED + MEASURED, medium; RC30-27 every frame)
Caption "jackpot" at f000640; sweep starts f000643 (+3 f), moves right as a diagonal streak ≈ 12 % of bar width, exits
by f000650 (8 f); bar saturates f000651–f000657; second smaller glint f000669–f000671 on the "7" icon.

## F-a12-010 UI pop-ins (OBSERVED at 1 fps only, low)
Countdown digits, stopwatch counter, coloured grid highlights are synced to words at ≈ 1 s steps; frame timing unknown.

## F-a12-011 Frequency (MEASURED luma only, low)
Merged |Δluma_mean| > 8 events, 15-frame gap (upper bound — includes cuts and wipes):
| Video | Events | Per 10 s |
|---|---|---|
| 15 | 11 in 77.8 s | 1.4 |
| 23 | 5 in 40.6 s | 1.2 |
| 25 | 8 in 34.4 s | 2.3 |
| 27 | 4 in 30.9 s | 1.3 |
| 28 | 5 in 40.0 s | 1.25 |
| 30 | 3 in 39.1 s | 0.77 |
Median ≈ 1.3 / 10 s (n = 6). 22 of 23 viewed videos show ≥ 3 VFX types in 40 s. Heavy: 22, 04, 09, 11, 02, 05, 07;
light: 19, 18, 29, 13. "VFX per minute" not measured (needs a hand count).

## F-a12-012 Story-beat triggers (OBSERVED + INFERRED, low–medium)
Impacts/destruction; rage and emotion peaks; reveals of valuables (gold glitter, jackpot shine, memory-card glow);
science explanations (x-ray, caustics, colour wash); looping ambience (fire, smoke, rain, dust, rays).

## Contradictions and uncertainty
Calibration note's RC30-27 "stamping/counter" not re-examined. A04 F-a04-006 (VFX delivers follow-through) supported
qualitatively (22, 09, 04); impact-to-pose lag not measured. The wireframe fade is both an A15 candidate and a VFX —
count once.

## Open questions
A21: sync of shine (27-f000643), splinter burst (22-f000203), vein start (09-f000799) vs SFX onsets. A15: classify the
27 wireframe fade, 23 prop wipe, 30 iris zoom. Phase 7: validate E01–E18 at 24 fps in short A/B tests before `src/fx/`.
