# Voice Analysis Prompt

Use this when the buyer has existing listings (3 or more) you can pull from Shopify or another connector. The goal is to extract a usable voice profile in one pass, then verify it with the buyer.

---

## Inputs

You need 3-5 existing product descriptions, ideally:
- Across at least two product categories (so you can separate product-specific language from voice)
- Including at least one description the buyer wrote themselves (vs. ones a previous freelancer or agency wrote)

If you only have access to 1-2, run the analysis but tell the buyer the profile may be thin and offer to supplement with the questionnaire.

---

## What to extract

For each listing, identify:

1. **Sentence rhythm** — short and punchy? Long and flowing? Mixed?
2. **Voice register** — formal, conversational, casual, technical, lyrical?
3. **Recurring words and phrases** that aren't product-specific
4. **Words conspicuously absent** — what would a generic AI write that this brand doesn't?
5. **Structural patterns** — do they open with a question? A story? A spec? Do they always end with a call to action, or never?
6. **Audience signals** — who do these listings assume is reading?

Then synthesize across all listings to produce a unified voice profile.

---

## Output template

Fill this in based on the analysis:

```yaml
archetype: [pick one: rebel, sage, lover, jester, caregiver, ruler, creator, innocent, magician, hero, everyman, explorer]
tone: [3-5 adjectives, comma-separated]
vocabulary_use:
  - [word or phrase 1]
  - [word or phrase 2]
  - [...]
vocabulary_avoid:
  - [word the brand clearly avoids]
  - [...]
voice_examples:
  - "[one short paragraph that's representative]"
  - "[a second representative paragraph]"
structural_patterns:
  - [e.g., "Always opens with a sensory detail"]
  - [e.g., "Bullets are full sentences, never fragments"]
```

---

## Confirm with the buyer

Never save the profile silently. Present it back:

> "Here's what I'm reading from your listings:
> - Archetype: [X]
> - Tone: [Y]
> - You lean into: [words]
> - You seem to avoid: [words]
>
> Two example passages I think capture it:
> > [example 1]
> > [example 2]
>
> Does this sound like your brand? Edit anything before I save it."

Then save the final, edited version. Buyers often catch things in the readback that they wouldn't have surfaced otherwise.

---

## Pitfalls to avoid

- **Don't confuse the freelancer's voice with the buyer's voice.** If the listings were ghostwritten, the buyer may not even agree with them. Ask: "Did you write these yourself, or did someone else?"
- **Don't over-index on one outlier listing.** If 4 listings sound one way and 1 sounds different, ignore the outlier or ask why it's different.
- **Don't infer values from absence.** If the listings never mention sustainability, don't conclude the brand doesn't care about it. They may just not have written about it yet.
