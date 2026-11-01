# Single SKU Deep Dive — Reference Example

Shows what gets produced when the buyer asks "Forecast the River Stone Pour-Over and tell me when I need to reorder."

**Brand:** {{brand_name}}
**SKU:** RS-POUR-OVER-001 (River Stone Pour-Over Mug, hero ceramic SKU)
**Method selected:** Holt-Winters (seasonal exponential smoothing, 7-day period)
**Output:** Single `.docx`

---

## Input

- Sales history: 456 days (15 months) from Shopify Orders CSV
- Current on-hand: 220 units
- Supplier: Shenzhen Stoneworks Co., Ltd. (Cindy Chen) — from supplier memory cache
- Lead time: 45 days (from supplier memory)
- Transit: 30 days (sea freight, from supplier memory)
- MOQ: 1500 units (from sku_to_supplier mapping)
- Unit price: $4.20 (from supplier memory)
- Payment terms: 30/70 TT before shipping (from supplier memory)

---

## .docx output structure

```
Forecast: River Stone Pour-Over Mug
SKU: RS-POUR-OVER-001  ·  Method: Holt-Winters (seasonal, 7-day)  ·  Generated 2026-04-15
Confidence: high
```

### DATA SUMMARY
- History days: 456
- First sale: 2025-01-15
- Last sale: 2026-04-15
- Total units sold (history): 5,612
- Average daily velocity: 12.3 units/day
- Seasonal signal: 7-day period (autocorrelation 0.42)
- Trend: Growing 1.2% week-over-week

### METHOD CHOICE + RATIONALE
- **Method**: Holt-Winters (seasonal exponential smoothing)
- **Why**: 180+ days of history (456 days observed) combined with detected weekly seasonal signal (autocorrelation 0.42 at 7-day lag, well above the 0.30 threshold). The data shows clear weekday/weekend rhythm with consistent amplitude across 65 cycles.

### 30 / 60 / 90 DAY FORECAST
- **30-day demand**:
  - Conservative (P10): 330 units
  - Base (P50): 390 units
  - Aggressive (P90): 450 units
- **60-day demand**:
  - Conservative: 660, Base: 780, Aggressive: 900
- **90-day demand**:
  - Conservative: 990, Base: 1,170, Aggressive: 1,350

### STOCKOUT RISK + REORDER MATH

**Status: URGENT REORDER**

- Current on-hand: 220 units
- Velocity (P50): 12.3 units/day
- Days until stockout (P50): 18 days
- Days until stockout (P90 — demand spike): 13 days

**Supplier + reorder structure**:
- Lead time: 45 days
- Transit: 30 days (sea freight)
- MOQ: 1500 units
- Payment terms in force: 30_70_tt_before_shipping

**Recommended action**:
- Reorder quantity: 1,500 units (MOQ)
- Send deposit by: 2026-04-15
- Expected arrival: 2026-06-29
- Estimated reorder cost: $6,300.00
- ⚠ **57 days short before arrival** — consider expediting via air freight or accepting partial stockout.

### WARNINGS
- None on this SKU. Confident forecast.

### NEXT STEPS
1. Stockout will happen before reorder can arrive. Decide: expedite via air freight (reduces transit from 30 days to 7), or accept partial stockout for 57 days.
2. Trigger written to `<plugin-root>/.cache/reorder_triggers/2026-04-15.json` — Skill #11 (Supplier Negotiation Assistant) will surface this when drafting next supplier letters.
3. Plan customer communication if stockout is unavoidable (waitlist signup, expected restock date messaging).

---

## Reorder trigger written

To `<plugin-root>/.cache/reorder_triggers/2026-04-15.json`:

```json
{
  "sku": "RS-POUR-OVER-001",
  "product_name": "River Stone Pour-Over Mug",
  "supplier_id": "shenzhen-stoneworks-co-ltd-cindy-chen",
  "urgency": "urgent",
  "trigger_reason": "Days until stockout (18) < lead time (45) + safety stock (14)",
  "current_on_hand": 220,
  "velocity_p50_units_per_day": 12.3,
  "velocity_p90_units_per_day": 16.8,
  "days_until_stockout_p50": 18,
  "lead_time_days": 45,
  "transit_days": 30,
  "moq": 1500,
  "recommended_reorder_quantity": 1500,
  "recommended_deposit_date": "2026-04-15",
  "expected_arrive_date": "2026-06-29",
  "days_short_before_arrival": 57,
  "estimated_reorder_cost_usd": 6300.00,
  "expedite_suggested": true,
  "notes": "Lead time exceeds days-until-stockout by 57 days — consider air-freight expedite or accept partial stockout.",
  "consumed_by_skill_11": false
}
```

---

## What the buyer does next

1. Decide between air-freight expedite vs. accept stockout (cost of expediting ~$2,500 extra; cost of stockout = 57 days × 12.3 units × $X margin)
2. Run skill #11 (Supplier Negotiation Assistant) and say "draft reorder letters for the triggers from today's forecast" — skill #11 reads the trigger and drafts a region-aware reorder letter to Cindy
3. Send the letter; track via supplier memory
4. Re-forecast in 7 days to confirm

---

## Why this skill saves time

Manually:
- Pull sales history from Shopify, clean it: 15 min
- Compute velocity, identify seasonality (intuitively or in a spreadsheet): 30 min
- Look up supplier lead time / MOQ / payment terms from past invoices: 15 min
- Calculate days-until-stockout vs. lead time: 5 min
- Decide reorder quantity: 10 min
- Realize the stockout-imminent issue too late: priceless (negative ROI)
- **Total: 1+ hour, with seasonality usually missed**

With this skill:
- Skill runs: ~10 seconds
- Buyer reviews + acts: ~5 min
- **Total: ~5 min, with seasonality auto-detected + reorder trigger written for skill #11**

The real value: catching urgent reorders 4-6 weeks earlier than manual review surfaces them. For a hero SKU like River Stone Pour-Over, that's the difference between a smooth Q3 and a 2-month stockout that kills momentum.
