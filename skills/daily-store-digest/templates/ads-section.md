# Ads Section Methodology (Meta)

The paid-ads section. Where most operators have the highest variance and the most actionable insight per dollar of attention.

## What it covers

- Yesterday's spend, revenue, ROAS
- ROAS vs. baseline
- Per-campaign spend + ROAS
- Top + worst performing creative
- Fatigue check (frequency)
- Cost-per-purchase trends

## Narrative tone

Paid-ad operators read this section daily for one reason: **decide what to pause, what to scale, and what to leave alone.** The narrative should make that decision faster, not bury it in numbers.

## Required elements

1. **Spend, revenue, ROAS** for the account
2. **Account-level ROAS vs. baseline** (with anomaly classification)
3. **Per-campaign breakdown** when more than one campaign is active
4. **Fatigue check** — any campaign with frequency >3.5
5. **Pause-candidate flags** — any campaign with ROAS <1.0x for 3+ days
6. **Top creative** — the ad that drove most ROAS yesterday
7. **Worst creative** — the ad that wasted most spend yesterday

## ROAS thresholds

Break-even ROAS varies by brand (gross margin matters). The skill uses:

- **Configured break-even ROAS** from `daily_store_digest.break_even_roas` (buyer sets based on margin)
- Default 2.0x if buyer hasn't configured
- Anomaly z-score against 7-day rolling baseline
- Plus a hard floor: any campaign or account ROAS below `break_even_roas - 0.3` for 3+ consecutive days gets flagged regardless of z-score

## Fatigue detection rules

Frequency = average impressions per unique user. When frequency climbs:

| Frequency | Status | Skill action |
|---|---|---|
| <2.0 | Healthy | Not mentioned |
| 2.0-3.0 | Healthy → mature | Not flagged (still effective range) |
| 3.0-3.5 | Mature | Mentioned as context if CTR is declining |
| 3.5-4.5 | Fatigue zone | Flagged — recommend creative refresh |
| 4.5-6.0 | Heavy fatigue | Flagged prominently — recommend pause or major refresh |
| >6.0 | Critical fatigue | Critical flag — pause campaign |

The fatigue check considers frequency trend, not just absolute value. A campaign at 4.0 frequency that's been stable for a week is less urgent than one climbing from 3.5 to 4.5 over 3 days.

## Pause-candidate framing

When a campaign should likely be paused, the skill states the recommendation directly:

> "Pause-candidate: 'Cold prospecting — broad' has run $220/day for 4 days at average ROAS 0.9x. Total spend $880, total revenue $792. Frequency held at 2.1 (not fatigue). Read: audience mismatch or creative mismatch — neither will fix with more spend. Recommend pause + refresh."

The skill never says "pause this" without justification. Always:
- The campaign name
- Days of underperformance
- Spend and revenue numbers
- Frequency/CTR context to rule out fatigue
- A one-sentence diagnosis

## Scale-candidate framing

When a campaign is overperforming:

> "Scale-candidate: 'Retargeting — 30d viewers' ran $180 at 4.0x ROAS yesterday. Frequency at 3.4 — approaching fatigue but holding for now. Daily revenue $720. Recommend increasing daily budget 15-20% and adding 1-2 new creatives within 7 days before frequency hits 4.0+."

Note: "scale" recommendations always come with the fatigue warning attached. Scaling a campaign nearing fatigue is a short-term win that becomes a long-term loss.

## Creative-level surfaces

The digest surfaces the **single best** and **single worst** ad creative yesterday:

- Best = highest ROAS in campaigns with >$50 spend
- Worst = lowest ROAS in campaigns with >$50 spend

For the best creative, the skill recommends adding it to creative-test variants or duplicating it for new audiences.

For the worst creative, the skill recommends pausing it specifically (not the whole campaign) — most often the creative is the problem, not the audience.

## What NOT to include

- Detailed cohort/audience breakdowns (lives in a deeper analytics tool, not the morning digest)
- Recommendations to change ad objectives (too operationally heavy for a morning briefing)
- New campaign suggestions (this is yesterday-focused, not strategy-planning)
- Comparisons across ad accounts if multi-account setup (defer to a multi-account view)

## Length target

3-6 short paragraphs. Should include a clear pause-recommendation or scale-recommendation when one exists.

## Example complete section

```
══════════════════════════════════════════════════
PAID ADS (META)
══════════════════════════════════════════════════

Spend: $480 | Revenue: $1,450 | ROAS: 3.02x
Baseline ROAS: 3.18x — within normal range (-0.7σ)

By campaign:
- "Retargeting — 30d viewers"
  Spend $180  Revenue $720  ROAS 4.00x  Freq 3.4
  ✦ TOP PERFORMER — Scale candidate (increase budget
    15-20%; add fresh creative before frequency hits 4.0)

- "Cold prospecting — broad"
  Spend $220  Revenue $620  ROAS 2.82x  Freq 1.5
  Healthy. Holding steady.

- "Spring sale push"
  Spend $80   Revenue $110  ROAS 1.38x  Freq 4.2
  ⚠ Fatigue zone (freq 4.2). 3-day ROAS 1.2x.
  Recommend: pause + creative refresh.

Top ad creative: "Slow Morning Reel v3" — $80 spend
$416 revenue (5.2x ROAS).
Worst ad creative: "Direct UGC product shot" —
$65 spend $26 revenue (0.4x ROAS). Pause this
specific creative.
```

The reader gets pause/scale guidance in 30 seconds.
