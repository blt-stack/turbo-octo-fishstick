# CSV Shapes — Per-Platform Sales Data

The forecast engine works on a canonical (SKU, date, units_sold) schema. The CSV parser detects which platform the upload is from based on header signature, then maps to canonical.

## Canonical schema (post-parse)

Every row after parsing:

```python
{
  "sku": str,             # canonical SKU identifier
  "product_name": str,    # optional, but useful for human-readable output
  "date": "YYYY-MM-DD",   # ISO date
  "units_sold": int,
  "revenue": float | None,
  "channel": str          # "shopify" | "amazon" | "etsy" | "ebay" | "walmart" | "tiktok_shop" | "manual"
}
```

The skill aggregates multiple rows for the same (SKU, date) — useful when multiple orders ship on the same day.

## Shopify Orders CSV

Export from Shopify Admin → Orders → Export → CSV (all orders).

Header signature: includes `Lineitem sku` AND `Created at`.

Parser logic:
- Each row in the export is a line item (a product within an order)
- Group rows by (Lineitem sku, date-of-Created-at)
- Sum Lineitem quantity to get units_sold
- Sum (Lineitem price × Lineitem quantity) to get revenue
- Skip rows where `Cancelled at` is non-empty (cancelled orders) or `Financial Status == "refunded"` for refund rows

Columns used:
- `Name` (order ID)
- `Created at` (date)
- `Lineitem sku` → canonical sku
- `Lineitem name` → product_name
- `Lineitem quantity` → units_sold (per row, summed)
- `Lineitem price` → for revenue calc
- `Cancelled at` (filter)
- `Financial Status` (filter)

## Amazon Business Reports CSV

Export from Seller Central → Reports → Business Reports → Detail Page Sales and Traffic by Child Item.

Header signature: includes `(Child) ASIN` AND `Units Ordered`.

Parser logic:
- Each row is already aggregated by ASIN per date
- Map `(Child) ASIN` → canonical sku
- `Title` → product_name
- `Units Ordered` → units_sold
- `Ordered Product Sales` → revenue (numeric clean: strip $ and commas)
- Date column varies — some exports name it `Date`, some `Reporting Period`; skill auto-detects

## Etsy stats CSV

Export from Etsy Shop Manager → Stats → Download CSV.

Header signature: includes `Listing ID` AND `Quantity sold`.

Parser logic:
- One row per listing per date
- `Listing ID` → canonical sku
- `Listing title` → product_name
- `Quantity sold` → units_sold
- `Revenue` → revenue

Etsy exports often span date ranges in a single field — skill normalizes.

## Generic multi-platform CSV

For buyers combining channels or using non-supported platforms.

Required columns (any subset of names accepted — case-insensitive):
- `sku` (required)
- `date` (required)
- `units_sold` (required)
- `product_name` (optional)
- `revenue` (optional)
- `channel` (optional)

Header signature: includes `sku` AND `date` AND `units_sold` (case-insensitive).

## Auto-detection logic

The parser inspects the CSV's header row and matches signatures in this order:

1. **Has `(Child) ASIN`**: Amazon
2. **Has `Listing ID` + `Quantity sold`**: Etsy
3. **Has `Lineitem sku` + `Created at`**: Shopify
4. **Has lowercase `sku` + `date` + `units_sold`**: Generic
5. **Otherwise**: asks buyer to confirm format

## Date parsing

Skill handles common date formats:
- ISO: `2026-04-15`
- US: `4/15/2026` or `04/15/2026`
- EU: `15/04/2026`
- Shopify: `2026-04-15 14:23:00 +0000` (truncated to date)
- Amazon: `2026-04-15` or `2026-04-15T00:00:00`

Ambiguous cases (e.g., `03/04/2026` — March 4 US or April 3 EU?) prompt the buyer to confirm.

## Multi-channel data

When buyer uploads multiple CSVs (one per channel), the parser:
1. Parses each independently per its platform conventions
2. Aggregates by canonical SKU
3. Tags each (sku, date) entry with the `channel` it came from
4. Sums units_sold across channels for total demand
5. Allows per-channel filtering in the forecast (single mode can isolate to one channel)

For SKUs sold on multiple platforms with different SKU codes (e.g., Shopify SKU `RS-001`, Amazon ASIN `B0CXXX...`), the buyer maps these in the config under `inventory_forecasting.sku_aliases`:

```json
"sku_aliases": {
  "RS-POUR-OVER-001": ["RS-001", "B0CXXX1234", "ETSY-1234567"]
}
```

The parser collapses aliases to the canonical SKU.

## Stockout-day detection

A complication: zero sales on a given day might be (a) low demand, or (b) stockout. The forecast can't distinguish without inventory history.

The parser flags suspect stockout days:
- A day with zero sales
- Bracketed by days with positive sales within the past 14 days
- For a SKU with average velocity > 1 unit/day

These flagged days get a `_suspect_stockout: true` annotation. The forecast engine optionally excludes them from velocity calc when buyer confirms.

## Returns + refunds handling

For Shopify:
- Skip cancelled orders
- For partial refunds, decrement units_sold by the refunded line items
- For full refunds, treat as cancelled

For Amazon:
- Returns appear in a separate report (Returns Report); not auto-merged
- Buyer can upload returns CSV separately; skill subtracts

For Etsy:
- Returns rare; skill ignores by default

## Per-platform quirks

| Platform | Quirk |
|---|---|
| Shopify | Pre-orders may show as sold but not shipped — buyer should filter or accept some inflation |
| Amazon | FBM and FBA reports may need separate exports; skill merges if both uploaded |
| Etsy | Personalized / made-to-order items have variable lead-time-from-order; flag separately |
| eBay | "Buy It Now" vs auction can have different demand patterns — skill treats uniformly |
| Walmart | Walmart's CSV format differs from Amazon's — uses `Walmart Item Number` instead of ASIN |
| TikTok Shop | Newer platform; exports inconsistent — generic CSV path is safest |

## Empty / sparse data

The parser fails gracefully on sparse data:
- < 7 days of any sales: skill warns "insufficient data for any forecast method"
- 7-30 days: works but flags low-confidence
- 30-60 days: rolling average works; trend/seasonality not detectable
- 60+: full method tier accessible

## Pre-parse data hygiene

The parser runs basic checks:
- Date column is parseable and within reasonable range (not 1900, not 2050)
- SKU column has consistent capitalization (normalizes to uppercase)
- units_sold is a positive integer (negative values flagged as suspect — returns?)
- No duplicate (sku, date) pairs (would cause double-counting)

Issues are flagged in the bulk audit log; the forecast still runs but with confidence reductions.
