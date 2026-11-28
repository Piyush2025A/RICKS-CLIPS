# A16 TECHNIQUES — original edit decision list recipes (evidence: FINDINGS F-a16-001..009; confidence mostly medium)
Timeline master: 30 fps (final), 24 fps for dev renders (360p). Define everything in seconds and convert: frames30 = round(s*30), frames24 = round(s*24). EDL template: `data/EDL_TEMPLATE.json`.
Validation: `total_frames == round(audio_length_s*fps)` (QC R1).

## 1. Shot-length and rate targets (≈ 60 s video; median shot ≈ 3 s, 12-18 shots)
| Window (norm. time) | Transitions per video | Shot length target (s) | 30 fps frames | 24 fps frames |
|---|---|---|---|---|
| Hook 0-3 s | 0-1 (median 0) | first shot 2.1-6.3 s (median 3.7) | 64-189 | 51-151 |
| Setup 3 s-25 % | 2 (1-4) | median 2.9, IQR 1.9-5.1 | 87 (58-153) | 70 (46-123) |
| Escalation 25-55 % | 4-5 | 2.9 (1.8-4.8) | 87 (55-143) | 70 (44-114) |
| Reveal 55-85 % | 3 | 3.1 (1.9-5.1) | 92 (56-153) | 74 (45-122) |
| Punch 85-100 % | 1 | 3.1 (1.9-4.1); last shot ≈ 2.9 (1.8-5.1) | 94 (56-124) | 75 (45-99) |
Overall rate 2-2.6 transitions /10 s; no ramp-up (F-a16-001). Min shot ≈ 0.47 s (14 f), max ≈ 10 s unless camera/acting changes (rule 4). For a faster cut-driven variant (RC30-22/01/25 style) use 0.7-1.2 transitions/s only with hard cuts/scene hops.
Scale for other runtimes by normalised time; keep shot length absolute.

## 2. Transition placement relative to narration (F-a16-003/004)
- Default join: 7-frame crossfade at 30 fps (≈ 0.233 s; 6 f at 24 fps, converted by time; A15 3B + AUDIT_3B #3), centred on a clause boundary. [Phase 4 correction 2026-11-28, D033: see knowledge/PRODUCTION_DEFAULTS.md]
- Target: centre of the blend at (pause_start + pause_end)/2 of the nearest A20-style speech gap ≥ 0.15 s, tolerance ±5 f (0.17 s); observed median offset 2.8 f, signed +1.2 f from a gap edge. Pauses ≥ 0.3 s are scarce (≈ 8-9 per video) - use them for act joins and reveals.
- Do NOT lock to word onsets; they are every ~0.33 s. Word-locked items: captions only (lead audio ≈ 140 ms, A20 3B). Expression swaps follow story beats, not words (A02 3B F-A02-103). [Phase 4 correction 2026-11-28, D033: see knowledge/PRODUCTION_DEFAULTS.md]
- If no pause within ±0.25 s, shift the cut to the nearest clause end; never cut mid-word-group for story reveals.
- Camera move starts at or just after the cut (A13: 34-44 % within 6 f of the join).
- Shot ≈ one clause (~9 tokens/3 s, one pause-phrase). A 2-clause sentence = 2 shots; 1 shot rarely > 2 pause-phrases.

## 3. Max dead-time rule (F-a16-008)
Event set E = {cut/crossfade start, camera move start or direction change, expression burst or pose change, prop/character entry, VFX}. Captions do not count.
- Gap between consecutive E members ≤ 3.5 s (typical max in references: median 3.3 s, IQR 2.6-3.8); hard fail at 6 s.
- Camera still ≤ 2.3 s (reference longest static run: median 1.5 s, p75 2.3 s); camera always has slow drift (static only 17 % of frames).
- Single scene with no cut ≥ 8 s is allowed only with ≥ 1 acting change per 2 s (RC30-18 t 33-43 s pattern).

## 4. Beat budget (60 s example, 30 fps = 1800 f)
Act 1 (0-15 s): 3 transitions + 1 move per shot; Act 2 (15-39 s): 5; Act 3 (39-60 s): 4 (end on the shortest-cut-rate section ~1.8/10 s). Open with a posed scene in motion; ≥ 1 visible change inside 1 s; first spoken word ≤ 0.3 s.

## 5. Pacing QC script spec (implemented: `scripts/pacing_qc.py`, smoke-tested on a 2-shot EDL only)
Input: EDL.json + words.json (A20 word timings t_on/t_off). Rules: R1 total frames == audio length (FAIL); R2 shots contiguous (FAIL); R3 shot < 12 f (WARN) or > 450 f with no move/expression (FAIL);
R5 max event gap ≤ qc.max_dead_s (FAIL; captions not counted); R6 ≥ 60 % of transition centres within ±7.5 f of a word gap ≥ 0.15 s (WARN; reference ≈ 65 % with span overlap, 26 % centre-in-gap);
R4 first transition ≤ 6 s (WARN); R7 crossfade length 4-8 f (WARN); R8 per-act cut rate 1.0-4.0 /10 s (WARN) — R4, R7, R8 are specified, not yet coded.
Report: per-act shot-length quartiles, events/10 s, max gap + frame, pause-alignment %. Re-run after every re-time; log `sha256(EDL)`.

## 6. Measurement recipe for new references (reproducible)
`scripts/gaps.py` → `pacing.py` → `beats.py` → `deadtime.py`; inputs: A15 CSV, A20 capser npy, A13 moves, A27 shot_features/motion. Check long-take videos at 1 fps before trusting cut counts (F-a16-002).

## Phase 3B: two-unit pacing budget (evidence F-a16-100..104; medium)
- Per 60 s video: ~13 edits (A15 real, 2.2/10 s, shots 3.2 s median, IQR 2.0-5.2) AND ~25 visual beats (4/10 s, ~1.9 s median) - so about one extra camera-driven scene change (fly-through, whip, fast push/pull) between consecutive edits. Use edit shots for EDL slots, beats for camera/animation scripts.
- Opener (0-3 s = 90 frames at 30 fps, 72 at 24): caption on screen from frame 0 (28/30); frame 0 is a live scene (mid-action 14/30, posed 16/30), never a title card; one visible beat (edit or fast camera event) inside 1-3 s (25/30 have >= 1; edit in 12/30; >= 2 beats in 15/30). If a stage opener is chosen (0-1 beats), carry it with a slow push/pull and expression changes.
- Dev check: count beats by composite every 3rd-5th frame, not by 1 fps tiles.
