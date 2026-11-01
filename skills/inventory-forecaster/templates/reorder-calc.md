# Reorder Calculation — Stockout Risk + Reorder Quantity + Deposit Date

The core math that turns "forecast" into "actionable action."

## Inputs per SKU

```
on_hand_units:               current physical inventory
velocity_p50:                forecasted units/day (base case)
velocity_p90:                forecasted units/day (aggressive case)
lead_time_days:              from supplier memory (or buyer-provided)
transit_days:                from supplier memory (or default by region — China 30, Vietnam 25, NA 5, etc.)
moq:                         from supplier memory (per SKU)
safety_stock_days:           buyer-configured (default 14 days at base velocity)
reorder_window_days:         buyer-configured (default 14 days) — how much advance notice you want before "urgent"
payment_terms_structure:     from supplier memory ("100_upfront", "30_70_tt_before_ship", "30_70_tt_after_bl", "net_30", etc.)
days_to_send_deposit:        derived from payment_terms (varies by terms)
```

## Stockout risk classification

```python
def classify_stockout_risk(on_hand, velocity_p50, lead_time, safety_stock_days, reorder_window_days):
    days_until_stockout = on_hand / velocity_p50 if velocity_p50 > 0 else 9999

    if days_until_stockout < lead_time:
        return "stockout_imminent"      # already too late for full coverage
    elif days_until_stockout < (lead_time + safety_stock_days):
        return "urgent_reorder"          # order now to avoid stockout after lead time
    elif days_until_stockout < (lead_time + safety_stock_days + reorder_window_days):
        return "reorder_soon"            # order within reorder window
    else:
        return "healthy"
```

## Days-until-stockout — base vs. aggressive case

For risk surfacing, the skill computes BOTH:
- `days_until_stockout_p50`: at base velocity
- `days_until_stockout_p90`: at aggressive velocity (in case demand spikes)

If `days_until_stockout_p90 < lead_time` even when p50 looks fine, the skill warns "demand spike scenario would stockout — consider ordering early."

## Reorder quantity

Goal: order enough to cover from arrival date through next-reorder date, plus safety stock.

```python
def recommended_reorder_quantity(
    velocity_p50,
    lead_time,
    transit,
    next_reorder_cycle_days,    # how many days the order should cover (default: 60-90)
    safety_stock_days,
    moq,
):
    coverage_days = lead_time + transit + next_reorder_cycle_days + safety_stock_days
    raw_quantity = velocity_p50 * coverage_days
    return max(moq, raw_quantity)
```

The MOQ floor enforces the supplier's minimum. When MOQ exceeds raw_quantity meaningfully (e.g., raw = 200 but MOQ = 500), the skill flags "ordering above forecast — consider negotiating lower MOQ via skill #11."

## Reorder cycle considerations

The buyer decides how often to reorder:
- **Reorder every 30 days**: more frequent, smaller orders, higher inventory turnover, more cash flow flexibility
- **Reorder every 60-90 days**: less frequent, larger orders, better bulk pricing
- **Reorder every 6+ months**: long-lead-time products (sea freight, slow-velocity)

The skill defaults to 60-day reorder cycles but adjusts per SKU:
- Velocity > 10/day: 30-day cycle (frequent reorders, lighter inventory)
- Velocity 1-10/day: 60-day cycle (balanced)
- Velocity < 1/day: 90+ day cycle (large but infrequent)

## Deposit date

When does the buyer actually need to send the deposit? Depends on payment terms:

```python
def deposit_date(reorder_decision_date, payment_terms_structure):
    if payment_terms_structure == "100_upfront":
        return reorder_decision_date
    elif payment_terms_structure == "30_70_tt_before_ship":
        # Supplier starts production after 30% deposit
        return reorder_decision_date
    elif payment_terms_structure == "30_70_tt_after_bl":
        # Supplier starts production after 30% deposit, balance after B/L
        return reorder_decision_date
    elif payment_terms_structure == "lc_at_sight":
        # LC opening takes 3-5 business days at bank
        return reorder_decision_date - 5_business_days  # buyer initiates LC earlier
    elif payment_terms_structure == "net_30":
        # No deposit; ship first, pay 30 days after invoice
        return shipped_date + 30
    elif payment_terms_structure == "net_60":
        return shipped_date + 60
    else:
        return reorder_decision_date
```

The skill renders this in the .docx as:
- "Send 30% deposit by [date]"
- "Open LC by [date]" (if LC terms)
- "Issue PO by [date]; payment due [date]" (NET terms)

## Expected arrive date

```python
def expected_arrive_date(reorder_decision_date, lead_time, transit):
    return reorder_decision_date + lead_time + transit
```

The skill assumes:
- Lead time starts when deposit is received (for upfront/deposit-based terms)
- Lead time is calendar days (not business days), unless supplier memory says otherwise
- Transit is calendar days

Transit defaults by region (when supplier memory doesn't have it):
- China (sea freight): 30 days
- China (air freight): 7 days
- Vietnam (sea): 25 days
- Vietnam (air): 5 days
- India (sea): 28 days, (air): 4 days
- North America: 3-5 days
- EU to US: 10-14 days

## Safety stock buffer

```python
def safety_stock(velocity_p50, velocity_p90, safety_stock_days):
    """
    Safety stock buffers against demand variability + lead-time variability.
    """
    base_buffer = velocity_p50 * safety_stock_days
    # Add demand-variance buffer: difference between p90 and p50 over lead time
    variance_buffer = (velocity_p90 - velocity_p50) * safety_stock_days
    return base_buffer + variance_buffer
```

Default `safety_stock_days = 14`. The buyer can configure per SKU or globally.

Some SKUs warrant more safety stock:
- High-margin SKUs (cost of stockout > cost of holding excess)
- SKUs with unreliable suppliers (lead-time variance)
- SKUs with volatile demand (high p90/p50 ratio)
- SKUs that drive accessory sales (stockout of hero SKU kills accessory orders too)

Other SKUs warrant less:
- Low-margin SKUs (holding cost > stockout cost)
- Easily-substitutable SKUs (customer buys alternative)
- Slow-moving SKUs (already have lots of days of cover)

Safety stock multiplier presets in config:
```json
"inventory_forecasting": {
  "safety_stock_defaults": {
    "default_days": 14,
    "hero_skus": 21,
    "high_margin_skus": 21,
    "low_margin_skus": 7
  }
}
```

## Order timing summary table

For each SKU, the .docx and .xlsx report:

| Field | Value |
|---|---|
| Status | `urgent_reorder` |
| Current on-hand | 220 units |
| Velocity (P50) | 12 units/day |
| Days until stockout | 18 days |
| Lead time | 45 days |
| Transit | 30 days (sea freight from China) |
| **Critical date — send deposit by** | **2026-04-15** |
| Expected ship date | 2026-05-30 |
| Expected arrive date | 2026-06-29 |
| **Days short before arrival** | **57 days short** ← warning |
| Recommended reorder quantity | 1500 units (MOQ 1500) |
| Cover period after arrival | 125 days at base velocity |
| Estimated reorder cost | $6,300 (1500 × $4.20) |

The "days short" warning surfaces when reorder timing missed the safe window — the buyer either expedites (air freight, smaller order to bridge) or accepts some stockout.

## Expedited-delivery option

For stockout-imminent SKUs, the skill suggests two paths:

1. **Air freight** the next order (reduces transit from 30 days to 5-7 days; cost is 3-5× sea freight per kg)
2. **Bridge order** — small order from a US-based supplier or warehouse to cover the gap; reorder from primary supplier as normal

The skill estimates cost differential and recommends if cost-of-stockout > cost-of-expediting.

## Cost-of-stockout estimation

```python
def cost_of_stockout(velocity_p50, days_short, unit_margin_usd):
    units_lost = velocity_p50 * days_short
    return units_lost * unit_margin_usd
```

If cost-of-stockout > 3× the cost of expediting, the skill recommends expediting. Below that threshold, the skill recommends accepting the stockout.

## Buyer overrides

The buyer can override per SKU:
- Force a different reorder cycle (`reorder_cycle_days`)
- Force a different safety stock (`safety_stock_days`)
- Skip the SKU (`skip_reorder_calc: true`) — useful for drop-ship, made-to-order

Overrides live in config:
```json
"inventory_forecasting": {
  "sku_overrides": {
    "RS-POUR-OVER-001": {
      "reorder_cycle_days": 45,
      "safety_stock_days": 21
    }
  }
}
```
