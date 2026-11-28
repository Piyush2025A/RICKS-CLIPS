"""Minimal JSON-Schema subset validator (no jsonschema package in the analysis venv).
Supports: type (incl. lists), required, properties, items, enum, minimum, maximum, pattern. Unknown keywords ignored."""
import re

_T = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}

def _is(v, t):
    if t == "integer": return isinstance(v, int) and not isinstance(v, bool)
    if t == "number": return isinstance(v, (int, float)) and not isinstance(v, bool)
    return isinstance(v, _T[t])

def validate(v, schema, path="$"):
    errs = []
    t = schema.get("type")
    if t is not None:
        ts = t if isinstance(t, list) else [t]
        if not any(_is(v, x) for x in ts):
            return [f"{path}: expected {ts}, got {type(v).__name__}"]
    if "enum" in schema and v not in schema["enum"]: errs.append(f"{path}: {v!r} not in {schema['enum']}")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "minimum" in schema and v < schema["minimum"]: errs.append(f"{path}: {v} < min")
        if "maximum" in schema and v > schema["maximum"]: errs.append(f"{path}: {v} > max")
    if isinstance(v, str) and "pattern" in schema and not re.search(schema["pattern"], v): errs.append(f"{path}: pattern")
    if isinstance(v, dict):
        for r in schema.get("required", []):
            if r not in v: errs.append(f"{path}: missing '{r}'")
        for k, s in schema.get("properties", {}).items():
            if k in v: errs += validate(v[k], s, f"{path}.{k}")
    if isinstance(v, list) and "items" in schema:
        for i, x in enumerate(v): errs += validate(x, schema["items"], f"{path}[{i}]")
    return errs
