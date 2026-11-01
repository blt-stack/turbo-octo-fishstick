# Reply Craft — Universal Structure

Every reply, regardless of tier or platform, follows the same skeleton. Tier + platform + sentiment shape *what fills each part*, but the skeleton holds.

## The 4-part skeleton

1. **Open by name** — "Hi [First name]" — never "Dear Customer."
2. **Reflect the specific thing** — name the issue (recovery), the friction (clarify), or the praise (amplify) back to them in their own words.
3. **Resolve / probe / amplify** — the tier-specific middle.
4. **Close with a real first name.**

## Length targets

| Tier | Word target | Why |
|---|---|---|
| 1-2★ Recovery | 60-140 words | Public proof of brand handling. Long enough to show care, short enough to read as confident. |
| 3★ Clarify | 40-90 words | The probe is short. The customer wants to be heard, not lectured. |
| 4-5★ Amplify | 30-70 words | Restraint reads as confidence. A long amplify reply looks desperate. |

When the platform has a hard character limit (Trustpilot ~5000, Etsy ~500 practical), the limit overrides the word target.

## Tone hierarchy

When multiple inputs conflict, apply this order:

1. **Platform TOS / policy** — never violate (e.g., no discount codes in Amazon replies)
2. **Sentiment override** — abusive/fake/sycophantic override the tier default
3. **Brand voice** — apply config.brand_voice on top of the structural reply
4. **Tier reply pattern** — recovery / clarify / amplify
5. **Issue category specifics** — shipping vs. defect vs. sizing patterns

## Opener variations (don't repeat in a single bulk batch)

In bulk mode, readers compare adjacent replies. Same opener twice in a row reads as form-letter. Vary across:

- "Hi [Name],"
- "[Name] —"
- "Thank you for this, [Name]."
- "Hey [Name],"
- "[Name],"

Pick per-reply randomly within the brand voice's tone register. A formal brand uses "Hi [Name]" and "[Name] —" not "Hey [Name]."

## Closer variations

Same idea — don't repeat across a batch.

- "— [Name], [Role]"
- "— [Name]"
- "Best, [Name]"
- "Cheers, [Name]"
- "Thank you again, [Name]"

Match the brand voice register. A no-fuss workwear brand probably doesn't close with "Cheers."

## Real first names > "the team"

When at all possible, sign with a person's first name (the buyer's, the founder's, or a named CS rep). Reviews + replies are public; future readers are evaluating whether real people work at this brand. "The Customer Service Team" loses every time to "— Jamie."

When the config doesn't yet have signer names, the skill asks during onboarding (one-time). Add to the config under `brand_voice.signer_names: ["Jamie", "Alex"]`.

## Voice calibration to brand archetype

Adjust opener warmth, sentence length, and word choices to match `config.brand_voice.archetype`:

- **Craft / Maker archetype** — sentences a little longer, more sensory language ("how it feels," "the weight," "the finish")
- **Performance / Athlete archetype** — sentences clipped, action verbs, no fluff
- **Wellness / Care archetype** — soft openers, gentle pacing, plenty of "I"
- **Minimalist / Modern archetype** — short, declarative, dry
- **Playful / Indie archetype** — informal openers, occasional dash of humor (only on amplify tier — never on recovery)

## When to use "I" vs. "we"

- **Recovery tier**: lean toward "I" — personal accountability ("I'm so sorry," "I just sent you an email"). Stronger than "we."
- **Clarify tier**: mix — "Thank you for the feedback. We're curious about ..."
- **Amplify tier**: "we" works fine — the brand stands together in gratitude.

The exception: when the founder is signing on a recovery reply, **always "I."** Founder signing as "we" defeats the point of founder signing.

## Per-character cost considerations

On Trustpilot and Amazon, replies are indexed by search engines. Every reply is permanent. This means:

- No throwaway language ("just wanted to say...")
- No filler intros ("Thank you for taking the time to write this review")
- No hedge phrases ("Hopefully," "Perhaps," "It may be that")

Every sentence earns its place.

## Reading the reply aloud

The skill's last check before output: read each reply aloud in your head. If a sentence trips, rewrite it. If the apology sounds performative, rewrite it. If the amplification sounds gushy, rewrite it.

Public replies that read awkwardly stay awkward forever. Private replies you can re-send. Public replies you can't take back.

## Worked examples

### Recovery example (Judge.me, 1★, shipping)

Original review:
> "Ordered 3 weeks ago. Still not here. No updates from anyone. Useless."

Drafted reply (78 words):
> Hi Marcus,
>
> Three weeks with no update is on us, and I'm sorry. I just pulled your order — it's been sitting at the carrier hub since the 12th, which isn't acceptable.
>
> I refunded your order in full this morning, and I'm sending a replacement out today via expedited. No need to do anything on your end.
>
> I just emailed the details. Thank you for the honest review — it pushed us to fix something we'd missed.
>
> — Jamie

### Clarify example (Google, 3★, expectation mismatch)

Original review:
> "Good quality but the color looked totally different in the photos. Wish I'd known."

Drafted reply (52 words):
> Hi Priya,
>
> Thank you for this — color accuracy is something we're actively working on. Was it the warmth, the saturation, or just a general "lighter / darker than expected"? That detail helps us improve the photos.
>
> Happy to swap for a different color if you'd like — just email us.
>
> — Alex

### Amplify example (Loox, 5★, craft brand)

Original review:
> "I've had a lot of mugs in my life. This one feels like it was made by a person. The weight, the way the handle sits. Beautiful."

Drafted reply (38 words):
> Hi Sam,
>
> "Made by a person" — that's the highest compliment we could ask for. Pieces like this one were thrown by Maya in our Brooklyn studio.
>
> Thank you for choosing the long road.
>
> — Jamie
