# RFQ + Quote Comparison Methodology

Comparison bulk mode is the answer to "I want to send the same ask to 4-8 suppliers and compare their replies." It's the actual sourcing workflow for solo operators, not just "draft multiple letters."

## When to use comparison bulk

| Scenario | Comparison bulk fits? |
|---|---|
| First-time sourcing for a new product | Yes — comparing 4-8 quotes is standard |
| Switching suppliers due to quality issues | Yes — comparing alternates side-by-side |
| Annual price re-bid for existing supplier | Yes — keep current supplier in the comparison + 2-3 alternates |
| Routine reorder to existing supplier | No — single mode |
| Dispute or sample request | No — those are single mode |

## The workflow

1. Buyer defines the RFQ:
   - Product description + spec sheet
   - Target quantity (e.g., 1500 units)
   - Target lead time
   - Target unit price (optional)
   - Shipping terms expectation (FOB / EXW / DDP / DDU)
   - Sample requirements
2. Buyer provides the supplier list (N suppliers — typically 4-8):
   - Company name + contact + region for each
3. Skill drafts a tailored letter to each supplier:
   - Same RFQ content
   - Region-appropriate tone per supplier's region
   - Relationship-stage-aware (if some are known suppliers, others new)
   - Subject line consistent across all
4. Skill renders the .xlsx with:
   - Sheet 1: Outreach Queue (one row per supplier with letter draft + status)
   - Sheet 2: Quote Comparison (auto-populates when buyer fills in replies)
   - Sheet 3: Supplier Memory Updates
   - Sheet 4: Negotiation Tactics Reference
5. Buyer sends each letter
6. As replies arrive, buyer fills in the Quote Response columns in Sheet 1
7. Sheet 2 auto-calculates total landed cost + ranks suppliers

## The RFQ letter

The RFQ letter is a hybrid of pricing-tier + sample-request asks. Structure:

```
Subject: [Brand] RFQ: [product name] / [target quantity]

Dear [Supplier-specific opener — uses region/stage memory],

[Region-appropriate bridge — for new suppliers: brief intro of brand; for known suppliers: reference prior orders]

We're sourcing [product] for our [season / launch / line]. Our planning specs:

- Product: [name + brief spec]
- Target quantity: [N] units (initial order)
- Annual volume potential: [X] units
- Target lead time: [Y] days from PO
- Shipping: [FOB / EXW / DDP] to [destination]
- Sample: [we'd like 2-3 samples to evaluate before placing the production order]
- Target launch date: [date]

We're requesting quotes from a small set of qualified suppliers. We'd appreciate your quote on:

- Unit price at the [N]-unit volume
- Lead time from deposit to ready-to-ship
- Sample cost and shipping
- Payment terms you can offer
- Any volume tiers above [N] that would change the pricing

[Region-appropriate mutual-benefit framing]

[Close — request for response by specific date]

Best regards,
[Buyer name]
[Brand]
```

The skill tailors the opener / bridge / mutual-benefit framing per supplier's region and relationship stage, but the RFQ content (the specs) is identical across all supplier letters — that's what makes them comparable.

## Quote comparison — what to capture

When replies come in, the buyer fills the Quote Response columns:

| Column | What goes here |
|---|---|
| MOQ offered | Supplier's actual MOQ for this product (may differ from target) |
| Unit price quoted | At the target quantity |
| Lead time quoted | Days from deposit to ready-to-ship |
| Payment terms offered | E.g., "30/70 TT, balance before shipping" |
| Shipping terms | FOB / EXW / DDP |
| Sample cost | Per-sample cost in USD |
| Sample availability | "Ready to ship" / "Custom — 14 days" |
| Lead time at higher volume | Often shorter at higher volume (helpful signal) |
| Quote validity | How long the price is good for |
| Notes from supplier | Anything else the supplier said |
| Quote received date | When the reply came in |

## Total landed cost calculation

Sheet 2 calculates:

```
unit_price * quantity                       (= base cost)
+ shipping_estimate                          (per FOB → destination; skill estimates)
+ duty_estimate                              (per origin country + product HS code; skill estimates)
+ sample_cost                                (factored in proportionally if sample-credit applies)
─────────────────────────────────────────
= total_landed_cost
total_landed_cost / quantity                 (= effective per-unit landed cost)
```

Suppliers ranked by per-unit landed cost. The lowest landed cost isn't always the answer — but the comparison surfaces tradeoffs.

## Quality factors not in the spreadsheet

The comparison sheet captures hard numbers. Soft factors that matter but aren't in the calc:

- Communication speed during quoting (a slow-to-quote supplier is often a slow-to-respond-to-problems supplier)
- Quality of the supplier's questions back ("Are these dimensions critical to ±1mm?" signals attention; no questions signals indifference)
- Sample turnaround
- Existing relationship vs. cold supplier
- Supplier's request for additional info (engagement signal)
- Red flags (unusually low price, evasive answers, push-back on payment terms)

Sheet 4 (Negotiation Tactics Reference) flags these patterns for the buyer.

## Negotiation tactics reference (Sheet 4 contents)

The reference card surfaces:

### Red flags in quotes
- Unit price significantly below the cluster (e.g., 30% below the average) → quality risk; ask hard questions
- "Free samples" offer from a brand-new supplier on a custom product → likely doesn't have the capability
- Refusal to give a quote validity period → not serious
- Confused replies about basic specs → factory may not actually make this product

### When to counter-negotiate
- Lowest landed-cost supplier is also the slowest replier → push for faster lead time as a condition of award
- Multiple suppliers cluster around the same price → ask each for tier breakdowns; one will reveal more
- One supplier is significantly faster than the others → leverage for tighter lead time

### Awarding the contract
- Don't announce the loser publicly — keep declining letters short and respectful (you may want them next year)
- The skill drafts a "thank you, we've selected another supplier this time" follow-up letter
- The skill recommends keeping non-selected suppliers in the memory cache for future RFQs

## Decline letter pattern

When the buyer awards to one supplier, the skill drafts decline letters to the others:

```
Subject: Re: [original RFQ subject] — update

Dear [Supplier],

Thank you for your detailed quote on [product]. We've reviewed all the responses and have decided to move forward with another supplier this time.

We appreciated [specific positive about their quote — lead time, communication, etc.] and would like to keep you in mind for [future product / upcoming categories]. We'd value the chance to work together on a future project.

If you'd be open to it, we'd appreciate keeping the door open for future quotes.

Best regards,
[Buyer name]
```

The decline letter preserves the relationship for future RFQs. Many suppliers will remember a respectful decline letter for years.

## How long the RFQ process takes

Typical timeline:
- Day 0: send RFQ to N suppliers
- Day 3-5: first quotes arrive (faster regions: NA, Indian); China usually 5-7 days
- Day 7-10: all quotes arrived (assume some require nudges)
- Day 10-14: buyer fills in Sheet 2, reviews comparison, asks clarifying questions
- Day 14-21: buyer awards to one supplier and sends decline letters

The skill recommends 21 days end-to-end for a standard RFQ. Compressed timelines (under 10 days) are possible but reduce the depth of quotes — suppliers reading "respond by tomorrow" will send shallow quotes.

## Edge cases

- **Mixed regions in one RFQ**: handled — each letter is tailored to its supplier's region while keeping the RFQ specs identical
- **One supplier is established + the others are new**: handled — the established supplier's letter references the relationship; new-supplier letters introduce the brand
- **Supplier asks for more info before quoting**: not the skill's job to manage the back-and-forth; the buyer takes over after the initial letter
- **Supplier counters with a different product variant**: log in the Quote Comparison sheet's Notes; consider whether the alt product meets the brand standard
- **All suppliers come in above target price**: skill recommends a second round with a revised RFQ acknowledging the price reality
