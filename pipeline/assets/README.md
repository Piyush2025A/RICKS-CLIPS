# pipeline/assets — asset intake and verification (A24)

Intake step after a download (e.g. Google Flow). Originals are copied **byte-exact** into the private store; they are never
modified, re-encoded, cropped or metadata-stripped (visible watermark, C2PA `caBX`, SynthID are preserved).
Stdlib + Pillow + numpy (+ soundfile for audio). Always run with `.venv-analysis/bin/python -I`.

## Usage
```
intake.py <file> --kind character|expression|parts|prop|texture|environment|audio|other --request-id <id> \
  [--provider google-flow --model "..." --prompt-file P.txt --settings-json '{...}' --credits 0] \
  [--generated-utc ... --downloaded-utc ... --event 'transferred_via_drive|<utc>|detail'] \
  [--visible-watermark yes|no|unknown --terms-note "..."] [--store DIR] [--force-type]
verify.py --store DIR [--record]                      # re-hash store vs sidecars + ledger; exit 1 on problems
verify.py --check FILE --expect-sha256 HEX            # Drive round-trip: downloaded file vs known hash
```
Default store: `~/ricks-clips-private/assets`. Tests: `.venv-analysis/bin/python -I -m unittest discover -s pipeline/assets/tests`.

## Naming
`<kind>/<YYYYMMDD>_<request-id>_<slug>_v<NN>.<ext>` (UTC date; slug from filename, Flow's trailing 8-hex id dropped;
NN = next free version). Sidecar `<name>.provenance.json` (schema: `schemas/asset-provenance.schema.json`);
ledger `INTAKE_LEDGER.jsonl` (append-only). Re-intake of identical bytes (SHA-256) is a no-op reporting the existing path.

## What is checked
SHA-256, size, true format (magic bytes, not extension), dimensions, mode, bit depth, ICC/EXIF/XMP presence, alpha
statistics (fractions transparent/semi/opaque, non-zero bbox), PNG chunk list with CRC check (C2PA `caBX`, text chunks),
audio rate/channels/duration. Copy hash is verified; on mismatch the copy is deleted and exit code is 3.
Refused: >50 MB; non-image/non-audio unless `--force-type`.

## Privacy
Store, sidecars (contain prompts) and ledger live **outside the repo**. Never commit media, sidecars or provenance records
with account data. Operators pass only non-personal fields to the sidecar; the Flow account/project record stays separate.
Gap: no C2PA manifest validation (only chunk presence); no SynthID check.
