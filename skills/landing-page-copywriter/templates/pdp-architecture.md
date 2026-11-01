# PDP (Product Detail Page) Architecture

A high-converting product page is more than a description with photos. It's a sequence of blocks that move a shopper from arrival to purchase, addressing objections in the order they form. This template specifies the block order, length targets, conversion job per block, and pitfalls.

Treat the order as the default. The chosen conversion framework (PAS, AIDA, BAB, JTBD, FAB) determines *how* copy flows through the blocks, not whether the blocks exist.

---

## Block sequence (top to bottom)

1. **Sticky announcement bar** (optional, only for active promos)
2. **Hero** — image + headline + sub-headline + CTA + trust signals
3. **Value propositions** (3-5 benefits with icons)
4. **Story / "Why we made this"** (founder voice, narrative)
5. **Detailed product walkthrough** (features + photos + diagrams)
6. **How it works** (3-4 steps with images, only for products that need explanation)
7. **Comparison table** (vs alternatives, only when competitive frame helps)
8. **Social proof** (reviews block, press logos, customer photos)
9. **FAQ** (5-8 questions addressing the most common objections)
10. **Sticky CTA / final purchase block**
11. **Cross-sell / "you might also like"**
12. **Trust footer** (returns, shipping, security badges)

Skip blocks that don't earn their place (e.g., "How it works" for a t-shirt). Don't add blocks for completeness — every block has to do conversion work.

---

## Block 1: Sticky announcement bar (optional)

**When to include:** active promo, free-shipping threshold, holiday deadline, low-stock signal.
**Length:** under 60 characters.
**Format:** single line, link to relevant policy or product.

Example: `Free shipping on orders $50+ · Order by Dec 18 for Christmas`

**Pitfall:** leaving the announcement bar up when the promo has ended kills trust immediately.

---

## Block 2: Hero

The most important block on the page. Six elements:

- **Headline** — primary value proposition, 6-12 words
- **Sub-headline** — supports the headline, 12-20 words, names who it's for and what specifically it does
- **Primary product image** — recommended 1200×1200px square, on background that matches brand voice
- **CTA button** — verb-led, 2-4 words ("Shop the [product]", "Try it free", "Get yours")
- **Price** — visible above the fold
- **Trust signals** — 2-4 small badges: star rating + review count, free shipping, money-back guarantee, press mentions

**Length targets:**
- Headline: 6-12 words (under 60 chars)
- Sub-headline: 12-20 words (under 120 chars)

**Conversion job:** in 3 seconds, the shopper knows what this is, who it's for, and whether to keep scrolling. If the hero fails, nothing else matters.

This skill generates 3 alternate heroes (problem-aware, outcome-aware, social-proof-aware) — see `hero-variations.md`.

---

## Block 3: Value propositions

3-5 benefit bullets, icon-led, visible immediately after the hero.

**Format per bullet:**
- Icon (line icon, 40px, matches brand color)
- Benefit headline (3-5 words, sentence case)
- Supporting sentence (12-20 words)

**Example:**

> ⚡ **All-day comfort**
> Memory-foam insole molds to your foot within the first week — no break-in period.

**Conversion job:** the shopper who skims (most of them) needs to see why this product matters in 5 seconds.

**Pitfalls:**
- Listing features instead of benefits ("100% cotton" → benefit-version: "Breathable enough for August humidity")
- Generic claims ("high quality", "premium materials") — replace with specifics
- More than 5 bullets — picks become harder, attention drops

---

## Block 4: Story / "Why we made this"

Narrative prose. 100-200 words. Founder voice when possible.

**Structure:**
- Opening: the moment the buyer realized this product needed to exist (or, for non-founder brands, the customer-facing version)
- Middle: what they tried, what didn't work, what shaped the final product
- Close: why this matters now

**Conversion job:** trust and differentiation. The shopper learns this product was made by humans who care, not stamped out by a factory. This is where the brand stops being interchangeable.

**Pitfalls:**
- Saccharine ("we love what we do") — show, don't tell
- Mission-statement language ("our mission is to...") — narrate, don't proclaim
- Missing entirely on stores that have a real story to tell — leaving conversion on the table

---

## Block 5: Detailed product walkthrough

Features + photos. 4-8 elements depending on product complexity.

**Format per element:**
- Photo or diagram (recommended 800×600px)
- Feature name (3-5 words)
- Description (20-40 words)

**Conversion job:** the shopper who's interested but uncertain gets the specifics they need.

For physical products: materials, dimensions, what's in the box, how it's made.
For variant-heavy products: variant axes explained (size guide, color guide).

**Pitfalls:**
- Stock photos instead of real product photos — kills trust
- Specs walls (15+ features in a row) — break into 2-3 groups with subheads

---

## Block 6: How it works (conditional — only for products that need explanation)

3-4 steps with images. Each step has a number, a verb-led title, and 1-2 sentence explanation.

**Include this block when:** the product is unfamiliar, technical, has a non-obvious use, or requires setup.

**Skip when:** the product is self-evident (a t-shirt, a coffee mug).

**Pitfall:** treating obvious products as if they need explanation — wastes the shopper's time and signals you don't understand them.

---

## Block 7: Comparison table (conditional)

Vs alternatives. 3-6 columns (your product vs 2-5 competitors or category alternatives).

**Include when:**
- The buyer is competing against a well-known incumbent
- The product is in a feature-comparison category (mattresses, knives, supplements, software)

**Skip when:**
- The category isn't about specs (apparel, art, gifts)
- The buyer doesn't have meaningfully different specs from competitors (just makes the buyer look defensive)

**Format:** columns are brands, rows are features. Use ✓/✗ or short text per cell. Highlight the buyer's column with brand color.

**Pitfall:** making the comparison too one-sided looks dishonest. Show one or two areas where a competitor wins, then own why the buyer's overall package is still better.

---

## Block 8: Social proof

The block that closes the most deals. Three elements, in order:

- **Aggregate rating** — star count + review count + link to all reviews (e.g., "4.8 stars · 1,247 reviews")
- **Featured reviews** — 3 reviews, each with reviewer name, star rating, review headline, 2-3 sentence body, and ideally a photo
- **UGC / customer photos** — 4-8 customer photos in a grid, ideally pulled from Instagram or review widget

**Selection criteria for featured reviews:**
- One that confirms the primary benefit
- One that addresses the most common objection
- One that mentions an unexpected use case or surprise delight

**Pitfalls:**
- Cherry-picking only 5-star reviews when the product has mixed reviews — shoppers notice
- Showing only the rating, no actual review text — shoppers don't trust unverified numbers
- Stock photos labeled as "customer photos" — instant trust failure

---

## Block 9: FAQ

5-8 questions. Real objections, in the buyer's brand voice.

**Selection criteria:**
- Pick from the most common questions the buyer actually gets (from customer service tickets, reviews, comments)
- Cover the top 3-4 objections explicitly (sizing, shipping, returns, materials, fit, comparison to alternatives, "is this right for me")
- Include at least one fun or unexpected question — humanizes the page

**Format:** expandable accordions (Tailwind has `<details>` patterns). Question is brief (5-10 words); answer is 1-3 sentences.

**Pitfall:** generic FAQ ("Is this a quality product?") that no real shopper would ask — flag of weak FAQ. Replace with real questions from real customers.

---

## Block 10: Sticky CTA / final purchase block

The shopper has scrolled to the bottom and not bought yet. They need one more confident push.

**Elements:**
- Product image (different angle from the hero — typically lifestyle or in-use)
- Headline (different from the hero — typically value-summary like "Built for the long haul" or outcome-restated)
- 2-3 line summary
- Big CTA button + price
- Final trust signal (e.g., "30-day money-back guarantee · Free shipping")

**Pitfall:** repeating the hero verbatim — shows you ran out of things to say. The closer should *summarize* the page argument, not restart it.

---

## Block 11: Cross-sell / "You might also like"

3-4 related products with thumbnail, name, price, and quick "Add to cart" or "View."

**Selection criteria:**
- Frequently bought together (data-driven if Shopify analytics available)
- Manually curated cross-sells from the buyer
- Same collection (fallback)

**Pitfall:** showing too many cross-sells (>4) splits attention; just one tasteful row works better.

---

## Block 12: Trust footer

Compact strip: returns policy, shipping info, payment badges, security badges.

**Elements:**
- Returns policy (1 line: "30-day returns, no questions")
- Shipping policy (1 line: "Ships within 2 business days from [location]")
- Payment badges (Visa, MasterCard, AmEx, PayPal, Shop Pay, Apple Pay)
- Security badge (SSL, McAfee, or platform-issued)

**Conversion job:** the shopper looking for any reason to bail finds reassurance instead.

---

## Length targets (whole page)

- Total word count: 800-1500 words depending on price point
- Lower-ticket (<$30): 500-800 words
- Mid-ticket ($30-150): 800-1300 words
- Higher-ticket ($150+): 1300-2500 words (more objection-handling needed)

The skill should aim for the middle of the range unless the product price clearly signals otherwise.

## Mobile-first reminder

70%+ of e-commerce traffic is mobile. Every block needs to work on a 375px-wide screen:
- Single-column layouts for everything except the hero
- Buttons 44×44px minimum tappable area
- Comparison tables convert to vertical stacks on mobile
- Reviews show one at a time on mobile (carousel)

The HTML output uses Tailwind's responsive prefixes (`md:`, `lg:`) — see `html-conventions.md`.
