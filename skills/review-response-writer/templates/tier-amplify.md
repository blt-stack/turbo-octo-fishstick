# Tier: Amplify (4★, 5★)

4-5★ replies feel small — but they're the most-read replies on the product page. New shoppers spend 60% of their review-page time on 5★ reviews. The brand's reply under those reviews is the closest thing to a free conversion-rate-optimization tool.

## Reply mode

1. **Specific thanks** — name what they praised, not a generic "thanks!"
2. **Reinforce a brand value** — connect their experience to what you stand for in one line.
3. **Seed something forward** — a referral cue, a related product mention, a "thanks for being part of this" — but never pushy, never an upsell.
4. **Sign with a real first name.**

## The 4-part amplify skeleton

```
Hi [First name],

[Specific thanks: "Hearing that [the specific thing they praised] is exactly what we hoped for" or "[Quote one phrase from their review back to them]."]

[Brand value reinforcement: "[product] was built to [the value]" or "We made [product] for moments like this."]

[Light seed: "If you ever want to try [adjacent product], we'd love your honest take" / "Tell a friend who might love this" / "We can't wait to see what you make."]

— [First name]
```

## Specific thanks — examples that work vs. don't

| Generic (avoid) | Specific (use) |
|---|---|
| "Thanks for the kind words!" | "Hearing that the grip 'feels balanced from the first pour' is exactly what we hoped for." |
| "Glad you love it!" | "I love that you used it on a road trip — it was built for that." |
| "We appreciate the review!" | "Knowing the spoon felt 'just right' for your morning routine made my day." |
| "Awesome to hear!" | "The bit about your kid stealing it for breakfast — that's the kind of review we frame." |

## Brand value reinforcement

A single line that ties the customer's experience back to *why the brand exists*. Read `config.brand_voice.archetype` and `config.audience.aspirations` for source material.

Examples (the value will vary by brand; these are illustrative):

- For a craft / quality archetype: "We make these one at a time so they earn the kind of detail you noticed."
- For a sustainability archetype: "Pieces that last decades is the whole point — thank you for choosing the long path."
- For a community archetype: "You're part of why this brand exists — and reviews like this make a real difference for someone deciding right now."
- For a results / performance archetype: "Your [outcome] is the reason we test [feature] the way we do."

## Seed types (low-pressure forward motion)

Pick **one** seed per reply. Don't stack.

### Referral seed
> "If you know someone who'd love this, sharing means the world to us."

### Adjacent product seed (only if the original review mentioned a use case the adjacent product complements)
> "If you ever try [adjacent product], I'd love your honest take — your reviews are gold."

### Repeat-purchase seed (replenishables)
> "When it's time to restock, we'd be honored to be your go-to."

### Community seed
> "Tag us @[handle] if you ever want to share how you're using it — we read everything."

### No-seed (sometimes the right call)
For a glowing 5★ from a long-time customer, just thank them and stop. Not every reply needs a forward-motion line. Restraint reads as confidence.

## Length is the differentiator

Amplify replies should be **30-70 words**. A 200-word amplification reply reads as desperate. A 4-line, specific, warm reply reads as a brand that gets it.

## Sycophantic / paid-looking reviews

When the review reads as generic ("Best product ever! Love this brand!" with nothing specific), apply a low-key thank-you that doesn't engage with the suspect content. Don't amplify in the testimonial cache (the `testimonial_cache.py` script auto-skips these via the sycophancy filter — but flag the buyer in the report).

```
Hi [Name],

Thank you so much for the kind review — really appreciate the support.

— [Name]
```

Short, warm, unprovokable. Move on.

## What NEVER goes in an amplify reply

- A discount code ("Use REPEAT15 next time" — looks like incentivizing the review on most platforms; explicitly violates Amazon TOS)
- "We'd love it if you'd share this review!" (asking for amplification after the fact is awkward and TOS-risky)
- "Please leave us a review on [other platform]" (asking for off-platform action is TOS-risky on Amazon and tacky elsewhere)
- A long autobiographical brand story (save it for the About page)
- An apology for anything (this is a 4-5★ — there's nothing to apologize for)
- A request to update the rating (only relevant on Amazon, where it's TOS-prohibited anyway)
- Replying with an upsell that wasn't in their review's use case ("Have you tried our $200 add-on?")

## Saving the gold for downstream skills

The best 5★ reviews become testimonials in the Landing Page Copywriter, social proof modules in the A+ Content Creator, and testimonial-format ads in the Ad Creative Generator. The testimonial cache writer (`scripts/testimonial_cache.py`) auto-extracts pull-quotes that meet the testimonial criteria.

When you draft the amplify reply, you're doing two jobs: (1) responding to this reviewer, (2) marking the review for the downstream caches. The reply itself doesn't change based on (2) — but the cache write is happening in parallel.
