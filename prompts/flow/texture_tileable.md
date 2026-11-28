---
template: texture_tileable
version: 1
intake_kind: texture
model_default: Nano Banana Pro
aspect_ratio: "1:1"
outputs: 1
---
# Tileable painted texture (albedo only)

## Prompt
Seamless tileable top-down painted texture of {{material}} for a stylised 3D scene, filling the whole square frame edge to
edge, no border, no vignette, no perspective, no lighting gradient across the image, no shadows, no objects, no text.
Painted flat colour with very low contrast variation; {{grain_note}} (default: flat with only subtle local variation for wood,
paint, sand, dirt, floors, sky; visible grain only for grass, gravel or lattice). Palette: {{palette}}, evenly lit.
The left edge must continue seamlessly into the right edge and the top edge into the bottom edge.
Original design only. No real photographs, brands, logos, text or watermark text.
Avoid: a single large feature in the centre, vignette, directional light, repeating obvious motifs, seams.

## Checklist (computational, A24/A25)
tile test: 2x2 repeat in a viewer shows no visible seam | mean luminance of centre vs edges within a few percent | no text
Note: the model does not guarantee seamlessness; offset the image by half its size to inspect the seams, and repair only in
derived copies (never alter the original).
