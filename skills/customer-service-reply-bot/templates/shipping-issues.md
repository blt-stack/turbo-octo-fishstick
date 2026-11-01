# Shipping Issues — Reply Patterns + Action Recommendations

The single highest-volume CS category for most e-commerce stores. Often emotionally charged (customer waiting on a gift, expected delivery missed, etc.). The shipping carrier is often at fault, but the customer doesn't care — they bought from the brand, the brand owns the experience.

## Sub-types and how to identify them

| Sub-type | Identifier signals |
|---|---|
| **Delayed** | Tracking shows shipped but stuck; "where is my order"; "X days late"; order placed N days ago |
| **Lost in transit** | Tracking stalled for 7+ days OR shows delivered but customer doesn't have it; "marked delivered but I don't see it" |
| **Wrong address** | Customer says "I put the wrong address"; or "shipped to my old address"; or address typo visible |
| **Tracking question** | "What's my tracking number"; "is this normal"; "when will it arrive" — customer just wants info |
| **Missing item** | "Box arrived but [item] is missing"; "got my pour-over but no filter"; partial shipment issue |

## Per-sub-type reply patterns + action recommendations

### Delayed

**Reply pattern:**
```
[Acknowledge the wait + name the order]
Hi [name],

I'm so sorry order #[order_id] has been delayed. [Carrier] currently shows
it at [last known location] — it left our fulfillment partner on [ship date]
and should have arrived by now.

[Take ownership]
This isn't the experience we wanted for you.

[Resolve specifically]
Here's what I'm going to do:
- [Specific resolution: e.g., "Reach out to UPS today to escalate the trace"]
- [Followup commitment: "If it hasn't moved by Friday, I'll ship you a
  replacement at no charge"]
- [Optional credit: "And here's a $10 credit for the trouble: code TROUBLE10"]

[Close warmly]
I'll personally follow up by [day]. If anything comes up before then, just
reply to this email — it comes directly to me.

— [Founder name]
```

**Recommended actions:**
- Delay under 3 business days past estimate: no-action reply + offer tracking escalation
- Delay 3-7 days past estimate: $5-15 store credit + escalation commitment + 48-hour followup
- Delay 7+ days past estimate: full refund OR reship at brand's expense (customer chooses); add a $10-20 credit
- Customer-side address issue: politely explain the reship cost (carrier policy), offer to ship to corrected address at discounted shipping rate

### Lost in transit

**Reply pattern:**
```
Hi [name],

I'm sorry your order is showing as [delivered / stalled] but you don't have
it. That's frustrating, and we're going to fix it.

[Resolve]
Two options:
1) I can file a lost-package claim with [carrier] today — they typically
   take 5-7 days to investigate and confirm. If they confirm lost, we'll
   reship at no charge.
2) Or we can skip the claim and reship right now. Slightly faster.

Either way, you'll get your [product]. Which works better for you?

[Close]
Reply with your preference and I'll get it moving today.

— [Founder name]
```

**Recommended actions:**
- Default: reship immediately at brand's expense (filing the claim adds delay; brand absorbs the cost or recovers via carrier insurance later)
- For high-value orders (>$200): file claim simultaneously with reship to recover cost
- For repeat-issue customers (3rd lost-package claim in 12 months): escalate — may be fraud or chronic address issue; investigate before reshipping

### Wrong address (customer error)

**Reply pattern:**
```
Hi [name],

Thanks for catching this — let's get it sorted.

Since the package is already in transit to [old address], here's what I
can do:

If it hasn't shipped yet: I'll update the address on our end at no charge.
Reply with the correct address and I'll fix it within the hour.

If it has shipped (which I'll check now): the package is on its way to the
old address. Options:
1) Try to redirect via the carrier (sometimes works, sometimes doesn't —
   small fee from the carrier, typically $5-15)
2) Wait for delivery to the old address and have them forward it (depends
   on who lives there now)
3) Reship to the new address at our shipping cost ($X), and you get the
   delayed package as a backup if it eventually finds you

What works best?

— [Founder name]
```

**Recommended actions:**
- Not yet shipped: free address update, no charge
- Already shipped: charge reship cost (this is buyer-error), unless brand wants to absorb as a goodwill gesture for repeat customers
- Don't absorb the cost reflexively — over time, customers learn that mistakes are free

### Tracking question

**Reply pattern:**
```
Hi [name],

Easy one — here's your tracking link: [URL]

Latest update: [last known status, e.g., "Out for delivery in [city], should
arrive by end of day"]

If it doesn't show up by [date], just reply to this email and I'll dig in.

— [Founder name]
```

**Recommended actions:**
- No action needed — pure info request
- Brief reply, no apology (nothing to apologize for)
- Quick turnaround beats elaborate reply

### Missing item from shipment

**Reply pattern:**
```
Hi [name],

I'm so sorry the [missing item] wasn't in your shipment. That's our error,
not yours.

I'm shipping a [missing item] today via priority — you should have it within
[X business days].

You don't need to send back anything. And here's $10 credit for the hassle:
[code]

— [Founder name]
```

**Recommended actions:**
- Reship the missing item at brand's expense (priority/expedited shipping)
- Add small credit ($5-15) for the inconvenience
- For valuable missing items (>$100): also include a personal phone-call or video-message follow-up if the buyer can do it
- Flag the fulfillment partner internally — multiple missing-item reports point to a packing issue

---

## Sentiment overrides for shipping issues

Shipping tickets skew toward angry (the customer's been waiting). Tone adjustments:

| Sentiment | Adjustments |
|---|---|
| Angry | More direct apology, faster action (don't ask for permission — just refund/reship), longer credit, founder-name sign-off |
| Neutral | Standard pattern works |
| Friendly | Match the warmth, small extra (e.g., free shipping on next order) as a thank-you for patience |

---

## Common pitfalls in shipping replies

- **Blaming the carrier** ("UPS dropped the ball") — true but customers don't care. The brand owns the experience.
- **Hiding behind policy** ("Per our shipping disclaimer...") — kills relationships even when technically correct.
- **No specific timeline** ("We'll look into this") — open-ended commitments don't reassure.
- **Asking the customer to do the work** ("Can you check with your mail carrier...") — customer's already done that. The brand should be the one doing the chasing.
- **Generic apologies** ("So sorry for the inconvenience") — empty. Be specific about what went wrong.
- **No name on the sign-off** ("The Support Team") — depersonalizes; customers respond better to a real name.

---

## Auto-detected systemic issues

When the batch mode processes 5+ shipping tickets in one run, the skill flags patterns in Sheet 3 of the .xlsx:

- **Same carrier in 50%+ of complaints:** the carrier is the systemic problem; consider switching
- **Same fulfillment region in 50%+ of complaints:** that region has a fulfillment partner issue
- **Same product in 30%+ of complaints:** that product is shipping in inadequate packaging or sustaining transit damage
- **Same address mistype pattern:** the checkout form may be allowing typos that should be caught

These show up as "recommended process changes" so the buyer fixes the root cause rather than just replying forever.
