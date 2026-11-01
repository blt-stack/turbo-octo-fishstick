# Objection Mining — Extract Pain Points for Downstream Skills

Every 1-2★ review processed by this skill is mined for the underlying *objection* the customer felt. Downstream skills (Ad Creative Generator, Landing Page Copywriter, Product Description Writer) use the objection cache to write copy that **proactively addresses concerns** future customers might have.

A 1★ review about "took 3 weeks to ship" isn't just a shipping complaint — it's the surfaced version of the objection "this brand's shipping is unreliable." If 10 future customers have that doubt before they buy, addressing it explicitly in the listing or ad converts.

## What makes a complaint mine-able as an objection

Three filters. A complaint must pass all three to enter the objection cache.

### Filter 1: Sentiment safety
- Skip abusive reviews (the underlying complaint is often valid but contaminated by tone)
- Skip fake/competitor reviews (no real signal)
- Skip reviews where the customer is clearly misusing the product or misunderstanding the category — those aren't objections, they're outliers

### Filter 2: Generalizability
The complaint must be the kind a *new shopper* could have:
- "Smaller than I expected" → ✅ generalizable (new shoppers wonder about size all the time)
- "My specific use case at my specific home didn't work" → ❌ not generalizable

A good objection is the customer's surface complaint *translated into a doubt the next shopper would have before buying*.

### Filter 3: Frequency tracking
A single 1★ complaint is anecdote. Three 1★ complaints saying similar things is a pattern. The cache stores all eligible complaints, and downstream skills can filter by frequency to surface patterns.

## Objection extraction process

For each 1-2★ review that passes sentiment-override:

1. **Read the review body**
2. **Identify the customer's surface complaint** ("took 3 weeks to ship," "smaller than expected," "felt cheap")
3. **Translate the complaint into the underlying objection** — the belief the customer formed:
   - "took 3 weeks to ship" → "shipping is unreliable"
   - "smaller than expected" → "listing photos don't reflect real-life scale"
   - "felt cheap" → "doesn't match the premium price point"
4. **Categorize by issue category** — shipping, quality, sizing, expectation mismatch, value, customer service, other
5. **Write to cache**

## Objection format in cache

```json
{
  "objection": "Shipping is unreliable",
  "surface_complaint": "Took 3 weeks to arrive with no updates",
  "issue_category": "shipping",
  "specific_failure_mode": "carrier delay no proactive comms",
  "platform_source": "trustpilot",
  "platform_review_id": "...",
  "product_identifier": "river-stone-pour-over",
  "product_name": "River Stone Pour-Over",
  "reviewer_first_name": "Marcus",
  "star_rating": 1,
  "review_date": "2026-05-15",
  "objection_strength": 88,
  "frequency_tag": "novel",
  "do_not_mine": false,
  "downstream_handling_suggestions": {
    "ad_creative": "Address shipping speed and tracking proactively in pre-purchase ads. Mention specific carrier + tracking experience.",
    "landing_page_faq": "Add FAQ: 'How long does shipping take?' with realistic ranges + what happens if delayed",
    "product_description": "Include a shipping expectation line in the listing's shipping section"
  },
  "added_at": "2026-05-22T16:30:00Z",
  "added_by": "review-response-writer"
}
```

## Frequency tagging

When the same objection appears multiple times in the cache, the writer tags subsequent entries:

- **`novel`** — first time this objection appears in the cache
- **`emerging`** — 2-3 entries with the same objection
- **`systemic`** — 4+ entries with the same objection (flagged for the buyer to address operationally, not just in copy)

The Ad Creative Generator and Landing Page Copywriter prioritize `emerging` and `systemic` objections in their copy.

## Objection categories

Common objections by issue category:

### Shipping
- "Shipping is unreliable"
- "No tracking visibility"
- "Took longer than the listing promised"
- "Damaged in transit"

### Product quality
- "Doesn't match the premium price point"
- "Quality varies between units" (suggests batch issue)
- "Breaks after [time period]"
- "Material feels [cheap/light/flimsy]"

### Sizing / fit
- "Sizing photos don't reflect real-life scale"
- "Listing doesn't say how to choose between sizes"
- "Sizing inconsistent between products in the line"

### Expectation mismatch
- "Listing photos don't match the real product (color, finish)"
- "Looks smaller / larger in person"
- "Doesn't do what I thought it would do"
- "Listing oversold the [feature]"

### Customer service
- "CS unreachable when problems happen"
- "Returns process is painful"
- "Refund timing is too long"

### Value / pricing
- "Doesn't justify the price"
- "Hidden fees / shipping costs at checkout"
- "Better deals available elsewhere"

### Other
- Anything not fitting above categories

## Downstream handling suggestions

Each objection comes with downstream handling suggestions for the downstream skills. These aren't authoritative — the downstream skill decides how to handle — but they provide a starting point.

### Ad Creative Generator handling

The Ad Creative Generator can use the objection cache in two modes:
1. **Direct objection handling** — write ad copy that names and addresses the objection
2. **Indirect reframe** — write ad copy that emphasizes the OPPOSITE of the objection

Example for "shipping is unreliable":
- Direct: "We ship within 24 hours. UPS tracking from the moment it leaves our warehouse. No mystery weeks."
- Indirect: "Free 2-day shipping on every order over $40. Real-time tracking. Show up exactly when we said we would."

### Landing Page Copywriter handling

The Landing Page Copywriter typically uses the objection cache in:
1. **FAQ section** — turn the top 3-5 systemic objections into FAQ entries that address them head-on
2. **Above-the-fold reassurance** — for shipping/sizing objections, add brief reassurance in the hero (e.g., "Free shipping under 5 days")
3. **Below-the-fold trust marks** — surface specific commitments (return policy, shipping guarantee) tied to objection categories

### Product Description Writer handling

For listings where the same objection appears 3+ times, the description writer:
1. Adds a proactive callout in the spec/feature section
2. Updates the "what to expect" framing
3. Adjusts sizing/feature language to set realistic expectations

## When the buyer overrides

Buyers can mark objections in the .xlsx bulk output as:
- **Real** — leave in cache as-is
- **Misuse** — customer was using the product wrong; objection doesn't generalize → remove from cache
- **Outlier** — one-off, not a real pattern → remove from cache
- **Operational** — not a copy issue; an actual operations issue to fix → tag, leave in cache, flag for operational review

The cache writer respects these overrides.

## Mining audit trail

The cache mining writes a summary to the bulk .xlsx Sheet 3:

```
OBJECTION MINING
  Reviews processed:                        23
  Reviews eligible for mining (1-2★ ok):     4
  Objections extracted:                      4
  Novel objections (new patterns):           2
  Emerging objections (2-3 prior):           1
  Systemic objections (4+):                  1 ← "Shipping reliability via UPS Memphis"
  Cache file:                                ~/.the-ecommerce-seller/cache/objections/river-stone-pour-over.json
```

The systemic objection in this example surfaces in Sheet 4 (Systemic Issues) too — it's both a copy concern and an operational concern.
