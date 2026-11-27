#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["google-genai>=3.6,<4"]
# ///
"""Generate and edit images with Google's Nano Banana models (Gemini API).

Run it with uv, which installs google-genai on the fly:
    uv run --script generate.py "your prompt" [options]

Regular generation uses the Interactions API (client.interactions.create), which
Google recommends for the Nano Banana models. --batch uses the Batch API, which
still takes the generateContent format; a submitted job is recorded in the output
folder (batch-jobs.json) and collected with --batch-result, in the same run or later.

The API key is read from GEMINI_API_KEY (or GOOGLE_API_KEY), otherwise from
~/.config/nano-banana/api-key.
"""
import argparse
import base64
import json
import math
import mimetypes
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG = json.loads((HERE / "models.json").read_text(encoding="utf-8"))
MODELS = CATALOG["models"]

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9",
                 "1:4", "4:1", "1:8", "8:1"]
EXTREME_RATIOS = {"1:4", "4:1", "1:8", "8:1"}
KEY_FILE = Path.home() / ".config" / "nano-banana" / "api-key"
LAST_ID_FILE = "last-interaction.txt"
CNB_URL = ("https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/"
           "kurzy-devizoveho-trhu/denni_kurz.txt")
IMAGE_FORMATS = {"png": "image/png", "jpeg": "image/jpeg"}
DEFAULT_MAX_COST = 0.50  # USD; above this the script stops until the user raises --max-cost
DEFAULT_CURRENCY = "USD"
DEFAULT_OUT = ".cache/nano-banana"
# Google's own CLI caps inline input images at about 14 MB raw: a request body is limited to 20 MB
# and base64 makes the images a third bigger.
MAX_INPUT_BYTES = 14_000_000
BATCH_FILE = "batch-jobs.json"
DEFAULT_WAIT_MINUTES = 8  # stays under the 10-minute limit many agents put on one shell call
POLL_SECONDS = 20
FINAL_STATES = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".txt"}
CONFIG_FILE = Path.home() / ".config" / "nano-banana" / "config.json"


# ---------- money ----------

def fx_rate(code):
    """Units of `code` per 1 USD, from the Czech National Bank daily table. None if unavailable."""
    code = code.upper()
    if code == "USD":
        return 1.0, "USD"
    try:
        with urllib.request.urlopen(CNB_URL, timeout=5) as r:
            lines = r.read().decode("utf-8").splitlines()
        czk = {"CZK": 1.0}
        for line in lines[2:]:
            parts = line.split("|")
            if len(parts) == 5:
                czk[parts[3]] = float(parts[4].replace(",", ".")) / int(parts[2])
        if "USD" in czk and code in czk:
            return czk["USD"] / czk[code], f"CNB rate of {lines[0].split(' #')[0]}"
    except Exception:
        pass
    return None


def money(usd, fx, code):
    """Format a USD amount, with a converted amount when an exchange rate is available."""
    text = f"{usd:.4f} USD"
    if fx and code.upper() != "USD":
        text += f" (~ {usd * fx[0]:.2f} {code.upper()}, {fx[1]})"
    return text


# ---------- setup ----------

def api_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key and KEY_FILE.exists():
        key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        sys.exit(f"Missing API key. Set GEMINI_API_KEY or save the key to {KEY_FILE}. "
                 "Create one at https://aistudio.google.com/apikey (billing must be enabled: "
                 "image models have no free tier).")
    return key


def apply_settings(a, env=None, config_file=None):
    """Fill in --currency and --max-cost: command line first, then the environment variables
    NANO_BANANA_CURRENCY / NANO_BANANA_MAX_COST, then ~/.config/nano-banana/config.json
    ({"currency": "EUR", "max_cost": 1.0}), then the built-in defaults."""
    env = os.environ if env is None else env
    config_file = CONFIG_FILE if config_file is None else Path(config_file)
    config = {}
    if config_file.is_file():
        try:
            config = json.loads(config_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            sys.exit(f"Cannot read {config_file}: {exc}")
        if not isinstance(config, dict):
            sys.exit(f"{config_file} must hold a JSON object such as {{\"currency\": \"EUR\", \"max_cost\": 1.0}}.")

    def first(*values):
        return next((v for v in values if v not in (None, "")), None)

    a.currency = str(first(a.currency, env.get("NANO_BANANA_CURRENCY"), config.get("currency"),
                           DEFAULT_CURRENCY)).strip().upper()
    max_cost = first(a.max_cost, env.get("NANO_BANANA_MAX_COST"), config.get("max_cost"), DEFAULT_MAX_COST)
    try:
        a.max_cost = float(max_cost)
    except (TypeError, ValueError):
        sys.exit(f"The cost limit must be a number in USD, got {max_cost!r} "
                 "(from NANO_BANANA_MAX_COST or the config file).")
    return a


def check(a, model):
    """Return a list of problems with the requested option combination."""
    errors = []
    if not a.prompt:
        errors.append("Give a prompt, or --prompt-file.")
    if a.size not in model["sizes"]:
        errors.append(f"Model {a.model} does not support size {a.size}. Options: {', '.join(model['sizes'])}.")
    if a.aspect in EXTREME_RATIOS and not model["extreme_aspect_ratios"]:
        errors.append(f"Aspect ratio {a.aspect} is only supported by models 2.1 and 2.")
    if a.thinking and a.thinking not in model["thinking"]:
        options = ", ".join(model["thinking"]) or "none (this model always thinks)"
        errors.append(f"Model {a.model} does not support thinking level {a.thinking}. Options: {options}.")
    if a.search and not model["search"]:
        errors.append(f"Model {a.model} does not support Google Search grounding.")
    if len(a.image) > model["max_input_images"]:
        errors.append(f"At most {model['max_input_images']} input images are allowed.")
    for path in a.image:
        if not Path(path).is_file():
            errors.append(f"Input image not found: {path}")
    total = sum(Path(p).stat().st_size for p in a.image if Path(p).is_file())
    if total > MAX_INPUT_BYTES:
        errors.append(f"The input images add up to {total / 1e6:.1f} MB, above the limit of about "
                      f"{MAX_INPUT_BYTES / 1e6:.0f} MB for images sent with a request (20 MB per request after "
                      "encoding). Make them smaller first: fewer pixels or JPEG.")
    if a.name is not None and not re.search(r"[A-Za-z0-9]", a.name):
        errors.append("--name needs at least one letter or digit.")
    if a.count < 1:
        errors.append("--count must be at least 1.")
    if a.max_cost < 0:
        errors.append("--max-cost cannot be negative.")
    if a.wait < 0:
        errors.append("--wait cannot be negative.")
    if a.batch:
        if a.follow_up:
            errors.append("--follow-up cannot be combined with --batch.")
        if a.format:
            errors.append("--format cannot be combined with --batch.")
        if model["sizes"].get(a.size, {}).get("batch") is None:
            errors.append(f"No batch price is published or verified for model {a.model} at {a.size}, "
                          "so --batch is disabled for it.")
    if a.no_store and a.follow_up:
        errors.append("--no-store cannot be combined with --follow-up (follow-ups need the stored interaction).")
    return errors


def estimate_usd(a, model):
    price = model["sizes"][a.size]
    return (price["batch"] if a.batch else price["price"]) * a.count


def needed_limit(usd):
    """The smallest --max-cost, in whole cents, that lets an estimate of `usd` through."""
    return math.ceil(round(usd * 100, 6)) / 100


def cost_guard(usd, limit):
    """None when the estimate is within the limit, otherwise the message to stop with."""
    if usd <= limit + 1e-9:
        return None
    return (f"Stopped before calling the API: the estimated cost {usd:.4f} USD is above the limit of "
            f"{limit:.2f} USD (--max-cost). Tell the user the price and ask for their go-ahead. "
            f"Only if they agree, rerun with --max-cost {needed_limit(usd):.2f}.")


# ---------- files ----------

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower())[:40].strip("-") or "image"


def save_image(data, mime, label, out_dir, index):
    """Write one image as <timestamp>-<slug of label>-<n>.<ext>, never over an existing file."""
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(mime or "", ".png")
    stem = f"{datetime.now():%Y%m%d-%H%M%S}-{slugify(label)}-{index + 1}"
    path = out_dir / f"{stem}{ext}"
    extra = 1
    while path.exists():
        extra += 1
        path = out_dir / f"{stem}-{extra}{ext}"
    path.write_bytes(data if isinstance(data, bytes) else base64.b64decode(data))
    return path


def prepare_out_dir(out_dir, is_default):
    """Create the output folder. The default folder gets a .gitignore with `*`, so it ignores itself;
    a folder chosen with -o may be a real project folder and is left alone."""
    created = not out_dir.exists()
    out_dir.mkdir(parents=True, exist_ok=True)
    if created and is_default:
        (out_dir / ".gitignore").write_text("*\n", encoding="utf-8")


def save_sidecar(path, a, interaction_id=None, previous_id=None, suggestions=None, seconds=None, cost=None,
                 batch_job=None):
    """Save the prompt and options next to the image so variants can be compared and repeated."""
    options = [f"model {a.model}", a.size, f"aspect {a.aspect or 'auto'}"]
    if a.thinking:
        options.append(f"thinking {a.thinking}")
    if a.search:
        options.append("with search")
    if a.image:
        options.append("inputs " + ", ".join(Path(p).name for p in a.image))
    if previous_id:
        options.append(f"follows {previous_id}")
    if interaction_id:
        options.append(f"id {interaction_id}")
    if batch_job:
        options.append(f"batch job {batch_job}")
    if seconds is not None:
        options.append(f"took {seconds:.1f} s")
    if cost is not None:
        options.append(f"cost {cost:.4f} USD")
    text = "# " + " | ".join(options) + "\n\n" + a.prompt + "\n"
    if suggestions:
        text += "\n# Google Search suggestions (HTML; Google requires showing them when you publish grounded output)\n"
        text += "\n".join(suggestions) + "\n"
    path.with_suffix(".txt").write_text(text, encoding="utf-8")


def sidecar_interaction_id(image_path):
    """The interaction ID recorded in the .txt file next to an image, or None."""
    sidecar = Path(image_path).with_suffix(".txt")
    if not sidecar.is_file():
        return None
    header = sidecar.read_text(encoding="utf-8").partition("\n")[0].lstrip("# ")
    for part in header.split(" | "):
        if part.startswith("id "):
            return part[3:].strip() or None
    return None


def resolve_interaction(value, out_dir):
    """Turn "last", an image path (read from its sidecar .txt) or an ID into an interaction ID."""
    if value == "last":
        last_id_file = Path(out_dir) / LAST_ID_FILE
        if not last_id_file.is_file():
            sys.exit(f"No last interaction: {last_id_file} is missing. Pass an image path or an interaction ID.")
        return last_id_file.read_text(encoding="utf-8").strip()
    path = Path(value)
    if path.is_file() or path.suffix.lower() in IMAGE_SUFFIXES:
        if not path.with_suffix(".txt").is_file():
            sys.exit(f"{path.with_suffix('.txt')} is missing, so the interaction behind {value} is unknown. "
                     "Pass the interaction ID instead.")
        found = sidecar_interaction_id(path)
        if not found:
            sys.exit(f"{path.with_suffix('.txt')} records no interaction ID (made with --batch or --no-store?).")
        return found
    return value


def load_images(paths):
    """Input images as (base64, mime)."""
    return [(base64.b64encode(Path(p).read_bytes()).decode(), mimetypes.guess_type(p)[0] or "image/png")
            for p in paths]


def find_key(obj, key):
    """All values stored under `key` anywhere in a nested dict/list structure."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and v:
                found.append(v)
            found += find_key(v, key)
    elif isinstance(obj, list):
        for v in obj:
            found += find_key(v, key)
    return found


# ---------- Interactions API (regular generation) ----------

def interact(client, a, model, images, previous_id):
    content = [{"type": "text", "text": a.prompt}]
    content += [{"type": "image", "data": data, "mime_type": mime} for data, mime in images]
    response_format = {"type": "image", "image_size": a.size}
    if a.aspect:  # without it, edits keep the input photo's shape and new images are square
        response_format["aspect_ratio"] = a.aspect
    if a.format:
        response_format["mime_type"] = IMAGE_FORMATS[a.format]
    params = {"model": model["id"], "input": content, "response_format": response_format}
    if a.thinking:
        params["generation_config"] = {"thinking_level": a.thinking}
    if a.search:
        params["tools"] = [{"type": "google_search", "search_types": ["web_search", "image_search"]}]
    if previous_id:
        params["previous_interaction_id"] = previous_id
    if a.no_store:
        params["store"] = False
    return client.interactions.create(**params)


def images_from_interaction(response):
    """Finished images only; thought steps are skipped."""
    images = []
    for step in response.steps or []:
        if getattr(step, "type", None) != "model_output":
            continue
        for block in getattr(step, "content", None) or []:
            if getattr(block, "type", None) == "image" and getattr(block, "data", None):
                images.append((block.data, getattr(block, "mime_type", None)))
    if not images and response.output_image is not None and response.output_image.data:
        images.append((response.output_image.data, response.output_image.mime_type))
    return images


def suggestions_from_interaction(response):
    found = []
    for step in response.steps or []:
        if getattr(step, "type", None) == "google_search_result":
            data = step.model_dump() if hasattr(step, "model_dump") else {}
            found += [s for s in find_key(data, "search_suggestions") if isinstance(s, str)]
    return list(dict.fromkeys(found))  # the API repeats the same snippet


# ---------- real cost from the reported usage ----------

def modality_tokens(entries, image):
    """Sum the tokens of image (image=True) or non-image (image=False) entries of a per-modality list."""
    total = 0
    for entry in entries or []:
        tokens = getattr(entry, "tokens", None)
        if tokens is None:
            tokens = getattr(entry, "token_count", None)
        if str(getattr(entry, "modality", "")).lower().endswith("image") == image:
            total += tokens or 0
    return total


def token_counts(usage):
    """Billed tokens as {"input", "image", "text", "thinking"}, or None when the response has no usage.

    Accepts both shapes the SDK returns: the Interactions API `usage` (total_input_tokens,
    output_tokens_by_modality, total_thought_tokens) and the generateContent `usage_metadata`
    used by batch jobs (prompt_token_count, candidates_tokens_details, thoughts_token_count).
    """
    if usage is None:
        return None
    if getattr(usage, "total_input_tokens", None) is not None or getattr(usage, "output_tokens_by_modality", None):
        by_modality = getattr(usage, "output_tokens_by_modality", None)
        total_output = getattr(usage, "total_output_tokens", None) or 0
        input_tokens = getattr(usage, "total_input_tokens", None) or 0
        thinking = getattr(usage, "total_thought_tokens", None) or 0
    else:
        by_modality = getattr(usage, "candidates_tokens_details", None)
        total_output = getattr(usage, "candidates_token_count", None) or 0
        input_tokens = getattr(usage, "prompt_token_count", None) or 0
        thinking = getattr(usage, "thoughts_token_count", None) or 0
    image = modality_tokens(by_modality, True)
    text = modality_tokens(by_modality, False) if by_modality else max(total_output - image, 0)
    return {"input": input_tokens, "image": image, "text": text, "thinking": thinking}


def cost_usd(counts, model, batch=False):
    """USD per part: image output, text and thinking output, input. Batch jobs get the batch discount."""
    factor = CATALOG["batch_factor"] if batch else 1.0
    return {
        "image": counts["image"] / 1e6 * model["per_million_image_tokens"] * factor,
        "text": (counts["text"] + counts["thinking"]) / 1e6 * model["per_million_text_tokens"] * factor,
        "input": counts["input"] / 1e6 * model["per_million_input_tokens"] * factor,
    }


def cost_line(counts, costs, fx, currency):
    total = sum(costs.values())
    thinking = f"thinking {counts['thinking']}" + (f" + text {counts['text']}" if counts["text"] else "")
    return (f"Real cost: {money(total, fx, currency)} = image {counts['image']} tokens {costs['image']:.4f}"
            f" + {thinking} tokens {costs['text']:.4f} + input {counts['input']} tokens {costs['input']:.4f}")


def response_cost(response, model, batch=False):
    """(token counts, USD per part) of one response, or (None, None) when the API reported no usage."""
    counts = token_counts(getattr(response, "usage", None) or getattr(response, "usage_metadata", None))
    return (counts, cost_usd(counts, model, batch)) if counts else (None, None)


def print_usage(response, model, fx, currency, batch=False):
    """Print the real cost of one response and return it in USD (None when the API reported no usage)."""
    counts, costs = response_cost(response, model, batch)
    if counts is None:
        print("Real cost: unknown, the API reported no usage for this call.")
        return None
    print(cost_line(counts, costs, fx, currency))
    return sum(costs.values())


# ---------- Batch API (generateContent format) ----------

def batch_request(a, images):
    parts = [{"text": a.prompt}] + [{"inline_data": {"mime_type": mime, "data": data}} for data, mime in images]
    image_config = {"image_size": a.size}
    if a.aspect:
        image_config["aspect_ratio"] = a.aspect
    config = {"response_modalities": ["IMAGE"], "image_config": image_config}
    if a.thinking:
        config["thinking_config"] = {"thinking_level": a.thinking}
    if a.search:
        config["tools"] = [{"google_search": {}}]
    return {"contents": [{"role": "user", "parts": parts}], "config": config}


def images_from_generate_content(response):
    images = []
    for candidate in response.candidates or []:
        for part in (candidate.content.parts if candidate.content else None) or []:
            if getattr(part, "thought", False):
                continue  # thinking step, not a result
            if getattr(part, "inline_data", None) and part.inline_data.data:
                images.append((part.inline_data.data, part.inline_data.mime_type))
    return images


def job_state(job):
    state = getattr(job, "state", None)
    return getattr(state, "name", None) or (str(state) if state else "JOB_STATE_UNSPECIFIED")


def load_batch_records(out_dir):
    """The batch jobs submitted into this output folder, oldest first."""
    path = Path(out_dir) / BATCH_FILE
    if not path.is_file():
        return []
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        sys.exit(f"{path} is damaged: {exc}")
    return records if isinstance(records, list) else []


def save_batch_records(out_dir, records):
    path = Path(out_dir) / BATCH_FILE
    path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_batch(out_dir, job_name, a, estimate):
    """Remember a submitted job, so a later run can collect it with --batch-result."""
    records = load_batch_records(out_dir)
    records.append({
        "job": job_name, "submitted": datetime.now().isoformat(timespec="seconds"),
        "model": a.model, "size": a.size, "aspect": a.aspect, "thinking": a.thinking, "search": a.search,
        "count": a.count, "inputs": [Path(p).name for p in a.image], "name": a.name, "prompt": a.prompt,
        "estimate_usd": round(estimate, 4), "state": "submitted", "collected": None, "saved": [],
    })
    save_batch_records(out_dir, records)


def find_batch_record(records, ref):
    """The record for "last" or a job name (with or without the "batches/" prefix), or None."""
    if ref == "last":
        return records[-1] if records else None
    short = ref.split("/")[-1]
    return next((r for r in reversed(records) if r.get("job", "").split("/")[-1] == short), None)


def collect_command(name, out_dir):
    script = Path(__file__).resolve()
    return f'uv run --script "{script}" --batch-result {name} -o "{out_dir}"'


def wait_for_batch(client, name, minutes, sleep=None, clock=None):
    """Poll the job until it ends or `minutes` pass; return its last state."""
    sleep, clock = sleep or time.sleep, clock or time.monotonic
    deadline = clock() + minutes * 60
    while True:
        state = job_state(client.batches.get(name=name))
        remaining = deadline - clock()
        if state in FINAL_STATES or remaining <= 0:
            return state
        sleep(min(POLL_SECONDS, remaining))


def run_batch(client, a, model, images, out_dir, estimate, fx):
    """Submit a batch job, record it, wait at most --wait minutes, and collect it if it is done."""
    requests = [batch_request(a, images) for _ in range(a.count)]
    try:
        job = client.batches.create(model=model["id"], src=requests,
                                    config={"display_name": f"nano-banana {slugify(a.name or a.prompt)}"})
    except Exception as exc:
        print(f"Submitting the batch job failed: {describe(exc)}", file=sys.stderr)
        print(f"Retry: {classify_error(exc)[1]}", file=sys.stderr)
        return 1
    record_batch(out_dir, job.name, a, estimate)
    print(f"Batch job submitted: {job.name} (recorded in {Path(out_dir) / BATCH_FILE})")
    later = f"Collect the images later with:\n  {collect_command(job.name, out_dir)}"
    if a.wait <= 0:
        print(f"Not waiting (--wait 0). A batch job can take up to 24 hours. {later}")
        return 0
    print(f"Waiting up to {a.wait:g} min for it (checking every {POLL_SECONDS} s; Ctrl+C stops waiting, "
          "the job keeps running)...")
    try:
        state = wait_for_batch(client, job.name, a.wait)
    except KeyboardInterrupt:
        print(f"Stopped waiting. The job keeps running at Google and is billed when it finishes. {later}",
              file=sys.stderr)
        return 130
    if state not in FINAL_STATES:
        print(f"The job is still {state} after {a.wait:g} min, which is normal: a batch job can take up to "
              f"24 hours. {later}")
        return 0
    return collect_batch(client, out_dir, job.name, fx, a.currency)


def model_key_for(model_id):
    return next((key for key, m in MODELS.items() if str(model_id or "").endswith(m["id"])), None)


def batch_minutes(job):
    """Minutes from submission to the end of the job by Google's own timestamps, or None."""
    start, end = getattr(job, "create_time", None), getattr(job, "end_time", None)
    try:
        return (end - start).total_seconds() / 60
    except TypeError:
        return None


def collect_batch(client, out_dir, ref, fx, currency):
    """Save the images of a finished batch job, or report its state. Returns the exit code.

    A job is collected only once: a second call lists the files saved the first time instead of
    writing them again (unless those files are gone).
    """
    out_dir = Path(out_dir)
    records = load_batch_records(out_dir)
    record = find_batch_record(records, ref)
    if record is None and ref == "last":
        sys.exit(f"No batch job is recorded in {out_dir / BATCH_FILE}. Pass the job name, or the -o folder "
                 "that was used when the job was submitted.")
    name = record["job"] if record else (ref if ref.startswith("batches/") else f"batches/{ref}")
    if record and record.get("collected"):
        existing = [p for p in record.get("saved", []) if Path(p).is_file()]
        if existing or not record.get("saved"):
            print(f"Batch job {name} was already collected on {record['collected']}; nothing was saved again.")
            for path in existing:
                print(f"Saved earlier: {path}")
            return 0
        print(f"Batch job {name} was collected before, but its files are gone; saving them again.")
    try:
        job = client.batches.get(name=name)
    except Exception as exc:
        print(f"Could not look up batch job {name}: {describe(exc)}", file=sys.stderr)
        return 1
    state = job_state(job)
    if record is None:
        record = {"job": name, "submitted": None, "model": model_key_for(getattr(job, "model", None)),
                  "collected": None, "saved": []}
        records.append(record)
    record["state"] = state
    if state not in FINAL_STATES:
        save_batch_records(out_dir, records)
        submitted = f", submitted {record['submitted']}" if record.get("submitted") else ""
        print(f"Batch job {name} is not finished yet ({state}{submitted}). Nothing to collect yet; try again "
              "later, a batch job can take up to 24 hours.")
        return 0
    if state != "JOB_STATE_SUCCEEDED":
        save_batch_records(out_dir, records)
        print(f"Batch job {name} ended with {state}: {getattr(job, 'error', None)}. There is nothing to collect.",
              file=sys.stderr)
        return 1

    model = MODELS.get(record.get("model"))
    a = argparse.Namespace(
        model=record.get("model") or "unknown", size=record.get("size") or "size unknown",
        aspect=record.get("aspect"), thinking=record.get("thinking"), search=record.get("search"),
        image=record.get("inputs") or [], name=record.get("name"),
        prompt=record.get("prompt") or "(prompt not recorded: the job was submitted into another folder)")
    minutes = batch_minutes(job)
    print(f"Batch job {name} has finished" + (f"; Google took {minutes:.1f} min from submission to the end."
                                                if minutes is not None else "."))
    responses = getattr(getattr(job, "dest", None), "inlined_responses", None) or []
    saved, problems, total_usd = [], [], 0.0
    for i, item in enumerate(responses):
        label = f"Request {i + 1} of {len(responses)}" if len(responses) > 1 else "Request"
        if getattr(item, "error", None):
            problems.append(f"{label} failed: {item.error}")
            print(f"{label} failed: {item.error}", file=sys.stderr)
            continue
        response = getattr(item, "response", None)
        results = images_from_generate_content(response) if response is not None else []
        counts, costs = response_cost(response, model, batch=True) if model and response is not None else (None, None)
        call_usd = sum(costs.values()) if costs else None
        total_usd += call_usd or 0.0
        for data, mime in results:
            path = save_image(data, mime, a.name or a.prompt, out_dir, len(saved))
            save_sidecar(path, a, batch_job=name, cost=call_usd)
            saved.append(path)
            print(f"Saved: {path}")
        if counts:
            print(cost_line(counts, costs, fx, currency))
        if not results:
            problems.append(f"{label}: the response holds no image.")
    if len(responses) > 1:
        print(f"Total for this batch: {money(total_usd, fx, currency)}")
    record["collected"] = datetime.now().isoformat(timespec="seconds")
    record["saved"] = [str(p.resolve()) for p in saved]
    save_batch_records(out_dir, records)
    return summarize(saved, problems, record.get("count") or len(responses), 0)


# ---------- main ----------

def build_parser():
    ap = argparse.ArgumentParser(description="Generate and edit images with Nano Banana (Gemini API).")
    ap.add_argument("prompt", nargs="?", help="image description or requested edit (English works best)")
    ap.add_argument("--prompt-file", help="read the prompt from a file (avoids shell quoting problems)")
    ap.add_argument("-m", "--model", choices=MODELS, default="2.1", help="2.1 (default), 2, pro, lite")
    ap.add_argument("-s", "--size", default="1K", help="512, 1K, 2K, 4K (depends on the model), default 1K")
    ap.add_argument("-a", "--aspect", choices=ASPECT_RATIOS,
                    help="aspect ratio; without it edits keep the input shape and new images are 1:1")
    ap.add_argument("-i", "--image", action="append", default=[], help="input image (repeatable, max 14)")
    ap.add_argument("-t", "--thinking", choices=["minimal", "medium", "high"],
                    help="thinking level (2.1: minimal/medium/high, 2 and lite: minimal/high)")
    ap.add_argument("--search", action="store_true", help="Google Search grounding incl. image search (not lite)")
    ap.add_argument("--follow-up", nargs="?", const="last", metavar="IMAGE|ID",
                    help="edit a previous result with this prompt; the model remembers the image. Without a "
                         "value the last result; or the path of a generated image (its .txt holds the ID); "
                         "or an interaction ID")
    ap.add_argument("-n", "--count", type=int, default=1, help="number of images (each one is billed)")
    ap.add_argument("-o", "--out", default=DEFAULT_OUT,
                    help=f"output folder (default {DEFAULT_OUT}, which gets a .gitignore that ignores it)")
    ap.add_argument("--name", help="file-name stem for the images (default: the start of the prompt)")
    ap.add_argument("--format", choices=IMAGE_FORMATS, help="output file format (default: what the model returns)")
    ap.add_argument("--no-store", action="store_true",
                    help="ask Google not to store the interaction (disables --follow-up on this result)")
    ap.add_argument("--delete", metavar="IMAGE|ID",
                    help="delete a stored interaction at Google (an image path, an interaction ID, or 'last'); "
                         "generates nothing")
    ap.add_argument("--batch", action="store_true",
                    help="half price, the result can take up to 24 h; the job is recorded in the output folder")
    ap.add_argument("--wait", type=float, default=DEFAULT_WAIT_MINUTES, metavar="MINUTES",
                    help=f"with --batch: wait at most this long for the result (default {DEFAULT_WAIT_MINUTES}, "
                         "0 = submit and exit), then collect it later with --batch-result")
    ap.add_argument("--batch-result", nargs="?", const="last", metavar="JOB",
                    help="collect a batch job submitted earlier (default: the last one recorded in the output "
                         "folder): saves its images if it is done, otherwise reports its state")
    ap.add_argument("--estimate", action="store_true", help="only print the price estimate, generate nothing")
    ap.add_argument("--max-cost", type=float, metavar="USD",
                    help="stop before calling the API when the estimate is above this (default "
                         f"{DEFAULT_MAX_COST:.2f}, or NANO_BANANA_MAX_COST, or max_cost in the config file)")
    ap.add_argument("--currency",
                    help="also show prices in this currency (ISO code, rate from the Czech National Bank; "
                         "default USD, or NANO_BANANA_CURRENCY, or currency in the config file)")
    return ap


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    a = apply_settings(build_parser().parse_args(argv))
    if a.delete and a.batch_result:
        sys.exit("Use --delete and --batch-result in separate runs.")
    if a.delete:
        interaction_id = resolve_interaction(a.delete, Path(a.out))
        sys.exit(delete_interaction(make_client(), interaction_id, a.delete, Path(a.out)))
    if a.batch_result:
        fx = fx_rate(a.currency)
        client = make_client()
        prepare_out_dir(Path(a.out), a.out == DEFAULT_OUT)
        sys.exit(collect_batch(client, Path(a.out), a.batch_result, fx, a.currency))
    if a.prompt_file:
        a.prompt = Path(a.prompt_file).read_text(encoding="utf-8").strip()
    a.size = "512" if a.size.lower() in ("512", "0.5k") else a.size.upper()
    model = MODELS[a.model]
    errors = check(a, model)
    if errors:
        sys.exit("\n".join(errors))

    fx = fx_rate(a.currency)
    if fx is None:
        print(f"Note: no exchange rate for {a.currency.upper()}, showing USD only.", file=sys.stderr)
    usd = estimate_usd(a, model)
    print(f"Model: {model['name']} ({model['id']}), {a.size}, aspect {a.aspect or 'auto'}, "
          f"{a.count}x {'batch' if a.batch else 'standard'}"
          + (f", thinking {a.thinking}" if a.thinking else "") + (", with search" if a.search else ""))
    print(f"Estimated cost: {money(usd, fx, a.currency)}, image output only; "
          "thinking and input tokens come on top (see the real cost after the call)")
    if a.search:
        print(f"Search grounding is billed separately: {CATALOG['search_pricing']}")
    over_limit = cost_guard(usd, a.max_cost)
    if a.estimate:
        if over_limit:
            print(f"Note: this is above the --max-cost limit of {a.max_cost:.2f} USD; a real run needs "
                  f"--max-cost {needed_limit(usd):.2f} after the user agrees.")
        return
    if over_limit:
        sys.exit(over_limit)

    out_dir = Path(a.out)
    previous_id = resolve_interaction(a.follow_up, out_dir) if a.follow_up else None
    client = make_client()
    prepare_out_dir(out_dir, a.out == DEFAULT_OUT)
    images = load_images(a.image)

    if a.batch:
        sys.exit(run_batch(client, a, model, images, out_dir, usd, fx))
    sys.exit(run_interactions(client, a, model, images, previous_id, out_dir, fx, usd))


def make_client():
    from google import genai  # imported here so --estimate and the tests work without google-genai

    return genai.Client(api_key=api_key())


def delete_interaction(client, interaction_id, ref, out_dir):
    """Delete a stored interaction at Google (for sensitive inputs) and return the exit code."""
    try:
        client.interactions.delete(id=interaction_id)
    except Exception as exc:
        print(f"Could not delete interaction {interaction_id}: {describe(exc)}", file=sys.stderr)
        return 1
    print(f"Deleted interaction {interaction_id}. Google no longer stores it, so --follow-up on it is no "
          "longer possible. The image files on disk are untouched.")
    last_id_file = Path(out_dir) / LAST_ID_FILE
    if last_id_file.is_file() and last_id_file.read_text(encoding="utf-8").strip() == interaction_id:
        last_id_file.unlink()
    path = Path(ref)
    if path.with_suffix(".txt").is_file():
        header = path.with_suffix(".txt").read_text(encoding="utf-8").partition("\n")[0]
        earlier = re.search(r"\| follows (\S+)", header)
        if earlier:
            print(f"This image continued interaction {earlier.group(1)}, which Google still stores. Delete it "
                  f"too (--delete {earlier.group(1)}) if the sensitive input was sent there.")
    return 0


def describe(exc):
    """One line about an exception, without the traceback."""
    text = " ".join(str(exc).split())
    return f"{type(exc).__name__}: {text[:500]}" if text else type(exc).__name__


def error_status(exc):
    """The HTTP status of an API exception, or None (timeouts, dropped connections, unknown errors).

    google-genai raises errors with `status_code` (Interactions API) or `code` (other APIs).
    """
    for holder in (exc, getattr(exc, "response", None), getattr(exc, "raw_response", None)):
        for attr in ("status_code", "code"):
            value = getattr(holder, attr, None)
            if isinstance(value, int) and 100 <= value <= 599:
                return value
    return None


def classify_error(exc):
    """(retry_is_safe, verdict) for an exception raised by an API call.

    A 4xx answer means Google rejected the request before generating anything, so nothing was
    billed and a corrected retry is safe. A 5xx answer, a timeout or a dropped connection leaves
    the outcome open: the image may have been generated and billed.
    """
    status = error_status(exc)
    if status == 429:
        return True, ("Rate limit or quota exceeded (429). The request was rejected and not billed. "
                      "Retrying is safe after a pause or once the quota allows it.")
    if status is not None and 400 <= status < 500 and status not in (408, 499):
        return True, (f"The API rejected the request ({status}), so nothing was generated or billed. "
                      "Fix the cause (options, prompt, key, billing); retrying after that is safe.")
    if status is not None and status >= 500:
        what = f"Server error ({status})"
    elif status is not None:
        what = f"HTTP {status}"
    elif any(word in type(exc).__name__.lower() for word in ("timeout", "connect", "network", "noresponse")):
        what = "Timeout or dropped connection"
    else:
        what = "Unexpected error"
    return False, (f"{what}: the outcome is uncertain, the image may have been generated and billed. "
                   "Do not retry blindly; tell the user and let them decide.")


def run_interactions(client, a, model, images, previous_id, out_dir, fx, estimate):
    """Make a.count calls and return the exit code.

    Every image is saved and printed as soon as it arrives, so a failure in call 3 of 4 does not
    hide images 1 and 2. The first API error stops the run: the remaining calls would most likely
    fail the same way, and each uncertain failure may have been billed.
    """
    last_id_file = out_dir / LAST_ID_FILE
    saved, problems = [], []
    total_usd = 0.0
    attempted = 0
    interrupted = False
    for i in range(a.count):
        label = f"Image {i + 1} of {a.count}" if a.count > 1 else "Image"
        attempted += 1
        start = time.monotonic()
        try:
            response = interact(client, a, model, images, previous_id)
        except KeyboardInterrupt:
            problems.append(f"{label}: interrupted after {time.monotonic() - start:.1f} s while waiting for "
                            "the API. The request may still be generated and billed.")
            interrupted = True
            break
        except Exception as exc:
            _, verdict = classify_error(exc)
            print(f"{label} failed after {time.monotonic() - start:.1f} s: {describe(exc)}", file=sys.stderr)
            print(f"Retry: {verdict}", file=sys.stderr)
            problems.append(f"{label} failed. {verdict}")
            break
        seconds = time.monotonic() - start
        print(f"{label}: the API answered in {seconds:.1f} s")
        results = images_from_interaction(response)
        suggestions = suggestions_from_interaction(response) if a.search else None
        _, costs = response_cost(response, model)
        call_usd = sum(costs.values()) if costs else None
        for data, mime in results:
            path = save_image(data, mime, a.name or a.prompt, out_dir, len(saved))
            save_sidecar(path, a, response.id, previous_id, suggestions, seconds, call_usd)
            saved.append(path)
            print(f"Saved: {path}")
        if not results:
            reason = response.errors or response.output_text or response.status
            print(f"{label}: the model returned no image ({reason}).", file=sys.stderr)
            problems.append(f"{label}: the model returned no image ({reason}).")
        if response.output_text:
            print(f"Model said: {response.output_text.strip()}")
        if suggestions:
            print("Search suggestions were saved next to the image (Google requires showing them "
                  "if you publish grounded output).")
        if response.id and not a.no_store:
            last_id_file.write_text(response.id, encoding="utf-8")
            print(f"Interaction ID: {response.id} (continue with --follow-up)")
        total_usd += print_usage(response, model, fx, a.currency) or 0.0
    if a.count > 1:
        print(f"Total for this run: {money(total_usd, fx, a.currency)} (estimate was {estimate:.4f} USD "
              "for the images alone)")
    return summarize(saved, problems, a.count, a.count - attempted, interrupted)


def summarize(saved, problems, wanted, skipped, interrupted=False):
    """Print the closing summary and return the exit code (0 only when every image arrived)."""
    if not problems and len(saved) >= wanted:
        if wanted > 1:
            print(f"Done: {len(saved)} of {wanted} images saved.")
        return 0
    print(f"Finished with problems: {len(saved)} of {wanted} images saved.", file=sys.stderr)
    for problem in problems:
        print(f"- {problem}", file=sys.stderr)
    if skipped:
        print(f"- {skipped} more image(s) were not attempted; nothing was sent or billed for them.",
              file=sys.stderr)
    for path in saved:
        print(f"Saved: {path}")
    return 130 if interrupted else 1


if __name__ == "__main__":
    main()
