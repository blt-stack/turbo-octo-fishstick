# Cross-Skill Cache Integrations

The "What Needs Attention Today" section reads from four cross-skill caches written by skills #11-14. The Digest is the **morning rollup** of state these other skills track in real-time.

## The 4 caches read

| Cache | Writer skill | What gets surfaced |
|---|---|---|
| `~/.the-ecommerce-seller/cache/reorder_triggers/{date}.json` | #12 Inventory Forecaster | SKUs approaching stockout |
| `~/.the-ecommerce-seller/cache/suppliers/{*}.json` | #11 Supplier Negotiation Assistant | Overdue supplier responses |
| `~/.the-ecommerce-seller/cache/bundles/{*}.json` | #13 Bundle Builder | Undeployed bundles ranked by score |
| `~/.the-ecommerce-seller/cache/influencers/{*}.json` | #14 Influencer Outreach Pro | Pending influencer follow-ups |

Plus optional:

| Cache | Writer skill | What gets surfaced |
|---|---|---|
| `~/.the-ecommerce-seller/cache/forecast_runs/{date}.json` | #12 Inventory Forecaster | Recent forecast method changes (when a SKU swapped to a different forecasting method or gained seasonality detection) |

## Cache 1: Inventory reorder triggers (skill #12)

### Schema

```json
{
  "run_date": "2026-05-22",
  "triggers": [
    {
      "sku": "RS-POUR-OVER-001",
      "product_name": "River Stone Pour-Over",
      "current_stock": 120,
      "daily_velocity_p50": 14.2,
      "days_until_stockout_p50": 8.5,
      "supplier_lead_time_days": 60,
      "reorder_recommended_qty": 1500,
      "urgency_tier": "critical"
    }
  ]
}
```

### How it surfaces in the digest

Group by urgency_tier:

- **Critical** (`days_until_stockout_p50 <= 14`): top of inventory list
- **Plan** (`14 < days_until_stockout_p50 <= 30`): second priority
- **Watch** (`30 < days_until_stockout_p50 <= 60`): noted if SKU is also a top-revenue mover

For each surfaced SKU, the digest line includes:

```
- [SKU name] — stocks out in [N days at current velocity];
  supplier lead time [N days];
  reorder [N units] (estimated cost from supplier cache);
  recommended action: [send PO via skill #11 / send reorder letter / etc.]
```

### Cross-reference with supplier cache

When a SKU has a known primary supplier (from `~/.the-ecommerce-seller/cache/sku_to_supplier.json`), the digest pulls:

- Supplier's current lead time
- Supplier's MOQ
- Supplier's response pattern
- Whether a reorder letter has already been sent (if so, surfaces the pending response from supplier cache instead)

This prevents double-flagging (the SKU is "critical" but a PO is already in flight).

## Cache 2: Supplier pending responses (skill #11)

### Schema (relevant subset)

```json
{
  "supplier_id": "shenzhen-stoneworks",
  "company_name": "Shenzhen Stoneworks Co., Ltd.",
  "relationship_stage": "established",
  "pending_responses": [
    {
      "letter_date": "2026-05-15",
      "letter_type": "moq_reduction",
      "expected_response_by": "2026-05-18",
      "follow_up_due": "2026-05-19"
    }
  ]
}
```

### How it surfaces

For each supplier cache file, the skill reads `pending_responses` and flags any where `follow_up_due <= today`:

- **Overdue ≤7 days**: routine follow-up
- **Overdue 8-14 days**: notable — send Variant A follow-up
- **Overdue 15+ days**: critical — supplier silent; escalate or pivot

Each line:

```
- [Company name] — [letter type] sent [N days ago];
  follow-up was due [N days ago] (overdue [N days]);
  region: [region]; recommend: [send Variant A follow-up via skill #11]
```

The digest groups by region (China / India / Vietnam / NA / EU) because regional follow-up tactics differ.

## Cache 3: Undeployed bundles (skill #13)

### Schema (relevant subset)

```json
{
  "bundle_id": "complete-coffee-brewing-set",
  "bundle_name_descriptive": "Complete Coffee Brewing Set",
  "bundle_name_evocative": "The Slow Morning Bundle",
  "discovery_evidence": {"composite_score": 84.3},
  "recommended_tier": "standard",
  "pricing_tiers": {"standard": {"bundle_price_usd": 78.20}},
  "deployed": false,
  "downstream_consumed_by": []
}
```

### How it surfaces

Filter bundles where `deployed != true`. Sort by `discovery_evidence.composite_score` descending. Surface top 3.

Each line:

```
- [Bundle evocative name] (composite score [N]/100)
  Price: $[N] (standard tier; saves $[N] vs. individual)
  Type: [primary type] (+ [secondary])
  Recommend: launch as today's promo, or run skill #3
  Landing Page Copywriter to generate landing page
```

A bundle's `deployed` flag flips to `true` when the buyer adds it to Shopify (manual update) or when one of the downstream skills (Landing Page Copywriter, Ad Creative Generator) consumes it. The digest respects this and stops re-surfacing deployed bundles.

## Cache 4: Pending influencer follow-ups (skill #14)

### Schema (relevant subset)

```json
{
  "handle": "@maya_brews",
  "platforms": {"instagram": {"tier": "nano"}},
  "pending_responses": [
    {
      "outreach_date": "2026-05-15",
      "outreach_type": "initial",
      "expected_response_by": "2026-05-22",
      "follow_up_due": "2026-05-23"
    }
  ],
  "relationship_stage": "outreached"
}
```

### How it surfaces

For each influencer cache file:

- Read `pending_responses`
- Flag any where `follow_up_due <= today`
- Determine which follow-up variant comes next based on `relationship_stage`:
  - `outreached` → Variant A
  - `follow_up_sent_a` → Variant B
  - `follow_up_sent_b` → Variant C
  - `follow_up_sent_c` → none (creator marked as `no_reply_terminal`)

Each line:

```
- [@handle] ([platform], [tier]) — initial outreach sent [N days ago];
  Variant [A/B/C] due [today / N days ago];
  recommend: run skill #14 with "follow up with @[handle]"
```

The digest groups by tier × platform when multiple follow-ups are due (helps the buyer batch the day's outreach).

## Cache 5 (optional): Recent forecast method changes (skill #12)

For buyers who care about forecasting methodology transparency, the digest can optionally surface:

- SKUs that changed forecasting method in the last 24 hours (e.g., switched from rolling 14-day to Holt-Winters as enough history accumulated)
- SKUs that newly detected seasonality
- SKUs whose stockout prediction shifted by >30%

Enabled via `daily_store_digest.surface_forecast_method_changes=true`. Off by default.

## Ranking the action queue

When the cross-skill cache reader returns multiple items across all 4 buckets, the digest ranks them for the "Suggested Actions Today" section:

1. **Critical inventory** (stockout <14 days) for top-revenue SKUs
2. **Overdue supplier responses** that are blocking inventory reorders
3. **Critical inventory** for mid-tier SKUs
4. **Critical inventory** for low-tier SKUs
5. **Influencer Variant C** (final ask — close out or move on)
6. **High-score undeployed bundles** (composite score >80)
7. **Influencer Variant A** (soft nudges — quick action)
8. **Overdue supplier responses** for non-inventory letters (price tier, payment terms)
9. **Influencer Variant B** (reframed offers)
10. **Mid-score undeployed bundles** (composite score 60-80)
11. **Plan-tier inventory** (stockout 14-30 days)

The top 3-5 from this ranked list become the "Suggested Actions" of the day.

## What the digest does NOT do

- Does not modify any cache (read-only)
- Does not auto-trigger downstream skills (the buyer initiates)
- Does not duplicate-flag (deployed bundles, completed influencer follow-ups, etc. are filtered out)
- Does not surface stale-dated triggers (a stockout warning from 2 weeks ago that the buyer has already resolved is filtered if the SKU is no longer in the latest `reorder_triggers/{date}.json`)

## When caches are empty

If a cache directory doesn't exist or contains no relevant items, the digest section just notes the absence neutrally:

```
INVENTORY: No reorder triggers within the next 60 days. Healthy.
SUPPLIERS: No overdue responses. Quiet.
BUNDLES: No undeployed bundles in the cache (or all have been deployed).
INFLUENCERS: No follow-ups due today.
```

This is normal early in a buyer's plugin journey before they've run the other skills.
