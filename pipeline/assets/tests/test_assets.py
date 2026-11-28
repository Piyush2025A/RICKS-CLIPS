"""Run: .venv-analysis/bin/python -I -m unittest discover -s pipeline/assets/tests (pytest also works if installed)."""
import io, json, os, struct, sys, tempfile, unittest, zlib, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from PIL import Image
import assetlib as L, intake, verify

SCHEMA = json.load(open(os.path.join(os.path.dirname(HERE), "schemas", "asset-provenance.schema.json")))
TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list, "null": type(None)}


def check(inst, sch, path="$"):
    """Minimal JSON-Schema subset validator (jsonschema not installed): type/required/properties/enum/const/items/minItems/pattern."""
    import re
    errs = []
    t = sch.get("type")
    if t:
        ts = t if isinstance(t, list) else [t]
        if not any(isinstance(inst, TYPES[x]) and not (x in ("integer", "number") and isinstance(inst, bool)) for x in ts):
            return [f"{path}: type {type(inst).__name__} not in {ts}"]
    if "enum" in sch and inst not in sch["enum"]: errs.append(f"{path}: not in enum")
    if "const" in sch and inst != sch["const"]: errs.append(f"{path}: const")
    if "pattern" in sch and not re.search(sch["pattern"], inst): errs.append(f"{path}: pattern")
    if isinstance(inst, dict):
        for r in sch.get("required", []):
            if r not in inst: errs.append(f"{path}: missing {r}")
        for k, s in sch.get("properties", {}).items():
            if k in inst: errs += check(inst[k], s, f"{path}.{k}")
    if isinstance(inst, list):
        if len(inst) < sch.get("minItems", 0): errs.append(f"{path}: minItems")
        if "items" in sch:
            for i, x in enumerate(inst): errs += check(x, sch["items"], f"{path}[{i}]")
    return errs


def add_chunk_after_ihdr(png_bytes, typ, data):
    chunk = struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    i = 8 + 12 + 13
    return png_bytes[:i] + chunk + png_bytes[i:]


def run(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = intake.main(argv)
    return rc, json.loads(buf.getvalue())


class T(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory(); self.d = self.td.name
        self.store = os.path.join(self.d, "store")
        self.src = os.path.join(self.d, "src"); os.makedirs(self.src)
        # RGBA 10x10: left 4 cols transparent (alpha 0), col 4 semi (128), rest opaque
        a = np.full((10, 10), 255, np.uint8); a[:, :4] = 0; a[:, 4] = 128
        rgba = np.dstack([np.full((10, 10, 3), 200, np.uint8), a])
        self.rgba = os.path.join(self.src, "Test_Char_deadbeef.png"); Image.fromarray(rgba, "RGBA").save(self.rgba)
        self.rgb = os.path.join(self.src, "rgb.png"); Image.new("RGB", (8, 6), (1, 2, 3)).save(self.rgb)
        self.jpg = os.path.join(self.src, "photo.jpg"); Image.new("RGB", (16, 16), (9, 9, 9)).save(self.jpg)
        data = open(self.rgba, "rb").read()
        self.c2pa = os.path.join(self.src, "c2pa.png")
        open(self.c2pa, "wb").write(add_chunk_after_ihdr(data, b"caBX", b"\x00" * 100))
        self.txt = os.path.join(self.src, "notes.txt"); open(self.txt, "w").write("hi")

    def tearDown(self): self.td.cleanup()

    def common(self, f, kind="character", rid="R1"):
        return [f, "--kind", kind, "--request-id", rid, "--store", self.store, "--date", "20261128"]

    def test_rgba_alpha_stats_and_copy(self):
        before = L.sha256_file(self.rgba); mt = os.stat(self.rgba).st_mtime_ns
        rc, r = run(self.common(self.rgba) + ["--provider", "google-flow", "--model", "m", "--settings-json", '{"a":1}'])
        self.assertEqual(rc, 0); self.assertEqual(r["status"], "intaken")
        self.assertEqual(L.sha256_file(r["stored_path"]), before)
        self.assertEqual(open(r["stored_path"], "rb").read(), open(self.rgba, "rb").read())
        self.assertEqual(os.stat(self.rgba).st_mtime_ns, mt)  # original untouched
        self.assertTrue(r["stored_path"].endswith("character/20261128_R1_test-char_v01.png"))
        s = json.load(open(r["sidecar"]))
        al = s["technical"]["alpha"]
        self.assertAlmostEqual(al["fraction_transparent"], 0.4); self.assertAlmostEqual(al["fraction_semi_transparent"], 0.1)
        self.assertAlmostEqual(al["fraction_opaque"], 0.5); self.assertEqual(al["bbox_nonzero_xywh_exclusive"], [4, 0, 10, 10])
        self.assertEqual(s["technical"]["mode"], "RGBA"); self.assertEqual(s["technical"]["bit_depth"], 8)
        self.assertEqual(check(s, SCHEMA), [])

    def test_rgb_no_alpha(self):
        rc, r = run(self.common(self.rgb, "prop")); s = json.load(open(r["sidecar"]))
        self.assertFalse(s["technical"]["has_alpha_channel"]); self.assertIsNone(s["technical"]["alpha"])
        self.assertEqual(check(s, SCHEMA), [])

    def test_fake_c2pa_chunk_preserved(self):
        rc, r = run(self.common(self.c2pa)); s = json.load(open(r["sidecar"]))
        self.assertTrue(s["protection"]["c2pa_chunk_present"])
        self.assertEqual(s["technical"]["c2pa_chunks"], [{"type": "caBX", "length": 100}])
        self.assertTrue(s["technical"]["png_chunks_crc_all_ok"])
        self.assertEqual(open(r["stored_path"], "rb").read(), open(self.c2pa, "rb").read())

    def test_jpeg(self):
        rc, r = run(self.common(self.jpg, "texture")); s = json.load(open(r["sidecar"]))
        self.assertEqual(s["technical"]["format"], "jpeg"); self.assertFalse(s["technical"]["has_alpha_channel"])
        self.assertFalse(s["technical"]["exif_present"])

    def test_idempotent(self):
        run(self.common(self.rgb)); rc, r = run(self.common(self.rgb, rid="R2"))
        self.assertEqual(r["status"], "already_intaken")
        self.assertEqual(len(L.read_ledger(os.path.join(self.store, "INTAKE_LEDGER.jsonl"))), 1)

    def test_versioning_distinct_content(self):
        run(self.common(self.rgb))
        other = os.path.join(self.src, "rgb.png"); Image.new("RGB", (8, 6), (9, 9, 9)).save(os.path.join(self.src, "x", "rgb.png") if False else other)
        rc, r = run(self.common(other)); self.assertTrue(r["stored_path"].endswith("_v02.png"))

    def test_refusals(self):
        rc, r = run(self.common(self.txt)); self.assertEqual(rc, 2)
        rc, r = run(self.common(self.txt) + ["--force-type"]); self.assertEqual(rc, 0)
        big = os.path.join(self.src, "big.png")
        with open(big, "wb") as f: f.write(L.PNG_SIG); f.truncate(L.MAX_BYTES + 1)
        rc, r = run(self.common(big)); self.assertEqual(rc, 2); self.assertIn("50 MB", r["error"])

    def test_verify_detects_tamper_and_roundtrip(self):
        rc, r = run(self.common(self.rgb))
        self.assertEqual(verify.audit(self.store, record=True), {"ok": 1, "problems": []})
        s = json.load(open(r["sidecar"])); self.assertEqual(s["chain_of_custody"][-1]["event"], "verified")
        self.assertEqual(check(s, SCHEMA), [])
        with open(r["stored_path"], "ab") as f: f.write(b"x")
        res = verify.audit(self.store); self.assertEqual(res["problems"][0]["problem"], "ledger_hash_mismatch")
        open(os.path.join(self.store, "character", "stray.png"), "wb").write(b"1")
        self.assertIn("not_in_ledger", [p["problem"] for p in verify.audit(self.store)["problems"]])

    def test_verify_check_file(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(verify.main(["--check", self.rgb, "--expect-sha256", L.sha256_file(self.rgb)]), 0)
            self.assertEqual(verify.main(["--check", self.rgb, "--expect-sha256", "0" * 64]), 1)

    def test_events(self):
        rc, r = run(self.common(self.rgb) + ["--generated-utc", "2026-11-27T15:06:14Z", "--event", "transferred_via_drive|2026-11-27T16:00:00Z|ok"])
        ev = [e["event"] for e in json.load(open(r["sidecar"]))["chain_of_custody"]]
        self.assertEqual(ev, ["generated", "intaken", "transferred_via_drive"])


if __name__ == "__main__":
    unittest.main()
