# FINDINGS — A24 asset processing engineer

## F-a24-001: Lighthouse Flow PNG has an alpha channel that is fully opaque (2026-11-28)
- **Claim:** `Lighthouse_keeper_standing_on_pier_5e7acb04.png` (SHA-256 bd4fac1d…7a3a, 2,206,600 B, 768x1376, RGBA 8-bit, non-interlaced) has alpha min = max = 255: 100.0 % opaque, 0 % transparent, 0 % semi-transparent, bbox = full frame. `MEASURED`, confidence high.
- **Method:** `pipeline/assets/intake.py` (script v1.0.0) on the file, n = 1 asset, 1,056,768 pixels, no exclusions (watermark region included). Reproduce: `.venv-analysis/bin/python -I pipeline/assets/intake.py <file> --kind character --request-id X --store <tmp>`.
- **Implication:** Flow "Image" output is a flat, background-included picture; RGBA is nominal. Cut-outs/character layers need matting or a background-removal step (new method = director approval + licence check), or generation on a keyable flat background. `INFERRED` from one asset (low-medium confidence for other models/modes).

## F-a24-002: Chunk structure and byte-exact intake (2026-11-28)
- PNG chunks: IHDR(13), caBX(15,050 B, C2PA carrier), IDAT x268 (2,188,277 B), IEND; all CRCs valid; no tEXt/iTXt/zTXt/eXIf; no ICC profile, no XMP. `MEASURED`, high. Matches A-record in the private provenance file.
- Intake copy to `_intake_test` store is byte-identical (`cmp`, SHA-256), original size and mtime unchanged; re-intake detected as duplicate; `verify.py` reports 0 problems. `MEASURED`, high.
- Not verified: C2PA manifest validity/signature, SynthID (no tooling; gap).

## Tests
10 unittest cases (synthetic RGBA/RGB/JPEG/fake caBX, idempotency, refusals, tamper detection, schema subset check) pass. pytest/jsonschema are not installed in `.venv-analysis`; tests use unittest and a minimal schema-subset validator.
