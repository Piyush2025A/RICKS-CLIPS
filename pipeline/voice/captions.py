#!/usr/bin/env python3
"""Caption scheduling from words.json (A20), per knowledge/PRODUCTION_DEFAULTS.md.

Rules (all times seconds; frames derived BY TIME for each fps, never copied between rates):
 * one token on screen at a time (default: 1 word = 1 token; optional --merge-function-words joins a short
   function word with the following word, e.g. "dug a"; reference median is 1-3 words per token);
 * show_at = onset - 0.140 s (round(0.14*fps) = 4 f @30, 3 f @24), clamped >= 0;
 * never blank: hide_at of a token == show_at of the next token;
 * sentence-final token (word ends . ! ? ...) stays >= 5 f @30 (=0.1667 s) after its t_off before the next
   caption may appear, unless the next onset arrives earlier (next show_at is then capped at the next onset);
 * the last token hides at t_off + hold, clamped to the audio duration; all times clamped to [0, duration];
 * frame_in = round(show_at*fps); frame_out (exclusive) = next frame_in; each caption lasts >= 1 frame.
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SCHEMA_VERSION, frames, load_json, dump_json

LEAD_S = 0.140
HOLD_S = 5 / 30            # sentence-final hold, defined at 30 fps, converted by time
MIN_SHOW_S = 0.10          # minimum on-screen time between two successive show_at values
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "in", "on", "at", "by", "and", "or", "but", "as", "is", "it",
                  "he", "she", "we", "i", "my", "his", "her", "its", "so", "if", "no", "up", "do"}
SENT_END = re.compile(r"[.!?…][\"'”’)\]]*$")

def is_sentence_final(token):
    return bool(SENT_END.search(token))

def make_tokens(words, merge_function_words=False, max_words=3):
    """Group words into caption tokens -> list of dicts(word_indices, token, t_on, t_off)."""
    groups, i = [], 0
    while i < len(words):
        g = [i]
        if merge_function_words:
            while (len(g) < max_words and i + len(g) < len(words)
                   and re.sub(r"\W", "", words[g[-1]]["word"]).lower() in FUNCTION_WORDS
                   and not is_sentence_final(words[g[-1]]["word"])
                   and not words[g[-1]]["word"].endswith((",", ";", ":"))):
                g.append(i + len(g))
        groups.append(g); i += len(g)
    return [{"word_indices": g, "token": " ".join(words[k]["word"] for k in g),
             "t_on": words[g[0]]["t_on"], "t_off": words[g[-1]]["t_off"]} for g in groups]

def schedule(words, duration, fps, lead=LEAD_S, hold=HOLD_S, merge_function_words=False):
    """Return (captions, warnings)."""
    toks = make_tokens(words, merge_function_words)
    warns, n = [], len(toks)
    total = frames(duration, fps)
    show = []
    for i, t in enumerate(toks):
        s = max(0.0, t["t_on"] - lead)
        if i:
            p = toks[i - 1]
            if is_sentence_final(p["token"]):                       # keep the final word up for the hold
                s = max(s, min(p["t_off"] + hold, t["t_on"]))
            if s < show[-1] + MIN_SHOW_S:
                s = show[-1] + MIN_SHOW_S
                if s > t["t_on"] + 1e-9:
                    warns.append(f"token {i} '{t['token']}' shown {s - t['t_on']:.3f}s after onset (words too close)")
        show.append(min(s, duration))
    caps, prev_fi = [], -1
    for i, t in enumerate(toks):
        fi = max(frames(show[i], fps), prev_fi + 1)
        hide = show[i + 1] if i + 1 < n else min(duration, t["t_off"] + hold)
        caps.append({"index": i, "token": t["token"], "word_indices": t["word_indices"], "show_at": round(show[i], 4),
                     "hide_at": round(hide, 4), "frame_in": fi, "frame_out": 0,
                     "sentence_final": is_sentence_final(t["token"])})
        prev_fi = fi
    for i, c in enumerate(caps):
        fo = caps[i + 1]["frame_in"] if i + 1 < n else frames(c["hide_at"], fps)
        c["frame_out"] = max(fo, c["frame_in"] + 1)
    for c in caps:                                                   # clamp to the clip
        if c["frame_in"] >= total:
            warns.append(f"caption {c['index']} starts at/after the last frame ({c['frame_in']} >= {total})")
        c["frame_in"] = min(c["frame_in"], max(0, total - 1)); c["frame_out"] = min(c["frame_out"], total)
        c["frame_out"] = max(c["frame_out"], c["frame_in"] + 1)
    return caps, warns

def build_doc(words_doc, fps, **kw):
    dur = words_doc.get("duration_s") or (words_doc["words"][-1]["t_off"] if words_doc["words"] else 0.0)
    caps, warns = schedule(words_doc["words"], dur, fps, **kw)
    return {"schema_version": SCHEMA_VERSION, "fps": fps, "duration_s": dur, "total_frames": frames(dur, fps),
            "lead_s": kw.get("lead", LEAD_S), "lead_frames": frames(kw.get("lead", LEAD_S), fps),
            "hold_frames": frames(kw.get("hold", HOLD_S), fps),
            "merge_function_words": bool(kw.get("merge_function_words")), "captions": caps, "warnings": warns}

def to_srt(doc):
    def ts(t):
        ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
    fps = doc["fps"]
    return "".join(f"{c['index']+1}\n{ts(c['frame_in']/fps)} --> {ts(c['frame_out']/fps)}\n{c['token']}\n\n"
                   for c in doc["captions"])

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words"); ap.add_argument("--fps", type=int, nargs="+", default=[30, 24])
    ap.add_argument("--duration", type=float, help="override duration_s of words.json")
    ap.add_argument("--merge-function-words", action="store_true")
    ap.add_argument("--srt", action="store_true"); ap.add_argument("-o", "--outdir", required=True)
    a = ap.parse_args(argv)
    wd = load_json(a.words)
    if a.duration: wd["duration_s"] = a.duration
    os.makedirs(a.outdir, exist_ok=True)
    for fps in a.fps:
        doc = build_doc(wd, fps, merge_function_words=a.merge_function_words)
        p = os.path.join(a.outdir, f"captions_{fps}.json")
        if os.path.exists(p): print("refusing to overwrite", p, file=sys.stderr); return 2
        dump_json(doc, p)
        if a.srt:
            with open(p[:-5] + ".srt", "w", encoding="utf-8") as f: f.write(to_srt(doc))
        print(f"{fps} fps: {len(doc['captions'])} captions, {len(doc['warnings'])} warnings -> {p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
