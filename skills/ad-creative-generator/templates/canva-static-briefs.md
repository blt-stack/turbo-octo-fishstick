# Canva Brief Template for Static Ad Creative (Fal Fallback)

When the buyer hasn't set a Fal AI API key, the skill produces detailed Canva briefs the buyer or their designer can build into actual static ad images.

The brief structure mirrors skill #4's Canva brief approach but tunes the composition advice for ad-creative best practice (high contrast, single subject, thumbnail-readable) rather than catalog-style imagery.

---

## Universal Canva brief structure

Every Canva brief block in the .docx output has:

1. **Concept name** (e.g., "Concept 1 — Problem-aware")
2. **Required dimensions** (per platform + format combination)
3. **File format** (JPG for photographic; PNG if transparency is needed)
4. **Composition** (what's in frame, where, hierarchy)
5. **Mood + lighting** (energy, color temperature)
6. **Color anchor** (one dominant color the ad uses to read at thumbnail scale)
7. **Brand tokens** (from `config.brand_voice` — typography, secondary colors, etc.)
8. **Text overlay recommendation** (the hook line, where to position it, suggested type style — text gets added separately in Canva, not baked into a photo)
9. **What to AVOID** (specific things that would break the ad's effectiveness or Meta/TikTok policy)
10. **Recommended Canva starting template** (a real Canva template category to start from)
11. **SELF-DESIGNER CHECKLIST** (common solo-builder mistakes to catch)

---

## Per-archetype + per-dimension brief examples

### Concept 1 — Problem-aware — Meta Feed (1080×1080)

```
CONCEPT 1 — PROBLEM-AWARE (Meta Feed Static, 1080×1080)

Image dimensions: 1080 × 1080 px (Meta spec; export at 2x = 2160 × 2160 for retina)
File format: JPG

Composition:
- Subject: hand-thrown ceramic pour-over coffee dripper, center-right of frame
- Subject occupies 55-60% of frame width
- Left third of frame: a slightly out-of-focus bulky espresso machine (the
  "problem" — the wrong tool sitting on a counter, present but de-prioritized)
- Surface: warm wooden countertop
- The compositional hierarchy: pour-over sharp and front, espresso machine
  soft and back

Mood + lighting:
- Warm morning daylight, soft directional from window
- Color temperature 3500-4000K
- Pour-over lit warmly (the hero); espresso machine in cooler / flatter light

Color anchor: Warm cream + oak wood (with the espresso machine's metallic
silver as the visual "old way" contrast)

Text overlay (added in Canva, not baked into the image):
- Headline placement: top third of image, in 60-80pt typeface
- Headline copy: "The $400 mistake fixer" (from the ad copy in the brief)
- Type: brand's primary typeface, white or cream with slight shadow for legibility

What to AVOID:
- Text baked into the photo itself (overlay it in Canva so it's editable)
- Espresso machine being too prominent (it should feel "fading out," not central)
- Multiple competing focal points (one subject wins; the others support)
- Watermarks
- Anything that could read as Meta-prohibited content (no people's bodies, no
  "before/after" implication)

Recommended Canva starting point:
- Canva Custom Size 1080x1080
- Use the brand kit (if set up in Canva) for the typography
- Start from a "Product Lifestyle" template category and modify

SELF-DESIGNER CHECKLIST:
☐ Canvas at 1080 × 1080 (or 2160 × 2160 for retina)
☐ Subject (pour-over) occupies 55-60% of frame
☐ Espresso machine present but de-prioritized
☐ Text overlay added in Canva (not baked into the image source)
☐ Hook line legible at thumbnail scale (test by zooming Canva to 25%)
☐ No Canva watermark visible on export
☐ Exported as JPG under 5 MB
☐ Color profile is sRGB
☐ Verify Meta compliance: no implied personal attributes, no health claims
```

### Concept 1 — Problem-aware — Meta Reels/Stories (1080×1920)

```
CONCEPT 1 — PROBLEM-AWARE (Reels/Stories, 1080×1920)

Image dimensions: 1080 × 1920 px (vertical)
File format: JPG

Composition:
- Subject: pour-over centered, occupying top 2/3 of frame
- Bottom 1/3: reserved for text overlay + CTA button (Reels' interactive layer)
- Surface visible at the bottom edge of the subject area
- Top quarter of frame: clean negative space for headline overlay

Mood + lighting:
- Same as the Feed version — warm morning, soft directional
- Make sure the lighting works at the vertical aspect — directional from
  one side (not top-down, which flattens in 9:16)

Color anchor: Warm cream + oak

Text overlay placement (Reels-specific):
- Headline at top quarter (the safe zone — Reels overlays its own UI at
  bottom)
- Hook line ("$400 in a cabinet") in 80-100pt
- Brand mark at bottom-left, small

What to AVOID:
- Text near the bottom 25% of frame (Reels UI overlays it)
- Critical content in the absolute center (Reels' tap-to-pause indicator
  appears there)
- Anything horizontal — full vertical only

SELF-DESIGNER CHECKLIST:
☐ Canvas at 1080 × 1920 (9:16)
☐ Subject in top 2/3, text overlay at top, CTA-safe zone at bottom
☐ Test on phone: open the image in your phone gallery to verify scale
☐ Hook readable at scroll-stopping speed (test by quick-flipping past it)
☐ Exported as JPG under 5 MB
```

### Concept 1 — Problem-aware — Google PMax (1200×628 horizontal)

```
CONCEPT 1 — PROBLEM-AWARE (Google PMax Display Asset, 1200×628)

Image dimensions: 1200 × 628 px (1.91:1 horizontal — Google's required ratio
for Display + Discovery)
File format: JPG

Composition:
- Subject: pour-over on the right third of frame
- Left two-thirds: clean photographic scene (counter + soft scene cues
  suggesting "morning kitchen") with negative space for headline overlay
- The horizontal aspect requires a different composition than the square
  Feed version — the pour-over can't dominate the whole frame; it has
  to share space with the headline area

Mood + lighting: Same as other concept variants

Color anchor: Same

Text overlay (Google adds dynamic headlines via PMax, but for the static
fallback if you're uploading as a single image):
- Headline area: left two-thirds, vertically centered
- Suggested headline: "Stop wasting on coffee machines" (one of the RSA
  headlines)

What to AVOID:
- Centered composition (Google Display thumbnails crop to weird aspects)
- More than 20% text-in-image (Google penalizes high-text-density ads)

SELF-DESIGNER CHECKLIST:
☐ Canvas at 1200 × 628 (1.91:1)
☐ Subject on right third; left has negative space
☐ Text overlay (if any) occupies less than 20% of total image area
☐ Test crop at 600x600 and 600x900 (Google may auto-crop for some placements)
☐ Exported as JPG under 5 MB
```

---

## Universal mood-token guide for Canva briefs

Whatever the brand voice, the Canva brief includes specific mood tokens so the designer knows what aesthetic to hit:

### Warm / slow / artisanal brands
- Lighting: natural daylight, soft directional, golden hour ideal
- Color palette: cream, oak, terracotta, soft sage
- Textures: ceramic, linen, wood
- Reference brands for visual feel: Aesop, Snow Peak, Fellow Coffee

### Modern / technical / clean brands
- Lighting: studio, even, slightly cool
- Color palette: charcoal, white, accent (one brand color)
- Textures: matte metal, glass, paper
- Reference brands: Apple, Notion, Linear

### Playful / bold / vibrant brands
- Lighting: high-key, colorful, slight grain
- Color palette: 2-3 saturated brand colors, white base
- Textures: clean surfaces, colored backdrops
- Reference brands: Glossier, Liquid Death, Pop-Tarts

### Premium / luxurious brands
- Lighting: dramatic directional, deep shadows
- Color palette: black, white, metallic accents (gold, copper)
- Textures: marble, velvet, leather
- Reference brands: Chanel, Aman, Le Labo

### Outdoor / rugged / lived-in brands
- Lighting: natural outdoor, golden hour, slight grain
- Color palette: earth tones, faded denim, weathered wood
- Textures: canvas, raw wood, stone
- Reference brands: Filson, Yeti, Patagonia

The skill picks the closest match from `config.brand_voice` and lists those tokens in every Canva brief so the designer's output is brand-consistent.

---

## When the buyer is the designer

Many solo e-commerce operators design their own Canva assets. The SELF-DESIGNER CHECKLIST at the bottom of every brief catches the most common solo-builder mistakes:

- Wrong canvas dimensions
- Canva watermark left visible
- Color profile not set to sRGB
- File too large for Ads Manager upload (>5 MB)
- Text overlay too small to read at thumbnail
- Compliance issues (Meta-prohibited content, body shots, etc.)

These checkboxes are the difference between a brief that produces a working ad and one that produces a designer-revision-loop.

---

## When images come from the buyer's library (not Fal, not Canva)

Some ads work best with the buyer's existing imagery:
- Real product packaging photos
- Real founder / studio photos
- Real customer-use photos (UGC the buyer has rights to)
- Approved lifestyle photos from past photo shoots

For these, the brief includes a "Use your own photo" note instead of a Canva brief:

```
USE YOUR OWN PHOTO

For this concept, we recommend using one of your existing photos:
- [specific description of what to look for in the library]
- Required dimensions: 1080 × 1080 (Meta Feed)
- Required cropping: subject occupies 55-60% of frame
- Required mood: warm morning daylight (matches your brand)

If you don't have a photo that fits, the alternative is the Canva brief
above. But existing real photos almost always outperform Canva composites.
```

This avoids the "we generated a fake-looking image of your team" trap.
