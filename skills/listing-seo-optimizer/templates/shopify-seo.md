# Shopify SEO

Shopify product pages get indexed by Google, not by Shopify itself. There's no internal search algorithm to optimize for — the SEO target is Google SERP. That changes everything: keywords, metadata, schema, internal linking all matter; bullets and backend search terms don't exist as a concept.

## Ranking factors (in rough order of impact)

1. **Page title (meta title)** — what appears as the SERP headline. Most important on-page element.
2. **Meta description** — doesn't directly affect ranking, but affects click-through rate from the SERP, which Google does measure.
3. **URL handle** — Shopify lets you set this manually. Keyword-rich handles outperform `/products/12345`.
4. **Image alt text** — image search traffic is real. Also accessibility.
5. **Body copy** — keyword density and semantic relevance.
6. **Schema markup** — product schema enables Google rich snippets (price, stock, rating). Shopify themes vary in default schema quality.
7. **Internal linking** — collection pages linking to the product, product pages linking to related products. Shopify themes mostly handle this; the buyer can boost with custom collections.
8. **Page speed and mobile-friendliness** — Google Core Web Vitals. Out of scope for this skill but worth flagging if the buyer mentions a slow store.

## What this skill optimizes

### Page title (meta title) — target 50-60 chars, hard cap 60
- Formula: `[Primary keyword] | [Secondary keyword or modifier] | [Brand]`
- Example: `Ceramic Pour Over Coffee Dripper | Single Cup Handmade | [Brand]`
- Front-load the primary keyword. Brand at the end (unless the brand IS the search term).
- Avoid stop words near the front ("the", "a", "for").

### Meta description — target 150-160 chars, hard cap 160
- Doesn't affect ranking but heavily affects CTR.
- Include primary keyword (Google bolds matches in SERP).
- Include one specific benefit or differentiator.
- End with a soft CTA ("Shop now", "Order today", "Free shipping over $50" — only if true).

### URL handle
- Lowercase, hyphens, no underscores or query params.
- Include the primary keyword + the product noun.
- Keep it short: `/products/ceramic-pour-over` beats `/products/handmade-ceramic-pour-over-coffee-dripper-single-cup-reusable-filter`.
- Don't change an existing handle unless ranking is poor — changing handles breaks links and resets SEO authority unless you set up 301 redirects.

### Image alt text
- Every product image needs alt text.
- Pattern: `[Product name] — [angle/context]` e.g., "Ceramic Pour Over — front view", "Ceramic Pour Over — brewing in use"
- Primary keyword should appear in at least one image's alt text.
- Don't keyword-stuff every alt — that's a manual penalty trigger.

### Body copy
- The product description body should naturally include the primary keyword 2-4 times across the full body.
- Use semantic variations ("pour over dripper", "pour over coffee maker", "ceramic dripper") — Google understands these are related.
- Headings (H2, H3) carry SEO weight — use them for sub-topics (Materials, Care, FAQ) and include keywords where natural.

### Schema markup
Most Shopify themes auto-generate Product schema. Check whether the theme includes:
- `name`, `description`, `image`, `sku`, `brand`
- `offers` (price, availability)
- `aggregateRating` and `review` (if reviews are present)

If any are missing, recommend installing a schema app or editing the theme. Don't write schema by hand inside the audit — flag it for the buyer to address.

### Internal linking
- Recommend the buyer link from at least one collection page and 2-3 related product pages.
- Recommend at least one blog post or guide linking to the product (if the buyer publishes content).

## Bullet-equivalent for Shopify

Shopify doesn't have bullets per se, but it has a value-proposition block (usually 3-5 bullets in the body). For scoring purposes, treat these as bullets — apply the same rubric: count, benefit-led structure, differentiation.

## Completeness checks (Shopify-specific)

- Meta title present and within 50-60 chars
- Meta description present and within 150-160 chars
- URL handle is clean and keyword-rich
- All product images have alt text
- At least one alt text contains the primary keyword
- Product is in at least one collection (better discoverability via collection pages)
- Schema markup present (theme check or app check)

## Common pitfalls

- **Duplicate meta titles across products.** Shopify defaults can leave many products with `Product Name | Store Name` — fine for one product, ranking-killing for a catalog of 100. Audit cross-listing duplicates in bulk mode.
- **Auto-generated handles.** A product imported via CSV or app sometimes ends up with `/products/product-12345`. Always recommend setting a manual handle.
- **Empty alt text.** Common with bulk product imports. Big win to fix.
- **Over-optimization in meta title.** "Ceramic Pour Over Pour Over Coffee Maker Pour Over Dripper" gets penalized by Google as keyword stuffing.
- **Missing meta description.** Shopify will auto-generate one from the first 160 chars of the body, which is rarely what you'd choose. Always recommend a hand-written one.

## Rewrite output structure for Shopify

When this skill produces optimized Shopify rewrites, output:

```
SHOPIFY — Rewrite

Meta title (XX/60): [...]
Meta description (XX/160): [...]
URL handle: /products/[...]
H1 (page title — usually matches product title): [...]

Recommended alt text per image (if image URLs available):
  Image 1: [...]
  Image 2: [...]

Body keyword integration notes:
- Primary keyword appears in: H1 (×1), intro paragraph (×1), [section] heading (×1), [section] body (×1)
- Semantic variations to use: [...]

Schema markup notes:
- [What's missing or what to verify]
```
