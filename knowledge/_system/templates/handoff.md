<!-- Return message format, <= 250 words. Detail goes in files. -->
HANDOFF <agent-id> -> <director | agent-id>  (brief: <path>)
status: done | partial | blocked
changed_files: [paths]
outputs: [paths with one-line meaning]
evidence: [finding / experiment / frame-range IDs]
coverage: computational <records>, visual <records>
contradictions: [claim A vs claim B, evidence, which is stronger]
requests: [owner: what is needed and why]
open_questions: []
spend: none | <credits/time used, approval ref>
