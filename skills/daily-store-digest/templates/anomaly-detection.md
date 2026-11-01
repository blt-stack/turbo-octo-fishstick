# Anomaly Detection — Statistical Methodology

The digest's "what changed yesterday" layer. Uses a 7-day rolling baseline plus standard deviation to flag metrics that drift significantly from recent patterns.

## Core method: z-score against 7-day rolling baseline

For each numeric metric on the target date:

```
mean   = mean of the prior 7 days (excluding target date)
stdev  = stdev of the prior 7 days (excluding target date)
z      = (yesterday_value - mean) / stdev
```

The skill uses **population stdev** (N denominator), not sample stdev (N-1). At N=7 this difference is small but population is the appropriate choice here since the 7 days ARE the baseline (not a sample of something larger).

### Severity tiers

| |z| range | Severity | Behavior |
|---|---|---|
| < 1.0 | Normal | Not surfaced |
| 1.0 – 2.0 | Notable | Surfaced as context only |
| 2.0 – 3.0 | Anomaly | Flagged prominently in digest |
| ≥ 3.0 | Critical | Top-of-digest flag; drives "Critical" verdict |

### Direction matters

The skill labels anomalies with `↑` (above baseline) or `↓` (below baseline) and applies direction-specific judgment:

| Metric | ↑ direction | ↓ direction |
|---|---|---|
| Revenue | Good (celebrate, note cause) | Bad (flag, investigate) |
| Orders | Good | Bad |
| Conversion rate | Good | Bad |
| AOV | Good | Investigate (could be discount-driven) |
| Sessions | Good | Bad |
| Bounce rate | Bad | Good |
| Ad spend | Investigate (could be runaway scaling) | Could be intentional pause |
| ROAS | Good | Bad |
| CPM | Bad | Good |
| Frequency | Bad if >3.5 | OK |
| Unsubscribes | Bad | Good |
| Refunds | Bad | Good |

The narrative tone for a ↑ anomaly differs from ↓ — anomalies in the good direction get curiosity ("what worked?") while bad-direction anomalies get diagnostic framing ("what broke?").

## Metrics tracked

The detector runs against every numeric metric pulled from the 4 sources. Default set:

**Shopify:**
- `revenue.net_usd`
- `orders.count`
- `orders.avg_order_value_usd`
- `conversion.conversion_rate_pct`
- `conversion.sessions`
- `refunds_returns.count`
- `refunds_returns.amount_usd`

**Klaviyo:**
- `total_email_revenue_usd`
- `email_pct_of_total_revenue`
- `list_growth.net_change`
- Per-flow: `open_rate_pct`, `click_rate_pct`, `revenue_yesterday_usd`

**Meta Ads:**
- `spend_usd`
- `roas`
- `cpm_usd`
- `ctr_pct`
- `frequency`
- `cost_per_purchase_usd`

**GA4:**
- `sessions`
- `engagement_rate_pct`
- `bounce_rate_pct`
- `funnel.add_to_cart_pct`
- `funnel.begin_checkout_pct`
- `funnel.purchase_pct`

Buyer can disable specific metrics via `daily_store_digest.disabled_metrics` config.

## Low-volume fallback

When the 7-day mean is small (default threshold: <5 events/day for count metrics, <$100 for revenue metrics), stdev is unreliable and a small absolute change shows as a huge z-score.

For low-volume metrics, the skill falls back to rule-based detection:

```json
"daily_store_digest.fallback_rules": {
  "orders.count": {
    "low_volume_threshold": 5,
    "flag_if_drop_pct_below": 50,
    "flag_if_zero_when_baseline_nonzero": true
  },
  "revenue.net_usd": {
    "low_volume_threshold": 100,
    "flag_if_drop_pct_below": 40
  }
}
```

The digest labels low-volume detections as such ("Low-volume metric — using rule-based threshold") so the buyer knows the methodology shifted.

## Sparse-data mode (<7 days of history)

For brand-new stores with insufficient history:

- **0-2 days of history**: skill reports raw values + DoD comparison only; no anomaly detection
- **3-6 days of history**: anomaly detection runs with reduced confidence flag; uses N=available days; severity tiers loosened by 0.5σ (2.5σ becomes the anomaly threshold instead of 2.0σ)
- **7+ days of history**: full anomaly detection enabled

The skill flags reduced-confidence mode in the digest header: "Anomaly detection running on N days of baseline (full confidence requires 7+ days)."

## Weekday-aware variant

For stores with strong weekly seasonality (e.g., huge Sunday boost from email blasts, dead Tuesdays), the standard 7-day-calendar baseline produces false anomalies.

Enable via `daily_store_digest.weekday_aware_baseline=true`. When enabled, the baseline uses the **last 7 same-weekday values** instead of the last 7 calendar days:

- Target = Monday → baseline = the prior 7 Mondays
- Target = Friday → baseline = the prior 7 Fridays

Requires ~50 days of history minimum (7 same-weekday values × min 7 weeks). The skill falls back to calendar baseline if insufficient weekday data.

## Likely-cause hypothesis layer

When an anomaly is flagged, the skill attempts a likely-cause hypothesis by cross-referencing other metrics:

| Anomaly | Cross-referenced signal | Hypothesis |
|---|---|---|
| Revenue ↓ + sessions normal | Conversion rate ↓ | Site issue or pricing change |
| Revenue ↓ + sessions ↓ | Traffic source breakdown | Paid ads paused or organic drop |
| Revenue ↓ + ROAS ↓ | Ad spend normal | Creative fatigue or audience saturation |
| Revenue ↓ + email revenue 0 | No campaigns sent | Missed campaign; flow may be paused |
| AOV ↑ + units ↓ | Top SKU = expensive | Buyer mix shifted upmarket (good) |
| AOV ↓ + units ↑ | Discount code usage spiked | Promo or bot activity |
| Bounce ↑ + sessions ↑ | Source = paid social | Wrong audience targeting on a new campaign |
| CPM ↑ + frequency ↑ | Campaign frequency >3.5 | Creative fatigue |
| Funnel drop-off cart→checkout | Recent site change | Checkout error or shipping rate change |

These hypotheses are framed as **starting points for investigation**, not conclusions. The narrative explicitly says "likely cause" — never "the cause is."

## Multi-anomaly correlation

When 3+ metrics anomalize together, the skill checks for known correlation patterns:

- **All paid metrics anomalize together** → Meta Ads account-level issue (spending limit, account suspended, billing issue)
- **All email metrics anomalize together** → Klaviyo deliverability issue (IP reputation, list health, ESP problem)
- **Traffic + revenue drop together while ad spend is constant** → tracking issue (pixel broken, GA4 misconfigured) OR major site outage
- **All metrics drop on a known holiday** → expected seasonal drop, not anomaly (the digest auto-detects major holidays from a calendar file)

## Holiday-aware suppression

The skill maintains a holiday calendar (`daily_store_digest.holiday_calendar`) that lists dates where anomalies should be **expected** rather than alarming:

- US: Thanksgiving morning, Christmas Day, etc.
- Easter Sunday (varies)
- Black Friday week (anomalies in the OTHER direction — bigger-than-baseline)

On holiday dates, the skill flags anomalies but tags them as "Expected anomaly — holiday calendar match" and downgrades severity by one tier.

## Buyer override

The buyer can mark a specific date as a known-promo-day:

```
"daily_store_digest.known_promo_dates": ["2026-05-23", "2026-05-24", "2026-05-25"]
```

On those dates, the skill flags anomalies but tags them as "Known promo day — anomaly expected" and downgrades severity by one tier.

## Confidence intervals (optional)

For buyers who want more statistical rigor, enable `daily_store_digest.show_confidence_intervals=true`. The digest then includes:

- 95% confidence interval = baseline ± 1.96 × stdev
- Yesterday inside CI: normal
- Yesterday outside CI: anomalous at p<0.05

This is the formal stats framing of the same logic. Default off because most buyers prefer the simpler "Nσ above baseline" language.
