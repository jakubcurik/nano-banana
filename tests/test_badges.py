"""The badge generator: well-formed SVG, sensible widths, and every README badge file exists. Offline, standard library only."""
import importlib.util
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("make_badges", ROOT / ".github" / "scripts" / "make_badges.py")
make_badges = importlib.util.module_from_spec(spec)
spec.loader.exec_module(make_badges)


class BadgeTests(unittest.TestCase):
    def test_svg_is_well_formed_and_escaped(self):
        svg = make_badges.badge("a & b", "<1>")
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("a &amp; b", svg)

    def test_width_grows_with_text(self):
        short = float(ET.fromstring(make_badges.badge("a", "b")).get("width"))
        long = float(ET.fromstring(make_badges.badge("a long label", "a long value")).get("width"))
        self.assertGreater(long, short)

    def test_every_badge_file_is_valid(self):
        names = list(make_badges.STATIC) + ["release.svg", "stars.svg"]
        for name in names:
            path = ROOT / "assets" / "badges" / name
            self.assertTrue(path.is_file(), name)
            ET.fromstring(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
