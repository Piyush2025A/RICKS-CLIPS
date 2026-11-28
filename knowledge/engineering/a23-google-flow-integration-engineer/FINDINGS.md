# A23 FINDINGS (evidence-backed only)
| ID | Finding | Label / conf | Evidence |
|---|---|---|---|
| F-a23-001 | Local Claude in Chrome generated and downloaded 1 Flow image (Nano Banana 2 Lite, 9:16, x1) with 0 credits (1050 -> 1050); PNG RGBA 768x1376, 2,206,600 B, sha256 bd4fac1d...a3a, `caBX` C2PA chunk 15,050 B preserved, visible watermark preserved. n = 1. | MEASURED / medium (n = 1) | private provenance JSON (2026-11-27), D015 |
| F-a23-002 | Prompt shape words were not obeyed (bean head, stick limbs, flat colour) in that image. n = 1. | OBSERVED / low-medium | provenance `visual_inspection` |
| F-a23-003 | Drive connector is byte-exact (25/25), limits: cloud -> Drive ~3.1 MB, Drive -> cloud 10 MB. | MEASURED / high | research/t5-drive-transfer.md, D022-D023 |
| F-a23-004 | Flow help states Agent media uses credits; direct images use daily per-model allowance. Whether Agent images consume credits is untested. | PUBLISHED, contradiction open | TERMS_REVIEW T16, integration-feasibility 1.3 |
| F-a23-005 | Terms: no fetched official page forbids supervised UI assistance; none grants explicit commercial rights for Flow images; SynthID "should not be tampered with or removed". | PUBLISHED / medium | TERMS_REVIEW.md |
