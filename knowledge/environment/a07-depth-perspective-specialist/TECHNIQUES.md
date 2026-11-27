# A07 TECHNIQUES (derived from FINDINGS; parameters at 1080x1920, scale blur px by output height/1920)

| Shot type | DOF | Bokeh/blur (px@1080 wide) | Focus target | Share of shots with DOF |
|---|---|---|---|---|
| Wide / establishing | off | 0 | n/a | ~8 % |
| Medium (default) | off, or 2-3 px on far plane | 0-3 | character card | ~15 % |
| Close-up | on | 6-12 on background | face | ~70 % |
| Macro / object | on | 6-12 (strong 12-20 rarely) | object | ~30 % |
- Scale: at 360p output multiply by 360/1920 (12 px -> 2.3 px). Implement with @react-three/postprocessing DepthOfField (focusDistance = distance to card in normalised depth, focalLength 0.02-0.05, bokehScale 2-4) or custom 2-pass Gaussian on a depth mask; keep ink outline of the focused card unblurred.
- Focus pull: ramp bokehScale 0 to 3 (or reverse) over 24-30 frames at the cut-in, max once per video.
- Fog (outdoors only): THREE.Fog colour = horizon sky colour, near 10 m, far 150-400 m so far ground colour sits at about 55 % of the near-ground distance from sky colour (dE76 far/near 0.4-0.65); keep texture contrast. Stylised full-frame haze (colour veil) only for metaphor scenes (red haze, blue underwater).
- Camera height: default eye-level to character mid-body (0.8-1.2 m for 1.5 m characters); 16 % low (0.2-0.4 m, ground and rails dominate), 20 % high (looking down 25-45 degrees for desks/plazas/aerial).
- FOV: start at vertical 60-70 degrees (hypothesis), horizon at 0.35-0.45 of height from top (shift principal point rather than tilt when cards must stay upright).
- Depth ordering: every shot has near framing element (0.5-2 m), subject, far backdrop; props in front of lower card body.
