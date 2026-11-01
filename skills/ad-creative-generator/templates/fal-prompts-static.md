# Fal AI Prompt Templates for Static Ad Creative

When the Fal AI key is set, the skill generates static ad images directly. This file defines prompt patterns per archetype + ad dimension.

## How ad creative differs from A+ Content imagery

Skill #4 (A+ Content Creator) also uses Fal, but for catalog-style imagery — the dripper on a counter, the materials close-up, the cooking scene. A+ images live inside a product page, paired with descriptive copy.

Ad creative serves a different purpose. The image has to:
- Stop the scroll in a fraction of a second
- Carry one clear message (not show off the product range)
- Read at thumbnail size (small mobile previews)
- Match the ad's archetype voice

That changes the prompt strategy:
- **Higher contrast** (catches the eye at thumbnail scale)
- **Less negative space** (every pixel earns attention)
- **One subject** (no busy compositions)
- **Strong color anchor** (a single dominant color reads at scroll speed)

---

## Universal negative prompts (every Fal call)

Append to every prompt to enforce ad-compliance + ad-creative best practice:

```
--no text, --no watermark, --no logo overlay, --no price tag, --no
promotional badge, --no sale sticker, --no competitor branding, --no
distorted product proportions, --no extra limbs, --no surreal artifacts,
--no busy backgrounds, --no low contrast, --no faded colors, --no
stock-photo aesthetic
```

The "no text" is critical for ad imagery — text overlay is added by the designer (in Canva or the buyer's editor), not baked into the generated image. Text baked into the image can't be edited or A/B tested.

---

## Default model

Use **flux/dev** for ad creative. Higher fidelity than flux/schnell, important for thumbnail readability. Set:
- `num_inference_steps: 28`
- `guidance_scale: 4.0` (slightly higher than skill #4's 3.5 — ad creative benefits from more guidance toward the brand aesthetic)
- `enable_safety_checker: true`

Target dimensions per ad type — see below.

---

## Prompts per archetype

The archetype shapes the visual mood. Same product, 5 different visual interpretations.

### Archetype 1: Problem-aware

**Visual idea:** Show the "problem state" subtly — clutter, the wrong tool, the chaotic version. The product appears as the calming alternative.

**Prompt template:**

```
A photographic ad image showing [product description] positioned as the
solution to [pain point]. Composition: product center-right of frame, with
[symbol of the problem — clutter, the wrong tool, the chaotic version]
visible in the left half of frame, slightly out of focus or de-prioritized.
Lighting: warm, kitchen / lifestyle. Mood: relief — the product brings
order. High contrast between product (sharp, lit) and the chaos (softer,
darker). Photographic, realistic.
```

**Worked example (pour-over, problem-aware):**

```
A photographic ad image showing a hand-thrown ceramic pour-over coffee
dripper positioned as the solution to overflowing kitchen counters and
espresso machines that don't get used. Composition: pour-over center-right
of frame, in soft natural light. Left half of frame shows a slightly
out-of-focus glimpse of a bulky espresso machine on a counter — present
but unimportant. Lighting: warm morning daylight, soft directional.
Mood: relief — the simpler tool. High contrast between pour-over (sharp,
lit warmly) and espresso machine (de-prioritized, slightly desaturated).
Photographic, realistic. --no text, --no watermark, [...]
```

### Archetype 2: Social-proof

**Visual idea:** Show the product in use by many people / in many contexts. Visual implication of widespread adoption.

**Prompt template:**

```
A photographic ad image showing [product description] in a moment of
trusted, expert use. Composition: product central, with subtle context cues
suggesting trust — a barista's apron in frame, a professional setting,
or hand details suggesting an experienced user. Lighting: clean, slightly
editorial. Mood: confidence, expertise. Photographic, realistic.
```

**Worked example (pour-over, social-proof):**

```
A photographic ad image showing a hand-thrown ceramic pour-over coffee
dripper in a professional barista setup. Composition: pour-over center
of frame on a clean coffee bar counter, with a barista's apron and
hands visible just at the edge of frame (a kettle held mid-pour). The
overall scene suggests professional use rather than amateur. Lighting:
clean, slightly editorial coffee-shop ambiance. Mood: confidence,
expertise, "professionals use this." Photographic, realistic.
```

### Archetype 3: Transformation

**Visual idea:** The after-state. The aspirational moment the product enables. Calm, sensory, complete.

**Prompt template:**

```
A photographic ad image showing the aspirational moment [product description]
creates. Composition: a person (faceless or back-to-camera) in the
[after-state scene], with the product visible but not the central focus
— the LIFESTYLE is the subject. Lighting: golden hour, natural, slightly
warm. Mood: calm, fulfilled, "this is the morning you want." Photographic.
```

**Worked example (pour-over, transformation):**

```
A photographic ad image showing the aspirational morning the hand-thrown
ceramic pour-over creates. Composition: a person (faceless, hands only)
in a quiet kitchen, holding a mug of coffee, with the pour-over visible
on the counter behind. The morning light through a window catches steam
rising from the mug. The LIFESTYLE is the subject; the product is the
visible enabler. Lighting: golden hour, natural, warm. Mood: calm,
fulfilled, slow Saturday. Photographic.
```

### Archetype 4: Curiosity-gap

**Visual idea:** Visual incompleteness. Something that requires the viewer to lean in. Often: a detail close-up, an unexpected angle, a moment caught mid-action.

**Prompt template:**

```
A photographic ad image showing [product description] from an unexpected
or attention-arresting angle. Composition: extreme close-up, top-down view,
or mid-action freeze-frame — something that makes the viewer pause to
parse what they're seeing. Lighting: directional, with strong shadows.
Mood: deliberate, slightly cinematic. Photographic, realistic.
```

**Worked example (pour-over, curiosity-gap):**

```
A photographic ad image showing the hand-thrown ceramic pour-over coffee
dripper from directly overhead, mid-pour. Composition: extreme top-down
view (bird's eye), with the kettle's water visible streaming into the
dripper in a perfect spiral. The pattern of the water and the dripper's
opening creates an almost abstract circular composition that the viewer
has to parse for a moment. Lighting: directional from one side, dramatic
shadows on the rim of the dripper. Mood: deliberate, almost meditative.
Photographic.
```

### Archetype 5: Contrarian

**Visual idea:** Visual hierarchy that prioritizes the product over an established category leader. Often: product foregrounded against (or beside) the category default, with the product looking calmer/cleaner/more confident.

**Prompt template:**

```
A photographic ad image showing [product description] positioned as the
calmer / better / smarter alternative to the category default. Composition:
product central and sharp, with the category default (espresso machine,
big appliance, complicated tool) visible but slightly diminished — like
the old thing is on its way out. Lighting: confident, clean. Mood: quiet
conviction. Photographic.
```

**Worked example (pour-over, contrarian):**

```
A photographic ad image showing the hand-thrown ceramic pour-over coffee
dripper as the confident replacement for an espresso machine. Composition:
pour-over central and sharp in foreground, espresso machine visible
behind it but desaturated and slightly out of focus — the new thing
in focus, the old thing fading. Lighting: confident overhead light on
the pour-over; flatter / cooler light on the espresso machine. Mood:
quiet conviction, "this is the better way now." Photographic.
```

---

## Image dimensions per platform + format

The skill generates per platform per format. Common combinations:

| Platform | Format | Dimensions (generated) | Aspect |
|---|---|---|---|
| Meta Feed | Static | 1080×1080 | 1:1 |
| Meta Feed | Static (vertical preferred) | 1080×1350 | 4:5 |
| Meta Reels/Stories | Static | 1080×1920 | 9:16 |
| TikTok | Static (rare) | 1080×1920 | 9:16 |
| Google Display/PMax | Static (horizontal) | 1200×628 | 1.91:1 |
| Google Display/PMax | Static (square) | 1200×1200 | 1:1 |
| Google Display/PMax | Static (vertical) | 720×1280 | 9:16 |
| Pinterest | Static | 1000×1500 | 2:3 |

For each archetype concept, the skill generates the primary dimension for the chosen platforms. If "all platforms" is selected, the skill generates the 1080×1080 Meta version + 1080×1920 vertical + 1200×628 horizontal (covers most placements) and notes the others as Canva-crop briefs from those source images.

Generate at 2x dimensions (1080×1080 → 2160×2160) for retina-sharp rendering when affordable on Fal credits.

---

## Brand-aesthetic style tokens (same mapping as skill #4)

The skill maps brand voice descriptors to visual tokens:

| Brand voice | Visual tokens |
|---|---|
| Warm, slow, artisanal | natural daylight, warm color temperature, organic textures, ceramic, linen, wood |
| Modern, technical, clean | studio lighting, cool color temperature, geometric composition, matte surfaces |
| Playful, bold, vibrant | high-key lighting, saturated colors, energetic composition, contrasting backgrounds |
| Premium, luxurious | dramatic directional lighting, deep shadows, rich textures, marble or velvet |
| Outdoor, rugged | natural outdoor light, golden hour, weathered textures, sense of place |

These get layered into every prompt's mood/lighting section.

---

## When images come back wrong

Common failures for ad creative:

- **Text accidentally in image** → re-run with stronger negative prompt on "text"
- **Too busy / too much going on** → re-run with explicit "simple composition, one subject" + reduce scene description
- **Doesn't match brand aesthetic** → strengthen the brand-token layer with explicit hex codes or specific references
- **Looks like a stock photo** → add "candid, real, not-stock" tokens and reduce explicit "ad" framing in prompt

The skill auto-retries once with refined prompt before falling back to Canva brief for that archetype.

---

## What should NOT be generated by Fal

Some ad imagery should always be created by the buyer or a designer, not generated:

- **The buyer's actual product packaging** (generated packaging looks fake)
- **Real customer photos / UGC** (Fal can't fake real customers)
- **Founder photos / team shots** (uncanny when generated)
- **Specific known landmarks or recognizable people** (legal + ethical reasons)

Flag these as Canva briefs or "use your own photo" even when Fal key is set.
