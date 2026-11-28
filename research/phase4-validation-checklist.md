# Phase 4 — end-to-end verification checklist (Google Flow + ElevenLabs integration)
Created 2026-11-28 (D033 authorisation). An item is ✅ only with evidence recorded in `PROGRESS.md` (rule 3). Dev renders:
360 × 640, 24 fps. Private media never enters the repo (pre-commit guard `tools/git-hooks/pre-commit`).

## A. Flow prompt → generated asset (local session, Claude in Chrome, user present)
| # | Check | Pass criterion | Status |
|---|---|---|---|
| A1 | Supervised generation path works | Local session drives the user's signed-in Chrome; user approves the request; image appears in Flow | ✅ D015 (Nano Banana 2 Lite, 0 credits, 2026-11-27) |
| A2 | Credits recorded before/after | provenance `credits.before/after/consumed` filled from the Flow panel | ✅ D015 (1,050 → 1,050) |
| A3 | Standard request templates used | request record validates against `prompts/flow/REQUEST_SCHEMA.json`; template id stored in provenance | pending (A23 templates) |
| A4 | Download at original size | "1K Original size"; no upscale; file untouched before intake | ✅ D015 |
| A5 | Watermark + content credentials preserved | visible watermark present; PNG `caBX` (C2PA) chunk present after every step | ✅ D015 + A24 dry-run (chunk preserved) |
| A6 | Terms compliance | supervised use only; outputs labelled AI-generated where required; no automation loops | ✅ reviewed (A23); supervised runs within the existing allowance approved (D036); commercial terms still to be confirmed by the user |

## B. Asset intake and provenance (`pipeline/assets/`)
| # | Check | Pass criterion | Status |
|---|---|---|---|
| B1 | Intake copies byte-exact | `intake.py` copy SHA-256 = source SHA-256; source unchanged (size, mtime) | ✅ A24 dry-run on the lighthouse PNG (bd4fac1d…7a3a) |
| B2 | Technical facts | format, dimensions, bit depth, alpha stats, chunk list recorded | ✅ dry-run: RGBA 768×1376, alpha 100 % opaque, caBX 15,050 B |
| B3 | Naming + idempotency | `<kind>/<YYYYMMDD>_<request>_<slug>_v<NN>.<ext>`; re-intake detected | ✅ A24 tests 10/10 + dry-run |
| B4 | Sidecar + ledger | `*.provenance.json` valid against `pipeline/assets/schemas/asset-provenance.schema.json`; ledger line | ✅ A24 tests |
| B5 | Store re-verification | `verify.py --store` reports 0 problems | ✅ dry-run |
| B6 | Cut-out readiness | Flow PNGs are fully opaque → keyable-background prompt + background removal on intaken copies (originals unchanged, watermark/C2PA respected) | approved (D036); tool choice pending (local install or credits need approval) |

## C. Private local → cloud transfer (Google Drive, private folder `ricks-clips-handoff`, id `182jdqEbNrvk6TuidBaRBrK589XDgGYHu`)
| # | Check | Pass criterion | Status |
|---|---|---|---|
| C1 | Local → Drive upload of a real Flow asset | `create_file` (file reference, no conversion); Drive size = local size | ✅ 2026-11-28: lighthouse PNG, Drive id `1Z7A-w2CrTALkAxAWC2_yYTrvmJ9g6Ftz`, 2,206,600 B = local |
| C2 | Drive → cloud byte-exact | cloud session downloads into its filesystem; SHA-256 = bd4fac1d3593467ed7583b42146712b6ee7d8d622edcd1d8a9056ed3d62a7a3a; `caBX` chunk present | ✅ 2026-11-28 (D035, cloud session): SHA-256 match, 2,206,600 B, 768×1376 RGBA 8-bit, chunks IHDR + caBX 15,050 B + 268 IDAT + IEND, 0 CRC failures, no trailing bytes, full decode OK |
| C3 | Size limits respected | ≤ ~3.1 MB per upload from the cloud, ≤ 10 MB download into the cloud (D022); larger files processed locally | ✅ D022 (limits measured) |
| C4 | Privacy | folder not shared; no link sharing | ✅ created without sharing changes |

Cloud prompt for C2 (paste into the claude.ai/code cloud session on this repo branch):
> Using the Google Drive connector, download file id `1Z7A-w2CrTALkAxAWC2_yYTrvmJ9g6Ftz` (Lighthouse PNG, 2,206,600 bytes) into the session scratchpad (not the repo) the same way as the T5 test (`research/t5-drive-transfer.md`). Report its byte size and SHA-256 (expected `bd4fac1d3593467ed7583b42146712b6ee7d8d622edcd1d8a9056ed3d62a7a3a`), list its PNG chunks (expect `caBX` 15,050 bytes), do not open, convert or commit it, and append the result to `PROGRESS.md` Phase 4 (C2) with a commit.

## D. ElevenLabs narration and timestamps
| # | Check | Pass criterion | Status |
|---|---|---|---|
| D1 | Connector available and authenticated | read-only calls succeed | ✅ 2026-11-28 (`account_get_usage`, `creative_list_voices`, model schemas, guides) |
| D2 | Allowance known | plan, credits used/limit, voice slots | ✅ free tier, 5,011 / 10,000 credits used, voice slots 3/3 |
| D3 | Commercial terms | free tier = non-commercial + attribution; paid plan needed for commercial publishing | ✅ documented (ElevenLabs Help Center); **user decision pending** |
| D4 | Cost estimate for the 6-s test | `estimate_only` | ✅ 120 credits, 1 take, eleven_multilingual_v2 |
| D5 | Narration generated (original text, original voice, no cloning) | 1 take, ≈ 6 s, user-approved spend ≤ 150 credits | ✅ 2026-11-28: 1 take, 7.06 s, **136 credits** (counter 5,011 → 5,147), David voice, multilingual_v2 |
| D6 | Audio retrieved to private storage + intake | file in `~/ricks-clips-private/audio/`, intake `--kind audio`, SHA-256 recorded | ✅ signed `content_url` from the flow status, downloaded twice (identical SHA-256 63768ec7…927b), read-only, intaken + verified |
| D7 | ~~Word timestamps~~ → **sentence/story-beat timings** (D036: no Scribe) | `beats.json` from script + measured pauses; monotonic, within duration | ✅ 2 sentences, both edges measured; word timing optional/off |
| D8 | Captions | D036: rendered captions **disabled by default** (Canva Auto Captions post-render); `captions.py` kept and unit-tested for optional use | ✅ (decision recorded; tool tests pass) |
| D9 | Loudness | normalised VO −14 LUFS ±0.5, TP ≤ −2 dBTP, also after AAC | ✅ −14.2 / −2.8 (WAV); −14.3 / −2.2 (AAC) after a tool fix (linear-only gave −15.3) |
| D10 | Duration, silence, quality | measured and recorded | ✅ `productions/TEST6S/voice/TEST_RESULT.md` (pace 197 wpm < 220 target: note) |

## E. Readiness for Remotion / Three.js
| # | Check | Pass criterion | Status |
|---|---|---|---|
| E1 | Asset contract | images: sidecar + dimensions + alpha known; audio: provenance sidecar + `silence.json` + `beats.json` (words/captions optional) | ✅ lighthouse PNG + TEST6S audio |
| E2 | Media readiness at dev format | 360×640 / 24 fps clip from one intaken image + the normalised narration | ✅ FFmpeg readiness clip (169 f, 7.059 s, −14.3 LUFS, TP −2.2), frame viewed. **Remotion/Three.js import itself** needs the engine scaffold (`npm install`, A25) — next phase, not started |
| E3 | Three.js card | intaken image on a card plane with premultiplied alpha | not started (engine scaffold, next phase); cut-outs: background removal approved (D036), tool not yet chosen |
