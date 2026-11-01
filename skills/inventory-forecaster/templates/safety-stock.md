# Safety Stock — Buffer Against Demand and Lead-Time Variance

Safety stock is the extra inventory you hold above expected demand to avoid stockouts when reality deviates from forecast. Getting this right is the difference between "I never stockout" and "I'm tying up $50K in inventory I don't need."

## The two sources of variance

1. **Demand variance**: customers don't buy at the average rate every day. Some days are higher, some lower.
2. **Lead-time variance**: suppliers don't always deliver in exactly N days. Sometimes 45, sometimes 60.

Safety stock buffers both.

## Default formula

```
safety_stock_units = velocity_p50 × safety_stock_days  +  (velocity_p90 - velocity_p50) × lead_time_days
```

Two components:
- **Steady-state buffer**: `velocity_p50 × safety_stock_days` — covers the buyer's reaction window if demand stays at base velocity
- **Demand-spike buffer**: `(velocity_p90 - velocity_p50) × lead_time_days` — covers the case where demand spikes during the lead time

## Default values

- `safety_stock_days = 14` (two-week reaction window)
- The demand-spike multiplier is implicit (uses P90 from the forecast)

## Tuning safety stock by SKU type

| SKU type | Recommended safety_stock_days | Why |
|---|---|---|
| Hero SKU (>30% of revenue) | 21-28 days | Stockout is catastrophic; over-stock is acceptable |
| High-margin SKU (>50% margin) | 21 days | Cost of stockout >> cost of holding |
| Average SKU | 14 days | Default |
| Low-margin SKU (<20% margin) | 7-10 days | Cost of holding > cost of one-time stockout |
| Replenishable / substitutable SKU | 7-10 days | Customer buys alternative if stockout |
| Drop-ship SKU | 0 days (skip) | No inventory held |
| Seasonal SKU (out-of-season) | Low or zero buffer | Hold next year's inventory, not current |

## Tuning safety stock by supplier reliability

Lead-time variance matters as much as demand variance:

| Supplier reliability | Multiplier |
|---|---|
| Highly reliable (lead times within ±5%) | 1.0× |
| Moderate reliability (±15% lead time) | 1.3× |
| Low reliability (±25% lead time) | 1.7× |
| Unknown reliability (new supplier) | 1.5× |

The skill reads supplier reliability from `lead_time_variance_observed` in supplier memory if available; falls back to 1.5× for new suppliers.

## Tuning safety stock by season

Just before high-demand periods (December, holidays, summer for relevant SKUs):
- Increase safety stock by 30-50% for the season
- Decrease back to baseline after the season

The skill checks the seasonality detection result and recommends seasonal safety stock adjustments in the .docx.

## Service-level approach

Some operators set safety stock based on a target service level (probability of NOT stocking out):

| Service level | Z-score | Safety stock multiplier |
|---|---|---|
| 90% (1 stockout per 10 cycles) | 1.28 | 1.28 × stdev × sqrt(lead_time) |
| 95% (1 stockout per 20 cycles) | 1.65 | 1.65 × stdev × sqrt(lead_time) |
| 98% (1 stockout per 50 cycles) | 2.05 | 2.05 × stdev × sqrt(lead_time) |
| 99% (1 stockout per 100 cycles) | 2.33 | 2.33 × stdev × sqrt(lead_time) |

```python
def safety_stock_service_level(daily_demand_stdev, lead_time_days, service_level_z):
    return service_level_z * daily_demand_stdev * math.sqrt(lead_time_days)
```

The skill defaults to days-based safety stock (simpler) but can switch to service-level mode if the buyer prefers:

```json
"inventory_forecasting": {
  "safety_stock_mode": "service_level",
  "service_level_target": 0.95
}
```

## Carrying cost vs. stockout cost tradeoff

Holding extra inventory costs money:
- Cost of capital tied up
- Warehouse / storage cost
- Risk of obsolescence
- Insurance

Annual carrying cost is typically 20-30% of inventory value. So $10,000 of safety stock costs $2,000-$3,000/year to carry.

Stockout cost:
- Lost margin × units short
- Lost customer lifetime value if first-time customer experiences stockout
- Lost word-of-mouth
- Wholesale customer penalty if applicable

A rough rule:
- If stockout cost > 5× annual carrying cost → carry more safety stock
- If stockout cost < 2× annual carrying cost → carry less
- Hero / first-touchpoint SKUs almost always warrant more safety stock than the math suggests because the LTV impact of a first-stockout is hard to quantify but real

## Buyer-friendly safety stock recommendations

The skill outputs safety stock recommendations as:

```
SAFETY STOCK RECOMMENDATION
Current setting: 14 days
Recommendation:  21 days (raise by 7)
Why:
  - This is a hero SKU (32% of brand revenue)
  - Supplier lead-time variance observed at ±18% (medium reliability)
  - Cost-of-stockout estimate: $X — 6× higher than additional carrying cost
  - Heading into Q4 peak season — raising the buffer preemptively
```

Recommendations are surfaced but never auto-applied. Buyer decides.

## Common safety stock mistakes

1. **One-size-fits-all** — applying the same days to every SKU. Hero SKUs need more; drop-ship needs zero.
2. **Setting it once and forgetting** — safety stock should be reviewed quarterly as supplier reliability and demand patterns shift.
3. **Treating safety stock as "buffer that's always there"** — safety stock is meant to be drawn down occasionally; if you never dip into it, you have too much.
4. **Ignoring lead-time variance** — assuming the supplier always delivers in 45 days is naïve.
5. **Confusing safety stock with reorder point** — safety stock is the buffer below the reorder point; reorder point is when you trigger the next order.

## Re-calibration cadence

The skill recommends reviewing safety stock per SKU:
- **Monthly** for hero / volatile SKUs
- **Quarterly** for most SKUs
- **Annually** for slow-moving / drop-ship

The audit log tracks each SKU's last safety-stock review date.
