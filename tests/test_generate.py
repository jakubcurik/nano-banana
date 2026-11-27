"""Offline tests: option validation, price maths and the model catalog. No API calls, no google-genai needed.

Run:  python -m unittest discover -s tests
"""
import base64
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
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
        required = {"id", "name", "sizes", "per_million_image_tokens", "per_million_text_tokens",
                    "per_million_input_tokens", "thinking", "search", "extreme_aspect_ratios", "max_input_images"}
        for key, model in generate.MODELS.items():
            self.assertTrue(required <= set(model), key)
            for size, price in model["sizes"].items():
                self.assertGreater(price["price"], 0, f"{key} {size}")
                if price["batch"] is not None:
                    self.assertLess(price["batch"], price["price"], f"{key} {size}")

    def test_per_image_price_matches_token_rate(self):
        # Google's per-image prices are image tokens times the image rate; 1K images are 1120 tokens.
        for key, model in generate.MODELS.items():
            if "1K" in model["sizes"]:
                self.assertAlmostEqual(1120 * model["per_million_image_tokens"] / 1e6,
                                       model["sizes"]["1K"]["price"], places=3, msg=key)


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


def interaction_usage(image=1120, text=0, thinking=1000, input_tokens=15):
    by_modality = [SimpleNamespace(modality="image", tokens=image)]
    if text:
        by_modality.append(SimpleNamespace(modality="text", tokens=text))
    return SimpleNamespace(total_input_tokens=input_tokens, output_tokens_by_modality=by_modality,
                           total_output_tokens=image + text, total_thought_tokens=thinking)


class CostTests(unittest.TestCase):
    def test_counts_from_interactions_usage(self):
        counts = generate.token_counts(interaction_usage(text=7))
        self.assertEqual(counts, {"input": 15, "image": 1120, "text": 7, "thinking": 1000})

    def test_counts_from_generate_content_usage(self):
        usage = SimpleNamespace(prompt_token_count=20, thoughts_token_count=300, candidates_token_count=1120,
                                candidates_tokens_details=[SimpleNamespace(modality="MediaModality.IMAGE",
                                                                           token_count=1120)])
        self.assertEqual(generate.token_counts(usage), {"input": 20, "image": 1120, "text": 0, "thinking": 300})

    def test_counts_without_modality_breakdown(self):
        usage = SimpleNamespace(total_input_tokens=10, output_tokens_by_modality=None,
                                total_output_tokens=1200, total_thought_tokens=None)
        self.assertEqual(generate.token_counts(usage), {"input": 10, "image": 0, "text": 1200, "thinking": 0})

    def test_no_usage(self):
        self.assertIsNone(generate.token_counts(None))

    def test_cost_adds_thinking_and_input(self):
        counts = generate.token_counts(interaction_usage())
        costs = generate.cost_usd(counts, generate.MODELS["2.1"])
        self.assertAlmostEqual(costs["image"], 0.0336)
        self.assertAlmostEqual(costs["text"], 1000 * 7.5 / 1e6)
        self.assertAlmostEqual(costs["input"], 15 * 1.5 / 1e6)
        batch = generate.cost_usd(counts, generate.MODELS["2.1"], batch=True)
        self.assertAlmostEqual(sum(batch.values()), sum(costs.values()) / 2)

    def test_print_usage_returns_total(self):
        response = interaction(usage=interaction_usage())
        with redirect_stdout(io.StringIO()) as out:
            total = generate.print_usage(response, generate.MODELS["2.1"], None, "USD")
        self.assertAlmostEqual(total, 0.0336 + 0.0075 + 0.0000225)
        self.assertIn("Real cost: 0.0411 USD", out.getvalue())
        with redirect_stdout(io.StringIO()):
            self.assertIsNone(generate.print_usage(interaction(), generate.MODELS["2.1"], None, "USD"))


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
