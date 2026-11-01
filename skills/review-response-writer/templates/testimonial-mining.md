# Testimonial Mining — Extract Pull-Quotes for Downstream Skills

Every 4-5★ review processed by this skill is mined for testimonial-grade pull-quotes that downstream skills (Landing Page Copywriter, A+ Content Creator, Ad Creative Generator) can use as social proof.

The mining happens automatically as part of the bulk/single workflow. The buyer doesn't have to manage the testimonial cache directly.

## What makes a quote testimonial-grade

Five filters. A quote must pass **all five** to be added to the testimonial cache.

### Filter 1: Length
- **Minimum 8 words** — anything shorter doesn't carry enough story
- **Maximum 30 words** — anything longer doesn't fit in a landing-page testimonial slot
- Edit-down is allowed if the long version can be cleanly shortened to a pull-quote (mark the original as `truncated`)

### Filter 2: Specificity
The quote must reference at least one of:
- A specific feature ("the heat-resistant handle")
- A specific outcome ("my coffee tastes completely different")
- A specific feeling tied to use ("makes mornings feel like a ritual")
- A specific comparison ("better than the $200 one I had")

Generic praise ("love this," "great product," "5 stars") does NOT qualify.

### Filter 3: Read-aloud naturalness
The quote should read naturally aloud. Awkward fragments don't make good testimonials. Run a mental test: would a customer of the brand listen to this and feel "yes, that's what I'd say"?

### Filter 4: Attributability
The reviewer must have:
- A first name or full name (not just initials, not anonymous)
- Ideally a verified purchase
- Ideally a location or photo (more weight to localized testimonials)

### Filter 5: Sentiment safety
- Skip sycophantic / paid-looking reviews (flagged by sentiment override layer)
- Skip reviews from suspect accounts
- Skip reviews that violate platform TOS for re-use as testimonials (very rare; mostly applies to Amazon — Amazon prohibits using reviews in off-Amazon marketing if the customer hasn't consented)

## Quote extraction process

For each 4-5★ review that passes sentiment-override:

1. **Read the full review body**
2. **Identify candidate sentences** — any sentence that meets the specificity filter
3. **Score each candidate** on a 0-100 scale weighted by:
   - Specificity (40%)
   - Length within range (20%)
   - Read-aloud quality (20%)
   - Emotional resonance (20%)
4. **Pull the top 1-2 candidates** per review
5. **Format the quote** with attribution

## Quote format in cache

```json
{
  "quote": "Hearing that the grip feels balanced from the first pour is exactly what we hoped for.",
  "reviewer_first_name": "Sam",
  "reviewer_last_initial": "K",
  "reviewer_full_attribution": "Sam K., verified purchase, Brooklyn NY",
  "platform_source": "judge_me",
  "platform_review_id": "...",
  "product_identifier": "river-stone-pour-over",
  "product_name": "River Stone Pour-Over",
  "star_rating": 5,
  "review_date": "2026-05-10",
  "quote_score": 87,
  "specificity_tags": ["feature", "feeling"],
  "use_cases": ["landing_page_testimonial", "amazon_a_plus_module", "ad_creative_testimonial"],
  "do_not_amplify": false,
  "consent_note": "Standard public-review usage — verify platform TOS before using in paid ads",
  "added_at": "2026-05-22T16:30:00Z",
  "added_by": "review-response-writer"
}
```

## Use cases (consumers of the testimonial cache)

The `use_cases` array tags each testimonial with the downstream surface that should consume it:

- **`landing_page_testimonial`** — most quotes that pass all 5 filters get this tag
- **`amazon_a_plus_module`** — quotes from Amazon reviews can be reused on Amazon A+ Content (within Amazon's policies); quotes from off-Amazon sources can also be used on Amazon A+ if attribution is clear
- **`ad_creative_testimonial`** — quotes used in paid ads. **Has the strictest filters** — only verified purchases, only quotes with clear consent considerations. The Ad Creative Generator may further filter these based on platform (e.g., Meta's review-content policies)
- **`product_description`** — short, punchy quotes (8-15 words) suitable for embedding in product descriptions
- **`email_copy`** — quotes that work in email subject lines or hero sections

## Per-use-case filters

When downstream skills read the cache, they can filter by use case:

```python
# In landing-page-copywriter:
testimonials = testimonial_cache.load_for_product(product_id)
landing_quotes = [t for t in testimonials if "landing_page_testimonial" in t["use_cases"]]
```

## Quote variation per testimonial

Some reviews yield more than one quote-worthy sentence. The mining process pulls up to **2 quotes per review** if both pass all filters. The second quote gets a slightly lower score by default to indicate it's the secondary pull.

## TOS considerations per platform

| Platform | OK to use as testimonial? | Notes |
|---|---|---|
| Shopify review apps (Judge.me / Loox / Yotpo) | Yes | These reviews are explicitly intended for marketing reuse. Standard attribution. |
| Amazon | With caveats | Amazon's policy is murky on off-Amazon reuse of Amazon reviews. Best practice: don't quote Amazon reviews in paid ads outside Amazon. OK to quote them on the brand's own site with clear "Amazon verified purchase" attribution. |
| Etsy | Yes | Standard. |
| Google | Yes | Standard. |
| Trustpilot | Yes with attribution | Trustpilot's TOS explicitly allows brands to quote reviews with attribution + linking back to the Trustpilot review. |
| Facebook | Yes with attribution | Standard. |

The `consent_note` field captures any platform-specific caveat for the downstream consumer.

## When the buyer overrides

Buyers can manually mark a testimonial as "do not use" in the .xlsx bulk output (column: "Use as Testimonial?"). The cache writer respects manual overrides — quotes the buyer rejects don't flow to the cache.

Conversely, buyers can promote a quote the skill skipped by checking the column. This goes into the cache with a `manual_override: true` flag.

## Cache size management

The testimonial cache can grow large over time. The cache file at `<plugin-root>/.cache/testimonials/{product-identifier}.json` retains all entries indefinitely, but downstream skills typically request the top N (default 20) by quote_score and recency.

The cache writer auto-prunes entries marked `do_not_amplify: true` after 30 days to keep file size reasonable.

## Cross-product testimonial portability

Some testimonials are useful for multiple products (e.g., "I've tried five things from this brand and they all hit"). The cache supports a `cross_product: true` flag — those testimonials are returned by downstream skills regardless of which product they're working on.

Cross-product testimonials are detected by the skill when the review body explicitly references multiple products or the brand as a whole.

## Mining audit trail

The cache mining writes a summary to the bulk .xlsx Sheet 3 (Cache Mining Summary):

```
TESTIMONIAL MINING
  Reviews processed:                        23
  Reviews eligible for mining (4-5★ ok):    14
  Quotes extracted:                          17
  Top quote score:                           92
  Cache file:                                <plugin-root>/.cache/testimonials/river-stone-pour-over.json
```

The buyer can audit what flowed downstream before running Landing Page Copywriter or Ad Creative Generator next.
