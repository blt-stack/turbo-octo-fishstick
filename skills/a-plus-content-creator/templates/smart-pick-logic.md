# Smart-Pick Algorithm — Choosing 4-5 Modules per Product

Amazon allows a max of 5 modules in Standard A+ Content (plus an optional Product Description Text module that doesn't count). Different products convert better with different module combinations. This file specifies how to pick the right 4-5 for any product.

## Why not always pick the same 5

A coffee dripper, a face cream, and a kitchen knife have completely different conversion bottlenecks. The dripper benefits most from comparison + ritual story. The face cream benefits most from ingredients + before/after. The knife benefits most from use cases + craft + comparison. A one-size-fits-all module set leaves conversion on the table.

The smart-pick algorithm produces the strongest 4-5 modules for each product's specific bottlenecks.

---

## The 4-pillar pick

Every A+ page includes one module from each of these 4 pillars. Then a 5th is added based on product type.

### Pillar 1: Hero (mandatory — always pick exactly one)

**Goal:** set the page tone, name the value proposition.

**Pick logic:**
- If the brand has a strong atmospheric product photo → **Module 9: Image Header With Text Overlay** (light or dark depending on image)
- If the product photo is clean catalog-style → **Module 2: Image Header With Text**
- Default: Module 2

### Pillar 2: Benefits (mandatory — always pick exactly one)

**Goal:** show 3-4 key benefits visually + textually.

**Pick logic:**
- If the buyer has 4 strong individual feature photos → **Module 5: Four Image & Text** (best for visual benefit grid)
- If the buyer has one strong feature photo + 4 written benefits → **Module 3: Single Image & Highlights** (best when only one supporting visual exists)
- Default: Module 3

### Pillar 3: Story OR Detail (mandatory — pick one)

**Goal:** add depth — either the brand story (why this product exists) or a deep-dive on a key feature.

**Pick logic:**
- If `config.brand_voice.voice_examples` has substantive brand-story content → **Module 8: Single Side Image** with story-led copy
- If the product has a single technical/material detail that deserves a deep dive → **Module 4: Single Image & Sidebar**
- If the buyer has a long-form story they want to tell prose-only → **Module 7: Product Description Text**
- Default: Module 8 with story-led copy

### Pillar 4: Trust OR Comparison (mandatory — pick one)

**Goal:** address the most common objection (either via FAQ-style or comparison-style framing).

**Pick logic:**
- If the buyer has 2+ related products in their Amazon catalog (so a cross-product comparison helps shoppers self-select) → **Module 6: Comparison Chart**
- If reviews / customer service tickets surface a consistent objection → **Module 12: FAQ Module**
- If neither applies → **Module 12: FAQ Module** with generic-but-real questions
- Default: Module 12

### Pillar 5: Optional fifth pick (when room exists)

**Pick logic:**
- If the product has multiple use cases, color variants, or scene variations and Pillars 1-4 didn't already cover them → **Module 10: Multiple Image Module** (visual use-case row)
- If the product story is half-told and another image-rich module would deepen it → **Module 11: Single Left Image** (copy-led detail)
- If the brand has a recognizable logo worth showing as a visual rest → **Module 1: Company Logo**
- If 4 modules already cover the product comprehensively → **stop at 4.** Don't add modules for completeness — every module has to do conversion work.

---

## Category-specific tuning

The pick logic adjusts for product category. These overrides take precedence over the defaults above.

### Apparel / Accessories
- Add **Module 10: Multiple Image Module** (color/style variants)
- Use **Module 12: FAQ** for sizing questions specifically

### Supplements / Beauty / Skincare
- Use **Module 4: Single Image & Sidebar** for ingredients deep-dive
- Use **Module 5: Four Image & Text** for benefits (faster perception than highlights for sensory products)
- **Comparison module skip rule:** comparison only if buyer has multiple SKUs in the same line; otherwise FAQ wins

### Kitchen Tools / Cookware
- Use **Module 5: Four Image & Text** for use-case grid (4 dishes to make, 4 cooking methods, etc.)
- Use **Module 6: Comparison Chart** when buyer has multiple cookware SKUs
- Use **Module 7: Product Description Text** for materials/craft story

### Electronics
- Use **Module 6: Comparison Chart** liberally (Amazon shoppers comparison-shop electronics aggressively)
- Use **Module 5: Four Image & Text** for feature highlights
- Use **Module 12: FAQ** for "is it compatible with X" questions

### Home & Decor
- Use **Module 10: Multiple Image Module** for room scenes
- Use **Module 8: Single Side Image** for story (the brand's POV on the category)

### Fitness / Outdoor / Hobbyist Equipment
- Use **Module 5: Four Image & Text** for in-use variation
- Use **Module 12: FAQ** for skill-level questions ("Is this for beginners?")
- Use **Module 4: Single Image & Sidebar** for the differentiating spec

### Kids / Baby
- Use **Module 12: FAQ** for safety questions specifically
- Use **Module 3: Single Image & Highlights** for benefits
- Use **Module 7: Product Description Text** for the brand's safety / sourcing commitment

---

## The "skip these modules" list

Some modules are weak for A+ Content and should rarely be picked:

- **Module 1: Company Logo** — only pick when the logo carries real brand recognition. Otherwise wastes a slot.
- **Module 7: Product Description Text** — only when there's substantive long-form prose to add. Doesn't count against the 5-module cap, so it's a "bonus" module rather than a primary pick.
- **Module 11: Single Left Image** — overlaps heavily with Module 8 (Single Side Image); typically pick one or the other based on layout preference.

---

## Output format for the pick rationale

The brief includes a one-paragraph explanation of the picks. Use this template:

```
MODULE SELECTION RATIONALE

For [product name], the strongest module set is:

1. [Module X: name] — picked as the Hero because [reason: image style, brand voice, etc.]
2. [Module X: name] — picked as Benefits because [reason: photo availability, benefit count]
3. [Module X: name] — picked for Story because [reason: brand has narrative depth / single
   deep-dive feature warrants its own spotlight]
4. [Module X: name] — picked for Trust because [reason: comparison opportunity / common
   objection in reviews / etc.]
5. [Module X: name OR "stopped at 4 — 4 modules cover this product fully"]

Skipped:
- [Module X] — [reason it's a bad fit for this product]
- [Module X] — [reason]
```

This transparency lets the buyer see the reasoning and override if they have inside knowledge ("actually, we should use the FAQ — we keep getting the same shipping question").

---

## When the buyer overrides the picks

If the buyer says "include FAQ instead of comparison" or "skip the story module, my brand doesn't have one yet" — honor the override. Note it in the brief ("Picks reflect buyer override — comparison swapped for FAQ at buyer request") so the rationale stays transparent.

Don't argue with the override. If the buyer's wrong, they'll see it in the metrics and ask for a re-run.
