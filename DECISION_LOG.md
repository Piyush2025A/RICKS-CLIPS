# DECISION LOG

Format: ID · date · decision · reasoning · status (proposed = awaiting user approval; accepted = user approved).

## D001 · 2026-11-27 · Reference repository is research material only
- Cloned `mromidev/claude-animated-shorts` at `e3b817b6afc6cd413466d43f11ba31209e034bbf` into the session scratchpad,
  outside the tracked project. No code, frames or contact sheets copied into this repo; nothing executed.
- Why: its code is MIT, but its `references/frames` and `references/sheets` are stills from a third-party channel
  ("for style study only"); no licence covers them, and our repository is public.
- Status: accepted (follows the user's Phase 1 instructions).

## D002 · 2026-11-27 · Upstream measured numbers are hypotheses, not facts
- The upstream reports contradict each other (e.g. STYLE_BIBLE "ease-out burst" camera grammar vs motion.md, which
  calls that finding wrong; LUFS −14 measured vs −15 mix target). Scores are self-assessed by its own verifier.
- Why: rule 2 (no unverified findings). Phase 3 re-measures from footage we are authorised to analyse.
- Status: accepted.

## D003 · 2026-11-27 · Google Flow is reached through the user's own browser, not from the cloud container (proposed)
- No official Flow API exists (no endpoint, key or SDK found). The container has no logged-in Google session and must
  not create one by extracting cookies or automating a login from a datacenter IP.
- Proposed primary path: **user-operated Flow → download → hand-off folder (Google Drive) → pipeline pulls via the
  Google Drive connector**, with a provenance manifest. Optional later: browser assistance on the user's own computer
  (Claude in Chrome / Remote Control) after a terms-of-service review.
- Rejected: third-party hosted wrappers that require our Google session cookies (e.g. useapi.net); unreviewed CDP
  browser MCPs that take over a logged-in Chrome profile.
- Status: proposed — needs user decision in Phase 4.

## D004 · 2026-11-27 · Google AI Pro does not pay for Gemini API calls
- Google's AI-plans doc and support replies state subscription benefits apply in the apps / AI Studio UI; API keys
  use separate Cloud billing. Any Nano Banana / Imagen API use is a separate paid decision.
- Status: accepted as a finding; any API use requires user approval (rule 10).

## D005 · 2026-11-27 · No dependencies installed in Phase 1; setup script proposed, not applied
- Proposed contents are in `research/technical-audit.md` §4. Status: proposed.

## D006 · 2026-11-27 · Development render spec
- 360p vertical (360×640), 24 fps for all development tests; reference analysis at native fps.
- Status: accepted (user rule 6 and 7).
