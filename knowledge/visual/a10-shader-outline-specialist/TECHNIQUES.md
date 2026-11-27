# A10 TECHNIQUES — shader designs (proposals; nothing built or approved)

## T-a10-001 Card material (A09 §4) with baked ink
- Geometry: one billboarded plane per character.
- Texture: Flow art holds the ink line ≈ 3.5 % of head width (6–15 px at 1080; 500 px head → 17 px). Hard premultiplied
  alpha edge, eroded 1 px, no feather.
- Shader: `MeshBasicMaterial` + `onBeforeCompile` (or `ShaderMaterial`), `alphaTest` 0.5, mipmaps off at intended
  scale. Uniforms: `uShade` (key + local lights, 0..1), `uMinExp` 0.36, `uSkyTint` (hemisphere colour), `uPractical`
  (warm/pink tint, 0..0.25), `uFaceFloor` (L* ≥ 85 ≈ min albedo multiplier 0.62 in dark scenes).
- Fragment: `vec3 c = albedo.rgb * mix(uMinExp,1.0,shade); c = mix(c, c*uSkyTint, 0.15*(1.0-shade)); c += uPractical; c = max(c, albedo.rgb*uFaceFloor);`
- Optional hard terminator: `shade = smoothstep(t-0.02, t+0.02, nDotL)` on a fake normal from the card UV.
- Shadow-map and gobo patterns via `receiveShadow`. (A09 F-A09-001: cards *cast* shadows in hard-key presets — use an
  alpha-tested depth material there; none in night/fire/illustrated presets.)
- No screen-space outline on cards (F-a10-002).
- H.264 line cores read lighter than true ink → author ink at L* 0–10.

## T-a10-002 World outline pass — treatment B only
- Prepass: depth + view-space normals to a half/full-res target (`MeshNormalMaterial` override or WebGL2 MRT). Cards on
  layer 1, excluded (flat depth, normal (0,0,1), ID mask).
- Sobel on linearised depth and normals: `edge = max(smoothstep(0.02,0.06,depthSobel/linDepth), smoothstep(0.35,0.7,normalSobel))`;
  Sobel offset (px) = `uWidthPx * renderWidth/1080`, `uWidthPx` = 2.5 (measured 2.0–3.0) → resolution independent;
  test at 360p (`uWidthPx` ≈ 0.83) and 1080p.
- Colour: `ink = mix(sceneColor*0.4, vec3(0.10,0.07,0.06), 0.25)` (measured: darkened surface colour, RGB 65–120,
  55–81, 41–69).
- No width taper with distance (optionally 80 % beyond 40 m). Composite after the scene render, before DOF. Interior
  creases mostly from the normal-edge term plus painted textures. Treatment A skips the pass.

## T-a10-003 Shading choice and post stack
- Treatment A: `MeshStandardMaterial`, PBR, roughness 0.6–0.9, no outlines. Treatment B: same lit model with painted
  albedo + T-a10-002. No toon ramps in either.
- @react-three/postprocessing order: RenderPass → (outline, B only) → N8AO/SSAO (A09 §6) → DepthOfField (A07) → Bloom →
  Vignette → ToneMapping → SMAA / output pass.
- Bloom: `luminanceThreshold` 0.9, `luminanceSmoothing` 0.2, `intensity` 0.35–0.6, `mipmapBlur` true (HYPOTHESIS).
- Vignette: `offset` 0.35, `darkness` 0.25 (corner/centre luma ≥ 0.8; low confidence).
- No grain, no chromatic aberration (measured absent). Captions composited later in Remotion.
