# Returns / Refunds / Exchanges — Reply Patterns + Action Recommendations

Policy-driven category. Tone matters more than category-specific cleverness — customers want a clear path forward, not a treatise on the return policy. Don't sound rigid; don't give away the store.

## Sub-types and how to identify them

| Sub-type | Identifier signals |
|---|---|
| **Doesn't fit / wrong size** | Apparel-specific; "size up/down"; "fit issue"; "I usually wear a [size]" |
| **Changed my mind** | "Decided I don't want it"; "no longer need it"; "want to return for refund" |
| **Arrived damaged** | "Broken when it arrived"; "damaged in shipping" — overlaps with defects but treated as return-route |
| **Want to exchange for different color/size** | "Can I swap for the [other variant]"; "got the wrong color" |
| **Late return request** | "It's been more than [N] days"; outside the return window |
| **Lost the return packaging / shipping label** | "Need a new return label"; "lost the box" |
| **Refund status check** | "When will my refund process"; "I returned this 2 weeks ago" |

## Per-sub-type reply patterns + action recommendations

### Doesn't fit / wrong size (apparel)

**Reply pattern:**
```
Hi [name],

Sorry the fit isn't right. Sizing is hard online — totally on us when it
doesn't work.

[Action path]
I can ship you the next size up/down at no extra cost — just keep the original
or donate it (no need to ship it back). Reply with which size you'd prefer
and I'll get it out today.

If you'd rather just have your money back, that works too — let me know and
I'll process the refund within 2 business days.

[Close]
Whichever works for you.

— [Founder name]
```

**Recommended actions:**
- Default: free exchange + tell them to keep/donate the original (saves return-shipping cost on cheap apparel; preserves goodwill)
- For higher-priced apparel (>$80): standard exchange with return label
- For unworn-with-tags items: full refund or exchange, customer's choice
- For worn items: usually case-by-case; brand's discretion

### Changed my mind

**Reply pattern:**
```
Hi [name],

No problem at all. Here's the return process:

1) I'll email you a prepaid return label in the next [X hours]
2) Drop the package at any [carrier] location
3) Once it's scanned in transit, your refund processes automatically
   within [Y business days] to your original payment method

The product needs to be in original condition + unused for a full refund. If
it's been opened/used, we can offer store credit instead — just let me know.

— [Founder name]
```

**Recommended actions:**
- Within return window + unused: full refund per policy
- Within return window + lightly used (depends on category): partial refund or store credit
- Outside window: see "late return request"
- Buyer's policy is the source of truth — skill respects whatever's in `config.store.policies` if set; otherwise asks once

### Arrived damaged

(Cross-listed with defects — see `defects-damages.md` for fuller treatment when the damage is product-related, not shipping-related.)

**Reply pattern:**
```
Hi [name],

I'm so sorry your [product] arrived damaged. That's not OK.

[Resolve fast]
I'm shipping a replacement today via priority — should arrive within
[X business days]. You don't need to send anything back; just dispose of
the damaged one when convenient.

If you'd prefer a refund instead of replacement, let me know and I'll process
that within 2 business days.

— [Founder name]
```

**Recommended actions:**
- Default: reship + no return required (the damaged item isn't recoverable; the return-shipping cost exceeds the item value for most categories)
- For high-value items (>$200): reship + ask for damage photos (for the carrier's insurance claim)
- Add a small credit ($5-15) for the inconvenience

### Exchange for different color/size

**Reply pattern:**
```
Hi [name],

Easy — let me swap that for you.

I'll ship the [requested variant] today via standard shipping. Once you
receive it, drop the original in a box with the included return label
(I'll email it separately) and send it back when convenient.

You won't be charged the difference — straight swap.

— [Founder name]
```

**Recommended actions:**
- Same-price exchange: straight swap, free both directions for "doesn't fit" cases
- Different-price exchange: charge or refund the difference; usually free return shipping
- For items where exchange = waste (perishables, cosmetics, intimate items): full refund, customer keeps the original

### Late return request (outside window)

**Reply pattern:**
```
Hi [name],

I appreciate you reaching out. Our return window is [N] days and your
order shipped on [date], so technically the window closed [X days ago].

That said — I can offer store credit for the value of the order ([$amount]).
You can use it any time, no expiry. Refund-to-original-payment is harder
this far out, but credit's easier on our end and gives you the same
purchasing power.

If that works, just reply yes and I'll set it up. Or if you'd rather not,
no hard feelings.

— [Founder name]
```

**Recommended actions:**
- 1-30 days past window: store credit instead of refund (preserves relationship without setting a policy-defying precedent)
- 30-90 days past window: store credit at a reduced amount (e.g., 80%)
- 90+ days past window: decline gracefully, offer a small discount on future orders
- For high-LTV repeat customers: be more generous (relationship > precedent)

### Refund status check

**Reply pattern:**
```
Hi [name],

Quick update — your return for order #[id] was received on [date]. Refund
of $[amount] processed [date] back to your [payment method]. It typically
takes [3-5] business days to show up on your statement, sometimes longer
depending on your card issuer.

If you don't see it by [date], just reply and I'll dig in.

— [Founder name]
```

**Recommended actions:**
- Lookup status in Shopify or payment processor
- If refund processed: confirm + explain the lag
- If refund not yet processed (sitting in queue): process now + reply
- If return not yet received: explain status + ask if they have the tracking number

### Lost the return packaging / shipping label

**Reply pattern:**
```
Hi [name],

No worries — I'll email you a fresh return label in the next [X hours].

You don't need the original packaging — any clean box that fits the [product]
works fine. Tape the label on, drop it at any [carrier] location.

— [Founder name]
```

**Recommended actions:**
- Resend the label, no friction
- Don't make the customer hunt for the original
- Tracks as "label reissued" so it doesn't accidentally get charged twice

---

## Sentiment overrides for returns

Returns tend toward neutral or slightly negative — customer wants something they have less of. Tone:

| Sentiment | Adjustments |
|---|---|
| Angry | Lead with apology, prioritize speed, longer credit, founder-name sign-off |
| Neutral | Standard pattern |
| Friendly | Match warmth, smaller credit (e.g., $5 instead of $15) since less is needed to repair the relationship |

---

## Common pitfalls in returns replies

- **Hiding behind the return policy** when the brand could be slightly more generous and earn the relationship
- **Charging return shipping on doesn't-fit items** under $50 — the return-shipping cost often exceeds the item value
- **Requiring a return for damaged items** that can't be refurbished — wastes the customer's time and brand's shipping cost
- **Slow refund processing** (more than 3 business days) — kills trust even on otherwise-handled returns
- **No follow-through on store credit offers** — if the brand says "$10 store credit," it needs to actually appear in the customer's account
- **Snippy "as a courtesy" language** — even when the return is outside the window, "as a courtesy this time" reads as passive-aggressive

---

## Buyer's return policy as source of truth

If the buyer has documented their return policy in `config.store.policies` (during onboarding or via a later update), the skill respects it strictly. If not, the skill assumes standard DTC defaults:

- 30-day return window for most categories
- Free returns on first order; customer pays for returns on subsequent orders (or all-free if buyer prefers)
- Full refund to original payment within 5 business days of receipt
- Final-sale items (clearance, custom-made, personalized) excluded
- Cosmetics / supplements / intimate items: return for credit only, sealed-only

Skill flags any policy conflict when it detects the buyer's stated policy diverges from these defaults.
