# Outreach Craft — Universal Structure

The 6-part skeleton applies regardless of platform or tier. Platform shapes length + register; tier shapes voice; the structure holds.

## The 6-part skeleton

1. **Personalized opener** — specific recent-post reference
2. **Brand intro** — 1-2 sentences on who the brand is + why this creator would care
3. **Product or bundle fit** — why this specific thing fits THEIR content
4. **The offer** — what's being offered (framework + value)
5. **The ask** — what the brand wants (deliverables + timeline + scope)
6. **Soft CTA + sign-off** — easy yes/no path + name

## Per-section guidance

### 1. Personalized opener (1-2 sentences)

The most important sentence in the outreach. Determines whether the rest gets read.

Requirements:
- Must contain at least 1 specific reference from the creator's recent content
- Must not contain generic praise ("love your content," "such a fan")
- Must sound like a real person noticing the creator's actual work
- Must match the creator's voice register

Good examples:
> "Hi Maya — your post about brewing pour-over on the camping trip last week made me actually try it myself this weekend. The way you explained the bloom step finally clicked for me."

> "Hey Marcus — your video this week about the espresso-vs-pour-over taste test cracked me up (the chocolate-milk reference KILLED)."

> "Hi Sarah, your post on minimal kitchen setups — specifically the one where you tested the 5-piece challenge — made me rethink the way I think about our own packaging design."

Bad examples (avoid):
- "Hi @creator! I love your content!"
- "Your content speaks to my soul"
- "I've been following you for years"
- "We love your aesthetic"

### 2. Brand intro (1-2 sentences)

Compressed. Who the brand is + why this creator would care.

Good:
> "I run Stone & Glass, a small ceramics brand in Brooklyn. We make pour-over devices and mugs for the way you describe your morning ritual."

Compresses: brand name, location, category, audience-relevance hook (linking to the creator's content from sentence 1).

Bad:
> "Stone & Glass is a multifaceted artisanal ceramics company founded in 2019 with a mission to bring craft pottery back into everyday life..."

(Too long, too marketing, doesn't connect to the creator.)

### 3. Product or bundle fit (1-2 sentences)

Specific to THIS creator's content + the product/bundle:

Good:
> "We just launched a complete brewing set — pour-over, filters, and carafe — that I think would fit the 'morning ritual' angle you posted about last week. The kit's been a sleeper hit and I'd love your honest take on it."

Specific to the creator + specific to the product + signals the brand wants real feedback.

Bad:
> "Our products are perfect for content creators like you!"

(Generic; says nothing.)

### 4. The offer (1-3 sentences)

What's being offered. Be specific about the framework + value.

Good (gifted nano):
> "I'd love to send the brewing set your way — no expectations on posting, just want you to have it and try it. If you end up loving it, no pressure either way."

Good (hybrid micro):
> "I'd send the kit + $200 for one Reel (with creative latitude on your end) + 2 Stories. I can share more details on what we usually see work well, but the angle is yours."

Good (paid mid-tier):
> "We can budget $1,800 + product for a dedicated post + 3 Stories + 30-day usage rights, with first-week posting and a 14-day exclusivity window in the pour-over category."

The offer must be specific. Vague offers ("we'd love to discuss a partnership") get ignored.

### 5. The ask (1-2 sentences)

What the brand wants from the creator. The skill makes this clear and modest:

Good:
> "If you're open, I'd love to send the kit your way next week — would just need your shipping address."

Good (for mid-tier+):
> "Could we get on a quick call next week to discuss the angle and timing? I'm flexible on schedule."

Don't ask for too much upfront. The ask is for the next-step conversation, not the contract.

### 6. Soft CTA + sign-off (1-2 sentences)

Easy yes/no path:

Good:
> "Either way, no worries — just wanted to reach out personally. Best, Jamie"

Good:
> "If it's not a fit timing-wise or otherwise, totally understand. Best, Jamie"

The skill always offers an easy out. Pushy CTAs reduce response rate.

## Sign-off conventions

- **Nano**: "— Jamie" or "Best, Jamie"
- **Micro**: "Best, Jamie" or "Cheers, Jamie"
- **Mid-tier**: "Best regards, Jamie" or "Best, Jamie / [brand]"
- **Macro / email**: "Best regards, Jamie Carter / Founder, Stone & Glass"

## Length total by platform + tier

Sum the section lengths to hit platform + tier targets:

```
Nano Instagram DM target: 80-120 words total
  Personalized opener: 20-30 words
  Brand intro: 15-20 words
  Product fit: 15-25 words
  Offer: 20-30 words
  Ask: 5-15 words
  Sign-off: 5-10 words

Mid-tier YouTube email target: 280-400 words total
  Personalized opener: 30-50 words
  Brand intro: 40-60 words
  Product fit: 40-60 words
  Offer: 60-100 words (more detail at this tier)
  Ask: 30-50 words
  Sign-off: 10-20 words
```

## Voice calibration to brand archetype

The outreach voice inherits from `config.brand_voice.archetype` but stays creator-platform-appropriate:

- **Craft / Maker brand archetype**: outreach mentions craft, attention to detail
- **Performance brand**: outreach is direct, results-oriented
- **Wellness / Care brand**: outreach is softer, relational
- **Modern minimal brand**: shorter sentences, less ornamentation
- **Playful / Indie brand**: more personality, lighter touch

The skill applies brand voice to the outreach voice but doesn't override platform/tier conventions (e.g., a playful brand still uses formal email for macro outreach).

## What NEVER goes in cold outreach

- "Dear Influencer" (or any title-only greeting)
- "We've been a huge fan of your content" (when followed by zero specifics)
- "We came across your profile and..." (signals automated scraping)
- "We think your audience would love..." (presumptuous about their audience)
- Excessive flattery ("you're amazing," "you're so talented")
- "Exclusive opportunity" framing (sounds like spam)
- "Limited time" pressure
- Mentions of competitor brands by name
- Demands for "honest review" (legally fraught; reads as inexperienced)
- "Quick favor" framing (reduces perceived value)
- "I know you're busy but..." (don't lead with that frame)

## What ALWAYS goes in cold outreach

- A specific reference to recent creator content
- A specific product or bundle being pitched
- A specific offer + value
- A specific ask + timing
- The brand's actual name in the opener or close
- The sender's actual name (not "team" or "marketing")

## The ear test

Before output, the skill reads the outreach aloud (mentally):
- Does it sound like a real person who watched the creator's content?
- Or does it sound like a template with [VARIABLES] filled in?

If the second, redraft. The most common failure mode is technically-correct outreach that reads as auto-generated.

## Adjustments by relationship stage

The skill checks the influencer memory cache:

- **Stage = new (first contact)**: full 6-part outreach as described
- **Stage = outreached (no_reply)**: use a follow-up template instead
- **Stage = responded (in conversation)**: contextualize within the existing thread
- **Stage = agreed**: skip cold outreach; switch to deliverables tracking
- **Stage = strained**: extra care; relationship-repair before any new ask
- **Stage = blacklisted**: skill refuses to draft (with explanation)
