---
name: gemini-image
description: >
  Generate and edit images with Google's Nano Banana models through the Gemini API, using a
  single-file script that estimates the price before every call and reports the real cost after.
  Use whenever the user wants an AI-made or AI-edited image, even if they never say "Nano Banana":
  illustrations, website hero images or backgrounds, banners, icons, mockups, infographics,
  images with text, photo retouching, removing or adding things in a photo, style changes,
  combining several photos ("generate an image", "draw", "make a graphic", "edit this photo").
  Also use when the user hands over a finished prompt, even as JSON. For a specific animal
  species or real-world object where accuracy matters, generate only with 2-3 reference photos.
  Do not use for charts built from data (use code for those).
license: MIT
compatibility: Needs uv (https://docs.astral.sh/uv/) or Python 3.11+ with google-genai, network access, and a Gemini API key with billing enabled (image models have no free tier).
metadata:
  author: jakubcurik
  version: "1.0.0"
---

# Gemini image generation (Nano Banana)

`scripts/generate.py` (in this skill's folder) calls the Gemini API through the official `google-genai` library: the Interactions API for normal runs, the Batch API for `--batch`. Run it with `uv`, which installs the library by itself:

```bash
uv run --script <skill-dir>/scripts/generate.py "English prompt" [options]
```

`<skill-dir>` is the folder that holds this `SKILL.md`. Prices and model data live in `scripts/models.json`.

## Options

| Option | Meaning |
|---|---|
| `-m 2.1 / 2 / pro / lite` | model, default `2.1` |
| `-s 512 / 1K / 2K / 4K` | resolution, default `1K` (512 only on model `2`) |
| `-a 16:9` | aspect ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; also 1:4, 4:1, 1:8, 8:1 on models 2.1 and 2 |
| `-i photo.jpg` | input image for editing or as a reference, repeatable (max 14) |
| `-t minimal / medium / high` | thinking level (2.1: all three, default medium; 2 and lite: minimal/high; Pro: not configurable) |
| `--search` | Google Search grounding incl. image search (2.1, 2, Pro; not lite) |
| `--follow-up [ID]` | edit the last result (or the given interaction) with a new prompt; the model remembers the image |
| `-n 4` | number of images, each one is billed |
| `-o folder` | output folder, default `.cache/gemini-image` in the current directory |
| `--format png / jpeg` | output file format (jpeg is much smaller, good for the web) |
| `--prompt-file file` | read the prompt from a file instead of the command line |
| `--no-store` | ask Google not to keep the interaction (then `--follow-up` is impossible) |
| `--batch` | half price, the result can take up to 24 h (a test run on 2.1 took about 2 minutes; models 2.1 and lite only) |
| `--estimate` | only print the estimated price, generate nothing |
| `--currency CZK` | also show prices in another currency (rate from the Czech National Bank) |

The script checks that the model supports the requested combination before it calls the API. After a run it prints the real token usage and cost. Next to every image it saves a `.txt` file with the prompt, the options and the interaction ID, so you can compare variants and repeat a run.

Put a long prompt in a file (`--prompt-file .cache/prompt.txt`) rather than into the command line. That avoids shell quoting problems.

## Choosing a model

| Model | Use it when | Price 1K / 2K / 4K (USD) |
|---|---|---|
| **2.1** | almost always: cheapest of the full-featured models, good text in images, follow-up edits, search | 0.034 / 0.050 / 0.113 |
| **2** | only when you need 512 px or 2.1 fails. Deprecated by Google, no shutdown date yet | 0.067 / 0.101 / 0.151 (512 px: 0.045) |
| **pro** | the hardest prompts, lots of text, professional output; up to 6 object and 5 character references plus 3 style references | 0.134 / 0.134 / 0.24 |
| **lite** | lots of simple images, 1K only, no search, weak at multi-image input and follow-ups | 0.034 |

Prices are a snapshot from 26 Nov 2026. `--estimate` prints the number for the current options, and `scripts/models.json` is the one place to update when Google changes the price list (<https://ai.google.dev/gemini-api/docs/pricing>). Batch is half price where the table shows a batch price.

## Workflow

1. **Find out the purpose.** Where will the image be used (web, slides, print), which aspect ratio, will text appear in it? The purpose improves the result and sets the resolution: web usually 2K, print 4K, previews 1K.
2. **When anatomy or appearance matters** (a specific animal or plant species, a real object, building or product), never generate from text alone. Get 2-3 reference photos first (from the user, from the project, or found on the web), show them to the user to confirm they really show that species or thing, and pass them with `-i`. In the prompt, call them the binding reference for shape, proportions and coloring. From text alone the model confidently invents wrong anatomy: asked for a flower chafer of the genus *Eudicella*, it gave the forked horn of a stag beetle two horns and the domed body of a rhinoceros beetle.
3. **Write the prompt** following [references/prompting.md](references/prompting.md). Write it in English, in full sentences, not keyword lists. Show the user a short summary of what will be generated, in their language. For photos of people and real-life scenes, read section 6 (photorealism) of the guide.
   **A finished prompt from the user** (even JSON) is sent as it is if they want that. Check it first against section 5 of the guide: contradictions between fields (aspect ratio vs orientation), convert ratio and resolution to `-a` and `-s`, and warn that a `negative_prompt` field is read as plain text. If the user has no format preference, offer to convert JSON into flowing text.
4. **Watch the cost.** Every call costs money. When the estimate exceeds about 0.50 USD, or for more than 4 images, tell the user the price and wait for their go-ahead. After an error or a timeout, do not retry automatically: the request may have gone through and been billed.
5. **Look at the result.** Open the image with your image-viewing tool, compare it with the request (and with the reference photos), and give the user the file path and a short assessment. Check composition separately (cropping, headroom, position of the subject) and the direction of light; the model often ignores both.
6. **Refine with `--follow-up`.** Small changes go through `--follow-up`, and the prompt lists what must not change. It is cheaper and more consistent than generating again.
   **Same image in a higher resolution or another aspect ratio:** sending the same prompt again with `-s 4K` or `-a 9:16` gives a completely different image (a different person, for portraits). To keep the image, use `--follow-up` with the new `-s` or `-a` and a prompt like "Recreate this exact photo as a horizontal image... Keep everything else the same." Tested on 26 Oct 2026: a 9:16 portrait converted to 16:9 kept face, hair, clothes, room and light, and the model only painted in the surroundings. The model redraws the image, so compare the result with the original. If it is unclear whether the user wants the same image or a new variant, ask.
7. **Comparing variants** (two prompts, JSON vs. text, two models): do not conclude anything from a single image, differences are often chance. For a real comparison generate at least 3-4 images per variant (`-n`) and state the price first.
8. **Clean up.** `.cache/gemini-image` belongs in `.gitignore`. Move an image that will be used into the project, where it belongs.

## API key

The script looks for the key in `GEMINI_API_KEY` (or `GOOGLE_API_KEY`), otherwise in `~/.config/gemini-image/api-key`. If it is missing, ask the user to create one in [Google AI Studio](https://aistudio.google.com/apikey) with billing enabled and to save it themselves. Never print the key or store it in a project: it could be abused on the user's account.

## Limits and good to know

- The model invents details. A specific species, real object or building needs 2-3 reference photos through `-i` (step 2); neither text nor `--search` is enough. Even with photos, check the result against them.
- All images carry an invisible SynthID watermark.
- Refusals for content reasons (`PROHIBITED_CONTENT`, `IMAGE_RECITATION`): rephrase more neutrally, do not resend the same prompt.
- Gemini has no negative prompt. Describe what should be in the image ("an empty street" instead of "no cars"). One exception: for text, "No other text." works.
- An aspect-ratio instruction inside the prompt may be ignored; only `-a` is reliable.
- Interactions are stored by Google so that follow-ups work: 55 days on paid projects (1 day on the free tier), unless you pass `--no-store`. Do not send sensitive photos without `--no-store`.
- `--search` is billed separately from the image: 5,000 grounded prompts per month are free, then 14 USD per 1,000 search queries. Google requires the returned search suggestions to be displayed when you publish grounded output; the script saves them next to the image. Search with real photos of people is not supported.
- Google's own `gemini-api` CLI (`gemini-api image "..."`) generates images too. If it is installed, it works as an alternative for the generation step. It does not estimate cost, validate options, run batches or give prompting guidance, so the workflow above still applies.
- Models and prices change. When they do, update `scripts/models.json` and the model table above from the [price list](https://ai.google.dev/gemini-api/docs/pricing) and the [documentation](https://ai.google.dev/gemini-api/docs/image-generation).
