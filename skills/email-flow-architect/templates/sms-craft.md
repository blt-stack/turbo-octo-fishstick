# SMS Craft — 160-Char Limits, TCPA, Opt-in, Link Handling

SMS is the highest-conversion automated channel for DTC e-commerce but the strictest from a compliance perspective. Done wrong, the buyer's SMS program gets shut down by their provider or sued under TCPA. Done right, SMS drives 5-20% of program revenue at a fraction of email's send cost.

This file covers the conventions every SMS in every flow follows.

---

## Hard character limits

| Limit | Description |
|---|---|
| 160 characters | Standard single-segment SMS. Stays as one message, doesn't fragment. |
| 70 characters | When using emoji or non-Latin characters (which switch encoding to UCS-2) |
| 1,600 characters | Hard cap before SMS becomes MMS (more expensive, different deliverability) |

The skill defaults to **140-160 characters** to leave room for link expansion (Klaviyo shortens links to ~22-25 chars but the buyer's preview shows the longer version).

---

## TCPA compliance (US regulation)

TCPA (Telephone Consumer Protection Act) governs SMS marketing in the US. Violations carry $500-1,500 per text penalties — a single non-compliant blast can cost six figures.

### Required elements

Every marketing SMS must:

1. **Be sent only to opted-in numbers.** Implicit consent (email subscriber → SMS sub) is NOT enough. The customer must have explicitly opted into SMS, typically via:
   - A checkbox on a signup form ("Send me SMS updates too")
   - A keyword-to-shortcode opt-in (text JOIN to 12345)
   - A double opt-in confirmation reply
2. **Include opt-out instructions in every message** — typically "Reply STOP to opt out"
3. **Identify the sender** — the brand name should appear in the message (usually at the start)
4. **Respect quiet hours** — no marketing SMS before 8am or after 9pm in the recipient's time zone
5. **Honor opt-outs immediately** — if a customer replies STOP, the platform (Klaviyo, etc.) auto-handles this; but custom workflows need to respect it

### What this looks like in copy

Every SMS the skill writes ends with:
```
Reply STOP to opt out.
```

And starts with the brand identifier:
```
[brand] - [message]
```

Or for shorter brands:
```
Hey [first name], [message from the brand context]
```

### Compliance fail patterns

The skill auto-flags:
- SMS missing "Reply STOP" or equivalent opt-out language
- SMS missing brand identification in the first 30 chars
- SMS with claims that would require additional disclosure (financial, medical, lottery)
- SMS in regulated categories (CBD, alcohol, supplements with health claims) — flagged for review

---

## SMS body patterns

### Greeting

**With first name (when known):**
```
Hey [first name],
```

**Without first name:**
```
[brand] - 
```

Don't combine both ("Hey [first name], [brand] -") — feels stilted.

### Body

Short, declarative sentences. SMS isn't the place for nuance. Examples by flow:

**Welcome SMS:**
```
Hey [first name], your welcome code is WELCOME10 for 10% off. Use it in
the next 7 days: [shortlink]. Reply STOP to opt out.
```
(140 chars)

**Abandoned Cart SMS:**
```
Hey [first name], your cart at [brand] is still here: [shortlink]. We'll
hold it for the next 24 hours. Reply STOP to opt out.
```
(135 chars)

**Post-Purchase shipping SMS:**
```
[brand] - Your order #[number] just shipped. Tracking: [shortlink].
Should arrive [date]. Reply STOP to opt out.
```
(115 chars — short because tracking link will be a real URL the recipient
expands; leaves room)

**Birthday SMS:**
```
Happy birthday, [first name]! Your gift from [brand]: BIRTHDAY15 for 15%
off your order this week. [shortlink] Reply STOP to opt out.
```
(150 chars)

**Back-in-stock SMS:**
```
[Product] is back in stock at [brand]! Grab yours before it sells out:
[shortlink]. Reply STOP to opt out.
```
(110 chars)

### Sign-off

Standard: `Reply STOP to opt out.`

That's it. SMS doesn't sign off with names or formal closings — feels overdone.

---

## Links in SMS

### Use shortened links

Klaviyo auto-shortens links to ~22-25 characters via their `kvy.io` shortener. Most platforms have similar shortening.

The skill writes `[shortlink]` as a placeholder in the brief and the Klaviyo-paste block. Klaviyo substitutes the actual shortened URL when the SMS sends.

### Don't include UTM parameters in the visible link

UTM params make the link 60-80 chars longer if not shortened, eating into the character budget. The buyer's analytics tool (GA4, etc.) should append UTMs at the destination side, not in the SMS link itself.

### One link per SMS, maximum

Multi-link SMS read as spammy and confuse the recipient. Pick the one most important destination.

---

## Personalization in SMS

Same merge tags as email work in SMS:
- `{{ first_name|default:'there' }}` — first name with fallback
- `{{ product_name }}` — for cart / browse / back-in-stock messages
- `{{ event.checkout_url }}` — for cart recovery

The skill always uses the default filter on first_name to avoid awkward "Hey ," renders.

---

## Tone for SMS

SMS feels more personal than email — it lives next to texts from friends. Default tone:

- **Lowercase casual** (NOT all caps, NOT title case): "hey amy, your cart..." reads native; "Hey Amy, Your Cart..." reads marketing
- **Sentence fragments OK**: SMS isn't an essay
- **Emoji, very sparingly**: 1 emoji per SMS at most — and remember emoji switches encoding, halving the character budget
- **First-person feel** when possible: "we'll hold it" / "I noticed you" reads warmer than "the system has reserved"

Adjust per `config.brand_voice`. A formal/premium brand's SMS reads differently from a playful brand's — but ALL SMS should feel more conversational than the brand's email.

---

## Flow-specific SMS conventions

| Flow | SMS character | Default count |
|---|---|---|
| Welcome | Casual + offer | 2 (steps 2, 6) |
| Abandoned Cart | Friendly reminder + offer | 2 (steps 2, 4) |
| Post-Purchase | Shipping update + replenishment nudge | 2 (steps 2, 5) |
| Browse Abandonment | Friendly nudge | 1 (step 2) |
| Win-back | Warm + offer | 1 (step 3) |
| Birthday | Warm | 1 (the day-of message) |
| Replenishment | Practical reminder | 1 (step 2) |
| Back-in-stock | Urgent (in a friendly way) | 1 (immediate) |

Each per-flow template specifies the SMS step's exact placement in the sequence.

---

## What to test in SMS

Less to A/B test in SMS than email (the messages are so short there's less room for variation). Recommended:

1. **Send timing** — 8am vs 12pm vs 6pm
2. **Personalization presence** — with first name vs without
3. **Offer mention placement** — early vs later in the message
4. **Opt-out phrasing** — "Reply STOP" vs "Text STOP" (region-dependent)

---

## Common pitfalls

- **No opt-in flow set up** — sending SMS to email-only subscribers is illegal under TCPA
- **Missing "Reply STOP"** — TCPA violation, fines accrue per message
- **Multiple SMS in 24 hours** — high unsubscribe rate, frequent blocking
- **SMS that read like email** — too long, too formal, paragraphs of content
- **Time-zone unaware** — sending at 8pm Pacific = 11pm Eastern. The recipient is asleep, you wake them, they unsubscribe.
- **Same content as the email** — SMS that paraphrases the email it accompanies feels redundant. Different angle, different value.

---

## When to recommend SMS-first vs email-first

Some flows perform better via SMS than email:

| Flow | Channel preference |
|---|---|
| Welcome | Email primary (room for the offer + story); SMS supplementary |
| Abandoned Cart | Tied — SMS reaches the mobile-cart-abandoners email misses |
| Post-Purchase shipping | SMS primary (time-sensitive, mobile-relevant) |
| Browse Abandonment | Email primary (the browse signal is weaker; SMS would feel intrusive) |
| Win-back | Email primary, SMS-only for the lapsed-but-SMS-active segment |
| Birthday | Tied |
| Replenishment | Tied — SMS hits at runout moment |
| Back-in-stock | SMS primary (speed wins; competitors might restock too) |

The skill builds both channels per flow, but per-step prominence varies — the per-flow template captures the right balance.
