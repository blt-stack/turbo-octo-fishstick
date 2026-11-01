# Tier Classification

Follower count tiers + voice register per tier. The first decision in any influencer outreach.

## The 4 tiers

| Tier | Follower range | Engagement rate range | Voice register |
|---|---|---|---|
| Nano | 1K - 10K | 4-15% | Peer-to-peer, casual, warm |
| Micro | 10K - 100K | 2-7% | Friendly professional |
| Mid-tier | 100K - 500K | 1-3% | Professional, business-aware |
| Macro | 500K+ | 0.5-2% | Formal, often manager-mediated |

## Why tiers matter

Each tier behaves differently — content rhythm, response time, decision-making, payment expectations. A nano outreach written in macro voice reads as condescending; a macro outreach written in nano voice reads as unprofessional.

## Tier signals beyond follower count

Follower count alone is misleading. The skill also considers:

- **Engagement rate**: a 50K creator with 8% engagement is closer to a micro behavior pattern; a 50K creator with 0.4% engagement is closer to mid-tier behavior
- **Posting frequency**: nano creators often post daily; macros may post 2-3×/week
- **Content production quality**: a nano with cinematic-quality video may behave like a micro
- **Existing brand collab history**: a nano with 20 brand collabs already behaves like a micro

When the data is available, the skill uses a composite score rather than just follower count.

## Per-tier characteristics

### Nano (1K - 10K followers)

**Behavior:**
- Often respond within hours-to-1-day
- High engagement rates (loyal small audience)
- Often manage their own DMs
- Open to gifted-only collabs
- Don't usually have media kits or rate cards

**Outreach voice:**
- Warm, peer-to-peer
- Lowercase ok where it matches their style
- First-name only ("hey Maya")
- Casual sign-off ("— Jamie")
- Emoji acceptable if on-brand for both
- Short paragraphs

**Pitfalls:**
- Don't be too formal — reads as condescending
- Don't be too business-y — they're not running an agency
- Don't promise huge reach in return — they know they're nano

### Micro (10K - 100K)

**Behavior:**
- Respond within 1-7 days
- Often manage their own outreach
- Many have a media kit or rate card
- Mix of gifted + paid; depends on tier
- May have brand collab boundaries (e.g., "no fast fashion")

**Outreach voice:**
- Friendly professional
- "Hi [First name]" greeting
- Full punctuation
- Sentence-level emoji acceptable
- Moderate sign-off ("Best, Jamie")

**Pitfalls:**
- Don't assume they'll do gifted-only — many have moved to paid
- Don't underprice — they know their rate
- Don't be too casual — they want to be taken seriously

### Mid-tier (100K - 500K)

**Behavior:**
- Respond within 7-21 days
- Often have managers or agents
- Media kits standard; rate cards normal
- Paid partnerships expected; gifted rare
- Usage rights + exclusivity considerations matter

**Outreach voice:**
- Professional, business-aware
- "Hi [First name]" or "Hi [First name] [Last name]"
- Full punctuation, minimal emoji
- Reference their professional brand, not just their content
- "Best regards, [Name + role]" sign-off

**Pitfalls:**
- Don't pitch gifted-only (waste of their time)
- Don't lowball
- Don't skip the contract conversation
- Don't bypass their manager if one is listed

### Macro (500K+)

**Behavior:**
- Respond within 14-45 days (often through manager)
- Almost always managed
- Detailed media kits + rate sheets
- Paid partnerships only; rates negotiable
- Heavy emphasis on creative control + usage rights

**Outreach voice:**
- Formal business correspondence
- "Hi [First name] team" if managed
- Full punctuation, no emoji
- Reference their brand as a business entity
- "Best regards, [Name + brand + brand role]"
- Often via email, not DM

**Pitfalls:**
- Don't DM the creator if they have a managed contact
- Don't pitch without specifics (timeline, deliverables, budget)
- Don't underprice — better to skip than lowball
- Don't expect quick replies

## Cross-tier campaign strategy

A balanced influencer campaign typically includes a mix:

- **Nano (10-30 creators)**: high volume, authentic voices, low cost per creator
- **Micro (5-15 creators)**: better content quality, moderate cost, balance of authenticity + reach
- **Mid-tier (2-5 creators)**: focal points of campaign reach + credibility
- **Macro (0-1 creator)**: only when budget justifies; brand-anchor

The skill recommends this mix unless the buyer specifies a single-tier focus.

## Special cases

### Creator with rapidly-growing follower count
A creator who went from 8K to 50K in 90 days behaves more like a nano in approach (still hands-on, open to gifted) but their rate expectations may have updated. Pitch as nano + offer micro-tier compensation.

### Creator with declining following
A creator who's dropped from 200K to 100K may be unwilling to take previous rate levels. Pitch carefully; engagement quality often persists even when follower count drops.

### Niche creator with very small but very engaged audience
A 3K-follower nano with 25% engagement rate and a perfectly-aligned audience is often more valuable than a 100K mid-tier in the wrong niche. The skill weights niche alignment heavily.

## Tier determination workflow

```python
def classify_tier(follower_count: int, engagement_rate: float = None) -> str:
    if follower_count < 10_000:
        base = "nano"
    elif follower_count < 100_000:
        base = "micro"
    elif follower_count < 500_000:
        base = "mid_tier"
    else:
        base = "macro"

    # Optional refinement based on engagement
    if engagement_rate is not None:
        if base == "micro" and engagement_rate > 0.08:
            return "nano"  # behaves like nano
        if base == "mid_tier" and engagement_rate < 0.008:
            return "macro"  # behaves like macro
    return base
```

The skill outputs both the raw classification and any adjusted recommendation.
