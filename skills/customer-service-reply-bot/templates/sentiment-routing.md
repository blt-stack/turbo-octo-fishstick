# Sentiment Routing

Detect ticket sentiment, then route to the appropriate tone. The underlying business action doesn't change based on sentiment — owed refunds stay owed, defects stay defects — but how the reply reads should match the customer's emotional state.

## Why sentiment matters

A defect-ticket from an angry customer needs a different reply than the same defect-ticket from a calm customer. Same fix, different framing. Mismatched tone (rebutting an angry customer with a chipper "we'd be happy to help!") makes them angrier; over-apologizing to a calm customer ("WE ARE SO SORRY THIS HAPPENED") feels like the brand is overreacting.

The skill matches reply tone to ticket sentiment.

## Three sentiment tiers

### Tier 1: Angry / frustrated

**Signals:**
- ALL CAPS words (especially "URGENT," "NOW," "THIS IS RIDICULOUS")
- Multiple exclamation marks (!!!, ?!?!)
- Expletives (even mild — "ridiculous," "absurd," "BS")
- Threats (refund/chargeback/legal action/public complaint)
- Time-pressure language ("immediately," "ASAP," "I want this resolved today")
- Specific grievances stated multiple times in one message
- Reference to multiple prior contacts that didn't resolve
- Sentiment words: "disappointed," "frustrated," "angry," "unacceptable," "appalled"
- Customer's first message in the thread is already escalated (not de-escalating from earlier polite contact)

**Default tone adjustments:**
- Open with apology (warranted or not — at least acknowledging their frustration)
- Take ownership clearly, even if the brand is only partially at fault
- Skip warm openers ("Hope you're doing well") — feels tone-deaf
- Take fast, definitive action (don't ask for permission — fix it)
- Offer the resolution PLUS a bit extra (credit, discount) to acknowledge the frustration
- Sign with the founder name or a senior person — depersonalizes the conflict to a corporate "team" is worse
- Keep the reply tight — angry customers don't want to read long-winded explanations

**Example tone shift:**

Angry ticket:
> "I have been waiting 14 DAYS for my order. This is COMPLETELY UNACCEPTABLE. I want a refund NOW and I'm telling everyone I know NEVER to buy from you again."

Reply (angry-tier tone):
```
Hi Sarah,

You're right — 14 days is unacceptable, and I'm sorry it's gone this long.

I'm processing your full refund today; it'll be back on your card within
2 business days. I'm also escalating with our shipping partner so this
doesn't happen to anyone else.

I owe you better than this. If there's anything else, just reply — it
comes straight to me.

— Sarah Chen, Founder, {{brand_name}}
```

(Acknowledges the time, takes ownership, action without asking permission, founder sign-off, no warm padding.)

### Tier 2: Neutral / matter-of-fact

**Signals:**
- Professional tone
- Clear, calm description of the issue
- No exclamation marks (or just one casual one)
- Standard greetings/sign-offs ("Hi," "Thanks," "Best")
- No emotional language
- Asks for the resolution without pressure
- Often: "I noticed..." or "Just wanted to let you know..." opener

**Default tone adjustments:**
- Match their calm energy
- Don't over-apologize (sounds weirdly intense relative to their tone)
- Acknowledge briefly + move to the resolution
- Standard sign-off (don't force founder name unless the ticket warrants escalation)
- Standard length (80-180 words)

**Example tone shift:**

Neutral ticket:
> "Hi! Just letting you know my order arrived today but the dripper has a small crack on the base. Was wondering if I could get a replacement. Thanks!"

Reply (neutral-tier tone):
```
Hi Mark,

Sorry about that — I'll get a replacement out today via priority. Should
arrive by [date]. You don't need to send the cracked one back; please just
dispose of it.

Thanks for letting us know.

— Sarah, {{brand_name}}
```

(Standard warmth, calibrated action, brief sign-off, no over-apology.)

### Tier 3: Friendly / patient

**Signals:**
- "Hope you're well" / "How are you" openers
- Thanks the brand in advance
- "No rush" / "whenever you have a chance"
- Soft phrasing on the complaint ("I think there might be an issue with...")
- "Just wondering if..." rather than demands
- Sometimes apologizes themselves ("Sorry to bother you")
- Sentiment words: positive ("love the brand," "huge fan," "really impressed")

**Default tone adjustments:**
- Match their warmth — the customer is being lovely, lean in
- Brief acknowledgment of their patience/warmth
- Standard resolution with maybe a small extra (the customer who's nice often gets a small thank-you, e.g., free shipping next order)
- Friendly sign-off
- Optional: a small "this isn't typical — sorry it happened to a nice one" line

**Example tone shift:**

Friendly ticket:
> "Hi! Huge fan of the brand and I really love my pour-over. Sorry to bother you — I think there might be a small issue with the filter that came with it (one of the screen panels is bent). No rush at all, but if you can swap it out whenever, that would be amazing. Thanks so much!"

Reply (friendly-tier tone):
```
Hi Jess,

Thanks for the kind words — and zero bother, this is exactly what we want
to hear about so we can fix it.

I'm sending a new filter out today (along with a small extra you'll see when
it arrives). Should land in [X] business days.

Enjoy the next cup.

— Sarah, {{brand_name}}
```

(Matches warmth, small thank-you implied via "small extra," ends warmly.)

---

## Detecting sentiment programmatically

The skill uses LLM judgment for sentiment detection — no rigid keyword matching. The signals above are guides, not rules. Skill considers:

- The overall tone of the message (not isolated words)
- The number and intensity of negative signals
- Whether the customer is a repeat-issue customer (their normal tone matters; for some customers "this is annoying" is mild, for others it's an outlier)
- The context (a defect on a $300 order warrants more emotional weight than the same defect on a $20 order)

## Edge cases

### Mixed-signal tickets

Some tickets have both angry and friendly elements:

> "Look, I love your brand and I've ordered a ton, but this is the SECOND time my package has been late and I'm getting really frustrated."

Treat as the higher-intensity tier. Don't average — better to over-respond to potential anger than to under-respond.

### Sarcastic friendly

Some tickets are passive-aggressively "polite":

> "I would just LOVE to get my order someday, that would be great, thanks!!!"

Treat as Tier 1 (angry). Sarcasm signals real frustration.

### Foreign-language nuance

For non-English tickets, sentiment detection depends on cultural norms. Some cultures express dissatisfaction more reservedly than others; some more directly. The skill flags non-English tickets for the buyer to verify sentiment.

### Calm-but-resigned customers

The "I've been a customer for years, and this is the third issue this year, I think we're done" message is hard. It reads neutral but signals churn. Treat as escalation-worthy — these are LTV-loss tickets, not just complaint tickets.

---

## How sentiment shows up in the brief

In single mode, the .docx brief includes:

```
Sentiment: angry
Reasoning: ALL CAPS in subject, three exclamation marks, threat to leave a
review, second contact about this issue.
Reply tone adjusted: more apologetic, founder-name sign-off, faster action.
```

In batch mode, Sheet 2 (Category Breakdown) shows the sentiment distribution across the batch. A healthy CS operation should see roughly:

- 60-70% neutral
- 15-25% friendly
- 10-20% angry

A spike in angry tickets (>30% on a given day or week) usually correlates to a systemic issue worth investigating — a recent product release, a shipping partner change, etc. The .xlsx Sheet 3 flags this when detected.

---

## What sentiment does NOT change

- **The factual content of the reply** — same products, same dates, same actions
- **The recommended business action** — refunds owed stay owed regardless of tone
- **Compliance / policy** — angry customers don't override return-window rules; the tone changes but the policy doesn't

Sentiment is about HOW the message reads, not WHAT it says.
