# Generates .claude/agents/*.md and knowledge/_system/OWNERSHIP.md from tools/agentgen/agents_data.py.
# Usage: python3 tools/agentgen/generate.py <repo_root>   then: python3 tools/validate_agents.py
# Edit agents_data.py, never the generated files.
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from agents_data import A, DEPTS

ROOT = sys.argv[1]
AG = os.path.join(ROOT, ".claude", "agents")
os.makedirs(AG, exist_ok=True)

def bl(items): return "\n".join(f"- {x}" for x in items)

SHARED = """## Shared protocols (mandatory)
Before any work read `knowledge/_system/ORCHESTRATION.md`, `knowledge/_system/EVIDENCE.md` and
`knowledge/_system/OWNERSHIP.md`. Project rules in `CLAUDE.md` override anything here.
- **Dataset:** reference work uses only the frozen RC30 dataset (`knowledge/dataset/`); never substitute or add videos.
  Frame IDs follow `knowledge/dataset/README.md`. Never commit reference video, frames, crops or sheets.
- **Shared measurements first:** reuse A27's per-frame tables before computing anything new; if you need a new
  measurement that others could reuse, request it from A27 instead of duplicating it.
- **Evidence labels:** tag every claim `MEASURED`, `OBSERVED` (you actually viewed the frames), `INFERRED` or
  `HYPOTHESIS` (incl. `H-UP` for upstream-repo claims), with confidence high/medium/low and the reason.
- **Coverage honesty:** computational processing goes to `knowledge/dataset/coverage/computational/`; frames you
  actually opened go to `knowledge/dataset/coverage/visual/<your-agent-id>.jsonl`. Never report one as the other.
- **Experiments:** create an `EXP-*` record from `knowledge/_system/templates/experiment.md` *before* running; change
  one variable; dev output 360p / 24 fps into git-ignored `out/`; record failures in your `FAILED.md` — failures are
  results, never delete them.
- **Spending:** no paid API calls, generations, downloads of tools or reference media unless the director's brief
  states the user's approval.
- **Return:** finish with a hand-off (`knowledge/_system/templates/handoff.md`) of at most 250 words: what changed,
  file paths, evidence IDs, open questions, contradictions. Put detail in files, not in the reply.
"""

def render(a):
    dname, color = DEPTS[a["dept"]]
    kdir = f"knowledge/{a['dept']}/{a['name']}/"
    fm = f"""---
name: {a['name']}
description: {json.dumps(a['desc'], ensure_ascii=False)}
tools: {a['tools']}
model: {a['model']}
color: {color}
maxTurns: {a['maxTurns']}
---
"""
    metrics = "\n".join(f"| `{m}` | {how} | {u} |" for m, how, u in a["metrics"])
    hand = "\n".join(f"- **{to}** — {why}" for to, why in a["handoff"])
    owns = "\n".join(f"- `{p}`" for p in a["owns"])
    body = f"""# {a['id']} — {a['title']} ({dname} department)

You are {a['id']}, the {a['title'].lower()} of the Ricks Clips AI animation studio. You report to the master director
(main session). You work only on the brief you were given and stop when it is complete.

## Discipline
{a['discipline']}

## Responsibilities
{bl(a['resp'])}

## Limitations (do not cross)
{bl(a['limits'])}
- Edit only files you own (below). For anything else, write a hand-off request to the owner.

## Input contract
{bl(a['inputs'])}
- A director brief stating: task, phase, approved scope, evidence to use, output paths, spending approval (if any).

## Output contract
{bl(a['outputs'])}
- Knowledge updates in `{kdir}` using the templates in `knowledge/_system/templates/`.

## Research methodology
{bl(a['research'])}

## Computational methods
{bl(a['comp'])}

## Visual inspection methods
{bl(a['visual'])}

## Measurements (schema: `knowledge/_system/schemas/measurement.schema.json`)
| Metric | Method | Unit |
|---|---|---|
{metrics}

Every value reports n, median and IQR (or the full distribution), the frame IDs or source IDs used, the script
version, and exclusions (e.g. caption band, motion blur).

## Knowledge files
`{kdir}`: `FINDINGS.md` (evidence-backed findings), `TECHNIQUES.md` (approved techniques only), `FAILED.md`
(failed approaches and lessons), `experiments/EXP-<id>.md`, `reports/<date>-<topic>.md`. Create files from the
templates on first use; never fill them with unverified conclusions.

## File ownership (exclusive write access)
{owns}

## Quality standards and validation
{bl(a['quality'])}
- Validation is reproducible: every number can be regenerated from a listed command and input checksum.

## Uncertainty and contradictory findings
- {a['contra']}
- Record contradictions in the hand-off `contradictions` field and in `FINDINGS.md` with both evidence sets; never
  average them away. Escalate to the director when a contradiction changes a decision.

## Hand-offs
{hand}

## Controlled experiments
{a['exp']}

{SHARED}"""
    return fm + "\n" + body

for a in A:
    open(os.path.join(AG, a["name"] + ".md"), "w").write(render(a))

# ownership matrix
rows = ["| ID | Agent | Dept | Model | Tools | Owned paths | Owned knowledge folder |", "|---|---|---|---|---|---|---|"]
for a in A:
    owns = [p for p in a["owns"] if not p.startswith("knowledge/" + a["dept"] + "/")]
    rows.append(f"| {a['id']} | `{a['name']}` | {DEPTS[a['dept']][0]} | {a['model']} | {a['tools']} | "
                + "<br>".join(f"`{p}`" for p in owns) + f" | `knowledge/{a['dept']}/{a['name']}/` |")
open(os.path.join(ROOT, "knowledge", "_system", "OWNERSHIP.md"), "w").write(
"""# Agent responsibility and file-ownership matrix

Generated with the agent definitions from `tools/agentgen/agents_data.py` (`python3 tools/agentgen/generate.py .`); never hand-edit either. Validated by `tools/validate_agents.py`.
Exclusive write access: only the listed owner edits a path. Everyone may read everything.

## Director-owned (main session)
`CLAUDE.md`, `MASTER_PLAN.md`, `PROGRESS.md`, `DECISION_LOG.md`, `README.md`, `.gitignore`, `.claude/`,
`knowledge/_system/`, `knowledge/README.md`, `knowledge/contracts/`, `knowledge/dataset/README.md`,
`knowledge/dataset/MANIFEST.json` (the frozen dataset), `research/` (except
`research/integration-feasibility.md`, owned by A23), `setup/`, `tools/`, `productions/*/BRIEF.md`.

## Specialists
""" + "\n".join(rows) + """

## Shared append-only files
- `knowledge/dataset/coverage/visual/<agent-id>.jsonl` — each agent appends only to its own file.
- `knowledge/contracts/*.md` — director-owned; a change requires sign-off lines from every listed party.

`*` in a path means "any production id"; each production folder is split by sub-folder owner.
""")
print("generated", len(A))
