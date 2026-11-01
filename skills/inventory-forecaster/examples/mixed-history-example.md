# Mixed-History Example — Method Transparency

Shows how the skill picks different methods for different SKUs in the same catalog and explains why. Useful for buyers who want to understand the audit log before trusting forecasts.

**Brand:** Hypothetical wellness brand
**Scope:** 6 representative SKUs covering all method tiers
**Focus:** Method selection logic, not the forecasts themselves

---

## The 6 SKUs

| SKU | Lifecycle | History | Velocity | Pattern |
|---|---|---|---|---|
| WELLNESS-OIL-A | Established hero | 720 days | 18/day | Clear weekly + annual seasonality |
| WELLNESS-OIL-B | Established | 280 days | 7/day | Mild weekly seasonality |
| ROLLER-NEW | New launch | 45 days | 9/day | Too short for trend detection |
| GIFT-CARD-BUNDLE | Holiday only | 540 days | 0.3/day avg | Annual cycle, sporadic |
| LIMITED-EDITION-XYZ | Discontinued | 90 days | 0.2/day | Sporadic + ending |
| DROPSHIP-SAMPLE | Drop-ship | n/a | n/a | Skip |

---

## Method selection per SKU + rationale

### WELLNESS-OIL-A → Holt-Winters (annual cycle, 365-day period)

```
Method: holt_winters
Rationale: 720 days history (well above 180-day threshold) + seasonal signal detected at 365-day lag (autocorr 0.68) and 7-day lag (autocorr 0.41).
Picked 365-day period because annual signal is stronger.
Confidence: high
Seasonal amplitude: ±32% around mean (December peaks, January troughs)
```

Why this matters: the forecast for December 2026 will be significantly higher than a naïve linear extrapolation, because the seasonal component captures the holiday surge.

### WELLNESS-OIL-B → Holt (no seasonal signal)

```
Method: holt
Rationale: 280 days history (60-180 threshold), but at the higher end. Autocorrelation check found weekly signal at 0.27 — below the 0.30 threshold for seasonal mode. Falling back to Holt for trend.
Confidence: medium
Note: Seasonal signal is borderline. If 2 more full weekly cycles confirm, the skill may upgrade to Holt-Winters next forecast.
```

Why this matters: the skill is appropriately conservative. A weak signal could be coincidence; waiting for stronger evidence is the right call.

### ROLLER-NEW → Rolling Average 14-day

```
Method: rolling_average_14d
Rationale: 45 days history (below 60-day threshold for Holt). Rolling average is the robust choice for new SKUs.
Confidence: low
Warning: low_history
Note: At day 60, the skill will upgrade to Holt and the forecast may shift.
```

Why this matters: don't apply Holt to 45 days of data — the trend coefficient is too noisy to trust. The simpler method is safer.

### GIFT-CARD-BUNDLE → Holt-Winters (365-day) or sporadic fallback

```
Method: poisson_heuristic
Rationale: 540 days history but >50% of days have zero sales, and average velocity 0.3/day. Below sporadic threshold (0.5/day with >30% zero days). Poisson heuristic is more accurate than Holt for this pattern.
Confidence: low
Warnings: velocity_below_threshold, sporadic_sales
Note: The skill won't use Holt-Winters here because despite the long history, the data is too zero-stuffed for the model to fit cleanly.
```

Why this matters: long history doesn't always mean Holt-Winters is appropriate. The forecast engine reads the underlying data character, not just the day count.

### LIMITED-EDITION-XYZ → Skipped (discontinued)

```
Method: skipped
Rationale: SKU is marked discontinued in config. No reorder needed; no forecast required.
Confidence: n/a
```

The buyer can mark SKUs as discontinued in `inventory_forecasting.discontinued_skus`, and the skill respects that without producing a forecast.

### DROPSHIP-SAMPLE → Skipped (drop-ship)

```
Method: skipped
Rationale: SKU is marked as drop-ship in config (no inventory held). No reorder math applies.
Confidence: n/a
```

---

## The audit log surfaces method changes over time

In subsequent forecast runs, the audit will show transitions:

- ROLLER-NEW at day 45: rolling_average_14d
- ROLLER-NEW at day 75: holt (now eligible)  ← method upgraded
- ROLLER-NEW at day 200: holt or holt_winters (depending on seasonal signal that develops)

The buyer sees "ROLLER-NEW: method changed from rolling_average to Holt this run — investigate whether forecast moves meaningfully."

---

## What this teaches the buyer

1. **Method choice is driven by data, not assumption** — the skill picks based on history depth + seasonal signal, not on what the buyer "thinks" the SKU is
2. **Long history doesn't always mean fancy method** — sporadic SKUs use Poisson heuristic regardless of history length
3. **Borderline signals don't trigger upgrades** — autocorrelation just below threshold means Holt, not Holt-Winters
4. **New SKUs get conservative treatment** — rolling average is the right call below 60 days
5. **Discontinued / drop-ship SKUs are skipped cleanly** — no forecast noise

---

## How to override method when warranted

The buyer can override methods per SKU:

```json
"inventory_forecasting": {
  "method_overrides": {
    "WELLNESS-OIL-B": "holt_winters"   // Buyer wants seasonal mode even with weak signal
  }
}
```

The skill respects the override but flags "method_override_questionable" if the data doesn't support it (e.g., applying Holt-Winters to 30 days of history). The buyer can see this in the audit and decide whether the override is wise.

---

## When to trust the method choice

- **High confidence**: trust the forecast as the primary signal
- **Medium confidence**: trust the direction but treat numbers as approximate; cross-check against gut
- **Low confidence**: use forecast as one input among several; don't over-rely
- **Unreliable**: forecast is a guess; consider manual estimation instead

The .xlsx confidence column is color-coded so the buyer can prioritize attention.

---

## Real-world correspondence

These tiers map to common e-commerce patterns:

- **High confidence** SKUs are usually hero products with long histories and stable patterns. The forecast is reliable enough to drive reorder decisions automatically.
- **Medium confidence** SKUs are establishing or have moderate variability. Forecast is directionally useful but warrants a human sanity check.
- **Low confidence** SKUs are new, sporadic, or have noisy data. Forecast is a starting point; the buyer's domain knowledge matters more.
- **Unreliable** SKUs lack enough data to model. Buyer relies on intuition until more data arrives.

---

## Bottom line

The audit transparency is itself the value-add. A buyer who understands *why* the forecast picked Holt-Winters vs. Holt vs. Poisson can:
1. Build trust in the system
2. Override intelligently when domain knowledge contradicts the choice
3. Plan when SKUs will transition to better methods (e.g., "in 30 days, ROLLER-NEW becomes Holt-eligible — re-forecast then")
4. Communicate forecast logic to partners, accountants, lenders without hand-waving
