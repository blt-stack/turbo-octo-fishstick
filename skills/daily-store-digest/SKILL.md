---
name: daily-store-digest
description: >
  Produces a morning briefing for solo e-commerce operators by pulling yesterday's data from Shopify
  (revenue, orders, AOV, top SKUs), Klaviyo (campaign and flow performance), Meta Ads (spend, ROAS,
  fatigue), and GA4 (sessions, funnel). Runs statistical anomaly detection against a 7-day rolling
  baseline and surfaces cross-skill action items (stockout-imminent SKUs, overdue supplier responses,
  undeployed bundles, pending influencer follow-ups). Outputs a single narrative .docx briefing (3-5
  pages, 11 sections) with verdict (Healthy / Needs Attention / Critical) and ranked Suggested Actions
  for Today. Use this skill when the user asks for a daily digest, morning briefing, store digest,
  'how did we do yesterday,' 'what should I focus on today,' or 'give me my numbers.' Pairs with the
  scheduler to auto-run each morning.
---

# Daily Store Digest

Morning briefing that pulls Shopify + Klaviyo + Meta Ads + GA4 yesterday-data, runs anomaly detection vs. a 7-day rolling baseline, and surfaces cross-skill action items from the inventory, supplier, bundle, and influencer caches. One .docx per morning.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Determine target date.** Default: yesterday in buyer's timezone.
3. **Pull yesterday's data from 4 sources.** Shopify, Klaviyo, Meta Ads, GA4 (graceful degradation when a source is missing).
4. **Pull comparison-window data.** Last 7 days (rolling baseline) + same-day-last-week + same-day-last-year if available.
5. **Run anomaly detection.** Statistical: flags metrics >2 stdev or >3 stdev from 7-day rolling baseline.
6. **Read cross-skill caches.** Inventory reorder triggers, supplier pending responses, bundle opportunities, influencer follow-ups due.
7. **Compute verdict.** Healthy / Needs Attention / Critical based on anomaly severity + cross-skill urgency.
8. **Render the narrative.** 10-section .docx briefing in buyer's brand voice.
9. **Report back.** File path, verdict, top 3 actions, optional offer to schedule for daily automation.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

Verify the buyer has set `daily_store_digest.timezone`. If not, ask before computing "yesterday."

---

## Step 2: Determine target date

By default, the digest covers **yesterday** in the buyer's timezone (config field `daily_store_digest.timezone`, defaults to America/New_York).

Buyer overrides supported:
- "digest for last Friday" → specific date
- "digest for the last 7 days" → range mode (skill recommends running once-per-day instead)
- "last week's digest" → 7-day rollup

The skill confirms the date out loud before pulling data.

---

## Step 3: Pull yesterday's data from 4 sources

Read `templates/data-sources.md` for the full schema per source.

### Shopify (primary)

Required metrics:
- Total revenue (gross, net of refunds)
- Order count
- Average order value (AOV)
- Conversion rate (orders ÷ sessions; needs GA4 cross-reference)
- Top 10 SKUs by revenue
- Top 10 SKUs by units
- New customers vs. returning split
- Refunds + returns count

Fallback when Shopify connector isn't connected: buyer can paste a CSV export. The skill flags the missing connector as upgrade path.

### Klaviyo (email + SMS)

Required metrics:
- Campaigns sent yesterday (count + names)
- Open rate per campaign, click rate, revenue per send
- Active flow performance (Welcome / Cart Abandon / Post-Purchase / Browse Abandonment / etc.)
- Total email-driven revenue
- Unsubscribe count
- List growth (new subscribers)

Fallback: skill flags Klaviyo data missing; digest still runs with placeholder.

### Meta Ads (paid)

Required metrics:
- Total spend
- Total ad-attributed revenue
- ROAS (revenue ÷ spend)
- CPM, CPC, CTR
- Frequency (avg impressions per user; >3.5 flags fatigue)
- Top + worst performing campaigns
- Top + worst performing ad creative

Fallback: skill flags Meta data missing.

### GA4 (traffic + behavior)

Required metrics:
- Sessions, users, new users
- Bounce rate
- Avg engagement time
- Source/medium breakdown (organic / direct / paid / email / social / referral)
- Top 10 landing pages
- Top 10 exit pages
- Cart-add → checkout → purchase funnel

Fallback: skill flags GA4 missing.

---

## Step 4: Pull comparison-window data

For each metric, the skill pulls:

- **Yesterday** (target date)
- **Day-over-Day (DoD)** comparison: yesterday vs. the previous day
- **7-day rolling baseline**: mean and stdev of the prior 7 days (anomaly window)
- **Week-over-Week (WoW)**: same-day-last-week comparison
- **Month-over-Month (MoM)**: same-day-last-month
- **Year-over-Year (YoY)**: same-day-last-year (skipped if <365 days of data)

The 7-day rolling baseline is the canonical anomaly comparator. WoW and YoY are secondary context.

---

## Step 5: Run anomaly detection

Read `templates/anomaly-detection.md`. Implementation in `scripts/anomaly_detector.py`.

For each numeric metric, the detector:

1. Computes the 7-day rolling mean and stdev (excluding yesterday)
2. Computes the z-score: `z = (yesterday - mean) / stdev`
3. Classifies:
   - `|z| < 1.0` → normal variation, not flagged
   - `1.0 <= |z| < 2.0` → notable but not anomalous; surfaced as context
   - `2.0 <= |z| < 3.0` → anomaly; flagged in digest
   - `|z| >= 3.0` → critical anomaly; flagged prominently
4. Direction matters: a -3 stdev drop in revenue is critical; a +3 stdev spike in spend is critical; a +3 stdev spike in revenue is great news worth surfacing as "what went right"

### Special cases

- **Low-volume metrics**: when the metric's 7-day mean is small (e.g., <5 orders/day for a small brand), stdev is unreliable. The skill falls back to rule-based thresholds (configured in `daily_store_digest.fallback_rules`) for low-volume metrics.
- **Sparse data**: if <7 days of comparable history exist, the skill flags reduced confidence and uses whatever baseline exists (3+ days minimum to attempt detection; below that, raw values only).
- **Weekend/weekday separation**: optionally enable `daily_store_digest.weekday_aware_baseline=true` to use the last 7 same-weekday values as the baseline instead of the last 7 calendar days. Better for stores with strong weekly seasonality.

---

## Step 6: Read cross-skill caches

Read `templates/cross-skill-integrations.md`. Implementation in `scripts/cache_reader.py`.

Four caches to read:

### `~/.the-ecommerce-seller/cache/reorder_triggers/{date}.json` (skill #12)

SKUs the inventory forecaster flagged as approaching stockout. The digest surfaces SKUs with:
- Stockout date within 14 days → "Reorder this week"
- Stockout date within 30 days → "Plan reorder this month"
- Stockout date within 60 days → flagged as context if SKU is also a top mover

### `~/.the-ecommerce-seller/cache/suppliers/{*}.json` (skill #11)

Iterates all supplier files. For each, surfaces `pending_responses` where `follow_up_due <= today`. The digest lists overdue supplier responses with letter type + days overdue.

### `~/.the-ecommerce-seller/cache/bundles/{*}.json` (skill #13)

Iterates all bundle files. For bundles not yet marked `deployed: true`, surfaces top 3 by composite score with a suggestion to launch as today's promo angle.

### `~/.the-ecommerce-seller/cache/influencers/{*}.json` (skill #14)

Iterates all influencer files. For each, surfaces `pending_responses` where `follow_up_due <= today`. Groups by tier + platform. The digest lists overdue influencer follow-ups with which follow-up variant (A/B/C) is now due.

### Optional: `~/.the-ecommerce-seller/cache/forecast_runs/` (skill #12)

If a fresh forecast run exists from the last 24 hours, surfaces method audit highlights (which SKUs switched methods, which gained seasonality detection).

---

## Step 7: Compute verdict

Three verdict levels:

| Verdict | Trigger |
|---|---|
| Healthy | No anomalies above 2 stdev; <2 cross-skill items overdue |
| Needs Attention | 1+ anomaly between 2-3 stdev; OR 3-5 cross-skill items overdue |
| Critical | 1+ anomaly above 3 stdev; OR ROAS dropped below break-even; OR stockout in <7 days for a top-10 SKU; OR 5+ overdue cross-skill items |

The verdict drives the digest's opening tone and the action priority order.

---

## Step 8: Render the narrative .docx briefing

Use `scripts/render_digest_docx.py`. Read `templates/digest-structure.md` and `templates/narrative-craft.md`.

Structure:

```
══════════════════════════════════════════════════
DAILY DIGEST — [Brand Name] — [Date covered]
Verdict: [HEALTHY / NEEDS ATTENTION / CRITICAL]
Generated: [generation timestamp]
══════════════════════════════════════════════════

[One-sentence summary tailored to verdict]

══════════════════════════════════════════════════
YESTERDAY'S NUMBERS
══════════════════════════════════════════════════
Revenue:        $X      (DoD ±X%, WoW ±X%, MoM ±X%)
Orders:         N       (DoD ±X%, WoW ±X%)
AOV:            $X      (DoD ±X%, WoW ±X%)
Conversion:     X.X%    (DoD ±X.X pts, WoW ±X.X pts)
Sessions:       N       (DoD ±X%, WoW ±X%)

══════════════════════════════════════════════════
ANOMALIES DETECTED (vs. 7-day rolling baseline)
══════════════════════════════════════════════════
[Per anomaly:]
- Metric: [name]
  Yesterday: [value]
  Baseline: [mean ± stdev]
  Z-score: [Nσ]
  Severity: [notable / anomaly / critical]
  Direction: [↑ / ↓]
  Likely cause: [hypothesis based on cross-data inspection]

══════════════════════════════════════════════════
CHANNEL BREAKDOWN
══════════════════════════════════════════════════
[Source breakdown table from GA4 + revenue attribution]

══════════════════════════════════════════════════
TOP SKUs YESTERDAY
══════════════════════════════════════════════════
Movers (up vs. 7-day avg):
- [SKU] [+X%, $X yesterday vs. $X avg]
- ...

Decliners (down vs. 7-day avg):
- [SKU] [-X%, $X yesterday vs. $X avg]
- ...

Top 5 by revenue: [...]

══════════════════════════════════════════════════
EMAIL + SMS PERFORMANCE
══════════════════════════════════════════════════
Campaigns sent: [count]
Total email revenue: $X (X% of yesterday's revenue)
Top campaign: [name] — [open/click/RPS]
Active flows: [Welcome: X opens, $X revenue]...
List growth: [+N subscribers]

══════════════════════════════════════════════════
PAID ADS (META)
══════════════════════════════════════════════════
Spend: $X
Revenue: $X
ROAS: X.Xx (baseline X.Xx; [direction])
CPM: $X | CPC: $X | CTR: X.X% | Frequency: X.X
Top campaign: [name] $X spend $X revenue X.Xx ROAS
Worst campaign: [name] $X spend $X revenue X.Xx ROAS [flag: PAUSE?]

[Fatigue check if any campaign frequency >3.5]

══════════════════════════════════════════════════
TRAFFIC + ON-SITE
══════════════════════════════════════════════════
Sessions: X | New users: X | Bounce: X.X%
Top landing pages: [list]
Funnel: Add-to-cart X% → Checkout X% → Purchase X.X%

══════════════════════════════════════════════════
NEEDS ATTENTION TODAY (cross-skill action queue)
══════════════════════════════════════════════════
INVENTORY:
- [SKU] stocks out in [N days] — reorder needed
- ...

SUPPLIERS:
- [Company] overdue [N days] on [letter type]
- ...

BUNDLES:
- [Bundle name] (composite score X) — not yet deployed
- ...

INFLUENCERS:
- [@handle] follow-up [variant A/B/C] due today
- ...

══════════════════════════════════════════════════
SUGGESTED ACTIONS FOR TODAY
══════════════════════════════════════════════════
1. [Top-priority action with rationale]
2. [Second action]
3. [Third action]
4. [Optional fourth]
5. [Optional fifth]
══════════════════════════════════════════════════
```

Saved as `digest_{date}.docx` in `config.output_folder`.

---

## Step 9: Report back

Tell the buyer:
1. File path (`computer://` link)
2. Verdict + one-line summary
3. Top 3 actions extracted from the digest
4. If not already scheduled: offer to schedule the digest to run daily via the scheduler

Example wrap-up:

> Verdict: NEEDS ATTENTION. Revenue dropped 18% DoD (1.4σ below baseline; within notable range), ROAS dropped to 1.8x (down from 3.1x baseline; 2.9σ — anomaly), and 2 SKUs are stocking out within 14 days.
>
> Top actions today:
> 1. Pause the "Spring sale broad" campaign (frequency 4.2, ROAS 0.9 — fatigued)
> 2. Place reorder for River Stone Pour-Over (14 days to stockout)
> 3. Reply to Marcus's response (came in yesterday, sitting in your DMs)
>
> Want me to schedule this digest to run every morning at 7am?

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill asks for CSV upload; digest still runs with that data |
| Klaviyo | Email section blank; skill flags as upgrade path |
| Meta Ads | Ads section blank; skill flags |
| GA4 | Traffic + funnel section blank; conversion rate is omitted |
| Any cache (`~/.the-ecommerce-seller/cache/...`) | Section is omitted from the "Needs Attention" queue |

The skill always produces a digest — connectors enrich the picture.

---

## Edge cases

- **No yesterday data yet (early-morning run before yesterday's data fully reconciled)**: skill flags and offers to either (a) wait and re-run, or (b) proceed with partial data (e.g., Shopify but not yet Meta which reports on a delay)
- **Brand-new store with <7 days of history**: anomaly detection downgraded to "tracking" mode; digest reports raw values + DoD only, no z-scores
- **Weekend digest**: if `daily_store_digest.skip_weekends=true`, skill skips Saturday and Sunday digests by default; Monday digest covers the whole weekend
- **One-off promo day (anomaly in a known-good direction)**: skill detects unusual spend or revenue spikes and asks if this is a known promo day before classifying as critical
- **Time zone mismatch**: buyer in PT but Shopify reports in UTC; skill normalizes everything to buyer's configured timezone and reports start/end of "yesterday" explicitly
- **Multiple stores under one Shopify account**: skill requires buyer to specify which store via config; doesn't auto-pick
- **Data source returns error mid-fetch**: skill renders partial digest with explicit gaps + flag in narrative; never silently omits

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config (extended with `daily_store_digest` section)
- `templates/data-sources.md` — per-source metric schemas (Shopify / Klaviyo / Meta Ads / GA4)
- `templates/anomaly-detection.md` — statistical methodology (7-day rolling baseline + stdev; weekday-aware variant; low-volume fallback)
- `templates/revenue-section.md` — revenue + orders + AOV narrative methodology
- `templates/ads-section.md` — Meta Ads narrative methodology + fatigue detection rules
- `templates/email-section.md` — Klaviyo campaign + flow narrative methodology
- `templates/traffic-section.md` — GA4 traffic + funnel narrative methodology
- `templates/cross-skill-integrations.md` — cache schemas + how each integration surfaces in the digest
- `templates/digest-structure.md` — the 10-section narrative .docx structure
- `templates/narrative-craft.md` — brand-voice-aware narrative tone rules
- `scripts/config_loader.py` — shared config loader
- `scripts/anomaly_detector.py` — z-score anomaly detection + weekday-aware variant
- `scripts/cache_reader.py` — reads all 4 cross-skill caches + aggregates action queue
- `scripts/render_digest_docx.py` — single-mode .docx renderer
- `examples/daily-digest-healthy-example.md` — what a calm-day digest looks like
- `examples/daily-digest-critical-example.md` — what a critical-day digest looks like (multiple anomalies + overdue cross-skill items)
