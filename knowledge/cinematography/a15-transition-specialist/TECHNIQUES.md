# A15 TECHNIQUES (provisional; OBSERVED on 24 videos)
- **Crossfade** (default scene join, 79 % of joins on 30 videos): linear alpha, **7 frames at 30 fps (≈ 0.233 s; typical
  6–8)** — 3B: tile reads median 6 f, A28 every-frame reads +2 f; convert by time for other rates: 24 fps dev renders
  round(0.233 × 24) = **6 frames**. [Phase 4 correction 2026-11-28, D033: see knowledge/PRODUCTION_DEFAULTS.md] Fast variant 4 frames (RC30-23/26 style); slow variant 8–10 frames for time/location
  change (day→night, RC30-15 style). Remotion: overlap two Sequences by N frames, outgoing opacity
  `interpolate([0,N],[1,0])`, incoming 1; keep camera moves and animation running through the overlap. Easing not yet
  measured → linear.
- **Hard cut**: 1 frame, no blend; angle change within a location, reaction/punchline beats. Use sparingly (12 % of
  joins; absent in 14 of 24 videos).
- **Zoom-through / iris**: continuous scale move into an eye, lens, scope, screen or porthole for 8–14 frames until the
  target fills the frame, then a 4–6-frame dissolve or circular iris reveal of the new scene (device = concept metaphor:
  eye = memory/brain, scope = watching). Three.js camera dolly or 2D scale + circular mask.
- **Fly-through**: camera path through an aperture (vent, windshield, doorway, barrel, foliage) with motion blur; new
  scene on the far side; 30+ frames when it carries narration.
- **VFX / object cover**: smoke puff, dust, explosion, glow bloom or foreground object (tree, pillar, hat) fills the frame
  for ~5–10 frames, scene swapped behind, then dissolve or circular/straight wipe. Muzzle flash: 1 white frame, cut next.
- **Validation**: run rcpipe on our render: dissolves = gradual candidates of 5–10 frames, hard cuts = single-frame
  candidates; in-shot VFX and camera moves also fire (precision ≈ 70 %) → confirm visually. Do not rely on the rcpipe
  hard-cut label meaning a real cut in 12–30-style content.
