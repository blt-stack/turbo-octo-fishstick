---
name: landing-page-copywriter
description: >
  Writes full-page landing page architectures with copy for e-commerce — product detail pages (PDPs),
  collection pages, marketing landing pages, and About pages. Uses six conversion frameworks (PAS,
  AIDA, BAB, JTBD, FAB, PASTOR) selected by page type and audience awareness level. Includes hero
  variations (main plus 3 alternates for A/B testing). Outputs a .docx brief for designers plus a
  ready-to-paste Tailwind HTML sections file. Pulls keywords from the Listing SEO Optimizer cache for
  organic lift without compromising conversion. Use this skill when the user mentions landing page,
  PDP, product detail page, product page copy, collection page, marketing landing page, about page,
  'write me a landing page,' 'PDP copy,' 'collection page copy,' 'rewrite my product page,' or 'page
  architecture.'
---

# Landing Page Copywriter

Writes full-page architectures plus copy for PDPs, collection pages, marketing LPs, and About pages. Output is both a `.docx` brief and a Tailwind HTML version the buyer can paste straight into their store.

## How this skill works at a glance

1. **First-run check.** Load the shared plugin config; trigger onboarding if missing.
2. **Detect page type.** PDP, collection, marketing LP, or About — default to PDP.
3. **Gather page input.** Shopify pull, URL fetch, paste, or photos.
4. **Check the keyword cache.** If skill #2 wrote a `keywords.json` for this product, load it.
5. **Pick a conversion framework.** Smart default based on page type and product fit, overridable.
6. **Write the page architecture.** Block-by-block, following the page-type guide.
7. **Generate the main page + 3 alternate hero blocks.** Hero is the highest-leverage A/B slot.
8. **Render both outputs.** `.docx` brief and Tailwind HTML sections.
9. **Report back.** File paths, framework chosen, keyword integration summary, suggested next test.

---

## Step 1: First-run check

Look for the shared plugin config at `<plugin-root>/.config/the-ecommerce-seller.config.json`. If missing or incomplete, run the onboarding flow from `../product-description-writer/templates/onboarding.md`. The config is shared across all skills in this plugin.

Use `scripts/config_loader.py` (identical to the version in skills #1 and #2).

---

## Step 2: Detect page type

The four supported types:

| Type | Trigger phrases | Default framework |
|---|---|---|
| **PDP** | "product page", "PDP", "product detail page", "rewrite my product", or just product info with no other context | JTBD or PAS, depending on product category |
| **Collection** | "collection page", "category page", "collection hero", "category description" | FAB or AIDA |
| **Marketing LP** | "landing page", "campaign page", "BFCM page", "launch page", "paid ad destination", "promo page" | PASTOR or PAS |
| **About** | "About page", "About Us", "brand story", "founder note", "mission page" | (none — narrative-driven, no conversion framework) |

If the user's request is ambiguous, ask one clarifying question with options ("Is this a product page, a collection page, a campaign landing page, or an About page?"). Default to PDP when no signal at all.

---

## Step 3: Gather page input

Same flexible input pattern as skill #1. The buyer can mix and match sources.

### Source A: Shopify connector pull

If Shopify is connected and the buyer references a product, collection, or page, pull it. Capture title, current content, images (with current alt text), variants, price, tags, and reviews (where accessible — reviews are gold for social-proof blocks).

For PDP: pull the product + its reviews.
For collection: pull the collection + the first 6-12 products in it (used in the page).
For About: pull existing About page content if it exists.

### Source B: Paste current page content

The buyer pastes whatever they have — could be a current page, a brief, a half-finished draft, an old version. Parse and use as starting context.

### Source C: URL fetch

The buyer drops a URL (own or competitor). Use `mcp__workspace__web_fetch` first. If client-rendered, escalate to `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`.

For competitor URLs: extract structural choices (how many blocks, what order, what content types) but never copy phrasing.

### Source D: Photos

Useful for PDP (infer product details) and About (founder photo informs the narrative tone). Use vision to extract relevant context.

---

## Step 4: Check the keyword cache

After Step 3, before drafting, check the shared cache:

**Path:** `<plugin-root>/.cache/keywords/{product-identifier}.json`

Where `{product-identifier}` matches what the SEO Optimizer would have written:
1. Shopify product handle (preferred)
2. Amazon ASIN
3. Slugified product name (fallback)

Use `scripts/keyword_cache_reader.py` to load. If present, capture the top 8-10 ranked keywords for weaving into the page's high-visibility blocks (hero hook, value-prop bullets, FAQ questions).

If no cache entry exists, proceed without — the page still gets written, just without the SEO boost. Tell the buyer in the final report ("No keyword cache found for this product — run the Listing SEO Optimizer first if you want SEO-weighted copy").

---

## Step 5: Pick a conversion framework

Read `templates/conversion-frameworks.md` for the full library. Pick using this logic:

1. **If the user named a framework** ("write this in PAS", "use AIDA") → use that one.
2. **If the page type strongly implies a framework** (e.g., About → no framework; PASTOR for marketing LP) → use the type default.
3. **Otherwise** apply the framework-fit heuristic:
   - Product solves a known painful problem → **PAS** (Problem, Agitate, Solve)
   - Product enables a transformation/aspiration → **BAB** (Before, After, Bridge)
   - Product is hired for a job to be done → **JTBD** (Job, Constraints, Outcome)
   - Product is feature-rich and benefits aren't obvious → **FAB** (Features, Advantages, Benefits)
   - Product is paid-traffic-destination LP → **PASTOR** (Person, Amplify, Story, Transformation, Offer, Response)
   - Product is in a category where shoppers compare specs → **AIDA** (Attention, Interest, Desire, Action)

Tell the buyer in the brief which framework was picked and why. They can ask for an alternate run with a different framework.

---

## Step 6: Write the page architecture

Read the matching page-type architecture file for block-by-block structure:

- `templates/pdp-architecture.md`
- `templates/collection-architecture.md`
- `templates/marketing-lp-architecture.md`
- `templates/about-page-architecture.md`

Each file specifies:
- The exact blocks to include and their order
- What each block accomplishes (the conversion job)
- Word/length targets per block
- Variant tactics per block
- Common pitfalls

The framework picked in Step 5 determines *how* the copy flows through the blocks. The page-type guide determines *what blocks exist and in what order*. Combine both.

Apply the buyer's brand voice from `config.brand_voice` to every block. Voice is what makes the page feel like the brand's, not generic high-converting AI output.

---

## Step 7: Generate the main page + 3 alternate hero blocks

After the main page is written, generate **3 alternate hero blocks** (the section above the fold) using `templates/hero-variations.md`. The three alternates use different angles:

- **Alternate A — Problem-aware hero**: leads with the pain the buyer's customer is escaping
- **Alternate B — Outcome-aware hero**: leads with the transformation/result
- **Alternate C — Social-proof-aware hero**: leads with credibility (review count, press mention, founder credential)

Each alternate has its own headline, sub-headline, visual brief, and CTA copy — and is independently runnable in an A/B test. The hero is the highest-leverage A/B slot on any page, so giving the buyer three to test is the single most valuable thing this skill ships.

---

## Step 8: Render both outputs

### Output 1: `.docx` brief

Use the `docx` skill (read its SKILL.md first if you haven't) and `scripts/render_brief_docx.py`. Structure:

```
[Page name / Product name] — Landing Page Brief
Generated [date] · Brand: [brand_name] · Page type: [PDP | Collection | Marketing LP | About]
Framework: [chosen framework] — [one-line reason]
Keywords used: [list, with source: "from SEO Optimizer cache" or "none"]

══════════════════════════════════════════════════
PAGE ARCHITECTURE
══════════════════════════════════════════════════
Block-by-block walkthrough. For each block:
  - Block name (e.g., "HERO", "VALUE PROPS", "FAQ")
  - Purpose (one line — what conversion job this block does)
  - Copy (full text)
  - Visual brief (what image/video should go here, recommended dimensions)
  - Notes for the designer

══════════════════════════════════════════════════
ALTERNATE HERO BLOCKS (for A/B testing)
══════════════════════════════════════════════════
Hero A — Problem-aware
  Headline / Sub-headline / Visual brief / CTA

Hero B — Outcome-aware
  Headline / Sub-headline / Visual brief / CTA

Hero C — Social-proof-aware
  Headline / Sub-headline / Visual brief / CTA

══════════════════════════════════════════════════
RECOMMENDED A/B TEST
══════════════════════════════════════════════════
Which alternate to test first and why, expected lift band, how long to run.
```

Save to `config.output_folder`.

### Output 2: Tailwind HTML sections

Use `scripts/render_html_sections.py`. Produces a single `.html` file with each block as a self-contained Tailwind section the buyer can paste into a Shopify section, PageFly block, or custom theme.

Read `templates/html-conventions.md` for class patterns, semantic structure, accessibility rules, and image placeholder format.

Key conventions:
- Each block wrapped in a `<section>` with a descriptive class (e.g., `.lp-hero`, `.lp-value-props`)
- Tailwind utility classes only — no custom CSS
- Responsive by default (`md:`, `lg:` breakpoints)
- Image placeholders use `<img>` with `src="REPLACE_WITH_YOUR_IMAGE"` and descriptive `alt` text + recommended `width`/`height`
- Semantic HTML (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` where appropriate)
- Accessible (alt text on every image, ARIA labels on icon-only buttons, proper heading hierarchy)

Both files saved with matching base name: `{slug}_landing_page_brief.docx` and `{slug}_landing_page.html`.

---

## Step 9: Report back

Tell the buyer:
1. Where both files are (use `computer://` links)
2. Page type and framework used (one line each)
3. Whether keywords were pulled from the cache (and from where if so)
4. Which alternate hero to test first and why
5. One suggested next step (e.g., "Run the Ad Creative Generator next to write ads pointing at this page")

Keep the report short. Buyer wants the files, not commentary.

---

## Connector availability and graceful degradation

- **Shopify connected**: full product pull + reviews + variants → strongest social-proof block
- **Shopify missing but URL provided**: parse the URL → some loss of review data unless reviews are visible on-page
- **Neither**: buyer pastes specs → page still gets built, social-proof block becomes a placeholder ("INSERT REVIEW HERE") with a note that reviews lift conversion 8-15% and the buyer should add even one

Always work. Always tell the buyer what was lost and how to add it.

---

## Edge cases

- **Buyer wants only the hero block** (not a full page): respect it. Output the main hero + 3 alternates only. Skip the rest of the page architecture. Note in the brief that the full-page workflow is available.
- **About page with no founder story yet**: ask the buyer 3-5 short story-prompt questions (where the brand started, what frustration sparked it, what they want their customer to feel). Use those to write the page. Don't fabricate origin stories.
- **Collection page with sparse data** (5 products or fewer): write the page but note the collection feels thin to shoppers below ~8 products. Suggest adding more SKUs or merging with a related collection.
- **Marketing LP for a regulated product** (supplements, CBD, weight loss, financial products): write claims that are platform-compliant and disclaim where required. Don't write copy that triggers ad-platform rejections.
- **Buyer asks for a "high-pressure sales LP"**: politely steer toward principled persuasion. Write copy that converts without false scarcity or fake urgency. Note that high-pressure tactics raise short-term conversion but burn trust + ad accounts.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema (mirrors skills #1 and #2)
- `templates/pdp-architecture.md` — PDP block structure
- `templates/collection-architecture.md` — collection page block structure
- `templates/marketing-lp-architecture.md` — campaign LP block structure
- `templates/about-page-architecture.md` — About / brand story page block structure
- `templates/conversion-frameworks.md` — PAS, AIDA, BAB, JTBD, FAB, PASTOR library
- `templates/hero-variations.md` — the 3-alternate-hero playbook
- `templates/html-conventions.md` — Tailwind class patterns, accessibility, image placeholders
- `scripts/config_loader.py` — shared config loader
- `scripts/keyword_cache_reader.py` — read the keywords.json shared cache from skill #2
- `scripts/render_brief_docx.py` — .docx brief renderer
- `scripts/render_html_sections.py` — Tailwind HTML renderer
- `examples/pdp-example.md` — reference PDP output
- `examples/collection-example.md` — reference collection page output
- `examples/marketing-lp-example.md` — reference marketing LP output
- `examples/about-example.md` — reference About page output
