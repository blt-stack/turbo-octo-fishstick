# Single Defect Ticket — Reference Example

Fictional customer used to show structure. Never reproduce verbatim.

**Scenario:** Customer Marcus emails {{brand_name}} the day his order arrives. The pour-over cracked in transit. He's angry — caps, exclamation marks, threat to leave a public review.

---

## Original ticket

```
From: Marcus T. <marcus.t@email.com>
Subject: BROKEN ON ARRIVAL
Received: 2026-05-22 11:08

I just opened my order and the ENTIRE THING IS CRACKED. The pour-over
arrived in PIECES. I paid $48 for this and got a box of broken ceramic.
This is RIDICULOUS. I want a full refund IMMEDIATELY and I'm going to be
leaving a review about this on Trustpilot if it's not handled today.

Marcus
```

---

## Detected categorization

- **Category:** Defects / damages
- **Sub-type:** Broken on arrival (BOA)
- **Sentiment:** Angry (ALL CAPS in subject + body, exclamation marks, "RIDICULOUS," explicit threat of Trustpilot review)
- **Public-complaint risk:** HIGH (Trustpilot threat is explicit)
- **Order context:** Fetched from Shopify — Order #1042, placed May 18, delivered today (May 22)

---

## .docx output structure

```
Reply to: Marcus T.
Received 2026-05-22 11:08 · Category: Defects/Damages — Broken on Arrival (BOA)
Sentiment: angry
Reasoning: ALL CAPS in subject + body, multiple exclamation marks, "RIDICULOUS," explicit Trustpilot threat.

══════════════════════════════════════════════════
ORDER CONTEXT
══════════════════════════════════════════════════
Order: #1042
Placed: 2026-05-18
Shipped: 2026-05-19
Status: delivered (2026-05-22)
Tracking: UPS 1Z9999A2C45678901

Products in order:
  • 1 × River Stone Pour-Over — Cream — $48.00

Order total: $52.00 (includes $4 shipping)
Customer LTV: $48.00 (first-time customer)

⚠ PUBLIC-COMPLAINT RISK: HIGH
Customer explicitly threatens Trustpilot review.

══════════════════════════════════════════════════
DRAFTED REPLY
══════════════════════════════════════════════════
Subject: Re: BROKEN ON ARRIVAL

Body:

Hi Marcus,

I'm so sorry. Opening a brand-new pour-over and finding it shattered is
exactly the experience we work hard to prevent — and we failed you on
this one.

Here's what I'm doing right now:

- Full refund of $52 processed today — back on your card within 2 business
  days
- A replacement pour-over (same cream colorway) ships today via priority,
  free — should arrive by Tuesday
- A $20 store credit for the trouble, no expiry: APOLOGIES20

You don't need to send the broken one back; please just dispose of the
pieces. If you can send a quick photo of the damage (just so we can file
with UPS), that would help, but no pressure either way.

I'm taking this personally — would you give us a chance to make this right
before the public review? Either way, I appreciate you flagging it, and
you have my direct line: this email comes straight to me.

— Sarah Chen, Founder, {{brand_name}}

══════════════════════════════════════════════════
RECOMMENDED ACTION
══════════════════════════════════════════════════
Action: Full refund + free replacement + $20 store credit + founder personal reply
Rationale: BOA on first-time customer order with explicit Trustpilot threat. The cost of over-delivering (~$70 in refund + replacement + credit value) is much less than the risk of a negative public review on a brand-new customer. Founder sign-off + the soft "give us a chance" ask gives the customer dignity in choosing to retract the threat. Even if they post the review anyway, the resolution speaks for itself.
Estimated cost: $52 (refund) + $4 (replacement shipping) + ~$15 (credit if used) = ~$71. Risk-adjusted value: protects against potential $500-2,000 in lost LTV from public review.

══════════════════════════════════════════════════
ORIGINAL TICKET (for reference)
══════════════════════════════════════════════════
I just opened my order and the ENTIRE THING IS CRACKED. The pour-over
arrived in PIECES. I paid $48 for this and got a box of broken ceramic.
This is RIDICULOUS. I want a full refund IMMEDIATELY and I'm going to be
leaving a review about this on Trustpilot if it's not handled today.

Marcus
```

---

## Notes on this exemplar

- **Sentiment correctly tagged angry** — drives the more apologetic tone, faster action, founder-name sign-off
- **Public-complaint risk flagged** — high-risk tickets warrant over-delivery (refund + replacement + credit, not just one of those)
- **Reply opens with the apology** — angry customers want to feel heard before they hear about the fix
- **Action list is concrete** — refund processed, replacement shipping, credit issued; no "we'll look into this"
- **Photo request is OPTIONAL and AFTER committing** to the fix — never make the angry customer prove their case before fixing
- **The "give us a chance" soft ask** is gentle, not manipulative — gives the customer dignity to retract the review threat without losing face
- **Founder name + "comes straight to me"** depersonalizes the corporate tone; angry customers don't want "the team"
- **Rationale explicitly does the risk math** — $71 spent prevents $500-2,000 in LTV risk. The buyer sees why over-delivering is the financially-correct call.
- **Reply is 195 words** — longer than a typical shipping reply because angry + defect needs more reassurance, but still tight
