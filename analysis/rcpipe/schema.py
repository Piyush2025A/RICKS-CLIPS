"""Minimal JSON-Schema validator (draft 2020-12 subset used by our schemas); jsonschema is not installed."""
import re


def validate(obj, schema, path="$"):
    errs = []
    t = schema.get("type")
    tm = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool}
    if t and not (isinstance(obj, tm[t]) and not (t in ("integer", "number") and isinstance(obj, bool))):
        return [f"{path}: expected {t}, got {type(obj).__name__}"]
    if "enum" in schema and obj not in schema["enum"]:
        errs.append(f"{path}: {obj!r} not in enum")
    if "pattern" in schema and isinstance(obj, str) and not re.search(schema["pattern"], obj):
        errs.append(f"{path}: {obj!r} !~ {schema['pattern']}")
    if isinstance(obj, dict):
        for k in schema.get("required", []):
            if k not in obj:
                errs.append(f"{path}: missing required {k}")
        props = schema.get("properties", {})
        for k, v in obj.items():
            if k in props:
                errs += validate(v, props[k], f"{path}.{k}")
            elif isinstance(schema.get("additionalProperties"), dict):
                errs += validate(v, schema["additionalProperties"], f"{path}.{k}")
    if isinstance(obj, list) and "items" in schema:
        for i, v in enumerate(obj):
            errs += validate(v, schema["items"], f"{path}[{i}]")
    return errs
