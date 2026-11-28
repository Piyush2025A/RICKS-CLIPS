# Supervised Google Flow generation run (A23, v1, 2026-11-28)

Scope: image generation in the Flow web UI, driven by the LOCAL Claude Code session through the official Claude in Chrome
extension in the user's own signed-in Chrome, **user present, one approved request at a time**. Verified once (D015,
n = 1). Terms position: `knowledge/engineering/a23-google-flow-integration-engineer/TERMS_REVIEW.md` (supervised = grey,
leaning permitted; unattended = do not). The Claude skill that executes this is `.claude/skills/google-flow-supervised/SKILL.md`.
The cloud session never touches Flow or Chrome (D014); it only prepares request files and receives text/small files.

## Roles
| Who | Does |
|---|---|
| Cloud/director session | writes request records (`prompts/flow/REQUEST_SCHEMA.json`), commits text only |
| User | approves each request, is present and watching, confirms the browser download, reads credit/limit counters if the page is not readable by the assistant |
| Local session + Claude in Chrome | fills prompt, sets options, clicks Generate only after approval, downloads, moves file, runs A24 intake |
| A24 `pipeline/assets/intake.py` | checksum, dimensions, alpha, naming, provenance ledger in the private store |

## 0. Preconditions (all must hold; otherwise stop)
1. User message in the current session explicitly approves this batch: request IDs, model, count, and credit/quota ceiling.
2. User is at the computer; Chrome is visible; Flow is signed in by the user (assistant never types credentials or opens login).
3. Request records exist and passed `python3 -m json.tool` / schema check; prompts contain no confidential data (TERMS_REVIEW privacy note) and no reference characters/sets (originality).
4. Private dirs exist: `~/ricks-clips-private/flow/inbox/` (downloads land here), `~/ricks-clips-private/assets/` (A24 store).
5. Chrome download folder known (D015: `~/Desktop`); file will be moved by checksum-verified copy.

## 1. Per request (loop is human-paced, never automatic)
1. **Show the request** to the user: ID, mode, model, aspect, count, prompt text. Wait for "approved: <ID>".
2. **Credit and quota check BEFORE**: read the Flow credits balance and the on-screen cost line ("Generating will use N credits"). Record both. If N > approved ceiling or cost is not shown: stop and ask. Image generation is expected to be 0 credits (D015); video or Agent-made media is not covered by this workflow.
3. **Capture settings** (screenshot/text of the settings chip): mode, model, aspect ratio, output count, Flow Agent switch (must be off), reference ingredients (none unless the request lists them), visible watermarking state.
4. Paste prompt exactly from the request file; no edits. Click Generate once. Record UTC time before clicking.
5. **Wait** for completion without refreshing; no retry for 60 s. On CAPTCHA, sign-in, safety or "try again later" prompts: stop (section 4).
6. **Look at the result** (it is a viewing, log it): the tile is the expected asset; note deviations against the request checklist. Do not auto-regenerate; a regeneration is a new request needing new approval.
7. **Download at original size**: tile > More options > Download > "1K (Original size)" (D015 menu). Do not choose upscale unless the request says so (upscales have their own daily limit). The user confirms the browser download prompt.
8. **Credit and quota check AFTER**: read balance again; consumed = before - after. Record.
9. **Move, do not re-encode**: from the Chrome download folder to `~/ricks-clips-private/flow/inbox/<request_id>__<original_filename>` using `cp` then `sha256sum` compare, then remove the original only after the match. Never open in an editor, convert, resize, or strip metadata.
10. Write the provenance JSON next to it (`<file>.provenance.json`, fields in the skill) and append one line to `~/ricks-clips-private/flow/quota_log.jsonl` (date UTC, model, images generated, credits before/after).
11. Pause >= 10 s between requests (INFERRED safe pace; the page warns about "very rapid generations"). Batches of at most 4 outputs per request, at most 10 requests per run, unless the user says otherwise.

## 2. Hand-off to A24 intake
```
.venv-analysis/bin/python -I pipeline/assets/intake.py ~/ricks-clips-private/flow/inbox/<file> \
  --kind <character|expression|parts|prop|texture|environment> --request-id <ID> --provider "Google Flow" \
  --model "<model>" --prompt-file <prompt.txt> --settings-json <settings.json> --credits <consumed> \
  --visible-watermark yes --synthid yes --terms-note "<TERMS_REVIEW ref>" --generated-utc <t> --downloaded-utc <t>
```
Intake is byte-exact and idempotent by SHA-256 (A24 owns it; flags per its `--help`). Intake refuses > 50 MB. If A24's CLI
changes, A24's documentation wins. A24 decisions about alpha/cut-out (derived assets) are recorded as derived, never
overwriting the original. `--visible-watermark yes` is the expected value for this user's region (locked on).

## 3. Hand-off to the cloud (only if the cloud needs the pixels)
- Default: pixels stay local; the cloud receives only the manifest/ledger text (git).
- File <= 3 MB: user uploads it in the browser to the private Drive folder (or the local session does, if a Drive connector is available there); the cloud downloads with the Drive connector (limit 10 MB per file into cloud; T5, D023). Cloud re-hashes and compares to the ledger SHA-256.
- File 3-10 MB: same path works into the cloud (10 MB limit); out of the cloud it does not (3.1 MB), irrelevant for Flow assets.
- File > 10 MB (2K/4K upscales, video): local processing only, or a <= 3 MB preview.
- Never commit media; never put the Drive folder ID, file IDs or links in the repo if the folder is shared.

## 4. Failure handling
| Event | Action |
|---|---|
| CAPTCHA, unusual-traffic page, sign-in or 2FA request | stop the run; user handles it themselves; do not resume without new approval; do not try again for >= 1 h |
| Safety block / policy warning | log, do not reword to evade; failed or blocked generations do not count toward the limit (16729550) but repeated attempts at evasion violate the Prohibited Use Policy 2.3; ask the user |
| Daily limit message / throttling | stop; record time; the limit is a rolling 24 h from the first generation of that model |
| Generation stuck > 90 s | one page-state read, no reload; ask the user |
| Credits changed unexpectedly (consumed > approved) | stop, screenshot the balance, tell the user |
| Download missing or checksum mismatch after move | keep both copies, record in `FAILED.md`, do not delete |
| Extension disconnected / wrong tab | stop; do not switch to another browser profile |
| Result off-brief | log deviation; propose a revised request; wait for approval |

## 5. Never
- No unattended loops, schedulers, headless or background browsers; the user must be present.
- No CAPTCHA/anti-bot bypass, no stealth or automation masking, no cookie/token extraction, no account switching to escape limits.
- No watermark, SynthID or C2PA removal or alteration; no re-encoding, resizing, recompressing or metadata stripping before intake.
- No third-party Flow MCP servers/extensions (D013), no unofficial endpoints, no passwords typed by the assistant.
- No generation without the user's approval of that exact request; no Agent "Confirm before generating = Never".
- No confidential or personal data in prompts or uploads; no reference-character names or reference-video frames as prompts or references.
- No use of Flow outputs to train or fine-tune ML models (Google ToS).
- No media, provenance JSON, project IDs or URLs in the public repo (the D015 record stays under `~/ricks-clips-private/`).

## 6. Measurements (A23 schema)
`manual_steps` per asset (expected: approve 1, download confirm 1, plus any reads), `intake_success`, `checksum_match`,
`quota_used` per model per day. Log n, median, IQR, request IDs, script version, exclusions. Reproducible from
`quota_log.jsonl` and the A24 ledger.
