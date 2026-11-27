# A18 FAILED — Phase 3

## FA-a18-001 Blind hook re-code was not blind
The mandatory reading order (A19 FINDINGS before the task) exposed A19's labels for RC30-04, 09, 16, 23, 30 before
coding. Result kept (F-a18-001) but labelled not blind. Lesson: blind re-codes need a brief that withholds the other
coder's labels (director strips them or a coder who has not read them, e.g. A28). (Director note: the brief's reading
list caused this — a director error, not the agent's.)

## FA-a18-002 Sentence length cannot be read directly at 1 fps
Overview tiles show ≈ 35 % of caption tokens, so sentences cannot be reconstructed. Workaround: sentence-final
punctuation rate as an estimator (F-a18-003). Weak: small periods may be missed at 180×320; ±40 % per video.
Needs a full caption OCR timeline (A27/A20).

## FA-a18-003 No reproducible script
No Bash in this agent: counts are hand counts from the ledgered sheets (`data/caption_sample_counts.csv`), not
regenerable by command. Re-run with an OCR timeline when available.

## FA-a18-004 Deliverables refused by Write
The Write tool refused FINDINGS.md; files returned as text in the hand-off for the director to write verbatim.
