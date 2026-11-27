# A13 Camera director — FINDINGS (Phase 3, RC30)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` · date 2026-11-28 · visual-ledger records 6
(`knowledge/dataset/coverage/visual/a13-camera-director.jsonl`) · **videos covered computationally: 23** (RC30-01..05, 07, 08, 14..20, 22..30 as
processed so far; 06, 09-13, 21 absent from `v0.2.0` at run time). Scripts: `data/scripts/*.py` (originals in
`~/ricks-clips-private/analysis-data/rc30/agents/a13-camera-director/`, run order moves.py > ease.py > shake.py > sync.py > final.py).
Tables: `data/camera_per_video.csv`, `data/moves_table.csv` (555 moves), `data/*.json`.

## Method and global caveats (apply to all findings)
- Input: `motion.csv` tx, ty, scale, rot_deg are per-frame increments (frame 0 NaN), proxy <= 320 px. I convert tx/ty to **% of frame width/frame**
  (tx/320*100), scale to **%/frame** ((scale-1)*100), roll in deg/frame. 1 % W = 10.8 native px.
- Masked (NaN) frames: confidence `low`/`none`, and frames within +-2 of every `shot_candidates.json` candidate (cut/gradual/flash; so crossfades are
  excluded, candidates used as soft boundaries). 79-91 % of frames remain per video. Masking biases against static low-texture frames.
- Segmentation: valid runs >= 12 frames, 3-frame box smoothing. Intensity = max(|scale|/0.6 %/f, hypot(tx,ty)/1.2 %W/f, |rot|/0.3 deg/f). A **move** = run with intensity >= 0.5
  for >= 4 frames and a peak >= 1.0, extended to 15 % of peak. Hold = |scale|<0.10 %/f and |t|<0.20 %W/f and |rot|<0.05; creep = below half the move thresholds; else move.
- Tiers: **fast** = peak scale >= 3 %/f or peak translation >= 6 %W/f (303 of 555 moves; mostly transition-like, whips, dives, screen-zoom reveals; low reliability);
  **non-fast** = the other 252 (the camera-craft moves). `near_cand` = within 15 frames of a candidate.
- The 2-D similarity model of a 3-D scene: dolly vs zoom not separable; object motion and parallax leak in (calibration doc). Magnitudes are proxy estimates (upper bounds).
- Not a source of ground truth for our renders yet: our renders have not been run through this estimator (open item).

## F-a13-001 — The camera is almost never locked off; dead holds are rare
Label MEASURED. Confidence medium-high (n=23 videos, 29,782 valid frames; thresholds mine; proxy).
Evidence: `motion.csv` all 23 videos; `data/camera_per_video.csv`. Per-video share of valid frames: hold median **10.5 %** (IQR 8.7-19.1; range 1-34 %, highest RC30-07 34 %),
creep (slow drift) **18.6 %** (IQR 14.7-25.9), move **64 %** (IQR 56-74). So ~90 % of frames have camera change above the noise floor, consistent with F-A05-002 (59-80 %).
Noise floor of the estimator in held frames: high-pass RMS 0.08 %W (about 0.8 native px).
Limitations: low-confidence frames dropped; object motion leaks into "move". Implementation: never hold a static camera > ~0.5 s; add a slow creep (push or drift 0.1-0.3 %/frame, about 3-9 %/s) under every hold; see TECHNIQUES T-04.

## F-a13-002 — Move taxonomy: pushes dominate, mostly combined with a small pan/tilt
Label MEASURED (+ OBSERVED, 6 ledger records). Confidence medium (n=252 non-fast moves, 23 videos; kind label depends on my thresholds).
Counts non-fast (roll flag removed): push+tilt 63, push+pan 38, pull+pan 34, pan 33, push (pure) 32, pull+tilt 24, tilt 16, pull (pure) 10, roll-only 2.
Push-in 133 vs pull-out 68 (all non-fast moves containing scale change) = **66 % push / 34 % pull**; present in 23/23 (push) and 21/23 (pull) videos. Pure pan/tilt only 49 of 252 (19 %);
**combined moves = 66 %**. Roll: 55/252 moves exceed 0.3 deg/f but cumulative roll median 0.9 deg (p90 4.7, p99 12.1): roll is a by-product (parallax/tilt coupling), not a deliberate dutch in the table; no deliberate roll move found. Roll-only = 2 moves (likely estimator artefacts).
Moves per minute (all tiers) median 32.6 (IQR 25.5-35.0). Typical duration non-fast median 32 frames (1.07 s at 30 fps; IQR 17-52 f). Frequency per video: `data/camera_per_video.csv`.
Implementation: library T-01..T-06.

## F-a13-003 — Push-in magnitude and duration (reconciles the A14 zoom-rate contradiction)
Label MEASURED proxy; visual check OBSERVED (RC30-15 f000336-f000383). Confidence medium-low (magnitude upper-bound, n=133).
Non-fast push-in: cumulative scale change (sum of per-frame %) **median 22 % (IQR 13-40)** over **35 frames (IQR 20-54)** = 1.2 s (0.67-1.8 s); mean rate 0.68 %/f (IQR 0.42-1.03) = 20 %/s;
peak rate 1.24 %/f (IQR 0.83-1.93). Pull-out: median 15 % (IQR 7-30) over 27 f. These are rates *during moves*; across whole shots (including holds) A14's 12 %/s median window is consistent. Eye check in RC30-15: a
tracking dolly-in with simultaneous pan, the subject roughly doubles in size over ~40 frames, so even the proxy's 55 % is not an over-estimate there (dolly + subject approaching). Where A14 eyeballed 5-10 %/1.6 s (RC30-15/-30) those are the creep category (F-a13-001), not moves. Not a contradiction once moves and creeps are separated. Both stay recorded.
Implementation: T-01 (push), T-04 (creep).

## F-a13-004 — Easing: in-shot moves are symmetric ease-in-out (smoothstep-like); asymmetric ease-out belongs to the fast tier
Label MEASURED proxy. Confidence medium (n=233 fitted non-fast moves with >= 8 frames, 23 videos; fast n=274).
Method: speed profile intensity(t) of each move window normalised to unit area; compare cumulative curves to 8 closed forms + generalised beta(a,b) (speed ~ tau^a (1-tau)^b, grid 0-4); RMSE of normalised cumulative.
Results non-fast: best fit smoothstep (3t^2-2t^3) 92 (40 %), linear 70 (30 %), ease-out quad 33 (14 %), ease-in quad 27 (12 %), sine 10, smootherstep 1. Median time of peak speed = **0.50** of move (IQR 0.32-0.68); attack (10 % to 90 % of peak) median **10 f** (IQR 4-20), release 11 f (IQR 5-19);
beta median a=b=0.5, |a-b| <= 0.5 in 82 % of moves. Clean subset (not near a shot candidate, not fast; n=74, 21 videos): smoothstep 48 (65 %), linear 10, ease-in 7, ease-out 6, sine 3; median RMSE smoothstep 0.054 vs linear 0.074, ease-out quad 0.198 (cumulative fraction); attack 12.5 f, release 12 f.
"Linear" wins mostly in windows truncated by crossfade masking (boundary-adjacent group: linear 60 / smoothstep 44), so a flat profile is partly an artefact.
Fast tier (n=274): ease-out quad best most often (69, 25 %), ease-in 48 (18 %), smoothstep 47, linear 40; peak in first 30 % of the move in 30 % of cases and in last 30 % in 28 %: no dominant shape.
**Contradiction (STYLE_BIBLE "ease-out bursts" vs motion.md "symmetric ease")**: our measurement supports symmetric ease-in-out for deliberate in-shot moves (65 % smoothstep in clean subset; peak position 0.5); ease-out decay exists as a settle after fast shot-entry moves (see F-a13-007; fits `exp_out`/ease-out in ~25 % of fast moves) but is not the majority. Both kept; estimator smoothing (3 f) and proxy limit fine detail.
Fitted parameters are in `data/moves_table.csv` (`best`, `ab`, `lam`). Implementation: T-02 easing table.

## F-a13-005 — No handheld shake, no impact shake in camera data
Label MEASURED + OBSERVED. Confidence medium-high for "no handheld" (n=23), medium for "no impact shake" (visual n=2 sequences).
Quiet frames (hold+creep, 10,879 frames): high-pass (frame minus 5-frame mean) RMS tx 0.076 %W (IQR 0.053-0.109), ty 0.098 (0.074-0.136), scale 0.057 %/f, roll 0.019 deg/f = about 0.8 native px: at the estimator noise floor; power is mostly below 5 Hz (fraction of tx power >= 5 Hz in quiet runs >= 48 f: median 0.27, n=22 videos; white noise would give about 0.67), i.e. no high-frequency jitter band. 
Sign-alternating burst detector (>=3 alternations in 12 f with amp >= 1.0 %W) fired 136 times in 22 videos, 79 away from candidates; checked RC30-01 f001344-f001391 (bubble impact/boil): the camera is steady, the signal is object/droplet motion leaking into the global model; and RC30-15 f000336-f000383 (cyclist crash): no camera shake on the impact. So the detections are not camera shakes. Impacts are sold by object animation, smears and VFX, not by shaking the camera (A14 may see "whip impact" as a different thing).
Limitation: 320 px proxy would show < 0.3 %W shakes poorly; only two visual sequences. Implementation: do not add procedural shake by default (T-07: optional, off).

## F-a13-006 — Moves begin with the shot, not on caption words (null result for words)
Label MEASURED, confidence low (caption events exist for 7 of my videos only: RC30-01..05, 07, 08; A20 capev.json; n=108 non-fast moves).
Move onset to nearest caption-change event: median |lag| 2 frames vs 3 for random onsets; within 3 f: 65 % vs 63 % baseline (200 random draws per move, same videos); within 6 f 90 % vs 90 %. Captions change every ~9 frames, so the test has no power to separate word-locking at 3-6 f: **no evidence of word-locked move onsets; neither proven absent.**
Move onset vs shot boundary candidates: non-fast moves starting within 6 frames of a candidate end 34.5 % vs 14.7 % chance (n=252, 23 videos); fast moves 43.6 % vs 14.8 % (n=303); within 15 f 45 % / 55 % vs 31 %. So moves are **shot-anchored** (they start at or right after the cut/transition), partly inflated because masking removes the crossfade and truncates the start (limitation). Hold-then-move inside a shot is also common (clean subset n=78).
Visual: RC30-01 f000096-f000143 and RC30-15 sheets agree (the move begins on the shot entry, the caption word changes during it).
Implementation: start each shot's camera move on the shot's first frame (T-08); don't spend effort syncing camera onset to words; sync object beats instead (A04/A12).

## F-a13-007 — Fast shot-entry moves decay to rest (settle) and carry shot-to-shot transitions
Label MEASURED + OBSERVED. Confidence medium (n=303 fast moves, 23 videos; 55 % of all detected moves).
Peak speeds in this tier: scale to 3-6+ %/f and translation 6-12 %W/f (about 65-130 native px per frame at 1080 wide) at the first frames after a cut/crossfade and then decays over 20-60 frames to rest (RC30-01 f000128-f000190 trace: tx from -7 %W/f to 0, scale -6 %/f to 0 in ~45 frames). Duration median 30 f (IQR 17-52). OBSERVED RC30-01 f000096-f000143: the previous shot (rocket plume) is shrunk into an in-world screen while the new shot's camera pulls back (screen-zoom transition, ~6-frame blend then settle). These carry the cut and belong to A15; they are the "kinetic" component of the grammar (kinds: push+tilt 54+39, pull+tilt 44+26, etc.).
Implementation: T-09 shot-entry decay move (exponential/ease-out settle after a transition).

## F-a13-008 — Signature big moves inventory (frame ranges; 4 OBSERVED, rest MEASURED candidates)
Label: OBSERVED where marked (ledger), otherwise MEASURED candidates (needs sheet confirmation). Confidence medium for observed.
Criteria: cumulative |scale| >= 100 % or translation >= 100 %W within one move (>= 20 f). 284 moves exceed 40 % scale or 100 %W; top examples:
- RC30-25 f000446-f000721 (275 f) and f000725-f000879 (154 f): **long corridor dolly** down a hall of doors toward a far door (OBSERVED overview f000509-f000959: repeated runs down the same hallway, vanishing point stays centred; scale +533 %/+336 %). Interior depth makes the push read as flight.
- RC30-25 f000989-f001032: pull back out of the character's skull to his face (loop to the opening) (OBSERVED).
- RC30-14 f000114-f000177: pull-out from holster/bullet close-up to the full street, + pan (OBSERVED overview f000089-f000149; scale -296 %).
- RC30-14 f001079-f001199: low push/track across table to the phone (OBSERVED overview).
- RC30-01 f000128-f000190: pull-out from inside a screen (see F-a13-007).
- RC30-07 f000565-f000776 and f000624-f000774: pull + 670 %W pan (large lateral track, MEASURED only).
- RC30-29 f000744-f000845 pull -306 %, RC30-16 f000544-f000616 pull -283 % with tilt +389 %W, RC30-04 f000150-f000186 pull -240 %, f001127-f001189 pull -244 %, RC30-28 f000448-f000611 push +209 %, RC30-19 f000290-f000407 pull+tilt, f001702-f001806 push+pan: all MEASURED candidates, not viewed.
Dives into eyes / orbit reveals were not isolated: an orbit (rotation about a subject) shows as pan+roll+scale in a 2-D model and cannot be told from a dolly with parallax. Full list: `data/moves_table.csv` (sorted by |Z|). 
Limit: dolly vs zoom not separable; some entries may be cut-hidden zooms.

## F-a13-009 — FOV/lens guidance from motion (only inference)
Label HYPOTHESIS/INFERRED, confidence low. Deep corridor dolly (RC30-25), strong perspective converge during pushes and large pan translations (up to 6-10 %W/f) are consistent with A07's wide lens hypothesis (vertical FOV 55-80 deg). A pure zoom would not change parallax; the corridor sequence shows changing relative depth (OBSERVED), so camera translation (dolly) is used there. For pushes on characters (2.5D cards) scale change of the whole card is a dolly or a scale tween: equivalent. Use FOV 55-60 for 3D sets with dolly; do not animate FOV (no evidence of lens-zoom moves).

## Open items
- Run our own Three.js renders through the same estimator to validate magnitudes (EVIDENCE: our moves validated on 360p renders).
- Re-run after the batch completes (RC30-06, 09-13, 21 missing): `python3 data/scripts/final.py` chain.
- Dolly vs zoom separation needs depth cues (A27/A07).
