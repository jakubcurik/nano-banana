# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [1.1.1] - 2026-11-28

### Fixed

- The real cost counts all output tokens. Real responses list only the image tokens per modality while the total output is a few hundred tokens higher (the model's short text answer among them); those are now billed at the text rate.
- `--format png` is refused before the call on models 2.1, 2 and lite, whose API accepts only JPEG. `models.json` records the accepted formats per model.
- A follow-up on a deleted or expired interaction explains what happened and suggests `-i` instead.
- The help no longer claims that new images default to 1:1; without `-a` the model picks the shape (16:9 in tests).

### Changed

- Documentation from live checks: measured call durations, what happens when you ask for transparency (the model paints a checkerboard into a JPEG), the output format, and a new terminal screenshot from a 1.1 run.

## [1.1.0] - 2026-11-28

### Added

- Batch jobs are recorded in `batch-jobs.json` in the output folder. `--wait MINUTES` (default 8, `0` = submit and exit) limits the wait, and `--batch-result [JOB]` collects the images in a later run. A job is collected only once.
- `--max-cost USD`: the script stops before the API call when the estimate is above the limit.
- After an API error the script says whether a retry is safe: a rejected request (4xx) was not billed, a server error or timeout may have been.
- The duration of every call is printed and stored in the `.txt` next to the image, together with the call's cost.
- `--follow-up path/to/image.png` continues from a picked image, reading the interaction ID from its `.txt`.
- `--delete IMAGE or ID` deletes a stored interaction at Google.
- `--name` sets the file-name stem.
- Defaults for the currency and the cost limit from `NANO_BANANA_CURRENCY` / `NANO_BANANA_MAX_COST` or `~/.config/nano-banana/config.json`.
- `scripts/finish.py`: crop to exact pixel sizes, convert to WebP, AVIF, JPEG or PNG, and make a flat background transparent.
- Skill instructions for shell time limits, finishing images for the web, series with a consistent character, and continuing from a picked variant.
- Tests for response parsing, costs, batch handling, `finish.py`, and a check that the documented prices match `models.json`.

### Changed

- **The default cost limit is 0.50 USD.** Runs whose estimate is higher (for example `-n 20 -s 4K`) now stop until you pass a higher `--max-cost`. Until 1.0.0 this was only an instruction to the agent.
- The real cost after a call now counts thinking and input tokens at their own rates, so it is slightly higher than the image-only estimate. `models.json` holds the text and input rates for every model.
- With `-n`, each image path is printed as soon as the file exists. The first API error stops the run with a summary and a non-zero exit code instead of a traceback.
- The default output folder `.cache/nano-banana` is created with a `.gitignore` that ignores it.
- Input images larger than about 14 MB in total are refused before the call.
- The agent infers purpose, aspect ratio and text from the request and the project, and asks only about what is missing.

### Fixed

- Normal output and errors no longer appear out of order when an agent reads them through a pipe.

## [1.0.0] - 2026-11-26

First release.

- Generate and edit images with the Nano Banana models (2.1, 2, Pro, Lite) through the Gemini API.
- Price estimate before every call, real cost after, in USD or another currency.
- Options are checked against the chosen model before the API is called.
- Follow-up edits, batch (half price), Google Search grounding, `--no-store`, JPEG or PNG output.
- A workflow for the agent and a prompting guide with templates.

[1.1.1]: https://github.com/jakubcurik/nano-banana/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/jakubcurik/nano-banana/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/jakubcurik/nano-banana/releases/tag/v1.0.0
