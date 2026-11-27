"""JSON-Schema validator (draft 2020-12 subset actually used by our schemas; `jsonschema` is not installed) plus the
semantic invariants that JSON Schema cannot express (coverage sums, audio interval sums, key/dataset consistency,
analysis_resolution consistency).

Keywords: type (string or list), const, enum, pattern, minimum, maximum, required, properties, additionalProperties
(bool or schema), propertyNames, items, if/then/else, allOf, anyOf, oneOf, not, format (date-time only).
Unknown keywords that matter are rejected loudly (UNSUPPORTED) instead of being silently ignored."""
import json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_DIR = os.path.join(REPO, "knowledge", "_system", "schemas")
KNOWN = {"$schema", "$id", "title", "description", "type", "const", "enum", "pattern", "minimum", "maximum", "required",
         "properties", "additionalProperties", "propertyNames", "items", "if", "then", "else", "allOf", "anyOf", "oneOf",
         "not", "format", "default"}
_TYPES = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool,
          "null": type(None)}
_DT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
KEY_RE = r"^(RC30-(0[1-9]|[12][0-9]|30)|OUR-[A-Za-z0-9_-]+-[A-Za-z0-9_-]+|SYN-[A-Za-z0-9_-]+)$"


def load_schema(name):
    return json.load(open(os.path.join(SCHEMA_DIR, name)))


def _is(obj, t):
    if t not in _TYPES:
        return False
    if t in ("integer", "number") and isinstance(obj, bool):
        return False
    if t == "integer" and isinstance(obj, float):
        return obj == int(obj) if obj == obj and abs(obj) != float("inf") else False
    return isinstance(obj, _TYPES[t])


def validate(obj, schema, path="$"):
    """Return a list of error strings (empty = valid)."""
    errs = []
    if schema is True or schema == {}:
        return errs
    if schema is False:
        return [f"{path}: schema is false"]
    for k in schema:
        if k not in KNOWN:
            errs.append(f"{path}: UNSUPPORTED schema keyword {k!r} (validator would ignore it)")
    t = schema.get("type")
    if t is not None:
        ts = t if isinstance(t, list) else [t]
        if not any(_is(obj, x) for x in ts):
            return errs + [f"{path}: expected {'|'.join(ts)}, got {type(obj).__name__}"]
    if "const" in schema and not (obj == schema["const"] and type(obj) is type(schema["const"])):
        errs.append(f"{path}: {obj!r} != const {schema['const']!r}")
    if "enum" in schema and not any(obj == e and type(obj) is type(e) for e in schema["enum"]):
        errs.append(f"{path}: {obj!r} not in enum {schema['enum']}")
    if isinstance(obj, str):
        if "pattern" in schema and not re.search(schema["pattern"], obj):
            errs.append(f"{path}: {obj!r} !~ {schema['pattern']}")
        if schema.get("format") == "date-time" and not _DT.match(obj):
            errs.append(f"{path}: {obj!r} is not an RFC 3339 date-time")
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if "minimum" in schema and obj < schema["minimum"]:
            errs.append(f"{path}: {obj} < minimum {schema['minimum']}")
        if "maximum" in schema and obj > schema["maximum"]:
            errs.append(f"{path}: {obj} > maximum {schema['maximum']}")
    if isinstance(obj, dict):
        for k in schema.get("required", []):
            if k not in obj:
                errs.append(f"{path}: missing required {k}")
        props = schema.get("properties", {})
        ap = schema.get("additionalProperties", True)
        for k, v in obj.items():
            if "propertyNames" in schema:
                errs += [f"{path}.<key {k!r}>: " + e.split(": ", 1)[1] for e in validate(k, schema["propertyNames"], "k")]
            if k in props:
                errs += validate(v, props[k], f"{path}.{k}")
            elif isinstance(ap, dict):
                errs += validate(v, ap, f"{path}.{k}")
            elif ap is False:
                errs.append(f"{path}: additional property {k!r} not allowed")
    if isinstance(obj, list) and "items" in schema:
        for i, v in enumerate(obj):
            errs += validate(v, schema["items"], f"{path}[{i}]")
    for sub in schema.get("allOf", []):
        errs += validate(obj, sub, path)
    if "anyOf" in schema and not any(not validate(obj, s, path) for s in schema["anyOf"]):
        errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema and sum(1 for s in schema["oneOf"] if not validate(obj, s, path)) != 1:
        errs.append(f"{path}: does not match exactly one of oneOf")
    if "not" in schema and not validate(obj, schema["not"], path):
        errs.append(f"{path}: matches a 'not' schema")
    if "if" in schema:
        # spec semantics: `if` passes when the instance satisfies it (an absent property satisfies `properties`)
        if not validate(obj, schema["if"], path):
            if "then" in schema:
                errs += validate(obj, schema["then"], path)
        elif "else" in schema:
            errs += validate(obj, schema["else"], path)
    return errs


# ---------------------------------------------------------------- semantic checks
def key_dataset(key):
    """Dataset implied by a key/frame-id prefix, or None."""
    if not isinstance(key, str):
        return None
    for pre, ds in (("RC30-", "RC30"), ("OUR-", "OUR"), ("SYN-", "SYN")):
        if key.startswith(pre):
            return ds
    return None


def _check_keys(keys, dataset, where):
    return [f"{where}: key {k!r} implies dataset {key_dataset(k)!r} but record says {dataset!r}"
            for k in keys if key_dataset(k) != dataset]


def check_resolution(ar, where="analysis_resolution"):
    errs = []
    if not isinstance(ar, dict):
        return errs
    try:
        w, h, nw, nh, mode = ar["width"], ar["height"], ar["native_width"], ar["native_height"], ar["mode"]
    except KeyError:
        return errs  # missing keys are the schema's job
    if mode == "native":
        if (w, h) != (nw, nh):
            errs.append(f"{where}: mode native but {w}x{h} != native {nw}x{nh}")
        if ar.get("scaler"):
            errs.append(f"{where}: mode native must not name a scaler ({ar['scaler']!r})")
    elif mode == "proxy":
        if (w, h) == (nw, nh):
            errs.append(f"{where}: mode proxy but {w}x{h} equals native (would be mislabelled)")
        if w > nw or h > nh:
            errs.append(f"{where}: proxy {w}x{h} larger than native {nw}x{nh}")
        if not ar.get("scaler"):
            errs.append(f"{where}: proxy must name the scaler")
    return errs


def validate_coverage(rec, schema=None):
    """coverage-computational v2: JSON Schema + invariants. Returns a list of errors."""
    schema = schema or load_schema("coverage-computational.schema.json")
    errs = validate(rec, schema)
    if not isinstance(rec, dict):
        return errs
    ds = rec.get("dataset")
    if ds in ("RC30", "OUR", "SYN"):
        errs += _check_keys([rec.get("video_key")], ds, "video_key")
        errs += _check_keys([m.get("frame", "")[: m.get("frame", "").rfind("-f")] for m in rec.get("missing", []) if isinstance(m, dict)],
                            ds, "missing[].frame")
    if ds == "RC30" and not rec.get("manifest_sha256"):
        errs.append("RC30 record without manifest_sha256")
    cnt = ("frames_ok", "frames_uncertain", "frames_failed", "frames_missing", "frames_expected")
    if all(isinstance(rec.get(k), int) for k in cnt):
        s = rec["frames_ok"] + rec["frames_uncertain"] + rec["frames_failed"] + rec["frames_missing"]
        if s != rec["frames_expected"]:
            errs.append(f"invariant: ok+uncertain+failed+missing = {s} != frames_expected {rec['frames_expected']}")
        if isinstance(rec.get("frames_processed"), int) and rec["frames_processed"] != rec["frames_ok"] + rec["frames_uncertain"]:
            errs.append("invariant: frames_processed != frames_ok + frames_uncertain")
        if isinstance(rec.get("frames_decoded"), int) and rec["frames_decoded"] > rec["frames_expected"]:
            errs.append("frames_decoded > frames_expected")
        for st, d in (rec.get("stages") or {}).items():
            if isinstance(d, dict) and all(isinstance(d.get(k), int) for k in ("ok", "uncertain", "failed", "missing")):
                ss = d["ok"] + d["uncertain"] + d["failed"] + d["missing"]
                if ss != rec["frames_expected"]:
                    errs.append(f"invariant: stage {st}: ok+uncertain+failed+missing = {ss} != frames_expected")
                errs += check_resolution(d.get("analysis_resolution"), f"stages.{st}.analysis_resolution")
        # every failed/missing frame must be listed (distinct frames in the list == failed + missing overall)
        listed = {m.get("frame") for m in rec.get("missing", []) if isinstance(m, dict)}
        if len(listed) != rec["frames_failed"] + rec["frames_missing"]:
            errs.append(f"invariant: {len(listed)} distinct frames listed in missing[] != frames_failed+frames_missing "
                        f"({rec['frames_failed'] + rec['frames_missing']})")
    errs += check_resolution(rec.get("analysis_resolution"))
    return errs


def validate_audio_coverage(rec, schema=None, tol=None):
    schema = schema or load_schema("coverage-audio.schema.json")
    errs = validate(rec, schema)
    if not isinstance(rec, dict):
        return errs
    ds = rec.get("dataset")
    if ds in ("RC30", "OUR", "SYN"):
        errs += _check_keys([rec.get("video_key")], ds, "video_key")
    if ds == "RC30" and not rec.get("manifest_sha256"):
        errs.append("RC30 audio record without manifest_sha256")
    if rec.get("audio_present") is False:
        if rec.get("stream") is not None:
            errs.append("audio_present false but stream is not null")
        if rec.get("analyzed_s") not in (0, 0.0):
            errs.append("audio_present false but analyzed_s != 0")
        mi0 = rec.get("missing_intervals") or []
        if not (len(mi0) == 1 and isinstance(mi0[0], dict) and mi0[0].get("reason") == "no audio stream"
                and abs(mi0[0].get("start_s", -1)) < 1e-9 and abs(mi0[0].get("end_s", -1) - (rec.get("duration_s") or 0)) < 1e-3):
            errs.append("audio_present false: missing_intervals must be the whole duration with reason 'no audio stream'")
    if all(isinstance(rec.get(k), (int, float)) and not isinstance(rec.get(k), bool) for k in ("duration_s", "analyzed_s")):
        mi = [m for m in rec.get("missing_intervals", []) if isinstance(m, dict) and
              all(isinstance(m.get(k), (int, float)) for k in ("start_s", "end_s"))]
        for m in mi:
            if m["end_s"] < m["start_s"]:
                errs.append(f"missing interval {m} ends before it starts")
            if m["start_s"] < -1e-9 or m["end_s"] > rec["duration_s"] + 1e-6:
                errs.append(f"missing interval {m} outside [0, duration_s={rec['duration_s']}]")
        tot = sum(m["end_s"] - m["start_s"] for m in mi)
        tol = tol if tol is not None else (rec.get("hop_s") or 0.01)
        gap = rec["duration_s"] - rec["analyzed_s"] - tot
        if abs(gap) > tol + 1e-9:
            errs.append(f"invariant: analyzed_s + missing = {rec['analyzed_s'] + tot:.4f} != duration_s {rec['duration_s']:.4f} "
                        f"(off by {gap:.4f} s > one hop {tol})")
        if rec["analyzed_s"] > rec["duration_s"] + tol:
            errs.append("analyzed_s > duration_s")
    return errs


def validate_measurement(rec, schema=None):
    """measurement v2: JSON Schema + RC30 rules + key/dataset consistency + resolution consistency."""
    schema = schema or load_schema("measurement.schema.json")
    errs = validate(rec, schema)
    if not isinstance(rec, dict):
        return errs
    ds = rec.get("dataset")
    if ds in ("RC30", "OUR", "SYN"):
        errs += _check_keys(list((rec.get("per_video") or {}).keys()), ds, "per_video")
        errs += _check_keys(list((rec.get("input_sha256") or {}).keys()), ds, "input_sha256")
        if ds == "RC30":
            if not rec.get("manifest_sha256"):
                errs.append("RC30 measurement without manifest_sha256")
            if set((rec.get("per_video") or {})) - set(rec.get("input_sha256") or {}):
                errs.append("RC30 per_video key without input_sha256")
    for k, v in (rec.get("per_video") or {}).items():
        if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float))):
            errs.append(f"per_video[{k}] = {v!r}: non-numeric must be null")
    errs += check_resolution((rec.get("method") or {}).get("analysis_resolution"), "method.analysis_resolution")
    return errs
