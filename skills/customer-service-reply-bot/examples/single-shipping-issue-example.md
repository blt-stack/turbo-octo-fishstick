# Single Shipping Issue — Reference Example

Fictional customer used to show structure. Never reproduce verbatim.

**Scenario:** Customer Sarah emails {{brand_name}} 6 days after her order was due to arrive. UPS tracking shows the package stuck at a facility in Memphis. Brand uses Shopify; order #1024 fetched automatically.

---

## Original ticket (parsed from Gmail or paste)

```
From: Sarah Mitchell <sarah.m@email.com>
Subject: where is my order
Received: 2026-05-22 09:14

Hi - I ordered the River Stone Pour-Over on May 10 and it was supposed
to arrive last week. UPS tracking says it's been sitting in Memphis for
days. Can you let me know what's going on?

Sarah
```

---

## Detected categorization

- **Category:** Shipping issues
- **Sub-type:** Delayed
- **Sentiment:** Neutral (matter-of-fact phrasing, no caps, no exclamation marks, polite sign-off)
- **Order context:** Fetched from Shopify — Order #1024, placed May 10, shipped May 12, currently in_transit, last scanned in Memphis TN

---

## .docx output structure

```
Reply to: Sarah Mitchell
Received 2026-05-22 09:14 · Category: Shipping Issue — Delayed
Sentiment: neutral
Reasoning: Matter-of-fact phrasing, no caps, no exclamation marks. Polite sign-off.

══════════════════════════════════════════════════
ORDER CONTEXT
══════════════════════════════════════════════════
Order: #1024
Placed: 2026-05-10
Shipped: 2026-05-12
Status: in_transit
Tracking: UPS 1Z9999A1B23456789
Last known location: Memphis, TN (scanned 2026-05-18)

Products in order:
  • 1 × River Stone Pour-Over — Cream — $48.00
  • 1 × Reusable Stainless Filter (included) — $0.00

Order total: $52.00 (includes $4 shipping)
Customer LTV: $340.00 across 4 orders

══════════════════════════════════════════════════
DRAFTED REPLY
══════════════════════════════════════════════════
Subject: Re: where is my order

Body:

Hi Sarah,

Sorry your order has been sitting. UPS tracking shows #1024 left our
fulfillment partner on May 12 and has been parked at the Memphis facility
since the 18th. That's frustrating, and we owe you better.

Here's what I'm going to do:

- I'm escalating with UPS today to ask them to move it forward
- If it hasn't shown movement by Friday (5/24), I'll ship you a replacement
  via priority at no charge — you should have it by the following Tuesday
- Either way, here's a $10 store credit for the wait: TROUBLE10

I'll personally follow up on Friday with an update. If anything else comes
up before then, just reply to this email — it comes straight to me.

— Sarah Chen, {{brand_name}}

══════════════════════════════════════════════════
RECOMMENDED ACTION
══════════════════════════════════════════════════
Action: Issue $10 store credit + escalate with UPS + 48-hour follow-up commitment
Rationale: Order is 6 days past estimated arrival. Customer is being measured (no threats, no complaints elsewhere). Small credit + clear escalation + brand-side commitment to follow up earns the relationship. Repeat customer with $340 LTV — worth proactive handling.
Estimated cost: $10 store credit (if used) + ~10 min of buyer's time for the follow-up

══════════════════════════════════════════════════
ORIGINAL TICKET (for reference)
══════════════════════════════════════════════════
Hi - I ordered the River Stone Pour-Over on May 10 and it was supposed
to arrive last week. UPS tracking says it's been sitting in Memphis for
days. Can you let me know what's going on?

Sarah
```

---

## Notes on this exemplar

- **Order context loaded automatically** — the reply references specifics (Memphis, May 12, last scan May 18) without the buyer needing to look them up
- **Sentiment matches the reply tone** — neutral ticket → calm, measured reply (not over-apologetic)
- **Specific action with a timeline** — "if it hasn't moved by Friday, replacement ships Tuesday" beats "we'll look into this"
- **Store credit + commitment to follow up** are both included in the reply AND tracked in the action recommendation with rationale
- **Founder-name sign-off** because the order value + customer LTV warrant personal touch
- **Customer LTV ($340) noted in context** — informs the slightly more generous treatment than a first-time buyer would get
- **Reply is 117 words** — in the target range for shipping delays
