# A09 TECHNIQUES — lighting presets (starting values; calibrate by rendering a still and running pair.py)

## 1. Rig
One `DirectionalLight` key; one `HemisphereLight` (sky colour = shadow colour); local `PointLight`/`SpotLight` practicals;
emissive bloom (UnrealBloom threshold ≈ 0.85). Target ambient/key irradiance ≈ 0.14.

## 2. Hard-key shadows
`renderer.shadowMap.type = PCFSoftShadowMap`; `key.shadow.mapSize = 2048`, radius 2–4, bias −0.0005, normalBias 0.02.
Cards: **`castShadow = false` by default** (3B F-A09-101: hard card shadows in 4/30 videos, per-scene switch); when a scene calls for it, `castShadow = true` with an alpha-tested `customDepthMaterial`. [Phase 4 correction 2026-11-28, D033: see knowledge/PRODUCTION_DEFAULTS.md] Key azimuth ≈ 40° off camera axis; elevation 55°
(day), 15–25° from behind (sunset).

## 3. Per-mood presets (HYPOTHESIS values from F-A09-006; hex/Kelvin approximate)
| Preset | Key | Hemisphere (shadow colour) | Extra | Target frame L*/a*/b* | Card shadow |
|---|---|---|---|---|---|
| DAY | #fff1d6 (~5800 K), 3.0, elev 55 | sky #8fb8ff, ground #6b6a52, 0.45 | — | 61/3/−11 | yes |
| SUNNY_WARM | #ffd9a0 (~4500 K), 3.0 | sky #9fb4e0, 0.5 | — | 65/6/17 | yes |
| SUNSET | #ffa64d (~3000 K), 3.2, elev 15–25, behind-right | sky #4c425e, ground #b0602a, 0.5 | sun disc + shafts (A12) | ~46/19/21 | yes, long, toward camera |
| NIGHT_BLUE | moon #8fa8ff (~9000 K), 0.6, elev 40 | #1c2a55, 0.35 | fire PointLight #ff8a3a (~2000 K), ≈ 40, decay 2, reach ≈ 3 card heights | 37/7/−13 | no |
| WARM_INTERIOR | #ffc27a (~3000 K) spot | #3a2a22 | candle/lantern PointLights | 44/10/16 | optional |
| WINDOW_SUN_INTERIOR | #fff4e0 through barred gobo | #7fb0d8 | haze shafts | ~62/−7/−16 | yes |
| SPOT_CABARET | SpotLight #fff0d0, angle 0.5, penumbra 0.6, high | #0b0d0c very low | pool with rings | 23/6/−9 | no |
| RED_WASH | #ff6a5a | #b03a30 + red fog | — | 46/19/21 | no |
| VIOLET_NEON | magenta #c040ff + cyan #30a0ff | #201a50 | wet-floor reflection | 37/20/−31 | no |
| HOLOGRAM_XRAY | none | flat | emissive cyan wireframe (A12) | n/m | no |
| BRIGHT_OFFICE | soft key | 1.0 hemisphere | yellow wedge decal #f2d43a α 0.5 | 69/3/3 | no/soft |
| ILLUSTRATED | none | painted gradient | decal light pools | n/m | no |

## 4. Card lighting (spec for A10's shader)
`shade = lightTerm` (key + locals) → `c = albedo * mix(0.36, 1.0, shade)`; shade tint toward the hemisphere sky; minimum
card exposure so faces stay L* ≥ 85 in dark scenes; warm/cool tint from the nearest practical (peach near lantern, pink
toward fire); hard terminator across the face allowed; cards receive projected shadow-map and gobo patterns.

## 5. Hubs and beats
One hub set exposes three lighting states (day, dusk, night); switch by cut or 7-frame crossfade (30 fps; 6 f at 24) on beats (A16/A18).

## 6. AO and blobs
SSAO/GTAO or baked AO on props; optional blob under a card only where the key is weak (opacity 0.15–0.25).

## 7. Hand-offs
A11: do not grade away the violet/blue shadow hue in sunset/day presets. A07: fog colour = hemisphere colour. A12:
shafts, bloom, glow.
