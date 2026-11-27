# Prompting guide for Nano Banana

Based on Google's [image generation guide](https://ai.google.dev/gemini-api/docs/image-generation) (checked 26 Nov 2026). Sections 5 and 6 come from community sources and from my own experiments on 26 Oct 2026. Keep the templates in English: the models work best in English.

## Contents

1. Principles
2. Templates for new images
3. Templates for edits
4. Common mistakes
5. JSON prompts
6. Photorealism

## 1. Principles

- **Describe the scene in sentences, not keywords.** Gemini 3 image models "think" before they draw and understand a coherent description better than a list like `4k, trending, masterpiece`.
- **Be specific.** Not "fantasy armor" but "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings". More detail gives more control.
- **State the purpose.** "Create a logo for a high-end, minimalist skincare brand" beats "Create a logo". The model picks style, composition and level of detail from the purpose.
- **Cover the basics:** subject, composition, action, setting, style, light. For edits also what must stay the same.
- **Talk like a photographer.** Shot type and lens (`wide-angle shot`, `macro shot`, `85mm portrait lens`), angle (`low-angle perspective`, `top-down`), light (`golden hour`, `three-point softbox`, `overcast diffuse light`), depth of field (`shallow depth of field`).
- **Describe what is there instead of what is not.** Not "no cars" but "an empty, deserted street with no signs of traffic". Exception: for text, "No other text." works.
- **Give a complex scene in steps.** "First, create a background of... Then, in the foreground, add... Finally, place..."
- **Put text that must appear in the image in quotes** and describe the lettering in words (bold sans-serif, elegant serif, hand-lettered). Write longer text first, then paste it into the prompt.
- **Set aspect ratio and resolution with `-a` and `-s`,** not in the prompt.
- **Edits that must stay faithful** (only the light or the time of day changes): pass the original with `-i` and list what must not change, instead of using `--follow-up`. `--follow-up` redraws the scene and shifts pose and gaze.
- **Refine in steps** with `--follow-up`: "That's great, but make the lighting a bit warmer. Keep everything else the same."

## 2. Templates for new images

**Photorealistic scene**
```
A photorealistic [type of shot] of [subject] in [setting]. [Description of the light].
Shot from a [camera angle] with a [lens type]. [Mood].
```
Example: *A photorealistic wide-angle shot of a vibrant coral reef teeming with tropical fish. Crystal-clear turquoise water with sunbeams filtering down from the surface, illuminating a sea turtle gliding over the coral. Shot from a low perspective with a wide-angle lens.*

**Photorealistic portrait** (more in section 6)
```
A photorealistic [kind of photo, e.g. casual smartphone selfie / editorial headshot] of
[person: age, look, expression, pose] in [setting], [purpose, e.g. posted to an Instagram story].
[One concrete light source and its direction]. [Skin and hair texture, small imperfections].
Shot on [camera / lens], [framing], [focus and depth of field]. [Colors and amount of editing].
```
Example (shortened): *A casual, photorealistic smartphone selfie of a young woman in her early twenties, the kind of lightly edited photo someone would post to their Instagram story, taken at arm's length in her living room. Strong warm sunlight streams through a window to the left of the camera... Her skin looks real: visible pores, faint peach fuzz catching the sun, a natural pink flush on her cheeks... Shot on a modern phone's main camera at about 26mm equivalent, sharp focus on her face, the background softly out of focus but still recognizable, sunlit highlights just starting to clip.*

**Illustrations and stickers**
```
A [style] of [subject, with details] doing [activity]. The design features
[visual qualities, e.g. bold outlines, cel-shading, flat colors] and [color/background].
```

**Image with text** (poster, logo, infographic, menu)
```
Create a [image type] for [brand/concept] with the text "[text]" in a [font style].
The design should be [style], with a [color scheme]. No other text.
```
For a lot of text or professional output use Pro.

**Product photo**
```
A high-resolution, studio-lit product photograph of [product] on [surface/background].
The lighting is a [setup, e.g. three-point softbox] to [purpose]. The camera angle is
[angle] to showcase [feature]. Ultra-realistic, with sharp focus on [key detail].
```

**Minimalist background for text** (website hero images, slides)
```
A minimalist composition featuring a single [subject] positioned in the
[bottom-right / top-left / ...] of the frame. The background is a vast, empty [color]
canvas, creating significant negative space for text. Soft, subtle lighting.
```

**Comic and storyboard** (best with 2.1, 2 or Pro)
```
Make a [N] panel comic in a [style]. Put the character in a [type of scene].
```
Supply the character as an input image (`-i`) to keep it the same across panels.

**With search** (`--search`) for current or factual information
```
Use search to find [information]. Create a [image type] showing [what] in [style].
```

## 3. Templates for edits

Pass the input image with `-i`. Without `-a` the aspect ratio stays that of the input.

**Adding or removing an element**
```
Using the provided image of [subject], please [add/remove/modify] [element]
to/from the scene. Ensure the change is [how it should integrate, e.g. matching
the original lighting and perspective].
```

**Changing only part of the image** (no mask, by description)
```
Using the provided image, change only the [specific element] to [new element].
Keep everything else in the image exactly the same, preserving the original style,
lighting, and composition.
```

**Converting to another style**
```
Transform the provided photograph of [subject] into the artistic style of [style].
Preserve the original composition but render it with [stylistic elements].
```

**Combining several images** (`-i` several times)
```
Create a new image by combining the elements from the provided images. Take the
[element from image 1] and place it with/on the [element from image 2]. The final
image should be a [description of the final scene].
```

**Preserving details** (a face, a logo)
```
Using the provided images, place [element from image 2] onto [element from image 1].
Ensure that the features of [element from image 1] remain completely unchanged.
The added element should [how it integrates].
```
Describe the detail that must not change as precisely as you can.

## 4. Common mistakes

| Mistake | Better |
|---|---|
| `mug, kitchen, 4k, realistic` | A full sentence: what, where, which light, which shot. |
| "no people, no text" | Describe the empty scene; for text use "No other text." |
| Aspect ratio in the prompt ("make it 16:9") | The option `-a 16:9`. |
| Generating again for a small change | `--follow-up` and "keep everything else the same". |
| Long text straight into the image | Write the text first, then put it in quotes. |
| Prompt in a language other than English | English; give the user a short summary in their language. |
| `negative_prompt` or an `avoid` list in JSON | Gemini has no negative prompt, it is just text. Describe what is in the image (section 5). |
| "flawless skin", "perfect", "beautiful" | Pores, fine hair, freckles, uneven skin tone (section 6). |
| "cinematic / studio lighting" for a real-life photo | One concrete light source with a direction. |
| Concluding "format A is better" from one image | At least 3-4 images per variant (`-n`), otherwise you compare chance. |
| Same prompt again in 4K or portrait, expecting the same image | A new generation gives a different image. Follow up on the finished one (`--follow-up` with `-s` / `-a`). |

## 5. JSON prompts

"JSON prompting" means splitting the image description into fields (`subject`, `lighting`, `camera`, `negative_prompt`...). For Nano Banana it has no proven advantage:

- **The model does not parse JSON.** Gemini has no structured-prompt mode. It reads braces, quotes and field names as plain text. Google's guides never mention JSON and recommend a flowing description.
- **Tests showed nothing.** [Chase Jarvis](https://chasejarvis.com/blog/does-json-prompting-actually-work-tested-with-nano-banana/) sent the same brief as JSON and as text to Nano Banana Pro and got practically the same images. The opposite result from [Fanch AI](https://fanchai.app/posts/json-vs-natural-language-prompts-nano-banana-2) rests on one image, and its JSON contained style words the text lacked. There is no proper study.
- **Other models:** FLUX.2 [officially supports](https://docs.eu.bfl.ai/guides/usecases_t2i_json_prompting) JSON, but even its documentation says it understands both formats equally well.
- **`negative_prompt` switches nothing off.** Gemini has no negative prompt field. In JSON it is just more text that the model reads as part of the description.
- **Contradictions between fields are easy to miss,** for example `"aspect_ratio": "16:9 horizontal"` and a few lines below `"orientation": "vertical"`. In flowing text they would jump out.

**Where JSON helps:** in working with prompts, not for the model ([analysis](https://www.human-ai-human.org/posts/json-prompting-images-video/)). It is handy as a template for a series where you change one field and keep the rest, for automation, and for comparing versions.

**How to handle a finished JSON prompt:**

1. If the user wants it sent "as is", send it unchanged. Before that, check for contradictions between fields and pass aspect ratio and resolution as `-a` and `-s`. Warn that `negative_prompt` and `avoid` lists are read only as text.
2. Otherwise convert it into flowing text in the order purpose, person and pose, appearance, clothing, light, setting, shot and camera. Rewrite prohibitions as a description of what is in the image (`no jewelry` becomes `her ears and neck are bare`). Resolve contradictions, and when you cannot tell which one applies, ask.
3. Keep the JSON as the source for further variants and send the converted text to the model.

## 6. Photorealism

Community practice ([artsmart](https://artsmart.ai/blog/ai-image-prompts-photorealistic/), [aivideobootcamp](https://aivideobootcamp.com/blog/photorealistic-ai-prompts-guide-2026/), [wearview](https://www.wearview.co/blog/fix-ai-skin-texture)), not measured results. Google itself advises only in general terms: describe light and shot like a photographer.

- **Say what kind of photo it is:** "casual smartphone selfie posted to an Instagram story", "editorial headshot on an 85mm lens". The kind of photo sets perspective, sharpness and level of editing.
- **Lens by type:** 85 mm for portraits and headshots, 24-35 mm or "smartphone" for spontaneous lifestyle photos. A phone perspective looks more believable.
- **One concrete light source with a direction:** "warm sunlight through a window to the left of the camera", "overcast daylight from a north-facing window". Generic "cinematic lighting" or "studio lighting" leads to the smooth look typical of AI.
- **Skin texture:** pores, faint peach fuzz, a few freckles, uneven skin tone, slight facial asymmetry. Leave out "flawless", "perfect" and "beautiful": one such word overrides all the texture descriptions.
- **Deliberate imperfections:** blown highlights in the sun, noise in the shadows, an imperfect crop, creased fabric, a lived-in setting with everyday objects. These separate a photo from a render.
- **Colors and editing:** "natural, slightly muted colors, light editing". Leave out "vibrant", "dramatic color grading", "hyperrealistic" and "8k, masterpiece".
- **Resolution:** for facial detail use 2K or 4K; at 1K the pores have nowhere to render.
- **A specific person or thing** only with a reference photo through `-i` (step 2 in SKILL.md).

**My own experiments** (26 Oct 2026, Nano Banana 2.1, one image per variant, so only indicative):

- The composition instruction ("top of head just below the upper edge") was ignored by the model in JSON and in text alike, and a fifth of the ceiling stayed above the head. Fix it with a follow-up or by cropping.
- The direction of light can flip (asked for from the left, came from the right). Check it and correct it with a follow-up.
- Text written as a description of a real-life photo gave the most spontaneous result. JSON kept small details more precisely (straight hair, expression).
- The same prompt sent again in 4K or portrait gave a different person every time. A follow-up (`--follow-up -a 16:9`) kept face, hair, clothes, room and light and only painted in the surroundings.
