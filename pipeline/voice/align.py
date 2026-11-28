#!/usr/bin/env python3
"""Word-timeline builders and validation (A20).

(a) chars_to_words: ElevenLabs character alignment (/with-timestamps) -> canonical words.
(b) scribe_to_words: Scribe `words` JSON (+ optional script text) -> canonical words, with drift report.
(c) validate_words: monotonic / non-overlapping / inside the audio.
Char spans are [char_start, char_end) offsets into the text exactly as submitted to TTS (tags included).
Run: .venv-analysis/bin/python -I pipeline/voice/align.py --help
"""
import argparse, difflib, math, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SCHEMA_VERSION, load_json, dump_json

TAG_RE = re.compile(r"<[^>]*>|\[[^\]]*\]")          # SSML (<break .../>, <phoneme>) and v3 audio tags ([whispers])
TOKEN_RE = re.compile(r"[^\s—–]+[—–]*|[—–]+")  # split after em/en dash, keep hyphens/apostrophes
HAS_ALNUM = re.compile(r"[0-9A-Za-zÀ-ɏ]")

def mask_tags(text):
    """Replace tags by spaces of equal length so character offsets stay valid."""
    return TAG_RE.sub(lambda m: " " * len(m.group(0)), text)

def tokenise(text):
    """Return [(token, start, end)] over the text with tags masked. Punctuation-only tokens are merged into the
    previous word (or the next one at the start). Numbers ('3.5', '1,000'), hyphens and apostrophes stay inside a word."""
    toks = []
    pending_prefix = None
    for m in TOKEN_RE.finditer(mask_tags(text)):
        s, e = m.start(), m.end()
        if not HAS_ALNUM.search(m.group(0)):
            if toks:
                t, ts, _ = toks[-1]
                toks[-1] = (t + m.group(0), ts, e)
            elif pending_prefix is None:
                pending_prefix = (s, m.group(0))
            continue
        tok = m.group(0)
        if pending_prefix is not None:
            s, tok = pending_prefix[0], pending_prefix[1] + tok
            pending_prefix = None
        toks.append((tok, s, e))
    return toks

def _word(i, w, a, b, cs, ce, source, conf, flags=None):
    d = {"index": i, "word": w, "t_on": round(a, 4), "t_off": round(b, 4), "char_start": cs, "char_end": ce,
         "source": source, "confidence": conf}
    if flags:
        d["flags"] = flags
    return d

def _fill(vals):
    """Forward/backward fill None/NaN in a list of floats."""
    out = [None if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v) for v in vals]
    last = None
    for i, v in enumerate(out):
        if v is None: out[i] = last
        else: last = v
    nxt = None
    for i in range(len(out) - 1, -1, -1):
        if out[i] is None: out[i] = nxt
        else: nxt = out[i]
    return out

def chars_to_words(characters, starts, ends, text=None):
    """Character alignment -> words. `characters` may hold multi-char strings; empty strings are skipped.
    If `text` is given and differs from ''.join(characters) the joined string is used (it is what was spoken)
    and a warning flag is set on every word."""
    if not (len(characters) == len(starts) == len(ends)):
        raise ValueError("characters/starts/ends length mismatch")
    starts, ends = _fill(starts), _fill(ends)
    joined, pos2idx = "", []
    for i, ch in enumerate(characters):
        joined += ch
        pos2idx += [i] * len(ch)
    if starts and starts[0] is None:
        raise ValueError("no usable timestamps")
    flags = ["text_differs_from_alignment"] if text is not None and text != joined else None
    words = []
    for k, (tok, s, e) in enumerate(tokenise(joined)):
        idx = [pos2idx[p] for p in range(s, e) if not joined[p].isspace()]
        a = min(starts[j] for j in idx); b = max(ends[j] for j in idx)
        words.append(_word(k, tok, a, max(a, b), s, e, "api_alignment", 1.0, flags))
    return words

# ---------------------------------------------------------------- Scribe
def norm(w):
    """Comparison key: lowercase, strip surrounding punctuation, keep inner apostrophes/hyphens."""
    w = w.lower().replace("’", "'")
    return re.sub(r"^[^\w]+|[^\w]+$", "", w)

def scribe_words(doc):
    """Return [(text, start, end, logprob)] for items of type 'word' only (spacing/audio_event dropped).
    `doc` may be the full response ({'words': [...]}) or the bare list."""
    items = doc["words"] if isinstance(doc, dict) else doc
    out = []
    for it in items:
        if it.get("type", "word") != "word":
            continue
        t = (it.get("text") or "").strip()
        if not t or it.get("start") is None or it.get("end") is None:
            continue
        out.append((t, float(it["start"]), float(it["end"]), it.get("logprob")))
    return out

def _conf(logprob):
    return 0.8 if logprob is None else round(max(0.0, min(1.0, math.exp(logprob))), 3)

def scribe_to_words(doc, script_text=None):
    """Scribe -> canonical words. Without script text: transcript words, no char span (-1). With script text:
    SequenceMatcher on normalised tokens; script wording/spans win; returns (words, report)."""
    tw = scribe_words(doc)
    report = {"transcript_words": len(tw), "script_words": None, "matched": 0, "mismatches": []}
    if script_text is None:
        return [_word(i, t, a, b, -1, -1, "scribe", _conf(lp)) for i, (t, a, b, lp) in enumerate(tw)], report
    st = tokenise(script_text)
    report["script_words"] = len(st)
    sm = difflib.SequenceMatcher(a=[norm(t[0]) for t in st], b=[norm(t[0]) for t in tw], autojunk=False)
    slots = [None] * len(st)          # per script word: (a, b, conf, flags)
    extra = []                        # transcript words absent from the script
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                t, a, b, lp = tw[j1 + k]; slots[i1 + k] = (a, b, _conf(lp), None)
            report["matched"] += i2 - i1
        elif op == "replace":
            n = min(i2 - i1, j2 - j1)
            for k in range(n):
                t, a, b, lp = tw[j1 + k]; slots[i1 + k] = (a, b, min(_conf(lp), 0.5), ["substituted"])
                report["mismatches"].append({"kind": "substituted", "script": st[i1 + k][0], "transcript": t, "t": a})
            for k in range(n, i2 - i1):
                report["mismatches"].append({"kind": "missing", "script": st[i1 + k][0], "transcript": None})
            for k in range(n, j2 - j1):
                t, a, b, lp = tw[j1 + k]; extra.append((i2, t, a, b))
                report["mismatches"].append({"kind": "extra", "script": None, "transcript": t, "t": a})
        elif op == "delete":
            for k in range(i1, i2):
                report["mismatches"].append({"kind": "missing", "script": st[k][0], "transcript": None})
        elif op == "insert":
            for k in range(j1, j2):
                t, a, b, lp = tw[k]; extra.append((i1, t, a, b))
                report["mismatches"].append({"kind": "extra", "script": None, "transcript": t, "t": a})
    # interpolate missing script words between timed neighbours
    for i, s in enumerate(slots):
        if s is not None: continue
        l = next((j for j in range(i - 1, -1, -1) if slots[j]), None)
        r = next((j for j in range(i + 1, len(slots)) if slots[j]), None)
        lo = slots[l][1] if l is not None else (tw[0][1] if tw else 0.0)
        hi = slots[r][0] if r is not None else (tw[-1][2] if tw else lo)
        run = [j for j in range(l + 1 if l is not None else 0, r if r is not None else len(slots)) if slots[j] is None]
        n, k = len(run), run.index(i)
        w = max(0.0, hi - lo) / n
        slots[i] = (lo + k * w, lo + (k + 1) * w, 0.0, ["interpolated"])
    words = [_word(i, st[i][0], *slots[i][:2], st[i][1], st[i][2], "scribe", slots[i][2], slots[i][3])
             for i in range(len(st))]
    report["match_ratio"] = round(report["matched"] / max(1, len(st)), 4)
    report["extra_words"] = [e[1] for e in extra]
    return words, report

# ---------------------------------------------------------------- validation / repair
def validate_words(words, duration=None, eps=1e-3):
    """Return a list of issue strings (empty = valid)."""
    issues = []
    for i, w in enumerate(words):
        if w["t_off"] < w["t_on"] - eps: issues.append(f"{i} '{w['word']}': t_off < t_on")
        if w["t_on"] < -eps: issues.append(f"{i} '{w['word']}': t_on < 0")
        if duration is not None and w["t_off"] > duration + eps:
            issues.append(f"{i} '{w['word']}': t_off {w['t_off']:.3f} beyond duration {duration:.3f}")
        if i:
            p = words[i - 1]
            if w["t_on"] < p["t_on"] - eps: issues.append(f"{i} '{w['word']}': onset not monotonic")
            elif w["t_on"] < p["t_off"] - eps: issues.append(f"{i} '{w['word']}': overlaps previous by {p['t_off']-w['t_on']:.3f}s")
    return issues

def repair_words(words, duration=None):
    """Clamp into [0,duration], make onsets monotonic, trim overlaps. Marks repaired words with flag 'repaired'."""
    out = [dict(w) for w in words]
    for i, w in enumerate(out):
        a, b = w["t_on"], w["t_off"]
        if duration is not None: a, b = min(a, duration), min(b, duration)
        a = max(0.0, a); b = max(a, b)
        if i:
            a = max(a, out[i - 1]["t_on"])
            if a < out[i - 1]["t_off"]:
                out[i - 1]["t_off"] = round(max(out[i - 1]["t_on"], a), 4)
                out[i - 1].setdefault("flags", []).append("repaired")
            b = max(a, b)
        if (a, b) != (w["t_on"], w["t_off"]): w.setdefault("flags", []).append("repaired")
        w["t_on"], w["t_off"] = round(a, 4), round(b, 4)
    return out

def build_doc(words, source, text=None, duration=None, audio_sha256=None, report=None):
    doc = {"schema_version": SCHEMA_VERSION, "source": source, "duration_s": duration, "text": text,
           "audio_sha256": audio_sha256, "words": words, "validation_issues": validate_words(words, duration)}
    if report: doc["alignment_report"] = report
    return doc

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("chars", help="API alignment JSON -> words.json")
    c.add_argument("alignment"); c.add_argument("--text-file"); c.add_argument("--duration", type=float)
    c.add_argument("--audio-sha256"); c.add_argument("-o", "--out", required=True)
    s = sub.add_parser("scribe", help="Scribe JSON -> words.json")
    s.add_argument("scribe"); s.add_argument("--script-file"); s.add_argument("--duration", type=float)
    s.add_argument("--audio-sha256"); s.add_argument("-o", "--out", required=True)
    v = sub.add_parser("validate", help="validate a words.json")
    v.add_argument("words"); v.add_argument("--duration", type=float)
    a = ap.parse_args(argv)
    if os.path.exists(getattr(a, "out", "/nonexistent/x")):
        print("refusing to overwrite", a.out, file=sys.stderr); return 2
    if a.cmd == "chars":
        j = load_json(a.alignment); j = j.get("alignment", j)
        text = open(a.text_file, encoding="utf-8").read() if a.text_file else None
        words = chars_to_words(j["characters"], j["character_start_times_seconds"], j["character_end_times_seconds"], text)
        doc = build_doc(words, "api_alignment", "".join(j["characters"]), a.duration, a.audio_sha256)
    elif a.cmd == "scribe":
        script = open(a.script_file, encoding="utf-8").read() if a.script_file else None
        words, rep = scribe_to_words(load_json(a.scribe), script)
        doc = build_doc(words, "scribe", script, a.duration, a.audio_sha256, rep)
    else:
        w = load_json(a.words); issues = validate_words(w["words"], a.duration or w.get("duration_s"))
        print("\n".join(issues) or "OK"); return 1 if issues else 0
    dump_json(doc, a.out)
    print(f"{len(doc['words'])} words, {len(doc['validation_issues'])} validation issues -> {a.out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
