# Bundle Type: Starter Kit

Bundles designed specifically for first-time customers. The job of a starter kit is:
1. **Lower the friction** of trying the brand for the first time
2. **Demonstrate the brand's range** without requiring the customer to research
3. **Build an entry-level relationship** that leads to repeat purchases

Starter kits are different from other bundles because the buyer hasn't yet experienced the brand. Trust is the primary barrier; pricing is secondary.

## Source layer

Categorical complementarity + margin optimization. Starter kits prioritize SKUs that demonstrate brand identity over SKUs with the best margins.

## Filter thresholds

A starter kit qualifies when:
- Includes 2-4 SKUs representing the brand's core categories
- Total bundle price is in the buyer's "trial-comfortable" range (typically $25-75 for consumables, $50-150 for premium goods)
- Includes at least one signature/hero SKU
- Excludes the most expensive SKUs (would feel risky for a trial)

## Starter Kit structure

The ideal starter kit:
- **1 hero SKU** — the brand's most iconic / signature product
- **1-2 complementary SKUs** — items that demonstrate the brand's range
- **1 small intro item** (optional) — sample, accessory, or consumable that signals "we care about your full experience"

The hero SKU does the heavy lifting; the supporting items prove the brand has depth.

## Pricing strategy

Starter kits use **Aggressive tier (20-25% off)**. Why:
- First-time customers are price-sensitive; the discount lowers risk perception
- Margin is offset by lifetime value (CAC payback over multiple orders)
- A 20-25% discount on a $80 kit ($60 net) is one of the strongest first-touch offers possible

Exceptions:
- Ultra-premium brands where deep discounts cheapen the brand: standard tier (12-18%), but bundle gets framed as "introduction" rather than "deal"
- Subscription-onboarding starter kits: aggressive + automatic 2nd-order discount (different mechanism, more complex)

## Positioning angle

Starter kits position as **risk-free introduction**:
> "Start here. New to [Brand]? This is the way in."
> "The three things we'd give a friend to try first."
> "Everything you need to see if we're for you."

Strong starter kit copy includes:
- Specific endorsement: "Our most-loved pieces, together for less"
- Risk-reducer: "If you don't love it, return for full refund — no questions"
- Forward path: "Then explore the rest of the catalog with confidence"

Avoid:
- "Build your collection" (assumes brand-loyalty the customer doesn't have yet)
- "Limited time" (manufactured urgency on a permanent offering)
- Overly enthusiastic marketing copy (first-time customers are skeptical)

## Why these bundles work

Starter kits solve the new-customer acquisition equation:
- **Acquisition cost**: paid ads + retargeting + organic = $X per first-order customer
- **First-order revenue**: typically $40-80 for a solo brand without a starter kit
- **First-order revenue with starter kit**: typically $60-120 (1.5× lift)
- **Repeat rate impact**: customers who started with a curated kit show 1.3-2× higher 60-day repeat rate than customers who started with a single SKU

The starter kit's job isn't to be profitable on first order; it's to onboard customers who will buy 3-8 more times over the next 12 months.

## Example Starter Kits

### Coffee Brand Starter
```
- River Stone Pour-Over     $48
- Filter Pack (100)         $12
- Single-Origin Beans (250g) $18

Individual total: $78
Starter Kit (22% off): $60.85
Savings: $17.15

Position: "Start here. The pour-over, the filters, the beans we'd brew on day one."
Audience: First-time coffee customers
Margin floor check: blended margin 38% (above 25% floor — OK)
```

### Skincare Brand Starter
```
- Gentle Cleanser           $28
- Toner                     $24
- Daily Moisturizer SPF     $32

Individual total: $84
Starter Kit (25% off): $63
Savings: $21

Position: "The morning routine to try us with. Three steps. Five minutes. Easy."
```

### Premium Goods Starter
```
- Signature Mug             $42
- Wool Coaster              $18
- Brass Spoon               $24

Individual total: $84
Starter Kit (20% off): $67
Savings: $17

Position: "Our three most-given pieces. The introduction to a craft brand."
```

### Wellness Starter (with intro item)
```
- Daily Vitamin             $32
- Herbal Tea Blend          $24
- Wellness Journal          $18
- Free travel pouch          $0

Individual total: $74 (+ free pouch)
Starter Kit (22% off): $58
Savings: $16
```

## Starter kit vs. sample/trial size

Starter kits are full-size. Sample/trial bundles are smaller and cheaper:

| Starter Kit | Trial Bundle |
|---|---|
| Full-size hero + companions | Mini/sample sizes only |
| $50-150 | $15-35 |
| Long-term use experience | Short-lived experience |
| 22-25% off | 50%+ off or free with order |

Trial bundles work for skincare and consumables where the customer needs to commit to a routine; starter kits work better for product categories where one experience is enough to convert (coffee, mugs, accessories).

The skill recommends both when applicable but treats them as separate bundle types in the output.

## When starter kits fail

- **Wrong hero SKU**: starter kit anchored on a non-iconic product → fails to demonstrate the brand
- **Too expensive**: starter kit price exceeds first-time customer comfort → no conversion
- **Too cheap**: starter kit looks like clearance → cheapens the brand
- **No follow-up flow**: customer buys the kit, then the brand doesn't have a post-purchase email flow to convert to a 2nd order → wasted acquisition
- **No clear position vs. individual SKUs**: customer doesn't see why to buy the kit over picking the hero individually

## Cross-skill integration

The starter kit benefits from:
- **Skill #7 (Email Flow Architect)**: starter kits should trigger a "first-time customer" welcome flow with brand storytelling
- **Skill #5 (Ad Creative Generator)**: starter kits are the bundle format that paid acquisition ads should feature most often (lowest-friction conversion)
- **Skill #3 (Landing Page Copywriter)**: dedicated starter-kit landing page with first-time-customer framing

The bundle cache tags starter kits with `is_starter_kit: true` so downstream skills know to apply first-time-customer framing.

## Buyer config

```json
"bundle_builder": {
  "starter_kit_price_range_usd": [40, 150],
  "starter_kit_must_include_hero": true,
  "starter_kit_default_discount_pct": 0.22,
  "starter_kit_includes_intro_item": true,
  "starter_kit_lifetime_value_estimate": 280
}
```

The `starter_kit_lifetime_value_estimate` informs the margin calculation — a starter kit that loses $10 on first order is fine if 60-day LTV is $280.
