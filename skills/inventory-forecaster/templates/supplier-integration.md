# Supplier Integration — Reading Memory from Skill #11

The forecaster reads the supplier memory cache written by the Supplier Negotiation Assistant (skill #11) to pull lead times, MOQs, and payment terms per SKU. This turns generic forecasts into supplier-specific reorder plans.

## SKU-to-supplier mapping

Each SKU needs to know which supplier(s) make it. The mapping lives at:

```
~/.the-ecommerce-seller/cache/sku_to_supplier.json
```

Schema:

```json
{
  "_meta": {
    "last_updated": "2026-04-15T12:00:00Z",
    "version": 1
  },
  "RS-POUR-OVER-001": {
    "primary_supplier_id": "shenzhen-stoneworks-co-ltd-cindy-chen",
    "supplier_specific_overrides": {
      "lead_time_days": 45,
      "transit_days": 30,
      "transit_mode": "sea_freight",
      "moq": 1500,
      "current_unit_price_usd": 4.20
    },
    "secondary_suppliers": []
  },
  "STUDIO-BOWL-LRG": {
    "primary_supplier_id": "jingdezhen-ceramics-co-ltd",
    "supplier_specific_overrides": {
      "lead_time_days": 50,
      "transit_days": 30,
      "moq": 500,
      "current_unit_price_usd": 6.10
    }
  }
}
```

The mapping is populated:
- **By the buyer during onboarding** — for SKUs already in production
- **By skill #11** — when the buyer drafts a sample request or RFQ that designates a supplier for a SKU
- **By skill #12 (this skill)** — when the buyer manually maps during a forecast run

## Reading lead time

The cascade for finding lead time:

1. `sku_to_supplier.json` → `supplier_specific_overrides.lead_time_days` (most specific)
2. `~/.the-ecommerce-seller/cache/suppliers/{supplier_id}.json` → `product_lines_sourced[matching product].lead_time_days`
3. `~/.the-ecommerce-seller/cache/suppliers/{supplier_id}.json` → supplier-wide default lead time
4. Regional default (China 45 days, Vietnam 40, India 35, NA 14, EU 21)
5. Buyer prompt — skill asks for lead time before proceeding

The skill logs which step in the cascade produced the value, so the buyer can audit confidence.

## Reading MOQ

Same cascade:
1. SKU-specific override
2. Product-line entry in supplier file
3. Supplier-wide default (rare)
4. Buyer prompt

MOQ matters for reorder quantity calculation — even if forecast says "you need 800 units," if MOQ is 1500, you order 1500 (and flag for negotiation via skill #11).

## Reading payment terms

Read from `supplier.payment_terms_in_force.structure` in the supplier file.

Payment terms drive the *deposit date* calculation:
- "100_upfront": deposit on reorder decision
- "30_70_tt_before_shipping": 30% on reorder decision
- "30_70_tt_against_bl": 30% on reorder decision; balance later
- "lc_at_sight": initiate LC 5 days before reorder decision (LC opening time)
- "net_30": no deposit; pay 30 days after shipped invoice
- "net_45" / "net_60": same pattern

## What happens when supplier memory is missing

The skill gracefully degrades:

1. SKU has no `sku_to_supplier.json` entry → prompt buyer for primary supplier
2. Buyer provides supplier name → skill looks for matching `~/.the-ecommerce-seller/cache/suppliers/{slug}.json`
3. If supplier file doesn't exist → skill prompts for lead time / MOQ / unit price / payment terms
4. Auto-creates a stub `sku_to_supplier.json` entry so the next forecast run doesn't re-prompt

After the prompt, the skill suggests the buyer use skill #11 to flesh out the supplier file fully.

## Per-product overrides (some products from one supplier have different terms)

A supplier may make multiple products with different MOQs, prices, and lead times. The `supplier_specific_overrides` in `sku_to_supplier.json` lets each SKU pin its own values:

- River Stone Pour-Over: MOQ 1500, $4.20/unit, 45-day lead
- Studio Glaze Bowl: MOQ 500, $6.10/unit, 50-day lead (same supplier)

The skill writes back updated overrides if the buyer corrects them during a forecast run.

## Multi-supplier SKUs (rare but possible)

Some SKUs have multiple qualified suppliers — for risk diversification or capacity. The mapping supports:

```json
"RS-POUR-OVER-001": {
  "primary_supplier_id": "shenzhen-stoneworks",
  "secondary_suppliers": ["jingdezhen-ceramics-co-ltd"],
  "split_allocation": {
    "shenzhen-stoneworks": 0.7,
    "jingdezhen-ceramics-co-ltd": 0.3
  }
}
```

In this case, the forecast splits the reorder across suppliers per the allocation. The skill outputs separate reorder triggers per supplier.

For most solo operators, a single primary supplier per SKU is standard. The multi-supplier path is opt-in.

## Lead-time variance tracking

When the buyer marks an order as delivered (manually or via Shopify connector), the skill updates the supplier file with the actual lead time observed:

```json
"product_lines_sourced": [{
  "product_name": "River Stone Pour-Over",
  "lead_time_days_quoted": 45,
  "lead_time_observed_history": [42, 47, 45, 51, 44],
  "lead_time_variance_observed": 0.07
}]
```

Variance feeds back into safety stock calculations. High-variance suppliers warrant more safety stock.

## Cross-skill data flow summary

```
[Sales CSV upload]
        │
        ▼
[Skill #12 reads SKU history]
        │
        ▼
[Skill #12 looks up SKU → supplier via sku_to_supplier.json]
        │
        ▼
[Skill #12 reads ~/.the-ecommerce-seller/cache/suppliers/{supplier_id}.json for lead time, MOQ, terms]
        │
        ▼
[Skill #12 computes reorder dates + quantities]
        │
        ▼
[Skill #12 writes ~/.the-ecommerce-seller/cache/reorder_triggers/{date}.json]
        │
        ▼
[Buyer runs skill #11 next: "what supplier letters do I need to send?"]
        │
        ▼
[Skill #11 reads ~/.the-ecommerce-seller/cache/reorder_triggers/, drafts reorder outreach letters]
```

The two skills compound — the forecaster says when to order; the negotiation assistant drafts the letter to make it happen.

## What if the buyer doesn't use skill #11

The skill works fine without skill #11:
- Reads buyer-provided lead times / MOQs from `sku_to_supplier.json` (entered during onboarding or first forecast)
- Skips the `~/.the-ecommerce-seller/cache/reorder_triggers/` write (or writes them but flags "no downstream consumer found")
- Outputs reorder dates and quantities in the .xlsx for the buyer to act on manually

The integration is opt-in and compounds value; it's not required.

## What if the buyer has many SKUs without supplier mapping

When the first forecast run finds 20+ unmapped SKUs, the skill suggests batching them:

1. Skill outputs a list of unmapped SKUs sorted by velocity (most important first)
2. Buyer maps top N during the forecast run (or after)
3. Subsequent runs only prompt for newly-detected unmapped SKUs

The bulk catalog .xlsx includes a "SKUs needing supplier mapping" column on Sheet 1 so the buyer can address gaps over time.

## Lead time disagreements

If the supplier file says 45 days but the buyer overrides to 60 in this forecast run, the skill:
1. Uses 60 for this run
2. Logs the override in the audit
3. Optionally writes back to update the supplier file (buyer confirms)

This handles the common case where a supplier's quoted lead time differs from observed reality.
