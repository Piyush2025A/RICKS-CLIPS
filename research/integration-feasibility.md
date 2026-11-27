# Integration feasibility — Google Flow and ElevenLabs (Phase 1, 2026-11-27)

Desk research only. Nothing was authenticated, installed or generated. Sources are listed at the end; third-party
claims are marked as such.

## 1. Google Flow

### 1.1 Official integration possibilities
- **No official Flow API found.** Flow is a web app at labs.google (also mobile). Multiple sources report no endpoint,
  key or SDK; developers are pointed to the Gemini API / Vertex AI instead. (Confidence: medium-high; absence of
  evidence, consistent across sources, no Google page contradicts it.)
- **Official export paths:** in-app download of images/videos; Google Takeout export of Flow data (Google Help).
- Flow's default image model is **Nano Banana Pro**; aspect ratio, output count and model are selectable (Google Help).
- All Flow outputs carry an invisible **SynthID** watermark; a visible watermark is a user toggle for images, and
  Pro-tier videos carry a visible Veo watermark (Flow FAQ). Google does not claim ownership of generated content.
- Reported AI Pro allowance: ~1,000 Flow credits/month (third-party; verify in the user's account).

### 1.2 Is local browser assistance required?
**Yes, for any Flow automation.** Flow requires the user's interactive Google login. The only allowance-funded path
is a human (or a browser assistant acting on the user's own computer, in the user's own logged-in browser).

### 1.3 Cloud environment limitations
- The container has no logged-in Google session. Creating one would mean logging in from a datacenter IP (likely to
  trip Google's anti-abuse checks) or importing cookies/session tokens — **both prohibited by our rules**.
- Therefore the cloud container **cannot drive Flow directly**. It can receive Flow outputs via a hand-off channel.
- The session has a **Google Drive connector**, which can read files the user places in Drive — a clean hand-off.
- The platform supports attaching the user's own computer (Remote Control) — a possible route for browser
  assistance, subject to user approval and ToS review.

### 1.4 MCP approaches and security risks
| Option | How it works | Risk | Verdict |
|---|---|---|---|
| Community CDP/browser MCPs (e.g. `GTAI-1/flow-mcp`, `google-flow-browser-mcp`, `gflow-cli`, others) | Local server drives a logged-in Chrome via DevTools Protocol | Full control of a Google-logged-in browser (Gmail, Drive, payments); unreviewed code; alpha, breaks on UI changes; ToS unclear | **Do not install.** Possible later only after source review, pinned commit, dedicated Chrome profile, ToS check, user approval |
| useapi.net hosted Flow API/MCP | Third party drives *your* Flow account; paid ($15/mo reported) | Requires handing over Google session credentials to a third party | **Rejected** (violates "no session token extraction", adds paid service) |
| Claude in Chrome / computer use on user's machine | Claude operates the visible Flow UI in the user's browser with the user present | Lower (official Anthropic tooling, user-visible), but still automation of a Google UI — ToS unknown | Candidate for Phase 4 pilot, after ToS review |
| Manual Flow + Drive hand-off | User generates and downloads; drops files into a shared Drive folder; we pull via Drive connector | Minimal | **Recommended first path** |

### 1.5 Asset download and transfer workflow (proposed)
1. We generate prompt packs (`prompts/<asset-id>.md`: prompt, model, aspect ratio, seed/variation notes).
2. User runs them in Flow (AI Pro allowance), downloads originals at full resolution, uses filename `<asset-id>_vN.png`.
3. User places files in a Drive folder, e.g. `RicksClips/flow-inbox/`.
4. Pipeline pulls via the Google Drive connector into git-ignored `assets/flow-inbox/`, records a manifest
   (asset id, prompt hash, model, Flow project, download date, SHA-256, dimensions, SynthID note).
5. Asset processing (A24): background removal, part separation, upscaling where needed, normalisation.
6. Only approved, original assets ever leave git-ignored storage; publishing decisions are recorded.
End-to-end verification (Phase 4): checksum match Drive ↔ local, dimensions as downloaded, image visually viewed.

### 1.6 Separate API billing implications
- **Google AI Pro does not cover Gemini API usage.** Subscription benefits apply in the apps / AI Studio UI; API keys
  bill separately through Cloud Billing (Google AI-plans doc; Google support replies on the developer forum).
- Programmatic Nano Banana / Imagen / Veo = **separately billed**; per-image prices must be read from Google's pricing
  page (a third-party figure of ~$0.02/image is unverified). Developer-program Cloud credits may apply — unverified.
- Any API route needs explicit approval (rule 10). It would, however, be the only fully automatable cloud path.

### 1.7 Open questions for the user
1. Approve the manual Flow → Drive hand-off as the Phase 4 baseline?
2. Is browser assistance on your own computer acceptable for a later pilot (after a ToS review)?
3. Would separately billed Gemini API image generation ever be acceptable as a fallback, and with what budget?
4. Commercial-use terms for Flow outputs must be read in Google's current ToS / Generative AI terms before publishing.

## 2. ElevenLabs

- **API:** `POST /v1/text-to-speech/{voice_id}/with-timestamps` returns audio (base64) plus character-level
  `alignment` (start/end seconds) — directly usable for word timing, replacing a separate STT step (ElevenLabs docs).
- **Billing:** usage-based, priced per 1K characters / credits; exact cost for the timestamp endpoint vs plain TTS not
  confirmed — measure with one short approved test and record credit deltas.
- **Credentials:** no ElevenLabs key in the environment. Recommended: store it as an environment **network secret**
  (injected by the proxy for `api.elevenlabs.io`), never in `.env` committed files or chat.
- **Connector:** this session also has a claude.ai ElevenLabs connector (speech generation tools). Untested; it spends
  credits on the user's account; voice and model choice need approval.
- **Licensing:** commercial use rights depend on the ElevenLabs plan tier — confirm the user's plan before publishing.
- Feasibility: **high**; blockers are only the credential and approval.

## 3. Summary of blockers
| Blocker | Owner | Unblocks |
|---|---|---|
| No official Flow API; cloud cannot log in | Architecture (accept hand-off) | Phase 4 Flow path |
| Flow ToS on automation and commercial use unread | User + A23 | Browser-assistance pilot, publishing |
| ElevenLabs key not configured | User (environment secret) | Phase 4 TTS test |
| Credit-spend approval | User | Any generation |

## Sources
- Google Flow Help — Create & edit images: https://support.google.com/labs/answer/16729550
- Google Flow Help — Download your Flow data: https://support.google.com/flow/answer/17571126
- Google Flow FAQ: https://labs.google/fx/tools/flow/faq
- Google AI plans in AI Studio: https://ai.google.dev/gemini-api/docs/google-ai-plans
- Developer forum, Pro subscription vs API quota: https://discuss.ai.google.dev/t/pro-subscription-gemini-advanced-vs-api-quota-0-resource-exhausted/113011
- Third-party: "There is no official Flow API": https://www.wireflow.ai/blog/google-flow-api
- Third-party: Flow pricing/credits: https://costgoat.com/pricing/google-flow
- Third-party wrapper (rejected): https://useapi.net/docs/api-google-flow-v1
- Community MCPs (not reviewed): https://github.com/GTAI-1/flow-mcp/wiki · https://github.com/Mitanshp5/Google-Flow_MCP · https://mcpservers.org/servers/ffroliva/gflow-cli
- ElevenLabs TTS with timestamps: https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
