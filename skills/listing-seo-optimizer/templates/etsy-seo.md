# Etsy SEO

Etsy's search algorithm rewards keyword-rich titles (much more aggressively than Amazon), 13 fully-utilized multi-word tags, and complete attribute coverage. Etsy also factors in shop-level metrics (recent sales, conversion, customer service) — but this skill only optimizes the listing-level levers.

## Ranking factors (in rough order of impact)

1. **Title keyword density and front-loading**
2. **Tags** (13 max, ~20 chars each) — second-highest impact
3. **Attributes** (category-specific fields like material, color, occasion)
4. **Listing description** (less weighted than Amazon's, but still indexed)
5. **Recency of listing** — fresh listings get a small boost
6. **Conversion rate** — Etsy prefers listings that convert
7. **Shop "quality score"** — sales velocity, ratings, customer service responsiveness
8. **Photos** — Etsy weights photo quality and consistency

## What this skill optimizes

### Title — hard cap 140 chars
Etsy's title strategy is different from every other platform. Etsy *rewards* listing the keyword in the title multiple ways, separated by commas, pipes, or em-dashes.

- Formula: `[Primary keyword phrase], [Secondary keyword phrase], [Audience/occasion], [Material/style modifier]`
- Example: `Handmade Ceramic Pour Over, Single Cup Coffee Dripper, Stoneware Coffee Gift, Slow Coffee Ritual`
- Front-load the highest-priority keyword.
- Use commas as separators (most common in high-ranking Etsy listings). Pipes also work. Be consistent across the shop.
- Title can repeat words across separators (different keyword phrases sharing the word "ceramic"). This is normal for Etsy.

### Tags — 13 tags, 20 chars each
**The single most under-utilized Etsy SEO field for new shops.** Multi-word tags outperform single-word tags by a wide margin.

Rules:
- Use all 13 tags. Empty slots = lost ranking opportunities.
- Multi-word tags ("rustic wedding decor", "ceramic pour over") beat single words ("rustic", "ceramic") because Etsy can match a multi-word tag to a multi-word query, but a single-word tag only matches single-word queries.
- Don't duplicate words across tags excessively — if "ceramic" is in 8 of your 13 tags, that's wasted.
- Mix tag types: product type, style, material, occasion, recipient, color, audience.
- Don't reuse exact phrases from the title — Etsy already matches the title.
- Singular vs plural matters less than people think; Etsy stems both.

### Attributes — fill every category-specific attribute Etsy offers
Etsy's category-specific attributes (material, color, occasion, recipient, style) are searchable filters in addition to ranking factors. A listing with all attributes filled appears in more filtered searches than one with attributes blank.

This is the closest Etsy gets to "backend search terms" — and it's often empty on the buyer's listings.

### Description — no character limit, but first 160 chars become the meta description
- Open with the most important keyword phrase, not "Welcome to my shop!"
- Use ALL CAPS for section headers (Etsy doesn't render markdown).
- Cover: what it is, materials, dimensions, what's included, care, shipping/processing info.
- Length: 300-800 words is the sweet spot. Longer doesn't hurt; shorter looks thin.
- Keyword integration: primary keyword appears 2-3 times in the body. Semantic variants throughout.

## Bullet-equivalent for Etsy

Etsy doesn't use bullets. For scoring purposes, evaluate the description's structure: does it use section headers, is information scannable, are specs in a clear block?

## Completeness checks (Etsy-specific)

- All 13 tags used
- All category-specific attributes filled
- Title uses ≥80% of 140 chars
- Description ≥300 words
- ≥5 product photos (Etsy allows up to 10)
- Shipping profile complete (out of scope for this skill, but worth a flag if missing)
- Production partner info filled (required for non-handmade items)

## Common pitfalls

- **Single-word tags.** "Ceramic" is a wasted tag slot. "Handmade ceramic pour over" is a winner.
- **Tags duplicating title.** If "ceramic pour over" is in the title, don't burn a tag on the exact same phrase.
- **Generic openers in description.** "Welcome to my shop! Thanks for stopping by!" — Etsy buyers click away. Open with the product or the keyword.
- **Empty attribute fields.** Especially Occasion and Recipient — these power the Etsy gift discovery flow.
- **Aggressive keyword repetition in the title.** Etsy tolerates more repetition than Amazon, but a title like "Ceramic Pour Over Ceramic Pour Over Coffee Ceramic" gets flagged.

## Rewrite output structure for Etsy

```
ETSY — Rewrite

Title (XX/140): [...]

Tags (13/13, each ≤20 chars):
1. [tag] (X/20)
2. [tag] (X/20)
...
13. [tag] (X/20)

Attributes (recommended fills for Etsy Listing Editor):
- Material: [...]
- Color: [...]
- Occasion: [...]
- Recipient: [...]
- Style: [...]
- [other category-specific attributes...]

Description: [full text, with ALL CAPS section headers]

Meta description (first 160 chars — verify this reads cleanly): [...]

Keyword integration notes:
- Primary keyword in title (×2), description body (×2)
- Semantic variants used: [...]
```
