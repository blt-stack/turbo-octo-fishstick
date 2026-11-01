# Positioning Copy — Names + 3 Variants per Bundle

For each bundle, the skill generates: 2 name styles + 3 copy variants. The buyer picks per bundle.

## Name styles

### Descriptive
States what the bundle is. Functional. Easy to understand. SEO-friendly.

Examples:
- "Complete Coffee Brewing Set"
- "Morning Skincare Routine"
- "Home Bar Essentials"
- "Three-Piece Sneaker Bundle"

When to use: data-driven shoppers, search-driven traffic, comparison shoppers.

### Evocative
Captures the feeling/identity of the bundle. Brand-voice expressive. Memorable.

Examples:
- "The Slow Morning Bundle"
- "Wake Up Glowing"
- "The After-Hours Set"
- "Saturday's Best"

When to use: discovery-driven shoppers, social media traffic, brand-loyal customers.

The skill outputs both styles. Buyer picks per bundle; many brands use descriptive names for SEO/PDP and evocative names for landing pages + social.

## The 3 copy variants

For each bundle, the skill generates 3 positioning copy variants. Each targets a different shopper psychology.

### Variant A: Benefit-led
Leads with the savings or convenience.

Template:
```
[Bundle name]

Save $X when you buy [SKUs] together.

[1-2 sentences on what the bundle does practically]

[Call-to-action]
```

Example:
```
Complete Coffee Brewing Set

Save $14 when you buy the pour-over, filters, and carafe together.

Three pieces that work together to make a proper pour-over morning. Skip the guesswork on what goes with what.

Add the bundle.
```

When to use: cart-page bundles, retargeting ads, paid-traffic landing pages.

### Variant B: Story-led
Leads with the brand's narrative or the customer's experience.

Template:
```
[Bundle name]

[1-2 sentences on the experience / ritual the bundle enables]

[Why the brand built it this way]

[Soft call-to-action]
```

Example:
```
The Slow Morning Bundle

The way we drink coffee at home: slow, deliberate, one cup at a time.

We picked these three pieces because they work together — the pour-over has the spout balance for clean pours, the carafe matches the volume, and the filters are the only kind we'd use ourselves.

Try the ritual.
```

When to use: brand landing pages, organic social, email nurture content, story-driven brands.

### Variant C: Social-proof-led
Leads with customer testimony or aggregate validation.

Template:
```
[Bundle name]

"[Pulled testimonial quote]" — [Reviewer name], verified buyer

[The pieces customers reach for together — now in one click]

[Call-to-action]
```

Example:
```
The Slow Morning Bundle

"This pour-over makes my whole morning feel different. I never thought a coffee setup could matter this much." — Sam K., verified buyer

The three pieces our customers reach for most often, together at a lower price.

See the bundle.
```

When to use: when testimonial cache (from skill #10) has a strong relevant quote; converts well on cold traffic.

## Pulling testimonials from cache

The skill reads `~/.the-ecommerce-seller/cache/testimonials/{product-identifier}.json` (written by skill #10) for each SKU in the bundle:

1. For each SKU, load testimonials
2. Filter to quotes tagged `use_cases: ["landing_page_testimonial"]`
3. Sort by `quote_score` descending
4. Pick the highest-scoring quote whose attribution + content fits the bundle's positioning

If no testimonial exists for any SKU in the bundle, the Variant C falls back to brand-voice (without a quote):

```
The Slow Morning Bundle

The pieces our customers reach for together — now at one price.

[Continue with brand-voice positioning]
```

## Length targets

Bundle copy fits PDP-level use:

| Component | Length |
|---|---|
| Name | 2-6 words |
| Tagline / first sentence | 8-18 words |
| Body | 40-100 words |
| CTA | 2-5 words |

The skill outputs all components separately so the buyer can assemble into PDP, ad, email, or landing-page templates.

## Brand voice integration

Each copy variant respects `config.brand_voice.archetype`:

- **Craft / Maker archetype**: emphasize curation, sensory details, hands-on language ("we made," "thrown by," "tested by hand")
- **Performance / Athlete archetype**: emphasize outcomes, action verbs, clip-and-direct sentences
- **Wellness / Care archetype**: emphasize ritual, slowness, intentionality
- **Minimalist / Modern archetype**: leaner sentences, declarative, less hedging
- **Playful / Indie archetype**: looser tone, light humor (only on Variant B), brand personality

## Avoid in all variants

- "Limited time only" (for permanent bundles)
- "Hurry while supplies last" (manufactured urgency)
- ALL CAPS
- Multiple exclamation marks
- Discount codes in the body copy (mention savings amount or %, not a code)
- "Customers love this" without attribution (Variant C should have a real testimonial)
- Generic "perfect for" phrasing
- Phrases that obviously feel like a marketing template ("Look no further than...")

## Bundle copy for Shopify PDP

The skill outputs a PDP-ready block:

```
[Bundle name]
[Tagline — 1 sentence]

[Body — 60-100 words from chosen variant]

What's included:
- [SKU 1 + qty]
- [SKU 2 + qty]
- [SKU 3 + qty]

Individual price: $X
Bundle price: $Y
You save: $Z

[CTA]
```

The buyer pastes into Shopify product description editor. Skill #1 (Product Description Writer) can also pick this up from the bundle cache and apply brand voice + platform-specific formatting if the buyer wants more polish.

## Bundle copy for landing pages

The skill outputs a longer-form block (300-500 words) suitable for a dedicated bundle landing page. Skill #3 (Landing Page Copywriter) can read from the bundle cache and generate the full landing page architecture.

## Bundle copy for ads

The skill outputs short-form variants (3-7 words for headlines, 20-40 words for primary text):

```
HEADLINES (3 variants for Meta ads):
- "Three pieces. One ritual."
- "Save $14 on the brewing set."
- "What our customers buy together."

PRIMARY TEXT (3 variants, ~25 words each):
- "The pour-over, filters, and carafe — now in one bundle. Save $14 vs. buying separately."
- "We picked these three pieces because they work together. Make the perfect cup."
- "[Customer quote about the experience]. Try the bundle."

CALL-TO-ACTION (3 options):
- "Shop the Bundle"
- "See What's Included"
- "Make the Morning"
```

Skill #5 (Ad Creative Generator) reads from the bundle cache and incorporates these into platform-specific ad concepts.

## Output structure in .docx

For each bundle, the .docx outputs:

```
══════════════════════════════════════════════════
POSITIONING COPY
══════════════════════════════════════════════════
Names:
  Descriptive: [name]
  Evocative:   [name]

Variant A — Benefit-led (recommended for: cart/retargeting)
[copy block]

Variant B — Story-led (recommended for: brand pages/social)
[copy block]

Variant C — Social-proof-led (recommended for: cold traffic)
[copy block + testimonial reference]

Short-form for ads:
[headlines + primary text + CTA options]
```

The buyer picks the variant per surface. The cache stores all variants so downstream skills can pull what's right for their context.
