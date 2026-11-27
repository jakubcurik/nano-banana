"""Offline tests: option validation, price maths and the model catalog. No API calls, no google-genai needed.

Run:  python -m unittest discover -s tests
"""
import base64
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "nano-banana" / "scripts" / "generate.py"
spec = importlib.util.spec_from_file_location("generate", SCRIPT)
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


def parse(*argv):
    args = generate.build_parser().parse_args(list(argv))
    args.size = args.size.upper()
    return args


class CheckTests(unittest.TestCase):
    def problems(self, *argv):
        args = parse(*argv)
        return generate.check(args, generate.MODELS[args.model])

    def test_defaults_are_valid(self):
        self.assertEqual(self.problems("a red apple"), [])

    def test_prompt_required(self):
        self.assertTrue(self.problems())

    def test_512_only_on_model_2(self):
        self.assertTrue(self.problems("x", "-s", "512"))
        self.assertEqual(self.problems("x", "-m", "2", "-s", "512"), [])

    def test_extreme_ratio_not_on_pro(self):
        self.assertTrue(self.problems("x", "-m", "pro", "-a", "1:8"))
        self.assertEqual(self.problems("x", "-m", "2.1", "-a", "1:8"), [])

    def test_thinking_levels_per_model(self):
        self.assertEqual(self.problems("x", "-t", "medium"), [])
        self.assertTrue(self.problems("x", "-m", "lite", "-t", "medium"))
        self.assertTrue(self.problems("x", "-m", "pro", "-t", "high"))

    def test_search_not_on_lite(self):
        self.assertTrue(self.problems("x", "-m", "lite", "--search"))

    def test_batch_rules(self):
        self.assertEqual(self.problems("x", "--batch"), [])
        self.assertTrue(self.problems("x", "--batch", "--follow-up"))
        self.assertTrue(self.problems("x", "--batch", "--format", "jpeg"))
        self.assertTrue(self.problems("x", "-m", "pro", "--batch"))  # no verified batch price

    def test_no_store_and_follow_up_conflict(self):
        self.assertTrue(self.problems("x", "--no-store", "--follow-up"))

    def test_too_many_and_missing_inputs(self):
        self.assertTrue(self.problems("x", "-i", "does-not-exist.png"))
        many = [item for _ in range(15) for item in ("-i", "does-not-exist.png")]
        self.assertTrue(any("At most 14" in p for p in self.problems("x", *many)))


class PriceTests(unittest.TestCase):
    def test_estimate_standard_and_batch(self):
        args = parse("x", "-n", "4")
        model = generate.MODELS["2.1"]
        self.assertAlmostEqual(generate.estimate_usd(args, model), 0.0336 * 4)
        args = parse("x", "-n", "4", "--batch")
        self.assertAlmostEqual(generate.estimate_usd(args, model), 0.0168 * 4)

    def test_usd_needs_no_network(self):
        self.assertEqual(generate.fx_rate("usd"), (1.0, "USD"))

    def test_money_formatting(self):
        self.assertEqual(generate.money(0.0336, (22.0, "CNB rate of 26.11.2026"), "CZK"),
                         "0.0336 USD (~ 0.74 CZK, CNB rate of 26.11.2026)")
        self.assertEqual(generate.money(0.0336, None, "EUR"), "0.0336 USD")


class CatalogTests(unittest.TestCase):
    def test_every_model_is_complete(self):
        required = {"id", "name", "sizes", "per_million_image_tokens", "thinking", "search",
                    "extreme_aspect_ratios", "max_input_images"}
        for key, model in generate.MODELS.items():
            self.assertTrue(required <= set(model), key)
            for size, price in model["sizes"].items():
                self.assertGreater(price["price"], 0, f"{key} {size}")
                if price["batch"] is not None:
                    self.assertLess(price["batch"], price["price"], f"{key} {size}")


class HelperTests(unittest.TestCase):
    def test_find_key_walks_nested_data(self):
        data = {"a": [{"search_suggestions": "<div>x</div>"}], "b": {"c": {"search_suggestions": "y"}}}
        self.assertEqual(sorted(generate.find_key(data, "search_suggestions")), ["<div>x</div>", "y"])


# ---------- fake API responses (shaped like google-genai 3.6 objects) ----------

def block(type_, **fields):
    return SimpleNamespace(type=type_, **fields)


def interaction(steps=(), output_image=None, **fields):
    defaults = {"id": "v1_abc", "usage": None, "output_text": None, "errors": None, "status": "completed"}
    defaults.update(fields)
    return SimpleNamespace(steps=list(steps), output_image=output_image, **defaults)


def gc_response(parts, usage=None):
    candidate = SimpleNamespace(content=SimpleNamespace(parts=parts))
    return SimpleNamespace(candidates=[candidate], usage_metadata=usage)


class ResponseParsingTests(unittest.TestCase):
    def test_interaction_images_skip_thoughts(self):
        response = interaction([
            block("thought", content=[block("image", data="THOUGHT", mime_type="image/png")]),
            block("model_output", content=[block("text", text="hi"),
                                           block("image", data="FINAL", mime_type="image/jpeg")]),
        ])
        self.assertEqual(generate.images_from_interaction(response), [("FINAL", "image/jpeg")])

    def test_interaction_falls_back_to_output_image(self):
        response = interaction([], output_image=SimpleNamespace(data="IMG", mime_type="image/png"))
        self.assertEqual(generate.images_from_interaction(response), [("IMG", "image/png")])

    def test_interaction_without_image(self):
        self.assertEqual(generate.images_from_interaction(interaction([block("model_output", content=None)])), [])

    def test_generate_content_images_skip_thoughts(self):
        parts = [SimpleNamespace(thought=True, inline_data=SimpleNamespace(data=b"T", mime_type="image/png")),
                 SimpleNamespace(thought=False, inline_data=None, text="caption"),
                 SimpleNamespace(thought=None, inline_data=SimpleNamespace(data=b"I", mime_type="image/png"))]
        self.assertEqual(generate.images_from_generate_content(gc_response(parts)), [(b"I", "image/png")])

    def test_generate_content_without_candidates(self):
        self.assertEqual(generate.images_from_generate_content(SimpleNamespace(candidates=None)), [])

    def test_search_suggestions_are_deduplicated(self):
        dump = {"result": [{"search_suggestions": "<div>s</div>"}, {"search_suggestions": "<div>s</div>"}]}
        step = SimpleNamespace(type="google_search_result", model_dump=lambda: dump)
        self.assertEqual(generate.suggestions_from_interaction(interaction([step])), ["<div>s</div>"])


class FileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_image_decodes_base64_and_picks_extension(self):
        path = generate.save_image(base64.b64encode(b"jpegdata").decode(), "image/jpeg", "A red apple!", self.dir, 0)
        self.assertEqual(path.suffix, ".jpg")
        self.assertIn("a-red-apple", path.name)
        self.assertEqual(path.read_bytes(), b"jpegdata")

    def test_sidecar_holds_prompt_options_and_id(self):
        image = self.dir / "x.png"
        args = parse("A red apple", "-a", "16:9", "--search")
        generate.save_sidecar(image, args, "v1_new", "v1_old", ["<div>s</div>"])
        text = image.with_suffix(".txt").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# model 2.1 | 1K | aspect 16:9 | with search | follows v1_old | id v1_new"))
        self.assertIn("\nA red apple\n", text)
        self.assertIn("<div>s</div>", text)


if __name__ == "__main__":
    unittest.main()
