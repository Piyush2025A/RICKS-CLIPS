# A13 TECHNIQUES — camera move library (derived from F-a13-001..009; parameters are measured medians, validate on our renders before locking)

Conventions: frames at 30 fps (reference) and 24 fps (dev renders; multiply by 0.8). Zoom % = cumulative scale change (log-ish sum of per-frame %).
Translation % = % of frame width (10.8 native px at 1080). Easing functions: `smoothstep(t)=t*t*(3-2*t)`, `sine(t)=0.5-0.5*cos(pi*t)`,
`easeOutQuad(t)=1-(1-t)^2`, `expDecay(t)=(1-exp(-lam*t))/(1-exp(-lam))`. Status: all `proxy-measured` (status candidate until validated on renders).

| ID | Move | Dur 30 fps | Dur 24 fps | Easing | Magnitude | Notes |
|---|---|---|---|---|---|---|
| T-01 | Push-in (dolly/scale) | 35 f (IQR 20-54) | 28 f (16-43) | smoothstep (3B: 60 % of 30-video fits, 75 % native) | 3B: +24 % total scale (IQR 10-46) over ≈ 33 f, native-validated (F-a13-100/101; old +22 % summed proxy superseded) | peak rate ~1.2 %/f at 30 fps (about 0.85 s mid-move); peak at 50 % of move; start on shot's first frame (F-a13-006) |
| T-02 | Pull-out | 27 f (12-42) | 22 f (10-34) | smoothstep | -15 % (7-30) | 34 % of scale moves are pulls; use for reveals / ends of beats |
| T-03 | Pan/tilt track | 32 f (median, 17-52) | 26 f | smoothstep, or linear for constant-speed tracks | 45 % W total (IQR 21-72), peak 2.3 %W/f | rarely pure (19 %); combine with T-01 |
| T-03b | Push + drift (combined) | 32 f | 26 f | one smoothstep on both channels, same timing | scale 22 % + pan/tilt 20-70 % W | 66 % of all moves are combined; the default move |
| T-04 | Creep under holds | whole hold (>=15 f) | | linear | 0.10-0.30 %/f scale (3-9 %/s) or 0.2-0.5 %W/f drift | 18.6 % of frames are creep; dead hold 10.5 % (use <= 0.5 s) |
| T-05 | Dead hold | 8-15 f | 6-12 f | - | 0 | sparingly; before a hit or after a fast settle |
| T-06 | Roll | not a deliberate move | | - | cumulative <= 1 deg | median cumulative roll 0.9 deg; do not add a dutch roll by default |
| T-07 | Shake | none | | - | optional <= 0.1 %W RMS if a render looks too stable | F-a13-005: dataset shows no shake, impacts are sold by object animation |
| T-08 | Shot-anchored timing | onset = shot frame 0..6 | | - | - | 35-44 % of moves start within 6 f of a boundary (chance 15 %); no word-sync needed |
| T-09 | Fast entry + settle | 30 f (IQR 17-52) | 24 f | `expDecay` lam 3-4 or easeOutQuad | start 3-6 %/f scale or 6-12 %W/f, decays to rest | for transitions into a shot (screen zoom, whip); coordinate with A15 |
| T-10 | Long corridor dolly | 150-275 f | 120-220 f | linear speed with 10-20 f ease ends | +300 % to +500 % scale | needs deep interior geometry (A05/A07); keep vanishing point near centre |

## Easing fit summary (for code)
- Default for deliberate moves: `smoothstep`; attack (10 to 90 % of peak) about 10 f at 30 fps (8 f at 24), release about 11 f; peak at t = 0.5.
- Alternatives seen: linear 30 %, ease-out quad 14 %, ease-in quad 12 % of non-fast moves; use ease-out (or `expDecay`) only for settle after fast entries.
- Remotion: `interpolate(frame,[0,dur],[0,1],{easing:Easing.bezier(0.42,0,0.58,1)})` is the closest built-in to smoothstep; for exact smoothstep use `t*t*(3-2*t)` by hand. Three.js: tween `camera.position` (dolly) or `object scale` of 2.5D layers (T-01 on cards), combined channels share a single eased `t`.

## FOV guidance (INFERRED, low confidence)
Vertical FOV 55-60 deg for 3D sets with real dolly (parallax visible), A07 hypothesis 55-80 deg; do not animate FOV. For 2.5D card layers apply push as uniform scale about the framing target (A14 owns the target), parallax from layer depth.

## Shot plan rule of thumb
Per 60 s short: about 33 moves/min detected over 16.5 valid minutes (555 moves): about 15/min non-fast plus 18/min fast entries/transitions; every shot should have either a creep or a move; at most one 8-15 f dead hold per shot.
