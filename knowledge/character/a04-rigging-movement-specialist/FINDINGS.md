# A04 FINDINGS: character rig and body motion (Phase 3, RC30)
Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 · A04.
(Written to disk verbatim by the director from A04's hand-off; the agent's Write tool refused this file.)
Visual ledger: `knowledge/dataset/coverage/visual/a04-rigging-movement-specialist.jsonl`, 27 records (5 every-frame contact sheets, 120x213 tiles: 15 x2, 25, 28, 30; 16 overview sheets, 180x320 tiles; 6 private every-frame/every-2nd-frame strips, 150-200 px wide, made from native decode).
Videos with visual evidence: 20 of 30 (01, 02, 04, 06, 07, 09, 10, 11, 12, 13, 14, 15, 19, 20, 22, 24, 25, 26, 28, 30). Deep views (>= 24 consecutive frames): 15, 25, 28, 30 (sheets), 06, 14, 07, 04, 22, 20 (strips) = 10 videos.
Computational: private scripts in `data/` (iou.py, roi.py, upd.py, walk.py, strip.py; run with `.venv-analysis/bin/python -I`). No audio work.
Coverage limits: only 5 videos had A27 sheets at run time (15, 25, 27, 28, 30; 23 had none; 27 not opened). `motion.csv` residual columns are dominated by camera-model error (res_mean_mag 8-50 in nearly every window), and the camera is never static for 15+ frames (only RC30-15 has three runs of 14-22 frames), so I used them only to locate windows. Frame-rate counting is therefore limited (F-a04-002). All confidence is LOW-MEDIUM unless stated.

## F-a04-001 Rig type: per-pose redrawn bodies and limbs + rigid card transforms + swapped face parts (hybrid)
- Label: OBSERVED. Confidence: medium for "limbs/bodies are redrawn per pose, not a fixed bone chain"; low for the exact split of parts inside a pose (tiles too small to prove rigidity).
- Evidence: RC30-14-f000656..f000703 (walk, every frame): leg strokes change shape and angle every frame, incl. bent/curved knees. RC30-07-f000213..f000252: arms, legs and a held red object change shape per frame while the head stays a constant circle. RC30-25-f000192..f000207: arms are curved arcs; eyes/mouth change with pose. RC30-26-f000479 back view; 12-f000029 / 02-f000809 seated with crossed/splayed legs; 14-f000539..f000599 and 19-f000629 lying: whole body drawn as different pose drawings, not rotations of the standing pose.
- Rigid transform evidence (card and props): RC30-25-f000224..f000239 pill tumbles with smooth rotation and scale change; RC30-06-f000778..f000810 hat leaves the head and spins as a rigid ellipse through an arc (about 30 frames); RC30-04-f000125..f000140 tyre flops (3D prop with perspective); RC30-15-f000000..f000031 the whole card scales with the camera push while only the face drawing changes.
- Squash/stretch: not seen on the head (stays a circle, matches F-a03-007). Smear/arc VFX appear at fast hits (06-f000778 red arc; 14-f000419..f000449 flame streaks) instead of limb stretch. Limb lengths vary slightly pose to pose (07 strip): consistent with redrawn limbs, not constant-length bones.
- Method: viewed every frame (see ledger). Limits: no tile showed a clear head/body layer split; hands/feet joints are small.
- Implementation: TECHNIQUES.md "Hybrid rig": head circle + torso pill + limb strokes as variable-curve Beziers + pose-library swap for large changes + face swap sets. A plain 2-bone IK chain is not enough.

## F-a04-002 Pose update rate: action on ones (about 30 Hz), holds exist, no on-twos pattern found
- Label: MEASURED (3 segments) + OBSERVED. Confidence: low-medium (n = 3 computational segments in 3 videos).
- Method (`data/iou.py`): crop character, threshold ink (gray < 50), phase-correlate consecutive frames to remove camera translation, report fraction of ink (3x3 dilated) covered in the next frame. Identical pose gives about 0.95-1.0; changed pose 0.5-0.8; on-twos would alternate high/low.
- Evidence: RC30-14-f000657..f000703 walker: median 0.66, max 0.83, 0 of 47 pairs > 0.9, no alternation => new leg drawing every frame. RC30-07-f000214..f000251 gesturing pair: median 0.88, 37 % of pairs > 0.9, no alternate-frame zeros (changes every 1-3 frames). RC30-20-f001183..f001189: 0.97-0.98 for 7 frames (held pose, camera drift only), then f001192..f001204 falls 0.69..0.50 continuously. RC30-22-f000213..f000240 debris-contaminated, discarded.
- Face swaps (`data/roi.py`, tight face ROI): RC30-15-f001393..f001411: noise floor 1.1-1.7; spikes 5.7, 6.2 at f001397-98 and 6.5, 7.0 at f001400-01 (two consecutive new drawings, then floor f001402..f001408 = 7-frame hold). Sheet confirms eye shape changes at f001393/4, f001397, f001398, f001399.
- Whole-frame check: RC30-01 frame differences (180x320, caption band masked) never < 0.2/255; no exact duplicate frame in 1,835 frames (the shot is re-rendered every frame because the camera never stops).
- Implication: 30 fps (24 dev) with animated drawings in bursts of 1-3 new drawings then holds of 6-12+ frames; no 2s/3s look seen.
- Limits: 3 numeric segments only; on-twos talk gestures not excluded for unmeasured characters. Re-test on 10+ segments is open.
- Implementation: motion library stores pose keys at 30 fps with per-key hold; no frame-skip filter.

## F-a04-003 Walk: step about 11 frames at 30 fps (one walker), legs redrawn every frame
- Label: MEASURED, n = 1 walker (RC30-14 f000656..f000703); OBSERVED only for 06 army march (f000119) and 02 prisoner (f000659..f000719, overview). Confidence: low. EVIDENCE.md wants n >= 3; not reached.
- Evidence: ink-overlap maxima at f000662, f000673, f000684-685, f000694-695 => intervals 11, 11.5, 10 (median 11, n = 3 intervals). Leg-ink vertical centroid (`data/walk.py`, ROI y 1060-1420): minima f000664, f000675, f000686; maxima f000668, f000678-679, f000689-691: period 10.7 frames. If one oscillation = one step: step 11 f (2.7 steps/s), cycle about 22 f. H-UP 9-12 f is consistent (supported, not proven). Step vs stride was not resolved visually.
- Form: slight forward body tilt, small head up-down motion (bob NOT measured), hat attached, small arm swing, thin straight/curved leg strokes, short foot strokes; camera follows so the walker is held near centre.
- Foot slip: NOT measured (see FAILED).
- Implementation: TECHNIQUES.md walk preset: step 11 f at 30 (9 f at 24), cycle 22 f.

## F-a04-004 Motion inventory
- Label: OBSERVED. Confidence: medium for existence of each type; low for timings.
- Idle: held body, small face changes; camera push-ins supply motion (15-f000000..f000031 card grows about 3x in 31 f while only the blink changes; 30-f000768..f000815 seated figure grows about 3x, body held, bubbles/caustics add life). Regular breathing bob not seen in about 10 idle stretches.
- Talking: head/face drawings change with narration; body mostly held (04, 06, 12, 14, 19, 20 overviews). Mouth shapes are face parts (A02).
- Gestures: arm re-poses between drawings (point 06-f000329; hold-up object 09-f000419; hands on head 22-f000209); 07-f000209..f000252 two characters change arm/leg shapes on ones.
- Walk/run: 14 walk; 04-f000149 stand then dash; 06-f000119 group march. Run not measured.
- Falls/tumbles: 25-f000224..f000239 pill spins and drops (card rotation + scale); 14-f000419..f000599 cowboy falls, then a separate lying drawing with dust puff; 06-f000764..f000810 slap: victim and bystander redrawn, hat flies off ballistic.
- Blast launch: 22-f000205..f000252 pirate holds one frozen scream pose for about 28 frames while debris/camera move.
- Entrances/exits: doorway pop-in 19-f001139..f001169; ladder climb 13-f000419..f000449 (small card, legs redrawn). Exits are mostly cuts/crossfades (A15), not walk-outs.
- Interaction: 2-3 characters per shot (07, 09, 10, 12, 13, 22, 24, 26), staggered in depth, reacting by face swaps; physical contact is hidden by cuts or VFX arcs (06-f000778).
- State tints: 10-f000539 anger turns the body purple with steam puffs; 09-f000809..f000839 red crack lines radiate (VFX layer).
- Exceptions: 28 brain character with zoom through the eye (f000192..f000224); 30 dream scene, translucent stylised body, closed-eye swaps; 25 pills, liquid occludes body (f000192..f000223); 12 galloping horses as animated cards (f000839..f000930); 24 characters static during long camera moves; 21/29 not opened.

## F-a04-005 Timing and easing (low n)
- Label: MEASURED for blink/expression/hold, otherwise OBSERVED/INFERRED. Confidence: low.
- Blink: RC30-15-f000000..f000005 eyes narrowed f000000-02, open by f000003-05 (about 3-frame close/open, on ones). No blink rate counted.
- Expression change: 2-4 consecutive new drawings (15-f001397..f001401), then hold 7+ frames.
- Holds: 7 f (15 face), 7+ f (20 body f001183..f001189), 28 f (22 scream).
- Overshoot/settle: no spring overshoot on cards seen (15-f000000..f000031 constant-rate scale rise). Anticipation: 06-f000764..f000776 victim leans before hit (about 12 f); 14-f000419 arms rise before the shot (counts approximate).

## F-a04-006 Secondary motion: detached props and VFX follow through; hair/hat otherwise rigid
- Label: OBSERVED. Confidence: low-medium.
- Evidence: hat detaches and spins (06-f000778..f000810); plume on the cap does not flutter (11-f000749 overview); hair spikes rigid (15-f000000..f000031, 15-f001392..f001439); tyre rolls with perspective (04-f000125..f000140); liquid rises on the pill (25-f000208..f000223); debris/splinters carry energy (22-f000205..f000252, 09-f000809..f000839).
- INFERRED: follow-through is delivered by props and particle/VFX layers (A09), not jiggle bones. Do not build hair physics.

## F-a04-007 Cards in 3D: motion by camera plus card translation/scale/roll; depth sorting by geometry
- Label: OBSERVED (agrees with F-A06-001). Confidence: medium.
- Evidence: 25-f000192..f000223 pill sinks below the liquid surface (occluded by water) then tumbles; 28-f000192..f000224 camera dives into the eye (card about 10x then scene cut in the iris); 15-f000000..f000031 push into the card; 06-f000764..f000810 character stays frontal while the wall changes perspective.
- Implementation: card transform = x, y, z, uniform scale, roll; yaw lock to camera (A06).

## Contradictions and uncertainty
- H-UP 9-12 f steps / 3-7 % bob: step supported with n = 1; bob not measured. Not averaged.
- A03/A01 describe limbs as straight strokes without knees; here limbs are drawn curves per pose (arms 25-f000192, walking legs 14). Single stroke width (F-a03-008) is not contradicted; "straight, no-knee strokes" as a rig assumption is.

## Open questions
1. n >= 3 walkers plus bob/lean/slip: request from A27 tracked head/foot tables for 14-f000656..f000703, the 06 march and 02-f000659..f000719.
2. Frame-rate test on 10+ segments.
3. Whether hands, feet and head sit on separate layers inside a pose (needs 1080 px native crops).
