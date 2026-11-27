# A06 TECHNIQUES — layer recipes (derived from FINDINGS F-A06-001..008; parameters are proposals to test, not yet validated in our renders)

## T-01 Character card (Three.js / @remotion/three)
- Mesh: PlaneGeometry(h*aspect, h), h = 1.5 m (A05 F-005); material MeshBasicMaterial/toon with `alphaTest 0.5`, `premultipliedAlpha`, `depthWrite true`, `side DoubleSide`. Origin at feet.
- Billboard: yaw-only toward camera (`mesh.rotation.y = atan2(cam.x-m.x, cam.z-m.z)`); roll only for gags. Never tilt pitch (cards stay upright even in crane-ups, F-001).
- Keep depth-tested: props, rails, desks, car frames occlude it (F-001). Held props: separate planes 2–5 cm toward camera (F-008).
- Light: tint card with the local key light colour (multiply 0.7–1.0, add warm/blue rim). No shadow maps; optional 30 % blob only if grounding fails (F-002).
- Matte: outline baked in art, alpha eroded 1 px, feather ≤ 1 px, no extra edge light (F-007). Test at 360p: no fringe on bright and dark backgrounds.

## T-02 Layer stack by shot type (true 3D, not plates)
| Shot type | Depth bands (z from camera at start) | Notes |
|---|---|---|
| Wide exterior (04, 06, 21) | fg props/grass 1–3 m, mid cards 6–15 m, set 20–80 m, backdrop mountains/sky 300 m+ (sky dome/ billboard ring) | near/far speed ratio target 3–8 (F-004); horizon never touches a flat plate |
| Interior mid (01, 02, 19, 25) | nearest prop/desk edge 1–2 m, card 2.5–4 m, walls 5–8 m | real room box; instanced repetition for corridors |
| Macro/hero (05, 16, 27) | object 0.2–0.5 m, rest blurred | A07 sets DOF |
| Cutaway slab (02, 17) | box 1–2 m deep, frontal camera | parallax stays small |
Plate fallback (budget only, never seen in the reference): 3 plates (fg 2 m, mid 8 m, far 40 m) + sky; overscan = max travel/width, here ≥ 25 % at near-plate for a 15° move; only for locked-off pans < 8°.

## T-03 Flat inserts
- Parent a plane (canvas texture) to a world object; keep ≥ 3 px outline/mat. Counters/UI animate in the texture. Stack of cards: separate planes, Z-offset 2–4 cm, 1–3° different tilt (RC30-16).
- Circular vignette/scope: screen-space mask over the render (HYPOTHESIS until tested).
- Captions stay a screen-space layer, outside the 3D scene.

## T-04 Occlusion / sorting checks for each shot
1. A prop passes in front of a card at least once per establishing move (pole, rail, balustrade).
2. Card never intersects geometry (push 5 cm off walls).
3. Verify at 360p/24 fps strip every 5 frames: no gap/halo along card edge.

## T-05 Measurement protocol reuse
`data_flowlayers.py` + `data_flow_layers.json`: use against OUR renders to confirm near/far speed ratio in the 2–8 band and k distribution (59/26 % for k=2/3) before the A28 review.
