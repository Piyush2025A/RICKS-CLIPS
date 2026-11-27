# A15 TECHNIQUES (provisional; derived from OBSERVED partial data, 7 videos)
- Crossfade: linear alpha over 6 frames at 30 fps (0.2 s) default; 24 fps dev renders use 5 frames (same 0.2 s). Slow variant 8-10 frames (0.3 s) for time/location change (day to night). Remotion: overlap two <Sequence> by N frames, outgoing opacity interpolate([0,N],[1,0]), incoming 1; keep camera moves running through the overlap (do not freeze).
- Hard cut: 1 frame, no blend; use for angle change within a location, reaction beats, punchline.
- Zoom-through / pull-back: continuous scale move (camera dolly on a Three.js scene) into an eye, screen, or porthole for 8-14 frames, dissolve (4-6 frames) once the target fills the frame, then POV exit in the new scene.
- Fly-through: camera path through an aperture (vent, windshield) with motion blur, new scene revealed on the far side; 30+ frames when it carries narration.
- VFX cover: flash/dust/explosion fills frame for ~8-10 frames, scene is swapped behind it, then dissolve or reveal. Muzzle flash: 1 white frame, cut next frame.
- Validate by running rcpipe on our render: dissolves should appear as gradual candidates of 5-10 frames, hard cuts as single-frame candidates.
