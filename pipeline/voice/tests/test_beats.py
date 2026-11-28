import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import beats


class TestBeats(unittest.TestCase):
    SIL = {"first_voiced_s": 0.1, "last_voiced_s": 6.0,
           "internal_pauses": [{"start_s": 2.0, "end_s": 2.4, "dur_s": 0.4}, {"start_s": 3.5, "end_s": 4.0, "dur_s": 0.5}]}

    def test_pauses_map_to_punctuation(self):
        r = beats.plan("One two three four, five six seven. Eight nine ten eleven twelve.", self.SIL)
        self.assertEqual(r["pauses_matched"], 2)
        self.assertEqual(len(r["sentences"]), 2)
        s0, s1 = r["sentences"]
        self.assertEqual((s0["t_on"], s0["t_off"]), (0.1, 3.5))
        self.assertEqual((s1["t_on"], s1["t_off"]), (4.0, 6.0))
        self.assertEqual(s1["frames_24"], [96, 144])

    def test_no_pauses_estimates_and_is_monotonic(self):
        r = beats.plan("Alpha beta, gamma delta. Epsilon zeta.", {"first_voiced_s": 0.0, "last_voiced_s": 3.0, "internal_pauses": []})
        ts = [c["t_on"] for c in r["clauses"]] + [r["clauses"][-1]["t_off"]]
        self.assertEqual(ts, sorted(ts))
        self.assertTrue(all(c["off_source"] in ("estimated", "measured") for c in r["clauses"]))


if __name__ == "__main__":
    unittest.main()
