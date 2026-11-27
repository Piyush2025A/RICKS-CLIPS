#!/usr/bin/env python3
"""A27 wave-C1 consolidation (not part of rcpipe; rcpipe v0.2.0 frozen). script version consolidate_c1@1.0
Copies coverage ledgers, validates them, writes table checksums + frame index summary, prints run stats as JSON."""
import os, sys, json, csv, hashlib, re, glob, shutil
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "analysis"))
from rcpipe import schema
PRIV = os.path.expanduser("~/ricks-clips-private/analysis-data/rc30")
V = os.path.join(PRIV, "v0.2.0")
COV = os.path.join(REPO, "knowledge/dataset/coverage/computational")
IDX = os.path.join(REPO, "knowledge/dataset/index")
TABLES = ["frames.csv", "color.csv", "edges.csv", "sharpness.csv", "motion.csv", "shot_features.csv", "audio_env.csv",
          "shot_candidates.json", "measurements.json"]
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
def rows(p):
    with open(p, "rb") as f:
        return max(0, sum(1 for _ in f) - 1)
keys = sorted(d for d in os.listdir(V) if re.match(r"RC30-\d\d$", d))
res = {"validation": {}, "keys": len(keys)}
sums, summ = [], []
for k in keys:
    d = os.path.join(V, k)
    for src, dst, fn in (("coverage.jsonl", f"{k}.jsonl", schema.validate_coverage),
                         ("audio.coverage.jsonl", f"{k}.audio.jsonl", schema.validate_audio_coverage)):
        shutil.copyfile(os.path.join(d, src), os.path.join(COV, dst))
        errs = []
        n = 0
        for l in open(os.path.join(COV, dst)):
            if l.strip():
                n += 1
                errs += fn(json.loads(l))
        res["validation"][dst] = {"records": n, "errors": errs}
    for t in TABLES:
        sums.append(f"{sha(os.path.join(d, t))}  v0.2.0/{k}/{t}")
    fr = list(csv.DictReader(open(os.path.join(d, "frames.csv"))))
    cov = json.loads(open(os.path.join(d, "coverage.jsonl")).readline())
    sh = json.load(open(os.path.join(d, "sheets.json")))
    nsh = len(glob.glob(os.path.join(d, "sheets", "*.png")))
    rc = {t: rows(os.path.join(d, t)) for t in ("frames.csv", "color.csv", "edges.csv", "sharpness.csv", "motion.csv", "shot_features.csv", "audio_env.csv")}
    cand = json.load(open(os.path.join(d, "shot_candidates.json")))["candidates"]
    summ.append(dict(key=k, nb_frames=len(fr), first_pts=fr[0]["pts_time"], last_pts=fr[-1]["pts_time"], sheets=nsh,
                     sheets_json_entries=len(sh), **{"rows_" + t[:-4]: v for t, v in rc.items()}, n_candidates=len(cand),
                     input_sha256=cov["input_sha256"]))
open(os.path.join(IDX, "RC30_tables.sha256"), "w").write("\n".join(sums) + "\n")
with open(os.path.join(IDX, "RC30_frame_index_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summ[0])); w.writeheader(); w.writerows(summ)
json.dump(res, open(os.environ.get("C1_OUT", "/dev/stdout"), "w"), indent=1)
