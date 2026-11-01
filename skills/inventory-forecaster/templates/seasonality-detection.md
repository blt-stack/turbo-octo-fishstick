# Seasonality Detection

Automated detection of seasonal patterns using autocorrelation. Used by the forecast engine to decide whether to use Holt vs. Holt-Winters and which period to specify.

## What seasonality means in this context

A repeating pattern in sales that recurs at a fixed interval:
- **Weekly (7-day)**: more sales on Fridays/weekends than midweek; common for treats, gifts, leisure goods
- **Biweekly (14-day)**: paycheck cycle for products tied to discretionary spending
- **Monthly (30-day)**: month-end / payday spikes
- **Quarterly (90-day)**: promotional cycle alignment, fiscal-quarter end
- **Semi-annual (180-day)**: spring/fall pattern
- **Annual (365-day)**: holiday-driven peaks (December, Valentine's, Mother's Day, etc.)

## How detection works

The skill uses the autocorrelation function (ACF) from statsmodels:

```python
from statsmodels.tsa.stattools import acf
import numpy as np

def detect_seasonal_period(series, max_lag=400, threshold=0.30):
    """
    Returns the seasonal period if detected, else None.
    """
    acf_values = acf(series, nlags=max_lag, fft=True)

    # Skip lag 0 (always 1.0) and trivially small lags
    candidate_periods = [7, 14, 30, 60, 90, 180, 365]

    best_period = None
    best_corr = threshold

    for p in candidate_periods:
        if p > len(series) // 2:
            continue  # need at least 2 cycles
        if abs(acf_values[p]) > best_corr:
            best_corr = abs(acf_values[p])
            best_period = p

    return best_period, best_corr
```

## Threshold rationale

The `threshold = 0.30` is the practical minimum autocorrelation that's both:
- Strong enough to be meaningful (vs. noise)
- Low enough not to miss real-but-modest patterns

In testing, 0.30 catches the obvious seasonal SKUs without false-positive on noisy data. Buyers can tune in config.

## Multiple periods

A SKU may show seasonality at multiple periods (e.g., both 7-day weekly and 365-day annual). The skill picks the strongest signal but logs the secondary in the audit.

When both 7-day and 30-day are detected, the skill prefers 7-day (more cycles → more reliable fit) unless 30-day is materially stronger (autocorr 0.5+ vs 0.4-).

## Detection requires sufficient history

The skill needs **at least 2 full cycles** to confidently detect a period:
- 7-day: ≥14 days history
- 30-day: ≥60 days history
- 90-day: ≥180 days history
- 365-day: ≥730 days history

SKUs with less history get default to non-seasonal (Holt) regardless of underlying pattern.

## Amplitude estimation

When a seasonal period is detected, the skill estimates amplitude (how big the seasonal swing is):

```python
def seasonal_amplitude(series, period):
    """
    Returns the peak-to-trough amplitude as a % of the mean.
    """
    # Decompose into trend + seasonal + residual
    from statsmodels.tsa.seasonal import seasonal_decompose
    decomp = seasonal_decompose(series, model="additive", period=period)
    seasonal_component = decomp.seasonal.dropna()
    amplitude = (seasonal_component.max() - seasonal_component.min()) / series.mean()
    return amplitude
```

Reported as: "Weekly cycle, amplitude ±18% around mean."

Buyer uses this for promotional planning:
- High-amplitude weekly cycles → schedule paid ads around peak days
- Low-amplitude (< 10%) → seasonality exists but isn't worth marketing-planning around

## When detection is suspect

The skill flags detection results as suspect when:
- The autocorrelation is just above threshold (0.30-0.35) — could be noise
- History is barely above the minimum (e.g., 14 days for 7-day cycle)
- The seasonal amplitude is tiny relative to forecast horizon variance
- Multiple periods have similar autocorrelation (no clear winner)

In these cases, the audit log notes "weak seasonal signal" and the buyer can override.

## Holiday calendar overlay

For 365-day seasonality, the skill cross-references the buyer's holiday calendar (if `campaign-calendar-planner` cache exists) to confirm whether the peaks align with known shopping holidays. If yes, confidence is higher; if no, the annual pattern might be product-specific (cycling-season SKU, school-year SKU, etc.).

## Reading seasonality charts

When the skill renders a single-SKU .docx, it includes a simple text-based seasonality summary:

```
Seasonality: Weekly cycle, 7-day period
Peak day: Saturday  (+22% above mean)
Trough day: Tuesday  (-18% below mean)
Confidence: High (autocorrelation 0.42 at 7-day lag, 24 full cycles observed)
```

Helpful for understanding when the product naturally sells well, beyond just the forecast number.

## Detection edge cases

- **Series with strong trend masks seasonality**: skill detrends first via differencing, then runs seasonality check
- **Stockout days create false zeros**: if `_suspect_stockout: true` days are present, skill optionally interpolates before seasonality check (buyer's call)
- **Holiday spikes (e.g., December 12 every year) without broader Q4 ramp**: these are single-day events, not seasonality — skill detects via outlier check, not period detection
- **Two products in one SKU (different lifecycles)**: rare but possible if SKU got repurposed; skill doesn't detect, but the buyer should split the data

## Reforecasting frequency for seasonal SKUs

Seasonal SKUs benefit from re-forecasting:
- **Before each detected peak**: gives the buyer time to reorder ahead of the surge
- **After each detected trough**: confirms whether the trough was as deep as expected; adjusts forward forecast

The skill recommends seasonal-SKU re-forecast cadence in the .docx output:

```
Recommended reforecast schedule:
  - Weekly (every Monday) — for steady-velocity monitoring
  - Pre-peak alert: reforecast 2 weeks before each expected peak (next peak: 2026-05-30, reforecast by 2026-05-16)
```

## Disabling seasonality detection

For buyers who don't trust automated seasonality:

```json
"inventory_forecasting": {
  "disable_seasonality_detection": true
}
```

Skill defaults to Holt for all 180+ day SKUs in that case. Useful when the buyer wants the most conservative, least-surprising forecasts.
