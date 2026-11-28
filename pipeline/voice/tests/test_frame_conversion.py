import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import seconds_to_frame, duration_frames_covering


class TestFrameConversion(unittest.TestCase):
    def test_fixture_vectors(self):
        doc = json.load(open(os.path.join(HERE, "fixtures", "frame_conversion_vectors.json")))
        self.assertGreaterEqual(len(doc["cases"]), 30)
        for c in doc["cases"]:
            with self.subTest(t=c["t"], fps=c["fps"]):
                self.assertEqual(seconds_to_frame(float(c["t"]), c["fps"]), c["expected"], c["note"])

    def test_duration_vectors(self):
        doc = json.load(open(os.path.join(HERE, "fixtures", "frame_conversion_vectors.json")))
        self.assertGreaterEqual(len(doc["duration_cases"]), 15)
        for c in doc["duration_cases"]:
            with self.subTest(t=c["t"], fps=c["fps"]):
                self.assertEqual(duration_frames_covering(float(c["t"]), c["fps"]), c["expected"], c["note"])

    def test_duration_examples_and_validation(self):
        self.assertEqual(duration_frames_covering(7.058875, 24), 170)
        self.assertEqual((duration_frames_covering(2.0, 24), duration_frames_covering(7.0, 30)), (48, 210))
        self.assertEqual(duration_frames_covering(0, 30), 0)
        for t in (-0.001, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                duration_frames_covering(t, 30)
        with self.assertRaises(ValueError):
            duration_frames_covering(1.0, 29.97)

    def test_tie_2_55_at_30_is_77(self):
        self.assertEqual(seconds_to_frame(2.55, 30), 77)

    def test_ties_go_up(self):
        self.assertEqual((seconds_to_frame(0.0625, 24), seconds_to_frame(0.1875, 24)), (2, 5))

    def test_rejects_bad_input(self):
        for t in (-0.001, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                seconds_to_frame(t, 30)
        with self.assertRaises(ValueError):
            seconds_to_frame(1.0, 29.97)


if __name__ == "__main__":
    unittest.main()
