# Daily Digest — Healthy Day — Reference Example

Shows what gets produced when yesterday was a calm, on-baseline day.

**Brand:** {{brand_name}} (Brooklyn pour-over brand placeholder)
**Date covered:** Friday, May 22, 2026
**Verdict:** HEALTHY
**Output:** Single `.docx` (~3 pages)

---

## What the day actually looked like

- Revenue tracked slightly below baseline but within normal variance
- ROAS held steady at 3.0x
- Email campaign performed strongly (Memorial Day reminder)
- No critical anomalies
- 2 cross-skill items in the queue, neither urgent

The digest shows this is a normal day — short, scannable, no fire drills.

---

## .docx output structure

### Section 1: Header + Verdict

```
DAILY DIGEST — River Stone Co.
Yesterday: 2026-05-22 (Friday) — America/New_York
Verdict: HEALTHY (green)
Generated: 2026-05-23T07:00:00-04:00
```

### Section 2: One-sentence summary

> "Quiet day — revenue tracked within normal range; one watch-item on cart-to-checkout funnel worth confirming."

### Section 3: Yesterday's Numbers

```
Revenue (net): $4,500.50   (DoD -8%, WoW -2%, MoM +4%)
Orders: 47                 (DoD +5%, WoW +3%)
AOV: $95.76                (DoD -12%, WoW -4%)
Conversion: 2.58%          (DoD -0.1 pts)
Sessions: 1,820            (DoD +4%, WoW +1%)

Customer mix: 38% new / 62% returning
Refunds: 1 ($48; "damaged in transit") — single incident
```

### Section 4: Anomalies Detected

```
No anomalies flagged. Metrics tracked within normal range.
```

(One notable item — AOV down 1.4σ — is suppressed because it's within
the "notable" tier and the cause is obvious from the email push.)

### Section 5: Channel Breakdown

```
Channel          Sessions  Revenue   % of revenue   Conv rate
Email (Klaviyo)  220       $1,280    28.4%          5.9%
Paid (Meta)      480       $1,450    32.2%          2.9%
Google Organic   620       $1,100    24.4%          2.4%
Direct           310       $920      20.4%          3.5%
Social Organic   190       $250      5.6%           1.8%
```

### Section 6: Top SKUs

```
Movers (up vs. 7-day avg):
- River Stone Pour-Over — 18 units, $864 (+38%)
- Filter Pack 100 — 22 units, $264 (+45%)

Decliners:
- Aero-Cup Tumbler — 3 units, $48 (-50%)

Top 5 by revenue: River Stone Pour-Over $864, Filter Pack $264,
Glass Carafe $192, Aero-Cup $48, Mug Pack $40
```

### Section 7: Email + SMS Performance

```
Campaigns sent: 1
- "Memorial Day Sale Reminder" — Open 32.4%, Click 4.1%,
  Revenue $1,280 (RPS $0.092). Above promotional baseline. Strong send.

Active flows:
- Welcome Series: 142 sends, $380, open 48.2% (normal)
- Abandoned Cart: 88 sends, $520, open 41.3% (normal)
- Post-Purchase: 240 sends, $180, open 38.4% (mild dip)
- Browse Abandonment: 320 sends, $90, open 28.1% (dip — watch)

Email % of total revenue: 28.4% (healthy 20-35% range)
List growth (net): +14 subscribers
```

### Section 8: Paid Ads (Meta)

```
Spend: $480 | Revenue: $1,450 | ROAS: 3.02x
Baseline ROAS: 3.18x (z=-0.7σ, normal range)

By campaign:
- Retargeting — 30d viewers [SCALE_CANDIDATE]
  Spend $180, Revenue $720, ROAS 4.00x, Freq 3.4
  Top performer. Increase budget 15-20% with fresh creative.

- Cold prospecting — broad
  Spend $220, Revenue $620, ROAS 2.82x, Freq 1.5
  Healthy. Holding steady.

- Spring sale push
  Spend $80, Revenue $110, ROAS 1.38x, Freq 2.1
  Below baseline; 1-day dip. Track tomorrow.

Top ad creative: Slow Morning Reel v3 — $80 spend, $416 revenue (5.2x)
Worst ad creative: Direct UGC product shot — $65 spend, $26 revenue (0.4x)
```

### Section 9: Traffic + On-site

```
Sessions: 1,820 (DoD +4%)
New users: 70%
Bounce: 31.9% (healthy)
Avg engagement: 142s

Top landing pages:
- /products/river-stone-pour-over — 480 sessions, 18 conv (3.75%, +34%)
- / — 380 sessions, 12 conv (3.16%)
- /collections/all — 220 sessions, 5 conv (2.27%, -27% — watch)

Funnel:
- Add-to-cart: 8.4% (baseline 8.1%, healthy)
- Begin checkout: 4.2% (baseline 5.1%, -0.9 pts)
- Purchase: 2.58% (baseline 2.78%)

Funnel flags: cart-to-checkout dropped 0.9 pts. Single-day,
confirm tomorrow no shipping rate or checkout change.
```

### Section 10: Needs Attention Today

```
INVENTORY:
- River Stone Pour-Over — stocks out in 28 days at current velocity;
  supplier lead time 60 days (actually overdue against lead time);
  reorder 1,500 units recommended

SUPPLIERS:
(none — healthy)

BUNDLES:
- The Slow Morning Bundle (composite score 84.3/100) — undeployed
  Recommend: launch as next promo angle

INFLUENCERS:
(none — healthy)
```

### Section 11: Suggested Actions for Today

```
1. Place reorder for River Stone Pour-Over (1,500 units, Shenzhen Stoneworks)
   Skill to use: supplier-negotiation-assistant

2. Launch the Slow Morning Bundle as next promo
   Skill to use: landing-page-copywriter

3. Confirm cart-to-checkout 0.9pt dip wasn't caused by a recent
   Shopify settings change (1-day, may resolve on its own)

4. Increase Retargeting 30d budget 15-20% and queue 1-2 fresh creatives
   (frequency 3.4, approaching fatigue zone)
```

---

## What's notable about this digest

- The anomalies section is empty (good news) but the section still renders so the reader sees "no anomalies"
- The watch-items (Browse Abandonment dip, checkout funnel) are surfaced as soft signals, not anomalies
- Two cross-skill items show up (inventory + bundle) — the buyer sees them clearly without alarm
- Suggested actions are concrete and skill-referenced

---

## Time to read

This digest is ~3 pages of .docx. A founder reading on phone with coffee:
- Header + summary + verdict: 15 seconds
- Yesterday's numbers: 30 seconds
- Channel breakdown table: 30 seconds
- Skim through ads + email + traffic: 90 seconds
- Cross-skill queue + suggested actions: 60 seconds
- **Total: ~4 minutes**

The healthy-day digest is light because there's nothing to dig into.

---

## What the same data would look like via dashboards instead

To get the same picture via dashboards, the founder would have to:
- Open Shopify Home: 30s
- Open Klaviyo Analytics: 60s (load, filter to yesterday, scan campaigns + flows)
- Open Meta Ads Manager: 90s (load, set columns, scan campaign-level + ad-level)
- Open GA4: 90s (load, navigate to source/medium and landing pages)
- Cross-reference timezones + reconcile differences: 5 min
- Run mental math on anomalies vs. recent days: 5 min
- Open inventory spreadsheet for reorder check: 2 min
- Check supplier email for outstanding responses: 2 min
- Open bundle plan: 1 min
- Open influencer tracker: 2 min
- **Total: 20-30 minutes daily**

This skill compresses to ~4 minutes of reading + ~10 seconds of skill run.

Cost saved: 20-25 minutes × 365 days = ~120-150 hours per year.
