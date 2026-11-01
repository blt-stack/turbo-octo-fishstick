# Pitch Selection — Single SKU vs. Bundle

For each outreach, the skill picks what to pitch: a single SKU, a bundle from skill #13's cache, or a multi-option ladder.

## Decision tree

```
Is the creator's content focused on a single use-case?
  │
  ├─ Yes  → Does a bundle exist that fits this use-case?
  │           │
  │           ├─ Yes  → Pitch the bundle (better fit + better creator latitude)
  │           └─ No   → Pitch the most-aligned single SKU
  │
  └─ No (creator covers multiple aligned use-cases)
            → Pitch a "multi-option ladder" — give them choice
```

## When to pitch a single SKU

- Creator's content is laser-focused on one topic
- Brand has one obvious SKU match
- Creator is nano + the brand has limited bandwidth
- Single SKU is a hero product that anchors the brand identity

Example: a creator who exclusively makes pour-over coffee content → pitch the River Stone Pour-Over single SKU.

## When to pitch a bundle

- Brand has a bundle from skill #13's cache that fits the creator's use-case (e.g., "Complete Coffee Brewing Set" → pour-over content creator)
- Creator's content shows they curate setups, kits, or routines (not just single items)
- Brand wants to drive higher AOV from the partnership's traffic
- Bundle has stronger positioning copy than the single SKU

Example: a creator who makes "morning routine" videos → pitch "The Slow Morning Bundle" (mug + pour-over + journal + candle).

The bundle pitch has 3 advantages over single-SKU:
1. **Higher conversion**: bundles convert better than single items in influencer campaigns
2. **Better story**: "complete set" is easier to explain than a single SKU
3. **Higher AOV**: each conversion is worth more

## When to pitch a multi-option ladder

When the creator's audience has multiple aligned interests, present 2-3 options and let the creator pick. This works particularly well for:
- Mid-tier creators (they value creative control)
- Macro creators (they need to fit it into existing video format)
- Creators with mixed content themes

Multi-option ladder structure:

> "We have three things we think could work for your audience:
> 1. [Single SKU] — for a quick feature
> 2. [Bundle] — for a 'complete setup' video
> 3. [Different bundle] — for a 'comparison' video
>
> Pick the one that fits how you'd want to feature it (or tell me if you'd rather we discuss a different angle)."

The ladder positions the brand as flexible and partnership-savvy.

## Reading the bundle cache

The skill checks `~/.the-ecommerce-seller/cache/bundles/{slug}.json` (written by skill #13) for bundles. For each bundle:

- `bundle_type_primary`: prefer "complementary" and "starter_kit" bundles for influencer pitches
- `use_case_label`: matches the creator's content themes
- `is_active`: only active bundles get pitched
- `recommended_tier`: bundle's price for influencer-pitch context

The skill checks the bundle's `is_starter_kit: true` flag — starter kit bundles are often the best influencer pitch because:
- They demonstrate the brand's full range
- They're priced at acquisition tier (creator audiences are first-time buyers)
- They have first-time-customer framing already baked in

## Bundle pitch outreach language

When pitching a bundle, the outreach changes:

```
[Instead of: "We'd love to send you our River Stone Pour-Over"]
[Pitch a bundle: "We'd love to send you our Complete Coffee Brewing Set — pour-over, filters, and carafe — because it's how we'd actually want a friend to start with our brand"]
```

The bundle framing is stronger because:
- It signals brand curation
- It gives the creator more material for content (3 items vs. 1)
- It lets the creator choose which to feature

## Multi-option ladder outreach language

```
[At the offer section]

"We have three options we think could fit your content:

1. River Stone Pour-Over (single piece, $48 retail) — fits a quick post or Reel
2. The Slow Morning Bundle (pour-over + filters + carafe, $78 retail) — fits a 'morning setup' video
3. The Brewing Starter Kit (pour-over + filters + beans, $60 retail at starter pricing) — fits a 'just getting into pour-over' angle

Which feels right for the kind of content you'd want to make? Or if a different angle entirely makes more sense, I'm all ears."
```

The ladder is friendly and gives creative control without overwhelming.

## When to avoid bundles

Don't pitch a bundle when:
- The bundle's price exceeds the creator's typical product-feature range (a $200 bundle to a nano content creator who features $20 items)
- The bundle includes a product the creator has explicitly disliked
- The bundle's positioning conflicts with the creator's voice (e.g., a "luxury indulgence" bundle to a creator known for affordable hacks)
- The creator has already featured a competing product/bundle recently

The skill checks the creator's recent content for these signals.

## Pitch ladder for new SKUs

For a new product launch, the skill recommends:
- Nano + micro creators get the new SKU as a focused pitch
- Mid-tier+ creators get the new SKU as one option in a multi-option ladder (less risk; creator can choose)
- Don't pitch the new SKU as part of a bundle for the first 30 days — let the new SKU have its own moment

## Cost considerations

Bundles cost the brand more per gift (more product) but typically deliver higher ROI:

| Pitch type | Brand cost per shipment | Expected creator action |
|---|---|---|
| Single SKU gifted | 1× product cost | 1 post (if any) |
| Bundle gifted | 2-4× product cost | 1-2 posts + better content quality |
| Bundle paid (hybrid) | 2-4× product + cash | 2-3 contractually-guaranteed posts |

The skill computes the cost exposure per pitch + outputs in the .docx so the buyer sees the math.

## Buyer can override

The buyer can explicitly tell the skill what to pitch:
- "Pitch the River Stone Pour-Over to this creator" → skill follows even if a bundle would be a better fit
- "Pitch the Slow Morning Bundle" → skill follows
- "Show me both options" → skill builds a multi-option ladder

When the buyer specifies, the skill respects but optionally flags a better-fit alternative in the audit:

> "Buyer requested River Stone Pour-Over for @[handle]. Skill notes: 'The Slow Morning Bundle' would also fit (creator's content includes 'morning routine' themes) — consider as alternative."
