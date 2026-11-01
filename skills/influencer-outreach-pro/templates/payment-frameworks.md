# Payment Frameworks

The three frameworks the skill recommends per tier, with rate guidance and deliverables expectations.

## The three frameworks

### 1. Gifted product only

The brand sends product. The creator decides whether and how to post. No cash exchange.

**Deliverables**: not contractually guaranteed; "we'd love if you share but no pressure"
**Disclosure required**: yes (FTC) — #gift / #ad on most platforms
**Typical tier fit**: nano + micro (sometimes mid-tier with high brand alignment)
**Brand cost**: product cost only
**Risk**: creator may not post; no guaranteed deliverable
**Reward**: highest authenticity when creator does post; lowest cost; tests fit before paid commitment

### 2. Hybrid (product + payment)

The brand sends product + pays a flat fee. Deliverables are contractually agreed.

**Deliverables**: 1-2 posts typically (Reel + Story, video + caption, etc.)
**Disclosure required**: yes — #ad / #sponsored + platform paid-partnership tag
**Typical tier fit**: micro + mid-tier
**Brand cost**: product + cash
**Risk**: medium; creator may produce content that misses the brief
**Reward**: balance of authenticity + guaranteed deliverable; standard for most campaigns

### 3. Paid partnership

The brand pays a cash fee for a defined deliverables package. Product may or may not be included.

**Deliverables**: contractually specified (post types, count, usage rights, exclusivity window)
**Disclosure required**: yes — full #ad / #sponsored / platform paid-partnership tag
**Typical tier fit**: mid-tier + macro
**Brand cost**: cash + sometimes product
**Risk**: lower (contractual); higher financial commitment
**Reward**: most predictable outcome; required for serious mid-tier+ campaigns

## Rate guidance per tier

These are 2026-baseline US/EU/CA rates. Niche, geography, and engagement quality vary significantly.

### Nano (1K - 10K)

| Framework | Range | Notes |
|---|---|---|
| Gifted only | $0 | Product value typically $20-150 |
| Hybrid | $25 - $150 + product | Per post; often for 1-2 deliverables |
| Paid | $50 - $200 + product | Per post |

Sample nano deal: gifted $40 product + $50 = "post a Reel + 2 Stories about it"

### Micro (10K - 100K)

| Framework | Range | Notes |
|---|---|---|
| Gifted only | $0 | Increasingly rare above 50K |
| Hybrid | $150 - $800 + product | Per post; varies wildly by niche |
| Paid | $300 - $1,500 + product | Per post; higher for video |

Sample micro deal: $80 product + $400 hybrid = "post a Reel within 14 days + 3 Stories with link"

### Mid-tier (100K - 500K)

| Framework | Range | Notes |
|---|---|---|
| Gifted only | Rare | Only for extreme brand alignment |
| Hybrid | $800 - $3,500 + product | Per post |
| Paid | $1,500 - $8,000 + product | Per post; YouTube dedicated videos higher |

Sample mid-tier deal: $200 product + $2,500 paid = "dedicated Reel + Stories + 1 in-grid post over 30 days; 1-week exclusivity"

### Macro (500K+)

| Framework | Range | Notes |
|---|---|---|
| Gifted only | Rare | Only for celebrity-tier brands |
| Hybrid | $3,500 - $15,000 + product | Less common at this tier |
| Paid | $5,000 - $50,000+ + product | Often negotiated bespoke |

Sample macro deal: $500 product + $12,000 paid = "dedicated post + Reel + Story takeover over 60 days; usage rights + 30-day exclusivity in category"

## Variables that shift rates

These adjust the baseline up or down:

| Factor | Direction | Magnitude |
|---|---|---|
| Engagement rate above 8% | Up | +50-100% |
| Engagement rate below 1% | Down | -30-50% |
| Niche match (perfect) | Up | +20-30% |
| Niche match (loose) | Down | -20-30% |
| Geography premium (US/UK creators for US brand) | Up | +20% |
| Geography discount (LATAM/SEA creators for US brand) | Down | -30-50% |
| Dedicated video on YouTube | Up | +200-400% vs. IG post equivalent |
| Story-only on Instagram | Down | -50-70% vs. feed post |
| Usage rights (brand can re-use content) | Up | +30-50% |
| Exclusivity window (no competitor for X days) | Up | +20-40% per week |
| Whitelist (brand can run as ad) | Up | +30-50% |

The skill applies these adjustments and outputs a recommended range, not a single price.

## Framework recommendation logic

```python
def recommend_framework(tier, brand_alignment, brand_budget_per_creator):
    if tier == "nano":
        if brand_budget_per_creator < 30:
            return "gifted_only"
        else:
            return "hybrid"
    elif tier == "micro":
        if brand_alignment == "perfect" and brand_budget_per_creator < 100:
            return "gifted_only"  # rare but possible
        elif brand_budget_per_creator < 600:
            return "hybrid"
        else:
            return "paid"
    elif tier == "mid_tier":
        if brand_budget_per_creator < 2000:
            return "hybrid"
        else:
            return "paid"
    elif tier == "macro":
        return "paid"
```

The skill outputs the recommendation + rationale.

## Negotiating gifted-only with mid-tier+

Sometimes mid-tier creators will accept gifted-only IF:
- Brand alignment is extraordinary (creator is already a fan)
- Brand has cultural relevance the creator wants association with
- Product value is genuinely high ($300+)

The skill includes this as an option but flags low odds.

## Affiliate as a complement, not a framework

Many partnerships include affiliate links as a complement to whatever framework is being used:

- Nano with hybrid: $50 + product + 10% affiliate commission on referrals
- Micro with paid: $1000 + product + tracked link + 8% affiliate

Affiliate isn't its own framework — it's an add-on. The skill recommends including affiliate when:
- The brand has the infrastructure (tracked links, payout system)
- The creator has demonstrated track-record of driving sales (not just impressions)
- The product has decent margin to absorb the commission

## Calculating campaign budget

For a balanced campaign:

```
Budget = (nano_count × nano_rate_avg) + (micro_count × micro_rate_avg) + ...

Example for a $5,000 campaign:
- 15 nano @ $50 = $750
- 8 micro @ $400 = $3,200
- 1 mid-tier @ $1,500 = $1,500 (over budget; adjust to 0 mid-tier)
- Revised: 15 nano @ $50 + 10 micro @ $400 + 0 mid-tier = $4,750
```

The skill outputs budget exposure per scenario.

## When to skip a tier

Sometimes a campaign should focus only on one tier:

- **Nano-only**: pre-launch or community-building; budget under $2K
- **Micro-only**: focused launch campaign; budget $3-15K
- **Mid-tier-only**: brand-positioning campaign; budget $10-50K
- **Macro-only**: major launch or rebrand; budget $50K+

The skill recommends tier mix based on stated budget.

## Don't lowball

The skill enforces a hard floor: it won't recommend a rate below 60% of the lower bound of the tier range. If the buyer's budget doesn't support that, the skill recommends going to a smaller tier instead of lowballing the targeted tier.

A lowball offer from a brand:
- Gets ignored by serious creators
- Signals lack of seriousness
- Burns the brand's reputation in creator networks (creators talk)
- Doesn't save money — saves the wrong money
