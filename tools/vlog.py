#!/usr/bin/env python3
"""Append one visual-inspection record to knowledge/dataset/coverage/visual/<agent>.jsonl (schema coverage-visual).
Usage: python3 tools/vlog.py AGENT KIND VIEW_RES "PURPOSE" FRAMES...
  AGENT    your agent id, e.g. a15-transition-specialist   KIND frame|crop|contact_sheet|strip|overlay
  VIEW_RES per-frame size as you saw it, e.g. 1080x1920 or 120x213   FRAMES frame IDs or ranges RC30-07-f000010..f000057
Log ONLY images you actually opened. One call per image."""
import sys, json, datetime, os
if len(sys.argv) < 6:
    sys.exit(__doc__)
agent, kind, res, purpose, *frames = sys.argv[1:]
assert kind in ("frame", "crop", "contact_sheet", "strip", "overlay", "render"), kind
rec = {"agent": agent, "viewed_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
       "image_kind": kind, "frames": frames, "view_resolution": res, "purpose": purpose}
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(root, "knowledge", "dataset", "coverage", "visual", f"{agent}.jsonl"), "a") as f:
    f.write(json.dumps(rec) + "\n")
