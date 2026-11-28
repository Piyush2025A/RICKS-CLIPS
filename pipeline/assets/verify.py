#!/usr/bin/env python3
"""Verify the private store: re-hash files vs sidecars and ledger. Optionally compare one file to a known SHA-256.

  verify.py --store DIR [--record]              # whole-store audit; exit 1 on any mismatch
  verify.py --check FILE --expect-sha256 HEX    # Drive round-trip check of a downloaded file
--record appends a 'verified' custody event to each passing sidecar (only the sidecar changes, never the asset).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assetlib as L


def audit(store, record=False):
    store = os.path.abspath(os.path.expanduser(store))
    problems, ok = [], 0
    ledger = [e for e in L.read_ledger(os.path.join(store, "INTAKE_LEDGER.jsonl")) if e.get("event") == "intake"]
    seen = set()
    for e in ledger:
        rel = e["stored_path"]; seen.add(rel)
        p = os.path.join(store, rel)
        if not os.path.exists(p):
            problems.append({"path": rel, "problem": "missing"}); continue
        h = L.sha256_file(p)
        if h != e["sha256"]:
            problems.append({"path": rel, "problem": "ledger_hash_mismatch", "expected": e["sha256"], "actual": h}); continue
        sc = os.path.join(store, e["sidecar"])
        if not os.path.exists(sc):
            problems.append({"path": rel, "problem": "sidecar_missing"}); continue
        with open(sc, encoding="utf-8") as f:
            s = json.load(f)
        if s["file"]["sha256"] != h:
            problems.append({"path": rel, "problem": "sidecar_hash_mismatch", "expected": s["file"]["sha256"], "actual": h}); continue
        if os.path.getsize(p) != s["file"]["size_bytes"]:
            problems.append({"path": rel, "problem": "size_mismatch"}); continue
        ok += 1
        if record:
            s["chain_of_custody"].append({"event": "verified", "utc": L.utcnow(), "actor": "a24/verify.py", "detail": "sha256 matches ledger and sidecar"})
            with open(sc, "w", encoding="utf-8") as f:
                json.dump(s, f, indent=2, ensure_ascii=False); f.write("\n")
    for root, _, files in os.walk(store):  # unregistered assets
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), store)
            if fn.endswith(".provenance.json") or fn == "INTAKE_LEDGER.jsonl" or rel in seen:
                continue
            problems.append({"path": rel, "problem": "not_in_ledger"})
    return {"ok": ok, "problems": problems}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store"); p.add_argument("--record", action="store_true")
    p.add_argument("--check"); p.add_argument("--expect-sha256")
    a = p.parse_args(argv)
    if a.check:
        h = L.sha256_file(os.path.expanduser(a.check))
        res = {"file": os.path.basename(a.check), "sha256": h, "match": (h == a.expect_sha256.lower()) if a.expect_sha256 else None}
        print(json.dumps(res, indent=2)); return 0 if res["match"] in (True, None) else 1
    if not a.store:
        p.error("--store or --check required")
    res = audit(a.store, a.record)
    print(json.dumps(res, indent=2)); return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
