# Browse Abandonment Flow

Often the second-highest-revenue flow in an e-commerce email program, after Abandoned Cart. Triggers when a subscriber viewed a product page but didn't add to cart. The browsing signal is softer than cart-add, so the flow is gentler — but with the right copy, browse abandonment recovery rates can hit 3-7% of triggered subscribers.

## Flow specs

- **Trigger:** subscriber views a product page (and the email/cookie identifies them as a known subscriber), doesn't add to cart within 1 hour
- **Default:** 2 emails + 1 SMS over 48 hours
- **Total duration:** ~48 hours
- **Goal:** bring the subscriber back to the product, lower the consideration friction

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | 4 hours after browsing | Email | "Still thinking about [product]?" — soft re-engagement |
| 2 | 24 hours after browsing | SMS | Mobile nudge with product link |
| 3 | 48 hours after browsing | Email | Address the friction + add social proof |

Total: 2 emails (steps 1, 3) + 1 SMS (step 2).

---

## Per-step copy patterns

### Step 1: Soft re-engagement email (4 hours)

Browse abandonment is gentler than Abandoned Cart — the subscriber didn't commit to anything. Don't sound like you're tracking them.

**Subject line patterns:**
- "Still thinking about [product]?"
- "Want a closer look at [product]?"
- "Things to know about [product]"

**Preview text:**
- "We pulled together some details that might help."
- "[Product] · [Price] · here's what makes it different"

**Body structure:**
1. Light opener referencing the product
2. The product image + name + price
3. 3 specific reasons people choose this product (from product reviews / brand voice / category positioning)
4. CTA: "See more about [product]" (links to PDP, not directly to checkout)
5. Soft sign-off

**Length:** 100-200 words.

### Step 2: SMS nudge (24 hours)

```
Hey [first name], you were checking out [product] yesterday. Still curious?
Here it is: [shortlink]. Reply STOP to opt out.
```

### Step 3: Friction-addressing email (48 hours)

If the subscriber still hasn't converted, add social proof + address the most likely reason they didn't add to cart.

**Subject line patterns:**
- "What people are saying about [product]"
- "Worth knowing before you decide on [product]"
- "[Product] reviews — and one question"

**Body structure:**
1. 2-3 customer reviews of the specific product (Klaviyo's review block)
2. Address the most likely friction (sizing, shipping, returns, materials) with one specific reassurance
3. Optionally: a complementary product the customer might prefer
4. CTA: "See [product]"

After step 3, the subscriber goes back into the general email program.

---

## Segmentation considerations

- **Filter out subscribers who have already purchased the product** (avoid the awkward "still thinking?" to someone who already bought)
- **Filter out subscribers currently in an Abandoned Cart flow** (Abandoned Cart wins — don't double up)
- **For high-ticket products ($150+):** extend the flow to 3 emails + 1 SMS, since consideration takes longer

---

## A/B test plan

1. **Subject line A/B on step 1** — "Still thinking" vs "Want a closer look" vs product-specific question
2. **Send delay on step 1** — 4 hours vs 8 hours vs 24 hours
3. **Step 3 friction angle** — depends on category

---

## Common pitfalls

- **Treating browse abandonment like cart abandonment** — way too aggressive
- **Not setting up the trigger correctly** — Browse Abandonment requires identified subscribers (cookie or logged-in). Anonymous browsers can't be retargeted via email.
- **Sending Browse Abandonment to all category pages** — should fire on specific product pages only

---

## Performance benchmarks

- Step 1 open rate: 30-45%
- Step 1 click rate: 5-10%
- Overall flow conversion: 3-7% of triggered subscribers
- Revenue contribution: 3-8% of store revenue
