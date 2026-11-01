# Digest Structure — 10-Section Narrative .docx

The complete structure of the daily digest output. Order matters — sections build context for each other.

## Top-level structure

```
1. HEADER + VERDICT
2. ONE-SENTENCE SUMMARY
3. YESTERDAY'S NUMBERS (revenue section)
4. ANOMALIES DETECTED
5. CHANNEL BREAKDOWN
6. TOP SKUs YESTERDAY
7. EMAIL + SMS PERFORMANCE
8. PAID ADS (META)
9. TRAFFIC + ON-SITE
10. NEEDS ATTENTION TODAY (cross-skill action queue)
11. SUGGESTED ACTIONS FOR TODAY
```

(11 sections counting header — section 1 is the title block.)

## Section 1: Header + Verdict

```
══════════════════════════════════════════════════
DAILY DIGEST — [Brand Name]
Yesterday: [Date covered] ([weekday]) — [timezone]
Verdict: [HEALTHY / NEEDS ATTENTION / CRITICAL]
Generated: [generation timestamp]
══════════════════════════════════════════════════
```

### Verdict colors (in .docx)

- HEALTHY: green
- NEEDS ATTENTION: orange
- CRITICAL: red

## Section 2: One-sentence summary

A single sentence that captures the day's headline. Examples:

- "Quiet day — revenue tracked within normal range; no anomalies flagged."
- "Mixed day — revenue down 18% DoD but within normal variance; ROAS dipped to 2.4x flagged as anomaly."
- "Hard day — revenue 2.9σ below baseline + ROAS collapsed to 0.9x + 2 SKUs stocking out within 7 days."

This sentence sets reader expectations. It should match the verdict.

## Section 3: Yesterday's numbers (revenue section)

See `revenue-section.md`. Includes:
- Revenue, Orders, AOV, Conversion, Sessions
- DoD / WoW / MoM / YoY comparisons (where data available)
- Anomaly status
- Customer mix
- Refunds (if notable)

## Section 4: Anomalies detected

Lists every anomaly flagged by the detector, grouped by severity:

```
CRITICAL (>3σ):
- [Metric] yesterday [value] vs. baseline [mean ± stdev] (z=[N]σ ↓/↑)
  Likely cause: [hypothesis]

ANOMALY (2-3σ):
- ...

NOTABLE (1-2σ):
- ...
```

If no anomalies in a tier, that tier is omitted.

If no anomalies at all: "No anomalies flagged. Metrics tracked within normal range."

## Section 5: Channel breakdown

Pulled from GA4 source/medium with revenue attribution. Format:

```
Channel              Sessions  Revenue   % of revenue   Conv Rate
─────────────────────────────────────────────────────────────────
Email (Klaviyo)      220       $1,280    28.4%          5.9%
Paid (Facebook)      480       $1,450    32.2%          2.9%
Organic (Google)     620       $1,100    24.4%          2.4%
Direct               310       $920      20.4%          3.5%
Social (organic)     190       $250      5.6%           1.8%
─────────────────────────────────────────────────────────────────
Total                1,820     $4,500    100%           2.58%
```

Plus 1-2 sentences of interpretation:

> "Email pulled above its usual 18-22% share (28% yesterday) thanks to the Memorial Day campaign. Paid ROAS came in at 3.02x — normal."

## Section 6: Top SKUs yesterday

```
Movers (up vs. 7-day average):
- [SKU name] — [units yesterday] units, $[revenue]
  vs. [units avg]/[$ avg] (+[N]% revenue)

Decliners (down vs. 7-day average):
- [SKU name] — [units yesterday] units, $[revenue]
  vs. [units avg]/[$ avg] (-[N]% revenue)

Top 5 by revenue yesterday:
1. [SKU name] [$N]
2. ...
```

Show top 5 movers, top 5 decliners, top 5 by revenue. Omit if data is sparse.

## Section 7: Email + SMS performance

See `email-section.md`. Includes:
- Campaigns sent
- Flow performance
- Email % of total revenue
- List growth
- Deliverability watch items

## Section 8: Paid Ads (Meta)

See `ads-section.md`. Includes:
- Account-level spend / revenue / ROAS
- Per-campaign breakdown
- Fatigue check
- Pause + scale candidates
- Top + worst creative

## Section 9: Traffic + on-site

See `traffic-section.md`. Includes:
- Sessions / users / engagement
- Source breakdown (cross-references channel breakdown)
- Top landing pages
- Funnel step performance

## Section 10: Needs attention today

The cross-skill action queue. Grouped by source:

```
INVENTORY:
- [SKU name] — stocks out in [N days]; reorder [N units] needed
- ...

SUPPLIERS:
- [Company] — [letter type] overdue [N days]
- ...

BUNDLES:
- [Bundle name] (composite score [N]/100) — undeployed
  Recommend: launch as today's promo
- ...

INFLUENCERS:
- @[handle] ([platform], [tier]) — Variant [A/B/C] due [today/N days ago]
- ...
```

If a section is empty, mark it: "INVENTORY: No reorder triggers. Healthy."

## Section 11: Suggested actions for today

Top 3-5 actions ranked from the action queue:

```
1. [Action description with rationale]
2. [Action]
3. [Action]
4. [Optional]
5. [Optional]
```

Each action includes:
- What to do (specific)
- Why now (urgency)
- Which skill to use (if applicable)

Example:

```
1. Pause "Spring sale push" (frequency 4.2, ROAS 1.2x for 3 days; creative fatigued).
   Action: pause in Meta Ads Manager.

2. Place reorder for River Stone Pour-Over (stocks out in 14 days at p50;
   supplier lead time 60 days — actually overdue against lead time).
   Action: run skill #11 (Supplier Negotiation Assistant) with "draft reorder
   to Shenzhen Stoneworks for 1,500 units."

3. Follow up with @maya_brews (Variant A due today; gifted nano outreach
   sent 7 days ago, no reply).
   Action: run skill #14 (Influencer Outreach Pro) with "follow up with
   @maya_brews."
```

## Total length target

The complete digest should be **3-5 pages of .docx output**:
- 1.5-2 pages of data sections (3-10)
- 0.5-1 page of cross-skill action queue (10)
- 0.5 page of suggested actions (11)
- Sections collapse cleanly when data is missing or absent

## Document formatting

The renderer (`scripts/render_digest_docx.py`) uses:

- Title font: 18pt bold, brand-aligned color
- Section headers: 14pt bold
- Subheaders: 11pt bold
- Body: 10-11pt regular
- Divider line: `══` characters, centered, for visual section breaks
- Anomaly flags: red text for critical, orange for anomaly, gray for notable
- Verdict label: matching color box around the verdict text
- Numbered actions in the Suggested Actions section
- Bulleted lists where appropriate (anomalies, action items)

## When data is partial

The renderer omits sections when their data is fully missing rather than rendering empty placeholders. Exception: the "Anomalies Detected" and "Needs Attention" sections always render even when empty — they show "No anomalies / No items" — because their absence is itself information.
