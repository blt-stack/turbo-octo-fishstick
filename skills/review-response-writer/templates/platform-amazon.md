# Platform: Amazon Seller Reviews

Amazon is the strictest platform. Replies are subject to Amazon's Customer Reviews Guidelines AND seller communication policy. Many things that are normal on Shopify (discount codes, asking for updated ratings, offering off-platform contact) are explicit TOS violations on Amazon.

## Reply visibility

- **Public:** Yes — appears as "Response from [Brand]" under the customer review
- **Indexed:** Yes — Amazon's reviews show in Google search results
- **Edit/delete:** Limited — once posted, replies can be deleted but editing is restricted
- **Reply quota:** Brand-registered sellers can reply once per review

## Hard TOS rules — never violate

| Prohibited | Why |
|---|---|
| Asking the customer to update or change their rating | Explicit TOS violation; "incentivizing review changes" |
| Offering discount codes in the reply | Explicit TOS violation; reads as buying off the review |
| Asking the customer to contact the brand off-Amazon (email, phone, social) | Off-Amazon contact is restricted; Amazon's view is everything goes through Amazon's messaging system |
| Promotional content for other products | Amazon penalizes |
| Referring to the customer by their full name (if they used initials) | Privacy |
| Disputing facts of the customer's experience publicly | Reads as combative; Amazon may pull combative replies |
| Mentioning competitors | TOS-risky |
| "Thanks for the review!" in isolation | Reads as fishing for positive sentiment; Amazon's spam filters may flag |

## Allowed but tricky

- Apologizing for an experience: ✅ allowed
- Offering a replacement: ✅ allowed, **must go through Amazon's Buyer-Seller Messaging system** — don't post the replacement details publicly
- Pointing the customer to Amazon's return process: ✅ allowed
- Pointing to "Buyer-Seller Messaging" by name: ✅ allowed — Amazon prefers this phrasing
- Mentioning product features factually: ✅ allowed
- Correcting factual errors (when done humbly): ✅ allowed, but rarely worth the risk

## Character limit

~3500 characters. Practically: target **80-150 words**. Amazon's reply box rewards concision.

## Tone register

**Professional, neutral, slightly formal.** Amazon's shopper audience expects a polished customer-service voice, not a personality-heavy DTC voice. Match the customer-service-voice of a major brand.

## Reply structure (Amazon-specific)

For 1-2★ recovery on Amazon:

```
Hello [First name or initial they used],

We're sorry [specific issue] — that's not the experience we want for any customer.

Please contact us through Amazon's Buyer-Seller Messaging so we can [process a return / send a replacement / resolve this directly]. We'll take care of it right away.

Thank you for letting us know.

[Brand name] Customer Care
```

Note: Amazon allows signing as "[Brand name] Customer Care" even though other platforms reward signing with a first name. Amazon's convention is brand-team signature.

For 3★ clarify on Amazon:

```
Hello [First name],

Thank you for the honest review — and especially for [specific positive].

We'd love to learn more about [the friction]. If you're able, please send us a quick note through Amazon's Buyer-Seller Messaging — it helps us improve.

[Brand name] Customer Care
```

For 4-5★ amplify on Amazon:

```
Hello [First name],

Thank you for the kind review — hearing that [specific praise] is exactly what we hoped for.

We're grateful you chose [product]. Have a great [day/week].

[Brand name] Customer Care
```

## What "Buyer-Seller Messaging" actually does

When the brand directs the customer to Buyer-Seller Messaging, the actual follow-through happens via Amazon Seller Central:
1. The customer responds to the message they received about their order
2. The brand processes a return / replacement / partial refund through Amazon's order management
3. Amazon handles the financial side; the brand handles fulfillment

The skill's job is to draft the **public reply** that points the customer to Buyer-Seller Messaging. The actual messaging is the buyer's manual work in Seller Central.

## What about asking for an updated review?

**Never explicitly.** Amazon will pull replies that say "Please update your review" or "Would you consider revising your rating."

Implicit pull-throughs that are allowed:
- A great replacement experience may organically lead the customer to update their review themselves
- The brand can never ask for this directly

## Fake / competitor reviews on Amazon

Amazon's Report Abuse function is the only escalation path. See `dispute-drafts.md` for the dispute draft template.

Amazon's review-team response rate has been historically poor on individual disputes (10-30 day SLA, frequent denials). The skill recommends:
- File reports only on clear-cut violations
- Document evidence in the dispute (purchase history mismatch, language overlap with known competitor reviews)
- Don't file >3-5 per month — high-volume filers get reduced priority

## Brand voice override on Amazon

Most brand voice configs need adjustment for Amazon. A playful DTC voice that works on Loox reads as off-brand on Amazon. The skill applies a **+1 formality step** to brand voice when the platform is Amazon, regardless of config setting.

Brand voice configs can include `platform_voice_override.amazon` for buyers who want explicit control. If unset, the skill defaults to "professional, neutral, slightly more formal than the base brand voice."

## Posting workflow

1. Buyer logs into Seller Central → Brand Registry → Customer Reviews
2. Finds the review
3. Pastes the drafted reply
4. Submits (cannot edit after posting — proofread carefully)

Note: Only Brand Registered sellers can reply to reviews on Amazon. If the buyer is not Brand Registered, the skill flags this in the report and notes that the public reply can't be posted — recommend Buyer-Seller Message contact instead.
