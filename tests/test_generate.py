"""Offline tests: option validation, price maths and the model catalog. No API calls, no google-genai needed.

Run:  python -m unittest discover -s tests
"""
import base64
import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "nano-banana" / "scripts" / "generate.py"
spec = importlib.util.spec_from_file_location("generate", SCRIPT)
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


NO_CONFIG = Path(__file__).resolve().parent / "no-such-config.json"
CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith("NANO_BANANA_")}


def parse(*argv):
    args = generate.build_parser().parse_args(list(argv))
    generate.apply_settings(args, env={}, config_file=NO_CONFIG)
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

    def test_counts_output_missing_from_the_modality_list(self):
        # Shape of a real 2.1 response (28 Nov 2026): only image tokens are listed per modality.
        usage = SimpleNamespace(total_input_tokens=15, output_tokens_by_modality=[
            SimpleNamespace(modality="image", tokens=1120)], total_output_tokens=1385, total_thought_tokens=642)
        self.assertEqual(generate.token_counts(usage), {"input": 15, "image": 1120, "text": 265, "thinking": 642})

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


PNG_B64 = base64.b64encode(b"\x89PNG fake").decode()


def image_response(n):
    return interaction([block("model_output", content=[block("image", data=PNG_B64, mime_type="image/png")])],
                       id=f"v1_{n}", usage=interaction_usage())


class FakeInteractions:
    """Stands in for client.interactions: returns or raises the queued outcomes in order."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = []
        self.deleted = []

    def create(self, **params):
        self.calls.append(params)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    def delete(self, id):
        self.deleted.append(id)


def fake_client(*outcomes):
    return SimpleNamespace(interactions=FakeInteractions(*outcomes))


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_count(self, client, *argv):
        args = parse("A red apple", *argv)
        model = generate.MODELS[args.model]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = generate.run_interactions(client, args, model, [], None, self.dir, None,
                                             generate.estimate_usd(args, model))
        return code, out.getvalue(), err.getvalue()

    def test_all_images_saved(self):
        code, out, _ = self.run_count(fake_client(image_response(1), image_response(2)), "-n", "2")
        self.assertEqual(code, 0)
        self.assertEqual(out.count("Saved: "), 2)
        self.assertIn("Total for this run:", out)
        self.assertIn("Done: 2 of 2 images saved.", out)
        self.assertIn("Image 1 of 2: the API answered in", out)
        sidecar = next(self.dir.glob("*-1.txt")).read_text(encoding="utf-8")
        self.assertRegex(sidecar, r"\| took \d+\.\d s \| cost 0\.0411 USD\n")
        self.assertEqual((self.dir / generate.LAST_ID_FILE).read_text(encoding="utf-8"), "v1_2")

    def test_failure_keeps_earlier_images_and_stops(self):
        client = fake_client(image_response(1), image_response(2), RuntimeError("boom"), image_response(4))
        code, out, err = self.run_count(client, "-n", "4")
        self.assertEqual(code, 1)
        self.assertEqual(len(client.interactions.calls), 3)  # stopped after the failure
        self.assertEqual(len(list(self.dir.glob("*.png"))), 2)
        first_saved = out.index("Saved: ")
        self.assertLess(first_saved, out.index("Real cost"))  # printed as soon as the file exists
        self.assertRegex(err, r"Image 3 of 4 failed after \d+\.\d s: RuntimeError: boom")
        self.assertIn("Retry: Unexpected error: the outcome is uncertain", err)
        self.assertIn("1 more image(s) were not attempted", err)
        self.assertIn("2 of 4 images saved", err)

    def test_no_image_is_a_problem_but_the_run_goes_on(self):
        refused = interaction([], id="v1_x", output_text="I can't make that.", usage=interaction_usage(image=0))
        code, out, err = self.run_count(fake_client(refused, image_response(2)), "-n", "2")
        self.assertEqual(code, 1)
        self.assertIn("returned no image", err)
        self.assertEqual(out.count("Saved: "), 2)  # once when saved, once in the summary

    def test_interrupt_ends_cleanly(self):
        code, _, err = self.run_count(fake_client(KeyboardInterrupt()))
        self.assertEqual(code, 130)
        self.assertIn("interrupted", err)


def run_main(*argv):
    """generate.main() with captured output: (exit code or message, stdout, stderr). Never calls the API."""
    out, err = io.StringIO(), io.StringIO()
    result = 0
    with redirect_stdout(out), redirect_stderr(err), patch.object(generate, "CONFIG_FILE", NO_CONFIG), \
            patch.dict(os.environ, CLEAN_ENV, clear=True):
        try:
            generate.main(list(argv))
        except SystemExit as exc:
            result = exc.code
    return result, out.getvalue(), err.getvalue()


class CostGuardTests(unittest.TestCase):
    def test_within_the_limit(self):
        self.assertIsNone(generate.cost_guard(0.50, 0.50))
        self.assertIsNone(generate.cost_guard(0.0336 * 4, 0.50))

    def test_above_the_limit_names_price_and_new_limit(self):
        message = generate.cost_guard(0.113 * 20, 0.50)
        self.assertIn("2.2600 USD", message)
        self.assertIn("--max-cost 2.26", message)
        self.assertIn("go-ahead", message)

    def test_needed_limit_rounds_up_to_cents(self):
        self.assertEqual(generate.needed_limit(0.6048), 0.61)
        self.assertEqual(generate.needed_limit(0.60), 0.60)

    def test_large_run_stops_before_any_api_call(self):
        with patch.object(generate, "api_key", side_effect=AssertionError("must not get this far")):
            result, out, _ = run_main("x", "-n", "20", "-s", "4K")
        self.assertIn("Stopped before calling the API", result)
        self.assertIn("Estimated cost: 2.2600 USD", out)

    def test_estimate_is_not_blocked(self):
        result, out, _ = run_main("x", "-n", "20", "-s", "4K", "--estimate")
        self.assertEqual(result, 0)
        self.assertIn("a real run needs --max-cost 2.26", out)

    def test_negative_limit_is_rejected(self):
        args = parse("x", "--max-cost", "-1")
        self.assertTrue(generate.check(args, generate.MODELS["2.1"]))


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Path(self.tmp.name) / "config.json"
        self.config.write_text(json.dumps({"currency": "eur", "max_cost": 2}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def settle(self, argv, env):
        args = generate.build_parser().parse_args(argv)
        return generate.apply_settings(args, env=env, config_file=self.config)

    def test_built_in_defaults(self):
        args = generate.apply_settings(generate.build_parser().parse_args(["x"]), env={}, config_file=NO_CONFIG)
        self.assertEqual((args.currency, args.max_cost), ("USD", 0.5))

    def test_config_file_beats_defaults(self):
        args = self.settle(["x"], {})
        self.assertEqual((args.currency, args.max_cost), ("EUR", 2.0))

    def test_environment_beats_config_file(self):
        args = self.settle(["x"], {"NANO_BANANA_CURRENCY": "CZK", "NANO_BANANA_MAX_COST": "1.5"})
        self.assertEqual((args.currency, args.max_cost), ("CZK", 1.5))

    def test_command_line_beats_everything(self):
        args = self.settle(["x", "--currency", "GBP", "--max-cost", "0.1"],
                           {"NANO_BANANA_CURRENCY": "CZK", "NANO_BANANA_MAX_COST": "1.5"})
        self.assertEqual((args.currency, args.max_cost), ("GBP", 0.1))

    def test_empty_environment_value_is_ignored(self):
        args = self.settle(["x"], {"NANO_BANANA_MAX_COST": ""})
        self.assertEqual(args.max_cost, 2.0)

    def test_bad_values_stop_with_a_message(self):
        with self.assertRaises(SystemExit):
            self.settle(["x"], {"NANO_BANANA_MAX_COST": "lots"})
        self.config.write_text("[1, 2]", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.settle(["x"], {})


class StatusError(Exception):
    """Like the SDK's errors: an HTTP status on the exception itself."""

    def __init__(self, status_code):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


class ReadTimeout(Exception):
    pass


class ErrorClassificationTests(unittest.TestCase):
    def test_client_errors_are_safe_to_retry(self):
        for status in (400, 401, 403, 404):
            safe, verdict = generate.classify_error(StatusError(status))
            self.assertTrue(safe, status)
            self.assertIn("not", verdict)

    def test_rate_limit_is_safe_after_a_pause(self):
        safe, verdict = generate.classify_error(StatusError(429))
        self.assertTrue(safe)
        self.assertIn("not billed", verdict)

    def test_server_errors_and_timeouts_are_uncertain(self):
        for exc in (StatusError(500), StatusError(503), StatusError(408), ReadTimeout("slow"), ValueError("?")):
            safe, verdict = generate.classify_error(exc)
            self.assertFalse(safe, exc)
            self.assertIn("may have been generated and billed", verdict)
        self.assertIn("Timeout", generate.classify_error(ReadTimeout("slow"))[1])

    def test_status_from_code_or_response(self):
        exc = Exception("x")
        exc.code = 400
        self.assertEqual(generate.error_status(exc), 400)
        exc = Exception("y")
        exc.response = SimpleNamespace(status_code=502)
        self.assertEqual(generate.error_status(exc), 502)

    def test_failed_run_prints_the_verdict(self):
        args = parse("x")
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            code = generate.run_interactions(fake_client(StatusError(400)), args, generate.MODELS["2.1"], [],
                                             None, Path(tempfile.gettempdir()), None, 0.0336)
        self.assertEqual(code, 1)
        self.assertIn("Retry: The API rejected the request (400)", err.getvalue())


def batch_job(state, responses=(), name="batches/job1"):
    return SimpleNamespace(name=name, state=SimpleNamespace(name=state), model="models/gemini-nano-banana-2.1",
                           error=None, dest=SimpleNamespace(inlined_responses=list(responses)),
                           create_time=generate.datetime(2026, 11, 28, 10, 0), end_time=generate.datetime(2026, 11, 28, 10, 3))


def batch_item(data=b"\x89PNG batch"):
    usage = SimpleNamespace(prompt_token_count=12, thoughts_token_count=400, candidates_token_count=1120,
                            candidates_tokens_details=[SimpleNamespace(modality="IMAGE", token_count=1120)])
    part = SimpleNamespace(thought=None, inline_data=SimpleNamespace(data=data, mime_type="image/png"))
    return SimpleNamespace(error=None, response=gc_response([part], usage))


class FakeBatches:
    def __init__(self, *states):
        self.states = list(states)
        self.created = []

    def create(self, model, src, config):
        self.created.append((model, src, config))
        return SimpleNamespace(name="batches/job1")

    def get(self, name):
        state = self.states.pop(0) if len(self.states) > 1 else self.states[0]
        return state if isinstance(state, SimpleNamespace) else batch_job(state)


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def submit(self, client, *argv):
        args = parse("A banner", "--batch", "--name", "banner", *argv)
        model = generate.MODELS[args.model]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), patch.object(generate.time, "sleep"):
            code = generate.run_batch(client, args, model, [], self.dir, generate.estimate_usd(args, model), None)
        return code, out.getvalue(), err.getvalue()

    def collect(self, client, ref="last"):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = generate.collect_batch(client, self.dir, ref, None, "USD")
        return code, out.getvalue(), err.getvalue()

    def test_submit_without_waiting_records_the_job(self):
        client = SimpleNamespace(batches=FakeBatches("JOB_STATE_PENDING"))
        code, out, _ = self.submit(client, "--wait", "0", "-n", "2")
        self.assertEqual(code, 0)
        self.assertIn("--batch-result batches/job1", out)
        record = generate.load_batch_records(self.dir)[-1]
        self.assertEqual((record["job"], record["prompt"], record["count"], record["name"]),
                         ("batches/job1", "A banner", 2, "banner"))
        self.assertEqual(len(client.batches.created[0][1]), 2)  # one request per image

    def test_wait_gives_up_after_the_limit(self):
        ticks = iter(range(0, 10000, 30))
        client = SimpleNamespace(batches=FakeBatches("JOB_STATE_RUNNING"))
        state = generate.wait_for_batch(client, "batches/job1", 2, sleep=lambda s: None, clock=lambda: next(ticks))
        self.assertEqual(state, "JOB_STATE_RUNNING")

    def test_interrupted_wait_ends_cleanly(self):
        client = SimpleNamespace(batches=FakeBatches("JOB_STATE_RUNNING"))
        with patch.object(generate, "wait_for_batch", side_effect=KeyboardInterrupt):
            code, _, err = self.submit(client)
        self.assertEqual(code, 130)
        self.assertIn("Stopped waiting", err)
        self.assertIn("--batch-result batches/job1", err)

    def test_finished_within_the_wait_is_collected_right_away(self):
        done = batch_job("JOB_STATE_SUCCEEDED", [batch_item()])
        client = SimpleNamespace(batches=FakeBatches("JOB_STATE_RUNNING", done))
        code, out, _ = self.submit(client)
        self.assertEqual(code, 0)
        self.assertIn("Saved: ", out)
        self.assertIn("Google took 3.0 min", out)

    def test_collect_reports_a_running_job(self):
        generate.record_batch(self.dir, "batches/job1", parse("x", "--batch"), 0.0168)
        code, out, _ = self.collect(SimpleNamespace(batches=FakeBatches("JOB_STATE_RUNNING")))
        self.assertEqual(code, 0)
        self.assertIn("not finished yet (JOB_STATE_RUNNING", out)
        self.assertEqual(list(self.dir.glob("*.png")), [])

    def test_collect_saves_images_with_batch_cost_and_only_once(self):
        generate.record_batch(self.dir, "batches/job1", parse("A banner", "--batch"), 0.0168)
        done = batch_job("JOB_STATE_SUCCEEDED", [batch_item(), batch_item()])
        client = SimpleNamespace(batches=FakeBatches(done))
        code, out, _ = self.collect(client, "job1")
        self.assertEqual(code, 0)
        self.assertEqual(len(list(self.dir.glob("*.png"))), 2)
        cost = (1120 * 30 + 400 * 7.5 + 12 * 1.5) / 1e6 / 2
        self.assertIn(f"Real cost: {cost:.4f} USD", out)
        self.assertIn("Total for this batch", out)
        sidecar = next(self.dir.glob("*.txt")).read_text(encoding="utf-8")
        self.assertIn("batch job batches/job1", sidecar)
        self.assertIn("A banner", sidecar)
        code, out, _ = self.collect(client)
        self.assertEqual(code, 0)
        self.assertIn("already collected", out)
        self.assertEqual(len(list(self.dir.glob("*.png"))), 2)

    def test_collect_a_failed_job(self):
        generate.record_batch(self.dir, "batches/job1", parse("x", "--batch"), 0.0168)
        code, _, err = self.collect(SimpleNamespace(batches=FakeBatches("JOB_STATE_FAILED")))
        self.assertEqual(code, 1)
        self.assertIn("JOB_STATE_FAILED", err)

    def test_collect_needs_a_record_or_a_name(self):
        with self.assertRaises(SystemExit):
            self.collect(SimpleNamespace(batches=FakeBatches("JOB_STATE_RUNNING")))
        done = batch_job("JOB_STATE_SUCCEEDED", [batch_item()], name="batches/other")
        code, out, _ = self.collect(SimpleNamespace(batches=FakeBatches(done)), "other")
        self.assertEqual(code, 0)
        self.assertIn("Saved: ", out)  # unknown prompt, but the paid image is still saved


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

    def test_name_sets_the_file_name(self):
        code, out, _ = RunTests.run_count(self, fake_client(image_response(1)), "--name", "Hero Banner")
        self.assertEqual(code, 0)
        self.assertRegex(next(self.dir.glob("*.png")).name, r"^\d{8}-\d{6}-hero-banner-1\.png$")

    def test_save_image_never_overwrites(self):
        fixed = generate.datetime(2026, 11, 28, 12, 0, 0)
        with patch.object(generate, "datetime") as fake_now:
            fake_now.now.return_value = fixed
            first = generate.save_image(b"a", "image/png", "same", self.dir, 0)
            second = generate.save_image(b"b", "image/png", "same", self.dir, 0)
        self.assertNotEqual(first, second)
        self.assertEqual(first.read_bytes(), b"a")

    def test_default_folder_ignores_itself(self):
        default = self.dir / "proj" / ".cache" / "nano-banana"
        generate.prepare_out_dir(default, True)
        self.assertEqual((default / ".gitignore").read_text(encoding="utf-8"), "*\n")
        chosen = self.dir / "assets"
        generate.prepare_out_dir(chosen, False)
        self.assertFalse((chosen / ".gitignore").exists())
        existing = self.dir / "existing"
        existing.mkdir()
        generate.prepare_out_dir(existing, True)  # only a folder the script creates gets one
        self.assertFalse((existing / ".gitignore").exists())

    def test_input_images_above_the_size_limit_are_refused(self):
        big = self.dir / "big.png"
        with open(big, "wb") as f:
            f.truncate(generate.MAX_INPUT_BYTES // 2 + 1)
        small_enough = generate.check(parse("x", "-i", str(big)), generate.MODELS["2.1"])
        self.assertEqual(small_enough, [])
        problems = generate.check(parse("x", "-i", str(big), "-i", str(big)), generate.MODELS["2.1"])
        self.assertTrue(any("MB" in p for p in problems), problems)

    def test_delete_by_image_path(self):
        image = self.dir / "secret.png"
        image.write_bytes(b"x")
        generate.save_sidecar(image, parse("edit"), "v1_secret", "v1_first")
        (self.dir / generate.LAST_ID_FILE).write_text("v1_secret", encoding="utf-8")
        client = fake_client()
        with patch.object(generate, "make_client", return_value=client), \
                patch.object(generate, "CONFIG_FILE", NO_CONFIG):
            result, out, _ = run_main("--delete", str(image), "-o", str(self.dir))
        self.assertEqual(result, 0)
        self.assertEqual(client.interactions.deleted, ["v1_secret"])
        self.assertIn("Deleted interaction v1_secret", out)
        self.assertIn("--delete v1_first", out)  # the earlier step may hold the photo too
        self.assertFalse((self.dir / generate.LAST_ID_FILE).exists())

    def test_delete_failure_is_reported(self):
        client = fake_client()
        client.interactions.delete = lambda id: (_ for _ in ()).throw(StatusError(404))
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            code = generate.delete_interaction(client, "v1_gone", "v1_gone", self.dir)
        self.assertEqual(code, 1)
        self.assertIn("Could not delete interaction v1_gone", err.getvalue())

    def test_follow_up_by_image_path_reads_the_sidecar(self):
        image = self.dir / "pick.png"
        image.write_bytes(b"x")
        generate.save_sidecar(image, parse("A red apple", "-i", __file__), "v1_picked", "v1_before")
        self.assertEqual(generate.resolve_interaction(str(image), self.dir), "v1_picked")
        self.assertEqual(generate.resolve_interaction(str(image.with_suffix(".txt")), self.dir), "v1_picked")

    def test_follow_up_last_and_explicit_id(self):
        (self.dir / generate.LAST_ID_FILE).write_text("v1_last\n", encoding="utf-8")
        self.assertEqual(generate.resolve_interaction("last", self.dir), "v1_last")
        self.assertEqual(generate.resolve_interaction("v1_given", self.dir), "v1_given")

    def test_follow_up_errors_are_explained(self):
        with self.assertRaises(SystemExit) as missing_last:
            generate.resolve_interaction("last", self.dir)
        self.assertIn("missing", str(missing_last.exception.code))
        with self.assertRaises(SystemExit) as no_sidecar:
            generate.resolve_interaction(str(self.dir / "gone.png"), self.dir)
        self.assertIn("unknown", str(no_sidecar.exception.code))
        image = self.dir / "batch.png"
        image.write_bytes(b"x")
        generate.save_sidecar(image, parse("x"), batch_job="batches/1")
        with self.assertRaises(SystemExit) as no_id:
            generate.resolve_interaction(str(image), self.dir)
        self.assertIn("no interaction ID", str(no_id.exception.code))

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
