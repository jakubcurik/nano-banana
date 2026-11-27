---
name: nano-banana
description: >
  Generate and edit images with Google's Nano Banana models through the Gemini API, using a
  single-file script that estimates the price before every call and reports the real cost after.
  Use whenever the user wants an AI-made or AI-edited image, even if they never say "Nano Banana":
  illustrations, website hero images or backgrounds, banners, icons, mockups, infographics,
  images with text, photo retouching, removing or adding things in a photo, style changes,
  combining several photos ("generate an image", "draw", "make a graphic", "edit this photo").
  Also use when the user hands over a finished prompt, even as JSON, and to finish a generated
  image for a website (exact pixel size, WebP, transparent background). For a specific animal
  species or real-world object where accuracy matters, generate only with 2-3 reference photos.
  Do not use for charts built from data (use code for those).
license: MIT
compatibility: Needs uv (https://docs.astral.sh/uv/) or Python 3.11+ with google-genai (and Pillow for finish.py), network access, and a Gemini API key with billing enabled (image models have no free tier).
metadata:
  author: jakubcurik
  version: "1.0.0"
---

# Gemini image generation (Nano Banana)

`scripts/generate.py` (in this skill's folder) calls the Gemini API through the official `google-genai` library: the Interactions API for normal runs, the Batch API for `--batch`. Run it with `uv`, which installs the library by itself:

```bash
uv run --script <skill-dir>/scripts/generate.py "English prompt" [options]
```

`<skill-dir>` is the folder that holds this `SKILL.md`. Prices and model data live in `scripts/models.json`. `scripts/finish.py` crops, converts and cuts out finished images (see "Finishing for the web").

## Options

| Option | Meaning |
|---|---|
| `-m 2.1 / 2 / pro / lite` | model, default `2.1` |
| `-s 512 / 1K / 2K / 4K` | resolution, default `1K` (512 only on model `2`) |
| `-a 16:9` | aspect ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; also 1:4, 4:1, 1:8, 8:1 on models 2.1 and 2 |
| `-i photo.jpg` | input image for editing or as a reference, repeatable (max 14, together at most about 14 MB) |
| `-t minimal / medium / high` | thinking level (2.1: all three, default medium; 2 and lite: minimal/high; Pro: not configurable) |
| `--search` | Google Search grounding incl. image search (2.1, 2, Pro; not lite) |
| `--follow-up [IMAGE or ID]` | edit an earlier result with a new prompt; the model remembers the image. No value: the last result. An image path: that image (its `.txt` holds the ID). Or an interaction ID |
| `-n 4` | number of images, each one is billed |
| `-o folder` | output folder, default `.cache/nano-banana` in the current directory (created with a `.gitignore` that ignores it) |
| `--name hero` | file-name stem instead of the start of the prompt |
| `--format png / jpeg` | output file format (jpeg is much smaller) |
| `--prompt-file file` | read the prompt from a file instead of the command line |
| `--no-store` | ask Google not to keep the interaction (then `--follow-up` is impossible) |
| `--delete IMAGE or ID` | delete a stored interaction at Google (sensitive photos); generates nothing |
| `--batch` | half price, the result can take up to 24 h (models 2.1 and lite only); the job is recorded in the output folder |
| `--wait 8` | with `--batch`: minutes to wait before exiting (default 8, `0` = submit and exit) |
| `--batch-result [JOB]` | collect a batch job: saves its images if it is done, otherwise reports its state. Default: the last job recorded in the output folder |
| `--estimate` | only print the estimated price, generate nothing |
| `--max-cost 0.50` | stop before the API call when the estimate is above this many USD (default 0.50) |
| `--currency CZK` | also show prices in another currency (rate from the Czech National Bank) |

The script checks that the model supports the requested combination before it calls the API. For every call it prints how long the API took, the path of each image as soon as it is saved, and the real cost from the reported tokens: image output, thinking and input (thinking usually adds most of a cent per image). Next to every image it saves a `.txt` file with the prompt, the options, the interaction ID, the duration and the cost. If a call of an `-n` run fails, the images saved before it stay, the run stops, and a summary lists what was saved and what failed (exit code 1).

Defaults for `--currency` and `--max-cost` can come from the environment (`NANO_BANANA_CURRENCY`, `NANO_BANANA_MAX_COST`) or from `~/.config/nano-banana/config.json` (`{"currency": "CZK", "max_cost": 0.5}`). The command line wins over the environment, the environment over the file.

Put a long prompt in a file (`--prompt-file .cache/prompt.txt`) rather than into the command line. That avoids shell quoting problems.

## Choosing a model

| Model | Use it when | Price 1K / 2K / 4K (USD) |
|---|---|---|
| **2.1** | almost always: cheapest of the full-featured models, good text in images, follow-up edits, search; up to 10 object and 4 character references | 0.034 / 0.050 / 0.113 |
| **2** | only when you need 512 px or 2.1 fails. Deprecated by Google, no shutdown date yet; up to 10 object and 4 character references | 0.067 / 0.101 / 0.151 (512 px: 0.045) |
| **pro** | the hardest prompts, lots of text, professional output; up to 6 object and 5 character references plus 3 style references | 0.134 / 0.134 / 0.24 |
| **lite** | lots of simple images, 1K only, no search, weak at multi-image input and follow-ups | 0.034 |

All models take at most 14 input images in total. Prices are a snapshot from 28 Nov 2026 (USD per image, image output only). `--estimate` prints the number for the current options, and `scripts/models.json` is the one place to update when Google changes the price list (<https://ai.google.dev/gemini-api/docs/pricing>); a test checks that this table and the READMEs agree with it. Batch is half price where the table shows a batch price.

## Time limits of your shell

One image usually takes 10-30 seconds, but Google publishes no latency figures and a slow call can take longer. Measured on 26-27 Nov 2026 as the time between consecutive images of `-n` runs: model 2.1 at 1K 12-30 s per image (the longer ones with `-t high`), at 2K 21-25 s; Pro 16 s at 1K and 21-23 s at 2K. 4K was not measured. The script prints the real duration of every call and stores it in the `.txt` file; use those numbers once you have them.

A shell call killed by its timeout loses the image, and the image may still be billed. So:

- Set the timeout of the shell call generously: at least 2 minutes per image, and the tool's maximum (often 10 minutes) for `-n` runs or 4K. A default 2-minute timeout is too short for `-n 4`.
- Run anything longer in the background and read its output when it ends.
- Batch jobs: the script waits `--wait` minutes (default 8, under a 10-minute tool limit) and exits with the command to collect the result later.

## Workflow

1. **Work out the purpose.** Infer from the request and the project first: where the image goes (a hero in a 16:9 slot, an Open Graph image, a print flyer), the aspect ratio, whether text appears in it, the style the project already uses. Ask only for what is missing and changes the result. The purpose sets the resolution: web usually 2K, print 4K, previews 1K.
2. **When anatomy or appearance matters** (a specific animal or plant species, a real object, building or product), never generate from text alone. Get 2-3 reference photos first (from the user, from the project, or found on the web), show them to the user to confirm they really show that species or thing, and pass them with `-i`. In the prompt, call them the binding reference for shape, proportions and coloring. From text alone the model confidently invents details that look plausible and are wrong.
3. **Write the prompt** following [references/prompting.md](references/prompting.md). Write it in English, in full sentences, not keyword lists. Show the user a short summary of what will be generated, in their language. For photos of people and real-life scenes, read section 6 (photorealism) of the guide.
   **A finished prompt from the user** (even JSON) is sent as it is if they want that. Check it first against section 5 of the guide: contradictions between fields (aspect ratio vs orientation), convert ratio and resolution to `-a` and `-s`, and warn that a `negative_prompt` field is read as plain text. If the user has no format preference, offer to convert JSON into flowing text.
4. **Watch the cost.** Every call costs money. The script refuses to run when the estimate is above `--max-cost` (default 0.50 USD) and prints the price. Then tell the user the price and wait for their go-ahead; raise `--max-cost` only after they agree, never on your own. Ask first for more than 4 images too, even when they fit under the limit. After a run, report the real cost it printed.
   **After an error,** read the `Retry:` line the script prints. A rejected request (4xx: invalid options, key, billing, quota or rate limit) was not billed, so fix the cause and run it again. A server error (5xx), a timeout or a dropped connection may have been generated and billed: do not retry on your own, tell the user and let them decide. The `Saved:` lines before the error are real images; use them.
5. **Look at the result.** Open the image with your image-viewing tool, compare it with the request (and with the reference photos), and give the user the file path and a short assessment. Check composition separately (cropping, headroom, position of the subject) and the direction of light; the model often ignores both.
6. **Refine with `--follow-up`.** Small changes go through `--follow-up`, and the prompt lists what must not change. It is cheaper and more consistent than generating again. After `-n` variants, continue from the one the user picked: `--follow-up path/to/that-image.png` (without a value it continues from the last image generated, which may be a different variant).
   **Faithful edits** (everything must stay the same except one thing, such as the light or the time of day): pass the original image with `-i` and say in the prompt exactly what must not change (face, expression, direction of the gaze, pose, hands, objects, clothing, framing). In a test this kept far more of the original than `--follow-up`, which redraws the whole scene and tends to shift the pose and the gaze. Compare the result with the original and rerun a few times: the gaze and the head angle drift most.
   **Same image in a higher resolution or another aspect ratio:** sending the same prompt again with `-s 4K` or `-a 9:16` gives a completely different image (a different person, for portraits). To keep the image, use `--follow-up` with the new `-s` or `-a` and a prompt like "Recreate this exact photo as a horizontal image... Keep everything else the same." In testing, a vertical portrait converted to horizontal this way kept the person, clothing, setting and light, and the model only painted in the surroundings. The model redraws the image, so compare the result with the original. If it is unclear whether the user wants the same image or a new variant, ask.
7. **A series with the same character or style** (several scenes with one mascot, a set of icons): pass the best image so far with `-i` in every later prompt and name it as the reference for the character or style ("the banana character from the provided image"). Google advises including previously generated images in later prompts to keep them consistent. Mind the reference limits in the model table.
8. **Comparing variants** (two prompts, JSON vs. text, two models): do not conclude anything from a single image, differences are often chance. For a real comparison generate at least 3-4 images per variant (`-n`) and state the price first.
9. **Finish and clean up.** Images in the default `.cache/nano-banana` are ignored by git through the folder's own `.gitignore`. Move an image that will be used into the project, finished for its purpose (next section).

## Batch jobs

`--batch` is half price but can take up to 24 hours (a test run on 2.1 took about 2 minutes). The script records the job in `batch-jobs.json` in the output folder, waits up to `--wait` minutes, and saves the images right away if the job is done by then. Otherwise it exits normally and prints the command to collect the result. Collect later with `--batch-result` (the last recorded job) or `--batch-result batches/...`, using the same `-o`. A job that is still running is only reported; a finished job is saved once, and collecting it again lists the files instead of duplicating them. Ctrl+C while waiting stops only the waiting; the job keeps running and is billed.

## Finishing for the web

The model returns fixed aspect ratios and sizes. For exact pixel dimensions, generate the nearest aspect ratio, then crop with `finish.py` (Pillow, installed by `uv`):

```bash
uv run --script <skill-dir>/scripts/finish.py hero.png --size 1200x630 --format webp
```

| Target | Pixels | Generate with |
|---|---|---|
| Open Graph / social share image | 1200 x 630 | `-a 16:9 -s 2K` |
| Full-width hero | 1920 x 1080 | `-a 16:9 -s 2K` |
| Square product or avatar | 1080 x 1080 | `-a 1:1 -s 2K` (1K is 1024 px, too small) |
| Instagram portrait | 1080 x 1350 | `-a 4:5 -s 2K` |
| Favicon / app icon source | 512 x 512 | `-a 1:1` |

- `--size WxH` scales and crops to exactly that size (cover fit); `--keep top / left / bottom-right ...` chooses the part that stays (default center). `--size 1200x` only scales.
- `--format webp` (or `avif`, `jpeg`, `png`) with `--quality 82` by default. WebP is the usual choice for photos and illustrations; PNG for flat graphics that need sharp edges.
- **Transparency.** Google's documentation says nothing about transparent output. A live check was planned for this version but could not run (the test account had no credit), so assume the model returns no alpha channel even when the prompt asks for one. Ask for a single flat background color that does not appear in the subject ("on a plain, solid light grey background, no shadow"), then run `finish.py logo.png --transparent` (color from the corners) or `--transparent "#d8d8d6"`. It removes only background connected to the image border, so the same color inside the subject stays. It is a color key, not a matting model: soft shadows, gradients, glows and hair stay or leave a fringe. On a generated sticker with a slight drop shadow, the flat grey vanished cleanly but the shadow remained as a grey rim. Open the result on a dark background and check the edges.
- `finish.py` writes next to the input (`hero-1200x630.webp`) or to `-o`, never over the input or into this skill's folder.

## API key

The script looks for the key in `GEMINI_API_KEY` (or `GOOGLE_API_KEY`), otherwise in `~/.config/nano-banana/api-key`. If it is missing, ask the user to create one in [Google AI Studio](https://aistudio.google.com/apikey) with billing enabled and to save it themselves. Never print the key or store it in a project: it could be abused on the user's account. An error 402 or a message about depleted prepayment credits means the account needs credit; that request was not billed.

## Limits and good to know

- The model invents details. A specific species, real object or building needs 2-3 reference photos through `-i` (step 2); neither text nor `--search` is enough. Even with photos, check the result against them.
- All images carry an invisible SynthID watermark.
- Refusals for content reasons (`PROHIBITED_CONTENT`, `IMAGE_RECITATION`): rephrase more neutrally, do not resend the same prompt.
- Gemini has no negative prompt. Describe what should be in the image ("an empty street" instead of "no cars"). One exception: for text, "No other text." works.
- An aspect-ratio instruction inside the prompt may be ignored; only `-a` is reliable.
- Interactions are stored by Google so that follow-ups work: 55 days on paid projects (1 day on the free tier), unless you pass `--no-store`. Do not send sensitive photos without `--no-store`; if they were sent already, remove them with `--delete IMAGE` (and the earlier interaction it names, if any).
- `--search` is billed separately from the image: 5,000 grounded prompts per month are free, then 14 USD per 1,000 search queries. Google requires the returned search suggestions to be displayed when you publish grounded output; the script saves them next to the image. Search with real photos of people is not supported.
- Google's own `gemini-api` CLI (`gemini-api image "..."`) generates images too. If it is installed, it works as an alternative for the generation step. It does not estimate cost, validate options, run batches or give prompting guidance, so the workflow above still applies.
- Models and prices change. When they do, update `scripts/models.json` and the model table above from the [price list](https://ai.google.dev/gemini-api/docs/pricing) and the [documentation](https://ai.google.dev/gemini-api/docs/image-generation).
