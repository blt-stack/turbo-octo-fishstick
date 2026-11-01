# Canva Brief Template (Fal AI Fallback)

When the buyer hasn't set a Fal AI API key, the skill produces detailed Canva briefs the buyer or their designer can build. These briefs need to be specific enough that a freelance Canva designer can build the asset without follow-up questions.

The brief for every module image follows the same structure. This file defines that structure and provides a per-module-type checklist.

---

## Universal brief structure

Every Canva brief block in the .docx output has:

1. **Module type** (e.g., "Module 2: Image Header With Text — Hero")
2. **Required dimensions** (exact pixel size per Amazon spec)
3. **File format** (JPG or PNG)
4. **Composition** (what's in the frame, where)
5. **Mood + lighting** (energy and visual feel)
6. **Brand tokens** (colors, fonts, references from `config.brand_voice`)
7. **What to AVOID** (specific things that would break Amazon compliance or the brand aesthetic)
8. **Recommended Canva starting template** (a real Canva template category to start from, when applicable)
9. **Notes for the designer** (anything else they need to know)

---

## Recommended Canva template starting points per module

Canva organizes templates by use case. Pointing the designer at the right category saves time.

| Module | Recommended Canva starting category |
|---|---|
| Module 1 (Logo) | "Logos" → "Minimal" or "Wordmark" |
| Module 2 (Image Header With Text) | "Posters" → "Product Posters" — then resize to 970×600 |
| Module 3 (Single Image & Highlights) | Custom: square product photo + 4 text overlays in adjacent column |
| Module 4 (Image & Sidebar) | Custom: 2 images side-by-side, then composite |
| Module 5 (Four Image & Text) | Canva grid templates — "Product Grids" or "Collage" |
| Module 6 (Comparison Chart) | Canva "Tables" or "Infographic Comparison" templates |
| Module 8/11 (Single Side Image) | Custom: lifestyle photo + minimal text overlay |
| Module 9 (Image Header With Text Overlay) | "Banner" templates with text overlay capability |
| Module 10 (Multiple Image Row) | Canva "Photo Collage" templates with 1×4 layout |
| Module 12 (FAQ) | Canva FAQ infographic templates |

---

## Per-module brief examples

### Module 2: Image Header With Text — Hero brief

```
MODULE 2 — HERO (Image Header With Text)

Image dimensions: 970 × 600 px (Amazon spec; recommend 1940 × 1200 px for retina)
File format: JPG

Composition:
- Subject: hand-thrown ceramic pour-over coffee dripper, full product visible
- Position: centered horizontally, slightly upper-third vertically
- Surface: warm-toned wooden countertop
- Context: morning kitchen scene, soft window light from frame-right
- Negative space: clean upper area (no clutter) so the header reads cleanly

Mood + lighting:
- Calm, slow, contemplative
- Natural morning daylight
- Warm color temperature (~3500-4000K)
- Soft shadows, no harsh contrast
- Steam rising from dripper if possible (in-use shot)

Brand tokens:
- Colors: warm neutrals — cream, oak, soft white
- Avoid: cool blues, neon, hard plastic textures
- Reference brands for visual feel: [from config — e.g., "Aesop", "Snow Peak", "Fellow Coffee"]

What to AVOID:
- Text in the image (Amazon may crop it; module copy goes outside)
- Watermarks or logos visible
- Other coffee brands or competitor products visible
- Hands or faces (unless explicitly desired)
- High saturation / oversaturated colors

Recommended Canva starting point:
- Canva Posters → Product Posters → Filter by "Lifestyle"
- Resize canvas to 970 × 600 px before starting

Notes for the designer:
- This image will be paired with a headline + body text BELOW it (not overlaid)
- The image should support the page-opening voice, not compete with the headline
- Test the image on mobile preview — Amazon may crop top/bottom on mobile devices
```

### Module 5: Four Image & Text — Benefits grid brief

```
MODULE 5 — BENEFITS GRID (Four Image & Text)

Image dimensions: each cell 220 × 220 px (recommend 440 × 440 for retina)
File format: JPG (photos preferred over graphics for visual consistency)
4 images total — to be created as a matched set

CRITICAL: all 4 images must be visually parallel — same lighting, same color
temperature, same compositional rule, same background style. They should
look like they're from one continuous photo shoot.

Composition (per image):
- Cell 1: [first benefit subject — e.g., "single cup brewing in progress"]
- Cell 2: [second benefit subject — e.g., "reusable mesh filter, close-up"]
- Cell 3: [third benefit subject — e.g., "stoneware texture detail"]
- Cell 4: [fourth benefit subject — e.g., "dripper on dishwasher rack — showing dishwasher safe"]

Mood + lighting:
- Same across all 4 cells: warm morning daylight, soft natural shadows
- Color temperature: 3500-4000K, consistent

Brand tokens:
- Same color palette as Module 2 hero
- Same surface style (warm wood / cream backgrounds)

What to AVOID:
- Mixing lighting styles between cells (kills the set's coherence)
- Different scales between cells (subject taking up wildly different portions of frame)
- Stock photos for any cell (will be visually obvious against the others)

Recommended Canva starting point:
- Canva Photo Collage → 2×2 grid
- OR shoot 4 photos with consistent lighting and assemble in Canva

Notes for the designer:
- If the buyer has only 1 product photo, this module isn't a fit. Use
  Module 3 (Single Image & Highlights) instead.
- Consider shooting all 4 images in a single 30-minute session to ensure
  lighting consistency.
```

### Module 6: Comparison Chart — brief

```
MODULE 6 — COMPARISON CHART

Per-column product image dimensions: 150 × 300 px (recommend 300 × 600 for retina)
File format: JPG
Number of columns: [3-5 based on the buyer's catalog]

CRITICAL: all column product images must use identical lighting, identical
background, identical scale. Comparison charts that look like cobbled-together
catalog screenshots reduce conversion rather than raising it.

Per-column composition:
- Column 1 (highlighted product): [the product on the listing page]
  - Background: white or near-white
  - Lighting: even, shadowless studio light
  - Product fills ~80% of vertical frame
- Columns 2-N: other products in the seller's catalog, same staging

Brand tokens:
- White background is Amazon comparison-chart convention
- Use the seller's lifestyle color palette only in the row labels above the chart, not the cells themselves

What to AVOID:
- Different lighting/background per column (instant trust failure)
- Competitor brand products in any column (TOS violation)
- Comparison rows that only flatter the highlighted product (looks defensive — include 1-2 rows where another product wins)

Recommended Canva starting point:
- Canva "Infographic Comparison Chart" templates
- Customize colors to match brand palette
- Resize cells to fit Amazon's 150 × 300 spec

Notes for the designer:
- Amazon's comparison chart renders well on desktop but compresses on mobile.
  Test the chart's readability at 375px width before submitting.
```

### Module 9: Image Header With Text Overlay — brief

```
MODULE 9 — IMAGE HEADER WITH TEXT OVERLAY

Image dimensions: 970 × 300 px (recommend 1940 × 600 for retina)
File format: JPG (photographic atmospheres work best for text overlay)

CRITICAL: the image must have a "quiet" zone where the overlay text will be
readable. Pick the side (left or right) intentionally based on brand visual
rhythm.

Composition:
- Subject: product positioned to one side (typically right), occupying
  ~45-60% of the horizontal frame
- Opposite side: relatively uncomplicated background area (sky, wall,
  out-of-focus environment) where text will overlay
- Negative space proportion: ~40-50% of the total frame area

Text overlay specs (these get composited at design time):
- Headline area: left third of frame (when product is on the right)
- Headline color: [light or dark based on image — verify WCAG AA contrast]
- Font: [from brand voice — match the brand's primary type]
- Headline body text below headline, smaller

Mood + lighting:
- Cinematic, atmospheric
- Directional light, with the lit side of the product facing camera
- Color grading slightly warmer than neutral

Brand tokens:
- Same color palette as the hero
- Don't use neon, hard primaries, or anything that fights with text legibility

What to AVOID:
- Image too busy (text becomes unreadable)
- Light text on partially-light image (low-vision accessibility fail)
- Text that gets cropped on mobile rendering

Recommended Canva starting point:
- Canva "Banner" templates with text overlay
- Filter for ones that use directional lighting

Notes for the designer:
- This module is the highest-craft module. If the brand doesn't have a
  strong photographic asset, default to Module 2 instead.
- Test the assembled image at both 970 × 300 (desktop) and the Amazon
  mobile crop before submitting.
```

---

## How the brief gets into the .docx output

For modules where Fal AI generated the image successfully, the .docx brief embeds the generated PNG inline and notes "Image generated by Fal AI — see attached file [path]".

For modules where Canva briefing is the path (either no Fal key, or generation failed twice), the .docx brief includes the full Canva brief structure above. Designers can be handed the relevant page directly.

---

## When the buyer is the designer

Many solo e-commerce operators design their own assets in Canva. The brief should still be specific enough — solo founders making their own assets often skim the spec and miss something critical (wrong dimensions, missing alt text, watermark accidentally left in).

The brief includes a small "Self-designer checklist" at the bottom of each module:

```
SELF-DESIGNER CHECKLIST
☐ Canvas resized to [exact dimensions]
☐ Subject positioned per composition notes above
☐ No text in the image (text goes in module copy, not in image)
☐ No watermark, no Canva watermark visible
☐ Exported as [JPG/PNG] under 5 MB
☐ Color profile is sRGB (Canva default)
☐ Alt text written (separate field in module copy)
```

This list catches the most common solo-designer mistakes.
