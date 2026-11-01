---
name: a-plus-content-creator
description: >
  Builds Amazon Standard A+ Content (Enhanced Brand Content / EBC) for Brand Registered sellers.
  Smart-picks the strongest 4-5 modules per product from the full Amazon A+ library, drafts compliant
  copy, and either generates per-module images via Fal AI (when key is set) or outputs detailed Canva
  briefs. Produces a .docx brief plus an HTML mock-up preview. Use this skill when the user mentions
  A+ Content, A Plus Content, Enhanced Brand Content, EBC, Amazon brand content, Amazon modules,
  comparison chart for Amazon, 'build A+ for my listing,' 'I just got Brand Registered,' 'create A+
  Content for [product],' 'rewrite my A+ Content,' or 'Amazon modules aren't converting.' Also trigger
  when the user references the Amazon Seller Central A+ Content editor or Brand Registry. Default to
  single-product mode.
---

# A+ Content Creator

Writes Amazon Standard A+ Content for Brand Registered sellers. Picks the best modules for the product, drafts compliant copy, generates module images via Fal AI (when key set) or outputs Canva briefs, and previews the result as a visual HTML mock-up.

## How this skill works at a glance

1. **First-run check.** Load the shared plugin config; trigger onboarding if missing. Check for Fal AI key.
2. **Confirm Brand Registry.** A+ Content requires Brand Registry. Confirm with the buyer before proceeding.
3. **Gather product input.** Shopify pull, Amazon pull (where available), URL fetch, paste, or photos.
4. **Check the keyword cache.** Pull `keywords.json` from skill #2's shared cache if it exists.
5. **Smart-pick the modules.** Pick the strongest 4-5 modules from the library based on product, category, and brand voice.
6. **Draft module copy.** Apply chosen modules + brand voice + keywords. Respect Amazon character limits per module.
7. **Generate or brief the images.** If Fal AI key set → generate. If not → produce detailed Canva briefs.
8. **Render both outputs.** `.docx` brief + HTML mock-up of the assembled page.
9. **Report back.** File paths, modules picked + why, image source (Fal vs Canva), compliance check, suggested next step.

---

## Step 1: First-run check

Look for `<plugin-root>/.config/the-ecommerce-seller.config.json`. If missing or incomplete, run the onboarding flow from `../product-description-writer/templates/onboarding.md`.

After loading config, **explicitly check for `config.api_keys.fal_ai`**. If absent or empty, note that the skill will fall back to Canva briefs for this run. Tell the buyer (once) that they can add a Fal AI key any time via "update my plugin config" → image generation kicks in automatically on the next run.

---

## Step 2: Confirm Brand Registry

A+ Content is **only available to Brand Registered Amazon sellers.** Before drafting, confirm:

- Ask: "Quick confirm — is your brand Amazon Brand Registered? A+ Content is only available to sellers with active Brand Registry."
- If yes → proceed.
- If no → explain the requirement (Brand Registry requires a registered trademark and an Amazon Seller Central account). Offer to write a brand-story Shopify page in the meantime (route them to the Landing Page Copywriter, skill #3). Don't waste time generating A+ Content the buyer can't publish.
- If "I think so" → ask them to verify in Seller Central → Brand Registry. The skill stays paused until confirmed.

This single check prevents the most common failure mode for this skill: drafting hours of A+ Content the buyer can't use.

---

## Step 3: Gather product input

Same flexible input pattern as skills #1, #2, #3. Sources:

- **Shopify connector pull** (if connected and the product is in Shopify)
- **Amazon connector pull** (where MCP support is available — pulls the current Amazon listing including any existing A+ Content for audit/refresh)
- **Product URL fetch** (Amazon listing URL → use `web_fetch`; escalate to Claude in Chrome if the page is client-rendered)
- **Pasted specs** (the universal fallback)
- **Product photos** (vision analysis for context — also feeds the image generation step downstream)

For best A+ Content output, the skill needs:
- Product category (essential — determines smart-pick module choices)
- Materials / ingredients / contents
- 3-5 key benefits in the brand's voice
- Existing reviews if available (gold for testimonial-style modules and FAQ selection)
- Reference photos (informs the visual style of generated images)

If anything's missing, ask one round of targeted questions before drafting.

---

## Step 4: Check the keyword cache

Use `scripts/keyword_cache_reader.py` to check `<plugin-root>/.cache/keywords/{product-identifier}.json`. Same lookup logic as skill #3: try Shopify handle → ASIN → slugified product name.

If keywords found, capture the top 6-10 ranked keywords. They get woven into:
- Module headlines (1-2 per module)
- Module body copy (naturally, never stuffed)
- Image alt text (1 keyword per image when relevant)

If no cache, proceed without — the modules still get written. Note in the final report that running the Listing SEO Optimizer first would improve organic indexing of the A+ Content.

---

## Step 5: Smart-pick the modules

Read `templates/module-library.md` for the full module library and `templates/smart-pick-logic.md` for the selection algorithm.

The short version of the algorithm:

1. **The Hero module** is included for every product. (Image header with text below — sets the page tone.)
2. **One Benefits module** is included for every product. (Either Image Header + Highlights or Four-Image Grid — depending on whether the buyer has 4 single feature photos or one strong hero shot.)
3. **One Comparison module** is included when:
   - The product is in a spec-comparable category (kitchen tools, supplements, electronics, fitness gear)
   - The buyer has at least 2-3 clear advantages over a competitor
4. **One Brand-or-Story module** is included when the buyer has a real story (loaded from `config.brand_voice.voice_examples`).
5. **One FAQ-or-Trust module** is included when reviews / customer service tickets surface common objections.

The final picks should total 4-5 modules. Amazon's hard cap is 5 modules in Standard A+, plus a Product Description Text module that doesn't count against the cap (we use that for closing copy when room allows).

Tell the buyer in the brief which modules were picked and why ("Picked the Comparison module because your product has 3 clear advantages over [category leader]; skipped FAQ because your reviews don't surface a consistent objection").

---

## Step 6: Draft module copy

For each picked module, read its section in `templates/module-library.md` for character limits and structural conventions. Read `templates/copy-conventions.md` for cross-module rules (Amazon compliance, no-claims, no external URLs).

Apply:
- The buyer's brand voice from `config.brand_voice`
- The audience description from `config.audience`
- Keywords from the cache (when present)
- The platform's strict character limits (over = rejection by Amazon)

Show character counts inline in the brief output so the buyer can verify nothing's over.

---

## Step 7: Generate or brief the images

For each module, there's an image (or several images) to either generate or brief.

### When Fal AI key is set

Read `templates/fal-prompts.md` for prompt patterns per module type. Then use `scripts/fal_image_generator.py` to call the Fal API.

Each module's image gets a Fal prompt assembled from:
- Module type (determines composition + style framing)
- Product context (color, material, mood from `config.brand_voice` and product photos)
- Background / setting (matches brand aesthetic)
- Negative prompts (avoid: stock-photo look, text-in-image, watermarks, distorted product)

Generated images get saved to the output folder alongside the brief, with filenames like `{product-slug}_aplus_module-1-hero.png`. The HTML mock-up references these files directly. The .docx brief embeds them inline.

### When Fal AI key is NOT set

Read `templates/canva-briefs.md` for the brief template. Each module's image gets a brief with:
- Composition (what's in the frame, where the product sits, what surrounds it)
- Mood (lighting, color palette, energy)
- Required dimensions (per Amazon spec, see `templates/amazon-image-specs.md`)
- Recommended Canva template starting point
- Notes for the photographer if they'll shoot custom (vs designer making a composite)

Briefs are detailed enough that the buyer can hand them to a freelance Canva designer or a photographer and get back assets that match the module spec exactly.

---

## Step 8: Render both outputs

### Output 1: `.docx` brief

Use the `docx` skill (read its SKILL.md if not already done this session) and `scripts/render_brief_docx.py`. Document structure:

```
[Product name] — Amazon A+ Content Brief
Generated [date] · Brand: [brand_name]
Modules picked: 5 (see selection rationale below)
Image source: Fal AI generated | Canva briefs

══════════════════════════════════════════════════
MODULE SELECTION RATIONALE
══════════════════════════════════════════════════
One paragraph explaining which modules were chosen and why,
which were skipped and why.

══════════════════════════════════════════════════
MODULE 1 — [module type name]
══════════════════════════════════════════════════
[Visual preview of the module image — embedded if generated, brief if not]
Headline (XX/[limit]): [...]
Body copy (XX/[limit]): [...]
Image specs: [Amazon's required dimensions for this module]
Image alt text (XX/[limit]): [...]

[For each module — total 4-5]

══════════════════════════════════════════════════
COMPLIANCE CHECK
══════════════════════════════════════════════════
- No prohibited claims (FDA, miracle, cure, etc.): ✓
- No external URLs: ✓
- No CTAs: ✓
- No competitor mentions: ✓
- No price/promotion mentions: ✓
- All images within size + dimension limits: ✓

══════════════════════════════════════════════════
HOW TO PUBLISH
══════════════════════════════════════════════════
1. Sign into Amazon Seller Central
2. Brands menu → A+ Content Manager → Create A+ Content
3. Select Standard A+
4. For each module: pick the matching module type from Amazon's menu,
   paste the copy from this brief, upload the image.
5. Save & submit for Amazon review (typically 1-7 days).
```

Save to `config.output_folder`.

### Output 2: HTML mock-up of the assembled page

Use `scripts/render_html_preview.py`. Produces a single `.html` file that visually stacks all the modules so the buyer sees the whole page before publishing.

Conventions:
- Each module wrapped in a `<section class="aplus-module aplus-module-{slug}">`
- Tailwind utility classes for styling
- Generated images shown inline (relative path); Canva-brief modules show a placeholder with the brief text overlaid
- Mobile preview included at the top — Amazon's mobile rendering is what most shoppers see

The mock-up isn't pixel-perfect (Amazon's actual rendering uses their own CSS) but it gives the buyer a structural preview of the visual flow.

Save with matching filename: `{slug}_aplus_brief.docx` and `{slug}_aplus_preview.html`.

---

## Step 9: Report back

Tell the buyer:
1. Where both files are (`computer://` links)
2. Modules picked (with one-line rationale)
3. Image source ("Generated 5 images via Fal AI" or "5 Canva briefs ready for your designer")
4. Compliance check summary (pass / fail per category)
5. One suggested next step:
   - If image generation succeeded: "Upload the images and copy to Seller Central → A+ Content Manager. Amazon review takes 1-7 days."
   - If using Canva briefs: "Hand the briefs to your designer. When images are ready, re-run the skill with the images attached for a final preview check."
   - If no keyword cache was found: "Run the Listing SEO Optimizer first if you want SEO-weighted copy."

Keep it short.

---

## Connector availability and graceful degradation

- **Best case** — Brand Registered + Shopify connected + Fal AI key set + keywords cached: full pipeline, generated images, keyword-weighted copy
- **No Fal key** — copy still drafted, Canva briefs produced instead of images. Skill still ships a complete deliverable.
- **No Shopify / no Amazon connector** — buyer pastes product info, no current-A+ audit possible, but new A+ Content still drafted from scratch
- **Not Brand Registered** — skill halts at Step 2 with a clear explanation and a redirect to the Landing Page Copywriter for Shopify brand-story work

---

## Edge cases

- **Buyer already has A+ Content and wants a refresh**: pull the current A+ Content (Amazon connector) or ask the buyer to paste it. Audit which modules are working, which aren't (based on engagement data if available), and propose replacements.
- **Regulated category (supplements, beauty, baby products, electronics with safety claims)**: Amazon has category-specific compliance rules. Read the Amazon Brand Registry guidelines for the category and avoid claims that will trigger rejection. Compliance check covers the common pitfalls; flag anything category-specific you can't verify.
- **Variant-heavy product**: A+ Content is per-listing, not per-variant. Write modules that cover the variant range generally ("available in three sizes") rather than per-variant copy.
- **Buyer wants Premium A+ modules**: politely note Premium A+ is invite-only and not in this skill's scope yet. Offer to draft the equivalent in Standard A+ modules where possible.
- **Image generation fails partway**: if Fal AI returns errors for one or more modules (rate limit, prompt safety, etc.), continue with the remaining modules and fall back to Canva briefs for the failed ones. Note clearly in the report.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- `templates/module-library.md` — full Standard A+ module library with character limits, use cases, examples
- `templates/smart-pick-logic.md` — algorithm for choosing 4-5 modules per product
- `templates/amazon-image-specs.md` — exact image dimensions per module + Amazon image rules
- `templates/copy-conventions.md` — A+ Content writing rules (compliance, voice, character limits)
- `templates/fal-prompts.md` — Fal AI prompt templates per module type
- `templates/canva-briefs.md` — Canva brief structure for the no-Fal-key fallback
- `scripts/config_loader.py` — shared config loader
- `scripts/keyword_cache_reader.py` — read the shared keywords cache from skill #2
- `scripts/fal_image_generator.py` — call Fal AI when key is set
- `scripts/render_brief_docx.py` — .docx brief renderer
- `scripts/render_html_preview.py` — HTML mock-up renderer
- `examples/single-product-aplus-example.md` — reference output with Fal images
- `examples/canva-brief-example.md` — reference output when no Fal key
