# gemini-image

An agent skill for generating and editing images with Google's **Nano Banana** models through the Gemini API. It adds what a bare API call does not give you: a **price estimate before every call**, the **real cost after**, option checks, a workflow that avoids wasted money, and a prompting guide.

> Unofficial. Not affiliated with or endorsed by Google. "Nano Banana" and "Gemini" are Google's names for its image models and API.

It follows the open [Agent Skills](https://agentskills.io) format, so it works in Claude Code and in other agents that load `SKILL.md` skills (Codex, Gemini CLI, Cursor and others).

## Why this exists when Google ships a CLI

Google's own `gemini-api` CLI (`gemini-api image "..."`) and its official skills handle the *call*. This skill handles everything around it:

| | Google `gemini-api` CLI + skills | gemini-image |
|---|---|---|
| Price estimate before a call, real cost after | no | yes |
| Cost gate: the agent asks before expensive runs | no | yes |
| Checks that the model supports your size / ratio / thinking / search combination | no, the API rejects it afterwards | yes |
| Batch (half price) | only through raw `--body` JSON | `--batch` |
| Follow-up edits without copying interaction IDs | manual | `--follow-up` |
| Prompt and options saved next to each image | no | yes |
| Prompting guide, templates, common mistakes | no | yes |
| "Never generate a real species or object from text alone" rule | no | yes |
| Install | Go binary via `curl \| bash` | one Python file, run by `uv` |

If the CLI is installed, the skill treats it as an alternative for the generation step. It is a beta that moves fast, so the table above will drift. Check both before choosing.

## Install

**Claude Code (plugin marketplace)**

```
/plugin marketplace add jakubcurik/gemini-image
/plugin install gemini-image@gemini-image
```

**Any agent, via [`npx skills`](https://github.com/vercel-labs/skills)**

```bash
npx skills add jakubcurik/gemini-image
```

**Manual**

Copy `skills/gemini-image/` into your agent's skills folder, for example `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex, Gemini CLI, Cursor).

### Requirements

- [`uv`](https://docs.astral.sh/uv/) (it installs `google-genai` and Python 3.11+ on the fly), or Python 3.11+ with `pip install "google-genai>=3.6,<4"`.
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) **with billing enabled**. Image models have no free tier.

Give the script the key in one of two ways:

```bash
export GEMINI_API_KEY="your-key"
# or save it once (outside any repository):
mkdir -p ~/.config/gemini-image && printf '%s' "your-key" > ~/.config/gemini-image/api-key
```

## Use it

Just ask your agent for an image: "make a hero image for my coffee shop site, 16:9", "remove the car from this photo", "combine these two photos". The skill triggers on its own, asks about the purpose, writes the prompt, tells you the price when it is not trivial, runs the script and checks the result.

You can also run the script directly:

```bash
S=skills/gemini-image/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table, soft daylight" --estimate
uv run --script $S "A flat illustration of a red apple on a white table, soft daylight" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency EUR
```

Images land in `.cache/gemini-image/` by default, each with a `.txt` file holding the prompt, options and interaction ID.

### Options

| Option | Meaning |
|---|---|
| `-m 2.1 / 2 / pro / lite` | model, default `2.1` |
| `-s 512 / 1K / 2K / 4K` | resolution, default `1K` (512 only on model `2`) |
| `-a 16:9` | aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; also 1:4, 4:1, 1:8, 8:1 on 2.1 and 2) |
| `-i photo.jpg` | input image for editing or reference, repeatable, max 14 |
| `-t minimal / medium / high` | thinking level (depends on the model) |
| `--search` | Google Search grounding, including image search (not on `lite`) |
| `--follow-up [ID]` | continue from the last (or a given) result |
| `-n 4` | number of images, each billed separately |
| `-o folder` | output folder |
| `--format png / jpeg` | output file format |
| `--prompt-file file` | read the prompt from a file |
| `--no-store` | ask Google not to keep the interaction (disables follow-ups on it) |
| `--batch` | half price, up to 24 h (models 2.1 and lite) |
| `--estimate` | print the price estimate only |
| `--currency CZK` | also show prices in this currency (rate from the Czech National Bank) |

### Models and prices (snapshot 26 Nov 2026)

| Model | Best for | 1K / 2K / 4K per image (USD) |
|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | almost everything | 0.034 / 0.050 / 0.113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; deprecated by Google, no shutdown date yet | 0.067 / 0.101 / 0.151 |
| `pro` (`gemini-3-pro-image`) | hardest prompts, a lot of text | 0.134 / 0.134 / 0.24 |
| `lite` (`gemini-3.1-flash-lite-image`) | many simple 1K images, no search | 0.034 |

Prices and model data live in [`skills/gemini-image/scripts/models.json`](skills/gemini-image/scripts/models.json), which is the one file to update when Google changes the [price list](https://ai.google.dev/gemini-api/docs/pricing). `--search` is billed on top (5,000 grounded prompts per month free, then 14 USD per 1,000 search queries).

## Things worth knowing

- **Privacy.** Google stores interactions so follow-ups work: 55 days on paid projects, 1 day on the free tier. Use `--no-store` for sensitive photos. All generated images carry an invisible SynthID watermark.
- **Accuracy.** The model invents details. For a specific animal species, real object or building, give it 2-3 reference photos with `-i`. Text alone, and even `--search`, is not enough. The skill enforces this in its workflow.
- **Errors are not retried automatically.** A request that timed out may still have been billed.
- **Search results.** When you publish output generated with `--search`, Google requires showing its search suggestions. The script saves them next to the image.
- **Your key never goes into a project.** It comes from the environment or `~/.config/gemini-image/api-key`.

## Tests

Offline tests (option validation, price maths, model catalog) need no API key and no network:

```bash
python -m unittest discover -s tests
```

The API paths were checked by hand against `google-genai` 3.6.1 on 26 Nov 2026: generation, JPEG output, follow-up, search with suggestions, `--no-store`, a batch job on model 2.1 (finished in about 2 minutes), and the API error for `lite` + search. Batch on `lite` has a published price but was not run. `pro` and `2` have no published batch price, so `--batch` is disabled for them.

## Layout

```
.claude-plugin/          plugin and marketplace manifests (Claude Code)
skills/gemini-image/
  SKILL.md               the skill: workflow, options, model choice, limits
  references/prompting.md  prompting guide and templates
  scripts/generate.py    the script (uv, single file)
  scripts/models.json    model IDs, prices, capabilities
tests/                   offline tests
```

## Contributing

Issues and pull requests are welcome, especially when Google changes models, prices or the API. Please update `models.json` and the tables in `SKILL.md` and this README together.

## License

[MIT](LICENSE)
