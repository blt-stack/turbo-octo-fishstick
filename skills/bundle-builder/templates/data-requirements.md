# Data Requirements

What the skill needs from the buyer to produce useful bundles. Two tiers: required + optional.

## Required (minimum viable forecast)

### 1. Sales / order history

Source: Shopify Orders CSV, Amazon Business Reports, Etsy stats, or generic multi-channel CSV (same shapes as skill #12).

The skill reads each order's line items to build market baskets. Required columns:
- Order identifier
- Order date
- SKU
- Quantity

Optional but valuable on each line:
- Product name (for display)
- Unit price (for revenue / margin calc)

Minimum: 100 orders. Below this, Apriori signals are too noisy; skill falls back to categorical-only mode.

### 2. Product catalog (basic)

For each SKU sold:
- SKU
- Product name
- Retail price

Without these, the skill can't compute bundle pricing or savings amounts.

## Optional (enriches the forecast)

### 3. Cost per SKU

When available, enables the margin optimization layer. Sources:
- Buyer-provided per-SKU cost in product catalog CSV
- Supplier memory cache (`current_unit_price_usd` from skill #11)
- Manual entry during onboarding

Without cost data:
- The skill skips margin analysis
- Pricing tiers show savings amounts but not blended margin
- Buyer is flagged: "add cost data to unlock margin optimization"

### 4. Category mapping

Each SKU mapped to one or more categories. Sources (cascading):
1. Shopify product type field
2. Shopify collections
3. Skill-auto-classified from product name keywords
4. Buyer manual mapping

Without category mapping, the Complementary Category and Gift Set layers degrade severely. The skill recommends spending 15-30 minutes mapping SKUs during onboarding.

### 5. Inventory forecast data (from skill #12)

Source: `<plugin-root>/.cache/forecast_runs/{date}/...` or per-SKU diagnostics.

The skill reads:
- Per-SKU velocity (units/day at P50)
- Per-SKU current stockout status
- Per-SKU urgency level

Used to:
- Favor in-stock + healthy-velocity SKUs in bundles
- Exclude stockout-imminent SKUs from new bundles (would create disappointment)
- Surface "consider bundling these slow-movers with hero" recommendations

### 6. Testimonial cache (from skill #10)

Source: `<plugin-root>/.cache/testimonials/{product-identifier}.json`

The skill reads pull-quotes for SKUs in each bundle for the social-proof-led copy variant. Without testimonials, that variant falls back to brand-voice-only.

### 7. Brand voice + audience config

Standard plugin config fields. Used for copy generation tone calibration.

## Failure modes by missing data

| Missing | Effect |
|---|---|
| < 100 orders | Apriori sparse; skill weights categorical higher; flags data-light bundles |
| No product catalog | Skill cannot produce pricing tiers; halts |
| No cost data | Margin analysis skipped; bundles still produced |
| No categories | Complementary + gift bundles dormant; only FBT works |
| No inventory data | Skill cannot prioritize in-stock SKUs; bundles may include risky stockouts |
| No testimonials | Variant C falls back to brand-voice-only |
| No brand voice config | Copy is generic; lacks brand-specific tone |

The skill outputs the data-quality status at the top of each run:

```
DATA QUALITY SUMMARY
- Orders: 412 (✓ sufficient)
- Product catalog: 47 SKUs (✓)
- Cost data: 35/47 SKUs have cost (74%; partial margin analysis)
- Categories: 47/47 SKUs categorized (✓ via Shopify product type)
- Inventory forecast: data from 2026-04-15 run (5 days old; ✓ fresh)
- Testimonials: cache has 23 quotes across 12 SKUs (✓)

Confidence: HIGH for FBT bundles, HIGH for Complementary, MEDIUM for AOV-Lift (cost data 74% coverage).
```

## Input format

The skill accepts:
- CSV uploads for orders + catalog
- Direct Shopify connector pull (when available)
- Manual data entry through buyer prompts (slow but possible for small catalogs)

The skill auto-detects format per skill #12's parser.

## Data freshness

| Data | Recommended refresh |
|---|---|
| Sales data | Monthly minimum (weekly is better) |
| Product catalog | When new SKUs launch |
| Cost data | When supplier prices change |
| Categories | Yearly review |
| Inventory forecast | Weekly (drives bundle prioritization) |
| Testimonials | Continuously (skill #10 writes as new reviews come in) |

Stale data produces stale bundles. The skill flags when sales data is > 60 days old or when forecast data is > 30 days old.

## Pre-run data validation

The skill validates inputs before running:
- Order count check (warn if < 100)
- Catalog completeness check (warn if > 10% of recent SKUs are missing from catalog)
- Cost data coverage check (warn if < 50% of SKUs have cost data)
- Category coverage check (warn if > 20% uncategorized)
- Velocity sanity check (compare against skill #12's data if available)

Buyer can proceed past warnings — the skill will note degraded confidence per-bundle.
