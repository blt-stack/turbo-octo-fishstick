# Revenue Section Methodology

The first substantive section of the digest. The brief that founders most want to read.

## What it covers

- Total revenue (gross + net of refunds) yesterday
- Order count
- Average order value (AOV)
- New customer vs. returning customer mix
- Comparison windows: DoD, WoW, MoM, YoY
- Anomaly status (from anomaly detector)

## Narrative tone

The revenue section is the briefing's lead. It should be **direct** — no preamble, no ramp. State the number first, then the context.

Bad opening:
> "Looking at yesterday's revenue, the store generated some sales, and we can compare these to recent days to see how things are tracking..."

Good opening:
> "Revenue: $4,500. Down 18% DoD, down 9% WoW. Within the notable range vs. the 7-day baseline but not anomalous — Tuesdays are typically the soft day this month."

## Required elements

Every revenue section MUST include:

1. **Yesterday's net revenue** (USD with thousands separator, 2 decimal cents)
2. **DoD percentage delta** with direction (↑ green, ↓ red)
3. **WoW percentage delta**
4. **Anomaly classification** if any metric is flagged

Optional elements (include only if signal is strong):

- MoM and YoY deltas (skip if <30 days or <365 days of history)
- New vs. returning customer split (mention if shifted >5 percentage points from baseline)
- Refunds (mention if refund amount >5% of net revenue)

## Common framings

### "Above baseline" framing

When yesterday outperforms:

> "Revenue: $7,200. Up 42% DoD, up 28% WoW. This is 2.4σ above the 7-day baseline — flagged as anomaly (good direction). Likely cause: the Memorial Day reminder sent at 11am drove $1,280 in email revenue, which doesn't usually contribute that share."

### "Below baseline" framing

When yesterday underperforms:

> "Revenue: $2,840. Down 36% DoD, down 22% WoW. This is 2.6σ below the 7-day baseline — flagged as anomaly. Sessions held at 1,780 (normal), so this is a conversion-rate issue: yesterday's conversion was 1.6% vs. the 2.5% baseline. Likely cause: investigation needed — site issue, checkout error, or pricing change are first candidates."

### "Mixed signals" framing

When metrics tell competing stories:

> "Revenue: $4,500. Down 18% DoD but within normal range (-1.4σ). AOV: $96 — down from $108 baseline. Orders: 47 — up from 42 baseline. Read: more orders, smaller carts. Likely cause: a discount code is over-applying or buyers shifted to smaller-bundle purchases. Check yesterday's checkouts for code patterns."

## AOV narrative rules

AOV is informative but easily misleading. The section never reports AOV in isolation — always pair with:
- Order count (a 5-order day with one $500 order spikes AOV; signal-thin)
- Top SKU shift (if AOV ↑ and top SKU shifted to expensive item, that's the explanation)
- Discount code usage (if AOV ↓ and discount codes spiked, that's the explanation)

## New vs. returning split

Healthy DTC brands typically run 60-75% returning customer revenue once they're past month 6. The skill flags shifts:

- New customer share ↑ → recent ad spend or organic acquisition pulse; check ROAS to confirm sustainable
- New customer share ↓ + revenue ↓ → acquisition channel broke
- Returning share ↑ + new ↓ → could be email campaigns to existing list (good short-term, not scalable)

## Refunds + returns

Mentioned only when meaningful:

- 0-1 refunds → not mentioned (noise)
- 2-4 refunds with no pattern → mentioned as data
- 3+ refunds with same reason → flagged as pattern; surfaces in "Needs Attention" section
- Refund amount >10% of net revenue → flagged prominently regardless of count

## What NOT to include in this section

- Channel breakdown (lives in its own section)
- SKU-level detail (lives in Top SKUs section)
- Email campaign attribution (mentioned only as a quick reference; full data in Email section)
- Forecasting / projections (this is a backward-looking briefing, not a forecast)

## Length target

The revenue section should be **3-5 short paragraphs**. A founder reading this on their phone at 7am with coffee in hand should be able to parse it in 30-45 seconds.

If the section is >7 paragraphs, the skill is over-explaining — trim.

## Example complete section

```
══════════════════════════════════════════════════
YESTERDAY'S NUMBERS
══════════════════════════════════════════════════

Revenue: $4,500.50  (DoD -18%, WoW -9%, MoM +4%)
Orders: 47          (DoD +12%, WoW +3%)
AOV: $95.76         (DoD -27%, WoW -12%)
Conversion: 2.58%   (DoD -0.3 pts, WoW -0.1 pts)
Sessions: 1,820     (DoD +4%, WoW +1%)

Anomaly status: 1 anomaly flagged. AOV is 2.3σ below
baseline — notable. Likely cause: yesterday's email
push promoted a $24 filter pack which became the
top SKU by units (22 sold), pulling AOV down.

Customer mix: 38% new / 62% returning — within the
healthy 35-45% new range.

Refunds: 1 ($48; "damaged in transit") — single
incident, no pattern to flag.
```

This is the full section. Notice:
- Numbers first
- Anomalies stated plainly with magnitude and direction
- Hypothesis offered for the anomaly (filter-pack push)
- Customer mix mentioned only because it's normal-noteworthy
- Refunds mentioned only because there was one (and the section was short, so it fit)
