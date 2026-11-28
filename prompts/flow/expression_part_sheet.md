---
template: expression_part_sheet
version: 1
intake_kind: expression
model_default: Nano Banana Pro
aspect_ratio: "1:1"
outputs: 1
---
# Expression part sheet (face swaps; hard swaps, no in-betweens)

## Prompt
Face expression sheet for the ORIGINAL cartoon character "{{character_name}}", using the attached approved turnaround as the
identity reference ({{reference_asset_id}}). A grid of {{rows}} by {{cols}} equally sized cells on a flat uniform neutral grey
(#808080) background, each cell holding ONE front-facing head only (same head size, same position inside its cell, same
head shape, headgear removed), with only eyes, brows and mouth changing. Expressions, left to right and top to bottom:
{{expression_list}} (default set: neutral, happy, sad, angry, surprised, scared, smug, blinking, talking open, talking closed).
Eye style: {{eye_style}}; resting face uses {{resting_eye_shape}} under a brow.
Style: flat 2D cut-out, soft gradient shading with no cel bands, clean uniform {{ink_colour}} outline about 3.7 percent of
head width baked in, at most 6 colours, no text, no labels, no cast shadows.
Original design only. Do not imitate any existing character or franchise. No real people, brands, text or watermark text.
Avoid: different head sizes between cells, tilted heads, hands, bodies, tears or sweat marks unless listed, text captions.

## Checklist
identical head outline across cells | cells aligned to a grid with clear grey gutters | each expression readable at 64 px
height | ink uniform | no text
