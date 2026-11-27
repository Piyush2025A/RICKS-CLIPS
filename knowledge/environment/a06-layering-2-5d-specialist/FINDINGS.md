# A06 FINDINGS — depth layering of characters, props, foreground/background, flat inserts (Phase 3)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · 2026-11-28 ·
visual-ledger records: 14 (`knowledge/dataset/coverage/visual/a06-layering-2-5d-specialist.jsonl`; 13 strips/crops/frames + 1 montage).
Videos covered: computational 30/30 (flow windows); visual 12 with strips/crops (01,02,04,06,10,13,16,19,21,22,25,29) + 18 more in one 18-tile montage (03,05,07,08,09,11,12,14,15,17,18,20,23,24,26,27,28,30) = 30/30 at one-frame level.
Builds on A05 (F-A05-001/012). Original-work rule: techniques only.
Sheets note: per-frame contact sheets existed for only 4 videos when I ran; I decoded native video with OpenCV myself (private scripts, `data_flowlayers.py` is a copy of the flow script).

## F-A06-001 — Characters are camera-facing flat cards (billboards) with correct depth sorting against 3D props
- Label: OBSERVED. Confidence: high for billboard (consistent in all 30 montage tiles and 9 strips); medium for "never foreshorten" (no extreme orbit found).
- Evidence: RC30-25-f000509..f000559 (camera yaws until wall fills frame f539/f549: the small pill character stays frontal and un-foreshortened while door/sign/wall planes are strongly oblique); RC30-04-f000149..f000199 and RC30-06-f000089..f000139 (crane/dolly: cards keep a frontal silhouette, only scale/position change); RC30-10-f000059..f000109 (dolly along rails: card constant 3/4-drawn pose, tilts only in roll, f000099 drawn head tilt); RC30-28-f000120 and 13-f000159 cards seen from above stay upright-flat (roll rotation only seen in 28).
- Occlusion: card sorted against geometry — RC30-06-f000129 general stands behind the palanquin rail (legs seen between rails) and a soldier's arm holds the pole in front; RC30-10-f000079 a telegraph pole passes behind the head; RC30-01-f000149..f000199 desk/console hides lower bodies; RC30-07-f001380 card sits inside car geometry, door frame in front; RC30-21-f000449..f000499 balustrade in front of the character.
- Method: viewed 6-frame strips at 10-frame steps and native crops (ledger). Limits: strips 238x422; no camera orbit >30 deg around a card was located, so true billboard-vs-fixed-plane at large angles is not distinguished from "fixed plane facing the shot's start camera". INFERRED rule: yaw-lock card to the camera.
- Implementation: THREE.Mesh plane (alphaTest cutout) with `lookAt(camera)` yaw-only (Y-up) or copy `camera.quaternion`; keep it a real depth-tested mesh so props occlude it; roll allowed for gags (28).

## F-A06-002 — Cards are lit by the scene, but I found no cast/contact shadows from cards
- Label: OBSERVED. Confidence: medium (4 frames inspected for shadows; absence is hard to prove).
- Evidence: RC30-19-f001019 a warm light patch tints face and body orange where the shaft crosses the card; RC30-02-f000749 specular/gradient highlight on the white body, orange lower half, blue cast; RC30-30-f000075 spotlight cone pool on the character; RC30-15-f002145, 20-f001650 blue-tinted cards in blue rooms. No dark cast shadow on the desk/bunk/gravel under the card in RC30-19-f001019, 02-f000749, 10-f000079 (feet end on gravel with no blob). Thin sticks legs overlap floor with ink only.
- Implementation: use a lit/toon material (or multiply by a per-card light probe / vertex-tint from scene key light) so the card picks up local colour; do NOT rely on shadow maps; optional fake blob only if a shot needs grounding (our choice, not seen in reference). Hand-off: lighting to A09.
- Contradiction note: none found; if cast shadows exist they are very faint.

## F-A06-003 — Layer structure is a continuous depth gradient (true 3D), not discrete plates; typically 3 visual bands
- Label: MEASURED (flow) + OBSERVED. Confidence: medium (flow k is an imperfect proxy, see limits).
- Evidence: Farneback flow at 270x480, frame pairs (i, i+2), 1,121 windows every 45 frames from frame 30, all 30 videos; texture pixels only, caption band y 58–82 % excluded; windows with flow p90 > 1.5 px counted as moving: 934 (83 %). k-means on (u,v), k=1..4 chosen by inertia-drop rule, clusters ≥ 8 % mass kept: k=1 110 (12 %), k=2 553 (59 %), k=3 245 (26 %), k=4 26 (3 %). Per-video mean k median 2.16 (range 1.87 RC30-26 … 2.63 RC30-08; IQR 2.06–2.29). Fraction of moving windows with k ≥ 2: ≥ 0.70 in all 30 videos. Residual after global affine fit = 43 % (median, IQR 25–74 %) of median flow magnitude: a single 2D plane would give ≈ 0, so depth variation is always present. Data: `data_flow_layers.json`; script `data_flowlayers.py` (v0.1); input checksum = manifest above.
- Visual bands: foreground (large near props / blurred bands / frame-edge cards, e.g. 06-f000089 grass, 20-f001650 giant head, 18 desk edge), mid (character + hero prop), far (sky/mountains/horizon, e.g. 04-f000169, 21-f000449). 3 bands + 1 sky/backdrop is the working count; sets inside rooms add many mid objects at distinct depths (continuous).
- Limits: k-means splits a continuous gradient and object animation also forms clusters, so k over-counts plates and cannot separate depth from character motion (EVIDENCE: cross-check with occlusion). Moving-window flag threshold mine; windows are 2 frames apart, so slow drifts count as noise.
- Implementation: do not build a 3-plate cut-out rig for dolly shots; use real depth. 2.5D plates are only a cost-saving fallback for shots below.

## F-A06-004 — Near/far speed ratio
- Label: MEASURED. Confidence: medium. 
- Evidence: ratio of fastest to slowest kept flow-cluster speed in moving windows with k ≥ 2 (n=824 windows, 30 videos): median 3.8, IQR 2.1–8.0 (slow cluster floor 0.05 px). Per-shot examples from LK tracking were rejected (FAILED.md).
- Implementation: set z so near/far screen-speed ratio ≈ 2–8 for ordinary moves: with lateral dolly, speed ∝ 1/z, e.g. foreground z=1.5 m, mid 5 m, far 15–40 m. Larger (>10) occurs on forward dollies passing near props.

## F-A06-005 — RC30-29 f000749 and RC30-22 f000779..f000869 are real 3D geometry, not plates (resolves A05 open question)
- Label: OBSERVED. Confidence: medium-high (strips at 8/15-frame steps).
- RC30-29-f000740..f000780: pull-back from a glass elevator cage with two cards inside; the tower facades change convergence, a wall panel rotates in from the right, side faces appear, the "THE ONE" sign rotates with the building — perspective, not scale of one plate. RC30-22-f000779..f000854: camera flies in through the cannon barrel; tunnel ring, powder bag and the glowing plug change perspective with parallax between rim and bag. Both need 3D geometry (tube, box tower), cards for characters only.
- Implementation: tower = box + facade texture; barrel = cylinder with inside-facing material and camera along its axis.

## F-A06-006 — Flat inserts are world-attached planes, not screen overlays (with two screen-space exceptions)
- Label: OBSERVED. Confidence: medium-high.
- World-attached: RC30-01-f000149..f000199 wall map/"FLUSH WINDOW" countdown screen slides and foreshortens with the room (the "3" counter is on the screen mesh and gets occluded by the character card in front); RC30-25-f000529..f000549 "FOR RENT" sign and smoke-alarm face disc stay glued to the wall and foreshorten; RC30-27-f000570 slot paper roll with text is a tilted plane; RC30-16-f000989..f001089 three ticket cards form a stack of slightly different planes with per-cell glow (UI inside the world, shifts relative to each other); RC30-12-f000525 mirror frame shows a scene texture (portal-like plane); RC30-18-f001425 pinboard of cards on a desk plane.
- Screen-space: burned-in captions (always, per brief); circular vignettes/scope masks (A05 F-012, RC30-12 f000569..f000599) look flat-on-screen. HYPOTHESIS: those are 2D masks over the render — test by checking whether the circle contents shift relative to the circle edge.
- Implementation: any readable UI = textured plane mesh parented to a world object; animate by canvas texture; keep out of the caption band.

## F-A06-007 — Matte/edge quality of cards: crisp thick ink outline, no halo
- Label: OBSERVED. Confidence: medium (native crops of 4 frames + 30 montage tiles at low res).
- Evidence: RC30-06-f000129, 10-f000079 (native crops 600x500/700x800), 19-f001019, 02-f000749 (540x960 view). Outline ≈ 6–10 native px dark line included in the card art (black/dark brown), fully opaque, smooth anti-aliasing; no light fringe or dark halo against green grass, orange cliff or blue wall. The outline hides the cut edge, so no feathered matte is needed. Limb sticks are 8–14 px lines; a rubbery highlight fill on bodies.
- Limits: 1080p after H.264 compression; no alpha access; halo test via pixel statistics not done.
- Implementation (Flow cards): generate on flat colour, key out (A24), keep outline, erode alpha 1 px, premultiplied alpha, no feather > 1 px; render with `alphaTest`/premultiplied and mipmaps off at card scale; the outline must be in the art.

## F-A06-008 — Cards are layered for gags: limbs/hands overlap props
- Label: OBSERVED. Confidence: low-medium.
- RC30-19-f001019 character's feet rest on desk top with hands on a phone, seated into 3D chair; RC30-02-f000749 hand grips the bunk pole in front of it (hand in front, body behind). Implies card = one plane for body with possibly separate small planes (hands/held props) offset by a few cm toward the camera, or a single card posed to fit. Not decidable from frames.
- Implementation: held props as separate planes 2–5 cm in front of the card.

## Open / not measured
- `overscan_needed`: not applicable (true 3D, no plates); not measured.
- Foreground blur layers: seen as DOF (RC30-20-f001650 near head soft, 18-f001425 desk); strengths belong to A07.
- No orbit >30 deg around a card (F-001 limit). Cast shadows absence is low-power.
