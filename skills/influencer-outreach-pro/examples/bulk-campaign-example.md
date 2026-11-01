# Bulk Influencer Campaign — Reference Example

Shows what gets produced when the buyer says "Build me a campaign of 20 nano + micro coffee creators on Instagram + TikTok for our Q3 launch. Here's the creator list + recent post context for each: [pasted CSV]."

**Brand:** {{brand_name}} (Brooklyn pour-over brand)
**Campaign:** Q3 Launch — Slow Morning Bundle Push
**Creator count:** 20 (12 nano + 8 micro)
**Output:** Single `.xlsx` with 5 sheets

---

## Input the buyer provided

```
Campaign name: q3_launch_slow_morning_push
20 creators in a CSV with these columns:
  handle, platform, follower_count, niche_hint, recent_post_excerpts (3 each), email_if_known

12 nano-tier (1.5K-9K), 8 micro-tier (12K-85K)
12 Instagram, 6 TikTok, 2 cross-platform (IG + TikTok primary IG)
Budget cap: $4,000 cash + $2,500 product value
```

---

## Discovery + extraction process

For each creator, the skill:

1. Slugifies handle → looks up `~/.the-ecommerce-seller/cache/influencers/{slug}.json`
2. If known with strained / declined / blacklisted stage → flags + skips
3. If known with prior healthy collab → routes to "returning creator" outreach template
4. If new → runs context extraction on the 3 pasted post excerpts
5. Picks pitch (single SKU vs. bundle) based on themes
6. Picks framework + rate based on tier + buyer budget
7. Drafts outreach + 3 follow-ups
8. Writes preliminary memory cache entry (stage: drafted; will be written to "outreached" stage upon send)

## .xlsx output — 5 sheets

### Sheet 1: Outreach Queue

One row per creator with all the personalized outreach data. Headers:

| Col | Header | Example value |
|---|---|---|
| A | Handle | @maya_brews |
| B | Platform | Instagram |
| C | Tier | Nano |
| D | Followers | 4,200 |
| E | Niche | pour-over + slow mornings |
| F | Content Themes | pour_over_coffee, camping_coffee, slow_mornings |
| G | Pitch | The Slow Morning Bundle |
| H | Framework | gifted_only |
| I | Rate (USD) | 0 |
| J | Product Value (USD) | 92 |
| K | Subject | (blank for DM channels) |
| L | Outreach Body | "hey maya — your camping pour-over update made me laugh..." |
| M | Expected Reply By | 2026-05-29 |
| N | Status | Drafted |

Tier column is color-coded:
- Nano: light green
- Micro: green
- Mid-tier: yellow
- Macro: light red

Status column color-coded:
- Drafted: yellow
- Sent: blue
- Responded: green
- Negotiating: blue
- Agreed: dark green
- Declined: red
- Posted: bright green

Frozen pane at B2; auto-filter enabled.

### Sheet 2: Campaign Summary

```
Metric                                              Value
Total creators                                      20

Tier distribution
  Nano                                              12
  Micro                                             8

Platform distribution
  Instagram                                         12
  TikTok                                            8

Framework distribution
  gifted_only                                       12
  hybrid                                            8

Budget exposure (if all convert)
  Total cash committed                              $3,200
  Total product value                               $1,840
  Total exposure                                    $5,040

Projected reach (if all convert + 15% engagement)   ~62,400 impressions
Total combined follower base                        416,000
```

The summary tells the buyer their budget exposure matches the brief ($3,200 cash + $1,840 product = within the $4K cash / $2.5K product caps).

### Sheet 3: Disclosure Compliance

Per-creator disclosure requirements:

| Handle | Platform | Framework | Required Disclosure | Brand Monitoring |
|---|---|---|---|---|
| @maya_brews | Instagram | gifted_only | #gift in caption + "gifted by [brand]" | Review live posts within 48h of publication |
| @marcus_taste | TikTok | hybrid | TikTok Branded Content toggle ON + #ad in caption + verbal "thanks to [brand]" | Review live posts within 48h |
| ... | ... | ... | ... | ... |

The buyer cross-references this sheet against creator posts to verify FTC compliance after publication.

### Sheet 4: Follow-up Calendar

Chronological list of follow-up dates across all creators. Sorted ascending so today's follow-ups appear at top.

| Date | Handle | Variant | Outreach Type | Action |
|---|---|---|---|---|
| 2026-05-29 | @maya_brews | A | Soft nudge | Send Variant A |
| 2026-05-29 | @sam_coffee | A | Soft nudge | Send Variant A |
| 2026-05-30 | @lila_morning | A | Soft nudge | Send Variant A |
| 2026-06-05 | @marcus_taste | A | Soft nudge | Send Variant A |
| 2026-06-12 | @maya_brews | B | Reframed offer | Send Variant B |
| ... | ... | ... | ... | ... |

The buyer scans this each morning to see what to send today.

### Sheet 5: Influencer Memory Updates

Per-creator audit of what got written to the cache:

| Handle | Memory Cache Updates |
|---|---|
| @maya_brews | • Created new file: maya-brews.json<br>• Stage: new → outreached<br>• Logged outreach: gifted_only / IG DM / Slow Morning Bundle<br>• Set follow-up due: 2026-05-30 |
| @marcus_taste | • Updated existing file: marcus-taste.json<br>• Returning creator: 1 prior gifted collab (2025-Q4, performed well)<br>• Stage: completed → outreached<br>• Logged outreach: hybrid $400 / TikTok DM / Pour-Over Hero |
| ... | ... |

This sheet documents the cache write so the buyer can audit what changed.

---

## Status updates as the campaign progresses

The buyer updates the Status column in Sheet 1 as conversations progress:

- Day 1-3: All "Drafted" → "Sent" as buyer fires the outreach
- Day 4-7: First replies arrive → "Responded" for engaged, leave "Sent" for silent
- Day 7-10: Buyer runs the skill again with "draft follow-up A for the no-reply creators" → skill reads the cache, identifies "Sent" without "Responded," outputs follow-up A messages for each
- Day 14-21: Same pattern for follow-up B
- Day 30+: Final ask / variant C
- Concurrent: As "Responded" creators move to "Agreed," buyer fills in deliverables
- Post-publication: "Agreed" → "Posted" + buyer adds performance notes to the cache for next-campaign reference

The skill is designed to be re-run on the same campaign as state changes.

---

## Bulk campaign cache writes summary

20 cache writes total:
- 17 new creator files created
- 3 existing creator files updated (returning creators)
- All 20 transitioned stage: new/completed/declined → outreached
- 20 pending_responses entries added with tier-appropriate follow-up dates

---

## Time savings

Manually running a 20-creator influencer outreach campaign with the same depth:

| Step | Manual time per creator | Manual time × 20 |
|---|---|---|
| Read + extract themes from 3 posts | 10-15 min | 3-5 hours |
| Pick pitch (SKU vs. bundle) | 5-10 min | 1.5-3 hours |
| Draft initial outreach (personalized) | 15-25 min | 5-8 hours |
| Draft 3 follow-up variants | 15-25 min | 5-8 hours |
| Calculate follow-up dates + track in spreadsheet | 5-10 min | 1.5-3 hours |
| Document disclosure requirements | 5 min | 1.5 hours |
| Maintain influencer memory across campaigns | 5-15 min | 1.5-5 hours |
| **Total** | **60-105 min per creator** | **20-34 hours total** |

With this skill:
- Skill runs: ~30 seconds for 20 creators
- Buyer reviews + sends 20 outreaches: ~60 min
- Cache writes happen automatically
- **Total: ~1 hour for the entire campaign**

The compounding value: the cache makes the SECOND campaign 30% faster than the first, the third 40% faster, and so on — each new campaign benefits from the relationship state built across all prior outreach.

---

## Edge cases the skill flagged in this campaign

The skill audits and surfaces:

- **2 of 20 creators are currently running competitor partnerships** (detected in pasted post context) → flagged with recommendation to wait 30-60 days before outreach
- **1 creator's recent posts suggest audience demographic mismatch** (creator's audience skews 50+; brand audience skews 25-40) → flagged for buyer to confirm before sending
- **1 creator has 22K followers but only 200 likes per post** (engagement <1%) → flagged as possible inflated audience; recommend skipping or treating as smaller tier
- **3 of 20 budget calculations push the campaign $200 over the $4K cash cap** → flagged with two options: (a) reduce 3 micro rates by ~$70 each, or (b) drop 2 lowest-fit micros

The buyer reviews flags before sending. The skill never sends unilaterally — all sends are buyer-driven.

---

## What the buyer does next

1. Open the .xlsx
2. Review Sheet 1 (Outreach Queue) — scan each Outreach Body for tone fit
3. Resolve the 4 flags surfaced (3 budget, 1 mismatch) — drop or adjust
4. Send outreach over 2-3 days (not all at once — platform spam filters)
5. Update Status column as replies arrive
6. Re-run skill with "draft follow-ups for no-reply creators" when Variant A dates come due (Sheet 4 reminds)
7. Update cache with deliverables + performance as content publishes
8. End of campaign: re-run skill with "campaign performance summary" to roll up actual response rate, conversion rate, total spend, total reach, ROI vs. baseline
