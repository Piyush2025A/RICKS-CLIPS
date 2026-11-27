#!/usr/bin/env python3
"""Validate .claude/agents/*.md against the Claude Code subagent format and studio rules.

Usage: python3 tools/validate_agents.py [repo_root]
Exit code 0 = all checks pass. Stdlib only (uses PyYAML if installed, else a minimal parser).
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, ".claude", "agents")

# Built-in tools documented for subagents (code.claude.com/docs/en/sub-agents, 2026-11-27) that we allow.
KNOWN_TOOLS = {"Read", "Grep", "Glob", "Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch",
               "TodoWrite", "Skill", "LSP", "Monitor"}
FORBIDDEN_TOOLS = {"Agent", "SendMessage"}  # specialists must not spawn/coordinate agents (director only)
WEB_ALLOWED = {"A10", "A17", "A23", "A24", "A25", "A26"}  # agents whose briefs require official docs / research
MODELS = {"sonnet", "opus", "haiku", "fable", "inherit"}
COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
SECTIONS = ["Discipline", "Responsibilities", "Limitations", "Input contract", "Output contract",
            "Research methodology", "Computational methods", "Visual inspection methods", "Measurements",
            "Knowledge files", "File ownership", "Quality standards and validation",
            "Uncertainty and contradictory findings", "Hand-offs", "Controlled experiments", "Shared protocols"]
REQUIRED_IDS = {f"A{i:02d}" for i in range(1, 30)}
DIRECTOR_PATHS = ["CLAUDE.md", "MASTER_PLAN.md", "PROGRESS.md", "DECISION_LOG.md", "README.md", ".gitignore",
                  ".claude/", "knowledge/_system/", "knowledge/README.md", "knowledge/contracts/",
                  "knowledge/dataset/README.md", "knowledge/dataset/MANIFEST.json", "setup/", "tools/"]
SHARED_EXCEPTIONS = {"knowledge/dataset/coverage/visual/"}  # per-agent files inside, each agent its own file

errors, warnings = [], []

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    raw, body = m.group(1), text[m.end():]
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            return yaml.safe_load(raw), body
        except yaml.YAMLError as e:
            return {"__error__": str(e).splitlines()[0]}, body
    else:
        d = {}
        for line in raw.splitlines():
            k, _, v = line.partition(":")
            d[k.strip()] = v.strip()
        return d, body

def norm(p):
    return p.strip().strip("`")

def overlaps(a, b):
    """True if two owned paths can refer to the same file. '*' matches one path segment."""
    sa, sb = a.rstrip("/").split("/"), b.rstrip("/").split("/")
    da, db = a.endswith("/"), b.endswith("/")
    for i in range(min(len(sa), len(sb))):
        if not (sa[i] == sb[i] or sa[i] == "*" or sb[i] == "*"):
            return False
    if len(sa) == len(sb):
        return True
    return (len(sa) < len(sb) and da) or (len(sb) < len(sa) and db)

files = sorted(f for f in os.listdir(AGENTS) if f.endswith(".md"))
seen_names, seen_ids, owners = {}, {}, {}
for f in files:
    text = open(os.path.join(AGENTS, f), encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{f}: missing YAML frontmatter"); continue
    if "__error__" in fm:
        errors.append(f"{f}: YAML error: {fm['__error__']}"); continue
    name = fm.get("name")
    if not name or not fm.get("description"):
        errors.append(f"{f}: name and description are required")
        continue
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,255}", str(name)):
        errors.append(f"{f}: invalid name '{name}'")
    if f != f"{name}.md":
        errors.append(f"{f}: filename does not match name '{name}'")
    if name in seen_names:
        errors.append(f"{f}: duplicate name (also {seen_names[name]})")
    seen_names[name] = f
    model = str(fm.get("model", "inherit"))
    if model not in MODELS and not model.startswith("claude-"):
        errors.append(f"{f}: invalid model '{model}'")
    tools = fm.get("tools")
    if tools is None:
        errors.append(f"{f}: tools must be explicit (omitting inherits every tool)")
        tools = []
    tools = [t.strip() for t in (tools.split(",") if isinstance(tools, str) else tools)]
    for t in tools:
        if t in FORBIDDEN_TOOLS:
            errors.append(f"{f}: forbidden tool {t}")
        elif t not in KNOWN_TOOLS:
            errors.append(f"{f}: unknown tool {t}")
    if len(set(tools)) != len(tools):
        errors.append(f"{f}: duplicate tools")
    if fm.get("color") and fm["color"] not in COLORS:
        errors.append(f"{f}: invalid color {fm['color']}")
    if "maxTurns" in fm and not isinstance(fm["maxTurns"], int) and not str(fm["maxTurns"]).isdigit():
        errors.append(f"{f}: maxTurns must be an integer")
    for k in ("permissionMode",):
        if k in fm:
            warnings.append(f"{f}: sets {k}; review")
    m = re.search(r"^# (A\d\d) — ", body, re.M)
    if not m:
        errors.append(f"{f}: missing '# Axx — title' heading"); continue
    aid = m.group(1)
    if aid in seen_ids:
        errors.append(f"{f}: duplicate id {aid} (also {seen_ids[aid]})")
    seen_ids[aid] = f
    if not name.startswith(aid.lower() + "-"):
        errors.append(f"{f}: name does not start with {aid.lower()}-")
    if ("WebFetch" in tools or "WebSearch" in tools) and aid not in WEB_ALLOWED:
        errors.append(f"{f}: web tools not justified for {aid}")
    heads = re.findall(r"^## (.+)$", body, re.M)
    for s in SECTIONS:
        if not any(h.startswith(s) for h in heads):
            errors.append(f"{f}: missing section '{s}'")
    sec = re.search(r"^## File ownership.*?\n(.*?)(?=^## )", body, re.S | re.M)
    paths = [norm(p) for p in re.findall(r"^- (`[^`]+`)", sec.group(1), re.M)] if sec else []
    if not paths:
        errors.append(f"{f}: no owned paths")
    kdir = [p for p in paths if p.startswith("knowledge/") and p.rstrip("/").endswith(name)]
    if len(kdir) != 1:
        errors.append(f"{f}: must own exactly one knowledge folder ending in its name")
    owners[aid] = paths

missing = REQUIRED_IDS - set(seen_ids)
extra = set(seen_ids) - REQUIRED_IDS
if missing: errors.append(f"missing agent ids: {sorted(missing)}")
if extra: errors.append(f"unexpected agent ids: {sorted(extra)}")

ids = sorted(owners)
for i, a in enumerate(ids):
    for p in owners[a]:
        for d in DIRECTOR_PATHS:
            if overlaps(p, d):
                errors.append(f"ownership conflict: {a} `{p}` vs director `{d}`")
        for b in ids[i + 1:]:
            for q in owners[b]:
                if overlaps(p, q) and not any(p.startswith(x) or q.startswith(x) for x in SHARED_EXCEPTIONS):
                    errors.append(f"ownership conflict: {a} `{p}` vs {b} `{q}`")

print(f"agents: {len(files)}  unique names: {len(seen_names)}  ids: {len(seen_ids)}/29")
tool_counts = {}
for f in files:
    fm, _ = parse_frontmatter(open(os.path.join(AGENTS, f), encoding="utf-8").read())
    tool_counts.setdefault(fm.get("tools"), []).append(f.split("-")[0])
for t, who in sorted(tool_counts.items(), key=lambda x: str(x[0])):
    print(f"tools [{t}]: {' '.join(who)}")
for w in warnings: print("WARN", w)
for e in errors: print("ERROR", e)
print("RESULT:", "PASS" if not errors else f"FAIL ({len(errors)} errors)")
sys.exit(1 if errors else 0)
