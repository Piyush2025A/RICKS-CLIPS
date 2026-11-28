"""A20 voice pipeline tests. Run: .venv-analysis/bin/python -I -m unittest discover -s pipeline/voice/tests -v
Audio is synthesised at test time into a temp dir (no audio is committed)."""
import json, os, sys, tempfile, unittest
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); VOICE = os.path.dirname(HERE)
sys.path.insert(0, VOICE); sys.path.insert(0, HERE)
import align, captions, silence, normalize, schemacheck
from common import seconds_to_frame as frames, decode_audio

FX = os.path.join(HERE, "fixtures")
def fx(n): return json.load(open(os.path.join(FX, n), encoding="utf-8"))
def schema(n): return json.load(open(os.path.join(VOICE, "schemas", n)))
def W(word, a, b, i=0): return {"index": i, "word": word, "t_on": a, "t_off": b, "char_start": 0, "char_end": 0, "source": "scribe", "confidence": 1.0}
SR = 48000

def write_wav(path, x, sr=SR):
    import soundfile as sf
    sf.write(path, x.astype(np.float32), sr, subtype="PCM_24")

class TestCharAlignment(unittest.TestCase):
    def setUp(self):
        j = fx("char_alignment_edge.json")["alignment"]
        self.j = j; self.text = "".join(j["characters"])
        self.words = align.chars_to_words(j["characters"], j["character_start_times_seconds"], j["character_end_times_seconds"])

    def test_tokens(self):
        self.assertEqual([w["word"] for w in self.words],
            ["Hello,", "world!", "It's", "a", "well-known", "3.5", "rate—", "really.", "Dug", "a", "hole", "now...", "end."])

    def test_tags_removed(self):
        joined = " ".join(w["word"] for w in self.words)
        self.assertNotIn("whispers", joined); self.assertNotIn("break", joined)

    def test_spans_and_times(self):
        for w in self.words:
            self.assertEqual(self.text[w["char_start"]:w["char_end"]].replace(" ", ""), w["word"])
        h = self.words[0]; i = self.text.index("Hello")
        self.assertAlmostEqual(h["t_on"], 0.2 + i * 0.05, places=3)          # leading spaces skipped, zero-length char ignored
        self.assertAlmostEqual(h["t_off"], 0.2 + (i + 6) * 0.05, places=3)   # trailing comma included
        self.assertEqual(align.validate_words(self.words, 99.0), [])

    def test_leading_trailing_spaces_and_zero_length(self):
        w = align.chars_to_words([" ", "H", "i", "!", " "], [0, .1, .2, .3, .4], [0, .2, .3, .4, .4])
        self.assertEqual([(x["word"], x["t_on"], x["t_off"]) for x in w], [("Hi!", 0.1, 0.4)])

    def test_missing_timestamps_filled(self):
        w = align.chars_to_words(list("ab cd"), [0.0, None, 0.2, 0.3, None], [0.1, None, 0.3, 0.4, None])
        self.assertEqual(len(w), 2); self.assertEqual(w[1]["t_on"], 0.3)

    def test_standalone_punctuation_and_dash(self):
        w = align.chars_to_words(list("Wait — what ?"), [i * .1 for i in range(13)], [i * .1 + .1 for i in range(13)])
        self.assertEqual([x["word"] for x in w], ["Wait—", "what?"])
        self.assertEqual([t[0] for t in align.tokenise("\u2014 Hi there")], ["\u2014Hi", "there"])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError): align.chars_to_words(["a"], [0.0], [])

    def test_multichar_and_empty_entries(self):
        w = align.chars_to_words(["He", "", "llo", " ", "x"], [0, 0.1, 0.1, 0.3, 0.4], [0.1, 0.1, 0.3, 0.4, 0.5])
        self.assertEqual([x["word"] for x in w], ["Hello", "x"]); self.assertEqual(w[0]["t_off"], 0.3)

class TestScribe(unittest.TestCase):
    def test_types_filtered(self):
        tw = align.scribe_words(fx("scribe_sample.json"))
        self.assertEqual(len(tw), 11); self.assertNotIn("(sniff)", [t[0] for t in tw]); self.assertNotIn(" ", [t[0] for t in tw])

    def test_no_script(self):
        w, rep = align.scribe_to_words(fx("scribe_sample.json"))
        self.assertEqual(len(w), 11); self.assertEqual(w[0]["char_start"], -1); self.assertEqual(w[0]["source"], "scribe")
        self.assertLess(w[0]["t_on"], w[1]["t_on"])

    def test_drift_vs_script(self):
        script = open(os.path.join(FX, "script_sample.txt"), encoding="utf-8").read()
        w, rep = align.scribe_to_words(fx("scribe_sample.json"), script)
        self.assertEqual([x["word"] for x in w], ["It", "was", "a", "cold", "morning.", "The", "kettle", "sang,", "then", "stopped!"])
        kinds = {(m["kind"], m.get("script") or m.get("transcript")) for m in rep["mismatches"]}
        self.assertIn(("substituted", "morning."), kinds); self.assertIn(("extra", "really"), kinds)
        self.assertEqual(w[4]["flags"], ["substituted"]); self.assertLessEqual(w[4]["confidence"], 0.5)
        self.assertEqual(script[w[4]["char_start"]:w[4]["char_end"]], "morning.")
        self.assertAlmostEqual(w[5]["t_on"], 1.80); self.assertEqual(rep["matched"], 9)
        self.assertEqual(align.validate_words(w, 4.0), [])

    def test_missing_word_interpolated(self):
        doc = [{"text": "one", "start": 0.0, "end": 0.3, "type": "word"}, {"text": "three", "start": 0.9, "end": 1.2, "type": "word"}]
        w, rep = align.scribe_to_words(doc, "one two three")
        self.assertEqual(w[1]["flags"], ["interpolated"]); self.assertEqual(w[1]["confidence"], 0.0)
        self.assertTrue(0.3 <= w[1]["t_on"] < w[1]["t_off"] <= 0.9); self.assertEqual(rep["mismatches"][0]["kind"], "missing")

    def test_case_and_punct_insensitive(self):
        doc = [{"text": "Don’t", "start": 0.0, "end": 0.3, "type": "word"}]
        w, rep = align.scribe_to_words(doc, "don't!"); self.assertEqual(rep["matched"], 1)

class TestValidation(unittest.TestCase):
    def test_issues_and_repair(self):
        ws = [W("a", 0.0, 0.5), W("b", 0.4, 0.8), W("c", 0.3, 0.6), W("d", 0.9, 2.5)]
        issues = align.validate_words(ws, 2.0)
        self.assertTrue(any("overlaps" in i for i in issues)); self.assertTrue(any("monotonic" in i for i in issues))
        self.assertTrue(any("beyond duration" in i for i in issues))
        fixed = align.repair_words(ws, 2.0)
        self.assertEqual(align.validate_words(fixed, 2.0), []); self.assertIn("repaired", fixed[1]["flags"])
    def test_clean(self):
        self.assertEqual(align.validate_words([W("a", 0, .2), W("b", .2, .4)], .4), [])

def words_fx(items): return [W(w, a, b, i) for i, (w, a, b) in enumerate(items)]

class TestCaptions(unittest.TestCase):
    def test_lead_frames_30_and_24(self):
        ws = words_fx([("Hello", 1.0, 1.4)])
        for fps, lead_f in ((30, 4), (24, 3)):
            c, _ = captions.schedule(ws, 3.0, fps)
            self.assertEqual(frames(1.0, fps) - c[0]["frame_in"], lead_f, fps)
            self.assertAlmostEqual(c[0]["show_at"], 0.86)
        self.assertEqual((frames(0.14, 30), frames(0.14, 24)), (4, 3))

    def test_clamp_at_zero(self):
        c, _ = captions.schedule(words_fx([("Go", 0.05, 0.3)]), 2.0, 30)
        self.assertEqual(c[0]["show_at"], 0.0); self.assertEqual(c[0]["frame_in"], 0)

    def test_never_blank(self):
        ws = words_fx([("one", 0.5, 0.8), ("two", 1.4, 1.7), ("three,", 1.75, 2.0), ("four", 2.9, 3.2), ("end.", 3.3, 3.6)])
        for fps in (30, 24):
            c, _ = captions.schedule(ws, 4.5, fps)
            for a, b in zip(c, c[1:]): self.assertEqual(a["frame_out"], b["frame_in"])
            self.assertTrue(all(x["frame_out"] > x["frame_in"] for x in c))
            for a, b in zip(c, c[1:]): self.assertEqual(a["hide_at"], b["show_at"])

    def test_sentence_hold(self):
        ws = words_fx([("done.", 1.0, 1.5), ("Next", 1.7, 2.0)])      # next lead would show at 1.56 < t_off + 0.1667
        c, _ = captions.schedule(ws, 3.0, 30)
        self.assertTrue(c[0]["sentence_final"]); self.assertAlmostEqual(c[0]["hide_at"] - 1.5, 5 / 30, places=3)
        self.assertEqual(frames(c[0]["hide_at"], 30) - frames(1.5, 30), 5)
        self.assertLessEqual(c[1]["show_at"], 1.7)
        # next onset arrives within the hold: shown at onset, no overlap
        ws2 = words_fx([("done.", 1.0, 1.5), ("Next", 1.6, 2.0)])
        c2, _ = captions.schedule(ws2, 3.0, 30); self.assertAlmostEqual(c2[1]["show_at"], 1.6)

    def test_last_token_hold_and_duration_clamp(self):
        c, _ = captions.schedule(words_fx([("end.", 2.7, 2.95)]), 3.0, 30)
        self.assertAlmostEqual(c[-1]["hide_at"], 3.0); self.assertEqual(c[-1]["frame_out"], 90)
        c, _ = captions.schedule(words_fx([("end.", 1.0, 1.3)]), 3.0, 24)
        self.assertEqual(c[-1]["frame_out"] - frames(1.3, 24), 4)             # 5 f @30 = 0.1667 s = 4 f @24

    def test_fast_words_min_show(self):
        ws = words_fx([("a", 0.0, 0.04), ("b", 0.05, 0.1), ("c", 0.11, 0.2)])
        c, w = captions.schedule(ws, 3.0, 30)
        self.assertTrue(all(x["frame_out"] > x["frame_in"] for x in c)); self.assertTrue(w)

    def test_merge_function_words(self):
        ws = words_fx([("We", 0.5, 0.6), ("dug", 0.6, 0.9), ("a", 1.0, 1.1), ("hole.", 1.1, 1.5)])
        self.assertEqual([t["token"] for t in captions.make_tokens(ws)], ["We", "dug", "a", "hole."])
        self.assertEqual([t["token"] for t in captions.make_tokens(ws, True)], ["We dug", "a hole."])

    def test_schema_and_srt(self):
        wd = {"duration_s": 3.0, "words": words_fx([("Hi", 0.5, 0.7), ("there.", 0.8, 1.2)])}
        d = captions.build_doc(wd, 24)
        self.assertEqual(schemacheck.validate(d, schema("captions.schema.json")), [])
        self.assertIn("00:00:00,", captions.to_srt(d)); self.assertEqual(d["total_frames"], 72)

class TestSchemas(unittest.TestCase):
    def test_words_doc(self):
        j = fx("char_alignment_edge.json")["alignment"]
        ws = align.chars_to_words(j["characters"], j["character_start_times_seconds"], j["character_end_times_seconds"])
        d = align.build_doc(ws, "api_alignment", "".join(j["characters"]), 30.0, "b" * 64)
        self.assertEqual(schemacheck.validate(d, schema("words.schema.json")), [])
        ws2, rep = align.scribe_to_words(fx("scribe_sample.json"), "It was a cold morning.")
        self.assertEqual(schemacheck.validate(align.build_doc(ws2, "scribe", None, 4.0, None, rep), schema("words.schema.json")), [])
    def test_manifest(self):
        self.assertEqual(schemacheck.validate(fx("manifest_sample.json"), schema("narration.manifest.schema.json")), [])
        bad = fx("manifest_sample.json"); del bad["audio"]["sha256"]; bad["voice"]["origin"] = "cloned"
        self.assertEqual(len(schemacheck.validate(bad, schema("narration.manifest.schema.json"))), 2)
    def test_schemas_are_json(self):
        for n in os.listdir(os.path.join(VOICE, "schemas")): schema(n)

class TestSilence(unittest.TestCase):
    def test_tone_and_gap(self):
        t = lambda d: np.arange(int(d * SR)) / SR
        tone = lambda d: 0.3 * np.sin(2 * np.pi * 220 * t(d))
        z = lambda d: np.zeros(int(d * SR))
        x = np.concatenate([z(0.5), tone(1.0), z(0.7), tone(1.0), z(0.4)])
        r = silence.analyse(x, SR)
        self.assertAlmostEqual(r["lead_silence_s"], 0.5, delta=0.02); self.assertAlmostEqual(r["tail_silence_s"], 0.4, delta=0.02)
        self.assertEqual(len(r["internal_pauses"]), 1); self.assertAlmostEqual(r["internal_pauses"][0]["dur_s"], 0.7, delta=0.03)
        self.assertEqual(len(r["warnings"]), 1)
        p = r["trim_plan"]; self.assertAlmostEqual(p["trim_start_s"], 0.3, delta=0.02)
        self.assertAlmostEqual(p["trim_end_s"], 3.6 - 0.1, delta=0.02)        # keep 0.3 of 0.4 tail
        # via file + ffmpeg decode
        with tempfile.TemporaryDirectory() as td:
            f = os.path.join(td, "t.wav"); write_wav(f, x)
            y, sr = decode_audio(f); r2 = silence.analyse(y, sr); self.assertAlmostEqual(r2["lead_silence_s"], 0.5, delta=0.02)

    def test_short_edges_untrimmed_and_silent_file(self):
        x = np.concatenate([np.zeros(int(0.1 * SR)), 0.3 * np.sin(np.arange(SR) * 0.1), np.zeros(int(0.2 * SR))])
        p = silence.analyse(x, SR)["trim_plan"]; self.assertEqual(p["trim_start_s"], 0.0)
        self.assertFalse(silence.analyse(np.zeros(SR), SR)["voiced"])

def noise_bursts(seconds=8.0, level=0.1, seed=1):
    rng = np.random.default_rng(seed); n = int(seconds * SR); x = np.zeros(n)
    t = 0.2
    while t < seconds - 1.0:
        a, d = int(t * SR), int(rng.uniform(0.6, 1.0) * SR)
        env = np.hanning(d) ** 0.3 * rng.uniform(0.7, 1.0)
        x[a:a + d] = rng.standard_normal(d) * level * env; t += d / SR + rng.uniform(0.2, 0.4)
    return x

class TestLoudness(unittest.TestCase):
    def test_vo_normalises_to_minus14(self):
        with tempfile.TemporaryDirectory() as td:
            src, dst = os.path.join(td, "in.wav"), os.path.join(td, "out.wav")
            write_wav(src, noise_bursts(level=0.03)); before = normalize.measure(src)
            self.assertLess(before["I"], -25)
            r = normalize.normalize_vo(src, dst)
            self.assertAlmostEqual(r["result"]["I"], -14.0, delta=0.5)
            self.assertLessEqual(r["result"]["TP"], -2.0 + 0.2)
            y, sr = decode_audio(dst); self.assertEqual(sr, SR)
            import soundfile as sf; self.assertEqual(sf.info(dst).channels, 1)
            with self.assertRaises(FileExistsError): normalize.normalize_vo(src, dst)         # never overwrite
            with self.assertRaises(FileExistsError): normalize.normalize_vo(src, src)
            self.assertAlmostEqual(normalize.measure(src)["I"], before["I"], places=1)       # input untouched

    def test_mix_bed_minus20_and_master(self):
        with tempfile.TemporaryDirectory() as td:
            vo = os.path.join(td, "vo.wav"); bed = os.path.join(td, "bed.wav"); out = os.path.join(td, "mix.wav")
            write_wav(vo, noise_bursts(seconds=8.0, level=0.1))
            tt = np.arange(3 * SR) / SR                                    # 3 s bed, must loop to 8 s
            write_wav(bed, 0.2 * np.sin(2 * np.pi * 800 * tt) + 0.1 * np.sin(2 * np.pi * 1300 * tt))
            r = normalize.mix_with_bed(vo, bed, out)
            self.assertAlmostEqual(r["bed_band_db"] - r["vo_band_db"], -20.0, delta=0.1)
            self.assertAlmostEqual(r["result"]["I"], -14.0, delta=0.5)
            import soundfile as sf; info = sf.info(out)
            self.assertEqual((info.channels, info.samplerate), (2, SR)); self.assertAlmostEqual(info.duration, 8.0, delta=0.05)

if __name__ == "__main__":
    unittest.main()
