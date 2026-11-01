# Post Context Extraction

When the buyer pastes 1-3 recent post captions or video descriptions from a creator, the skill extracts signals that flow into the personalized opener.

## What to extract

### 1. Content themes
What are the creator's repeated topics? Topic tags:
- Coffee / brewing / cafés
- Skincare / morning routine / self-care
- Cooking / recipes / food
- Travel / outdoors / camping
- Workspace / productivity / desk setups
- Fitness / wellness
- Tech / gadgets
- Fashion / outfits
- Home / interiors
- Parenting / family
- Mental health / mindfulness

Often a creator has 1 primary theme + 2-3 secondary. The skill identifies all of them.

### 2. Voice signals
- **Formal vs. casual**: pronoun choice, contractions, hashtag usage
- **Earnest vs. ironic**: emoji direction, framing of opinions
- **Personal vs. tutorial**: first-person experience vs. how-to teaching
- **Long-form vs. punchy**: sentence length patterns

The opener should match the creator's voice register.

### 3. Specific recent references
- A specific product/brand they mentioned
- A specific moment or experience they referenced
- A specific takeaway or observation they made
- A specific number/stat/anecdote in their content

These are the highest-value signals for the personalized opener. The opener should call back to at least one specific reference.

### 4. Current campaign signals
- Hashtags suggesting current paid partnerships (#ad, #sponsored, #partner)
- Hashtags suggesting an active campaign (#brand_x_campaign)
- Recent mentions of other brands

The skill checks if the creator is currently in a competitor's partnership window. If yes, flag and recommend waiting 30-60 days before pitching.

### 5. Audience signals
- Comment language style (helps gauge audience demographic)
- Comment topics (helps confirm niche)
- Engagement patterns (high vs. low engagement on recent posts)

These help confirm the audience fit, but require seeing recent comments — buyer can paste those too.

## Extraction process

When the buyer pastes "I want to reach out to @[handle]. Here are 3 recent post captions:" followed by the captions, the skill:

1. **Reads each caption fully**
2. **Identifies recurring keywords** (manual or via simple frequency analysis)
3. **Maps keywords to content themes**
4. **Identifies the most specific reference** that the opener should call back to
5. **Detects voice register** by counting markers (emoji density, hashtag usage, formality signals)
6. **Flags any disqualifying signals** (current competitor campaign, content shift away from brand-relevant topics, audience misalignment)

## What "specific reference" looks like

| Vague (avoid) | Specific (use) |
|---|---|
| "love your coffee content" | "your post about the espresso-vs-pour-over taste test cracked me up" |
| "great morning routine vibes" | "your line about not photographing your skincare anymore made me actually want to do mine" |
| "you make beautiful pieces" | "the ceramic mug you posted Tuesday — the one with the unfinished edge — is exactly the aesthetic we built our brand around" |

The specific reference proves the brand actually engaged with the creator's content rather than running a template.

## The 1-2 specific reference rule

A great cold outreach opener contains 1-2 specific references. More than 2 starts to feel like surveillance ("I see you posted X on Monday and Y on Wednesday and Z on Friday"). Less than 1 reads as a template.

The skill enforces this: the opener must have at least 1 specific reference, no more than 2.

## What the buyer should paste

The skill's prompt to the buyer when collecting post context:

> "Paste 1-3 recent captions or video descriptions from [creator handle]. The most useful are:
> - Their most recent post
> - A post that fits the type of content the brand could fit into
> - A post where the creator says something specific that resonated
>
> Paste them raw — captions, hashtags, link descriptions all included."

The buyer typically pastes 1-3 captions of 50-500 words each. The skill reads all of them.

## When post context is missing

If the buyer can't or won't paste recent posts:
- Skill flags "outreach quality will be reduced without specific context"
- Outreach defaults to brand-context-led rather than creator-context-led (still has personalization slots but they're filled by brand pitch rather than creator references)
- Skill recommends buyer paste context before sending if at all possible

A creator's profile bio + 1 recent caption is the minimum useful context. Below that, outreach is essentially generic + low-conversion.

## When post context reveals misalignment

Common misalignment signals:

- **Creator's content is all sponsored**: signals high price + saturated; pitch only if budget supports
- **Creator's content shifted away from brand-relevant topics**: e.g., a former coffee creator now posting about cars; pitch only if there's still a relevant angle
- **Creator is mid-controversy or hiatus**: wait
- **Creator's audience demographic doesn't match brand**: skill flags and recommends finding a better fit
- **Creator's brand collabs include direct competitors**: pitch carefully, with awareness of exclusivity windows

The skill outputs a brief alignment audit before drafting:

```
ALIGNMENT AUDIT
- Content themes: coffee brewing, slow mornings, home interiors (3/3 brand-aligned ✓)
- Voice register: warm, ironic, conversational — matches brand voice tone
- Current campaigns visible: 1 sponsored post for [competitor coffee brand] 3 weeks ago — recommend 30+ day window before pitching
- Audience demographic: appears US/UK 25-40, primarily female, design-aware — matches brand audience ✓
- Recent references: 'pour-over with the chocolate-milk taste test joke' — specific reference candidate for opener
```

## Caching extracted context

The extracted themes get written to the influencer memory cache:

```json
"content_themes": ["coffee_brewing", "slow_mornings", "home_interiors"],
"voice_register": "warm_ironic_conversational",
"recent_references": [
  {"caption_date": "2026-05-15", "key_reference": "espresso-vs-pour-over taste test"},
  {"caption_date": "2026-05-18", "key_reference": "chocolate-milk joke about taste"}
],
"alignment_score": 8.5,
"alignment_notes": "Strong brand fit; potential competitor overlap window 3 weeks ago"
```

This lets future outreach to the same creator reference these themes without re-extraction.

## Re-extraction frequency

When the buyer comes back to the same creator 30+ days later:
- Skill recommends re-pasting recent posts (creator content drifts)
- Old themes stay in cache but get marked as `last_validated`
- Skill compares old themes vs. new posts to detect content shifts
