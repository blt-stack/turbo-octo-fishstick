# Back-in-Stock Flow

When a product is restocked, the waitlist gets notified. Highest-converting email/SMS the brand sends — typically 30-50% open rates and 10-25% conversion rates because the recipient explicitly asked to be notified.

## Flow specs

- **Trigger:** product restocked + customer is on the waitlist for that product
- **Default:** 1 email + 1 SMS over 24 hours
- **Total duration:** ~24 hours (with optional 48-hour follow-up)
- **Goal:** maximize conversion among waitlist subscribers before they lose interest or competitors notify them first

## Prerequisite: a waitlist mechanism

The flow only works if the buyer has back-in-stock waitlist sign-ups enabled (a "notify me when back in stock" button on out-of-stock product pages). Most Shopify themes support this either natively or via apps (Klaviyo's Back in Stock, Notify Me, Restock Rocket, etc.).

The skill flags this as a prerequisite and recommends Klaviyo's native Back-in-Stock feature for best integration.

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | Within 5 minutes of restock | Email + SMS (simultaneously) | "It's back in stock!" |
| 2 | 24 hours later (if not purchased) | Email | "Still available, but going fast" |

Total: 1-2 emails + 1 SMS depending on initial conversion.

---

## Per-step copy patterns

### Step 1: Back-in-stock notification (immediate)

Send email and SMS simultaneously (or within 5 minutes of each other). Speed matters — competitors may have the same customer on a similar waitlist.

**Email subject line patterns:**
- "[Product] is back in stock — yours if you want it"
- "Back: [Product]"
- "Restocked just now — [Product]"

**Email body:**
1. The product (image + name + price + Add to Cart link prominently)
2. Brief acknowledgment ("You waited — thank you")
3. Soft scarcity reminder (only if true): "We typically sell out of this in [X days/hours] after restock"
4. Reassurance about shipping speed
5. Single clear CTA: "Add to cart"

Length: 80-150 words. Brevity matters — the goal is fast conversion, not deep selling.

**SMS body:**
```
[Product] is back in stock at [brand]! Grab yours before it sells out:
[shortlink]. Reply STOP to opt out.
```

### Step 2: Follow-up email (24 hours later, if no purchase)

For waitlist subscribers who got the back-in-stock notice but didn't convert in 24 hours.

**Subject line patterns:**
- "[Product] is still available — for now"
- "Heads up: [Product] is back, going fast"
- "Quick reminder about [Product]"

**Body:**
1. Brief reminder
2. Product image + price + CTA
3. Optional: 1 review from a recent buyer
4. Final CTA

Length: 80-120 words.

After step 2, the waitlist subscription is fulfilled. Customer goes back into the regular program.

---

## Segmentation considerations

- **Filter by waitlist signup date** — if the customer signed up months ago, they may have forgotten. The skill can adapt copy: "Six months ago you asked us to notify you when [Product] came back. It's here."
- **Filter by stock-level remaining** — if very low stock, lean into honest scarcity. If high stock, skip the urgency framing.
- **Filter by customer status** — repeat customers can get a slightly warmer "welcome back to [product]" framing; first-time waitlist subscribers get the standard one.

## A/B test plan

Less testing needed for this flow than others (conversion is so high that A/B test signal is fast and clean). Recommended:

1. **Subject line A/B on step 1** — explicit name vs urgency-led
2. **Email body length** — short vs longer with review
3. **Email-only vs email + SMS** for the initial notification

## Common pitfalls

- **Delayed notification** — sending the back-in-stock notice 1-2 hours after restock kills the flow's effectiveness. Set up the trigger for under 5 minutes.
- **No SMS** — SMS is the highest-conversion channel for back-in-stock because urgency is real.
- **Fake scarcity** — "Only 3 left!" when there are 300 erodes trust permanently.
- **Sending to customers who already bought** — Klaviyo should auto-filter, but verify the setup.

## Performance benchmarks

- Email open rate: 40-60% (highest of any flow)
- Email click rate: 20-35%
- SMS conversion rate: 15-30% (often higher than email for this flow)
- Overall waitlist-to-purchase rate: 25-50% within 48 hours

This flow is often the buyer's first "free money" — waitlists are already opted-in and waiting. Setting it up well is one of the highest-ROI changes a buyer can make.
