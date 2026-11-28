---
name: google-flow-supervised
description: Run a supervised, user-present Google Flow image generation through Claude in Chrome in the LOCAL Claude Code session, with per-request approval, credit checks, provenance capture and download to the private inbox. Use when the user asks to generate, download or intake an asset in Google Flow, run a Flow prompt pack, check Flow credits or daily image quota, or hand a Flow download to asset intake. Do NOT use in the cloud session, for unattended or looped generation, for Veo video, or for Flow Agent/Tools unless the user separately approves.
---

# Supervised Google Flow run (local session only)

Full procedure and rationale: `pipeline/flow/WORKFLOW.md`. Terms: `knowledge/engineering/a23-google-flow-integration-engineer/TERMS_REVIEW.md`.
Request format: `prompts/flow/REQUEST_SCHEMA.json`; templates in `prompts/flow/`.

## Step 0. Gate checks (stop and say why if any fails)
1. This is the local session with the `claude-in-chrome` tools available. If they are absent (cloud session), stop: prepare request files only.
2. The user is present and has, in this conversation, approved the batch (request IDs, model, count, credit ceiling). Past approval does not carry over.
3. Chrome shows Flow signed in by the user. Never enter passwords, 2FA codes or cookies; never open sign-in flows.
4. Request records validate; the prompt contains no confidential data, no reference characters or sets.

## Step 1. Per request (strictly sequential, human paced)
1. Show: request ID, mode, model, aspect ratio, output count, full prompt. Wait for the user's "approved <ID>".
2. Read and record BEFORE values: credits balance, the "Generating will use N credits" line, model daily counter if visible. If N exceeds the approved ceiling or cost is not shown, stop and ask.
3. Capture settings: mode, model, aspect, count, Flow Agent switch (must be OFF), reference ingredients, visible-watermark state.
4. Enter the prompt verbatim, click Generate once, record UTC time.
5. Wait without reloading. No retry for 60 s. No automatic regeneration; regenerate only as a new approved request.
6. View the result, note it matches the expected asset and list deviations from the request checklist.
7. Download via tile > More options > Download > "1K (Original size)"; the user confirms the browser prompt. No upscale unless the request lists it.
8. Read AFTER values; consumed = before - after.
9. Copy from the Chrome download folder to `~/ricks-clips-private/flow/inbox/<request_id>__<name>` (`cp`, then `sha256sum` both; keep the downloaded original in place — never delete or move it; the user may tidy the download folder). Do not open in editors, convert or resize.
10. Write `<file>.provenance.json` and one line in `~/ricks-clips-private/flow/quota_log.jsonl`.
11. Run A24 intake (see WORKFLOW section 2), then wait at least 10 s before the next request. Max 4 outputs per request, 10 requests per run.

## Provenance fields to capture (private JSON, never committed)
request_id, approved_by_user_utc, provider, access_method, account_plan_badge, flow_project (name; id and URL stay private),
prompt (verbatim), settings {mode, model, aspect_ratio, output_count, agent_switch, reference_ingredients, visible_watermark},
ui_cost_before, credits {before, after, consumed, reset_shown}, model_quota_counter {before, after, if visible},
submitted_utc, completed_utc, retries, captcha_or_safety_warning, download {menu_choice, browser_folder, moved_to},
file {name, format, dimensions, bytes, sha256, png_chunks incl. caBX size}, watermarks {visible, synthid_statement, c2pa_present},
visual_inspection {viewed_by, matches, deviations}, terms_note.

## Stop conditions (stop at once, report, wait for the user)
CAPTCHA or "unusual traffic"; sign-in/2FA/consent screen; safety or policy block (never reword to evade); daily-limit or
throttle message; credits consumed above the approved ceiling; unexpected UI (Agent panel, upgrade/payment prompts: never
click purchase or upgrade); extension disconnect or wrong tab; user says stop. After a stop, do not resume without a new approval.

## Never
Unattended or looped runs; CAPTCHA/anti-bot bypass; stealth; cookie or token extraction; account switching; watermark,
SynthID or C2PA removal or re-encoding before intake; third-party Flow MCP servers or extensions; Agent with
"Confirm before generating = Never"; committing media, provenance JSON, project IDs or URLs to the repo; using Flow
outputs to train ML models.

## Report back
Per request: ID, model, credits before/after, file name, sha256, dimensions, deviations, manual steps count (human actions),
intake status. Aggregate with n, median, IQR when 3 or more assets.
