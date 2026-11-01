# Single 1★ Recovery — Reference Example

Shows what gets produced when the buyer pastes a single 1★ review and asks for a reply.

**Brand:** {{brand_name}}
**Platform:** Trustpilot (highest stakes — replies indexed by Google, surface in brand search)
**Star rating:** 1★
**Tier:** Recovery
**Sentiment:** Constructive (legitimate, specific complaint)
**Issue category:** Shipping + CS failure
**Output:** Single `.docx`

---

## Input (what the buyer pasted)

```
Platform: Trustpilot
Reviewer: Marcus T.
Rating: 1 star
Title: Worst customer service I've ever experienced
Body: I ordered the River Stone Pour-Over on April 25 and as of today (May 15) it still hasn't arrived. I've emailed customer service three times — once on May 4, once on May 9, and once on May 13 — and have not received a single response. This is the worst customer service I've experienced from any brand I've ordered from, and I'd never order from you again. I'm filing a chargeback with my credit card company today.
Verified purchase: Yes
Date: 2026-05-15
```

---

## Detection

- **Tier:** Recovery (1★)
- **Sentiment:** Constructive (specific, factual complaint — not abusive, not fake)
- **Issue category:** Shipping + CS failure (composite — both 3-week shipping AND 11-day support silence)
- **Sentiment override:** None — this is a real customer with a real complaint
- **Founder escalation:** Recommended (Trustpilot + CS failure + chargeback threat = high-risk)

---

## .docx output structure

```
Reply to: Marcus T.  ·  1★  ·  Trustpilot
Posted 2026-05-15  ·  River Stone Pour-Over  ·  verified purchase
Tier: Recovery (1-2★)
Sentiment: constructive
Issue category: shipping_cs_failure
```

### ORIGINAL REVIEW (for reference)

[Worst customer service I've ever experienced]

[The full review body, formatted in 55% grey]

### DRAFTED PUBLIC REPLY

```
Hi Marcus,

Three emails over eleven days without a response isn't acceptable, and I'm sorry it took a Trustpilot review for us to surface this. I'm Jamie, the founder — I've found your emails in our system and am personally responding now.

Here's what's happening: your order has been sitting at the carrier's regional hub since May 4. I've issued a full refund as of today and am sending a replacement out via expedited shipping, no charge.

I just emailed you directly so we can close this out. You deserved a better experience the first time, and we'll do better.

— Jamie, founder, {{brand_name}}
```

Character count: 624 (limit: 10000)

### DRAFTED PRIVATE FOLLOW-UP

Subject: Personal note from Jamie — refund + replacement for order #1047

Body:
```
Hi Marcus,

Jamie here, founder of {{brand_name}}. I read your Trustpilot review and wanted to write directly.

Here's what we're doing right now:
- Full refund processed today (you'll see it in 3-5 business days)
- Replacement going out via FedEx Overnight at no charge
- Tracking will be sent the moment it ships — today by 5pm ET
- I've also found and read all three of your emails — and have set up a flag so any future emails route directly to me

You shouldn't have had to file a chargeback to get a response, and you shouldn't have to anymore. If you've already filed, no worries — the refund will reconcile.

If you'd be open to a quick 10-minute call this week so I can hear what we missed, I'd value it. No obligation either way.

— Jamie
Founder, {{brand_name}}
jamie@{{brand_name}}.com  /  direct: [number]
```

### CACHE WRITES

- Testimonials extracted: 0 (1★ — not amplifiable)
- Objections extracted: 2
  - "Shipping is unreliable" (category: shipping, frequency_tag: systemic — 5th instance)
  - "CS unreachable when problems happen" (category: customer_service, frequency_tag: emerging — 2nd instance)
- Keyword phrases enriched: 0
- Objection cache: `~/.the-ecommerce-seller/cache/objections/river-stone-pour-over.json`

---

## What the buyer does next

1. **Post the public reply** to Trustpilot
2. **Send the private follow-up email** within the hour (the public reply commits to it — follow-through within 24h is critical)
3. **Process the refund + reship** in the Shopify admin
4. **Address the systemic issue** — the objection cache shows "Shipping is unreliable" is now systemic (5+ instances). This is no longer a copy issue; it's an operations issue. Recommend reviewing the carrier choice or fulfillment partner this week.
5. **Address the emerging CS issue** — 2 CS-unreachable complaints in recent batches suggests support response time is slipping. Worth a process check.

---

## Why this reply works

- **Founder-signed** — Marcus mentioned a chargeback threat. A junior CS rep replying to a chargeback threat undermines the apology. Founder signing signals that the brand is taking this seriously.
- **Specific timeline accountability** — "eleven days" and "three emails" reflect Marcus's exact words back to him. No vague "we're sorry you had an issue."
- **Concrete action upfront** — refund + replacement + tracking. Marcus knows what's happening before he's done reading.
- **Doesn't argue or explain** — the reply doesn't say "our team has been understaffed" or "the carrier has been slow." Future readers don't care; they care that the brand owns it.
- **Private follow-up is the real apology** — the public reply is for future Trustpilot readers; the private email is for Marcus. The private email is longer, warmer, more specific, and offers a call.
- **Downstream cache writes** — the systemic shipping objection now propagates to Ad Creative Generator (proactively address shipping in ads), Landing Page Copywriter (add shipping reassurance to the PDP), and Product Description Writer (set realistic expectations).

---

## Time savings

Manually:
- Read review, gather context, look up emails: ~10 min
- Draft public reply, second-guess it, revise: ~15 min
- Draft private follow-up: ~10 min
- Decide founder vs CS signature: ~5 min (often skipped, often wrong)
- **Total: ~40 min**

With this skill:
- Skill runs: ~30 seconds
- Buyer reviews + edits: ~5 min
- **Total: ~5 min** + the systemic cache writes happen in the background
