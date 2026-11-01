# Single 5★ Amplify — Reference Example

Shows what gets produced when the buyer pastes a single 5★ review and asks for a reply — plus what flows into the testimonial cache.

**Brand:** {{brand_name}}
**Platform:** Judge.me (Shopify review app)
**Star rating:** 5★
**Tier:** Amplify
**Sentiment:** Constructive (genuine, specific praise — not sycophantic)
**Output:** Single `.docx` + testimonial cache write

---

## Input (what the buyer pasted)

```
Platform: Judge.me
Reviewer: Sam K.
Rating: 5 stars
Title: Beautiful piece — made by a person
Body: I've had a lot of mugs in my life. This one feels like it was made by a person. The weight, the way the handle sits in your hand, the slight irregularities in the glaze — it's the kind of object that makes you slow down. I bought it for myself but I'm already eyeing one for a wedding gift in October.
Verified purchase: Yes
Date: 2026-05-19
```

---

## Detection

- **Tier:** Amplify (5★)
- **Sentiment:** Constructive (specific, sensory praise — not generic, not sycophantic)
- **Issue category:** N/A (amplify tier)
- **Testimonial mining:** 1-2 candidates pass all filters
- **Cross-product portability:** Note — Sam mentioned a future wedding gift purchase, useful as a referral seed

---

## .docx output structure

```
Reply to: Sam K.  ·  5★  ·  Judge.me
Posted 2026-05-19  ·  River Stone Pour-Over Mug  ·  verified purchase
Tier: Amplify (4-5★)
Sentiment: constructive
```

### ORIGINAL REVIEW (for reference)

[Beautiful piece — made by a person]

[Full review body, in 55% grey]

### DRAFTED PUBLIC REPLY

```
Hi Sam,

"Made by a person" — that's the highest compliment we could ask for. Pieces like this one were thrown by Maya in our Brooklyn studio.

If the wedding gift moment comes around, we'd be honored to help pick the right piece.

— Jamie
```

Character count: 218 (limit: 5000)

### DRAFTED PRIVATE FOLLOW-UP

(None — amplify tier doesn't typically warrant a private follow-up unless the customer is high-LTV and a relationship warrants it. The skill flagged this for "optional founder DM" but didn't draft one by default. The buyer can request one if desired.)

### CACHE WRITES

- **Testimonials extracted: 2**
  - **Primary quote (score 92):** "This one feels like it was made by a person. The weight, the way the handle sits in your hand, the slight irregularities in the glaze — it's the kind of object that makes you slow down."
    - Tagged for: landing_page_testimonial, amazon_a_plus_module, ad_creative_testimonial
    - Attribution: Sam K., verified purchase
    - Specificity tags: feature, feeling, sensory
  - **Secondary quote (score 78):** "I've had a lot of mugs in my life. This one feels like it was made by a person."
    - Tagged for: landing_page_testimonial, product_description
    - Attribution: Sam K., verified purchase
    - Specificity tags: comparison, feeling
- Objections extracted: 0 (5★ — none expected)
- Keyword phrases enriched: 1
  - "made by a person" (occurrence 1; not yet at the 3-occurrence promotion threshold but logged)
- Testimonial cache: `~/.the-ecommerce-seller/cache/testimonials/river-stone-pour-over-mug.json`

---

## What the buyer does next

1. **Post the public reply** to Judge.me
2. **The testimonial cache is updated automatically** — the next time the buyer runs:
   - Landing Page Copywriter on this product, Sam's quote will appear as a candidate testimonial
   - A+ Content Creator, the quote is available for the social-proof module
   - Ad Creative Generator, the quote is available for the testimonial-format ad
3. **No further action needed for this review.** Restraint is the point of amplify replies.

---

## Why this reply works

- **Specific reflection** — "Made by a person" is Sam's exact phrase, called back to him verbatim. Proves the reply isn't a form letter.
- **Brand value reinforcement in one line** — "Thrown by Maya in our Brooklyn studio" connects Sam's experience to the brand's craft archetype without lecturing.
- **Soft seed, not a hard sell** — "If the wedding gift moment comes around" responds to Sam's own mention of a future purchase. It's not pushy because Sam brought it up first.
- **Sign with founder first name** — short reply, founder-signed signals the brand reads every review.
- **Length restraint** — 38 words. Future readers see this as a confident brand.
- **No discount code** — never on amplify replies. Cheapens the moment.

---

## Why the cache writes matter (the compounding value)

A 5★ review like this one is worth far more than the reply itself. The downstream uses:

- **Landing page hero testimonial** — "Made by a person" — Sam K., Brooklyn — verified purchase
- **Amazon A+ Content social proof module** — image of the mug + Sam's quote
- **Meta ad creative variant** — testimonial-style image ad with the quote as the headline
- **Email subject line for the brand's nurture flow** — "What a customer just said about our mugs..."
- **Product description body** — "This one feels like it was made by a person" — verified review

By the time the brand has 50+ reviews, the testimonial cache becomes a curated asset library that the rest of the plugin draws from automatically. No more "we need a testimonial for the landing page — where did that great quote come from again?"

---

## Time savings

Manually:
- Read review, draft a thoughtful reply: ~5 min
- Remember to save the quote somewhere for marketing: ~rarely happens
- **Total: ~5 min, with the marketing quote lost to time**

With this skill:
- Skill runs: ~20 seconds
- Buyer posts the reply: ~30 seconds
- **Total: ~1 min, with the quote permanently captured in the testimonial cache for downstream use**

The real ROI isn't the reply time; it's the asset library that builds over months without manual effort.
