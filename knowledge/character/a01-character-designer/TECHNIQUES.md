# A01 TECHNIQUES — original character design (derived from F-a01-001…012; untested)

## T-a01-01 Original cast spec template (one page per character)
- Role, personality, one-line silhouette sentence.
- Body template: slim / stout / tall + scale. Head ellipse w:h 1.1–1.25; torso width 0.55–0.8× head width; legs 2–3×
  torso (A03 finalises).
- Headgear/hair silhouette unique in the cast, readable as a filled shape at 64 px.
- Torso hue from a role table; ≥ 60° hue spacing between characters sharing a frame.
- Palette ≤ 6 hex: torso, hair/hat, accent 1–2, outline (dark tinted, not #000), face white.
- One mark only: glasses, facial hair or prop.
- Outline ≈ 3 % of head width.
- Consistency checklist: same hat/hair, hue within ±15° after lighting, same outline weight, same face proportions.

## T-a01-02 Google Flow brief (for A23)
- Flat 2D cut-out character sheet: front, 3/4, side, back on neutral grey; thick even dark-indigo outline; solid fills
  with one soft gradient; near-white face; no cast shadow; no background; orthographic.
- Separate sheets for head parts, expressions, hats; vary one attribute per run (e.g. hat silhouette only).
- Gate every sheet with the checklist and the 64 px silhouette test.
- Originality (HYPOTHESIS, director to confirm): do not reuse the reference's exact combination (white oval head, dot
  eyes, uniform stick limbs, pill torso). Candidate own signature: tapered limbs, rounded-square head, mitten hands,
  indigo outline.

## T-a01-03 Three.js / Remotion character card
- Layered PNG planes: head, hair/hat, face parts (eyes × 3 states, brows × 2, mouth ≥ 6), torso, arms, legs.
- Tint: `color = lerp(white, sceneAmbient, ~0.25)`; outline kept emissive (unlit).
- Blob or projected contact shadow under the figure; outline constant in screen space.
- Crowds: instanced cards, 3-colour palette, no face below ≈ 10 px head height.
- Exceptions by material swap: additive translucent blue for x-ray; recoloured face for gags.
