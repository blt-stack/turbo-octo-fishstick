# Daily Digest — Critical Day — Reference Example

Shows what gets produced when yesterday had multiple anomalies + several urgent cross-skill items. This is the "founder's worst Tuesday" scenario.

**Brand:** {{brand_name}} (placeholder)
**Date covered:** Tuesday, May 19, 2026
**Verdict:** CRITICAL
**Output:** Single `.docx` (~5 pages — longer because there's more to surface)

---

## What the day actually looked like

- Revenue dropped 38% DoD, 32% WoW (z = -2.9σ — anomaly)
- ROAS collapsed from 3.2x to 0.9x (z = -3.4σ — critical)
- Sessions normal but conversion dropped from 2.8% to 1.4%
- 2 SKUs stocking out within 7 days
- A supplier response 18 days overdue
- 4 influencer follow-ups due today

The digest treats this as a 3-alarm day. Top of mind: pause the bleeding (ad spend, checkout investigation), then work through the cross-skill queue.

---

## .docx output structure

### Section 1: Header + Verdict

```
DAILY DIGEST — River Stone Co.
Yesterday: 2026-05-19 (Tuesday) — America/New_York
Verdict: CRITICAL (red)
Generated: 2026-05-20T07:00:00-04:00
```

### Section 2: One-sentence summary

> "Hard day — revenue 2.9σ below baseline + ROAS collapsed to 0.9x flagged critical + 2 SKUs stocking out within 7 days. Top action: pause Spring Sale push and investigate checkout."

### Section 3: Yesterday's Numbers

```
Revenue (net): $2,840.50    (DoD -38%, WoW -32%, MoM -18%)
Orders: 27                  (DoD -42%, WoW -38%)
AOV: $105.20                (DoD +6%, WoW -2%)
Conversion: 1.45%           (DoD -1.2 pts, WoW -1.1 pts)
Sessions: 1,861             (DoD -2%, WoW +2%)

Customer mix: 28% new / 72% returning
  (new customer share down 10 pts — acquisition channel issue)
Refunds: 3 ($142; "didn't work as expected") — pattern flag
```

### Section 4: Anomalies Detected

```
CRITICAL (≥3σ):
- ROAS: yesterday 0.92x vs. baseline 3.18x (stdev 0.31) — z=-3.4σ ↓
  Likely cause: Spring Sale push at 4.2 frequency — creative
  fatigue compounding with broader audience cooling. ROAS has
  dropped 3 days running.

ANOMALY (2-3σ):
- Revenue (net): yesterday $2,840 vs. baseline $4,520 (stdev 580) — z=-2.9σ ↓
  Likely cause: conversion-rate driven (sessions normal at 1,861;
  conversion dropped from 2.8% to 1.45%). Investigation needed —
  funnel shows cart-to-checkout dropped 12 pts.

- Orders: yesterday 27 vs. baseline 44 (stdev 6) — z=-2.8σ ↓
  Likely cause: same as revenue (conversion-rate issue, not traffic).

NOTABLE (1-2σ):
- New customer share: 28% vs. baseline 38% (stdev 5pts) — z=-2.0σ ↓
  Likely cause: paid prospecting ROAS collapse means fewer
  new buyers came through paid; returning customer share elevated.

- Refunds: 3 yesterday vs. baseline 0.7 — refund pattern
  "didn't work as expected" appeared on 2 of 3. Possible quality
  issue on a recent batch.
```

### Section 5: Channel Breakdown

```
Channel          Sessions  Revenue  % of revenue  Conv rate
Email            180       $620     21.8%         3.4%
Paid (Meta)      660       $610     21.5%         0.9%   ⚠ POOR
Google Organic   580       $920     32.4%         2.1%
Direct           320       $580     20.4%         1.8%
Social Organic   121       $110     3.9%          0.8%
```

The paid channel's 0.9% conversion is the chart-flattening signal.
Sessions held up; the conversions didn't.

### Section 6: Top SKUs

```
Movers (up vs. 7-day avg):
- Glass Carafe — 8 units, $256 (+27%)

Decliners:
- River Stone Pour-Over — 5 units, $240 (-72%)  ← Top SKU collapsed
- Filter Pack — 6 units, $72 (-65%)
- Mug Pack — 0 units, $0 (-100%)  ← Zero
- Aero-Cup Tumbler — 2 units, $32 (-60%)

Top 5 by revenue: Glass Carafe $256, River Stone $240, Pour-Over Kit $180,
Filter Pack $72, Aero-Cup $32

Pattern: every primary SKU dropped together — not a SKU-specific issue;
broader conversion/traffic-quality issue.
```

### Section 7: Email + SMS Performance

```
Campaigns sent: 0 (no campaign yesterday)

Active flows:
- Welcome Series: 95 sends, $180, open 41.2% (baseline 48%, dip)
- Abandoned Cart: 142 sends, $440, open 38% (baseline 44%, dip)
- Post-Purchase: 180 sends, $140, open 34% (baseline 41%, dip)
- Browse Abandonment: 280 sends, $0, open 22% (baseline 32%, dip — broken?)

Email % of total revenue: 21.8% (within healthy range)
List growth (net): -8 subscribers (-22 unsubscribed, +14 new)
  Unsubscribes elevated 3 days running — investigate.

Watch items:
- Browse Abandonment generated $0 revenue (typical $90-150/day)
- Open rates across all flows dipped 5-7 pts
- Possible deliverability issue or list-segment break
```

### Section 8: Paid Ads (Meta)

```
Spend: $665 | Revenue: $610 | ROAS: 0.92x  ⚠ CRITICAL
Baseline ROAS: 3.18x  (z=-3.4σ ↓)

By campaign:
- Spring Sale push [PAUSE_CANDIDATE]
  Spend $420, Revenue $180, ROAS 0.43x, Freq 4.2
  ⚠ 3-day ROAS 0.6x. Frequency 4.2 (fatigue zone).
  Pause + creative refresh. Total wasted spend last 3 days: $920.

- Cold prospecting — broad
  Spend $180, Revenue $250, ROAS 1.39x, Freq 2.1
  Below break-even (configured 2.0x). 2-day trend: down 22%.
  Trim budget 30%, watch for stabilization.

- Retargeting — 30d viewers
  Spend $65, Revenue $180, ROAS 2.77x, Freq 3.6
  Healthy but frequency creeping. Add fresh creative within 5 days.

Top ad creative: Slow Morning Reel v3 — $40 spend, $180 revenue (4.5x)
Worst ad creative: Direct UGC product shot — $180 spend, $80 revenue (0.4x)
  Pause this creative specifically — 3 days of underperformance.
```

### Section 9: Traffic + On-site

```
Sessions: 1,861 (DoD -2%)
New users: 64% (DoD -8 pts)  ← cold-traffic share dropped
Bounce: 38.4% (DoD +6 pts)
Avg engagement: 98s (DoD -44s)

Top landing pages:
- /products/river-stone-pour-over — 410 sessions, 6 conv (1.46%, -52%)
- / — 380 sessions, 5 conv (1.32%, -58%)
- /collections/sale — 280 sessions, 2 conv (0.71%, -77%)
  ← Sale page underperforming hard

Funnel:
- Add-to-cart: 7.2% (baseline 8.1%, -0.9 pts)
- Begin checkout: 2.1% (baseline 5.1%, -3.0 pts ⚠)
- Purchase: 1.45% (baseline 2.78%, -1.3 pts)

Funnel flags:
- ⚠ Cart-to-checkout collapse: 3-pt drop overnight.
  Likely causes: checkout error, shipping rate change,
  payment processor issue, OR pixel/tracking break causing
  attribution loss (revenue may be normalized once attribution catches up).
  First investigation: check Shopify settings audit log for last 48 hours.
```

### Section 10: Needs Attention Today

```
INVENTORY:
- ⚠ Filter Pack 100 — stocks out in 6 days at current velocity;
  supplier lead time 45 days (OVERDUE); 800 units needed
- ⚠ River Stone Pour-Over — stocks out in 14 days; supplier lead 60 days;
  1,500 units needed
- Mug Pack — stocks out in 28 days; plan reorder

SUPPLIERS:
- ⚠ Shenzhen Stoneworks — MOQ reduction letter overdue 18 days (CRITICAL)
- Vietnam Ceramics Co. — sample request overdue 6 days
- Mumbai Glassworks Ltd. — pricing tier request overdue 11 days

BUNDLES:
- The Slow Morning Bundle (composite score 84.3) — undeployed
  Recommend: launch ASAP — could counter the revenue drop
- The First Pour Starter Kit (composite score 81.7) — undeployed

INFLUENCERS:
- @maya_brews (instagram, nano) — Variant A due today
- @marcus_taste (tiktok, micro) — Variant A due 2 days ago (overdue)
- @sarah_kitchen (youtube, mid_tier) — Variant B due today
- @james_coffee (youtube, macro) — Variant C due today
```

### Section 11: Suggested Actions for Today

```
1. PAUSE Spring Sale push campaign — $920 wasted spend over 3 days at
   0.6x ROAS. Frequency 4.2 confirms creative fatigue, not audience issue.
   Action: pause in Meta Ads Manager immediately.

2. INVESTIGATE checkout funnel — cart-to-checkout dropped 3 pts.
   First place to look: Shopify settings audit log for last 48 hours
   (recent change to shipping rates, payment methods, or checkout flow
   is the highest-probability culprit). Test a checkout end-to-end.
   Skill to use: (manual investigation; no skill)

3. SEND emergency reorder to Shenzhen Stoneworks (Filter Pack 100, 800 units).
   Lead time 45 days; we have 6 days of inventory. THIS REORDER IS
   ALREADY 39 DAYS LATE on its lead-time math. Concurrent: follow up on
   the 18-day-overdue MOQ letter — that buyer's silence is a relationship
   risk; send Variant A follow-up today.
   Skill to use: supplier-negotiation-assistant

4. LAUNCH the Slow Morning Bundle. Composite score 84.3 is the highest in
   the bundle cache and it's been sitting undeployed for 2 weeks. Use as
   today's promo to defend revenue while paid spend is being restructured.
   Skill to use: landing-page-copywriter, then ad-creative-generator

5. CONFIRM email deliverability. Open rates dipped 5-7 pts across all flows
   yesterday + unsubscribes elevated 3 days running + Browse Abandonment
   generated $0 (vs. typical $90-150). Likely deliverability or segment break.
   Check Klaviyo dashboard for hard bounces and IP reputation today.
```

---

## What's notable about this digest

- The verdict and one-sentence summary set the right tone immediately
- The most urgent items get top billing (pause ad spend, investigate checkout)
- The anomalies section connects each anomaly to a likely cause (not a definitive cause)
- The cross-skill queue shows the cascading effect: low inventory + overdue supplier + undeployed bundle + influencer follow-ups all stacking
- The suggested actions are sequenced by impact: pause the bleeding first, then investigate, then deploy responses

---

## Time to read

This digest is ~5 pages. A founder reading on a hard day with coffee:
- Headers + verdict + summary: 30s (this is the "OK, it's bad" moment)
- Yesterday's numbers + anomalies: 90s
- Channel breakdown + skip ads underperformer: 60s
- Top SKUs (the unified collapse pattern): 60s
- Email watch items: 30s
- Ads section (where the action is): 90s
- Traffic + funnel diagnostic: 90s
- Cross-skill queue: 60s
- Suggested actions: 60s
- **Total: ~9 minutes**

The critical-day digest is longer because there's more to surface — but
it's organized so the founder can pause, investigate, and act in priority
order.

---

## The compounding value

Without this digest, this founder discovers each problem reactively:
- Notices revenue is down in Shopify mid-morning: 1-2 hours lost
- Opens Meta Ads to investigate ROAS: 30 min more
- Calculates wasted spend manually: 20 min
- Checks supplier emails for overdue items: 15 min
- Forgets the bundle, doesn't get to it for 2 weeks
- Doesn't realize email is degrading until Friday

With the digest, **all of this is on the table by 7am** — total reading time
9 minutes, full priority list ready, day starts with action instead of triage.
