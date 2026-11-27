# Phase 3 execution plan — RC30 exhaustive reference analysis (prepared 2026-11-27, awaiting approval)

Status: **plan only.** No footage acquired, no dataset frozen, no specialist analysis started. Rules: `CLAUDE.md`
(RC30 rule, rules 2/9/12/13/14), `knowledge/dataset/README.md`, `knowledge/_system/EVIDENCE.md`,
`knowledge/_system/ORCHESTRATION.md` §3–7, `MASTER_PLAN.md` Phase 3.

## 0. Baseline carried into Phase 3
- **Analysis code frozen:** `rcpipe` v0.2.0 (`analysis/`), 318/318 synthetic checks (D018), environment
  `setup/setup-analysis.sh --with-audio` (D016). Changes allowed in Phase 3 only for real-footage calibration, as a
  new version with the full suite re-run, failures logged and a decision-log entry.
- **Transfer layer:** Google Drive connector, private folders, byte-exact; per-file limits verified in T5 (D023):
  cloud → Drive ≤ ~3.1 MB, Drive → cloud ≤ 10 MB. Report: `research/t5-drive-transfer.md`.

## 1. Rule review (RC30) — consistent across CLAUDE.md, MASTER_PLAN.md, dataset README, EVIDENCE.md, schemas
- Exactly the 30 most recently **published** Shorts of https://www.youtube.com/@RicksClips3000, by publication date
  (not popularity), determined once and frozen in `knowledge/dataset/MANIFEST.json` (schema enforces 30 items,
  keys `RC30-01` newest … `RC30-30` oldest).
- No older Shorts, no substitutes; unavailable → recorded `unavailable`, analysis reports n < 30.
- Footage only via a user-authorised method; stored privately; never committed (video, frames, crops, sheets).
- Every native frame processed computationally; computational and visual coverage kept separate.
- Picture and sound analysed (narration, SFX, music, editing, sync). Upstream reports are `H-UP` only.
- Gap found: no rule yet for *where derived per-frame tables live* (they are numbers, not media, but large).
  Proposed in §5.

## 2. Step P3.1 — identify the latest 30 Shorts (metadata only, no media)
Method (official API, read-only, ~5 quota units of the default 10,000/day):
1. `channels.list` (`forHandle=RicksClips3000`, `part=contentDetails`) → uploads playlist ID.
2. `playlistItems.list` over the uploads playlist, newest first, using `contentDetails.videoPublishedAt`
   (= publication date; `snippet.publishedAt` there is the playlist-add time and is **not** used).
3. `videos.list` (`part=snippet,contentDetails,status`) for `snippet.publishedAt`, `contentDetails.duration`, title.
4. **Shorts identification:** the API has no official Shorts field (verified on the docs read). Candidates = uploads
   with duration ≤ 180 s (current Shorts maximum — INFERRED, verify at freeze time). Because a ≤ 180 s upload is not
   necessarily a Short, the **user confirms the list against the channel's Shorts tab** in a browser (manual,
   no automation of youtube.com). Disagreements are resolved by the user and recorded.
5. Take the 30 newest confirmed Shorts by `videos.snippet.publishedAt`; write `MANIFEST.json` (schema-validated),
   record `frozen_at`, SHA-256 of the manifest, `metadata_source: "YouTube Data API v3 + user Shorts-tab check"`.
Credential: a YouTube Data API key (Google Cloud project, API restricted to YouTube Data API v3), stored as an
environment network secret via the secure form (header `X-Goog-Api-Key`) — never in chat or files. Cost: no charge
was found in the docs read and no billing is needed for the default quota (INFERRED; the docs do not state pricing).
Rejected: scraping youtube.com pages (ToS automated-access clause), third-party channel tools (unreviewed, may use
credits).

## 3. Step P3.2 — authorised footage acquisition (USER DECISION REQUIRED)
YouTube Terms of Service (read 2026-11-27) prohibit downloading Content "except: (a) as expressly authorized by the
Service; or (b) with prior written permission from YouTube and, if applicable, the respective rights holders", and
prohibit circumventing copy-restriction features. YouTube's offline feature keeps videos inside the app (48 h; no
export documented). Ranked options:

| # | Method | Quality / native fps | ToS / authorisation | Verdict |
|---|---|---|---|---|
| A | **Creator supplies files** (or written permission naming the 30 videos) after a request from the user | Best: original masters or exact uploads, native fps | Clean if the rights holder grants it in writing; outside YouTube's download prohibition when files come from the creator directly | **Recommended** |
| B | Ask YouTube/rights holder for written permission to download from YouTube | YouTube's best stream (re-encoded) | Compliant once both permissions exist; slow/uncertain | Possible |
| C | Download tools (e.g. yt-dlp) without permission | Re-encoded YouTube streams, native fps | Conflicts with the ToS clauses above; anti-bot measures (CLAUDE.md rule 13) | **Not recommended; not something I will run without a documented authorisation** |
| D | Screen recording of playback | Lossy, capture jitter, not native frames | Still "reproduce"; fails the every-native-frame requirement technically | Rejected |
Legal questions (e.g. research or fair-use exceptions in the user's jurisdiction) are the user's to decide; this plan
does not assume any. If no authorised method is available for a video, it is recorded `unavailable` (no substitute).

## 4. Step P3.3 — ingestion (files > 10 MB)
Footage arrives on the user's computer (option A/B). Recommended path, within verified limits:
1. User: place files in `~/ricks-clips-private/rc30/` (outside any repo), run one provided script that writes
   `SHA256SUMS`, splits each file into ≤ 9,000,000-byte parts (`split -b 9000000 -d`), and writes a per-file parts
   manifest (part names, sizes, SHA-256).
2. User uploads the parts + manifests to a new private Drive folder `rc30-private` (browser; no sharing).
3. Cloud: downloads each part (≤ 10 MB, verified limit), verifies each part, reassembles, verifies the whole-file
   SHA-256 against `SHA256SUMS`, then runs ffprobe. Any mismatch → stop and re-request that file.
Estimate: a 60 s 1080p Short is typically 10–40 MB (INFERRED) → 2–5 parts; 30 Shorts ≈ 60–150 downloads at ~1–2 s each.
The container is ephemeral: re-ingest from Drive in a new session if needed (the Drive copy is the private master).
Alternative (if transfer is too slow): run `rcpipe` on the user's computer and upload only text outputs; requires a
local Python environment (lock is CPython 3.13/x86_64; Linux Mint may ship another version → re-lock needed).

## 5. Storage and documentation rules for Phase 3 outputs
| Output | Where | Committed? |
|---|---|---|
| Source files, frames, crops, contact sheets, overlays | Drive `rc30-private` / scratchpad / git-ignored `private/` | **Never** |
| Per-frame tables (CSV/JSONL, numbers only) | Drive `rc30-derived` (zipped, ≤ 3 MB parts) + scratchpad | No (size); SHA-256 of each table committed |
| Computational coverage (`coverage/computational/*.jsonl`) | `knowledge/dataset/coverage/computational/` | Yes |
| Visual inspection ledgers (`coverage/visual/<agent>.jsonl`) | `knowledge/dataset/coverage/visual/` | Yes |
| Measurement records (aggregates, per-video values, frame-ID evidence) | each specialist's knowledge folder | Yes |
| Findings, techniques, failed approaches, limitations | each specialist's knowledge folder (`FINDINGS.md`, `TECHNIQUES.md`, `FAILED.md`) | Yes |
| `MANIFEST.json` (metadata only, no media) | `knowledge/dataset/` | Yes |
Every finding cites `manifest_sha256`, frame-ID evidence, method, confidence and limitations (EVIDENCE.md).

## 6. Step P3.4 — specialist execution order (ORCHESTRATION §4, max 2 concurrent)
| Wave | Agents | Depends on | Deliverables |
|---|---|---|---|
| 0 | Director | user actions | `MANIFEST.json` frozen; ingestion verified (sha256 + ffprobe per file) |
| 1 | **A27 alone** | wave 0 | real-footage calibration (rcpipe 0.3.0 if thresholds change; full suite re-run); frame index; shared per-frame tables; computational coverage 100% or every missing frame listed; contact sheets (private) |
| 2 | A20 ∥ A15 | A27 tables, audio | transcripts + word timings, speech rate/pauses/loudness; transition catalogue with exact frames |
| 3 | A13 ∥ A16 | A27 motion, A15 | camera trajectories/easing (camera vs character labelled); shot-length distribution, beat-to-shot map |
| 4 | A14 ∥ A07 | A13 | framing/safe zones; depth, parallax, DOF |
| 5 | A09 ∥ A11 | A27 colour tables | lighting/shadow model; tone/colour grade statistics |
| 6 | A10 ∥ A08 | A27 edge tables | outline width/colour behaviour; textures/materials |
| 7 | A01 ∥ A03, then A02 ∥ A04 | visual inspection | character identity, proportions, expressions, body motion |
| 8 | A05 ∥ A06; A12 ∥ A21; A22 ∥ A19; A17 ∥ A18 | earlier waves | world/layering; VFX/SFX; music-mix/hooks; topics/script structure |
| 9 | A28 | all findings | independent evidence-quality audit of a sample (does not grade own work) |
| 10 | Director | A28 | synthesis: measured style specification + open questions; Phase 3 gate report |
Each specialist: brief by file paths; reads shared tables instead of re-measuring; logs every viewed image in its
visual ledger (image kind, frames, view resolution, purpose); separates MEASURED / OBSERVED / INFERRED /
HYPOTHESIS / H-UP. Agents other than A23/A27 are unverified by invocation; each is checked on its first brief.

## 7. Coverage honesty
- Computational: per video, ok + uncertain + failed + missing = expected frames, per stage (schema v2 invariant);
  30 fps must reach 100% processed or list each missing frame with a reason. Audio: analysed vs total duration.
- Visual: only images actually opened by an agent count; contact-sheet views record the per-frame view resolution
  (a 108×192 thumbnail is not a native-resolution inspection). Expect visual coverage ≪ 100%; it is reported as is.
- Proxy-resolution measurements (motion, shots) are labelled proxy; native frames are retrieved by ID for detail.

## 8. Remaining Phase 2.5 / Phase 4 items (do not block Phase 3)
- Flow: user decisions §1A.9; T4 (Agent/Tools credit discrepancy); Labs.google/Flow ToS on automation unread;
  batch test T7.
- ElevenLabs: key/connector test (Phase 4).
- Cloud environment: optional saved setup script (re-run manually ~15 s until then).
- Drive: T5 test files still in `ricks-clips-t5` (user may trash; 2 browser-uploaded files only the user can remove).
- Large final-render transfer: deferred (D024).
- 27 agents still unverified by invocation (verified on first use).
