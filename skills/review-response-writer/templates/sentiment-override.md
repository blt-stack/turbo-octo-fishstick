# Sentiment Override Layer

Star rating tells you *what tier of reply* to write. Sentiment tells you *whether to write that reply at all*. Some reviews shouldn't get the standard recovery/clarify/amplify treatment — they need a different response, or no response, or a platform-removal request.

Four sentiment subtypes. Detect early in the pipeline, before drafting.

---

## 1. Constructive (default)

Most reviews. The customer raises a legitimate, specific concern (low star) or shares specific praise (high star). Handle per the standard star-tier template.

**Signals:**
- Specific details about the product / experience
- A real first name (matches purchase records if available)
- Tone is reasonable, even if frustrated
- Complaint is about a thing the brand could plausibly fix

**Handling:** Use the standard tier template. No override needed.

---

## 2. Abusive / unhinged

The review is a personal attack, profanity-laden, or wildly disproportionate to any actual issue.

**Signals:**
- ALL CAPS for entire sentences
- Profanity directed at staff or company
- Personal attacks on individuals
- Wild factual claims with no specifics ("this brand is a scam!" with no order details)
- Threats unrelated to the product (legal threats out of proportion, social media threats, "I'll make sure no one buys from you again")
- Hostile sarcasm throughout

**Handling:**
- Keep the public reply **short** (30-50 words max)
- Be professional, calm, and unprovokable
- **Apologize only for things the brand actually owns** — don't apologize for the customer's tone, don't apologize for things the brand didn't do
- Acknowledge if there's a real underlying issue ("It sounds like your order arrived damaged — please email us")
- Hand off to private channel immediately
- **Do not engage with the personal attack**
- Tag the review for **founder review** before posting

### Abusive reply skeleton

```
Hi [Name],

[If there's a real issue: "It looks like there may be an issue with your order — please email us at hello@brand.com and we'll take care of it."]
[If there's no real issue mentioned: "We're sorry you've had a frustrating experience. Please email us at hello@brand.com so we can understand what happened and make it right."]

— [Name]
```

Future readers will see the abuse + the calm, professional reply. They will overwhelmingly side with the brand. Don't undermine that by matching the tone.

---

## 3. Fake / competitor / suspect

The review is likely not from a real customer. Most platforms allow flagging these for removal.

**Signals (any one is a yellow flag; two+ is red):**
- Generic complaint with no order-specific details ("This is the worst product I've ever bought" with no product name, no use case)
- Reviewer name doesn't match any customer in records
- Reviewer's history shows reviews of competitor products with suspiciously similar phrasing
- Multiple suspect reviews posted in a short window
- Language that reads like a competitor or marketing copy in reverse ("This product fails to do X, unlike its competitors that succeed at X")
- 1★ rating with no review text
- Brand-new account / no other reviews on profile
- Review mentions products the brand doesn't sell
- Review is in a language inconsistent with the buyer's customer base
- Time/date posted is suspicious (3am cluster, all within 10 min of each other)

**Handling:**
- Draft a **platform dispute request** using `dispute-drafts.md` — this is the primary action.
- Only draft a **placeholder public reply** if the buyer wants to post one before/instead of disputing. The placeholder should be even shorter and more neutral than an abusive reply.
- **Do not mine for testimonials or objections.** Fake reviews must not flow into cross-skill caches.
- Tag with `do_not_amplify: true` and `do_not_mine: true` in any cache writes.

### Placeholder reply skeleton (only if buyer wants to post one)

```
Hi [Name],

We don't have a record of an order under this name. If there's a real issue we should address, please email us at hello@brand.com with your order number.

— [Name]
```

This reply makes the fake review look fake to future readers without the brand having to call it fake outright.

### Dispute draft

See `dispute-drafts.md` for the per-platform removal-request templates. The dispute draft goes in the .docx alongside (or instead of) the public reply.

---

## 4. Sycophantic / paid-looking

The review is overly glowing in a way that reads as fake/incentivized, even from the brand's side.

**Signals:**
- Reviewer's history shows a pattern of 5★ reviews across unrelated brands
- Marketing language ("This is a must-have product for any [audience]!")
- Reads like a paid placement (no use case, no specific feature praise, just superlatives)
- Phrasing matches a known incentivized-review platform template
- New account, no other reviews
- Inconsistencies between reviewer claims and product (claims "perfect for my home gym" but product is jewelry)

**Handling:**
- Draft a **low-key public thank-you** that doesn't engage with the suspect content (so the brand isn't endorsing fake reviews)
- **Do not mine for testimonials.** Sycophantic 5★ reviews must not flow into the testimonial cache.
- Tag with `do_not_amplify: true`.
- Note for the buyer: "This 5★ review looks suspect — recommend not featuring it in marketing."

### Sycophantic reply skeleton

```
Hi [Name],

Thank you for the kind words — appreciate you taking the time.

— [Name]
```

Short, polite, generic. Doesn't add narrative weight to a potentially fake positive review.

---

## Detection logic order

When processing each review, apply checks in this order:

1. **Fake/competitor check first** — if flagged, route to dispute draft + skip mining
2. **Abusive check second** — if flagged, route to short professional reply + founder tag
3. **Sycophantic check third** — if flagged (only for 4-5★), route to low-key thank-you + skip testimonial mining
4. **Otherwise: constructive** — route to standard tier template

The skill explains its sentiment classification in the output so the buyer can override. The buyer always has the final call on whether something is fake vs. constructive — the skill flags, doesn't decide.

---

## When the buyer disagrees with the classification

Common cases:

- **Skill flagged as abusive, buyer thinks it's just frustrated**: re-route to standard recovery tier. Acceptable.
- **Skill flagged as fake, buyer thinks it's real**: re-route to standard recovery tier. **But** keep the do_not_mine flag — even if the review is real, mining a hostile complaint into the objection cache is fine; mining vague-complaint text isn't.
- **Skill missed an obvious fake**: buyer can manually re-tag in the .xlsx. The cache write happens after the .xlsx is generated, so re-tagging before export-to-cache prevents bad data from flowing downstream.

---

## False positive cost vs. false negative cost

**False positive on fake/competitor (flagging a real review as fake):** Annoying, but the placeholder reply still works for a real customer. Recoverable.

**False negative on fake/competitor (missing a fake review):** Real reviewer's voice gets diluted by fake content amplified into the testimonial cache, brand looks like it's quoting fake reviews in landing pages. Severe.

**Lean toward flagging when uncertain.** The buyer reviews the .xlsx; they catch false positives quickly. The cost of a false negative is hidden and compounds.
