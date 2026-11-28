# A12 FINDINGS — visual effects (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A12.
(Written to disk by the director from A12's hand-off; the agent's Write tool refused the files. Content unchanged.)
Visual ledger: 38 records after Phase 3B (see Phase 3B additions; the 28-record text below is the Phase 3 state)
Visual ledger (Phase 3): 28 records (`knowledge/dataset/coverage/visual/a12-vfx-specialist.jsonl`): 18 overview sheets (180×320,
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

## F-a12-008 flash_candidate ≠ screen flash (PARTLY SUPERSEDED by F-a12-100/103: unopened candidates now opened; lightning/muzzle flashes do exist) (OBSERVED + MEASURED, medium; 4 videos, n = 8 candidates)
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

## Phase 3B additions (2026-11-28)
Ledger after 3B: 38 records, 29/30 videos with some visual evidence (all but RC30-26). Honest breakdown: every-frame
composites made from the A27 sheets (120x213 tiles, 14 consecutive frames per row) = 6 images / 36 windows in 21 videos
(01,03,04,05,06,08,09,10,11,12,13,14,15?,16,19,20,22,23,24,25,28,29,30; 15 only earlier); 1 fps overview sheets for the full
census exist for 22 videos (18 earlier + 10,14,17,20); 24, 25 have 14-frame windows only; 26 computational only.
Composites and scripts: private `agents/a12-vfx-specialist/{mkcomp.py,ser.py,c1..c6.png,ov*.png}`. Luma tables:
`data/luma_bumps_3B.csv` (80 returning bumps), `data/flash_candidates_luma_3B.csv` (all 43 flash_candidates).
Manifest SHA-256 `fc6f147a...8e06` (unchanged).

### F-a12-100 The three "not opened" candidates are not screen flashes (OBSERVED, high for these 3)
- 15-f001443 (luma 100->93): fast push-in; a dark ball enters and an object recedes; no overlay. Not a flash.
- 23-f000804..805 (128->99->back): foreground tree-foliage wipe uncovering a chest (A15 wipe); dip = dark foliage.
- 28-f000223 (luma 191->217 one frame, white background): iris-out from a white void with a black ring that grows and
  opens onto a room (f000216-f000229, ring scale ~x8 in 8 f). One-frame +26 luma pop sits inside the iris open; not a
  separate overlay at tile size (UNRESOLVED whether it is a deliberate white pop). Classification -> A15 (iris).

### F-a12-101 VFX census, 30 videos (OBSERVED at 1 fps / windows + A15 notes; counts NOT measured; medium-low)
Types per video (V = seen by me; A = only in A15 `transitions_confirmed.csv` notes). Impact flash/burst: 03(V,A lightning),
05(V muzzle 59, bullet impact A), 08(V fireball), 09(V), 22(V,A), 06(A explosion), 10(V mushroom fireball f1949).
Smoke/dust/steam: 22(V),03,04,07,08(V tyre dust),10(V train smoke, anger steam),12,14(V dust on fall),21(A). Sparks/embers/
sparkle/glitter: 01(V glitter+sun), 03,05(V),08,10(V rail sparks f1859),12,14(V flame aura),16(V golden glow),22,29.
Glow/wash/light rays: 02,04,05,13(V),15,16,17(V window shafts, lantern glow),19,20(V light-sweep overlays),21,22,24(V forge glow),28.
Lightning/flicker: 03,04,11. Speed lines/streaks: 10,14(flame/dust trail),21,22,11. Rain/water/liquid: 06,11,30. Fire/flame: 14,
22,24. Debris/shards/bills/confetti: 02,04,07,08,09,12(V money rain),22. X-ray/hologram/wireframe: 27, 15(?). UI overlays/
counters/markers: 01,04(V marquee),13,16,19(V inbox screen),27,29,30(V "AWAKE/LIGHT SLEEP" labels). Emotion marks: 04,13,18,21,22,29,10(V steam puffs).
Screen shake: not detected computationally (global-motion residual not examined) -> UNRESOLVED.
Every viewed video (29) has >= 2 effect types; the heaviest by effect-type variety: 22, 10, 14, 09, 05, 08, 11, 04.
Not seen: 26 (no census).

### F-a12-102 Frame-level timing, 18 effect events in 13 videos (OBSERVED every frame + MEASURED luma_mean; medium)
Videos: 01,03,04,05,08,09,11,12,16,19,22,24,28. Frame = 1/30 s. "base" = median luma 4-12 f earlier.
| Event | Build | Peak | Decay / end | Hold | Notes |
|---|---|---|---|---|---|
| 05-f000059 muzzle burst | 1 f (89) | 1 f (129, +49 over base 80) | cut next frame | 1 | white-gold star on character, ~60 % frame width, on ones; effect is the last frame of the shot |
| 22-f000038..051 cannon flame | 4 f | to f051+ | >14 f | >10 | orange cartoon flame blob with outline, grows ~x3, 2D sprite-flipbook look |
| 22-f000171..175 horizon muzzle glint | 0-1 f | 5 f | smoke bank f176+ | 5 | ~3 % of frame; then white smoke bank (hold >8 f) |
| 22-f000525..547 smoke cover | 15 f (puffs grow from barrel) | 3 f cover rise (150->188->226), peak 229 at f000542 | 3 f clear (192->150->117) | 6 f full | smoke fills frame and the next shot appears out of it = smoke-cover transition (A15 note) |
| 11-f000866..870 lightning | 0 | 2 f pulses at 866-867 and 869-870, +23 luma | 1-2 f gap | - | double flicker, full-frame pale tint |
| 11-f001181..1186 lightning | 0 | f1181 (+27), then 1183-1185 | to 97 by f1187 | - | 4 pulses in 6 f, decay tail ~3 f |
| 03-f001317..1330 bolt | 2 f | f1320-1325 (luma +37 over 10 f) | continues after f1330 | >12 | white-blue branching bolt redrawn every 1-2 f (on ones/twos), additive glow, ~25 % frame width |
| 09-f001544..1553 shatter burst | 1 f (+15) | f1545-1546 radial ray star | debris f1546-1553+ | 8+ | rays + shards, wall fragments; spawn full-density |
| 05-f001587..1599 dynamite sparks | 0 | continuous | - | 12+ | thin orange streak sparks + 2 f dust puff f1594-95 |
| 16-f000143..154 golden glow | 11 f (124->148) | f154 | cut f155 | - | additive warm halo on a prop |
| 19-f000748..761 UI white-out | 8 f (193->234 at f756) | 1-2 f | 5 f (220 by f761) | - | screen blooms to white, new illustration appears at the peak: bloom-dissolve (A15/A10) |
| 08-f001343..1356 tyre dust | 4 f | 3 f (peak 163 at f1351, +37) | 4 f | - | grey-white alpha cloud ~40 % width |
| 08-f001833..1846 rocket fireball | 4 f (first visible f1836 at ~25 % width) | f1838-1841 white core -> orange, peak luma 178 (+27) | >6 f | >10 | fireball ~60 % width, outlined puffs, 2D sprite |
| 01-f001498..1511 glitter + sun | - | loop | - | >14 | white specks stream + 15 % wide sun bloom |
| 12-f001862..1875 money rain | - | loop | - | >14 | 3D instanced bills |
| 24-f001131..1144 forge glow | 8 f (132->154) | hold | - | >6 | warm glow with flicker |
| 04-f000420..433 marquee blink | - | - | - | 14 | alternating bulb frames; label pop at f424 |
| 28-f000216..229 iris + 1-f pop | 1 f | 1 f (+26) | - | - | see F-a12-100 |
Drawn on ones/twos: hit bursts (05, 09) and lightning change shape every 1-2 f; ambience loops move smoothly (no stepping
seen at tile size). INFERRED compositing: lightning, glow, rays = additive; smoke/fireball/dust = alpha sprites with
cartoon outline (2D flipbook or baked); debris, money, sparks = 3D particles; wipes into smoke are the VFX itself.
Window rows judged NOT VFX (luma bump from cut, pan, wipe or crossfade): 12-f001464 (cut, first frame +35), 12-f000566 (iris-in),
10-f000851, 10-f000406, 30-f000714 (crossfades), 25-f000775 (pan), 20-f001038 & f001560 (smear / card zoom), 9-f001155
(window glare + tilt), 13-f001286, 6-f000540, 14-f001317 (eye zoom), 28-f001160 (paper-fold wipe), 16-f001645, 29-f000230.

### F-a12-103 Flash / luma peaks, 30 videos (MEASURED color.csv luma_mean; MEASURED medium)
Method: bump = luma_mean >10 above the median of frames i-12..i-3, run <=30 f, post-bump level within 8 of pre-bump level.
n = 80 bumps in 28/30 videos (none in 02, 07, 21; 03 and 13 have 1). delta median 15.8 (IQR 12.7-20.8); 22 bumps >= +20;
duration median 6 f (IQR 2.75-22). Rate median 0.45 per 10 s (IQR 0.19-0.64) -> supersedes F-a12-011 (1.3/10 s, which
included cuts). Top bumps: 22-f000525..547 (+99, peak 229.5, smoke cover), 12-f000571..592 (+89, iris-in to bright scene),
09-f001544..1569 (+50), 20-f001565..1585 (+40, card zoom), 03-f001319..1340 (+37, lightning), 12-f001464 (+35, cut),
10-f000853 (+36, crossfade), 25-f000775 (+36, pan). Only 2 bumps reach luma_mean >= 190: 22-f000542 (229) and 28-f000105 (197).
No true white-frame flash (luma_mean >190 for >=2 f from a normal scene) exists outside smoke/bloom builds (15 end 193; 19 UI 234).
All 43 `flash_candidate`s (data csv): 9 rise > +10 and return; visually these are lightning pulses (11: 866, 869, 1183), iris/zoom
(30: 856, 861; 28: 223), cut-in brightness (12: 1464), 13-f001293 (not opened), 9-f001164 (exposure dip, camera tilt). 34 do not
return or rise < +10 (pans, zooms, crossfades). Luma flash share of 43 candidates that are VFX: 3 lightning + 0 true overlay = 7 %.
Caveat: luma_mean averages the whole frame; a small bright effect (muzzle glint, sparkle) is invisible in it.

### F-a12-104 Preset sizes and colours (OBSERVED, low-medium; sizes from tile estimates)
Muzzle burst ~60 % width white-gold #FFF3C0; fireball up to ~60 % width orange #FF9A2A over white-yellow core; tyre dust ~40 %;
smoke bank 100 % cover; lightning bolt ~25 % width white-blue #CFE8FF with blue wash; golden glow warm #FFC94A; sun bloom ~15 %.

## Phase 3B revisions
- F-a12-008: "unopened" luma-only items now opened (F-a12-100); the sentence "true screen flashes rare or absent" is
  revised: lightning pulses and the muzzle burst are real flashes, white-overlay flashes still absent.
- F-a12-011: frequency 1.3/10 s SUPERSEDED by F-a12-103 (0.45/10 s on strict returning-bump definition, n = 30 videos).
- F-a12-010 (UI frame timing unknown) remains unresolved; F-a12-003..007, 009 unchanged.
- Coverage statement above replaces the Phase 3 "23/30 videos" (now 29/30 with ledger; census depth differs per video).
## Open (3B)
Per-video effect counts still not measured by hand; screen shake not tested; 13-f001293, 12-f000571 not opened;
effect-to-SFX lag still A21.
