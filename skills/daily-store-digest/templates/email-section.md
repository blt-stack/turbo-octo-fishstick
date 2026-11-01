# Email + SMS Section Methodology (Klaviyo)

What yesterday's campaigns and flows did. The lowest-cost-per-revenue channel for most DTC brands — and the one founders look at least carefully.

## What it covers

- Yesterday's campaigns sent (count + names + performance)
- Active flows performance (Welcome, Cart Abandon, Post-Purchase, etc.)
- Total email + SMS revenue
- Email's % share of total revenue
- List growth (new subscribers vs. unsubscribes)
- Deliverability warning signals

## Narrative tone

Email is **routine** — most days look similar. The narrative should highlight what differs: a notably strong campaign, a flow that broke, a deliverability warning, a list-growth anomaly.

On routine days the section is short and confirms normality.

## Campaign performance framing

For each campaign sent yesterday:

```
Campaign: [Name]
Sent: N  Delivered: N  Open: X%  Click: X%  Revenue: $X (RPS: $X)
[vs. campaign-type baseline]
```

The skill maintains rolling baselines **per campaign type** (one-off promos vs. content emails vs. weekly newsletter) because their performance varies systematically:

| Campaign type | Typical open rate | Typical click rate | Typical RPS |
|---|---|---|---|
| Welcome series (flow) | 40-60% | 8-15% | $0.50-2.00 |
| Promotional broadcast | 25-40% | 2-5% | $0.05-0.30 |
| Newsletter / content | 20-35% | 1-3% | $0.02-0.10 |
| Abandoned cart (flow) | 35-50% | 5-10% | $1.00-5.00 |
| Post-purchase (flow) | 40-55% | 3-7% | $0.10-0.50 |
| Sale / discount push | 25-35% | 3-6% | $0.10-0.40 |

Campaign-type detection: heuristic based on send size + flow vs. campaign + name keywords. Buyer can override.

## Active flows surveillance

Every brand has a few perennial revenue-driving flows:

- Welcome (highest RPS — biggest brand intro impact)
- Abandoned Cart (highest dollar/email — fixing dropoffs)
- Post-Purchase (cross-sell + retention)
- Browse Abandonment (mid-funnel rescue)
- Win-back (cold subscriber reactivation)

The skill compares each flow's yesterday performance against its own 30-day rolling baseline (not 7-day — flow performance is slower-moving).

Flag when:
- A flow's open rate drops >10 percentage points below its 30-day baseline → likely deliverability or segment issue
- A flow's revenue drops to $0 when baseline is >$0 → flow may be paused or broken
- A flow's send count drops to 0 → audience filter may have been changed

## List growth tracking

Daily net subscriber change. Trend matters more than single-day:

- Net positive every day → healthy
- Net positive most days but with periodic negatives → normal
- Net negative for 3+ consecutive days → flagged
- Sudden +500 subscribers in one day → flagged (could be a promo or a sketchy list buy)
- Sudden -200 unsubscribes in one day → flagged (could be a campaign misfire)

## Deliverability signals

The skill watches for early-stage deliverability degradation:

| Signal | What it might mean |
|---|---|
| Open rate of new campaigns drops >15 pts vs. baseline | IP/domain reputation degrading |
| Click-to-open ratio drops while open rate holds | Subject lines outperforming content |
| Unsubscribe rate climbing 3+ days in a row | Frequency too high or audience drift |
| Bounce rate >2% | List health degrading; suppress hard bounces |
| Total send volume up but revenue per send down | Audience saturation or cold list portion increasing |

The skill flags these in the digest with diagnostic context.

## Email's % of total revenue

A common DTC benchmark: 20-35% of revenue from email is healthy for established brands. The skill computes:

```
email_share = (klaviyo_revenue_yesterday) / (shopify_net_revenue_yesterday)
```

And classifies:

- `email_share < 10%` → underleveraged email channel (note as opportunity)
- `email_share 10-20%` → mid-cycle; could push more
- `email_share 20-35%` → healthy
- `email_share 35-50%` → email-heavy; check acquisition channels are not declining
- `email_share > 50%` → over-reliant; flag as risk

This is a context line, not an anomaly. It informs the overall narrative.

## What NOT to include

- Subject-line A/B test recommendations (too granular for the morning digest)
- Segmentation strategy advice (lives in dedicated email skills)
- Specific email body copy critiques

## Length target

2-4 short paragraphs. Briefer than revenue or ads sections on routine days.

## Example complete section

```
══════════════════════════════════════════════════
EMAIL + SMS PERFORMANCE
══════════════════════════════════════════════════

Campaigns sent: 1 ("Memorial Day Sale Reminder")
  Open 32.4%  Click 4.1%  Revenue $1,280  RPS $0.092
  vs. promotional baseline: open above (+4 pts),
  click above (+0.7 pts), RPS above (+$0.02).
  Strong send.

Active flows:
- Welcome Series:   142 sends  $380  open 48% (baseline 51%, normal)
- Abandoned Cart:    88 sends  $520  open 41% (baseline 44%, normal)
- Post-Purchase:    240 sends  $180  open 38% (baseline 41%, mild dip)
- Browse Aband.:    320 sends  $90   open 28% (baseline 32%, dip — check)

Email % of total revenue: 28.4% (within healthy 20-35% range).

List growth: +14 net subscribers (+28 new, -14 unsub).
Healthy.

Watch item: Browse Abandonment open rate dipped 4 pts.
Single-day; track tomorrow.
```

The reader sees: campaigns are strong, one flow has a small dip worth watching, list health is fine.
