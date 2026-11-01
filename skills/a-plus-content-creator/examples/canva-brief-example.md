# Canva Brief Output — Reference Example (No Fal AI Key)

Same product as the Fal example (`single-product-aplus-example.md`), but showing what gets output when the buyer hasn't set a Fal AI API key during onboarding. The copy and module selection are identical; only the image-handling section per module differs.

**Product:** River Stone Ceramic Pour-Over
**Image source:** Canva briefs (no Fal AI key)

---

## What changes vs the Fal AI path

- **Modules picked:** identical (5 modules, same rationale)
- **Copy generated:** identical (same headlines, body, alt text, FAQ)
- **Compliance check:** identical
- **Image handling:** instead of embedded generated PNGs, every module's image section becomes a detailed Canva brief
- **HTML preview:** modules show a "Canva brief — image to be created" placeholder with brief text overlaid (instead of generated images)

---

## Sample module with Canva brief instead of generated image

### Module 1 — Image Header With Text (Amazon Module ID 2)

Purpose: Page hero — sets tone, names the value proposition.

**Image:**
- Source: Canva brief (no Fal AI key — generate the image yourself or hand the brief to a Canva designer)
- Spec dimensions: 970 × 600 px (Amazon requirement; create at 1940 × 1200 for retina rendering)
- File format: JPG

**Canva brief:**

```
MODULE 2 — HERO (Image Header With Text)

Image dimensions: 970 × 600 px (Amazon spec; recommend 1940 × 1200 px for retina)
File format: JPG

Composition:
- Subject: hand-thrown ceramic pour-over coffee dripper in matte cream glaze
- Position: centered horizontally, slightly upper-third vertically
- Surface: warm-toned wooden countertop
- Context: morning kitchen scene, soft window light from frame-right
- Negative space: clean upper area (no clutter) so the headline reads cleanly when paired
- Steam rising from dripper if possible (in-use shot)

Mood + lighting:
- Calm, slow, contemplative
- Natural morning daylight
- Warm color temperature (~3500-4000K)
- Soft shadows, no harsh contrast

Brand tokens (from your brand voice profile):
- Colors: warm neutrals — cream, oak, soft white
- Avoid: cool blues, neon, hard plastic textures
- Reference visual feel: Aesop, Snow Peak, Fellow Coffee

What to AVOID:
- Text in the image (your headline goes BELOW the image in the module copy)
- Watermarks or logos visible
- Other coffee brands or competitor products visible
- Faces or hands (unless desired)
- Oversaturated colors

Recommended Canva starting point:
- Canva Posters → Product Posters → Filter by "Lifestyle"
- Resize canvas to 970 × 600 px before starting

SELF-DESIGNER CHECKLIST
☐ Canvas resized to 970 × 600 px (or 1940 × 1200 for retina)
☐ Subject positioned per composition notes above
☐ No text in the image (text goes in module copy, not in image)
☐ No watermark, no Canva watermark visible
☐ Exported as JPG under 5 MB
☐ Color profile is sRGB (Canva default)
☐ Alt text written (separate field in module copy below)
```

---

## Module 2 — Four Image & Text (the harder one for Canva)

This module needs **4 visually parallel images**. The brief is more detailed because consistency across the 4 cells is critical.

**Image:**
- Source: Canva brief (4 images to create as a matched set)
- Spec dimensions: each cell 220 × 220 px (recommend 440 × 440 for retina)
- File format: JPG

**Canva brief:**

```
MODULE 5 — BENEFITS GRID (Four Image & Text)

4 images required, dimensions 220 × 220 px each (recommend 440 × 440 for retina).

CRITICAL: all 4 images must be visually parallel. Same lighting, same color
temperature, same background style, same compositional rule. They should look
like they're from one continuous photo session.

Suggested approach: shoot all 4 images in a single 30-minute session with
identical camera/lighting setup. Or build all 4 in Canva with identical canvas,
background, and overlay style.

Per-cell composition:
- Cell 1: Brewing in motion — dripper from a slight 3/4 angle, mid-pour, water
  streaming through. Mug visible below.
- Cell 2: Reusable mesh filter close-up — show texture, clipped into dripper, no
  hands. Top-down or 3/4 angle.
- Cell 3: Stoneware texture detail — close-up of the glaze surface showing
  hand-thrown imperfections, ideal for "made by hand" framing.
- Cell 4: Dishwasher rack scene — dripper sitting on a top rack of an
  open dishwasher, clean, dry. Sells the "dishwasher safe" benefit visually.

Mood + lighting:
- Same across all 4 cells: warm morning daylight, soft natural shadows
- Color temperature: 3500-4000K, consistent across all 4

Brand tokens:
- Same color palette as the Module 1 hero
- Same surface style (warm wood / cream backgrounds)

What to AVOID:
- Mixing lighting styles between cells (kills the set's coherence)
- Different scales — keep the dripper proportionally similar across all 4 frames
- Stock photos for any cell (immediately visible against the others)

Recommended Canva starting point:
- Canva Photo Collage → 2×2 grid
- OR shoot 4 photos in one session and assemble in Canva

SELF-DESIGNER CHECKLIST
☐ All 4 canvases resized to 220 × 220 px each
☐ Lighting and color temperature consistent across all 4
☐ Subject scale consistent across all 4
☐ No text in any image
☐ No watermark, no Canva watermark on any
☐ All 4 exported as JPG, each under 5 MB
☐ Alt text written for each (separate fields in module copy)
```

---

## Modules 3, 4, 5 — same pattern

Module 3 (Brand Story Text) has no image.

Module 4 (Comparison Chart) has 3 column images (one per product variant). Brief calls out the white-background + consistent-staging requirement and notes the chart can be built natively in Canva from the Comparison Chart template.

Module 5 (FAQ Module) has no image.

So in total this product needs **the buyer to create 5 images** (1 hero + 4 grid + N/A + 3 columns + N/A = 8 images), all detailed in the brief.

---

## How the HTML preview looks without Fal images

Each module's image area becomes a styled placeholder showing the brief text:

- Background: subtle diagonal-stripe pattern (signals "this is a placeholder, not the final image")
- Inside: a white card with the brief summary and the required dimensions
- The buyer can scroll the preview and immediately see which modules need images, exactly what dimensions, and the design brief

---

## When the buyer adds a Fal key later

The skill works incrementally. If the buyer adds a Fal AI key after this first run:

1. Re-run the skill on the same product
2. The skill detects the new key
3. Generates the images this time
4. Both the .docx and the .html preview update with the actual generated images

So the Canva-brief output isn't a worse version of the skill — it's the version the buyer needed at this moment, and the upgrade path is one config edit away.

---

## Notes on this exemplar

- Briefs are detailed enough to be handed directly to a freelance Canva designer
- Self-designer checklists catch the most common solo-builder mistakes
- All briefs match Amazon's exact dimension and format requirements
- The compliance check passes the same way as the Fal path — Canva briefs are just deferred imagery, not deferred compliance
- The HTML preview makes the image gaps visually obvious so the buyer knows exactly what's still to do
