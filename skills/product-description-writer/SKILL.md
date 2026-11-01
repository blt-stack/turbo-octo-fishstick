---
name: product-description-writer
description: >
  Converts product specs, URLs, Shopify records, or photos into platform-ready product descriptions
  across six marketplaces — Shopify, Amazon, Etsy, eBay, Walmart, and TikTok Shop. Each description
  honors the platform's character limits, structural conventions, and SEO best practices. Supports
  single-product mode (one product, multiple platforms, .docx output) and bulk mode (CSV of products,
  .xlsx with one row per product per platform). Reads keywords from the Listing SEO Optimizer cache
  when present. Use this skill when the user mentions product description, product copy, 'write me a
  product description,' 'describe this product,' 'Shopify description,' 'Amazon listing copy,' 'Etsy
  listing,' 'list this product,' or pastes product specs or a product URL and asks for copy.
---

# Product Description Writer

Writes platform-ready product descriptions across Shopify, Amazon, Etsy, eBay, Walmart, and TikTok Shop from any input the user has on hand. Produces two variants per platform so the user can A/B test or pick the strongest.

## How this skill works at a glance

1. **First-run check.** If the buyer's config doesn't exist yet, run onboarding and save it.
2. **Detect mode.** Single product or bulk? Default is single unless the user provides a CSV, names a Shopify collection, or asks for many at once.
3. **Gather product input.** Use whatever source the user provided — Shopify connector, pasted specs, product URL, or photos. Fall back gracefully when a connector isn't available.
4. **Apply brand voice.** Load the voice profile from config and apply it to every variant.
5. **Generate per-platform copy.** Run through each platform the buyer sells on, producing two distinct variants each.
6. **Render output.** Single mode → one polished `.docx` per product saved to the buyer's output folder. Bulk mode → one `.xlsx` with all products and platforms.
7. **Report back.** Share the file path(s) and a one-line summary.

---

## Step 1: First-run check

Before doing anything else, check whether the buyer has completed onboarding. Look for a `config.json` file in the parent plugin directory:

**Expected location:** `<plugin-root>/.config/the-ecommerce-seller.config.json`

Where `<plugin-root>` is the directory containing `plugin.json` (one level above the `skills/` folder).

**If `config.json` exists and is complete** (all required fields present), load it and skip to Step 2.

**If `config.json` is missing or incomplete**, run the onboarding flow described in `templates/onboarding.md`. Once complete, save the answers to `config.json` and continue.

Onboarding covers store info, primary platforms, brand voice (analyzed from existing listings if Shopify is connected, otherwise a voice questionnaire), target audience, and vocabulary preferences. The whole flow should take the buyer 2-5 minutes. This config is shared across all skills in the plugin, so the buyer only does this once.

If config exists but the user explicitly says "redo onboarding" or "update my brand voice," re-run the flow and overwrite.

---

## Step 2: Detect mode

Single product mode is the default. Switch to bulk mode when any of these are true:

- The user attaches a CSV or .xlsx file of products
- The user says "all my products," "everything in [collection name]," "my whole catalog," "all [X] products," or similar
- The user references a Shopify collection or smart collection by name
- The user provides a list of 5+ product names/handles in one message

Confirm the mode out loud before proceeding. For bulk mode, additionally confirm the source (which CSV, which collection) and remind the buyer that bulk will produce a single `.xlsx` rather than per-product `.docx` files.

---

## Step 3: Gather product input

The skill accepts product information from any of four sources. The buyer can mix and match. If multiple sources are given for the same product, use all of them — they enrich each other.

### Source A: Shopify connector pull

If a Shopify connector is available (check via `mcp__mcp-registry__list_connectors` or by attempting a tool call), pull the product by handle or ID. Capture: title, current description, product type, vendor, tags, variants, price, images, and metafields if accessible.

When Shopify is not connected but the buyer wants to use it, point them to install the Shopify connector and offer to continue with another input method in the meantime.

### Source B: Pasted specs

The buyer pastes raw product info — could be a spec sheet, a list of features, a brief, or just bullet points. Parse it for: product name, category, materials, dimensions, use cases, key features, target audience signals, and price if mentioned. Fill in reasonable assumptions for missing fields and flag them so the buyer can correct.

### Source C: Product URL

The buyer drops a URL (their own listing, a competitor's, or an inspiration product). Use `mcp__workspace__web_fetch` to retrieve the page. Parse for title, bullets, description, images, and reviews if visible. If the page is client-rendered and returns an empty shell, escalate to `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text` (load tool schemas via ToolSearch first if needed).

For competitor URLs, never copy phrasing verbatim — extract the underlying product attributes and write fresh copy.

### Source D: Photos

The buyer attaches one or more images. Use vision to infer: product category, materials, colors, finish, scale (with context), styling, likely use cases, and audience. Ask the buyer to confirm any inferences that materially affect the copy (e.g., "I'm reading this as solid oak — correct?").

---

## Step 4: Apply brand voice

Load the voice profile from `config.json`. The profile includes:

- `brand_name`, `tagline`, `archetype` (e.g., "rebel", "sage", "everyman")
- `tone` (e.g., "warm and witty", "technical and direct", "playful and irreverent")
- `vocabulary_use` — words and phrases the brand leans into
- `vocabulary_avoid` — words and phrases the brand never uses
- `audience_description` — who the buyer sells to
- `voice_examples` — 2-3 short paragraphs of approved brand copy if the buyer provided them

Every variant generated must read like it came from the same brand. The voice is what makes the output feel like the buyer's, not generic AI copy. If the voice profile is sparse, lean on the audience description and the buyer's own examples rather than guessing.

---

## Step 5: Generate per-platform copy

For each platform the buyer sells on (from `config.platforms_enabled`), generate two variants. Each variant should have a meaningfully different angle — not minor wording tweaks. Lean on these angle archetypes:

- **Benefit-led**: focuses on outcomes and transformation
- **Story-led**: opens with a narrative or situational hook
- **Social-proof-led**: leans on reviews, popularity, or third-party validation
- **Problem/solution**: names the problem the buyer is escaping
- **Feature-rich**: foregrounds technical specs for spec-driven buyers

Pick the two strongest angles for each product based on the input. Don't pick at random.

Read the platform-specific format guides in `templates/`:

- `templates/shopify-format.md`
- `templates/amazon-format.md`
- `templates/etsy-format.md`
- `templates/ebay-format.md`
- `templates/walmart-format.md`
- `templates/tiktok-shop-format.md`

Each file describes the exact structure, character limits, and conventions for that platform. Follow them strictly — character limits in particular are not suggestions. Amazon titles over 200 characters get rejected; Etsy titles over 140 do too. The guides include common pitfalls.

### Keyword handling

If the user provided a keyword list (or a prior Listing SEO Optimizer run left keywords in the buyer's workspace), weave the keywords in naturally — title and first bullet first, then body copy. Never stuff. If no keywords were provided, write for humans first and don't infer keywords inside this skill.

---

## Step 6: Render output

### Single mode

Produce one `.docx` per product. Use the `docx` skill — read its SKILL.md if you haven't already in this session. The document structure:

```
[Product name]
Generated [date] · Brand: [brand_name] · Source: [Shopify | URL | pasted | photo]

──────────────────────────────────────────
Shopify — Variant 1 (Angle: [angle name])
──────────────────────────────────────────
[Title]
[Long-form description with subheadings, bullets, FAQ]
Meta description: [...]

Shopify — Variant 2 (Angle: [angle name])
[same structure]

──────────────────────────────────────────
Amazon — Variant 1 (Angle: [angle name])
──────────────────────────────────────────
Title (XX/200 chars): [...]
Bullet 1 (XX/250): [...]
Bullet 2 (XX/250): [...]
Bullet 3 (XX/250): [...]
Bullet 4 (XX/250): [...]
Bullet 5 (XX/250): [...]
Description (XX/2000): [...]
Backend search terms (XX/250): [...]

[...repeat for Amazon Variant 2, then Etsy, eBay, Walmart, TikTok Shop...]
```

Always show character counts inline so the buyer can verify nothing was truncated. Save the file to the buyer's output folder (from `config.output_folder`, defaulting to their workspace root).

A worked example output is in `examples/single-product-example.docx` — match that structure.

### Bulk mode

Produce one `.xlsx`. Use the `xlsx` skill — read its SKILL.md if needed. Structure:

- **Sheet 1: Products** — one row per product, columns for each platform variant
  - Columns: `Product Name`, `SKU`, `Shopify Title v1`, `Shopify Body v1`, `Shopify Title v2`, `Shopify Body v2`, `Amazon Title v1`, `Amazon Bullets v1`, `Amazon Description v1`, ... (and so on through all enabled platforms × 2 variants)
- **Sheet 2: Character Counts** — same shape, but each cell is `actual/limit` (e.g., `187/200`). Use conditional formatting (red fill) for any cell over limit.
- **Sheet 3: Source Info** — for traceability: per-product input source, brand voice version used, keywords applied.

Bulk runs should process products in parallel using Python helpers when possible. See `scripts/bulk_processor.py` for the orchestration pattern.

---

## Step 7: Report back

Tell the buyer:
1. Where the file is (use a `computer://` link)
2. Total platforms × variants generated
3. Any inferences flagged for their review (e.g., "I assumed this is solid oak based on the photo — confirm and I'll regenerate if it's veneer")
4. Quick reminder of the next logical step (e.g., "Run Listing SEO Optimizer next to get keyword-weighted variants" — but only when relevant)

Keep the report short. The buyer wants the file, not a lecture.

---

## Connector availability and graceful degradation

Skills in this plugin are designed to work even when no connectors are installed. Use this priority order when sourcing product info:

1. Shopify connector → if available and the buyer references a Shopify product
2. URL fetch → if the buyer provides a URL
3. Photos → if attached
4. Pasted text → universal fallback

When a connector the buyer asked for is missing, tell them once (with installation instructions) and offer to proceed with a different source. Don't nag.

If `mcp-registry` is available, use `mcp__mcp-registry__list_connectors` to detect what's installed. If not, attempt the tool call and handle failure gracefully.

---

## Edge cases

- **Product with multiple variants (size/color)**: generate copy that works across the variant set unless the user asks for variant-specific copy. Mention variant axes naturally where they matter (e.g., "available in three finishes").
- **Adult/restricted products**: refuse for prohibited categories (weapons, controlled substances, etc.). For age-restricted-but-legal categories, write copy that's compliant with the platform's content policy.
- **Very thin product info**: if input is sparse (e.g., one blurry photo, no specs), ask one round of clarifying questions before generating. Don't fabricate features that aren't supported by input.
- **Mismatch between input sources**: if pasted specs and the URL fetch disagree, ask the buyer which is canonical.
- **Bulk run with hundreds of products**: warn the buyer about expected runtime and confirm before starting. Offer to process the first 10 as a preview, get sign-off, then proceed.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — config schema with documented defaults
- `templates/onboarding.md` — first-run onboarding flow
- `templates/voice-questionnaire.md` — fallback voice capture when no listings to analyze
- `templates/voice-analysis-prompt.md` — instructions for inferring voice from existing listings
- `templates/shopify-format.md` — Shopify PDP format and character limits
- `templates/amazon-format.md` — Amazon listing format and character limits
- `templates/etsy-format.md` — Etsy listing format and character limits
- `templates/ebay-format.md` — eBay listing format and character limits
- `templates/walmart-format.md` — Walmart listing format and character limits
- `templates/tiktok-shop-format.md` — TikTok Shop listing format
- `scripts/config_loader.py` — load/save/validate config
- `scripts/render_single_docx.py` — render single-product .docx
- `scripts/render_bulk_xlsx.py` — render bulk .xlsx
- `scripts/bulk_processor.py` — parallel orchestration for bulk runs
- `examples/single-product-example.md` — reference output for single mode
- `examples/bulk-output-example.md` — reference output structure for bulk mode
