# Post-Purchase Flow

The Post-Purchase flow does more than confirm an order — it deepens the customer relationship in the first weeks after purchase, which determines whether they become a repeat customer (worth 2-7x their first order over their lifetime). Most stores fire off a single "Thanks for your order!" and leave the relationship to chance.

## Flow specs

- **Trigger:** customer places an order
- **Default:** 4 emails + 2 SMS over 30 days
- **Total duration:** ~30 days (last touch is at day 30, just before the next predictable purchase cycle)
- **Goal:** delight the customer, drive a review, set up the second purchase

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | Immediate | Email | Order confirmation (Klaviyo can use Shopify's default; this skill builds a branded version) |
| 2 | Day of shipment | SMS | Shipping notification + tracking link |
| 3 | 3 days after delivery | Email | "Are you enjoying it?" — engagement + soft review request |
| 4 | 14 days after delivery | Email | Review request (formal) + content |
| 5 | 21 days after delivery | SMS | Replenishment / cross-sell tease |
| 6 | 30 days after delivery | Email | Loyalty / next purchase invitation |

Total: 4 emails (1, 3, 4, 6) + 2 SMS (2, 5).

---

## Per-step copy patterns

### Step 1: Order confirmation email (immediate)

Klaviyo can pass through Shopify's default order confirmation, but a branded version dramatically improves the first impression. This email gets 70-90% open rates — the highest of any e-commerce email.

**Subject line patterns:**
- "Order confirmed — thanks, [first name]"
- "Your [brand] order is in"
- "Your [hero product] is on its way"

Avoid:
- Generic "Order #12345 confirmed" (Shopify's default — feels transactional)

**Preview text patterns:**
- "Here's what's coming and when."
- "Order #[number] · ships in 2 business days"

**Body structure:**
1. Warm thank-you in brand voice (one sentence, not paragraphs)
2. Order summary (Klaviyo's order-items block — products, quantities, prices, total)
3. Shipping address + estimated delivery window
4. Order management links (track, modify, contact us)
5. Brief brand voice sign-off
6. Optional: pre-tease of the next step ("we'll text you when it ships")

**Length target:** 150-300 words plus the order details.

### Step 2: Shipping notification SMS (day of shipment)

SMS hits hardest here — customers want shipping updates fast.

**Pattern:**
```
[brand] - Your order #[number] just shipped. Tracking: [shortlink]. Should
arrive [date]. Reply STOP to opt out.
```

If the buyer doesn't use SMS, this becomes an email instead. Most buyers should be using SMS at this step.

### Step 3: Engagement check-in email (3 days after delivery)

This is the "soft" touch — checks in without yet asking for the review. Builds trust + identifies unhappy customers before they leave a bad review.

**Subject line patterns:**
- "How's the [product] treating you?"
- "Just checking in — how's [product] so far?"
- "Three days in. What's the verdict?"

**Body structure:**
1. Friendly opener referencing the product they bought
2. One question to invite reply ("How's it going?")
3. Reassurance about returns/issues ("If anything's off, just reply — we'll take care of it")
4. Use-case content — "While you're getting to know your [product], here's a tip..." (a use case, a styling idea, a recipe, a care tip)
5. Soft close: no hard CTA, just an invitation to reach out

This email rarely converts directly — its purpose is relationship + signal. Customers who reply with negative feedback get routed to customer service before they write a public review. That's the real win.

### Step 4: Review request email (14 days after delivery)

By day 14, the customer has had two weeks with the product — enough to form a genuine opinion. Earlier review requests get fewer responses and less-substantive reviews.

**Subject line patterns:**
- "Two weeks with your [product]. How's it going?"
- "Mind sharing what you think?"
- "Your [product] review — and a thank-you"

**Body structure:**
1. Brief context: "It's been two weeks since your [product] arrived"
2. The ask: "If you have 60 seconds, leaving a review really helps us"
3. Direct link to the review form (deep-link to the specific product's review page)
4. Soft incentive: "We send everyone who reviews a [small reward — sticker pack, discount code, entry into a giveaway]" — only if the buyer offers this
5. Brief sign-off

**Length target:** 100-200 words. Don't over-explain.

### Step 5: Replenishment / cross-sell SMS (21 days after delivery)

SMS works for this kind of "we noticed you'd be running low" nudge.

For consumable products (skincare, supplements, food, candles):

```
Hey [first name], it's been 3 weeks since your [product] arrived. Most
people get a 30-day supply — restock here when you're ready: [shortlink].
Reply STOP to opt out.
```

For non-consumable products (apparel, kitchen tools, decor), shift to cross-sell:

```
Loved your [product]? Customers often grab a [complementary product] next:
[shortlink]. Reply STOP to opt out.
```

The skill picks the right framing based on `config.store.primary_category`.

### Step 6: Loyalty / next purchase email (30 days after delivery)

By day 30, the customer is at the decision point about whether to repurchase. This email opens that door.

**Subject line patterns:**
- "One month in. What's next?"
- "We saved you a spot in our customer-only collection"
- "Welcome to the [brand] regulars"

**Body structure:**
1. Reference the past purchase
2. Acknowledge they're now a customer, not a stranger (different tone from the first email)
3. Curated recommendations — 2-3 products picked based on their first purchase (use Klaviyo's predictive cross-sell block or buyer's manual curation)
4. Optional loyalty-program intro if the brand has one (typically 50-100 word explanation)
5. Clear next-step CTA

This email transitions the customer out of the Post-Purchase flow and back into the normal marketing program — but with a "customer" label, not "subscriber."

---

## Segmentation considerations

Post-Purchase has rich segmentation opportunities:

- **Order value tier:** higher-value first orders get the longer / more personal flow
- **Product category:** Replenishment timing differs (supplements = 30 days, candles = 60 days, apparel = N/A)
- **First-time vs repeat customer:** repeat customers can skip the "welcome to the brand" framing in step 1 and get a "thanks for coming back" instead
- **Subscriber status before purchase:** customers who were already subscribers can skip the engagement-building emails (they already know the brand)

### Replenishment timing per category

The skill recommends per-category timing for step 5:

| Category | Replenishment SMS at |
|---|---|
| Supplements | 25-28 days |
| Skincare (single product) | 45 days |
| Skincare (full routine) | 60 days |
| Coffee / tea (subscription-suitable) | 21 days |
| Pet food | days = (bag weight × portion factor) |
| Apparel | N/A — skip to cross-sell |
| Home decor | N/A — skip to cross-sell |
| Kitchen tools | N/A — skip to cross-sell |

Read `segmentation-logic.md` for the Klaviyo filter syntax.

---

## A/B test plan

1. **Subject line A/B on step 3** — most engagement leverage. Casual vs check-in vs question-led.
2. **Review request incentive on step 4** — with vs without small reward.
3. **Send delay on step 4** — 14 days vs 10 days vs 21 days.
4. **Cross-sell vs replenishment framing on step 5** for borderline categories.

---

## Common pitfalls

- **Skipping the engagement email (step 3)** — buyers leave bad reviews because they're frustrated and nobody asked. Step 3 catches them.
- **Asking for the review too early** — day 3 review requests get fewer responses than day 14.
- **Generic order confirmations** — Shopify's default works but feels transactional. Branded version improves brand perception.
- **No SMS leg for shipping** — customers expect shipping updates by SMS; not having them feels antiquated.
- **One-size-fits-all** — a $300 first order should get a more personal flow than a $30 first order.
- **Stopping at step 4** — the loyalty/next-purchase email (step 6) drives second-purchase rates 20-30% higher than not sending it.

---

## Performance benchmarks

- Step 1 open rate: 70-90% (Klaviyo benchmark for branded order confirmations)
- Step 3 open rate: 35-55%
- Step 4 review-submission rate: 8-20% of recipients
- Step 6 conversion (second purchase within 30 days of email): 5-12%
- Overall flow contribution to lifetime value: 15-30% lift vs no Post-Purchase flow
