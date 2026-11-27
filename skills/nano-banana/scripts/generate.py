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
still takes the generateContent format.

The API key is read from GEMINI_API_KEY (or GOOGLE_API_KEY), otherwise from
~/.config/nano-banana/api-key.
"""
import argparse
import base64
import json
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
    if a.count < 1:
        errors.append("--count must be at least 1.")
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


# ---------- files ----------

def save_image(data, mime, prompt, out_dir, index):
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(mime or "", ".png")
    slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower())[:40].strip("-") or "image"
    path = out_dir / f"{datetime.now():%Y%m%d-%H%M%S}-{slug}-{index + 1}{ext}"
    path.write_bytes(data if isinstance(data, bytes) else base64.b64decode(data))
    return path


def save_sidecar(path, a, interaction_id=None, previous_id=None, suggestions=None):
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
    text = "# " + " | ".join(options) + "\n\n" + a.prompt + "\n"
    if suggestions:
        text += "\n# Google Search suggestions (HTML; Google requires showing them when you publish grounded output)\n"
        text += "\n".join(suggestions) + "\n"
    path.with_suffix(".txt").write_text(text, encoding="utf-8")


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


def print_usage(response, model, fx, currency, batch=False):
    """Print the real cost of one response and return it in USD (None when the API reported no usage)."""
    counts = token_counts(getattr(response, "usage", None) or getattr(response, "usage_metadata", None))
    if counts is None:
        print("Real cost: unknown, the API reported no usage for this call.")
        return None
    costs = cost_usd(counts, model, batch)
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


def run_batch(client, a, model, images):
    requests = [batch_request(a, images) for _ in range(a.count)]
    job = client.batches.create(model=model["id"], src=requests, config={"display_name": "nano-banana"})
    print(f"Batch job: {job.name}. Waiting for the result (checking every 30 s, Ctrl+C stops waiting; "
          "the job keeps running and can take up to 24 h)...")
    final_states = ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED")
    while True:
        job = client.batches.get(name=job.name)
        state = job.state.name if job.state else ""
        if state in final_states:
            break
        time.sleep(30)
    if state != "JOB_STATE_SUCCEEDED":
        sys.exit(f"Batch job ended with state {state}: {job.error}")
    results = []
    for response in job.dest.inlined_responses or []:
        if response.error:
            print(f"One request failed: {response.error}", file=sys.stderr)
            continue
        results += images_from_generate_content(response.response)
    return results


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
    ap.add_argument("--follow-up", nargs="?", const="last", metavar="ID",
                    help="edit the last (or the given) result with this prompt; the model remembers the image")
    ap.add_argument("-n", "--count", type=int, default=1, help="number of images (each one is billed)")
    ap.add_argument("-o", "--out", default=".cache/nano-banana", help="output folder")
    ap.add_argument("--format", choices=IMAGE_FORMATS, help="output file format (default: what the model returns)")
    ap.add_argument("--no-store", action="store_true",
                    help="ask Google not to store the interaction (disables --follow-up on this result)")
    ap.add_argument("--batch", action="store_true", help="half price, the result can take up to 24 h")
    ap.add_argument("--estimate", action="store_true", help="only print the price estimate, generate nothing")
    ap.add_argument("--currency", default="USD",
                    help="also show prices in this currency (ISO code, rate from the Czech National Bank)")
    return ap


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    a = build_parser().parse_args()
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
    if a.estimate:
        return

    from google import genai

    client = genai.Client(api_key=api_key())
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    images = load_images(a.image)
    last_id_file = out_dir / LAST_ID_FILE
    previous_id = None
    if a.follow_up:
        if a.follow_up != "last":
            previous_id = a.follow_up
        elif last_id_file.exists():
            previous_id = last_id_file.read_text(encoding="utf-8").strip()
        else:
            sys.exit(f"Nothing to follow up on: {last_id_file} is missing.")

    if a.batch:
        saved = []
        for data, mime in run_batch(client, a, model, images):
            saved.append(save_image(data, mime, a.prompt, out_dir, len(saved)))
            save_sidecar(saved[-1], a)
            print(f"Saved: {saved[-1]}")
        if not saved:
            sys.exit("No image was produced.")
        return
    sys.exit(run_interactions(client, a, model, images, previous_id, out_dir, fx, usd))


def describe(exc):
    """One line about an exception, without the traceback."""
    text = " ".join(str(exc).split())
    return f"{type(exc).__name__}: {text[:500]}" if text else type(exc).__name__


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
        try:
            response = interact(client, a, model, images, previous_id)
        except KeyboardInterrupt:
            problems.append(f"{label}: interrupted while waiting for the API. "
                            "The request may still be generated and billed.")
            interrupted = True
            break
        except Exception as exc:
            print(f"{label} failed: {describe(exc)}", file=sys.stderr)
            problems.append(f"{label} failed: {describe(exc)}")
            break
        results = images_from_interaction(response)
        suggestions = suggestions_from_interaction(response) if a.search else None
        for data, mime in results:
            path = save_image(data, mime, a.prompt, out_dir, len(saved))
            save_sidecar(path, a, response.id, previous_id, suggestions)
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
