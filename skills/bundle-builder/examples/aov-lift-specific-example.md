# AOV-Lift Bundle Specific Example

Shows the AOV-Lift bundle type in detail — how the skill threads the needle between cart-abandonment psychology and margin reality.

**Brand:** {{brand_name}}
**Free-shipping threshold:** $75 (set in config)
**Current average cart value:** $58 (from sales data)
**Gap to threshold:** $17 — too small for a single product to bridge, ideal for AOV-Lift bundle

---

## The customer scenario

A customer is browsing {{brand_name}}'s site. They:
1. Click the River Stone Pour-Over ($48)
2. Add to cart
3. Cart subtotal: $48
4. See "Add $27 more for free shipping" at checkout
5. Wander around the site adding random small items to try to clear the threshold
6. Either: hit $75-80 and convert, OR abandon at $60 because they couldn't find anything attractive

The AOV-Lift bundle pre-solves this:
- "Add this $31 bundle to qualify for free shipping" — curated, easy, almost-organic

---

## The bundle the skill suggests

**Bundle name (Evocative)**: The Free-Shipping Threshold Bundle
**Bundle name (Descriptive)**: Pour-Over + Filters + Mug (Free Shipping Add-On)

**SKUs included**:
- 1 × River Stone Pour-Over (anchor) — $48
- 1 × Filter Pack (100) — $12 (15% off bundle attached)
- 1 × Studio Mug — $24

**Total individual price**: $84
**Bundle price (conservative 8% off)**: $77.30 (clears $75 free shipping)
**Savings**: $6.70

**Free shipping savings**: $8 (shipping cost the customer would otherwise pay)
**Total customer perceived savings**: $14.70 ($6.70 bundle discount + $8 free shipping)
**Customer's net spend**: $77.30 + $0 shipping = $77.30
**Without bundle**: $48 (pour-over alone) + $8 shipping = $56 (but customer might still wander/abandon)
**Brand-perceived AOV lift**: $21.30 ($77.30 vs. $56 without bundle conversion)

---

## Discovery evidence

```
Source layer: margin + apriori
Apriori support: 8.0% of orders (pour-over + filter pair is well-documented)
Apriori lift: 2.8× (strong association)
Co-occurrence count: 272 over 12 months
Margin score: 72/100
In-stock velocity score: 92/100 (all SKUs healthy)
Composite score: 76.0
AOV-Lift specific: bundle price ($77.30) is $2.30 above free shipping threshold — ideal narrow band
```

---

## Pricing tiers

- **Conservative (8% off)**: $77.30 — margin 64% — clears free shipping ✓ (recommended)
- **Standard (15% off)**: $71.40 — margin 62% — BELOW free shipping threshold ✗ (don't use)
- **Aggressive (22% off)**: $65.50 — margin 60% — BELOW threshold ✗ (don't use)

**Critical insight**: only conservative tier works for this bundle, because deeper discounts drop the bundle below the free-shipping threshold (defeating the purpose).

The skill auto-recommends conservative tier and flags the others as "below AOV target."

---

## Positioning copy

**Variant A — Benefit-led (recommended for cart page):**
> "Free shipping with one click."
>
> "The pour-over, filters, and a mug — bundled to qualify for free shipping while saving $6.70 vs. buying separately."
>
> CTA: Add Bundle, Ship Free

**Variant B — Story-led (recommended for product page upsell):**
> "Just over the line — and you save on shipping."
>
> "We built this bundle for the pour-over customer who's halfway there. Add the filters and mug, qualify for free shipping, and have what you need for the first morning's brew."
>
> CTA: Add the Bundle

**Variant C — Social-proof-led:**
> "Our customers buy these together. Now you can hit free shipping too."
>
> "The set our customers reach for together — bundled to clear $75 free shipping."
>
> CTA: See the Bundle

---

## Where the buyer deploys this bundle

The AOV-Lift bundle works in three specific surfaces:

1. **Cart page upsell**: when customer's cart subtotal is between $40-65, show this bundle as "complete your cart to ship free"
2. **Product page**: on the River Stone Pour-Over PDP, surface this bundle in the "Add to cart with..." section
3. **Abandoned cart email** (skill #7): when a cart has the pour-over and is $20-30 short of threshold, the email recommends this exact bundle

This is different from a generic discount promotion — it's surgical. The bundle only makes sense when the customer is in the abandon-zone of "almost cleared free shipping."

---

## Why this bundle works in the data

Looking at sales data:
- Cart subtotals between $45-65 abandon at 38% (vs. 22% overall abandonment)
- Cart subtotals between $75-80 abandon at 18% (free shipping converts well)
- The AOV-Lift bundle moves 30-50% of cart-abandon-zone customers into the converting zone

The skill estimates the bundle's impact:
- Existing abandons in the $45-65 zone: ~80 per month based on traffic
- Expected conversion of those carts to the AOV-Lift bundle: 20% (16 conversions/month)
- Incremental revenue: 16 × $77.30 = $1,237/month
- Cost of free shipping on those orders: 16 × $8 = $128/month
- Net margin contribution: 16 × ($77.30 × 0.64 - $0) = $792/month margin
- vs. existing baseline of those 16 carts abandoning: $0
- **Net monthly impact: ~$792/month**

---

## When AOV-Lift bundles don't work

The skill flags scenarios where AOV-Lift bundles shouldn't be deployed:

- **Threshold too far from current cart values**: if avg cart is $30 and threshold is $75, no plausible bundle can bridge the gap with 2-3 SKUs (skill recommends lowering threshold)
- **Threshold is so close to avg cart that customers self-clear**: if avg cart is $72 and threshold is $75, the AOV-Lift bundle is unnecessary (most carts already clear naturally)
- **Free shipping isn't the primary friction**: if the brand's data shows other abandonment causes (price, trust, shipping speed), AOV-Lift bundles solve the wrong problem

---

## Buyer config for AOV-Lift sensitivity

```json
"bundle_builder": {
  "free_shipping_threshold_usd": 75,
  "current_avg_cart_value_usd": 58,
  "aov_lift_target_pct_above_threshold": 0.05,
  "aov_lift_max_pct_above_threshold": 0.15
}
```

- `aov_lift_target_pct_above_threshold = 0.05`: bundle should be ~5% above threshold (e.g., $79 for $75 threshold)
- `aov_lift_max_pct_above_threshold = 0.15`: bundle should NOT exceed 15% above (e.g., not $90 for $75 threshold)

The skill enforces this band when generating AOV-Lift bundles.

---

## Bundle cache write

Written as `~/.the-ecommerce-seller/cache/bundles/pour-over-filters-mug-free-shipping-add-on.json` with:

```json
{
  "bundle_type_primary": "aov_lift",
  "bundle_type_secondary": ["fbt"],
  "tags": ["aov_lift_threshold_75", "fbt_validated"],
  "is_seasonal": false,
  ...
}
```

Skill #7 (Email Flow Architect) reads this and includes it in cart-abandonment email automation. Skill #3 (Landing Page Copywriter) reads it for the cart page upsell surface design.

---

## The lesson

AOV-Lift bundles are NOT discount-driven. They're **shipping-cost-arbitrage** bundles. The math is:
- Brand absorbs the $8 shipping cost
- Customer absorbs the $20-30 additional purchase
- Both come out ahead vs. abandonment

The skill outputs this reasoning in the .docx so the buyer understands *why* the bundle is structured the way it is — and resists the temptation to "deepen the discount" thinking that'll convert better. (It won't; it'll drop margin and not improve conversion since the customer is converting on free shipping, not discount.)
