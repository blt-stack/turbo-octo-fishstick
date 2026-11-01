---
name: inventory-forecaster
description: >
  Forecasts 30/60/90-day inventory needs per SKU across Shopify, Amazon, Etsy, and generic CSV. Tiered
  method selection — rolling 14-day average for under 60 days history, Holt exponential smoothing for
  60-179 days, Holt-Winters seasonal for 180+ days with detected seasonality. Reads supplier lead
  times and MOQs from the supplier memory cache so reorder dates are computed from real data; writes
  reorder triggers downstream skills consume. Single mode (one SKU deep-dive) outputs .docx with
  confidence bands and scenarios. Bulk mode (full catalog) outputs .xlsx with 5 sheets including
  stockout-risk and reorder calendar. Use this skill when the user mentions inventory forecast,
  reorder point, safety stock, stockout, demand forecast, 'when do I need to reorder,' 'forecast my
  SKUs,' or 'how much should I order.'
---

# Inventory Forecaster

Forecasts 30/60/90-day inventory needs per SKU. Tiered methods (rolling average / Holt / Holt-Winters). Reads supplier lead times from the supplier memory cache; writes reorder triggers back. Single deep-dive or full-catalog bulk.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single SKU (default for one-product asks) or full-catalog bulk.
3. **Ingest sales data.** Shopify CSV / Amazon CSV / Etsy CSV / generic CSV — auto-detected by header signature.
4. **Map SKUs to suppliers.** Read `~/.the-ecommerce-seller/cache/suppliers/{id}.json` to pull lead times, MOQs, and payment terms per SKU. Ask buyer if a SKU has no mapped supplier yet.
5. **Pick forecast method per SKU.** Based on history depth + seasonal signal detection.
6. **Generate forecasts.** 30 / 60 / 90 day demand per SKU with confidence band.
7. **Compute stockout risk + reorder dates + quantities.** Factor in lead time, MOQ, safety stock, current on-hand.
8. **Write reorder triggers.** Anything needing reorder in next N days gets logged to `~/.the-ecommerce-seller/cache/reorder_triggers/{date}.json` for skill #11 to pick up.
9. **Render output.** Single mode → `.docx`. Bulk mode → `.xlsx` with 5 sheets.
10. **Report back.** File path, summary statistics, stockout-risk SKU count, reorder triggers written, suggested next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single SKU mode is the default when:**
- The user names one SKU specifically ("forecast the River Stone Pour-Over")
- The user asks "should I reorder X?"
- The user shares a single-SKU sales history

**Full-catalog bulk mode is the default when:**
- The user uploads a multi-SKU CSV
- The user says "forecast everything," "all my SKUs," "full catalog"
- The user asks "what do I need to reorder this quarter?"
- The user wants a stockout-risk report

Confirm out loud before proceeding.

---

## Step 3: Ingest sales data

Four ingestion paths, all map to a canonical schema:

### Canonical schema (post-parse)

```json
{
  "sku": "RS-POUR-OVER-001",
  "product_name": "River Stone Pour-Over",
  "date": "2026-03-14",
  "units_sold": 8,
  "revenue": 33.60,
  "channel": "shopify"
}
```

### Path A: Shopify Orders CSV

Export from Shopify Admin → Orders → Export → CSV (all orders). Skill aggregates line items by SKU + date.

Expected columns (subset): `Name`, `Created at`, `Lineitem name`, `Lineitem sku`, `Lineitem quantity`, `Lineitem price`.

### Path B: Amazon Business Reports CSV

Export from Seller Central → Reports → Business Reports → Detail Page Sales and Traffic by Child Item. Date-aggregated by SKU/ASIN.

Expected columns: `(Child) ASIN`, `Title`, `Units Ordered`, `Ordered Product Sales`, `Date`.

### Path C: Etsy stats CSV

Export from Etsy Shop Manager → Stats → Download CSV.

Expected columns: `Date`, `Listing ID`, `Listing title`, `Quantity sold`, `Revenue`.

### Path D: Generic multi-platform CSV

For buyers combining channels or using eBay/Walmart/TikTok Shop:

Required columns: `sku`, `date`, `units_sold` (and optionally `product_name`, `revenue`, `channel`).

Read `templates/csv-shapes.md` for the full parser logic and auto-detection signatures.

---

## Step 4: Map SKUs to suppliers

For each SKU in the sales data, look up the supplier:

1. Check `~/.the-ecommerce-seller/cache/sku_to_supplier.json` for an existing SKU→supplier mapping
2. If found, read the supplier file at `~/.the-ecommerce-seller/cache/suppliers/{supplier-id}.json` and pull:
   - `lead_time_days` (from supplier profile or per-product override)
   - `current_moq` (per product)
   - `current_unit_price_usd` (per product)
   - `payment_terms_in_force.structure` (for reorder calc — when does the deposit need to be sent?)
3. If no mapping found, prompt buyer for the supplier; auto-write the new mapping
4. If supplier file doesn't exist at all, fall back to buyer-provided lead time + MOQ

Read `templates/supplier-integration.md` for the full handoff logic.

---

## Step 5: Pick forecast method per SKU

Read `templates/forecast-methods.md` for the full decision tree. Summary:

| Data history | Method | Why |
|---|---|---|
| < 60 days | **Simple 14-day rolling average** with safety-stock multiplier | Not enough data for trend or seasonality. Rolling average is conservative + transparent. |
| 60-180 days | **Exponential smoothing (Holt's method)** | Captures trend (growing or declining velocity). Statsmodels `ExponentialSmoothing(trend='add')`. |
| 180+ days | **Seasonal decomposition (Holt-Winters)** | Captures trend + seasonality. Skill auto-detects seasonal signal via autocorrelation. If no seasonal signal, falls back to Holt. Statsmodels `ExponentialSmoothing(trend='add', seasonal='add', seasonal_periods=N)`. |

The seasonal period auto-detected:
- 7 days (weekly cycle — common for routine purchases)
- 30 days (monthly cycle — payday-correlated)
- 365 days (annual — holiday-correlated)

Method selection is transparent — the .docx and .xlsx report which method ran on which SKU and why.

---

## Step 6: Generate forecasts

For each SKU, compute:

- **30-day forecast**: expected units sold in next 30 days
- **60-day forecast**: cumulative through day 60
- **90-day forecast**: cumulative through day 90
- **Confidence band**: 80% confidence interval (10th-90th percentile range)
- **Per-day velocity**: forecasted units per day (current and over forecast window)

In single mode, the skill also outputs three scenarios per SKU:

- **Conservative** (P10 — lowest 10th percentile demand)
- **Base** (P50 — median forecast)
- **Aggressive** (P90 — highest 90th percentile demand)

Buyers reorder for the base case but stock for the aggressive case (the safety stock layer).

---

## Step 7: Compute stockout risk + reorder dates + quantities

Read `templates/reorder-calc.md` for the full math. Summary formula:

```
days_until_stockout = current_on_hand / per_day_velocity_p50

if days_until_stockout < lead_time_days:
    STOCKOUT RISK — already too late to reorder fully; partial coverage at best
elif days_until_stockout < (lead_time_days + safety_stock_days):
    URGENT REORDER — order immediately
elif days_until_stockout < (lead_time_days + safety_stock_days + reorder_window_days):
    REORDER SOON — schedule in next 7-14 days
else:
    HEALTHY — no action

reorder_quantity = max(
    MOQ,
    forecast_for_lead_time_period + safety_stock_buffer
)

deposit_date = today + days_to_send_deposit_to_meet_lead_time
ship_date = deposit_date + (lead_time_days)
arrive_date = ship_date + transit_days
```

The reorder calc accounts for the supplier's payment terms:
- 100% upfront: deposit_date = order_decision_date
- 30/70 TT: deposit_date triggers the 30%; balance triggers later
- NET 30: deposit_date is later, but the order still has to be placed earlier

So the actual *order placement date* depends on when the supplier needs the deposit, which depends on payment terms.

---

## Step 8: Write reorder triggers

For each SKU that needs reorder within the next 30 days, append to:

```
~/.the-ecommerce-seller/cache/reorder_triggers/{YYYY-MM-DD}.json
```

Where the date is the forecast run date. The trigger file contains:

```json
{
  "forecast_run_at": "2026-04-15",
  "triggers": [
    {
      "sku": "RS-POUR-OVER-001",
      "product_name": "River Stone Pour-Over",
      "supplier_id": "shenzhen-stoneworks-co-ltd-cindy-chen",
      "urgency": "urgent",
      "days_until_stockout": 18,
      "lead_time_days": 45,
      "recommended_reorder_quantity": 1500,
      "recommended_deposit_date": "2026-04-15",
      "expected_arrive_date": "2026-06-12",
      "current_unit_price_usd": 4.20,
      "estimated_reorder_cost_usd": 6300,
      "notes": "Lead time exceeds days-until-stockout — expedite or expect partial stockout"
    },
    ...
  ]
}
```

Skill #11 (Supplier Negotiation Assistant) reads this cache when buyer says "what do I need to reorder this week?" — it can draft reorder letters automatically to the suppliers.

The skill writes the cache atomically; the buyer can edit / delete trigger entries before they flow downstream.

---

## Step 9: Render output

### Single SKU mode

Use `scripts/render_forecast_docx.py`. Structure:

```
Forecast: [Product name] (SKU: [SKU])
Generated: [date]  ·  Method: [Holt-Winters seasonal, 7-day period]

══════════════════════════════════════════════════
DATA SUMMARY
══════════════════════════════════════════════════
- History window: 2025-01-15 to 2026-04-15 (456 days)
- Total units sold: [N]
- Average daily velocity: [X.X] units/day
- Seasonal signal detected: [Weekly cycle, 7-day period, amplitude ±18%]
- Trend: [Growing 1.2% week-over-week]

══════════════════════════════════════════════════
METHOD CHOICE + RATIONALE
══════════════════════════════════════════════════
Method: [Holt-Winters (additive seasonal)]
Why: [180+ days history + seasonal autocorrelation at 7-day lag (r=0.42) above threshold (r=0.30)]
Confidence in method: [High — 6+ seasonal cycles observed]

══════════════════════════════════════════════════
30 / 60 / 90 DAY FORECAST
══════════════════════════════════════════════════
30-day demand:
  Conservative (P10): [N] units
  Base (P50): [N] units
  Aggressive (P90): [N] units

60-day demand:
  Conservative: [N], Base: [N], Aggressive: [N]

90-day demand:
  Conservative: [N], Base: [N], Aggressive: [N]

══════════════════════════════════════════════════
STOCKOUT RISK + REORDER MATH
══════════════════════════════════════════════════
Current on-hand: [N] units
Velocity (base case): [X.X] units/day
Days until stockout: [N] days  →  Status: [URGENT REORDER]

Supplier: [Company name] ([Region], stage: [established])
Lead time: [N] days
MOQ: [N] units
Current unit price: $[X.XX]
Payment terms: [30/70 TT before shipping]

Recommended action:
- Reorder quantity: [N] units
- Send deposit by: [date]
- Expected arrival: [date]
- Estimated cost: $[XXX]
- Cover period: [N] days after arrival at base velocity

══════════════════════════════════════════════════
RISKS + ASSUMPTIONS
══════════════════════════════════════════════════
- [Forecast assumes the seasonal pattern continues]
- [Lead time assumes no Lunar New Year overlap]
- [Safety stock buffer: 14 days of base-case velocity]
- [Confidence band reflects historical variance; novel events (viral moment, supply disruption) not captured]

══════════════════════════════════════════════════
NEXT STEPS
══════════════════════════════════════════════════
1. Place reorder by [date] via skill #11 (Supplier Negotiation Assistant)
2. Reorder trigger has been written to cache for downstream pickup
3. Re-run forecast in 14 days to monitor velocity drift
```

Save to `config.output_folder` as `inventory_forecast_{sku-slug}_{date}.docx`.

### Full-catalog bulk mode

Use `scripts/render_catalog_xlsx.py`. Five-sheet workbook:

**Sheet 1: SKU Forecast** — one row per SKU with:
- SKU, product name, supplier, channel
- History days, method used, seasonal signal detected
- Current on-hand, velocity (units/day), days until stockout
- 30/60/90-day forecast (base case)
- Status (Healthy / Reorder Soon / Urgent / Stockout Risk) — color-coded
- Recommended reorder quantity, deposit date, expected arrival
- Estimated reorder cost

**Sheet 2: Stockout Risk** — filtered view of just at-risk SKUs:
- Top 20 by urgency (days-until-stockout vs. lead time gap)
- Action plan column the buyer fills in
- Cost-of-stockout estimate (forecast × unit margin × days short)

**Sheet 3: Reorder Calendar** — chronological:
- Rows are dates, sorted ascending
- Columns are recommended actions per date
- "Send Cindy Chen the reorder letter for River Stone Pour-Over by April 22 (deposit due April 25)"
- Read like a calendar — buyer can scan the next 90 days at a glance

**Sheet 4: Seasonality Patterns** — for SKUs with 180+ day history:
- SKU, seasonal period detected, amplitude, last cycle peak/trough
- Helps the buyer plan promotional calendar around organic demand peaks

**Sheet 5: Method Audit Log** — for transparency:
- Each SKU's history depth, method selected, why, confidence in method
- Buyer can spot when a SKU just hit the 60-day threshold (method change incoming)
- Buyer can override method per SKU in their next forecast run

Save to `config.output_folder` as `inventory_catalog_forecast_{date}.xlsx`.

---

## Step 10: Report back

Tell the buyer:
1. Where the file is (`computer://` link)
2. SKU count + summary statistics (median velocity, total stockout-risk count, etc.)
3. Top 3 urgent reorders (SKU + recommended date)
4. Reorder trigger summary ("12 triggers written to cache; skill #11 will see these when drafting next supplier letters")
5. Suggested next step:
   - If stockouts are imminent: "Address the urgent reorders today; the supplier negotiation skill has the triggers ready"
   - If catalog is healthy: "Re-run in 14 days to monitor; no immediate action needed"
   - If many SKUs lack supplier mapping: "Map remaining SKUs to suppliers via the SKU→supplier prompt before next forecast for cleaner reorder math"

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill works on Shopify CSV; flags direct API pull as upgrade |
| Amazon Seller Central | Skill works on Amazon CSV exports |
| Supplier memory cache (skill #11) | Skill drafts forecasts; flags missing supplier mapping; buyer enters lead times manually for unmapped SKUs |

The skill always produces a forecast — connectors enrich.

---

## Edge cases

- **Brand-new SKU with no history**: skill flags as "no history — buyer-set initial assumptions"; recommends conservative initial order at MOQ × 1.5 with reforecast after 30 days
- **SKU with sporadic sales (long zero-stretches)**: rolling average and Holt both struggle; skill uses median + buffer instead and flags as "sporadic — high variance"
- **One-time spike (viral moment)**: skill detects outlier days (3+ standard deviations from mean) and flags but does NOT exclude from forecast — the buyer decides whether the spike is a new normal or a one-off
- **SKU discontinued**: buyer can mark as discontinued in `inventory_forecasting.discontinued_skus`; skill skips it
- **Multi-variant product (sizes / colors)**: skill forecasts per variant SKU; provides parent-product roll-up in bulk mode
- **Stockout history (zero sales because out of stock, not because of no demand)**: skill cannot distinguish — flags days with zero sales but recent positive sales as "potential stockout days" and asks buyer to confirm
- **Drop-shipped SKUs (no lead time, infinite stock)**: skill flags as "drop-ship — no reorder needed" if `is_dropshipped: true` in SKU metadata
- **Manufactured-on-demand SKUs**: similar — skill flags and skips reorder calc; only forecasts demand
- **Seasonal-only SKUs**: skill detects out-of-season periods and reforecast schedule + reorder timing around in-season ramp

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema (extended with inventory_forecasting section)
- `templates/csv-shapes.md` — Shopify / Amazon / Etsy / generic CSV parsers + auto-detection
- `templates/forecast-methods.md` — tiered method decision tree + statsmodels usage
- `templates/seasonality-detection.md` — autocorrelation-based seasonal signal detection
- `templates/reorder-calc.md` — stockout-risk + reorder-quantity + deposit-date math
- `templates/safety-stock.md` — safety stock buffer rationale + multiplier guidance
- `templates/supplier-integration.md` — SKU→supplier mapping + reading lead times from skill #11
- `templates/reorder-triggers.md` — schema for the reorder triggers cache + handoff to skill #11
- `templates/audit-log.md` — method-by-SKU audit conventions for transparency
- `scripts/config_loader.py` — shared config loader
- `scripts/sales_csv_parser.py` — multi-platform CSV parser with auto-detection
- `scripts/forecast_engine.py` — tiered forecasting (rolling avg / Holt / Holt-Winters)
- `scripts/supplier_memory_reader.py` — reads supplier memory cache from skill #11
- `scripts/reorder_trigger_writer.py` — writes reorder triggers cache for skill #11
- `scripts/render_forecast_docx.py` — single SKU forecast .docx renderer
- `scripts/render_catalog_xlsx.py` — full-catalog .xlsx renderer (5 sheets)
- `examples/single-sku-deep-dive-example.md`
- `examples/full-catalog-bulk-example.md`
- `examples/mixed-history-example.md`
