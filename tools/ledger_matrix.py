#!/usr/bin/env python3
"""Visual-coverage matrix from knowledge/dataset/coverage/visual/*.jsonl (director tool).
Counts, per agent and per video, ledger records that name that video, and the number of distinct frames covered
(ranges expanded; overview/sheet records count every frame in the stated range as *viewed at that record's size* —
an upper bound for tiles). Usage: python3 tools/ledger_matrix.py [--md]"""
import glob, json, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RX = re.compile(r"RC30-(\d\d)-f(\d{6})(?:\.\.f?(\d{6}))?")
rows = {}
for p in sorted(glob.glob(f"{ROOT}/knowledge/dataset/coverage/visual/*.jsonl")):
    agent = os.path.basename(p)[:-6]
    rec = collections.Counter(); frames = collections.defaultdict(set); n = 0
    for line in open(p):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line); n += 1
        vids = set()
        for f in r.get("frames", []):
            for m in RX.finditer(str(f)):
                v = int(m.group(1)); a = int(m.group(2)); b = int(m.group(3) or a)
                if b < a or b - a > 5000:
                    b = a
                frames[v].update(range(a, b + 1)); vids.add(v)
        for v in vids:
            rec[v] += 1
    rows[agent] = (n, rec, frames)
md = "--md" in sys.argv
vids = range(1, 31)
if md:
    print("| Agent | records | videos | " + " | ".join(f"{v:02d}" for v in vids) + " |")
    print("|---|---|---|" + "---|" * 30)
for agent, (n, rec, frames) in rows.items():
    cells = [str(rec[v]) if rec[v] else "·" for v in vids]
    if md:
        print(f"| {agent} | {n} | {len(rec)} | " + " | ".join(cells) + " |")
    else:
        print(f"{agent:40s} rec={n:4d} videos={len(rec):2d} frames={sum(len(s) for s in frames.values())}")
allv = collections.Counter(); union = collections.defaultdict(set)
for agent, (n, rec, frames) in rows.items():
    for v in rec: allv[v] += 1
    for v, s in frames.items(): union[v] |= s
tot = sum(r[0] for r in rows.values())
if md:
    print(f"| **all** | {tot} | {len(allv)} | " + " | ".join(str(allv[v]) for v in vids) + " |")
    print()
    print("Distinct frames named in any ledger record (upper bound; tiles/sheets included) per video: " +
          ", ".join(f"{v:02d}: {len(union[v])}" for v in vids))
else:
    print("total records", tot, "videos with any visual evidence", len(allv))
