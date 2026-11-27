# A12 TECHNIQUES — starting VFX recipes (durations from n = 1 events; test before locking)

## Conversion
frames@24 = frames@30 × 0.8 (preserve seconds). Shine 8 f → 6–7 f; bloom rise 20 → 16, decay 13 → 10; wireframe fade
5 → 4; vein growth 18 → 14.

## Rules
- Hit effects cut in (no fade-in): first frame at full density (hub/star), then ease-out expansion.
- Ambience loops 2–4 s, invisible at start/end.
- Sync: start 0–3 frames after the caption word change, or on a cut.
- Remotion: `interpolate(frame, [t0, t1], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})`.
- Three.js: shared effect clock driven by the Remotion frame (never wall time) → deterministic renders.

## Starter library (timing at 30 fps)
| ID | Effect | Type | Timing | Recipe |
|---|---|---|---|---|
| E01 | impact_debris | 3D InstancedMesh, scene-lit | spawn 2, spread 12, dwell 15, tail 30+ | 150–300 shards, radial velocity ease-out, gravity, spin; star hub sprite 2 f; wall-hole alpha cut-out |
| E02 | crack_veins | 2D line mesh/SVG + additive halo | grow 6–18 in 6 steps, hold 30 | polyline growth 0→1, flat red #D91E2E, blurred additive copy, faint ring r 0→1.3 character heights over 8 f, 10–20 specks |
| E03 | anger_eyes | 2D flat glow | on in 1 step, hold | red additive eye shape, 2 flicker drawings |
| E04 | smoke_puff | 3D or sprite | grow 8–10, fade 20 | 3–5 overlapping grey-white puffs, upward drift, scale ×1.5, alpha 0.9→0 |
| E05 | dust_ground | sprite | 12–20 | low puff at feet, brown-grey, scale up, fade |
| E06 | sparks_embers | 3D points, additive | loop | 30–60 warm-orange points, small gravity, flicker |
| E07 | sparkle_glint | 2D 4-point star | 6–10 | scale 0→1→0 with 45° rotation; 2–4 per object, staggered 3–5 f |
| E08 | shine_sweep | mask + additive band | 8 (6–7 @24) | skew −20°, band 12 % width, travel −10 %→110 % linear, peak alpha 0.8; saturation lift on target afterwards |
| E09 | glow_wash | additive overlay | rise 12–20, hold, decay 13 | radial/full-frame glow, S-curve; coordinate with A10 bloom |
| E10 | colour_mood_wash | grade overlay | ramp 12–14, hold 25+ | multiply/overlay alpha 0→0.6, vignette pulse ≈ 1.5 Hz |
| E11 | light_rays | additive quads | loop or 20–30 ramp | 6–12 radial streak quads, slow rotation, alpha 0.2–0.5; sunburst variant for reveals |
| E12 | speed_lines | additive streaks | 6–12 on a fast move | 20–40 thin white streaks from the vanishing point, length 20–40 % frame, alpha 0.7→0 |
| E13 | water_splash_rain | 3D particles | splash 12–20; rain loop | droplets + foam ring; rain 200+ slanted streaks |
| E14 | wireframe_hologram | LineSegments, additive cyan | fade-in 5 (4 @24), hold 30+ | EdgesGeometry + face grid; alpha ease-out; first-frame white veil 35 %→0 over 4 f |
| E15 | emotion_marks | 2D flat | pop 2–3, hold 10–20 | sweat drop (ease-in fall 6 f), drifting "Z" with fade, anger cross; on twos |
| E16 | ui_callout | SVG/text mesh + additive outline | pop 2 f (scale 0.8→1.1→1); countdown step 30 f | colour highlights fade in 4–6 f |
| E17 | confetti_money | 3D instanced quads | 60–90 f burst | flutter rotation, gravity, random hue |
| E18 | bubbles_caustics | ring sprites + tiled caustic | loop | rising rings; caustic scroll 0.1 uv/s |

## Measurement recipe
`color.csv` luma_mean / luma_p99 → merge |Δ| > 8 events with 15-frame gap → confirm visually. Rises/dips that are not
flashes: zooms, wipes, iris.

## Do not
Use fades for hit effects; treat `flash_candidate` as a flash; double-count crossfade-based VFX (A15 owns transitions).
