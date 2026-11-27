# A05 TECHNIQUES — approved only after verification; entries below are RECIPES derived from F-A05-xxx, not yet tested in our renders
Status: all entries `derived-not-yet-built` (no OUR-* render exists). Promote to "approved" only after an EXP record with an OUR- frame.

## T-01 Geometry vs plate per shot type (from F-001, F-009, F-010, F-012)
| Shot type | Build as | Camera | Notes |
|---|---|---|---|
| Establishing exterior (street, field, fort, town) | true 3D: terrain + 20-200 instanced props + sky dome | dolly/crane 2-6 m travel, 30-90 deg orbit | depth of field + fog for falloff |
| Room interior with character | box room 3-5 m, real-scale furniture (door 2.1 m), practical lights | slow dolly 0.5-1.5 m or orbit 10-30 deg | back wall must stay >=2 m behind the character |
| Macro object hero | single modelled object + blurred set | near-plane 0.01, FOV 25-35, DOF | 20-80x magnification |
| Cutaway / cross-section | box slab 1-2 m thick, front removed, painted strata | perspective -> frontal move | characters flat inside |
| Diagram / UI / counter | flat plane in scene (canvas texture) | any | text crisp via canvas, MSDF if distant |
| Scope / peephole bridge | full-frame circular mask over a 3D or plate render | static | doubles as transition |

## T-02 Set budget per short (30-60 s)
5-8 distinct sets; 1-2 hubs reused 2-3 times (new angle + time-of-day variant); 1-2 macro objects; 1 diagram. Establish with a wide shot where the character is <10 % of frame height, then cut/dolly to 15-25 %.

## T-03 Scale table
Door 2.1 m, character plane 1.5 m (bean body 0.5 m, legs 0.9 m), chair seat 0.45 m, table 0.75 m; hero props x1.5-3; crowd members 1.5 m planes (instanced, 2-4 colour variants).

## T-04 Treatment A (lit PBR, no scenery outlines)
MeshStandardMaterial + HDRI-light + 1 key directional with PCF shadow + bloom (threshold 0.8) + SSAO light; tiling PBR textures; ink outline on characters only (2-4 px at 1080 wide, black). Fog: exponential, matched to sky.

## T-05 Treatment B (inked scenery)
Outline pass: inverted-hull mesh (back-face scale 1.01-1.02, black) on architecture/props, or post-process depth+normal Sobel; line weight 1.5-3 px (1080 wide), thinner with distance. Flat or 3-step ramp toon fill (MeshToonMaterial with gradientMap 3 steps), painterly noise texture overlay (tileable, 5-10 % luminance variance), rim light. Keep outline locked to geometry edges (it does so in the reference during moves).

## T-06 Asset list template (per set)
`set-id | type(int/ext/cutaway/macro/diagram) | footprint m | hero props (<=3, oversize) | instanced repeats (what, count) | signage planes (text, size) | light key hue + practicals | time-of-day variants | camera corridors (A13) | surfaces for A08`.

## T-07 Camera corridor rules
Keep a clear 0.6-0.8 m wide tube along the dolly path, 1.2 m headroom for crane-up; orbit target at the character plane; no geometry between camera and character within 1 m except planned foreground (DOF-blurred foreground framing objects are used in the reference, e.g. 02 f000254..f000337 area).

## T-08 Google Flow prompt guidance (original environment art, for texture/concept plates only; Flow cannot be driven from this container)
Template: "<location type>, original design, stylised 3D game-engine render, <time of day> lighting, <key hue> palette, wide establishing view, vertical 9:16, no characters, no text, no logos, no real brands". Add "inked outlines, flat painterly fills" for treatment B. Avoid referencing the channel, its characters or exact set concepts. Output = concept/texture reference for A08; geometry is still built in Three.js.
