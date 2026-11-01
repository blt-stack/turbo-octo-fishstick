# Audit Log — Method Selection + Forecast Transparency

Every forecast run logs which method was chosen per SKU and why. The buyer can review this to spot when methods change, when confidence is low, and where the skill's choices warrant a manual override.

## Where the audit lives

- **Single mode**: in the .docx output under "METHOD CHOICE + RATIONALE"
- **Bulk mode**: as Sheet 5 ("Method Audit Log") in the .xlsx
- **Forecast run record**: `~/.the-ecommerce-seller/cache/forecast_runs/{YYYY-MM-DD-HHMM}.json` — full audit per run, including per-SKU diagnostics

## What gets logged per SKU

```json
{
  "sku": "RS-POUR-OVER-001",
  "product_name": "River Stone Pour-Over",
  "forecast_run_id": "fc-2026-04-15-1030",
  "history_days": 456,
  "first_sale_date": "2025-01-15",
  "last_sale_date": "2026-04-15",
  "total_units_sold_history": 5612,
  "method_selected": "holt_winters",
  "method_rationale": "180+ days history; seasonal autocorrelation at 7-day lag = 0.42 (threshold 0.30)",
  "seasonal_period_detected": 7,
  "seasonal_amplitude_pct": 0.18,
  "seasonal_signal_strength": 0.42,
  "trend_detected": "growing 1.2% week-over-week",
  "outlier_days_detected": ["2025-11-29", "2025-12-21"],
  "outlier_days_excluded": [],
  "suspect_stockout_days": [],
  "fit_residual_stdev": 1.8,
  "fit_aic": 2456.3,
  "fallback_applied": false,
  "method_override_by_buyer": null,
  "confidence_assessment": "high",
  "warnings": []
}
```

## Confidence assessment

The skill rates each forecast's confidence:

| Confidence | Criteria |
|---|---|
| `high` | 180+ days history, low residual variance, clean seasonal/trend signal |
| `medium` | 60-180 days, moderate variance, OR 180+ with mixed signal |
| `low` | <60 days, OR sporadic/lumpy data, OR many outliers |
| `unreliable` | Insufficient data; forecast is essentially guess |

Confidence shows in the .xlsx as a color-coded column so the buyer focuses attention on lower-confidence SKUs.

## Warnings

The skill flags specific issues per SKU:

| Warning code | Meaning | Action |
|---|---|---|
| `low_history` | <30 days of sales | Use buyer-provided initial assumptions |
| `recent_outlier` | Spike in last 14 days inflates forecast | Verify viral/promo vs. new normal |
| `recent_zero_run` | 7+ days zero sales suspicious | Likely stockout, not no demand |
| `seasonal_signal_weak` | Detected but below confidence | Treat seasonality as optional |
| `trend_unclear` | Holt fit residuals show no consistent trend | Consider rolling average instead |
| `fit_unstable` | Model parameters near boundary | Use shorter forecast horizon |
| `method_override_questionable` | Buyer override doesn't match data depth | Skill respected override but flags |
| `velocity_below_threshold` | <0.5 units/day | Sporadic — Poisson heuristic may be more accurate |

The warnings surface in the .xlsx as a "Warnings" column with one row per active warning.

## Forecast run record

The full audit lives at:

```
~/.the-ecommerce-seller/cache/forecast_runs/{YYYY-MM-DD-HHMM}.json
```

Schema:

```json
{
  "run_id": "fc-2026-04-15-1030",
  "run_at": "2026-04-15T10:30:00Z",
  "scope": "full_catalog",
  "input_csv_signatures": ["shopify_orders_2026-04-14.csv"],
  "sku_count": 87,
  "method_distribution": {
    "rolling_average_14d": 12,
    "holt": 38,
    "holt_winters": 31,
    "poisson_heuristic": 4,
    "skipped_dropship": 2
  },
  "confidence_distribution": {
    "high": 28,
    "medium": 41,
    "low": 16,
    "unreliable": 2
  },
  "reorder_triggers_written": 12,
  "reorder_trigger_distribution": {
    "stockout_imminent": 1,
    "urgent": 5,
    "reorder_soon": 6
  },
  "per_sku_diagnostics_path": "forecast_runs/fc-2026-04-15-1030_diagnostics.json",
  "warnings_summary": {
    "low_history": 5,
    "recent_outlier": 2,
    "seasonal_signal_weak": 8
  }
}
```

Per-SKU diagnostics live in a sister file to avoid bloating the top-level run record.

## Comparing runs over time

When the buyer re-forecasts, the skill compares to the prior run:

```
COMPARISON TO PRIOR RUN (2026-04-08)
- Method changes:  3 SKUs upgraded (rolling avg → Holt), 1 downgraded (Holt → rolling avg due to recent volatility)
- Velocity drift:  12 SKUs +/- 10% velocity change vs. prior run
- New stockout risks: 2 SKUs now flagged urgent (were healthy last run)
- Resolved stockout risks: 4 SKUs no longer flagged (reorders placed)
```

This comparison surface in the .xlsx so the buyer can see what's moving and where attention is needed.

## Method override audit

When the buyer overrides a method, the audit logs:

```json
"method_override_by_buyer": "rolling_average_14d",
"method_selected_originally": "holt_winters",
"override_reason": "Buyer flagged seasonal pattern as 2025 anomaly; expected to revert in 2026",
"override_set_at": "2026-04-15"
```

The skill respects overrides but warns when they're questionable.

## Reproducibility

Each forecast run records:
- Input CSV file paths + checksums
- Config snapshot (key settings)
- Statsmodels version (since methods can shift across versions)
- Forecast run date + timezone

This means a buyer can reproduce any prior forecast given the cached inputs, useful for debugging surprising results.

## What NOT to put in the audit log

- Raw sales numbers per day — too much data; lives in source CSV
- Cost / margin info — separate concerns; lives in supplier files + accounting
- Customer-level data — privacy / scope

The audit is for *method transparency*, not data warehousing.

## Buyer questions the audit answers

Common buyer questions and where the audit surfaces the answer:

- "Why did the forecast for X suddenly drop?" → Look at velocity drift comparison + recent outlier flag
- "How confident is this forecast?" → Confidence assessment column
- "Should I trust the seasonal pattern?" → Seasonal signal strength + amplitude
- "Why is this SKU using rolling average instead of Holt-Winters?" → method_rationale field
- "How has this SKU's forecast changed over time?" → Comparison to prior runs

The skill outputs the audit as both raw JSON (for power users) and a clean Sheet 5 in the .xlsx (for everyone).
