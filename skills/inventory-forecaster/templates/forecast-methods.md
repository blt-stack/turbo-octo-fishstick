# Forecast Methods — Tiered Decision Tree

The skill picks one of three methods per SKU based on data history depth and seasonal signal. Every choice is logged in the audit sheet so the buyer can review.

## The decision tree

```
For each SKU:
  1. Count the days of sales history available
  2. If < 60 days:
       method = "rolling_average_14d"
  3. Else if 60-179 days:
       method = "holt"   (exponential smoothing with trend)
  4. Else (180+ days):
       Run seasonal autocorrelation check
       If seasonal signal detected (autocorr > 0.3 at any period):
         method = "holt_winters" with detected period
       Else:
         method = "holt"
```

## Why these thresholds

- **60 days**: Holt needs at least one full cycle of trend signal to fit reliably. Below 60 days, the trend coefficient is noisy.
- **180 days**: Holt-Winters needs at least 2 full seasonal cycles. For 7-day seasonality, that's 14 days minimum; for 30-day, 60 days; for 365-day, 730 days. 180 days is a practical floor for detecting weekly + monthly seasonality without overfitting.

## Method 1: Simple 14-day rolling average

```python
def rolling_avg_forecast(history, horizon_days, safety_multiplier=1.2):
    last_14 = history[-14:]
    daily_avg = sum(units_sold for d in last_14) / 14
    forecast = daily_avg * horizon_days * safety_multiplier
    return forecast
```

Reasoning:
- Recent 14 days reflect current demand
- Safety multiplier accounts for variance (default 1.2 = 20% buffer)
- Robust to outliers if the history isn't too short

When this method shines:
- New SKUs (just launched, < 60 days)
- Stable products with low seasonal sensitivity
- When the buyer wants transparent + auditable math

When it fails:
- Trending up — underforecast
- Trending down — overforecast
- Seasonal SKUs — misses peaks and troughs

The audit log warns when the rolling average likely misses signal.

## Method 2: Exponential smoothing (Holt's method)

Captures level + trend. No seasonality.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    series,
    trend="add",       # additive trend
    seasonal=None,     # no seasonality
    initialization_method="estimated",
)
fit = model.fit()
forecast = fit.forecast(steps=horizon_days)
```

Reasoning:
- Recent observations weighted more heavily (exponential decay)
- Trend component captures growth/decline
- Variance + confidence band derived from model residuals

When this method shines:
- SKUs growing or declining steadily
- SKUs with 60-180 days history
- Products with no clear seasonality but a clear trend direction

When it fails:
- Strong seasonality treated as noise → wide confidence bands
- Sudden trend changes (recently viral, recently broken)

The audit log flags Holt-fit SKUs whose residuals show seasonal autocorrelation — buyer may want to upgrade to Holt-Winters once more history accumulates.

## Method 3: Holt-Winters (seasonal exponential smoothing)

Captures level + trend + seasonality.

```python
model = ExponentialSmoothing(
    series,
    trend="add",
    seasonal="add",            # additive seasonality
    seasonal_periods=period,   # detected via autocorrelation
    initialization_method="estimated",
)
fit = model.fit()
forecast = fit.forecast(steps=horizon_days)
```

Period selection:
- 7 (weekly cycle)
- 14 (biweekly — uncommon, but exists for some products)
- 30 (monthly — paycheck-correlated)
- 90 (quarterly — promotional cycles)
- 365 (annual — holiday-correlated)

The skill auto-detects via the autocorrelation function (see `seasonality-detection.md`).

When this method shines:
- SKUs with clear weekly cycles (Friday-heavy, Sunday-heavy)
- Seasonal products (December peaks, summer peaks)
- Products with strong promotional cadence

When it fails:
- Less than 2 full cycles of history (Holt-Winters needs the cycle pattern to repeat)
- Highly variable amplitude — model assumes consistent seasonal swings

## Confidence band

For each method, the skill computes a confidence band:

- **Rolling average**: ±1 standard deviation of the recent 14 days × horizon (rough but transparent)
- **Holt**: derived from model residual variance
- **Holt-Winters**: derived from model residual variance after seasonal decomposition

The band is rendered as P10 (conservative) / P50 (base) / P90 (aggressive) in the output.

## Method override

The buyer can override method selection per SKU:

```json
"inventory_forecasting": {
  "method_overrides": {
    "RS-POUR-OVER-001": "holt_winters",
    "JIGSAW-PUZZLE-XMAS": "holt_winters",
    "DROP-SHIP-SKU-A": "rolling_average_14d"
  }
}
```

The skill respects overrides but flags if the override is questionable (e.g., applying Holt-Winters to a SKU with 90 days of history — won't fail but will produce wide confidence bands).

## Sporadic-sales handling

Some SKUs sell in clusters — three units one day, zero for 9 days, two units, etc. The rolling average underforecasts these; Holt assumes continuous demand.

The skill detects sporadic patterns:
- > 30% of days have zero sales
- Mean velocity < 0.5 units/day

For sporadic SKUs, the skill switches to a Poisson-based heuristic:
- Compute average inter-arrival time between non-zero days
- Estimate next-30-days as: (30 / inter_arrival_time) × mean_burst_size
- Wide confidence band reflects high variance

The audit log notes "sporadic — Poisson heuristic applied."

## Outlier days

The skill detects outlier days:
- Days where units_sold > mean + 3 × stdev
- Days where units_sold > 5× the 14-day rolling average

Outliers are NOT removed by default — they may be real spikes (viral moment, promotion). But the audit log notes them, and the buyer can mark days as "exclude from forecast" if they're sure the spike was one-off.

## Model fitting failures

Statsmodels occasionally fails to fit (rare but possible — flat series, degenerate cases). The skill catches the exception and falls back to:
- Holt-Winters fail → try Holt
- Holt fail → try rolling average
- Rolling average always works (worst case: forecast equals zero if history is zero)

The audit log notes any fallbacks.

## Skill dependencies

```
statsmodels >= 0.14.0
numpy
pandas
```

Install with `pip install statsmodels pandas --break-system-packages`.

## Worked example — method choices across SKU portfolio

For a hypothetical portfolio:

| SKU | History days | Avg velocity | Variance | Seasonal? | Method chosen |
|---|---|---|---|---|---|
| RS-POUR-OVER-001 | 456 | 12.3/day | Low | Yes (weekly) | holt_winters (7-day) |
| STUDIO-BOWL-LRG | 210 | 8.1/day | Medium | No detected | holt |
| GIFT-SET-HOLIDAY | 540 | 0.4/day | Very high (clustered) | Yes (annual) | holt_winters (365-day) |
| NEW-LAUNCH-A | 32 | 4.5/day | Low | Unknown (insufficient) | rolling_average_14d |
| DROP-SHIP-A | n/a | n/a | n/a | n/a | skipped (drop-ship) |
| SPORADIC-ART-PIECE | 180 | 0.3/day | Very high (lumpy) | No | poisson_heuristic |

The audit log captures all of this so the buyer can review.

## Re-forecasting cadence

The skill recommends re-running forecasts:
- **Weekly** for fast-moving SKUs (>10 units/day)
- **Bi-weekly** for medium-velocity SKUs
- **Monthly** for slow-moving + sporadic SKUs
- **Quarterly** for very slow / drop-ship SKUs

Frequent re-forecasting catches velocity drift faster. The skill embeds the cadence recommendation in the .docx and .xlsx so the buyer can set reminders.
