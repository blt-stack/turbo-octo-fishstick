# Traffic + On-Site Section Methodology (GA4)

What drove people to the site yesterday and what they did once they arrived. Often the hidden story behind a revenue anomaly.

## What it covers

- Sessions, users, new users
- Bounce rate + engagement rate
- Average engagement time
- Source/medium breakdown (with revenue attribution per source)
- Top landing pages + conversion per landing
- Funnel step performance (view → cart → checkout → purchase)

## Narrative tone

Traffic is **diagnostic** — the section often explains anomalies surfaced in revenue. The narrative should connect the dots when applicable.

## Required elements

1. **Sessions** (DoD + WoW)
2. **New users %** of total users (indicates acquisition channel mix)
3. **Bounce rate** (DoD)
4. **Top 3-5 source/medium** with sessions + revenue attribution
5. **Top 2-3 landing pages**
6. **Funnel drop-off** flags (any step that dropped >20% from baseline)

## Source/medium attribution

GA4 attribution helps explain revenue mix:

| Source/Medium | Typical % share for established DTC | Healthy ratio? |
|---|---|---|
| `google / organic` | 25-40% | Stable growth = healthy |
| `(direct) / (none)` | 15-30% | Brand strength signal |
| `facebook / paid` | 15-30% | Track ROAS context |
| `klaviyo / email` | 10-20% | Match to email section |
| `instagram / referral` | 5-15% | Organic social health |
| `google / cpc` | 5-20% | Google Ads if running |
| `tiktok / paid` | 0-20% | TikTok Ads if running |

The skill flags major shifts: a source dropping >30% in share DoD signals something specific to that channel.

## Top landing page surveillance

For each top landing page yesterday:

- Sessions
- Conversion rate (yesterday vs. 7-day baseline)
- Revenue from that page

A landing page whose conversion rate drops materially is the most actionable diagnostic the digest can surface. Common causes:

- Page broke (technical error or merchandising error)
- Pricing change deterred buyers
- Out-of-stock messaging on the page
- Recent design change tanked conversion
- New traffic source brought low-intent traffic

The skill flags landing pages where conversion dropped >30% vs. baseline.

## Funnel step analysis

GA4 funnel:

```
Sessions → View Item → Add-to-Cart → Begin Checkout → Purchase
```

Typical DTC funnel drop-offs (median benchmarks):

| Step | Healthy rate |
|---|---|
| Session → View Item | 60-80% |
| View Item → Add-to-Cart | 8-15% |
| Add-to-Cart → Begin Checkout | 45-65% |
| Begin Checkout → Purchase | 50-75% |

The skill computes yesterday's rates and compares to baseline. Anomalous drops:

- View Item → Add-to-Cart dropped >5 pts → product page issue or pricing issue
- Add-to-Cart → Begin Checkout dropped >10 pts → cart UX issue or shipping rate change
- Begin Checkout → Purchase dropped >10 pts → checkout error or payment issue

These are surfaced with diagnostic framing.

## New vs. returning user mix

GA4 new user % offers a different view than Shopify's customer mix (because GA4 tracks browser-cookie new, not order-history new).

The skill cross-references:

- GA4 new users ↑ + Shopify new customers ↑ → genuine acquisition pulse
- GA4 new users ↑ + Shopify new customers ~ → new traffic isn't converting (acquisition channel mismatch)
- GA4 new users ↓ + Shopify new customers ↓ → acquisition channel pause or paid ads pulled back

## Bounce rate context

Bounce rate is per-source. Healthy ranges vary:

| Source | Healthy bounce rate |
|---|---|
| Direct | 30-50% |
| Organic search | 40-55% |
| Paid social | 50-70% (cold traffic) |
| Email | 25-45% |
| Referral | 35-55% |

A site-wide bounce rate of 65%+ with a known traffic mix dominated by paid social is normal. The same number on a brand with mostly direct + email traffic is alarming.

The skill computes weighted-baseline bounce rate from the source mix and flags only meaningful deviations.

## What NOT to include

- Page-level UX recommendations (lives in a CRO skill, not the daily digest)
- Site speed analysis (Performance is its own deep-dive)
- Heatmap interpretation
- Detailed cohort retention analysis

## Length target

2-4 short paragraphs.

## Example complete section

```
══════════════════════════════════════════════════
TRAFFIC + ON-SITE
══════════════════════════════════════════════════

Sessions: 1,820  (DoD +4%, WoW +1%)
New users: 70%   (DoD +2 pts; within normal)
Bounce: 31.9%    (DoD -1 pt; healthy)
Engagement: 142s avg

Top sources by revenue:
- klaviyo / email      $1,280  (28% of revenue;
                                from yesterday's Memorial Day push)
- facebook / paid       $1,450  (32%; tracking with Meta Ads section)
- google / organic      $1,100  (24%)
- (direct) / (none)       $920  (20%)

Top landing pages:
- /products/river-stone-pour-over
  480 sessions, 18 conversions (3.75% — above baseline 2.8%)
- /
  380 sessions, 12 conversions (3.16%)
- /collections/all
  220 sessions, 5 conversions (2.27% — below baseline 3.1%, watch)

Funnel:
- Add-to-cart 8.4% (baseline 8.1%, healthy)
- Begin checkout 4.2% (baseline 5.1%, ↓0.9 pts)
- Purchase 2.58% (baseline 2.78%)

Watch: cart-to-checkout dropped 0.9 pts. Single-day,
not anomalous but worth confirming no shipping rate
or checkout change.
```

The reader sees: traffic was fine, pour-over landing was strong, checkout has a possible 1-day issue worth confirming.
