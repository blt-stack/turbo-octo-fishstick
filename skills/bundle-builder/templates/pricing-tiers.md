# Pricing Tiers — Conservative / Standard / Aggressive

For each bundle, the skill computes three pricing options. Buyer picks. The defaults below are tunable in config.

## The three tiers

| Tier | Discount range | Use case | Typical bundle types |
|---|---|---|---|
| Conservative | 5-10% off | Low risk; testing; premium brands | Gift sets, complementary bundles for new launches |
| Standard | 12-18% off | Most common; balanced | FBT bundles, complementary bundles for established categories |
| Aggressive | 20-25% off | Promo, clearance, acquisition | Starter kits, holiday gift sets, clearance |

## Tier defaults per bundle type

| Bundle type | Default tier |
|---|---|
| Frequently-Bought-Together | Standard |
| Complementary Category | Standard |
| AOV-Lift | Conservative |
| Gift Set | Conservative |
| Starter Kit | Aggressive |

The skill picks the default but always outputs all 3 tiers so the buyer can pick.

## Tier computation per bundle

```python
def compute_tiers(bundle_skus, cost_total, retail_total, default_discount_pct):
    # Three discount levels: conservative, standard, aggressive
    discounts = {
        "conservative": 0.075,  # midpoint of 5-10%
        "standard":     0.15,   # midpoint of 12-18%
        "aggressive":   0.22,   # midpoint of 20-25%
    }
    tiers = {}
    for name, disc in discounts.items():
        bundle_price = retail_total * (1 - disc)
        savings_usd = retail_total - bundle_price
        margin_usd = bundle_price - cost_total
        margin_pct = margin_usd / bundle_price if bundle_price > 0 else 0
        tiers[name] = {
            "discount_pct": disc,
            "bundle_price_usd": round(bundle_price, 2),
            "savings_usd": round(savings_usd, 2),
            "savings_pct": disc,
            "blended_margin_usd": round(margin_usd, 2),
            "blended_margin_pct": round(margin_pct, 3),
            "passes_margin_floor": margin_pct >= 0.25  # configurable
        }
    return tiers
```

## Buyer-tunable discount ranges

The buyer can configure the discount levels per tier:

```json
"bundle_builder": {
  "pricing_tiers": {
    "conservative": {"min_pct": 0.05, "max_pct": 0.10, "default_pct": 0.075},
    "standard":     {"min_pct": 0.12, "max_pct": 0.18, "default_pct": 0.15},
    "aggressive":   {"min_pct": 0.20, "max_pct": 0.25, "default_pct": 0.22}
  }
}
```

Some brands customize:
- Premium brands set conservative=3-5%, standard=8-12%, aggressive=15%
- Value brands set conservative=10%, standard=20%, aggressive=30%
- Subscription brands set higher first-order discounts for retention

## Pricing principles

### Round to psychologically familiar numbers

After computing the bundle price, the skill rounds to ".99," ".95," ".00," or other patterns per brand preference:

```json
"pricing_tiers": {
  "rounding_strategy": "psychological_99"  // options: "99", "95", "00", "none"
}
```

A $76.50 bundle with "99" strategy becomes $74.99 (or $76.99, depending on rounding direction).

The skill defaults to ".00" (clean numbers) for premium brands and ".99" for value-tier brands. Buyer can override.

### Anchor against individual price

Every bundle's positioning copy mentions the individual-price anchor:

> "Individual price: $92"
> "Bundle price: $78"
> "You save: $14"

The anchor matters because it's how customers understand value. A "$78 bundle" without context could be cheap or expensive; "$78 bundle vs. $92 individually" is clearly a deal.

The skill ensures the anchor is always present in positioning copy. See `positioning-copy.md`.

### Avoid sub-$1 savings amounts

A bundle that saves $0.75 looks unserious. The skill rounds to whole dollars and flags bundles where the savings amount is below $3 (suggests the bundle doesn't have enough value to bundle).

Minimum savings flag: < $3 → "consider deeper discount or different bundle"
Healthy savings: $5-30 for most bundles
Premium savings: $30-100 for high-end starter kits

### Discount as $ amount can read better than %

In positioning copy, the skill alternates between:
- "Save 15% on the bundle"
- "Save $14 when you buy together"

The $ amount often converts better for under-$100 bundles. The % framing converts better for over-$200 bundles.

The skill outputs both for the buyer's positioning copy variants and recommends which to lead with based on bundle price.

## Margin floor enforcement

For each tier, the skill checks:

```python
passes_margin_floor = blended_margin_pct >= config.bundle_builder.margin_floor_pct  # default 0.25
```

Tiers below the floor are flagged but not removed — the buyer may still want to deploy them for strategic reasons (e.g., starter kits with thin margin offset by LTV).

Output format:

```
Conservative: $84 — 8% off — margin 68% ✓
Standard:     $76 — 17% off — margin 65% ✓ (recommended)
Aggressive:   $69 — 25% off — margin 60% ✓

All tiers pass margin floor (25%). No constraints.
```

vs.

```
Conservative: $52 — 8% off — margin 31% ✓
Standard:     $46 — 19% off — margin 22% ✗ BELOW FLOOR
Aggressive:   $42 — 27% off — margin 14% ✗ BELOW FLOOR

Only conservative tier passes margin floor.
Consider: this is a low-margin bundle — even conservative is on the edge.
```

The buyer sees the constraint clearly and decides.

## Pricing tiers for starter kits

Starter kits are an exception. The aggressive tier becomes the default because the bundle's job is acquisition, not immediate margin:

```
Starter Kit pricing:
  Conservative (10% off):  $76 — margin 55% — but: too high for first-time customer
  Standard (15% off):      $72 — margin 51%
  Aggressive (22% off):    $66 — margin 47% (recommended for starter kit)
```

The skill notes that aggressive pricing is the right call for starter kits and shows the LTV math:

```
Aggressive tier first-order margin: $31 (vs. $43 at conservative)
Estimated 60-day LTV of starter-kit acquisition: $280
LTV/CAC ratio assuming $25 acquisition cost: 11.2:1
Margin sacrifice on first order ($12) is recoverable in 1 repeat purchase
```

## Pricing tier transitions during promotions

Bundles can swap tiers temporarily for promotions:
- Q4 holiday: bump conservative bundles up to standard tier discount
- Anniversary sale: bump everything to aggressive for the week
- Cyber Monday: all bundles at aggressive

The skill doesn't manage promotional schedules but tags bundles with `promo_tier_eligibility` for skill #8 (Campaign Calendar Planner) to consume.

## Bundle pricing as marketing signal

The discount amount sends a brand signal:
- 5-10%: "Curated set, slight thank-you for buying together" — premium feel
- 12-18%: "Bundle deal, real value" — mainstream
- 20-25%: "Promotional bundle, significant savings" — promotional / value brand
- 30%+: "Clearance / desperate" — generally avoid (signals problems)

The skill's tier defaults track to brand archetype where possible (premium brands default to lower discounts). Buyer can override per brand identity.
