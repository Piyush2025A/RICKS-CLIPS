---
template: environment_plate
version: 1
intake_kind: environment
model_default: Nano Banana Pro
aspect_ratio: "9:16"
outputs: 1
---
# Environment plate for 2.5D layers (one request per layer)

## Prompt
Background art for an ORIGINAL animated short, location: {{setting}}, {{time_of_day}}, layer: {{layer}} (one of: far
plane (sky and distant shapes, calm and low detail); mid plane (main set, subject area clear and uncluttered); near
foreground framing (objects at the edges only, centre empty); each as a separate image).
Perspective: eye-level camera, horizon about 38 percent from the top, vertical field of view about 70 degrees, one clear
vanishing point. Key light from {{key_light_direction}} with sky-coloured fill (key to fill about 7 to 1), colour shift toward
the sky colour with distance (haze), warm light, cool shadows. Calm back plane, denser detail only in foreground and mid.
Painterly flat colour, soft gradients; {{scenery_ink}} (A: no outline on scenery; B: clean {{ink_colour}} outline on objects).
No characters, no people, no animals unless listed: {{allowed_creatures}}. No text, signs with readable writing, logos or
watermark text. Leave the central vertical third free for character placement.
Original design only. Do not recreate any existing film, game, channel or real place.
Avoid: photorealism, lens flare, heavy blur, vignette baked in, grain, tiny clutter, characters.

## Notes
Far plane: no alpha needed. Mid and near planes need alpha for layered parallax; Flow is not guaranteed to deliver
transparency, so request near-layer elements on flat neutral grey (#808080) background and let A24/A25 key them as derived
assets. Targets in the prompt are initial values from the bibles, not rules.

## Checklist
horizon height | light direction consistent across layers of one scene | centre third clear | no text | no characters
