# A02 FINDINGS — facial expression system (Phase 3, RC30)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` | date 2026-11-28 | visual ledger
`knowledge/dataset/coverage/visual/a02-facial-expression-specialist.jsonl` = 58 records after Phase 3B (29 overview/strip images in 3A + 29 every-frame strips in 3B). Phase 3B: every-frame native-crop strips viewed for 24 more videos (see F-A02-101).
Videos with catalogue evidence (1 fps overview, first ~40 s): RC30-01,02,03,05,07,09,10,12,13,15,16,18,19,21,22,25,26,27,28,30
(**20 of 30**). Every-frame face strips (native frames, private): RC30-03 f830-877, RC30-25 f0-95, RC30-27 f100-195,
RC30-30 f30-125 (+f560-607). Builds on F-a01-008; not repeated. Overview tiles are 1 frame/second, so rare states are
under-sampled; counts below are "seen", not frequencies.

Limits: second halves of videos were not viewed; timing n is tiny (4 shots) -> every timing claim is low/medium confidence.
Audio: caption-vs-audio alignment could not be established (see FAILED.md F-A02-X1), so "word onset" = burned-in caption change.

## F-A02-001 [PARTLY SUPERSEDED by F-A02-101: construction claim stands; swap-timing claim re-graded] Face grammar is one construction with swappable parts (eyes x brows x mouth x accessories)
OBSERVED. Construction part: high (20 videos at 1 fps tiles). Swap-timing part ("between consecutive frames, no tweens"): was labelled high (20/20) but 3A had frame-level evidence in only 4 videos; 1-fps tile ranges cannot show a tween (A28 claim #16). Re-graded in F-A02-101. Head = white/skin circle with ink outline; every state is a hard-cut swap of drawn parts,
no tweened morphs seen (swaps happen between consecutive frames: RC30-25 f37->f38 bars->rings, f44->f45 half-lid->`><`;
RC30-30 f79->f80 sleepy bars->ring eyes). Same grammar is applied to non-humans: pills (25 f239), powder sack (22 f869),
brain (28 f239), gold-coin/fish faces. Characters facing away show no face (26 f479).
Implementation: face rig = 4 independent layers (eyes, brows, mouth, accessories) + head wobble; state change = visibility
swap on one frame, no interpolation. See TECHNIQUES T-A02-01.

## F-A02-002 Eye states catalogue (11 seen)
OBSERVED, high for 1-6, medium for rest (single examples).
1 dot/oval pupils (neutral, default): 27 f89-150, 30 f97-125. 2 dot eyes + heavy half-lid bar over them = smug/bored
(09 f179, 27 f209, 03 f830-844). 3 flat bars / stacked double lines = closed/sleepy/pain-stricken (30 f30-79, 25 f36-37,
f70-80 headache stripes). 4 closed upward arcs `^ ^` = happy/laugh (01 f29, 09 f779, 05 f1139, 19 f89, 25 f299).
5 white rings with centred pupil dot = shock/realisation (01 f509, 28 f209 with huge size, 25 f38-43, 30 f80-89,
13 f89, 16 f719). 6 `> <` squeezed X = pain/rage/strain (25 f45-64, f93-95; 13 f1199). 7 big round white eyes with
small pupil, brow-less = panic/terror (28 f89-119, 22 f239). 8 glasses (ring frames, persistent, 02,09,19). 9 sunglasses/
black visor = smug-cool (02 f449-509, 07 f869). 10 glowing blue irises = supernatural (30 f839 "hypnagogia").
11 red glowing eyes + red cracks = rage (09 f809-839). Pupil position shifts 1-2 px inside rings to indicate look
direction (30 f568-570).

## F-A02-003 Brow vocabulary
OBSERVED, medium-high. Heavy single-stroke brows, separate from eye: flat (neutral), one raised (27 f100-147 left raised
+ half-lid = sceptical/smug), both raised high with ring eyes (30 f574-577), inward-down angled (angry, 30 f584-607, 10 f539),
inner-up worried (13 f89, 21 f149), none visible in `><` and arc-eye states (brows merge into the glyph). Brow angle
swap is one of the cheapest, most-used beats: 30 f574->578->584 changes brow 3 times in 10 frames.

## F-A02-004 Mouth catalogue (13 seen)
OBSERVED, high (1-6 in >= 12 videos). 1 tiny line/dash or small tick (neutral, narrator). 2 small smirk curve (30 f93-96).
3 wide grin with teeth grid (22 f89, 13 f89, 19 f929) = joy or nervous. 4 gritted rectangular teeth grid = pain/strain/
rage (25 f16-21, f48-64; 13 f1019; 18 f1049). 5 open oval `o` = shout/surprise (25 f15-20, 22 f239). 6 wide open
shouting mouth with tongue/red inside (25 f29, 03 f854-866, 05 f1109 laugh). 7 wavy "mustache" squiggle = unease/awe
(30 f80-89, 22 f869). 8 frown arc (22 f899, 21 f659). 9 lopsided toothy smirk (30 f90-92, 03 f849). 10 closed-smile
curve (18 f509, 12 f1019). 11 laugh = closed-arc eyes + open mouth with dark interior (05 f1109-1139, 21 f209). 12 whistling/
pursed (rare, 16 f959). 13 mouth hidden by hand/object. Mouth colours: red tongue/interior drawn inside open shapes.

## F-A02-005 Accessories / effect marks
OBSERVED, high. Sweat drop(s) on temple (25 f0-95, 13 f89-119, 01 f509, 28 f239, 22 f869, 10 f1139); red radiating
"pain/anger" tick lines around head (25 f0-65, 03 f449); blush patch pink on cheek/forehead (25 f48-95); steam puffs +
skin tint purple for fury (10 f539-599); X/"Z" sleep marks (21 f1019); tears (A01 f-a01-008); stacked headache lines
(25 f70-80); emotion colour tint of whole head (green-yellow 16 f119, purple 10 f539, blue-ish 30 f989 sleep). Accessories
appear in the same frame as the state swap and persist as long as the state holds (25 f0-64 sweat+ticks ~65 frames).

## F-A02-006 Expression is hold-and-snap, not continuous
OBSERVED/MEASURED-by-eye over 4 shots, medium-low (n=4 shots, ~190 frames).
Segment tally (state changes of eyes/brows/mouth visible in every-frame strip):
- RC30-25 f0-95 (3.17 s, pain-gag beat): ~13 changes = ~4/s; holds of 1-4 frames until f45, then ONE hold of 20 frames
  (f45-64, `><` + grit teeth + sweat).
- RC30-30 f78-125 (1.57 s, wake-up snap): changes at f80, f90, f93, f97 -> 4 changes in 20 frames then a >=28-frame hold.
- RC30-03 f830-877 (1.6 s, talking character): mouth shape swaps ~11 + 1 blink; shapes held 1-5 frames.
- RC30-27 f100-195 (3.2 s, narrator close-up): 0 expression changes, only blinks/half-lids (f100, ~f146).
So: expression density is bursty. Burst = 3-5 swaps within ~10-20 frames at the beat, then a hold of 20-100 frames.
Per-second rate averages ~1-4 depending on beat; bursts exceed 4/s. Distribution: holds 1-5 f (inside a burst), 20-30 f
(reaction hold), >=96 f (narrator neutral).

## F-A02-007 Expression snap relative to word change
MEASURED (caption-change detection, `scripts/cap.py`) + OBSERVED, low (n=9 swaps, 1 shot with clean data).
RC30-30 f78-125: caption changes at f83, f93 (+f114). Swaps: ring eyes + wavy mouth at f80 (3 frames BEFORE caption f83),
smirk/bars at f90 (3 BEFORE f93), pupils/half-lid at f93 (0), neutral dots at f97 (4 after). RC30-03 f830-877: captions at
f830, 841, 846, 852, 871, 876; blink f845-846; mouth burst starts f848 (+2 after f846 caption, 4 before f852), open mouth
f854, f863, mouth change f870-871 (0 vs caption 871). Reading: swaps lead or coincide with the caption word by -3..+4 frames
(median ~ -1, IQR ~ [-3, +2], n=9); NOT locked to a single constant. Assumption: caption appears at (or slightly after)
speech onset; unverified against audio. Implementation: schedule swaps at word_onset - 3 .. +2 frames (median 0/-1).

## F-A02-008 Mouths: narrator does not lip-sync; acting characters flap in bursts
OBSERVED, medium (n=4 shots). Narration (voice-over, caption-timed) runs while the on-screen face is silent: RC30-27
f100-195 (>= 96 frames of narration, mouth = one static tiny shape). Characters "speaking" in-scene (03 f848-877)
use a 4-shape flap set (closed line, teeth-grid half-open, open with red tongue, narrow grin), shape held 1-5 frames, no
phoneme matching to the VO (the VO is the narrator describing the scene). RC30 frame data cannot show a speaker/
non-speaker highlight; the "speaker" is distinguished by head tilt/wobble + open mouth, not by outline or tag.
No visible per-word mouth sync -> do not build a phoneme viseme engine; build a 4-6 shape "acting flap" triggered per beat.

## F-A02-009 Blink
OBSERVED, low-medium (n=4 blinks in ~240 frames). Shape: open -> half-lid (1 f) -> shut bar/arc (1-2 f) -> open
(03 f845-847, 25 f35-37, 27 f100, f146-147). Duration 2-4 frames (~67-133 ms) at 30 fps. Interval: ~2-4 s where seen
(no blink in 30 f30-77 = 1.6 s; none in 27 f101-145 = 1.5 s); eyes also hold shut as expression (sleep, 30 f30-79). Blinks
are drawn as the same swap layer (eyes layer replaced with bars for 1-2 frames), not a separate animation.

## F-A02-010 Dialogue/actor distinguishability and exceptions
OBSERVED, medium. Exceptions/variations: (a) RC30-13/18/19 show 3+ characters each with different brow+mouth in the
same frame (13 f989-1019, 02 f389), group reactions use the same states; (b) crowd faces are dot-eyes at tiny scale (A01);
(c) full-face colour/shape effects (02 f419 sunglasses, 10 f539 purple, 09 f809 red cracks) are used once per video at the
climax; (d) eyes/mouth rarely rendered in wides (< 8 % frame height); readable states in wides: ring eyes, grin, `><`.
Readability at 48 px NOT tested numerically (could not crop at 48 px; viewed overview tiles 180x320 where the 9 largest-eyed
states above are still legible: ring/dot/arc/`><`/bar; mouth teeth grids and tongue were legible only on close-ups).

## Phase 3B additions (2026-11-28)
Method (all F-A02-1NN): candidate local-change frames found computationally (`scripts/det3b.py`: half-res-quarter gray frame diff, caption boxes masked, local component < 130 px; all 30 videos decoded, 29 had >=1 cluster picked by `scripts/pick3b.py`), then 3 clusters per video rendered as every-frame native-resolution crops (110x110 tiles, 14/row, frame number printed) and viewed (29 images, logged). Events were then read by eye from those strips into `data/expression_events_3b.csv` (56 rows: 46 active events, 10 hold controls; 123 individual swaps counted). Detector hits many non-face things (signs, text, objects): ~1-2 of 3 clusters per video were faces, 5 videos (04, 11, 25-3B, 26, 28) gave no usable face. Tile size 110 px: part-level reads (eyes vs mouth) are reliable, fine shape reads and "0 in-between" are medium/low confidence. Manifest SHA-256 `fc6f147a...8e06`.

### F-A02-101 Expression changes are hard swaps of discrete drawings; no interpolated in-betweens seen (frame level, 24 videos)
OBSERVED, medium (24 videos with every-frame strips: 01,02,03,05,06,07,08,09,10,12,13,14,15,16,17,18,19,20,21,22,23,24,27,29 plus earlier 25,30; n = 46 active events in the CSV; 45/46 show 0 in-between, 1 (E13, eyes dots->line->ring over 2 frames) ambiguous). Reason for medium, not high: the 110 px tiles cannot rule out subtle tweens, "in-between" = a drawing that is a geometric interpolation of its neighbours (a sequence like squint -> half-lid bar -> ring counts as 3 distinct states, E01), and one reader. A change = one frame between consecutive drawings. Part changed (46 active events, multi-part events counted in each): eyes in 36, mouth in 20, brows in 7, whole face/head tilt 2. Mouth-open sequences (E05 f378-380) step through 2-3 drawings over 3 frames, i.e. a 1-frame-per-drawing mini-sequence, not a tween.
Implementation: layer visibility swap on a single frame; for "opening" actions chain 2-3 drawings at 1 frame each. Unchanged T-A02-01.

### F-A02-102 Hold lengths: bursts of 1-3 frame drawings, then holds of 10-30 frames
MEASURED-by-eye over strips, medium-low. Uncensored holds adjacent to active events (n = 26): median 5 f, IQR 4-8 (these are within-burst gaps). Ten hold controls (face visible, 0 swaps) lasted 11-31 frames (median 19; strip window limits them, so they are lower bounds): RC30-08 f1002-1020, 12 f808-818, 14 f984-1002, 15 f918-938, 17 f1419-1449 and f1555-1581, 19 f1694-1707, 22 f1371-1393, 23 f478-488, 29 f637-654. Pattern repeats from 3A F-A02-006: burst (3-6 swaps inside 6-15 frames) then hold >= 11 frames. Counts per burst in the CSV: median 3 swaps (IQR 2-4), longest talking bursts 12-17 swaps in 20-28 frames (RC30-02 f743-763, 27 f283-310 and f446-474).

### F-A02-103 Mouths are not locked to caption word onsets (12 talking shots, 10 videos)
MEASURED (low power) + OBSERVED, medium-low. Test (`scripts/sync3b.py`): local-change frames in the mouth/face ROI of 12 talking shots (RC30-02 f743-763, 03 f322-341, f761-775, 05 f1074-1093, 06 f1062-1078, 09 f16-36, f381-399, 12 f356-370, 14 f1390-1407, 15 f1333-1353, 27 f283-310, f446-474; 10 videos; 8-18 changes each) vs caption onsets (`caption_segments.csv`, 1-4 onsets per shot). Share of changes within +-2 frames of an onset vs the random-placement null (2000 draws): observed 0.25-0.73, null 0.25-0.65; per-shot p = 0.13 (min), 0.96 (max); 0/12 below p = 0.1. No shot shows lip-sync to words. Visual confirmation: the face holds one open-mouth drawing across two caption changes in 09 f16-36 (f19 'jail', f30 'cell'), the faces in 08 f1002-1020, 12 f808-818, 17 f1419-1449, 22 f1371-1393 do not move at all while the captions change 2-3 times. Acting characters flap mouths in the strip at 1-2 frames per shape (RC30-02 f743-763: 17 shape changes in 21 frames) regardless of word timing. Limits: 1-4 onsets per window -> low power; captions are the narrator's, not necessarily the shown character's speech; ROI proxy at 1/4 resolution.
Implementation: do not build a phoneme viseme engine; drive a 4-6 shape flap at 1-2 frames per shape on beat windows (talk window = caption phrase duration), hold neutral otherwise. Ratio of "talking-flap" to "silent hold" shots is high-variance, see CSV.

### F-A02-104 Blink shape in strips: shut for 1-3 frames, no tween
OBSERVED, low-medium (7 blink events in 6 videos: 03, 01, 09, 13 (x2, f948-950 and f961), 16, 29). Shape: open -> (half-lid 1 f in 3 of 7) -> shut line/bar 1-3 frames (median 2) -> open. Total 2-4 frames (67-133 ms at 30 fps), consistent with 3A F-A02-009. Interval: only one pair in a window (13 f948 -> f961, 13 frames = 0.43 s, probably a double-blink or a half-lid, low confidence). Interval/frequency could not be measured with 20-30 frame windows: still unresolved.

### F-A02-105 Face-detector yield and coverage limits
MEASURED. 29/30 videos produced at least one local-change cluster; ~half of 87 picked clusters were faces. 4 videos (04, 11, 26, 28) contributed no readable face, so the event table is biased toward videos with large head close-ups; wide shots with tiny faces are under-represented (consistent with F-A02-010d).

## Phase 3B revisions
- F-A02-001: swap-timing portion "high (20/20)" was an overclaim (A28 #16: frame-level evidence in 4 videos). Re-graded to medium via F-A02-101 (24 more videos at frame level, n = 46). Construction portion stays.
- F-A02-006: confirmed by 3B (burst-then-hold), evidence now frame-level in 26 videos instead of 4 shots; still medium.
- F-A02-007 (swap leads word by -3..+4 f): not upheld as a rule; F-A02-103 finds no caption-onset locking at all in 12 shots. Treat 007 as low and non-general; contradicting evidence is listed in F-A02-103.
- F-A02-008: "no lip-sync" upgraded from low-n observation to medium-low with a permutation test (n = 12 shots, 10 videos).
- F-A02-009: confirmed shape; interval still unresolved.
Overview-based catalogue statements (F-A02-002..005, 010) were NOT re-checked in 3B.
