# Listing Audit Rubric — 0 to 100

Every listing is scored per platform on five weighted dimensions. The total is the sum of sub-scores. Same rubric for every platform; the *checks* inside each dimension are platform-specific because what makes a strong Amazon title is different from what makes a strong Etsy title.

## Why these weights

Keyword coverage is weighted highest (30%) because it's the single biggest determinant of whether the listing is even *eligible* to rank for the buyer's target searches. Title and bullets are next because they're what shoppers see first and the algorithm reads most aggressively. Backend/structured fields and completeness round out the score — they're often the lowest-hanging fruit because most sellers neglect them.

## Total = 100 points

| Dimension | Weight | What it measures |
|---|---|---|
| Keyword coverage | 30 | How well the title + body cover the top-ranked target keywords |
| Title strength | 20 | Length utilization, front-loading, structural quality |
| Bullet quality | 20 | Number used, benefit-led structure, character utilization |
| Backend / structured fields | 15 | Backend search terms, attributes, tags filled and unique |
| Completeness | 15 | Meta description, alt text, URL handle, schema fields |

---

## Dimension 1: Keyword coverage (30 points)

Inputs: the ranked keyword list from the research step (typically 15-25 keywords), the existing listing fields.

Sub-points:

- **15 pts** — Top 5 keywords coverage. Count how many of the top 5 keywords appear in title + body. Award 3 pts per top-5 keyword present.
- **10 pts** — Top 6-15 keywords coverage. Count how many of keywords 6-15 appear anywhere in the listing. Award 1 pt per keyword present.
- **5 pts** — No stuffing. Subtract 1 pt for every keyword repeated more than 3 times in title + body. Cap subtraction at -5.

A listing covering all top-5 keywords + 10 of keywords 6-15 + no stuffing scores 30/30.

---

## Dimension 2: Title strength (20 points)

Each platform has a target character length and a preferred structural pattern. Score against the platform's target.

Generic checks (apply to every platform unless overridden):

- **6 pts** — Length utilization. Award based on how close the title is to the platform's recommended sweet spot (not the hard cap — the sweet spot, which is shorter).
  - At or above 80% of sweet spot: 6/6
  - 60-79%: 4/6
  - 40-59%: 2/6
  - Below 40%: 0/6
  - Over 100% of hard cap: 0/6 AND flag as critical issue
- **6 pts** — Front-loading. Top-priority keyword in the first 5 words of the title: 6/6. Within the first 10 words: 4/6. Anywhere in the title: 2/6. Missing: 0/6.
- **4 pts** — Brand placement matches platform convention. Amazon: brand first. Shopify: brand optional in title (often in store branding). Etsy: brand at end or omitted. eBay: brand early. Walmart: brand first.
- **4 pts** — No spammy patterns. Subtract 1 pt for each: ALL CAPS for emphasis, excessive punctuation, "L@@K", "BEST", "AMAZING", trademark symbols not owned by the seller, emoji where category prohibits.

Platform-specific overrides are in each `*-seo.md` template.

---

## Dimension 3: Bullet quality (20 points)

Bullets only meaningfully exist on Amazon, Walmart, and some Etsy categories. For platforms without bullets (Shopify long-form descriptions, eBay, TikTok Shop), this dimension is rescaled to evaluate the equivalent structural element (e.g., Shopify value-prop section, eBay item specifics).

Generic checks for bullet-having platforms:

- **6 pts** — Bullet count. Used the full count the platform allows? Amazon = 5 bullets, Walmart = up to 10. Award proportional to count used vs allowed (5/5 on Amazon = 6/6; 3/5 = ~3.6/6).
- **6 pts** — Benefit-led structure. Each bullet opens with a benefit (outcome) before the feature. Count compliant bullets ÷ total bullets × 6.
- **4 pts** — Character utilization. Each bullet hits at least 70% of its character limit. Count compliant bullets ÷ total bullets × 4. (Too-short bullets waste real estate; too-long bullets get truncated.)
- **4 pts** — Differentiation. Each bullet covers a distinct point — no redundancy. Subtract 1 pt for each pair of bullets covering the same point.

For non-bullet platforms, use the equivalent rescaled checks documented in each `*-seo.md` template.

---

## Dimension 4: Backend / structured fields (15 points)

This is the most under-utilized SEO surface for most sellers. It's also the easiest to fix.

Generic checks (with platform-specific overrides):

- **6 pts** — Field utilization. The platform offers backend fields (Amazon search terms, Etsy tags + attributes, Walmart attributes). Award proportional to how many are filled vs available.
- **5 pts** — No duplication with front-end fields. Backend search terms shouldn't repeat words already in the title/bullets — that wastes space. Award 5 if there's <10% overlap; subtract 1 pt per 10% overlap above that.
- **4 pts** — Uniqueness across the catalog (only checked in bulk mode). When auditing many listings, products in the same category shouldn't share identical backend terms — that's wasted optimization. Award based on uniqueness ratio in the cohort.

---

## Dimension 5: Completeness (15 points)

Things that aren't sexy but matter.

- **4 pts** — Meta description present (Shopify, Google SERP), within character limit. Skip for platforms without one.
- **3 pts** — All images have alt text (Shopify). Alt text contains a relevant keyword. Skip for platforms that handle this automatically.
- **3 pts** — URL handle is clean: lowercase, hyphens, includes primary keyword, no auto-generated junk like `product-12345`. Shopify-relevant.
- **3 pts** — Schema markup populated where applicable (Shopify — product schema for Google rich snippets). Skip for marketplaces that handle schema automatically.
- **2 pts** — Category and attributes correctly assigned. Wrong category = wrong audience seeing the listing.

For Amazon/Etsy/eBay/Walmart/TikTok Shop, the 4 + 3 + 3 = 10 pts for meta/alt/handle/schema are rescaled into "platform-specific completeness" — typically attribute completion (Walmart Listing Quality Score, eBay item specifics filled, Etsy attributes filled, TikTok product attributes filled).

---

## Score interpretation

| Score | Meaning | Recommended action |
|---|---|---|
| 90-100 | Excellent | Maintain. Focus optimization effort on other listings. |
| 75-89 | Strong | One or two specific fixes get this to 90+. |
| 60-74 | Mediocre | Multiple dimensions need work. Apply the rewrites. |
| 40-59 | Weak | Most of the listing needs to be rewritten. Big lift available. |
| 0-39 | Poor | Treat as greenfield. Don't try to incrementally fix — start over with the rewrite output. |

## Worked example

A hypothetical Amazon listing for "River Stone Ceramic Pour-Over":

- Keyword coverage: top 5 keywords have 4 present (12 pts), keywords 6-15 have 7 present (7 pts), no stuffing (5/5) → **24/30**
- Title strength: title is 142/200 chars (sweet spot 150-180 → 4/6), primary keyword in word 3 (6/6), brand first (4/4), no spammy patterns (4/4) → **18/20**
- Bullet quality: 5/5 bullets used (6/6), 4 of 5 benefit-led (4.8/6), 4 of 5 hit 70%+ characters (3.2/4), all differentiated (4/4) → **18/20**
- Backend: Amazon backend search terms field is empty (0/6), N/A (5/5 by default), N/A (4/4 by default) → **9/15**
- Completeness: A+ Content not used (Amazon's equivalent), category correct → **7/15**

**Total: 76/100** — Strong, but the empty backend search terms field is leaving 6 easy points on the table. Action: write 200+ bytes of unique, non-overlapping keywords into backend search terms.

That kind of specific, evidence-based audit is what the buyer needs out of every run.
