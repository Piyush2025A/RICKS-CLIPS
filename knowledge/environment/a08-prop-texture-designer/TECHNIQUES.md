# A08 TECHNIQUES — prop and material recipes (derived, NOT yet built or tested in our renders)
Status: every entry is `derived-not-yet-built`. Promote only after an EXP record with an OUR- frame (CLAUDE.md rule 3).
Parameters marked (ref) come from F-A08 measurements; the rest are engineering defaults to be tuned in the first EXP.

## T-A08-01 Prop design checklist (from F-001, F-002, F-010)
1. One story job per prop (fact, gag, or counter). If none, it is set dressing: 1-2 shapes, no text.
2. Silhouette readable at 15 % frame height: built from boxes/cylinders, 1-3 cm bevel, <= ~12 distinct parts.
3. Scale: hero x1.5-3 real size; character plane 1.5 m (A05 T-03).
4. Detail budget: all label/number/gauge detail on ONE face; elsewhere rivets as dots, vents as 3 lines, hazard stripes.
5. Colour: hero prop chroma C* 55-95 vs set surfaces C* 3-30 (ref F-006); max 3 hues + neutral.
6. Text: fictional names only; no real brands (rule 8).
7. Macro variant: same prop rebuilt with 2-3x detail for the hero close-up (near plane 0.01, FOV 25-35).
8. Ink: treatment B outline 3-4 px near / 2 px far at 1080 wide (ref F-005); A: none on scenery.
9. Provide emissive map for any screen/counter; separate mesh for rolling digits.

## T-A08-02 Three.js material presets (starting values; verify in EXP)
| Class | Material | color target (screen L*/C*) | roughness | metalness | texture |
|---|---|---|---|---|---|
| Rock/earth (A) | MeshStandardMaterial | L 50-68, C 25-50, hue ~65 deg (warm) | 0.9 | 0 | 1024 tiling speckle, local std 3-5 L* |
| Wood, painted (A/B) | MeshStandardMaterial or Toon | L 25-45, C 26-32 (dark) / planks 58, C 41 | 0.6 | 0 | 1024-2048 soft streaks, seams 2-4 px, micro-std < 0.5 |
| Paper | MeshStandardMaterial + CanvasTexture | L 90-95, C 5-20 (cream) | 0.9 | 0 | print at 2048 for hero faces |
| Plaster/laminate/tile | MeshToon or Standard | L 63-89, C < 5 (light tints it) | 0.8 | 0 | flat + sparse flecks 8-30 px |
| Painted metal, enamel (hero) | MeshStandardMaterial | red L 55, C 94; yellow/teal similar | 0.35 | 0.2 | flat fill, edge wear optional |
| Gold / brass | MeshStandardMaterial | L 69, C 67, hue 87 | 0.25 | 1.0 | gradient env map + sparkle sprites |
| Steel / chrome | MeshStandardMaterial | grey | 0.2-0.3 | 1.0 | gradient-band envMap (2 bright strips) |
| Glass (dome, jar) | MeshPhysicalMaterial transmission 0, opacity 0.25-0.4, clearcoat 1 | white tint | 0.05 | 0 | edge highlight only, no refraction |
| Liquid | MeshStandardMaterial flat saturated | per liquid | 0.2 | 0 | swirl texture + 2 spec dots |
| Emissive screen / LED | MeshBasicMaterial or emissiveIntensity 1.5-3 + UnrealBloom (threshold 0.8, radius ~12 px) | dark bezel, glow C* 80+ | -- | -- | 7-seg with unlit ghost segments at 15-20 % |
| Foil / holographic edge | MeshPhysicalMaterial iridescence 1 | rainbow | 0.2 | 0.5 | thin border only |
Treatment B swap: MeshToonMaterial, gradientMap 3 steps (0.45/0.75/1.0), + inverted-hull outline (A10).
Texel density: target 1 texel per 1 screen px at the closest planned camera distance for hero faces (text, labels): hero label texture 2048 px across <= 1080 px of screen (2x supersample for 360p downscale); set surfaces 0.5-1 texel/px; repeat tile >= 2 m physical to hide repetition. (HYPOTHESIS: reference density not measurable.)

## T-A08-03 Surface texture rules (F-003, F-004)
- Organic (rock, sand, gravel, dirt): tileable speckle/blob noise, local std 3-6 L* at 7x7, painterly not photographic.
- Man-made (wood, plastic, enamel, fabric, floors): flat fills; variation by large soft gradients and sparse painted marks. Do NOT add fine noise (reference std < 0.5).
- Pattern surfaces (brick, tiles): geometry rectangles + hairline dark joints 2-3 px, tint alternate blocks +-3 L*.
- Validation: 360p 24 fps motion test; reject any texture that shimmers (mipmaps on, anisotropy 8, noise period >= 4 px at 360p).

## T-A08-04 Sign and typography rules (F-007)
- Beat-carrying text: cap height >= 35 px at 1080x1920 (>= 12 px at 360p), contrast ratio high (dark on cream or white on navy), <= 3 words or one number.
- Headlines: bold condensed/slab serif or sans, ALL CAPS; body copy only as greeked grey lines (<= 7 px) for realism.
- Numbers: mono or 7-seg; dotted-matrix for tickets. Counters on physical bezels with emissive glow.
- Highlight matches by colour glow around the digit (halo ~12 px), not by changing font.
- Render text via canvas texture (MSDF if camera is far); fictional brand names only; keep one text language per prop (EN here).
- Counter animation: digits roll with a short blur/ghost of the next digit; carry to the next place. (timing from A12.)

## T-A08-05 Google Flow prompt guidance for ORIGINAL prop/texture art (Flow cannot be driven from this container; prompts for the user/A23)
Prop: "<object>, original design, chunky toy-like proportions, rounded bevelled edges, <treatment keywords>, single object centred on plain neutral background, even soft light, orthographic three-quarter view, vertical 9:16, no characters, no logos, no real brands, label text left blank".
Treatment B keywords: "thick dark ink outline, flat colour fills, simple 2-3 tone cel shading, saturated primary palette, hazard stripes". Treatment A: "stylised game-engine render, soft PBR materials, subtle bloom".
Texture: "seamless tileable <material> texture, hand-painted stylised, <flat | fine speckle> detail, no perspective, no lighting, no shadows, even exposure, 1:1". Man-made: add "perfectly flat colour, soft broad streaks only". Rock/earth: add "fine multicolour speckle".
Never ask for a named channel, film or brand style; add text in canvas afterwards so it stays editable and original. Hand the result to A24 for tiling and A10 for line matching.

## Phase 3B additions (2026-11-28) — numeric material presets from 14-video native patches (still derived-not-yet-built; verify in the first EXP with an OUR- frame)
Screen targets (after our light and grade), not albedo. To get albedo for a Standard material, divide by the expected light: start colour L* = screen L* x 1.0 under neutral key and tune.
| Class | three.js | color target (L*/C*/hue) | rough | metal | map | detail |
|---|---|---|---|---|---|---|
| Painted car/prop enamel | MeshStandardMaterial + clearcoat 0.6 | L 45-64, C 60-90, hue 31-38 | 0.35 | 0 | none | flat colour, 2-3 broad highlights; local std 0.2-0.5 |
| Pale enamel appliance | MeshStandard | L 81, C 21 | 0.4 | 0 | none | flat, std 0.16 |
| Dark painted metal | MeshStandard | L 29, C 14 | 0.45 | 0.6 | none | flat, std 0.15, rim spec only |
| Gold | MeshStandard | L 65, C 46, hue 78 | 0.25 | 1.0 | envMap gradient | std ~1.8 from speculars; add warm point light |
| Wood planks | MeshStandard | L 45 C 27 hue 48 | 0.7 | 0 | 1024 flat soft-streak, 1 knot per 1-2 m | std 0.6 L*; seams 5 px at 1080 (2 px at 360p) depth 16 L* |
| Sand/dirt | MeshStandard | L 27-71, C 28-43, hue 52-72 | 0.95 | 0 | flat soft blobs | std 0.2; no grain |
| Stone (pillar) | MeshStandard | L 23, C 8 | 0.8 | 0 | flat | std 0.8 |
| Grass | instanced blades (3-12 px at 1080) or MeshStandard + 1024 blade-noise map | L 39-69, C 46-64, hue 112-130 | 0.9 | 0 | blade strokes 3-12 px | local std 3-12; the one grained surface |
| Gravel/ballast | MeshStandard + 1024 pebble map | L 46-56, C 9-17 | 0.9 | 0 | pebbles 6-20 px | std 4-10 |
| Lattice/mesh pattern | geometry or 512 tile, period ~14 px | L 35 C 45 | 0.7 | 0 | 512 repeat | std 13 (pattern); keep period >= 4 px at 360p |
| Glass capsule/dome | MeshPhysicalMaterial transmission 0, opacity 0.3, clearcoat 1 | L 93, C 3 | 0.05 | 0 | none | soft gradient, near-clip highlight |
| Flesh/skin world | MeshStandard | L 32-39, C 40-54, hue 13-29 | 0.7 | 0 | flat | std 0.3-0.4 |
| Character fill | MeshBasic/Toon | L 93, C 6 | -- | -- | none | flat |
| Floors/walls flat | MeshStandard | dark rooms L 17-38 C 16-34; bright rooms L 72-83 C 12-24 | 0.85 | 0 | flat | std 0-0.5 |
| Sky | gradient shader (not a mesh) | L 47-81, C 16-66, hue ~283 | -- | -- | 2-stop gradient | std < 0.12 |
Texture resolution: grained classes 1024 px tile covering 2 m; flat classes 256-512 px tile (nothing to resolve) or untextured vertex-colour; hero label faces 2048 px; mipmaps on, anisotropy 8 (T-A08-03). Texel density stays a HYPOTHESIS: target 1 texel per screen pixel on hero faces, 0.5 elsewhere.

## T-A08-06 Prop budget per short (F-A08-101, 102)
2-3 hero props per short (median 3), each a modelled mesh with ONE readable face (text or number, cap height >= 35 px); at least one sign/board/counter per short; 1 flat-card illustration panel mounted on a mesh frame when a picture is needed; no outline on props in lit-PBR scenes (outline only on characters; props get rim light + shadow shape). Camera must move >= 10 degrees around a hero prop at least once per beat so perspective proves it is 3D.

## T-A08-07 In-world screen builds (F-A08-107)
(a) Monitor: plane with dark bezel mesh, texture = pre-rendered 2D clip (render-to-texture or video), emissive 1.5, slight reflection stripe; content flat 2D, smaller than the room. (b) UI card: Remotion overlay, rounded white card, 12 px outer glow, loading spinner; no 3D. (c) Lens/scope insert: circular mask (gold ring 8-12 px) over a flat painted scene, slow 2D parallax only. Budget: at most 1 screen per short; A28's frame check: second scene inside must be legibly different from the room (different palette).
