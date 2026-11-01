# Fal AI Prompt Templates per Module Type

When the buyer has added a Fal AI API key during onboarding, the skill generates module images directly via Fal. This file defines the prompt patterns per module type, so generated images match the module's spec and the brand's aesthetic.

## How prompts get assembled

Each module image's Fal prompt is built from four layers:

1. **Module composition** — what's in the frame, where things sit (specific to the module type)
2. **Product description** — extracted from product info + photos (consistent across the page)
3. **Brand aesthetic** — colors, mood, style tokens (from `config.brand_voice` + audience description)
4. **Negative prompts** — what to avoid (consistent across modules — no text, no watermarks, etc.)

The final prompt sent to Fal looks like:

```
[Module composition layer], [Product description layer], [Brand aesthetic layer]. Style: [brand aesthetic style]. --no [negative prompts]
```

## Fal model recommendation

Default to **flux/dev** for product imagery — it produces clean, photographic output and handles compositional instructions well. Alternative: **flux/schnell** for faster (less detailed) iteration.

Image size: target the 2x of the module's spec dimensions (see `amazon-image-specs.md`).

## Negative prompts (used on every Fal call)

These never change. Append to every Fal prompt to enforce Amazon's image rules:

```
--no text, --no watermark, --no logo overlay, --no signature, --no price tag,
--no promotional badge, --no sale sticker, --no competitor branding, --no human faces in
detail (unless explicitly requested), --no distorted product proportions, --no extra limbs,
--no surreal artifacts
```

(Note: Fal's actual negative-prompt syntax varies by model — adapt as needed. The intent is consistent.)

---

## Module 2: Image Header With Text — prompt template

Spec: 970 × 600 px (generate at 1940 × 1200 for 2x).

```
A horizontal hero image of [product description]. Composition: product
centered horizontally, occupying approximately 50% of the vertical frame.
Negative space top and bottom for clarity. Background: [brand aesthetic
background — e.g., "soft natural light against a warm neutral wall" for
calm brands; "vibrant studio backdrop in [brand color]" for bold brands].
Lighting: [from brand voice — soft daylight / studio / dramatic / etc.].
Mood: [brand mood tokens]. Photographic, real-world, high resolution.
```

Worked example for a hand-thrown ceramic pour-over from a slow-craft brand:

```
A horizontal hero image of a hand-thrown ceramic pour-over coffee dripper
in a matte cream glaze, sitting on a wooden countertop. Composition:
dripper centered horizontally, occupying ~50% of the vertical frame.
Negative space top and bottom for clarity. Background: soft morning light
through a window, warm wood tones, slightly out-of-focus kitchen elements
in the background. Lighting: natural daylight, warm color temperature,
soft shadows. Mood: calm, slow, artisanal, contemplative. Photographic,
real-world, high resolution. --no text, --no watermark, --no logo overlay,
--no signature, --no price tag, --no promotional badge, --no surreal
artifacts, --no distorted product proportions
```

---

## Module 3: Single Image & Highlights — prompt template

Spec: 300 × 300 px (generate at 600 × 600).

```
A square product photo of [product description]. Composition: product
centered, occupying 60-70% of the square frame. Background: [brand
aesthetic background — should be cleaner / more minimal than the hero
since this image sits in a column next to text]. Lighting: even,
shadowless or soft. Mood: [brand mood]. Photographic, catalog-quality
but warmer than pure-white catalog. --no text, --no watermark, ...
```

---

## Module 4: Single Image & Sidebar — prompt template

This module needs TWO images. Generate them as a pair to ensure they relate visually.

### Primary (300 × 300 px → generate at 600 × 600)

```
A square product photo of [product description], full-product shot.
Background: [brand background]. Lighting: even. Mood: [brand mood].
Photographic, slightly editorial.
```

### Sidebar (350 × 175 px → generate at 700 × 350)

```
A horizontal detail shot of [the specific feature being called out in
the sidebar — e.g., "the cork base of the ceramic pour-over, close-up,
showing the texture and the slight overhang against the wooden countertop"].
Composition: detail fills frame. Background: continuous with the primary
image's surface. Lighting: same color temperature and direction as primary.
Mood: matches primary. Photographic.
```

The pairing is critical — if the sidebar image looks like it's from a different shoot, the module reads as cobbled-together.

---

## Module 5: Four Image & Text — prompt template

Four square images that must be visually parallel. Generate all four with the same style tokens so they look like a set.

```
A square product photo showing [variation 1: e.g., "the dripper brewing,
mid-pour"]. Same lighting, same background, same color temperature, same
compositional rules across this and all other images in this set.
Background: [consistent brand background]. Lighting: [consistent].
Mood: [consistent].
```

Repeat for variations 2, 3, 4 — varying only the variation description, keeping all other tokens identical.

**Critical:** in the Fal call, set the same seed across all 4 images, OR explicitly set "same style as previous image" tokens to keep the set visually unified.

---

## Module 6: Comparison Chart — prompt template

Each column gets a product image at 150 × 300 px (generate at 300 × 600). All columns must use identical lighting / background.

```
A vertical product photo of [product variant — e.g., "the 10oz River Stone
Pour-Over in cream"]. Background: pure white or near-white (per Amazon
comparison chart convention). Lighting: even, shadowless studio light.
Composition: product fills 80% of vertical frame, centered.
Photographic, catalog-quality.
```

Use the same prompt template (with only the variant description changing) for every column. Setting the same seed across columns is critical for consistency.

---

## Module 8: Single Side Image / Module 11: Single Left Image — prompt template

Spec: 300 × 300 px (generate at 600 × 600).

```
A square lifestyle photo of [product description] in use OR in context.
Composition: product is the clear focal point but not isolated — show
context (hands, surface, scene). Background: [brand context — e.g., a
warm kitchen, a clean desk, a studio table]. Lighting: natural, warm.
Mood: [brand mood]. Photographic, editorial.
```

These modules carry more weight than the hero on copy-led pages, so the image should feel scene-set and inhabited.

---

## Module 9: Image Header With Text Overlay — prompt template

Spec: 970 × 300 px (generate at 1940 × 600). Wide and short.

**Critical:** the image must have a "quiet" zone where overlay text will appear. Specify this in the prompt.

```
A wide horizontal hero image of [product description]. Composition: product
positioned to one side (left or right — specify per design), leaving the
opposite half of the frame as a relatively uncomplicated background area
where text will be overlaid. Background: [brand atmospheric — soft, slightly
out of focus]. Lighting: directional, with the lit side facing the camera.
Mood: [brand mood]. Cinematic, atmospheric.
```

Tell the skill which side gets the product vs the text overlay based on the brand's visual rhythm.

---

## Module 10: Multiple Image Module — prompt template

Same approach as Module 5 — four parallel images. The difference is these are typically use-case variations rather than benefit-explainer variations.

```
A square photo showing [use-case variation — e.g., "the pour-over being
used in a kitchen on a weekday morning"]. Same lighting, same color
temperature, same compositional rules across all images in this row.
Background: [consistent].
```

---

## Brand-aesthetic style tokens (from config)

The skill maps the brand voice / mood from config to specific visual tokens:

| Brand voice descriptor | Visual tokens to include |
|---|---|
| Warm, slow, artisanal | "natural daylight, warm color temperature, organic textures, wood, linen, ceramic, hand-made imperfections visible" |
| Modern, technical, clean | "studio lighting, cool color temperature, geometric composition, matte surfaces, minimalist staging" |
| Playful, bold, vibrant | "high-key lighting, saturated colors, energetic composition, contrasting backgrounds, sense of motion" |
| Premium, luxurious | "dramatic directional lighting, deep shadows, rich textures, marble or velvet surfaces, low ISO photographic feel" |
| Outdoor, rugged, lived-in | "natural outdoor light, golden hour, weathered textures, wood and stone surfaces, sense of place" |
| Clinical, scientific, trustworthy | "clean white background, even shadowless lighting, sharp focus, clinical precision in composition" |

These get fed into the "brand aesthetic" layer of every prompt. The mapping isn't rigid — the LLM driving the skill should adapt based on the specific brand-voice profile.

---

## When images come back wrong

Fal generation isn't perfect. Common failures:

- **Product proportions distorted** → re-run with a stronger compositional anchor in the prompt (e.g., "product is exactly 4 inches tall")
- **Text accidentally appearing in image** → add "--no text" more prominently, re-run
- **Off-brand colors** → strengthen the brand-aesthetic layer with explicit hex codes
- **Different style than the rest of the set** → set the same seed, OR explicitly reference "same lighting and style as the hero image"
- **Surreal / AI-looking artifacts** → re-run; try the higher-quality flux model

The skill should automatically retry once with a refined prompt before falling back to a Canva brief for that module. If a module fails 2+ retries, fall back to the Canva brief and note it in the report.

---

## When NOT to generate (always Canva brief these)

Some module images should never be generated:

- **Product packaging shots** — generated packaging looks fake
- **Real workshop / team photos** — for brand-story modules where the team is the point
- **Real customer-use UGC** — Fal can't fake real customers
- **The buyer's logo on the product** — generated logos look uncanny

For these, output a Canva brief or a "use your own photo" note even when Fal key is set. Don't try to fake these images.
