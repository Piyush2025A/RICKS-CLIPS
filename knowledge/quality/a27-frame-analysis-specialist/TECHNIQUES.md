<!-- owner: A27 | format: knowledge/_system/templates/technique.md | only approved techniques; labels below are SYNTHETIC-VALIDATED, not approved by the director/A28 -->
## T-A27-001: Coverage v2 accounting with per-stage invariant  (rcpipe 0.2.0, synthetic-validated 2026-11-27, EXP-A27-20261127-02; not yet director-approved)
- **What:** every frame gets a class per stage (ok/uncertain/failed/missing); overall class = worst stage; ok+uncertain+failed+missing == expected overall and per stage is enforced by `rcpipe.schema.validate_coverage` on every emitted record.
- **Evidence (SYN only):** EXP-A27-20261127-02: 69 coverage records valid; 39 negative controls rejected; fault injection accounted exactly.
- **Known limits:** first frame of pair stages counted ok by convention; no real-footage validation.

## T-A27-002: Audio coverage with missing-interval complement  (rcpipe 0.2.0, synthetic-validated 2026-11-27)
- **What:** `ashowinfo` frame timestamps during decode give the covered intervals; missing = complement within [0, max(video, audio end)]; gaps zero-filled on the wav axis and flagged `valid=0`; decoder errors captured; undecodable audio recorded, never fatal.
- **Evidence (SYN only):** short audio, dropped frames, no stream, partly/fully corrupt AAC, AAC priming (EXP-02).
- **Known limits:** gap edges are decoder-frame granular (~20 ms); only a:0; real corruption modes beyond overwritten AAC payloads untested.

## T-A27-003: Exact native frame retrieval by frame ID  (rcpipe 0.2.0, synthetic-validated 2026-11-27)
- **What:** `analysis/get_frames.py` re-decodes natively (passthrough, no scaling), writes lossless PNG + JSON sidecar (index, pts, sha256 of raw BGR, input sha256, native dims) and can cross-check against an independent ffmpeg `select=eq(n,i)` decode.
- **Evidence (SYN only):** bit-exact for CFR and VFR clips after a proxy run; barcode == index. **Limits:** decode-index identity only; no seeking optimisation (decodes up to the highest requested index).

## T-A27-004: Second-motion flag for camera estimates  (rcpipe 0.2.0, synthetic-validated 2026-11-27)
- **What:** second RANSAC on the primary outliers -> `tx2,ty2,n_inliers2`, status `ok:second_motion`, confidence medium. **Evidence:** parallax clip 90-100% flagged, rigid-pan accuracy kept (<= 0.06 px) down to CRF 45. **Limits:** cannot distinguish parallax from an independent object; thresholds (8 inliers, 0.5 px) set once, no hold-out.
