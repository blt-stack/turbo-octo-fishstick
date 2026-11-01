# Amazon SEO (A9 / A10 algorithm)

Amazon's search algorithm (commonly called A9, with A10 referring to more recent updates) ranks listings on a combination of relevance (keyword matching), conversion rate, and account-level performance. This skill only optimizes the on-listing levers — keywords and structure. Conversion and account performance are downstream of those + outside what copy alone can fix.

## Ranking factors (in rough order of impact)

1. **Title keyword match** — single highest-weighted field.
2. **Backend search terms** — indexed but not shown to shoppers. Most under-utilized lever.
3. **Bullet keyword coverage** — bullets are indexed, also primary conversion driver.
4. **Product description / A+ Content** — indexed (A+ Content less so than plain description, paradoxically).
5. **Conversion rate** — Amazon prefers listings that convert. Driven by images, price, reviews, copy.
6. **Sales velocity** — recent units sold per day. Hard to influence with copy alone.
7. **Review count and rating** — handled by the Review Response Writer skill, not this one.
8. **Compliance** — listing violations (banned phrases, prohibited claims) suppress ranking. Audit catches these.

## What this skill optimizes

### Title — hard cap 200 chars, target 150-180 chars
- Formula: `[Brand] [Product Type] [Primary Keyword Phrase] [Secondary Keyword] [Size/Color/Quantity]`
- Brand first is required for brand-registered sellers; permissible for others.
- Front-load the primary keyword phrase in the first 5 words.
- Use natural phrasing — A10 penalizes obvious keyword stuffing.
- Avoid: ALL CAPS, special characters, decorative symbols, claims like "best" or "#1".

### Bullets — 5 bullets, hard cap 250 chars each, target 180-240 chars
- Open each bullet with a benefit headline (3-5 words, often capitalized).
- Pattern: `BENEFIT HEADLINE — Sentence explaining the feature that delivers it.`
- All 5 bullets should be used. Empty bullet slots = lost SEO + lost conversion real estate.
- No two bullets cover the same point.
- Indexing: words in bullets are searchable. Bullets should collectively cover the top 8-12 keywords without stuffing.

### Description (plain) — hard cap 2000 chars
- For sellers WITHOUT A+ Content access (no Brand Registry): this is the only long-form copy slot. Use all 2000 chars.
- For sellers WITH A+ Content: the plain description is shown rarely (A+ Content replaces it on most listings). Don't over-invest here — focus optimization on A+ Content modules.
- Plain text, line breaks allowed. No HTML.
- No CTAs ("buy now"), no external URLs, no contact info.

### Backend search terms — hard cap 250 BYTES (not characters)
**This is the highest-leverage under-utilized field on Amazon.** Most sellers leave it empty or fill it with brand name repetitions. Filling it correctly is often the single largest SEO win available.

Rules:
- Space-separated words, not phrases. Amazon tokenizes.
- No duplicates of words already in title/bullets/description (those are indexed separately).
- No competitor brand names (TOS violation).
- No subjective claims ("best", "cheapest", "amazing").
- No category names (Amazon already knows the category).
- Foreign language equivalents OK and recommended if the buyer ships internationally.
- 250 bytes is approximately 250 ASCII characters; multi-byte characters (accented, CJK) count for more bytes.

What to put in:
- Misspellings buyers commonly type ("celing fan", "wireles")
- Synonyms not used in front-end copy
- Audience modifiers ("gift", "men", "women", "kids")
- Use-case modifiers ("camping", "office", "kitchen")
- Long-tail variants compressed into single words ("paperless", "reusable")

### A+ Content (Brand Registry only)
- Indexes more weakly than plain description but converts much better.
- Modules (text + image combos) can carry keyword-rich alt text and headings.
- This skill notes A+ Content keyword coverage in the audit but defers full A+ Content creation to the A+ Content Creator skill (skill #4 in the plugin).

## Bullet quality rubric (Amazon-specific)

Each bullet scored on:
- Opens with a benefit (not a feature) — 1 pt
- 180-240 chars utilization — 1 pt
- Distinct point not covered by other bullets — 1 pt
- Includes at least one target keyword — 1 pt

Apply to all 5 bullets, sum, scale to the rubric's 20-pt allocation.

## Completeness checks (Amazon-specific)

- All 5 bullets used
- Backend search terms field has ≥200 bytes filled
- At least 7 product images uploaded (1 main + 6 secondary)
- A+ Content present (if Brand Registered)
- Product attribute fields filled (color, size, material, etc.)
- Category and sub-category correctly assigned

## Compliance flags (audit catches these)

- Title over 200 chars (auto-suppression)
- Trademark symbols not owned (TOS)
- External URLs anywhere (TOS)
- CTAs (TOS)
- Prohibited claims ("FDA approved", "miracle", "cure", etc. depending on category)
- Competitor brand mentions (TOS)

Flag these in the audit as critical issues, separate from scoring.

## Common pitfalls

- **Empty backend search terms.** Huge missed opportunity. ~60% of sellers leave this empty or use it wrong.
- **Title stuffing.** Listing reads like keyword soup. A10 penalizes — and shoppers don't click.
- **Using all 5 bullets to repeat the same benefit.** Variety wins. One bullet for materials, one for use case, one for differentiation, one for what's in the box, one for guarantee/brand.
- **Mistaking A+ Content for indexed SEO content.** A+ Content barely indexes — its value is conversion, not ranking.
- **Bullets shorter than 80 chars.** Wasted real estate.

## Rewrite output structure for Amazon

```
AMAZON — Rewrite

Title (XX/200): [...]
Bullet 1 (XX/250): BENEFIT HEADLINE — Body sentence...
Bullet 2 (XX/250): BENEFIT HEADLINE — Body sentence...
Bullet 3 (XX/250): BENEFIT HEADLINE — Body sentence...
Bullet 4 (XX/250): BENEFIT HEADLINE — Body sentence...
Bullet 5 (XX/250): BENEFIT HEADLINE — Body sentence...

Description (XX/2000): [...]

Backend search terms (XX/250 bytes):
[space-separated unique words]

Compliance check:
- [pass/fail per compliance flag]

A+ Content recommendation:
- [If Brand Registered: which modules to use and what to put in them. Defer detailed
  module creation to the A+ Content Creator skill.]
```
