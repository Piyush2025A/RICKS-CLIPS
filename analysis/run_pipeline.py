#!/usr/bin/env python3
"""CLI for the rcpipe pipeline. Usage: run_pipeline.py INPUT --key RC30-07 --out DIR [options]. See analysis/README.md."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcpipe import pipeline


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("--key", required=True, help="video key, e.g. RC30-07, OUR-prod-r1 or SYN-01 (tests)")
    ap.add_argument("--out", required=True, help="output root (git-ignored, e.g. analysis/data/<table>)")
    ap.add_argument("--proxy-width", type=int, default=None, help="decode+analyse at this width (default native)")
    ap.add_argument("--chunk", type=int, default=150, help="frames per checkpoint chunk")
    ap.add_argument("--stages", default=",".join(pipeline.ALL_STAGES))
    ap.add_argument("--sheets-every", type=int, default=0, help="contact sheet every N frames (0 = none)")
    ap.add_argument("--exclude-bottom", type=float, default=0.0, help="fraction of height excluded from motion (caption band)")
    ap.add_argument("--exclude-top", type=float, default=0.0)
    ap.add_argument("--no-flow", action="store_true")
    ap.add_argument("--dataset", choices=["RC30", "OUR", "SYN"], default=None,
                    help="optional; must agree with the key prefix. RC30 additionally needs knowledge/dataset/MANIFEST.json")
    ap.add_argument("--manifest", default=None, help="path of the frozen dataset manifest (RC30 only)")
    ap.add_argument("--stop-after-chunks", type=int, default=None, help="TEST HOOK: simulate crash")
    a = ap.parse_args()
    mk = {"exclude_bottom": a.exclude_bottom, "exclude_top": a.exclude_top, "flow": not a.no_flow}
    try:
        r = pipeline.run(a.input, a.key, a.out, a.proxy_width, a.chunk, a.stages.split(","), a.sheets_every,
                         a.stop_after_chunks, None, mk, dataset=a.dataset, manifest_path=a.manifest)
    except ValueError as e:  # refusals (bad key, dataset/key mismatch, RC30 without manifest)
        print("REFUSED:", e, file=sys.stderr, flush=True)
        sys.exit(2)
    except pipeline.SimulatedInterrupt as e:
        print("INTERRUPTED:", e, flush=True)
        os._exit(75)
    print(f"done {a.key}: {r['decoded']} frames, peak RSS {r['manifest']['peak_rss']}, wall {r['manifest']['wall_s']} s")


if __name__ == "__main__":
    main()
