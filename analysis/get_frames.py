#!/usr/bin/env python3
"""Extract exact native-resolution frames (lossless PNG + JSON sidecar) by frame ID, for visual inspection.
Usage: get_frames.py INPUT --key RC30-07 --frames RC30-07-f000012 RC30-07-f000013 --out DIR [--cross-check]
Output must go outside the repo or into a git-ignored dir (private/, out/): frames are never committed."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcpipe import native


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("--key", required=True)
    ap.add_argument("--frames", nargs="+", required=True, help="frame IDs (<key>-fNNNNNN) or integer indices")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cross-check", action="store_true", help="verify bit-exactness against ffmpeg select filter")
    a = ap.parse_args()
    ids = [int(x) if x.isdigit() else x for x in a.frames]
    for s in native.get_frames(a.input, a.key, ids, a.out, cross_check=a.cross_check):
        print(s["frame_id"], s["analysis_resolution"]["width"], "x", s["analysis_resolution"]["height"], s["frame_bgr_sha256"][:16],
              s["verified"])


if __name__ == "__main__":
    main()
