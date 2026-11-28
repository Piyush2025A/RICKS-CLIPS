#!/usr/bin/env python3
"""Sentence / clause (story-beat) timings from the script + measured pauses — no transcription, no credits.

Phase 4 default (D035): animation syncs to sentence and story-beat timings; word-level timestamps (Scribe / API
alignment) are optional and off by default. Method:
 1. Split the script at punctuation into clauses (, ; : — …) and sentences (. ? !). A line in the script that starts with
    `#beat` (optional) forces a story-beat boundary there.
 2. Voiced span and internal pauses come from `silence.py` JSON (RMS, -45 dBFS, pauses >= 0.25 s).
 3. Every punctuation boundary gets an estimated time by character proportion over the voiced speech time (pauses
    excluded). Each measured pause is matched, in order, to the nearest unused boundary (sentence ends preferred on
    ties); matched boundaries take the pause times ("measured"), unmatched ones keep the estimate ("estimated").
Output JSON: sentences[] and clauses[] with t_on/t_off (s), frames at 24 and 30 fps (by time), source per edge.
Usage: beats.py <script.txt> <silence.json> -o beats.json
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import seconds_to_frame  # noqa: E402

SENT_END = ".?!"
CLAUSE = ",;:—…"


def tokens(text):
    """Return list of (segment_text, boundary_kind) where kind is 'sentence', 'clause' or 'end'."""
    out, buf = [], ""
    for ch in text.strip():
        buf += ch
        if ch in SENT_END or ch in CLAUSE:
            kind = "sentence" if ch in SENT_END else "clause"
            if buf.strip():
                out.append([buf.strip(), kind])
            buf = ""
    if buf.strip():
        out.append([buf.strip(), "end"])
    if out:
        out[-1][1] = "end"
    return out


def plan(script, sil):
    segs = tokens(script)
    t0, t1 = sil["first_voiced_s"], sil["last_voiced_s"]
    pauses = sorted(sil.get("internal_pauses", []), key=lambda p: p["start_s"])
    speech = (t1 - t0) - sum(p["dur_s"] for p in pauses)
    chars = [len(s) for s, _ in segs]
    total = sum(chars) or 1

    def speech_to_time(sp):  # map speech-time offset to clock time, skipping pauses
        t = t0 + sp
        for p in pauses:
            if t >= p["start_s"]:
                t += p["dur_s"]
        return t

    # estimated boundary times (end of each segment except the last)
    acc, est = 0, []
    for c in chars[:-1]:
        acc += c
        est.append(speech_to_time(speech * acc / total))
    used, edges = set(), [{"t": e, "src": "estimated"} for e in est]
    for p in pauses:
        mid = (p["start_s"] + p["end_s"]) / 2
        cands = [i for i in range(len(est)) if i not in used]
        if not cands:
            break
        best = min(cands, key=lambda i: (abs(est[i] - mid), 0 if segs[i][1] == "sentence" else 1))
        used.add(best)
        edges[best] = {"t_off": p["start_s"], "t_on_next": p["end_s"], "src": "measured"}
    clauses, t_on, on_src = [], t0, "measured"
    for i, (s, kind) in enumerate(segs):
        if i < len(edges):
            e = edges[i]
            t_off = e.get("t_off", e.get("t")); nxt = e.get("t_on_next", e.get("t")); off_src = e["src"]
        else:
            t_off, nxt, off_src = t1, None, "measured"
        clauses.append({"index": i, "text_chars": len(s), "ends_with": kind, "t_on": round(t_on, 3), "t_off": round(t_off, 3),
                        "on_source": on_src, "off_source": off_src,
                        "frames_24": [seconds_to_frame(t_on, 24), seconds_to_frame(t_off, 24)], "frames_30": [seconds_to_frame(t_on, 30), seconds_to_frame(t_off, 30)]})
        if nxt is not None:
            t_on, on_src = nxt, off_src
    sentences, cur = [], []
    for c in clauses:
        cur.append(c)
        if c["ends_with"] in ("sentence", "end"):
            sentences.append({"index": len(sentences), "clauses": [x["index"] for x in cur], "t_on": cur[0]["t_on"],
                              "t_off": cur[-1]["t_off"], "on_source": cur[0]["on_source"], "off_source": cur[-1]["off_source"],
                              "frames_24": [cur[0]["frames_24"][0], cur[-1]["frames_24"][1]],
                              "frames_30": [cur[0]["frames_30"][0], cur[-1]["frames_30"][1]]})
            cur = []
    return {"method": "script punctuation + silence.py pauses (no transcription)", "voiced": [t0, t1],
            "pauses_matched": len(used), "pauses_total": len(pauses), "sentences": sentences, "clauses": clauses}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script"); ap.add_argument("silence_json"); ap.add_argument("-o", "--out")
    a = ap.parse_args(argv)
    res = plan(open(a.script, encoding="utf-8").read(), json.load(open(a.silence_json)))
    txt = json.dumps(res, indent=2)
    if a.out:
        open(a.out, "w").write(txt + "\n")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
