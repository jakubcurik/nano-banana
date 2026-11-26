<p align="center">
  <img src="assets/logo.png" width="132" alt="nano-banana logo: a glossy yellow banana character waving on a dark graphite square">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>Images from your coding agent, with the bill under control.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/tests.yml?branch=main&style=flat-square&label=tests&labelColor=0f1b2d&cacheSeconds=600"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validate" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/validate.yml?branch=main&style=flat-square&label=validate&labelColor=0f1b2d&cacheSeconds=600"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Release" src="https://img.shields.io/github/v/release/jakubcurik/nano-banana?style=flat-square&label=release&labelColor=0f1b2d&color=ffd54a&cacheSeconds=600"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/jakubcurik/nano-banana?style=flat-square&labelColor=0f1b2d&color=ffd54a&cacheSeconds=600"></a>
</p>

<p align="center">
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude_Code-plugin-ffd54a?style=flat-square&labelColor=0f1b2d">
  <a href="https://agentskills.io"><img alt="Agent Skills format" src="https://img.shields.io/badge/Agent_Skills-compatible-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <img alt="Python 3.11 or newer" src="https://img.shields.io/badge/python-3.11%2B-ffd54a?style=flat-square&labelColor=0f1b2d">
  <img alt="Gemini API" src="https://img.shields.io/badge/Gemini_API-Nano_Banana-ffd54a?style=flat-square&labelColor=0f1b2d">
</p>

<p align="center">
  <a href="#install">Install</a> &middot;
  <a href="#quick-start">Quick start</a> &middot;
  <a href="#gallery">Gallery</a> &middot;
  <a href="#how-it-works">How it works</a> &middot;
  <a href="#models-and-prices">Models and prices</a> &middot;
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <sub>English &middot;
  <a href="i18n/README.zh-CN.md">简体中文</a> &middot;
  <a href="i18n/README.es.md">Español</a> &middot;
  <a href="i18n/README.ja.md">日本語</a> &middot;
  <a href="i18n/README.pt-BR.md">Português (Brasil)</a> &middot;
  <a href="i18n/README.de.md">Deutsch</a> &middot;
  <a href="i18n/README.fr.md">Français</a> &middot;
  <a href="i18n/README.ko.md">한국어</a> &middot;
  <a href="i18n/README.cs.md">Čeština</a></sub>
</p>

<p align="center">
  <img src="assets/hero.jpg" width="880" alt="A glossy 3D banana character paints a sunny landscape on a small easel, next to a long paper receipt and a few gold coins. The title reads nano-banana.">
</p>

nano-banana is an agent skill that lets Claude Code and other coding agents make and edit images with Google's Nano Banana models. It also keeps track of what that costs.

Ask an agent for a hero image and you get one. Ask it to "try a few more variations" and a plain API call can run a dozen 4K generations while you are still looking at the first. Every image is billed, and nothing in the chat tells you how much.

This skill prints the estimated price before each call and the real cost after it. It checks your options against what the chosen model supports, so a wrong size or an unsupported thinking level fails on your machine and not at the API. For everything else it gives the agent a short routine: ask what the image is for, get reference photos when the subject has to look like something real, write the prompt in English, and look at the result before calling it done.

<sub>Unofficial. Not affiliated with or endorsed by Google. "Nano Banana" and "Gemini" are Google's names for its image models and API.</sub>

## See it work

<p align="center">
  <img src="assets/terminal.png" width="880" alt="Terminal output of one generation: the model, an estimated cost of 0.0504 USD, the interaction ID, the usage of 1680 image tokens for 0.0504 USD, and the saved file path.">
</p>

That is a real run. A 2K image on the default model costs about five US cents, and you see the number before the call and again after it.

## Gallery

Apart from the text and the terminal screenshot, every image in this README was made with the skill. The prompts are in [`assets/prompts`](assets/prompts).

<p align="center">
  <img src="assets/gallery/1-illustration.jpg" width="760" alt="A flat illustration of a steaming coffee cup and a croissant on a wooden counter by a sunny window, with empty space on the right for a headline.">
  <br>
  <sub><b>Text to image.</b> Model 2.1, 2K, 16:9, about 5 cents.</sub>
</p>

<p align="center">
  <img src="assets/gallery/2a-edit-before.jpg" width="372" alt="A plain white ceramic mug on a light grey studio background.">
  <img src="assets/gallery/2b-edit-after.jpg" width="372" alt="The same white mug on a rustic wooden table by a sunny window, next to a small bowl of coffee beans.">
  <br>
  <sub><b>Edit with <code>--follow-up</code>.</b> Same mug, new scene. Model 2.1, 2K, about 5 cents per image.</sub>
</p>

<p align="center">
  <img src="assets/gallery/3-poster-text.jpg" width="400" alt="A minimalist cafe poster that reads FRESH COFFEE above a flat coffee cup, with the line Open daily from 8 to 18.">
  <br>
  <sub><b>Text in an image.</b> Model Pro, 2K, 4:5, about 13 cents.</sub>
</p>

## Install

Claude Code, from the plugin marketplace:

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

Any agent that reads `SKILL.md` skills, through [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add jakubcurik/nano-banana
```

Or copy `skills/nano-banana/` into your agent's skills folder by hand, for example `~/.claude/skills/` for Claude Code or `~/.agents/skills/` for Codex, Gemini CLI and Cursor.

You also need:

- [`uv`](https://docs.astral.sh/uv/), which fetches `google-genai` and Python 3.11+ on its own. Without it, install Python 3.11+ and `pip install "google-genai>=3.6,<4"`.
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey), with billing turned on. The image models have no free tier.

Give the script the key through the environment, or save it once outside any repository:

```bash
export GEMINI_API_KEY="your-key"
# or
mkdir -p ~/.config/nano-banana && printf '%s' "your-key" > ~/.config/nano-banana/api-key
```

## Quick start

Ask your agent: "make a hero image for my coffee shop site, 16:9", "remove the car from this photo", "combine these two photos". The skill triggers on its own. It asks what the image is for, writes the prompt, tells you the price when it is not trivial, runs the script and checks the result.

You can also call the script yourself:

```bash
S=skills/nano-banana/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table" --estimate
uv run --script $S "A flat illustration of a red apple on a white table" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency EUR
```

Images land in `.cache/nano-banana/`, each next to a `.txt` file with the prompt, the options and the interaction ID.

<details>
<summary>All options</summary>

| Option | Meaning |
|---|---|
| `-m 2.1 / 2 / pro / lite` | model, default `2.1` |
| `-s 512 / 1K / 2K / 4K` | resolution, default `1K` (512 only on model `2`) |
| `-a 16:9` | aspect ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; also 1:4, 4:1, 1:8, 8:1 on 2.1 and 2 |
| `-i photo.jpg` | input image for editing or as a reference, repeatable, max 14 |
| `-t minimal / medium / high` | thinking level, depends on the model |
| `--search` | Google Search grounding, including image search (not on `lite`) |
| `--follow-up [ID]` | continue from the last result, or from a given interaction |
| `-n 4` | number of images, each billed separately |
| `-o folder` | output folder |
| `--format png / jpeg` | output file format |
| `--prompt-file file` | read the prompt from a file |
| `--no-store` | ask Google not to keep the interaction (this disables follow-ups on it) |
| `--batch` | half price, up to 24 h (models 2.1 and lite) |
| `--estimate` | print the price estimate and stop |
| `--currency CZK` | also show prices in this currency (rate from the Czech National Bank) |

</details>

## How it works

The skill makes the agent work in a fixed order. It first asks what the image is for. If the picture has to show a real species, product or place, it gets two or three reference photos and asks you to confirm them. Then it writes the prompt in English and estimates the price, and it asks you first when the estimate is above about 0.50 USD or more than four images are wanted. After generating, it looks at the result and fixes small things with a follow-up instead of starting over.

The full workflow is in [`SKILL.md`](skills/nano-banana/SKILL.md). Prompt templates, edit templates and a list of common mistakes are in [`references/prompting.md`](skills/nano-banana/references/prompting.md).

## Models and prices

Snapshot from 26 November 2026, USD per image.

| Model | Best for | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | almost everything | 0.034 | 0.050 | 0.113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; deprecated by Google, no shutdown date yet | 0.067 | 0.101 | 0.151 |
| `pro` (`gemini-3-pro-image`) | the hardest prompts, a lot of text | 0.134 | 0.134 | 0.240 |
| `lite` (`gemini-3.1-flash-lite-image`) | many simple images, 1K only, no search | 0.034 | n/a | n/a |

Prices and model data live in [`models.json`](skills/nano-banana/scripts/models.json), the one file to edit when Google changes its [price list](https://ai.google.dev/gemini-api/docs/pricing). `--search` is billed on top: 5,000 grounded prompts per month are free, then 14 USD per 1,000 search queries.

## Good to know

- Google stores interactions so follow-ups work: 55 days on paid projects, 1 day on the free tier. Use `--no-store` for sensitive photos.
- Every generated image carries an invisible SynthID watermark.
- The model invents details. When a picture has to match a real species, product or building, give it 2-3 reference photos with `-i`. The skill's workflow insists on that.
- A request that times out may still have been billed, so the script never retries on its own.
- If you publish output made with `--search`, Google requires showing its search suggestions. The script saves them next to the image.

## FAQ

**Google has its own `gemini-api` CLI. Why use this?**
The CLI makes the call, and it does that well. This skill adds what sits around the call. You may want both.

| | Google `gemini-api` CLI and skills | nano-banana |
|---|---|---|
| Price estimate before, real cost after | no | yes |
| The agent asks before expensive runs | no | yes |
| Options checked against the model | no, the API rejects them | yes |
| Follow-up edits without copying IDs | manual | `--follow-up` |
| Prompt and options saved next to each image | no | yes |
| Prompting guide and templates | no | yes |

The CLI is a beta that moves quickly, so check both before you choose.

**Does it work outside Claude Code?**
The skill follows the open [Agent Skills](https://agentskills.io) format, so other agents that load `SKILL.md` files can use it. I have tested it in Claude Code only.

**Prices changed. What do I edit?**
`skills/nano-banana/scripts/models.json`, and the tables in `SKILL.md` and here.

**Why does it ask for reference photos?**
Without one, the model fills in the details of a real thing from its imagination, and the result looks plausible and wrong.

## Contributing

Issues and pull requests are welcome, especially when Google changes models, prices or the API. Update `models.json` and the tables in `SKILL.md` and this README together. The translations in `i18n/` were made with the help of AI, and corrections are welcome.

The offline tests need no API key and no network:

```bash
python -m unittest discover -s tests
```

## License

[MIT](LICENSE)
