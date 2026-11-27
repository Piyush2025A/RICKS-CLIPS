# A05 FINDINGS — how the reference channel builds environments (Phase 3, wave V1)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · date 2026-11-28 ·
visual-ledger records: 39 (`knowledge/dataset/coverage/visual/a05-3d-world-designer.jsonl`) ·
videos covered: 30/30 at one-frame level (montage f000450); 24/30 with a full 1-fps overview sheet (01-14, 16-22, 25, 29, 30); 10 consecutive-frame strips; 4 native crops.
Computational: `motion.csv` for RC30-15 and RC30-27 only (other videos not yet processed by A27 when this was written).
All view-based claims are at 180x320 (sheet tile), 240x427 (strip/montage) or native crop; counts are manual and approximate.
Original-work rule: everything below describes *technique*; do not reproduce their sets, characters or signage.

## F-A05-001 — The worlds are real 3D scenes with flat cut-out characters placed in them
- Label: OBSERVED. Confidence: high (24 sheets + 30-frame montage, consistent in every video; strips show perspective change).
- Evidence: strips RC30-04-f000149..f000199 (orbit/dolly from tree to road, horizon and road vanishing point rotate, tree shrinks with correct perspective), RC30-06-f000089..f000139 (low dolly up a path, parallax between grass, army, hills), RC30-10-f000059..f000109 (dolly along rails: rail sleepers/telegraph pole/cliff all converge, train occludes pole), RC30-13-f000119..f000169 (crane-up from plaza to bird's-eye: houses on concentric rings re-project, ground-plane circle foreshortens), RC30-01-f000569..f000619 (cockpit: window frame, seats, starfield move at different rates, camera tilts), RC30-25-f000509..f000559 (corridor with 3D arches, door jambs occluding the far wall).
- Method: viewed 6 frames at 10-frame spacing per move; judged parallax, occlusion, vanishing-point rotation.
- Limits: parallax judged by eye; dolly vs zoom is not separable in `motion.csv` (calibration §3).
- Characters: flat 2D bean/ellipse bodies with thick black ink outline, thin stick limbs; they keep a camera-facing silhouette across the move (billboard / cut-out in 3D) — RC30-04 f000149..f000199, RC30-06 f000109..f000139, RC30-10 f000059..f000109.
- Implementation: Three.js scene with a real perspective camera; characters as camera-facing planes (A03/A06 own those); never fake camera moves with 2D scale/pan on a flat plate.

## F-A05-002 — Camera is moving almost constantly, which is why true 3D is required
- Label: MEASURED (2 videos) + OBSERVED. Confidence: medium (n=2 for the numbers; overview sheets suggest the same in all others).
- Evidence: `motion.csv` (proxy <=320 px): RC30-15 camera-moving frames 58.6 % (1,367/2,333 valid), scale-change (dolly/zoom) in 51.5 %; RC30-27 79.7 % moving, 74.8 % scale change; median |t| 1.11 / 3.18 proxy-px/frame. Threshold |t|>1 px or |scale-1|>0.002. Command: inline Python over `v0.2.0/RC30-{15,27}/motion.csv`, rows with non-NaN tx.
- Limits: proxy resolution; thresholds are mine (not validated); static shots with small drift counted as moving when |t|>1.
- Implementation: design every set to be seen from a moving camera; leave no flat backdrop visible through a >=15 degree move.

## F-A05-003 — Environment taxonomy (recurring location types)
- Label: OBSERVED. Confidence: high for existence of categories (all 30 videos), low for exact counts (eyeballed from 1-fps sheets).
- Categories with keys:
  1. Real-world interior set (rooms with floor, walls, ceiling, a dozen to ~40 props): 01 (toilet, mission control, crew pod), 02 (cells, vault, guard corridor), 03 (tent), 05 (mine drift, assay office), 09 (paint shop, cell block "pod C"), 12 (betting room), 16/18 (lottery shop), 17 (attic bedroom, parlour), 19 (office), 20 (house), 21 (throne hall), 26/27 (slot parlour), 29, 30.
  2. Exterior landscape / street at wide scale: 04 (road with one tree, town), 06 (fort and field), 10 (canyon railway), 12 (town street, racetrack), 14 (Western main street), 03 (camp at night), 08 (fairground), 13 (circular town), 24 (road/tournament lawn).
  3. Cutaway / cross-section ("x-ray" side view): 02 f000089..f000239 (street + soil layers + tunnel + vault), 17 f000119..f000299 (coffin under graveyard, soil strata), 15/27 holographic wireframe (calibration §1.7), 30 brain-wave depth diagram (f000749..f000809).
  4. Macro "object hero" worlds (object fills frame, shallow DOF): 05 gold pan/assay dish f000869..f000929, 09 paint mixing f000149..f000239, 16 scratch card / printing machine f000569..f000659, 18 ID/wallet f000449, 22 powder bag/hot-shot oven f000689..f000869, 29 combination panel, 30 pinboard f000869..f000929.
  5. Inner-body / metaphor worlds (diegetic miniaturised): 25 whole video is a bloodstream-as-corridor-and-house metaphor (f000149..f000959), 30 brain/hypnagogia ocean.
  6. Abstract/diagram inserts (flat UI over a 3D plate, text on a plane): 01 f000149..f000209 world map / countdown UI, 16 f000989..f001199 number grids, 12 binoculars/scope circle vignettes f000389, f000569..f000599, 29 f000749..f000869 city of floating numerals.
- Locations per video (manual, from 1-fps sheets, distinct set identities in first 40 s): 01 ~7, 02 ~6, 03 ~4, 04 ~6, 05 ~7, 06 ~4, 07 ~8, 08 ~5, 09 ~6, 10 ~7, 11 ~3 (ship, sea, deck zones), 12 ~6, 13 ~5, 14 ~4, 16 ~6, 17 ~8, 18 ~7, 19 ~4, 20 ~5, 21 ~6, 22 ~4, 25 ~4, 29 ~6, 30 ~5. Median ~5-6 in ~40 s, i.e. a new location roughly every 6-8 s. Limits: counts eyeballed, +/-1.
- Recurrence: a hub set is revisited with a different camera angle: 02 vault (f000149, f000239, f000569), 01 cabin/toilet (f000029, f000509, f001019), 03 camp (f000089..f000239 and f000599..f001199), 12 betting room and racetrack; 16/18 shop counter. Time/mood varies per revisit (see F-007).
- Implementation: budget ~5-8 sets per 30-60 s short, 1-2 of them hubs reused 2-3x with new camera positions; one reusable hub-set build amortises cost.

## F-A05-004 — Two environment art treatments coexist (contradiction-in-style, not in technique)
- Label: OBSERVED. Confidence: medium (one frame/video + sheets; boundaries are fuzzy).
- Treatment A "lit PBR / game-engine": soft real-time lighting, bloom, photographic-feeling textures (tree bark, grass blades, gravel), no outlines on scenery. Native crops RC30-04-f000299, RC30-07-f000389; also 01, 02, 03, 05, 06, 09 (concrete/brick), 10, 26, 27.
- Treatment B "inked / illustrated": scenery carries dark contour lines, flat or gradient fills and painterly noise textures, simplified props (windows as rectangles with stripes, palm leaves as outlined shapes). Native crops RC30-25-f000519 (corridor with outlined arches/doors), RC30-29-f000359 (tower with outlined facade). Also 15, 16, 17, 18, 19, 20, 21, 30.
- Intermediate/hybrid (toon shading, light outlines or none, saturated gradient skies): 08, 11, 12, 13, 14, 22, 23, 24, 28.
- Trend by key: A dominates keys 01-07/09 and 26-27; B dominates 15-21, 25, 29-30; hybrid 08, 10-14, 22-24, 28. Keys are ordered by publication date (newest=01), so there is no monotone drift; it is a per-video choice, perhaps tied to subject (science/body/money = B). HYPOTHESIS only; test would need identity metadata (deferred D028).
- Both treatments are the SAME construction: perspective 3D geometry + flat characters + camera moves (F-001); B adds an outline pass/painted textures. Corridor RC30-25 f000509..f000559 shows contour lines staying locked to geometry edges under camera motion (inverted-hull or post-process line, not hand-drawn per frame) — OBSERVED, medium.
- Implementation: choose ONE treatment per production for consistency; recipe in TECHNIQUES T-04 / T-05.

## F-A05-005 — Scale conventions: characters are small relative to architecture, props are scaled for readability
- Label: OBSERVED/INFERRED. Confidence: medium.
- Characters ~0.8-1.4 "door heights" tall in sets; in establishing shots they shrink to <10 % frame height (RC30-03 f000029, RC30-21 f000449..f000479 with an army of hundreds, RC30-13 f000149..f000209, RC30-29 f000359). Mid shots put the head at 15-25 % frame height; close-ups fill 40-60 % (heads up to full width, e.g. RC30-02 f000749, RC30-19 f001019).
- Hero props are exaggerated: slot machine larger than the character (27), paint can, stopwatch, button pedestal (13 f000719..f000749), cannon barrels (22). Doors ~2.0-2.2 m are used as scale cues (09 cell door, 25 corridor doors) but chairs, tables and toilets are drawn at normal scale beside bean characters that are ~1.3-1.6 m tall with proportionally long legs.
- Limits: no calibrated measurement (no camera intrinsics); H-1 (vanishing-point recovery) not run.
- Implementation: model sets at real scale (door 2.1 m); give character planes 1.5 m height and let hero props go 1.5-3x oversize.

## F-A05-006 — Set-dressing density: dense foreground+midground, calm back-plane
- Label: OBSERVED. Confidence: medium (manual, 4-6 sheets studied closely).
- Establishing interiors typically hold ~25-60 distinct objects in frame (02 f000389 cell block: tables, stools, bunk rails, monitors, bars; 16 f000299 shop shelves; 25 f000509 corridor ~40 doors/lamps/tables as repeating pattern; 01 f000149 mission control: ~15 screens/consoles). Mid shots reduce to ~8-15 recognisable items near the character. Repetition (instanced pattern: doors, crowd, houses on rings, seats, coins) supplies density cheaply — 13 f000149 (~200 houses), 21 f000449 (thousands of soldiers), 12 f000869 (crowd stands), 29 f000989 (100-coin grid).
- Heavy depth-of-field blur on foreground/background bands in two-shots and macros (calibration §1.7; 02 f000299..f000337 region, 05 f000869..f001139) hides low-density areas.
- Limits: count = my manual estimate; no per-frame annotation grid yet.
- Implementation: instanced meshes for repetition; DOF + fog to fall off density at distance.

## F-A05-007 — Time-of-day / mood palettes per location type (descriptive; lighting detail is A09)
- Label: OBSERVED. Confidence: medium.
- Narrative night = deep blue shadows with warm practical lights (candles, lanterns, windows): 03 camp (f000029..f001199), 08 f000509..f000839, 17 f000329..f000959, 13 f000419..f000689, 07 f000869..f001139, 20 f000029, f001079; 06 rain night f000899..f001079.
- Dawn/dusk = orange-pink gradients with long shadows: 06 f001109, 14 f000779..f000869, 22 f001019..f001109, 21 f000899..f000989, 29 f000779..f000869, 07 f000569..f000839 (purple dusk).
- Day exteriors = saturated blue sky, green grass, high-contrast shadows: 04, 06, 08, 10, 12, 14, 24, 28.
- Interiors = single dominant hue per set: red (25 body), pink (09 cell after paint), teal/white (09 yard), yellow-green office (19), warm amber (16, 05 mine), cold blue (01 cockpit, 30 brain). A palette shift marks a location change and a time jump (e.g. 08 day -> night -> day).
- Implementation: one key hue + complementary practicals per set (A09 owns the lights); a day/night pair of the same hub set.

## F-A05-008 — Signage and in-world text are heavily used and are diegetic planes
- Label: OBSERVED. Confidence: high (>=15 videos).
- Examples: 04 "DAYS SINCE LAST CRASH" counter (f000329..f000359), marquee arrow sign (f000389..f000479); 05 newspaper "MILLIONAIRE DUE TO-MORROW" (f000449), "SURE THING MINE" (f000659); 01 "NO FLUSHING TONIGHT" screens, "OFF COURSE" HUD, hull lettering; 08 "OPENING TOMORROW" banner (f000329..f000449); 10 "FIRST LINE IN GETS IT ALL!" (f000329); 12 betting board odds; 16/18 scratch tickets as hero cards; 22 crate labels "LANGRAGE", "CARCASS"; 27 slot UI; 29 "AUDIT" plaque, numbers on tower. Text is on planes/props inside the scene with perspective, sometimes animated counters/LEDs (04 counter 7 -> 0; 07 "DAYS SINCE" desk calendar).
- Limit: text content is invented per script; do not copy.
- Implementation: canvas-texture planes in the scene, with a Canvas->Texture pipeline; keep in-world copy separate from the burned-in caption band (~70 % frame height, per calibration).

## F-A05-009 — Cutaway / cross-section worlds are built as a thin 3D slab with a straight-on camera
- Label: OBSERVED. Confidence: medium (02, 17, 15/27, 30).
- 02 f000089..f000119: street above, soil layers with pebbles/pipes, tunnel strip below; the camera is nearly frontal and almost static, with the brick shaft and strata lit from within; 17 f000139..f000169: coffin and bell rope cross-section, camera moves from perspective bell-post view (f000119, f000129) to frontal slab (f000139+). Characters (flat) lie inside the slab. Strata are bands with noise texture and inset objects (stones, worms, pipes).
- Implementation: a box with the front face removed and inner surfaces painted; dolly in from perspective to orthographic-like frontal view; thickness 1-2 m so that a small parallax is still visible.

## F-A05-010 — Macro hero shots: real 3D objects, very shallow DOF, 20-80x scale
- Label: OBSERVED. Confidence: medium.
- 05 gold pan f000869..f001139 (spiral of sand, speckles, rim in focus), 09 paint pot f000209..f000239, 22 powder bag f000869..f000899, 16 scratch card f000779, 29 coin board f000989..f001049. The camera sits ~0.2-0.5 m from the object, blurred scenery behind, the character partly visible as a hand/stylus.
- Implementation: model small, high-detail objects with normal maps; camera near-plane 0.01; bokeh DOF pass.

## F-A05-011 — Transition between locations often uses a foreground wipe / dissolve over a continuing camera move
- Label: OBSERVED (partially from calibration §2.2). Confidence: low-medium.
- Overview tiles show ghost-overlaid frames between scenes: 02 f000869 (cell -> next), 06 f000179, 06 f000809 ("rain" crossfade), 08 f000209..f000269, 13 f000479, 17 f000659, 18 f000179, 20 f000659..f000689 (peephole fisheye), 12 f000389 (looking-glass circle). Dissolves are ~6-14 frames. A "peephole / lens-circle" vignette is a recurring location-bridge device (12, 18 f000389..f000419, 20 f000659..f000689).
- Owner for transitions is A15; listed here only as set-to-set bridges.

## F-A05-012 — Exceptions / flat-feeling shots
- Label: OBSERVED. Confidence: medium.
- Flat or near-flat: 12 f000569..f000599 (circular scope image of the race — flat illustrated plate inside a circle mask), 16 f000989..f001199 (number grids are a flat UI plane with lit cells), 30 f000749..f000809 (diagram), 16 f000179 (lottery number sheet), 18 f000389..f000419 (circle vignette). 21 f000419..f000479 (army) looks like a 3D set with a very high-density instanced crowd, not a plate (balustrade slides across, carpet vanishing point moves).
- Cannot be told from a plate: 29 f000749 ("elevator tower" city plates) and 22 f000779..f000869 (inside barrel/cannon), where camera motion is small — record both readings (3D or layered plate); defer to a controlled experiment with A06/A07 (e.g. render the same shot both ways).
- Contradiction recorded: F-A05-001 (all environments are real 3D) vs the existence of flat diagram inserts (F-A05-012); resolved as "world = 3D, UI/diagram = flat planes inside the 3D camera space".

## Not done / limits of this report
- No vanishing-point (LSD/Hough) or horizon computation was run; `horizon_y`, `camera_height_est`, `props_per_establishing` as formal measurements are not produced (manual counts above only). See FAILED.md.
- `parallax_class` from A07 was not available; parallax judged by A05 viewing only.
- 6 videos (15, 23, 24, 26, 27, 28) were seen at one frame (montage) + calibration notes, not at sheet level; 02-04/07 etc. were studied in detail.
