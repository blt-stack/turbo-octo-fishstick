# Bundle Type: AOV-Lift Bundle

Bundles specifically designed to push average order value above a target threshold. Most commonly used to qualify carts for free shipping (the buyer-set free-shipping threshold), but also useful for hitting promotional tier thresholds (BOGO eligibility, gift-with-purchase qualification).

## Source layer

Margin optimization + Apriori. See `margin-optimization.md` and `apriori-discovery.md`.

## The AOV-lift math

```
target_threshold:       buyer-configured (e.g., $75 for free shipping)
current_avg_cart_value: from sales data
gap_to_target:          target_threshold - current_avg_cart_value
```

For each AOV-Lift bundle candidate, the skill checks:
- Bundle price ≥ target_threshold (clears the bar)
- Bundle price ≤ target_threshold + 25% (not too far over; bundle should be "just enough")
- Bundle includes at least one SKU that's commonly added near checkout (small accessory, consumable)

## Why "just enough" matters

If the free-shipping threshold is $75 and the bundle is $200, customers don't see "free shipping bundle" — they see "expensive bundle." The bundle should feel like a near-organic decision: "I was going to spend $65 anyway; for $79 I get the bundle AND free shipping."

The skill prefers bundles in the range `[threshold, threshold × 1.15]` and flags bundles outside this range.

## Filter thresholds

An AOV-Lift bundle qualifies when:
- Bundle price clears the target threshold
- At least one SKU in the bundle is a frequent low-cart-add (skill #12's velocity data favors low-priced SKUs with high velocity — these are "add-on" candidates)
- Blended margin remains above floor (no incinerating margin to hit free shipping)
- Composite includes 1 hero SKU + 1-2 attachable add-ons

## Bundle structure

AOV-Lift bundles are typically:
- 1 hero SKU (the customer's primary purchase)
- 1-2 attachable add-ons that lift the cart above threshold

The hero SKU is what the customer wanted anyway. The add-ons are the AOV-lift mechanism.

## Pricing strategy

AOV-Lift bundles usually use **Conservative tier (5-10% off)**. The bundle's value isn't the discount — it's:
- Hitting the free-shipping threshold (saves $5-15 in shipping fees the customer would otherwise pay)
- Slight bundle discount on top

A typical AOV-Lift bundle structure:
- Hero SKU @ full price: $58
- Add-on @ 50% off (introductory): $7
- Add-on @ full price: $14
- Bundle total: $79 (clears $75 free shipping)

The "discount" framing is on the add-on, not the hero. Customer perceives the deal as "I got a cheap add-on AND free shipping" — which converts better than "$79 bundle saves $X."

## Positioning angle

AOV-Lift bundles position as **practical**:
> "Add this to qualify for free shipping"
> "Bundle this trio and ship free"
> "Just over the line — and you save on shipping"

The free-shipping mention is non-optional. If the bundle doesn't unlock free shipping, position differently (use Standard tier discount language).

## Why these bundles work

Free shipping is the single most-leveraged offer in e-commerce. ~50-70% of cart abandonment cites shipping cost. An AOV-Lift bundle:
1. **Solves the abandonment trigger** — converts a $65 cart that would abandon at the $10 shipping cost into a $79 cart with free shipping
2. **Increases brand profit** — customer was leaving anyway; the bundle's marginal cost is small vs. the lost-cart cost
3. **Customer-perceived win** — the buyer thinks they "outsmarted" shipping, even though the brand priced it that way deliberately

The math typically works in the brand's favor:
- Avoided lost order: full margin on $58 hero
- New AOV: $79
- Cost of free shipping: $8
- Net margin lift: significant

## Example AOV-Lift bundles

### Free Shipping at $75 — Coffee buyer

```
Hero: River Stone Pour-Over     $48
Add-on: Filter Pack (100)       $12  (10% off bundle)
Add-on: Spoon                   $14

Bundle total: $74  (just under)
Bundle bumped: $79 with conservative 5% discount

— Clears $75 free-shipping threshold
— Customer pays $79 + free shipping (vs. $74 + $8 shipping = $82 without bundle)
— Brand collects extra $5 + shipping cost saved
```

### Free Shipping at $50 — Skincare buyer

```
Hero: Vitamin C Serum           $42
Add-on: Travel-size Moisturizer $9  (15% off — discontinuing sample size)
Add-on: Cotton pads (50)        $6

Bundle: $54  (clears $50 free shipping)
```

### Free Shipping at $100 — Premium buyer

```
Hero: Premium Cashmere Sweater  $95
Add-on: Wool Wash               $12
Add-on: Cedar Hanger Pack       $9

Bundle: $107  (clears $100)
```

## AOV-Lift vs. spend-and-save promos

AOV-Lift bundles are different from "$10 off $75" promos:

| AOV-Lift Bundle | Spend-and-save promo |
|---|---|
| Targeted at near-threshold carts | Applied to any cart over threshold |
| Curated SKU set | Customer picks anything |
| Permanent fixture | Time-limited |
| Drives accessory attachment | Drives free SKU rotation |

Both have their place. The skill recommends AOV-Lift bundles as permanent fixtures + spend-and-save as periodic promotions.

## When AOV-Lift bundles fail

- **Bundle price too far over threshold**: feels like a manufactured upsell, not a natural lift
- **Hero SKU has no natural add-on**: customer wonders why you're packaging unrelated items
- **Threshold is wrong for the customer**: a $30 average cart can't be lifted to $75 via bundle; bundle should be calibrated to ~30% above current avg
- **No free-shipping framing**: the bundle exists but the value isn't connected to shipping qualification

## Buyer config

```json
"bundle_builder": {
  "free_shipping_threshold_usd": 75,
  "aov_lift_target_pct_above_threshold": 0.05,
  "aov_lift_max_pct_above_threshold": 0.15,
  "current_avg_cart_value_usd": 58
}
```

The skill flags when current avg cart × 1.30 < free-shipping threshold (i.e., a bundle can't reasonably bridge the gap with 1-2 add-ons). In those cases, the threshold may be miscalibrated, and the skill recommends lowering the threshold instead of forcing implausible bundles.
