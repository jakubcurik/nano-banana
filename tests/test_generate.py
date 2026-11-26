"""Offline tests: option validation, price maths and the model catalog. No API calls, no google-genai needed.

Run:  python -m unittest discover -s tests
"""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "gemini-image" / "scripts" / "generate.py"
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


if __name__ == "__main__":
    unittest.main()
