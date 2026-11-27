# A02 FINDINGS — facial expression system (Phase 3, RC30)

Manifest SHA-256 `fc6f147abae5a83252de6f9a832cbf524d8ee87e946e25a2915a966fc8278e06` | date 2026-11-28 | visual ledger
`knowledge/dataset/coverage/visual/a02-facial-expression-specialist.jsonl` = 29 records (29 images opened).
Videos with catalogue evidence (1 fps overview, first ~40 s): RC30-01,02,03,05,07,09,10,12,13,15,16,18,19,21,22,25,26,27,28,30
(**20 of 30**). Every-frame face strips (native frames, private): RC30-03 f830-877, RC30-25 f0-95, RC30-27 f100-195,
RC30-30 f30-125 (+f560-607). Builds on F-a01-008; not repeated. Overview tiles are 1 frame/second, so rare states are
under-sampled; counts below are "seen", not frequencies.

Limits: second halves of videos were not viewed; timing n is tiny (4 shots) -> every timing claim is low/medium confidence.
Audio: caption-vs-audio alignment could not be established (see FAILED.md F-A02-X1), so "word onset" = burned-in caption change.

## F-A02-001 Face grammar is one construction with swappable parts (eyes x brows x mouth x accessories)
OBSERVED, high (20/20 videos). Head = white/skin circle with ink outline; every state is a hard-cut swap of drawn parts,
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
