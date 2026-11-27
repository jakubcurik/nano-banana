"""Offline tests for finish.py (exact size, web formats, transparent background).

They need Pillow and are skipped cleanly without it. CI installs Pillow so they run there.
"""
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "nano-banana" / "scripts" / "finish.py"
HAS_PILLOW = importlib.util.find_spec("PIL") is not None

if HAS_PILLOW:
    from PIL import Image

    spec = importlib.util.spec_from_file_location("finish", SCRIPT)
    finish = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(finish)


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with redirect_stdout(out), redirect_stderr(err):
        try:
            finish.main([str(a) for a in argv])
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def icon(size=100, background=(240, 240, 240)):
    """A red square with a background-colored hole in the middle, on a flat background."""
    image = Image.new("RGB", (size, size), background)
    image.paste((200, 20, 20), (25, 25, 75, 75))
    image.paste(background, (45, 45, 55, 55))
    return image


@unittest.skipUnless(HAS_PILLOW, "Pillow is not installed")
class ParseTests(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(finish.parse_size("1200x630"), (1200, 630))
        self.assertEqual(finish.parse_size("1200x"), (1200, None))
        self.assertEqual(finish.parse_size("x630"), (None, 630))
        for bad in ("x", "1200", "0x10", "abc"):
            with self.assertRaises(ValueError, msg=bad):
                finish.parse_size(bad)

    def test_colors(self):
        self.assertEqual(finish.parse_color("#F0f0f0"), (240, 240, 240))
        self.assertEqual(finish.parse_color("1,2,3"), (1, 2, 3))
        with self.assertRaises(ValueError):
            finish.parse_color("white")


@unittest.skipUnless(HAS_PILLOW, "Pillow is not installed")
class ImageTests(unittest.TestCase):
    def test_cover_fit_gives_exact_size_and_keeps_the_chosen_side(self):
        image = Image.new("RGB", (200, 100), "white")
        image.paste((0, 0, 255), (0, 0, 20, 100))  # blue stripe on the left
        left = finish.resize(image, 100, 100, "left")
        right = finish.resize(image, 100, 100, "right")
        self.assertEqual(left.size, (100, 100))
        self.assertEqual(left.getpixel((2, 50))[2], 255)
        self.assertEqual(right.getpixel((2, 50)), (255, 255, 255))

    def test_proportional_scale(self):
        self.assertEqual(finish.resize(Image.new("RGB", (2000, 1000)), 1000, None).size, (1000, 500))
        self.assertEqual(finish.resize(Image.new("RGB", (2000, 1000)), None, 250).size, (500, 250))

    def test_background_removed_but_enclosed_hole_kept(self):
        result, color, removed = finish.remove_background(icon())
        self.assertEqual(color, (240, 240, 240))
        self.assertEqual(result.mode, "RGBA")
        self.assertEqual(result.getpixel((5, 5))[3], 0)       # border-connected background: transparent
        self.assertEqual(result.getpixel((50, 50))[3], 255)   # same color inside the subject: kept
        self.assertEqual(result.getpixel((30, 30))[3], 255)   # subject: opaque
        self.assertAlmostEqual(removed, 1 - 0.25, places=1)

    def test_tolerance_covers_jpeg_noise(self):
        noisy = icon()
        noisy.putpixel((3, 3), (232, 247, 236))
        result, _, _ = finish.remove_background(noisy, tolerance=24)
        self.assertEqual(result.getpixel((3, 3))[3], 0)


@unittest.skipUnless(HAS_PILLOW, "Pillow is not installed")
class CommandTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.source = self.dir / "logo.jpg"
        icon(200).save(self.source, "JPEG", quality=95)

    def tearDown(self):
        self.tmp.cleanup()

    def test_resize_and_convert_next_to_the_input(self):
        code, out, _ = run(self.source, "--size", "120x63", "--format", "webp")
        self.assertEqual(code, 0, out)
        result = self.dir / "logo-120x63.webp"
        with Image.open(result) as image:
            self.assertEqual((image.format, image.size), ("WEBP", (120, 63)))

    def test_transparent_jpeg_input_becomes_png(self):
        code, out, _ = run(self.source, "--transparent")
        self.assertEqual(code, 0, out)
        with Image.open(self.dir / "logo-transparent.png") as image:
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getpixel((2, 2))[3], 0)

    def test_format_follows_the_output_name(self):
        code, _, _ = run(self.source, "--transparent", "-o", self.dir / "out" / "icon.webp")
        self.assertEqual(code, 0)
        with Image.open(self.dir / "out" / "icon.webp") as image:
            self.assertEqual((image.format, image.mode), ("WEBP", "RGBA"))

    def test_refusals(self):
        self.assertIn("transparency", str(run(self.source, "--transparent", "--format", "jpeg")[0]))
        self.assertIn("overwrite", str(run(self.source, "-o", self.source)[0]))
        self.assertIn("skill", str(run(self.source, "-o", SCRIPT.parent / "x.png")[0]))
        self.assertFalse((SCRIPT.parent / "x.png").exists())
        self.assertIn("not found", str(run(self.dir / "missing.png")[0]))


if __name__ == "__main__":
    unittest.main()
