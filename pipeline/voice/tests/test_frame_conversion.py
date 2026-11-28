import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import seconds_to_frame


class TestFrameConversion(unittest.TestCase):
    def test_fixture_vectors(self):
        doc = json.load(open(os.path.join(HERE, "fixtures", "frame_conversion_vectors.json")))
        self.assertGreaterEqual(len(doc["cases"]), 30)
        for c in doc["cases"]:
            with self.subTest(t=c["t"], fps=c["fps"]):
                self.assertEqual(seconds_to_frame(float(c["t"]), c["fps"]), c["expected"], c["note"])

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
