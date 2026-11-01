# Margin Optimization

The third layer of bundle discovery. Identifies bundle constructions that improve blended margin vs. discounting hero SKUs alone.

## The blended margin problem

When a brand wants to discount its hero SKU (often to drive acquisition or move inventory), the discount comes out of the hero's margin alone. Example:

- River Stone Pour-Over: $48 retail, $14 cost → 71% margin = $34 profit
- Discount the pour-over 20% to $38.40 → margin drops to 64% = $24.40 profit
- Loss per unit: $9.60

A bundle approach:

- River Stone Pour-Over @ $48 retail, $14 cost → $34 margin
- + Filter Pack @ $12 retail, $3 cost → $9 margin
- + Carafe @ $32 retail, $10 cost → $22 margin
- **Bundle total**: $92 retail, $27 cost → $65 blended margin (70%)
- Discount bundle 15% → $78.20 retail, $27 cost → $51.20 blended margin (65%)

The bundle approach keeps the brand at 65% blended margin while still appearing to give a "great deal" — better than discounting the hero alone to 64%.

This is the math the margin optimization layer surfaces.

## Margin attractor identification

For each SKU, the skill computes:
- **Margin %** = (retail - cost) / retail
- **Velocity** = recent days' units sold / day

Then classifies:

| Classification | Criteria | Bundle role |
|---|---|---|
| High-margin hero | High margin (>60%), high velocity | Bundle anchor (pulls customers in) |
| High-margin add-on | High margin (>60%), low velocity | Bundle multiplier (improves blended margin) |
| Low-margin attractor | Low margin (<40%), high velocity | Bundle door-opener (use sparingly) |
| Loss-leader | Negative margin or near-zero, any velocity | Avoid in bundles unless intentional |

The ideal bundle combines: 1 high-margin hero + 1-2 high-margin add-ons.
A risky bundle: 1 low-margin attractor + 1-2 high-margin add-ons (still net positive but less robust).

## Margin scoring per bundle

```python
def margin_score(bundle_skus, retail_total, cost_total, discount_pct):
    bundle_retail = retail_total * (1 - discount_pct)
    bundle_cost = cost_total
    blended_margin_pct = (bundle_retail - bundle_cost) / bundle_retail if bundle_retail > 0 else 0

    # Compare to discounting the most-expensive SKU alone at the same level
    hero_sku = max(bundle_skus, key=lambda s: s["retail"])
    hero_discounted = hero_sku["retail"] * (1 - discount_pct)
    hero_alone_margin = (hero_discounted - hero_sku["cost"]) / hero_discounted

    margin_improvement_vs_hero_discount = blended_margin_pct - hero_alone_margin

    return {
        "blended_margin_pct": blended_margin_pct,
        "margin_improvement_vs_hero_discount": margin_improvement_vs_hero_discount,
        "score": min(100, max(0, blended_margin_pct * 100))  # simple 0-100 normalization
    }
```

A bundle with positive `margin_improvement_vs_hero_discount` is a margin-positive bundle — discounting the bundle is strictly better than discounting the hero alone.

## Margin floor enforcement

Buyer configures a margin floor in config:

```json
"bundle_builder": {
  "margin_floor_pct": 0.25
}
```

Default 25%. Bundles with blended margin below this floor get flagged but not auto-excluded — sometimes a thin-margin bundle is intentional (acquisition, clearance). The buyer reviews flagged bundles.

The skill reports per-bundle:
- Blended margin at conservative tier
- Blended margin at standard tier
- Blended margin at aggressive tier
- Whether each tier passes the floor

## Margin layer interaction with other layers

The margin layer doesn't *generate* bundle candidates by itself — it *filters and ranks* candidates from the Apriori and Categorical layers.

Workflow:
1. Apriori produces FBT candidates → margin layer scores and filters
2. Categorical produces use-case candidates → margin layer scores and filters
3. Final candidate list is ranked by composite score (which includes margin)

## Margin-improving bundle constructions

The skill surfaces specific bundle patterns where margin improves vs. solo discounting:

### Pattern A: Hero + High-margin accessory
```
Hero (60% margin) + Accessory (80% margin) at 15% off
vs. Hero alone at 15% off
→ Bundle margin: 65%; Hero alone margin: 47%
→ Bundle is 18 points better
```

### Pattern B: Hero + Consumable
```
Durable hero (70% margin) + Consumable refill (75% margin) at 12% off
vs. Hero alone at 12% off
→ Bundle margin: 70%; Hero alone margin: 56%
→ Bundle adds repeat-purchase potential AND improves immediate margin
```

### Pattern C: Two complementary heroes
```
Hero A (65% margin) + Hero B (65% margin) at 18% off
vs. Hero A alone at 18% off
→ Bundle margin: 53%; Hero A alone margin: 41%
→ Bundle is 12 points better; both SKUs sold instead of just A
```

### Anti-pattern: Hero + Low-margin filler
```
Hero (65% margin) + Low-margin item (20% margin) at 15% off
vs. Hero alone at 15% off
→ Bundle margin: 47%; Hero alone margin: 47%
→ Bundle isn't materially better; the low-margin filler drags blended margin down
→ Skill flags this as anti-pattern and recommends substitution
```

## Cost data sourcing

Margin calculation requires per-SKU cost. Sources (in order of preference):

1. **Buyer-provided cost** in product catalog CSV or product metafields
2. **Supplier memory cache** (skill #11) — `current_unit_price_usd` is the brand's cost from the supplier
3. **Buyer's spreadsheet** uploaded alongside sales data
4. **Buyer's manual entry** during onboarding

When no cost is available, the skill skips the margin layer and outputs a warning. Bundles still get generated via Apriori + Categorical layers, but the margin-improvement analysis is unavailable.

## Margin-aware tier selection

When multiple tiers are possible, the skill recommends the highest tier (most discount) that still clears the margin floor:

```
Conservative (10% off): margin 68% — well above floor → could go lower
Standard (15% off): margin 65% — above floor → recommended
Aggressive (22% off): margin 58% — above floor → also acceptable
```

But the skill caps at "standard" by default unless:
- Bundle is type=starter_kit (aggressive is normal here)
- Bundle is type=gift_set with clearance tag
- Buyer explicitly overrides

## Bundle vs. solo: when bundling makes margin sense

The fundamental question: is bundling at X% off better than discounting the hero at X% off?

The answer depends on:
- **Attach rate**: % of customers who would buy add-ons separately
- **Add-on margins**: higher add-on margins improve bundle math
- **Bundle uplift**: how much more often customers buy multiple vs. one

The skill computes this ratio for each candidate:

```
bundle_attractiveness_ratio = bundle_margin_per_order / solo_discounted_margin_per_order
```

Ratio > 1.0: bundle is the better promotional tool
Ratio = 1.0: neutral
Ratio < 1.0: solo discount is more efficient (rare but possible for thin-margin add-ons)

This ratio surfaces in the .xlsx audit so the buyer can quickly see which bundles are margin-positive.

## When margin optimization fails

- **All SKUs same margin**: optimization can't differentiate
- **Catalog is all low-margin**: no high-margin add-ons available for the multiplier effect
- **Cost data is wrong**: garbage-in, garbage-out — the skill encourages accuracy
- **Bundle is loss-leader by design**: the skill flags but doesn't override buyer intent

The skill explains its reasoning in the Discovery Audit sheet so the buyer can override.
