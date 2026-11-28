# Flow asset request templates (A23, v1, 2026-11-28)
Generic templates derived from STYLE_BIBLE v0.3 + CHARACTER/ENVIRONMENT bibles. **No final character or world design lives here:**
every `{{placeholder}}` is filled from a user-approved design brief (D-pending: own character signature, scenery-ink A or B).
Measured values are initial targets, not mandatory rules. One template file = one request type; one filled copy = one request
record (`REQUEST_SCHEMA.json`) that the user approves before a run (`pipeline/flow/WORKFLOW.md`).

| File | A24 intake `--kind` | Aspect | Background |
|---|---|---|---|
| `character_turnaround.md` | character | 16:9 | flat neutral grey |
| `expression_part_sheet.md` | expression | 1:1 | flat neutral grey |
| `separated_body_parts.md` | parts | 1:1 | flat neutral grey |
| `prop.md` | prop | 1:1 | flat neutral grey (hero) or in-scene |
| `texture_tileable.md` | texture | 1:1 | n/a (full-frame) |
| `environment_plate.md` | environment | 9:16 (or 16:9 for wide plates) | scene |

## Shared placeholders
`{{character_name}}` working ID (not a reference name), `{{head_shape}}` e.g. rounded-square or round (user-approved),
`{{palette}}` up to 6 named colours with hue spacing >= 60 degrees between co-present characters, `{{ink_colour}}` one very
dark hue (not pure black), `{{hand_style}}` ball or mitten (no fingers), `{{headgear}}`, `{{tertiary_mark}}`, `{{setting}}`,
`{{time_of_day}}`, `{{key_light_direction}}`, `{{scenery_ink}}` A (none) or B (inked).

## Style core block (copied into every prompt, from the bibles)
Flat 2D cut-out illustration, simple geometric construction, soft gradient shading with no cel bands, a clean uniform dark
ink outline of constant thickness about 3.7 percent of the head width baked into the art, limited palette of at most 6 colours,
very dark {{ink_colour}} line (not pure black).

## Originality block (copied into every prompt and checked by the user before approval)
Original design only. Do not imitate any existing character, mascot, franchise, channel, logo or set. No real people, no
brands, no text, letters or numbers anywhere in the image, no watermark text (the platform applies its own mark; never ask
for removal or imitation of a watermark).

## Lessons from the D015 test (viewed)
Shape words in the prompt were not obeyed (bean head, stick limbs came out as an ordinary face and body; hatching appeared
instead of flat colour). Templates therefore: state shape and proportions as numbers, repeat key constraints once in an
"Avoid" line, ask for gradient shading rather than "flat colours", and require a post-generation checklist (viewed by a
human) before accepting an asset. Expect several iterations per asset; each is a separate approved request.

## Checklist after every generation (human or viewed by assistant, log it)
Views/panels as requested and aligned; proportions near targets (head H/W about 0.93, height about 3.3 head heights, leg/torso
about 1.4 for the slim-adult default); no fingers; ink uniform; at most 6 colours; background flat; no text; not resembling a
known character; watermark present and untouched.
