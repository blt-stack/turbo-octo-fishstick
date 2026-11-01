# Standard A+ Content Module Library

Amazon's Standard A+ Content (free for Brand Registered sellers) offers 12 module types. Maximum 5 modules per page, plus an optional Product Description Text module that doesn't count against the cap. This file documents every module type with character limits, use cases, and pitfalls.

The smart-pick logic in `smart-pick-logic.md` decides which modules to use for a specific product. This file is the reference for *how* each picked module is written.

---

## Module 1: Standard Company Logo

A standalone logo image, typically used as a separator or brand identifier between modules.

**Use case:** seldom used as a primary module; better as a small visual rest between heavier text-and-image modules. Skip unless the brand identity is a strong conversion lever.

**Spec:** image only, 600×180 px.

**Pitfalls:** wastes one of 5 module slots if used purely decoratively. Use only when the brand logo carries real recognition weight.

---

## Module 2: Standard Image Header With Text

The most common hero module. A full-width header image with a headline + body text block below it.

**Use case:** opening module for almost every A+ Content page. Sets the tone, names the value proposition.

**Character limits:**
- Headline: 150 characters
- Body text: 500 characters

**Image spec:** 970×600 px (recommended). Mobile-cropped to a 16:9-ish view — keep the key visual centered.

**Writing pattern:**
- Headline: the primary value proposition or product name + benefit (e.g., "Hand-thrown ceramic pour-over that brews one perfect cup in three minutes")
- Body: 3-4 sentences elaborating the value prop with sensory detail and one specific benefit

**Pitfalls:**
- Headline that just repeats the listing title (waste)
- Body that becomes a feature list (use the value-prop modules for features; this is for the brand story / outcome)
- Image with overlaid text that gets cropped on mobile (Amazon's mobile rendering doesn't always show the full image)

---

## Module 3: Standard Single Image & Highlights

A square image alongside a column of 4 short text highlights. Each highlight has a small heading + 1-line body.

**Use case:** showcasing 4 key benefits with one supporting visual.

**Character limits:**
- Headline (above the module): 150 characters
- Image alt text: 100 characters
- For each of 4 highlights:
  - Headline: 80 characters
  - Body: 175 characters

**Image spec:** 300×300 px (square). On the right column of the module.

**Writing pattern:**
- Each highlight = one benefit with one feature backing it ("All-day comfort — Memory-foam insole molds to your foot within the first week")
- Highlights should be visually parallel (similar length, similar grammatical structure)

**Pitfalls:**
- Mixing benefit-led and feature-led highlights — picks one consistent voice
- Highlights that read as marketing fluff ("Best in class", "Premium quality")

---

## Module 4: Standard Single Image & Sidebar

A large primary image with a small sidebar image + text. Used for product detail callouts.

**Use case:** "here's the product, here's a specific detail/feature called out separately."

**Character limits:**
- Headline: 150 characters
- Description (next to primary image): 350 characters
- Sidebar headline: 100 characters
- Sidebar body: 500 characters

**Image specs:**
- Primary image: 300×300 px
- Sidebar image: 350×175 px

**Writing pattern:** primary copy = the product overview; sidebar = a single deep-dive feature or differentiator.

**Pitfalls:**
- Using both image slots for similar shots — the sidebar should add new visual information
- Sidebar body that exceeds visual weight of the primary description

---

## Module 5: Standard Four Image & Text

A 2×2 grid of images, each with its own headline + body text. Often used for benefit grids or "what makes this different" features.

**Use case:** when the product has 4 clear, visually-distinct features or use cases.

**Character limits per cell (×4):**
- Image alt text: 100 characters
- Headline: 200 characters
- Body: 150 characters

**Image specs:** each image 220×220 px (square).

**Writing pattern:** each cell = one benefit with its supporting visual. Cells should be visually + verbally parallel.

**Pitfalls:**
- Using stock or stylistically inconsistent images across the 4 cells
- Repeating the same benefit across cells just to fill the grid

---

## Module 6: Standard Comparison Chart

A table comparing the product against up to 5 other products (often the seller's own catalog) across up to 10 attributes. This is one of the highest-converting module types.

**Use case:** the seller has multiple SKUs/variants in the catalog. The comparison helps shoppers self-select into the right product.

**Note:** Amazon's policy does NOT allow comparing against competitor products (only against the seller's own catalog).

**Character limits:**
- Headline (above chart): 150 characters
- Description: 200 characters
- Per cell (~80 characters; varies by Amazon's templating)
- Column headers: 80 characters each

**Image spec:** per-column product image at 150×300 px.

**Writing pattern:**
- Column 1 = the product on the listing page (highlight column)
- Columns 2-6 = related products in the catalog
- Rows = attributes that differentiate (capacity, color, use case, included accessories, price tier)
- Each cell = short factual content (e.g., "10-12 oz", "✓", "Included", "Adults only")

**Pitfalls:**
- Comparing only on dimensions where the highlighted product wins — looks defensive
- Including attributes no shopper cares about (specs without consequence)
- Comparing against competitor products (TOS violation)

---

## Module 7: Standard Product Description Text

A text-only block. Plain paragraphs only. No images.

**Use case:** when there's substantive prose to add (story, materials deep-dive, technical detail) that doesn't need imagery.

**Character limits:**
- Headline: 200 characters
- Body: 1000 characters

**Writing pattern:** narrative prose, not bullet lists. Use this module for the "story" beat of the page.

**Pitfalls:**
- Using this module when the page already has image-rich modules covering the same content (redundant)
- Writing it as bullets — bullets belong in the highlights modules; this is for prose

---

## Module 8: Standard Single Side Image

A single image on the left with copy on the right. Cleanest layout module for a strong product shot + narrative.

**Use case:** mid-page module that lets a single hero shot do most of the work.

**Character limits:**
- Headline: 200 characters
- Body: 500 characters

**Image spec:** 300×300 px (square).

**Writing pattern:** image carries the visual; copy carries one specific value point.

**Pitfalls:**
- Long copy paired with a tiny square image — visual imbalance
- Image that doesn't earn the half-page real estate

---

## Module 9: Standard Image Header With Text Overlay (Light or Dark)

A header image with text overlaid directly on the image. Two variants: light text (for dark images) or dark text (for light images).

**Use case:** stylish hero replacement when the image is photographic and atmospheric enough to carry text overlay legibly.

**Character limits:**
- Headline: 150 characters
- Body: 500 characters
- Image alt text: 100 characters

**Image spec:** 970×300 px. Image must have enough negative space for the text to be readable.

**Writing pattern:** same as Standard Image Header (Module 2), but the headline + body get composited onto the image itself.

**Pitfalls:**
- Image too busy → text becomes unreadable
- Light text on a partially-light image → fails for low-vision shoppers and may fail Amazon accessibility checks
- Text-overlay images get cropped differently on mobile vs desktop; test both before publishing

---

## Module 10: Standard Multiple Image Module A

Four small images in a horizontal row, no individual text per image. Used as a visual rhythm break.

**Use case:** showing multiple use cases, color options, or scene variations in a single visual row.

**Character limits:**
- Headline (above row): 200 characters
- Image alt text per image: 100 characters each

**Image spec:** each image 300×300 px (4 in a row).

**Writing pattern:** the headline does most of the work ("Six ways to wear it"); the images carry the variation.

**Pitfalls:**
- Four images that aren't visually parallel (different lighting, different scales) → looks careless
- Headline that doesn't unite the four images thematically

---

## Module 11: Standard Single Left Image

Similar to Single Side Image but with a different default arrangement. Image on the left, copy on the right, with more text than Module 8.

**Use case:** when the image is supporting and the copy is the lead.

**Character limits:**
- Headline: 200 characters
- Body: 1000 characters

**Image spec:** 300×300 px.

**Writing pattern:** copy-led module. Use when there's substantive narrative content that benefits from one supporting image.

---

## Module 12: Standard FAQ Module (Amazon's Question/Answer module)

A 3-5 question accordion-style FAQ block.

**Use case:** addressing the most common objections in question form.

**Character limits:**
- Module headline: 200 characters
- Per Q&A pair:
  - Question: 200 characters
  - Answer: 500 characters

**Writing pattern:**
- Questions should be real ones shoppers ask (pull from customer service tickets, reviews, comments)
- Answers should be concise, factual, brand-voice-appropriate
- Don't disguise marketing as FAQ — shoppers see through it

**Pitfalls:**
- Fake FAQ ("Is this product great?") — instant trust failure
- Answers longer than the question merits — keep them tight

---

## Module summary table (for the smart-pick algorithm to reference)

| ID | Module name | Best use | Image-heavy? | Copy-heavy? |
|----|---|---|---|---|
| 1 | Company Logo | Brand visual rest | Yes | No |
| 2 | Image Header With Text | Page hero | Balanced | Balanced |
| 3 | Single Image & Highlights | 4-benefit summary | Balanced | Balanced |
| 4 | Single Image & Sidebar | Detail callout | Balanced | Balanced |
| 5 | Four Image & Text | Benefit grid | Yes | Balanced |
| 6 | Comparison Chart | Catalog cross-sell | Balanced | Yes |
| 7 | Product Description Text | Long-form story | No | Yes |
| 8 | Single Side Image | Mid-page hero | Yes | Balanced |
| 9 | Image Header With Text Overlay | Atmospheric hero | Yes | Balanced |
| 10 | Multiple Image Module | Use-case variation | Yes | No |
| 11 | Single Left Image | Copy-led detail | Balanced | Yes |
| 12 | FAQ | Objection handling | No | Yes |

---

## What never to put in any A+ Content module

Cross-module compliance rules — enforced in `copy-conventions.md` and verified in the compliance check step:

- **No external URLs** (TOS)
- **No CTAs that route off-Amazon** ("Visit our website", "Email us", "Follow us")
- **No prohibited claims** (FDA approval, "cures", "miracle", "guaranteed weight loss", etc. — category-specific)
- **No pricing or promotional language** ("$50", "On sale", "Save 20%") — Amazon controls price display
- **No competitor brand names** (TOS)
- **No reviews or testimonials with attribution** (Amazon's policy — testimonials need to be generic, not "Jane S. said...")
- **No trademark symbols (™, ®, ©) you don't own**
- **No copyright violations** — only use imagery you own or have rights to
