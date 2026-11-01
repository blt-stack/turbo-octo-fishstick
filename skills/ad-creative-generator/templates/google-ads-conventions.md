# Google Ads Conventions (Search, Shopping, Performance Max)

Google Ads is fundamentally different from Meta and TikTok:

- **Intent-driven:** shoppers are searching for something specific. The ad responds to a query rather than interrupting a feed.
- **Keyword-led:** ad relevance depends on keyword match, not creative hook
- **Structured fields:** the system assembles headlines and descriptions in combinations the algorithm picks; the buyer writes the inventory, not the final assembly
- **Less visual:** Search ads are mostly text. PMax + Shopping are visual but still keyword-targeted underneath

The skill produces three Google Ads output types: Responsive Search Ads (RSA), Shopping ad titles, and Performance Max asset groups.

---

## Type 1: Responsive Search Ads (RSA)

The dominant Google Search ad format. Buyer provides up to 15 headlines + 4 descriptions; Google's algorithm tests combinations and serves the best mix per query.

### Field specs

| Field | Limit | Count |
|---|---|---|
| Headline | **30 characters** | Up to 15 |
| Description | **90 characters** | Up to 4 |
| Path 1 (display URL slug) | 15 characters | 1 |
| Path 2 (display URL slug) | 15 characters | 1 |
| Final URL | (no limit) | 1 |

### Headline writing rules

Each headline must:
- Stand alone as a complete thought (Google's algorithm shows them in different combinations, so each must work independently)
- Be specific (vague headlines lose to specific ones)
- Include the primary keyword in 3-5 of the 15 (pinned to position 1 or 2)
- Cover different angles across the 15 (don't write 15 variations of the same idea)

### Recommended headline composition for an e-commerce listing

The skill generates 15 headlines following this distribution:

- **3-5 headlines** with the primary keyword + benefit
- **3-4 headlines** with brand name + product
- **2-3 headlines** with USP / differentiator
- **2-3 headlines** with social proof (review count, press, certifications)
- **1-2 headlines** with offer (free shipping, returns, guarantee)

Example for "ceramic pour-over coffee dripper" keyword:

```
Headline 1 (28/30): Ceramic Pour Over Coffee Dripper
Headline 2 (27/30): Handmade Pour Over - One Cup
Headline 3 (24/30): Hand-Thrown in Portland
Headline 4 (26/30): Reusable Filter Included
Headline 5 (29/30): 1,247 5-Star Reviews on Etsy
Headline 6 (28/30): Free Shipping Over $50
Headline 7 (25/30): Brews One Cup in 3 Min
Headline 8 (24/30): Dishwasher Safe Pour Over
Headline 9 (27/30): No Paper Filter Ever Again
Headline 10 (28/30): Stoneware Holds Heat Longer
Headline 11 (24/30): Made by Three People
Headline 12 (29/30): The Pour Over We Make Daily
Headline 13 (28/30): 30-Day Money-Back Guarantee
Headline 14 (27/30): Single-Cup Pour Over Setup
Headline 15 (26/30): Slow Coffee, Done Right
```

Each headline includes the char count and stays under 30.

### Description writing rules

Each description (90 chars):
- Must work standalone but also pair well with any of the headlines
- Should expand on what a headline promises with a sensory or specific detail
- Always end with a soft CTA (Shop now, See more, Learn why)
- Avoid character-stuffing that reads as keyword soup

The skill generates 4 descriptions per RSA, covering different angles:

```
Description 1 (88/90): Hand-thrown ceramic pour-over with a reusable mesh filter. Brews one cup in 3 min. Shop now.
Description 2 (86/90): Made in our Portland studio. Dishwasher safe stoneware that lasts. Free shipping over $50.
Description 3 (89/90): Stop buying paper filters. Stainless mesh included with every pour-over. 30-day returns.
Description 4 (87/90): Slow-craft coffee gear for the morning when you want one good cup, not five fast ones.
```

### Path fields

Path 1 and Path 2 form the display URL suffix:
`www.brand.com/Path1/Path2`

Use these for keyword reinforcement + categorization:
- Path 1: usually the primary keyword
- Path 2: usually a benefit modifier or category

Example: `www.brand.com/Pour-Over/Handmade`

---

## Type 2: Shopping Ad Titles (Google Shopping / Free Listings)

Shopping ads pull their title and image from the product feed. The skill helps the buyer optimize the title in the feed (which they upload to Google Merchant Center).

### Title format spec

- **Max length:** 150 characters
- **Sweet spot:** 70-100 characters
- **First 70 characters are the most visible** (mobile preview cuts here)

### Title structure (Google's recommended pattern)

`[Brand] + [Product] + [Key Attribute] + [Color/Size/Material] + [Use Case/Audience]`

Example for the pour-over:

```
{{brand_name}} Ceramic Pour Over Coffee Dripper Handmade Stoneware
Single Cup Reusable Filter
(97 characters — front-loads brand + product, then attributes)
```

### What to avoid in Shopping titles

- Promotional language ("Sale", "Best Price", "Free Shipping") — Google rejects these
- ALL CAPS for emphasis — Google rejects
- Symbols / decorative characters — Google rejects
- Competitor brand names — TOS violation

### Distinct from organic listing SEO

The Listing SEO Optimizer (skill #2) writes Shopify meta titles for Google SERP organic ranking. This skill writes Shopping ad feed titles for Google Shopping ad placement. They're related but serve different surfaces:

- Skill #2's Shopify meta title: appears as the SERP organic snippet headline
- This skill's Shopping ad title: appears in the Shopping carousel and Shopping tab

When skill #2 has written a meta title to the keyword cache, this skill uses it as a starting point but may adapt for Shopping's stricter rules (no promo language, no symbols).

---

## Type 3: Performance Max (PMax) Asset Groups

Performance Max is Google's "everything campaign" — runs ads across Search, Display, YouTube, Discovery, Maps, Gmail, all from a single asset library Google's algorithm assembles. The skill produces a PMax asset group ready to upload.

### Asset group structure

A PMax asset group contains:

- **Headlines:** 3-15 (each 30 chars max)
- **Long headlines:** 1-5 (each 90 chars max)
- **Descriptions:** 2-5 (each 90 chars max)
- **Business name:** 25 chars
- **Image assets:** 1-20 images (multiple aspect ratios — see below)
- **Logo assets:** 1-5 logos
- **Video assets:** 0-5 videos (optional but recommended)
- **Audience signals:** keyword themes + remarketing lists (configured in Google Ads, not in this brief)
- **Final URLs:** 1 destination URL

### Image asset specs for PMax

PMax needs images in multiple aspect ratios so the algorithm can serve them across placements:

| Aspect ratio | Pixel size (recommended) | Where it shows |
|---|---|---|
| 1.91:1 (horizontal) | 1200×628 | Display, Gmail, Discovery |
| 1:1 (square) | 1200×1200 | Display, Discovery |
| 4:5 (portrait) | 960×1200 | Mobile-first placements |
| 9:16 (vertical) | 720×1280 | YouTube Shorts, Discover feed |

Logo specs:
- 1:1 logo: 1200×1200
- 4:1 wide logo: 1200×300

For PMax brief output, the skill specifies all four image aspect ratios. When Fal AI key is set, the skill can generate the primary 1.91:1 and 1:1 images. The other ratios are flagged as Canva briefs for the buyer to size accordingly (or to crop from the generated primary).

### PMax headlines + descriptions

Same character rules as RSA (30-char headlines, 90-char descriptions).

The skill generates PMax with a similar 15-headline / 4-description set but tuned for the broader PMax distribution (less keyword-stuffed, more general-audience friendly, since PMax serves on Display + YouTube too).

---

## Compliance: what Google rejects

### Universal across all Google ad types

- **Misrepresentation** (false or misleading product claims)
- **Competitor brand keywords in copy** (you can bid on them, but mentioning them in the copy itself is fraught)
- **Trademark violations**
- **Phone numbers in copy** (Google strips these; use call extensions instead)
- **Excessive capitalization, symbols, emoji** (Google has strict text policies)
- **Repeated punctuation** ("Sale!!!" or "Best ever...")
- **Trademark symbols (™, ®) you don't own**

### Category-specific (similar to Meta + TikTok)

- Medical / health claims for supplements / beauty
- Financial promises for financial products
- Adult content
- Gambling content (regional)
- Cryptocurrency-related advertising (regional)

The compliance check in the brief flags these per ad type.

---

## CTA conventions for Google Ads

Google doesn't have explicit CTA buttons the way Meta and TikTok do. Instead, the description's final sentence carries the CTA. Common patterns:

- "Shop now."
- "See the full collection."
- "Order today."
- "Learn more at [brand]."
- "Free shipping on orders $50+."

Avoid weak CTAs ("Click here," "Visit our site"). They underperform specific ones.

---

## Keyword integration (this is where Google Ads diverges from Meta/TikTok)

Google Ads relevance depends on keyword match. The skill heavily integrates the keyword cache from skill #2 when generating Google Ads copy.

### Where keywords go in Google Ads output

- **RSA Headline 1 (pinned position 1):** primary keyword
- **RSA Headline 2-3:** primary keyword variants + benefit
- **RSA Description 1:** primary keyword in the first 30 chars
- **Path 1:** primary keyword (sluggified — hyphens, no spaces)
- **Shopping title:** primary keyword in first 50 chars
- **PMax keyword themes:** 5-10 keyword themes from the cache (configured in Google Ads, listed in the brief)

When no keyword cache exists, the skill generates 5-10 candidate keywords from product info and uses those. Buyer can run skill #2 first for better quality.

---

## Format adjustments

### Search RSA
- Generate 15 headlines + 4 descriptions per ad
- 1 ad per archetype, so 5 ads per run = 75 headlines + 20 descriptions total

### Shopping ad title
- Single optimized title per product
- The 5-archetype model doesn't apply to Shopping titles (the title is what it is)
- For multi-product runs, the skill optimizes one title per product

### Performance Max asset group
- Single asset group per product (not per archetype)
- The 5 archetypes inform headline variety within the single asset group, not separate groups

---

## Buyer override behaviors

The skill defaults to:
- All 15 RSA headlines + 4 descriptions per archetype
- Shopping title in 70-100 char range
- PMax with all 4 image aspect ratios specified

Buyer can override:
- "Just RSA, skip Shopping and PMax" → skill produces only the Search ads
- "Use a 100-char Shopping title (longer)" → skill produces longer title
- "No PMax asset group, I'm just running Search" → skill skips PMax
